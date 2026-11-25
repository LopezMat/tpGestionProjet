---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-074
titre: Revue humaine T-073 (en-têtes sur la 500 interne)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.25          # heures équivalent humain, quel que soit l'assigné
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

# T-074 — Revue humaine T-073 (en-têtes sur la 500 interne)

## Description
Revue humaine (S3-R2, AF3) de [T-073](T-073-en-tetes-securite-erreur-500.md), écrit par `agent:dev-backend` : Karim n'en est pas l'auteur (S3-R1). **Pas de `depend_de` vers T-073** (dépendance circulaire, AF3) : ce ticket devient prenable quand T-073 passe `EN_REVUE`. **À faire dans la même séance que la revue humaine de T-063 (T-064)**, dès que T-073 est livré : T-013, premier ticket du chemin critique de `dev-backend`, dépend de T-073, qui ne passe `TERMINE` qu'après cette revue.

Points à confirmer : la 500 porte les en-têtes, l'ordre des middlewares garde le contrôle d'hôte avant toute route, et la limite des 400 émises par Uvicorn hors application (constat 16, jugée acceptable par le `securite`) est acceptée.

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-073 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] L'acceptation (ou non) de la limite des 400 Uvicorn sans en-têtes est écrite dans cette ligne.
- [ ] Chaque réserve donne un commentaire à traiter dans T-073 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 16:40 · agent:chef-de-projet · création · 0 h
