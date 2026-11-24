---
titre: Système 2 — Suivi et maintenance
statut: EN_REVUE
responsable: B
version: 1.0
maj_le: 2026-11-23
valide_par: 
decision: DEC-001
---

# Système 2 — Suivi et maintenance

## 1. Objectifs (consigne)
- Assurer une veille technologique.
- Suivre les performances et les bugs de l'application, et transmettre ces informations à la gestion de projet après le déploiement.
- Suivre les remontées du support (problèmes signalés par les utilisateurs finaux).
- Gérer une situation de crise : perte de données, coupure du serveur, intrusion.

## 2. Acteurs
| Agent | Rôle | Entrées | Sorties |
|---|---|---|---|
| `veilleur` | veille techno et CVE sur les stacks utilisées | `architecture.md` des projets, web | `veille/AAAA-Sxx.md`, tickets sécurité ou amélioration |
| `analyste-prod` | performances et bugs en production | `/health` réel, logs et métriques simulés (`rapports/`) | tickets bug ou incident, rapport de suivi |
| `support` | qualification des remontées utilisateurs | `support/entrant/*.md` | tickets support ou bug, réponse type |
| `gestionnaire-crise` | conduite de crise | alerte ou incident, `runbooks/` | ticket incident critique, `ATTENTE_HUMAIN`, `rapports/post-mortem-*.md` |

## 3. Sources de données (décision Q3, DEC-001)
- **Réel** : `/health` de l'application en ligne (disponibilité, SHA déployé, temps de réponse).
- **Simulé** : logs et métriques d'exemple dans `projets/<slug>/rapports/`, remontées utilisateurs dans `projets/<slug>/support/entrant/`.

*Pourquoi :* une semaine ne permet pas de brancher un vrai outil de monitoring ni d'avoir de vrais utilisateurs. Des sources simulées permettent de rejouer des scénarios (bug, pic de charge, intrusion) devant le jury, tandis que le healthcheck réel prouve la mise en ligne.

## 4. Circuit des tickets bug, incident et support

```
remontée / alerte / veille → agent S2 qualifie → ticket (type, priorité proposée, reproduction)
   → priorité critique ? oui → gestionnaire-crise immédiatement + ATTENTE_HUMAIN si action sensible
                         non → triage par chef-de-projet (S1) → réalisation → S3 → déploiement
```

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

## 6. Crises et runbooks
| Situation | Runbook | S'appuie sur |
|---|---|---|
| Perte de données | `runbooks/perte-donnees.md` | sauvegarde prise avant chaque déploiement (S3) |
| Coupure du serveur | `runbooks/coupure-serveur.md` | `/health`, tableau de bord Render, rollback |
| Intrusion | `runbooks/intrusion.md` | rotation des secrets, analyse des logs, `securite` |
| Déploiement défectueux | `runbooks/rollback.md` | procédure de rollback testée (S3) |

Les runbooks arrivent dans un lot ultérieur. Les mécanismes de sauvegarde et de rollback sont à trancher au lot workflows ([ARCHITECTURE § 10](../ARCHITECTURE.md#10-à-trancher-au-lot-workflows)).

## 7. Contrôles
- Chaque ticket S2 contient : la source, les étapes de reproduction ou les preuves, la priorité proposée et sa justification.
- Chaque crise a un post-mortem lié au ticket d'incident.

## 8. Interfaces
- **→ S1** : tickets à trier ; tickets `amelioration` issus de la veille et des post-mortems.
- **→ S3** : les corrections passent par revue, tests et déploiement ; le rollback est demandé au `deployeur`.
- **← S3** : rapport de déploiement (SHA attendu), point de départ du suivi en production.
