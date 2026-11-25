---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-052
titre: Formation Hugo — backend-python (binôme T-006)
projet: reservation-coworking
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: basse             # critique | haute | normale | basse
assigne: salarie:hugo       # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-050]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-052 — Formation Hugo — backend-python (binôme T-006)

## Description
> **ANNULE le 2026-11-25 : déplacé vers les règles de l'ESN (PR de règles)**, avec T-006 (Ethan, 2026-11-24, DEC-009, points D1 et E ; DEC-010). Le besoin de formation reste à inscrire au plan de formation de l'ESN (projet interne), hors budget client.

Besoin de formation détecté par AF7 et AF10 (c) : Hugo est affecté à [T-006](T-006-ecritures-md-par-edit-uniquement.md), qui demande `backend-python` confirmé, alors qu'il est débutant.
- **Compétence** : `backend-python` ; **niveau actuel** : débutant ; **niveau visé** : confirmé (étape vers).
- **Ticket déclencheur** : T-006 ; binôme T-051 (Karim, expert).
- **Modalité** : binôme interne (formation sur le tas, le temps de réalisation est compté dans T-006) ; ce ticket compte le temps propre à la formation : débriefing avec Karim après la revue, lecture ciblée (tests `pytest` paramétrés, expressions régulières, hooks Claude Code).
- **Coût estimé** : 1 h × 50,00 €/h = **50,00 €** (Hugo) ; le temps de Karim est dans T-051.
- **Budget** : lot ESN, hors budget client (T-007, point D). **Affectation conditionnelle** à l'allocation de Hugo proposée dans T-007.

## Critères d'acceptation
- [ ] Le débriefing avec Karim a eu lieu ; les points de progrès sont notés au journal.
- [ ] La fiche de Hugo (`equipe/membres/hugo.md`, section « Formations ») est mise à jour par le coordinateur, avec le niveau atteint décidé par un humain.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création au tri de T-006 (AF7, AF10 c) ; affectation conditionnelle à l'allocation de Hugo proposée dans T-007 · 0 h
- 2026-11-25 09:00 · agent:chef-de-projet · statut A_FAIRE → ANNULE : déplacé vers les règles de l'ESN (PR de règles) (Ethan, 2026-11-24, DEC-009, points D1 et E ; DEC-010) ; Hugo à 0 % sur ce projet ; temps compté dans T-008 · 0 h
