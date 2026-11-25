"""Configuration lue dans les variables d'environnement (aucun secret en dur)."""

import os

PORT_PAR_DEFAUT = 8000


def commit() -> str:
    """SHA déployé : GIT_COMMIT (figé dans l'image), puis RENDER_GIT_COMMIT, sinon "inconnu"."""
    return os.environ.get("GIT_COMMIT") or os.environ.get("RENDER_GIT_COMMIT") or "inconnu"


def port() -> int:
    """Port d'écoute : $PORT, 8000 à défaut."""
    brut = os.environ.get("PORT")
    if not brut:
        return PORT_PAR_DEFAUT
    try:
        port = int(brut)
    except ValueError:
        raise ValueError("PORT doit être un nombre entier entre 1 et 65535.") from None
    if not 1 <= port <= 65535:
        raise ValueError("PORT doit être un nombre entier entre 1 et 65535.")
    return port


def convertir_url_base(url: str) -> str:
    """Convertit une URL PostgreSQL standard pour le pilote psycopg 3 de SQLAlchemy."""
    for prefixe in ("postgresql://", "postgres://"):
        if url.startswith(prefixe):
            return "postgresql+psycopg://" + url[len(prefixe):]
    return url


def url_base() -> str | None:
    """URL SQLAlchemy de la base, ou None si DATABASE_URL n'est pas renseignée."""
    brut = os.environ.get("DATABASE_URL")
    return convertir_url_base(brut) if brut else None
