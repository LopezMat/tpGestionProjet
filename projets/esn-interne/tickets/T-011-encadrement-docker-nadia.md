---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-011
titre: Encadrement de Léa (T-010) — docker
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-012]          # ex. [T-001, T-002]
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

# T-011 — Encadrement de Léa (T-010) — docker

## Description
Temps de formatrice du binôme interne de [T-010](T-010-formation-docker-lea.md) (plan de formation de l'ESN, S1-R13). Proposé par T-001, **soumis à l'arbitrage de [T-017](T-017-decision-plan-formation-initial.md) (DEC-024)**.

- **Formatrice** : Nadia. Séance en binôme (2,5 h, sur les 4 h de binôme de Léa ; Léa travaille seule le reste du temps), puis correction du guide de T-012 à partir des écarts relevés par Léa et attestation (0,5 h).
- **Fenêtre** : du 2026-12-29 au 2027-01-12 (pas le mercredi).
- **Coût** : 3 h × 64,29 €/h = **192,86 €**.
- Pas de `depend_de` vers T-010 (les deux se font ensemble, même principe qu'AF3) ; il dépend de T-012 (le guide).

## Critères d'acceptation
- [ ] La séance en binôme est faite ; son contenu est noté au journal de T-010.
- [ ] Les écarts relevés par Léa sont corrigés dans le guide de T-012 (nouvelle version, ligne au journal).
- [ ] L'attestation de niveau de Léa est écrite au journal de T-010.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (encadrement de formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:45 · agent:chef-de-projet · création (T-001, temps de formatrice de T-010) ; en attente de DEC-024 (T-017) · 0 h
