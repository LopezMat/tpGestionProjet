<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). Régénérer : python scripts/tableau.py -->

# Portefeuille des projets

> **Fichier généré** le 2026-11-26 par `scripts/tableau.py` à partir des tickets, seule source de vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.

## Vue d'ensemble

| Projet | Client | Type | État | Avancement | Budget consommé / prévu | % | Fin projetée | Deadline | Écart (j ouvrés) | BLOQUE | ATTENTE_HUMAIN | Alertes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [reservation-coworking](projets/reservation-coworking/TABLEAU.md) | Coworking Les Arcades (Perpignan) | metier | cadrage | 17,3 % | 1 300,04 € / 6 000,00 € | 21,7 % | 2026-12-30 | 2026-12-18 | +7 | 0 | 5 | 9 |

## Alertes

| Projet | Type | Détail |
|---|---|---|
| reservation-coworking | Délais | fin projetée le 2026-12-30 après la deadline du 2026-12-18 (+7 j ouvrés) (S1-R11) |
| reservation-coworking | Critique | T-029 « Sauvegarde quotidienne et limite d'âge de 30 jours (outillage) » est ouvert (A_FAIRE) |
| reservation-coworking | Critique | T-080 « SIMULATION — Perte de la base de production (volume Docker supprimé) » est ouvert (EN_REVUE) |
| reservation-coworking | Critique | T-081 « SIMULATION — Décision restauration de la base de production (T-080) » est ouvert (ATTENTE_HUMAIN) |
| reservation-coworking | Critique | T-082 « SIMULATION — Décision mise en maintenance pendant l'opération (T-080) » est ouvert (ATTENTE_HUMAIN) |
| reservation-coworking | Critique | T-083 « SIMULATION — Décision communication au client sur la perte de données (T-080) » est ouvert (ATTENTE_HUMAIN) |
| reservation-coworking | Absence (S1-R9) | T-081 (salarie:nadia) : fenêtre prévue du 2026-12-02 au 2026-12-04 chevauche EV-002 (2026-12-03 → 2026-12-03) |
| reservation-coworking | Utilisation (info) | claire utilisé à 44,1 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |
| reservation-coworking | Surcharge | nadia : 24,5 h assignées pour 17,9 h de capacité allouée (136,7 %) |

## Décisions humaines attendues

| Priorité | Projet | Ticket | Titre | Question (bloque_par) |
|---|---|---|---|---|
| critique | reservation-coworking | T-081 | SIMULATION — Décision restauration de la base de production (T-080) | décision humaine requise (S2-R4, restauration de données) ; préalable, vérification physique des dossiers de sauvegardes par Nadia |
| critique | reservation-coworking | T-082 | SIMULATION — Décision mise en maintenance pendant l'opération (T-080) | décision humaine requise (S2-R4, coupure volontaire ou mise en maintenance) |
| critique | reservation-coworking | T-083 | SIMULATION — Décision communication au client sur la perte de données (T-080) | décision humaine requise (S2-R4 et AF1, communication au client) ; le message 2 attend aussi la décision T-081 |
| haute | reservation-coworking | T-057 | Rôle PostgreSQL de l'application (constat 10, moindre privilège) | décision humaine sur le rôle PostgreSQL de l'application (constat 10 du rapport securite-2026-11-25-3), avec l'accord de C sur le modèle commun |
| haute | reservation-coworking | T-084 | SIMULATION — Décision notification CNIL de la violation de données (T-080) | décision humaine requise (S2-R4, notification CNIL, compétence juridique) ; recommandation à transmettre au client avant le 2026-11-27 17:00 |

## Équipe : allocation et utilisation

| Salarié | Statut | Niveau | Allocation totale | Par projet | Utilisation (AF9) |
|---|---|---|---|---|---|
| claire | actif | expert | 20 % | reservation-coworking 20 % | reservation-coworking 44,1 % |
| hugo | actif | debutant | 0 % | aucune | — |
| karim | actif | expert | 15 % | reservation-coworking 15 % | reservation-coworking 51,8 % |
| lea | actif | confirme | 0 % | aucune | — |
| nadia | actif | confirme | 20 % | reservation-coworking 20 % | reservation-coworking 136,7 % |

## Événements d'équipe à venir

| Id | Qui | Type | Du | Au | Motif | Statut |
|---|---|---|---|---|---|---|
| EV-001 | salarie:lea | absence | 2026-11-26 | 2026-11-27 | conges | prevu |
| EV-002 | salarie:nadia | absence | 2026-12-03 | 2026-12-03 | formation | prevu |
| EV-003 | salarie:karim | absence | 2026-12-21 | 2026-12-31 | conges | prevu |

## Anomalies de données

- reservation-coworking : 1 anomalie(s), voir son TABLEAU.md
