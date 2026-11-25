"""Critère 4 de T-010 : démarrage sur $PORT / DATABASE_URL, 1 worker."""

import pytest

from reservation import config, demarrer


def test_port_lu_dans_la_variable(monkeypatch):
    monkeypatch.setenv("PORT", "9123")
    assert config.port() == 9123


def test_port_par_defaut():
    assert config.port() == 8000


@pytest.mark.parametrize("valeur", ["abc", "80a", "0", "70000", "-1"])
def test_port_invalide_donne_un_message_explicite(monkeypatch, valeur):
    monkeypatch.setenv("PORT", valeur)
    with pytest.raises(ValueError, match="PORT doit être un nombre entier"):
        config.port()


def test_main_echoue_proprement_avec_un_port_invalide(monkeypatch, caplog):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db/app")
    monkeypatch.setenv("PORT", "huit-mille")
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    assert demarrer.main() == 1
    assert "PORT doit être un nombre entier" in caplog.text


def test_attendre_base_reussit_apres_quelques_essais(monkeypatch):
    reponses = iter([False, False, True])
    monkeypatch.setattr(demarrer.bdd, "base_repond", lambda: next(reponses))
    assert demarrer.attendre_base(attente_max_s=5, pause_s=0) is True


def test_attendre_base_abandonne_apres_le_delai(monkeypatch):
    monkeypatch.setattr(demarrer.bdd, "base_repond", lambda: False)
    assert demarrer.attendre_base(attente_max_s=0.05, pause_s=0.01) is False


def test_main_echoue_sans_database_url():
    assert demarrer.main() == 1


def test_main_echoue_si_la_base_ne_repond_pas(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db/app")
    monkeypatch.setattr(demarrer, "attendre_base", lambda: False)
    assert demarrer.main() == 1


def test_main_lance_uvicorn_avec_un_worker_sur_port(monkeypatch):
    appels = {}
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db/app")
    monkeypatch.setenv("PORT", "8123")
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    monkeypatch.setattr(demarrer.uvicorn, "run", lambda *a, **kw: appels.update(args=a, kw=kw))
    assert demarrer.main() == 0
    assert appels["args"] == ("reservation.app:app",)
    assert appels["kw"]["port"] == 8123
    assert appels["kw"]["workers"] == 1
    assert appels["kw"]["server_header"] is False


def test_aucune_autre_variable_exigee(monkeypatch):
    """Seules PORT (défaut 8000) et DATABASE_URL sont lues au lancement."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db/app")
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    monkeypatch.setattr(demarrer.uvicorn, "run", lambda *a, **kw: None)
    assert demarrer.main() == 0
