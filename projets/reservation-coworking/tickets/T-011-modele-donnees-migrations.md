---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-011
titre: Modèle de données et migrations
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
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
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-011 — Modèle de données et migrations

## Description
Schéma PostgreSQL 16 de [architecture.md](../architecture.md) § 4, créé uniquement par migrations Alembic, et démarrage tolérant du § 8 (compatibilité avec le rollback, règle « étendre puis contracter »). Base de F-01 à F-08 ; insertion des 3 salles (H-20, F-06).

## Critères d'acceptation
- [ ] Une migration Alembic crée les tables `utilisateur`, `salle`, `reservation` et `session` avec les colonnes du § 4 et les contraintes : `UNIQUE (email)`, `CHECK role IN ('membre', 'accueil')`, `UNIQUE (salle_id, date_creneau, heure_debut)`, `CHECK heure_debut BETWEEN 8 AND 19`, `CHECK EXTRACT(ISODOW FROM date_creneau) <= 5`, `ON DELETE CASCADE` de `reservation` et `session` vers `utilisateur`, index `(utilisateur_id, date_creneau)` et `(date_creneau)` (test d'intégration sur le schéma).
- [ ] Les 3 salles « Salle 1 », « Salle 2 » et « Salle 3 » sont insérées par migration (H-20).
- [ ] Le catalogue des salles est une donnée de référence indépendante de l'authentification : sur une base vide, `alembic upgrade head` suffit à obtenir les 3 salles, sans aucun compte, script d'initialisation ni jeu de données de démonstration (test d'intégration) ; relancer la migration ne crée pas de doublon (DEC-011).
- [ ] Au démarrage, `reservation.demarrer` lance `alembic upgrade head` si la révision de la base est connue de l'image ; si la base est à une révision plus récente, il journalise un avertissement et démarre sans migrer (test).
- [ ] Les migrations sont uniquement additives ; aucune migration descendante n'est lancée automatiquement.
- [ ] Les tests d'intégration tournent sur un PostgreSQL 16 réel (conteneur jetable), jamais sur SQLite.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
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
