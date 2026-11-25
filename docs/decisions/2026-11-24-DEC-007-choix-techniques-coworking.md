---
titre: Choix techniques du projet reservation-coworking
statut: VALIDÉ  
responsable: A
version: 1.0
maj_le: 2026-11-24
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-007           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-007
date: 2026-11-24
decide_par: Ethan
projet: reservation-coworking
ticket: T-005
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-007 — Choix techniques (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir des décisions d'Ethan du 2026-11-24 sur T-005. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`, après relecture de l'architecture v0.4. Chaque « Pourquoi » est celui formulé par Ethan (skill `tracer-decision`, étape 1).

## Contexte
L'`architecte` a livré [architecture.md](../../projets/reservation-coworking/architecture.md) v0.1 à partir du CDC v1.0 (`VALIDÉ`, [DEC-006](2026-11-24-DEC-006-validation-cdc-coworking.md)) et le ticket [T-005](../../projets/reservation-coworking/tickets/T-005-choix-techniques.md) « Choix techniques », qui pose sept points à arbitrer (A à G). L'hébergement reste la production locale Docker ([DEC-003](2026-11-24-DEC-003-production-locale-docker.md)). Les décisions ci-dessous sont reportées par l'`architecte` dans l'architecture v0.2, puis les corrections d'Ethan (seuil global, limite de 30 jours des sauvegardes, Pourquoi de C) dans la v0.3, et le choix de C sur la purge par âge au déploiement dans la v0.4.

## Options étudiées
| Point | Options (détail dans T-005) | Retenue |
|---|---|---|
| A. Stack | A1 Python 3.14 + FastAPI, front HTML/CSS/JS sans build, PostgreSQL 16, Argon2id, sessions en base ; A2 front React + Vite ; A3 Django | **A1** |
| B. Compte accueil initial | B1 commande `init_accueil` lancée par un humain via `docker exec` ; B2 variable dans le `docker-compose.yml` commun | **B1, durcie** (variable passée sans valeur) |
| C. Clé de signature des sessions (CDC § 8) | prise d'acte de l'écart de forme ; ou modification du CDC | **Prise d'acte**, CDC non modifié |
| D. Sauvegarde quotidienne (CDC § 9) | D1 tâche quotidienne 14 j + limite de 30 j pour toutes les sauvegardes du projet ; D2 tâche quotidienne seule ; D3 sauvegardes d'avant déploiement seules | **Commande de sauvegarde seule dans l'outillage, rétention 14 jours, tâche planifiée quotidienne, et suppression de toute sauvegarde du projet au plus tard 30 jours après sa création** (équivalent de D1) |
| E. Accès limité au poste (`127.0.0.1`) | accepter pour la démonstration ; exposer l'app (hébergeur distant) | **Accepté comme limite de la démonstration** |
| F. Suppression d'un compte accueil | ajouter ; ne pas ajouter | **Ne pas ajouter** |
| G. Seuils de sécurité | seuils proposés par l'architecte ; autres | **Acceptés provisoirement**, sauf le blocage global : remplacé par une alerte journalisée |

## Décision
1. **A. Stack A1** : une seule image ; Python 3.14 + FastAPI + Uvicorn ; front HTML/CSS/JS sans framework ni build, servi par l'app ; PostgreSQL 16 + SQLAlchemy 2.0 + Alembic + psycopg 3 ; mots de passe hachés en Argon2id ; sessions opaques stockées en base.
2. **B. Compte accueil initial** : la commande `init_accueil` est lancée une fois par un humain via `docker exec`, avec la variable du mot de passe passée **sans valeur** (`docker exec -e ACCUEIL_MOT_DE_PASSE_INITIAL …`) ; la valeur est saisie sans affichage dans la session juste avant, puis effacée. La procédure exacte est documentée dans l'architecture.
3. **C. Prise d'acte** : avec des sessions stockées en base, il n'existe pas de clé de signature des sessions ; l'identifiant de session est un jeton aléatoire vérifié côté serveur. L'écart de forme avec le CDC § 8 est tracé ici ; **le CDC validé n'est pas modifié**.
4. **D. Sauvegardes** : avec l'accord de C (Ethan), une commande de sauvegarde seule est ajoutée à l'outillage, en réutilisant `scripts/prod_locale.py`, avec une **rétention de 14 jours** ; une tâche planifiée quotidienne est documentée. De plus, **toute sauvegarde du projet (avant déploiement et quotidienne) est supprimée au plus tard 30 jours après sa création**, en plus de la règle des 10 dernières de DEC-003 : `prod_locale.py` est modifié en conséquence (accord de C, Ethan). **Choix de C (Ethan) : la limite de 30 jours s'applique aussi au déploiement** (`deployer_local.py` / `purger_sauvegardes()`), pas seulement dans la commande quotidienne ; `test_retention` est adapté (dates relatives au jour du test). **Les tests de `prod_locale` doivent rester verts.** Le code est réalisé par un ticket du planning.
5. **E. Limite de la démonstration** : l'application n'est accessible que depuis le poste (`127.0.0.1:8080`). Une mise en ligne réelle demanderait un hébergeur distant et une nouvelle décision (DEC-003).
6. **F.** Pas de suppression de compte accueil (hors CDC).
7. **G. Seuils provisoires** : mot de passe de 12 à 128 caractères ; 5 échecs de connexion par e-mail en 15 min → refus pendant 15 min (blocage par compte) ; **pas de blocage global** : au-delà de 30 échecs toutes adresses confondues en 15 min, l'application journalise une alerte (remontée par `analyste-prod`) sans bloquer personne ; session expirée après 2 h d'inactivité, 12 h au maximum. Ils sont à confirmer à l'audit `securite` et à la revue humaine de Karim.
8. **Karim** : son allocation au projet est décidée au planning (il est sur le chemin critique de l'authentification).
9. **Architecture validée par Ethan ; la revue humaine de Karim est reportée aux tickets d'authentification (S3-R2).**

## Pourquoi
*(Ethan, 2026-11-24)*
- **A** : la plus simple à maintenir et à auditer pour ce périmètre ; aucune chaîne de build front ; aucune clé secrète à gérer.
- **B** : le mot de passe ne doit apparaître ni dans l'historique du terminal, ni dans un fichier, ni chez un agent.
- **C** : avec des sessions stockées en base, l'identifiant de session est un jeton aléatoire vérifié côté serveur ; l'exigence du CDC (protéger les sessions) est couverte sans clé de signature.
- **D** : exigence du CDC § 9, au coût minimal. Limite de 30 jours : un compte supprimé sur demande (RGPD) ne doit pas survivre indéfiniment dans les sauvegardes ; le risque R-03 est ainsi traité, pas reporté sur le client. Limite appliquée aussi au déploiement : la garantie RGPD ne doit pas dépendre d'une tâche planifiée qui peut ne pas tourner.
- **E** : accepté explicitement comme limite de la démonstration ; une mise en ligne réelle relève d'une nouvelle décision d'hébergement (DEC-003).
- **F** : hors CDC.
- **G** : seuils acceptés provisoirement, à confirmer à l'audit `securite` et à la revue humaine de Karim. Pas de blocage global : il permettrait à un attaquant d'empêcher tous les membres de se connecter (déni de service) ; le blocage par compte suffit.

## Impacts
- Fichiers ou règles à mettre à jour :
  - `projets/reservation-coworking/architecture.md` : v0.2, v0.3 puis v0.4 par l'`architecte`, puis `VALIDÉ` par Ethan (relecture de Karim reportée aux tickets d'authentification) (`valide_par`, `decision: DEC-007`, version 1.0) ;
  - `scripts/prod_locale.py` et `scripts/deployer_local.py` (outillage de C) : commande de sauvegarde seule (rétention 14 jours) et suppression de toute sauvegarde du projet au plus tard 30 jours après sa création, appliquée aussi à chaque déploiement ; `test_retention` adapté (dates relatives au jour du test), tests verts ; par PR relue par C.
- Tickets créés ou débloqués :
  - T-005 débloqué par l'humain (`decision: DEC-007`) ; T-004 (« Architecture ») conclu par le coordinateur une fois l'architecture validée ;
  - au planning (`chef-de-projet`) : ticket de la commande de sauvegarde et de la tâche planifiée (compétence `sauvegarde-restauration`, Nadia ou revue de Nadia) ; décision d'allocation de Karim ; revue humaine des tickets d'authentification par Karim (AF3) ; confirmation des seuils G à l'audit `securite`.
- **Point D, durée maximale dans les sauvegardes** : une donnée supprimée sur demande (compte membre) subsiste au plus 30 jours dans les sauvegardes ; c'est cette durée que mentionne la page de confidentialité (H-21).
- **Point G, supervision** : l'alerte « plus de 30 échecs de connexion en 15 min » est suivie par `analyste-prod` (S2).
- Règles : aucune règle modifiée.
