"""T-060 : la garde des fixtures destructrices refuse les cibles non jetables, sans écriture."""

import pytest
from sqlalchemy import create_engine

import garde_base
import test_api_consultation
import test_migrations
from garde_base import GardeBaseRefusee, verifier_base_jetable

REFUSEES = [
    "postgresql://esn:x@127.0.0.1:5432/app",             # base du modèle commun
    "postgresql://esn:x@127.0.0.1:5432/contest",          # « test » dedans, mais pas en suffixe
    "postgresql://esn:x@127.0.0.1:5432/test",
    "postgresql://esn:x@127.0.0.1:5432/_test",
    "postgresql://esn:x@127.0.0.1:5432/app_test_prod",
    "postgresql://esn:x@127.0.0.1:5432/app_TEST",
    "postgresql://esn:x@127.0.0.1:5432/",
    "postgresql://esn:x@127.0.0.1:5432/app?dbname=app",
    "postgresql://esn:x@db.exemple.invalid:5432/app_test",   # hôte distant
    "postgresql://esn:x@db:5432/app_test",                    # conteneur non déclaré
    "postgresql://esn:x@127.0.0.1:5432/app_test?host=db.exemple.invalid",
    "postgresql:///app_test",                                 # socket Unix, pas d'hôte
    "pas une url",
    "",
    None,
]
ACCEPTEES = [
    "postgresql://esn:x@127.0.0.1:55432/app_test",
    "postgresql://esn:x@localhost/coworking_test",
    "postgresql+psycopg://esn:x@[::1]:5432/app_test",
]


@pytest.mark.parametrize("url", REFUSEES)
def test_url_refusee(url, monkeypatch):
    monkeypatch.delenv("TEST_DATABASE_HOTES_JETABLES", raising=False)
    with pytest.raises(GardeBaseRefusee):
        verifier_base_jetable(url)


@pytest.mark.parametrize("url", ACCEPTEES)
def test_url_acceptee(url, monkeypatch):
    monkeypatch.delenv("TEST_DATABASE_HOTES_JETABLES", raising=False)
    assert verifier_base_jetable(url) == url


def test_hote_conteneur_accepte_seulement_s_il_est_declare(monkeypatch):
    url = "postgresql://esn:x@pg-test:5432/app_test"
    monkeypatch.delenv("TEST_DATABASE_HOTES_JETABLES", raising=False)
    with pytest.raises(GardeBaseRefusee):
        verifier_base_jetable(url)
    monkeypatch.setenv("TEST_DATABASE_HOTES_JETABLES", "autre, PG-Test")
    assert verifier_base_jetable(url) == url
    # la déclaration de l'hôte ne dispense pas du suffixe _test
    with pytest.raises(GardeBaseRefusee):
        verifier_base_jetable("postgresql://esn:x@pg-test:5432/app")


def test_le_message_ne_fuit_pas_l_url(monkeypatch):
    monkeypatch.delenv("TEST_DATABASE_HOTES_JETABLES", raising=False)
    with pytest.raises(GardeBaseRefusee) as e:
        verifier_base_jetable("postgresql://esn:SECRET@127.0.0.1/app")
    assert "SECRET" not in str(e.value)


@pytest.mark.parametrize("module", [test_migrations, test_api_consultation])
def test_fixture_refusee_n_envoie_aucune_instruction(module, monkeypatch):
    """Une URL vers une base `app` sur un hôte injoignable : refus avant tout moteur."""
    appels = []
    monkeypatch.setattr(module, "URL_TEST", "postgresql://esn:x@db.invalide.test:5432/app")
    monkeypatch.setattr(module, "create_engine",
                        lambda *a, **k: appels.append("create_engine"))
    monkeypatch.setattr(garde_base, "create_engine", create_engine, raising=False)
    monkeypatch.setattr(module.migrer, "appliquer", lambda: appels.append("appliquer"))
    generateur = module.base.__wrapped__(monkeypatch) if hasattr(module.base, "__wrapped__") \
        else None
    assert generateur is not None
    with pytest.raises(GardeBaseRefusee):
        next(generateur)
    assert appels == []
