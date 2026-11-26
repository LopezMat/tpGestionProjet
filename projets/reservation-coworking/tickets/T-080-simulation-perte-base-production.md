---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-080
titre: SIMULATION — Perte de la base de production (volume Docker supprimé)
projet: reservation-coworking
type: incident              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: critique          # critique | haute | normale | basse
assigne: agent:gestionnaire-crise   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-de-crise (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 4.6          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Exercice de crise (scénario 5, S2) demandé par l'humain le 2026-11-26. Aucun événement réel : aucune commande Docker ni restauration n'est exécutée, `deploiement/local/` n'est ni lu ni modifié.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-080 — SIMULATION — Perte de la base de production (volume Docker supprimé)

## Description
**SIMULATION.** Hypothèse posée par l'humain : le **2026-11-26 à 10:00**, la base de la production locale de `reservation-coworking` est perdue, parce que le volume Docker de la base (`esn-reservation-coworking_pgdata`, [architecture.md](../architecture.md) § 4) a été supprimé par erreur.

- **Symptôme** : base de données de production perdue ; l'application ne peut plus lire ni écrire les réservations ni les comptes.
- **Heure de détection** : 2026-11-26 10:00 (signalement humain).
- **Impact utilisateur** : membres et accueil ne peuvent plus réserver ni se connecter ; toutes les réservations, tous les comptes (nom, e-mail, empreinte du mot de passe) et toutes les sessions de la base sont perdus. Données personnelles touchées (perte de disponibilité).
- **Runbook concerné** : [runbooks/perte-donnees.md](../../../runbooks/perte-donnees.md).
- **Environnement** : production locale Docker (DEC-003), `url_prod: http://localhost:8080`.

Priorité `critique` : perte de données de production (grille S2 § 4 ; runbook `perte-donnees`, « Déclencheurs et sévérité »). Prise immédiate par le `gestionnaire-crise`, sans attendre le triage (S2-R3).

### Diagnostic du gestionnaire-crise (SIMULATION, heures simulées à partir de 10:00)
**Runbook appliqué** : [perte-donnees](../../../runbooks/perte-donnees.md). Il correspond à la situation (S2 § 6, « Perte de données »), donc aucun ticket « Runbook manquant » n'est créé. Le cas particulier « volume supprimé » n'y est pas décrit : proposition P-1 du post-mortem.

**Gravité : `critique`, confirmée.**
- Le runbook classe en `critique` des « données de production supprimées ».
- La grille S2 § 4 classe en `critique` une « production indisponible, perte de données ».
- L'étendue est maximale : toutes les tables, tous les utilisateurs, avec des données personnelles, et aucune sauvegarde n'est établie par les traces (ci-dessous).
- Ce n'est pas une fuite d'après les éléments connus, donc on n'enchaîne pas avec le runbook `intrusion`, sous réserve que l'origine accidentelle soit confirmée par l'humain qui a signalé l'incident.

**Périmètre figé** (minutes 0-5)
- **Tables** ([architecture.md](../architecture.md) § 4) : `utilisateur` (nom, e-mail, empreinte Argon2id, rôle, indicateurs), `salle` (3 lignes insérées par migration, recréables), `reservation` (salle, date, créneau, lien au compte), `session` (empreinte SHA-256 du jeton). S'y ajoute la table de version Alembic. **Les quatre tables sont perdues en entier** : c'est le volume qui a disparu, pas des lignes.
- **Depuis quand** : 10:00 (premier symptôme et signalement). Aucun symptôme antérieur n'est connu : il n'existe ni `rapports/logs-*`, ni `rapports/metriques-*`, ni rapport de suivi pour ce projet.
- **Utilisateurs touchés** : **tous**, c'est-à-dire tous les comptes membres (« quelques dizaines », H-05) et tous les comptes accueil. Leur nombre exact n'est pas connu : aucune trace versionnée n'en compte.
- **Données personnelles** : nom, e-mail et empreinte du mot de passe. La perte de disponibilité est une violation au sens du RGPD (art. 4.12). Aucune donnée sensible (art. 9). La confidentialité n'est pas atteinte d'après les éléments connus : base sans port publié, app sur `127.0.0.1` seulement.

**Dernière sauvegarde utilisable** (minutes 5-10)
- **(a) Ce que les règles promettent** ([architecture.md](../architecture.md) § 6 lignes « § 9 Sauvegarde » et « § 8 Crise », § 8 « Sauvegardes » ; DEC-003 ; DEC-007 ; DEC-008) :
  - un `pg_dump -Fc` avant chaque déploiement (10 derniers gardés) ;
  - un `pg_dump` quotidien à **20:30** par `sauvegarder_local.py` (tâche planifiée, rétention de 14 jours) ;
  - aucune sauvegarde de plus de 30 jours.
  
  La sauvegarde attendue est donc **la quotidienne du 2026-11-25 à 20:30**, sauf déploiement plus récent. **Fenêtre de perte promise** : 2026-11-25 20:30 → 2026-11-26 10:00 (13 h 30). Les écritures effectivement perdues seraient celles du matin, de 08:00 à 10:00 (réservations créées ou annulées, comptes créés ou supprimés, changements de mot de passe, sessions), parce que l'app n'est joignable que depuis le poste (R-01) et que l'espace est fermé la nuit.
- **(b) Ce que les traces versionnées établissent : aucune sauvegarde.** C'est le **constat majeur** de la crise.
  - Il n'existe **aucun** `rapports/deploiement-*.md`, donc aucune ligne « Sauvegarde » (porte 5, S3-R4), aucun SHA attendu et aucun fichier `verifier-prod-*.json` du projet.
  - T-046 (GO), T-047 (déploiement) et T-048 (mise en service et tâche planifiée) sont `A_FAIRE`.
  - T-029 (sauvegarde quotidienne) est `A_FAIRE`. `scripts/sauvegarder_local.py` n'existe ni dans l'arbre ni dans l'historique (`git log --all -- scripts/sauvegarder_local.py` : vide). **Aucune sauvegarde quotidienne ne peut exister.**
  - À la première mise en service, `deployer_local.py` ne prend aucun `pg_dump` (« aucune (première mise en service, aucune base existante) »). Un dump d'avant déploiement suppose donc au moins un second déploiement, et aucun n'est tracé.
  - Les deux dumps de [test-rollback-2026-11-26.md](../rapports/test-rollback-2026-11-26.md) (09:51-09:53) appartiennent au projet jetable `esn-test-dd1be5ec` et à la mini-app de démonstration, détruits par le `tearDown` du test (`down -v`). Ce ne sont pas les données du projet. Ce rapport prouve seulement que la commande `pg_restore --clean --if-exists` du runbook fonctionne sur un vrai dump.
  - Les traces n'établissent même pas qu'une production existe. Sous l'hypothèse posée, elle aurait donc tourné **hors du circuit S3** (sans GO, sans porte 5, sans rapport), ou ses traces manquent. Le dernier SHA vérifié, nécessaire à la sonde de retour à la normale, n'est pas connu par les traces.
  - **Conséquence** : la vérification physique des dossiers `deploiement/local/reservation-coworking/sauvegardes/` et `sauvegardes-quotidiennes/` (lecture seule, `pg_restore --list`), ainsi que la lecture du dernier SHA de `historique.json`, sont une **action humaine** (Nadia), préalable inscrit dans [T-081](T-081-simulation-decision-restauration-base.md). Sans fichier valide, la fenêtre de perte couvre **toutes les données depuis la mise en service**.
- **Effet de la suppression du volume sur la procédure** : voir T-081. Il faut recréer seulement le service `db`, ce qui recrée le rôle `esn` et la base `app` sur un volume vide, puis restaurer avant tout démarrage de l'app. **Il ne faut lancer ni `deployer_local.py` ni `rollback_local.py`** : sur un volume absent, ils créent une base vide comme pour une première mise en service, sans alerte.

**Lien avec un changement** (minutes 5-10)
- `git log` : le dernier commit de l'app est `dc53a1d` (T-055) et `HEAD` est `fc6bd8a` (veille 2026-S48). Aucune migration n'a été ajoutée depuis `0001_schema_initial`, et aucun déploiement n'est tracé. La perte n'est donc liée **ni à une migration ni à un déploiement**.
- Opération manuelle : la suppression d'un volume utilisé est refusée par Docker. Il y a donc eu soit un `docker compose … down -v` sur le projet `esn-reservation-coworking`, soit une suppression ou un `docker volume prune` après l'arrêt des conteneurs. **Hypothèse à confirmer, sans blâme** : le test réel de rollback a tourné de 09:51 à 09:53 sur le même moteur Docker. Son nettoyage utilise `down -v` sur un projet nommé `esn-test-…`, et un nettoyage manuel qui suivrait ce modèle avec le mauvais nom de projet (préfixe commun `esn-`) supprimerait le volume de production.
- Si les conteneurs ont été supprimés, leurs journaux (`docker logs`) sont perdus. Il ne reste pas d'autre preuve que le témoignage de l'humain qui a signalé l'incident.

**Décisions préparées** (minutes 10-15), toutes en `ATTENTE_HUMAIN`
| Ticket | Décision | Porteur | Ordre |
|---|---|---|---|
| [T-081](T-081-simulation-decision-restauration-base.md) | Restauration : (a) intégrale, (b) sans `session` (recommandée si une sauvegarde valide existe), (c) reconstruction (imposée sinon) | Nadia | **1re**, elle bloque l'incident |
| [T-082](T-082-simulation-decision-mise-en-maintenance.md) | Maintenance : garder l'app arrêtée jusqu'au retour à la normale | Nadia | en même temps que T-081 |
| [T-083](T-083-simulation-decision-communication-client.md) | Communication au client : message 1 immédiat (notification art. 33.2), message 2 après T-081 | Claire | message 1 en même temps que T-081 |
| [T-084](T-084-simulation-decision-notification-cnil.md) | Recommandation CNIL au client (responsable du traitement) : registre sans notification, sous conditions | Claire (avis juridique externe recommandé) | avant le 2026-11-27 17:00 |

**Décision** : [DEC-019](../../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md) (`EN_REVUE`).
- Constat de Nadia, jouée par Ethan : aucun fichier de sauvegarde.
- **T-081 : option (c), reconstruction.**
- **T-083 : Claire prévient le client**, avec le message rédigé dans le post-mortem.
- T-082 et T-084 ne sont pas tranchés et restent `ATTENTE_HUMAIN`. Pour T-084, la recommandation au client est due au plus tard le 2026-11-27 à 17:00, et les 72 h expirent le 2026-11-29 vers 10:40.

**Retour à la normale (SIMULÉ, NON EXÉCUTÉ)** : option (c) de T-081.
1. Service `db` recréé seul (10:45).
2. GO humain (10:55). **En réalité**, ce GO exigerait le circuit S3 complet (R16, recette `CONFORME` sur le SHA, T-046), qui n'est pas franchi aujourd'hui.
3. `deployer_local.py` par le `deployeur` (11:00).
4. `init_accueil` (11:10).
5. Sonde `python scripts/sonde_sante.py --url http://localhost:8080 --sha <SHA du GO>` → `RESULTAT: DISPONIBLE ET À JOUR` **simulée** (11:15).
6. Contrôle de cohérence : 3 salles, 1 compte accueil, 0 membre, 0 réservation (11:20).

**Données définitivement perdues** (en agrégé) :
- tous les comptes membres (« quelques dizaines », nombre non tracé) et tous les comptes accueil (un seul recréé par `init_accueil`) ;
- toutes les réservations, passées et à venir (au plus 540 à venir) ;
- toutes les sessions.

Les 3 salles sont recréées à l'identique par migration. **Utilisateurs touchés** : tous ; ils reçoivent un nouveau compte de l'accueil et ressaisissent leurs réservations.

Post-mortem complet : [post-mortem-2026-11-26-perte-donnees.md](../rapports/post-mortem-2026-11-26-perte-donnees.md), v0.2, `EN_REVUE`. Leçon principale : **une règle sans preuve d'exécution n'est pas une garantie.**

## Critères d'acceptation
- [x] Le runbook `perte-donnees` est déroulé, chaque étape journalisée avec son heure (§ 1 à 4, puis § 5 et § 6 simulés après DEC-019).
- [ ] Chaque action sensible (restauration, mise en maintenance, communication au client, notification à la CNIL) a son ticket `decision` en `ATTENTE_HUMAIN`, tranché par un humain (`DEC-NNN`). T-081 et T-083 sont tranchés par DEC-019 (champ `decision` à renseigner par l'humain, à la fin des scénarios) ; T-082 (`ANNULE`, sans objet) et T-084 (`TERMINE`) sont clos par DEC-019 v0.2.
- [x] La dernière sauvegarde utilisable et la fenêtre de perte sont établies d'après les règles de rétention (DEC-003, DEC-007, DEC-008) : la règle promettait la quotidienne du 2026-11-25 20:30 ; en réalité, aucune sauvegarde (traces, puis constat physique, DEC-019). Fenêtre de perte : toutes les données.
- [x] Le retour à la normale est prouvé par la sonde (en simulation : décrit, non exécuté). `DISPONIBLE ET À JOUR` simulé à 11:15, non exécuté.
- [x] Le post-mortem `rapports/post-mortem-2026-11-26-perte-donnees.md` est rédigé, sans blâme, et chaque action corrective est liée à un ticket. Post-mortem complet (v0.3, `EN_REVUE`) ; actions liées à T-029, T-046, T-085 à T-087 et T-089 à T-092. **P-7 et P-8 (formations) : sans objet**, selon DEC-009 point E (tickets `formation` interdits dans ce projet, besoins renvoyés au plan de formation de l'ESN) ; coché sur instruction d'Ethan.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (incident)
- **Commentaires** :
- **Revue humaine requise** : oui (priorité critique)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 10:00 · agent:coordinateur · SIMULATION · création sur signalement humain (volume de la base supprimé), priorité critique, assigné au gestionnaire-crise (S2-R3) · 0 h
- 2026-11-26 10:00 · agent:gestionnaire-crise · SIMULATION · prise immédiate (S2-R3), ticket EN_COURS ; runbook appliqué : runbooks/perte-donnees.md (S2 § 6, perte de données) · 0.1 h
- 2026-11-26 10:01 · agent:gestionnaire-crise · SIMULATION · escalade (runbook § 3) : niveau 1 coordinateur et humain dès la prise ; niveau 2 Nadia (sauvegarde-restauration) et Karim (base-de-donnees-sql), restauration envisagée ; niveau 3 Claire (relation-client), données personnelles touchées ; compétence juridique absente de l'équipe · 0.1 h
- 2026-11-26 10:03 · agent:gestionnaire-crise · SIMULATION · constat : sonde non lancée (consigne de simulation) ; résultat attendu sous l'hypothèse `RESULTAT: INDISPONIBLE` (code 4) sur http://localhost:8080 · 0.1 h
- 2026-11-26 10:05 · agent:gestionnaire-crise · SIMULATION · périmètre figé (minutes 0-5) : 4 tables perdues en entier (utilisateur, salle, reservation, session), tous les comptes (quelques dizaines, H-05), données personnelles (nom, e-mail, empreinte), perte de disponibilité sans fuite connue ; pas d'enchaînement intrusion sous réserve de confirmer l'origine accidentelle · 0.3 h
- 2026-11-26 10:08 · agent:gestionnaire-crise · SIMULATION · dernière sauvegarde (minutes 5-10) : règles → quotidienne du 2026-11-25 20:30, fenêtre de 13 h 30 (écritures de 08:00 à 10:00) ; traces → aucune (aucun rapport de déploiement, T-029, T-046, T-047, T-048 en A_FAIRE, sauvegarder_local.py absent de l'historique Git, dumps du test de rollback sur un projet jetable) ; vérification physique confiée à Nadia (T-081) · 0.5 h
- 2026-11-26 10:10 · agent:gestionnaire-crise · SIMULATION · lien avec un changement (minutes 5-10) : git log (HEAD fc6bd8a, app dc53a1d), aucune migration ni aucun déploiement tracé ; opération manuelle probable (down -v ou suppression après arrêt), hypothèse d'un nettoyage après le test de rollback de 09:51-09:53, à confirmer sans blâme · 0.2 h
- 2026-11-26 10:12 · agent:gestionnaire-crise · SIMULATION · gravité confirmée critique (runbook « Déclencheurs et sévérité », grille S2 § 4) · 0.1 h
- 2026-11-26 10:15 · agent:gestionnaire-crise · SIMULATION · décisions préparées (minutes 10-15) : T-081 restauration, T-082 maintenance, T-083 communication client, T-084 notification CNIL, toutes en ATTENTE_HUMAIN au format R7 avec impact chiffré · 0.6 h
- 2026-11-26 10:15 · agent:gestionnaire-crise · SIMULATION · ticket BLOQUE (bloque_par : attente décision T-081, la première à trancher) ; décisions à présenter immédiatement par le coordinateur (R7) · 0 h
- 2026-11-26 10:50 · agent:gestionnaire-crise · SIMULATION · post-mortem provisoire rédigé pendant l'attente (S2-R5), rapports/post-mortem-2026-11-26-perte-donnees.md, EN_REVUE ; propositions d'actions correctives P-1 à P-9 pour le chef-de-projet (aucun ticket créé, consigne de l'humain) ; message de retour au coordinateur · 0.6 h
- 2026-11-26 10:20 · agent:gestionnaire-crise · SIMULATION · constat de la vérification physique reçu (Nadia, jouée par Ethan) : aucun fichier de sauvegarde dans deploiement/local/, T-029 jamais réalisé, aucun déploiement · 0 h
- 2026-11-26 10:30 · agent:gestionnaire-crise · SIMULATION · décision DEC-019 reçue (T-081 option (c) reconstruction ; T-083 Claire prévient le client) ; ticket EN_COURS, bloque_par vidé ; T-082 et T-084 toujours en ATTENTE_HUMAIN · 0.1 h
- 2026-11-26 10:35 · agent:gestionnaire-crise · SIMULATION · message au client rédigé dans le post-mortem (perte totale, reprise sous environ 1 h, cause, actions correctives), à relire et envoyer par Claire (AF1), non envoyé · 0.4 h
- 2026-11-26 10:40 · agent:gestionnaire-crise · SIMULATION · suivi : message envoyé par Claire (simulé) ; échéance CNIL (T-084) fixée à 72 h, soit 2026-11-29 vers 10:40, recommandation au client avant 2026-11-27 17:00 · 0.1 h
- 2026-11-26 10:45 · agent:gestionnaire-crise · SIMULATION · suivi de l'option (c) : service db recréé seul par Nadia sur un volume neuf (simulé, non exécuté) · 0 h
- 2026-11-26 11:00 · agent:gestionnaire-crise · SIMULATION · suivi : GO humain (10:55) puis deployer_local.py par le deployeur via le coordinateur, verifier-prod EN LIGNE ET À JOUR (simulé, non exécuté ; en réalité, circuit S3 complet requis, R16) · 0 h
- 2026-11-26 11:10 · agent:gestionnaire-crise · SIMULATION · suivi : compte accueil initial par init_accueil (Nadia, procédure de l'architecture § 7, hors session Claude Code ; simulé) · 0 h
- 2026-11-26 11:15 · agent:gestionnaire-crise · SIMULATION · retour à la normale : sonde sonde_sante.py --url http://localhost:8080 --sha <SHA du GO> → DISPONIBLE ET À JOUR, preuve SIMULÉE, sonde non exécutée · 0.2 h
- 2026-11-26 11:20 · agent:gestionnaire-crise · SIMULATION · contrôle de cohérence (Karim, simulé) : 3 salles, 1 compte accueil, 0 membre, 0 réservation ; données définitivement perdues et utilisateurs touchés listés en agrégé (runbook § 5) · 0.2 h
- 2026-11-26 11:45 · agent:gestionnaire-crise · SIMULATION · post-mortem complet (v0.2, EN_REVUE) : chronologie jusqu'au retour à la normale, DEC-019, message au client, leçon principale « une règle sans preuve d'exécution n'est pas une garantie », actions correctives T-029, T-046, T-085 à T-087, T-089 à T-092 (T-088 annulé ; P-7 et P-8 non créés, DEC-009 point E), décisions ouvertes T-082 et T-084 · 1.0 h
- 2026-11-26 11:45 · agent:gestionnaire-crise · SIMULATION · ticket EN_REVUE : service rétabli en simulation (preuve de la sonde simulée, non exécutée) et post-mortem rédigé ; passage TERMINE laissé au coordinateur (R13), critère « actions sensibles tranchées » non rempli tant que T-082 et T-084 sont ouverts · 0 h
- 2026-11-26 19:30 · agent:coordinateur · SIMULATION · critère « actions correctives liées à un ticket » coché : P-7 et P-8 sans objet (DEC-009 point E), sur instruction d'Ethan. Critère « actions sensibles » mis à jour : T-082 annulé et T-084 terminé (DEC-019 v0.2), reste le déblocage de T-081 et T-083 par Ethan à la fin des scénarios. Ticket laissé `EN_REVUE` · 0 h
