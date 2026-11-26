---
titre: SIMULATION — Post-mortem — Perte de la base de production — 2026-11-26
statut: EN_REVUE
responsable: agent:gestionnaire-crise
version: 0.2
maj_le: 2026-11-26
valide_par:
decision:
---
> **SIMULATION** — Exercice de crise (scénario 5, S2) demandé par l'humain le 2026-11-26, ticket incident [T-080](../tickets/T-080-simulation-perte-base-production.md), décision [DEC-019](../../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md). **Rapport complet** (version 0.2), en attente de relecture humaine. Aucun événement réel : aucune commande Docker, aucune reconstruction ni aucun déploiement n'a été exécuté, la sonde n'a pas été lancée, aucun message n'a été envoyé au client, et `deploiement/local/` n'a été ni lu ni modifié par l'agent. Les heures sont simulées à partir de 10:00, et **le retour à la normale ainsi que la sonde `DISPONIBLE ET À JOUR` sont simulés, non exécutés**.

<!-- modèle : templates/post-mortem.md v0.1 · responsable du modèle : A -->

# Post-mortem — Perte de la base de production — 2026-11-26

> Sans blâme : on cherche ce qui a permis l'erreur, pas un coupable.

- **Ticket incident** : [T-080](../tickets/T-080-simulation-perte-base-production.md)
- **Type** : perte de données
- **Runbook utilisé** : [runbooks/perte-donnees.md](../../../runbooks/perte-donnees.md)
- **Durée d'impact** (simulée) :
  - service indisponible de **10:00 à 11:15** (1 h 15), jusqu'à la sonde `DISPONIBLE ET À JOUR` simulée ;
  - service réduit (base vide, comptes membres à recréer) de **11:15 à environ 13:00** ;
  - **données perdues définitivement**.
- **Gravité** : `critique`. Le runbook classe ainsi les « données de production supprimées », et la grille S2 § 4 une « production indisponible, perte de données ». L'étendue est maximale : toutes les tables, tous les comptes, des données personnelles, aucune sauvegarde.
- **Décision humaine** : [DEC-019](../../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md) (`EN_REVUE`). Elle retient l'option (c) de T-081, la reconstruction, et fait prévenir le client (T-083). T-082 et T-084 restent ouverts (voir la dernière section).

## Leçon principale : une règle sans preuve d'exécution n'est pas une garantie
Les règles de sauvegarde étaient écrites, cohérentes et **validées par un humain** :
- un `pg_dump` avant chaque déploiement, les 10 derniers gardés ([DEC-003](../../../docs/decisions/2026-11-24-DEC-003-production-locale-docker.md)) ;
- un `pg_dump` quotidien à 20:30, gardé 14 jours, et aucune sauvegarde de plus de 30 jours ([DEC-007](../../../docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md), [DEC-008](../../../docs/decisions/2026-11-24-DEC-008-architecture-coherente-coworking.md), [architecture.md](../architecture.md) § 8).

Elles promettaient une perte limitée aux écritures du matin. **Rien ne prouvait qu'elles s'exécutaient** :
- l'outil de sauvegarde quotidienne n'avait jamais été écrit (T-029 `A_FAIRE`) ;
- la tâche planifiée n'avait jamais été créée (T-048 `A_FAIRE`) ;
- aucun déploiement n'avait eu lieu, donc aucune sauvegarde d'avant déploiement ;
- aucun contrôle, aucune trace et aucune alerte ne signalait ces absences.

Le jour de la crise, la règle n'a rien protégé : **toutes les données sont perdues**. Une garantie n'existe que si son exécution est **prouvée et vérifiée régulièrement**. Pour une sauvegarde, cela veut dire un fichier qui existe, qui se restaure et qui laisse une trace. Les actions T-029 (passé `critique`, dépendance du GO), T-092 et T-089 appliquent cette leçon (voir « Actions correctives »).

## Impact
- **Service** : application indisponible de 10:00 à 11:15 (simulé) pour les membres et l'accueil (ni connexion, ni réservation, ni vue du jour). Ensuite, service rétabli sur une base vide, avec un seul compte accueil ; les membres retrouvent l'accès à mesure que l'accueil recrée leurs comptes.
- **Données définitivement perdues** (runbook § 5, en termes agrégés, sans aucune donnée personnelle) :
  - **tous les comptes membres**, au nombre non tracé (« quelques dizaines », H-05), à recréer par l'accueil ;
  - **tous les comptes accueil** : un compte accueil initial est recréé par `init_accueil`, les autres sont à recréer par l'accueil ;
  - **toutes les réservations**, passées (historique de moins de 12 mois) et à venir. Les réservations à venir sont au plus 540, soit 36 créneaux par jour sur J à J+14 ; elles sont à ressaisir par les membres ou par l'accueil ;
  - **toutes les sessions**, sans conséquence au-delà d'une reconnexion.
- **Données recréées à l'identique** : les 3 salles, insérées par migration (H-20). Les fiches de salle n'avaient pas été personnalisées (T-027 `A_FAIRE`).
- **Utilisateurs touchés** : **tous** les comptes, membres et accueil. Chacun doit recevoir un nouveau compte (mot de passe temporaire, changement obligatoire à la première connexion) et ressaisir ses réservations.
- **Données personnelles** : nom, e-mail et empreinte Argon2id du mot de passe. La perte de disponibilité est **définitive**, donc c'est une violation au sens du RGPD (art. 4.12). La confidentialité n'est pas atteinte d'après les éléments connus. Le client, responsable du traitement, est prévenu par le message de T-083 (art. 33.2). La notification à la CNIL est encore à trancher (T-084, voir plus bas).
- **Coût ESN** (simulé) :
  - Nadia environ 1,5 h (environ 96 €) : recréation de la base, `init_accueil`, contrôles ;
  - Karim 0,25 h (environ 20 €) : contrôle de cohérence ;
  - Claire environ 0,75 h (environ 59 €) : relecture et envoi du message, remise du compte accueil ;
  - `gestionnaire-crise` 4,6 h (69 €) ;
  - `deployeur` environ 0,5 h (7,50 €).
  
  Il faut y ajouter le temps du client : environ 1 h 30 de recréation des comptes pour 30 comptes, plus la ressaisie des réservations.

### Dernière sauvegarde et fenêtre de perte
| | Ce que les règles promettaient | Ce qui existait réellement |
|---|---|---|
| Sauvegarde d'avant déploiement (DEC-003) | un `pg_dump -Fc` avant chaque déploiement | **aucune** : aucun déploiement n'a eu lieu, ni rapport de déploiement, ni ligne « Sauvegarde » (porte 5) |
| Sauvegarde quotidienne (DEC-007, DEC-008) | la quotidienne du **2026-11-25 à 20:30** | **aucune** : `scripts/sauvegarder_local.py` n'a jamais existé (T-029 non réalisé), et la tâche planifiée n'a pas été créée (T-048) |
| Vérification physique (Nadia, jouée par Ethan) | — | « aucun fichier de sauvegarde n'existe dans deploiement/local/ » (DEC-019) |
| Fenêtre de perte | 2026-11-25 20:30 → 2026-11-26 10:00, soit en pratique les écritures de 08:00 à 10:00 | **toutes les données depuis la mise en service** |

## Chronologie
Toutes les heures sont simulées. Les actions de 10:45 à 11:20 décrivent l'option (c) telle qu'elle figure dans [T-081](../tickets/T-081-simulation-decision-restauration-base.md). **Elles n'ont pas été exécutées.**

| Heure | Événement / action | Par |
|---|---|---|
| 09:51-09:53 | Test réel de rollback sur le même moteur Docker (projet jetable `esn-test-dd1be5ec`, nettoyé par `down -v` sur ce projet) | coordinateur, à la demande d'un humain (contexte, sans lien établi) |
| 10:00 | Suppression du volume `esn-reservation-coworking_pgdata` ; base perdue, application indisponible | opération manuelle sur le poste (origine non confirmée) |
| 10:00 | Signalement ; ticket incident T-080 `critique` créé et assigné au `gestionnaire-crise` (S2-R3) | humain, coordinateur |
| 10:00 | Prise immédiate, T-080 `EN_COURS`, runbook `perte-donnees` | agent:gestionnaire-crise |
| 10:01 | Escalade : niveau 1 (coordinateur, humain), niveau 2 (Nadia, Karim), niveau 3 (Claire ; compétence `juridique` absente) | agent:gestionnaire-crise |
| 10:03 | Constat : sonde non lancée (simulation) ; résultat attendu `INDISPONIBLE` | agent:gestionnaire-crise |
| 10:05 | Périmètre figé : 4 tables, tous les comptes, données personnelles, pas de fuite connue | agent:gestionnaire-crise |
| 10:08 | Dernière sauvegarde : promise (2026-11-25 20:30), aucune d'après les traces ; vérification physique confiée à Nadia | agent:gestionnaire-crise |
| 10:10 | Lien avec un changement (`git log`) : aucune migration ni aucun déploiement ; opération manuelle probable | agent:gestionnaire-crise |
| 10:12 | Gravité confirmée `critique` | agent:gestionnaire-crise |
| 10:13-10:15 | Décisions T-081 (restauration), T-082 (maintenance), T-083 (communication client), T-084 (CNIL) en `ATTENTE_HUMAIN` | agent:gestionnaire-crise |
| 10:15 | T-080 `BLOQUE` (attente de la décision T-081) ; décisions présentées (R7) | agent:gestionnaire-crise, coordinateur |
| 10:20 | Vérification physique : aucun fichier de sauvegarde dans les deux dossiers | Nadia (jouée par Ethan) |
| 10:30 | **DEC-019** : T-081 option (c), reconstruction ; T-083, prévenir le client | humain (Ethan, dans le rôle de Nadia) |
| 10:30 | T-080 `EN_COURS` (`bloque_par` vidé) | agent:gestionnaire-crise |
| 10:35 | Message au client rédigé dans ce rapport (section « Message au client ») | agent:gestionnaire-crise |
| 10:40 | Message relu et envoyé au client (**simulé, non envoyé**). Le délai de 72 h d'une éventuelle notification CNIL court pour le client à partir de ce moment | Claire |
| 10:45 | Service `db` recréé **seul** sur un volume neuf, avec le mot de passe existant ; l'image `postgres` recrée le rôle `esn` et la base `app` (simulé) | Nadia |
| 10:55 | GO humain pour redéployer le SHA en ligne sur la base neuve (simulé). **En réalité**, ce déploiement exigerait le circuit S3 complet : tickets `TERMINE`, rapports de tests, de sécurité et de recette `CONFORME` sur ce SHA (R16), GO T-046 tracé par un `DEC-NNN`. Aucun de ces éléments n'existe aujourd'hui | humain (GO) |
| 11:00 | `deployer_local.py` lancé par le `deployeur`, sur demande du coordinateur : `pg_dump` d'une base vide, build, lancement ; les migrations recréent le schéma et les 3 salles ; `verifier-prod` `EN LIGNE ET À JOUR` (simulé) | agent:deployeur, coordinateur |
| 11:10 | Compte accueil initial créé par `init_accueil`, selon la procédure de l'architecture § 7, dans un terminal hors de toute session Claude Code, avec les contrôles de non-fuite (simulé) | Nadia |
| 11:15 | **Sonde `python scripts/sonde_sante.py --url http://localhost:8080 --sha <SHA du GO>` → `RESULTAT: DISPONIBLE ET À JOUR` (simulée, non exécutée)** | Nadia, agent:gestionnaire-crise |
| 11:20 | Contrôle de cohérence (simulé) : 3 salles, 1 compte accueil, 0 compte membre, 0 réservation, révision Alembic `0001` | Karim |
| 11:25 | Compte accueil remis au client, qui change son mot de passe à la première connexion (simulé) | Claire |
| 11:30-13:00 | Recréation des comptes membres par l'accueil (environ 3 min par compte), puis ressaisie des réservations à venir par les membres (simulé, temps du client) | accueil du client, membres |
| 11:45 | Rapport d'incident complété ; T-080 `EN_REVUE` | agent:gestionnaire-crise |

## Cause racine
Cinq pourquoi, sans blâme. Ils portent sur ce que le système a permis, pas sur la personne qui a lancé la commande.

1. **Pourquoi le service et les données sont-ils perdus ?** Le volume Docker qui contient toute la base a été supprimé. Ce n'est pas une ligne effacée : c'est toute la base qui a disparu.
2. **Pourquoi cette suppression a-t-elle été possible ?** Rien ne distingue ni ne protège le volume de production. Le modèle commun le déclare comme un volume nommé ordinaire. `docker compose … down -v` ou `docker volume prune` le suppriment sans confirmation particulière. Les tests réels (`esn-test-…`) et la production (`esn-reservation-coworking`) partagent le même moteur Docker, le même préfixe et les mêmes commandes, à un nom de projet près.
3. **Pourquoi la perte est-elle définitive ?** Aucune sauvegarde n'existait. L'outillage de sauvegarde quotidienne (T-029) n'avait jamais été écrit, la tâche planifiée (T-048) jamais créée. La première mise en service ne fait, par conception, aucun `pg_dump`, et aucun déploiement n'avait eu lieu.
4. **Pourquoi une base avec des données a-t-elle pu exister sans sauvegarde ?** Les règles de sauvegarde étaient validées, mais **rien ne conditionnait l'existence des données à leur exécution**.
   - Le GO (T-046) ne dépendait pas de T-029.
   - Dans T-048, la création des comptes précède la tâche planifiée.
   - `deployer_local.py` et `rollback_local.py` traitent un volume absent comme une première installation, sans alerte.
5. **Pourquoi cette absence n'a-t-elle pas été vue avant la crise ?** **Aucune preuve d'exécution n'était exigée ni vérifiée.**
   - Aucun contrôle ne vérifie qu'une sauvegarde récente existe et qu'elle se restaure.
   - Les sauvegardes ne laissent aucune trace versionnée.
   - La sonde ne regarde que `/health`.

**Cause racine** : une règle de sauvegarde validée a été traitée comme une garantie, alors que rien ne prouvait ni ne vérifiait son exécution. De plus, aucun garde-fou ne protège le volume unique de la base. C'est la leçon principale en tête de ce rapport.

**Origine exacte de la suppression** : elle n'est pas confirmée par DEC-019. L'hypothèse d'un nettoyage Docker après le test de rollback de 09:51-09:53, avec le mauvais nom de projet, n'est ni confirmée ni rejetée. Elle ne change pas la cause racine : la protection du volume (T-086) vaut quelle que soit la commande. La qualification CNIL (T-084) reste conditionnée à la confirmation de l'origine accidentelle.

## Ce qui a bien fonctionné / mal fonctionné
- **+** Prise immédiate de l'incident `critique` sans triage (S2-R3) ; décisions prêtes à la 15e minute ; décision humaine 15 min plus tard (simulé).
- **+** Le runbook fixe clairement les rôles. Aucun agent n'a restauré, déployé ni contacté le client. Le garde-fou Bash du `gestionnaire-crise` n'a permis que des commandes de diagnostic.
- **+** La préparation de T-081 avait anticipé le piège de l'outillage : ne relancer ni `deployer_local.py` ni `rollback_local.py` sur un volume absent avant la décision, et recréer d'abord le seul service `db`. DEC-019 a repris cette consigne.
- **+** Empreintes Argon2id et jetons de session hachés : même une copie de la base n'aurait exposé ni mot de passe ni session utilisable.
- **+** Dans la réalité du dépôt, la dépendance de T-047 à T-029 avait empêché un déploiement sans outillage de sauvegarde.
- **−** **Les règles de sauvegarde n'ont rien protégé, faute d'exécution prouvée** (leçon principale) : perte totale.
- **−** Les sauvegardes ne laissent aucune trace versionnée lisible par les agents. Le runbook (minutes 5-10) ne prévoit pas le cas « aucune sauvegarde ».
- **−** Le runbook ne couvre pas la suppression du volume. L'outillage aurait recréé une base vide sans alerte.
- **−** Les preuves sont minces : si les conteneurs ont été supprimés, leurs journaux le sont aussi, et l'origine repose sur un témoignage non encore recueilli.
- **−** Dépendance à une seule personne. Seule Nadia sait restaurer, et elle est absente le mercredi et le 2026-12-03. Aucun salarié n'a la compétence `juridique` exigée par la décision CNIL.
- **−** La reprise « sous environ 1 h » suppose un GO immédiat. En réalité, le circuit S3 (R16, recette `CONFORME` sur le SHA) n'est pas franchi aujourd'hui, et le délai réel serait bien plus long.
- **−** Deux décisions sensibles restent ouvertes après le retour à la normale : T-082 et T-084.

## Message au client
Texte final rédigé par l'agent pour **Claire** (`relation-client`), qui le relit et l'envoie (AF1, T-083, DEC-019). Il ne contient aucune donnée personnelle. **Simulation : il n'a pas été envoyé.**

> **Objet : Incident sur l'application de réservation des salles — 26 novembre 2026**
>
> Bonjour,
>
> Nous vous informons d'un incident survenu ce matin sur l'application de réservation des salles.
>
> **Ce qui s'est passé.** Le 26 novembre vers 10 h, la base de données de l'application a été supprimée par erreur lors d'une opération technique sur le poste qui l'héberge. Aucune sauvegarde n'était encore en service : nous ne pouvons pas récupérer les données.
>
> **Ce que cela signifie pour vous.** Toutes les données de démonstration enregistrées dans l'application sont définitivement perdues :
> - les comptes des membres et de l'accueil (nom, adresse e-mail, mot de passe protégé) ;
> - toutes les réservations ;
> - les connexions en cours.
>
> Rien n'indique que ces données aient été consultées ou copiées par un tiers : il s'agit d'une perte, pas d'une fuite.
>
> **Reprise.** Nous remettons l'application en service sur une base neuve. Elle sera de nouveau disponible **dans environ 1 heure**, avec un compte accueil que nous vous remettrons. L'accueil pourra alors recréer les comptes des membres, environ 3 minutes par compte ; chaque membre choisira un nouveau mot de passe à sa première connexion, puis ressaisira ses réservations à venir. D'ici là, nous vous conseillons de noter à la main les réservations du jour. Nous pouvons vous accompagner pour la recréation des comptes.
>
> **Cause.** Une mesure de protection prévue n'était pas encore en place : la sauvegarde quotidienne de la base était définie, mais n'avait pas encore été mise en service, et rien ne nous alertait de son absence. Nous en assumons la responsabilité.
>
> **Ce que nous changeons.**
> - La sauvegarde quotidienne devient une condition préalable à toute mise en service.
> - Chaque jour, une vérification contrôlera que la sauvegarde existe et qu'elle peut être restaurée, avec une alerte en cas d'anomalie.
> - La base sera protégée contre une suppression accidentelle.
> - Notre procédure de crise sera complétée et testée.
>
> **Vos données personnelles.** En tant que responsable du traitement de ces données, il vous revient de consigner cet incident dans votre registre des violations de données et, le cas échéant, de le notifier à la CNIL dans les 72 heures. Nous vous transmettrons notre analyse et notre recommandation **au plus tard le vendredi 27 novembre à 17 h**.
>
> Nous vous enverrons sous 2 jours ouvrés un compte rendu complet de l'incident. Nous vous prions de nous excuser pour la gêne occasionnée.
>
> Claire, pour l'ESN

## Actions correctives
Les tickets ont été créés par le `chef-de-projet` en `A_FAIRE` à partir des propositions P-1 à P-9 de la version 0.1, et à la demande de DEC-019.

| Action | Type de ticket | Ticket | Responsable |
|---|---|---|---|
| Écrire l'outillage de sauvegarde quotidienne et la limite d'âge. **Passé `critique`** et devenu une dépendance du GO, à la demande de DEC-019 (causes 3 et 4) | tache | [T-029](../tickets/T-029-sauvegarde-quotidienne-limite-age.md) | salarie:nadia |
| Le GO dépend désormais de T-029 (cause 4) | decision | [T-046](../tickets/T-046-go-mise-en-production.md) | salarie:claire |
| **Vérifier chaque jour qu'une sauvegarde existe et se restaure dans une base jetable, avec alerte.** Preuve d'exécution, leçon principale ; remplace T-088 (P-4) à la demande de DEC-019 | amelioration | [T-092](../tickets/T-092-simulation-verification-restauration-sauvegardes.md) | salarie:nadia |
| Contrôle de fraîcheur des sauvegardes par l'`analyste-prod` (P-4) : **annulé**, remplacé par T-092 | amelioration | [T-088](../tickets/T-088-simulation-fraicheur-sauvegardes-suivi.md) (`ANNULE`) | — |
| Runbook `perte-donnees` : cas « volume supprimé » et « sauvegarde absente des traces » (P-1) | amelioration | [T-085](../tickets/T-085-simulation-runbook-volume-supprime.md) | salarie:nadia |
| Protéger le volume de production contre une suppression accidentelle (P-2, cause 2) | amelioration | [T-086](../tickets/T-086-simulation-proteger-volume-production.md) | salarie:nadia |
| Refuser de recréer une base vide quand l'historique contient un déploiement vérifié (P-3) | amelioration | [T-087](../tickets/T-087-simulation-refus-base-vide.md) | salarie:nadia |
| Exercice de restauration réel sur l'app du projet, cas « volume supprimé », chronométré (P-5) | tache | [T-089](../tickets/T-089-simulation-exercice-restauration-chronometre.md) | salarie:nadia |
| Fermer la fenêtre « production sans sauvegarde » dans le planning (P-6) | tache | [T-090](../tickets/T-090-simulation-planning-sans-sauvegarde.md) | agent:chef-de-projet |
| Registre des demandes de suppression chez le client avant la mise en service (P-9) | tache | [T-091](../tickets/T-091-simulation-registre-demandes-suppression.md) | salarie:claire |
| Second salarié formé à `sauvegarde-restauration` (P-7) | formation | **non créé** : [DEC-009](../../../docs/decisions/2026-11-24-DEC-009-budget-delais-coworking.md) point E (`VALIDÉ`) interdit les tickets `formation` dans ce projet ; besoin renvoyé au plan de formation de l'ESN | — |
| Compétence `juridique` sur les violations de données (P-8) | formation | **non créé** : même raison (DEC-009 point E) ; besoin renvoyé au plan de formation de l'ESN | — |
| Tâche planifiée et première sauvegarde manuelle réussie (existant) | tache | [T-048](../tickets/T-048-mise-en-service.md) | salarie:nadia |
| Rôle applicatif à recréer avant toute restauration une fois réalisé (existant, repris dans T-085) | amelioration | [T-058](../tickets/T-058-role-applicatif-non-superutilisateur.md) | salarie:nadia |
| Pas de changement d'image PostgreSQL pendant une crise ; même fichier que T-086 (existant, coordination) | bug | [T-078](../tickets/T-078-image-postgresql-16-16.md) | salarie:nadia |

[T-072](../tickets/T-072-rotation-journaux-modele-commun.md) (rotation des journaux) ne couvre pas la perte des journaux à la suppression des conteneurs. Cette perte est acceptée par l'architecture (§ 8, « Restauration ») et ne donne pas de ticket. [T-049](../tickets/T-049-fin-de-demonstration.md) reste la seule voie autorisée de suppression du volume, citée par T-086.

## Décisions humaines prises pendant la crise
- **[DEC-019](../../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md)** (2026-11-26, `EN_REVUE`, Ethan dans le rôle de Nadia, simulation) :
  - [T-081](../tickets/T-081-simulation-decision-restauration-base.md) : **option (c), reconstruction**, aucune sauvegarde n'existant ;
  - [T-083](../tickets/T-083-simulation-decision-communication-client.md) : **Claire prévient le client** (perte totale, reprise sous environ 1 h, cause et actions correctives) ;
  - retour d'expérience : T-029 `critique` et dépendance du GO, vérification régulière des sauvegardes avec alerte (T-092), leçon principale.
  
  T-081 et T-083 restent `ATTENTE_HUMAIN` jusqu'à ce que l'humain renseigne lui-même leur champ `decision`.

**Décisions encore ouvertes** (`ATTENTE_HUMAIN`, non tranchées par DEC-019) :
- [T-082](../tickets/T-082-simulation-decision-mise-en-maintenance.md) **mise en maintenance** : l'application est restée indisponible de fait de 10:00 à 11:15, sans décision de maintenance volontaire. Le service étant rétabli (simulé), la décision est devenue sans objet pour cet incident : à clore par un humain, l'agent ne la débloque pas.
- [T-084](../tickets/T-084-simulation-decision-notification-cnil.md) **notification CNIL** : la perte est désormais **définitive**, ce qui renforce la question du risque. T-084 prévoyait de basculer vers une notification par le client en cas de perte définitive, si l'avis juridique conclut à un risque.
  - **Échéance** : le client a été prévenu à 10:40 (simulé), donc les 72 h expirent le **dimanche 2026-11-29 vers 10:40**.
  - La recommandation de l'ESN doit lui parvenir **au plus tard le vendredi 2026-11-27 à 17:00**, ce que le message au client annonce.
