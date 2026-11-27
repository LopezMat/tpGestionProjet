---
titre: Registre des décisions humaines
statut: EN_REVUE          # journal, jamais VALIDÉ (évolue uniquement par PR, exclu de R6)
responsable: B
version: 0.17
maj_le: 2026-11-27
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
| [DEC-014](2026-11-26-DEC-014-page-qui-fait-quoi.md) | 2026-11-26 | Page de pilotage « qui fait quoi » (outil interne, régularisation de la PR #14, page générée hors Git) | VALIDÉ |
| [DEC-015](2026-11-26-DEC-015-regle-r17.md) | 2026-11-26 | ESN : règle R17 mise en œuvre (Markdown par Edit/Write uniquement, détection dans `restreindre_bash.py` pour tout appelant ; DEC-010) | VALIDÉ |
| [DEC-016](2026-11-26-DEC-016-page-le-bureau.md) | 2026-11-26 | Page « Le bureau » de la console : vue de dessus en pixel art, instantané tiré des tickets, replay des journaux (outil interne, lecture seule) | VALIDÉ |
| [DEC-017](2026-11-26-DEC-017-membres-humains-equipe.md) | 2026-11-26 | Membres humains de l'équipe projet (Ethan, Johan, Stéphane, Matthieu) dans `equipe/humains.md`, toujours présents à l'accueil du bureau, acteurs rattachés sans doublon | VALIDÉ |
| [DEC-018](2026-11-26-DEC-018-mode-direct-bureau.md) | 2026-11-26 | Mode « Direct » de la page « Le bureau » : activité en temps réel du coordinateur et des sous-agents, hook d'observation optionnel et local (`settings.local.json`), journal en liste blanche hors Git, serveur 127.0.0.1 en lecture seule | VALIDÉ |
| [DEC-019](2026-11-26-DEC-019-simulation-reconstruction-base.md) | 2026-11-26 | SIMULATION — reservation-coworking : perte de la base de production, reconstruction sans sauvegarde (T-081, option c), communication au client par Claire (T-083), retour d'expérience (T-029 critique et dépendance du GO, contrôle des sauvegardes) ; v0.2 : recommandation CNIL laissée au client (T-084), T-082 sans objet, Nadia à 30 % (T-090, option A) | VALIDÉ |
| [DEC-020](2026-11-26-DEC-020-simulation-budget-4200.md) | 2026-11-26 | SIMULATION — reservation-coworking : budget 6 000 → 4 200 € HT (scénario B en gardant F-08) : F-06 abandonné, crise et outillage commun imputés à l'ESN, alerte à 90 % et arbitrage avant tout dépassement (T-093) ; v0.2 : F-08 non abandonnable, question ouverte sur le suivi des coûts pris en charge par l'ESN ; v0.3 : condition 1 appliquée au bug T-105 (reproduction d'abord, correctif à la charge de l'ESN au titre de la garantie, T-106) | VALIDÉ |
| [DEC-021](2026-11-26-DEC-021-simulation-absence-lea-depart-hugo.md) | 2026-11-26 | SIMULATION — reservation-coworking : absence de Léa (26-27/11) et départ de Hugo (04/12) pris en compte sans réaffectation, besoins `documentation` et second relecteur sécurité renvoyés au plan de formation de l'ESN, analyses à la charge de l'ESN (T-102, T-103) | VALIDÉ |
| [DEC-022](2026-11-26-DEC-022-methodologie-retenue.md) | 2026-11-26 | Méthodologie retenue : Kanban à portes de validation humaines, livraisons incrémentales (VISION § 3.5), Definition of Done et équivalents des rituels ; aucune règle modifiée | VALIDÉ |
| [DEC-023](2026-11-26-DEC-023-imputation-esn-plan-formation.md) | 2026-11-26 | Coûts pris en charge par l'ESN (R18 : champ `imputation`, décision VALIDÉ obligatoire, coût client calculé par `tableau.py`) et projet interne `esn-interne` (R19, S1-R6, S1-R13 : plan de formation) ; migration de `reservation-coworking`, T-104 au client | VALIDÉ |
| [DEC-024](2026-11-27-DEC-024-plan-formation-initial.md) | 2026-11-27 | esn-interne : plan de formation initial, option B (T-002 à T-014, juridique par conseil externe), budget de fonctionnement 4 360 €, échéance 2027-01-15, allocations P1/P2 de Claire, Karim, Léa et Nadia, enveloppe de frais externes de 700 € HT hors budget (T-017) | VALIDÉ |
