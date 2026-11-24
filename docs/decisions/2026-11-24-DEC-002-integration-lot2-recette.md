---
titre: Intégration du Lot 2, recette humaine et listes blanches Bash S2
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-24
valide_par:
decision: DEC-002
id: DEC-002
date: 2026-11-24
decide_par: Ethan
projet: ESN
ticket:
modifie_une_regle: oui
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-002 — Intégration du Lot 2, recette humaine et listes blanches Bash S2

> **En attente de validation humaine.** Ce fichier a été rédigé par le coordinateur à partir de la décision d'Ethan (validation du plan d'intégration le 2026-11-24, et réponses aux 4 arbitrages posés). Conformément à R5, c'est à un membre de l'équipe de le passer lui-même à `VALIDÉ` et de renseigner `valide_par`.

## Contexte
Les 4 périmètres du Lot 2 ont livré leurs agents, leurs skills, leurs hooks et leurs scripts sans modifier les fichiers partagés. Les changements qui en découlent sont listés dans `docs/a-integrer/lot2-A.md` (3 points), `lot2-B.md` (9), `lot2-C.md` (11) et `lot2-D.md` (12). Un humain a repassé CLAUDE.md, ARCHITECTURE.md et S1 à S4 en `EN_REVUE` pour cette intégration (R6).

Ethan a demandé en plus :
- une **recette humaine**, nouvelle porte de S3 entre les tests et le GO, avec son template, son skill, le contrôle par le `deployeur` et un ticket « Recette » dans chaque planning ;
- les **listes blanches Bash** d'`analyste-prod` et de `gestionnaire-crise` (lot2-D, point 2), avec leurs tests et les règles `allow` correspondantes.

Le coordinateur a proposé, pour chaque point, un fichier cible, la modification et l'origine, ainsi que des arbitrages pour les conflits et les reports. Ethan a tranché 4 questions, puis validé l'ensemble.

## Options étudiées
| Question | Options | Retenue par Ethan |
|---|---|---|
| Pourquoi de la règle de recette | (a) regard du client ; (b) engagement de l'ESN ; (c) les deux | **(c) les deux** |
| Verdict CONFORME | (a) Must stricts ; (b) tout OK sans exception | **(a) Must stricts** |
| lot2-D point 9 (tickets internes à l'ESN) | (a) reporter ; (b) créer `projets/esn-interne/` maintenant | **(a) reporter** |
| Format du ticket (lot2-B 5 et lot2-D 5) | (a) champs et tenue par les agents ; (b) champs seuls ; (c) tout reporter | **(a) champs et agents** |

## Décision

Une section par point. « Pourquoi » reprend la justification écrite par le responsable du point dans `docs/a-integrer/`, adoptée par Ethan à la validation du plan ; pour la recette, ce sont les mots d'Ethan.

## Périmètre A

### 1. lot2-A § 1 — Template de l'analyse de l'existant
- **Décision** : création de `templates/existant.md` (en-tête, provenance, Fonctionnalités, Données, Dette technique, Risques, Questions ouvertes) ; S4 § 3 et `analyste-besoin` y renvoient ; CLAUDE.md § 1 (modernisation) aussi.
- **Pourquoi** : S4 et CLAUDE.md exigent une analyse de l'existant validée avant toute architecture, mais aucun template ne la définissait ; R2 impose un template par livrable. Un fichier séparé du CDC se valide avant d'écrire le CDC.
- **État** : intégré.

### 2. lot2-A § 2 — Permissions sur les commandes git destructrices
- **Décision** : constaté déjà appliqué par C : `deny` sur `git push --force`, `git reset --hard`, `rm -rf` dans `settings.json`, `ask` sur `git push`, et refus de `git push` et `reset --hard` pour tout subagent par `restreindre_bash.py`. Décrit dans ARCHITECTURE § 6 (garde-fou 7) et S3 § 5.
- **Pourquoi** : le champ `tools` d'un subagent autorise Bash entier ; seule une permission ou un hook rend l'interdiction effective (DEC-001 § 7).
- **État** : intégré (constaté).

### 3. lot2-A § 3 — Ticket de travail avant l'analyste et l'architecte
- **Décision** : doublon de lot2-B § 1, traité en § 4 (nouvelle règle R14).
- **État** : intégré (voir § 4).

## Périmètre B

### 4. lot2-B § 1 — Ticket de travail avant l'analyste et l'architecte (R14)
- **Décision** : nouvelle règle **R14** dans CLAUDE.md : avant de lancer `analyste-besoin` ou `architecte`, le coordinateur crée leur ticket de travail selon `creer-ticket` (`tache`, assigné à l'agent, estimé). CLAUDE.md § 4 y renvoie.
- **Pourquoi** : les tickets de réalisation ne sont créés qu'après la validation du CDC et de l'architecture (S1-R1) ; sans ticket de travail, le temps de l'analyste et de l'architecte n'est rattaché à rien et le budget consommé est sous-estimé.
- **État** : intégré.

### 5. lot2-B § 2 — AF9 et AF11 dans CLAUDE.md
- **Décision** : CLAUDE.md § 2 reprend **AF9** (l'utilisation des salariés est un indicateur, jamais une obligation) ; **AF11** devient la règle **R15** (un ticket `salarie:` est une responsabilité humaine).
- **Pourquoi** : AF11 limite ce que fait le coordinateur, pas seulement le chef ; une règle écrite seulement dans un fichier d'agent ne lie pas la session principale. AF9 évite les tickets artificiels. AF11 : la responsabilité humaine est réelle, l'outil n'y change rien.
- **État** : intégré.

### 6. lot2-B § 3 — Références aux agents et skills livrés
- **Décision** : les mentions « arrivent au Lot 2 / Lot 3 » de CLAUDE.md (§ 2, § 4, § 5) et de S1 (§ 4, § 6) sont remplacées par des liens vers `.claude/agents/` et `.claude/skills/<nom>/SKILL.md`.
- **Pourquoi** : le coordinateur doit savoir que ces procédures existent ; une mention « à venir » l'inciterait à improviser.
- **État** : intégré.

### 7. lot2-B § 4 — Critères d'affectation et événements dans S1
- **Décision** : S1 § 4, étape 3 : résumé d'AF1 à AF11 avec un lien vers `chef-de-projet.md`. S1 § 6 : séquence exacte (le coordinateur crée le ticket `decision` assigné au chef ; le chef analyse et le passe `ATTENTE_HUMAIN` ; l'humain décide ; le coordinateur applique les changements d'`equipe/`). Reprise dans CLAUDE.md § 5.
- **Pourquoi** : les critères étaient la pièce manquante de S1 identifiée par DEC-001 ; la séquence garde le texte de S1 tout en respectant R2 et en comptant le temps du chef.
- **État** : intégré.

### 8. lot2-B § 5 — Champ `competence_requise`
- **Décision** : `templates/ticket.md` v0.2 porte `competence_requise: <nom> (<niveau>)`. Il **remplace** la ligne `**Compétence requise**` de la Description (arbitrage d'Ethan). Mis à jour : `creer-ticket`, `chef-de-projet`, `analyste-besoin`, `architecte`, S1 § 8.
- **Pourquoi** : AF1 à AF10 et la détection des besoins de formation reposent sur la compétence requise ; un champ structuré est lisible par `tableau.py`, une ligne dans le corps ne l'est pas de façon fiable. Une seule source évite la double saisie.
- **État** : intégré. `tableau.py` ne lit pas encore ce champ ; à signaler à D pour le taux de couverture des compétences.

### 9. lot2-B § 6 — `tableau.py` et les données d'`equipe/`
- **Décision** : constaté déjà livré par D (lot 4 en avance) : lecture d'`equipe/agents.md` et de `calendrier.md`, jours ouvrés, S1-R9, préavis, utilisation AF9, tickets `formation`. Hypothèses documentées dans ARCHITECTURE § 7 (§ 31).
- **Pourquoi** : les skills `avancement`, `absence` et `depart-membre` s'appuient sur ces chiffres.
- **État** : intégré (constaté).

### 10. lot2-B § 7 — Bash du chef-de-projet limité à `tableau.py`
- **Décision** : constaté déjà appliqué par la liste blanche `chef-de-projet` de `restreindre_bash.py` ; le Pourquoi de la règle 12 du chef et le catalogue le disent désormais.
- **Pourquoi** : le champ `tools` autorise Bash entier ; une limite qui n'est qu'une consigne n'est pas effective.
- **État** : intégré (constaté).

### 11. lot2-B § 8 — Catalogue et circuit d'`equipe/`
- **Décision** : ARCHITECTURE § 4 : Bash du chef « limité à `python scripts/tableau.py` (hook) ». ARCHITECTURE § 3 et § 5, CLAUDE.md § 5 : `equipe/` est écrit uniquement par le coordinateur, via les skills d'événements et après décision humaine ; les agents le lisent.
- **Pourquoi** : la syntaxe `Bash(python scripts/tableau.py)` laissait croire à une restriction technique qui n'existait pas encore ; la règle d'écriture d'`equipe/` n'était écrite nulle part dans ARCHITECTURE.
- **État** : intégré.

### 12. lot2-B § 9 — Renvoi au skill `creer-ticket` dans les agents de A
- **Décision** : `analyste-besoin.md` et `architecte.md` créent leur ticket de validation selon `.claude/skills/creer-ticket/SKILL.md` (champ `competence_requise` compris).
- **Pourquoi** : une seule procédure de création évite des tickets de formats différents selon l'agent.
- **État** : intégré.

## Périmètre C

### 13. lot2-C § 1 — Catalogue des agents de C
- **Décision** : ARCHITECTURE § 4 : `securite` + Edit (son ticket et ses rapports, jamais `app/`) ; `deployeur` + Glob, Grep, et `verifier_prod.py` au lieu de `curl` ; `relecteur-code` : `git diff`, `log`, `show`, `status`, `blame` ; les limites Bash sont appliquées par le hook.
- **Pourquoi** : le catalogue doit décrire ce qui est réellement appliqué ; sans Edit, `securite` devrait réécrire son ticket entier avec Write, au risque d'abîmer le journal.
- **État** : intégré.

### 14. lot2-C § 2 — Arborescence et garde-fous
- **Décision** : ARCHITECTURE § 3 : hooks, `verifier_prod.py`, tests de C. ARCHITECTURE § 6 : garde-fou 1 précisé (passage à `VALIDÉ`) ; garde-fou 6 décrit avec ses **deux barrières** (`Edit(/templates/**)` et l'`ask` du hook) et le résultat du test réel ; **nouveau garde-fou 7 « Bash par agent »**.
- **Pourquoi** : les règles Bash de `settings.json` se contournent (`git -C . push`, `bash -c`, `cat .env`) ; le hook analyse la commande. Les précisions décrivent le comportement réellement livré et testé.
- **État** : intégré.

### 15. lot2-C § 3 — Qui passe un ticket `TERMINE`
- **Décision** : R13 précise : le `testeur` passe `TERMINE` un ticket de réalisation (avis APPROUVÉ, revue humaine faite si requise, critères cochés, suites vertes) ; le `deployeur`, un ticket de déploiement (SHA vérifié) ; un agent S3 ne termine jamais son propre ticket de travail ; un ticket `salarie:` est terminé par l'humain qui le porte. Le Pourquoi de R5 renvoie au hook livré, et le contrôle CI au lot 5.
- **Pourquoi** : ni CLAUDE.md, ni S3, ni les agents de A ne disaient qui passe un ticket de réalisation `TERMINE`. Arbitrage d'Ethan à la revue du plan du lot 2-C : le `testeur` est la dernière porte par ticket et il est indépendant de l'auteur (S3-R1).
- **État** : intégré.

### 16. lot2-C § 4 — S3 : porte 2, permissions réelles, production locale
- **Décision** : S3 § 3, porte 2 : le `testeur` coche les critères constatés et passe le ticket `TERMINE`. S3 § 5 devient « Permissions appliquées » : `Edit(/templates/**)` couvre Write et MultiEdit, ligne « Bash des subagents », `Read(**/.env*)` ne couvre pas Bash, ligne « fichiers générés ». S3 § 6 : production locale admise avec `hebergement: local` et `url_prod: http://localhost:<port>`, après décision humaine. En-tête : B pour le fichier, C pour le système.
- **Pourquoi** : S3 doit décrire ce qui est appliqué ; le professeur peut dispenser l'équipe d'hébergement réel, et la preuve par le SHA reste la même.
- **État** : intégré.

### 17. lot2-C § 5 — `chef-de-projet` : ticket « Revue de code » et règle 12
- **Décision** : règle 6 : ticket `tache` « Revue de code » par projet, assigné à `agent:relecteur-code`, environ 0,5 h par ticket de réalisation. Le Pourquoi de la règle 12 cite le hook.
- **Pourquoi** : le relecteur n'écrit que la section « Revue » du ticket relu ; sans ticket dédié, son temps serait imputé au taux de l'assigné, ou rattaché à rien (même principe que le ticket « Pilotage »).
- **État** : intégré.

### 18. lot2-C § 6 — `/health` en production locale et `env.example`
- **Décision** : `dev-backend` (règle 6) et `architecte` (règle 5, contrôle) : `/health` lit `RENDER_GIT_COMMIT`, avec un repli sur `GIT_COMMIT`, sinon `"inconnu"`. `architecte`, `dev-backend` et `dev-frontend` (règle C10) : le fichier d'exemple s'appelle `env.example`.
- **Pourquoi** : sans repli, une app locale ne peut pas prouver sa version ; la règle `deny` sur `**/.env*` refuserait `.env.example`.
- **État** : intégré.

### 19. lot2-C § 7 — Interfaces avec S2
- **Décision** : constaté déjà appliqué par D (règle 7 de `gestionnaire-crise`, runbook `rollback`, entrées de l'`analyste-prod`). S2 § 6, S2 § 8 et S3 § 8 le décrivent désormais.
- **Pourquoi** : les interfaces S3 → S2 doivent correspondre aux fichiers et outils réellement livrés.
- **État** : intégré (constaté).

### 20. lot2-C § 8 — Workflows et ARCHITECTURE § 10
- **Décision** : reporté au **lot 5** (C) : `ci.yml`, `securite.yml`, `deploy.yml`, `tableau.yml`, `validations.yml` et `verifier_validations.py` ; valeurs de retries, base persistante et sauvegardes, mécanisme de rollback ; procédure de production locale.
- **Pourquoi** : c'est le contenu même du lot workflows (ARCHITECTURE § 11) ; le `deployeur` s'arrête proprement tant qu'ils n'existent pas.
- **État** : reporté (lot 5).

### 21. lot2-C § 9 — Plan B si `agent_type` manque
- **Décision** : sans objet tant que `agent_type` est transmis aux hooks (test réel du 2026-11-23). Le plan B (hook dans le frontmatter des agents, option `--agent` déjà testée) ne se réactive que si un test ultérieur le contredit. Mention dans ARCHITECTURE § 6 (Pourquoi du garde-fou 7).
- **Pourquoi** : la voie de repli est documentée et testée ; l'appliquer maintenant ajouterait une configuration inutile.
- **État** : reporté (conditionnel, sans objet aujourd'hui).

### 22. lot2-C § 10 — Risque : un hook introuvable ne bloque rien
- **Décision** : note de risque et parades dans ARCHITECTURE § 6 (commande `python` puis `python3`, fermeture en cas de doute, procédure du README). `"onFailure": "block"` et le filet CI `validations.yml` sont reportés au **lot 5**.
- **Pourquoi** : une protection qui peut tomber sans bruit n'est pas une protection. `onFailure` exige Claude Code 2.1.295 ou plus (2.1.285 installé), et un champ inconnu risquerait d'invalider tout `settings.json`.
- **État** : intégré en partie ; reporté pour le reste (lot 5).

### 23. lot2-C § 11 — Procédure « vérifier ses hooks » dans le README
- **Décision** : constaté déjà faite par C ; complétée par les tests `test_tableau.py` et `test_sonde_sante.py` (§ 34).
- **Pourquoi** : chaque nouveau poste et chaque mise à jour peuvent désactiver les hooks sans bruit.
- **État** : intégré (constaté).

## Périmètre D

### 24. lot2-D § 1 — Catalogue et arborescence des agents S2
- **Décision** : ARCHITECTURE § 4 : outils livrés de `veilleur` (+ Grep, Edit), `analyste-prod` (+ Glob, Edit ; Bash limité à la sonde), `gestionnaire-crise` (diagnostic précisé) ; colonne « Modèle » pour les 13 agents. ARCHITECTURE § 3 : `sonde_sante.py`, `test_sonde_sante.py`, `requirements.txt`, rapports de suivi.
- **Pourquoi** : le catalogue doit décrire ce qui est livré. La sonde, choisie par Ethan à la revue du plan, réutilise le contrat `/health` de `verifier_prod.py` et remplace `curl`.
- **État** : intégré.

### 25. lot2-D § 2 — Listes blanches Bash d'`analyste-prod` et de `gestionnaire-crise`
- **Décision** : `restreindre_bash.py` :
  - `analyste-prod` : `python|python3|py scripts/sonde_sante.py [options sûres]` uniquement ;
  - `gestionnaire-crise` : la sonde, `git log` et `git rev-parse` (sans `--output` ni `--ext-diff`), `gh run list` et `gh run view` ; jamais `gh workflow run`, `gh run rerun` ni `gh run watch`.

  Tests ajoutés dans `scripts/test_restreindre_bash.py` (`test_analyste_prod`, `test_gestionnaire_crise`). Les règles 3 et 6 de ces agents citent le hook.
- **Pourquoi** : le champ `tools` autorise Bash entier ; le `gestionnaire-crise` intervient en production pendant une crise, moment où une commande de trop coûte le plus cher.
- **État** : intégré.

### 26. lot2-D § 3 — Règles `allow` de `settings.json`
- **Décision** : ajout, en `python` et en `python3`, de `scripts/test_tableau.py`, `scripts/sonde_sante.py *` et `scripts/test_sonde_sante.py`.
- **Pourquoi** : sans règle `allow`, chaque lancement demande une confirmation, ce qui gêne le suivi de production et la procédure « vérifier ses hooks ».
- **État** : intégré.

### 27. lot2-D § 4 — R9 appliqué techniquement
- **Décision** : `proteger_valide.py` refuse Write, Edit et MultiEdit sur `PORTFOLIO.md` (racine) et `projets/<slug>/TABLEAU.md`, avec un message qui renvoie à `python scripts/tableau.py` ; 3 tests ajoutés. ARCHITECTURE § 6 : **garde-fou 8 « fichiers générés »**, qui n'ont pas d'en-tête standard. Le Pourquoi de R9 le mentionne.
- **Pourquoi** : R9 n'était appliquée que par consigne ; un tableau retouché à la main mentirait, et la règle « la validation est appliquée techniquement » (DEC-001 § 7) s'étend naturellement aux fichiers générés.
- **État** : intégré.

### 28. lot2-D § 5 — Champs de date du ticket
- **Décision** : `templates/ticket.md` v0.2 : `statut_depuis` (rempli à la création et à chaque changement de statut), `debut_le` et `termine_le` (facultatifs). `creer-ticket` les remplit ; la règle commune C11 des 13 agents impose leur tenue (arbitrage d'Ethan). ARCHITECTURE § 7 les mentionne.
- **Pourquoi** : sans date de travail, `tableau.py` estime l'ancienneté d'un blocage et le Gantt à partir de `maj_le`, qu'une simple correction de faute fait bouger. Le script lit déjà ces champs.
- **État** : intégré.

### 29. lot2-D § 6 — Templates manquants et données simulées
- **Décision** : création de `templates/rapport-suivi.md` (structure fixée par l'`analyste-prod`), référencé par S2 § 2. Conventions de nommage des données simulées écrites dans S2 § 3. `templates/runbook.md` (facultatif) et les données simulées elles-mêmes sont reportés au **lot 6**.
- **Pourquoi** : R2, chaque livrable suit son template ; sans convention de nommage, les agents S2 ne retrouvent pas leurs entrées. Les 4 runbooks ont déjà une structure commune, et aucun agent n'en produit.
- **État** : intégré en partie ; reporté pour le reste (lot 6).

### 30. lot2-D § 7 — Workflow `tableau.yml` et CI
- **Décision** : reporté au **lot 5** (C) : `tableau.yml` (installation de `requirements.txt`, lancement quotidien, commit seulement s'il y a des changements) et tests de D dans `ci.yml`.
- **Pourquoi** : les workflows relèvent du lot 5.
- **État** : reporté (lot 5).

### 31. lot2-D § 8 — Hypothèses de calcul de `tableau.py`
- **Décision** : ARCHITECTURE § 7 : capacité agent de 7 h/j, un ticket à la fois ; capacité salarié ; jours ouvrés ; ordonnancement ; budget consommé avec ANNULE et coût projeté à terminaison ; utilisation AF9 ; « sans mise à jour » ; Gantt ; préavis ; alertes ajoutées.
- **Pourquoi** : un chiffre du tableau de bord doit pouvoir s'expliquer en soutenance ; une hypothèse écrite seulement dans le code n'est pas une règle de l'équipe.
- **État** : intégré.

### 32. lot2-D § 9 — Tickets internes à l'ESN
- **Décision** : reporté (arbitrage d'Ethan). En attendant, le `veilleur` répartit son temps entre les tickets « Veille » des projets surveillés, et les pistes transverses restent dans son rapport, d'où le coordinateur les présente à l'humain.
- **Pourquoi** : la création d'un projet interne exige un budget de fonctionnement et une deadline, décisions humaines qui ne sont pas encore prises.
- **État** : reporté (décision humaine à prendre).

### 33. lot2-D § 10 — S2
- **Décision** : S2 § 2 : sources et sortie de l'`analyste-prod`. S2 § 6 : liens vers les runbooks, incidents de rollback reçus du `deployeur`, le `gestionnaire-crise` ne lance jamais de rollback lui-même. **Nouvelle S2-R7** : une régression constatée après un déploiement vérifié donne une décision humaine « rollback ou correctif ». S3-R6 précise qu'il ne vise que l'échec de vérification. En-tête : B pour le fichier, D pour le système.
- **Pourquoi** : S2 doit décrire ce qui est livré ; la distinction sur le rollback évite qu'un agent annule une mise en production validée par un humain.
- **État** : intégré.

### 34. lot2-D § 11 — README et `equipe/agents.md`
- **Décision** : README : `pip install -r requirements.txt`, tests `test_tableau.py` et `test_sonde_sante.py`, état d'avancement des lots. `equipe/agents.md` : les 13 agents existent et sont assignables.
- **Pourquoi** : sans PyYAML, `tableau.py` ne tourne pas ; le chef-de-projet ne doit pas refuser d'assigner un ticket à un agent qui existe.
- **État** : intégré.

### 35. lot2-D § 12 — Temps partiel
- **Décision** : information prise en compte (le temps partiel est moyenné sur 5 jours, écrit dans ARCHITECTURE § 7). Le champ `jours_travailles` n'est pas ajouté.
- **Pourquoi** : la différence ne peut décaler une fin projetée que d'un jour sur un projet d'une semaine ; on ne l'ajoutera, par R11, que si l'équipe le demande.
- **État** : reporté (information, sans suite tant que l'équipe ne le demande pas).

## Demande d'Ethan

### 36. Recette humaine
- **Décision** :
  - **S3** : porte **3 bis « Recette humaine »** entre la sécurité (porte 3) et le GO (porte 4) ; nouvelle règle **S3-R9 · Pas de GO sans rapport de recette CONFORME** portant sur le SHA du GO.
  - **Règle du verdict (« Must stricts »)** : CONFORME si tous les critères des exigences Must sont OK et qu'aucun bug `critique` ou `haute` issu de la recette n'est ouvert ; un KO sur un Should ou un Could est admis s'il a son ticket bug. Toute correction impose une nouvelle recette sur le nouveau SHA.
  - **CLAUDE.md** : étape 6 bis du pipeline, point d'arrêt, règle **R16**.
  - **`templates/rapport-recette.md`** : critère du CDC, résultat, ticket bug lié, verdict CONFORME / NON CONFORME. `templates/_ENTETE.md` admet `responsable: salarie:<prenom>`.
  - **Skill `.claude/skills/recette/SKILL.md`** : procédure du recetteur humain (liste des critères, test au SHA candidat, tickets bug via `creer-ticket`, re-test, rapport). Claude n'écrit jamais un résultat que l'humain n'a pas constaté.
  - **`deployeur`** : vérifie un rapport de recette CONFORME sur le SHA attendu avant la porte 4 ; `templates/rapport-deploiement.md` v0.2 a la ligne de précondition correspondante.
  - **`chef-de-projet`** (règle 6) : un ticket « Recette » dans chaque planning, toujours assigné à un salarié qui a `recette-fonctionnelle` au moins au niveau `confirme` et qui n'est pas l'auteur du code ; le GO en dépend.
  - ARCHITECTURE § 3, § 4 et § 5 et S4 § 5 sont mis en cohérence.
- **Pourquoi (Ethan)** : les tests des agents et de la CI vérifient le code au regard de ses propres critères. Seul un humain qui utilise l'app comme le client vérifie qu'elle répond au CDC, et un agent qui teste du code écrit par un agent en partage les angles morts. De plus, la recette engage l'ESN auprès du client (AF1) : un humain identifié atteste la conformité avant le GO.
- **État** : intégré.

### 37. Arbitrages transverses
- **A3 = B1** : un doublon, une seule règle (R14).
- **A2, B7, C1, C2, D2** : un seul garde-fou « Bash par agent » (n° 7), qui décrit les 5 listes blanches.
- **B5 + D5** : une seule modification de `templates/ticket.md` ; `competence_requise` remplace la ligne de la Description.
- **C4 ↔ D10** : S3-R6 (rollback sans GO) est limité à l'échec de vérification ; une régression ultérieure relève de S2-R7.
- **Recette ↔ AF6** : la compétence `recette-fonctionnelle` est aussi celle du `testeur` ; la recette humaine est une exception explicite à AF6 (toujours un salarié).
- **Recette ↔ numérotation** : la porte « 3 bis » évite de renuméroter les portes 4 à 8 citées par le `deployeur`, `rapport-deploiement` et `verifier-prod`.
- **Recette ↔ `_ENTETE.md`** : `salarie:<prenom>` est admis dans `responsable`.
- **Remarque corrigée** : la liste blanche du `deployeur` acceptait `git log --output=…`, qui écrit un fichier. Elle applique désormais le même filtre que `relecteur-code` et `gestionnaire-crise` : `git log` et `git rev-parse` sans `--output` ni `--ext-diff` (`restreindre_bash.py`, fonction `git_lecture`), avec le test `test_deployeur_git_sans_ecriture` dans `scripts/test_restreindre_bash.py`.

## Pourquoi
Les points des fichiers `a-integrer` décrivent des écarts entre ce que les règles disent et ce qui a été livré ; les laisser en suspens rendrait le système indéfendable en soutenance. Chaque point est intégré avec sa justification d'origine, ou reporté avec une raison explicite. La recette humaine et les listes blanches S2 renforcent la supervision humaine et l'application technique des règles, qui sont au cœur de la consigne.

## Impacts
- **Règles nouvelles ou modifiées** : R5 (Pourquoi), R9 (Pourquoi), R13, R14, R15, R16, points d'arrêt (CLAUDE.md) ; S1 § 4 et § 6 ; S2-R7 ; S3-R6, S3-R9, porte 3 bis, S3 § 5 et § 6 ; ARCHITECTURE § 6 (garde-fous 1, 6, 7, 8) et § 7.
- **Fichiers** :
  - documents : `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/systemes/S1` à `S4` ;
  - agents : les 13 (règle C11), plus des règles propres dans `chef-de-projet`, `deployeur`, `dev-backend`, `dev-frontend`, `architecte`, `analyste-besoin`, `analyste-prod` et `gestionnaire-crise` ;
  - skills : `creer-ticket`, et le nouveau `recette` ;
  - templates : `ticket` (v0.2), `rapport-deploiement` (v0.2), `_ENTETE` (v0.3), et les nouveaux `existant`, `rapport-suivi`, `rapport-recette` ;
  - code et configuration : `.claude/hooks/restreindre_bash.py`, `.claude/hooks/proteger_valide.py`, `.claude/settings.json`, `scripts/test_restreindre_bash.py`, `scripts/test_proteger_valide.py` ;
  - autres : `README.md`, `equipe/agents.md`, `docs/a-integrer/lot2-*.md`.
- **Reports** : lot 5 (C8, C10 en partie, D7) ; lot 6 (D6 en partie) ; décision humaine ultérieure (D9) ; sans objet ou information (C9, D12).
- **À signaler à D** : `competence_requise` existe dans le ticket ; `tableau.py` peut l'exploiter (taux de couverture des compétences).
- **Tickets** : aucun.
