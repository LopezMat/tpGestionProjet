---
titre: Rapport de suivi de production — <projet> — <date>
statut: BROUILLON
responsable: agent:analyste-prod
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/rapport-suivi.md v0.1 · responsable du modèle : A -->

# Rapport de suivi de production — <projet> — <date>

- **Référence** : `rapports/deploiement-…` (EN LIGNE ET À JOUR) · **SHA attendu** : · **URL** :
- **Période couverte** : <du … au …>

## 1. Sources
| Source | Type | Fichier ou commande |
|---|---|---|
| `/health` | réel | `python scripts/sonde_sante.py --url <url> --sha <sha>` |
| Logs | simulé | `rapports/logs-AAAA-MM-JJ.log` |
| Métriques | simulé | `rapports/metriques-AAAA-MM-JJ.csv` |

## 2. Disponibilité et version
<tableau de la sonde recopié tel quel, avec sa ligne RESULTAT>

## 3. Performances
| Indicateur | Valeur | Seuil | Constat |
|---|---|---|---|
| Temps de réponse médian `/health` | | 2000 ms | |

## 4. Erreurs et bugs
| # | Constat | Preuve (ligne de log, métrique) | Priorité proposée (S2 § 4) | Ticket |
|---|---|---|---|---|

## 5. Tickets créés
- T-… <titre> (type, priorité)

## 6. Rien à signaler
<à remplir quand aucune anomalie n'a été constatée : ce qui a été vérifié, et sur quelle période>
