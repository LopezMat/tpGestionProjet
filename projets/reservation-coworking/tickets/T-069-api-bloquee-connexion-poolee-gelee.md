---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-069
titre: API de consultation sans réponse si une connexion poolée gèle
projet: reservation-coworking
type: bug                   # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-054]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:testeur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-069 — API de consultation sans réponse si une connexion poolée gèle

## Description
Défaut constaté par le testeur sur le SHA 4674c76 (porte 2 de T-054), hors critères de T-054 : le cas déjà vu pour `/health` (T-010, T-056) existe aussi pour `bdd.moteur_applicatif()` (`pool_pre_ping=True`, pool de 5 connexions) : `connect_timeout=5` ne borne que l'ouverture, `statement_timeout` est côté serveur, `pool_timeout=3` ne borne que l'attente d'une connexion libre. Une connexion déjà ouverte dont le serveur ne répond plus est testée par le pre-ping sans délai côté client.

**Étapes de reproduction.** (1) Image construite avec `--build-arg GIT_COMMIT=4674c76...`, conteneur + `postgres:16` jetable sur un réseau Docker dédié. (2) `GET /api/disponibilites?date=2026-12-01` → 200 (une connexion est poolée). (3) `docker pause` du conteneur PostgreSQL. (4) `curl --max-time 130 /api/disponibilites?date=2026-12-01`.

**Résultat attendu.** 503 JSON `indisponible` en quelques secondes (conception : pool 3 s, requête 5 s).
**Résultat obtenu.** Aucune réponse en 130 s (également en 40 s dans un premier essai) ; le fil de travail reste bloqué. Les appels suivants, qui ouvrent une connexion neuve, renvoient bien 503 en 5,04 s ; `/health` reste correct (503 en 1,01 s) et `/` répond 200. Après `docker unpause`, tout répond de nouveau (200).
**Environnement.** Docker Desktop 29.9.3, `python:3.14-slim` (3.14.10), `postgres:16`, 1 worker uvicorn.
**Assigné proposé.** `agent:dev-backend`, à trier par le `chef-de-projet` (S1-R5). Pistes : `TCP_USER_TIMEOUT` / keepalives libpq (`keepalives_idle`, `tcp_user_timeout`) dans `connect_args`, ou exécution bornée comme `_lancer` pour `/health`, ou `NullPool`.

**Fusion du constat 14 (triage du 2026-11-25).** Le constat 14 (bas, A04 disponibilité) du rapport [securite-2026-11-25-4.md](../rapports/securite-2026-11-25-4.md) décrit le même défaut, vu par l'auditeur : base gelée et 14 requêtes concurrentes, 5 réponses 503 après 5 s, 4 après 3 s, et **5 requêtes sans réponse après 40 s** (les connexions déjà poolées, dont le `SELECT 1` du `pool_pre_ping` attend sans borne). Recommandation de l'auditeur : `tcp_user_timeout` (par exemple 10 000 ms) et keepalives TCP courts (`keepalives_idle`, `keepalives_interval`, `keepalives_count`) dans `connect_args` du moteur applicatif. Aucun ticket séparé n'est créé pour le constat 14 : ce ticket le traite. Le constat 9 (même absence de borne sur `_moteur_sonde` de `/health`) n'est **pas** inclus : `/health` n'est pas modifié ici (critère 3), il reste à trier.

**Priorité et place dans le planning.** Correction **avant tout GO** (recommandation du testeur) : T-046 dépend de ce ticket. Hors de l'incrément de la soutenance du 2026-11-27 : ce ticket ne retarde ni T-054 ni T-055 (`dev-frontend`), et se fait après T-054 `TERMINE` (même fichier `bdd.py`). Revue de code dans T-066, vérification dans T-067.

## Critères d'acceptation
- [ ] Avec une connexion poolée dont la base est gelée (`docker pause`), `GET /api/disponibilites` et `GET /api/salles` renvoient 503 JSON en moins de 10 s.
- [ ] Un test automatisé reproduit ce cas (fausse base qui devient muette sur une connexion déjà ouverte, comme `FausseBase` de `test_health_delai.py`), vert sur le correctif et rouge sans lui.
- [ ] Scénario du constat 14 : base gelée et 14 requêtes concurrentes sur `GET /api/disponibilites` (dont des connexions déjà poolées) ; chacune reçoit une réponse 503 JSON en moins de 15 s, et le service répond 200 après `docker unpause` (constat au journal, sur une instance jetable).
- [ ] Le moyen retenu (paramètres de `connect_args`, exécution bornée ou autre) et ses valeurs sont notés au journal, avec la mention « constat 14 du rapport securite-2026-11-25-4 traité ».
- [ ] Les 140 tests existants restent verts ; `/health` n'est pas modifié.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : 
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 13:30 · agent:testeur · création · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage (S1-R5) : constat 14 du rapport securite-2026-11-25-4 fusionné ici (pas de doublon), 2 critères ajoutés ; assigné `agent:dev-backend` confirmé (AF6, `backend-python`) ; priorité `normale` maintenue (sévérité basse, hors incrément de la soutenance) ; estimation 1,5 h maintenue ; `depend_de: [T-054]` maintenu ; T-046 (GO) dépend désormais de ce ticket ; revue humaine non requise (disponibilité, ni authentification ni donnée personnelle). Temps compté dans T-008 · 0 h
