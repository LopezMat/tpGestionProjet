"""T-054 : GET /api/salles et GET /api/disponibilites (lecture seule, provisoirement publiques).

Les tests d'intégration exigent TEST_DATABASE_URL (PostgreSQL jetable, voir README). Leur
fixture ne supprime pas le schéma : elle migre (idempotent) et ne vide que `reservation`
et `utilisateur`.
"""

import os
import time
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from reservation import bdd, config, migrer
from reservation.app import creer_app
from reservation.horloge import FUSEAU, fournir_horloge

URL_TEST = os.environ.get("TEST_DATABASE_URL")
integration = pytest.mark.skipif(not URL_TEST, reason="TEST_DATABASE_URL non renseignée")

# Mardi 2026-12-01, 10 h 30 à Paris. J+14 = mardi 2026-12-15.
MAINTENANT = datetime(2026, 12, 1, 10, 30, tzinfo=FUSEAU)
MOTS_PERSONNELS = ("nom_membre", "email", "utilisateur", "@", "reservation_id", "mot_de_passe")


def _client(horloge=MAINTENANT):
    app = creer_app()
    app.dependency_overrides[fournir_horloge] = lambda: (lambda: horloge)
    return TestClient(app, base_url="http://localhost")


@pytest.fixture
def client():
    return _client()


@pytest.fixture
def base(monkeypatch):
    assert URL_TEST
    nom = URL_TEST.rsplit("/", 1)[-1].split("?")[0]
    assert "test" in nom, "TEST_DATABASE_URL doit désigner une base jetable (nom contenant test)"
    monkeypatch.setenv("DATABASE_URL", URL_TEST)
    bdd.moteur_applicatif.cache_clear()
    moteur = create_engine(config.convertir_url_base(URL_TEST))
    assert migrer.appliquer() is True or migrer.appliquer() is False
    _vider(moteur)
    yield moteur
    _vider(moteur)
    moteur.dispose()
    bdd.moteur_applicatif.cache_clear()


def _vider(moteur):
    with moteur.begin() as c:
        c.execute(text("DELETE FROM reservation"))
        c.execute(text("DELETE FROM utilisateur"))


def _reserver(moteur, salle, jour, heure, email="secret.membre@exemple.fr", nom="Nom Secret"):
    with moteur.begin() as c:
        uid = c.execute(
            text("INSERT INTO utilisateur (nom,email,mot_de_passe_hash,role) "
                 "VALUES (:n,:e,'h','membre') ON CONFLICT (email) DO UPDATE SET nom=:n "
                 "RETURNING id"), {"n": nom, "e": email}).scalar()
        c.execute(
            text("INSERT INTO reservation (salle_id,utilisateur_id,date_creneau,heure_debut) "
                 "VALUES (:s,:u,:d,:h)"), {"s": salle, "u": uid, "d": jour, "h": heure})


# --- Sans base --------------------------------------------------------------------------

@pytest.mark.parametrize("valeur", [
    "01/12/2026", "2026-1-1", "20261201", "abc", "", "2026-13-01", "2026-02-30",
    "1764547200", "2026-12-01T00:00:00", "2026-12-01 ", "%27%3B--", "２０２６-12-01",
])
def test_date_invalide_422_sans_echo(client, valeur):
    reponse = client.get("/api/disponibilites", params={"date": valeur})
    assert reponse.status_code == 422
    corps = reponse.json()
    assert set(corps) == {"erreur", "message"}
    assert valeur.strip() == "" or valeur not in reponse.text
    for mot in ("Traceback", "pydantic", "sqlalchemy", "psycopg", "File "):
        assert mot not in reponse.text


def test_date_absente_ou_trop_longue_422(client):
    for params in ({}, {"date": "2026-12-01" + "9" * 5000}):
        reponse = client.get("/api/disponibilites", params=params)
        assert reponse.status_code == 422
        assert set(reponse.json()) == {"erreur", "message"}


@pytest.mark.parametrize("jour,code", [
    ("2026-11-30", "date_passee"), ("0001-01-01", "date_passee"),
    ("2026-12-16", "date_hors_fenetre"), ("9999-12-31", "date_hors_fenetre"),
])
def test_date_hors_fenetre_422(client, jour, code):
    reponse = client.get("/api/disponibilites", params={"date": jour})
    assert reponse.status_code == 422
    assert reponse.json()["erreur"] == code


def test_fenetre_utilise_l_horloge_de_paris_et_non_utc():
    """Constat 12 : 00 h 30 à Paris le 2 déc. = 23 h 30 UTC le 1er ; le jour de Paris prévaut."""
    tard = datetime(2026, 12, 2, 0, 30, tzinfo=FUSEAU)
    assert tard.astimezone(timezone.utc).date().isoformat() == "2026-12-01"
    reponse = _client(tard).get("/api/disponibilites", params={"date": "2026-12-01"})
    assert reponse.status_code == 422 and reponse.json()["erreur"] == "date_passee"


def test_routes_api_inconnues_gardent_une_404_json(client):
    for chemin in ("/api/inconnue", "/api/accueil/reservations-du-jour", "/api"):
        reponse = client.get(chemin)
        assert reponse.status_code == 404
        assert reponse.headers["content-type"].startswith("application/json")
        assert reponse.json()["erreur"] == "introuvable"
    assert client.post("/api/reservations").status_code == 404


def test_routes_en_ecriture_refusees(client):
    for methode in ("post", "put", "delete", "patch"):
        reponse = getattr(client, methode)("/api/salles")
        assert reponse.status_code in (404, 405)


def test_front_statique_et_health_inchanges(client_base_ok):
    assert client_base_ok.get("/").status_code == 200
    assert client_base_ok.get("/health").status_code == 200


def test_503_json_sans_base_configuree(client):
    for chemin, params in (("/api/salles", {}), ("/api/disponibilites", {"date": "2026-12-01"})):
        reponse = client.get(chemin, params=params)
        assert reponse.status_code == 503
        assert reponse.json() == {"erreur": "indisponible",
                                  "message": "Service momentanément indisponible."}


def test_503_sans_detail_quand_la_base_est_injoignable(monkeypatch):
    # Hôte inexistant : l'erreur du pilote (avec l'URL) ne doit rien laisser filtrer.
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:MOTDEPASSE@hote-inexistant.invalid/b")
    bdd.moteur_applicatif.cache_clear()
    try:
        reponse = _client().get("/api/salles")
    finally:
        bdd.moteur_applicatif.cache_clear()
    assert reponse.status_code == 503
    assert "MOTDEPASSE" not in reponse.text and "invalid" not in reponse.text


def test_moteur_applicatif_borne_attente_et_requete(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@localhost/b")
    bdd.moteur_applicatif.cache_clear()
    try:
        moteur = bdd.moteur_applicatif()
        assert moteur.pool.timeout() <= 5
    finally:
        bdd.moteur_applicatif.cache_clear()
    import inspect
    source = inspect.getsource(bdd.moteur_applicatif)
    assert "statement_timeout" in source


def test_les_routes_n_utilisent_pas_la_sonde():
    import inspect

    from reservation import api
    assert "_moteur_sonde" not in inspect.getsource(api)
    assert "bdd.moteur_applicatif" in inspect.getsource(api.fournir_moteur)


def test_le_code_ne_lit_aucune_donnee_de_membre():
    import inspect

    from reservation import api
    source = inspect.getsource(api)
    assert "FROM utilisateur" not in source and "JOIN" not in source
    assert "SELECT salle_id, heure_debut FROM reservation" in source


def test_acces_provisoire_signale_dans_le_code():
    import inspect

    from reservation import api
    source = inspect.getsource(api)
    assert "PROVISOIRE" in source and "T-013" in source and "T-020" in source


# --- Intégration PostgreSQL -------------------------------------------------------------

@integration
def test_salles_renvoie_les_trois_salles(base, client):
    reponse = client.get("/api/salles")
    assert reponse.status_code == 200
    assert reponse.json() == [
        {"id": 1, "nom": "Salle 1", "capacite": None, "equipements": None},
        {"id": 2, "nom": "Salle 2", "capacite": None, "equipements": None},
        {"id": 3, "nom": "Salle 3", "capacite": None, "equipements": None},
    ]


@integration
def test_jour_ouvre_12_creneaux_par_salle_tous_libres(base, client):
    reponse = client.get("/api/disponibilites", params={"date": "2026-12-02"})  # mercredi
    assert reponse.status_code == 200
    corps = reponse.json()
    assert corps["date"] == "2026-12-02"
    assert [s["nom"] for s in corps["salles"]] == ["Salle 1", "Salle 2", "Salle 3"]
    for salle in corps["salles"]:
        assert len(salle["creneaux"]) == 12
        assert [c["heure_debut"] for c in salle["creneaux"]] == list(range(8, 20))
        assert [c["heure_fin"] for c in salle["creneaux"]] == list(range(9, 21))
        assert {c["etat"] for c in salle["creneaux"]} == {"libre"}


@integration
@pytest.mark.parametrize("jour", ["2026-12-05", "2026-12-06"])  # samedi, dimanche
def test_week_end_aucun_creneau(base, client, jour):
    reponse = client.get("/api/disponibilites", params={"date": jour})
    assert reponse.status_code == 200
    salles = reponse.json()["salles"]
    assert len(salles) == 3
    assert all(s["creneaux"] == [] for s in salles)


@integration
def test_reservation_rend_le_creneau_occupe_sans_donnee_de_membre(base, client):
    _reserver(base, 2, "2026-12-02", 9)
    _reserver(base, 3, "2026-12-02", 19, email="autre@exemple.fr", nom="Autre Personne")
    _reserver(base, 1, "2026-12-03", 9)  # un autre jour : sans effet
    reponse = client.get("/api/disponibilites", params={"date": "2026-12-02"})
    assert reponse.status_code == 200
    occupes = {(s["salle_id"], c["heure_debut"])
               for s in reponse.json()["salles"] for c in s["creneaux"] if c["etat"] == "occupe"}
    assert occupes == {(2, 9), (3, 19)}
    libres = sum(c["etat"] == "libre" for s in reponse.json()["salles"] for c in s["creneaux"])
    assert libres == 34
    brut = reponse.text.lower()
    for interdit in ("secret", "nom secret", "exemple.fr", "autre personne", "@",
                     "utilisateur", "email", '"id"'):
        assert interdit not in brut
    for salle in reponse.json()["salles"]:
        assert set(salle) == {"salle_id", "nom", "creneaux"}
        for c in salle["creneaux"]:
            assert set(c) == {"heure_debut", "heure_fin", "etat"}


@integration
def test_bornes_de_la_fenetre_acceptees(base):
    assert _client().get("/api/disponibilites", params={"date": "2026-12-01"}).status_code == 200
    assert _client().get("/api/disponibilites", params={"date": "2026-12-15"}).status_code == 200


@integration
def test_requete_sans_connexion_ni_cookie_et_sans_set_cookie(base, client):
    reponse = client.get("/api/salles")
    assert reponse.status_code == 200 and "set-cookie" not in reponse.headers


@integration
def test_temps_de_reponse_sous_2_s_h05(base, client):
    for h in range(8, 20):
        for s in (1, 2, 3):
            _reserver(base, s, "2026-12-02", h)
    client.get("/api/disponibilites", params={"date": "2026-12-02"})  # chauffe le pool
    debut = time.perf_counter()
    reponse = client.get("/api/disponibilites", params={"date": "2026-12-02"})
    duree = time.perf_counter() - debut
    assert reponse.status_code == 200
    assert duree < 2.0, f"{duree:.3f} s"
    assert sum(c["etat"] == "occupe" for s in reponse.json()["salles"] for c in s["creneaux"]) == 36
