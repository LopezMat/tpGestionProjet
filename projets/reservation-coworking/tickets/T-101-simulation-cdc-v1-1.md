---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-101
titre: SIMULATION — Révision du CDC v1.1 (DEC-020)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:analyste-besoin   # agent:<nom> | salarie:<prenom>
competence_requise: redaction-cdc (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Ticket de travail de la révision du CDC v1.1 qui suit la révision du budget simulée (scénario 2, DEC-020).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-101 — SIMULATION — Révision du CDC v1.1 (DEC-020)

## Description
Ticket de travail de l'`analyste-besoin` (R14) pour la v1.1 de [cdc.md](../cdc.md), repassé `EN_REVUE` par Ethan après [DEC-020](../../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md). Contenu de la v1.1 :
- F-06 abandonné (Exclu) ;
- F-08 obligatoire, par exception à la règle de DEC-009 ;
- budget de 4 200 € HT, deadline du 2026-12-18 inchangée ;
- condition d'alerte à 90 % et arbitrage avant tout dépassement ;
- H-20, Q-05, Q-09 et Q-15 annotées.

**Créé après coup** : le coordinateur a lancé l'analyste sans créer ce ticket au préalable, contrairement à R14. Il le crée pour rattacher le temps passé.

## Critères d'acceptation
- [x] `cdc.md` v1.1 en `EN_REVUE`, `valide_par` et `decision` vides, bandeau SIMULATION, historique qui cite DEC-020.
- [x] F-06 Exclu, F-08 obligatoire, budget de 4 200 € et condition d'alerte présents dans les § 2, 4, 9, 10, 11 et 12.
- [ ] La v1.1 est validée par Ethan (`statut`, `valide_par`, `decision` renseignés par lui).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non (la validation du CDC est humaine, R5)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 20:30 · agent:coordinateur · SIMULATION · création après coup (écart à R14 : ticket non créé avant le lancement de l'analyste) ; temps de l'analyste reporté · 0 h
- 2026-11-26 20:30 · agent:analyste-besoin · SIMULATION · CDC v1.1 rédigé d'après DEC-020 (§ 2, 4, 9, 10, 11, 12, 13 et historique) ; en attente de validation par Ethan ; ligne reportée par le coordinateur · 0,5 h
