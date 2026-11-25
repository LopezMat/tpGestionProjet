---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-064
titre: Revue humaine T-063 (en-têtes de sécurité et Host)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-064 — Revue humaine T-063 (en-têtes de sécurité et Host)

## Description
Revue humaine (S3-R2, AF3) de [T-063](T-063-en-tetes-securite-host.md), écrit par `agent:dev-backend` : Karim n'en est pas l'auteur (S3-R1). **Pas de `depend_de` vers T-063** (dépendance circulaire, AF3) : ce ticket devient prenable quand T-063 passe `EN_REVUE`. La revue de T-013 (T-030) n'a plus à revoir la pose de ces en-têtes, seulement leur présence sur les routes d'authentification.

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-063 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] La CSP est conforme à l'architecture § 6 et la liste des hôtes acceptés ne dépend d'aucune entrée de la requête.
- [ ] Chaque réserve donne un commentaire à traiter dans T-063 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création · 0 h
