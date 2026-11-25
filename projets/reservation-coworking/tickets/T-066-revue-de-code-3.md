---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-066
titre: Revue de code (3/3) — correctifs de l'audit d'incrément
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:relecteur-code   # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.8          # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-066 — Revue de code (3/3) — correctifs de l'audit d'incrément

## Description
Ticket de travail du `relecteur-code` (porte 1 de S3 ; règle 6 du `chef-de-projet`) pour les 6 tickets de réalisation issus du triage du 2026-11-25 : T-058, T-060, T-061, T-062, T-063 et T-065, à 0,5 h par ticket ; ajout du triage de T-054 (2026-11-25, 14 h 45) : T-069, T-070, T-071 et T-072, soit 10 tickets et 5 h (T-065 a grossi de 1,5 h mais reste une revue d'environ 0,5 h). T-039 (6 h, T-010 à T-021) atteindrait 9 h s'il les recevait, au-delà de la limite de 7 h par ticket (règle 3).

Pas de `depend_de` vers les tickets relus (dépendance circulaire, R13). T-058 porte sur l'outillage commun : la revue de code complète celle de C sur la PR et la revue humaine de Karim (T-059). Le `relecteur-code` ne passe pas ce ticket `TERMINE` : le coordinateur conclut (R13).

## Critères d'acceptation
- [ ] Chacun des tickets T-058, T-060, T-061, T-062, T-063, T-065, T-069, T-070, T-071 et T-072 a un avis `APPROUVÉ` ou `CHANGEMENTS_DEMANDÉS` dans sa section « Revue », et chaque reprise a été relue (ou le ticket est `ANNULE`).
- [ ] Une ligne de journal par revue ici, avec le ticket relu, l'avis et le temps.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage des suites de T-054 : T-069, T-070, T-071 et T-072 ajoutés ; estimation 3 → 5 h (toujours sous 7 h, règle 3). Temps compté dans T-008 · 0 h
- 2026-11-25 · coordinateur pour agent:relecteur-code · revue de T-063 (commit b8b0004) : APPROUVÉ, revue humaine requise : oui (T-064) · 0.4 h
- 2026-11-25 · coordinateur pour agent:relecteur-code · revue de T-062 (commit 16282cc) : APPROUVÉ, revue humaine non requise · 0.4 h
