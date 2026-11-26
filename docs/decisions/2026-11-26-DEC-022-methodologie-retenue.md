---
titre: Méthodologie retenue (Kanban à portes de validation humaines, livraisons incrémentales)
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-26
valide_par:      Ethan           # rempli par l'humain qui valide
decision: DEC-022           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-022
date: 2026-11-26
decide_par: l'équipe (Johan à l'initiative)
projet: ESN
ticket:
modifie_une_regle: non      # § 3.5 de VISION.md nomme et décrit des pratiques déjà régies par des règles existantes ; aucune règle n'est créée ni modifiée (voir « Impacts »)
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-022 — Méthodologie retenue

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir du § 3.5 de [VISION.md](../VISION.md), écrit par Johan (branche `docs/methodologie`, PR #21) et complété par le coordinateur à la demande d'Ethan. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. Le « Pourquoi » est repris du § 3.5.
>
> **Numérotation.** Le 2026-11-26, avant le commit, DEC-022 était libre dans `docs/decisions/` et sur toutes les branches locales et distantes.

## Contexte
Le professeur a noté : « Méthodologie : partiel, aucune méthode nommée ; fonctionnement par tickets et validations humaines ». Le dépôt appliquait déjà des pratiques de plusieurs méthodes (flux de tickets, portes de validation, incréments, retours d'expérience), mais aucun document ne nommait la méthode, ne disait d'où venait chaque pratique ni ce qui remplaçait les rituels habituels.

Johan a ajouté le § 3.5 « Méthodologie » à `VISION.md` : méthode nommée, tableau « méthode → ce que nous en reprenons → où c'est appliqué », et le « Pourquoi ». Le coordinateur l'a complété par la Definition of Done, les équivalents des rituels et des exemples tirés de la semaine (« La méthode appliquée cette semaine »).

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| Méthode unique : Scrum | méthode connue, vocabulaire partagé (sprint, backlog, mêlée quotidienne, revue, rétrospective) | les cérémonies supposent une équipe humaine qui se réunit, ce que des agents IA ne font pas ; des sprints d'une ou deux semaines n'ont pas de sens sur un projet d'une semaine ; Scrum ne dit rien des validations humaines, du déploiement vérifié ni de la gestion de crise exigés par la consigne |
| Méthode unique : cycle en V | une vérification en face de chaque étape de conception (CDC ↔ recette, architecture ↔ tests) ; validations formelles | séquentiel : aucune livraison avant la fin, donc rien à montrer en soutenance ; s'adapte mal aux changements imposés en cours de semaine (budget revu, départ, incident) |
| **Combinaison retenue : Kanban à portes de validation humaines, livraisons incrémentales** | chaque pratique répond à une exigence précise de la consigne (voir « Pourquoi ») ; correspond à ce que le dépôt applique déjà, preuves à l'appui | méthode « composée » qu'il faut expliquer à l'oral ; pas de cadence fixe, compensée par les équivalents des rituels déclenchés par le flux |

## Décision
1. **La méthode de l'ESN est un Kanban à portes de validation humaines, avec des livraisons incrémentales**, décrite au [§ 3.5 de VISION.md](../VISION.md#35-méthodologie). Elle combine Kanban, l'agile itératif et incrémental, des portes de validation inspirées du cycle en V, MoSCoW, la planification par dépendances, le suivi budgétaire à terminaison, DevOps, le principe des quatre yeux, les ADR et la gestion des incidents (ITIL, SRE).
2. **La Definition of Done d'un ticket** reprend les règles existantes : tous les critères d'acceptation cochés (S1-R4, R13) ; vérification par quelqu'un d'autre que l'auteur (R13, S3-R1), le `testeur` pour un ticket de réalisation et le `deployeur` pour un déploiement, après que `verifier-prod` a confirmé le SHA en ligne (S3-R5) ; passage à `TERMINE` écrit dans le journal du ticket. Pour une livraison, ce sont les portes 1 à 8 de S3.
3. **Les rituels ont des équivalents déclenchés par le flux**, sans cérémonie à date fixe :
   - point d'avancement : skill `avancement`, et tableaux régénérés chaque jour par la CI (`tableau.yml`) ;
   - revue de fin d'incrément : recette humaine (R16) et GO (S3-R3) ;
   - rétrospective : `retex.md` et tickets `amelioration` (S1-R7) et `formation` ; post-mortem sans blâme après une crise (S2-R5).

## Pourquoi
*(§ 3.5 de VISION.md, Johan)* Une semaine et des agents IA ne permettent pas de reproduire les cérémonies d'une méthode unique (sprints, réunions quotidiennes). Nous avons pris de chaque méthode la pratique qui répond à un besoin précis :
- Kanban pour suivre un flux de tickets réalisés en parallèle par des agents ;
- les portes de validation pour la supervision humaine exigée par la consigne ;
- l'incrémental pour livrer une démonstration avant la soutenance ;
- DevOps pour l'exigence « un push ne suffit pas » (S3).

La méthode est déjà appliquée : incrément de soutenance (DEC-011), arbitrage budgétaire avec effet sur le planning (DEC-020, simulation), post-mortem sans blâme (DEC-019, simulation), boucle incident → règle → garde-fou (DEC-007 → DEC-010 → DEC-015). Le détail est dans « La méthode appliquée cette semaine » (§ 3.5).

## Impacts
- **Fichiers** : `docs/VISION.md` (§ 3.5, Johan, complété par le coordinateur) ; `docs/decisions/README.md` (ligne d'index).
- **Règles : aucune modifiée (R11).** Le § 3.5 nomme la méthode et renvoie, pour chaque pratique, à une règle qui existe déjà (R4, R9, R12, R13, R15, R16 ; S1-R2, S1-R3, S1-R4, S1-R7, S1-R11, S1-R12 ; S2-R1 à S2-R5 ; S3-R1, S3-R2, S3-R3, S3-R5, S3-R6, S3-R7, S3-R9 ; S4-R2). La Definition of Done et les équivalents des rituels reformulent ces règles sans rien y ajouter. Aucun fichier du périmètre de [CHANGELOG-REGLES.md](../CHANGELOG-REGLES.md) (`CLAUDE.md`, `docs/systemes/`, agents, skills, templates, settings) n'est modifié : pas d'entrée au changelog. Si l'équipe veut un jour rendre un rituel obligatoire à date fixe (par exemple un `avancement` quotidien), ce sera une nouvelle règle, avec sa PR, sa décision et sa ligne de changelog.
- **Tickets** : aucun.
