---
titre: Rapport de déploiement — <projet> — <date>
statut: BROUILLON
responsable: agent:deployeur
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/rapport-deploiement.md v0.2 · responsable du modèle : A -->

# Rapport de déploiement — <projet> — <date>

## Préconditions (portes S3)
| Porte | Preuve | OK |
|---|---|---|
| Revue de code | tickets avec avis APPROUVÉ | [ ] |
| Tests | rapports/tests-… | [ ] |
| Sécurité | rapports/securite-… (NON BLOQUANT) | [ ] |
| Recette humaine (3 bis) | rapports/recette-… (CONFORME, même SHA) | [ ] |
| GO humain | ticket T-… / DEC-… | [ ] |

## Déploiement
- **SHA attendu** :
- **Version précédente (SHA)** :
- **Sauvegarde** : <référence de l'artefact / emplacement>
- **Exécution** : <lien vers le run deploy.yml>
- **Hébergeur / service** :
- **URL** :

## Vérification en ligne (verifier-prod)
| Tentative | Heure | Code HTTP | SHA renvoyé | Résultat |
|---|---|---|---|---|
| 1 | | | | |

**Résultat : <EN LIGNE ET À JOUR | ÉCHEC>**

## Rollback (si échec)
- Déclenché : <oui / non>
- Version restaurée :
- Vérification après rollback :
- Ticket incident : T-…
