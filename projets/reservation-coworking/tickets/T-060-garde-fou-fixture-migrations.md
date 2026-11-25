---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-060
titre: Garde-fou de la fixture destructrice des tests de migration (constat 13)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: tests-unitaires (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.6            # heures équivalent humain
depend_de: [T-011]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25         # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-25     # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-060 — Garde-fou de la fixture destructrice des tests de migration (constat 13)

## Description
Constat 13 (bas) du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), qui rejoint la remarque 6 du `relecteur-code` sur [T-011](T-011-modele-donnees-migrations.md). Dans `app/tests/test_migrations.py` (lignes 21 à 36, fixture `base` et `_vider`), `DROP SCHEMA public CASCADE` est exécuté sur la base de `TEST_DATABASE_URL` au début et à la fin de chaque test, sans aucun contrôle. Une variable mal renseignée (par exemple vers la base `app` du conteneur d'aperçu ou de la production locale) effacerait toutes les réservations et tous les comptes.

À faire après le passage `TERMINE` de T-011 (le `testeur` y travaille), et avant T-061, qui ajoute des tests de migration sur cette même fixture.

## Critères d'acceptation
- [x] Avant toute connexion, la fixture refuse de s'exécuter (échec explicite, sans aucune requête envoyée) si le nom de la base de `TEST_DATABASE_URL` ne contient pas `test` ; la base `app` du modèle commun est donc toujours refusée.
- [x] Un test vérifie ce refus avec une URL qui désigne une base `app` sur un hôte injoignable (aucune base nécessaire), et vérifie qu'aucune instruction n'a été exécutée.
- [x] Le README de `app/` indique comment nommer la base de test (`…_test`) ; la suite complète est verte sur un PostgreSQL 16 jetable avec une base ainsi nommée.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25, commit 14398c1)
- **Commentaires** :
  1. Aucun point bloquant. Grille examinée : architecture (code de test uniquement, aucun fichier hors `app/` et ticket), lisibilité, duplication (une seule garde commune aux deux fixtures), erreurs (`GardeBaseRefusee` explicite), tests, sécurité (messages sans l'URL, vérifié par `test_le_message_ne_fuit_pas_l_url`), commit préfixé `T-060`.
  2. Règle de garde : correcte et plus stricte que le libellé. Suffixe `_test` obligatoire (`contest`, `test`, `_test`, `app_TEST` refusés, ce qui clôt ma remarque 6 sur T-011 et ma remarque 4 sur T-054), hôte local ou déclaré dans `TEST_DATABASE_HOTES_JETABLES`, paramètres `host`/`hostaddr`/`dbname`/`service` refusés, socket Unix refusée (hôte vide), URL illisible ou absente refusée.
  3. Appel avant toute écriture : confirmé dans les deux fixtures (`test_migrations.py:32`, avant `create_engine` et avant `_vider`, `DROP SCHEMA` ; `test_api_consultation.py`, avant `monkeypatch.setenv`, `create_engine` et `migrer`). Le test `test_fixture_refusee_n_envoie_aucune_instruction` couvre les deux avec une base `app` sur hôte injoignable.
  4. Écart de libellé du critère 1 (« ne contient pas `test` » remplacé par « ne se termine pas par `_test` ») : justifié, il couvre l'intention du critère (la base `app` est toujours refusée) et corrige le défaut de `"test" in nom`. À faire constater par le `testeur` au moment de cocher le critère ; le coordinateur peut le tracer dans le journal.
  5. Remarque (non bloquante) : l'écart de forme déclaré (module d'aide `tests/garde_base.py` au lieu d'un `conftest.py`) est acceptable. L'import `from garde_base import …` repose sur le `sys.path` de pytest ; la suite verte (214 tests) le confirme, mais il faut lancer pytest depuis `app/`, ce que le README indique déjà.
  6. Remarque (non bloquante) : j'ai relu le diff, pas relancé la suite (mon Bash est limité à git) ; la preuve « 214 passed sur PostgreSQL 16 » est celle du journal du développeur, à rejouer par le `testeur`. Je n'ai pas pu vérifier par recherche s'il existe d'autres fixtures qui lisent `TEST_DATABASE_URL` hors des deux modules modifiés ; le diff n'en montre pas, à confirmer par le `testeur`.
  7. Impact sur les autres agents : base nommée `…_test` désormais obligatoire pour lancer les tests d'intégration ; une base du type `app` (ancien exemple du README) ou `…test…` sans suffixe fait échouer les fixtures avec un message clair. Un lancement dans un conteneur sur réseau Docker exige `TEST_DATABASE_HOTES_JETABLES=<nom du conteneur de base>`. Le README le documente ; le coordinateur doit le rappeler aux agents `testeur` et `securite` dans leurs consignes de lancement.
- **Revue humaine requise** : non (code de test, aucune donnée réelle ; le risque couvert est une erreur de manipulation ; priorité normale, ne touche ni authentification, ni droits, ni données personnelles, ni secrets, ni paiements)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage du constat 13 et de la remarque 6 de T-011) · 0 h
- 2026-11-26 00:05 · agent:dev-backend · prise en charge (T-011 TERMINE, architecture et CDC VALIDÉS) · 0 h
- 2026-11-26 00:40 · agent:dev-backend · livré pour revue (non commité, à la demande du coordinateur). Fichiers : app/tests/garde_base.py (nouveau, garde commune), app/tests/test_garde_base.py (nouveau), app/tests/test_migrations.py (fixture `base` appelle la garde avant create_engine), app/tests/test_api_consultation.py (fixture `base` : l'assertion `"test" in nom` est remplacée par la même garde ; reste du comportement inchangé), app/README.md (nommage de la base de test). Pas de modification de conftest.py : la garde est un module d'aide `garde_base.py` importé par les fixtures (écart de forme signalé : fichier ajouté dans tests/). Ne touche pas T-071. · 0.6 h
- 2026-11-26 00:40 · agent:dev-backend · règle de garde : (1) nom de base finissant par `_test` (et plus que `_test`), plus strict que le critère « contient test » car `contest` passait ; (2) hôte dans {localhost, 127.0.0.1, ::1} ou listé dans la variable `TEST_DATABASE_HOTES_JETABLES` (noms séparés par des virgules) ; (3) paramètres d'URL host/hostaddr/dbname/service refusés (ils détourneraient la cible) ; socket Unix (hôte vide) refusée ; messages sans l'URL. Cas du conteneur sur réseau Docker : l'hôte est le nom du conteneur de base, qui ne peut pas être reconnu automatiquement comme jetable ; il doit être déclaré explicitement par la variable (liste blanche explicite plutôt qu'un motif de nom, pour qu'aucun hôte ne passe par accident) ; le suffixe `_test` reste exigé même pour un hôte déclaré. Documenté dans le README.
- 2026-11-26 00:40 · agent:dev-backend · couverture des critères (non cochés) : critère 1 → garde_base.py + test_garde_base.py::test_url_refusee (app, contest, test, hôtes distants…) ; critère 2 → test_garde_base.py::test_fixture_refusee_n_envoie_aucune_instruction (URL `app` sur hôte injoignable `db.invalide.test`, pour les deux fixtures ; create_engine et migrer.appliquer simulés et jamais appelés) ; critère 3 → README § tests ; suite complète sur PostgreSQL 16 jetable `coworking_test`. Sécurité : ne touche ni authentification ni données personnelles.
- 2026-11-26 00:40 · agent:dev-backend · tests : Docker python:3.14-slim + postgres:16-alpine sur réseau dédié, `TEST_DATABASE_URL=postgresql://esn:test@t060-pg:5432/coworking_test`, `TEST_DATABASE_HOTES_JETABLES=t060-pg`, `python -m pytest -q` → 214 passed, 0 skipped. Conteneur, réseau et image postgres:16-alpine d'essai supprimés. · 0 h
- 2026-11-25 15:30 · agent:testeur · vérifié sur le SHA 9114f9e4ff26b35c6fd219b05da94165b47c1a78 (git archive, copie en lecture seule ; python:3.14-slim 3.14.10 + postgres:16 jetable, réseau dédié, `TEST_DATABASE_URL=…@t067c6-pg:5432/coworking_test`, `TEST_DATABASE_HOTES_JETABLES=t067c6-pg`) : suite complète 214 passés, 0 ignoré, 0 échec. Critère 1 : base `app` refusée dans tous les cas constatés (`GardeBaseRefusee`, « le nom de la base de test doit se terminer par _test »), y compris sur un hôte déclaré jetable ; écart de libellé (« ne contient pas test » → « ne se termine pas par `_test` ») constaté : la règle retenue refuse tout ce que refusait le libellé (`app`) et en plus `contest`, `test`, `app_TEST` ; l'intention (la base `app` est toujours refusée) est satisfaite, critère coché. Preuve à la main : base `app` réelle créée dans le PostgreSQL jetable (table sentinelle = 42, table `reservations` = 2 lignes) ; `pytest tests/test_migrations.py tests/test_api_consultation.py` avec `TEST_DATABASE_URL` vers cette base `app` et l'hôte déclaré : 19 erreurs de fixture (garde), 31 passés (tests sans base) ; après coup sentinelle = 42 et 2 lignes, aucun DROP effectué. URL `db.invalide.test/app` et `…/coworking_test?dbname=app` refusées. Critère 2 : `test_fixture_refusee_n_envoie_aucune_instruction` rejoué (2 passés, un par module) ; mutation sur copie jetable (contrôle du suffixe retiré) : 9 échecs dans test_garde_base.py, donc le test est discriminant. Critère 3 : README (lignes 33 à 41) indique le suffixe `_test` et `TEST_DATABASE_HOTES_JETABLES` ; suite verte sur PostgreSQL 16 avec la base `coworking_test`. Lecteurs de `TEST_DATABASE_URL` dans app/ : `test_migrations.py` et `test_api_consultation.py` (garde appelée avant create_engine) ; `test_base.py` (lignes 34 à 51) lit la variable sans la garde mais n'exécute que `SELECT 1` et `GET /health` (lecture seule) : pas de risque destructeur, observation sans ticket. Avis APPROUVÉ, revue humaine non requise. vérifié : 3/3 critères, suites vertes, SHA 9114f9e → TERMINE · 0.3 h (temps compté dans T-067)
- 2026-11-25 16:15 · agent:securite · audit sécurité : NON BLOQUANT, rapport [securite-2026-11-25-6.md](../rapports/securite-2026-11-25-6.md) (SHA `14398c1585a6b5f045567aa383e28c506e480136`, valable aussi pour `9114f9e` et `748c75e`). Constat 13 fermé : garde appelée avant toute écriture dans les deux fixtures ; 42 URL hostiles (noms, hôtes, paramètres, encodage, `options`, majuscules) sans atteinte de la base `app`. Réserves basses : constat 18 (pytest afficherait l'URL, mot de passe compris, comme argument de `verifier_base_jetable` dans la trace d'un refus ; `ValueError` pour un port invalide) et constat 19 (`PGHOSTADDR` et assimilées contournent le contrôle d'hôte ; le suffixe `_test` protège toujours). Aucun ticket `bug`. Statut et critères inchangés. Temps compté dans T-043 · 0 h
