"""Point d'entrée de l'image : python -m reservation.demarrer.

T-010 : attente de la base, puis Uvicorn avec 1 worker (architecture.md § 8). Les migrations
(T-011), l'avertissement « aucun compte accueil », la limitation des tentatives de connexion
et la tâche de purge seront ajoutés par les tickets suivants.
"""

import logging
import sys
import time

import uvicorn

from . import bdd, config

journal = logging.getLogger("reservation.demarrer")

ATTENTE_MAX_S = 60
PAUSE_S = 1


def attendre_base(attente_max_s: float = ATTENTE_MAX_S, pause_s: float = PAUSE_S) -> bool:
    """Attend que la base réponde ; faux si le délai est dépassé."""
    fin = time.monotonic() + attente_max_s
    while True:
        if bdd.base_repond():
            return True
        if time.monotonic() >= fin:
            return False
        journal.info("Base de données pas encore joignable, nouvel essai.")
        time.sleep(pause_s)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    if config.url_base() is None:
        journal.error("DATABASE_URL n'est pas renseignée.")
        return 1
    if not attendre_base():
        journal.error("La base n'a pas répondu dans le délai de %s s.", ATTENTE_MAX_S)
        return 1
    try:
        port = config.port()
    except ValueError as erreur:
        journal.error("%s", erreur)
        return 1
    uvicorn.run(
        "reservation.app:app",
        host="0.0.0.0",  # nosec B104 : dans le conteneur ; publié sur 127.0.0.1 par le modèle compose
        port=port,
        workers=1,
        server_header=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
