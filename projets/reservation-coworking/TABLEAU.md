<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). Régénérer : python scripts/tableau.py -->

# Tableau de bord — Coworking Les Arcades (Perpignan) (`reservation-coworking`)

> **Fichier généré** le 2026-11-26 par `scripts/tableau.py` à partir des tickets, seule source de vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.

## Synthèse

| Indicateur | Valeur |
|---|---|
| Type · état | metier · cadrage |
| Avancement (h estimées terminées / h estimées hors ANNULE) | 19,1 % (35,5 h / 186,0 h) |
| Temps restant (Σ max(0, estimation − passé), DEC-001 § 4) | 118,7 h |
| Budget consommé / prévu | 1 193,54 € / 6 000,00 € (19,9 %) |
| Coût projeté à terminaison (consommé + reste × taux) | 4 612,04 € |
| Fin projetée | 2026-12-21 |
| Deadline | 2026-12-18 |
| Écart avec la deadline | +1 j ouvré |

## Alertes

| Type | Détail |
|---|---|
| Délais | fin projetée le 2026-12-21 après la deadline du 2026-12-18 (+1 j ouvré) (S1-R11) |
| Utilisation (info) | claire utilisé à 33,6 % de sa capacité allouée : ajuster l'allocation ? (AF9, indicateur) |

## Tickets par statut

| Statut | Nombre |
|---|---|
| A_FAIRE | 48 |
| EN_COURS | 6 |
| EN_REVUE | 3 |
| BLOQUE | 0 |
| ATTENTE_HUMAIN | 1 |
| TERMINE | 15 |
| ANNULE | 5 |
| **Total** | 78 |

## Tickets BLOQUE

Aucun ticket bloqué.

## En attente d'une décision humaine (ATTENTE_HUMAIN)

| Priorité | Ticket | Titre | Porteur | Question (bloque_par) | Ancienneté |
|---|---|---|---|---|---|
| haute | T-057 | Rôle PostgreSQL de l'application (constat 10, moindre privilège) | salarie:karim | décision humaine sur le rôle PostgreSQL de l'application (constat 10 du rapport securite-2026-11-25-3), avec l'accord de C sur le modèle commun | 1 j ouvré |

## Tickets salariés à faire par un humain (AF11)

| Ticket | Titre | Assigné | Statut | Reste | Fenêtre prévue |
|---|---|---|---|---|---|
| T-009 | Points client (mention de confidentialité, F-08, recette) | salarie:claire | A_FAIRE | 2,5 h | 2026-11-26 → 2026-11-27 |
| T-029 | Sauvegarde quotidienne et limite d'âge de 30 jours (outillage) | salarie:nadia | A_FAIRE | 4,5 h | 2026-11-26 → 2026-12-02 |
| T-030 | Revue humaine T-013 (authentification, sessions, rôles) | salarie:karim | A_FAIRE | 1,5 h | 2026-11-26 → 2026-11-27 |
| T-031 | Revue humaine T-014 (limitation des tentatives) | salarie:karim | A_FAIRE | 1,0 h | 2026-11-27 → 2026-11-30 |
| T-032 | Revue humaine T-015 (changement de mot de passe) | salarie:karim | A_FAIRE | 1,0 h | 2026-11-30 → 2026-12-01 |
| T-033 | Revue humaine T-016 (gestion des comptes) | salarie:karim | A_FAIRE | 1,0 h | 2026-12-01 → 2026-12-02 |
| T-034 | Revue humaine T-017 (compte accueil initial) | salarie:karim | A_FAIRE | 0,5 h | 2026-12-02 → 2026-12-02 |
| T-035 | Revue humaine T-019 (annulation et vue du jour) | salarie:karim | A_FAIRE | 0,5 h | 2026-12-02 → 2026-12-03 |
| T-036 | Revue humaine T-020 (matrice d'autorisation) | salarie:karim | A_FAIRE | 1,0 h | 2026-12-03 → 2026-12-04 |
| T-037 | Revue humaine T-028 (purge à 12 mois) | salarie:karim | A_FAIRE | 0,5 h | 2026-12-08 → 2026-12-08 |
| T-038 | Revue humaine T-029 (sauvegarde et limite d'âge) | salarie:karim | A_FAIRE | 0,5 h | 2026-12-04 → 2026-12-04 |
| T-044 | Environnement de recette (app au SHA candidat, compte accueil de recette) | salarie:nadia | A_FAIRE | 1,0 h | 2026-12-08 → 2026-12-09 |
| T-045 | Recette de la livraison | salarie:claire | A_FAIRE | 5,0 h | 2026-12-09 → 2026-12-15 |
| T-046 | GO mise en production | salarie:claire | A_FAIRE | 0,5 h | 2026-12-15 → 2026-12-15 |
| T-048 | Mise en service (compte accueil initial, tâche planifiée de sauvegarde) | salarie:nadia | A_FAIRE | 1,0 h | 2026-12-15 → 2026-12-16 |
| T-049 | Fin de démonstration (suppression des données sur le poste) | salarie:nadia | A_FAIRE | 0,5 h | 2026-12-16 → 2026-12-17 |
| T-057 | Rôle PostgreSQL de l'application (constat 10, moindre privilège) | salarie:karim | ATTENTE_HUMAIN | 0,5 h | 2026-12-04 → 2026-12-07 |
| T-058 | Rôle PostgreSQL applicatif non superutilisateur (constat 10) | salarie:nadia | A_FAIRE | 2,0 h | 2026-12-07 → 2026-12-08 |
| T-059 | Revue humaine T-058 (rôle PostgreSQL applicatif) | salarie:karim | A_FAIRE | 0,5 h | 2026-12-07 → 2026-12-07 |
| T-064 | Revue humaine T-063 (en-têtes de sécurité et Host) | salarie:karim | A_FAIRE | 0,5 h | 2026-12-07 → 2026-12-08 |
| T-072 | Rotation des journaux dans le modèle compose commun (constat 15) | salarie:nadia | A_FAIRE | 0,5 h | 2026-12-17 → 2026-12-17 |
| T-074 | Revue humaine T-073 (en-têtes sur la 500 interne) | salarie:karim | A_FAIRE | 0,2 h | 2026-12-08 → 2026-12-08 |
| T-078 | Image PostgreSQL 16.16 ou plus (43 CVE corrigées, veille P-1) | salarie:nadia | A_FAIRE | 1,5 h | 2026-12-17 → 2026-12-21 |

## Tickets formation ouverts

Aucun.

## Utilisation des salariés (AF9, indicateur)

Période : du 2026-11-26 au 2026-12-18. Heures restantes assignées ÷ capacité allouée sur la période (calendrier et jours fériés compris). Sous 50,0 %, proposer d'ajuster l'allocation ; jamais de ticket artificiel.

| Salarié | Allocation | h restantes assignées | Capacité allouée | Utilisation | Observation |
|---|---|---|---|---|---|
| claire | 20 % | 8,0 h | 23,8 h | 33,6 % | sous 50,0 % : ajuster l'allocation ? |
| karim | 15 % | 9,2 h | 17,9 h | 51,8 % | — |
| nadia | 20 % | 11,0 h | 17,9 h | 61,4 % | — |

## Planning prévisionnel (Gantt)

```mermaid
gantt
    title Planning — reservation-coworking (calculé le 2026-11-26)
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    section agent analyste-besoin
    T-001 Rédaction du CDC :done, t001, 2026-11-24, 2026-11-25
    T-003 Validation du CDC :done, t003, 2026-11-24, 2026-11-25
    section agent architecte
    T-004 Architecture :done, t004, 2026-11-24, 2026-11-25
    T-005 Choix techniques :done, t005, 2026-11-24, 2026-11-25
    section agent chef-de-projet
    T-002 Interlocuteur client et allocation initiale :done, t002, 2026-11-24, 2026-11-25
    T-008 Pilotage :active, t008, 2026-11-26, 2026-11-27
    section agent deployeur
    T-047 Déploiement en production locale :t047, 2026-12-15, 2026-12-16
    section agent dev-backend
    T-010 Socle de l'application (/health, Dockerfile, démarrage) :done, t010, 2026-11-25, 2026-11-26
    T-011 Modèle de données et migrations :done, t011, 2026-11-25, 2026-11-26
    T-012 Règles métier et horloge (F-01, F-02, F-08) :done, t012, 2026-11-25, 2026-11-26
    T-013 Authentification, sessions et rôles (F-04) :t013, 2026-11-26, 2026-11-27
    T-014 Limitation des tentatives et alerte de sécurité (F-04) :t014, 2026-11-27, 2026-11-28
    T-015 Profil et changement de mot de passe (F-04, F-07) :t015, 2026-11-27, 2026-11-28
    T-016 Gestion des comptes par l'accueil (F-07) :t016, 2026-12-02, 2026-12-04
    T-017 Compte accueil initial (init_accueil) et commande forcer_cha :t017, 2026-11-30, 2026-12-01
    T-018 Disponibilités et réservation (F-01) :t018, 2026-11-30, 2026-12-02
    T-019 Annulation et vue du jour de l'accueil (F-02, F-03) :t019, 2026-12-01, 2026-12-02
    T-020 Matrice d'autorisation et tests sur toutes les routes :t020, 2026-12-03, 2026-12-05
    T-021 Jeu de données de recette (donnees_demo) :t021, 2026-12-01, 2026-12-03
    T-026 Tests de bout en bout Playwright (parcours 1, 5, 7) :t026, 2026-12-02, 2026-12-03
    T-028 Purge des réservations à 12 mois (F-08, Should) :t028, 2026-12-04, 2026-12-05
    T-054 API de consultation des disponibilités (F-01, lecture seule) :done, t054, 2026-11-25, 2026-11-27
    T-056 Test manquant T-010 (/health sous base gelée) :done, t056, 2026-11-25, 2026-11-26
    T-060 Garde-fou de la fixture destructrice des tests de migration  :done, t060, 2026-11-25, 2026-11-26
    T-061 Contraintes sur l'e-mail et les champs vides de « utilisateu :t061, 2026-12-02, 2026-12-03
    T-062 Instant hors fuseau de Paris non converti dans « regles » (c :done, t062, 2026-11-25, 2026-11-26
    T-063 En-têtes de sécurité et contrôle de l'en-tête Host (constats :active, t063, 2026-11-26, 2026-11-27
    T-065 Dette de tests et de documentation de l'incrément (remarques :t065, 2026-12-07, 2026-12-08
    T-069 API de consultation sans réponse si une connexion poolée gèl :t069, 2026-12-04, 2026-12-05
    T-070 Test manquant T-054 (503 sur statement_timeout) :t070, 2026-12-04, 2026-12-05
    T-071 Journal d'accès sans chaîne de requête (constat 15) :done, t071, 2026-11-25, 2026-11-26
    T-073 En-têtes de sécurité sur la 500 interne (constat 16) :active, t073, 2026-11-26, 2026-11-27
    T-079 Verrou des dépendances avec empreintes, image Python figée,  :t079, 2026-12-04, 2026-12-08
    section agent dev-frontend
    T-022 Front socle (connexion, mot de passe, navigation) (F-04) :t022, 2026-11-26, 2026-11-27
    T-023 Front membres (disponibilités, réservation, annulation) (F-0 :t023, 2026-11-27, 2026-12-01
    T-024 Front accueil (vue du jour, gestion des comptes) (F-03, F-07 :t024, 2026-11-26, 2026-11-28
    T-025 Page de confidentialité (texte validé par le client) :t025, 2026-11-27, 2026-11-28
    T-027 Fiches des salles (F-06, Should) :t027, 2026-12-04, 2026-12-05
    T-055 Page de consultation des disponibilités (F-01, lecture seule :active, t055, 2026-11-27, 2026-11-28
    T-075 Contrôle statique du front par analyse HTML (constat 20) :t075, 2026-12-04, 2026-12-05
    section agent relecteur-code
    T-039 Revue de code (1/2) — socle, authentification, réservations :active, t039, 2026-11-26, 2026-11-27
    T-040 Revue de code (2/2) — front, bout en bout, Should, outillage :t040, 2026-11-26, 2026-11-27
    T-066 Revue de code (3/3) — correctifs de l'audit d'incrément :active, t066, 2026-11-26, 2026-11-28
    section agent securite
    T-043 Audit sécurité :t043, 2026-12-04, 2026-12-05
    section agent testeur
    T-041 Tests (1/2) — vérification des tickets de réalisation :active, t041, 2026-11-26, 2026-11-27
    T-042 Tests (2/2) — rapport de tests de la livraison :t042, 2026-12-04, 2026-12-05
    T-067 Tests (3/3) — vérification des correctifs de l'audit d'incré :active, t067, 2026-12-04, 2026-12-08
    section agent veilleur
    T-077 Veille :active, t077, 2026-11-26, 2026-11-27
    section salarie claire
    T-007 Validation du budget et des délais :done, t007, 2026-11-24, 2026-11-26
    T-009 Points client (mention de confidentialité, F-08, recette) :t009, 2026-11-26, 2026-11-28
    T-045 Recette de la livraison :t045, 2026-12-09, 2026-12-16
    T-046 GO mise en production :t046, 2026-12-15, 2026-12-16
    section salarie karim
    T-030 Revue humaine T-013 (authentification, sessions, rôles) :t030, 2026-11-26, 2026-11-28
    T-031 Revue humaine T-014 (limitation des tentatives) :t031, 2026-11-27, 2026-12-01
    T-032 Revue humaine T-015 (changement de mot de passe) :t032, 2026-11-30, 2026-12-02
    T-033 Revue humaine T-016 (gestion des comptes) :t033, 2026-12-01, 2026-12-03
    T-034 Revue humaine T-017 (compte accueil initial) :t034, 2026-12-02, 2026-12-03
    T-035 Revue humaine T-019 (annulation et vue du jour) :t035, 2026-12-02, 2026-12-04
    T-036 Revue humaine T-020 (matrice d'autorisation) :t036, 2026-12-03, 2026-12-05
    T-037 Revue humaine T-028 (purge à 12 mois) :t037, 2026-12-08, 2026-12-09
    T-038 Revue humaine T-029 (sauvegarde et limite d'âge) :t038, 2026-12-04, 2026-12-05
    T-057 Rôle PostgreSQL de l'application (constat 10, moindre privil :crit, t057, 2026-12-04, 2026-12-08
    T-059 Revue humaine T-058 (rôle PostgreSQL applicatif) :t059, 2026-12-07, 2026-12-08
    T-064 Revue humaine T-063 (en-têtes de sécurité et Host) :t064, 2026-12-07, 2026-12-09
    T-068 Revue humaine T-054 (API de consultation sans connexion) :done, t068, 2026-11-26, 2026-11-27
    T-074 Revue humaine T-073 (en-têtes sur la 500 interne) :t074, 2026-12-08, 2026-12-09
    section salarie nadia
    T-029 Sauvegarde quotidienne et limite d'âge de 30 jours (outillag :t029, 2026-11-26, 2026-12-03
    T-044 Environnement de recette (app au SHA candidat, compte accuei :t044, 2026-12-08, 2026-12-10
    T-048 Mise en service (compte accueil initial, tâche planifiée de  :t048, 2026-12-15, 2026-12-17
    T-049 Fin de démonstration (suppression des données sur le poste) :t049, 2026-12-16, 2026-12-18
    T-058 Rôle PostgreSQL applicatif non superutilisateur (constat 10) :t058, 2026-12-07, 2026-12-09
    T-072 Rotation des journaux dans le modèle compose commun (constat :t072, 2026-12-17, 2026-12-18
    T-078 Image PostgreSQL 16.16 ou plus (43 CVE corrigées, veille P-1 :t078, 2026-12-17, 2026-12-22
    section Jalons
    Deadline :milestone, deadline, 2026-12-18, 0d
```

## Hypothèses de calcul

- Taux : agent 15,00 €/h ; salarié : coût journalier ÷ 7 (ARCHITECTURE § 8). Le budget consommé compte aussi le temps passé sur les tickets ANNULE.
- Ordonnancement à partir du 2026-11-26 : dépendances, puis priorité (critique → basse), puis id ; un ticket à la fois par assigné.
- Capacité : agent 7,0 h par jour ouvré ; salarié capacite_h_semaine ÷ 5 × allocation au projet × capacité restante du calendrier (temps partiel moyenné sur 5 jours) ; nulle avant l'arrivée et après le départ.
- Jours ouvrés : hors samedis, dimanches et jours fériés d'`equipe/calendrier.md`.
- Les tickets BLOQUE et ATTENTE_HUMAIN sont supposés débloqués aujourd'hui ; leur date de fin est donc optimiste.
- Tickets TERMINE dans le Gantt : de `cree_le` à `maj_le` (ou `debut_le` / `termine_le` s'ils existent).

## Anomalies de données

- tickets/T-076-page-consultation-message-commande-tests.md : YAML invalide (mapping values are not allowed here) ; ticket ignoré
