---
titre: Retour d'expérience — ESN (projet interne) — semaine projet du 23 au 27/11
statut: VALIDÉ
responsable: agent:chef-de-projet
version: 0.1
maj_le: 2026-11-27
valide_par: Ethan
decision: DEC-025
---
<!-- modèle : templates/retex.md v0.1 · responsable du modèle : A -->

# Retour d'expérience — ESN (projet interne) — semaine projet du 23 au 27/11

> Rituel de rétrospective de fin de semaine (VISION § 3.5, S1-R7, S1-R13, [DEC-022](../../docs/decisions/2026-11-26-DEC-022-methodologie-retenue.md)), rédigé par le ticket [T-020](tickets/T-020-retrospective-semaine-projet.md). Le retex porte sur **l'ESN** : règles, agents, outils et façon de travailler de l'équipe humaine. Celui de `reservation-coworking` reste [le retex du projet](../reservation-coworking/retex.md) (étape 9 du pipeline).
>
> **Règle de rédaction : chaque constat cite sa source** (ticket et ligne de journal, DEC, ligne de `docs/CHANGELOG-REGLES.md`, rapport, ou fait Git relevé par le coordinateur dans la Description de T-020). Le `chef-de-projet` n'a pas accès à `git` : les commits et les PR sont cités tels que le coordinateur les a relevés. Une piste sans trace est rangée sous « Pistes non tracées » et n'est jamais présentée comme un fait.
>
> **Décision attendue** : [T-021](tickets/T-021-decision-actions-retrospective.md) (`ATTENTE_HUMAIN`), qui porte sur les actions A1 à A10 de la section « Ce qu'on change ». Aucun ticket `amelioration` ni `formation` n'est créé avant cette décision.

## Chiffres
### Production de la semaine (2026-11-23 → 2026-11-27)
| Indicateur | Valeur | Source |
|---|---|---|
| PR mergées sur `main` | **24** (#1 à #24). Par jour : 23/11 : 6 · 24/11 : 5 · 25/11 : 3 · 26/11 : 8 · 27/11 : 2 | T-020, faits Git (coordinateur) |
| Commits sur `main` | **134**. Par jour : 23/11 : 19 · 24/11 : 19 · 25/11 : 25 · **26/11 : 62** · 27/11 : 9 | T-020, faits Git |
| PR qui ne portent **qu'une** validation humaine, faite après le merge du contenu | **4 sur 24** (#2, #3, #9, #15) | T-020, faits Git |
| PR où la validation est faite dans la PR du contenu (cas nominal) | 9 (#10, #11, #17, #18, #20 à #24) | T-020, faits Git |
| Décisions humaines | **24** (DEC-001 à DEC-024), toutes `VALIDÉ` ; 3 marquées SIMULATION (DEC-019 à DEC-021) | [registre](../../docs/decisions/README.md), index |
| Décisions qui modifient une règle (avec au moins une ligne au changelog) | 11 : DEC-001, 002, 003, 004, 012, 014, 015, 016, 017, 018, 023 | `docs/CHANGELOG-REGLES.md`, colonne « Décision » |
| Lignes datées du changelog des règles | **44**. 23/11 : 4 · 24/11 : 25 · 25/11 : 1 · 26/11 : 14. Par décision : DEC-002 : 15 · DEC-003 : 9 · DEC-023 : 8 · DEC-001 : 4 · DEC-015 : 2 · les 6 autres : 1 chacune | `docs/CHANGELOG-REGLES.md` v0.11 |
| Règles nouvelles de `CLAUDE.md` | **6** : R14, R15 (DEC-002), R16 (DEC-002 § 36), R17 (DEC-015), R18, R19 (DEC-023) | changelog, lignes du 24/11 « R14 », « R15 », « Recette humaine » ; du 26/11 « R17 », « R18 », « R19 » |
| Règles de `CLAUDE.md` modifiées | 4 : R5 (statut normalisé), R6 (journaux exclus), R13 (qui passe `TERMINE`), R5/R9 (Pourquoi : hook livré) | changelog, 23/11 (2 lignes) et 24/11 (« R13 », « R5 et R9 ») |
| Règles des systèmes nouvelles | 3 : S2-R7 (DEC-002 § 33), S3-R9 (DEC-002 § 36), S1-R13 (DEC-023) | changelog, 24/11 « S2-R7 », « Recette humaine » ; 26/11 « S1-R13 » |
| Règles des systèmes modifiées | 6 : S3-R6 ; S3-R3, S3-R5, S3-R8 (DEC-003) ; S1-R6, S1-R11 (DEC-023) | changelog, 24/11 « S2-R7 et S3-R6 », « S3 portes 5, 6 et 8 » ; 26/11 « S1-R6 », « S1-R11 » |
| Garde-fous ajoutés (ARCHITECTURE § 6) | 3 : n° 7 et 8 (DEC-002 § 14), n° 9 (DEC-015) | changelog, 24/11 « garde-fous 7 et 8 » ; 26/11 « R17 » |
| Format du ticket | v0.1 → v0.2 (DEC-002 § 8) → v0.3 (DEC-023) | changelog, 24/11 « Format du ticket » ; 26/11 « Formats » |
| Agents | 13 (`.claude/agents/`) ; aucun créé ni retiré pendant la semaine (aucune ligne du changelog) | `.claude/agents/` ; changelog |
| Skills | 10 (`.claude/skills/`) | `.claude/skills/` |
| Hooks | 3 : `proteger_valide.py`, `restreindre_bash.py`, `journal_direct.py` (local, optionnel, DEC-018) | `.claude/hooks/` ; changelog, 26/11 « mode Direct » |
| Workflows | 4 : `ci.yml`, `securite.yml`, `tableau.yml`, `validations.yml` ; **pas de `deploy.yml`** (DEC-003) | `.github/workflows/` ; changelog, 24/11 « Workflows » |
| Runbooks | 4 : `coupure-serveur`, `intrusion`, `perte-donnees`, `rollback` | `runbooks/` |
| Outils internes ajoutés | 4 : console (DEC-012), « qui fait quoi » (DEC-014, régularisation), « Le bureau » (DEC-016), mode Direct (DEC-018) | changelog, 25/11 et 26/11 |
| Simulations | 3 scénarios le 26/11 : crise, perte de la base (DEC-019) ; révision du budget à 4 200 € (DEC-020) ; absence de Léa et départ de Hugo (DEC-021). 33 tickets marqués SIMULATION dans `reservation-coworking` | DEC-019 à DEC-021 ; T-020, chiffres du coordinateur |
| Rapports produits (`reservation-coworking/rapports/`) | 7 audits de sécurité, 1 rapport de tests, 1 test de rollback, 1 post-mortem | `projets/reservation-coworking/rapports/` |

### Tickets par projet et par statut (`python scripts/tableau.py`, 2026-11-27)
| Projet | Total | A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE | Source |
|---|---|---|---|---|---|---|---|---|---|
| `reservation-coworking` | 106 | 61 | 6 | 6 | 0 | 1 (T-057) | 22 | 10 | [TABLEAU.md](../reservation-coworking/TABLEAU.md), « Tickets par statut » |
| `esn-interne` (avec T-020 en `EN_REVUE` et T-021) | 21 | 15 | 1 | 1 | 0 | 1 (T-021) | 2 | 1 | [TABLEAU.md](TABLEAU.md), régénéré à la fin de T-020 |

Tickets `decision` passés `TERMINE` avec `temps_passe_h: 0` : **9** (`reservation-coworking` : T-002, T-003, T-005, T-007, T-081, T-083, T-084, T-106 ; `esn-interne` : T-017). Ils totalisent **6,25 h** estimées, soit **342,50 €** au taux de leur assigné, que la projection ne compte plus (détail en P5). Source : frontmatter de ces tickets.

### Charge et budget (`python scripts/tableau.py`, 2026-11-27)
| Indicateur | Prévu | Réel ou projeté | Écart | Source |
|---|---|---|---|---|
| `esn-interne` : budget de fonctionnement | 4 360,00 € (DEC-024) | consommé 60,00 € avant ce ticket (1,4 %), 112,50 € après (2,6 %) ; **projeté 3 723,21 €** (85,4 %) avec T-020 (3,5 h) et T-021 (0,5 h) | marge 636,79 € ; **réserve sous le seuil S1-R11 (3 924 €) : 200,79 €** | [TABLEAU.md](TABLEAU.md) ; [planning.md](planning.md), « Charge et budget prévisionnels » |
| `esn-interne` : écart avec le planning v1.0 | 3 655,71 € | 3 723,21 € | +67,50 € : T-019 (+15,00 €), T-020 (+52,50 €), T-021 (+7,50 €), T-017 clos à 0 h (−7,50 €) | planning.md ; frontmatter de T-017, T-019, T-020, T-021 |
| `esn-interne` : date de fin | 2027-01-15 | 2027-01-26 selon `tableau.py` ; **2027-01-14** selon la projection P1/P2 de planning.md | +7 j ouvrés au tableau : **artefact de l'allocation unique**, déjà analysé (planning.md, alerte 1) et traité par T-019 | TABLEAU.md ; planning.md, « Analyse des alertes » |
| `reservation-coworking` : budget client | 4 200,00 € HT (DEC-020) | consommé client 1 371,29 € (32,6 %) ; **coût client projeté 4 098,93 €** (97,6 %), **4 173,93 € (99,4 %) avec l'audit avant GO non compté** (environ 75 €) | marge réelle 26,07 € | [TABLEAU.md](../reservation-coworking/TABLEAU.md), synthèse ; [T-008](../reservation-coworking/tickets/T-008-pilotage.md), critère « Condition 1 » ; DEC-023, Impacts (« Reste manuel ») |
| `reservation-coworking` : part prise en charge par l'ESN | 1 789,64 € (DEC-020 point 3) | consommé 22,50 € · projeté 1 652,50 € | −137,14 €, dont −175,00 € dus à la clôture de T-081 et de T-083 à 0 h (DEC-023, voir P5), compensés en partie par les tickets imputés depuis (T-102, T-103, T-105) | TABLEAU.md ; DEC-020 ; DEC-023, « Écart de 175 € » |
| `reservation-coworking` : date de fin | 2026-12-18 | 2026-12-16 | −2 j ouvrés | TABLEAU.md |
| Bugs après mise en production | — | aucune mise en production pendant la semaine ; 1 bug remonté par la recette (T-105) | — | TABLEAU.md ; DEC-020 v0.3 |
| **ESN, total** (PORTFOLIO) | — | consommé 82,50 € · projeté 5 360,71 € avant T-020 et T-021 | — | `PORTFOLIO.md`, « Coûts pris en charge par l'ESN » |

## Ce qui a bien marché
- **Le garde-fou R6 a refusé une écriture sur un document `VALIDÉ`.** Le 2026-11-24, le hook a refusé la suite de la révision de l'architecture par l'`architecte`, une fois le document passé `VALIDÉ` (DEC-008, Contexte ; [retex du projet](../reservation-coworking/retex.md), ligne « architecture passée VALIDÉ »). *Limite* : c'est le seul refus tracé, car les refus des hooks ne laissent aucune trace dans le dépôt (voir « Pistes non tracées »).
- **De l'incident à la règle testée, en deux jours.** Le 2026-11-24, DEC-007 est modifié par Bash alors qu'il est `VALIDÉ`. L'écriture est détectée après coup par `verifier_validations.py` (filet CI de R5), notée à chaud dans le retex du projet, puis traitée dans [T-006](../reservation-coworking/tickets/T-006-ecritures-md-par-edit-uniquement.md). Elle aboutit à DEC-010 (principe), puis à [DEC-015](../../docs/decisions/2026-11-26-DEC-015-regle-r17.md) : R17 et le garde-fou 9. Le test `test_rejeu_incident_dec007` de `scripts/test_restreindre_bash.py` (classe `TestR17`) rejoue l'incident et vérifie qu'il est refusé pour la session principale. Sources : changelog, ligne du 2026-11-26 « R17 » ; DEC-015, Décision, point 6.
- **On a testé les garde-fous au lieu de les supposer.** Le test du 2026-11-23 a montré qu'une règle `ask` seule ne déclenchait pas de confirmation : elle a été doublée d'une décision `ask` du hook (changelog, 24/11, « Liste blanche Bash du `deployeur` »). La revue du lot 5 a trouvé qu'un fichier d'état réutilisé de `verifier-prod` donnait un faux « EN LIGNE », et la correction a été faite (changelog, 24/11, « Fichier d'état de `verifier-prod` »). La valeur `VALIDE` sans accent contournait le hook, et elle est désormais normalisée (changelog, 23/11, DEC-001 § 23).
- **La crise simulée a mis au jour l'absence de sauvegarde, et la leçon a été suivie d'actions.** Leçon principale du [post-mortem](../reservation-coworking/rapports/post-mortem-2026-11-26-perte-donnees.md) : « une règle sans preuve d'exécution n'est pas une garantie ». T-029 passe `critique` et devient un prérequis du GO, T-092 (vérification quotidienne des sauvegardes) est créé (T-008, journal du 2026-11-26 18:30), et le registre du plan de formation inscrit `sauvegarde-restauration` en R-04, traité par la formation T-008 de l'ESN (DEC-024). Aucun agent n'a restauré, déployé ni contacté le client (post-mortem, « Ce qui a bien fonctionné »). *Limite* : T-029 est encore `A_FAIRE` (alerte « Critique » de TABLEAU.md). La preuve d'exécution reste donc à apporter.
- **Les arbitrages budgétaires ont été répercutés sur le planning et sur les tickets.** DEC-020 se retrouve dans le planning v1.1 de `reservation-coworking` (`VALIDÉ`, `decision: DEC-020`, Historique v1.1), dans les tickets passés `ANNULE` et dans un nouveau critère du pilotage (T-008, journal du 2026-11-26 22:20 et 23:10). DEC-024 se retrouve dans le planning v1.0 d'`esn-interne` (T-016, journal du 2026-11-27 14:50).
- **L'alerte a précédé le dépassement.** Le tri de T-105 annonçait un dépassement de 11,43 € : la condition 1 de DEC-020 a fait créer la décision [T-106](../reservation-coworking/tickets/T-106-simulation-depassement-t-105.md) **avant** d'engager le correctif (T-008, journal du 2026-11-26 23:30 ; DEC-020 v0.3).
- **Un chiffre d'agent a corrigé un chiffre humain, et la trace en est restée.** DEC-020 v0.3, « Écart à confirmer par Ethan », signale que le coût client retenu par la décision (4 158,93 €) suppose T-104 imputé à l'ESN, et que le coordinateur ne l'a pas fait sans décision explicite. DEC-023 (Décision, point 5) confirme le chiffre de T-008 : 4 173,93 €. C'est la seule trace d'un agent qui conteste à raison un chiffre ou une consigne humaine (voir « Pistes non tracées »).
- **Un problème récurrent est devenu une règle outillée.** Le calcul manuel du coût client (voir P9) a été remplacé par le champ `imputation`, lu par `tableau.py` (R18, DEC-023). Le coût client et la part ESN se lisent désormais dans TABLEAU.md (synthèse de `reservation-coworking`).
- **Les besoins de formation renvoyés à plus tard ont fini par être arbitrés.** DEC-009 E et DEC-021 renvoyaient à un « plan de formation de l'ESN » qui n'existait pas. Le 2026-11-26, DEC-023 crée `esn-interne` ; le 2026-11-27, DEC-024 décide un plan chiffré (T-001, T-017). Les deux tickets `formation` restés dans `reservation-coworking` (T-052, T-053) sont `ANNULE` depuis le 2026-11-25, à 0 h, et leurs besoins sont repris au registre (R-02, R-17) : rien à corriger.
- **La recette sans Claude Code a fonctionné.** La note `support/entrant/recette-2026-11-26-01.md` (DEC-004) a donné le bug T-105, trié par le `chef-de-projet` (T-008, journal du 2026-11-26 23:30).

## Ce qui a posé problème
| # | Problème | Cause | Concerne (agent / règle / salarié / outil) |
|---|---|---|---|
| P1 | **Validations faites après le merge, ou complétées après coup.** 4 PR sur 24 ne portent qu'une validation faite après le merge du contenu (#2, #3, #9, #15). Des champs de validation ont été complétés après coup (b4b1ba1, e091bce, f557d9f puis 075200b). DEC-007 est passé `VALIDÉ` sans `valide_par`. | La procédure du registre (« Commit dans une PR », étape 6) ne dit pas *quelle* PR ; la validation se fait parfois dans l'interface web (6 commits « Update … »). Sources : T-020, faits Git ; retex du projet, ligne « DEC-007 ». | règle (procédure du registre, skill `tracer-decision`) ; équipe humaine |
| P2 | **Documents validés trop tôt.** L'architecture est passée `VALIDÉ` pendant la révision v0.4 et se contredisait (§ 8 à 11). DEC-007 a été validé pendant que le coordinateur appliquait les modifications demandées. 4 documents ont dû être repassés `EN_REVUE` pour être modifiés (138a1b1, f893d7a, 5172c37, ec0e240 : coût normal de R6). | Aucun signal « révision en cours » sur un document ; aucune annonce de fin de révision. Sources : retex du projet, 2 lignes du 2026-11-24 ; DEC-008, Contexte. **Aucune récidive tracée depuis le 2026-11-24.** | règle de validation ; coordinateur |
| P3 | **Une décision prise n'a pas été reportée sur son ticket.** DEC-013 (`VALIDÉ`, `ticket: T-057`) demande de débloquer T-057. Pourtant, T-057 est toujours `ATTENTE_HUMAIN`, avec `decision` vide, depuis le 2026-11-25 (2 jours ouvrés). C'est la seule décision « attendue » de PORTFOLIO.md. De même, T-080 reste `EN_REVUE` depuis le 2026-11-26 19:30, alors que T-081 et T-083 sont désormais `TERMINE` avec `decision: DEC-019` : l'alerte « Critique » reste affichée. | L'étape 6 de `tracer-decision` (« dans le ticket : `decision: DEC-NNN`, puis le débloquer ») repose sur la mémoire de l'humain, et aucun contrôle ne croise les DEC `VALIDÉ` avec les tickets. Sources : DEC-013, Impacts ; frontmatter de T-057 ; TABLEAU.md de `reservation-coworking` ; T-080, journal du 2026-11-26 19:30. | humain ; skill `tracer-decision` ; outil (`tableau.py`) |
| P4 | **Des documents contredisent leur propre en-tête.** 21 des 24 fichiers DEC, tous `VALIDÉ`, portent encore le bandeau « En attente de validation humaine ». Le post-mortem (`VALIDÉ`, DEC-019) écrit que DEC-019 est « `EN_REVUE` ». Le planning v1.1 du projet (`VALIDÉ`) se décrit comme « v1.1 (…, `EN_REVUE`) ». | Le bandeau est écrit dans le corps à la rédaction, et personne ne le retire à la validation. R6 fige ensuite le fichier. Sources : recherche « En attente de validation humaine » dans `docs/decisions/` (21 fichiers) ; post-mortem, en-tête et § « Décision humaine » ; planning v1.1, § Historique. | coordinateur ; skill `tracer-decision` |
| P5 | **Tickets `decision` passés `TERMINE` à 0 h.** 9 tickets (liste dans « Chiffres »), 6,25 h estimées, **342,50 €** sortis de la projection. Les 175 € de T-081 et T-083 ont faussé la part ESN calculée à la main (DEC-023, « Écart de 175 € »). T-017 a fait baisser la projection d'`esn-interne` de 7,50 € le 2026-11-27, alors que son journal compte 0,35 h d'Ethan (lignes de 09:30 et de 09:45). | Aucune règle ne dit qui note le temps d'un ticket `decision`, ni si le temps de décision est compté. R15 ne vise que les tickets `salarie:` réalisés ; T-007, T-081, T-083, T-084 et T-106 sont pourtant assignés à Claire ou à Nadia. Sources : frontmatter des 9 tickets ; DEC-023 ; T-017, journal. | règle (R13, R15, `tracer-decision`) ; outil (`tableau.py` ne signale rien) |
| P6 | **L'audit de sécurité a été estimé pour un seul passage, alors que la livraison était incrémentale.** T-043 : 5 h estimées, **12,5 h passées** en 7 audits d'incrément (DEC-011). La ré-estimation proposée le 2026-11-25 14:45 n'est toujours pas arbitrée le 2026-11-26 22:05. Résultat : l'audit avant GO (environ 75 €) n'est pas compté dans le coût client, qui est faux de 75 € (99,4 % au lieu de 97,6 %). | La règle 6 du `chef-de-projet` prévoit un seul ticket « Audit » par projet ; DEC-011 a ajouté des incréments sans ré-estimation. Sources : T-043, journal (lignes du 2026-11-25 15:30 au 2026-11-26 22:05) ; DEC-023, Impacts (« Reste manuel ») ; T-008, critère « Condition 1 ». | agent `chef-de-projet` (règle 6) ; coordinateur (arbitrage en attente) |
| P7 | **L'agent `securite` audite sans ses outils.** Les 7 audits notent `pip-audit`, `bandit` et `gitleaks` absents du poste, et selon les cas `trivy`, `safety` et `semgrep` : la revue des dépendances se fait alors à la main (OSV). Par ailleurs, `securite.yml` ne lance `bandit` que sur `scripts` et `.claude`, pas sur `projets/*/app`. | L'agent n'installe rien, par règle, et ne lit pas les résultats de la CI. Le workflow n'a pas été étendu aux applications clientes. Sources : T-043, journal du 2026-11-25 15:30 au 2026-11-26 09:45 ; `.claude/agents/securite.md` (dépendances « seulement si l'outil est déjà disponible ») ; `.github/workflows/securite.yml`, étape `bandit`. | outil (`securite.yml`) ; agent `securite` ; hook (liste blanche) |
| P8 | **Les heures des journaux ne sont pas fiables.** Lignes dans le désordre : T-008 (2026-11-25 23:50 avant 14:45 ; 2026-11-26 23:59 avant 23:30), T-043 (21:30 avant 13:45 ; 16:20 avant 16:15), T-017 (décision d'Ethan à 09:30 avant la création à 11:15). Ce ticket même : l'agent n'a pas accès à l'horloge. | Les agents n'ont pas l'heure réelle ; le replay de « Le bureau » (DEC-016) s'appuie sur ces lignes. Sources : journaux cités ; journal de T-020. | agents (règle C11) ; coordinateur |
| P9 | **Le calcul manuel du coût client dérivait.** Deux chiffres pour le même coût (4 158,93 € et 4 173,93 €) ; une part ESN de 1 782,50 € contre 1 607,50 € ; l'alerte à 90 % était faussée. Trois calculs manuels successifs dans T-008 (journal du 2026-11-26 23:10, 23:59 et 23:30), chacun avec une soustraction de la part ESN. **Corrigé** par R18 et DEC-023. | Faute de mécanisme d'imputation, une convention de journal et un calcul à la main dans le pilotage (DEC-020, Impacts). Sources : DEC-023, Contexte ; changelog, 26/11 « R18 ». | règle (traitée) |
| P10 | **Un outil a été ajouté sans décision.** La page « qui fait quoi » est arrivée par la PR #14 sans décision, puis a été régularisée par DEC-014. Les outils suivants ont été décidés avant le merge (DEC-016, DEC-018). | Pas de point d'arrêt ressenti pour un « petit » outil interne. Source : changelog, 26/11 « Outillage interne : `scripts/qui_fait_quoi.py` ». | équipe humaine (occurrence unique) |
| P11 | **`tableau.py` n'a pas pu être lancé par l'agent.** Le 2026-11-25 à 23:50 et à 14:45, le hook n'acceptait que le chemin relatif, et le répertoire courant de l'agent n'était pas la racine du dépôt. Le script a ensuite été lancé le 2026-11-25 à 16:40, le 2026-11-26 et dans ce ticket, mais **le cas s'est reproduit le 2026-11-27** pendant la préparation de `reservation-coworking/T-107` : le répertoire courant de la session avait changé, et le chemin absolu est refusé (ajout du coordinateur, journal de T-008). | Répertoire courant de l'agent, hérité de la session ; la liste blanche n'accepte que le chemin relatif. Source : T-008, journal (2026-11-25 et 2026-11-27). | outil (`restreindre_bash.py`) ; coordinateur (lancer les agents depuis la racine) |

## Pistes signalées par Ethan : vérification dans les traces
| Piste | Verdict | Traces |
|---|---|---|
| *A marché* : garde-fous R5/R6 qui ont tenu | **Confirmée en partie** | 1 refus R6 tracé (architecture, DEC-008) ; 1 contournement par Bash (DEC-007), détecté par la CI, puis fermé par R17 et son test de rejeu. Aucun refus R5 n'est tracé (les refus ne sont pas journalisés). |
| *A marché* : incident DEC-007 → R17 → hook testé | **Confirmée** | retex du projet ; T-006 ; DEC-010 ; DEC-015 ; `test_rejeu_incident_dec007` |
| *A marché* : crise simulée qui a révélé l'absence de sauvegarde | **Confirmée** | post-mortem, leçon principale ; T-029, T-092 ; R-04 et T-008 du plan de formation. Exécution pas encore prouvée (T-029 `A_FAIRE`). |
| *A marché* : arbitrages budgétaires répercutés sur le planning | **Confirmée** | planning v1.1 (DEC-020) ; T-008, journal ; planning d'`esn-interne` v1.0 (DEC-024) |
| *A marché* : agents qui ont contredit à raison une consigne humaine | **Une seule trace** | DEC-020 v0.3, « Écart à confirmer » → DEC-023, point 5. Le reste relève de « Pistes non tracées ». |
| *A coincé* : validations après le merge ou oubliées | **Confirmée** | P1 et P3 |
| *A coincé* : documents validés trop tôt | **Confirmée** (2 cas, le 2026-11-24) | P2 |
| *A coincé* : commandes Git lancées pendant qu'un agent travaillait | **Non tracée** | voir « Pistes non tracées » |
| *A coincé* : calcul manuel du coût client qui dérivait | **Confirmée, et corrigée** | P9 |
| *A coincé* : tickets `decision` passés `TERMINE` à 0 h | **Confirmée** (9 tickets, 342,50 €) | P5 |
| *A coincé* : quota de l'outil | **Non tracée** | voir « Pistes non tracées » |

### Pistes non tracées
Rien dans les tickets, les décisions, le changelog ni les rapports ne permet de les affirmer. Elles ne sont donc pas des constats.
- **Quota de l'outil (Claude Code).** Aucune trace : une recherche de « quota », « limite d'usage » ou « interrompu » dans `projets/` et `docs/` ne renvoie que le quota métier de 2 réservations par jour et des tests interrompus volontairement. *Pour la tracer* : quand une session s'arrête pour cette raison, une ligne `interruption · quota de l'outil · <ce qui reste à faire>` dans le journal du ticket en cours (action A9, sans coût).
- **Commandes Git lancées pendant qu'un agent travaillait.** Aucune trace d'un tel événement. Le seul fait voisin est une **pause demandée** (commit 69b3694, 2026-11-26 09:33 : « vérification du testeur sur T-055 interrompue (pause demandée) : T-055 reste EN_REVUE »), qui n'est pas une commande Git concurrente. Le mode Direct (DEC-018, point « Deux coordinateurs ») avertit si deux sessions sont actives, mais son journal est local et hors Git. *Pour la tracer* : la même ligne `interruption · <cause>` (A9) ; si le cas se reproduit, un humain le décrit dans le ticket concerné, avec le commit.
- **Agents qui ont contredit à raison une consigne humaine (autres cas que DEC-020).** Aucun autre désaccord n'est écrit comme tel. Les journaux montrent plutôt des agents qui appliquent la consigne et la tracent (« coché sur instruction d'Ethan », T-080 ; « statut laissé `A_FAIRE` sur consigne du coordinateur », T-043). *Pour la tracer* : une ligne `désaccord · <consigne> · <raison> · <suite donnée>` quand un agent conteste une consigne (A9).
- **Nombre de refus des hooks R5/R6/R17.** Les refus ne laissent aucune trace dans le dépôt. *Proposition* : aucun outil nouveau ; l'agent ou le coordinateur note le refus au journal du ticket en cours, comme T-008 l'a fait pour `tableau.py` (A9).

## Ce qu'on change
Taux (ARCHITECTURE § 8, R12) : agent 15 €/h ; Claire et Karim 78,57 €/h ; Léa et Nadia 64,29 €/h. Le temps des membres humains de l'équipe projet (Ethan, Johan, Stéphane, Matthieu, `equipe/humains.md`) n'est pas chiffré par `tableau.py`. Toutes les actions coûtées sont à la charge d'`esn-interne` : outils et règles communs (R19).

| Id | Constat | Contenu | Classement | h | € | Assigné proposé | Priorité | Recommandation |
|---|---|---|---|---|---|---|---|---|
| **A1** | P3, P5 | **`tableau.py` signale deux incohérences** dans « Anomalies de données » : (a) un ticket `ATTENTE_HUMAIN` ou `BLOQUE` cité par le champ `ticket` d'une DEC `VALIDÉ` (cas de T-057) ; (b) un ticket `decision` `TERMINE` avec `temps_passe_h: 0` et `estimation_h > 0`. Tests dans `test_tableau.py` ; sortie inchangée sans ces cas. **Ajouté au périmètre de [T-019](tickets/T-019-tableau-allocations-par-periode.md)** (même PR de règles sur `tableau.py`), sans nouveau ticket. | `amelioration` (T-019 enrichi), PR R11 | 2,5 (dev 2, relecture 0,25, tests 0,25) | 37,50 | `agent:dev-backend` (réalisation de T-019), `relecteur-code`, `testeur` | haute | **retenir** |
| **A2** | P5 | **Le temps d'un ticket `decision` est noté à sa clôture.** Skill `tracer-decision`, étape 6, liste remise à l'humain : « dans le ticket : `decision: DEC-NNN`, **`temps_passe_h`** (temps du porteur, en h équivalent humain ; 0 seulement si c'est assumé, avec une ligne de journal), puis le débloquer ». Aucune correction rétroactive, sauf si un porteur a réellement passé du temps (R15, DEC-023). | PR R11 (skill) | 0,5 | 7,50 | cadrage : `agent:chef-de-projet` ; PR : coordinateur ; relecture : B | normale | **retenir** (même PR que A3 et A4) |
| **A3** | P4 | **Plus de bandeau d'état dans le corps d'un document.** Skill `tracer-decision`, étape 3 : l'en-tête fait foi (R3). Le bandeau « En attente de validation humaine » est remplacé par une ligne neutre (« Rédigé par le coordinateur le … à partir de … »). Une phrase dans `docs/decisions/README.md` : « en cas d'écart, l'en-tête fait foi ». Les 21 fichiers existants ne sont pas modifiés : il faudrait 21 passages en `EN_REVUE` (R6), un coût sans proportion avec le gain. | PR R11 (skill, registre) | 0,5 | 7,50 | idem A2 | basse | **retenir** (même PR) |
| **A4** | P1 | **La validation se fait dans la PR du contenu, avant son merge**, et après le message de fin de l'agent (rubrique « Produit »). Message de commit explicite : `validation: DEC-NNN <document>`. Étape 6 de la procédure du registre et de `tracer-decision`. En option, un humain rend `validations.yml` obligatoire avant le merge sur `main` (réglage GitHub, non chiffré). | PR R11 (registre, skill) | 0,5 | 7,50 | idem A2 | normale | **retenir** (même PR) |
| **A5** | P2 | **Signal « révision en cours »** : un agent repasse un document `BROUILLON` au début d'une révision et `EN_REVUE` à la fin (`_ENTETE.md`, règles communes des 13 agents). | PR R11 (13 agents, modèle) | 1,5 | 22,50 | coordinateur ; relecture A à D | basse | **reporter** : 2 cas, tous deux du 2026-11-24, aucune récidive tracée depuis ; R6 a limité les dégâts, et A4 couvre l'essentiel. À revoir au retex de `reservation-coworking` |
| **A6** | P6 | **Estimer l'audit de sécurité par incrément.** Règle 6 du `chef-de-projet` : un ticket « Audit sécurité » par livraison incrémentale (DEC-022), plus l'audit avant GO, estimés séparément. Une décision qui ajoute un incrément (comme DEC-011) entraîne une ré-estimation au même triage. | PR R11 (`chef-de-projet.md`) | 0,5 | 7,50 | coordinateur ; relecture B | normale | **retenir**. *Hors retex, à faire tout de suite dans le projet client* : arbitrer la proposition A de T-043 (journal du 2026-11-25 14:45), soit +75 € au coût client, qui atteint alors 99,4 % |
| **A7** | P7 | **Des outils pour l'audit avant GO.** Cadrage : (a) l'agent `securite` lit les résultats de `securite.yml` sur le SHA candidat (lecture de l'exécution CI dans sa liste blanche, ou rapport joint par le coordinateur), ou bien les outils sont installés sur le poste ; (b) `bandit` est étendu à `projets/*/app`. La réalisation passe par une PR de règles (workflow, agent `securite`, `restreindre_bash.py`). | `amelioration` (cadrage), puis PR R11 | 3 (cadrage 1, réalisation 2) | 45,00 | cadrage : `agent:chef-de-projet` ; réalisation : `agent:dev-backend` ; relecture : C (hooks et workflows) | **haute** : avant l'audit avant GO de `reservation-coworking` (GO le 2026-12-15) | **retenir** |
| **A8** | P8 | **Heure des journaux** : le coordinateur donne la date et l'heure dans chaque message de lancement ; un agent qui ne les connaît pas écrit la date seule. Simple pratique, aucune règle. (Variante écartée : modifier la règle C11 des 13 agents par une PR, 1 h, 15 €.) | rien (pratique) | 0 | 0 | coordinateur | basse | **ne rien faire** au-delà de la pratique |
| **A9** | pistes non tracées | **Lignes de journal `interruption · <cause>` et `désaccord · <consigne> · <raison> · <suite>`** dans le ticket en cours, et note d'un refus de hook quand il survient. Pratique, aucune règle. | rien (pratique) | 0 | 0 | coordinateur, agents, humains | basse | **ne rien faire** au-delà de la pratique ; à revoir si le cas se reproduit |
| **A10** | P9, P10, P11 ; plan de formation | **Rien à ajouter** : P9 est corrigé par R18 ; P10 n'est arrivé qu'une fois et a été régularisé ; P11 est résolu de fait. **Plan de formation (S1-R13)** : aucune trace de la semaine ne révèle un besoin de compétence salariée nouveau ; P6 et P7 relèvent d'outils et de règles. Le registre R-01 à R-17 de [planning.md](planning.md) (DEC-024) couvre déjà les besoins. Pas de mise à jour du registre, ni de ticket `formation`, ni de ticket `decision` de plan. | rien | 0 | 0 | — | — | **ne rien faire** |

**Synthèse des coûts**

| Sélection | Actions | h | € |
|---|---|---|---|
| Tout retenir | A1 à A7 | 9,0 | 135,00 |
| **Sélection recommandée** | **A1, A2, A3, A4, A6, A7** (A5 reporté) | **7,5** | **112,50** |
| Minimum | A1, A7 (chiffres justes et audit avant GO outillé) | 5,5 | 82,50 |
| Rien | — | 0 | 0 |

**Effet sur le budget d'`esn-interne`** (4 360 € ; seuil S1-R11 à 3 924 € ; projeté actuel 3 723,21 €, T-020 et T-021 compris) :

| Sélection | Projeté | % du budget | Réserve sous le seuil |
|---|---|---|---|
| Tout retenir | 3 858,21 € | 88,5 % | 65,79 € |
| **Sélection recommandée** | **3 835,71 €** | **88,0 %** | **88,29 €** |
| Minimum | 3 805,71 € | 87,3 % | 118,29 € |
| Rien | 3 723,21 € | 85,4 % | 200,79 € |

Toutes les sélections restent sous le seuil, sans révision du budget. **Point d'attention** : la réalisation de T-019 (allocations par période) n'est pas encore estimée. Avec la sélection recommandée, il reste 88,29 €, soit environ 5,9 h d'agent, avant le seuil : si T-019 dépasse ce volume, sa décision de modification de règle devra comporter une révision du budget d'`esn-interne`, ou un report.

**Autres points relevés, hors actions** (à traiter par le coordinateur ou par un humain, sans coût pour `esn-interne`) :
- **T-057** : renseigner `decision: DEC-013` et le débloquer (humain, P3) ;
- **T-080** : son critère 2 est rempli de fait (T-081 et T-083 `TERMINE`, `decision: DEC-019`). Le conclure lèverait l'alerte « Critique » (coordinateur, R13) ;
- **T-043** : arbitrer la ré-estimation (A6, projet client) ;
- **planning.md d'`esn-interne`** : les hypothèses confirmées par Ethan le 2026-11-27 (T-016, journal) restent à reporter à sa prochaine révision (v1.0 `VALIDÉ`, figée par R6).

## Améliorations des agents IA → tickets `amelioration`
| Agent ou règle | Amélioration proposée | Ticket |
|---|---|---|
| `scripts/tableau.py` | A1 : anomalies « DEC `VALIDÉ` / ticket encore en attente » et « `decision` `TERMINE` à 0 h » | après décision (T-021) : T-019 enrichi, pas de nouveau ticket |
| skill `tracer-decision`, registre des décisions | A2 (temps du ticket `decision`), A3 (pas de bandeau d'état dans le corps), A4 (validation dans la PR du contenu) | après décision (T-021) |
| agent `chef-de-projet` (règle 6) | A6 : un audit de sécurité par incrément, plus l'audit avant GO | après décision (T-021) |
| agent `securite`, `securite.yml`, `restreindre_bash.py` | A7 : audit avant GO avec les outils (résultats de la CI ou outils installés), `bandit` sur les applications clientes | après décision (T-021) |
| règles communes des agents, `_ENTETE.md` | A5 : signal « révision en cours » (recommandation : reporter) | après décision (T-021) |

## Besoins de formation → tickets `formation`
| Salarié | Compétence | Ticket |
|---|---|---|
| — | Aucun besoin nouveau (A10). Le registre R-01 à R-17 et le plan décidé par DEC-024 restent inchangés. Prochaines revues : bascule P2 du 2026-12-21 (T-016), retex de `reservation-coworking` (R-08 `juridique`, R-10 `rgpd`). | sans objet (après décision T-021 : aucun ticket) |

## Règles à modifier (R11 : PR, décision et changelog)
- **A2, A3, A4** : skill `tracer-decision` (étapes 3 et 6) et procédure de `docs/decisions/README.md`. Une seule PR de règles est proposée, avec son DEC et ses lignes du changelog.
- **A6** : règle 6 de `.claude/agents/chef-de-projet.md`.
- **A7** : `.github/workflows/securite.yml`, `.claude/agents/securite.md`, `.claude/hooks/restreindre_bash.py` (liste blanche), après le cadrage.
- **A1** : `scripts/tableau.py` et `scripts/test_tableau.py`, dans la PR de règles de T-019.
- **A5** (si un humain le retient malgré la recommandation) : `templates/_ENTETE.md` et les règles communes des 13 agents.

Aucune de ces modifications n'est faite par ce retex : chacune passe par une PR, un fichier de décision et une ligne de `docs/CHANGELOG-REGLES.md` (R11), après la décision T-021.
