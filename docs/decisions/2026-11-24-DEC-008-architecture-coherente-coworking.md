---
titre: Architecture v1.1 cohérente avec DEC-007 (purge des sauvegardes, fin de démonstration)
statut: VALIDÉ
responsable: A
version: 1.0
maj_le: 2026-11-24
valide_par:      Ethan           # rempli par l'humain qui valide
decision: DEC-008           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-008
date: 2026-11-24
decide_par: Ethan
projet: reservation-coworking
ticket: T-004
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-008 — Architecture v1.1 cohérente avec DEC-007 (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir des décisions d'Ethan (rôle C) du 2026-11-24. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`, après relecture de l'architecture v1.1. Chaque « Pourquoi » est celui formulé par Ethan (skill `tracer-decision`, étape 1).

## Contexte
[DEC-007](2026-11-24-DEC-007-choix-techniques-coworking.md) (`VALIDÉ`) a retenu les choix techniques du projet, dont la suppression de toute sauvegarde au plus tard 30 jours après sa création, **appliquée aussi au déploiement**. L'`architecte` révisait [architecture.md](../../projets/reservation-coworking/architecture.md) en conséquence (v0.4) quand le document a été passé `VALIDÉ` (v1.0). Le hook a refusé la suite de la révision (R6) : la v1.0 validée se contredisait (§ 8 à 11 encore en v0.3). L'incident est noté dans le [retex](../../projets/reservation-coworking/retex.md).

Ethan a repassé l'architecture en `EN_REVUE` (R6, procédure « Modifier un document VALIDÉ » du registre) et tranché deux points restés ouverts, signalés par l'`architecte`. La révision complétée est l'architecture **v1.1**, qui sera revalidée avec cette décision.

## Options étudiées
| Point | Options | Retenue |
|---|---|---|
| Architecture v1.0 incohérente | garder la v1.0 validée et faire primer DEC-007 en cas de conflit ; rouvrir, compléter la révision et revalider | **Rouvrir et revalider (v1.1)** |
| R-05 : la purge par âge ne tourne que si un déploiement ou la sauvegarde quotidienne s'exécute | annoncer une garantie absolue ; écrire la limite telle quelle et ajouter une étape de fin de démonstration | **Limite écrite telle quelle + étape « supprimer les dossiers de sauvegardes » en fin de démonstration** |
| Message de la sortie du déploiement | un seul message « Rétention » pour les deux causes (code de `deployer_local.py` inchangé) ; message « Limite d'âge » distinct (modification de `deployer_local.py`) | **Message « Limite d'âge » distinct** |

## Décision
1. **L'architecture est revalidée en v1.1**, révision v0.4 complétée : la limite de 30 jours s'applique à chaque déploiement (`purger_sauvegardes()`) et à chaque sauvegarde quotidienne, `test_retention` est adapté (dates relatives au jour du test), et la revue humaine de Karim porte sur les tickets d'authentification (S3-R2). Elle remplace la v1.0 ; DEC-007 reste en vigueur.
2. **R-05** : la limite est écrite telle quelle — la purge s'exécute à chaque déploiement et à chaque sauvegarde quotidienne. **À la fin de la démonstration, les dossiers de sauvegardes du projet sont supprimés** selon la procédure décrite dans l'architecture.
3. **`deployer_local.py` affiche un message « Limite d'âge » distinct de « Rétention »** quand une sauvegarde est supprimée par la limite de 30 jours. La même distinction s'applique à la sortie de la sauvegarde quotidienne.
4. **Les autres données de démonstration sont traitées par un ticket « Fin de démonstration »** (ticket `decision`, décision humaine), créé par le `chef-de-projet` au planning. Il couvre le volume `esn-reservation-coworking_pgdata`, `historique.json`, `db_password` (dans `deploiement/local/reservation-coworking/`) et les sauvegardes. L'architecture v1.1 n'est pas modifiée pour ce point.

## Pourquoi
*(Ethan, 2026-11-24)*
- **Revalidation** : la v1.1 intègre les choix de C sur la limite de 30 jours et la fin de démonstration ; le reste de l'architecture validée en v1.0 est inchangé.
- **R-05** : aucune donnée de démonstration ne doit rester sur le poste après la soutenance.
- **Message distinct** : l'humain qui lit la sortie doit savoir quelle règle a supprimé une sauvegarde.
- **Ticket « Fin de démonstration »** : la suppression de données se décide au moment de les supprimer, après la soutenance.

## Impacts
- Fichiers ou règles à mettre à jour :
  - `projets/reservation-coworking/architecture.md` : v1.1 par l'`architecte`, puis `VALIDÉ` par un humain (`valide_par`, `decision: DEC-008`, version 2.0 ou 1.1 selon la convention retenue par l'humain) ;
  - `scripts/prod_locale.py`, `scripts/deployer_local.py` et leurs tests (outillage de C) : purge par âge au déploiement, message « Limite d'âge », `test_retention` adapté ; par PR relue par C, dans le ticket de sauvegarde du planning. `purger_sauvegardes()` renvoie désormais des couples `(règle, chemin)` (seul appelant : `deployer_local.py`) : changement d'interface à accepter par C à la PR ;
  - `docs/ARCHITECTURE.md` § 10.2 (qui ne mentionne que les « 10 dernières ») : à mettre à jour dans la même PR, car la limite de 30 jours s'applique à tous les projets en production locale.
- Tickets créés ou débloqués :
  - T-004 (« Architecture ») conclu par le coordinateur une fois la v1.1 validée ;
  - au planning (`chef-de-projet`) : le ticket de sauvegarde inclut la purge au déploiement, le message distinct et leurs tests ; un ticket `decision` « Fin de démonstration » (décision humaine, après la soutenance) couvrant le volume `esn-reservation-coworking_pgdata`, `historique.json`, `db_password` et les sauvegardes.
- Points d'outillage (interface de `purger_sauvegardes()`, `docs/ARCHITECTURE.md` § 10.2) : traités dans la PR de l'outillage.
- Règles : aucune règle modifiée.
