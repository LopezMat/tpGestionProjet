---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-083
titre: SIMULATION — Décision communication au client sur la perte de données (T-080)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: critique          # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: relation-client (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine requise (S2-R4 et AF1, communication au client) ; le message 2 attend aussi la décision T-081
validation_humaine_requise: oui   # oui | non
decision:         DEC-019          # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:gestionnaire-crise
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:       2026-11-26           # facultatif : date du passage TERMINE
---
> **SIMULATION** — Exercice de crise (scénario 5, S2) demandé par l'humain le 2026-11-26, ticket incident [T-080](T-080-simulation-perte-base-production.md). Aucun message n'est réellement envoyé au client. Heures simulées.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-083 — SIMULATION — Décision communication au client sur la perte de données (T-080)

## Description
Runbook [perte-donnees](../../../runbooks/perte-donnees.md) § 4, ligne « Informer le client ». Escalade de niveau 3 : données personnelles touchées et indisponibilité visible par le client. L'agent rédige ; **Claire** (`relation-client` expert, interlocutrice client, AF1) envoie, après décision. Aucun agent ne contacte le client.

**Pourquoi maintenant.** Le client (Coworking Les Arcades) est **responsable du traitement**, et l'ESN agit comme **sous-traitant** ([cdc.md](../cdc.md) § 8, Q-08). Un sous-traitant doit notifier toute violation de données personnelles au responsable du traitement **dans les meilleurs délais** après en avoir pris connaissance (RGPD, art. 33.2). Une perte de disponibilité est une violation au sens de l'art. 4.12. Le message 1 tient lieu de cette notification. Il ne dépend pas de [T-081](T-081-simulation-decision-restauration-base.md) et peut partir dès la décision. Le délai de 72 h d'une éventuelle notification à la CNIL court pour le client à partir de ce message ([T-084](T-084-simulation-decision-notification-cnil.md)).

**Question** : faut-il envoyer au client le message 1 (immédiat), puis le message 2 (après la décision T-081), tels que proposés ci-dessous ?

**Options**
- **(1) Envoi en deux temps** : message 1 dès la décision, par e-mail à l'interlocutrice client (fiche projet), doublé d'un appel ; message 2 dès que T-081 est tranché, avec la fenêtre de perte et la durée réelle.
- **(2) Un seul message, après T-081** : plus complet, mais il retarde la notification art. 33.2 et laisse l'accueil sans consigne de repli.
- **(3) Message 1 modifié par Claire** (ton, canal) : la décision porte alors sur le texte final, recopié au journal.

**Recommandation** : **(1)**, avec la liberté de forme de l'option (3) laissée à Claire, sans changer les faits.

**Message 1 proposé (immédiat)**
> Objet : Incident sur l'application de réservation des salles — 26/11/2026
>
> Bonjour,
>
> Ce matin, le 26 novembre vers 10 h, la base de données de l'application de réservation des salles a été supprimée, selon les premiers éléments par erreur lors d'une opération technique sur le poste qui l'héberge (origine en cours de confirmation). L'application est indisponible depuis.
>
> Ce que cela signifie pour vous :
> - les membres et l'accueil ne peuvent plus se connecter ni réserver ;
> - les comptes (nom, adresse e-mail, mot de passe protégé), les réservations et les connexions en cours enregistrés dans l'application ne sont plus accessibles ;
> - rien n'indique que ces données aient été consultées ou copiées par un tiers : il s'agit d'une perte, pas d'une fuite.
>
> Ce que nous faisons : nous vérifions en ce moment les sauvegardes disponibles pour restaurer les données, et l'application reste arrêtée jusqu'à la fin de l'opération pour éviter toute nouvelle perte.
>
> Ce que nous vous proposons d'ici là : noter à la main les réservations de la journée à l'accueil (salle, créneau) ; nous vous aiderons à les ressaisir ensuite.
>
> Deux points pour la suite :
> - vous êtes responsable du traitement de ces données : nous vous transmettrons aujourd'hui les éléments pour décider s'il faut notifier la CNIL (délai de 72 h) ;
> - si des membres ont demandé la suppression de leur compte ces derniers jours, merci de nous indiquer où ces demandes sont consignées, pour qu'elles soient de nouveau appliquées après une éventuelle restauration.
>
> Prochaine information : aujourd'hui avant 12 h, avec la solution retenue et la durée prévue de l'interruption.
>
> Claire, pour l'ESN

**Message 2 proposé (après T-081, à compléter)**
> Objet : Incident sur l'application de réservation — solution retenue
>
> Bonjour,
>
> Suite à notre message de ce matin, voici la solution retenue : [restauration de la sauvegarde du JJ/MM à HH h MM | reconstruction de l'application sans sauvegarde disponible].
> - Données perdues : [les opérations faites entre JJ/MM HH h MM et le 26/11 10 h (réservations, créations ou suppressions de comptes) | l'ensemble des comptes et des réservations enregistrés depuis la mise en service].
> - Ce que les membres devront faire : [se reconnecter | recevoir un nouveau compte de l'accueil, changer leur mot de passe à la première connexion et ressaisir leurs réservations à venir].
> - Retour prévu de l'application : [heure].
> - [Si reconstruction : nous vous accompagnons pour recréer les comptes ; comptez environ 3 minutes par compte.]
>
> Nous vous enverrons sous 2 jours ouvrés un compte rendu de l'incident et les mesures prises pour qu'il ne se reproduise pas.
>
> Claire, pour l'ESN

Aucun nom de membre, aucune adresse ni aucun détail technique interne (nom du volume, commandes) dans les messages.

**Impact chiffré** : Claire, environ 1 h (rédaction finale, envoi, appel, message 2), environ 79 €. L'envoi déclenche pour le client le délai de 72 h de l'art. 33 ; sans envoi, l'ESN manque à son obligation de sous-traitant. Tous les membres et l'accueil sont concernés par le contenu ; ils sont informés par le client, pas par l'ESN.

## Critères d'acceptation
- [x] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [x] Le texte du message 1 effectivement envoyé, son heure et son canal sont recopiés au journal, sans donnée personnelle.
- [x] Le message 2 est envoyé après la décision T-081, avec la fenêtre de perte réelle ; texte, heure et canal au journal.
- [x] La réponse du client sur le registre des demandes de suppression est notée (existe / n'existe pas), pour le rejeu de T-081.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7 ; envoi par un humain, AF1)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 10:14 · agent:gestionnaire-crise · SIMULATION · création (ATTENTE_HUMAIN), messages 1 et 2 proposés, envoi par Claire après décision (AF1) · 0 h
