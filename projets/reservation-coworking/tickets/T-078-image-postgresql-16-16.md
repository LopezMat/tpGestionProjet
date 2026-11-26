---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-078
titre: Image PostgreSQL 16.16 ou plus (43 CVE corrigées, veille P-1)
projet: reservation-coworking
type: bug                   # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn (R18, DEC-023)
imputation_decision: DEC-020   # décision VALIDÉ qui met ce ticket à la charge de l'ESN
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-078 — Image PostgreSQL 16.16 ou plus (43 CVE corrigées, veille P-1)

## Description
Proposition **P-1** et constat 1 de la veille [2026-S48](../../../veille/2026-S48.md) (ticket de travail [T-077](T-077-veille.md)). Ticket créé en `A_FAIRE` pendant la pause du développement : **ni traité ni planifié** ; il sera trié à la reprise.

**Vulnérabilité.**
- **CVE** : 43 identifiants corrigés par PostgreSQL 16.16, dont des exécutions de code à CVSS 8,8 (CVE-2026-120151, -120150, -120149, -120143, -120141, -120139) et CVE-2026-120153 (CVSS 7,2) ; famille CVE-2026-120139 à CVE-2026-120154 et autres (liste complète dans les notes de version).
- **Paquet** : PostgreSQL serveur, image `postgres:16-alpine` du **modèle commun** [`deploiement/docker-compose.yml`](../../../deploiement/docker-compose.yml) (ligne 16, service de base ; DEC-003, responsable C, utilisé par tous les projets locaux). La même image est citée dans les commandes de test et d'essai de [`app/README.md`](../app/README.md).
- **Version installée** : **à confirmer**. Le tag `postgres:16-alpine` est flottant (Docker Hub : tag mis à jour le 2026-11-22, digest `sha256:f2f98726…`) ; une image tirée sur le poste avant le 2026-11-12 est affectée. Le `veilleur` n'avait pas d'accès Docker.
- **Versions corrigées** : 16.16 et suivantes (toute 16.x antérieure est affectée).
- **Sources** : [avis de sécurité postgresql.org](https://www.postgresql.org/support/security/) ; [notes de version 16.16](https://www.postgresql.org/docs/release/16.16/) (2026-11-12) ; [CVE-2026-120151](https://www.postgresql.org/support/security/CVE-2026-120151/) et [CVE-2026-120153](https://www.postgresql.org/support/security/CVE-2026-120153/) (2026-11-12) ; [Docker Hub, tag 16-alpine](https://hub.docker.com/v2/repositories/library/postgres/tags/16-alpine).
- **Impact** : exécution de code sur le serveur de base par un utilisateur de base authentifié (`PR:L`) ou disposant du droit de créer des objets ; lecture ou suppression de toutes les données (réservations, comptes). Dans l'app, seule l'application parle à la base et son SQL est statique ([securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), constat 10) : l'exposition suppose une injection SQL ou une compromission de l'app. Aucune exploitation active signalée par postgresql.org.
- **Preuve attendue** : sortie de `SELECT version()` sur l'instance du projet, avant et après.

**Reproduction (bug).**
1. Sur le poste, instance locale du projet lancée avec le modèle commun (ou base jetable `postgres:16-alpine` telle que tirée localement).
2. `docker compose exec db psql -U esn -d app -c "SELECT version();"` (ou `docker image inspect postgres:16-alpine` pour la date et le digest de l'image locale).
3. **Résultat attendu** : `PostgreSQL 16.16` ou plus.
4. **Résultat obtenu** : non lu (tag flottant, aucun accès Docker pendant la veille) ; affecté si l'image locale date d'avant le 2026-11-12.
5. **Environnement** : production locale Docker (DEC-003), Docker Desktop du poste, image `postgres:16-alpine`, volume `pgdata`.

**Mise à jour mineure** : pas de dump/restore. `REINDEX` recommandé seulement pour les index GIN, btree sur `bpchar` et `gist_trgm_ops` : la migration `0001_schema_initial.py` n'en déclare aucun (colonnes `String`/`Text`), à confirmer pour les migrations suivantes.

**Priorité `normale`** (proposition du `veilleur`, conservée) : grille S2 § 4 (CVE sans exploitation connue) et application hors production (aucun rapport de déploiement) ; pas d'exposition directe de secrets ni de données personnelles. **Passe à `haute` au premier déploiement** si l'image n'est pas à jour.

**Affectation : `salarie:nadia`, et non `agent:deployeur` comme proposé.** Aucun agent du catalogue ne convient :
- le `deployeur` n'intervient qu'après un GO humain, sur un SHA précis, avec les seules commandes `deployer_local.py`, `rollback_local.py` et `verifier-prod` ; il « n'appelle jamais `docker` lui-même » et ne modifie pas l'outillage (`.claude/agents/deployeur.md`, règles 1 et 6) ;
- le `dev-backend` n'écrit que dans `projets/<slug>/app/` (règle 8) ; le modèle commun `deploiement/` est hors de son périmètre ;
- aucun agent ne possède la compétence `docker` (`equipe/agents.md`).

Règle 7 du `chef-de-projet` : à défaut d'agent, un salarié compétent. Nadia est la seule salariée qui possède `docker` (niveau `confirme`, requis atteint, AF7) ; elle est allouée au projet (20 %, DEC-009), `actif`, sans `date_depart`. C'est le même choix que pour les autres modifications du modèle commun ([T-029](T-029-sauvegarde-quotidienne-limite-age.md), [T-058](T-058-role-applicatif-non-superutilisateur.md), [T-072](T-072-rotation-journaux-modele-commun.md)). L'affectation découle de la compétence et du périmètre, **pas d'un objectif d'utilisation** (AF9). Fenêtre à éviter au moment de la planification : le 2026-12-03 (Nadia en formation, EV-002). **Ticket salarié (AF11, R15)** : à faire par un humain ; la modification du modèle commun est relue et acceptée par C (PR).

**Estimation ajustée à 1,5 h** (au lieu de 1 h proposée) : lecture de la version, modification du modèle commun et PR, redémarrage sur le volume existant, migrations et suite de tests sur la nouvelle image, contrôle des index et des extensions.

**Coordination** : T-029, T-058 et T-072 modifient le même fichier `deploiement/docker-compose.yml` ; la modification de l'image peut partir dans la même PR que l'un d'eux (à arbitrer au triage).

**Recommandation pour le triage à la reprise du développement** (aucune dépendance ajoutée aujourd'hui, consigne du coordinateur) : ce ticket devrait être `TERMINE` **avant le GO [T-046](T-046-go-mise-en-production.md)** ; le chef-de-projet proposera alors de l'ajouter à `depend_de` de T-046.

**Revue humaine** : requise (sécurité, et modification d'un modèle commun). **Ticket compagnon de revue humaine à créer au triage, à la reprise du développement** (non créé aujourd'hui, ticket non planifié). Relecteur pressenti : un salarié autre que l'autrice, avec `securite-applicative` ou `base-de-donnees-sql` au moins `confirme` (Karim, comme pour T-059).

## Critères d'acceptation
- [ ] `SELECT version()` sur l'instance locale du projet affiche 16.16 ou plus ; la sortie (avant et après) est collée au journal du ticket.
- [ ] La version de l'image est fixée ou documentée dans le modèle commun (`postgres:16.16-alpine`, ou tag avec digest, ou procédure `docker compose pull` dans le runbook), **après accord du responsable C** (PR acceptée par C).
- [ ] Le volume `pgdata` existant démarre sur la nouvelle image sans dump/restore ; les migrations Alembic s'appliquent et la suite de tests de l'app passe sur cette image (résultat `pytest` au journal).
- [ ] Constat consigné au journal : aucun index GIN, btree sur `bpchar` ni `gist_trgm_ops` dans les migrations (donc pas de `REINDEX`), et liste des extensions installées (`SELECT extname FROM pg_extension;`) sans extension C à reconstruire.
- [ ] Les commandes de [`app/README.md`](../app/README.md) qui citent `postgres:16-alpine` sont alignées sur l'image retenue, ou l'écart est justifié au journal.
- [ ] La ligne « Revue humaine » ci-dessous est remplie par le relecteur humain ; le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (vulnérabilité de la base, modification du modèle commun DEC-003 ; ticket compagnon [T-099](T-099-revue-humaine-t-078.md), Karim, créé au triage le 2026-11-26)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 16:30 · agent:chef-de-projet · création (veille 2026-S48, proposition P-1, constat 1 ; assigné à Nadia faute d'agent compétent sur le modèle commun ; estimation 1 h portée à 1,5 h ; non planifié, développement en pause) · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 22:45 · agent:chef-de-projet · SIMULATION · triage : ticket compagnon de revue humaine T-099 créé (Karim, 0,5 h, imputé à l'ESN, DEC-020) ; ce ticket ajouté à depend_de du GO T-046 (DEC-020, point 3), comme le recommandait sa Description · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
