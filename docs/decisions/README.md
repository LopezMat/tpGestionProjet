---
titre: Registre des décisions humaines
statut: EN_REVUE          # journal, jamais VALIDÉ (évolue uniquement par PR, exclu de R6)
responsable: B
version: 0.11
maj_le: 2026-11-26
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
| [DEC-001](2026-11-23-DEC-001-arbitrages-plan-initial.md) | 2026-11-23 | Arbitrages du plan initial (Lot 1) | VALIDÉ |
| [DEC-002](2026-11-24-DEC-002-integration-lot2-recette.md) | 2026-11-24 | Intégration du Lot 2, recette humaine, listes blanches Bash S2 | VALIDÉ |
| [DEC-003](2026-11-24-DEC-003-production-locale-docker.md) | 2026-11-24 | Production locale Docker et workflows de contrôle (lot 5) | VALIDÉ |
| [DEC-004](2026-11-24-DEC-004-recette-sans-claude-code.md) | 2026-11-24 | Recette par un recetteur sans Claude Code (notes déposées, tickets bug par `support`) | VALIDÉ |
| [DEC-005](2026-11-24-DEC-005-interlocutrice-client-coworking.md) | 2026-11-24 | reservation-coworking : Claire interlocutrice client, allocation 10 % (T-002) | VALIDÉ |
| [DEC-006](2026-11-24-DEC-006-validation-cdc-coworking.md) | 2026-11-24 | reservation-coworking : réponses du client, arbitrages et validation du CDC v0.4 (T-003) | VALIDÉ |
| [DEC-007](2026-11-24-DEC-007-choix-techniques-coworking.md) | 2026-11-24 | reservation-coworking : choix techniques, stack A1, sauvegarde quotidienne, limite de démonstration (T-005) | VALIDÉ |
| [DEC-008](2026-11-24-DEC-008-architecture-coherente-coworking.md) | 2026-11-24 | reservation-coworking : architecture v1.1 cohérente avec DEC-007, purge au déploiement, fin de démonstration (T-004) | VALIDÉ |
| [DEC-009](2026-11-24-DEC-009-budget-delais-coworking.md) | 2026-11-24 | reservation-coworking : budget, délais et allocations, Should abandonnables, lot R17 sorti du projet (T-007) | VALIDÉ |
| [DEC-010](2026-11-24-DEC-010-principe-r17.md) | 2026-11-24 | ESN : règle R17 adoptée sur le principe, PR de règles après le projet client (T-050) | VALIDÉ |
| [DEC-011](2026-11-25-DEC-011-increment-consultation-coworking.md) | 2026-11-25 | reservation-coworking : incrément socle et consultation des disponibilités avant la soutenance, écart provisoire à F-04 (T-054, T-055) | VALIDÉ |
| [DEC-012](2026-11-25-DEC-012-console-consultation.md) | 2026-11-25 | Console de consultation de l'ESN (outil interne, lecture seule) | VALIDÉ |
| [DEC-013](2026-11-25-DEC-013-role-postgresql-coworking.md) | 2026-11-25 | reservation-coworking : rôle PostgreSQL applicatif non superutilisateur, propriétaire de la base, repli `absent` supprimé (T-057, option A) | VALIDÉ |
| [DEC-014](2026-11-26-DEC-014-page-qui-fait-quoi.md) | 2026-11-26 | Page de pilotage « qui fait quoi » (outil interne, régularisation de la PR #14, page générée hors Git) | EN_REVUE |
