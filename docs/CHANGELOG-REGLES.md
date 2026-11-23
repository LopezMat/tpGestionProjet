---
titre: Historique des modifications de règles
statut: EN_REVUE          # journal, jamais VALIDÉ (évolue uniquement par PR, exclu de R6)
responsable: B
version: 0.2
maj_le: 2026-11-23
valide_par:
decision:
---

# Historique des modifications de règles

Toute modification d'une règle (CLAUDE.md, docs/systemes/, agents, skills, templates, settings) ajoute une ligne ici, **dans la même PR** que la modification et le fichier de décision (R11).
*Pourquoi :* la consigne prévoit que la situation change en cours de semaine et que ce sont les humains qui modifient les règles ; ce journal permet de montrer en soutenance comment le système s'est adapté, et pourquoi.

| Date | Règle modifiée | Ancien | Nouveau | Pourquoi | Événement déclencheur | Décision |
|---|---|---|---|---|---|---|
| 2026-11-23 | v0 — ensemble des règles initiales (R1–R13, S1-R*, S2-R*, S3-R*, S4-R*, en-tête standard, formats ticket et membre) | — | création | mise en place du socle à partir de la vision et des arbitrages de l'équipe | démarrage du projet (Lot 1) | [DEC-001](decisions/2026-11-23-DEC-001-arbitrages-plan-initial.md) |
| 2026-11-23 | Garde-fous de validation (ARCHITECTURE § 6, `_ENTETE.md`, R5) | contrôle de la valeur littérale `VALIDÉ` | valeur normalisée (accents, majuscules) ; la CI refuse tout statut hors `BROUILLON` / `EN_REVUE` / `VALIDÉ` | `VALIDE` sans accent contournait le hook | revue du Lot 1 | [DEC-001 § 23](decisions/2026-11-23-DEC-001-arbitrages-plan-initial.md#23-normalisation-du-statut-validé) |
| 2026-11-23 | R6 (CLAUDE.md, `_ENTETE.md`, ARCHITECTURE § 6) | tout document peut passer `VALIDÉ` et est alors figé | les journaux (CHANGELOG-REGLES, registre des décisions) ne passent jamais `VALIDÉ`, évoluent par PR et sont exclus de R6 ; l'état des lots passe dans le README | un journal figé empêcherait de tracer les décisions suivantes | revue du Lot 1 | [DEC-001 § 24](decisions/2026-11-23-DEC-001-arbitrages-plan-initial.md#24-les-journaux-ne-sont-jamais-validés) |
| 2026-11-23 | Permissions prévues (S3 § 5, ARCHITECTURE § 6) | templates sans protection | `ask` sur `Write(templates/**)` et `Edit(templates/**)` | les templates restent en BROUILLON, donc hors R6, alors que `tableau.py` et les agents dépendent de leur format | revue du Lot 1 | [DEC-001 § 25](decisions/2026-11-23-DEC-001-arbitrages-plan-initial.md#25-protection-des-templates) |
