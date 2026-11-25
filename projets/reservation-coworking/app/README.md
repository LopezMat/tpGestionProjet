# App de réservation de salles - Coworking Les Arcades

Application FastAPI (Python 3.14) qui sert une API JSON et le front statique, sur PostgreSQL 16.
Référence : `../architecture.md` (v1.1). État après T-010 : socle seulement (`/health`, démarrage, image) ; pas encore de modèle de données ni d'authentification.

## Structure

| Chemin | Rôle |
|---|---|
| `reservation/app.py` | application FastAPI, `/health`, fichiers statiques |
| `reservation/config.py` | variables d'environnement (`PORT`, `DATABASE_URL`, `GIT_COMMIT`) |
| `reservation/bdd.py` | moteur de la sonde `SELECT 1` (`_moteur_sonde`) et moteur applicatif à pool (`moteur_applicatif`) |
| `reservation/migrer.py`, `reservation/migrations/` | migrations Alembic (schéma, 3 salles) appliquées au démarrage, de façon tolérante (T-011) |
| `reservation/demarrer.py` | point d'entrée de l'image : attend la base, migre, lance Uvicorn (1 worker) |
| `reservation/static/` | front HTML/CSS/JS sans build |
| `docs/openapi.json` | schéma OpenAPI versionné pour le `dev-frontend` |
| `tests/` | tests pytest |
| `env.example` | variables d'environnement, sans valeur |

## Variables d'environnement

`PORT` (8000 par défaut) et `DATABASE_URL` (`postgresql://utilisateur:mot_de_passe@hote:5432/base`) suffisent au lancement. `GIT_COMMIT` n'est pas une variable de lancement : c'est un argument de build, figé dans l'image. Voir `env.example`.

## Tests

```
python -m venv .venv
.venv/Scripts/activate          # Linux/macOS : source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest
```

Les tests qui exigent un vrai PostgreSQL sont ignorés tant que `TEST_DATABASE_URL` n'est pas renseignée :

```
docker run --rm -d --name pg-test -e POSTGRES_PASSWORD=test -e POSTGRES_USER=esn -e POSTGRES_DB=coworking_test -p 127.0.0.1:55432:5432 postgres:16-alpine
set TEST_DATABASE_URL=postgresql://esn:test@127.0.0.1:55432/coworking_test     # PowerShell : $env:TEST_DATABASE_URL = "..."
python -m pytest
```

**Nommer la base de test.** Les fixtures d'intégration vident la base (`DROP SCHEMA public CASCADE` dans `test_migrations.py`) : une garde (`tests/garde_base.py`) refuse, avant toute connexion, une base dont le nom ne se termine pas par `_test` (`app`, `contest`… sont refusées) ou dont l'hôte n'est pas `localhost`, `127.0.0.1` ou `::1`. Pour lancer les tests dans un conteneur relié à la base par un réseau Docker, déclarer le nom du conteneur de base jetable : `TEST_DATABASE_HOTES_JETABLES=pg-test` (noms séparés par des virgules). Ne jamais y mettre l'hôte d'une base d'aperçu ou de production.

Après une modification de l'API, régénérer le schéma versionné : `REGENERER_OPENAPI=1 python -m pytest tests/test_livraison.py` (PowerShell : `$env:REGENERER_OPENAPI = "1"`).

## Construire et lancer en local

Avec la base et l'app du modèle commun (DEC-003), depuis la racine du dépôt, par `scripts/deployer_local.py` (build au SHA du GO, sauvegarde, vérification). Pour un essai à la main :

```
cd projets/reservation-coworking/app
docker build --build-arg GIT_COMMIT=$(git rev-parse HEAD) -t esn-reservation-coworking:essai .
docker network create essai-reservation
docker run -d --name essai-db --network essai-reservation -e POSTGRES_USER=esn -e POSTGRES_DB=app -e POSTGRES_PASSWORD=essai postgres:16-alpine
docker run -d --name essai-app --network essai-reservation -e PORT=8000 -e DATABASE_URL=postgresql://esn:essai@essai-db:5432/app -p 127.0.0.1:8080:8000 esn-reservation-coworking:essai
curl http://127.0.0.1:8080/health        # {"status":"ok","commit":"<sha>"}
```

Nettoyage : `docker rm -f essai-app essai-db ; docker network rm essai-reservation`. Le mot de passe `essai` est jetable ; ne jamais réutiliser un vrai secret dans ces commandes.

Sans Docker, avec un PostgreSQL local : `DATABASE_URL=postgresql://... python -m reservation.demarrer`.
