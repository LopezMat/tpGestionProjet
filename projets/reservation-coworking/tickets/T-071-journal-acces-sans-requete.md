---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-071
titre: Journal d'accès sans chaîne de requête (constat 15)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE           # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
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
termine_le:                 # facultatif : date du passage TERMINE
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
- [ ] Une requête `GET /api/disponibilites?date=<valeur de 9 000 caractères>` produit dans le journal du conteneur une seule ligne d'accès, qui contient la méthode, le chemin `/api/disponibilites` et le statut (422), et ne contient ni `?`, ni `date=`, ni la valeur envoyée (constat sur une instance jetable, noté au journal).
- [ ] Un test automatisé vérifie que la configuration de journalisation transmise à Uvicorn n'écrit pas la chaîne de requête (journal capturé, ou format de journal sans `%(request_line)s` ni chemin complet avec requête).
- [ ] Les requêtes nominales (`/`, `/health`, `/api/salles`) apparaissent toujours dans le journal d'accès avec leur statut.
- [ ] Suite complète verte ; `/health` et les réponses de l'API inchangés.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (format du journal d'accès ; aucune authentification ni donnée personnelle manipulée)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 14:45 · agent:chef-de-projet · création (triage du constat 15, partie a, rapport securite-2026-11-25-4) · 0 h
- 2026-11-25 15:05 · agent:dev-backend · prise en charge · 0 h
- 2026-11-25 15:10 · agent:dev-backend · livré pour revue. Choix : configuration `log_config` d'Uvicorn (access_log reste actif) avec un formateur propre `FormatAcces` (app/reservation/journaux.py) ; ligne d'accès = `<date> INFO uvicorn.access GET /chemin 200` (méthode, chemin sans `?` ni fragment borné à 200 caractères avec caractères de contrôle remplacés, statut). Adresse du client, version HTTP et requête ne sont plus écrites ; forme d'arguments inattendue : message générique, rien recopié. Uvicorn : 1 worker et server_header=False inchangés. Fichiers : app/reservation/journaux.py (nouveau), app/reservation/demarrer.py (log_config), app/tests/test_journal_acces.py (nouveau). Tests : conteneur python:3.14-slim + postgres:16 jetable (base coworking_test, TEST_DATABASE_HOTES_JETABLES pour l'hôte du conteneur), `python -m pytest -q` : 214 passed. Constat sur l'image construite avec --build-arg GIT_COMMIT=$(git rev-parse HEAD) : GET /, /health, /api/salles puis /api/disponibilites?date=<9000 caractères> (422) donnent 4 lignes `uvicorn.access` (`GET / 200`, `GET /health 200`, `GET /api/salles 200`, `GET /api/disponibilites 422`) ; journal complet du conteneur 1077 octets, 0 occurrence de `?`, `date=` ou de la valeur. Couverture des critères : 1 = constat image ci-dessus + test_la_chaine_de_requete_n_est_pas_ecrite ; 2 = test_la_configuration_est_valide_et_capte_uvicorn_access et test_main_transmet_la_configuration_a_uvicorn ; 3 = test_requetes_nominales_journalisees + constat image ; 4 = suite complète verte, aucun changement de /health ni de l'API. Ne touche pas la sécurité au sens authentification/droits/données personnelles (journalisation seulement, réduit l'exposition des données). Critères non cochés. Conteneurs, réseau et image d'essai supprimés. Non commité (consigne du coordinateur). · 0.5 h
