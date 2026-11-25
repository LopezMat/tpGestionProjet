"""Application FastAPI : /health, puis le front statique à la racine."""

from collections.abc import Awaitable, Callable
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from . import api, bdd, config

DOSSIER_STATIQUE = Path(__file__).parent / "static"


# Hôtes acceptés dans l'en-tête Host (port ignoré) : liste fixée dans le code, qui ne dépend
# d'aucune entrée de la requête (T-063, constat 4 : DNS rebinding). Les sondes de
# verifier-prod, deployer_local.py et l'aperçu local joignent l'app par ces deux noms
# (url_prod http://localhost:<port>). À revoir par décision humaine si l'hébergement change.
HOTES_AUTORISES = ["localhost", "127.0.0.1"]

# CSP de l'architecture § 6 : aucun script ni style en ligne (T-055 doit s'y conformer).
EN_TETES_SECURITE = [
    (
        b"content-security-policy",
        b"default-src 'self'; script-src 'self'; style-src 'self'; "
        b"frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
    ),
    (b"x-content-type-options", b"nosniff"),
    (b"referrer-policy", b"no-referrer"),
]


class EnTetesSecurite:
    """Middleware ASGI : ajoute les en-têtes de sécurité à toute réponse HTTP (T-063)."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def envoyer(message: Message) -> None:
            if message["type"] == "http.response.start":
                deja = {nom.lower() for nom, _ in message["headers"]}
                message["headers"] = list(message["headers"]) + [
                    (n, v) for n, v in EN_TETES_SECURITE if n not in deja
                ]
            await send(message)

        await self.app(scope, receive, envoyer)


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

    # Ordre : le dernier ajouté est le plus externe. Les en-têtes enveloppent le contrôle
    # d'hôte, pour que même la réponse 400 les porte.
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=HOTES_AUTORISES)
    app.add_middleware(EnTetesSecurite)

    app.include_router(api.routeur)
    app.add_exception_handler(api.BaseIndisponible, api.gerer_base_indisponible)
    app.add_exception_handler(RequestValidationError, api.gerer_requete_invalide)

    # Monté en dernier : les routes de l'API restent prioritaires sur les fichiers statiques.
    app.mount("/", StaticFiles(directory=DOSSIER_STATIQUE, html=True), name="front")
    return app


app = creer_app()
