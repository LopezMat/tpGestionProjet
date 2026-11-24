---
titre: Système 3 — Déploiement automatisé
statut: EN_REVUE
responsable: B
version: 1.2
maj_le: 2026-11-24
valide_par: 
decision: 
---

# Système 3 — Déploiement automatisé

> Responsable du fichier : B (en-tête) · responsable du système : C (agents S3, settings et hooks, workflows ; ARCHITECTURE § 12).

## 1. Objectifs (consigne)
Avant toute mise en ligne, le système contrôle le code, directement par ses agents ou par des automatismes qu'ils déclenchent :
- les régressions ;
- la sécurité ;
- la mise en production effective : **un push ne suffit pas**, le système vérifie que l'application est bien en ligne et à jour.

## 2. Acteurs
| Acteur | Rôle |
|---|---|
| `relecteur-code` | revue de qualité et de maintenabilité, en lecture seule ; avis `APPROUVÉ` ou `CHANGEMENTS_DEMANDÉS` dans le ticket |
| `testeur` | tests fonctionnels et de régression ; vérification des critères d'acceptation |
| `securite` | audit OWASP, dépendances, secrets, configuration |
| Salarié recetteur (humain) | recette au regard du CDC, skill [recette](../../.claude/skills/recette/SKILL.md), `rapports/recette-*.md` |
| `deployeur` | sauvegarde, déploiement, vérification en ligne, rollback, par `scripts/deployer_local.py` et `scripts/rollback_local.py` (production locale Docker, DEC-003) |
| `ci.yml`, `securite.yml` | automatismes sur chaque push et chaque PR : tests de tous les scripts (test Docker réel compris) ; audit des dépendances, du code et des secrets. Tests des apps clientes au lot 6 |
| `validations.yml`, `tableau.yml` | contrôle des validations humaines (R5, R6) ; régénération quotidienne des tableaux de bord (R9) |
| Humains | revue humaine (tickets critiques ou sécurité), recette, GO mise en production |

## 3. Portes de contrôle (dans l'ordre)

| # | Porte | Par | Condition de passage |
|---|---|---|---|
| 1 | Revue de code | `relecteur-code` | avis `APPROUVÉ` |
| 1 bis | Revue humaine | humain | obligatoire si le ticket est `critique` ou touche la sécurité |
| 2 | Tests et régressions | `testeur` + `ci.yml` | tous les tests passent ; critères d'acceptation cochés. Le `testeur` coche les critères qu'il a constatés et passe le ticket `TERMINE` (R13) |
| 3 | Sécurité | `securite` + `securite.yml` | aucune vulnérabilité critique ou haute ouverte |
| 3 bis | Recette humaine | salarié recetteur (skill `recette`) | `rapports/recette-*.md` de verdict `CONFORME` **sur le SHA candidat** (S3-R9) |
| 4 | GO mise en production | humain | ticket `ATTENTE_HUMAIN` débloqué, décision tracée |
| 5 | Sauvegarde | `deployeur` via `deployer_local.py` | `pg_dump` réussi et référencé dans le rapport (« aucune » seulement à la première mise en service) |
| 6 | Déploiement | `deployeur` via `deployer_local.py` | image `esn-<slug>:<sha>` construite au SHA du GO, puis lancée |
| 7 | Vérification en ligne | skill `verifier-prod` (appelé par `deployer_local.py`) | `/health` répond et **le SHA en ligne est égal au SHA attendu** |
| 8 | Rollback si échec | `deployeur` via `rollback_local.py` | relance de l'image du SHA précédent, vérifiée par `verifier-prod`, puis ticket incident |

## 4. Règles

**S3-R1 · Celui qui écrit le code ne le valide pas.** `relecteur-code` et `securite` signalent, ils ne corrigent pas.
*Pourquoi :* un contrôle indépendant est le seul qui détecte ce que l'auteur ne voit pas.

**S3-R2 · Une revue humaine est obligatoire, en plus de `relecteur-code`, pour les tickets `critique` et ceux qui touchent la sécurité.**
*Pourquoi :* sur ces tickets, une erreur coûte trop cher pour ne s'appuyer que sur un agent.

**S3-R3 · Aucune mise en production sans GO humain**, donné via un ticket `ATTENTE_HUMAIN`.
*Pourquoi :* la vision place la mise en production parmi les validations humaines ; elle est aussi appliquée par les permissions : `git push`, `deployer_local.py` et `rollback_local.py` sont en `ask`, et le hook `restreindre_bash.py` redemande lui-même la confirmation pour ces deux scripts (DEC-003).

**S3-R4 · Une sauvegarde est prise avant chaque déploiement.**
*Pourquoi :* le runbook « perte de données » (S2) en dépend ; sans sauvegarde, il n'y a pas de retour possible.

**S3-R5 · Un déploiement n'est réussi que si `verifier-prod` constate que `/health` renvoie le SHA attendu**, après des retries espacés (en local : toutes les 5 s, pendant 120 s au plus ; ARCHITECTURE § 10.1).
*Pourquoi :* c'est l'exigence de la consigne, « un push ne suffit pas ». Les retries évitent les faux échecs pendant que l'app et sa base démarrent.

**S3-R6 · En cas d'échec de vérification, le `deployeur` déclenche le rollback** et crée un ticket incident (`critique`, assigné au `gestionnaire-crise`, qui cite le runbook `rollback` et le rapport de déploiement). Ce rollback sans nouveau GO ne vise **que l'échec de la vérification en ligne** ; une régression constatée plus tard, sur une version vérifiée, suit S2-R7 (décision humaine « rollback ou correctif »).
*Pourquoi :* on rétablit d'abord le service, on analyse ensuite. Mais une version vérifiée a fait l'objet d'un GO humain : revenir dessus est une décision humaine.

**S3-R7 · La procédure de rollback est testée** au moins une fois avant la soutenance, et le test est tracé dans un rapport. Le test réel de `scripts/test_prod_locale.py` (déploiement, panne, rollback) le rejoue automatiquement en CI ; le rapport est produit sur le projet de démonstration (ARCHITECTURE § 10.3).
*Pourquoi :* un rollback jamais testé ne fonctionne pas le jour où on en a besoin.

**S3-R8 · Les secrets ne sont jamais dans le dépôt.** Le mot de passe de la base locale est tiré au hasard et gardé, comme les sauvegardes, dans `deploiement/local/<slug>/`, que Git ignore. Les secrets éventuels d'un service tiers vont dans les secrets GitHub. La lecture de `.env*` est interdite aux agents (`deny`).
*Pourquoi :* une fuite de secret dans Git est permanente.

**S3-R9 · Pas de GO sans rapport de recette CONFORME** portant sur le SHA du GO (porte 3 bis). La recette est faite par un salarié qui n'est pas l'auteur du code, à partir des critères d'acceptation du CDC (skill `recette`). Le verdict est `CONFORME` si tous les critères des exigences **Must** sont OK et qu'aucun bug `critique` ou `haute` issu de la recette n'est ouvert ; un KO sur un Should ou un Could est admis s'il a son ticket bug. Toute correction produit un nouveau SHA, donc une nouvelle recette (au moins les critères KO et les Must en non-régression), comme pour les rapports de tests et de sécurité.
*Pourquoi :* les tests des agents et de la CI vérifient le code au regard de ses propres critères. Seul un humain qui utilise l'app comme le client vérifie qu'elle répond au CDC, et un agent qui teste du code écrit par un agent en partage les angles morts. De plus, la recette engage l'ESN auprès du client (AF1) : un humain identifié atteste la conformité avant le GO.

## 5. Permissions appliquées (`.claude/settings.json` et hooks)
| Action | Permission | Pourquoi |
|---|---|---|
| `git push` | ask | la publication du code est une action humaine |
| `python scripts/deployer_local.py …`, `python scripts/rollback_local.py …` (aussi `python3`, `py`) | ask, doublé d'un `ask` du hook `restreindre_bash.py` pour tout appelant | équivaut à une mise en production ou à son annulation (S3-R3, DEC-003). Le `deployeur` est lancé **au premier plan** : en arrière-plan, la confirmation ne peut pas s'afficher et la commande est refusée |
| `gh workflow run *` | ask | déclenche un workflow (`tableau.yml` à la main, par exemple) ; aucun workflow ne déploie |
| `rm -rf`, `git reset --hard`, `git push --force` | deny | actions destructrices et irréversibles |
| lecture et écriture de `.env*` | deny (`Read(**/.env*)`, `Edit(**/.env*)`) | secrets. La règle `Read` ne couvre pas Bash (`cat .env`) : pour les subagents, c'est le hook `restreindre_bash.py` qui refuse tout argument désignant un `.env*` |
| Bash des subagents | hook `restreindre_bash.py` | pas de `git push`, ni de `git reset --hard`, ni de `rm` récursif forcé, même déguisés (`git -C . push`, `bash -c`) ; listes blanches pour `chef-de-projet`, `relecteur-code`, `deployeur` (les 2 scripts de déploiement local, `verifier_prod.py`, `git rev-parse`, `git log`), `analyste-prod` et `gestionnaire-crise` ([ARCHITECTURE § 6](../ARCHITECTURE.md#6-modèle-de-validation), garde-fou 7) |
| Write/Edit d'un `statut: VALIDÉ` (valeur normalisée : `VALIDE`, `validé`…) ou d'un document VALIDÉ | bloqué par le hook `proteger_valide.py` | voir [ARCHITECTURE § 6](../ARCHITECTURE.md#6-modèle-de-validation) |
| Write/Edit de `TABLEAU.md` ou `PORTFOLIO.md` | bloqué par le hook `proteger_valide.py` | fichiers générés par `tableau.py` (R9, garde-fou 8) |
| `Edit(/templates/**)` | ask, doublé d'un `ask` du hook | les templates restent en BROUILLON, donc R6 ne les protège pas ; or `tableau.py` et tous les agents dépendent de leur format. Une règle `Edit` couvre aussi Write et MultiEdit (outil ancien) ; le `/` ancre le chemin à la racine du dépôt |

## 6. Hébergement : production locale Docker (DEC-003)
**Par défaut, la production est locale**, dans Docker, sur le poste de démonstration (décision du professeur du 2026-11-24). `projet.md` porte `hebergement: local` et `url_prod: http://localhost:<port>` (8080 par défaut). Détails et valeurs tranchées : [ARCHITECTURE § 9 et § 10](../ARCHITECTURE.md#9-hébergement-et-vérification-en-ligne).

- **Image étiquetée par SHA** : `esn-<slug>:<sha40>` est construite à partir du commit du GO (`git archive`, jamais l'arbre de travail), avec `--build-arg GIT_COMMIT=<sha>`. `/health` renvoie ce `GIT_COMMIT`, figé dans l'image : une image relancée par un rollback annonce donc son vrai SHA.
- **Modèle commun** `deploiement/docker-compose.yml` : l'app et une base Postgres 16 dans un volume nommé. La base n'a aucun port publié ; l'app n'est publiée que sur `127.0.0.1`.
- **Déploiement** : `python scripts/deployer_local.py --projet <slug> --sha <sha du GO>` enchaîne sauvegarde `pg_dump`, build, lancement et `verifier-prod`. Codes de retour :
  - 0 : en ligne et à jour ;
  - 1 : échec après le lancement, il faut un rollback ;
  - 2 : précondition non remplie, rien n'a changé ;
  - 3 : vérification en cours ;
  - 4 : sauvegarde en échec ;
  - 5 : build en échec, production inchangée.
- **Rollback** : `python scripts/rollback_local.py --projet <slug> [--sha <sha>]` relance l'image du SHA précédent, sans rebuild, puis lance `verifier-prod`. Sans `--sha`, il ne vise que la version précédente d'un déploiement en échec (S3-R6). Revenir sur un déploiement vérifié exige `--sha`, après une décision humaine (S2-R7). Il ne restaure jamais de données.
- **Un hébergeur distant** (Render ou autre) peut être proposé par l'`architecte`, avec une décision humaine. Son déploiement serait alors à outiller : aucun workflow ne déploie aujourd'hui.

*Pourquoi :* c'est la décision du professeur. Le rollback est immédiat, puisque l'image étiquetée existe déjà, et la soutenance ne dépend d'aucun réseau. La preuve par le SHA reste celle d'un hébergement réel.

## 7. Livrables
- `rapports/tests-<date>.md`, `rapports/securite-<date>.md`, `rapports/recette-<date>.md`, `rapports/deploiement-<date>.md` (templates dédiés), et un fichier d'état par vérification, `rapports/verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json`, jamais réutilisé.
- Hors du dépôt Git, dans `deploiement/local/<slug>/` (ignoré) : les sauvegardes `pg_dump`, l'historique des déploiements et le mot de passe de la base locale.
- Section « Revue » remplie dans chaque ticket de réalisation.

## 8. Interfaces
- **← Réalisation** : tickets EN_REVUE et code dans `app/`.
- **← S4** : critères d'acceptation du CDC, base de la recette humaine.
- **→ S1** : tickets bug ; confirmation du TERMINE des déploiements.
- **→ S2** : rapport de déploiement (SHA et URL), point de départ du suivi ; sauvegardes et rollback utilisés par les runbooks ; en cas d'échec de vérification, ticket `incident` `critique` assigné au `gestionnaire-crise` ; le runbook `rollback` s'appuie sur `rollback_local.py`, sur `verifier-prod` (codes retour 0 à 3) et sur ses fichiers d'état.
