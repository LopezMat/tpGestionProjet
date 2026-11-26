---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-104
titre: SIMULATION — Support utilisateurs
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:support      # agent:<nom> | salarie:<prenom>
competence_requise: support-utilisateur (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Ticket de travail de l'agent `support` créé pour le scénario 4 (S2) du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-104 — SIMULATION — Support utilisateurs

## Description
Ticket de travail de l'agent `support` sur le projet ([DEC-004](../../../docs/decisions/2026-11-24-DEC-004-recette-sans-claude-code.md), point 5 : créé par le coordinateur avant le premier lancement de `support`). Il porte le temps passé à qualifier et dédoublonner les remontées de `support/entrant/`, y compris les notes de recette `recette-AAAA-MM-JJ-NN.md`. Il reste ouvert pendant la vie du projet ; chaque passage ajoute une ligne de journal et met à jour `temps_passe_h`.

Premier passage : note [recette-2026-11-26-01.md](../support/entrant/recette-2026-11-26-01.md), qui est une SIMULATION.

## Critères d'acceptation
- [ ] Chaque remontée traitée est dédoublonnée (S2-R2), puis devient un ticket ou une ligne de journal sur un ticket existant.
- [ ] Chaque passage a une ligne de journal et `temps_passe_h` à jour.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 21:00 · agent:coordinateur · SIMULATION · création (DEC-004, point 5) avant le premier lancement de `support` · 0 h
- 2026-11-26 23:10 · agent:support · SIMULATION · A_FAIRE → EN_COURS (premier passage, note recette-2026-11-26-01) · 0 h
- 2026-11-26 23:10 · agent:support · SIMULATION · qualification et dédoublonnage de support/entrant/recette-2026-11-26-01.md : aucun doublon (recherches « Canigou », « Aucun créneau », consultation et disponibilités, T-054, T-055) ; ticket T-105 créé (bug, cree_par salarie:claire, F-01 Must, priorité haute proposée, assigné proposé agent:dev-frontend) ; information manquante (rapport de recette, URL) signalée au coordinateur · 0,5 h
