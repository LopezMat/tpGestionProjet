"""Horloge injectable : « maintenant » en Europe/Paris.

Aucune règle métier n'appelle `datetime.now()` : elles reçoivent l'instant en paramètre,
fourni par cette horloge (dépendance FastAPI `fournir_horloge`, remplaçable dans les tests).
"""

from collections.abc import Callable
from datetime import datetime
from zoneinfo import ZoneInfo

FUSEAU = ZoneInfo("Europe/Paris")

Horloge = Callable[[], datetime]


def maintenant() -> datetime:
    """Instant courant, aware, en Europe/Paris (H-17)."""
    return datetime.now(FUSEAU)


def fournir_horloge() -> Horloge:
    """Dépendance FastAPI : `Depends(fournir_horloge)` ; remplacée via dependency_overrides."""
    return maintenant
