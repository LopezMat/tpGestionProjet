---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-007
titre: Encadrement de Léa (T-006) — recette fonctionnelle
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: recette-fonctionnelle (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
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

# T-007 — Encadrement de Léa (T-006) — recette fonctionnelle

## Description
Temps de formatrice du binôme interne de [T-006](T-006-formation-recette-lea.md) (plan de formation de l'ESN, S1-R13). Proposé par T-001, **soumis à l'arbitrage de [T-017](T-017-decision-plan-formation-initial.md) (DEC-024)**.

Ce ticket ne compte que le temps d'explication et l'attestation (1 h). Le temps de recette de Claire reste dans `reservation-coworking/T-045`, au budget du client ; le surplus dû à la formation ne doit pas y être reporté.

- **Formatrice** : Claire. **Fenêtre** : du 2026-12-10 au 2026-12-15 (pendant T-045).
- **Coût** : 1 h × 78,57 €/h = **78,57 €**.
- Pas de `depend_de` vers T-006 (les deux se font ensemble, même principe qu'AF3).

## Critères d'acceptation
- [ ] Un débriefing par parcours fait en binôme est noté au journal de T-006.
- [ ] L'attestation de niveau (atteint ou non, avec la raison) est écrite au journal de T-006.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (encadrement de formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:25 · agent:chef-de-projet · création (T-001, temps de formatrice de T-006) ; en attente de DEC-024 (T-017) · 0 h
