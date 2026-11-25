---
titre: Planning — Réservation de salles, Coworking Les Arcades (Perpignan)
statut: VALIDÉ
responsable: agent:chef-de-projet
version: 1.0
maj_le: 2026-11-25
valide_par: Ethan
decision: DEC-009
---
<!-- modèle : templates/planning.md v0.1 · responsable du modèle : A -->

# Planning — Réservation de salles, Coworking Les Arcades (Perpignan)

> Le Gantt détaillé est **généré** dans `TABLEAU.md` à partir des tickets. Ce document fixe les jalons et les hypothèses.

Sources : [CDC v1.0](cdc.md) (`VALIDÉ`, DEC-006), [architecture v1.1](architecture.md) (`VALIDÉ`, DEC-007, DEC-008), `equipe/`, `equipe/calendrier.md`. Décisions sur [T-007](tickets/T-007-validation-budget-delais.md) (Ethan, 2026-11-24, [DEC-009](../../docs/decisions/2026-11-24-DEC-009-budget-delais-coworking.md)) et sur T-050 (Ethan, 2026-11-24, [DEC-010](../../docs/decisions/2026-11-24-DEC-010-principe-r17.md)).

**Changements depuis la v0.1** (Ethan, 2026-11-24, DEC-009) :
- **A1** : 5 Must (F-01, F-02, F-03, F-04, F-07) et Should F-06 (T-027) et F-08 (T-028), planifiés **après tous les Must** et **abandonnables** (règle ci-dessous) ;
- **B1 sans Hugo** : Claire 20 %, Karim 15 %, Nadia 20 %, Hugo 0 % ;
- **C1** : GO le 2026-12-14 ;
- **D1** : le lot R17 (T-006, T-050 à T-053) sort du projet client, parce que le client ne paie pas l'amélioration des outils internes. T-006, T-051, T-052 et T-053 sont passés `ANNULE` ; T-050, en `ATTENTE_HUMAIN`, sera passé `ANNULE` par l'humain lui-même (DEC-010). R17 est réalisée après le développement du projet client, dans une PR de règles séparée ;
- **E** : aucun ticket `formation` dans ce projet ; les besoins repérés vont au plan de formation de l'ESN ; pas de revue d'accessibilité par Léa.

> **Lecture du `TABLEAU.md` avant le report des allocations.** Tant que le coordinateur n'a pas reporté les allocations de DEC-009 dans `equipe/`, `tableau.py` voit Karim et Nadia à 0 % et Claire à 10 % : leurs tickets et tout ce qui en dépend (T-045 à T-049) y apparaissent « non planifiables », et la fin projetée y est fausse. Tant que T-050 n'est pas passé `ANNULE`, il y est aussi compté (0,5 h, 39,29 €). Les dates ci-dessous supposent les allocations décidées.

## Jalons
**Hypothèse de départ** : `planning.md` v0.2 validé et allocations reportées le 2026-11-25 ; `dev-backend` commence T-010 le 2026-11-25 après-midi. Chaque jour de retard sur ce départ consomme un jour de marge.

| Jalon | Date cible | Tickets inclus | Critère de passage |
|---|---|---|---|
| CDC validé | 2026-11-24 (atteint) | T-001, T-003 | décision humaine (DEC-006) |
| Architecture validée | 2026-11-24 (atteint) | T-004, T-005 | décision humaine (DEC-007, DEC-008) |
| Budget, délais et allocations décidés | 2026-11-24 (atteint) ; planning v0.2 validé et allocations reportées le 2026-11-25 | T-007 | décision humaine (DEC-009) ; allocations reportées dans `equipe/` par le coordinateur |
| Points client traités (mention RGPD, F-08, recette) | 2026-11-27 | T-009 | texte validé par Marie Lenoir |
| Sauvegarde quotidienne et limite d'âge | 2026-12-01 | T-029, T-038 | PR acceptée par C, tests de `scripts/` verts |
| Authentification livrée et revue | 2026-12-07 | T-013 à T-017, T-020 ; revues T-030 à T-034, T-036 | tickets `TERMINE` (R13), seuils G confirmés par Karim |
| **Fin des Must** | **2026-12-07** | T-010 à T-026 | tickets `TERMINE` (R13) |
| Fin des Should (abandonnables) | 2026-12-07 ; revue T-037 le 2026-12-08 | T-027, T-028, T-037 | tickets `TERMINE`, ou `ANNULE` selon la règle d'abandon |
| MVP en recette | 2026-12-08 | T-041, T-042, T-043, T-044 | tests `CONFORME` et sécurité `NON BLOQUANT` sur le même SHA ; environnement de recette au SHA candidat |
| Recette | 2026-12-08 (fin de journée) → 2026-12-14 | T-045 | rapport de recette `CONFORME` sur le SHA candidat (S3-R9) |
| **GO mise en production** | **2026-12-14** (C1) | T-046 | décision humaine qui cite le SHA (S3-R3, R16) |
| Mise en production | 2026-12-15 | T-047, T-048 | `verifier-prod` OK (SHA en ligne = SHA attendu) ; compte accueil initial et tâche planifiée en place |
| Marge avant la deadline | 2026-12-16 → 2026-12-18 | — | **3 jours ouvrés** ; abandon des Should si elle passe sous 2 jours ouvrés |
| Deadline client | 2026-12-18 | — | mise en ligne |
| Fin de démonstration | après la soutenance | T-049 | décision humaine (DEC-008) |

**Chemin critique.** T-007 → chaîne de `dev-backend` : T-010 → T-011 → T-012 → T-013 → T-014 → T-015 → T-016 → T-017 → T-018 → T-019 → T-020 → T-021 → T-026 (fin des Must, 2026-12-07) → T-028 (Should, 2026-12-07) → T-043 (audit, 2026-12-08 ; T-042 en parallèle) → T-045 (recette, 2026-12-08 → 2026-12-14) → T-046 (GO, 2026-12-14) → T-047 → T-048 (2026-12-15). Le goulot est `dev-backend` : 60,5 h enchaînées (57,5 h de Must et 3 h de Should), soit environ 8,6 jours à 7 h par jour (un ticket à la fois, ARCHITECTURE § 7). La recette de Claire (5 h à 1,4 h par jour) est le second goulot : elle occupe à elle seule 4 jours ouvrés. Les revues humaines de Karim (T-030 à T-037) conditionnent le passage `TERMINE` des tickets d'authentification et de la purge (R13), et la recette en dépend. Le front (`dev-frontend`, 20,5 h de Must) avance en parallèle et finit vers le 2026-12-01 ; T-027 attend la fin des Must et se fait le 2026-12-07, hors chemin critique.

**Tickets salariés sur le chemin critique** (AF11, R15 : à faire par des humains, jamais par le coordinateur) : T-030 à T-037 (Karim), T-044 et T-048 (Nadia), T-045 et T-046 (Claire) ; T-029 et T-038 sont des prérequis du déploiement (T-047).

**Absences prises en compte** (S1-R9) :
- Léa (2026-11-26 et 27) : aucun ticket affecté, aucun impact.
- Nadia en formation le 2026-12-03 : T-029 est fini avant (2026-12-01), T-044 après (2026-12-07).
- Karim en congés du 2026-12-21 au 31 : après la deadline ; ses revues se terminent le 2026-12-08. Risque sur la garantie de livraison (voir les risques).
- Jours fériés du 25 décembre et du 1er janvier : hors période.

**Ordonnancement indicatif de `dev-backend`** (7 h par jour) : 25/11 début de T-010 ; 26/11 fin de T-010, T-011, début de T-012 ; 27/11 fin de T-012, début de T-013 ; 30/11 fin de T-013, T-014, début de T-015 ; 01/12 fin de T-015, début de T-016 ; 02/12 fin de T-016, T-017, début de T-018 ; 03/12 fin de T-018, début de T-019 ; 04/12 fin de T-019, T-020, T-021, début de T-026 ; 07/12 fin de T-026 (**fin des Must**), puis T-028 (Should, en dernier).

### Règle d'abandon des Should (Ethan, 2026-11-24, DEC-009)
« Les Should sont planifiés après tous les Must et marqués abandonnables : si la marge passe sous 2 jours ouvrés, ils sont retirés sans toucher aux Must. » *Pourquoi (Ethan)* : le budget le permet, mais pas au prix de la deadline.

- **Tickets concernés** : T-027 (F-06, fiches des salles), T-028 (F-08, purge à 12 mois) et sa revue humaine T-037. Ils dépendent de la fin de tous les Must (`depend_de: [T-014, T-020, T-025, T-026]`, qui couvre T-010 à T-026) : les retirer ne retarde ni ne modifie aucun Must.
- **Mesure de la marge** : nombre de jours ouvrés entre la fin prévue de **T-048** (mise en service) et la deadline du 2026-12-18 (jours après la fin, deadline incluse, comme `tableau.py`). Valeur prévue : 3 (fin le 2026-12-15). **Seuil : marge < 2 jours ouvrés**, soit une mise en service prévue après le 2026-12-16. La fin projetée de `TABLEAU.md` inclut T-049 (fin de démonstration, après la soutenance), qui n'entre pas dans la livraison : la marge se lit donc sur la fenêtre de T-048 (section « Tickets salariés »), pas sur l'écart global.
- **Qui la constate** : le `chef-de-projet`, avec le skill `avancement`, à chaque point d'avancement et au moins à chaque jalon (fin des Must, rapports de tests et de sécurité, verdict de recette), ainsi qu'à chaque événement qui touche le chemin critique (absence, ré-estimation, reprise après `CHANGEMENTS_DEMANDÉS`, recette `NON CONFORME`).
- **Qui décide** : **un humain**. Le `chef-de-projet` crée un ticket `decision` « Abandon des Should » en `ATTENTE_HUMAIN` (R7 : question, options, recommandation, impact chiffré en coût et en jours ouvrés) ; il ne passe aucun ticket `ANNULE` avant la décision. Après la décision, il passe les tickets retirés `ANNULE` en citant le `DEC-NNN`.
- **Ordre d'abandon proposé** :
  1. **T-027 (F-06)** : aucune obligation légale ; gain de 22,50 € et d'environ 0,25 jour de recette, mais **aucun gain sur la chaîne `dev-backend`** (T-027 est fait par `dev-frontend` en parallèle). Suffit si le retard vient du front ou de la recette.
  2. **T-028 et T-037 (F-08)** : c'est ce palier qui rend du temps au chemin critique (3 h de `dev-backend`, la revue de Karim et une partie de la recette), soit environ 1 jour ouvré avec T-027 ; 84,29 € économisés. F-08 étant une obligation RGPD du client, Claire l'informe (AF1) et une seconde livraison lui est proposée (au moins 400 €, T-007 option A2).
- **Limites** : un Should déjà `TERMINE` n'est pas retiré (aucun gain) ; un Should `EN_COURS` peut l'être, et son temps passé reste compté. L'abandon ne touche jamais les Must (T-010 à T-026), leurs revues humaines, les tests, l'audit ni la recette. Si la marge reste sous 2 jours ouvrés après l'abandon, ou si la fin projetée dépasse la deadline, l'alerte S1-R11 s'applique (ticket `decision` avec au moins 2 scénarios chiffrés).

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
| salarie:claire | salarié | 20 % (DEC-009 ; 10 % dans `equipe/` jusqu'au report) | 7 | 78,57 |
| salarie:karim | salarié | 15 % (DEC-009 ; 0 % dans `equipe/` jusqu'au report) | 5,25 | 78,57 |
| salarie:nadia | salarié | 20 % (DEC-009 ; 0 % dans `equipe/` jusqu'au report) | 5,6 (sur 28 h, temps partiel) | 64,29 |

Hugo : 0 % (DEC-009), aucun ticket dans ce projet ; retiré de `salaries_affectes` par le coordinateur.

Capacité d'un agent : 7 h équivalent humain par jour ouvré, un ticket à la fois (ARCHITECTURE § 7). Le coordinateur peut lancer en parallèle des tickets sans dépendance entre eux (par exemple T-012 et T-021), ce qui rendrait la réalisation plus rapide que ce modèle.

**Utilisation des salariés (AF9, indicateur)**, du 2026-11-25 au 2026-12-18 (18 jours ouvrés, 17 pour Nadia) : Claire 34 % (8,5 h sur 25,2 h) ; Karim 40 % (7,5 h sur 18,9 h) ; Nadia 37 % (7 h sur 19,0 h). Les trois sont **sous 50 %** et sont signalées : ce sont des temps courts mais placés sur le chemin critique, qui demandent de la réactivité (revues dans la journée, recette sur 4 jours). Aucun ticket n'est ajouté pour atteindre un taux.

**Réductions d'allocation proposées après les jalons** : ce sont de **futures décisions humaines**, que le `chef-de-projet` proposera au jalon concerné et que le coordinateur appliquera ensuite. Elles ne sont pas couvertes par DEC-009 :
- Karim à 5 % après le 2026-12-09 (revues T-030 à T-038 terminées), à condition que la recette ne demande pas de reprise de l'authentification ;
- Claire à 10 % après le GO (2026-12-14), en gardant la relation client pendant la garantie de livraison ;
- Nadia à 5 % après la mise en service (2026-12-15), jusqu'à T-049.

## Charge et budget prévisionnels
- **Charge totale estimée** : **158,5 h** équivalent humain, dont 24,5 h déjà passées (T-001 : 8 h ; T-004 : 11,5 h ; T-008 : 5 h). Répartition : agents 135,5 h, Claire 8,5 h, Karim 7,5 h, Nadia 7 h. Le lot R17 (9,5 h) est retiré du projet (D1).
- **Budget prévisionnel** : **3 739,64 €**, soit **62,3 %** des 6 000 € HT. Déjà consommé : 367,50 € (agents). À venir : agents 1 665,00 € (`dev-backend` 907,50 €, `dev-frontend` 330,00 €, `relecteur-code` 150,00 €, `testeur` 120,00 €, `securite` 75,00 €, `deployeur` 22,50 €, `chef-de-projet` 60,00 €) ; Claire 667,86 € ; Karim 589,29 € ; Nadia 450,00 €. Écart avec la v0.1 : +15,00 € (1 h de replanification, T-008) ; le lot R17 (517,86 €) n'est plus compté.
- **Dont Should** : 106,79 € (T-027 22,50 €, T-028 45,00 €, T-037 39,29 €). Après un abandon des deux : 3 632,85 € (60,5 %).
- **Marge** : marge de risque de **25 %** sur le reste à faire (3 372,14 €), soit **843,04 €** ; **total avec marge : 4 582,68 €** (76,4 %). Reste du budget : **2 260,36 €** sans la marge, **1 417,32 €** avec. Pourquoi 25 % : T-004 a dépassé son estimation de 64 % et T-001 de 14 % ; la marge couvre les reprises après revue, les bugs de recette et un nouveau cycle de tests et de recette sur un nouveau SHA. **Marge de délai : 3 jours ouvrés** (16 au 18 décembre) ; seuil d'abandon des Should à 2.
- **Alerte S1-R11** : aucune (budget sous 90 %, mise en service prévue le 2026-12-15, avant la deadline).

## Risques planning
| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Validation de la v0.2 ou report des allocations après le 2026-11-25 | moyenne | chaque jour de retard consomme un jour de marge ; à 2 jours, seuil d'abandon des Should | validation et report le 2026-11-25 ; `dev-backend` peut démarrer T-010 dès la validation (agent, sans allocation) |
| Recette `NON CONFORME` | moyenne | 3 à 4 jours ouvrés de correction, nouveaux rapports et re-recette : la marge est consommée ; l'abandon des Should ne rend qu'environ 1 jour | auth revue tôt par Karim ; matrice d'autorisation (T-020) ; tests de bout en bout (T-026) avant la recette ; Claire disponible le 16 et le 17 ; alerte S1-R11 si la fin projetée dépasse la deadline |
| Marge sous 2 jours ouvrés (retard de `dev-backend`, reprise après revue) | moyenne | Should retirés (F-06, puis F-08) | règle d'abandon ci-dessus, décision humaine sur alerte du `chef-de-projet` |
| Abandon de F-08 alors que le client l'attend (obligation RGPD) | faible | seconde livraison (au moins 400 €) ; insatisfaction du client | F-08 abandonné en dernier ; Claire en informe le client (AF1) ; point recueilli dans T-009 |
| Revue de Karim qui remet en cause un choix d'authentification au-delà d'un seuil (architecture R-02) | faible | architecture à rouvrir par un humain (R6), reprise de T-013 à T-016 | seuils en constantes (R-04) ; revue au fil de l'eau, pas en fin de projet |
| Validation du texte RGPD par le client tardive | faible | T-025, puis la fin des Must, les Should et la recette, retardés | texte proposé par Claire dès le 2026-11-25 ; T-025 isolé (1 h) |
| `dev-backend` seul goulot (60,5 h enchaînées) | moyenne | un ticket qui dérape décale toute la fin de réalisation | le coordinateur peut paralléliser les tickets sans dépendance (T-012 et T-021) |
| Karim en congés du 21 au 31 décembre, seul relecteur `securite-applicative` | certaine | corrections d'authentification pendant la garantie de livraison non revues avant janvier | GO visé le 2026-12-14 ; second relecteur inscrit au plan de formation de l'ESN, hors de ce projet (DEC-009, E) |
| Claire seule recetteuse et seule interlocutrice client | faible | GO bloqué si elle est indisponible | besoin AF10 b inscrit au plan de formation de l'ESN (DEC-009, E) |
| Ticket T-029 sur l'outillage commun (tous les projets locaux) | faible | régression du déploiement | tests (a) à (e) de l'architecture, revue de Karim (T-038) et PR relue par C ; T-047 en dépend |
| Compétence `tests-e2e` absente des agents de développement | faible | qualité du test de bout en bout (T-026) | vérification par le `testeur` ; à traiter au retour d'expérience (ticket `amelioration`) |
