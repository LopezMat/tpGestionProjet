---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-039
titre: Revue de code (1/2) — socle, authentification, réservations
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:relecteur-code   # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 6             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 4.3          # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-26
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25 # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-039 — Revue de code (1/2) — socle, authentification, réservations

## Description
Ticket de travail du `relecteur-code` (porte 1 de S3 ; règle 6 du `chef-de-projet`) : son temps de revue y est compté, une ligne de journal par revue. Il couvre les 12 tickets de réalisation T-010 à T-021, à 0,5 h par ticket. Le projet a deux tickets « Revue de code » au lieu d'un, pour respecter la limite de 7 h par ticket (règle 3) ; le second est T-040.

Pas de `depend_de` vers les tickets relus : l'avis `APPROUVÉ` est une condition de leur passage `TERMINE` (R13), une dépendance créerait un cycle. Points de contrôle propres à l'architecture : migrations additives (« étendre puis contracter »), aucune règle n'appelle `datetime.now()`, requêtes paramétrées seulement. Le `relecteur-code` ne passe pas ce ticket `TERMINE` : le coordinateur conclut (R13).

## Critères d'acceptation
- [ ] Chacun des tickets T-010 à T-021 a un avis `APPROUVÉ` ou `CHANGEMENTS_DEMANDÉS` dans sa section « Revue », et chaque reprise a été relue.
- [ ] Une ligne de journal par revue ici, avec le ticket relu, l'avis et le temps.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 15:00 · agent:relecteur-code · revue T-010 : APPROUVÉ · 0.5 h
- 2026-11-25 21:00 · agent:relecteur-code · revue T-010 (passe 2, après NON CONFORME du testeur) : APPROUVÉ · 0.6 h
- 2026-11-25 21:00 · agent:relecteur-code · revue T-056 : APPROUVÉ · 0.3 h
- 2026-11-25 23:00 · coordinateur pour agent:relecteur-code · revue de T-012 : APPROUVÉ, revue humaine non requise (le relecteur n'a pas accès à ce ticket, temps noté par le coordinateur) · 0.75 h
- 2026-11-25 23:30 · coordinateur pour agent:relecteur-code · revue de T-011 (commit 2852fe7) : APPROUVÉ, revue humaine non requise · 0.75 h
- 2026-11-25 23:55 · coordinateur pour agent:relecteur-code · revue de T-054 (commit 4674c76) : APPROUVÉ, revue humaine requise : oui (ticket compagnon T-068) · 0.8 h
- 2026-11-26 · coordinateur pour agent:relecteur-code · revue de T-055 (commit dc53a1d) : APPROUVÉ, revue humaine non requise ; imputée ici comme T-054 (T-040 ne couvre que T-022 à T-029) · 0.6 h
