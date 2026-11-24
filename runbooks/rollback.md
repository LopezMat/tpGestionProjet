---
titre: Runbook — Déploiement défectueux et rollback
statut: EN_REVUE
responsable: D
version: 0.2
maj_le: 2026-11-24
valide_par:
decision:
---
<!-- Runbook ESN · système S2 · responsable : D · Lot 2 · structure commune décrite dans docs/a-integrer/lot2-D.md -->

# Runbook — Déploiement défectueux et rollback

> Conduit par l'agent `gestionnaire-crise` ([.claude/agents/gestionnaire-crise.md](../.claude/agents/gestionnaire-crise.md)). Le rollback lui-même est exécuté par le `deployeur` ([.claude/agents/deployeur.md](../.claude/agents/deployeur.md), règle 4). Outil de preuve : skill [verifier-prod](../.claude/skills/verifier-prod/SKILL.md). Règles applicables : S3-R5, S3-R6, S2-R1 à S2-R5, R7, R13.

## Déclencheurs et sévérité
| Situation | Sévérité | Origine |
|---|---|---|
| `verifier-prod` en `ÉCHEC` (code 1) après un déploiement ; le `deployeur` a lancé le rollback et créé l'incident | `critique` | `deployeur` |
| Régression constatée **après** un déploiement vérifié (`EN LIGNE ET À JOUR`) : fonctionnalité principale cassée, erreurs en hausse | `critique` ou `haute` | `analyste-prod`, `support` |
| SHA en ligne différent du dernier déploiement réussi, sans rapport qui l'explique | `haute` | `analyste-prod` |

## Rôles
| Rôle | Qui | Ce qu'il fait |
|---|---|---|
| Conduite | `agent:gestionnaire-crise` | diagnostic, vérification du rollback, décisions à préparer |
| Rollback du code | `agent:deployeur` | redéploie la version précédente, puis relance `verifier-prod` (confirmation `ask` de l'humain) |
| Orchestration | coordinateur | relaie les demandes de rollback au `deployeur` (R1), présente les décisions |
| Revue humaine | salarié `ci-cd` ≥ confirme (aujourd'hui : Nadia) | revue des déploiements et rollbacks (AF3) |

## 1. Détection
- **Fichier d'état de `verifier-prod`**, un par vérification : `projets/<slug>/rapports/verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json` (ligne `ETAT_VERIFICATION` du rapport), champ `resultat` à `ÉCHEC`. Ses `tentatives` donnent le diagnostic :

  | Résultat des tentatives | Lecture probable |
  |---|---|
  | `SHA_DIFFERENT` jusqu'au bout | l'ancienne version sert encore : build échoué ou non déclenché, mauvais SHA demandé |
  | `INJOIGNABLE` | l'app ne démarre plus, ou le service est arrêté → voir aussi [coupure-serveur.md](coupure-serveur.md) |
  | `HTTP_5xx` | crash au démarrage (configuration, variable manquante, migration) |
  | `JSON_INVALIDE` | `/health` cassé ou ne renvoie plus `commit` |

- Rapport de déploiement : section « Rollback » (déclenché, version restaurée, vérification après rollback, ticket incident).
- Après un déploiement réussi : rapport de suivi de l'`analyste-prod`, remontées du `support`.

## 2. Minutes 0–15
| Minute | Action | Par |
|---|---|---|
| 0 | Ticket `incident` `EN_COURS`, runbook noté au journal | agent |
| 0–5 | Lire le rapport de déploiement (SHA attendu, version précédente, sauvegarde) et le fichier d'état du SHA attendu ; classer le symptôme (tableau § 1) | agent |
| 5–8 | **Le rollback est-il fait et vérifié ?** La section « Rollback » du rapport cite le code retour de `rollback_local.py` (0 attendu), et le fichier d'état **du rollback** (`verifier-prod-<sha7 précédent>-<horodatage>.json`, le plus récent) doit avoir `resultat: EN LIGNE ET À JOUR`. Sinon, confirmer par la sonde : `python scripts/sonde_sante.py --url <url_prod> --sha <sha précédent>` | agent |
| 5–8 | Si le rollback n'a pas été lancé (régression après un déploiement vérifié) : préparer la décision « rollback ou correctif » (§ 4) | agent |
| 8–12 | Une **migration de données** faisait-elle partie du déploiement (`architecture.md` § 4 et § 8, diff du SHA) ? Si oui, le rollback du code peut ne pas suffire → [perte-donnees.md](perte-donnees.md) | agent |
| 12–15 | Rollback en échec, ou service toujours indisponible → [coupure-serveur.md](coupure-serveur.md) et escalade immédiate ; sinon, préparer le ticket `bug` du correctif ; message de retour | agent |

**Rollback** (par le `deployeur`, confirmation humaine `ask`) : `python scripts/rollback_local.py --projet <slug>`, qui relance l'image `esn-<slug>:<sha précédent>` sans rebuild puis la vérifie. Codes : 0 restaurée et vérifiée ; 1 rollback non vérifié (→ [coupure-serveur.md](coupure-serveur.md), escalade immédiate) ; 2 précondition (image absente, pas de version précédente vérifiée, dernier déploiement vérifié sans `--sha`) ; **3 en cours : relancer exactement la commande `verifier_prod` affichée**, l'état est repris. Le script ne restaure jamais de données.

## 3. Escalade
| Niveau | Qui | Quand |
|---|---|---|
| 1 | coordinateur et humain de l'équipe | dès la prise de l'incident |
| 2 | revue humaine `ci-cd` | rollback en échec, ou décision de rollback après un déploiement vérifié |
| 3 | salarié `relation-client` | indisponibilité ou régression visible par le client |

## 4. Points de décision humaine
| Décision | Options | Qui tranche | Trace |
|---|---|---|---|
| Rollback après un déploiement **vérifié** (régression) | (a) rollback vers le SHA précédent ; (b) correctif rapide par le circuit S3 ; (c) laisser en l'état avec contournement | humain : on revient sur un GO | ticket `decision` + `DEC-NNN` |
| Restaurer les données après une migration | voir [perte-donnees.md](perte-donnees.md) | humain (S2-R4) | ticket `decision` + `DEC-NNN` |
| Redéployer le SHA corrigé | nouveau GO mise en production (un GO vaut pour **un** SHA) | humain (S3-R3) | ticket `decision` GO + `DEC-NNN` |

Le rollback du code **après un échec de vérification** n'attend pas de nouveau GO (`deployeur`, règle 4) ; la confirmation `ask` de la commande reste demandée.

## 5. Retour à la normale
- [ ] Le SHA en ligne est le SHA précédent, prouvé par `verifier-prod` (code 0) ou par la sonde (`DISPONIBLE ET À JOUR`).
- [ ] Le ticket « Déploiement » est `BLOQUE` avec `bloque_par: rollback effectué, incident T-NNN` (il ne passe jamais `TERMINE` sur un SHA qui n'est pas en ligne, R13).
- [ ] Un ticket `bug` décrit le défaut du SHA refusé, pour le circuit S3, puis un nouveau GO.
- [ ] Ticket `incident` → `EN_REVUE` une fois le post-mortem rédigé.

## 6. Post-mortem
Dans les **2 jours ouvrés** (S2-R5), sans blâme, selon [templates/post-mortem.md](../templates/post-mortem.md) : `projets/<slug>/rapports/post-mortem-AAAA-MM-JJ-rollback.md`. Questions à traiter : pourquoi les portes 1 à 3 de S3 n'ont pas arrêté le défaut, et le rollback a-t-il fonctionné comme prévu ? Chaque action corrective devient un ticket.

## Ce que les agents ne font jamais
Le `gestionnaire-crise` ne lance jamais de déploiement ni de rollback lui-même (il le demande au `deployeur` via le coordinateur) ; aucun agent ne restaure de données ni ne pousse de code (S2-R1, S2-R4, S3-R3).

## Points ouverts
- **Rapport du test de rollback (S3-R7)** sur le projet de démonstration : lot 6, avant la soutenance. Le mécanisme est tranché par [DEC-003](../docs/decisions/2026-11-24-DEC-003-production-locale-docker.md) ([ARCHITECTURE § 10](../docs/ARCHITECTURE.md#10-décisions-du-lot-5--vérification-sauvegardes-rollback)) : relance de l'image étiquetée du SHA précédent ; sauvegarde `pg_dump` avant chaque déploiement ; vérification toutes les 5 s pendant 120 s au plus. Il est rejoué automatiquement par le test réel de `scripts/test_prod_locale.py` (CI).
- Une **migration de données** rend le retour à l'image précédente risqué : à signaler dans `architecture.md` § 8 (règle 7 de l'`architecte`).
