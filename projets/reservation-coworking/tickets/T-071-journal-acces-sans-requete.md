---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-071
titre: Journal d'accès sans chaîne de requête (constat 15)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE           # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25                 # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-25     # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-071 — Journal d'accès sans chaîne de requête (constat 15)

## Description
Constat 15 (bas, A09 Journalisation) du rapport [securite-2026-11-25-4.md](../rapports/securite-2026-11-25-4.md), partie (a), propre à l'app : le journal d'accès par défaut d'Uvicorn (`app/reservation/demarrer.py`, `uvicorn.run`) recopie la chaîne de requête brute et sans limite. Constaté par l'auditeur : une valeur de 9 000 caractères envoyée dans `date` est écrite en entier, deux fois, dans le journal du conteneur (environ 16 Ko par requête sur une route anonyme). Aujourd'hui la seule valeur reçue est une date ; mais toute route future qui passerait une donnée personnelle dans l'URL l'écrirait dans les journaux, contre le CDC § 8 « Journaux techniques ».

Attendu : un journal d'accès qui n'écrit que la méthode, le chemin (sans chaîne de requête) et le statut, par une configuration de journalisation d'Uvicorn, ou `access_log=False` avec un journal d'accès minimal propre à l'app (choix noté au journal).

Hors de ce ticket :
- partie (b), rotation des journaux dans le modèle commun `deploiement/docker-compose.yml` (outillage commun, responsable C) : [T-072](T-072-rotation-journaux-modele-commun.md) (Nadia) ;
- partie (c), règle « aucune donnée personnelle ni aucun secret dans l'URL » : critère ajouté à [T-013](T-013-authentification-sessions-roles.md) le 2026-11-25, à respecter par les tickets suivants (T-014 à T-019).

Hors de l'incrément de la soutenance du 2026-11-27 : ne retarde ni T-054 ni T-055. Revue de code dans T-066, vérification dans T-067. **Revue humaine non requise** : configuration du format d'un journal, sans authentification, sans droit ni donnée personnelle manipulée (même traitement que T-061 et T-062 pour des constats bas).

## Critères d'acceptation
- [x] Une requête `GET /api/disponibilites?date=<valeur de 9 000 caractères>` produit dans le journal du conteneur une seule ligne d'accès, qui contient la méthode, le chemin `/api/disponibilites` et le statut (422), et ne contient ni `?`, ni `date=`, ni la valeur envoyée (constat sur une instance jetable, noté au journal).
- [x] Un test automatisé vérifie que la configuration de journalisation transmise à Uvicorn n'écrit pas la chaîne de requête (journal capturé, ou format de journal sans `%(request_line)s` ni chemin complet avec requête).
- [x] Les requêtes nominales (`/`, `/health`, `/api/salles`) apparaissent toujours dans le journal d'accès avec leur statut.
- [x] Suite complète verte ; `/health` et les réponses de l'API inchangés.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25)
- **Commentaires** : aucun point bloquant. Grille examinée : architecture (1 worker et `server_header=False` conservés, § 8), lisibilité, duplication, erreurs, tests, sécurité de base, commits, périmètre (commit 9114f9e : `app/` et ce ticket uniquement). Remarques, sans effet sur l'avis :
  1. `journaux.py:30` : `str(methode)[:16]` borne la méthode mais ne neutralise pas les caractères non imprimables, contrairement au chemin. Uvicorn n'accepte qu'une méthode HTTP valide (jeton), donc risque très faible ; passer la méthode par la même neutralisation serait cohérent.
  2. `journaux.py` : `logging.Formatter.format()` appelle `record.getMessage()` avant `formatMessage`. Si une future version d'Uvicorn changeait le nombre d'arguments sans changer le gabarit, l'erreur surviendrait hors du `try`, et `logging.handleError` écrirait le gabarit et les arguments (donc la requête) sur stderr. La forme actuelle d'Uvicorn est cohérente, donc non bloquant. Redéfinir `format()` plutôt que `formatMessage()` fermerait ce cas.
  3. `test_journal_acces.py`, dernière assertion : `assert not appels["kw"].get("access_log") is False` se lit mal ; préférer `appels["kw"].get("access_log", True) is not False`.
  4. Les deux formats sont cohérents (même `FORMAT_GENERAL` pour `uvicorn`, `uvicorn.error` par propagation, et `uvicorn.access`). Le préfixe coloré d'Uvicorn disparaît : voulu. Aucune URL de base ni donnée d'entrée dans les journaux relus (`demarrer.py` ne journalise aucun détail de connexion). Le constat sur image (critère 1) est noté au journal du développeur ; les critères restent à vérifier par le `testeur` (T-067).
- **Revue humaine requise** : non (format du journal d'accès ; aucune authentification ni donnée personnelle manipulée)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 14:45 · agent:chef-de-projet · création (triage du constat 15, partie a, rapport securite-2026-11-25-4) · 0 h
- 2026-11-25 15:05 · agent:dev-backend · prise en charge · 0 h
- 2026-11-25 15:10 · agent:dev-backend · livré pour revue. Choix : configuration `log_config` d'Uvicorn (access_log reste actif) avec un formateur propre `FormatAcces` (app/reservation/journaux.py) ; ligne d'accès = `<date> INFO uvicorn.access GET /chemin 200` (méthode, chemin sans `?` ni fragment borné à 200 caractères avec caractères de contrôle remplacés, statut). Adresse du client, version HTTP et requête ne sont plus écrites ; forme d'arguments inattendue : message générique, rien recopié. Uvicorn : 1 worker et server_header=False inchangés. Fichiers : app/reservation/journaux.py (nouveau), app/reservation/demarrer.py (log_config), app/tests/test_journal_acces.py (nouveau). Tests : conteneur python:3.14-slim + postgres:16 jetable (base coworking_test, TEST_DATABASE_HOTES_JETABLES pour l'hôte du conteneur), `python -m pytest -q` : 214 passed. Constat sur l'image construite avec --build-arg GIT_COMMIT=$(git rev-parse HEAD) : GET /, /health, /api/salles puis /api/disponibilites?date=<9000 caractères> (422) donnent 4 lignes `uvicorn.access` (`GET / 200`, `GET /health 200`, `GET /api/salles 200`, `GET /api/disponibilites 422`) ; journal complet du conteneur 1077 octets, 0 occurrence de `?`, `date=` ou de la valeur. Couverture des critères : 1 = constat image ci-dessus + test_la_chaine_de_requete_n_est_pas_ecrite ; 2 = test_la_configuration_est_valide_et_capte_uvicorn_access et test_main_transmet_la_configuration_a_uvicorn ; 3 = test_requetes_nominales_journalisees + constat image ; 4 = suite complète verte, aucun changement de /health ni de l'API. Ne touche pas la sécurité au sens authentification/droits/données personnelles (journalisation seulement, réduit l'exposition des données). Critères non cochés. Conteneurs, réseau et image d'essai supprimés. Non commité (consigne du coordinateur). · 0.5 h
- 2026-11-25 15:30 · agent:testeur · vérifié sur le SHA 9114f9e4ff26b35c6fd219b05da94165b47c1a78 (git archive ; python:3.14-slim 3.14.10 + postgres:16 jetable). Suite complète : 214 passés, 0 ignoré, 0 échec. Image construite avec `--build-arg GIT_COMMIT=9114f9e4ff26b35c6fd219b05da94165b47c1a78`, conteneur sur réseau jetable avec PostgreSQL 16 (migration 0001 jouée au démarrage) ; `/health` 200 avec le commit 9114f9e… Critère 1 : `GET /api/disponibilites?date=<9000 caractères>` → 422 ; une seule ligne d'accès `uvicorn.access GET /api/disponibilites 422`, sans `?`, `date=` ni valeur. Critère 2 : `test_la_chaine_de_requete_n_est_pas_ecrite`, `test_la_configuration_est_valide_et_capte_uvicorn_access`, `test_main_transmet_la_configuration_a_uvicorn` verts (configuration sans `request_line`). Critère 3 : `/`, `/health`, `/api/salles` journalisés avec leur statut 200 ; `/api/disponibilites?date=2026-12-01` 200. Critère 4 : suite verte ; `/health` et réponses de l'API inchangés (200, 422, 404 ; CSP, nosniff, no-referrer présents). Chemins hostiles : `?date=%0aFAUX%20200&secret=1` (422), `/` + 5000 `a` + `?x=1` (chemin tronqué à 200 caractères + « … », ligne de 255 octets), `/a%0d%0aGET%20/faux%20200?z=1#frag` (404, journalisé `/a%0D%0AGET%20/faux%20200`, pas de saut de ligne ni de fragment), `/api/inconnu?token=abc`, `POST /api/salles?x=secret`, `/%00%1b[31m?q=1`, `/..%2f..%2fetc%2fpasswd?x=secret`, `Host: evil.example` (400) : journal complet du conteneur, 0 occurrence de `?`, `date=`, `secret`, `token`, `q=1` ou de la valeur de 9000 caractères ; ligne la plus longue 255 octets. Un seul processus serveur (`Started server process [1]`, `workers=1` aussi contrôlé par test), pas d'en-tête `Server` dans les réponses (`server_header=False`). Remarques du relecteur (méthode non neutralisée, `format()`, assertion mal lue) : non bloquantes, sans effet sur les critères. Avis APPROUVÉ, revue humaine non requise. vérifié : 4/4 critères, suites vertes, SHA 9114f9e → TERMINE · 0.3 h (temps compté dans T-067)
- 2026-11-25 16:15 · agent:securite · audit sécurité : NON BLOQUANT, rapport [securite-2026-11-25-6.md](../rapports/securite-2026-11-25-6.md) (SHA `9114f9e4ff26b35c6fd219b05da94165b47c1a78`). Constat 15, partie a, fermé : 21 requêtes hostiles sur une instance jetable (9 000 caractères, `%0d%0a`, non UTF-8, `#`, caractères de contrôle, méthodes anormales, en-têtes et cookie leurres), 0 fuite et 0 caractère de contrôle dans le journal ; partie b dans T-072. Nouveau constat 17 (bas, remarques 1 et 2 du relecteur) : `getMessage()` hors du `try` (pas atteignable avec Uvicorn 0.52.4 et h11), méthode non neutralisée (refusée par h11), docstring « fragment » inexact. Aucun ticket `bug`. Statut et critères inchangés. Temps compté dans T-043 · 0 h
