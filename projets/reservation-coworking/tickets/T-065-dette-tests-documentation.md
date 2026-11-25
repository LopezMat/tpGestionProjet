---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-065
titre: Dette de tests et de documentation de l'incrément (remarques T-010, T-011 et T-054)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: basse             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010, T-011, T-056, T-060, T-054, T-062, T-070]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-065 — Dette de tests et de documentation de l'incrément (remarques T-010 et T-011)

## Description
Regroupement des petites remarques non bloquantes du `relecteur-code` sur l'incrément de DEC-011, sans enjeu de sécurité :
- [T-010](T-010-socle-application.md), remarque 3 de la passe 2 : la docstring de `/health` (`app/reservation/app.py:43`) cite `bdd.DELAI_BASE_S` et se retrouve dans `docs/openapi.json`, lu par le `dev-frontend` ;
- T-010, remarque 4 de la passe 2 (et remarque 4 de [T-056](T-056-test-manquant-t-010.md)) : la borne basse `bdd.DELAI_BASE_S <= duree` de `tests/test_health_delai.py:152` peut être violée de quelques millisecondes (résolution d'horloge) ;
- [T-011](T-011-modele-donnees-migrations.md), remarque 7 : `test_aucune_migration_descendante` interdit toute chaîne `drop_` dans `versions/` et bloquera la phase « contracter » que l'architecture § 8 autorise en seconde livraison ;
- T-011, remarque 8 : `test_moteurs_distincts` compare deux fonctions différentes, son assertion est toujours vraie.

Ajouts du triage du 2026-11-25 (14 h 45), remarques sans enjeu de sécurité sur [T-054](T-054-api-consultation-disponibilites.md) (relecteur-code, passe 1 ; audit [securite-2026-11-25-4.md](../rapports/securite-2026-11-25-4.md), « Remarques sans enjeu de sécurité ») :
- remarque 1 : toute `SQLAlchemyError` devient `BaseIndisponible` et le journal ne dit que le chemin ; une table absente ou un `statement_timeout` sont indiscernables d'une base éteinte ;
- remarque 2 (et audit) : `_FORMAT_DATE` utilise `\d`, qui accepte les chiffres Unicode ;
- remarque 3 : le jour ouvré est déduit en rattrapant l'exception de `verifier_creneau_valide` ; variable `l` aux lignes 91 et 152 ;
- remarque 4 : garde de la fixture de `tests/test_api_consultation.py` en `"test" in nom` (`contest`, `latest` passeraient) ;
- remarque 5 : assertion tautologique `migrer.appliquer() is True or migrer.appliquer() is False`, qui joue la migration deux fois ;
- audit : le message `date_hors_fenetre` parle de « réserver » sur une route de consultation ;
- audit : `HEAD /api/salles` répond 404 (route déclarée en `GET` seulement, réponse du 404 JSON de `/api/*`).

La remarque 6 (503 sur `statement_timeout` non testé) est dans T-070, la remarque 7 (créneaux passés du jour J) dans T-055 et T-018, la remarque 8 (date du journal de T-020) relève du coordinateur. Le défaut de base gelée (constat 14) est dans T-069, le journal d'accès (constat 15) dans T-071 et T-072.

Priorité basse : **hors de l'incrément de la soutenance et après les Must**. À faire après le passage `TERMINE` de T-010, T-011 et T-056 (le `testeur` y travaille), et après T-060, qui modifie le même fichier `tests/test_migrations.py`. Les remarques 1 à 3 de T-012 sont traitées dans T-062 (même fichier que le constat 12). Après T-054 (code relu), T-062 (si `est_jour_ouvre` est ajouté à `regles.py`, même fichier) et T-070 (même fichier `tests/test_api_consultation.py`). Compétence passée de `tests-unitaires` à `backend-python` : les ajouts touchent le code de `api.py`.

## Critères d'acceptation
- [ ] La docstring de `/health` ne cite plus de nom interne (par exemple « répond 503 en 1 s au plus ») ; `docs/openapi.json` est régénéré par le test qui le produit, et ce test est vert.
- [ ] La borne basse de `tests/test_health_delai.py:152` laisse une marge (par exemple `0.9 <= duree`) ; le fichier passe 7 fois de suite.
- [ ] `test_aucune_migration_descendante` accepte une suppression marquée explicitement (marqueur documenté dans le README, qui cite la décision de « contracter ») et échoue toujours sur un `drop_` non marqué (deux tests).
- [ ] `test_moteurs_distincts` est supprimé ou remplacé par une assertion qui échouerait si le moteur applicatif et le moteur de sonde étaient le même objet.
- [ ] T-054, remarque 1 : quand `BaseIndisponible` est levée, le journal contient le nom de la classe de l'exception d'origine (par exemple `OperationalError`, `TimeoutError`) et le chemin, jamais le message de l'exception, l'URL de connexion ni les paramètres (test sur le journal capturé) ; la réponse 503 reste inchangée.
- [ ] T-054, remarque 2 : le format de `date` n'accepte que les chiffres ASCII (`[0-9]` ou `re.ASCII`) ; `٢٠٢٦-١١-٢٦` et `２０２６-12-01` reçoivent le message d'erreur de format (test).
- [ ] T-054, remarque 3 : le jour ouvré est déterminé par une fonction explicite (`weekday()` ou `regles.est_jour_ouvre`), sans rattraper d'exception ; aucune variable nommée `l` dans `api.py`.
- [ ] T-054, remarque 4 : la fixture d'intégration de `tests/test_api_consultation.py` refuse une base dont le nom ne se termine pas par `_test` (ou hors d'une liste explicite), avant toute écriture (test de la garde avec `latest` et `contest`).
- [ ] T-054, remarque 5 : l'assertion tautologique est remplacée par un seul appel à `migrer.appliquer()`.
- [ ] Message de fenêtre sur la consultation : `GET /api/disponibilites` au-delà de J+14 renvoie un 422 dont le message parle de consultation (« Les disponibilités ne sont consultables que jusqu'à 14 jours à l'avance. » ou équivalent) et ne contient pas « réserv » ; le message de `POST /api/reservations` (T-018) n'est pas concerné (test).
- [ ] `HEAD /api/salles` et `HEAD /api/disponibilites?date=<jour ouvré>` ne répondent plus 404 : 200 sans corps, ou 405 avec l'en-tête `Allow: GET` (choix noté au journal ; test) ; `docs/openapi.json` régénéré si le schéma change.
- [ ] Suite complète verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (tests et documentation)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage des remarques 3 et 4 de T-010 et 7 et 8 de T-011) · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage (S1-R5) : ajout des remarques 1 à 5 du relecteur-code sur T-054 et des remarques sans enjeu de sécurité de l'audit securite-2026-11-25-4 (message « réserver », `HEAD` en 404) ; 7 critères ajoutés ; estimation 1 → 2,5 h (remarque 1 : 0,4 h ; 2 et 3 : 0,4 h ; 4 et 5 : 0,2 h ; message : 0,2 h ; `HEAD` : 0,3 h) ; compétence `backend-python (confirme)` ; dépend aussi de T-054, T-062 et T-070 (mêmes fichiers) ; priorité `basse` maintenue. Temps compté dans T-008 · 0 h
