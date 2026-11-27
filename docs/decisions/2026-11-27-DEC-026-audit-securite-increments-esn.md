---
titre: "reservation-coworking : dépassement de l'audit de sécurité T-043, audits d'incrément pris en charge par l'ESN, audit avant GO au client (option D) ; pilotage T-008 +2 h"
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-27
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-026           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-026
date: 2026-11-27
decide_par: Ethan
projet: reservation-coworking
ticket: T-107
modifie_une_regle: non      # application de R18 à des tickets ; la règle 6 du chef-de-projet (audit par incrément) sera modifiée par la PR de l'action A6 (DEC-025)
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-026 — Audit de sécurité : audits d'incrément à l'ESN, audit avant GO au client

Rédigé par le coordinateur le 2026-11-27 à partir de la décision d'Ethan sur [T-107](../../projets/reservation-coworking/tickets/T-107-arbitrage-audit-securite-avant-go.md). Le « Pourquoi » est celui formulé par Ethan (skill `tracer-decision`, étape 1). L'en-tête fait foi pour le statut de ce document.

## Contexte
- [T-043](../../projets/reservation-coworking/tickets/T-043-audit-securite.md) « Audit sécurité » (`agent:securite`) était estimé à **5 h**. **12,5 h** ont été passées en 7 audits d'incrément, tous `NON BLOQUANT`. Ces audits découlent de [DEC-011](2026-11-25-DEC-011-increment-consultation-coworking.md) : chaque ticket de l'incrément de soutenance passait par `securite`.
- Le temps passé dépasse l'estimation. `tableau.py` compte donc un reste de 0 h, et l'**audit avant GO** (porte 3 de S3, environ 5 h, soit 75 €) n'était compté nulle part.
- La proposition de découpage du `chef-de-projet` du 2026-11-25 n'avait jamais été arbitrée. Le retex de l'ESN l'a relevé (constat P6, action A6, [DEC-025](2026-11-27-DEC-025-actions-retrospective-semaine.md)).
- Le pilotage [T-008](../../projets/reservation-coworking/tickets/T-008-pilotage.md) a le même défaut : il a 0 h de reste, alors que le suivi jusqu'au 2026-12-18 et le retex du projet restent à faire.
- Coût client projeté, confirmé par `tableau.py` le 2026-11-27 : **4 122,32 €** pour un budget de 4 200 € HT (budget issu de la SIMULATION [DEC-020](2026-11-26-DEC-020-simulation-budget-4200.md)). Si tout restait au client, avec l'audit avant GO et la réserve de pilotage, il serait de **4 227,32 €**, soit un dépassement prévisible de 27,32 €. La condition 1 de DEC-020 impose de l'arbitrer avant de l'engager.

## Options étudiées
| Option (détail dans T-107) | Avantages | Inconvénients |
|---|---|---|
| A · Découpage, tout au client | règle 3 respectée ; rien à la charge de l'ESN | 4 227,32 € avec le pilotage : dépassement de 27,32 €, qui demande un second arbitrage (avenant ou prise en charge) avant l'audit |
| B · Un seul ticket de 17,5 h | aucun ticket nouveau | même coût que A ; contraire à la règle 3 ; l'audit avant GO disparaît du Gantt |
| C · Découpage, audit avant GO à l'ESN | 4 152,32 € (98,9 %) | l'ESN paierait une porte S3 prévue depuis DEC-009 et achetée par le client, alors que l'écart vient des audits d'incrément |
| **D · Découpage, audits d'incrément (T-043) à l'ESN, audit avant GO au client** | le client paie l'audit qu'il a acheté ; l'ESN paie son choix interne (DEC-011) et son absence de ré-estimation ; 4 039,82 € (96,2 %) avec le pilotage | ces audits ont aussi amélioré le code du client (13 constats fermés sur 20) ; part ESN +187,50 € |
| E · Audit avant GO réduit à 3 h | 4 197,32 € avec le pilotage | pari d'estimation sur la partie la plus sensible (authentification, sessions, autorisation) juste avant le GO |

## Décision
**Question 1 : option D. Question 2 : oui.**
1. **T-043** est ré-estimé à **12,5 h** (= temps passé) et renommé « Audits d'incrément (DEC-011) ». Ses critères sont réécrits sur les 7 rapports existants. Il passe en **`imputation: esn`, avec `imputation_decision: DEC-026`** (R18), puis il est conclu par le coordinateur (R13). Montant pris en charge par l'ESN : 12,5 h × 15 € = **187,50 €**.
2. **Un nouveau ticket `tache` « Audit sécurité avant GO »** est créé : `agent:securite`, `securite-applicative (confirme)`, **5 h**, **au client** (`imputation: client`). Il reprend les dépendances et les critères actuels de T-043, avec l'examen de l'écart « clé de signature des sessions » (DEC-007), et remplace T-043 dans `depend_de` de **T-045** (recette) et de **T-046** (GO). L'audit avant GO garde son périmètre complet : il n'est pas réduit.
3. **T-008** (pilotage) est ré-estimé de 13,25 h à **15,25 h** (+2 h, 30 €, au client) pour le suivi jusqu'au 2026-12-18 et le retex du projet.
4. **Aucun avenant au client** n'est nécessaire.

## Pourquoi
*(Ethan, 2026-11-27)* « Le client paie l'audit de sécurité qu'il a acheté avant la mise en production. Les audits faits à chaque incrément viennent de notre choix interne de livrer par petits morceaux (DEC-011), c'est donc à l'ESN de les assumer. On garde l'audit avant GO complet (5 h) car l'authentification est la partie la plus sensible juste avant le GO. On ajoute 2 h au pilotage pour que le coût projeté corresponde au travail qui reste vraiment. Le client reste à 96,2 % de son budget, sans avenant. »

## Impacts
- **Budget client de `reservation-coworking`** (4 200 € HT) : coût client projeté **4 039,82 €, soit 96,2 %**, avec 160,18 € de marge. Consommé client : 1 198,79 € (28,5 %). Le coût client reste au-dessus du seuil d'alerte S1-R11 de 90 % (3 780 €), mais l'écart est maintenant arbitré : l'alerte reste visible dans le tableau.
- **Part ESN de `reservation-coworking`** : projetée de 1 652,50 € à **1 840,00 €** (+187,50 €) ; consommé ESN de 22,50 € à 210,00 €. Elle est visible dans `TABLEAU.md` et `PORTFOLIO.md` (R18).
- **Budget de fonctionnement d'`esn-interne`** (4 360 €, DEC-024) : **non touché**. Un ticket `imputation: esn` d'un projet client reste dans ce projet (R18, R19, `tableau.py`). Le projeté d'`esn-interne`, rétrospective (DEC-025) comprise, reste à **3 835,71 €, soit 88,0 %**, sous le seuil de 3 924 €.
  - *Pour mémoire* : si ces 187,50 € étaient comptés dans `esn-interne`, le projeté serait de 4 023,21 €, soit **92,3 %**, au-dessus du seuil.
  - **Dépense totale projetée de l'ESN** : 3 835,71 € (`esn-interne`) + 1 840,00 € (part ESN de `reservation-coworking`) = **5 675,71 €**.
  - **Aucune règle ne plafonne la part ESN d'un projet client** : chaque prise en charge exige une décision humaine `VALIDÉ` (R18), mais aucun budget global de l'ESN ne l'encadre.
- **Chemin critique** : aucun effet. L'audit avant GO tient en un jour ouvré, avant la recette (2026-12-10) ; GO le 2026-12-15, fin projetée le 2026-12-16.
- **Lien avec DEC-025** : l'action A7 (outils de l'agent `securite`) doit être faite avant l'audit avant GO. Si son ticket `esn-interne` n'est pas `TERMINE` à temps, le ticket « Audit sécurité avant GO » passe `BLOQUE`, avec `bloque_par: amelioration esn-interne/T-NNN`. `depend_de` ne traverse pas les projets.
- **Tickets, après la validation de ce fichier** (rien n'est écrit avant, en particulier `imputation: esn`, R18) :
  - T-107 : `decision: DEC-026`, débloqué par l'humain ;
  - le `chef-de-projet` applique les points 1 à 3 (T-043, nouveau ticket, T-045, T-046, T-008), avec une ligne de journal qui cite DEC-026 ;
  - le coordinateur conclut T-043 et relance `tableau.py`. Le coût client projeté doit alors être de 4 039,82 €, sans ajout manuel.
- **Règles** : aucune modifiée.
