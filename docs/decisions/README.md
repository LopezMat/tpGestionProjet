---
titre: Registre des décisions humaines
statut: EN_REVUE          # journal, jamais VALIDÉ (évolue uniquement par PR, exclu de R6)
responsable: B
version: 0.2
maj_le: 2026-11-23
valide_par:
decision:
---

# Registre des décisions humaines

Toute décision humaine est tracée ici : validation d'un document, arbitrage, événement d'équipe, GO de mise en production, modification de règle.
*Pourquoi :* chaque choix doit être justifiable à l'oral, et la CI vérifie que chaque document `VALIDÉ` pointe vers une décision existante.

## Nommage
- **Fichier** : `AAAA-MM-JJ-DEC-NNN-<sujet-court>.md`, par exemple `2026-11-24-DEC-002-validation-cdc-reservation.md`.
- **Id** : `DEC-NNN`, numéroté de façon séquentielle sur tout le dépôt, sans jamais réutiliser un numéro.
- **Template** : [templates/decision.md](../../templates/decision.md).

## Procédure de validation d'un document (humain)
1. Relire le document en `EN_REVUE`.
2. Créer le fichier de décision (une décision peut couvrir plusieurs documents).
3. Dans l'en-tête du document, **modifier soi-même**, dans son éditeur et pas via Claude : `statut: VALIDÉ`, `valide_par: <prénom>`, `decision: DEC-NNN`, puis incrémenter `version`.
4. Si un ticket `ATTENTE_HUMAIN` attendait cette décision : y renseigner `decision: DEC-NNN`, puis le débloquer.
5. Si la décision modifie une règle : `modifie_une_regle: oui` et ajouter une entrée dans [CHANGELOG-REGLES.md](../CHANGELOG-REGLES.md) (R11).
6. Commit dans une PR.

## Modifier un document VALIDÉ
Un document `VALIDÉ` est figé pour les agents (R6). Pour le faire évoluer, un humain le repasse lui-même en `EN_REVUE` ; les agents peuvent alors le modifier, puis il est revalidé avec une nouvelle décision.

## Index
| Id | Date | Sujet | Statut |
|---|---|---|---|
| [DEC-001](2026-11-23-DEC-001-arbitrages-plan-initial.md) | 2026-11-23 | Arbitrages du plan initial (Lot 1) | EN_REVUE |
