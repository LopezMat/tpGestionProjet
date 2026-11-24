---
titre: Recette par un recetteur sans Claude Code (notes déposées, tickets bug par support)
statut: EN_REVUE
responsable: D
version: 0.1
maj_le: 2026-11-24
valide_par:
decision: DEC-004
id: DEC-004
date: 2026-11-24
decide_par: Ethan
projet: ESN
ticket:
modifie_une_regle: oui
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-004 — Recette par un recetteur sans Claude Code

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la demande d'Ethan du 2026-11-24. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. **Le « Pourquoi » reprend les termes de la demande : Ethan le confirme ou le complète avant de valider** (skill `tracer-decision`, étape 1).

## Contexte
Le skill `recette` (DEC-002 § 36) suppose que le salarié recetteur travaille dans une session Claude Code. C'est là que les tickets bug sont créés (`creer-ticket`) et que chaque KO est lié dans le rapport de recette.

Le recetteur humain de l'équipe (Claire) n'a pas Claude Code. Il dépose une note courte par bug dans `projets/<slug>/support/entrant/recette-AAAA-MM-JJ-NN.md` (« Source : recette (Claire) », rapport lié, SHA testé, étapes, attendu, obtenu) et ses captures dans `projets/<slug>/support/entrant/captures/`.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| (a) Le coordinateur crée lui-même les tickets bug à partir des notes | simple, pas d'agent supplémentaire | pas de dédoublonnage S2-R2 ; le coordinateur ferait un travail de qualification qui n'est pas le sien |
| **(b) L'agent `support` traite les notes, lancé par le coordinateur (retenue)** | dédoublonnage S2-R2 conservé ; circuit S2 existant (qualification, priorité selon la grille § 4) ; le recetteur reste l'auteur du ticket (`cree_par: salarie:<prenom>`) | ajuste les règles de `support` et du skill `recette` ; S2 § 3 (nommage) à aligner plus tard |
| (c) Un autre salarié saisit les bugs dans une session Claude Code | aucun changement de règle | double saisie ; l'auteur du constat se perd ; dépend de la disponibilité d'un second salarié |

## Décision
1. **Une note de recette est une remontée `support`.** Une note `support/entrant/recette-AAAA-MM-JJ-NN.md` portant « Source : recette (<Prénom>) » est traitée par l'agent `support`, lancé par le coordinateur. Elle est dédoublonnée (S2-R2) et donne un ticket `bug`.
2. **Le ticket bug porte l'auteur et les liens.** Le ticket a `cree_par: salarie:<prenom>` et cite :
   - le lien vers la note ;
   - le lien vers le rapport de recette ;
   - le lien vers chaque capture ;
   - l'exigence `F-NN` si la note la cite.

   La « Réponse proposée » est sans objet (règle 10 de `support`).
3. **Le rapport reste celui du recetteur.** Le recetteur rédige lui-même son rapport de recette (résultats, observations, verdict).
4. **Le coordinateur relaie les ids.** Il reporte les ids créés dans la colonne « Ticket bug lié » et la section « Bugs créés » du rapport, tant que celui-ci n'est pas `VALIDÉ`, et n'y écrit rien d'autre.
5. **Le temps de `support` est rattaché à un ticket.** Avant de lancer `support`, le coordinateur crée le ticket « Support utilisateurs » s'il n'existe pas.

## Pourquoi
D'après la demande d'Ethan :
- le recetteur humain n'a pas Claude Code, et ne peut donc ni suivre le skill `recette` dans une session dédiée ni créer ses tickets ;
- ses bugs doivent tout de même devenir des tickets, dédoublonnés comme toute remontée, et rester attribués à l'humain qui les a constatés.

## Impacts
- **Fichiers ou règles mis à jour :**
  - `.claude/agents/support.md` : entrées, sorties, règles 1, 4 et 8, nouvelle règle 10, contrôles, cycle des tickets ;
  - `.claude/skills/recette/SKILL.md` : description, section « Variante : recetteur sans Claude Code », règle, contrôle ;
  - `docs/CHANGELOG-REGLES.md`.
- **Non modifiés, car `VALIDÉ` (R6) :**
  - `docs/systemes/S2-maintenance.md` § 3 : la convention de nommage `AAAA-MM-JJ-<n>.md` ne cite pas `recette-*.md` ;
  - `docs/ARCHITECTURE.md` : table des agents et schéma `USERS --> support/entrant`.

  Ils seront à aligner quand un humain les repassera en `EN_REVUE`.
- **Tickets créés ou débloqués :** aucun.
