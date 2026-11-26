<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). Régénérer : python scripts/tableau.py -->

# Portefeuille des projets

> **Fichier généré** le 2026-11-26 par `scripts/tableau.py` à partir des tickets, seule source de vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.

## Vue d'ensemble

| Projet | Client | Type | État | Avancement | Budget consommé / prévu | % | Fin projetée | Deadline | Écart (j ouvrés) | BLOQUE | ATTENTE_HUMAIN | Alertes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [reservation-coworking](projets/reservation-coworking/TABLEAU.md) | Coworking Les Arcades (Perpignan) | metier | cadrage | 19,9 % | 1 393,79 € / 4 200,00 € | 33,2 % | 2026-12-16 | 2026-12-18 | -2 | 0 | 1 | 3 |

## Alertes

| Projet | Type | Détail |
|---|---|---|
| reservation-coworking | Critique | T-029 « Sauvegarde quotidienne et limite d'âge de 30 jours (outillage) » est ouvert (A_FAIRE) |
| reservation-coworking | Critique | T-080 « SIMULATION — Perte de la base de production (volume Docker supprimé) » est ouvert (EN_REVUE) |
| reservation-coworking | Utilisation (info) | claire utilisé à 34,7 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |

## Décisions humaines attendues

| Priorité | Projet | Ticket | Titre | Question (bloque_par) |
|---|---|---|---|---|
| haute | reservation-coworking | T-057 | Rôle PostgreSQL de l'application (constat 10, moindre privilège) | décision humaine sur le rôle PostgreSQL de l'application (constat 10 du rapport securite-2026-11-25-3), avec l'accord de C sur le modèle commun |

## Équipe : allocation et utilisation

| Salarié | Statut | Niveau | Allocation totale | Par projet | Utilisation (AF9) |
|---|---|---|---|---|---|
| claire | actif | expert | 20 % | reservation-coworking 20 % | reservation-coworking 34,7 % |
| hugo | depart_prevu | debutant | 0 % | aucune | — |
| karim | actif | expert | 20 % | reservation-coworking 20 % | reservation-coworking 51,5 % |
| lea | conges | confirme | 0 % | aucune | — |
| nadia | actif | confirme | 50 % | reservation-coworking 50 % | reservation-coworking 50,2 % |

## Événements d'équipe à venir

| Id | Qui | Type | Du | Au | Motif | Statut |
|---|---|---|---|---|---|---|
| EV-001 | salarie:lea | absence | 2026-11-26 | 2026-11-27 | conges | prevu |
| EV-002 | salarie:nadia | absence | 2026-12-03 | 2026-12-03 | formation | prevu |
| EV-004 | salarie:hugo | depart | 2026-12-04 | 2026-12-04 | — | prevu |
| EV-003 | salarie:karim | absence | 2026-12-21 | 2026-12-31 | conges | prevu |

## Anomalies de données

Aucune.
