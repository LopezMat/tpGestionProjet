<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). Régénérer : python scripts/tableau.py -->

# Portefeuille des projets

> **Fichier généré** le 2026-11-27 par `scripts/tableau.py` à partir des tickets, seule source de vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.

## Vue d'ensemble

| Projet | Client | Type | État | Avancement | Budget consommé / prévu | % | Fin projetée | Deadline | Écart (j ouvrés) | BLOQUE | ATTENTE_HUMAIN | Alertes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [esn-interne](projets/esn-interne/TABLEAU.md) | ESN (projet interne) | interne | cadrage | 0,0 % | 45,00 € / — | — | 2026-11-27 | — | — | 0 | 1 | 14 |
| [reservation-coworking](projets/reservation-coworking/TABLEAU.md) | Coworking Les Arcades (Perpignan) | metier | cadrage | 19,9 % | 1 371,29 € / 4 200,00 € | 32,6 % | 2026-12-16 | 2026-12-18 | -2 | 0 | 1 | 3 |

## Alertes

| Projet | Type | Détail |
|---|---|---|
| esn-interne | Non planifiable | T-002 : salarie:nadia : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-003 : salarie:lea : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-004 : dépend de T-003 non planifiable |
| esn-interne | Non planifiable | T-005 : salarie:karim : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-006 : salarie:lea : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-007 : salarie:claire : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-008 : dépend de T-012 non planifiable |
| esn-interne | Non planifiable | T-009 : dépend de T-012 non planifiable |
| esn-interne | Non planifiable | T-010 : dépend de T-012 non planifiable |
| esn-interne | Non planifiable | T-011 : dépend de T-012 non planifiable |
| esn-interne | Non planifiable | T-012 : salarie:nadia : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-013 : salarie:lea : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-014 : salarie:claire : allocation au projet nulle (S1-R10) |
| esn-interne | Non planifiable | T-015 : salarie:claire : allocation au projet nulle (S1-R10) |
| reservation-coworking | Critique | T-029 « Sauvegarde quotidienne et limite d'âge de 30 jours (outillage) » est ouvert (A_FAIRE) |
| reservation-coworking | Critique | T-080 « SIMULATION — Perte de la base de production (volume Docker supprimé) » est ouvert (EN_REVUE) |
| reservation-coworking | Utilisation (info) | claire utilisé à 36,8 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |

## Décisions humaines attendues

| Priorité | Projet | Ticket | Titre | Question (bloque_par) |
|---|---|---|---|---|
| haute | esn-interne | T-017 | Plan de formation initial — budget de fonctionnement, échéance et allocations (DEC-024) | décision humaine sur le plan de formation initial de l'ESN (formations retenues, budget de fonctionnement, échéance, allocations à esn-interne), DEC-024 |
| haute | reservation-coworking | T-057 | Rôle PostgreSQL de l'application (constat 10, moindre privilège) | décision humaine sur le rôle PostgreSQL de l'application (constat 10 du rapport securite-2026-11-25-3), avec l'accord de C sur le modèle commun |

## Coûts pris en charge par l'ESN

Part ESN des projets clients (`imputation: esn` sur décision validée, R18) et projets internes de l'ESN (R19). Le coût client des projets clients n'en tient pas compte (S1-R11).

| Projet | Nature | Consommé | Projeté à terminaison | Budget de fonctionnement | Décisions |
|---|---|---|---|---|---|
| [esn-interne](projets/esn-interne/TABLEAU.md) | projet interne (R19) | 45,00 € | 4 205,71 € | non renseigné | — |
| [reservation-coworking](projets/reservation-coworking/TABLEAU.md) | prise en charge sur projet client (R18) | 22,50 € | 1 652,50 € | — | DEC-020, DEC-021 |
| **Total ESN** | — | 67,50 € | 5 858,21 € | — | — |

## Plan de formation de l'ESN

Tickets `formation` ouverts des projets internes (S1-R6, S1-R13).

| Projet | Ticket | Titre | Assigné | Statut | Estimation | Fin prévue |
|---|---|---|---|---|---|---|
| esn-interne | T-002 | Formation Nadia — supervision (journée du 2026-12-03, EV-002) | salarie:nadia | A_FAIRE | 7,0 h | non planifiable |
| esn-interne | T-003 | Formation Léa — securite-applicative (1/2) autoformation guidée | salarie:lea | A_FAIRE | 7,0 h | non planifiable |
| esn-interne | T-004 | Formation Léa — revue humaine et securite-applicative (2/2) revues en double avec Karim | salarie:lea | A_FAIRE | 4,0 h | non planifiable |
| esn-interne | T-006 | Formation Léa — recette-fonctionnelle en binôme avec Claire | salarie:lea | A_FAIRE | 4,0 h | non planifiable |
| esn-interne | T-008 | Formation Karim — sauvegarde-restauration (restauration réelle en binôme avec Nadia) | salarie:karim | A_FAIRE | 5,0 h | non planifiable |
| esn-interne | T-010 | Formation Léa — docker (autoformation et binôme avec Nadia) | salarie:lea | A_FAIRE | 7,0 h | non planifiable |
| esn-interne | T-012 | Formation Nadia — documentation (guide d'exploitation Docker et restauration) | salarie:nadia | A_FAIRE | 7,0 h | non planifiable |
| esn-interne | T-013 | Formation Léa — relation-client en binôme avec Claire | salarie:lea | A_FAIRE | 3,0 h | non planifiable |
| esn-interne | T-015 | Formation Claire — juridique (RGPD du sous-traitant, contrats, violations) | salarie:claire | A_FAIRE | 7,0 h | non planifiable |

## Équipe : allocation et utilisation

| Salarié | Statut | Niveau | Allocation totale | Par projet | Utilisation (AF9) |
|---|---|---|---|---|---|
| claire | actif | expert | 20 % | reservation-coworking 20 % | reservation-coworking 36,8 % |
| hugo | depart_prevu | debutant | 0 % | aucune | — |
| karim | actif | expert | 20 % | reservation-coworking 20 % | reservation-coworking 54,7 % |
| lea | conges | confirme | 0 % | aucune | — |
| nadia | actif | confirme | 50 % | reservation-coworking 50 % | reservation-coworking 53,6 % |

## Événements d'équipe à venir

| Id | Qui | Type | Du | Au | Motif | Statut |
|---|---|---|---|---|---|---|
| EV-001 | salarie:lea | absence | 2026-11-26 | 2026-11-27 | conges | prevu |
| EV-002 | salarie:nadia | absence | 2026-12-03 | 2026-12-03 | formation | prevu |
| EV-004 | salarie:hugo | depart | 2026-12-04 | 2026-12-04 | — | prevu |
| EV-003 | salarie:karim | absence | 2026-12-21 | 2026-12-31 | conges | prevu |

## Anomalies de données

- esn-interne : 2 anomalie(s), voir son TABLEAU.md
