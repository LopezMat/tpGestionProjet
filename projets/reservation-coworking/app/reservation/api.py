"""API de consultation : GET /api/salles et GET /api/disponibilites (T-054, lecture seule).

# PROVISOIRE (DEC-011) : ces deux routes répondent SANS connexion, par écart provisoire
# accepté au CDC F-04. T-013 (authentification) et T-020 (matrice d'autorisation) devront
# les placer derrière la session ; aucun GO tant que ce n'est pas fait.

Elles n'exposent aucune donnée de membre : les requêtes ne lisent jamais `utilisateur_id`
ni la table `utilisateur`, seulement l'existence d'une réservation par créneau.
"""

import logging
import re
from collections.abc import Callable
from datetime import date as Date

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from . import bdd, regles
from .horloge import Horloge, fournir_horloge

journal = logging.getLogger(__name__)

routeur = APIRouter(prefix="/api")

_FORMAT_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class BaseIndisponible(Exception):
    """La base ne répond pas (pool saturé, délai dépassé, non configurée)."""


class Salle(BaseModel):
    id: int
    nom: str
    capacite: int | None = None
    equipements: str | None = None


class Creneau(BaseModel):
    heure_debut: int
    heure_fin: int
    etat: str  # "libre" | "occupe"


class SalleDisponibilites(BaseModel):
    salle_id: int
    nom: str
    creneaux: list[Creneau]


class Disponibilites(BaseModel):
    date: Date
    salles: list[SalleDisponibilites]


class Erreur(BaseModel):
    erreur: str
    message: str


def erreur_json(statut: int, code: str, message: str) -> JSONResponse:
    """Erreur JSON uniforme : message fixe en français, jamais de détail interne ni d'écho."""
    return JSONResponse(status_code=statut, content={"erreur": code, "message": message})


def fournir_moteur() -> Callable[[], Engine]:
    """Dépendance : accès paresseux au moteur applicatif (jamais la sonde de /health).

    Paresseux pour que la validation des paramètres (422) passe avant tout accès à la base.
    Remplaçable en test.
    """

    def obtenir() -> Engine:
        try:
            return bdd.moteur_applicatif()
        except RuntimeError:
            raise BaseIndisponible from None

    return obtenir


def _lire_salles(moteur: Engine) -> list[Salle]:
    with moteur.connect() as c:
        lignes = c.execute(
            text("SELECT id, nom, capacite, equipements FROM salle ORDER BY ordre, id")
        ).all()
    return [Salle(id=l[0], nom=l[1], capacite=l[2], equipements=l[3]) for l in lignes]


@routeur.get("/salles", response_model=list[Salle], responses={503: {"model": Erreur}})
def lister_salles(obtenir_moteur: Callable[[], Engine] = Depends(fournir_moteur)):
    """Fiches des 3 salles (F-06). Provisoirement public (DEC-011, T-013, T-020)."""
    try:
        return _lire_salles(obtenir_moteur())
    except SQLAlchemyError:
        raise BaseIndisponible from None


@routeur.get(
    "/disponibilites",
    response_model=Disponibilites,
    responses={422: {"model": Erreur}, 503: {"model": Erreur}},
)
def lister_disponibilites(
    date_demandee: str = Query(alias="date", description="AAAA-MM-JJ", max_length=10),
    obtenir_moteur: Callable[[], Engine] = Depends(fournir_moteur),
    horloge: Horloge = Depends(fournir_horloge),
):
    """Créneaux libres ou occupés des 3 salles pour un jour, de J à J+14 (H-10).

    Provisoirement public (DEC-011, T-013, T-020). Un samedi ou un dimanche : chaque salle
    est renvoyée avec une liste de créneaux vide. Aucune donnée de membre.
    """
    if not _FORMAT_DATE.fullmatch(date_demandee):
        return erreur_json(422, "date_invalide", "La date doit avoir le format AAAA-MM-JJ.")
    try:
        jour = Date.fromisoformat(date_demandee)
    except ValueError:
        return erreur_json(422, "date_invalide", "Cette date n'existe pas.")

    # « Maintenant » vient de l'horloge (Europe/Paris), jamais de la base ni d'UTC.
    maintenant = horloge()
    if jour < maintenant.date():
        return erreur_json(422, "date_passee", "Cette date est passée.")
    try:
        regles.verifier_avance(jour, maintenant)
    except regles.ReglePasRespectee as e:
        return erreur_json(422, "date_hors_fenetre", str(e))

    jour_ouvre = True
    try:
        regles.verifier_creneau_valide(jour, regles.HEURE_PREMIER_CRENEAU)
    except regles.ReglePasRespectee:
        jour_ouvre = False

    try:
        moteur = obtenir_moteur()
        salles = _lire_salles(moteur)
        occupes: set[tuple[int, int]] = set()
        if jour_ouvre:
            with moteur.connect() as c:
                # Ne sélectionne ni utilisateur_id ni reservation.id : l'état seul suffit.
                lignes = c.execute(
                    text("SELECT salle_id, heure_debut FROM reservation "
                         "WHERE date_creneau = :jour"),
                    {"jour": jour},
                ).all()
            occupes = {(l[0], l[1]) for l in lignes}
    except SQLAlchemyError:
        raise BaseIndisponible from None

    heures = range(regles.HEURE_PREMIER_CRENEAU, regles.HEURE_DERNIER_CRENEAU + 1)
    return Disponibilites(
        date=jour,
        salles=[
            SalleDisponibilites(
                salle_id=s.id,
                nom=s.nom,
                creneaux=[
                    Creneau(
                        heure_debut=h,
                        heure_fin=h + 1,
                        etat="occupe" if (s.id, h) in occupes else "libre",
                    )
                    for h in (heures if jour_ouvre else [])
                ],
            )
            for s in salles
        ],
    )


@routeur.api_route("", methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
                   include_in_schema=False)
@routeur.api_route("/{chemin:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
                   include_in_schema=False)
def route_inconnue(chemin: str = ""):
    """404 JSON pour toute route /api inconnue : le montage statique ne l'avale pas."""
    return erreur_json(404, "introuvable", "Ressource introuvable.")


def gerer_base_indisponible(request: Request, exc: BaseIndisponible) -> JSONResponse:
    journal.warning("Base indisponible pour %s", request.url.path)  # sans détail ni paramètre
    return erreur_json(503, "indisponible", "Service momentanément indisponible.")


async def gerer_requete_invalide(request: Request, exc: Exception) -> JSONResponse:
    # Message fixe : jamais d'écho de la valeur reçue ni de détail interne.
    return erreur_json(422, "requete_invalide", "Paramètres de la requête invalides.")
