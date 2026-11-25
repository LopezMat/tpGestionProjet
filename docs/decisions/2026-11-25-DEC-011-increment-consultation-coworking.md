---
titre: Incrément « socle et consultation des disponibilités » avant la soutenance (reservation-coworking)
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-25
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-011           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-011
date: 2026-11-25
decide_par: Ethan
projet: reservation-coworking
ticket: T-054
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-011 — Incrément « socle et consultation des disponibilités » (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision d'Ethan du 2026-11-25. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. Le « Pourquoi » et les conditions sont ceux formulés par Ethan (skill `tracer-decision`, étape 1).

## Contexte
Le planning v1.0 ([DEC-009](2026-11-24-DEC-009-budget-delais-coworking.md)) prévoit de développer tout le projet. Le 2026-11-25, Ethan a changé la priorité : développer d'abord le socle et F-01 (voir les disponibilités et réserver un créneau), chaque ticket passant par tout le circuit (développement, `relecteur-code`, `securite`, `testeur`), les autres fonctions et l'authentification restant `A_FAIRE`. Or la réservation (T-018) dépend de l'authentification (T-013), puisque le CDC impose que seul un membre connecté réserve (F-01, F-04). Le coordinateur a posé la question ; Ethan a choisi l'option « Lecture seule ».

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| Authentification minimale (T-011, T-013, T-022, puis T-018 et la partie F-01 de T-023) | F-01 complet et conforme au CDC | revue humaine de Karim (T-030) avant T-018 ; plus long avant la soutenance |
| **Lecture seule : socle, T-011, T-012, consultation des disponibilités (T-054, T-055) (retenue)** | incrément visible rapidement ; aucune donnée personnelle exposée | F-01 incomplet (pas de réservation) ; écart provisoire au CDC F-04 (routes de consultation sans connexion) |
| F-01 sans connexion (nom saisi librement) | réservation visible | contraire au CDC validé (F-01, F-04) ; risque de sécurité et RGPD |

## Décision
1. **L'incrément en cours se limite au socle et à la consultation des disponibilités en lecture seule** : T-010 (socle), T-011 (modèle de données et migrations), T-012 (règles métier et horloge), [T-054](../../projets/reservation-coworking/tickets/T-054-api-consultation-disponibilites.md) (API `GET /api/salles` et `GET /api/disponibilites`, détachée de T-018) et [T-055](../../projets/reservation-coworking/tickets/T-055-page-disponibilites-lecture.md) (page de consultation, détachée de T-023). Chaque ticket passe par le développement, `relecteur-code`, `securite` et `testeur`. L'authentification et les autres fonctions restent `A_FAIRE`.
2. **Le catalogue des salles est une donnée de référence** créée par T-011 (migration), sans dépendre de l'authentification.
3. **Conditions (Ethan)** :
   - l'écart au CDC (F-04 : « toute page ou appel d'API de réservation sans connexion est refusé ») est **provisoire** ;
   - **aucun GO ni mise en production tant que T-013 et T-020 ne protègent pas ces routes** ;
   - **le CDC reste inchangé**.

## Pourquoi
*(Ethan, 2026-11-25)* La soutenance est le vendredi 2026-11-27 et la priorité est de montrer le fonctionnement du système (agents, tickets, contrôles) à travers un incrément visible ; la consultation est en lecture seule et n'expose aucune donnée personnelle.

## Impacts
- Fichiers ou règles à mettre à jour :
  - tickets : T-054 et T-055 créés ; T-018 (6 → 4,5 h) et T-023 (7 → 5,5 h, dépend aussi de T-055) allégés de la consultation ; T-011 complété (catalogue des salles sans authentification) ;
  - `planning.md` (`VALIDÉ`, DEC-009) n'est pas modifié : la charge totale est inchangée à 0,5 h près ; l'ordre de réalisation change pour cet incrément. Une replanification complète par le `chef-de-projet` sera nécessaire à la reprise du développement complet.
- Tickets créés ou débloqués : T-054, T-055 (A_FAIRE).
- **Garde-fous pour la suite** :
  - le ticket « GO mise en production » (T-046) ne peut être présenté que si T-013 et T-020 sont `TERMINE` et que la matrice d'autorisation couvre `GET /api/salles` et `GET /api/disponibilites` (en plus de R16) ;
  - l'audit `securite` signale ces deux routes comme écart provisoire accepté par DEC-011, et non comme constat ignoré.
- Délais : la deadline du 2026-12-18 reste l'objectif ; l'avancement est réévalué après la soutenance.
- Règles : aucune règle modifiée.
