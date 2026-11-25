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
maj_le: 2026-11-25
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
- [ ] Une exception non interceptée dans une route (route de test qui lève `RuntimeError`, ajoutée seulement dans le test) donne une 500 qui porte la CSP de l'architecture § 6, `X-Content-Type-Options: nosniff` et `Referrer-Policy: no-referrer`, chacun en un seul exemplaire ; le corps ne contient pas le message de l'exception (test sur l'objet application servi par Uvicorn).
- [ ] Les réponses déjà couvertes par T-063 (200, 404, 422, 400 d'hôte refusé, 503) portent toujours ces en-têtes, une seule fois chacun, et le contrôle d'hôte reste appliqué avant toute route (tests existants verts, sans modification de leurs assertions).
- [ ] La limite des 400 émises par Uvicorn hors application est notée en commentaire dans `app/reservation/app.py`, avec renvoi au constat 16.
- [ ] `demarrer.py` n'est pas modifié ; aucune nouvelle variable d'environnement ni dépendance ; suite complète verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (en-têtes de sécurité, S3-R2 ; ticket compagnon T-074)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 16:40 · agent:chef-de-projet · création (triage du constat 16 du rapport securite-2026-11-25-5 et de la remarque 3 du relecteur sur T-063) ; T-013 en dépend ; pas de dépendance vers T-063 (revue humaine commune T-064 et T-074) ; revue dans T-066, revue humaine T-074. Temps compté dans T-008 · 0 h
- 2026-11-25 17:05 · agent:dev-backend · prise en charge (T-010 TERMINE, architecture et CDC VALIDÉS) · 0 h
- 2026-11-25 17:20 · agent:dev-backend · choix : gestionnaire d'`Exception` (`gerer_erreur_interne`, app.py) plutôt qu'envelopper l'application entière. Raisons : `ServerErrorMiddleware` ne sert qu'une 500 à corps fixe ; le gestionnaire pose les trois en-têtes depuis `EN_TETES_SECURITE` (source unique), une seule fois (la réponse ne repasse pas par `EnTetesSecurite`) ; `app` reste un `FastAPI` (`dependency_overrides`, `creer_app()` des tests, `reservation.app:app` d'Uvicorn et `demarrer.py` inchangés, aucune assertion existante modifiée). Corps fixe « Internal Server Error », sans message ni trace ; Starlette relance ensuite l'exception, la trace reste donc dans le journal serveur. Limite des 400 d'Uvicorn (Host dupliqué, HTTP/1.1 sans Host) notée dans la docstring du gestionnaire, avec renvoi au constat 16 · 0 h
- 2026-11-25 17:35 · agent:dev-backend · tests ajoutés dans tests/test_en_tetes_hote.py : `test_500_porte_les_en_tetes_une_seule_fois_sans_detail` (route d'essai qui lève RuntimeError, montée seulement dans le test, avant le montage statique) et `test_en_tetes_une_seule_fois_sur_200_404_400_503`. Commande : Docker, python:3.14-slim + PostgreSQL 16 jetable (base `t073_test`, `TEST_DATABASE_HOTES_JETABLES=t073-db`), `python -m pytest -q` : 216 passed ; conteneurs et réseau d'essai supprimés · 0 h
- 2026-11-25 17:40 · agent:dev-backend · touche la sécurité (en-têtes de sécurité) : revue humaine T-074. Livré pour revue. Fichiers : app/reservation/app.py, app/tests/test_en_tetes_hote.py (non commités, sur demande du coordinateur). Couverture (critères non cochés) : 1 → test_500_porte_les_en_tetes… ; 2 → test_en_tetes_une_seule_fois_sur_200_404_400_503 + tests existants inchangés (404, 400 hôte, 503, 422 via l'API) ; 3 → commentaire de gerer_erreur_interne ; 4 → demarrer.py non touché, aucune dépendance ni variable, suite verte (216) · 0.5 h
