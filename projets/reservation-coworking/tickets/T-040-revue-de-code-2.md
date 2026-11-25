---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-040
titre: Revue de code (2/2) — front, bout en bout, Should, outillage
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:relecteur-code   # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
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

# T-040 — Revue de code (2/2) — front, bout en bout, Should, outillage

## Description
Second ticket de travail du `relecteur-code` (voir T-039) : 8 tickets de réalisation, T-022 à T-029, à 0,5 h par ticket. T-029 est écrit par Nadia dans `scripts/` (outillage commun) : la revue porte sur son diff comme pour les autres tickets. Points de contrôle du front : `textContent` uniquement, aucun script en ligne (CSP), formulaires accessibles. Pas de `depend_de` vers les tickets relus (cycle). Le coordinateur conclut (R13).

## Critères d'acceptation
- [ ] Chacun des tickets T-022 à T-029 a un avis `APPROUVÉ` ou `CHANGEMENTS_DEMANDÉS` dans sa section « Revue », et chaque reprise a été relue.
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
