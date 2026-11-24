---
titre: Système 3 — Déploiement automatisé
statut: EN_REVUE
responsable: B
version: 1.1
maj_le: 2026-11-24
valide_par: 
decision: DEC-001
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
| `deployeur` | sauvegarde, déclenchement, vérification en ligne, rollback |
| `ci.yml`, `securite.yml` | automatismes sur chaque PR, filtrés sur `projets/<slug>/app/**` |
| `deploy.yml` | sauvegarde, deploy hook Render, vérification |
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
| 5 | Sauvegarde | `deploy.yml` | sauvegarde réussie et référencée dans le rapport |
| 6 | Déploiement | `deploy.yml` (deploy hook Render) | déploiement déclenché |
| 7 | Vérification en ligne | skill `verifier-prod` | `/health` répond et **le SHA en ligne est égal au SHA attendu** |
| 8 | Rollback si échec | `deployeur` | retour à la version précédente, puis ticket incident |

## 4. Règles

**S3-R1 · Celui qui écrit le code ne le valide pas.** `relecteur-code` et `securite` signalent, ils ne corrigent pas.
*Pourquoi :* un contrôle indépendant est le seul qui détecte ce que l'auteur ne voit pas.

**S3-R2 · Une revue humaine est obligatoire, en plus de `relecteur-code`, pour les tickets `critique` et ceux qui touchent la sécurité.**
*Pourquoi :* sur ces tickets, une erreur coûte trop cher pour ne s'appuyer que sur un agent.

**S3-R3 · Aucune mise en production sans GO humain**, donné via un ticket `ATTENTE_HUMAIN`.
*Pourquoi :* la vision place la mise en production parmi les validations humaines ; elle est aussi appliquée par les permissions (`git push` et déclenchement du déploiement en `ask`).

**S3-R4 · Une sauvegarde est prise avant chaque déploiement.**
*Pourquoi :* le runbook « perte de données » (S2) en dépend ; sans sauvegarde, il n'y a pas de retour possible.

**S3-R5 · Un déploiement n'est réussi que si `verifier-prod` constate que `/health` renvoie le SHA attendu**, après des retries espacés (offre gratuite : mise en veille et build de plusieurs minutes).
*Pourquoi :* c'est l'exigence de la consigne, « un push ne suffit pas ». Les retries évitent les faux échecs dus au réveil de l'app.

**S3-R6 · En cas d'échec de vérification, le `deployeur` déclenche le rollback** et crée un ticket incident (`critique`, assigné au `gestionnaire-crise`, qui cite le runbook `rollback` et le rapport de déploiement). Ce rollback sans nouveau GO ne vise **que l'échec de la vérification en ligne** ; une régression constatée plus tard, sur une version vérifiée, suit S2-R7 (décision humaine « rollback ou correctif »).
*Pourquoi :* on rétablit d'abord le service, on analyse ensuite. Mais une version vérifiée a fait l'objet d'un GO humain : revenir dessus est une décision humaine.

**S3-R7 · La procédure de rollback est testée** au moins une fois avant la soutenance, et le test est tracé dans un rapport.
*Pourquoi :* un rollback jamais testé ne fonctionne pas le jour où on en a besoin.

**S3-R8 · Les secrets ne sont jamais dans le dépôt.** Ils sont dans les secrets GitHub ; la lecture de `.env*` est interdite aux agents (`deny`).
*Pourquoi :* une fuite de secret dans Git est permanente.

**S3-R9 · Pas de GO sans rapport de recette CONFORME** portant sur le SHA du GO (porte 3 bis). La recette est faite par un salarié qui n'est pas l'auteur du code, à partir des critères d'acceptation du CDC (skill `recette`). Le verdict est `CONFORME` si tous les critères des exigences **Must** sont OK et qu'aucun bug `critique` ou `haute` issu de la recette n'est ouvert ; un KO sur un Should ou un Could est admis s'il a son ticket bug. Toute correction produit un nouveau SHA, donc une nouvelle recette (au moins les critères KO et les Must en non-régression), comme pour les rapports de tests et de sécurité.
*Pourquoi :* les tests des agents et de la CI vérifient le code au regard de ses propres critères. Seul un humain qui utilise l'app comme le client vérifie qu'elle répond au CDC, et un agent qui teste du code écrit par un agent en partage les angles morts. De plus, la recette engage l'ESN auprès du client (AF1) : un humain identifié atteste la conformité avant le GO.

## 5. Permissions appliquées (`.claude/settings.json` et hooks)
| Action | Permission | Pourquoi |
|---|---|---|
| `git push` | ask | la publication du code est une action humaine |
| `gh workflow run deploy*` | ask | équivaut à une mise en production |
| `rm -rf`, `git reset --hard`, `git push --force` | deny | actions destructrices et irréversibles |
| lecture et écriture de `.env*` | deny (`Read(**/.env*)`, `Edit(**/.env*)`) | secrets. La règle `Read` ne couvre pas Bash (`cat .env`) : pour les subagents, c'est le hook `restreindre_bash.py` qui refuse tout argument désignant un `.env*` |
| Bash des subagents | hook `restreindre_bash.py` | pas de `git push`, ni de `git reset --hard`, ni de `rm` récursif forcé, même déguisés (`git -C . push`, `bash -c`) ; listes blanches pour `chef-de-projet`, `relecteur-code`, `deployeur`, `analyste-prod` et `gestionnaire-crise` ([ARCHITECTURE § 6](../ARCHITECTURE.md#6-modèle-de-validation), garde-fou 7) |
| Write/Edit d'un `statut: VALIDÉ` (valeur normalisée : `VALIDE`, `validé`…) ou d'un document VALIDÉ | bloqué par le hook `proteger_valide.py` | voir [ARCHITECTURE § 6](../ARCHITECTURE.md#6-modèle-de-validation) |
| Write/Edit de `TABLEAU.md` ou `PORTFOLIO.md` | bloqué par le hook `proteger_valide.py` | fichiers générés par `tableau.py` (R9, garde-fou 8) |
| `Edit(/templates/**)` | ask, doublé d'un `ask` du hook | les templates restent en BROUILLON, donc R6 ne les protège pas ; or `tableau.py` et tous les agents dépendent de leur format. Une règle `Edit` couvre aussi Write et MultiEdit (outil ancien) ; le `/` ancre le chemin à la racine du dépôt |

## 6. Hébergement
Render par défaut (offre gratuite, deploy hook déclenché par `deploy.yml`). `/health` renvoie le SHA du commit déployé : `RENDER_GIT_COMMIT`, avec un repli sur `GIT_COMMIT` fourni au lancement local, sinon `"inconnu"` (la vérification échoue alors). Un autre hébergeur peut être proposé par l'`architecte`, avec validation humaine. Détails : [ARCHITECTURE § 9](../ARCHITECTURE.md#9-hébergement-et-vérification-en-ligne).

**Production locale.** Elle est admise si `projet.md` porte `hebergement: local` et `url_prod: http://localhost:<port>`, après une décision humaine (« hébergeur différent de Render »). L'app est lancée au SHA attendu avec `GIT_COMMIT=$(git rev-parse HEAD)`, et `verifier-prod` fonctionne à l'identique.
*Pourquoi :* le professeur peut dispenser l'équipe d'hébergement réel ; la preuve par le SHA reste la même. La procédure de « déploiement » et de sauvegarde locaux est à écrire au lot 5.

**À trancher au lot workflows :** les valeurs des retries, la base persistante et les sauvegardes, le mécanisme de rollback. Voir [ARCHITECTURE § 10](../ARCHITECTURE.md#10-à-trancher-au-lot-workflows).

## 7. Livrables
- `rapports/tests-<date>.md`, `rapports/securite-<date>.md`, `rapports/recette-<date>.md`, `rapports/deploiement-<date>.md` (templates dédiés), et le fichier d'état `rapports/verifier-prod-<sha7>.json`.
- Section « Revue » remplie dans chaque ticket de réalisation.

## 8. Interfaces
- **← Réalisation** : tickets EN_REVUE et code dans `app/`.
- **← S4** : critères d'acceptation du CDC, base de la recette humaine.
- **→ S1** : tickets bug ; confirmation du TERMINE des déploiements.
- **→ S2** : rapport de déploiement (SHA et URL), point de départ du suivi ; sauvegardes et rollback utilisés par les runbooks ; en cas d'échec de vérification, ticket `incident` `critique` assigné au `gestionnaire-crise` ; le runbook `rollback` s'appuie sur `verifier-prod` (codes retour 0 à 3) et sur ses fichiers d'état.
