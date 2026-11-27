---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-020
titre: Rétrospective de la semaine projet (23 au 27/11) au niveau de l'ESN
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 3.5          # heures équivalent humain ; +0,5 h sur l'estimation (volume des sources : 24 DEC, 44 lignes du changelog, journaux de reservation-coworking), voir Journal
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le: 2026-11-27        # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-27      # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-020 — Rétrospective de la semaine projet (23 au 27/11) au niveau de l'ESN

## Description
Ticket de travail du `chef-de-projet` (CLAUDE.md R14) pour le rituel de **rétrospective** de fin de semaine projet (VISION § 3.5, « Équivalents des rituels » ; S1-R7 ; S1-R13), demandé par Ethan le 2026-11-27. Il porte sur **l'ESN** (règles, agents, outils, façon de travailler de l'équipe humaine), pas sur un projet client : le `retex.md` de `reservation-coworking` reste celui du projet (étape 9 du pipeline).

**Attendu.**
1. `projets/esn-interne/retex.md`, au format de [templates/retex.md](../../../templates/retex.md), en `EN_REVUE`. **Chaque constat cite sa source** (ticket, ligne de journal, DEC, entrée du CHANGELOG, rapport, commit ou PR). Un constat sans source tracée n'est pas écrit comme un fait.
   - **Ce qui a bien marché** ; **ce qui a posé problème** (problème, cause, concerne) ;
   - **les chiffres de la semaine** (PR, décisions, règles ajoutées ou modifiées, tickets, agents, skills) ;
   - **ce qu'on change** : une liste d'actions proposées, numérotées, chacune **chiffrée** (heures équivalent humain et €, R12) et **classée** : règle à modifier par PR (R11), ticket `amelioration`, `formation`, ou rien.
2. Un ticket `decision` `ATTENTE_HUMAIN` dans `projets/esn-interne/tickets/` (format R7 : question, options, recommandation, impact) pour qu'un humain choisisse les actions retenues. Les tickets `amelioration` et `formation` correspondants **ne sont créés qu'après cette décision**.

**Pistes signalées par Ethan au lancement** (à confirmer ou infirmer par les traces ; une piste sans trace est signalée comme telle, avec une action pour la tracer) :
- *a marché* : garde-fous R5/R6 qui ont tenu ; incident DEC-007 → R17 → hook testé ; crise simulée qui a révélé l'absence de sauvegarde ; arbitrages budgétaires répercutés sur le planning ; agents qui ont contredit à raison une consigne humaine ;
- *a coincé* : validations faites après le merge ou oubliées ; documents validés trop tôt ; commandes Git lancées pendant qu'un agent travaillait ; calcul manuel du coût client qui dérivait ; tickets de décision passés `TERMINE` à 0 h ; quota de l'outil.

**Faits Git relevés par le coordinateur le 2026-11-27** (le `chef-de-projet` n'a pas accès à `git`, liste blanche de `restreindre_bash.py` ; commandes reproductibles : `git log --merges --first-parent main`, `git rev-list --count main`, `git log --format='%ad' --date=short main | sort | uniq -c`, et pour chaque PR `git log <merge>^1..<merge>^2`) :

| Fait | Valeur |
|---|---|
| PR mergées sur `main` | **24** (#1 à #24), du 2026-11-23 15:31 au 2026-11-27 09:37 |
| PR par jour | 23/11 : 6 (#1 à #6) ; 24/11 : 5 (#7 à #11) ; 25/11 : 3 (#12 à #14) ; 26/11 : 8 (#15 à #22) ; 27/11 : 2 (#23, #24) |
| Commits sur `main` | **134** : 23/11 : 19 ; 24/11 : 19 ; 25/11 : 25 ; 26/11 : 62 ; 27/11 : 9 |
| PR qui ne contiennent **qu'une validation humaine** faite après le merge de la PR de contenu | **#2** (`validation/lot-1`, commit 6784d92, après #1 mergée à 15:31) ; **#3** (`validation/dec-001`, 70d9f38, « journaux remis en EN_REVUE ») ; **#9** (même branche `integration/lot2` que #8, mergée à 11:24 ; validation b25538e à 11:26 puis « valide_par de DEC-002 » e091bce à 11:28, mergée à 11:29) ; **#15** (`validation/dec-013`, 7092e44, « DEC-013 validée dans le registre », après « Update …DEC-013… » 1174b20) |
| Champs de validation complétés après coup | b4b1ba1 « corrections mineures (registre, changelog, valide_par) » (23/11) ; e091bce « valide_par de DEC-002 » (24/11) ; f557d9f « DEC-018, champ decision rempli » puis 075200b « DEC-018 champ decision, DEC-017 restauré » (26/11, dans #20) |
| Validations faites dans l'interface web de GitHub (commits « Update … ») | 35b7865 (DEC-012), 88396da et ce66342 (« Update decision status and version in README », #13) ; 81b4fa0 (DEC-011) et 45dfb02 (README, #12) ; 1174b20 (DEC-013) |
| Documents repassés `EN_REVUE` pour être modifiés (R6) | 138a1b1 (lot 2), f893d7a (lot 5), 5172c37 (architecture coworking v0.4), ec0e240 (PR de règles #17) |
| Pause du développement | 69b3694 (26/11 09:33) : « vérification du testeur sur T-055 interrompue (pause demandée) : T-055 reste EN_REVUE » |
| Validation dans la même PR que le contenu (cas nominal) | #10 (3738b9a), #11 (ed4510c), #17 (522f083), #18 (c891437), #20 (066429c), #21 (e8600d6), #22 (712b04d), #23 (5c12b93), #24 (24108ac, 3aa9ec3) |
| Commit du bot de la CI | 6058d3f « chore: régénère les tableaux de bord [skip ci] » (`tableau.yml`) |

**Autres chiffres relevés le 2026-11-27** (lecture seule des fichiers) : 24 fichiers DEC (DEC-001 à DEC-024 ; DEC-019 à DEC-021 marqués SIMULATION) ; 44 lignes datées dans `docs/CHANGELOG-REGLES.md` ; 13 agents (`.claude/agents/`) ; 10 skills (`.claude/skills/`) ; 3 hooks (`proteger_valide.py`, `restreindre_bash.py`, `journal_direct.py`) ; 4 workflows (`ci.yml`, `securite.yml`, `tableau.yml`, `validations.yml`) ; 4 runbooks ; tickets : `reservation-coworking` 106 (22 `TERMINE`, 10 `ANNULE`, 6 `EN_COURS`, 6 `EN_REVUE`, 1 `ATTENTE_HUMAIN`, 61 `A_FAIRE` ; dont 33 marqués SIMULATION), `esn-interne` 19 avant ce ticket. Tickets `decision` `TERMINE` avec `temps_passe_h: 0` : `reservation-coworking` T-002, T-003, T-005, T-007, T-081, T-083, T-084, T-106 ; `esn-interne` T-017. Deux tickets de type `formation` restent dans `reservation-coworking` (créés avant S1-R6 dans sa version DEC-023) : à vérifier.

**Sources à lire** : CLAUDE.md (R1 à R19), docs/VISION.md § 3.5, docs/systemes/ (S1 à S4), docs/CHANGELOG-REGLES.md, docs/decisions/ (DEC-001 à DEC-024), docs/ARCHITECTURE.md § 6 (garde-fous), `projets/reservation-coworking/` (retex.md, tickets, rapports dont post-mortem, planning.md), `projets/esn-interne/` (planning.md, tickets), `equipe/`, `veille/`.

**Périmètre.** Écriture uniquement dans `projets/esn-interne/` (retex.md, ce ticket, le ticket `decision`). Aucune modification de règle, d'agent, de skill, de template, de `docs/` ni d'`equipe/` (R11, C9). Rien n'est passé `VALIDÉ` (R5).

## Critères d'acceptation
- [x] `projets/esn-interne/retex.md` existe au format de `templates/retex.md`, en `EN_REVUE`, avec l'en-tête standard (R3).
- [x] Chaque constat (« a marché », « a posé problème ») cite au moins une source tracée ; les pistes d'Ethan sans trace sont signalées comme telles.
- [x] Les chiffres de la semaine couvrent PR, décisions, règles ajoutées ou modifiées, tickets, agents et skills, avec leur source.
- [x] Chaque action proposée est numérotée, chiffrée (h équivalent humain et €) et classée (PR R11, `amelioration`, `formation`, rien).
- [x] Un ticket `decision` `ATTENTE_HUMAIN` (format R7) est créé dans `projets/esn-interne/tickets/` et cité dans le retex.
- [x] Le temps passé est noté dans le journal de ce ticket (R12).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (rétrospective)
- **Commentaires** :
- **Revue humaine requise** : non (la décision humaine porte sur le ticket `decision`)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 · agent:coordinateur · création (R14) à la demande d'Ethan : rituel de rétrospective de fin de semaine projet au niveau de l'ESN ; faits Git et chiffres relevés par le coordinateur et reportés en Description · 0 h
- 2026-11-27 · agent:chef-de-projet · A_FAIRE → EN_COURS : début de la rétrospective (lecture des sources). Heure non indiquée : l'agent n'a pas accès à l'horloge (voir retex, P8) · 0 h
- 2026-11-27 · agent:chef-de-projet · retex.md v0.1 (EN_REVUE) : chiffres de la semaine avec leurs sources, `tableau.py` lancé (esn-interne projeté à 3 708,21 € avant ce ticket ; reservation-coworking : coût client projeté 4 098,93 €, plus environ 75 € d'audit avant GO non compté) ; 10 réussites et 11 problèmes, tous sourcés ; pistes d'Ethan vérifiées : 2 non tracées (quota de l'outil, commandes Git concurrentes) et 1 tracée une seule fois (désaccord d'agent), avec une action pour les tracer ; actions A1 à A10 chiffrées et classées (sélection recommandée : A1, A2, A3, A4, A6, A7, 112,50 €) ; plan de formation (S1-R13) : registre R-01 à R-17 sans mise à jour · 3,5 h
- 2026-11-27 · agent:chef-de-projet · création de T-021 (decision, ATTENTE_HUMAIN, options 1 à 4, option 2 recommandée ; projeté d'esn-interne à 88,0 % avec l'option 2, sous le seuil de 3 924 €) ; temps compté dans la ligne précédente · 0 h
- 2026-11-27 · agent:chef-de-projet · EN_COURS → EN_REVUE : tous les critères sont remplis ; passage TERMINE laissé au coordinateur. Signalé hors périmètre : T-057 (decision: DEC-013 à renseigner par un humain), T-080 (à conclure), T-043 (ré-estimation à arbitrer, +75 € au coût client) · 0 h
- 2026-11-27 10:50 · agent:coordinateur · EN_REVUE → TERMINE (R13) : 6 critères vérifiés ; retex validé par Ethan sous DEC-025 (v0.1, `VALIDÉ`) ; T-021 tranché (DEC-025) ; suites de DEC-025 lancées (T-019 enrichi, tickets `amelioration` A2-A3-A4, A6, A7) · 0 h
