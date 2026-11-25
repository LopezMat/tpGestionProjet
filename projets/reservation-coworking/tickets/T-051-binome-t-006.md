---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-051
titre: Binôme T-006 (pilotage et revue humaine)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-050]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-051 — Binôme T-006 (pilotage et revue humaine)

## Description
> **ANNULE le 2026-11-25 : déplacé vers les règles de l'ESN (PR de règles)**, avec T-006 (Ethan, 2026-11-24, DEC-009, point D1 ; DEC-010). Le binôme sera recréé, si besoin, dans le projet interne de l'ESN.

Binôme de [T-006](T-006-ecritures-md-par-edit-uniquement.md) (AF7 : Hugo, `backend-python` débutant, sur un ticket qui demande le niveau confirmé ; AF5 par analogie, T-006 touchant un garde-fou de sécurité). Karim (`backend-python` expert, `securite-applicative` confirmé) cadre l'approche de détection, relit le code et les tests, et **tient lieu de revue humaine** de T-006 (S3-R2) : il n'en est pas l'auteur. Prenable quand T-050 est tranché (option 1 ou 3) ; la revue finale a lieu quand T-006 passe `EN_REVUE` (pas de `depend_de` vers T-006, AF3).

Lot ESN (hors budget client, voir T-007 point D). **Ticket salarié (AF11, R15)** : à faire par un humain. **Affectation conditionnelle** à l'allocation de Karim proposée dans T-007.

## Critères d'acceptation
- [ ] L'approche de détection (formes refusées, chemins visés, limites) est fixée avec Hugo avant le code, et notée au journal de T-006.
- [ ] La ligne « Revue humaine » de T-006 est remplie par Karim : prénom, date, avis.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de binôme)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création au tri de T-006 ; affectation conditionnelle à l'allocation de Karim proposée dans T-007 · 0 h
- 2026-11-25 09:00 · agent:chef-de-projet · statut A_FAIRE → ANNULE : déplacé vers les règles de l'ESN (PR de règles) (Ethan, 2026-11-24, DEC-009, point D1 ; DEC-010) ; temps compté dans T-008 · 0 h
