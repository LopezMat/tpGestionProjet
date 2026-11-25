"""T-060 : garde commune des fixtures d'intégration qui écrivent dans PostgreSQL.

Une fixture ne doit jamais toucher une base qui n'est pas explicitement jetable. La garde
s'exécute AVANT toute connexion et lève GardeBaseRefusee si :
- le nom de la base ne se termine pas par `_test` (« contest » ou « app » sont refusés) ;
- l'hôte n'est pas local (localhost, 127.0.0.1, ::1) et n'est pas listé dans la variable
  TEST_DATABASE_HOTES_JETABLES (noms séparés par des virgules : conteneurs de base jetables
  d'un réseau Docker, par exemple « pg-test ») ;
- l'URL contient un paramètre qui peut détourner la cible (host, hostaddr, dbname, service).
"""

import os

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

HOTES_LOCAUX = frozenset({"localhost", "127.0.0.1", "::1"})
PARAMETRES_DETOURNANTS = frozenset({"host", "hostaddr", "dbname", "service"})


class GardeBaseRefusee(RuntimeError):
    pass


def verifier_base_jetable(url: str | None) -> str:
    """Retourne l'URL si elle désigne une base jetable ; sinon lève GardeBaseRefusee.

    Les messages ne reproduisent jamais l'URL (elle peut contenir un mot de passe).
    """
    if not url:
        raise GardeBaseRefusee("TEST_DATABASE_URL non renseignée")
    try:
        cible = make_url(url)
    except ArgumentError:
        raise GardeBaseRefusee("TEST_DATABASE_URL illisible") from None
    nom = cible.database or ""
    if not nom.endswith("_test") or nom == "_test":
        raise GardeBaseRefusee("le nom de la base de test doit se terminer par _test")
    if PARAMETRES_DETOURNANTS & set(cible.query):
        raise GardeBaseRefusee("paramètre d'URL interdit (host, hostaddr, dbname, service)")
    hote = (cible.host or "").lower()
    autorises = {h.strip().lower() for h in
                 os.environ.get("TEST_DATABASE_HOTES_JETABLES", "").split(",") if h.strip()}
    if hote not in HOTES_LOCAUX | autorises:
        raise GardeBaseRefusee("hôte non local et absent de TEST_DATABASE_HOTES_JETABLES")
    return url
