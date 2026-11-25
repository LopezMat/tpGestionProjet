"""Règles métier de date et d'heure (F-01, F-02, F-08). Module pur : ni base ni HTTP.

Toutes les fonctions reçoivent « maintenant » en paramètre (datetime en heure de Paris) :
aucune n'appelle l'horloge. Un refus lève `ReglePasRespectee` avec un message en français.
La garantie sous concurrence relève de T-018, pas de ce module.
"""

from datetime import date, datetime, timedelta

HEURE_PREMIER_CRENEAU = 8  # 8 h-9 h
HEURE_DERNIER_CRENEAU = 19  # 19 h-20 h
AVANCE_MAX_JOURS = 14  # H-10 : J à J+14 inclus
QUOTA_PAR_JOUR = 2  # H-12
ANNEES_CONSERVATION = 1  # H-13 : 12 mois


class ReglePasRespectee(ValueError):
    """Refus d'une règle métier ; `str(erreur)` est le message affiché à l'utilisateur."""


def _debut(jour: date, heure: int) -> datetime:
    return datetime(jour.year, jour.month, jour.day, heure)


def _heure_murale(instant: datetime) -> datetime:
    """Compare en heure murale de Paris : on retire l'information de fuseau."""
    return instant.replace(tzinfo=None)


def verifier_creneau_valide(jour: date, heure_debut: int) -> None:
    """F-01 : du lundi au vendredi, créneaux d'une heure de 8 h-9 h à 19 h-20 h."""
    if jour.weekday() >= 5:
        raise ReglePasRespectee("Les réservations ne sont possibles que du lundi au vendredi.")
    if not HEURE_PREMIER_CRENEAU <= heure_debut <= HEURE_DERNIER_CRENEAU:
        raise ReglePasRespectee("Les créneaux vont de 8 h à 20 h, par tranches d'une heure.")


def verifier_avance(jour: date, maintenant: datetime) -> None:
    """F-01, H-10 : au plus 14 jours à l'avance (J+14 accepté, J+15 refusé)."""
    if jour > maintenant.date() + timedelta(days=AVANCE_MAX_JOURS):
        raise ReglePasRespectee(
            f"Il n'est pas possible de réserver plus de {AVANCE_MAX_JOURS} jours à l'avance."
        )


def verifier_pas_commence(jour: date, heure_debut: int, maintenant: datetime) -> None:
    """F-01, H-11 : un créneau commencé (début <= maintenant) ou passé est refusé."""
    if _debut(jour, heure_debut) <= _heure_murale(maintenant):
        raise ReglePasRespectee("Ce créneau a déjà commencé ou est passé.")


def verifier_quota(reservations_actives_du_jour: int) -> None:
    """F-01, H-12 : au plus 2 réservations actives par membre et par date, salles confondues.

    L'appelant ne compte que les réservations non annulées de ce membre pour cette date.
    """
    if reservations_actives_du_jour >= QUOTA_PAR_JOUR:
        raise ReglePasRespectee(
            f"Vous avez déjà {QUOTA_PAR_JOUR} réservations ce jour-là : c'est le maximum."
        )


def verifier_reservation(
    jour: date,
    heure_debut: int,
    maintenant: datetime,
    reservations_actives_du_jour: int,
) -> None:
    """Enchaîne les règles de F-01 ; la première violée lève l'erreur."""
    verifier_creneau_valide(jour, heure_debut)
    verifier_pas_commence(jour, heure_debut, maintenant)
    verifier_avance(jour, maintenant)
    verifier_quota(reservations_actives_du_jour)


def verifier_annulation(
    jour: date, heure_debut: int, maintenant: datetime, est_accueil: bool = False
) -> None:
    """F-02, H-15 : le membre annule jusqu'au début du créneau (exclu) ;
    l'accueil tant que le créneau n'est pas terminé."""
    debut = _debut(jour, heure_debut)
    local = _heure_murale(maintenant)
    if est_accueil:
        if local >= debut + timedelta(hours=1):
            raise ReglePasRespectee("Ce créneau est terminé : l'annulation n'est plus possible.")
    elif local >= debut:
        raise ReglePasRespectee(
            "Le créneau a commencé : l'annulation n'est possible que jusqu'à son début."
        )


def date_limite_purge(aujourdhui: date) -> date:
    """F-08, H-13 : même jour 12 mois plus tôt ; le 29 février devient le 28 février."""
    annee = aujourdhui.year - ANNEES_CONSERVATION
    try:
        return aujourdhui.replace(year=annee)
    except ValueError:  # 29 février vers une année non bissextile
        return date(annee, 2, 28)


def doit_etre_purgee(jour_creneau: date, aujourdhui: date) -> bool:
    """Vrai si le créneau est strictement antérieur à la date limite (12 mois et 1 jour)."""
    return jour_creneau < date_limite_purge(aujourdhui)
