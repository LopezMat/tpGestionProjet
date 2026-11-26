---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-073
titre: En-têtes de sécurité sur la 500 interne (constat 16)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5          # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-26
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-073 — En-têtes de sécurité sur la 500 interne (constat 16)

## Description
Constat 16 (bas, A05) du rapport [securite-2026-11-25-5.md](../rapports/securite-2026-11-25-5.md), qui recoupe la remarque 3 du `relecteur-code` sur [T-063](T-063-en-tetes-securite-host.md). Le middleware `EnTetesSecurite` de T-063 (`app/reservation/app.py`) est placé sous `ServerErrorMiddleware` de Starlette : une exception non interceptée produit une 500 `text/plain` « Internal Server Error » **sans** CSP, `nosniff` ni `Referrer-Policy`. Le corps est fixe et ne divulgue rien, mais c'est un écart à « toutes les réponses » de l'[architecture](../architecture.md) § 6. Un `TypeError` de `regles` (instant naïf, voir T-062) mènerait à ce cas.

Pistes du `securite` et du relecteur, au choix du `dev-backend` (choix noté au journal) : envelopper l'application **entière** dans `EnTetesSecurite` (par exemple `app = EnTetesSecurite(creer_app())` au niveau du module, en retirant `add_middleware(EnTetesSecurite)`), ou poser les en-têtes dans le gestionnaire d'`Exception` passé à `ServerErrorMiddleware`. Le choix doit garder les tests existants fonctionnels (`dependency_overrides`, `TestClient` sur l'objet effectivement servi par Uvicorn).

**Hors périmètre, limite acceptée** : les 400 « Invalid HTTP request received. » émises par Uvicorn lui-même (Host dupliqué, HTTP/1.1 sans Host) ne passent pas par l'application et ne peuvent pas porter ces en-têtes sans proxy devant Uvicorn. La requête est refusée, le corps est un texte fixe sans HTML : c'est acceptable (avis du `securite`, rapport `-5`, essais du contrôle d'hôte). La limite est notée en commentaire dans `app.py` et confirmée à la revue humaine T-074.

**Ordre.** Se fait sur le code de T-063 tel que commité (`b8b0004`, relu `APPROUVÉ`, en attente de la revue humaine T-064) ; pas de `depend_de` vers T-063, pour que Karim puisse revoir T-063 (T-064) et ce ticket (T-074) **dans la même séance** au lieu de deux passages successifs sur le chemin critique. Si la revue T-064 demande une reprise de `EnTetesSecurite`, la reprise est faite dans T-063 et ce ticket est rebasé dessus (noté au journal). **À terminer avant T-013** (premières routes qui manipulent des données de membre ; recommandation du `securite`) : T-013 en dépend. Ne pas modifier `demarrer.py` (T-071 en cours) ; si le point d'entrée d'Uvicorn devait changer, ou si T-071 touche aussi `app.py`, le signaler au journal et attendre T-071.

**Touche la sécurité** (en-têtes de sécurité) : revue humaine obligatoire, ticket compagnon **T-074** (Karim).

## Critères d'acceptation
- [x] Une exception non interceptée dans une route (route de test qui lève `RuntimeError`, ajoutée seulement dans le test) donne une 500 qui porte la CSP de l'architecture § 6, `X-Content-Type-Options: nosniff` et `Referrer-Policy: no-referrer`, chacun en un seul exemplaire ; le corps ne contient pas le message de l'exception (test sur l'objet application servi par Uvicorn).
- [x] Les réponses déjà couvertes par T-063 (200, 404, 422, 400 d'hôte refusé, 503) portent toujours ces en-têtes, une seule fois chacun, et le contrôle d'hôte reste appliqué avant toute route (tests existants verts, sans modification de leurs assertions).
- [x] La limite des 400 émises par Uvicorn hors application est notée en commentaire dans `app/reservation/app.py`, avec renvoi au constat 16.
- [x] `demarrer.py` n'est pas modifié ; aucune nouvelle variable d'environnement ni dépendance ; suite complète verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25)
- **Commentaires** : (passe 1, aucun point bloquant ; grille examinée : architecture § 6, lisibilité, duplication, erreurs, tests, sécurité de base, commit, périmètre)
  1. Remarque, `app.py:60-77` : choix du gestionnaire d'`Exception` conforme à l'une des deux pistes du ticket. Il est enregistré au niveau de `ServerErrorMiddleware`, `app` reste un `FastAPI` (`dependency_overrides`, `reservation.app:app`, `demarrer.py` inchangés). Les trois en-têtes viennent de `EN_TETES_SECURITE` (source unique, pas de copie) et la réponse ne repasse pas par `EnTetesSecurite`, donc un seul exemplaire (test à l'appui).
  2. Remarque, `app.py:73-77` : corps fixe « Internal Server Error », sans message ni trace. Starlette relance l'exception après l'envoi, donc la trace reste dans le journal serveur. Les paramètres `_requete` et `_exc` sont inutilisés et nommés en conséquence : correct. Limite : si la réponse a déjà démarré, Starlette n'envoie pas de 500 et le gestionnaire n'est pas appelé, ce qui est sans effet sur les en-têtes (déjà posés par `EnTetesSecurite`).
  3. Remarque, `app.py:68-71` : la limite des 400 d'Uvicorn est notée avec renvoi au constat 16 (critère 3). Elle est dans la docstring et non dans un commentaire `#` : équivalent, sans écart.
  4. Remarque, `tests/test_en_tetes_hote.py:76-92` : la route d'essai n'existe que dans le test et est insérée en position 0, avant le montage statique « / » (nécessaire, vu le commentaire). `raise_server_exceptions=False` est adapté. Écart déclaré (test sur `creer_app()` et non sur l'objet `app` du module) : acceptable, `app = creer_app()` n'ajoute rien (`app.py:132`). Pas de modification d'assertions existantes ; le 422 reste couvert par les tests existants de l'API.
  5. Remarque sans effet sur l'avis : le journal du ticket dit « non commités » alors que le commit `748c75e` existe. Le commit ne touche que `app/reservation/app.py`, `app/tests/test_en_tetes_hote.py` et le ticket, préfixe `T-073` correct. `demarrer.py`, dépendances et variables d'environnement non touchés. La suite verte (216) est annoncée au journal par l'auteur ; je ne l'ai pas rejouée, c'est le rôle du `testeur`.
  6. Pas de régression visible sur T-063 : l'ordre des middlewares (`TrustedHost` sous `EnTetesSecurite`) est inchangé et le test 200/404/400/503 vérifie un seul exemplaire de chaque en-tête.
- **Revue humaine requise** : oui (en-têtes de sécurité, S3-R2 ; ticket compagnon T-074)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 16:40 · agent:chef-de-projet · création (triage du constat 16 du rapport securite-2026-11-25-5 et de la remarque 3 du relecteur sur T-063) ; T-013 en dépend ; pas de dépendance vers T-063 (revue humaine commune T-064 et T-074) ; revue dans T-066, revue humaine T-074. Temps compté dans T-008 · 0 h
- 2026-11-25 17:05 · agent:dev-backend · prise en charge (T-010 TERMINE, architecture et CDC VALIDÉS) · 0 h
- 2026-11-25 17:20 · agent:dev-backend · choix : gestionnaire d'`Exception` (`gerer_erreur_interne`, app.py) plutôt qu'envelopper l'application entière. Raisons : `ServerErrorMiddleware` ne sert qu'une 500 à corps fixe ; le gestionnaire pose les trois en-têtes depuis `EN_TETES_SECURITE` (source unique), une seule fois (la réponse ne repasse pas par `EnTetesSecurite`) ; `app` reste un `FastAPI` (`dependency_overrides`, `creer_app()` des tests, `reservation.app:app` d'Uvicorn et `demarrer.py` inchangés, aucune assertion existante modifiée). Corps fixe « Internal Server Error », sans message ni trace ; Starlette relance ensuite l'exception, la trace reste donc dans le journal serveur. Limite des 400 d'Uvicorn (Host dupliqué, HTTP/1.1 sans Host) notée dans la docstring du gestionnaire, avec renvoi au constat 16 · 0 h
- 2026-11-25 17:35 · agent:dev-backend · tests ajoutés dans tests/test_en_tetes_hote.py : `test_500_porte_les_en_tetes_une_seule_fois_sans_detail` (route d'essai qui lève RuntimeError, montée seulement dans le test, avant le montage statique) et `test_en_tetes_une_seule_fois_sur_200_404_400_503`. Commande : Docker, python:3.14-slim + PostgreSQL 16 jetable (base `t073_test`, `TEST_DATABASE_HOTES_JETABLES=t073-db`), `python -m pytest -q` : 216 passed ; conteneurs et réseau d'essai supprimés · 0 h
- 2026-11-25 17:40 · agent:dev-backend · touche la sécurité (en-têtes de sécurité) : revue humaine T-074. Livré pour revue. Fichiers : app/reservation/app.py, app/tests/test_en_tetes_hote.py (non commités, sur demande du coordinateur). Couverture (critères non cochés) : 1 → test_500_porte_les_en_tetes… ; 2 → test_en_tetes_une_seule_fois_sur_200_404_400_503 + tests existants inchangés (404, 400 hôte, 503, 422 via l'API) ; 3 → commentaire de gerer_erreur_interne ; 4 → demarrer.py non touché, aucune dépendance ni variable, suite verte (216) · 0.5 h
- 2026-11-25 16:30 · agent:testeur · vérifié sur le SHA 748c75e3a2b458d144f63d1327e7bcd83255f31c (git archive, copie en lecture seule ; python:3.14-slim 3.14.10 + postgres:16 jetable) : suite complète 216 passés, 0 ignoré, 0 échec. Critère 1 : `test_500_porte_les_en_tetes_une_seule_fois_sans_detail` rejoué (passé) : 500 avec CSP (architecture § 6), nosniff et no-referrer, un exemplaire chacun, corps fixe « Internal Server Error » sans le message de `RuntimeError` ; contrôle sur instance Uvicorn réelle (app importée de `reservation.app`, route d'essai qui lève, serveur lancé avec `server_header=False`) : `/boom` → 500, les trois en-têtes présents, corps `Internal Server Error`, aucun détail. Critère 2 : `test_en_tetes_une_seule_fois_sur_200_404_400_503` rejoué (passé) ; `git diff 9114f9e 748c75e` sur les tests : aucune ligne supprimée ni modifiée (45 ajouts), donc assertions existantes inchangées et vertes ; sur l'instance réelle : 422 (`/api/disponibilites?date=x`), 404 (`/inconnu`, `/api/nope`) et 400 (`Host: evil.example`, « Invalid host header ») portent les trois en-têtes. Critère 3 : limite des 400 d'Uvicorn avec renvoi au constat 16 présente dans la docstring de `gerer_erreur_interne` (app.py), jugée équivalente à un commentaire par le relecteur. Critère 4 : `git diff` : seuls app.py et test_en_tetes_hote.py changent ; `demarrer.py`, dépendances et variables d'environnement non touchés ; suite verte. Reste `EN_REVUE` : 4/4 critères cochés, avis APPROUVÉ, suites vertes ; il ne manque que la ligne « Revue humaine » (T-074, Karim), requise (sécurité) · 0.3 h (temps compté dans T-067)
- 2026-11-25 16:15 · agent:securite · audit sécurité : NON BLOQUANT, rapport [securite-2026-11-25-6.md](../rapports/securite-2026-11-25-6.md) (SHA `748c75e3a2b458d144f63d1327e7bcd83255f31c`). Constat 16 fermé, à l'exception acceptée des 400 émises par Uvicorn : 500 provoquées par des routes d'essai dans une copie jetable hors dépôt, CSP, `nosniff` et `Referrer-Policy` une seule fois, corps fixe sans message ni trace, trace dans le journal serveur sans donnée d'entrée ; pas de régression sur 200, 404, 422. Revue humaine T-074 toujours requise. Aucun ticket `bug`. Statut et critères inchangés. Temps compté dans T-043 · 0 h
- 2026-11-26 10:25 · agent:testeur · campagne 7, SHA 011ac347bd3674518d9592347125cd948580669b (code de app/ identique à 748c75e) : non-régression, 4/4 critères maintenus (suite complète 216 passés, 0 ignoré, 0 échec, dont les tests de la 500 avec les 3 en-têtes une seule fois ; sur l'image : 3 en-têtes relevés sur `/`, `Host: evil.example` donne 400 ; la 500 n'est vérifiée que par les tests, la vérification sur instance Uvicorn date de la campagne 6). **Reste EN_REVUE : il manque la revue humaine** (ligne « Revue humaine » vide, T-074 A_FAIRE, Karim), R13 · temps compté dans T-067
