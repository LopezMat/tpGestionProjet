---
titre: Runbook — Coupure du serveur
statut: EN_REVUE
responsable: D
version: 0.3
maj_le: 2026-11-24
valide_par:
decision:
---
<!-- Runbook ESN · système S2 · responsable : D · Lot 2 · structure commune décrite dans docs/a-integrer/lot2-D.md -->

# Runbook — Coupure du serveur

> Conduit par l'agent `gestionnaire-crise` ([.claude/agents/gestionnaire-crise.md](../.claude/agents/gestionnaire-crise.md)). Règles applicables : S2-R1 à S2-R5 ([S2](../docs/systemes/S2-maintenance.md)), R7, S3-R6.

## Déclencheurs et sévérité
| Situation | Sévérité |
|---|---|
| `/health` injoignable ou en erreur 5xx sur plusieurs mesures espacées | `critique` |
| Réponses très lentes (sonde `DÉGRADÉ`) mais service rendu | `haute` (pas de crise : triage S1) |
| Une seule mesure en échec, puis retour normal | aucune (conteneur en redémarrage ou déploiement en cours) |

## Rôles
| Rôle | Qui | Ce qu'il fait |
|---|---|---|
| Conduite | `agent:gestionnaire-crise` | diagnostic, journal, décisions à préparer |
| Orchestration | coordinateur | lance les agents, présente les décisions (R7) |
| Exploitation | salarié `ci-cd` / `linux` ≥ confirme (aujourd'hui : Nadia) | constate l'état des conteneurs (`docker compose -p esn-<slug> -f deploiement/docker-compose.yml ps`, `logs app`, `logs db`), redémarre après décision |
| Rollback | `agent:deployeur` | redéploie la version précédente si un déploiement est en cause |
| Communication | salarié `relation-client` (aujourd'hui : Claire) | informe le client, après décision |

## 1. Détection
- `analyste-prod` : la sonde rend `INDISPONIBLE` (code 4) sur des mesures répétées.
- `support` : plusieurs remontées « le site ne répond plus ».
- `deployeur` : `verifier-prod` en `ÉCHEC` avec des tentatives `INJOIGNABLE` ou `HTTP_5xx` → voir d'abord [rollback.md](rollback.md).

## 2. Minutes 0–15
| Minute | Action | Par |
|---|---|---|
| 0 | Ticket `incident` `EN_COURS`, runbook noté au journal | agent |
| 0–5 | **Confirmer** : `python scripts/sonde_sante.py --url <url_prod> --sha <sha du dernier déploiement réussi> --mesures 6 --intervalle 30`. Un conteneur qui redémarre, ou une base qui démarre, ne répond pas pendant quelques secondes : **ne jamais conclure sur une seule mesure** | agent |
| 5–8 | **Un déploiement est-il en cause ?** dernier `rapports/deploiement-*.md` (heure, SHA, code retour de `deployer_local.py`), `git log -5`, `gh run list` (CI du commit déployé). Si oui → [rollback.md](rollback.md) | agent |
| 8–12 | Classer le symptôme : `INJOIGNABLE` (conteneur arrêté, Docker Desktop arrêté, port occupé), `HTTP_5xx` (crash applicatif, base injoignable), `JSON_INVALIDE` (`/health` cassé) ; lire les logs simulés autour de l'heure du premier échec | agent |
| 8–12 | Demander à l'humain d'exploitation l'état des conteneurs : `docker compose -p esn-<slug> -f deploiement/docker-compose.yml ps` (statut, redémarrages), `logs app` et `logs db` autour de l'heure du premier échec, état de Docker Desktop et de l'espace disque. **Les agents n'ont pas accès à Docker** (hook `restreindre_bash.py`) | agent, via coordinateur |
| 12–15 | Préparer les décisions (§ 4) ; ticket `incident` → `BLOQUE` si une décision est attendue ; message de retour | agent |

## 3. Escalade
| Niveau | Qui | Quand |
|---|---|---|
| 1 | coordinateur et humain de l'équipe | dès la confirmation de l'indisponibilité |
| 2 | salarié d'exploitation | pour le constat Docker (`ps`, `logs`) et le redémarrage |
| 3 | salarié `relation-client` | indisponibilité de plus de 30 min, ou visible par le client |

## 4. Points de décision humaine
| Décision | Options | Qui tranche | Trace |
|---|---|---|---|
| Redémarrer le service | redémarrer l'app (`docker compose -p esn-<slug> -f deploiement/docker-compose.yml restart app`) / redémarrer Docker Desktop puis `docker compose -p esn-<slug> -f deploiement/docker-compose.yml up -d` / rollback si un déploiement est en cause | humain | ticket `decision` + `DEC-NNN` |
| Coupure volontaire ou page de maintenance | oui / non, durée | humain (S2-R4) | ticket `decision` + `DEC-NNN` |
| Rollback après un déploiement vérifié | rollback / correctif (voir [rollback.md](rollback.md)) | humain | ticket `decision` + `DEC-NNN` |
| Hébergement de secours (autre poste avec Docker, autre hébergeur) | oui / non | humain (choix technique) | ticket `decision` + `DEC-NNN` |
| Informer le client | message proposé par l'agent | humain | ticket `decision` + `DEC-NNN` |

## 5. Retour à la normale
- [ ] La sonde rend `DISPONIBLE ET À JOUR` sur au moins 3 mesures, avec le SHA du dernier déploiement réussi (ou le SHA précédent après un rollback).
- [ ] La cause immédiate est notée au journal (redémarrage du conteneur, Docker arrêté, disque plein, rollback…).
- [ ] L'`analyste-prod` reprend son suivi normal (rapport de suivi suivant).
- [ ] Ticket `incident` → `EN_REVUE` une fois le post-mortem rédigé.

## 6. Post-mortem
Dans les **2 jours ouvrés** (S2-R5), sans blâme, selon [templates/post-mortem.md](../templates/post-mortem.md) : `projets/<slug>/rapports/post-mortem-AAAA-MM-JJ-coupure-serveur.md`. Questions à traiter : délai de détection, fiabilité du poste de production locale (Docker, disque, mise en veille du poste), besoin d'une alerte plus tôt. Chaque action corrective devient un ticket.

## Ce que les agents ne font jamais
Redémarrer, couper ou reconfigurer le service, déclencher un déploiement en dehors du `deployeur`, contacter le client (S2-R1, S2-R4, AF1).

## Points ouverts
- Production locale Docker ([DEC-003](../docs/decisions/2026-11-24-DEC-003-production-locale-docker.md)). Le poste de démonstration ne doit pas se mettre en veille pendant la soutenance, et Docker Desktop doit démarrer avec la session. Les retries de `verifier-prod` sont tranchés ([ARCHITECTURE § 10.1](../docs/ARCHITECTURE.md#10-décisions-du-lot-5--vérification-sauvegardes-rollback)) : 5 s, 120 s au plus, puis ÉCHEC et rollback.
