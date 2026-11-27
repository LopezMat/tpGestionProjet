---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-009
titre: Encadrement de Karim (T-008) — sauvegarde et restauration
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
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

# T-009 — Encadrement de Karim (T-008) — sauvegarde et restauration

## Description
Temps de formatrice du binôme interne de [T-008](T-008-formation-sauvegarde-restauration-karim.md) (plan de formation de l'ESN, S1-R13). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 2 de priorité**. Allocation de Nadia à `esn-interne` : 20 % en P2.

- **Formatrice** : Nadia. Elle prépare la base jetable et la sauvegarde d'exercice (0,5 h), observe la restauration de Karim sans intervenir (1 h), puis corrige le guide de T-012 à partir des écarts relevés et atteste le niveau (0,5 h).
- **Fenêtre** : du 2027-01-04 au 2027-01-13, en même temps que T-008 (pas le mercredi).
- **Coût** : 2 h × 64,29 €/h = **128,57 €**.
- Pas de `depend_de` vers T-008 (les deux se font ensemble, même principe qu'AF3) ; il dépend de T-012 (le guide).

## Critères d'acceptation
- [ ] La base jetable et la sauvegarde d'exercice sont prêtes, sans donnée réelle d'un client.
- [ ] Les écarts relevés par T-008 sont corrigés dans le guide de T-012 (nouvelle version, ligne au journal).
- [ ] L'attestation de niveau de Karim est écrite au journal de T-008.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (encadrement de formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:35 · agent:chef-de-projet · création (T-001, temps de formatrice de T-008) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 2) ; fenêtre inchangée (2027-01-04 → 2027-01-13, avec T-008) (T-016) · 0 h
