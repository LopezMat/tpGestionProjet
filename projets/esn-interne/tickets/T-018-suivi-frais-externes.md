---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-018
titre: tableau.py ne suit pas les frais externes (devis, factures de formation) ; proposer un suivi de l'enveloppe de DEC-024
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: suivi-budget (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-018 — tableau.py ne suit pas les frais externes ; proposer un suivi de l'enveloppe de DEC-024

## Description
Ticket créé le 2026-11-27 à la demande d'Ethan, lors de la décision sur [T-017](T-017-decision-plan-formation-initial.md) ([DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md), point 4).

**Constat.** `scripts/tableau.py` ne chiffre que des heures (`estimation_h`, `temps_passe_h` × taux, R12). Les frais externes ne sont suivis nulle part de façon calculée : devis et factures d'une formation externe, d'un conseil juridique, etc. DEC-024 les a donc sortis de `budget_eur` dans une enveloppe séparée de 700 € HT (formation « supervision » de Nadia, T-002), pour ne pas fausser l'alerte à 90 % de S1-R11. En attendant, cette enveloppe n'est suivie qu'à la main, dans `planning.md`. C'est le type de calcul manuel qui a dérivé dans T-008 de `reservation-coworking` (DEC-023).

**Attendu : une proposition, pas une réalisation.** Le `chef-de-projet` rédige dans ce ticket une proposition de suivi de l'enveloppe et la soumet à un humain par un ticket `decision` `ATTENTE_HUMAIN`. Elle doit au moins comparer :
- un suivi manuel structuré dans `planning.md` (tableau devis / engagé / facturé, une ligne de journal par mouvement) ;
- un champ ou un fichier lu par `tableau.py` (par exemple des frais par ticket, ou un registre des frais par projet), avec la section correspondante dans `TABLEAU.md` et `PORTFOLIO.md` et une alerte sur l'enveloppe ;
- le cas échéant, une autre piste.

Pour chaque piste : ce qui est suivi (devis, engagé, facturé), qui l'écrit, l'alerte (seuil, enveloppe), l'effet sur R9 et R18, les fichiers touchés et l'estimation de réalisation.

Toute modification du format des tickets (`templates/ticket.md`, champs lus par `tableau.py`) ou de `scripts/tableau.py` est une modification d'outil et de règle commune : PR, fichier `DEC-NNN` et entrée dans `docs/CHANGELOG-REGLES.md` (R11). Elle ne se réalise pas dans ce ticket.

## Critères d'acceptation
- [ ] La proposition est écrite dans ce ticket : au moins deux pistes comparées (suivi, rédacteur, alerte, effet sur R9 et R18, fichiers touchés, estimation).
- [ ] Un ticket `decision` `ATTENTE_HUMAIN` est créé dans `projets/esn-interne/tickets/`, au format R7 (question, options, recommandation, impact).
- [ ] D'ici la décision, l'enveloppe de DEC-024 est suivie dans `projets/esn-interne/planning.md` (montant, devis, engagé, facturé).
- [ ] Aucune modification de `scripts/tableau.py` ni de `templates/` dans ce ticket (R11).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (proposition, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 · agent:coordinateur · création à la demande d'Ethan (décision sur T-017, DEC-024 point 4) · 0 h
