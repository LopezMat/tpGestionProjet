---
titre: Système 3 — Déploiement automatisé
statut: EN_REVUE
responsable: C
version: 0.2
maj_le: 2026-11-23
valide_par:
decision:
---

# Système 3 — Déploiement automatisé

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
| `deployeur` | sauvegarde, déclenchement, vérification en ligne, rollback |
| `ci.yml`, `securite.yml` | automatismes sur chaque PR, filtrés sur `projets/<slug>/app/**` |
| `deploy.yml` | sauvegarde, deploy hook Render, vérification |
| Humains | revue humaine (tickets critiques ou sécurité), GO mise en production |

## 3. Portes de contrôle (dans l'ordre)

| # | Porte | Par | Condition de passage |
|---|---|---|---|
| 1 | Revue de code | `relecteur-code` | avis `APPROUVÉ` |
| 1 bis | Revue humaine | humain | obligatoire si le ticket est `critique` ou touche la sécurité |
| 2 | Tests et régressions | `testeur` + `ci.yml` | tous les tests passent ; critères d'acceptation cochés |
| 3 | Sécurité | `securite` + `securite.yml` | aucune vulnérabilité critique ou haute ouverte |
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

**S3-R6 · En cas d'échec de vérification, le `deployeur` déclenche le rollback** et crée un ticket incident.
*Pourquoi :* on rétablit d'abord le service, on analyse ensuite.

**S3-R7 · La procédure de rollback est testée** au moins une fois avant la soutenance, et le test est tracé dans un rapport.
*Pourquoi :* un rollback jamais testé ne fonctionne pas le jour où on en a besoin.

**S3-R8 · Les secrets ne sont jamais dans le dépôt.** Ils sont dans les secrets GitHub ; la lecture de `.env*` est interdite aux agents (`deny`).
*Pourquoi :* une fuite de secret dans Git est permanente.

## 5. Permissions prévues (`.claude/settings.json`, lot settings/hooks)
| Action | Permission | Pourquoi |
|---|---|---|
| `git push` | ask | la publication du code est une action humaine |
| `gh workflow run deploy*` | ask | équivaut à une mise en production |
| `rm -rf`, `git reset --hard`, `git push --force` | deny | actions destructrices et irréversibles |
| lecture et écriture de `.env*` | deny | secrets |
| Write/Edit d'un `statut: VALIDÉ` (valeur normalisée : `VALIDE`, `validé`…) ou d'un document VALIDÉ | bloqué par hook | voir [ARCHITECTURE § 6](../ARCHITECTURE.md#6-modèle-de-validation) |
| `Write(templates/**)`, `Edit(templates/**)` | ask | les templates restent en BROUILLON, donc R6 ne les protège pas ; or `tableau.py` et tous les agents dépendent de leur format |

## 6. Hébergement
Render par défaut (offre gratuite, deploy hook déclenché par `deploy.yml`). `/health` renvoie le SHA du commit déployé. Un autre hébergeur peut être proposé par l'`architecte`, avec validation humaine. Détails : [ARCHITECTURE § 9](../ARCHITECTURE.md#9-hébergement-et-vérification-en-ligne).

**À trancher au lot workflows :** les valeurs des retries, la base persistante et les sauvegardes, le mécanisme de rollback. Voir [ARCHITECTURE § 10](../ARCHITECTURE.md#10-à-trancher-au-lot-workflows).

## 7. Livrables
- `rapports/tests-<date>.md`, `rapports/securite-<date>.md`, `rapports/deploiement-<date>.md` (templates dédiés).
- Section « Revue » remplie dans chaque ticket de réalisation.

## 8. Interfaces
- **← Réalisation** : tickets EN_REVUE et code dans `app/`.
- **→ S1** : tickets bug ; confirmation du TERMINE des déploiements.
- **→ S2** : rapport de déploiement (SHA et URL), point de départ du suivi ; sauvegardes et rollback utilisés par les runbooks.
