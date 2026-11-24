---
titre: Système 2 — Suivi et maintenance
statut: EN_REVUE
responsable: B
version: 1.2
maj_le: 2026-11-24
valide_par: 
decision: 
---

# Système 2 — Suivi et maintenance

> Responsable du fichier : B (en-tête) · responsable du système : D (agents S2, runbooks, sonde ; ARCHITECTURE § 12).

## 1. Objectifs (consigne)
- Assurer une veille technologique.
- Suivre les performances et les bugs de l'application, et transmettre ces informations à la gestion de projet après le déploiement.
- Suivre les remontées du support (problèmes signalés par les utilisateurs finaux).
- Gérer une situation de crise : perte de données, coupure du serveur, intrusion.

## 2. Acteurs
| Agent | Rôle | Entrées | Sorties |
|---|---|---|---|
| `veilleur` | veille techno et CVE sur les stacks utilisées | `architecture.md` des projets, web | `veille/AAAA-Sxx.md`, tickets sécurité ou amélioration |
| `analyste-prod` | performances et bugs en production | `/health` réel, mesuré uniquement par la sonde `scripts/sonde_sante.py` ; `rapports/logs-*.log` et `rapports/metriques-*.csv` (simulés) ; dernier rapport de déploiement (SHA, URL) | tickets bug ou incident, `rapports/suivi-AAAA-MM-JJ.md` (template [rapport-suivi](../../templates/rapport-suivi.md)) |
| `support` | qualification des remontées utilisateurs | `support/entrant/*.md` | tickets support ou bug, réponse type |
| `gestionnaire-crise` | conduite de crise | alerte ou incident, `runbooks/` | ticket incident critique, `ATTENTE_HUMAIN`, `rapports/post-mortem-*.md` |

## 3. Sources de données (décision Q3, DEC-001)
- **Réel** : `/health` de l'application en ligne (disponibilité, SHA déployé, temps de réponse).
- **Simulé** : logs et métriques d'exemple dans `projets/<slug>/rapports/`, remontées utilisateurs dans `projets/<slug>/support/entrant/`.

**Conventions de nommage des données simulées** (les données elles-mêmes arrivent avec le projet de démonstration, lot 6) :
- `projets/<slug>/support/entrant/AAAA-MM-JJ-<n>.md` : date, canal, message ; aucune donnée personnelle réelle ;
- `projets/<slug>/rapports/logs-AAAA-MM-JJ.log` ;
- `projets/<slug>/rapports/metriques-AAAA-MM-JJ.csv`.

*Pourquoi :* sans convention de nommage, les agents S2 ne retrouvent pas leurs entrées.

*Pourquoi :* une semaine ne permet pas de brancher un vrai outil de monitoring ni d'avoir de vrais utilisateurs. Des sources simulées permettent de rejouer des scénarios (bug, pic de charge, intrusion) devant le jury, tandis que le healthcheck réel prouve la mise en ligne.

## 4. Circuit des tickets bug, incident et support

```
remontée / alerte / veille → agent S2 qualifie → ticket (type, priorité proposée, reproduction)
   → priorité critique ? oui → gestionnaire-crise immédiatement + ATTENTE_HUMAIN si action sensible
                         non → triage par chef-de-projet (S1) → réalisation → S3 → déploiement
```

Une **régression constatée après un déploiement vérifié** (SHA en ligne = SHA attendu) suit S2-R7 : décision humaine « rollback ou correctif ».

**Grille de priorité proposée par S2 :**
| Priorité | Exemples |
|---|---|
| critique | production indisponible, perte ou fuite de données, intrusion avérée |
| haute | fonctionnalité principale en échec, faille exploitable, dégradation forte des performances |
| normale | bug avec contournement, CVE sans exploitation connue |
| basse | cosmétique, amélioration suggérée |

## 5. Règles

**S2-R1 · Un agent S2 ne corrige jamais lui-même : il crée un ticket.**
*Pourquoi :* la correction doit passer par la revue, les tests et le déploiement contrôlé de S3 ; une correction directe en production contournerait tous les contrôles.

**S2-R2 · Chaque remontée support est dédoublonnée** (recherche des tickets existants) avant toute création de ticket. Un doublon est lié au ticket existant.
*Pourquoi :* éviter de compter deux fois le même problème dans la charge et le tableau de bord.

**S2-R3 · Un incident `critique` est pris immédiatement par le `gestionnaire-crise`**, qui déroule le runbook correspondant, sans attendre le triage S1.
*Pourquoi :* en crise, le temps de réaction prime ; S1 est informé par le ticket.

**S2-R4 · Toute action sensible sur les données** (restauration, purge, coupure volontaire, rotation de secrets) **exige un ticket `ATTENTE_HUMAIN`**.
*Pourquoi :* ce sont des actions irréversibles ; la vision les réserve explicitement à la validation humaine.

**S2-R5 · Chaque crise donne lieu à un post-mortem sans blâme** dans les 2 jours ouvrés. Ses actions correctives deviennent des tickets, dont des tickets `amelioration` si un agent ou une règle est en cause.
*Pourquoi :* la crise doit améliorer le système au lieu de se répéter.

**S2-R6 · La veille est hebdomadaire et ciblée** sur les stacks réellement utilisées (lues dans les `architecture.md`). Une CVE qui touche une dépendance en production devient un ticket au moins `haute`.
*Pourquoi :* une veille générique ne sert à rien ; c'est le lien avec ce qui tourne réellement qui lui donne de la valeur.

**S2-R7 · Une régression constatée après un déploiement vérifié donne un ticket `decision` « rollback ou correctif »** en `ATTENTE_HUMAIN`, préparé par l'agent S2 qui la constate (ou par le `gestionnaire-crise` si elle est critique). Le rollback sans nouveau GO (S3-R6) ne vise que l'échec de la vérification en ligne.
*Pourquoi :* la version en ligne a fait l'objet d'un GO humain ; revenir dessus est une décision humaine, et la distinction évite qu'un agent annule une mise en production validée.

## 6. Crises et runbooks
| Situation | Runbook | S'appuie sur |
|---|---|---|
| Perte de données | [runbooks/perte-donnees.md](../../runbooks/perte-donnees.md) | sauvegarde prise avant chaque déploiement (S3) |
| Coupure du serveur | [runbooks/coupure-serveur.md](../../runbooks/coupure-serveur.md) | `/health` (sonde), état des conteneurs constaté par l'humain d'exploitation (`docker compose ps`, `logs`), rollback |
| Intrusion | [runbooks/intrusion.md](../../runbooks/intrusion.md) | rotation des secrets, analyse des logs, `securite` |
| Déploiement défectueux | [runbooks/rollback.md](../../runbooks/rollback.md) | procédure de rollback testée (S3, `scripts/rollback_local.py`), skill `verifier-prod` et ses fichiers d'état `rapports/verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json`, un par vérification |

Les 4 runbooks sont livrés (Lot 2, D). Le `gestionnaire-crise` reçoit aussi les **incidents de rollback** créés par le `deployeur` après un échec de vérification (S3-R6). **Il ne lance jamais de rollback lui-même** : il le demande au `deployeur` via le coordinateur (R1).
*Pourquoi :* un seul agent déclenche les déploiements, après les contrôles de S3 ; le gestionnaire de crise diagnostique et prépare les décisions.

Les mécanismes de sauvegarde et de rollback sont tranchés par [DEC-003](../decisions/2026-11-24-DEC-003-production-locale-docker.md) ([ARCHITECTURE § 10](../ARCHITECTURE.md#10-décisions-du-lot-5--vérification-sauvegardes-rollback)) :
- une sauvegarde `pg_dump` est prise avant chaque déploiement, dans `deploiement/local/<slug>/sauvegardes/` (ignoré par Git), et les 10 dernières sont gardées ;
- le rollback relance l'image étiquetée du SHA précédent, puis la vérifie ;
- une restauration de données reste toujours une décision humaine (S2-R4, runbook `perte-donnees`).

## 7. Contrôles
- Chaque ticket S2 contient : la source, les étapes de reproduction ou les preuves, la priorité proposée et sa justification.
- Chaque crise a un post-mortem lié au ticket d'incident.

## 8. Interfaces
- **→ S1** : tickets à trier ; tickets `amelioration` issus de la veille et des post-mortems.
- **→ S3** : les corrections passent par revue, tests et déploiement ; le rollback est demandé au `deployeur`.
- **← S3** : rapport de déploiement (SHA attendu, URL), point de départ du suivi en production ; l'`analyste-prod` peut constater la version en ligne avec la sonde ; incidents de rollback créés par le `deployeur`.
