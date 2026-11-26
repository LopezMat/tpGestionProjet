---
titre: SIMULATION — Perte de la base de production reservation-coworking, reconstruction et communication au client
statut: VALIDÉ
responsable: D
version: 1.0
maj_le: 2026-11-26
valide_par:     Ethan            # rempli par l'humain qui valide
decision: DEC-019           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-019
date: 2026-11-26
decide_par: Ethan (dans le rôle de Nadia pour T-081, simulation)
projet: reservation-coworking
ticket: T-081, T-082, T-083, T-084, T-090
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
> **SIMULATION** — Décision prise dans l'exercice de crise T-080 (scénario 5, S2) du 2026-11-26. Aucune commande Docker, aucune restauration ni reconstruction n'est exécutée, et aucun message n'est réellement envoyé au client.

<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-019 — SIMULATION — Perte de la base de production, reconstruction et communication au client

## Contexte
Le 2026-11-26 à 10:00 (hypothèse de la simulation), le volume Docker `esn-reservation-coworking_pgdata` de la production locale est supprimé par erreur : comptes, réservations et sessions sont perdus. C'est l'incident critique [T-080](../../projets/reservation-coworking/tickets/T-080-simulation-perte-base-production.md), traité selon le runbook [perte-donnees](../../runbooks/perte-donnees.md). Le `gestionnaire-crise` a préparé quatre décisions : [T-081](../../projets/reservation-coworking/tickets/T-081-simulation-decision-restauration-base.md) (restauration), [T-082](../../projets/reservation-coworking/tickets/T-082-simulation-decision-mise-en-maintenance.md) (mise en maintenance), [T-083](../../projets/reservation-coworking/tickets/T-083-simulation-decision-communication-client.md) (communication au client) et [T-084](../../projets/reservation-coworking/tickets/T-084-simulation-decision-notification-cnil.md) (CNIL). T-081 était la première à trancher.

Le préalable de T-081 était de vérifier physiquement les sauvegardes. Ethan l'a fait en jouant Nadia : « aucun fichier de sauvegarde n'existe dans deploiement/local/ ; T-029 n'a jamais été réalisé et aucun déploiement n'a eu lieu, donc aucune sauvegarde avant déploiement non plus ».

## Options étudiées
T-081, stratégie de restauration :

| Option | Avantages | Inconvénients |
|---|---|---|
| (a) Restauration intégrale de la sauvegarde valide la plus récente | environ 45 min ; on ne perd que les écritures faites depuis la sauvegarde | suppose une sauvegarde valide ; les sessions fermées depuis redeviennent valides (12 h au plus) |
| (b) Restauration de tout sauf les données de `session` (recommandée s'il existe une sauvegarde) | même durée ; aucune session n'est réactivée | suppose une sauvegarde valide |
| (c) Pas de restauration, reconstruction : base neuve après un GO, compte accueil par `init_accueil`, comptes membres recréés, réservations ressaisies | seule option possible sans sauvegarde | toutes les données sont perdues ; environ 1 h avant que l'app réponde ; ressaisie par le client |
| (d) Récupération sur le disque | — | écartée : chances faibles, coût élevé, compétence absente |

T-083, communication au client : (1) message immédiat, puis un second après T-081 ; (2) un seul message, plus tard ; (3) texte retouché par Claire.

## Décision
1. **T-081 : option (c), reconstruction.** Aucune restauration n'est possible, faute de sauvegarde. Il ne faut lancer ni `deployer_local.py` ni `rollback_local.py` avant que cette décision soit appliquée selon la procédure de T-081.
2. **T-083 : Claire prévient le client.** Le message annonce la perte totale des données de démonstration, une reprise sous environ 1 h, la cause et les actions correctives. Le `gestionnaire-crise` le rédige dans le rapport d'incident ; Claire le relit et l'envoie.
3. **Retour d'expérience à tracer dans le rapport d'incident et en tickets, par le `chef-de-projet`** :
   1. T-029 (sauvegarde quotidienne) passe en priorité `critique` et devient une dépendance du GO (T-046) ;
   2. un ticket est créé pour vérifier régulièrement qu'une sauvegarde existe et qu'elle se restaure (test de restauration), avec une alerte si elle manque ;
   3. la leçon principale du rapport : **une règle sans preuve d'exécution n'est pas une garantie**.
4. *(v0.1)* T-082 (mise en maintenance) et T-084 (CNIL) ne sont pas tranchés par la v0.1. Ils le sont par la v0.2 (points 5 et 6).

**Décisions complémentaires d'Ethan (v0.2, 2026-11-26, simulation)**

5. **T-084, CNIL** : « l'ESN est sous-traitant ; elle a prévenu le client (T-083) et lui recommande d'inscrire l'incident dans son registre des violations. Données de démonstration, sans fuite : risque faible, notification CNIL probablement non nécessaire, décision laissée au client. » C'est l'option (1) de T-084, sans avis juridique externe. La notification éventuelle revient au client, responsable du traitement (RGPD, art. 33.1), et l'ESN ne fixe aucune échéance à sa place. T-084 est clos.
6. **T-082, mise en maintenance** : clos, devenu sans objet. Le service a été rétabli (simulé) sans décision de maintenance volontaire.
7. **Message au client (T-083)** : « Nous en assumons la responsabilité » est remplacé par « Nous prenons cet incident très au sérieux et avons engagé les actions correctives décrites ci-dessous ». Le paragraphe sur la CNIL formule une recommandation au client, sans fixer d'échéance à sa place.
8. **Allocation de Nadia** : option (A) de T-090. Nadia passe à **30 %** sur `reservation-coworking` jusqu'à la mise en service ; T-090 prévoit le retour à 5 % ensuite, comme le dit `planning.md`. La fiche `equipe/membres/nadia.md` est mise à jour par le coordinateur après cette décision (CLAUDE.md § 5).

## Pourquoi
Les mots d'Ethan : « aucun fichier de sauvegarde n'existe dans deploiement/local/ ; T-029 n'a jamais été réalisé et aucun déploiement n'a eu lieu, donc aucune sauvegarde avant déploiement non plus. On applique donc (c) reconstruire d'office. » Les options (a) et (b) supposent une sauvegarde valide, qui n'existe pas. Pour le retour d'expérience : « une règle sans preuve d'exécution n'est pas une garantie ». Les règles de sauvegarde (DEC-003, DEC-007, DEC-008) étaient écrites et validées, mais rien n'en prouvait l'exécution.

Pour la v0.2, les mots d'Ethan : pour la CNIL, « données de démonstration, sans fuite : risque faible, notification CNIL probablement non nécessaire, décision laissée au client » ; l'ESN est sous-traitant, c'est donc au client, responsable du traitement, de décider. T-082 est « devenu sans objet ». Pour Nadia, l'option (A) de T-090 répond à sa surcharge (128 % de sa capacité avec les actions correctives) et à la dépendance à une seule personne pour la restauration. Le message au client est reformulé pour ne pas engager la responsabilité de l'ESN et ne pas imposer d'échéance au client.

## Impacts
- Fichiers ou règles à mettre à jour :
  - T-080 et le post-mortem `projets/reservation-coworking/rapports/post-mortem-2026-11-26-perte-donnees.md`, complétés par le `gestionnaire-crise` (rapport d'incident complet, message au client, leçon principale) ;
  - aucune règle modifiée.
- Tickets créés ou débloqués :
  - T-081 et T-083 sont à débloquer par l'humain (champ `decision`, statut, ligne de journal) ;
  - T-029 : priorité `critique` ; T-046 : dépendance ajoutée à T-029 (par le `chef-de-projet`, à la demande d'Ethan) ;
  - nouveau ticket de vérification périodique de l'existence et de la restauration des sauvegardes, avec alerte (par le `chef-de-projet`, en `A_FAIRE`) ;
  - *(v0.1)* T-082 et T-084 restent en `ATTENTE_HUMAIN`. **v0.2** : T-084 passe `TERMINE` et T-082 `ANNULE`, sur instruction écrite d'Ethan, écrits par le coordinateur ;
  - **v0.2** : `equipe/membres/nadia.md` (allocation 30 %), `projets/reservation-coworking/projet.md` (allocations, historique), post-mortem v0.3 (message au client, décisions).
