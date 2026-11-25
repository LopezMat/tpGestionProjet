---
titre: Interlocutrice client et allocation initiale du projet reservation-coworking
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-24
valide_par:     Ethan            # rempli par l'humain qui valide
decision: DEC-005           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-005
date: 2026-11-24
decide_par: Ethan
projet: reservation-coworking
ticket: T-002
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-005 — Interlocutrice client et allocation initiale (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision d'Ethan du 2026-11-24 (« T-002 : Claire à 10 %, interlocutrice client »). Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. Le « Pourquoi » est celui formulé par Ethan le 2026-11-24 (skill `tracer-decision`, étape 1).

## Contexte
Nouveau projet `reservation-coworking` (Coworking Les Arcades, Perpignan) : réservation en ligne de 3 salles de réunion, budget 6 000 € HT, mise en ligne au plus tard le 2026-12-18. Le skill `nouveau-projet` a créé le ticket [T-002](../../projets/reservation-coworking/tickets/T-002-interlocuteur-client-et-allocation.md) : le contact client relève d'un salarié (AF1) et l'allocation entre projets est une décision humaine (S1-R10).

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| **1. Claire à 10 % (3,5 h/semaine) (retenue)** | seule salariée `relation-client` (expert) ; disponible, allocation libre ; coût contenu (≈ 1 100 €, ~18 % du budget) | peu de marge si la recette ou les échanges client s'allongent |
| 2. Claire à 20 % (7 h/semaine) | plus de marge pour la recette et les échanges avant la deadline | ≈ 2 200 €, ~37 % du budget |
| 3. Un autre salarié | réduit la dépendance à Claire | aucun autre membre n'a `relation-client` (AF1 non satisfait) ; ticket `formation` nécessaire |

## Décision
1. **Claire est l'interlocutrice client du projet `reservation-coworking`** côté ESN : cadrage, réponses aux questions du CDC, recette avec le client.
2. **Son allocation au projet est de 10 %** de sa capacité (3,5 h/semaine) : `allocation: { reservation-coworking: 10 }` dans `equipe/membres/claire.md`.
3. `projet.md` porte `salaries_affectes: [claire]`.
4. L'allocation peut être relevée par une nouvelle décision humaine si la recette ou les échanges client l'exigent (AF9).

## Pourquoi
Claire est la seule salariée avec la compétence `relation-client` (AF1) ; 10 % suffisent pour un projet court centré sur quelques échanges avec la gérante. *(Ethan, 2026-11-24)*

## Impacts
- Fichiers ou règles à mettre à jour (par le coordinateur, après le déblocage de T-002) :
  - `equipe/membres/claire.md` : `allocation: { reservation-coworking: 10 }` ;
  - `projets/reservation-coworking/projet.md` : `salaries_affectes: [claire]`, ligne dans l'historique des décisions.
- Tickets créés ou débloqués : T-002 débloqué par l'humain (`decision: DEC-005`).
- Coût : 78,57 €/h, imputé au temps réellement passé sur des tickets ; capacité restante de Claire : 90 %.
