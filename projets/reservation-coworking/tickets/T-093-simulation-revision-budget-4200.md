---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-093
titre: "SIMULATION — Révision du budget : 6 000 € → 4 200 € HT"
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 1.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: arbitrage humain du scénario de budget (S1-R11)   # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:      DEC-020             # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:     2026-11-26              # facultatif : date du passage TERMINE
---
> **SIMULATION** — Exercice de révision du budget (scénario 2, S1) demandé par l'humain le 2026-11-26. Le client n'a rien annoncé en réalité : le budget de `projet.md` (6 000 €) n'est pas modifié tant qu'aucune décision n'est prise.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-093 — SIMULATION — Révision du budget : 6 000 € → 4 200 € HT

## Description
**Source (SIMULATION).** Annonce écrite du client (Coworking Les Arcades, responsable : Marie Lenoir) reçue le 2026-11-26 : le budget passe de **6 000 € HT** ([cdc.md](../cdc.md) § 10, [DEC-009](../../../docs/decisions/2026-11-24-DEC-009-budget-delais-coworking.md)) à **4 200 € HT** (− 1 800 €, − 30 %). La **deadline du 2026-12-18 ne change pas**. Skill [revision-budget](../../../.claude/skills/revision-budget/SKILL.md).

**Chiffres d'entrée** (skill `avancement`, `scripts/tableau.py` au 2026-11-26, après DEC-019 v0.2) :
- budget consommé : 1 300,04 € sur 6 000 € (21,7 %) ;
- reste à faire : 132,4 h ; avancement 17,8 % (36,5 h sur 205,0 h estimées hors `ANNULE`) ;
- **coût projeté à terminaison : 5 660,86 €**, soit **1 460,86 € au-dessus** du nouveau budget de 4 200 € ;
- fin projetée : 2026-12-21, deadline 2026-12-18 (+1 j ouvré).

**Attendu du `chef-de-projet`** (étape 4 du skill) : écrire ci-dessous l'analyse d'impact et au moins deux scénarios chiffrés, dont un qui respecte 4 200 €, puis sa recommandation, et passer le ticket `ATTENTE_HUMAIN`.

**Contraintes de l'humain** : ne jamais sacrifier [T-029](T-029-sauvegarde-quotidienne-limite-age.md) (sauvegarde quotidienne, critique, DEC-019) ni les tickets de sécurité critiques.

## Analyse d'impact
<!-- Remplie par le chef-de-projet -->
*Rédigée par `agent:chef-de-projet` le 2026-11-26 (SIMULATION). **Aucun scénario n'est appliqué** : aucun ticket n'est annulé ni réaffecté, et `projet.md`, `planning.md`, le CDC et `equipe/` ne sont pas modifiés. Taux réels : 15 €/h pour un agent ; Claire et Karim 550 €/j ÷ 7 = 78,57 €/h ; Nadia 450 €/j ÷ 7 = 64,29 €/h. Montants arrondis au centime.*

**Question (R7).** Le client ramène le budget de 6 000 € à 4 200 € HT et maintient la deadline du 2026-12-18. Quel scénario retenir pour livrer les Must à temps, sans sacrifier T-029 ni la sécurité ?

### 1. Situation au 2026-11-26

**Consommé : 1 300,04 €**, soit 84,05 h d'agents × 15 = 1 260,75 €, plus 0,5 h de Karim (T-068) = 39,29 €. Cela représente **31,0 % de 4 200 €**, contre 21,7 % de 6 000 €.

**Reste à faire selon `tableau.py`** : 132,4 h et **4 360,82 €**. C'est la somme de max(0, estimation − passé) sur les tickets ni `TERMINE` ni `ANNULE`, recalculée ticket par ticket ; le total est identique à celui du tableau.

| Assigné | Reste (h) | Calcul | Reste (€) |
|---|---|---|---|
| `dev-backend` | 52,75 | 52,75 × 15 | 791,25 |
| `dev-frontend` | 21,0 | 21 × 15 | 315,00 |
| `relecteur-code` | 9,4 | 9,4 × 15 | 141,00 |
| `testeur` | 4,5 | 4,5 × 15 | 67,50 |
| `deployeur` | 1,5 | 1,5 × 15 | 22,50 |
| `chef-de-projet` (T-090) | 0,5 | 0,5 × 15 | 7,50 |
| `securite` (T-043, voir plus bas) | 0 | — | 0,00 |
| **Agents** | **89,65** | 89,65 × 15 | **1 344,75** |
| Claire (T-009, T-045, T-046, T-083, T-091) | 9,5 | 9,5 × 550 / 7 | 746,43 |
| Karim (T-030 à T-038, T-057, T-059, T-064, T-074) | 9,25 | 9,25 × 550 / 7 | 726,79 |
| Nadia (T-029, T-044, T-048, T-049, T-058, T-072, T-078, T-081, T-085 à T-087, T-089, T-092) | 24,0 | 24 × 450 / 7 | 1 542,86 |
| **Salariés** | **42,75** | | **3 016,07** |
| **Total** | **132,4** | | **4 360,82** |

Les salariés représentent 32 % des heures restantes mais **69 % du coût restant**. Nadia seule en représente 35 %.

**Coût projeté selon `tableau.py`** : 1 300,04 + 4 360,82 = **5 660,86 €**, soit **+1 460,86 €** (+34,8 %) au-dessus de 4 200 €.

**Coûts connus que `tableau.py` ne compte pas encore.** Il faut les ajouter pour obtenir une projection fidèle.

| Élément | Calcul | € |
|---|---|---|
| **Audit sécurité avant le GO.** T-043 a 12,5 h passées pour 5 h estimées, toutes en audits d'incrément (DEC-011). Son reste est donc compté à 0, alors que l'audit du SHA candidat reste entièrement à faire. Le découpage proposé le 2026-11-25 n'a pas été arbitré. | 5 h × 15 | 75,00 |
| Revues humaines annoncées mais pas encore créées : T-085, T-086, T-087 et T-092 (Karim, AF3) | 4 × 0,5 h × 78,57 | 157,14 |
| Revues humaines de T-078 et T-079 (Karim), annoncées dans ces tickets | 2 × 0,5 h × 78,57 | 78,57 |
| T-089 : les 0,5 h de Karim sont comptées au taux de Nadia | 0,5 × (78,57 − 64,29) | 7,14 |
| T-093 (ce ticket), créé après le calcul | 1,5 h × 15 | 22,50 |
| T-076, ignoré par `tableau.py` (YAML invalide, à cause de « : » dans le `titre`) | 0,3 h × 15 | 4,50 |
| Pilotage jusqu'au retex : T-008 a déjà dépassé son estimation (10,25 h pour 9 h). Hypothèse : 3 h de plus | 3 h × 15 | 45,00 |
| **Total** | | **389,86** |

**Projection corrigée : 6 050,72 €**, soit **+1 850,72 € (+44,1 %)** au-dessus de 4 200 €. Elle dépasse même les 6 000 € initiaux. Les scénarios partent de ce chiffre.

Contrôle (2026-11-26, après la correction du YAML de T-093) : `tableau.py` compte désormais T-093. Il donne un consommé de 1 322,54 € et un coût projeté de 5 683,36 €, soit 5 660,86 € plus les 22,50 € de la ligne T-093. La projection corrigée reste de 6 050,72 €.

Écart possible à la baisse, non compté : T-081 et T-083 (décidés par DEC-019) et T-057 (décidé par DEC-013) sont encore comptés à leur estimation (3 h, 214,29 €). S'ils sont clos au temps réellement passé, la projection baisse au plus de ce montant.

**Poids de la crise SIMULATION (T-080 à T-092)**

| Ticket | Assigné | h | € |
|---|---|---|---|
| T-081 Décision de restauration | Nadia | 1,5 | 96,43 |
| T-083 Communication au client | Claire | 1 | 78,57 |
| T-085 Runbook « volume supprimé » | Nadia | 1,5 | 96,43 |
| T-086 Protection du volume | Nadia | 2 | 128,57 |
| T-087 Refus d'une base vide | Nadia | 1,5 | 96,43 |
| T-089 Exercice de restauration | Nadia (+ Karim) | 2,5 | 160,71 |
| T-090 Triage | `chef-de-projet` | 0,5 | 7,50 |
| T-091 Registre des suppressions | Claire | 0,5 | 39,29 |
| T-092 Vérification quotidienne des sauvegardes | Nadia | 4 | 257,14 |
| *Sous-total compté par `tableau.py`* | | *15* | *961,07* |
| Revues de T-085, T-086, T-087, T-092 et écart de T-089 | Karim | 2 | 164,29 |
| **Reste à venir** | | **17** | **1 125,36** |
| Déjà consommé (T-080, 4,6 h × 15) | `gestionnaire-crise` | | 69,00 |
| **Total de la crise** | | | **1 194,36** |

La crise pèse **23,7 % du reste à faire corrigé** (1 125,36 € sur 4 750,68 €), soit l'équivalent de 26,8 % du nouveau budget.

**Délais.**
- **Fin projetée selon `tableau.py`** : 2026-12-21, soit +1 jour ouvré. Elle est due à T-078 (Nadia, du 2026-12-18 au 2026-12-21). T-078 corrige 43 CVE, dont des exécutions de code à CVSS 8,8, et il est pourtant placé après la deadline, alors qu'il est recommandé avant le GO.
- **Mise en service T-048** : projetée du 2026-12-17 au 2026-12-18. Il ne reste donc **aucun jour ouvré de marge**, sous le seuil de 2 jours de la règle d'abandon des Should (DEC-009, `planning.md`). **La règle d'abandon est donc déclenchée par le calendrier, indépendamment du budget.**
- **Goulot : Nadia.** Elle a 24 h restantes pour 26,9 h de capacité à 30 % (89 %). T-092 occupe sa file jusqu'au 2026-12-17 et retarde T-048, alors que le déploiement T-047 est prévu le 2026-12-15.

### 2. Ce qui tient dans tous les scénarios

| Bloc | Tickets | Pourquoi |
|---|---|---|
| Must F-01, F-02, F-03, F-04, F-07 | `dev-backend` T-013 à T-021 et T-026 (42,25 h) ; `dev-frontend` T-022 à T-025 (19 h) : 918,75 € | CDC v1.0 validé (DEC-006). Retirer un Must change la nature de la livraison. |
| Correctifs prérequis | T-061 (prérequis de T-016), T-069 (prérequis du GO), T-070 (test du 503), T-075 (contrôle anti-XSS à faire avant T-022 et T-023) : 52,50 € | Dépendances déjà posées, ou sécurité pour un coût négligeable. |
| Revues humaines de sécurité (AF3) | T-030 à T-036 (authentification, F-04, F-07), T-064 et T-074 (en-têtes déjà codés), T-057 (DEC-013) : 7,75 h de Karim, 608,93 € | S3-R2 ; CDC § 8 (revue par Karim de tous les tickets d'authentification, DEC-006). `revue-humaine` est hors périmètre des agents. |
| **T-029 et sa revue T-038** | Nadia 4,5 h, Karim 0,5 h : 328,57 € | Ticket critique et prérequis du GO (DEC-019) ; consigne de l'humain. |
| **T-092 et sa revue** | Nadia 4 h, Karim 0,5 h : 296,43 € | Preuve d'exécution de T-029 (justification ci-dessous). |
| Sécurité moyenne ou haute déjà décidée ou constatée | T-058 et T-059 (rôle non superutilisateur, DEC-013) ; T-078 et sa revue (CVE à CVSS 8,8), à placer avant le GO ; T-079 et sa revue (constat 1, moyen, ouvert depuis le premier audit) | Constats `securite` ou veille ; T-078 et T-079 sont recommandés avant le GO. |
| Portes S3 | Revue de code T-039, T-040, T-066 ; tests T-041, T-042, T-067 ; audit avant GO ; recette T-045 (Claire) ; GO T-046 (Claire) ; déploiement T-047 | R13, R16, S3-R3, S3-R9 : sans elles, aucun GO. |
| Exploitation et relation client | T-044, T-048, T-049 (Nadia) ; T-009 (Claire, mention de confidentialité nécessaire à T-025 et information du client sur le périmètre) | AF1 ; mise en service ; DEC-008. |

**Pourquoi T-092 tient partout.** T-029 crée la sauvegarde, mais rien ne prouve qu'elle tourne. C'est exactement ce qui a mal tourné dans T-080 : les règles de sauvegarde étaient validées (DEC-003, DEC-007, DEC-008), l'outil n'avait jamais tourné, et personne ne le savait.
- T-048 ne crée la tâche planifiée qu'une seule fois. Si le poste est éteint, si la tâche est désactivée ou si une base recréée vide est sauvegardée chaque soir sans erreur, seul T-092 le détecte, en moins de 24 h, par une restauration réelle et un contrôle de cohérence.
- Le rapport `verification-sauvegarde-*.md` est aussi la trace versionnée qui a manqué pendant la crise (cause 5).
- Sans T-092, T-029 redevient « une règle sans preuve d'exécution », alors que c'est la leçon même de DEC-019.
- T-092 compense en partie le report de T-087, puisqu'il signale une base vide dès le lendemain matin. C'est ce qui rend acceptable le report de T-086, T-087 et T-089 dans le scénario A.
- Coût : 296,43 €, soit 7 % de 4 200 €.

**Noyau minimal.** Il comprend les Must, les correctifs T-061 et T-069, les revues AF3, T-029 et T-038, les portes S3 (sans les Should), l'exploitation, T-009 et le pilotage. Il ne compte ni T-092, ni T-058, ni T-078, ni T-079, ni aucune action de crise. Il coûte déjà **4 309,79 €**, consommé compris :
- consommé : 1 300,04 € ;
- agents : 1 322,25 € ;
- Claire : 7,5 h, 589,29 € ;
- Karim : 8,25 h, 648,21 € ;
- Nadia : 7 h, 450,00 €.

**4 200 € est donc inatteignable par des retraits seuls**, à moins de toucher aux Must, aux revues humaines ou aux portes S3. Une contribution de l'ESN est nécessaire.

### 3. Leviers

**3.1 Should abandonnables.** Le CDC ne contient aucune exigence Could. F-06 et F-08 sont les seuls Should.

| Should | Tickets | Gain direct | Gain induit (estimé) | Total | Effet sur les délais |
|---|---|---|---|---|---|
| F-06 Fiches des salles | T-027 (`dev-frontend` 1,5 h) : 22,50 € | 22,50 | Revue de code 0,5 h (7,50) + recette 0,25 h (19,64) | **49,64** | Aucun sur la chaîne `dev-backend` (le front avance en parallèle) ; environ 0,2 jour de recette |
| F-08 Purge à 12 mois | T-028 (`dev-backend` 3 h) : 45,00 € ; T-037 (Karim 0,5 h) : 39,29 € | 84,29 | 27,14 (idem) | **111,43** | Environ 0,4 jour de `dev-backend`, la revue de Karim et environ 0,2 jour de recette ; T-045 ne dépend plus de T-037 |
| **Total** | | **106,79** | **54,29** | **161,07** | Environ 1 jour ouvré (`planning.md` v1.0) |

- **Risque propre à F-08.** F-08 traduit une obligation RGPD du client, responsable du traitement (CDC § 4 et § 8 : conservation 12 mois, puis suppression). Aucune donnée n'atteint 12 mois avant fin 2027 : son retrait ne crée donc aucun manquement immédiat.
- Son dernier critère (les sauvegardes ne gardent pas les données au-delà de leur propre rétention) reste livré par T-029, avec la limite d'âge de 30 jours.
- **Risque résiduel** : l'oubli. À partir de fin 2027, des réservations pourraient être conservées au-delà de 12 mois. Ce serait un manquement du client, avec l'ESN comme sous-traitant.
- **Mitigation** : une seconde livraison (devis séparé, au moins 400 € selon T-007, option A2), avec une échéance écrite (2027-11), annoncée au client par Claire (AF1).
- **Préalable** : le CDC prévoit F-08 « avant la mise en ligne si le client l'exige », et cette question de T-009 n'a pas encore été posée. Le retrait de F-08 est donc **conditionné à l'accord écrit du client**.
- **Changement de périmètre du CDC.** `cdc.md` est `VALIDÉ` (DEC-006). Un humain doit le repasser `EN_REVUE` (R6) pour une v1.1 rédigée par l'`analyste-besoin`, qui marque F-06 et F-08 comme reportées. Le point A de DEC-009 est modifié par la nouvelle décision.
- **Ce que perd le client avec F-06** : l'affichage de la capacité et des équipements des salles. Les noms « Salle 1/2/3 » restent (H-20). Aucune obligation légale n'est en jeu.

**3.2 Tickets à reporter ou à annuler** (coût revue comprise)

| Ticket | € | Nature | Risque s'il n'est pas fait avant le GO | Position |
|---|---|---|---|---|
| T-065 | 37,50 | Dette de tests et de documentation (priorité basse) | Aucun effet pour le client ni sur la sécurité ; restent un test à borne fragile et deux assertions toujours vraies | **Annuler** (à reprendre en maintenance) |
| T-076 | 4,50 | Message d'erreur trompeur, commande de test | Gêne mineure | **Annuler** |
| T-075 | 7,50 | Contrôle statique anti-XSS du front (constat 20) | Une régression de T-022 ou T-023 non détectée ; la CSP reste la défense | Garder (coût négligeable) |
| T-079 | 69,29 | Verrou des dépendances (constat 1, moyen) | Dérive à la reconstruction vers une Starlette vulnérable | Garder |
| T-078 | 135,71 | Image PostgreSQL 16.16 (CVE à CVSS 8,8) | Exécution de code sur la base en cas d'injection | Garder, avant le GO |
| T-072 | 32,14 | Rotation des journaux du modèle commun (constat 15 b) | Le disque du poste peut être rempli par une route anonyme | Garder |
| T-085 | 135,71 | Runbook « volume supprimé » | Procédure à reconstituer en pleine crise, comme le 2026-11-26 (le brouillon existe dans T-081) | Reportable après le GO |
| T-086 | 167,86 | Volume `external` (cause 2) | La même erreur (`down -v`, `prune`) peut se reproduire ; avec T-029 et T-092, la perte est d'un jour au plus et reste restaurable | Reportable, mais c'est la prévention de la cause |
| T-087 | 135,71 | Refus de recréer une base vide (cause 4) | Une perte masquée par une base neuve ; T-092 la détecte le lendemain matin | Reportable si T-092 est fait |
| T-089 | 167,86 | Exercice de restauration chronométré | Durée de restauration inconnue ; Karim n'a jamais vu la procédure (dépendance à Nadia seule, AF10 b) | Reportable après la mise en service |
| T-091 | 39,29 | Registre des suppressions chez le client | Une restauration réintroduirait des comptes supprimés (manquement RGPD du client) | Garder (même échange que T-009) |
| T-092 | 296,43 | Vérification quotidienne des sauvegardes | Voir § 2 | **Garder partout** |

**3.3 Réaffectations d'un salarié vers un agent : aucun gain possible.** J'ai examiné les 42,75 h des salariés ; aucune ne peut passer à un agent sans enfreindre AF1 à AF5 ou la règle 7.
- **Claire (9,5 h)** : T-009, T-083 et T-091 relèvent du contact client (AF1) ; T-045 est la recette, toujours confiée à un salarié (règle 6, R16) ; T-046 est la décision de GO (AF2).
- **Karim (9,25 h)** : ce sont des revues humaines (AF3 ; `revue-humaine` est hors périmètre des agents), plus T-057, déjà décidé (AF2).
- **Nadia (24 h)** : son travail porte sur l'outillage commun (`scripts/`, `deploiement/`, `runbooks/`), où aucun agent n'écrit (règle 7, C9). Il demande aussi des commandes `docker` et une restauration réelle, qu'aucun agent n'exécute (S2-R1 ; règles 1 et 6 du `deployeur`). T-081 et T-049 sont des décisions (AF2).

Seule piste : élargir le périmètre d'écriture d'un agent, par exemple `dev-backend` dans `scripts/`. C'est une modification de règle (R11), hors du champ de ce ticket et impossible avant la deadline. Gain : **0 €**. La crise a d'ailleurs reporté du travail sur le type de ressource le plus cher.

**3.4 Imputation à l'ESN** (précédent : DEC-009, point D, « le client ne paie pas l'amélioration de nos outils internes »)
- **(a) Crise : 1 125,36 €** (T-081, T-083, T-085 à T-087, T-089 à T-092, leurs revues et l'écart de T-089).
  - La crise vient de deux fautes de l'ESN : une suppression du volume par erreur, sur son poste, et un engagement non tenu (la sauvegarde quotidienne du CDC § 9, décidée par DEC-007, n'avait jamais été réalisée).
  - Faire payer au client la réparation d'un défaut de l'ESN serait difficile à défendre, et contraire au message de T-083 : « nous prenons cet incident très au sérieux ».
  - T-080 (69 € déjà consommés) reste au projet pour l'historique de l'incident, sauf avoir commercial.
- **(b) Outillage commun à tous les projets locaux : 664,29 €.**
  - Tickets concernés : T-029 et T-038 (328,57 €), T-058 et T-059 (167,86 €), T-072 (32,14 €), T-078 et sa revue (135,71 €).
  - La partie propre au client reste au projet : T-044, T-048 (tâche planifiée sur sa production) et T-049.
  - **Contre-argument** : DEC-009 avait laissé T-029 au budget client, et DEC-013 a chiffré T-058 dans le projet (environ 175 €). Imputer ces tickets à l'ESN revient sur ces deux points ; c'est à un humain de le dire. T-029 reste réalisé, critique et prérequis du GO.
- **Total imputable : 1 789,64 €.**
- **Mécanique, selon le précédent D1** : les tickets passent `ANNULE` ici, avec la mention « déplacé vers … », et sont recréés dans un projet interne de l'ESN (à créer). Deux limites :
  - `tableau.py` ne suit pas un `depend_de` d'un projet à l'autre. Les prérequis du GO (T-029, T-087, T-092) deviennent donc des critères écrits de T-046, que le coordinateur vérifie avant de présenter le GO, avec le rapport de vérification de T-092 comme preuve.
  - Les heures de Nadia et de Karim sur ce projet interne demandent une allocation (S1-R10). Sinon, les dates du § 5 ne tiennent pas.

**3.5 Décaler la deadline (scénario C) : hors sujet.** Le client la maintient, et un report ne réduirait pas le coût : celui-ci se calcule en heures × taux, quelle que soit la durée, et un projet plus long ajoute du pilotage. Le seul effet serait de soulager la file de Nadia.

### 4. Scénarios chiffrés

Base : projection corrigée de 6 050,72 €. T-029, T-092, les revues AF3, la sécurité et les portes S3 sont gardés dans tous les scénarios.

| | **A · Recentrage seul** | **B · Recentrage et imputation à l'ESN** | **D · Maintien et dépassement** |
|---|---|---|---|
| Périmètre retiré | F-06, F-08 (T-027, T-028, T-037) ; T-065 et T-076 annulés ; T-085, T-086, T-087 et T-089 reportés après la livraison (sortis du projet, à reprendre par l'ESN) | F-06, F-08 ; T-065 et T-076 annulés ; la crise et l'outillage commun sortent du budget client mais **sont réalisés** | Rien |
| Calcul | 6 050,72 − 161,07 − 42,00 − 607,14 | 6 050,72 − 161,07 − 42,00 − 1 125,36 − 664,29 | — |
| **Coût projeté pour le client** | **5 240,50 €** | **4 058,00 €** (4 169,43 € si F-08 est gardé) | **6 050,72 €** |
| Écart à 4 200 € | **+1 040,50 €** (+24,8 %) : ne respecte pas le budget | **−142,00 €** (96,6 % du budget) : **respecte le budget** | **+1 850,72 €** (+44,1 %) |
| À la charge de l'ESN | 1 040,50 € pour tenir 4 200 €, puis la reprise des 4 tickets reportés (607,14 €) | **1 789,64 €** (+ 69 € déjà passés sur T-080) | D1 : 0 € (avenant au client) ; D2 : 1 850,72 €, sans plafond |
| Mise en service et marge | Vers le 2026-12-14 ou 15 ; environ 3 jours ouvrés | Vers le 2026-12-14 ou 15 ; environ 3 jours, **si Nadia reçoit une allocation interne** ; sinon le 2026-12-18 et 0 jour | Le 2026-12-18, 0 jour (fin le 2026-12-21) ; le 2026-12-16 et 2 jours si Nadia passe à +20 % |
| Qualité | Must, sécurité et portes S3 intacts. Pour la crise : détection (T-092), mais ni prévention (T-086, T-087) ni procédure éprouvée (T-085, T-089) | Tout le correctif de crise est fait avant la mise en service ; seule la dette de tests de T-065 reste | Complète |
| Risque principal | Ne tient pas 4 200 € ; la crise peut se reproduire | Marge de 142 € sans réserve pour les aléas ; deux décisions passées sont revues (DEC-009 sur T-029, DEC-013) | Dépassement non financé ; aucune marge de délai |

### 5. Effet sur la fin projetée (estimations à confirmer par `tableau.py` après application)

La capacité de Nadia sur ce projet est de 1,68 h par jour ouvré (30 % de 28 h ÷ 5), et elle est absente le 2026-12-03.

- **A** : Nadia garde 16,5 h, dont 15 h avant T-048 ; sa file est vide vers le 2026-12-09.
  - La chaîne `dev-backend` perd 5,5 h (T-028, T-065) et la recette 0,5 h ; T-045 ne dépend plus de T-037.
  - GO vers le 2026-12-11 au 2026-12-14, mise en service vers le 2026-12-14 ou 15 : **marge d'environ 3 jours ouvrés**, avec T-078 placé avant le GO.
- **B** : mêmes dates que A, à une condition : que les 21,5 h de Nadia imputées à l'ESN soient prises sur une allocation au projet interne et non sur ses 30 %. Il faut environ 40 % jusqu'au 2026-12-11 (21,5 h sur 10 jours ouvrés). Pour Karim, environ 5 % suffisent pour 4,5 h de revues.
  - Sans cette allocation, la file réelle de Nadia ne change pas : mise en service le 2026-12-18, marge nulle.
  - Une allocation ne coûte rien en soi : seules les heures passées comptent (T-090).
- **D** : mise en service le 2026-12-18 (marge 0), fin le 2026-12-21 (T-078 après la deadline). Si T-078 passe avant le GO, comme il le faut, la mise en service reste au 2026-12-18. Avec Nadia à +20 %, la mise en service peut arriver vers le 2026-12-16 (marge 2). Tout glissement porte alors la livraison après la deadline. Garder les Should avec une marge sous 2 jours exige en outre une dérogation à DEC-009.

### 6. Risques et ce que le client perd

- **A.** Le client perd :
  - les fiches des salles (capacité, équipements) ;
  - la purge automatique à 12 mois, jusqu'à une seconde livraison ;
  - la correction d'un message d'erreur (T-076).

  Sa production démarre sans protection du volume (T-086), sans refus d'une base vide (T-087) et sans procédure de restauration éprouvée (T-085, T-089). Les sauvegardes existent quand même et sont vérifiées chaque jour (T-029, T-092) : une récidive coûterait au plus un jour de données, au lieu de tout. Le budget n'est pas tenu, et l'alerte S1-R11 reste ouverte.
- **B.** Le client perd les mêmes Should et T-076, mais rien sur la sécurité ni sur l'exploitation.
  - Risques :
    - la marge de 142 € (3,4 %) ne couvre aucun aléa. Un seul cycle de corrections après une recette `NON CONFORME` (environ 10 h d'agents et 2 h de Claire, soit 300 € environ) suffirait à dépasser. L'alerte S1-R11 (90 %, soit 3 780 €) se déclenchera mécaniquement en fin de projet ;
    - les prérequis T-029, T-087 et T-092, sortis du projet, sont vérifiés par critère écrit, et non plus par `depend_de` ;
    - la file de Nadia dépend d'une allocation interne à décider ;
    - DEC-009 (T-029 au budget client) et DEC-013 (coût de T-058) sont revus.
  - Qualité : seule la dette de T-065 reste.
- **D.** Le client garde tout.
  - D1 (avenant de 1 850,72 €) : peu crédible le jour même où le client réduit son budget, et risqué pour la relation.
  - D2 (absorbé par l'ESN) : l'ESN prend en charge tout dépassement futur, sans plafond.
  - Dans les deux cas, la mise en service tombe le jour de la deadline, et la règle d'abandon de DEC-009 est contredite.
  - Note : D2 ne coûte à l'ESN que 61,08 € de plus que B (1 850,72 − 1 789,64). En revanche, le délai n'est pas tenu et l'engagement de l'ESN n'a pas de limite.

### 7. Recommandation : **scénario B**, sous conditions
1. **F-06 (T-027) est retiré.** **F-08 (T-028, T-037) est reporté** à une seconde livraison avant fin 2027, **sous réserve de l'accord écrit du client**, recueilli par Claire dans T-009 (AF1). Si le client exige F-08 avant la mise en ligne, le scénario devient B-bis, à **4 169,43 €**, qui respecte encore le budget (marge de 30,57 €). Le CDC passe alors en v1.1, après que l'humain l'a repassé `EN_REVUE`.
2. **T-065 et T-076 passent `ANNULE`.**
3. **Imputation à l'ESN de 1 789,64 €** : la crise (sa faute) et l'outillage commun (principe D de DEC-009). Ces tickets restent **réalisés**. T-029, T-087 et T-092 sont faits avant le GO, et T-078 aussi.
4. **Forfait de 4 200 € HT pour le client.** Un dépassement éventuel reste à la charge de l'ESN ; cet engagement est à écrire dans la décision, puisque B n'a pas de réserve pour les aléas.
5. **Allocations proposées** (décision humaine ; le coordinateur les applique, règle 13) :
   - Nadia : 10 % sur ce projet (2,5 h restantes) et 40 % sur le projet interne de l'ESN jusqu'au 2026-12-18 ;
   - Karim : +5 % sur le projet interne ;
   - Claire : 31 % d'utilisation en B, sous 50 % (AF9). Je propose de garder 20 % jusqu'au GO pour la réactivité de la recette, puis d'appliquer la réduction déjà prévue par `planning.md`.

**Pourquoi B.**
- C'est le seul scénario qui respecte 4 200 € sans toucher aux Must, à la sécurité, aux revues humaines ni aux portes S3. Le noyau minimal coûte déjà 4 309,79 € (§ 2).
- La réduction de budget du client a une contrepartie de périmètre : les Should, déjà déclarés abandonnables par DEC-009, dont la règle est par ailleurs déclenchée par le calendrier.
- L'ESN ne paie que ce qui relève d'elle, selon des critères bornés et défendables : sa faute et ses outils.
- Le correctif de crise est fait en entier, conformément à la leçon de DEC-019 : une règle sans preuve d'exécution n'est pas une garantie.
- A coûte moins cher à l'ESN (749,14 € de moins), mais laisse la prévention de la crise non faite, alors que l'ESN la paierait de toute façon pour ses propres outils.
- D2 garde les Should pour 61 € de plus, mais sans plafond et sans marge de délai.

**À trancher par l'humain** :
1. le scénario (A, B ou D) ;
2. F-08 : retiré ou gardé, après l'accord du client ;
3. la liste des tickets imputés à l'ESN et leur mécanique (déplacement ou maintien), dont T-029 et T-058, qui reviennent sur DEC-009 et DEC-013 ;
4. les allocations ;
5. l'engagement de forfait ;
6. le découpage de T-043 (audit avant GO, 5 h).

**Après la décision, à appliquer (rien ne l'est aujourd'hui)** :
- tracer la décision (DEC-NNN) ;
- `budget_eur: 4200` dans `projet.md` (coordinateur) ;
- `cdc.md` à repasser `EN_REVUE` par un humain, puis v1.1 par l'`analyste-besoin` ;
- `planning.md` à repasser `EN_REVUE`, puis v1.1 par le `chef-de-projet` ;
- tickets retirés ou déplacés passés `ANNULE` avec le DEC-NNN, et projet interne de l'ESN créé ;
- `depend_de` et critères de T-046 ; revues compagnons à créer ; découpage de T-043 ;
- allocations dans `equipe/` (coordinateur) ;
- information du client par Claire (T-009) ;
- relance de `python scripts/tableau.py`.

## Critères d'acceptation
- [x] L'analyse d'impact est écrite : consommé, reste à faire (h et €, au taux de chaque assigné), projection face à 4 200 € et à la deadline.
- [x] Au moins deux scénarios chiffrés (coût, délai, périmètre, risque, qualité), dont un qui respecte 4 200 € ; T-029 et les tickets de sécurité critiques gardés dans tous les scénarios.
- [x] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [x] Après la décision : `projet.md` (budget), tickets `ANNULE` ou réaffectés et CDC cohérents entre eux.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 19:40 · agent:coordinateur · SIMULATION · création (skill revision-budget, étape 3) sur annonce écrite du client (simulée) : 6 000 € → 4 200 € HT, deadline inchangée ; chiffres d'entrée de tableau.py · 0 h
- 2026-11-26 19:45 · agent:chef-de-projet · SIMULATION · passage EN_COURS ; lecture de projet.md, cdc.md, planning.md, DEC-009, DEC-011, DEC-013, DEC-019, TABLEAU.md, equipe/ et de tous les tickets ouverts · 0 h
- 2026-11-26 21:15 · agent:chef-de-projet · SIMULATION · analyse d'impact écrite (skill revision-budget, étape 4). Reste à faire recalculé ticket par ticket, identique à tableau.py (132,4 h, 4 360,82 €). Projection corrigée à 6 050,72 € (+389,86 € connus et non comptés : audit avant GO, revues compagnons, T-093, T-076 au YAML invalide, pilotage). Crise : 1 125,36 € à venir. Noyau minimal : 4 309,79 €, donc 4 200 € inatteignable par des retraits seuls. Réaffectation vers un agent : 0 h possible (AF1 à AF5, règle 7). Scénarios : A 5 240,50 € (ne respecte pas 4 200 €), B 4 058,00 € (respecte, l'ESN prend 1 789,64 € à sa charge), D 6 050,72 € ; recommandation B. Aucun scénario appliqué. Passage ATTENTE_HUMAIN. Temps compté ici, pas dans T-008 · 1.5 h
- 2026-11-26 21:20 · agent:chef-de-projet · SIMULATION · valeur de `titre` mise entre guillemets, sans changer le texte : le « : » rendait le YAML invalide et tableau.py ignorait le ticket. tableau.py relancé : T-093 est listé en ATTENTE_HUMAIN, coût projeté 5 683,36 € (T-093 compris) · 0 h
- 2026-11-26 22:20 · agent:chef-de-projet · SIMULATION · DEC-020 (scénario B en gardant F-08) appliquée aux tickets : T-027 (F-06), T-065 et T-076 passés ANNULE ; T-027 retiré de depend_de de T-042, T-043 et T-045 ; revues, vérifications et recette des tickets annulés retirées de T-040, T-041, T-045, T-066 et T-067 ; points F-06 et F-08 de T-009 retirés ; T-028 et T-037 inchangés (F-08 gardé) ; ligne « imputé à l'ESN (DEC-020) » dans les 13 tickets imputés (T-081 et T-083 non touchés, décisions en attente) ; T-094 créé (message au client, Claire, condition 2) ; condition 1 ajoutée en critère de T-008. Statut et `decision` de ce ticket inchangés (à renseigner par Ethan). Temps compté dans T-008 · 0 h
