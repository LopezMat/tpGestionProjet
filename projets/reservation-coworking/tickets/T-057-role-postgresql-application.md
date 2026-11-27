---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-057
titre: Rôle PostgreSQL de l'application (constat 10, moindre privilège)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: architecture-logicielle (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.25           # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur le rôle PostgreSQL de l'application (constat 10 du rapport securite-2026-11-25-3), avec l'accord de C sur le modèle commun
validation_humaine_requise: oui   # oui | non
decision:      DEC-013             # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:       2026-11-27          # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-057 — Rôle PostgreSQL de l'application (constat 10, moindre privilège)

## Description
**Origine.** Constat 10 (sévérité moyenne) du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), audit d'incrément de T-011 et T-012 (DEC-011), commit `2852fe7`, verdict NON BLOQUANT. L'app se connecte à PostgreSQL avec le rôle `esn`, `POSTGRES_USER` de l'image officielle, donc **superutilisateur** (`rolsuper`, `rolcreaterole`, `rolcreatedb` constatés sur une instance jetable). Depuis T-011, ce même rôle sert aux migrations (DDL) et au moteur applicatif qui manipulera les données personnelles (T-013 et suivants). Une future injection ou une compromission de l'app aurait un impact maximal : `COPY … TO PROGRAM` (commandes dans le conteneur de base), lecture et suppression de toutes les données. En plus, le modèle commun `deploiement/docker-compose.yml` (DEC-003, responsable C) prend `absent` comme mot de passe si `PG_PASSWORD` manque (lancement à la main).

**Pourquoi une décision humaine.** La correction touche le **modèle commun de DEC-003** (tous les projets en production locale) et le choix d'une **seule `DATABASE_URL`** de l'[architecture](../architecture.md) v1.1 (`VALIDÉ`, DEC-008, § 7 « Secrets » et tableau § 8 « Secrets hors dépôt »). Il s'agit d'un choix technique (CLAUDE.md R7). Le document `VALIDÉ` ne peut pas être modifié par un agent (R6).

**Porteur (AF2)** : Karim (architecture et base de données `expert`, `securite-applicative` `confirme`), qui présente et recommande. La validation reste celle d'un humain de l'équipe (R5), **avec l'accord de C** pour le modèle commun (même principe que le point D1 de T-005).

**Échéance** : décision **avant le début de T-013** (prévu après la soutenance du 2026-11-27, vers le 2026-11-30). T-013 crée les premières routes qui manipulent des données personnelles ; le `dev-backend` doit savoir avant d'écrire T-013 que l'app ne disposera pas de droits de superutilisateur (pas de `CREATE EXTENSION` ni de `CREATE ROLE` dans les migrations, par exemple).

### Question
Avec quel rôle PostgreSQL l'application et ses migrations doivent-elles se connecter, et quand corriger le modèle commun ?

### Options
Taux : agent 15 €/h ; Karim 78,57 €/h ; Nadia 64,29 €/h (ARCHITECTURE § 8). Estimations en heures équivalent humain (R12).

| Option | Contenu | Coût estimé | Délai et chemin critique | Impact sur `architecture.md` et le modèle commun | Risque résiduel |
|---|---|---|---|---|---|
| **A (recommandée)** : un rôle applicatif unique, non superutilisateur | Modèle commun : création idempotente, par `deployer_local.py`, d'un rôle applicatif `NOSUPERUSER NOCREATEDB NOCREATEROLE`, propriétaire de la base `app` (donc du schéma `public` sous PostgreSQL 16), avec un mot de passe tiré au hasard et gardé hors Git comme `PG_PASSWORD`. `DATABASE_URL` de l'app utilise ce rôle. `esn` ne sert plus qu'à l'initialisation et à l'exploitation (`pg_dump`, restauration). Suppression du repli `:-absent` (échec explicite si une variable manque). Aucun changement de code dans `app/`. | **≈ 175 €** : T-058 Nadia 2 h (128,57 €), revue humaine T-059 Karim 0,5 h (39,29 €), revue de code 0,5 h (7,50 €) ; vérification `testeur` comprise dans T-067 | **Hors de la chaîne `dev-backend`.** Nadia, après T-029 (même outillage), environ 2 jours ouvrés de sa capacité allouée (1,12 h/j) : T-044 (environnement de recette) glisse d'environ 1 jour ouvré, sans dépasser le début de recette prévu (2026-12-08/09) | Principe d'une seule `DATABASE_URL` **conservé**. Précision « rôle non superutilisateur, propriétaire de la base » tracée dans le DEC ; amendement d'`architecture.md` facultatif (un humain la repasse `EN_REVUE`, puis `architecte` 0,5 h, 7,50 €). Modèle commun modifié pour tous les projets : PR relue et acceptée par C | Le rôle applicatif reste propriétaire du schéma : une injection pourrait encore supprimer ou modifier les tables du projet, mais plus exécuter de commandes dans le conteneur ni toucher les autres bases ou rôles |
| B : deux rôles (migrations et exécution) | A, plus un rôle propriétaire réservé aux migrations et un rôle d'exécution limité au DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `ALTER DEFAULT PRIVILEGES`). Pour un vrai gain, les migrations doivent tourner dans une étape distincte (service ponctuel `migrer` dans le modèle commun) : sinon le processus de l'app détient les deux mots de passe. `migrer.py`, `env.py`, `demarrer.py`, `env.example` et les tests sont adaptés. | **≈ 324 €** : Nadia 3 h (192,86 €), `dev-backend` 2 h (30 €), Karim 1 h (78,57 €), `architecte` 0,5 h (7,50 €), revue et tests 1 h (15 €) | +2 h sur la chaîne `dev-backend` avant T-013 (≈ 0,3 jour ouvré) ; architecture à rouvrir par un humain **avant** T-013 ; Nadia environ 3 jours ouvrés | **§ 7 et § 8 modifiés** (deux URL, étape de migration séparée) : `architecture.md` repassée `EN_REVUE` par un humain (R6), puis nouvelle validation. Démarrage tolérant de T-011 (migration au démarrage) à revoir. Modèle commun : deux variables et un service de plus, pour tous les projets | Le plus faible : l'app ne peut ni créer ni supprimer de table |
| C : correctif minimal maintenant, rôle avant le GO | Maintenant : suppression du repli `:-absent` seulement (Nadia 0,5 h). Le rôle applicatif (contenu de A) est fait plus tard, au plus tard avant T-044 et T-047. Le développement et les tests de T-013 à T-020 tournent sous superutilisateur (poste local, données fictives) | **≈ 207 €** au total (A + 0,5 h de Nadia, 32,14 €) | Aucun effet immédiat ; le travail de A se place en fin de projet, sur le chemin de la recette (Nadia est déjà sur T-044, T-048), donc risque de retard du GO | Comme A, plus tard | Reprise possible si T-013 à T-020 dépendent sans le savoir de droits de superutilisateur ; audit final sur une configuration qui change juste avant la recette |
| D : accepter le risque (statu quo) | Aucun changement ; risque accepté et tracé dans le DEC | 0 € | Aucun | Aucun | **Moyen, conservé en production** : contraire à la recommandation du `securite` (« au plus tard avant le GO ») ; l'audit avant mise en production (T-043) le signalera ouvert |

### Recommandation
**Option A**, décidée avant T-013, réalisée par Nadia juste après T-029 (même outillage, pas de conflit de fichiers) et terminée **avant T-044** (premier environnement qui contient des comptes) et en tout cas avant T-047. Pourquoi : elle supprime l'impact maximal (superutilisateur) pour environ 175 €, sans toucher au code de `app/` ni à la chaîne `dev-backend`, et sans rouvrir l'architecture (le principe d'une seule `DATABASE_URL` est conservé). L'option B est la cible de sécurité, mais son gain réel exige une étape de migration séparée, ce qui rouvre l'architecture et le démarrage tolérant de T-011 à trois semaines de la deadline. Je propose de l'inscrire au retour d'expérience (ticket `amelioration` pour une seconde livraison ou pour le modèle commun).

### Impact
- **Tickets touchés** : T-058 (réalisation, `A_FAIRE`, dépend de ce ticket ; contenu rédigé pour l'option A, à ajuster par le `chef-de-projet` si B ou C est retenue) ; T-059 (revue humaine de T-058) ; après la décision, le `chef-de-projet` ajoute T-058 aux `depend_de` de T-044 et de T-047 (A et B), ou de T-047 seulement (C). Option B : un ticket `dev-backend` de plus et une révision d'`architecture.md`. Option D : T-058 et T-059 passent `ANNULE`.
- **Capacité** : Nadia +2 h (A), utilisation portée de 36,8 % à environ 47 % de sa capacité allouée, toujours sous 50 % (AF9, aucune allocation à changer) ; Karim +0,5 h.
- **Date de fin projetée** : inchangée avec A (hors chaîne `dev-backend`) ; +0,3 jour ouvré avec B.
- **Budget** : de 0 € (D) à 324 € (B) ; 175 € pour A, soit environ 2,9 % du budget de 6 000 €. Aucune alerte S1-R11.
- **Autres projets** : le modèle commun sert à tous les projets en production locale. La création du rôle doit être idempotente et fonctionner sur un volume créé par l'ancien modèle (critère de T-058).

## Critères d'acceptation
- [x] Un humain a choisi une option (A, B, C ou D), et C a donné son accord sur la modification du modèle commun (sauf option D).
- [x] Un fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé (skill `tracer-decision`) et référencé dans `decision`.
- [x] Option B : `architecture.md` est repassée `EN_REVUE` par un humain avant le début de T-013.
- [x] Le `chef-de-projet` a ajusté T-058 et les dépendances de T-044 et de T-047 selon l'option retenue, en citant le DEC.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : oui (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création, ATTENTE_HUMAIN (triage du constat 10 du rapport securite-2026-11-25-3) ; temps d'analyse compté dans T-008 · 0 h
- 2026-11-27 · Ethan · 0,25 h · Tranché par DEC-013 (validée le 25/11), ticket débloqué.