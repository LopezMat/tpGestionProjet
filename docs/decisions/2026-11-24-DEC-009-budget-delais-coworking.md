---
titre: Budget, délais et allocations du projet reservation-coworking
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-24
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-009           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-009
date: 2026-11-24
decide_par: Ethan
projet: reservation-coworking
ticket: T-007
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-009 — Budget, délais et allocations (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir des décisions d'Ethan du 2026-11-24 sur T-007. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`, après relecture de `planning.md` v0.2. Chaque « Pourquoi » est celui formulé par Ethan (skill `tracer-decision`, étape 1).

## Contexte
Étape 4 du pipeline : le `chef-de-projet` a découpé le projet (T-007 à T-053), rédigé [planning.md](../../projets/reservation-coworking/planning.md) et posé le ticket [T-007](../../projets/reservation-coworking/tickets/T-007-validation-budget-delais.md) « Validation du budget et des délais » (points A à E), à partir du CDC v1.0 (DEC-006) et de l'architecture v1.1 (DEC-007, DEC-008). Budget client : 6 000 € HT ; deadline : 2026-12-18. Prévision initiale : 3 724,64 € (62 %), 4 567,68 € avec une marge de risque de 25 % ; GO le 2026-12-14, mise en production le 2026-12-15, 3 jours ouvrés de marge.

## Options étudiées
| Point | Options (détail dans T-007) | Retenue |
|---|---|---|
| A. Périmètre | A1 Must + Should F-06 et F-08 ; A2 Must seuls | **A1, Should abandonnables** |
| B. Allocations | B1 Claire 20 %, Karim 15 %, Nadia 20 %, Hugo 10 % si le lot ESN reste ; B2 tous à 10 % (déploiement après la deadline) | **B1 sans Hugo** (Hugo 0 %) |
| C. Jalons | C1 GO le 2026-12-14 ; C2 GO le 2026-12-11 (recette concentrée) | **C1** |
| D. Lot ESN (T-006, T-050 à T-053) | D1 sortir du projet client ; D2 le laisser (budget affiché 4 242,50 €) | **D1** |
| E. Formations et compétences | recommandation du `chef-de-projet` ; autre | **Recommandation du `chef-de-projet`** |

## Décision
1. **A. Périmètre** : les 5 Must (F-01, F-02, F-03, F-04, F-07) et les Should F-06 (T-027) et F-08 (T-028). **Les Should sont planifiés après tous les Must et marqués abandonnables : si la marge passe sous 2 jours ouvrés avant la deadline, ils sont retirés sans toucher aux Must.**
2. **B. Allocations** : **Claire 20 %** (au lieu de 10 %, DEC-005), **Karim 15 %**, **Nadia 20 %**, **Hugo 0 %**. Hugo est retiré de `salaries_affectes` dans `projet.md`.
3. **C. Jalons** : **GO le 2026-12-14**, déploiement et mise en service le 2026-12-15, marge jusqu'au 2026-12-18.
4. **D. Lot ESN** : la règle R17 et son outillage sortent du projet client. **T-006, T-050, T-051, T-052 et T-053 passent `ANNULE`** avec la mention « déplacé vers les règles de l'ESN (PR de règles) » (voir [DEC-010](2026-11-24-DEC-010-principe-r17.md) pour T-050).
5. **E. Formations et compétences** : la recommandation du `chef-de-projet` est suivie. Pour rappel, elle consiste à :
   - **ne pas créer de ticket `formation` dans ce projet** : les besoins repérés sont inscrits au **plan de formation de l'ESN** (projet interne) :
     - `relation-client` et `recette-fonctionnelle` : Claire seule ; un empêchement bloquerait la recette, donc le GO ;
     - `sauvegarde-restauration` : Nadia seule ; la revue humaine de T-029 porte donc sur le code Python, par Karim ;
     - `juridique` : compétence absente ; la mention RGPD est validée par le client, responsable du traitement ;
     - formation « supervision » de Nadia du 2026-12-03 (EV-002) : elle ne sert pas ce client ;
   - les formations de Hugo (T-052 `backend-python`, T-053 `securite-applicative`) suivent le lot ESN (point D) ;
   - **ne pas retenir la revue d'accessibilité par Léa** (1,5 h, 96,43 €) : les bonnes pratiques de base (H-07) sont vérifiées par `relecteur-code`, le test de bout en bout et la recette.

## Pourquoi
*(Ethan, 2026-11-24)*
- **A** : le budget le permet, mais pas au prix de la deadline.
- **B** : couvrir les rôles du chemin critique (client et recette, revues de sécurité, sauvegarde) sans coût inutile.
- **C** : pas de « Pourquoi » distinct formulé ; option recommandée par le `chef-de-projet` (3 jours ouvrés de marge, recette sans concentration de la charge de Claire).
- **D** : le client ne paie pas l'amélioration de nos outils internes.
- **E** : pas de « Pourquoi » distinct formulé ; Ethan suit la recommandation du `chef-de-projet` (besoins de l'ESN, pas du client).

## Impacts
- Fichiers ou règles à mettre à jour :
  - `projets/reservation-coworking/planning.md` : v0.2 par le `chef-de-projet` (sans le lot R17, budget et dates recalculés, règle d'abandon des Should), puis `VALIDÉ` par un humain (`valide_par`, `decision: DEC-009`) ;
  - `equipe/membres/claire.md` (20 %), `karim.md` (15 %), `nadia.md` (20 %) : par le coordinateur, **après la validation** de cette décision ; `hugo.md` inchangé (0 %) ;
  - `projets/reservation-coworking/projet.md` : `salaries_affectes: [claire, karim, nadia]`, historique des décisions.
- Tickets créés ou débloqués :
  - T-007 débloqué par l'humain (`decision: DEC-009`) ;
  - T-006, T-051, T-052, T-053 passés `ANNULE` par le `chef-de-projet` ; T-050 passé `ANNULE` par l'humain (DEC-010) ;
  - T-027 et T-028 marqués « Should, abandonnables » ;
  - après validation : signaler T-009 à Claire et T-029 à Nadia (tickets à faire par des humains, R15), puis lancer `dev-backend` sur T-010.
- **Chiffres recalculés dans `planning.md` v0.2** (sans le lot R17) : **3 739,64 € HT (62,3 %)** sans marge, **4 582,68 € (76,4 %)** avec la marge de risque de 25 % ; 3 632,85 € si les Should sont abandonnés. GO le 2026-12-14, mise en production le 2026-12-15, 3 jours ouvrés de marge, à condition que les allocations soient reportées le 2026-11-25 (chaque jour de retard coûte un jour de marge). L'abandon des Should ne rend qu'environ 1 jour ouvré.
- **Supervision** : le `chef-de-projet` surveille la marge avant la deadline (skill `avancement`) et alerte l'humain si elle passe sous 2 jours ouvrés (abandon des Should, décision humaine).
- Règles : aucune règle modifiée.
