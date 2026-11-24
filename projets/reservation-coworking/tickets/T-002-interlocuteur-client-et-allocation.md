---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-002
titre: Interlocuteur client et allocation initiale
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet        # agent:<nom> | salarie:<prenom>
competence_requise: planification (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur l'interlocuteur client et son allocation au projet (AF1, S1-R10)
validation_humaine_requise: oui   # oui | non
decision:     DEC-005              # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-002 — Interlocuteur client et allocation initiale

## Description
**Question.** Quel salarié est l'interlocuteur client du projet `reservation-coworking` (cadrage, réponses aux questions ouvertes du CDC, recette avec le client), et avec quelle allocation de sa capacité ?

**Options.**
1. **Claire à 10 %** (3,5 h/semaine) : seule salariée `relation-client`, au niveau `expert` ; aucune absence au calendrier ; allocation actuelle vide (0 %).
2. **Claire à 20 %** (7 h/semaine) : la même, avec plus de marge pour la recette et les échanges avant la deadline du 2026-12-18.
3. **Un autre salarié** : aucun autre membre n'a la compétence `relation-client` (AF1 non satisfait) ; à n'envisager qu'avec un ticket `formation`.

**Recommandation.** Option 1, **Claire à 10 %**. Elle remplit AF1 (relation-client, au moins confirme) et AF8 (disponible, allocation libre). Le projet est petit (3 salles, budget 6 000 €) : 10 % suffisent au cadrage et aux questions ; l'allocation pourra être relevée au moment de la recette si besoin (AF9).

**Impact.**
- Coût horaire de Claire : 550 €/j ÷ 7 = **78,57 €/h**. À 10 % sur les ~4 semaines restantes (environ 14 h), ≈ **1 100 €**, soit ~18 % du budget ; à 20 %, ≈ 2 200 € (~37 %). Ce coût n'est imputé qu'au temps réellement passé sur des tickets.
- Capacité restante de Claire : 90 % (option 1) ou 80 % (option 2) pour les autres projets.
- Claire est aussi la candidate naturelle pour la recette humaine (`recette-fonctionnelle` confirme), qui sera décidée au planning.
- Dépendance à une seule personne pour la relation client (déjà signalée dans sa fiche, AF10 b).

## Critères d'acceptation
- [ ] Un humain a choisi l'interlocuteur client et le pourcentage d'allocation.
- [ ] Le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans le champ `decision`.
- [ ] `equipe/membres/<prenom>.md` (allocation) et `projet.md` (`salaries_affectes`) sont mis à jour par le coordinateur après la décision.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 13:49 · agent:coordinateur · création · 0 h
- 2026-11-24 · salarie:ethan · décision prise (DEC-005) · 0 h