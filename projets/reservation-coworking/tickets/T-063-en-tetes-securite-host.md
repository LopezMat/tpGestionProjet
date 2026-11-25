---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-063
titre: En-têtes de sécurité et contrôle de l'en-tête Host (constats 2 et 4)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 1            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-063 — En-têtes de sécurité et contrôle de l'en-tête Host (constats 2 et 4)

## Description
Constats 2 et 4 (bas) des rapports `securite` du 2026-11-25 (repris dans [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md)), toujours ouverts. `app/reservation/app.py` n'envoie ni CSP, ni `nosniff`, ni `Referrer-Policy`, ni `frame-ancestors` (constat 2), et ne valide pas l'en-tête `Host` : une page malveillante ouverte sur le poste pourrait lire les disponibilités de [T-054](T-054-api-consultation-disponibilites.md) par DNS rebinding sur `127.0.0.1` (constat 4). Recommandation du `securite` : à faire avant ou avec T-055, au plus tard avec T-054.

Les en-têtes étaient prévus dans T-013 (critère « Toutes les réponses portent la CSP… »), mais T-054 et T-055 publient des données avant T-013 (DEC-011). Ce ticket les pose dès l'incrément ; T-013 vérifie seulement qu'ils restent présents sur ses routes. **À réaliser dans l'incrément, juste après T-054** ; T-055 n'en dépend pas, pour ne pas bloquer la page de la soutenance, mais elle doit être compatible avec cette CSP (critère ajouté à T-055).

**Touche la sécurité** : revue humaine obligatoire, ticket compagnon **T-064** (Karim).

## Critères d'acceptation
- [ ] Toutes les réponses (page statique, `/api/*`, `/health`, une 404) portent la CSP de l'[architecture](../architecture.md) § 6 (`default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'`), `X-Content-Type-Options: nosniff` et `Referrer-Policy: no-referrer` (test sur ces 4 types de réponse).
- [ ] Une requête dont l'en-tête `Host` n'est pas `localhost` ni `127.0.0.1` (avec ou sans port) est refusée (400) ; ces deux hôtes sont acceptés (tests). La liste est fixée dans le code : aucune nouvelle variable d'environnement obligatoire (critère de T-010).
- [ ] `/health` reste joignable par `http://localhost:<port>` pour `verifier-prod` et `deployer_local.py` (test).
- [ ] La page actuelle (`static/index.html`) s'affiche sans erreur CSP dans la console du navigateur (vérification notée au journal).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (en-têtes de sécurité et contrôle d'accès par l'hôte, S3-R2 ; ticket compagnon T-064)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage des constats 2 et 4) · 0 h
- 2026-11-25 23:05 · agent:dev-backend · prise en charge (dépendance T-010 TERMINE, architecture et CDC VALIDÉS) · 0 h
- 2026-11-25 23:40 · agent:dev-backend · livré pour revue. **Touche la sécurité** (en-têtes, contrôle d'accès par l'hôte) : revue humaine T-064. Fichiers : `app/reservation/app.py` (middleware ASGI `EnTetesSecurite`, `TrustedHostMiddleware`, constantes `HOTES_AUTORISES` et `EN_TETES_SECURITE`), nouveau `app/tests/test_en_tetes_hote.py`. Fichiers partagés touchés (minimal) : `tests/conftest.py`, `test_api_consultation.py`, `test_base.py`, `test_health.py`, `test_health_delai.py`, `test_livraison.py` : les `TestClient` passent en `base_url="http://localhost"` (le Host par défaut `testserver` est désormais refusé). Pas de nouvelle variable d'environnement ni de dépendance (`env.example` et README inchangés). Liste d'hôtes retenue : `localhost` et `127.0.0.1`, port ignoré, fixée dans le code, indépendante de la requête. Compatibilité : `verifier-prod`/`sonde_sante` et `deployer_local.py` appellent `http://localhost:<port>/health` (url_prod), l'aperçu local utilise 127.0.0.1:8090, le modèle `deploiement/docker-compose.yml` n'a pas de sonde sur l'app (seule la base a un healthcheck `pg_isready`). Limite : `::1` / `[::1]` est refusé (verifier-prod tolère `::1` dans url_prod, mais deployer_local exige localhost). Les en-têtes enveloppent le contrôle d'hôte : la 400 les porte aussi ; une 500 interne produite par le serveur n'en porte pas. Tests : suite complète sous python:3.14-slim avec PostgreSQL 16 jetable (`TEST_DATABASE_URL=…/t063_test`), `python -m pytest -q` : 183 passed. Couverture des critères : 1 -> `test_en_tetes_de_securite_sur_chaque_type_de_reponse` (/, /api/salles, /health, 404) ; 2 -> `test_hotes_acceptes`, `test_hote_etranger_refuse_400_avec_en_tetes`, `test_x_forwarded_host_ne_change_pas_le_controle` ; 3 -> `test_health_joignable_comme_les_sondes` ; 4 -> `test_page_statique_sans_script_ni_style_en_ligne` (aucun script ni style en ligne dans index.html). Aucune vérification en navigateur réel n'a été faite (pas de navigateur dans l'environnement) : à confirmer à la revue T-064. Conteneurs, réseau d'essai supprimés. Rien commité. · 1 h
