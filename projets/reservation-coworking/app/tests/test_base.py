"""Contrôle de la base : sans PostgreSQL pour les cas d'échec, avec pour le cas nominal."""

import os
import time

import pytest

from reservation import bdd, config


def test_base_repond_faux_sans_url():
    assert bdd.base_repond() is False


def test_base_repond_faux_quand_la_base_est_injoignable(monkeypatch):
    # Port 1 sur la boucle locale : connexion refusée immédiatement.
    monkeypatch.setenv("DATABASE_URL", "postgresql://esn:secret-de-test@127.0.0.1:1/app")
    debut = time.monotonic()
    assert bdd.base_repond() is False
    assert time.monotonic() - debut < 5


def test_conversion_de_l_url_pour_psycopg3():
    assert config.convertir_url_base("postgresql://u:p@db:5432/app") == "postgresql+psycopg://u:p@db:5432/app"
    assert config.convertir_url_base("postgres://u:p@db/app") == "postgresql+psycopg://u:p@db/app"
    assert config.convertir_url_base("postgresql+psycopg://u:p@db/app") == "postgresql+psycopg://u:p@db/app"


def test_url_base_absente(monkeypatch):
    assert config.url_base() is None


@pytest.mark.skipif(
    not os.environ.get("TEST_DATABASE_URL"),
    reason="PostgreSQL requis : renseigner TEST_DATABASE_URL (postgresql://...)",
)
def test_base_repond_vrai_avec_un_vrai_postgres(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", os.environ["TEST_DATABASE_URL"])
    assert bdd.base_repond() is True


@pytest.mark.skipif(
    not os.environ.get("TEST_DATABASE_URL"),
    reason="PostgreSQL requis : renseigner TEST_DATABASE_URL (postgresql://...)",
)
def test_health_200_de_bout_en_bout_avec_un_vrai_postgres(monkeypatch):
    from fastapi.testclient import TestClient

    from reservation.app import creer_app

    monkeypatch.setenv("DATABASE_URL", os.environ["TEST_DATABASE_URL"])
    monkeypatch.setenv("GIT_COMMIT", "f" * 40)
    reponse = TestClient(creer_app()).get("/health")
    assert reponse.status_code == 200
    assert reponse.json() == {"status": "ok", "commit": "f" * 40}
