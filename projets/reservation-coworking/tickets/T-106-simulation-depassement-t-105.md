---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-106
titre: "SIMULATION — Condition 1 de DEC-020 : dépassement prévisible dû au bug T-105"
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ATTENTE_HUMAIN      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: relation-client (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.25          # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: arbitrage humain avant d'engager le correctif de T-105 (condition 1 de DEC-020)
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Arbitrage budgétaire déclenché par le tri du bug simulé T-105 (scénario 4, S2), en application de la condition 1 de DEC-020.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-106 — SIMULATION — Condition 1 de DEC-020 : dépassement prévisible dû au bug T-105

## Description
La **condition 1 de [DEC-020](../../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md)** s'applique : tout dépassement prévisible du budget client de 4 200 € HT donne lieu à un arbitrage humain et à une discussion avec le client **avant** d'être engagé, jamais après.

Le tri de [T-105](T-105-aucun-creneau-page-disponibilites.md) par le `chef-de-projet` établit un **coût client prévisible de 4 211,43 € HT**, soit **11,43 € au-dessus** des 4 200 €. Le bug a été remonté par la recette (note `support/entrant/recette-2026-11-26-01.md`, DEC-004) : « Aucun créneau » sur la page de consultation (F-01, Must). Il n'est pas encore reproduit, et la cause reste incertaine.

| Poste | Montant |
|---|---|
| Coût client avant le tri (y compris T-104, support, 1 h) | 4 173,93 € |
| T-105 (`dev-frontend`, 1,5 h × 15 €) | + 22,50 € |
| Revue de code et vérification par le testeur (1 h, non comptée par le tableau) | + 15,00 € |
| **Coût client prévisible** | **4 211,43 €** |

Consommé client : 1 371,29 € (32,6 %), loin du seuil d'alerte de 3 780 €. Fin projetée inchangée : 2026-12-16.

**Question** : comment financer le correctif de T-105, avant de l'engager ?

**Options** (proposées par le `chef-de-projet`)
- **A. L'ESN prend le dépassement à sa charge, par décision explicite** (environ 11 € ; jusqu'à 37,50 € si tout T-105 lui est imputé). C'est cohérent avec la garantie de livraison (CDC § 9 : correction des défauts constatés à la recette, comprise dans le budget), puisque le défaut vient de la livraison de l'ESN.
- **B. Retirer du périmètre ailleurs** pour environ 12 € : très contraint, car ni les Must, ni F-08, ni la sécurité, ni les revues humaines, ni les portes de contrôle ne peuvent être retirés.
- **C. Avenant au client**, porté par Claire : faible, puisque le défaut relève de la garantie.
- **Variante, quelle que soit l'option** : engager d'abord la **reproduction seule** (0,5 h, 7,50 €), qui tient dans la marge. Si le bug n'est pas reproduit, T-105 est clos sans correctif et le dépassement disparaît.

**Recommandation du coordinateur** : engager la reproduction seule, puis l'option A si le défaut est confirmé (garantie de livraison).

**Impact** : 11,43 € au-dessus du budget client, aucun effet sur le délai. Si le défaut est confirmé, T-105 deviendrait un prérequis de la recette T-045, et donc du GO (R16).

**Préalable, à demander à Claire** (relevé par `support` et le `chef-de-projet`) : le rapport de recette (ou la confirmation d'une recette partielle informelle), l'URL testée et le SHA de `/health`, le navigateur et l'appareil, le nom de salle affiché (« Canigou » n'existe pas dans le modèle), le message exact, la date et l'heure du test, et une capture.

## Critères d'acceptation
- [ ] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [ ] Si l'option C est retenue : la discussion avec le client par Claire est notée au journal avant tout engagement.
- [ ] T-105 porte une ligne de journal qui cite la décision avant d'être pris.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 23:59 · agent:coordinateur · SIMULATION · création (condition 1 de DEC-020) après le tri de T-105 par le chef-de-projet : coût client prévisible de 4 211,43 € pour 4 200 € ; correctif non engagé · 0 h
