---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-045
titre: Recette de la livraison
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: recette-fonctionnelle (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-009, T-010, T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026, T-027, T-028, T-030, T-031, T-032, T-033, T-034, T-035, T-036, T-037, T-042, T-043, T-044]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-045 — Recette de la livraison

## Description
Recette humaine (porte 3 bis de S3, S3-R9, CLAUDE.md R16) de la livraison unique du projet : F-01, F-02, F-03, F-04, F-07 (Must), puis F-06 et F-08 (Should), critères recopiés mot pour mot du CDC v1.0, skill [recette](../../../.claude/skills/recette/SKILL.md), **variante sans Claude Code** (DEC-004) : Claire rédige elle-même `rapports/recette-AAAA-MM-JJ.md` et dépose une note par KO dans `support/entrant/` ; le coordinateur crée le ticket « Support utilisateurs » s'il n'existe pas, puis lance `support`.

**Affectation.** Toujours un salarié (règle 6 du `chef-de-projet`, exception à AF6) qui a `recette-fonctionnelle` au moins confirmé et n'est l'auteur d'aucun ticket de la livraison : **Claire** est la seule. Si Marie Lenoir assiste (T-009), AF1 s'applique aussi. Les revues humaines de Karim (T-030 à T-037) figurent dans les dépendances : les tickets de réalisation ne peuvent pas être `TERMINE` sans elles (R13). T-029 (outillage, hors app) n'est pas dans le périmètre de la recette ; il conditionne le déploiement (T-047).

**Ticket salarié (AF11, R15)** : à faire par un humain ; Claire passe elle-même ce ticket `TERMINE` si le verdict est `CONFORME` (R13). Estimation : 5 h pour une quarantaine de critères et les 13 parcours du CDC § 7 ; un re-test après correction est couvert par la marge de risque du planning.

## Critères d'acceptation
- [ ] Le SHA candidat est le même dans les rapports de tests (T-042), de sécurité (T-043) et de recette, et dans la sonde de santé (T-044).
- [ ] Chaque critère d'acceptation des exigences de la livraison a une ligne dans le rapport ; les critères des Must sont tous `OK` ou `KO`, jamais vides.
- [ ] Chaque KO a sa note dans `support/entrant/` et son ticket `bug` lié.
- [ ] `rapports/recette-AAAA-MM-JJ.md` est en `EN_REVUE`, avec un verdict `CONFORME` ou `NON CONFORME` conforme à S3-R9.
- [ ] Le journal de ce ticket porte le verdict, le SHA, le nombre de critères OK et KO, et le temps.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (recette humaine)
- **Commentaires** :
- **Revue humaine requise** : non (la recette est elle-même une porte humaine)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
