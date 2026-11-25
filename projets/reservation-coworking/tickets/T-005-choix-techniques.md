---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-005
titre: Choix techniques
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:architecte   # agent:<nom> | salarie:<prenom>
competence_requise: architecture-logicielle (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-004]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:   DEC-007                # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:architecte
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:    2026-11-24             # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-005 — Choix techniques

## Description
**Question.** L'[architecture](../architecture.md) v0.1 (`EN_REVUE`) du projet `reservation-coworking` peut-elle être validée comme base du planning (S1) et du développement ? Sept points demandent un arbitrage explicite (A à G). L'hébergement reste la production locale Docker (DEC-003) : aucun changement d'hébergeur n'est proposé.

**A. Stack (§ 2, décisions 1 à 4).**
- **Option A1 (recommandée)** : une seule image ; Python 3.14 + FastAPI + Uvicorn ; front HTML/CSS/JS sans framework ni build, servi par l'app ; PostgreSQL 16 + SQLAlchemy 2.0 + Alembic + psycopg 3 ; Argon2id (argon2-cffi).
- Option A2 : même backend, front React + Vite (Léa et `dev-frontend` maîtrisent React) : ajoute une chaîne de build Node et des dépendances npm que `securite.yml` n'audite pas.
- Option A3 : Django (authentification, CSRF et sessions fournis) : impose une `SECRET_KEY`, que le modèle commun `docker-compose.yml` ne transmet pas (voir C).

**B. Compte accueil initial (Q-14, décision 11).**
- **Option B1 (recommandée)** : commande `python -m reservation.init_accueil`, lancée **une fois par un humain** dans le conteneur (`docker exec -e ACCUEIL_EMAIL -e ACCUEIL_MOT_DE_PASSE_INITIAL …`), la valeur venant de son terminal. Rien à modifier dans les fichiers communs ; le secret ne passe par aucun agent ni aucun fichier.
- Option B2 : ajouter la variable au modèle commun `deploiement/docker-compose.yml` (fichier de C, tous les projets) : le secret devrait être dans l'environnement de `deployer_local.py`, lancé par le `deployeur`, et resterait visible par `docker inspect`.

**C. Clé de signature des sessions (CDC § 8, décision 6) : prise d'acte.** Le CDC demande de tenir « la clé de signature des sessions » hors dépôt. L'architecture utilise des sessions opaques stockées en base (empreinte SHA-256 du jeton) : **il n'y a aucune clé de signature**, donc aucun secret de plus. Confirmer que cet écart de forme est accepté (le CDC validé n'est pas modifié).

**D. Sauvegarde quotidienne et rétention (CDC § 9, décision 14).** L'outillage DEC-003 ne fait qu'un `pg_dump` avant chaque déploiement et garde les 10 derniers, sans limite d'âge.
- **Option D1 (recommandée)** : tâche planifiée sur le poste qui fait un `pg_dump` quotidien dans `deploiement/local/reservation-coworking/sauvegardes-quotidiennes/` (rétention 14 jours), **et** limite de 30 jours pour toute sauvegarde du projet, y compris celles d'avant déploiement (modification de l'outillage de C, `prod_locale.py`, à décider avec C). Une donnée supprimée sur demande subsiste au plus 30 jours dans les sauvegardes.
- Option D2 : tâche quotidienne seulement, sans toucher à la rétention de DEC-003 : une sauvegarde d'avant déploiement peut garder pendant des mois un compte supprimé.
- Option D3 : sauvegardes d'avant déploiement seulement : écart à l'exigence « sauvegarde quotidienne » du CDC § 9.

**E. Accès limité au poste de démonstration (§ 7).** En production locale, l'app n'est joignable que sur `127.0.0.1:8080` : les membres ne peuvent pas réserver depuis leur téléphone. Le mobile est vérifié par émulation dans le navigateur. Recommandation : **accepter pour la démonstration** (H-19, DEC-003) ; une exposition réelle (HTTPS, reverse proxy, hébergeur) serait une nouvelle décision.

**F. Suppression des comptes accueil.** Le CDC ne prévoit que la suppression des comptes **membres**. Recommandation : **ne pas ajouter** la suppression d'un compte accueil (non demandée ; évite de supprimer le dernier compte accueil). Un compte accueil d'un salarié parti est neutralisé par réinitialisation de son mot de passe.

**G. Seuils de sécurité proposés (à confirmer par `securite` et Karim).** Mot de passe de 12 à 128 caractères, différent de l'e-mail et de l'ancien, sans règle de composition ; 5 échecs de connexion par e-mail en 15 min → refus 15 min, et 30 échecs toutes adresses confondues en 15 min → refus 15 min ; session expirée après 2 h d'inactivité, 12 h au maximum.

**Recommandation.** Valider l'architecture v0.1 avec **A1, B1, C (prise d'acte), D1, E (accepté pour la démonstration), F (pas de suppression d'accueil), G (seuils proposés)**. Faire relire les choix par **Karim** avant la décision (sa fiche le prévoit), car il assure la revue humaine des tickets d'authentification (AF3, DEC-006). Pour D1, décider avec C, responsable de `prod_locale.py`.

**Impact.**
- **Coût d'exploitation** : 0 € (production locale, aucun service tiers) ; mise en place de la sauvegarde quotidienne ≈ 2 à 3 h (D1), hors catalogue des agents, à confier par le `chef-de-projet` (compétence `sauvegarde-restauration` : Nadia, ou l'agent `deployeur` sous revue de Nadia).
- **Délais** : la stack A1 n'a ni build front ni dépendance npm, ce qui réduit le risque sur les 18 jours ouvrés. Le chemin critique est l'authentification (F-04, F-07) et sa **revue humaine par Karim**, dont l'allocation au projet est aujourd'hui nulle (`allocation: {}`) : à décider au planning (événement d'équipe). Valider ce ticket au plus tard le 2026-11-26 pour garder la cible « architecture validée début décembre » (CDC § 10).
- **Maintenance** : une seule langue (Python), une seule image, peu de dépendances à suivre par le `veilleur` ; migrations additives obligatoires (règle « étendre puis contracter ») pour que le rollback reste sûr.
- **Si A2 ou A3** : +1 à 2 jours (chaîne de build ou adaptation de la gestion de la clé), et pour A3 une décision de plus sur le modèle commun.

## Critères d'acceptation
- [ ] Un humain a arbitré les points A à G (options retenues tracées).
- [ ] Un fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé (skill `tracer-decision`) et référencé dans `decision`.
- [ ] `architecture.md` est passé `VALIDÉ` par un humain avec `valide_par` et `decision: DEC-NNN`, ou renvoyé à l'`architecte` avec les corrections demandées.
- [ ] Pour D1 : le responsable C a donné son accord sur la limite d'âge des sauvegardes d'avant déploiement, ou l'option D2 est retenue.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : oui (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 19:30 · agent:architecte · création, ATTENTE_HUMAIN (validation des choix techniques) · 0 h
- 2026-11-24 21:00 · agent:architecte · architecture révisée en v0.2 (EN_REVUE) selon les arbitrages d'Ethan (DEC-007) ; temps compté sur T-004 · 0 h
- 2026-11-24 22:00 · agent:architecte · architecture révisée en v0.3 (EN_REVUE) selon les corrections d'Ethan (DEC-007) : alerte sans blocage global au-delà de 30 échecs, limite de 30 jours pour toute sauvegarde du projet (R-03 traité), « Pourquoi » de C ; temps compté sur T-004 · 0 h
- décision prise (DEC-007)