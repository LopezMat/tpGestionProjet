---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-008
titre: Pilotage
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 9             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 5            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le: 2026-11-24        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-008 — Pilotage

## Description
Ticket de travail du `chef-de-projet` (règle 14) : le temps de pilotage du projet `reservation-coworking` y est compté, une ligne de journal par intervention.

Estimation : planification initiale 4 h (découpage, estimation, affectation, planning, budget, tri de T-006), replanification après DEC-009 1 h (planning v0.2), suivi et tri des tickets S2/S3 jusqu'à la mise en production 3 h (dont la surveillance de la marge pour l'abandon des Should), retour d'expérience 1 h.

## Critères d'acceptation
- [ ] `planning.md` produit et soumis à validation (T-007).
- [ ] Chaque intervention du `chef-de-projet` a une ligne de journal et son temps.
- [ ] `retex.md` complété en fin de projet, avec ses tickets `amelioration` et `formation`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création, passage EN_COURS · 0 h
- 2026-11-24 23:55 · agent:chef-de-projet · planification initiale : lecture du CDC v1.0, de l'architecture v1.1, de DEC-005 à DEC-008, de l'équipe et du calendrier ; création de T-007 et T-009 à T-053 ; tri de T-006 ; `planning.md` v0.1 ; budget prévisionnel et allocations proposées dans T-007 · 4 h
- 2026-11-25 09:00 · agent:chef-de-projet · replanification après DEC-009 et DEC-010 (Ethan, 2026-11-24) : `planning.md` v0.2 (sans le lot R17 ni Hugo, budget et dates recalculés, règle d'abandon des Should) ; T-027 et T-028 marqués abandonnables, dépendances après tous les Must ; T-037 lié à T-028 ; T-006, T-051, T-052, T-053 passés ANNULE ; estimation 8 → 9 h ; TABLEAU.md régénéré · 1 h
