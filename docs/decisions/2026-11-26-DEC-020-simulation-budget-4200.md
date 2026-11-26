---
titre: SIMULATION — Révision du budget de reservation-coworking, 6 000 € → 4 200 € HT (scénario B en gardant F-08)
statut: EN_REVUE
responsable: B
version: 0.2
maj_le: 2026-11-26
valide_par:                 # rempli par l'humain qui valide
decision: DEC-020           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-020
date: 2026-11-26
decide_par: Ethan
projet: reservation-coworking
ticket: T-093
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
> **SIMULATION** — Décision prise dans l'exercice de révision du budget (scénario 2, S1) du 2026-11-26. Le client n'a rien annoncé en réalité.

<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-020 — SIMULATION — Révision du budget : 6 000 € → 4 200 € HT

## Contexte
Le client annonce par écrit (simulation) que le budget passe de 6 000 € HT ([DEC-009](2026-11-24-DEC-009-budget-delais-coworking.md)) à **4 200 € HT**, sans changer la deadline du **2026-12-18**. Le ticket [T-093](../../projets/reservation-coworking/tickets/T-093-simulation-revision-budget-4200.md), traité selon le skill `revision-budget`, contient l'analyse d'impact du `chef-de-projet` :
- consommé : 1 300,04 € ;
- coût projeté corrigé : **6 050,72 €** ;
- le socle obligatoire (Must, revues humaines, T-029, portes S3) coûte à lui seul 4 309,79 € ;
- aucune heure ne peut passer d'un salarié à un agent (AF1 à AF5).

La crise simulée de DEC-019 (perte de la base, T-080) pèse 1 125,36 € sur le reste à faire.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| A · Recentrage seul : retrait de F-06, F-08, T-065, T-076 ; correctifs de crise reportés (5 240,50 €) | moins coûteux pour l'ESN | ne respecte pas 4 200 € (+1 040,50 €) ; la crise peut se reproduire |
| B · Recentrage et imputation à l'ESN de la crise et de l'outillage commun, F-08 retiré (4 058,00 €) | respecte 4 200 € (marge 142 €) ; correctifs de crise réalisés | F-08 (exigence RGPD) retiré ; revient sur DEC-009 et DEC-013 |
| **B en gardant F-08 (4 169,43 €)** | respecte 4 200 € ; F-08 et l'exigence RGPD gardés ; seul F-06 sort du CDC | marge de 30,57 € sans réserve pour les aléas ; revient sur DEC-009 et DEC-013 |
| D · Maintien et dépassement (6 050,72 €) | périmètre complet | +1 850,72 € (avenant ou charge de l'ESN) ; délai non tenu (fin projetée le 2026-12-21) |

## Décision
1. **Scénario B en gardant F-08.** Le budget client devient **4 200 € HT** et la deadline du 2026-12-18 est inchangée. Coût projeté pour le client : 4 169,43 €.
2. **F-08 (purge à 12 mois, T-028 et T-037) est gardé.** **F-06 (fiches des salles, T-027), un Should, est abandonné.** T-065 (dette de tests et de documentation) et T-076 (message de la page de consultation) passent `ANNULE`, comme dans le scénario B.
3. **L'ESN prend à sa charge, comme proposé dans T-093 § 3.4 :**
   - le coût de la crise : T-081, T-083, T-085 à T-087, T-089 à T-092 et leurs revues ;
   - l'outillage commun : T-029 et T-038, T-058 et T-059, T-072, T-078 et sa revue.

   Total : 1 789,64 €. Ces tickets **restent réalisés** : T-029, T-087 et T-092 sont faits avant le GO, et T-078 aussi. Cette décision revient sur DEC-009 (T-029 au budget client) et sur le chiffrage de T-058 dans DEC-013. T-080 (69 € consommés) reste au projet.
4. **Condition 1, alerte et arbitrage préalable.** La marge n'est que de 30 €. Une alerte budget est levée **dès que 90 % des 4 200 € sont consommés** (3 780 €). Tout **dépassement prévisible** donne lieu à un **arbitrage humain et à une discussion avec le client avant d'être engagé** (avenant ou nouveau retrait de périmètre), **jamais après**. Aucun dépassement n'est absorbé d'office par l'ESN.
5. **Condition 2, message au client.** Le message explique la répartition : le périmètre est réduit de F-06 pour répondre à la demande budgétaire du client, et les coûts de la crise sont pris en charge par l'ESN. Claire le relit et l'envoie (AF1).
6. **Allocations** (proposition de T-093, appliquée sans projet interne, voir Impacts) :
   - Nadia : 10 % pour la part client et 40 % pour la part imputée à l'ESN, jusqu'au 2026-12-18 ;
   - Karim : +5 % pour les revues imputées à l'ESN.

7. **(v0.2) F-08 n'est plus abandonnable.** La purge à 12 mois (CDC § 8, RGPD) devient obligatoire, **par exception à la règle de DEC-009** qui permettait d'abandonner les Should quand la marge passe sous 2 jours ouvrés. Seul F-06 reste abandonné. Le CDC v1.1 et le planning v1.1 l'écrivent.

## Pourquoi
Les mots d'Ethan :
- « F-08 (purge à 12 mois) est une exigence RGPD du CDC § 8, on ne la sacrifie pas pour le budget. F-06 est abandonné (Should) ; l'ESN prend à sa charge le coût de la crise et des outils communs, comme proposé. »
- Sur les conditions : « La marge n'étant que de 30 €, une alerte budget est levée dès 90 % des 4 200 € consommés, et tout dépassement prévisible fait l'objet d'un arbitrage humain et d'une discussion avec le client AVANT d'être engagé (avenant ou nouveau retrait de périmètre), jamais après. »

Les arguments de T-093 :
- c'est le seul scénario qui respecte 4 200 € sans toucher aux Must, à la sécurité, aux revues humaines ni à la recette ;
- l'ESN ne paie que ce qui relève d'elle : sa faute (la crise) et ses outils (principe D de DEC-009).

## Impacts
- **`projets/reservation-coworking/projet.md`** : `budget_eur: 4200` ; allocations de Nadia et de Karim ; historique.
- **`equipe/membres/nadia.md`** : allocation à `reservation-coworking` de 30 % (DEC-019) à **50 %** (10 % client et 40 % imputés à l'ESN) jusqu'au 2026-12-18. **`equipe/membres/karim.md`** : de 15 % à **20 %**.
- **Mécanique de l'imputation.** T-093 proposait de déplacer les tickets imputés vers un projet interne de l'ESN. Cet espace n'existe pas : sa création est une décision humaine encore ouverte, qui passe par R11 (`docs/a-integrer/lot2-D.md` point 9 ; DEC-002). En attendant :
  - les tickets imputés **restent dans ce projet**, avec une ligne de journal « imputé à l'ESN (DEC-020) » ;
  - les allocations ci-dessus couvrent les deux parts sur ce projet ;
  - la dépendance `T-046 → T-029` est gardée.

  **Conséquence** : le coût projeté et le budget consommé de `TABLEAU.md` incluent la part de l'ESN. Le coût pour le client = coût projeté du tableau − part imputée à l'ESN. L'alerte `tableau.py` à 90 % du budget consommé se déclenchera donc plus tôt que le seuil réel du client : c'est une alerte prudente, que le `chef-de-projet` doit corriger de la part imputée dans le suivi (`avancement`).
- **CDC et planning** : `cdc.md` (v1.0) et `planning.md` (v1.0) sont `VALIDÉ` et ne sont pas modifiés (R6).
  - Le retrait de F-06 demande un CDC v1.1 : l'humain repasse `cdc.md` `EN_REVUE`, puis l'`analyste-besoin` le révise.
  - Le nouveau budget et les annulations demandent un `planning.md` v1.1 : l'humain le repasse `EN_REVUE`, puis le `chef-de-projet` le révise.
- **Tickets** (appliqués par le `chef-de-projet`) :
  - T-027, T-065 et T-076 passent `ANNULE` ;
  - une ligne « imputé à l'ESN » est ajoutée dans le journal des tickets imputés ;
  - un ticket est créé pour le message au client de Claire (condition 2) ;
  - la condition 1 devient un critère du pilotage T-008.
- **T-093** reste `ATTENTE_HUMAIN` jusqu'à ce qu'Ethan renseigne lui-même `decision: DEC-020`.
- **(v0.2)** Ethan a repassé `cdc.md` et `planning.md` en `EN_REVUE` pour leur v1.1. Le `chef-de-projet` crée les revues humaines manquantes de Karim (imputées à l'ESN quand le ticket relu l'est), et ajoute T-087, T-092 et T-078 à `depend_de` de T-046.

## Question ouverte (pour une future PR de règles, R11)
**Comment suivre les coûts pris en charge par l'ESN ?** Aujourd'hui, `tableau.py` impute au budget du projet client tout ticket rangé dans le projet. La part de l'ESN se retranche donc à la main (DEC-020, Impacts), et l'alerte à 90 % se déclenche trop tôt. Deux pistes, à trancher par une PR accompagnée d'une décision et d'une entrée dans `docs/CHANGELOG-REGLES.md` :
- **(a) Un projet interne de l'ESN** (par exemple `projets/esn-interne/`), avec son budget de fonctionnement ; les tickets imputés y sont déplacés. Cela suppose de régler la question restée ouverte en `docs/a-integrer/lot2-D.md` point 9 (DEC-002) et le suivi des dépendances d'un projet à l'autre (le GO dépend de T-029, T-087 et T-092).
- **(b) Une imputation dans le tableau** : un champ de ticket (par exemple `imputation: client | esn`) lu par `tableau.py`, qui sépare le coût client du coût ESN et applique l'alerte au seul coût client. Cela modifie `templates/ticket.md` (champ ajouté) et `scripts/tableau.py`.

En attendant, la convention provisoire de DEC-020 s'applique : une ligne de journal « imputé à l'ESN (DEC-020) » dans chaque ticket concerné, et un calcul manuel du coût client dans le pilotage (T-008).
