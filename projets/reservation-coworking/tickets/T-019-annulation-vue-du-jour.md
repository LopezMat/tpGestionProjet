---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-019
titre: Annulation et vue du jour de l'accueil (F-02, F-03)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-018]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-019 — Annulation et vue du jour de l'accueil (F-02, F-03)

## Description
F-02 « Annuler une réservation » et F-03 « Vue des réservations du jour pour l'accueil » (Must), composants `api.reservations` et `api.accueil` de [architecture.md](../architecture.md) § 3 et § 4 : `GET /api/reservations/miennes`, `DELETE /api/reservations/{id}` (annulation = suppression de la ligne, décision 10), `GET /api/accueil/reservations-du-jour`. Une réservation d'autrui renvoie 404 (pas 403).

**Touche la sécurité** (rôle accueil, accès aux réservations d'autrui, données personnelles de la vue du jour) : revue humaine obligatoire, ticket compagnon **T-035** (Karim).

## Critères d'acceptation
- [ ] Un membre voit la liste de ses réservations à venir et peut en annuler une.
- [ ] **Délai** : un membre peut annuler sa réservation jusqu'au début du créneau ; à partir de l'heure de début, l'annulation est refusée (test aux bornes avec horloge injectée : réservation de 10 h-11 h annulable à 9 h 59, refusée à 10 h 00).
- [ ] **Accueil** : un utilisateur au rôle accueil peut annuler n'importe quelle réservation non terminée, quel que soit le membre (H-15).
- [ ] Après annulation, le créneau redevient « libre » pour tous les utilisateurs et disparaît de la vue de l'accueil ; le quota du membre est libéré (après annulation d'une de ses 2 réservations, une nouvelle est acceptée, test).
- [ ] Un membre ne peut ni voir le détail ni annuler la réservation d'un autre membre : réponse 404 identique à une réservation inexistante (test d'autorisation par appel direct à l'API avec l'identifiant d'une réservation d'autrui).
- [ ] L'annulation d'une réservation déjà annulée est refusée sans erreur serveur (404 « réservation introuvable ou déjà annulée »).
- [ ] **Vue du jour (F-03)** : un utilisateur accueil connecté obtient la liste des réservations de la date du jour pour les 3 salles, triée par heure, avec salle, créneau, nom du membre et e-mail, et aucun autre champ ; la route ne prend pas de paramètre de date.
- [ ] Une réservation créée ou annulée apparaît ou disparaît de cette liste sans intervention manuelle (au prochain appel) ; un jour sans réservation renvoie une liste vide (message « aucune réservation » affiché par T-024).
- [ ] Un membre (rôle non accueil) et un visiteur non connecté ne peuvent pas accéder à cette vue (test d'autorisation par appel direct à l'API).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (rôle accueil et accès aux réservations d'autrui, S3-R2 ; ticket compagnon T-035)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
