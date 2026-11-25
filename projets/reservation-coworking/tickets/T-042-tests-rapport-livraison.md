---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-042
titre: Tests (2/2) — rapport de tests de la livraison
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:testeur      # agent:<nom> | salarie:<prenom>
competence_requise: tests-e2e (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010, T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026, T-027, T-028, T-041]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-042 — Tests (2/2) — rapport de tests de la livraison

## Description
Second volet du ticket « Tests » : campagne complète sur le **SHA candidat** de la livraison, une fois tous les tickets de réalisation `TERMINE` (unitaires, intégration sur PostgreSQL réel, bout en bout T-026, non-régression), et `rapports/tests-AAAA-MM-JJ.md` (template `rapport-tests.md`), lu par la recette (T-045), le GO (T-046) et le `deployeur`. Le seuil de couverture proposé à l'architecture (80 % sur `regles` et `auth`) est vérifié. Le coordinateur conclut (R13).

## Critères d'acceptation
- [ ] Toutes les suites prévues par le CDC § 7 et l'architecture sont lancées sur un SHA noté ; chaque commande et son résultat sont relevés.
- [ ] `rapports/tests-AAAA-MM-JJ.md` existe, en `EN_REVUE`, avec le SHA testé et un verdict `CONFORME` ou `NON CONFORME` justifié.
- [ ] La couverture de `regles` et `auth` est relevée dans le rapport.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
