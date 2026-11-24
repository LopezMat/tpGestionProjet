---
titre: Retour d'expérience — reservation-coworking — cadrage (en cours)
statut: BROUILLON
responsable: B
version: 0.1
maj_le: 2026-11-24
valide_par:
decision:
---
<!-- modèle : templates/retex.md v0.1 · responsable du modèle : A -->

# Retour d'expérience — reservation-coworking — cadrage (en cours)

> Document ouvert par le coordinateur pour noter un incident à chaud (2026-11-24). Le `chef-de-projet` le complètera en fin de jalon (étape 9 du pipeline).

## Chiffres
| Indicateur | Prévu | Réel | Écart |
|---|---|---|---|
| Charge (h) | | | |
| Budget (€) | | | |
| Date de fin | 2026-12-18 | | |
| Tickets bug après mise en production | — | | |

## Ce qui a bien marché
- 

## Ce qui a posé problème
| Problème | Cause | Concerne (agent / règle / salarié / outil) |
|---|---|---|
| **2026-11-24 : DEC-007 modifié alors qu'il était `VALIDÉ` (R6).** Le coordinateur a appliqué des modifications demandées par Ethan à DEC-007 au moyen d'un script Python lancé par Bash ; Ethan venait de passer le fichier en `VALIDÉ` (sans encore renseigner `valide_par`). L'écriture n'a pas été bloquée ; elle a été détectée après coup par `scripts/verifier_validations.py` (« VALIDÉ sans valide_par »), puis signalée à Ethan. Le contenu modifié était celui demandé ; Ethan a relu puis complété `valide_par`. | (1) Le coordinateur n'a pas relu l'en-tête avant d'écrire. (2) Le hook `proteger_valide.py` ne surveille que Write et Edit : une écriture par Bash le contourne. Le filet CI (`validations.yml`) ne voit que le statut, pas une modification du contenu d'un document déjà correctement validé. | coordinateur ; R6 ; outil (`proteger_valide.py`, `restreindre_bash.py`) |
| **2026-11-24 : architecture passée `VALIDÉ` pendant la révision v0.4 par l'`architecte`.** Le hook a refusé la suite de la révision (R6, fonctionnement attendu), mais le document validé est resté à moitié révisé et se contredit (§ 8 à 11). | Validation humaine faite en parallèle d'une révision en cours, sans signal « révision en cours » sur le document. | règle de validation ; coordinateur (annonce de fin de révision) |

## Améliorations des agents IA → tickets `amelioration`
| Agent ou règle | Amélioration proposée | Ticket |
|---|---|---|
| coordinateur et tous les agents ; `restreindre_bash.py` | Ne jamais modifier un document Markdown par Bash (sed, redirection, script) : uniquement par Edit/Write, pour que le hook R5/R6 s'applique. Règle R17 (via R11) et détection des écritures (`sed -i`, `>`, `>>`) sur les `.md` de `docs/` et `projets/` dans le hook. | [T-006](tickets/T-006-ecritures-md-par-edit-uniquement.md) |

## Besoins de formation → tickets `formation`
| Salarié | Compétence | Ticket |
|---|---|---|

## Règles à modifier (R11 : PR, décision et changelog)
- R17 (proposée, T-006) : écritures des documents Markdown uniquement par Edit/Write.
