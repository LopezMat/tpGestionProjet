"""Accès à la base PostgreSQL (SQLAlchemy 2, pilote psycopg 3).

Le contrôle de la base (`/health`, attente au démarrage) est borné **côté client** par
une échéance ferme de `DELAI_BASE_S` secondes, quelle que soit la façon dont la base
se tait (arrêtée, nom non résolu, gelée, coupure réseau). Ni `connect_timeout` (libpq
le ramène à 2 s au minimum et ne couvre ni la résolution DNS ni une connexion déjà
ouverte) ni `statement_timeout` (côté serveur) ne le garantissent : le contrôle tourne
donc dans un fil dédié, et l'appelant cesse d'attendre à l'échéance.

Ce moteur (`_moteur_sonde`) ne sert qu'à la sonde de santé. L'accès métier passe par
`moteur_applicatif()` (avec pool) et les migrations par leur propre moteur
(`migrations/env.py`) : ne jamais les mélanger (NullPool et `statement_timeout` de 1 s
y seraient inadaptés).

Pas de pool pour la sonde : une sonde ouvre une connexion neuve, la ferme, et ne risque pas de
réutiliser une connexion devenue muette. Au plus `_MAX_CONTROLES` sondes sont en vol ;
si elles sont toutes bloquées (base gelée), les contrôles suivants répondent faux
immédiatement au lieu d'empiler des fils.
"""

import asyncio
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from functools import lru_cache

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.pool import NullPool

from . import config

# Borne de réponse de /health quand la base ne répond pas (secondes).
DELAI_BASE_S = 1

_MAX_CONTROLES = 4
_executeur = ThreadPoolExecutor(max_workers=_MAX_CONTROLES, thread_name_prefix="sonde-base")
_places = threading.BoundedSemaphore(_MAX_CONTROLES)


@lru_cache(maxsize=4)
def _moteur_sonde(url: str) -> Engine:
    return create_engine(
        url,
        poolclass=NullPool,
        connect_args={
            # libpq arrondit à 2 s minimum ; l'échéance de 1 s est tenue par l'appelant.
            "connect_timeout": 2,
            # Borne la durée de vie d'une sonde restée bloquée sur une coupure réseau.
            "tcp_user_timeout": 3000,
            "options": f"-c statement_timeout={DELAI_BASE_S * 1000}",
        },
    )


@lru_cache(maxsize=1)
def moteur_applicatif() -> Engine:
    """Moteur de l'accès métier : pool de connexions, vérifiées avant emploi (T-011).

    Distinct de la sonde : pas de `statement_timeout` de 1 s, connexions réutilisées.
    """
    url = config.url_base()
    if url is None:
        raise RuntimeError("DATABASE_URL n'est pas renseignée.")
    return create_engine(
        url,
        pool_size=5,
        max_overflow=5,
        pool_pre_ping=True,
        pool_recycle=1800,
        # Borne l'attente d'une connexion (503 côté API) et la durée d'une requête.
        pool_timeout=3,
        connect_args={"connect_timeout": 5, "options": "-c statement_timeout=5000"},
    )


def _sonder() -> bool:
    """Exécute `SELECT 1` sur une connexion neuve (peut bloquer : toujours via `_lancer`)."""
    url = config.url_base()
    if url is None:
        return False
    try:
        with _moteur_sonde(url).connect() as connexion:
            return connexion.execute(text("SELECT 1")).scalar() == 1
    except Exception:
        # Aucun détail renvoyé ni journalisé : il pourrait contenir l'URL de connexion,
        # donc le mot de passe de la base.
        return False


def _lancer() -> Future | None:
    """Lance une sonde dans le fil dédié, ou None si toutes les places sont prises."""
    if not _places.acquire(blocking=False):
        return None
    try:
        futur = _executeur.submit(_sonder)
    except Exception:
        _places.release()
        return None
    futur.add_done_callback(lambda _: _places.release())
    return futur


def base_repond(delai_s: float = DELAI_BASE_S) -> bool:
    """Vrai si la base répond à `SELECT 1` en moins de `delai_s` secondes (bloquant)."""
    if config.url_base() is None:
        return False
    futur = _lancer()
    if futur is None:
        return False
    try:
        return futur.result(timeout=delai_s) is True
    except Exception:
        return False


async def base_repond_async(delai_s: float = DELAI_BASE_S) -> bool:
    """Comme `base_repond`, sans bloquer la boucle d'événements."""
    if config.url_base() is None:
        return False
    futur = _lancer()
    if futur is None:
        return False
    try:
        return await asyncio.wait_for(asyncio.wrap_future(futur), timeout=delai_s) is True
    except Exception:
        return False
