---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-056
titre: Test manquant T-010 (/health sous base gelée)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE           # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 1            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:testeur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-25   # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-056 — Test manquant T-010 (/health sous base gelée)

## Description
Le critère 1 de [T-010](T-010-socle-application.md) exige que `/health` réponde 503 quand la base ne répond pas à `SELECT 1` dans le délai de 1 s. Aucun test ne couvre une base qui accepte la connexion mais ne répond plus (gelée, coupure réseau), ni une base dont le nom n'est plus résolu. Le testeur a constaté (image construite sur le SHA de base `6c53d31`, PostgreSQL 16 jetable) :

- après un premier `/health` en 200 (connexion poolée), `docker pause` du PostgreSQL puis `GET /health` : aucune réponse en 60 s, attendu 503 en environ 1 s ; cause probable : `pool_pre_ping` sur une connexion déjà ouverte, que `connect_timeout` et `statement_timeout` (côté serveur) ne bornent pas ;
- `docker stop` du PostgreSQL (nom non résolu) : 503 mais après 7,8 s.

Le défaut lui-même se corrige dans T-010 (critère 1 non coché, ticket resté `EN_REVUE`). Ce ticket ajoute le test qui l'aurait détecté et que le testeur pourra rejouer : base simulée qui accepte la connexion TCP sans répondre (par exemple une socket d'écoute locale qui n'envoie rien, y compris sur une connexion déjà établie), avec une assertion sur la durée de la réponse de `/health` (503 en moins de 2 s). À écrire par le développeur (le testeur ne modifie ni code ni tests).

## Critères d'acceptation
- [x] Un test montre que `/health` renvoie 503 en moins de 2 s quand la base accepte la connexion mais ne répond pas, avec une connexion ouverte qui devient muette et avec une connexion neuve.
- [x] Le test est vert sur le correctif de T-010 et rouge sur le code actuel (état de travail du 2026-11-25).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25, passe 1)
- **Commentaires** :
  1. Le fichier `app/tests/test_health_delai.py` répond à la demande : fausse base TCP locale sans Docker (`FausseBase`), deux modes (`tcp_muet` : connexion acceptée, rien lu ; `handshake_puis_muet` : handshake PostgreSQL terminé, puis silence), assertion 503 `{"status":"ko", ...}` en moins de 2 s. Les fils de la fausse base sont des démons, et `fermer()` fait `shutdown()` avant `close()` (justifié en commentaire). La fixture autouse attend la fin des sondes entre deux tests, ce qui évite qu'une sonde restée bloquée fausse le test suivant. Pas de `sleep` pour « laisser le temps » : les bornes sont mesurées.
  2. Remarque · cas « connexion déjà poolée » (critère 1) : il n'existe plus avec `NullPool` (T-010, passe 2), et `handshake_puis_muet` le remplace par une connexion ouverte qui gèle (la sonde bloque dans l'initialisation du dialecte après `ReadyForQuery`). Le remplacement est juste, mais le libellé du critère 1 parle encore d'une connexion poolée : au `testeur` d'apprécier ce point, et au coordinateur de reformuler le critère s'il le juge utile.
  3. Remarque · critère 2 (rouge sur l'ancien code) : l'ancien code n'existe dans aucun commit (le dossier `app/` n'a jamais été commité) ; le rouge annoncé (2,12 s pour `tcp_muet`, aucune réponse pour `handshake_puis_muet`) a été obtenu sur un code reconstitué et ne se vérifie pas par `git diff`. Je n'ai pas pu le rejouer. Le `testeur` peut le rejouer en rétablissant `pool_pre_ping=True` avec un pool (ou en supprimant le fil dédié) dans une copie jetable.
  4. Remarque · flakiness : bornes hautes de 2 s pour une conception à 1 s, marge suffisante ; seule la borne basse `bdd.DELAI_BASE_S <= duree` de `test_health_503_rapide_quand_le_controle_ne_revient_jamais` (`:152`) est trop stricte pour une horloge à 15 ms ; voir la remarque 4 de T-010. La fixture `_sondes_terminees` attend jusqu'à 20 s, ce qui couvre une résolution DNS lente (`.invalid`). Sans accès réseau du tout, ce test reste correct, car l'échec de résolution est immédiat ou borné par la sonde.
  5. Remarque · tests annexes pertinents : boucle d'événements libre pendant l'attente de `/health`, non-empilement des sondes à la limite de 4, `base_repond()` bloquant borné (utilisé par l'attente au démarrage). Ils couvrent bien le correctif, pas seulement le défaut observé.
  Grille : aucun secret réel (mot de passe factice local `secret-de-test`, hôte 127.0.0.1 ou `.invalid`) ; seul `app/` et le ticket sont concernés ; aucun commit `T-056` (code non commité, consigne du coordinateur), à régulariser avant la fusion. Vert 44 passés, 0 ignoré (annoncé par le développeur, sous Python 3.14.10 dans un conteneur) ; je n'ai pas exécuté les tests (pas d'outil d'exécution).
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 17:00 · agent:testeur · création · 0 h
- 2026-11-25 18:00 · agent:dev-backend · prise en charge (A_FAIRE → EN_COURS), traité avec la reprise de T-010 · 0 h
- 2026-11-25 20:15 · agent:dev-backend · livré pour revue (EN_COURS → EN_REVUE) : `app/tests/test_health_delai.py` (nouveau). Une fausse base locale (`FausseBase`, socket TCP, aucun Docker requis) simule : (a) `tcp_muet` : connexion TCP acceptée, rien lu ni écrit ; (b) `handshake_puis_muet` : handshake PostgreSQL terminé (refus SSL/GSS, AuthenticationOk, ReadyForQuery) puis aucune réponse aux requêtes, soit une connexion ouverte qui gèle ; la sonde bloque alors dans l'ouverture de connexion/initialisation, ce qui reproduit le silence d'une connexion poolée gelée (le nouveau code n'a plus de pool). Chaque cas assert 503 `{"status":"ko", ...}` en moins de 2 s (mesuré 1,01 s). Autres tests du même fichier : nom non résolu (`.invalid`), sonde qui ne revient jamais (durée entre 1 s et 2 s), boucle d'événements libre (`GET /` en moins de 0,5 s pendant que `/health` attend), sondes bloquées sans empilement, `base_repond()` bloquant borné. Une fixture attend la fin des sondes entre deux tests pour qu'une sonde restée bloquée ne fausse pas le suivant. · 0.8 h
- 2026-11-25 20:15 · agent:dev-backend · rouge sur l'ancien code (reconstitué dans un conteneur) : `tcp_muet` échoue (503 en 2,12 s, assertion `< 2.0`), `handshake_puis_muet` ne répond pas (interrompu à 40 s). Vert sur le correctif : suite complète sous Python 3.14.10, 44 passés, 0 ignoré (commande et détails dans le journal de T-010). Critères non cochés (rôle du testeur) : 1 couvert par les deux cas `tcp_muet` / `handshake_puis_muet` (le cas « connexion déjà poolée » n'existe plus avec `NullPool`, remplacé par la connexion ouverte qui gèle) ; 2 par la comparaison ancien / nouveau code ci-dessus. Non commité, non poussé · 0.2 h
- 2026-11-25 21:30 · agent:securite · audit sécurité : NON BLOQUANT ; fausse base de test sans risque hors test (écoute sur 127.0.0.1, port éphémère, fermée après chaque test, `tests/` exclu de l'image, identifiants factices), rapport [securite-2026-11-25-2.md](../rapports/securite-2026-11-25-2.md) ; temps compté dans T-043 · 0 h
- 2026-11-25 12:10 · agent:testeur · campagne SHA 9c0f8a8cf45329ef667ee7a4d4ca215006e4d47d : critère 2 coché, constaté : `tests/test_health_delai.py` vert sur le code commité (44 passés sous Python 3.14.10 ; 7 répétitions du fichier : 7 sur 7 vertes) ; rouge sur l'ancien code reconstitué par le testeur dans une copie jetable hors du dépôt (pool SQLAlchemy avec `pool_pre_ping=True`, `connect_timeout=1`, sonde synchrone sans fil dédié ni `wait_for`, `app/` non touché) : `tcp_muet` échoue (`assert 2.14 < 2.0`), `handshake_puis_muet` ne répond pas (interrompu à 40 s), les tests « ne revient jamais », « boucle libre », « sondes bloquées » et `base_repond` bloquant ne terminent pas (interrompus). Le cas « nom non résolu » reste vert sur l'ancien code dans cet environnement (échec DNS immédiat, 0,11 s) : il n'a donc pas de valeur de détection ici. Réserve : il s'agit d'une reconstitution, l'ancien code n'existant dans aucun commit.
- 2026-11-25 12:10 · agent:testeur · critère 1 NON COCHÉ (le ticket reste EN_REVUE) : le libellé exige « une connexion déjà poolée et une connexion neuve ». Le cas poolé n'existe plus avec `NullPool` (T-010, passe 2) et aucun test ne le couvre. `handshake_puis_muet` (handshake terminé, `ReadyForQuery`, puis silence) couvre une connexion neuve qui se fige juste après l'ouverture, pas une connexion déjà utilisée avec succès puis gelée (cas réel du `docker pause` après un premier 200). Je juge l'intention (« /health ne reste pas suspendu quand une connexion ouverte devient muette ») satisfaite par ce mode et par ma mesure sur l'image (200 puis pause : 503 en 1,008 s), mais le critère ne peut pas être coché tel qu'il est écrit : reformulation à faire par le coordinateur (par exemple remplacer « connexion déjà poolée » par « connexion ouverte qui devient muette »). · temps compté dans T-041
- 2026-11-25 23:45 · coordinateur · critère 1 reformulé sur décision humaine (option A) : « connexion déjà poolée » devient « connexion ouverte qui devient muette », le cas poolé n'existant plus avec `NullPool` depuis le correctif de T-010 (remarque 2 du relecteur, avis du testeur campagne 2) ; aucun changement de code · 0 h
- 2026-11-25 23:55 · agent:testeur · campagne SHA 2852fe7 : critère 1 (reformulé, ligne de 23:45) coché, constaté : `tests/test_health_delai.py` rejoué sur ce SHA, 7 passés (dont `tcp_muet` et `handshake_puis_muet`, 503 `{"status":"ko"}` en moins de 2 s), 3 répétitions du fichier seul sous Python 3.14.10 : 7 sur 7 vertes à chaque fois ; suite complète 105 passés, 0 ignoré. Critère 2 déjà coché (campagne 2). Vérifié : 2/2 critères, avis relecteur APPROUVÉ, revue humaine non requise, suites vertes, SHA 2852fe7 → TERMINE · temps compté dans T-041
