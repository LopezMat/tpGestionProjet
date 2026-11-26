---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-NNN
titre: <titre court>
projet: <slug>
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:<nom>        # agent:<nom> | salarie:<prenom>
competence_requise: <nom> (<niveau>)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: <agent:<nom> | salarie:<prenom>>
cree_le: AAAA-MM-JJ
maj_le: AAAA-MM-JJ
statut_depuis: AAAA-MM-JJ   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: client          # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-NNN — <titre>

## Description
<contexte, ce qui est attendu ; pour un bug : étapes de reproduction, résultat attendu / obtenu>

## Critères d'acceptation
- [ ] <critère vérifiable>
- [ ] <critère vérifiable>

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : <APPROUVÉ | CHANGEMENTS_DEMANDÉS>
- **Commentaires** :
- **Revue humaine requise** : <oui si priorite = critique ou si le ticket touche la sécurité | non>
- **Revue humaine** : <prénom, date, avis>

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- AAAA-MM-JJ HH:MM · <qui> · création · 0 h
