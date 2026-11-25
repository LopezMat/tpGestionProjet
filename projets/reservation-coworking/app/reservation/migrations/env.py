"""Environnement Alembic : l'URL vient de `config.attributes["url"]` ou de DATABASE_URL.

Moteur propre aux migrations (NullPool), distinct de la sonde et du moteur applicatif.
Pas de `fileConfig` : il désactiverait les journaux de l'application.
"""

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from reservation import config


def _url() -> str:
    url = context.config.attributes.get("url") or config.url_base()
    if not url:
        raise RuntimeError("DATABASE_URL n'est pas renseignée.")
    return url


moteur = create_engine(_url(), poolclass=NullPool)
with moteur.connect() as connexion:
    context.configure(connection=connexion, target_metadata=None)
    with context.begin_transaction():
        context.run_migrations()
moteur.dispose()
