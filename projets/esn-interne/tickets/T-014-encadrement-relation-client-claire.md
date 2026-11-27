---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-014
titre: Encadrement de Léa (T-013) — relation client
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: relation-client (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-017]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-014 — Encadrement de Léa (T-013) — relation client

## Description
Temps de formatrice du binôme interne de [T-013](T-013-formation-relation-client-lea.md) (plan de formation de l'ESN, S1-R13). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 7 de priorité**. Allocation de Claire à `esn-interne` : 5 % en P1, **0 % en P2** : ce ticket doit être `TERMINE` au plus tard le 2026-12-18, sinon il devient non planifiable après la bascule du 2026-12-21.

Ce ticket ne compte que la préparation et le débriefing de chaque échange avec Léa, et l'attestation (1 h). Le temps de l'échange lui-même reste dans le ticket du client (`T-094`, `T-009`, `T-046`, `T-091`).

- **Formatrice** : Claire. **Fenêtre** : du 2026-11-30 au 2026-12-18.
- **Coût** : 1 h × 78,57 €/h = **78,57 €**.
- Pas de `depend_de` vers T-013 (les deux se font ensemble, même principe qu'AF3).

## Critères d'acceptation
- [ ] Chaque échange suivi par Léa a une préparation et un débriefing notés au journal de T-013.
- [ ] L'attestation de niveau (atteint ou non, avec la raison) est écrite au journal de T-013.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (encadrement de formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:00 · agent:chef-de-projet · création (T-001, temps de formatrice de T-013) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 7) ; TERMINE au plus tard le 2026-12-18 (Claire à 0 % en P2) (T-016) · 0 h
