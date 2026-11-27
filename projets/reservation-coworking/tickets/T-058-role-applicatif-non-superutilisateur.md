---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-058
titre: Rôle PostgreSQL applicatif non superutilisateur (constat 10)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-057, T-029]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-27
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn (R18, DEC-023)
imputation_decision: DEC-020   # décision VALIDÉ qui met ce ticket à la charge de l'ESN
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-058 — Rôle PostgreSQL applicatif non superutilisateur (constat 10)

## Description
Réalisation de la décision [T-057](T-057-role-postgresql-application.md), tranchée par [DEC-013](../../../docs/decisions/2026-11-25-DEC-013-role-postgresql-coworking.md) (`VALIDÉ`, **option A** : un rôle applicatif unique, non superutilisateur, propriétaire de la base `app`). Le contenu, rédigé pour l'option A avant la décision, a été vérifié le 2026-11-27 au regard des points 1 à 5 de DEC-013 : il y correspond, aucun changement de périmètre ni d'estimation. **La condition « ne pas commencer avant la décision » est levée** (T-057 `TERMINE`, DEC-013 `VALIDÉ`) ; le ticket reste non prenable tant que **T-029** n'est pas `TERMINE` (même outillage, DEC-013 point 4).

**Ordre imposé par DEC-013 (point 4)** : terminé **avant T-044** (premier environnement qui contient des comptes) et en tout cas avant **T-047** ; T-044 et T-047 dépendent de ce ticket (`depend_de`).

**Contrainte associée pour la chaîne `dev-backend`** (DEC-013 point 4, rappel) : à partir de T-013, aucune migration ne doit exiger de droits de superutilisateur (pas de `CREATE EXTENSION` ni de `CREATE ROLE`). Le critère sur les migrations ci-dessous le vérifie pour le schéma existant.

Constat 10 du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md) : l'app et les migrations utilisent `esn`, superutilisateur de l'image `postgres`, et le modèle commun `deploiement/docker-compose.yml` (DEC-003, responsable C) prend `absent` comme mot de passe si `PG_PASSWORD` manque. Attendu : un rôle applicatif sans privilège de superutilisateur, propriétaire de la base `app`, utilisé dans `DATABASE_URL` ; `esn` réservé à l'initialisation et à l'exploitation (`pg_dump`, restauration, sauvegarde de T-029).

**Pourquoi un salarié (AF6 écarté).** Le travail porte sur l'outillage commun de tous les projets (`deploiement/`, `scripts/deployer_local.py`), hors du périmètre d'écriture des agents de réalisation (`app/` seulement) et du `deployeur` (qui exécute l'outillage sans le modifier). C'est le même cas que T-029, confié à Nadia (compétences `docker` et `ci-cd` `confirme`). Après T-029, parce que les deux tickets modifient les mêmes scripts. **Ticket salarié (AF11, R15)** : à faire par un humain ; la PR est relue et acceptée par C.

**Touche la sécurité** (droits sur la base, secrets) : revue humaine obligatoire, ticket compagnon **T-059** (Karim).

## Critères d'acceptation
- [ ] `deploiement/docker-compose.yml` ne contient plus aucun repli de mot de passe (`:-absent`) : sans `PG_PASSWORD` (ou sans le mot de passe du rôle applicatif), `docker compose config` échoue avec un message explicite (test de `scripts/`).
- [ ] Un rôle applicatif `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`, propriétaire de la base `app`, est créé de façon idempotente par `deployer_local.py` ; son mot de passe est tiré au hasard au premier déploiement, gardé dans `deploiement/local/<slug>/` (ignoré par Git), jamais affiché ni journalisé (recherche dans la sortie du déploiement).
- [ ] La `DATABASE_URL` transmise à l'app utilise ce rôle : sur une instance déployée, `SELECT rolsuper, rolcreaterole, rolcreatedb FROM pg_roles WHERE rolname = current_user`, exécuté avec cette URL, renvoie `f, f, f`, et `COPY (SELECT 1) TO PROGRAM 'true'` est refusé.
- [ ] Les migrations de l'app (`alembic upgrade head` au démarrage, T-011) passent avec ce rôle sur une base neuve : `/health` en 200 et 3 salles présentes.
- [ ] Sur un volume créé par l'ancien modèle (tables appartenant à `esn`), un redéploiement crée le rôle, lui transfère la propriété de la base, du schéma et des objets existants, et l'app redémarre sans erreur (test).
- [ ] `pg_dump` avant déploiement, `rollback_local.py` et la sauvegarde quotidienne de T-029 fonctionnent toujours (tests de `scripts/` verts).
- [ ] Le commentaire d'en-tête du modèle commun décrit les deux rôles (`esn` pour l'initialisation et l'exploitation, rôle applicatif pour l'app et ses migrations, DEC-013 points 1 et 2) et les variables ; PR acceptée par C (DEC-013 point 5).
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (droits de la base et secrets, S3-R2 ; ticket compagnon T-059)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage du constat 10, rapport securite-2026-11-25-3) ; contenu rédigé pour l'option A de T-057, à ajuster après la décision · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
- 2026-11-27 10:56 · agent:chef-de-projet · application de DEC-013 (option A, VALIDÉ) : contenu vérifié, conforme à l'option A (aucun changement de périmètre, d'assigné ni d'estimation) ; mention « ne pas commencer avant la décision » levée ; ordre « avant T-044 et T-047 » et contrainte sur les migrations rappelés en Description ; critère de l'en-tête du modèle commun précisé (rôles `esn` et applicatif) ; T-058 ajouté à `depend_de` de T-044 et de T-047 ; statut `A_FAIRE` et `depend_de: [T-057, T-029]` inchangés · 0 h (temps compté dans T-008)
