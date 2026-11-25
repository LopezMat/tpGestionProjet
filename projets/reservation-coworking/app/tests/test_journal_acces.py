"""T-071 : le journal d'accès n'écrit ni chaîne de requête ni donnée d'entrée."""

import logging
import logging.config

import pytest

from reservation import demarrer, journaux


def _enregistrement(chemin_complet, methode="GET", statut=200):
    return logging.LogRecord(
        "uvicorn.access", logging.INFO, "x", 0, '%s - "%s %s HTTP/%s" %d',
        ("203.0.113.9:5555", methode, chemin_complet, "1.1", statut), None,
    )


def _ligne(chemin_complet, **kw):
    return journaux.FormatAcces("%(message)s").format(_enregistrement(chemin_complet, **kw))


def test_la_chaine_de_requete_n_est_pas_ecrite():
    ligne = _ligne("/api/disponibilites?date=" + "9" * 9000, statut=422)
    assert ligne == "GET /api/disponibilites 422"
    assert "?" not in ligne and "date=" not in ligne and "9999" not in ligne


def test_adresse_du_client_non_ecrite():
    assert "203.0.113.9" not in _ligne("/health")


@pytest.mark.parametrize("chemin,statut", [("/", 200), ("/health", 200), ("/api/salles", 200)])
def test_requetes_nominales_journalisees(chemin, statut):
    assert _ligne(chemin, statut=statut) == f"GET {chemin} {statut}"


def test_chemin_borne_et_sans_saut_de_ligne():
    ligne = _ligne("/" + "a" * 5000 + "\nFAUX 200")
    assert len(ligne) < 300
    assert "\n" not in ligne


def test_forme_inattendue_ne_recopie_rien():
    rec = logging.LogRecord("uvicorn.access", logging.INFO, "x", 0, "%s", ("secret?x=1",), None)
    assert "secret" not in journaux.FormatAcces("%(message)s").format(rec)


def test_la_configuration_est_valide_et_capte_uvicorn_access(capsys):
    logging.config.dictConfig(journaux.config_journaux())
    try:
        logging.getLogger("uvicorn.access").info(
            '%s - "%s %s HTTP/%s" %d', "10.0.0.1:1", "GET", "/api/salles?x=secret", "1.1", 200
        )
        sortie = capsys.readouterr().out
        assert "GET /api/salles 200" in sortie
        assert "secret" not in sortie and "?" not in sortie
    finally:
        logging.getLogger("uvicorn.access").handlers.clear()
        logging.getLogger("uvicorn.access").propagate = True


def test_main_transmet_la_configuration_a_uvicorn(monkeypatch):
    appels = {}
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db/app")
    monkeypatch.setattr(demarrer.migrer, "appliquer", lambda: True)
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    monkeypatch.setattr(demarrer.uvicorn, "run", lambda *a, **kw: appels.update(kw=kw))
    assert demarrer.main() == 0
    config = appels["kw"]["log_config"]
    assert config["formatters"]["acces"]["()"].endswith("FormatAcces")
    assert "request_line" not in str(config)
    assert appels["kw"]["workers"] == 1 and appels["kw"]["server_header"] is False
    assert not appels["kw"].get("access_log") is False  # le journal d'accès reste actif
