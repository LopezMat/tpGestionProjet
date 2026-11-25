"""Application FastAPI : /health, puis le front statique à la racine."""

from collections.abc import Awaitable, Callable
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import bdd, config

DOSSIER_STATIQUE = Path(__file__).parent / "static"


class SanteReponse(BaseModel):
    status: str
    commit: str


def verifier_base() -> Callable[[], Awaitable[bool]]:
    """Dépendance : le contrôle asynchrone de la base, borné à 1 s (remplacé dans les tests)."""
    return bdd.base_repond_async


def creer_app(avec_documentation: bool = False) -> FastAPI:
    """Construit l'application.

    `avec_documentation` n'est vrai que pour générer le schéma OpenAPI (tests) :
    en production, /docs, /redoc et /openapi.json ne sont pas servis (404).
    """
    app = FastAPI(
        title="Réservation de salles - Les Arcades",
        docs_url="/docs" if avec_documentation else None,
        redoc_url="/redoc" if avec_documentation else None,
        openapi_url="/openapi.json" if avec_documentation else None,
    )

    @app.get("/health", response_model=SanteReponse, responses={503: {"model": SanteReponse}})
    async def sante(controle: Callable[[], Awaitable[bool]] = Depends(verifier_base)):
        """Public, sans session : SHA déployé et état de la base, rien d'autre.

        Répond au plus tard après `bdd.DELAI_BASE_S` (1 s) quand la base se tait, sans
        bloquer la boucle d'événements.
        """
        if await controle():
            return SanteReponse(status="ok", commit=config.commit())
        return JSONResponse(
            status_code=503,
            content=SanteReponse(status="ko", commit=config.commit()).model_dump(),
        )

    # Monté en dernier : les routes de l'API restent prioritaires sur les fichiers statiques.
    app.mount("/", StaticFiles(directory=DOSSIER_STATIQUE, html=True), name="front")
    return app


app = creer_app()
