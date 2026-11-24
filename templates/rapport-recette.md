---
titre: Rapport de recette — <projet> — <date>
statut: BROUILLON
responsable: salarie:<prenom>
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/rapport-recette.md v0.1 · responsable du modèle : A -->

# Rapport de recette — <projet> — <date>

> Porte 3 bis de S3 (S3-R9). Recette faite par un salarié humain qui n'est pas l'auteur du code, selon le skill `recette`. **Chaque résultat est constaté par le recetteur lui-même.**

- **Recetteur** : salarie:<prenom> · **Ticket « Recette »** : T-…
- **SHA recetté** : <sha> · **Environnement / URL** : <local avec GIT_COMMIT | URL de recette>
- **`/health` constaté** : <ligne RESULTAT de `sonde_sante.py`>
- **CDC de référence** : `cdc.md` v… (VALIDÉ, DEC-…)
- **Rapports de référence (même SHA)** : `rapports/tests-…` (CONFORME) · `rapports/securite-…` (NON BLOQUANT)

## Critères recettés
<!-- Une ligne par critère d'acceptation du CDC, recopié mot pour mot ; les Must d'abord. -->
| Exigence | MoSCoW | Critère d'acceptation (CDC) | Résultat | Observation | Ticket bug lié |
|---|---|---|---|---|---|
| F-01 | Must | | OK / KO / Non testé | | T-… |

## Re-tests
<!-- Après correction : nouveau SHA, donc nouveau rapport ; historique des critères re-testés. -->
| Critère | SHA précédent (résultat) | SHA re-testé | Résultat | Ticket |
|---|---|---|---|---|

## Bugs créés
- T-… <titre> (priorité)

## Verdict
**<CONFORME | NON CONFORME>** : <justification en une phrase>

Règle (S3-R9) : **CONFORME** si tous les critères des exigences **Must** sont `OK` et qu'aucun bug `critique` ou `haute` issu de la recette n'est ouvert ; un KO sur un Should ou un Could est admis s'il a son ticket bug. Sinon **NON CONFORME**, y compris quand un critère Must est `Non testé`. Un rapport NON CONFORME bloque le GO.
