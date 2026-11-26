---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-091
titre: SIMULATION — Registre des demandes de suppression chez le client avant la mise en service
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
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
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-9 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-091 — SIMULATION — Registre des demandes de suppression chez le client avant la mise en service

## Description
Proposition **P-9** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md). Après une restauration, les suppressions de comptes demandées depuis l'heure de la sauvegarde sont rejouées par l'accueil, à partir du **registre des demandes tenu par le client**, qui est responsable du traitement ([architecture.md](../architecture.md) § 8 « Restauration » ; [T-081](T-081-simulation-decision-restauration-base.md), point 5). L'app ne garde volontairement aucun journal persistant des suppressions. Sans ce registre, une restauration réintroduirait des comptes supprimés sur demande, ce qui serait un manquement RGPD du client.

**Attendu** :
- Claire obtient du client (Marie Lenoir) la confirmation écrite qu'un registre des demandes de suppression existe, et où il est tenu ; sinon, elle lui recommande d'en ouvrir un avant la mise en service ;
- la procédure de rejeu (qui, à partir de quoi, dans quel délai après une restauration) est notée, **sans aucune donnée personnelle**, dans T-048 ou dans le README de l'app.

**Lien avec [T-009](T-009-points-client.md)** (points client, `A_FAIRE`, même interlocutrice) : ce point aurait pu y figurer, mais aucun ticket existant n'est modifié pendant la pause. Ce ticket ne fait pas doublon : T-009 traite la mention d'information et l'exercice des droits, pas le registre. Les deux peuvent être traités dans le même échange avec le client, et leur fusion peut être décidée au triage.

**Affectation : `salarie:claire`, proposition du `gestionnaire-crise` conservée.**
- **Contact client (AF1).** Il revient à un salarié qui a `relation-client` au niveau `confirme` au moins. Claire est `expert`, interlocutrice désignée (DEC-005), allouée à 20 % (DEC-009), `actif` et sans absence prévue (AF8). Elle a aussi `rgpd` `confirme`.
- **Charge.** Son utilisation, ce ticket compris, est de 38 % sur la période : sous 50 %, c'est signalé dans [T-090](T-090-simulation-planning-sans-sauvegarde.md) (AF9). Ce ticket n'est pas créé pour remonter ce taux : il découle de la proposition P-9.
- **Ticket salarié (AF11, R15)** : à faire par un humain ; le coordinateur ne contacte jamais le client lui-même.

**Échéance** : avant la mise en service (T-048). L'ajout de ce ticket à `depend_de` de T-048 est proposé dans T-090. **Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] Le client confirme par écrit l'existence du registre et son emplacement (date et canal notés au journal, sans aucune donnée personnelle), ou la recommandation d'en ouvrir un lui est transmise et sa réponse est notée.
- [ ] La procédure de rejeu des suppressions après une restauration est notée dans T-048 ou dans le README de l'app, sans aucune donnée personnelle.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (relation client)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-9 ; assignée à Claire (AF1, relation-client expert) ; pas un doublon de T-009 (fusion possible au triage) ; non planifié (développement en pause) · 0 h
