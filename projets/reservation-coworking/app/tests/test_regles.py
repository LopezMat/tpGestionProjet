import inspect
from datetime import date, datetime

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from reservation import horloge, regles
from reservation.regles import ReglePasRespectee

# Lundi 2026-11-30 ; mardi 12-01 ; vendredi 12-04 ; samedi 12-05 ; dimanche 12-06.
LUNDI = date(2026, 11, 30)


def _t(jour: date, h: int = 0, m: int = 0) -> datetime:
    return datetime(jour.year, jour.month, jour.day, h, m, tzinfo=horloge.FUSEAU)


@pytest.mark.parametrize(
    "jour,heure",
    [(LUNDI, 8), (LUNDI, 19), (date(2026, 12, 4), 12), (date(2026, 12, 4), 19)],
)
def test_creneaux_valides(jour, heure):
    regles.verifier_creneau_valide(jour, heure)


@pytest.mark.parametrize(
    "jour,heure,extrait",
    [
        (LUNDI, 7, "8 h à 20 h"),
        (LUNDI, 20, "8 h à 20 h"),
        (LUNDI, 21, "8 h à 20 h"),
        (date(2026, 12, 5), 10, "lundi au vendredi"),
        (date(2026, 12, 6), 10, "lundi au vendredi"),
    ],
)
def test_creneaux_refuses(jour, heure, extrait):
    with pytest.raises(ReglePasRespectee, match=extrait):
        regles.verifier_creneau_valide(jour, heure)


def test_douze_creneaux_par_jour():
    valides = []
    for h in range(24):
        try:
            regles.verifier_creneau_valide(LUNDI, h)
            valides.append(h)
        except ReglePasRespectee:
            pass
    assert len(valides) == 12


def test_avance_bornes():
    now = _t(LUNDI, 7)
    regles.verifier_avance(date(2026, 12, 14), now)  # J+14
    with pytest.raises(ReglePasRespectee, match="14 jours"):
        regles.verifier_avance(date(2026, 12, 15), now)  # J+15


@pytest.mark.parametrize(
    "now,jour,heure,refuse",
    [
        (_t(LUNDI, 9, 59), LUNDI, 10, False),
        (_t(LUNDI, 10, 0), LUNDI, 10, True),
        (_t(LUNDI, 10, 30), LUNDI, 10, True),
        (_t(LUNDI, 12), LUNDI, 8, True),
        (_t(LUNDI, 23, 59), date(2026, 12, 1), 8, False),  # avant minuit, lendemain
        (_t(date(2026, 12, 1), 0, 0), LUNDI, 19, True),  # minuit passé, veille
        (_t(date(2026, 12, 4), 19, 59), date(2026, 12, 7), 8, False),  # semaine suivante
        (_t(date(2026, 12, 7), 8, 0), date(2026, 12, 4), 19, True),  # semaine précédente
    ],
)
def test_creneau_commence(now, jour, heure, refuse):
    if refuse:
        with pytest.raises(ReglePasRespectee, match="déjà commencé"):
            regles.verifier_pas_commence(jour, heure, now)
    else:
        regles.verifier_pas_commence(jour, heure, now)


@pytest.mark.parametrize("n,refuse", [(0, False), (1, False), (2, True), (3, True)])
def test_quota(n, refuse):
    if refuse:
        with pytest.raises(ReglePasRespectee, match="2 réservations"):
            regles.verifier_quota(n)
    else:
        regles.verifier_quota(n)


def test_reservation_annulee_ne_compte_plus():
    # Le module reçoit le nombre de réservations actives : 2 réservations dont 1 annulée = 1.
    statuts = ["active", "annulee"]
    regles.verifier_quota(sum(1 for s in statuts if s == "active"))


@pytest.mark.parametrize(
    "jour,heure,now,actives,extrait",
    [
        (LUNDI, 10, _t(LUNDI, 7), 0, None),
        (date(2026, 12, 5), 10, _t(LUNDI, 7), 0, "lundi au vendredi"),
        (LUNDI, 10, _t(LUNDI, 10), 0, "déjà commencé"),
        (date(2026, 12, 15), 10, _t(LUNDI, 7), 0, "14 jours"),
        (LUNDI, 10, _t(LUNDI, 7), 2, "2 réservations"),
    ],
)
def test_verifier_reservation(jour, heure, now, actives, extrait):
    if extrait is None:
        regles.verifier_reservation(jour, heure, now, actives)
    else:
        with pytest.raises(ReglePasRespectee, match=extrait):
            regles.verifier_reservation(jour, heure, now, actives)


@pytest.mark.parametrize(
    "now,accueil,refuse",
    [
        (_t(LUNDI, 9, 59), False, False),
        (_t(LUNDI, 10, 0), False, True),
        (_t(LUNDI, 10, 30), False, True),
        (_t(LUNDI, 10, 0), True, False),
        (_t(LUNDI, 10, 59), True, False),
        (_t(LUNDI, 11, 0), True, True),
    ],
)
def test_annulation(now, accueil, refuse):
    if refuse:
        with pytest.raises(ReglePasRespectee):
            regles.verifier_annulation(LUNDI, 10, now, est_accueil=accueil)
    else:
        regles.verifier_annulation(LUNDI, 10, now, est_accueil=accueil)


@pytest.mark.parametrize(
    "aujourdhui,attendue",
    [
        (date(2026, 11, 25), date(2025, 11, 25)),
        (date(2028, 2, 29), date(2027, 2, 28)),
        (date(2024, 2, 29), date(2023, 2, 28)),
        (date(2027, 3, 1), date(2026, 3, 1)),
    ],
)
def test_date_limite_purge(aujourdhui, attendue):
    assert regles.date_limite_purge(aujourdhui) == attendue


@pytest.mark.parametrize(
    "aujourdhui,creneau,purgee",
    [
        (date(2026, 11, 25), date(2025, 11, 24), True),  # 12 mois et 1 jour
        (date(2026, 11, 25), date(2025, 11, 25), False),  # exactement 12 mois : conservée
        (date(2026, 11, 25), date(2025, 12, 26), False),  # 11 mois et 29 jours
        (date(2028, 2, 29), date(2027, 2, 27), True),
        (date(2028, 2, 29), date(2027, 2, 28), False),
    ],
)
def test_purge(aujourdhui, creneau, purgee):
    assert regles.doit_etre_purgee(creneau, aujourdhui) is purgee


def test_horloge_paris_et_injection():
    n = horloge.maintenant()
    assert n.utcoffset() is not None
    assert str(n.tzinfo) == "Europe/Paris"

    app = FastAPI()

    @app.get("/h")
    def h(hl=Depends(horloge.fournir_horloge)):
        return {"t": hl().isoformat()}

    fixe = _t(LUNDI, 10)
    app.dependency_overrides[horloge.fournir_horloge] = lambda: (lambda: fixe)
    assert TestClient(app).get("/h").json() == {"t": fixe.isoformat()}


def test_regles_nappellent_pas_lhorloge(monkeypatch):
    def interdit():
        raise AssertionError("horloge appelée")

    monkeypatch.setattr(horloge, "maintenant", interdit)
    regles.verifier_reservation(LUNDI, 10, _t(LUNDI, 7), 0)
    source = inspect.getsource(regles)
    assert "now(" not in source and "horloge" not in source.replace("l'horloge", "")
