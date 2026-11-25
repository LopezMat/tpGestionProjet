---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-011
titre: Modèle de données et migrations
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: base-de-donnees-sql (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 3            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-25   # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-011 — Modèle de données et migrations

## Description
Schéma PostgreSQL 16 de [architecture.md](../architecture.md) § 4, créé uniquement par migrations Alembic, et démarrage tolérant du § 8 (compatibilité avec le rollback, règle « étendre puis contracter »). Base de F-01 à F-08 ; insertion des 3 salles (H-20, F-06).

## Critères d'acceptation
- [x] Une migration Alembic crée les tables `utilisateur`, `salle`, `reservation` et `session` avec les colonnes du § 4 et les contraintes : `UNIQUE (email)`, `CHECK role IN ('membre', 'accueil')`, `UNIQUE (salle_id, date_creneau, heure_debut)`, `CHECK heure_debut BETWEEN 8 AND 19`, `CHECK EXTRACT(ISODOW FROM date_creneau) <= 5`, `ON DELETE CASCADE` de `reservation` et `session` vers `utilisateur`, index `(utilisateur_id, date_creneau)` et `(date_creneau)` (test d'intégration sur le schéma).
- [x] Les 3 salles « Salle 1 », « Salle 2 » et « Salle 3 » sont insérées par migration (H-20).
- [x] Le catalogue des salles est une donnée de référence indépendante de l'authentification : sur une base vide, `alembic upgrade head` suffit à obtenir les 3 salles, sans aucun compte, script d'initialisation ni jeu de données de démonstration (test d'intégration) ; relancer la migration ne crée pas de doublon (DEC-011).
- [x] Au démarrage, `reservation.demarrer` lance `alembic upgrade head` si la révision de la base est connue de l'image ; si la base est à une révision plus récente, il journalise un avertissement et démarre sans migrer (test).
- [x] Les migrations sont uniquement additives ; aucune migration descendante n'est lancée automatiquement.
- [x] Les tests d'intégration tournent sur un PostgreSQL 16 réel (conteneur jetable), jamais sur SQLite.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25), commit 2852fe7. Aucun écart sur la grille ; remarques non bloquantes ci-dessous. Les 105 tests verts annoncés restent à vérifier par le `testeur` (porte 2).
- **Commentaires** :
  1. Conformité (architecture § 4, critères) : colonnes, `UNIQUE (email)`, `CHECK role`, `UNIQUE (salle_id, date_creneau, heure_debut)`, `CHECK heure_debut BETWEEN 8 AND 19`, `CHECK ISODOW <= 5`, `ON DELETE CASCADE` (reservation et session), index `(utilisateur_id, date_creneau)`, `(date_creneau)` et `session(utilisateur_id)` : conformes (`versions/0001_schema_initial.py`). Salles : ids fixes 1 à 3, `ON CONFLICT (id) DO NOTHING`, aucune dépendance à `utilisateur` (DEC-011) ; les tests couvrent base vide sans compte et double appel.
  2. « Étendre puis contracter » et § 8 : migration 0001 additive, sans `downgrade` ; `migrer.appliquer` n'appelle que `command.upgrade(cfg, "head")` ; révision inconnue de l'image : avertissement sans migration et démarrage (testé). Conforme.
  3. Remarque 1 de T-010 : `_moteur` renommé `_moteur_sonde` sans autre changement (aucune référence restante dans `app/` ni dans `test_health_delai.py`), moteur applicatif séparé (pool 5+5, `pool_pre_ping`, sans `statement_timeout`), moteur de migration propre (NullPool). Comportement de /health inchangé. Conforme.
  4. Écarts déclarés : `migrer.py` (évite le conflit de nom avec le paquet `migrations/`), Alembic sans `alembic.ini` (URL par `config.attributes`, non écrite ni journalisée), `salle.id` smallint sans auto-incrément (cohérent avec ids fixes) : acceptés, sans impact sur l'architecture.
  5. Échec de migration : message sans détail (`demarrer.py`), code 1, test sans fuite du mot de passe. Les messages d'erreur d'`env.py` ne contiennent pas l'URL. Conforme.
  6. Remarque (non bloquante) : `tests/test_migrations.py`, fixture `base` : `DROP SCHEMA public CASCADE` sur la base de `TEST_DATABASE_URL`. Ajouter un garde-fou (refuser si le nom de la base ne contient pas « test » ou si l'hôte n'est pas local) pour qu'une variable mal renseignée ne détruise jamais une base réelle.
  7. Remarque (non bloquante) : `test_aucune_migration_descendante` interdit toute chaîne `drop_` dans `versions/`. L'architecture § 8 autorise une suppression en seconde livraison (« contracter ») : prévoir d'adapter ce test (par exemple un marqueur explicite) quand ce cas se présentera.
  8. Remarque (non bloquante) : `test_moteurs_distincts` compare deux fonctions différentes ; l'assertion est toujours vraie. Seule la vérification `not hasattr(bdd, "_moteur")` a une valeur ; le test sur le pool (`test_moteur_applicatif_a_un_pool_et_sert_les_requetes`) est le bon.
  9. Périmètre : commits `T-011` ; fichiers uniquement sous `app/` et le ticket. Conforme.
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 09:45 · agent:coordinateur · critère ajouté : catalogue des salles créé par migration sans dépendre de l'authentification (demande d'Ethan, DEC-011) · 0 h
- 2026-11-25 · agent:coordinateur · à prendre en compte (remarque 1 de la revue passe 2 de T-010) : le moteur de `bdd.py` est un moteur de **sonde** (`NullPool`, `statement_timeout=1000`) ; ne pas le réutiliser pour les migrations ni pour les routes métier : créer un moteur applicatif séparé (pool) et renommer celui de la sonde · 0 h
- 2026-11-25 10:00 · agent:dev-backend · prise en charge (A_FAIRE -> EN_COURS) · 0 h
- 2026-11-25 11:30 · agent:dev-backend · réalisation. Choix : (1) remarque 1 de T-010 : `bdd._moteur` renommé `_moteur_sonde` (comportement de /health inchangé) ; ajout d'un moteur applicatif séparé `bdd.moteur_applicatif()` (QueuePool 5+5, pre_ping, sans statement_timeout) ; les migrations ont leur propre moteur (NullPool) dans `migrations/env.py`. (2) Alembic sans alembic.ini, dans le paquet `reservation/migrations/` (donc déjà copié par le Dockerfile, Dockerfile inchangé) ; URL passée par `config.attributes`, jamais écrite ni journalisée. (3) Module de démarrage nommé `reservation/migrer.py` (`appliquer()`), pour ne pas entrer en conflit avec le paquet `migrations/`. (4) Migration 0001 sans `downgrade` (additive uniquement) ; salles : id fixes 1 à 3, `INSERT ... ON CONFLICT (id) DO NOTHING`, aucune dépendance à `utilisateur` (DEC-011). (5) `demarrer.main` : migration après l'attente de la base ; échec -> message sans détail (l'URL peut contenir le mot de passe), code 1. (6) Base en avance : `alembic_version` inconnue de l'image -> avertissement, pas de migration, démarrage. Fichiers partagés modifiés de façon minimale : `reservation/demarrer.py` (appel de `migrer.appliquer`), `tests/test_demarrer.py` (fixture autouse qui neutralise la migration) ; `requirements*.txt`, `conftest.py` et `app.py` non touchés ; README mis à jour. Aucune dépendance ajoutée (alembic et SQLAlchemy déjà épinglés). Ne touche pas la sécurité (aucune authentification ni donnée personnelle manipulée, juste le schéma). · 2.5 h
- 2026-11-25 12:00 · agent:dev-backend · tests : PostgreSQL 16 jetable (postgres:16) + suite complète sous Python 3.14 (python:3.14-slim), via `TEST_DATABASE_URL`. Résultat : 105 passed (dont tests/test_health_delai.py : 7 passed). Conteneurs, réseau d'essai supprimés ; aucune image créée (les images postgres:16 et python:3.14-slim préexistaient et sont conservées). Couverture des critères (sans les cocher) : 1 schéma -> tests/test_migrations.py::test_tables_et_colonnes, test_email_unique_et_role_controle, test_contraintes_de_reservation, test_suppression_utilisateur_en_cascade, test_index_attendus ; 2 et 3 salles/DEC-011 -> test_trois_salles_sur_base_vide_sans_compte (double appel, aucun compte, aucun doublon), test_upgrade_head_direct_donne_les_salles ; 4 démarrage tolérant -> test_migrer_est_appele_au_demarrage_et_applique_la_tete, test_base_en_avance_avertit_et_ne_migre_pas, test_demarrage_avec_base_en_avance_demarre ; 5 additif -> test_aucune_migration_descendante, test_demarrage_n_appelle_que_upgrade_head ; 6 PostgreSQL réel -> tous les tests d'intégration (psycopg sur postgres:16, aucun SQLite). Commit : non fait, consigne du coordinateur. · 0.5 h
- 2026-11-25 12:00 · agent:dev-backend · livré pour revue (EN_COURS -> EN_REVUE) ; critères non cochés (rôle du testeur) · 0 h
- 2026-11-25 13:45 · agent:securite · audit sécurité : NON BLOQUANT (commit 2852fe7), rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md). 0 critique, 0 haute. Constats propres à T-011 : n° 10 (moyen, rôle PostgreSQL superutilisateur utilisé par l'app et les migrations, décision humaine), n° 11 (bas, e-mail unique sensible à la casse, champs vides acceptés), n° 13 (bas, `DROP SCHEMA` sans garde-fou dans la fixture de test). Journalisation d'un échec de migration vérifiée sans fuite sur une base jetable · 0 h (temps compté dans T-043)
- 2026-11-25 23:56 · agent:testeur · vérifié sur le SHA 2852fe7 : 6/6 critères, suites vertes, avis relecteur APPROUVÉ, revue humaine non requise → TERMINE. Preuves : suite complète sous Python 3.14.10 (`python:3.14-slim`) avec `TEST_DATABASE_URL` vers un `postgres:16` jetable : 105 passés, 0 ignoré (aucun test d'intégration ignoré), dont 15 de `test_migrations.py`. (1) schéma : `test_tables_et_colonnes`, `test_email_unique_et_role_controle`, `test_contraintes_de_reservation`, `test_suppression_utilisateur_en_cascade`, `test_index_attendus` verts ; constaté en plus par `pg_constraint` / `pg_indexes` sur la base du conteneur : `uq_utilisateur_email`, `ck_utilisateur_role`, `uq_reservation_creneau (salle_id, date_creneau, heure_debut)`, `ck_reservation_heure` (8 à 19), `ck_reservation_jour_ouvre` (ISODOW <= 5), deux `ON DELETE CASCADE` (reservation et session), index `(utilisateur_id, date_creneau)`, `(date_creneau)`. (2, 3) image construite avec `--build-arg GIT_COMMIT=2852fe7…` puis conteneur sur base vide sans aucun compte : migration 0001 appliquée au démarrage, 3 salles (« Salle 1 » à « Salle 3 »), 0 utilisateur ; redémarrage du conteneur : toujours 3 salles (pas de doublon) ; `test_trois_salles_sur_base_vide_sans_compte` (double appel) et `test_upgrade_head_direct_donne_les_salles` verts. (4) base mise à `9999_future` : redémarrage du conteneur, journal « La base est à une révision plus récente que cette image (9999_future) : démarrage sans migration. », /health 200, `alembic_version` inchangée ; `test_base_en_avance_avertit_et_ne_migre_pas` et `test_demarrage_avec_base_en_avance_demarre` verts. (5) `grep downgrade` dans `app/reservation` : seule la docstring de 0001 le mentionne ; `migrer.appliquer` n'appelle que `upgrade head` ; `test_aucune_migration_descendante`, `test_demarrage_n_appelle_que_upgrade_head` verts. (6) tous les tests d'intégration sur PostgreSQL 16 (psycopg), aucun SQLite. Non-régression T-010 : /health 200 `{"status":"ok","commit":"2852fe746fb4be045fca1a70c876a3e02fdd0120"}` en 0,049 s sur base vide après migration ; `test_health_delai.py` 7 sur 7. Constats 10, 11, 13 de l'audit et remarques 6 à 8 du relecteur : hors critères, non traités ici (constat 13 : `TEST_DATABASE_URL` n'a visé que la base jetable). Rapport [tests-2026-11-25.md](../rapports/tests-2026-11-25.md) · temps compté dans T-041
