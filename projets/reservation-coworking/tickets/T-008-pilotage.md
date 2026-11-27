---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-008
titre: Pilotage
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 15.25         # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 14           # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-27
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le: 2026-11-24        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-008 — Pilotage

## Description
Ticket de travail du `chef-de-projet` (règle 14) : le temps de pilotage du projet `reservation-coworking` y est compté, une ligne de journal par intervention.

Estimation : planification initiale 4 h (découpage, estimation, affectation, planning, budget, tri de T-006), replanification après DEC-009 1 h (planning v0.2), suivi et tri des tickets S2/S3 jusqu'à la mise en production 3 h (dont la surveillance de la marge pour l'abandon des Should), retour d'expérience 1 h. Après DEC-020 : 13,25 h. Après DEC-026 (question 2) : **15,25 h**, avec +2 h pour le suivi jusqu'au 2026-12-18 (triage des suites de l'audit avant GO et de la recette, passages `avancement` de la condition 1) et le retex du projet.

## Critères d'acceptation
- [ ] `planning.md` produit et soumis à validation (T-007).
- [ ] Chaque intervention du `chef-de-projet` a une ligne de journal et son temps.
- [ ] `retex.md` complété en fin de projet, avec ses tickets `amelioration`, et les tickets `formation` dans `projets/esn-interne/` (S1-R6, DEC-023).
- [ ] **Condition 1 de DEC-020 (SIMULATION)** : à chaque passage du skill `avancement`, le **coût client** est comparé à 4 200 € HT, et le calcul est noté au journal de ce ticket. Depuis DEC-023, c'est la ligne « Coût client projeté à terminaison » de `TABLEAU.md`, calculée par `tableau.py` à partir du champ `imputation` des tickets (R18), sans soustraction manuelle. Depuis DEC-026, il n'y a plus d'ajout manuel : l'audit avant GO est compté par son propre ticket (T-108, 5 h, au client). Dès que le consommé client atteint 90 % (3 780 €), ou dès qu'un dépassement de 4 200 € est prévisible, un ticket `decision` `ATTENTE_HUMAIN` est créé **avant** d'engager le travail concerné (options : avenant ou retrait de périmètre, discussion avec le client par Claire, AF1) ; aucun dépassement n'est absorbé d'office par l'ESN.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création, passage EN_COURS · 0 h
- 2026-11-24 23:55 · agent:chef-de-projet · planification initiale : lecture du CDC v1.0, de l'architecture v1.1, de DEC-005 à DEC-008, de l'équipe et du calendrier ; création de T-007 et T-009 à T-053 ; tri de T-006 ; `planning.md` v0.1 ; budget prévisionnel et allocations proposées dans T-007 · 4 h
- 2026-11-25 09:00 · agent:chef-de-projet · replanification après DEC-009 et DEC-010 (Ethan, 2026-11-24) : `planning.md` v0.2 (sans le lot R17 ni Hugo, budget et dates recalculés, règle d'abandon des Should) ; T-027 et T-028 marqués abandonnables, dépendances après tous les Must ; T-037 lié à T-028 ; T-006, T-051, T-052, T-053 passés ANNULE ; estimation 8 → 9 h ; TABLEAU.md régénéré · 1 h
- 2026-11-25 23:50 · agent:chef-de-projet · triage (S1-R5) du rapport securite-2026-11-25-3 (constats 2, 4, 10 à 13) et des remarques non bloquantes du `relecteur-code` sur T-010, T-011 et T-012 : création de T-057 (décision, ATTENTE_HUMAIN) et de T-058 à T-067 ; critères ajoutés à T-013, T-016, T-018, T-037 et T-055 ; dépendances ajoutées à T-016 (T-061) et à T-018 (T-062). `tableau.py` non lancé (le hook n'accepte que le chemin relatif et le répertoire courant de l'agent n'est pas la racine) : calcul à la main dans le message au coordinateur · 1 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage (S1-R5) des suites de T-054 : T-069 trié (constat 14 du rapport securite-2026-11-25-4 fusionné) et ajouté à `depend_de` de T-046 ; T-070 trié ; création de T-071 (journal d'accès, constat 15 a) et T-072 (rotation des journaux, constat 15 b, Nadia) ; critère ajouté à T-013 (constat 15 c) et à T-055 (créneaux passés du jour J, 1,5 → 2 h) ; remarques 1 à 5 du relecteur sur T-054 et remarques fonctionnelles de l'audit regroupées dans T-065 (1 → 2,5 h) ; journal de T-018 ; T-066 (3 → 5 h) et T-067 (2,5 → 4 h) étendus ; proposition de ré-estimation de T-043 au journal. `tableau.py` non lancé (hook et répertoire courant) : calcul à la main dans le message au coordinateur · 1 h
- 2026-11-25 16:40 · agent:chef-de-projet · triage (S1-R5) du rapport securite-2026-11-25-5 : création de T-073 (constat 16, en-têtes sur la 500 interne, `dev-backend`, 0,5 h) et de son compagnon T-074 (revue humaine, Karim, 0,25 h) ; T-013 dépend de T-073 ; remarque `api.py:127` regroupée en critère de T-018 (4,5 → 4,75 h) ; T-066 5 → 5,5 h ; T-067 non modifié (consigne du coordinateur). `tableau.py` lancé · 0,25 h
- 2026-11-26 16:30 · agent:chef-de-projet · création des tickets issus de la veille 2026-S48 (`veille/2026-S48.md`) : T-078 (P-1, image PostgreSQL 16.16, Nadia) et T-079 (P-2, verrou des dépendances, `dev-backend`), en `A_FAIRE`, non planifiés (développement en pause) ; aucun ticket existant modifié ; ligne reportée par le coordinateur · 0,5 h
- 2026-11-26 18:00 · agent:chef-de-projet · SIMULATION · exercice de crise T-080 : création des actions correctives T-085 à T-091 (P-1 à P-6, P-9 ; P-7 et P-8 non créés, DEC-009 point E), analyse de charge de Nadia dans T-090 ; ligne reportée par le coordinateur · 1,5 h
- 2026-11-26 18:30 · agent:chef-de-projet · SIMULATION · retour d'expérience DEC-019 : T-029 haute → critique, T-029 ajouté à `depend_de` de T-046, création de T-092 (vérification quotidienne des sauvegardes), T-088 annulé (couvert par T-092), T-090 annoté ; ligne reportée par le coordinateur · 1 h
- 2026-11-26 22:20 · agent:chef-de-projet · SIMULATION · application de DEC-020 (budget 4 200 € HT, scénario B en gardant F-08) : T-027, T-065 et T-076 passés ANNULE (titre de T-076 mis entre guillemets) ; T-027 retiré de depend_de de T-042, T-043 et T-045 ; revues et vérifications des tickets annulés retirées de T-040 (4 → 3,5 h), T-041 (6 → 5,7 h), T-066 (5,5 → 5 h) et T-067 (4 → 3,6 h) ; F-06 retiré de la recette T-045 (5 → 4,75 h) ; points F-06 et F-08 de T-009 retirés (2,5 → 2 h) ; ligne « imputé à l'ESN (DEC-020) » dans T-029, T-038, T-058, T-059, T-072, T-078, T-085 à T-087, T-089 à T-092 ; T-094 créé (message au client, Claire, condition 2) ; critère de la condition 1 ajouté ici ; estimation de ce ticket 9 → 13,25 h (10,25 h passées + 3 h de pilotage jusqu'au retex, hypothèse de T-093 § 1 comprise dans les 4 169,43 € de DEC-020) ; `tableau.py` lancé et coût client calculé dans le message au coordinateur · 0,75 h
- 2026-11-26 23:10 · agent:chef-de-projet · SIMULATION · triage demandé par Ethan (T-090) : revues humaines T-095 à T-100 créées (Karim ; T-095 à T-099 imputées à l'ESN, T-100 au budget client) ; T-087, T-092 et T-078 ajoutés à depend_de du GO T-046 (DEC-020) ; `planning.md` v1.1 rédigé (EN_REVUE, SIMULATION) : budget 4 200 €, condition d'alerte de DEC-020 à la place de la marge de 25 %, F-08 obligatoire, allocations, imputation à l'ESN, prérequis du GO, jalons. **Condition 1 (DEC-020)** : coût projeté `tableau.py` 5 858,93 € − part imputée à l'ESN 1 782,50 € = 4 076,43 € ; + audit avant GO non compté par le tableau (T-043, 5 h × 15 = 75 €) = **coût client 4 151,43 €** (98,8 % de 4 200 €, marge 48,57 €) ; consommé client 1 348,79 € (32,1 %, cette intervention comprise ; seuil d'alerte 3 780 €) ; aucun dépassement prévisible, pas d'alerte. `tableau.py` lancé · 1 h
- 2026-11-26 23:59 · agent:chef-de-projet · SIMULATION · analyses d'impact des événements d'équipe (scénario 3) : T-102 (absence de Léa, aucun impact, option A recommandée) et T-103 (départ de Hugo, aucun ticket ouvert, `documentation` orpheline renvoyée au plan de formation de l'ESN, option A recommandée), passés ATTENTE_HUMAIN ; aucune réaffectation ni création de ticket. **Condition 1 (DEC-020)** : coût projeté `tableau.py` 5 888,93 € − part imputée à l'ESN 1 782,50 € + audit avant GO 75,00 € = **coût client 4 181,43 €** (99,6 %, marge 18,57 €), dont +30,00 € depuis la v1.1 du planning (T-101 7,50 €, T-102 7,50 €, T-103 15,00 €) ; 4 158,93 € si T-102 et T-103 sont imputés à l'ESN (proposé, décision humaine) ; consommé client 1 378,79 € (32,8 %, seuil d'alerte 3 780 €) ; pas d'alerte. Le temps est compté dans T-102 (0,5 h) et T-103 (1 h), comme pour T-093, et pas une seconde fois ici · 0 h
- 2026-11-26 23:30 · agent:chef-de-projet · SIMULATION · tri (S1-R5) de T-105 (bug « Aucun créneau », note de recette recette-2026-11-26-01) : priorité `haute` confirmée, `agent:dev-frontend` confirmé (reproduction au SHA `dc53a1d` en premier), estimation 1 → 1,5 h, `depend_de` vide ; statut `A_FAIRE` inchangé, aucun autre ticket modifié. **Condition 1 (DEC-020)**, dans l'ordre :
  - coût projeté `tableau.py` sans T-105 : 5 903,93 € ;
  - − 1 782,50 € imputés à l'ESN (DEC-020) ;
  - − 22,50 € pour T-102 et T-103 (DEC-021) ;
  - + 75,00 € d'audit avant le GO ;
  - = **coût client avant tri 4 173,93 €** (marge 26,07 €), dont +15,00 € depuis DEC-021 pour T-104 ;
  - avec T-105 (1,5 h, 22,50 €) et la revue et la vérification induites (1 h, 15,00 €, non comptées par le tableau) : **4 211,43 €, soit un dépassement prévisible de 11,43 €**.

  **Alerte déclenchée** : ticket `decision` `ATTENTE_HUMAIN` à créer par le coordinateur **avant d'engager** le correctif. Le défaut est couvert par la garantie de livraison (CDC § 9) s'il est confirmé. Consommé client 1 371,29 € (32,6 %, cette intervention comprise ; seuil 3 780 €). `tableau.py` lancé · 0,5 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 (R18) : critère « Condition 1 » réécrit (le coût client se lit dans `TABLEAU.md`, plus de soustraction manuelle) ; 23 tickets portent désormais `imputation: esn` (DEC-020, DEC-021) ; T-104 reste au client (décision d'Ethan dans DEC-023). L'écart de 175 € avec la part ESN manuelle (1 782,50 €) vient de T-081 et T-083, clos TERMINE sans temps passé, et non d'une ré-estimation (DEC-023). Le temps de cette migration n'est pas compté au client · 0 h
- 2026-11-27 · agent:chef-de-projet · alerte S1-R11 et condition 1 de DEC-020 : création du ticket `decision` [T-107](T-107-arbitrage-audit-securite-avant-go.md) (ATTENTE_HUMAIN, porteuse Claire), qui arbitre le dépassement de T-043 et le comptage de l'audit avant GO (options A à E chiffrées). La question 2 porte sur la ré-estimation de ce ticket : +2 h, 30 €, pour le retex et le suivi, car le reste est de 0 h après cette intervention. Ligne de renvoi dans T-043 ; aucun autre ticket modifié. Refus du hook : `python scripts/tableau.py` est refusé avec un chemin absolu, et le chemin relatif échoue, car le répertoire courant de l'agent est `tickets/` (P11 du retex de l'ESN, récidive). **Condition 1**, calcul à la main en attendant que le coordinateur relance le script :
  - `TABLEAU.md` du 2026-11-27 : 4 098,93 € ;
  - + 3,75 € pour ce ticket : 1 h passée pour un reste de 0,75 h ;
  - + 19,64 € pour T-107 : 0,25 h de Claire ;
  - = **4 122,32 €** (98,2 %, marge 77,68 €), sans l'audit avant GO ;
  - **4 197,32 € avec l'audit avant GO** (99,9 %, marge 2,68 €) ;
  - **4 227,32 € avec aussi la réserve de pilotage** : dépassement prévisible de 27,32 € si rien n'est imputé à l'ESN, d'où T-107.

  Consommé client : 1 386,29 € (33,0 %, seuil 3 780 €) · 1 h
- 2026-11-27 11:05 · agent:chef-de-projet · application de [DEC-026](../../../docs/decisions/2026-11-27-DEC-026-audit-securite-increments-esn.md) (VALIDÉ par Ethan, option D), points 1 à 3 :
  - T-043 est renommé « Audits d'incrément (DEC-011) », passe de 5 à 12,5 h, reçoit `imputation: esn` et `imputation_decision: DEC-026`, et ses critères sont réécrits sur les 7 rapports, avec les preuves au journal ; il reste `A_FAIRE` en attendant la conclusion du coordinateur (R13) ;
  - T-108 « Audit sécurité avant GO » est créé (`agent:securite`, 5 h, au client, dépendances et critères d'origine de T-043, plus l'écart DEC-007 C, prérequis A7 de DEC-025) ;
  - T-108 remplace T-043 dans `depend_de` de T-045 et de T-046, sans cycle ;
  - l'estimation de ce ticket passe de 13,25 à 15,25 h, et le critère « Condition 1 » n'a plus d'ajout manuel.

  `tableau.py` lancé. **Condition 1 (DEC-020)** :
  - coût client projeté **4 036,07 €** (96,1 % de 4 200 €, marge 163,93 €), sans ajout manuel ;
  - consommé client 1 265,21 € (30,1 %, seuil 3 780 €) ;
  - part ESN consommée 210,00 €, projetée 1 840,00 € ;
  - fin projetée le 2026-12-15, pour une deadline au 2026-12-18 ; aucune anomalie de données.

  **Écart de −3,75 € avec les 4 039,82 € de DEC-026** :
  - T-107 : +19,64 €, car Ethan a noté 0,5 h au lieu des 0,25 h estimées (0,25 h × 78,57 €/h, Claire) ;
  - T-057 : −19,64 €, car Ethan l'a passé `TERMINE` avec 0,25 h passées pour 0,5 h estimées (0,25 h × 78,57 €/h, Karim) ;
  - ce ticket : −3,75 €, car DEC-026 comptait 13,5 h passées + 2 h = 15,5 h, alors que l'estimation décidée est de 15,25 h et que le passé (14 h, cette intervention comprise) reste en dessous.

  Pas de nouveau dépassement prévisible, donc pas de nouveau ticket `decision` : l'écart au-dessus de 90 % est arbitré par DEC-026 · 0.5 h
