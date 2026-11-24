---
titre: Production locale Docker et workflows de contrôle (lot 5)
statut: VALIDÉ
responsable: C
version: 1.0
maj_le: 2026-11-24
valide_par: Ethan
decision: DEC-003
id: DEC-003
date: 2026-11-24
decide_par: le professeur (pas de mise en production réelle) ; Ethan (modalités, plan du lot 5)
projet: ESN
ticket:
modifie_une_regle: oui
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-003 — Production locale Docker et workflows de contrôle (lot 5)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision du professeur du 2026-11-24 et du plan du lot 5 validé par Ethan le même jour. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`.

## Contexte
Le 2026-11-24, le professeur a décidé qu'il n'y aurait **pas de mise en production réelle**. La production tourne en local, dans Docker, sur le poste de démonstration. Le système 3 doit tout de même démontrer quatre choses : la sauvegarde, le déploiement, la vérification en ligne (le SHA renvoyé par `/health`) et le rollback.

Le lot 5 devait aussi livrer :
- les workflows, reportés par DEC-002 § 20 et § 30 ;
- les réponses aux questions d'ARCHITECTURE § 10 : délais de vérification, sauvegardes, rollback ;
- `onFailure: "block"` sur les hooks, reporté par DEC-002 § 22.

Un humain a repassé CLAUDE.md, ARCHITECTURE et S3 en `EN_REVUE`. Ethan a validé le plan, ainsi que l'alignement dans cette même décision des fichiers de A et de D qui citaient encore Render ou `deploy.yml`.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| (a) Render réel (plan initial) | vraie mise en ligne | exclu par le professeur ; dépend du réseau et d'un service tiers en soutenance ; rollback par redéploiement, qui prend plusieurs minutes |
| (b) Processus local sans conteneur (`GIT_COMMIT=$(git rev-parse HEAD)` au lancement) | simple | le SHA est déclaré au lancement, pas lié au code qui tourne ; pas de base isolée ; rollback = checkout et relance |
| **(c) Docker local, image étiquetée par SHA (retenue)** | le SHA est figé dans l'image au build ; base Postgres dans un volume ; rollback immédiat par relance de l'image précédente ; tout fonctionne hors ligne | Docker requis sur le poste de démonstration ; images à précharger |

## Décision

### 1. Production locale Docker (S3 portes 5 à 8, ARCHITECTURE § 9)
- **Hébergement par défaut** : la production locale Docker. `projet.md` porte `hebergement: local` et `url_prod: http://localhost:<port>` (8080 par défaut). Un hébergeur distant redevient possible sur décision humaine, mais il faut alors outiller son déploiement.
- **Modèle commun** `deploiement/docker-compose.yml`, avec un projet compose `esn-<slug>` :
  - service `db` : `postgres:16-alpine`, volume nommé, aucun port publié ;
  - service `app` : image `esn-<slug>:<sha40>`, port publié sur `127.0.0.1` seulement.
- **Contrat de l'app** : `projets/<slug>/app/Dockerfile` déclare `ARG GIT_COMMIT` et `ENV GIT_COMMIT=$GIT_COMMIT`. L'app écoute sur `$PORT` et lit `DATABASE_URL`. `/health` renvoie `commit` à partir de `GIT_COMMIT`. Le SHA est figé dans l'image et jamais passé au lancement : une image relancée par un rollback annonce donc son vrai SHA.
- **`scripts/deployer_local.py --projet <slug> --sha <sha>`** enchaîne :
  1. les préconditions ;
  2. une sauvegarde `pg_dump` horodatée ;
  3. le build à partir du commit (`git archive`, jamais l'arbre de travail) ;
  4. le lancement ;
  5. `verifier-prod`.

  Codes de retour : 0 en ligne et à jour ; 1 échec, il faut un rollback ; 2 précondition non remplie, rien n'a changé ; 3 vérification en cours ; 4 sauvegarde en échec ; 5 build en échec, la production est inchangée.
- **`scripts/rollback_local.py --projet <slug> [--sha <sha>]`** relance l'image étiquetée du SHA précédent, sans rebuild ni `git revert`, puis lance `verifier-prod`. Sans `--sha`, il ne prend pour cible que la version précédente d'un déploiement **en échec** (S3-R6). Revenir sur un déploiement vérifié exige `--sha` après une décision humaine (S2-R7). Il ne restaure jamais de données.
- **Tests** : `scripts/test_prod_locale.py`.
  - En simulation, sans Docker : faux Docker et serveur `/health` de test.
  - En réel, si Docker répond : v1, puis v2 avec un vrai dump, puis v3 en panne, puis rollback vers v2.

### 2. Hook et permissions (S3 § 5, ARCHITECTURE § 6, garde-fou 7)
- **Liste blanche du `deployeur`** (`restreindre_bash.py`) : `deployer_local.py`, `rollback_local.py`, `verifier_prod.py`, avec des arguments sûrs, plus `git rev-parse` et `git log` (sans `--output` ni `--ext-diff`). **`gh workflow run` et `gh run` sont retirés.**
- **Confirmation humaine** pour les deux scripts de déploiement : règles `ask` dans `settings.json`, **doublées** d'une décision `ask` renvoyée par le hook pour tout appelant, session principale comprise. Le garde-fou 6 suit le même principe, depuis qu'au test du 2026-11-23 une règle `ask` seule n'a pas déclenché de confirmation.
- Le `gestionnaire-crise` ne peut lancer aucun des deux scripts.

### 3. Workflows de contrôle, sans `deploy.yml`
- `ci.yml` : tous les `scripts/test_*.py`, y compris le test Docker réel.
- `securite.yml` : `pip-audit`, `bandit` et `gitleaks`, sur chaque push et chaque semaine.
- `validations.yml` : `scripts/verifier_validations.py`. Chaque document VALIDÉ doit avoir `valide_par` et un `DEC-NNN` qui existe dans `docs/decisions/`. Tout statut hors `BROUILLON`, `EN_REVUE`, `VALIDÉ` est refusé, et un journal n'est jamais VALIDÉ. La normalisation est importée du hook, pour que les deux ne puissent pas diverger.
- `tableau.yml` : cron quotidien. Il ne commite que s'il y a un changement, avec `[skip ci]` et un groupe `concurrency`. En cas de rejet, il régénère.

### 4. ARCHITECTURE § 10 tranché
- **10.1 Vérification en ligne** : en local, une sonde toutes les **5 s pendant 120 s au plus**. Au timeout, le déploiement est en ÉCHEC, puis vient le rollback (S3-R6). Chaque vérification a **son propre fichier d'état**, `verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json`, jamais réutilisé.
- **10.2 Données et sauvegardes** : Postgres 16 dans un volume nommé. `pg_dump -Fc` avant chaque déploiement, dans `deploiement/local/<slug>/sauvegardes/`, dossier ignoré par Git. Rétention : les **10 dernières** par projet. Une restauration est toujours une décision humaine.
- **10.3 Rollback** : relance de l'image étiquetée du SHA précédent, puis `verifier-prod`. Le test S3-R7 est répété automatiquement (test réel en CI et sur le poste). Il sera tracé dans un rapport sur le projet de démonstration au lot 6, avant la soutenance.

### 5. Alignement des documents
- **B** : CLAUDE.md (points d'arrêt, R5), ARCHITECTURE (§ 2 à § 6, § 9, § 10), S3 (§ 2, § 3, § 4, § 5, § 6, § 7).
- **C** : `deployeur`, skill `verifier-prod`.
- **A** : `dev-backend` (contrat Dockerfile), `architecte` (hébergement local par défaut) ; templates `projet`, `architecture`, `rapport-deploiement`.
- **D** :
  - runbooks `rollback` et `perte-donnees` (dont la procédure de restauration humaine) ;
  - runbook `coupure-serveur`, entièrement transposé : plus de réveil d'offre gratuite ni de tableau de bord Render ; constat de l'humain d'exploitation par `docker compose ps` et `logs` ; options de redémarrage locales ;
  - `gestionnaire-crise` : nom des fichiers d'état ;
  - `analyste-prod`, règle 4 : le Pourquoi des mesures espacées devient le redémarrage d'un conteneur, plus la mise en veille de Render.
- **S2 et S4**, repassés en `EN_REVUE` par Ethan pour cet alignement :
  - S4 § 4 : hébergement par défaut = production locale Docker ;
  - S2 § 6 : constat Docker au lieu du tableau de bord Render ; fichiers d'état horodatés et `rollback_local.py` ; mécanismes de sauvegarde et de rollback tranchés, avec lien vers ARCHITECTURE § 10.
- **Autres** : README, `docs/a-integrer/lot2-C.md` (points 8 et 10).

### 6. `onFailure: "block"` sur les hooks
- **Reporté.** Le poste d'Ethan a Claude Code **2.1.285**, alors que ce champ exige la 2.1.295 ou plus, et un champ inconnu risquerait d'invalider tout `settings.json`. Les parades restent en place : commande `python` puis `python3`, hooks qui refusent en cas d'erreur, procédure du README. Le filet CI `validations.yml` est désormais livré. On ajoutera le champ, par une PR, dès que tous les postes de l'équipe auront la 2.1.295 ou plus.

## Pourquoi
- **Décision du professeur** : pas de mise en production réelle. La preuve demandée par la consigne (« un push ne suffit pas ») reste la même : `/health` doit renvoyer le SHA attendu.
- **Rollback immédiat par image étiquetée** : l'image du SHA précédent existe déjà, et la relancer prend quelques secondes, sans rebuild ni `git revert`. Comme le SHA est figé dans l'image, `/health` ne peut pas mentir sur la version restaurée.
- **Aucune dépendance réseau en soutenance** : tout tourne sur le poste de démonstration, une fois les images de base préchargées. Une panne du réseau ou d'un hébergeur gratuit ne peut pas faire échouer la démonstration.

## Impacts
- **Règles modifiées** :
  - CLAUDE.md : point d'arrêt hébergeur ; Pourquoi de R5 ;
  - S4 § 4 : hébergement par défaut ; S2 § 6 : runbooks, sauvegardes et rollback ;
  - S3 : portes 5, 6 et 8 ; Pourquoi de S3-R3, S3-R5 et S3-R8 ; § 5, § 6 et § 7 ;
  - ARCHITECTURE : § 9 et § 10, garde-fous 4 et 7 ;
  - agents : règles 2, 4, 6, 7 et 8 du `deployeur` ; règle 6 de `dev-backend` ; règles 3, 5 et 7 d'`architecte` ;
  - le fichier d'état de `verifier-prod` est désormais horodaté.
- **Fichiers créés** :
  - `deploiement/docker-compose.yml`, `.gitignore` ;
  - `scripts/prod_locale.py`, `deployer_local.py`, `rollback_local.py`, `verifier_validations.py`, `test_prod_locale.py`, `test_verifier_validations.py`, `scripts/fixtures/` ;
  - `.github/workflows/ci.yml`, `securite.yml`, `validations.yml`, `tableau.yml`.
- **Fichiers modifiés** :
  - `.claude/hooks/restreindre_bash.py`, `.claude/settings.json`, `scripts/test_restreindre_bash.py` ;
  - les documents de la section 5.
- **Reports** : `onFailure: "block"` (version de Claude Code) ; rapport du test de rollback sur le projet de démonstration (lot 6) ; tests des apps clientes dans `ci.yml` (lot 6).
- **Avant la soutenance** : précharger `postgres:16-alpine` et l'image de base de l'app sur le poste de démonstration (README, « Installer son poste »).
- **Tickets** : aucun.
