---
titre: Planning — Réservation de salles, Coworking Les Arcades (Perpignan)
statut: EN_REVUE
responsable: agent:chef-de-projet
version: 1.1
maj_le: 2026-11-26
valide_par:
decision:
---
> **SIMULATION** — La v1.1 intègre les décisions simulées DEC-019 (crise) et DEC-020 (révision du budget) ; la v1.0 validée (DEC-009) reste dans l'historique Git.

<!-- modèle : templates/planning.md v0.1 · responsable du modèle : A -->

# Planning — Réservation de salles, Coworking Les Arcades (Perpignan)

> Le Gantt détaillé est **généré** dans `TABLEAU.md` à partir des tickets. Ce document fixe les jalons et les hypothèses.

Sources : [CDC](cdc.md) (v1.0 `VALIDÉ`, DEC-006 ; v1.1 en révision par l'`analyste-besoin`, `EN_REVUE`), [architecture v1.1](architecture.md) (`VALIDÉ`, DEC-007, DEC-008), `equipe/`, `equipe/calendrier.md`. Décisions : [DEC-009](../../docs/decisions/2026-11-24-DEC-009-budget-delais-coworking.md) (budget et délais, T-007), [DEC-010](../../docs/decisions/2026-11-24-DEC-010-principe-r17.md) (R17), [DEC-019](../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md) (crise T-080, SIMULATION) et [DEC-020](../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md) (révision du budget, T-093, SIMULATION). Chiffres : `python scripts/tableau.py` du 2026-11-26, lancé après le triage (revues T-095 à T-100, prérequis du GO).

## Historique
- **v1.0** (2026-11-25, `VALIDÉ` par Ethan, DEC-009). Changements depuis la v0.1 :
  - A1 : 5 Must, Should F-06 (T-027) et F-08 (T-028) planifiés après tous les Must et abandonnables ;
  - B1 sans Hugo : Claire 20 %, Karim 15 %, Nadia 20 % ;
  - C1 : GO le 2026-12-14 ;
  - D1 : lot R17 sorti du projet client ;
  - E : aucun ticket `formation` dans ce projet.
- **v1.1** (2026-11-26, `EN_REVUE`, **SIMULATION**). Changements depuis la v1.0 :
  - **budget** : 4 200 € HT au lieu de 6 000 € (DEC-020) ; deadline du 2026-12-18 inchangée ;
  - **marge** : la marge de risque de 25 % est remplacée par une **condition d'alerte** (DEC-020, condition 1) ;
  - **périmètre** : F-06 abandonné (T-027 `ANNULE`) ; T-065 et T-076 `ANNULE` (DEC-020) ; T-088 `ANNULE`, couvert par T-092 (DEC-019) ;
  - **F-08 obligatoire** : il n'est plus abandonnable, par exception à la règle d'abandon de DEC-009 (DEC-020, point 7) ;
  - **crise** (DEC-019) : T-029 passe `critique` et devient prérequis du GO ; actions correctives T-081 à T-092 ;
  - **revues humaines** créées au triage : T-095 à T-100 (Karim) ;
  - **prérequis du GO** : T-087, T-092 et T-078 ajoutés à `depend_de` de T-046, à côté de T-029 ;
  - **allocations** : Karim 20 %, Nadia 50 % jusqu'au 2026-12-18 (DEC-019, DEC-020) ;
  - **imputation à l'ESN** de la crise et de l'outillage commun (DEC-020, point 3), suivie par une ligne de journal dans chaque ticket ;
  - **jalons** recalculés : GO le 2026-12-15 (au lieu du 2026-12-14), mise en service le 2026-12-16, marge de 2 jours ouvrés.

## Jalons
**Hypothèse de départ** : les tickets `ATTENTE_HUMAIN` (T-057, T-081, T-083, T-093) sont supposés débloqués aujourd'hui, comme le fait `tableau.py` ; leurs dates sont donc optimistes. Les dates ci-dessous sont celles du Gantt de `TABLEAU.md` (2026-11-26), sauf mention contraire.

| Jalon | Date cible | Tickets inclus | Critère de passage |
|---|---|---|---|
| CDC validé | 2026-11-24 (atteint) ; CDC v1.1 à valider | T-001, T-003 | décision humaine (DEC-006) ; v1.1 : F-06 retiré, F-08 obligatoire, décision humaine à venir |
| Architecture validée | 2026-11-24 (atteint) | T-004, T-005 | décision humaine (DEC-007, DEC-008) |
| Budget, délais et allocations | DEC-009 (2026-11-24, atteint) ; révision DEC-020 (2026-11-26) ; planning v1.1 à valider | T-007, T-093 | décision humaine ; allocations reportées dans `equipe/` par le coordinateur (fait le 2026-11-26) |
| Information du client | 2026-11-30 | T-094 (budget et périmètre), T-083 (crise) | message relu et envoyé par Claire (AF1) |
| Points client traités (mention RGPD, recette) | 2026-11-30 | T-009 | texte validé par Marie Lenoir |
| Sauvegarde quotidienne et limite d'âge | 2026-11-27 ; revue T-038 le 2026-12-02 | T-029, T-038 | PR acceptée par C, tests de `scripts/` verts, ligne « Revue humaine » remplie |
| Authentification livrée et revue | 2026-12-04 ; revues T-030 à T-036 jusqu'au 2026-12-03 | T-013 à T-017, T-020 ; T-030 à T-036 | tickets `TERMINE` (R13) |
| **Fin des Must** | **2026-12-04** | T-010 à T-026, correctifs T-061, T-069, T-070, T-075 | tickets `TERMINE` (R13) |
| F-08 (obligatoire) | T-028 le 2026-12-04 ; revue T-037 le 2026-12-09 (à avancer, voir le chemin critique) | T-028, T-037 | tickets `TERMINE` (R13) |
| MVP en recette | 2026-12-07 | T-041, T-042, T-043, T-044, T-067 | tests `CONFORME` et sécurité `NON BLOQUANT` sur le même SHA ; environnement de recette au SHA candidat |
| Correctifs de crise et outillage commun (imputés à l'ESN) | du 2026-12-04 au 2026-12-11 ; revues au plus tard le 2026-12-14 | T-058, T-072, T-078, T-085 à T-087, T-089, T-092 ; revues T-059, T-095 à T-099 | tickets `TERMINE` ; PR acceptées par C ou D |
| Recette | 2026-12-09 → 2026-12-15 | T-045 | rapport de recette `CONFORME` sur le SHA candidat (S3-R9) |
| **Prérequis du GO** | **2026-12-14** au plus tard | T-029, T-087, T-092, T-078 (et leurs revues T-038, T-097, T-098, T-099), T-069 | tickets `TERMINE` (`depend_de` de T-046) |
| **GO mise en production** | **2026-12-15** (C1 visait le 2026-12-14) | T-046 | décision humaine qui cite le SHA (S3-R3, R16) |
| Mise en production | 2026-12-15 → 2026-12-16 | T-047, T-048 | `verifier-prod` OK (SHA en ligne = SHA attendu) ; compte accueil initial, tâches planifiées de sauvegarde et de vérification en place |
| Marge avant la deadline | 2026-12-17 → 2026-12-18 | — | **2 jours ouvrés** ; sous 2, condition d'alerte (voir « Charge et budget ») |
| Deadline client | 2026-12-18 | — | mise en ligne |
| Fin de démonstration | après la soutenance | T-049 | décision humaine (DEC-008) ; `tableau.py` le place le 2026-12-16, d'où sa fin projetée |

**Chemin critique.** Chaîne de `dev-backend` jusqu'à la fin des Must (T-020, 2026-12-04) → T-028 (F-08, 2026-12-04) → **T-037** (revue de Karim, placée le 2026-12-09) → T-045 (recette, 2026-12-09 → 2026-12-15) → T-046 (GO, 2026-12-15) → T-047 → T-048 (2026-12-15 → 2026-12-16).
- **T-037 est désormais sur le chemin critique** : F-08 étant obligatoire, la recette en dépend. `tableau.py` le place le 2026-12-09 parce que T-037 est en priorité `normale`, derrière les revues `haute` T-095 à T-099 dans la file de Karim. Si Karim le traite dès que T-028 passe `EN_REVUE` (vers le 2026-12-04), la recette peut commencer plus tôt, et le GO revenir vers le 2026-12-14 (C1) ; à confirmer par `tableau.py` après la décision (voir « Risques »).
- **Le second goulot est la recette de Claire** : 4,75 h à 1,4 h par jour, soit 4 à 5 jours ouvrés.
- **Les prérequis du GO portés par Nadia** (T-092 et T-078, finis le 2026-12-11) et leurs revues (T-098, T-099) laissent 1 à 2 jours ouvrés avant le GO.

**Tickets salariés sur le chemin critique** (AF11, R15 : à faire par des humains, jamais par le coordinateur) :
- Karim : T-030 à T-037, T-038, et les revues des prérequis du GO T-097, T-098, T-099 ;
- Nadia : T-029, T-044, T-048, ainsi que T-087, T-092 et T-078 (prérequis du GO) ;
- Claire : T-009, T-045, T-046.

**Revues humaines et `depend_de` (AF3).** Les revues T-095 à T-100 n'ont pas de `depend_de` vers le ticket relu, qui ne peut passer `TERMINE` qu'avec la ligne « Revue humaine » remplie : la dépendance bloquerait les deux tickets. Elles reprennent les dépendances du ticket relu et deviennent prenables quand il passe `EN_REVUE`. Conséquence : `tableau.py` peut placer une revue avant la fin du ticket relu (T-095 et T-096 le 2026-12-04, alors que T-085 et T-086 finissent les 2026-12-07 et 08). La date réelle est le lendemain de la fin du ticket relu.

**Absences prises en compte** (S1-R9) :
- Nadia : pas de travail le mercredi (4/5), et en formation le 2026-12-03 (EV-002). T-029 finit avant, et ses tickets suivants commencent le 2026-12-04.
- Karim : en congés du 2026-12-21 au 31 (EV-003), après la deadline. Toutes ses revues sont placées avant le 2026-12-11. Risque sur la garantie de livraison (voir « Risques »).
- Hugo : départ le 2026-12-04 (EV-004, SIMULATION). Sans effet : il n'a ni allocation ni ticket dans ce projet.
- Léa : absente les 2026-11-26 et 27 (EV-001). Sans effet : aucun ticket.
- Jours fériés du 25 décembre et du 1er janvier : hors période.

### Règle d'abandon des Should : levée (DEC-020)
- La règle de DEC-009 (« si la marge passe sous 2 jours ouvrés, les Should sont retirés sans toucher aux Must ») **n'a plus d'objet dans ce projet** :
  - F-06 est déjà abandonné (T-027 `ANNULE`) ;
  - F-08 (T-028, T-037) est **obligatoire**, par exception à cette règle (DEC-020, point 7 : exigence RGPD du CDC § 8).
- **Mesure de la marge**, inchangée : jours ouvrés entre la fin prévue de T-048 (mise en service) et la deadline, deadline incluse. Valeur au 2026-11-26 : **2** (T-048 finit le 2026-12-16).
- **Si la marge passe sous 2 jours ouvrés**, ou si la fin projetée de T-048 dépasse la deadline :
  - aucun retrait automatique n'est possible ;
  - le `chef-de-projet` crée un ticket `decision` en `ATTENTE_HUMAIN` (S1-R11, R7 : au moins 2 scénarios chiffrés) **avant d'engager** le travail qui ferait glisser la date ;
  - Claire en discute avec le client (AF1).

## Hypothèses de capacité
| Ressource | Type | Allocation au projet | h/semaine disponibles | Taux €/h |
|---|---|---|---|---|
| agent:dev-backend | agent | — | 35 | 15 |
| agent:dev-frontend | agent | — | 35 | 15 |
| agent:relecteur-code | agent | — | 35 | 15 |
| agent:testeur | agent | — | 35 | 15 |
| agent:securite | agent | — | 35 | 15 |
| agent:deployeur | agent | — | 35 | 15 |
| agent:chef-de-projet | agent | — | 35 | 15 |
| salarie:claire | salarié | 20 % (DEC-009) | 7 | 78,57 |
| salarie:karim | salarié | 20 % (DEC-020 ; 15 % pour le client, 5 % pour les revues imputées à l'ESN) | 7 | 78,57 |
| salarie:nadia | salarié | 50 % jusqu'au 2026-12-18 (DEC-020 ; 10 % pour le client, 40 % pour la part imputée à l'ESN) | 14 (sur 28 h, temps partiel) | 64,29 |

Hugo : 0 %, aucun ticket dans ce projet (DEC-009). Léa : 0 %.

Capacité d'un agent : 7 h équivalent humain par jour ouvré, un ticket à la fois (ARCHITECTURE § 7). Le coordinateur peut lancer en parallèle des tickets sans dépendance entre eux.

**Utilisation des salariés (AF9, indicateur)**, selon `tableau.py`, du 2026-11-26 au 2026-12-18 :

| Salarié | h restantes assignées | Capacité allouée | Utilisation | Dont part imputée à l'ESN |
|---|---|---|---|---|
| Claire | 9,25 h | 23,8 h | **38,9 %** | 1,5 h (T-083, T-091) |
| Karim | 12,25 h | 23,8 h | 51,5 % | 3,5 h (T-038, T-059, T-095 à T-099) |
| Nadia | 24,0 h | 44,8 h | 53,6 % | 21,5 h (tous ses tickets sauf T-044, T-048 et T-049) |

- **Claire est sous 50 %, ce qui est signalé.** DEC-020 garde ses 20 % jusqu'au GO pour la réactivité de la recette ; aucun ticket n'est ajouté pour atteindre un taux.
- **Karim** : la revue T-089 (0,5 h) est comptée sur Nadia, assignée de ce ticket.
- **Nadia** : sa part client (2,5 h) tient dans ses 10 %, et sa part imputée à l'ESN (21,5 h) dans ses 40 %.

**Réductions d'allocation proposées après les jalons** : ce sont de **futures décisions humaines**, que le `chef-de-projet` proposera au jalon et que le coordinateur appliquera ensuite :
- Karim à 5 % après ses dernières revues (vers le 2026-12-14), à condition que la recette ne demande pas de reprise de l'authentification ;
- Claire à 10 % après le GO, en gardant la relation client pendant la garantie de livraison ;
- Nadia : l'allocation de DEC-020 prend fin le 2026-12-18 ; ensuite 5 % jusqu'à T-049.

## Charge et budget prévisionnels
*Chiffres de `python scripts/tableau.py` du 2026-11-26, après le triage. Taux : 15 €/h pour un agent ; Claire et Karim 550 €/j ÷ 7 = 78,57 €/h ; Nadia 450 €/j ÷ 7 = 64,29 €/h.*

- **Budget client** : **4 200 € HT** (DEC-020, au lieu de 6 000 €, DEC-009). Deadline inchangée.
- **Charge** : 207,8 h estimées hors `ANNULE`, dont 36,5 h terminées (avancement 17,6 %). Reste : **130,7 h**, réparties ainsi :
  - agents : 85,2 h, 1 278,00 € ;
  - Claire : 9,25 h, 726,79 € ;
  - Karim : 12,25 h, 962,50 € ;
  - Nadia : 24,0 h, 1 542,86 €.
- **Budget consommé (tableau)** : **1 348,79 €**, soit 32,1 % de 4 200 €.
- **Coût projeté à terminaison (tableau)** : **5 858,93 €**. Il comprend la part imputée à l'ESN, que `tableau.py` ne sait pas séparer (DEC-020, Impacts).

### Imputation à l'ESN (DEC-020, point 3)
Les tickets imputés **restent dans ce projet et sont réalisés**. Chacun porte la ligne de journal « imputé à l'ESN (DEC-020) ». Aucun n'a de temps passé à ce jour.

| Bloc | Tickets | h | € (tableau) |
|---|---|---|---|
| Crise (T-080) | T-081 (1,5 h), T-085 (1,5 h), T-086 (2 h), T-087 (1,5 h), T-089 (2,5 h), T-092 (4 h) de Nadia ; T-083 (1 h), T-091 (0,5 h) de Claire ; revues T-095 à T-098 (2 h) de Karim ; T-090 (0,5 h) du `chef-de-projet` | 17,0 | 1 118,21 |
| Outillage commun | T-029 (4,5 h), T-058 (2 h), T-072 (0,5 h), T-078 (1,5 h) de Nadia ; revues T-038, T-059, T-099 (1,5 h) de Karim | 10,0 | 664,29 |
| **Total imputé (base du tableau)** | | **27,0** | **1 782,50** |
| Écart de taux de T-089 (0,5 h de Karim comptée au taux de Nadia) | | | 7,14 |
| **Total à la charge de l'ESN** | | | **1 789,64** (montant de DEC-020) |

Restent au budget client : T-080 (69 € déjà consommés, historique de l'incident), T-044, T-048 et T-049 (exploitation propre au client), T-079 et sa revue T-100.

### Coût client
**Formule** (convention provisoire de DEC-020) :

> coût client = coût projeté du tableau − part imputée à l'ESN (base du tableau) + coûts connus que le tableau ne compte pas

Calcul : 5 858,93 − 1 782,50 + 75,00 = **4 151,43 € HT**.
- Les 75,00 € sont l'audit sécurité du SHA candidat : T-043 a 12,5 h passées pour 5 h estimées, en audits d'incrément ; son reste est donc compté à 0, alors que l'audit avant le GO reste à faire (5 h × 15 €). Le découpage de T-043 n'est toujours pas arbitré.
- Résultat : **98,8 % de 4 200 €, marge de 48,57 €.**
- **Consommé client** : 1 348,79 € − 0 € imputé consommé = **1 348,79 €**, soit 32,1 % de 4 200 €.

**Écart avec DEC-020 (4 169,43 €) : −18,00 €.** Deux mouvements l'expliquent :
- les ré-estimations appliquées après DEC-020, plus fortes que l'effet induit de F-06 supposé par T-093 : T-041, T-066, T-067 et T-009, soit −57,29 € ;
- la création de T-094 (message au client, Claire, 0,5 h), soit +39,29 €.

**Écart possible à la baisse, non compté** : T-057 (décision, Karim, 0,5 h, 39,29 €), s'il est clos au temps réellement passé.

**Question ouverte** (DEC-020, « Question ouverte », R11). Comment suivre les coûts pris en charge par l'ESN ? Deux pistes :
- (a) un projet interne de l'ESN ;
- (b) un champ `imputation: client | esn` lu par `tableau.py`.

En attendant la PR de règles, le coût client est recalculé à la main dans le pilotage T-008, à chaque passage du skill `avancement`.

### Condition d'alerte (DEC-020, condition 1) : remplace la marge de risque de 25 %
La v1.0 prévoyait une marge de risque de 25 % sur le reste à faire (843,04 €). Avec 48,57 € de marge, aucune réserve n'est possible. Elle est remplacée par un arbitrage préalable :
1. **Seuil de consommation** : dès que le **consommé client atteint 90 % de 4 200 €, soit 3 780 €**, le `chef-de-projet` crée un ticket `decision` en `ATTENTE_HUMAIN` (S1-R11, au moins 2 scénarios chiffrés).
2. **Dépassement prévisible**, dans les cas suivants :
   - le coût client projeté dépasse 4 200 € après une ré-estimation, une création de ticket au budget client, une reprise après `CHANGEMENTS_DEMANDÉS` ou une recette `NON CONFORME` ;
   - un tel événement consomme plus que la marge restante (48,57 € aujourd'hui, soit environ 3 h d'agent ou 0,6 h de Claire ou de Karim).

   Le ticket `decision` est alors créé **avant d'engager** le travail concerné.
3. **Options présentées** : avenant au client, ou nouveau retrait de périmètre (ni Must, ni F-08, ni sécurité, ni revues humaines, ni portes S3). Claire porte la discussion avec le client (AF1). **Aucun dépassement n'est absorbé d'office par l'ESN** ; une prise en charge par l'ESN ne peut venir que d'une décision humaine explicite.
4. **Lecture du tableau** : l'alerte de `tableau.py` à 90 % porte sur le consommé total, part de l'ESN comprise. Elle se déclenchera donc plus tôt que le seuil réel du client. C'est une alerte prudente, que le `chef-de-projet` corrige de la part imputée dans T-008.
5. **Marge de délai** : 2 jours ouvrés (2026-12-17 et 18). En dessous, voir « Règle d'abandon des Should : levée ».

**Alerte S1-R11 au 2026-11-26 : aucune.**
- Le consommé client est à 32,1 % du budget, sous 90 %.
- Le coût client projeté (4 151,43 €) est sous 4 200 €.
- La mise en service est prévue le 2026-12-16, avant la deadline.

## Risques planning
| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Dépassement de 4 200 € : la marge n'est que de 48,57 € | **forte** | un seul aléa suffit. Par exemple, un cycle de corrections après une recette `NON CONFORME` (environ 10 h d'agents et 2 h de Claire) coûte environ 300 € | condition d'alerte : ticket `decision` et discussion avec le client **avant** d'engager ; coût client recalculé dans T-008 à chaque passage du skill `avancement` |
| Recette `NON CONFORME` | moyenne | 3 à 4 jours ouvrés de correction, nouveaux rapports et re-recette : la deadline n'est plus tenue, et le budget est dépassé. Aucun Should ne reste à retirer | auth revue tôt par Karim ; matrice d'autorisation (T-020) ; tests de bout en bout (T-026) ; Claire disponible les 16 et 17 ; alerte S1-R11 et arbitrage préalable |
| T-037 en priorité `normale` derrière les revues `haute` de Karim | forte (constat du tableau) | recette décalée au 2026-12-09, GO au 2026-12-15 au lieu du 2026-12-14 (C1) | proposition : T-028 et T-037 passent en priorité `haute` (F-08 obligatoire) ; Karim traite T-037 dès que T-028 passe `EN_REVUE` |
| Nadia, goulot et personne unique (`docker`, `sauvegarde-restauration`, `ci-cd`, AF10 b) | moyenne | T-092 et T-078 (prérequis du GO) finissent le 2026-12-11. Un retard ou une absence (mercredis, 2026-12-03) décale le GO | allocation de 50 % jusqu'au 2026-12-18 (DEC-020) ; prérequis du GO placés avant T-089, qui n'est pas prérequis ; besoin de formation renvoyé au plan de formation de l'ESN (DEC-009, E) |
| Revues des prérequis du GO (T-097, T-098, T-099) faites après la fin du ticket relu, sans `depend_de` (AF3) | moyenne | le tableau les place trop tôt ; dates réelles vers le 2026-12-11 au 2026-12-14, à 1,4 h par jour pour Karim | revues dans la journée qui suit le passage `EN_REVUE` ; jalon « Prérequis du GO » au 2026-12-14 |
| Erreur dans le calcul manuel du coût client (imputation non gérée par `tableau.py`) | moyenne | une alerte manquée ou tardive | liste des tickets imputés figée ci-dessus ; formule écrite ; question ouverte de DEC-020 (PR R11) |
| Audit avant GO non estimé dans T-043 (reste à 0) | certaine | 75 € hors du tableau, déjà comptés dans le coût client | découpage de T-043 à arbitrer (T-093, point 6) |
| T-079 (verrou des dépendances) hors des prérequis du GO alors qu'il est recommandé avant l'audit | faible | `pip-audit` du SHA candidat sans fichier de verrouillage | à arbitrer : ajout à `depend_de` de T-043 ou de T-046 |
| Karim en congés du 21 au 31 décembre, seul relecteur `securite-applicative` | certaine | corrections pendant la garantie de livraison non revues avant janvier | GO visé au plus tard le 2026-12-15 ; second relecteur au plan de formation de l'ESN (DEC-009, E) |
| Claire seule recetteuse et seule interlocutrice client | faible | GO bloqué si elle est indisponible | besoin AF10 b au plan de formation de l'ESN (DEC-009, E) |
| Validation tardive par le client du texte RGPD | faible | T-025, la fin des Must et la recette retardés | T-009 planifié du 2026-11-26 au 2026-11-30 ; T-025 isolé (1 h) |
| Tickets `ATTENTE_HUMAIN` supposés débloqués aujourd'hui par `tableau.py` (T-057, T-081, T-083, T-093) | moyenne | dates optimistes, en particulier pour T-058 (dépend de T-057) | décisions à renseigner par Ethan à la fin des scénarios |
