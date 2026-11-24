---
titre: Rapport de déploiement — <projet> — <date>
statut: BROUILLON
responsable: agent:deployeur
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/rapport-deploiement.md v0.3 · responsable du modèle : A -->

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
- **Sauvegarde** : <ligne SAUVEGARDE : chemin du dump dans deploiement/local/<slug>/sauvegardes/, ou « aucune (première mise en service) »>
- **Exécution** : <commande `python scripts/deployer_local.py --projet … --sha …`, confirmée par <prénom>, et son code retour>
- **Image** : <ligne IMAGE : esn-<slug>:<sha>>
- **Hébergeur / service** : <production locale Docker (mode local), projet compose esn-<slug>>
- **URL** :
- **Fichier d'état** : <ligne ETAT_VERIFICATION>


## Vérification en ligne (verifier-prod)
| Tentative | Heure | Code HTTP | SHA renvoyé | Résultat |
|---|---|---|---|---|
| 1 | | | | |

**Résultat : <EN LIGNE ET À JOUR | ÉCHEC>**

## Rollback (si échec)
- Déclenché : <oui / non>
- Commande : <`python scripts/rollback_local.py --projet …`, confirmée par <prénom>, et son code retour>
- Version restaurée :
- Vérification après rollback : <fichier d'état et résultat>
- Données : <non restaurées ; dernière sauvegarde : … (restauration = décision humaine)>
- Ticket incident : T-…
