---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-018
titre: Disponibilités et réservation (F-01)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 6             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-012, T-013]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-018 — Disponibilités et réservation (F-01)

## Description
F-01 « Consulter les disponibilités et réserver une salle » (Must), composant `api.reservations` de [architecture.md](../architecture.md) § 3 et § 4 : `GET /api/salles`, `GET /api/disponibilites?date=`, `POST /api/reservations`. Unicité garantie par la contrainte `UNIQUE` (409 « créneau indisponible ») et quota par `SELECT … FOR UPDATE` sur la ligne de l'utilisateur ; règles de T-012. L'annulation (et le critère « après annulation, une nouvelle réservation est acceptée ») est dans T-019. Les contrôles d'autorisation de toutes les routes sont vérifiés par la matrice de T-020 (revue humaine T-036).

## Critères d'acceptation
- [ ] `GET /api/salles` renvoie les 3 salles (nom ; capacité et équipements facultatifs).
- [ ] Pour une date donnée, `GET /api/disponibilites` renvoie pour chacune des 3 salles les créneaux d'une heure, chacun marqué « libre » ou « occupé », sans nom de l'occupant pour un membre.
- [ ] **Horaires** : les créneaux proposés vont de 8 h-9 h à 19 h-20 h (12 par salle et par jour), du lundi au vendredi ; aucun créneau n'est proposé le samedi et le dimanche ; une réservation forcée hors de ces plages (appel direct à l'API) est refusée (test : 7 h-8 h, 20 h-21 h, samedi, dimanche refusés ; 8 h-9 h et 19 h-20 h un jour ouvré acceptés).
- [ ] **Unicité** : si deux membres réservent simultanément le même créneau de la même salle, une seule réservation est enregistrée et l'autre reçoit un message d'indisponibilité (test de concurrence à deux connexions sur PostgreSQL réel).
- [ ] **Limite quotidienne** : un membre a au plus 2 réservations actives pour une même date, toutes salles confondues ; la 3e est refusée avec un message explicite ; la limite d'un membre n'affecte pas un autre membre ; deux réservations simultanées du même membre sont sérialisées (tests).
- [ ] **Avance maximale** : date du jour + 14 jours acceptée, + 15 jours refusée avec message (H-10).
- [ ] Un créneau déjà commencé ou passé ne peut pas être réservé (refus avec message clair, H-11).
- [ ] Seul un membre connecté peut réserver ; la réservation est enregistrée au nom du membre connecté (identité tirée de la session, jamais d'un identifiant fourni dans la requête).
- [ ] Après la réservation, le créneau apparaît « occupé » pour tous les utilisateurs.
- [ ] Le temps de `GET /api/disponibilites` est mesuré en test d'intégration et reste sous 2 s (H-05).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (règles métier ; les autorisations de toutes les routes sont revues avec T-020)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
