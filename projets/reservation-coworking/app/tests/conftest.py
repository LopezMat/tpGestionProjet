import pytest
from fastapi.testclient import TestClient

from reservation.app import creer_app, verifier_base


def _controle(valeur: bool):
    async def controle() -> bool:
        return valeur

    return controle


@pytest.fixture(autouse=True)
def _environnement_propre(monkeypatch):
    """Aucun test ne dépend des variables de la machine."""
    for nom in ("GIT_COMMIT", "RENDER_GIT_COMMIT", "DATABASE_URL", "PORT"):
        monkeypatch.delenv(nom, raising=False)


@pytest.fixture
def client_base_ok():
    app = creer_app()
    app.dependency_overrides[verifier_base] = lambda: _controle(True)
    return TestClient(app)


@pytest.fixture
def client_base_ko():
    app = creer_app()
    app.dependency_overrides[verifier_base] = lambda: _controle(False)
    return TestClient(app)
