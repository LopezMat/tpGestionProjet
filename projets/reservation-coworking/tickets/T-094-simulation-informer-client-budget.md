---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-094
titre: SIMULATION — Informer le client de la révision du budget
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: relation-client (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Ticket créé dans l'exercice de révision du budget (scénario 2, S1) du 2026-11-26, en application de DEC-020, condition 2. Le client n'a rien annoncé en réalité : aucun message ne doit lui être envoyé hors de l'exercice.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-094 — SIMULATION — Informer le client de la révision du budget

## Description
**Origine.** [DEC-020](../../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md), condition 2 : le message au client explique la répartition entre le retrait de périmètre (F-06) et la prise en charge de la crise par l'ESN. Claire le relit et l'envoie (AF1). Analyse d'impact : [T-093](T-093-simulation-revision-budget-4200.md).

**Ticket salarié (AF11, R15)** : à faire par un humain. Claire reste l'autrice et la responsable du message : elle peut l'adapter et choisit le canal (courriel ou échange suivi d'un écrit). Le coordinateur ne l'envoie pas. Le texte ci-dessous est une **proposition** ; il ne contient aucune donnée personnelle. Les champs entre chevrons sont à compléter par Claire.

**Message proposé** :

> Objet : Réservation des salles, révision du budget et du périmètre
>
> Bonjour,
>
> Suite à votre demande, nous avons revu le projet de réservation des salles pour le ramener à un budget de **4 200 € HT**, au lieu de 6 000 € HT. **La date de livraison du 18 décembre 2026 est maintenue.**
>
> Pour respecter ce nouveau budget, nous vous proposons de retirer une seule fonctionnalité : **les fiches des salles** (affichage de la capacité et des équipements de chaque salle). Les salles resteront affichées sous leur nom (« Salle 1 », « Salle 2 », « Salle 3 »). **Tout le reste du cahier des charges est livré**, y compris la suppression automatique des réservations au bout de 12 mois, qui répond à une exigence du RGPD.
>
> Un incident est survenu le 26 novembre sur notre environnement d'exploitation. **Les coûts liés à cet incident et aux mesures que nous prenons pour qu'il ne se reproduise pas sont entièrement pris en charge par notre société.** Ils n'ont aucun effet sur votre budget.
>
> Le nouveau budget laisse peu de marge. Nous suivons donc la consommation de près : **si un dépassement devient prévisible, nous vous le soumettrons avant d'engager le moindre travail supplémentaire**, en vous proposant soit un avenant, soit le retrait d'un autre élément du périmètre. Aucun dépassement ne vous sera présenté après coup.
>
> Le cahier des charges sera mis à jour (version 1.1) pour acter le retrait des fiches des salles ; nous vous l'adresserons dès qu'il sera prêt.
>
> Je reste à votre disposition pour en parler, par écrit ou lors d'un court échange.
>
> Bien cordialement,
> <signature de Claire>

**Pourquoi ce contenu.** Chaque paragraphe reprend un point de DEC-020 : budget et deadline (point 1) ; retrait de F-06 et maintien de F-08 (point 2) ; prise en charge de la crise par l'ESN (point 3, sans citer l'outillage commun, qui n'a jamais été facturé au client comme tel) ; arbitrage préalable de tout dépassement (condition 1) ; CDC v1.1 (Impacts). Le message ne cite ni montant interne ni ticket.

**Cohérence avec T-083.** La communication de l'incident au client est une décision encore en attente ([T-083](T-083-simulation-decision-communication-client.md), `ATTENTE_HUMAIN`). Le paragraphe sur l'incident doit rester cohérent avec ce qui sera décidé et envoyé dans T-083 : Claire l'ajuste, ou envoie ce message après celui de T-083. Ce ticket ne remplace pas T-083.

**Si le client conteste** (retrait de F-06, répartition des coûts, ou demande de garder F-06) : Claire note sa réponse au journal, et le coordinateur crée un ticket `decision` (R7) ; aucun engagement nouveau n'est pris dans la réponse.

## Critères d'acceptation
- [ ] Claire a relu le message, l'a adapté si besoin et l'a envoyé ; la date, l'heure et le canal de l'envoi sont notés au journal.
- [ ] Le message envoyé contient les cinq points de DEC-020 : budget de 4 200 € HT et deadline du 2026-12-18 tenue ; retrait de F-06 seul, le reste du CDC livré dont la purge à 12 mois ; coûts de la crise pris en charge par l'ESN ; tout dépassement prévisible soumis avant d'être engagé ; CDC v1.1 à venir.
- [ ] La réponse du client (accord, réserve ou contestation) est notée au journal avec sa date ; en cas de réserve ou de contestation, le ticket `decision` créé par le coordinateur est cité.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (communication client, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non (ticket salarié, Claire est l'autrice)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:15 · agent:chef-de-projet · SIMULATION · création en application de DEC-020 (condition 2) : message au client proposé, à relire et envoyer par Claire (AF1, R15) ; assignée à Claire (relation-client expert, allocation 20 %, aucune absence au calendrier, statut actif) ; sans dépendance · 0 h
