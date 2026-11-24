---
titre: Architecture technique — <projet>
statut: BROUILLON
responsable: agent:architecte
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/architecture.md v0.2 · responsable du modèle : A -->

# Architecture technique — <projet>

Source : [cdc.md](cdc.md) (doit être VALIDÉ)

## 1. Synthèse
<SI retenu en 3 lignes>

## 2. Stack
| Couche | Technologie | Version | Justification |
|---|---|---|---|
| Frontend | | | |
| Backend | | | |
| Base de données | | | |
| Hébergement | Production locale Docker (par défaut, DEC-003) | | |

## 3. Schéma
```mermaid
flowchart LR
  U([Utilisateur]) --> F[Frontend] --> B[API] --> D[(Base)]
```

## 4. Données et persistance
<modèle de données, données sensibles, persistance en production>

## 5. Endpoint `/health` (obligatoire)
Renvoie au minimum `{ "status": "ok", "commit": "<SHA déployé>" }`, à partir de `GIT_COMMIT`, figé dans l'image par `ARG GIT_COMMIT` (repli : `RENDER_GIT_COMMIT`, sinon `"inconnu"`).

## 6. Couverture des exigences non fonctionnelles du CDC
| Exigence CDC | Réponse architecturale |
|---|---|

## 7. Sécurité
<authentification, secrets, surface d'attaque, dépendances>

## 8. Déploiement, sauvegarde et rollback
<contrat de l'image : `app/Dockerfile` (`ARG GIT_COMMIT`, écoute sur `$PORT`, base dans `DATABASE_URL`) ; base (Postgres 16 du modèle `deploiement/docker-compose.yml`) ; migrations de données et leur compatibilité avec un rollback ; sauvegarde et rollback, ou renvoi à ARCHITECTURE § 10>

## 9. Décisions techniques
| # | Décision | Alternatives étudiées | Pourquoi | Coût / impact maintenance |
|---|---|---|---|---|
| 1 | | | | |

## 10. Estimation de coût d'exploitation
<hébergement, services tiers>
