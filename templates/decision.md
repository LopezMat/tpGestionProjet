---
titre: <sujet de la décision>
statut: EN_REVUE
responsable: <A|B|C|D>
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:                 # rempli par l'humain qui valide
decision: DEC-NNN           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-NNN
date: AAAA-MM-JJ
decide_par: <prénom(s) ou « équipe »>
projet: <slug | ESN>
ticket: <T-NNN si la décision débloque un ticket>
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-NNN — <sujet>

## Contexte
<situation, déclencheur (événement, ticket, question)>

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|

## Décision
<ce qui est décidé, formulé comme une règle applicable>

## Pourquoi
<justification, défendable à l'oral>

## Impacts
- Fichiers ou règles à mettre à jour :
- Tickets créés ou débloqués :
