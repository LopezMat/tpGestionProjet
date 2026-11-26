---
titre: Rôle PostgreSQL de l'application reservation-coworking (non superutilisateur)
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-25
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-013           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-013
date: 2026-11-25
decide_par: Johan
projet: reservation-coworking
ticket: T-057
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-013 — Rôle PostgreSQL de l'application (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision de Johan du 2026-11-25 (option A du ticket T-057). Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. Le « Pourquoi » est la recommandation du ticket T-057, que Johan a explicitement demandé de reprendre comme motif.

## Contexte
L'audit de sécurité d'incrément de T-011 et T-012 ([securite-2026-11-25-3.md](../../projets/reservation-coworking/rapports/securite-2026-11-25-3.md), constat 10, sévérité moyenne, commit `2852fe7`) a constaté que l'application se connecte à PostgreSQL avec le rôle `esn`, `POSTGRES_USER` de l'image officielle, donc **superutilisateur**. Depuis T-011, ce même rôle sert aux migrations et au moteur applicatif qui manipulera les données personnelles (T-013 et suivants). Une compromission de l'app aurait un impact maximal (`COPY … TO PROGRAM`, lecture et suppression de toutes les données). Le modèle commun `deploiement/docker-compose.yml` (DEC-003, responsable C) prend en outre `absent` comme mot de passe si `PG_PASSWORD` manque.

La correction touche le modèle commun de DEC-003 et le choix d'une seule `DATABASE_URL` de l'[architecture](../../projets/reservation-coworking/architecture.md) v1.1 (VALIDÉ, DEC-008) : c'est un choix technique, tranché par un humain (R7), via le ticket [T-057](../../projets/reservation-coworking/tickets/T-057-role-postgresql-application.md).

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| **A : un rôle applicatif unique, non superutilisateur, propriétaire de la base `app` (retenue)** | Supprime l'impact maximal ; aucun changement de code dans `app/` ni sur la chaîne `dev-backend` ; une seule `DATABASE_URL` conservée, architecture non rouverte ; ≈ 175 € | Le rôle reste propriétaire du schéma : une injection pourrait encore modifier ou supprimer les tables du projet ; modèle commun modifié pour tous les projets |
| B : deux rôles (migrations et exécution) | Risque résiduel le plus faible : l'app ne peut ni créer ni supprimer de table | Gain réel seulement avec une étape de migration séparée : `architecture.md` § 7 et § 8 à rouvrir avant T-013, démarrage tolérant de T-011 à revoir ; ≈ 324 € ; +0,3 jour ouvré |
| C : supprimer `:-absent` maintenant, rôle avant le GO | Aucun effet immédiat | Travail placé en fin de projet, sur le chemin de la recette (risque sur le GO) ; T-013 à T-020 développés sous superutilisateur ; ≈ 207 € |
| D : accepter le risque | 0 € | Risque moyen conservé en production, contraire à la recommandation du `securite` |

## Décision
1. **L'application reservation-coworking et ses migrations se connectent avec un rôle applicatif unique, `NOSUPERUSER NOCREATEDB NOCREATEROLE`, propriétaire de la base `app`** (donc du schéma `public` sous PostgreSQL 16), avec un mot de passe tiré au hasard et gardé hors Git comme `PG_PASSWORD`. La `DATABASE_URL` de l'app utilise ce rôle ; le principe d'une seule `DATABASE_URL` (architecture v1.1) est conservé.
2. **Le rôle `esn` ne sert plus qu'à l'initialisation et à l'exploitation** (`pg_dump`, restauration).
3. **Le modèle commun crée ce rôle de façon idempotente** (par `deployer_local.py`), y compris sur un volume créé par l'ancien modèle, et **le repli `:-absent` est supprimé** : une variable manquante fait échouer le lancement explicitement.
4. **Réalisation** : T-058 (Nadia), juste après T-029 (même outillage), **terminé avant T-044** (premier environnement qui contient des comptes) et en tout cas avant T-047 ; revue humaine T-059 (Karim). Aucune migration ne doit exiger de droits de superutilisateur (pas de `CREATE EXTENSION` ni de `CREATE ROLE`), à partir de T-013.
5. **Accord de C** sur la modification du modèle commun : donné (Johan, 2026-11-25). La modification passe par une PR relue et acceptée par C.

## Pourquoi
*(Johan, 2026-11-25, reprenant la recommandation du ticket T-057)* L'option A supprime l'impact maximal (superutilisateur) pour environ 175 €, sans toucher au code de `app/` ni à la chaîne `dev-backend`, et sans rouvrir l'architecture validée, puisque le principe d'une seule `DATABASE_URL` est conservé. L'option B est la cible de sécurité, mais son gain réel exige une étape de migration séparée, ce qui rouvrirait l'architecture et le démarrage tolérant de T-011 à trois semaines de la deadline : elle est à inscrire au retour d'expérience.

## Impacts
- Fichiers ou règles à mettre à jour :
  - `deploiement/docker-compose.yml` et `scripts/deployer_local.py` (modèle commun, DEC-003, responsable C) : par T-058, via une PR acceptée par C ;
  - `architecture.md` : aucun changement obligatoire ; précision « rôle non superutilisateur, propriétaire de la base » portée par ce DEC (amendement facultatif, à faire repasser `EN_REVUE` par un humain si souhaité) ;
  - aucune règle modifiée.
- Tickets créés ou débloqués :
  - T-057 : à débloquer par l'humain (`decision: DEC-013`) ;
  - T-058 : prenable après T-029 ; le `chef-de-projet` l'ajuste à l'option A en citant DEC-013 ;
  - T-044 et T-047 : `depend_de` complété par T-058 ;
  - T-059 : revue humaine de T-058 (Karim).
- Budget et délais : ≈ 175 € (Nadia 2 h, Karim 0,5 h, revue de code 0,5 h) ; date de fin projetée inchangée (hors chaîne `dev-backend`) ; T-044 peut glisser d'environ 1 jour ouvré, sans dépasser le début de la recette.
- Retour d'expérience : ticket `amelioration` à prévoir pour l'option B (deux rôles et étape de migration séparée) dans le modèle commun.
