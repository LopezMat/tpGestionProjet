<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). Régénérer : python scripts/tableau.py -->

# Portefeuille des projets

> **Fichier généré** le 2026-11-27 par `scripts/tableau.py` à partir des tickets, seule source de vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.

## Vue d'ensemble

| Projet | Client | Type | État | Avancement | Budget consommé / prévu | % | Fin projetée | Deadline | Écart (j ouvrés) | BLOQUE | ATTENTE_HUMAIN | Alertes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [esn-interne](projets/esn-interne/TABLEAU.md) | ESN (projet interne) | interne | en_cours | 8,2 % | 123,75 € / 4 360,00 € | 2,8 % | 2027-01-26 | 2027-01-15 | +7 | 0 | 0 | 5 |
| [reservation-coworking](projets/reservation-coworking/TABLEAU.md) | Coworking Les Arcades (Perpignan) | metier | cadrage | 25,7 % | 1 268,96 € / 4 200,00 € | 30,2 % | 2026-12-15 | 2026-12-18 | -3 | 0 | 0 | 2 |

## Alertes

| Projet | Type | Détail |
|---|---|---|
| esn-interne | Délais | fin projetée le 2027-01-26 après la deadline du 2027-01-15 (+7 j ouvrés) (S1-R11) |
| esn-interne | Absence (S1-R9) | T-002 (salarie:nadia) : fenêtre prévue du 2026-11-27 au 2026-12-16 chevauche EV-002 (2026-12-03 → 2026-12-03) |
| esn-interne | Utilisation (info) | claire utilisé à 16,8 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |
| esn-interne | Utilisation (info) | lea utilisé à 43,3 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |
| esn-interne | Surcharge | nadia : 19,0 h assignées pour 18,5 h de capacité allouée (102,8 %) |
| reservation-coworking | Critique | T-029 « Sauvegarde quotidienne et limite d'âge de 30 jours (outillage) » est ouvert (A_FAIRE) |
| reservation-coworking | Utilisation (info) | claire utilisé à 36,8 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |

## Décisions humaines attendues

Aucune.

## Coûts pris en charge par l'ESN

Part ESN des projets clients (`imputation: esn` sur décision validée, R18) et projets internes de l'ESN (R19). Le coût client des projets clients n'en tient pas compte (S1-R11).

| Projet | Nature | Consommé | Projeté à terminaison | Budget de fonctionnement | Décisions |
|---|---|---|---|---|---|
| [esn-interne](projets/esn-interne/TABLEAU.md) | projet interne (R19) | 123,75 € | 3 768,21 € | 4 360,00 € | — |
| [reservation-coworking](projets/reservation-coworking/TABLEAU.md) | prise en charge sur projet client (R18) | 210,00 € | 1 840,00 € | — | DEC-020, DEC-021, DEC-026 |
| **Total ESN** | — | 333,75 € | 5 608,21 € | — | — |

## Plan de formation de l'ESN

Tickets `formation` ouverts des projets internes (S1-R6, S1-R13).

| Projet | Ticket | Titre | Assigné | Statut | Estimation | Fin prévue |
|---|---|---|---|---|---|---|
| esn-interne | T-002 | Formation Nadia — supervision (journée du 2026-12-03, EV-002) | salarie:nadia | A_FAIRE | 7,0 h | 2026-12-16 |
| esn-interne | T-003 | Formation Léa — securite-applicative (1/2) autoformation guidée | salarie:lea | A_FAIRE | 7,0 h | 2026-12-03 |
| esn-interne | T-004 | Formation Léa — revue humaine et securite-applicative (2/2) revues en double avec Karim | salarie:lea | A_FAIRE | 4,0 h | 2026-12-08 |
| esn-interne | T-006 | Formation Léa — recette-fonctionnelle en binôme avec Claire | salarie:lea | A_FAIRE | 4,0 h | 2026-12-10 |
| esn-interne | T-008 | Formation Karim — sauvegarde-restauration (restauration réelle en binôme avec Nadia) | salarie:karim | A_FAIRE | 5,0 h | 2027-01-26 |
| esn-interne | T-010 | Formation Léa — docker (autoformation et binôme avec Nadia) | salarie:lea | A_FAIRE | 7,0 h | 2027-01-11 |
| esn-interne | T-012 | Formation Nadia — documentation (guide d'exploitation Docker et restauration) | salarie:nadia | A_FAIRE | 7,0 h | 2027-01-05 |
| esn-interne | T-013 | Formation Léa — relation-client en binôme avec Claire | salarie:lea | A_FAIRE | 3,0 h | 2027-01-13 |

## Équipe : allocation et utilisation

| Salarié | Statut | Niveau | Allocation totale | Par projet | Utilisation (AF9) |
|---|---|---|---|---|---|
| claire | actif | expert | 25 % | esn-interne 5 %, reservation-coworking 20 % | esn-interne 16,8 %, reservation-coworking 36,8 % |
| hugo | depart_prevu | debutant | 0 % | aucune | — |
| karim | actif | expert | 25 % | esn-interne 5 %, reservation-coworking 20 % | esn-interne 76,9 %, reservation-coworking 52,5 % |
| lea | conges | confirme | 25 % | esn-interne 25 % | esn-interne 43,3 % |
| nadia | actif | confirme | 60 % | esn-interne 10 %, reservation-coworking 50 % | esn-interne 102,8 %, reservation-coworking 53,6 % |

## Événements d'équipe à venir

| Id | Qui | Type | Du | Au | Motif | Statut |
|---|---|---|---|---|---|---|
| EV-001 | salarie:lea | absence | 2026-11-26 | 2026-11-27 | conges | prevu |
| EV-002 | salarie:nadia | absence | 2026-12-03 | 2026-12-03 | formation | prevu |
| EV-004 | salarie:hugo | depart | 2026-12-04 | 2026-12-04 | — | prevu |
| EV-003 | salarie:karim | absence | 2026-12-21 | 2026-12-31 | conges | prevu |

## Anomalies de données

Aucune.
