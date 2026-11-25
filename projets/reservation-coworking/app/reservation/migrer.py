"""Application des migrations Alembic au démarrage, de façon tolérante (architecture.md § 8).

- base vide ou à une révision connue de l'image : `alembic upgrade head` ;
- base à une révision plus récente que l'image (rollback) : avertissement, pas de migration ;
- jamais de migration descendante automatique.
"""

import logging
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.util.exc import CommandError
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from . import config

journal = logging.getLogger("reservation.migrer")

DOSSIER = Path(__file__).parent / "migrations"


def _configuration(url: str) -> Config:
    cfg = Config()
    cfg.set_main_option("script_location", str(DOSSIER))
    cfg.attributes["url"] = url  # jamais dans un fichier .ini, ni dans les journaux
    return cfg


def revisions_base(url: str) -> tuple[str, ...]:
    """Révisions courantes inscrites dans la base (vide : base neuve)."""
    moteur = create_engine(url, poolclass=NullPool)
    try:
        with moteur.connect() as connexion:
            return MigrationContext.configure(connexion).get_current_heads()
    finally:
        moteur.dispose()


def _connue(scripts: ScriptDirectory, revision: str) -> bool:
    try:
        return scripts.get_revision(revision) is not None
    except CommandError:
        return False


def appliquer() -> bool:
    """Migre la base vers la tête de l'image si c'est possible ; faux si la base est en avance."""
    url = config.url_base()
    if url is None:
        raise RuntimeError("DATABASE_URL n'est pas renseignée.")
    cfg = _configuration(url)
    scripts = ScriptDirectory.from_config(cfg)
    inconnues = [r for r in revisions_base(url) if not _connue(scripts, r)]
    if inconnues:
        journal.warning(
            "La base est à une révision plus récente que cette image (%s) : "
            "démarrage sans migration.", ", ".join(inconnues))
        return False
    command.upgrade(cfg, "head")
    return True
