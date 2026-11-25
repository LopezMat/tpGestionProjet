---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-054
titre: API de consultation des disponibilités (F-01, lecture seule)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-011, T-012]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-054 — API de consultation des disponibilités (F-01, lecture seule)

## Description
**Origine.** Changement de priorité d'Ethan du 2026-11-25 : développer d'abord le socle et la partie de F-01 réalisable sans authentification (option « Lecture seule »). La réservation reste dans [T-018](T-018-disponibilites-reservation.md), qui dépend de l'authentification (T-013). Ce ticket détache de T-018 la partie consultation : `GET /api/salles` et `GET /api/disponibilites?date=` (architecture § 3 et § 4, composant `api.reservations`), sur le modèle de T-011 et les règles de T-012.

**Caractère provisoire de l'accès.** En attendant T-013 et la matrice d'autorisation de T-020, ces deux routes répondent sans connexion. C'est un écart temporaire au CDC (F-04 : « toute page ou appel d'API de réservation sans connexion est refusé ») : T-013 et T-020 devront les placer derrière l'authentification. Les réponses ne contiennent aucune donnée personnelle.

## Critères d'acceptation
- [ ] `GET /api/salles` renvoie les 3 salles (nom ; capacité et équipements facultatifs).
- [ ] Pour une date donnée, `GET /api/disponibilites?date=AAAA-MM-JJ` renvoie pour chacune des 3 salles les créneaux d'une heure, chacun marqué « libre » ou « occupé », **sans aucun nom ni e-mail** d'occupant.
- [ ] **Horaires** : les créneaux renvoyés vont de 8 h-9 h à 19 h-20 h (12 par salle et par jour) du lundi au vendredi ; aucun créneau n'est renvoyé pour un samedi ou un dimanche (tests sur un jour ouvré, un samedi et un dimanche).
- [ ] Une réservation présente en base pour un créneau (insérée par le test) fait apparaître ce créneau « occupé » ; les autres restent « libres ».
- [ ] Une date invalide (format incorrect) renvoie une erreur 422 explicite, sans erreur serveur.
- [ ] Le temps de `GET /api/disponibilites` est mesuré en test d'intégration et reste sous 2 s (H-05).
- [ ] Le caractère provisoire de l'accès sans connexion est signalé dans le code (commentaire renvoyant à T-013 et T-020) et une ligne est ajoutée au journal de T-020 pour que la matrice d'autorisation couvre ces deux routes.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (lecture seule, aucune donnée personnelle ; les autorisations sont revues avec T-020, revue humaine T-036)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 09:30 · agent:coordinateur · création, détachée de T-018 (priorité d'Ethan du 2026-11-25, option « Lecture seule ») · 0 h
