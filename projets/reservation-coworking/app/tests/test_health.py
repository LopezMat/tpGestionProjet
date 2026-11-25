"""Critères 1 et 2 de T-010 : /health."""


def test_health_ok_renvoie_le_sha_de_git_commit(client_base_ok, monkeypatch):
    monkeypatch.setenv("GIT_COMMIT", "a" * 40)
    reponse = client_base_ok.get("/health")
    assert reponse.status_code == 200
    assert reponse.json() == {"status": "ok", "commit": "a" * 40}


def test_health_repli_sur_render_git_commit(client_base_ok, monkeypatch):
    monkeypatch.setenv("RENDER_GIT_COMMIT", "b" * 40)
    assert client_base_ok.get("/health").json()["commit"] == "b" * 40


def test_git_commit_prime_sur_render_git_commit(client_base_ok, monkeypatch):
    monkeypatch.setenv("GIT_COMMIT", "a" * 40)
    monkeypatch.setenv("RENDER_GIT_COMMIT", "b" * 40)
    assert client_base_ok.get("/health").json()["commit"] == "a" * 40


def test_health_commit_inconnu_sans_variable(client_base_ok):
    assert client_base_ok.get("/health").json() == {"status": "ok", "commit": "inconnu"}


def test_git_commit_vide_donne_le_repli(client_base_ok, monkeypatch):
    # Image construite sans --build-arg : ENV GIT_COMMIT="" dans le conteneur.
    monkeypatch.setenv("GIT_COMMIT", "")
    monkeypatch.setenv("RENDER_GIT_COMMIT", "c" * 40)
    assert client_base_ok.get("/health").json()["commit"] == "c" * 40
    monkeypatch.setenv("RENDER_GIT_COMMIT", "")
    assert client_base_ok.get("/health").json()["commit"] == "inconnu"


def test_health_503_quand_la_base_ne_repond_pas(client_base_ko, monkeypatch):
    monkeypatch.setenv("GIT_COMMIT", "d" * 40)
    reponse = client_base_ko.get("/health")
    assert reponse.status_code == 503
    assert reponse.json() == {"status": "ko", "commit": "d" * 40}


def test_health_503_sans_database_url():
    """Sans override : DATABASE_URL absente, la base est considérée injoignable."""
    from fastapi.testclient import TestClient

    from reservation.app import creer_app

    reponse = TestClient(creer_app()).get("/health")
    assert reponse.status_code == 503
    assert reponse.json() == {"status": "ko", "commit": "inconnu"}


def test_health_public_et_sans_autre_information(client_base_ok, monkeypatch):
    monkeypatch.setenv("GIT_COMMIT", "e" * 40)
    reponse = client_base_ok.get("/health")  # aucun cookie, aucun en-tête d'authentification
    assert reponse.status_code == 200
    assert set(reponse.json()) == {"status", "commit"}
    assert "set-cookie" not in reponse.headers
    corps = reponse.text.lower()
    for mot in ("fastapi", "version", "postgres", "database"):
        assert mot not in corps
