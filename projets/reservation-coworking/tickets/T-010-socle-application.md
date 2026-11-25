---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-010
titre: Socle de l'application (/health, Dockerfile, démarrage)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-010 — Socle de l'application (/health, Dockerfile, démarrage)

## Description
Premier ticket de réalisation, socle de toutes les exigences (F-01 à F-08). Selon [architecture.md](../architecture.md) § 2, § 3, § 5 et § 8 (contrat de l'image, DEC-003, ARCHITECTURE § 9) : paquet `reservation` dans `projets/reservation-coworking/app/`, application FastAPI qui sert aussi les fichiers statiques du front, configuration (`PORT`, `DATABASE_URL` converti pour psycopg 3), `/health`, `Dockerfile`, point d'entrée `reservation.demarrer` (attente de la base, lancement d'Uvicorn avec 1 worker ; les migrations sont ajoutées par T-011), `app/env.example`, `requirements.txt` et `requirements-dev.txt`, README de l'app.

Les versions exactes sont confirmées au premier ticket par `pip index versions <paquet>` (architecture § 2, écart de confiance sur FastAPI, Uvicorn, Playwright) et notées au journal.

## Critères d'acceptation
- [ ] `GET /health` renvoie 200 `{"status": "ok", "commit": "<sha>"}` quand la base répond à `SELECT 1` (délai 1 s), et 503 `{"status": "ko", "commit": "<sha>"}` sinon ; `commit` vaut `GIT_COMMIT`, à défaut `RENDER_GIT_COMMIT`, à défaut `"inconnu"` (tests).
- [ ] `/health` est public, sans session, et ne renvoie aucune autre information.
- [ ] `app/Dockerfile` : base `python:3.14-slim`, `ARG GIT_COMMIT` puis `ENV GIT_COMMIT=$GIT_COMMIT`, installation de `requirements.txt` seul, utilisateur non root, commande `python -m reservation.demarrer` ; une image construite avec `--build-arg GIT_COMMIT=<sha>` renvoie ce SHA sur `/health`.
- [ ] L'app écoute sur `$PORT` et lit sa base dans `DATABASE_URL` ; aucune autre variable n'est exigée au lancement ; Uvicorn tourne avec 1 worker.
- [ ] `requirements.txt` est épinglé (`==`) sur les lignes de version de l'architecture § 2 ; pytest, httpx et Playwright sont dans `requirements-dev.txt` seulement, absents de l'image.
- [ ] `/docs`, `/redoc` et `/openapi.json` ne sont pas servis en production (404) ; le schéma OpenAPI est généré par un test et versionné pour le `dev-frontend`.
- [ ] `app/env.example` (sans point initial) liste `PORT`, `DATABASE_URL`, `ACCUEIL_EMAIL`, `ACCUEIL_MOT_DE_PASSE_INITIAL` sans aucune valeur et rappelle que `GIT_COMMIT` est un argument de build.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
