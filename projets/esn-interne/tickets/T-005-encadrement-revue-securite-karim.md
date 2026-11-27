---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-005
titre: Encadrement de Léa (T-004) — revues humaines et sécurité
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
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

# T-005 — Encadrement de Léa (T-004) — revues humaines et sécurité

## Description
Temps de formateur du binôme interne de [T-004](T-004-formation-revue-humaine-lea.md) (plan de formation de l'ESN, S1-R13). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 1 de priorité**. Allocation de Karim à `esn-interne` : 5 % en P1.

Ce ticket rend visible le temps d'explication de Karim, qui n'a pas à peser sur le budget du client : ses revues de `reservation-coworking` restent dans leurs tickets, au même temps. Ici ne sont comptés que la relecture de la grille de T-003 (0,5 h), les débriefings des revues en double (1 h) et l'attestation (0,5 h).

- **Formateur** : Karim (`securite-applicative` confirmé, `revue-code` expert). **Fenêtre** : du 2026-12-04 au 2026-12-11 ; **au plus tard le 2026-12-18** (EV-003).
- **Coût** : 2 h × 78,57 €/h = **157,14 €**.
- **Pas de `depend_de` vers T-003 ni T-004** (même principe que AF3) : T-003 ne peut passer `TERMINE` qu'après la relecture de sa grille par Karim, qui est comptée ici ; une dépendance bloquerait les deux tickets. Ce ticket devient prenable quand T-003 passe `EN_REVUE`.

## Critères d'acceptation
- [ ] La grille de T-003 est relue (ligne au journal de T-003).
- [ ] Chaque revue en double de T-004 a un débriefing noté au journal de T-004.
- [ ] L'attestation de niveau (atteint ou non, avec la raison) est écrite au journal de T-004.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (encadrement de formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:15 · agent:chef-de-projet · création (T-001, temps de formateur de T-004) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 1) ; à conclure avant le 2026-12-18 (EV-003) (T-016) · 0 h
