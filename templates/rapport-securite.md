---
titre: Rapport de sécurité — <projet> — <date>
statut: BROUILLON
responsable: agent:securite
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/rapport-securite.md v0.1 · responsable du modèle : A -->

# Rapport de sécurité — <projet> — <date>

- **Commit audité (SHA)** :
- **Périmètre** : <app/, dépendances, configuration, secrets>
- **Outils** : <audit de dépendances, recherche de secrets, SAST, revue manuelle OWASP>
- **Exécution CI** : <lien vers le run securite.yml>

## Constats
| # | Sévérité | Catégorie (OWASP) | Emplacement | Description | Recommandation | Ticket |
|---|---|---|---|---|---|---|
| 1 | critique / haute / moyenne / basse | | | | | T-… |

## Exigences de sécurité du CDC
| Exigence (CDC § 8) | Couverte ? | Preuve |
|---|---|---|

## Verdict
**<BLOQUANT | NON BLOQUANT>**. Bloquant s'il reste un constat critique ou haut ouvert (porte 3 de S3).
