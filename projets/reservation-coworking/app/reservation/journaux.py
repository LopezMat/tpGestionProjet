"""Journal d'accès minimal (T-071, constat 15 du rapport securite-2026-11-25-4).

Le journal d'accès par défaut d'Uvicorn recopie la chaîne de requête brute, sans limite.
Ici, une ligne d'accès ne porte que : méthode, chemin sans chaîne de requête (borné à
LONGUEUR_MAX_CHEMIN caractères) et code de réponse. Ni adresse du client, ni requête,
ni en-tête : aucune donnée d'entrée n'est écrite.
"""

import logging

LONGUEUR_MAX_CHEMIN = 200
FORMAT_GENERAL = "%(asctime)s %(levelname)s %(name)s %(message)s"


def chemin_sans_requete(chemin_complet: object) -> str:
    """Retire la chaîne de requête et le fragment, puis borne la longueur."""
    chemin = str(chemin_complet).split("?", 1)[0].split("#", 1)[0]
    # Pas de saut de ligne ni de caractère de contrôle (injection dans le journal).
    chemin = "".join(c if c.isprintable() else "?" for c in chemin)
    if len(chemin) > LONGUEUR_MAX_CHEMIN:
        chemin = chemin[:LONGUEUR_MAX_CHEMIN] + "…"
    return chemin


class FormatAcces(logging.Formatter):
    """Reformate la ligne d'accès d'Uvicorn : « GET /chemin 200 »."""

    def formatMessage(self, record: logging.LogRecord) -> str:
        try:
            _client, methode, chemin_complet, _version, statut = record.args  # type: ignore[misc]
            record.message = f"{str(methode)[:16]} {chemin_sans_requete(chemin_complet)} {int(statut)}"
        except (TypeError, ValueError):
            # Forme inattendue : rien de ce qui a été reçu n'est recopié.
            record.message = "requête reçue (format de journal d'accès inattendu)"
        return super().formatMessage(record)


def config_journaux() -> dict:
    """Configuration `log_config` transmise à uvicorn.run."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "general": {"format": FORMAT_GENERAL},
            "acces": {"()": f"{__name__}.FormatAcces", "format": FORMAT_GENERAL},
        },
        "handlers": {
            "defaut": {"class": "logging.StreamHandler", "formatter": "general", "stream": "ext://sys.stderr"},
            "acces": {"class": "logging.StreamHandler", "formatter": "acces", "stream": "ext://sys.stdout"},
        },
        "loggers": {
            "uvicorn": {"handlers": ["defaut"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["acces"], "level": "INFO", "propagate": False},
        },
    }
