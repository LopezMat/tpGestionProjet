---
titre: Lot 2 (périmètre D) — changements à intégrer ailleurs
statut: EN_REVUE
responsable: D
version: 0.2
maj_le: 2026-11-24
valide_par:
decision:
---

# Lot 2 (périmètre D) — changements à intégrer ailleurs

Le périmètre D de ce lot comprend :
- les 4 agents S2 : `veilleur`, `analyste-prod`, `support`, `gestionnaire-crise` ;
- les 4 runbooks : `perte-donnees`, `coupure-serveur`, `intrusion`, `rollback` ;
- `scripts/tableau.py` et `scripts/test_tableau.py`, en avance sur le lot 4, et `requirements.txt` (PyYAML) ;
- la sonde `scripts/sonde_sante.py` et `scripts/test_sonde_sante.py`.

Leur création fait apparaître douze changements hors de ces fichiers. **Aucun fichier partagé n'a été modifié** : chaque point est à porter par son responsable, par PR (R11 quand une règle ou un format change). Le point 7 relève du lot 5.

| # | Changement | Fichier | Responsable | Voie | Intégration |
|---|---|---|---|---|---|
| 1 | Catalogue : outils des 4 agents S2 ; `curl` remplacé par `sonde_sante.py` ; arborescence (sonde, tests, `requirements.txt`, rapports de suivi) | `docs/ARCHITECTURE.md` § 3 et § 4 | B | R11 (ARCHITECTURE est VALIDÉ) | intégré (DEC-002 § 24) |
| 2 | Listes blanches Bash pour `analyste-prod` et `gestionnaire-crise` | `.claude/hooks/restreindre_bash.py`, `scripts/test_restreindre_bash.py` | C | PR (+ R11 : nouveau comportement) | intégré (DEC-002 § 25) |
| 3 | Règles `allow` pour les nouveaux scripts et tests | `.claude/settings.json` | C | PR | intégré (DEC-002 § 26) |
| 4 | R9 appliqué techniquement : Write/Edit refusés sur `TABLEAU.md` et `PORTFOLIO.md` ; statut des fichiers générés | `.claude/hooks/proteger_valide.py`, `docs/ARCHITECTURE.md` § 6 | C, B | R11 | intégré (DEC-002 § 27) |
| 5 | Champs facultatifs de date dans le ticket (`statut_depuis`, `debut_le`, `termine_le`) | `templates/ticket.md` | A (+ D) | R11 | intégré (DEC-002 § 28) |
| 6 | Templates manquants (`rapport-suivi`, `runbook`) et conventions des données simulées | `templates/`, lot 6 | A, puis lot 6 | R11 | intégré (DEC-002 § 29) pour `rapport-suivi.md` et les conventions de nommage (S2 § 3) ; reporté au lot 6 pour `runbook.md` (facultatif) et les données simulées |
| 7 | Workflow `tableau.yml` (dont `pip install -r requirements.txt` et un lancement quotidien) ; tests D dans `ci.yml` | `.github/workflows/` | C | **lot 5** | reporté (lot 5 : workflows ; DEC-002 § 30) |
| 8 | Hypothèses d'ordonnancement et de calcul de `tableau.py` | `docs/ARCHITECTURE.md` § 7 | B | R11 | intégré (DEC-002 § 31) |
| 9 | Pas d'espace pour les tickets internes à l'ESN (veille commune, améliorations transverses) | `docs/ARCHITECTURE.md` § 3, `CLAUDE.md` | B | décision humaine, puis R11 | reporté (décision humaine à prendre : budget et deadline d'un projet interne non décidés ; DEC-002 § 32) |
| 10 | S2 : runbooks livrés, sonde de l'analyste-prod, responsable du fichier | `docs/systemes/S2-maintenance.md` | B (fichier), D (système) | R11 (S2 est VALIDÉ) | intégré (DEC-002 § 33) : nouvelle S2-R7 |
| 11 | README : `pip install -r requirements.txt`, état des lots ; `equipe/agents.md` : agents de D disponibles | `README.md`, `equipe/agents.md` | B | PR | intégré (DEC-002 § 34) |
| 12 | Temps partiel moyenné (pas de semaine type dans la fiche) | `templates/membre.md` | A, B | information | reporté (information sans suite tant que l'équipe ne demande pas `jours_travailles` ; DEC-002 § 35) |

---

## 1. Catalogue et arborescence (B)

**Intégration** : intégré (DEC-002 § 24).

**Quoi.** Dans `docs/ARCHITECTURE.md` :
- **§ 4**, outils des agents S2, tels que livrés :

  | Agent | Catalogue actuel | Livré | Écart |
  |---|---|---|---|
  | `veilleur` | Read, Glob, Write, WebSearch, WebFetch | Read, Glob, **Grep**, Write, **Edit**, WebSearch, WebFetch | Grep pour dédoublonner les CVE dans les tickets ; Edit pour le journal du ticket « Veille » |
  | `analyste-prod` | Read, Grep, Write, Bash(`curl`) | Read, **Glob**, Grep, Write, **Edit**, Bash | Bash limité à `python scripts/sonde_sante.py …` (point 2) ; Glob pour trouver le dernier rapport ; Edit pour son journal |
  | `support` | Read, Glob, Grep, Write, Edit | inchangé | — |
  | `gestionnaire-crise` | Read, Glob, Grep, Write, Edit, Bash (diagnostic) | inchangé | « diagnostic » précisé : `sonde_sante.py`, `git log`, `git rev-parse`, `gh run list\|view` (point 2) |

  Modèles retenus : `veilleur` sonnet, `analyste-prod` sonnet, `support` haiku, `gestionnaire-crise` opus (justifiés dans chaque fichier).
- **§ 3** : ajouter `scripts/sonde_sante.py` et `scripts/test_sonde_sante.py` (D), `requirements.txt` à la racine (D), et `rapports/suivi-AAAA-MM-JJ.md` dans `projets/<slug>/rapports/`.

**Pourquoi.** Le catalogue doit décrire ce qui est réellement livré. Pour la sonde, le choix a été fait par Ethan à la revue du plan : un script dédié plutôt que `curl`. Il réutilise les fonctions `url_sante`, `sonder` et `comparer` de `verifier_prod.py` : le contrat `/health` reste écrit une seule fois. Il n'accepte que http et https, envoie un User-Agent générique, n'écrit aucun fichier, et ajoute ce que `verifier-prod` ne mesure pas : le temps de réponse (S2 § 3) et plusieurs mesures espacées (réveil de Render). C'est la même logique de sécurité que C, qui a remplacé `curl` par `verifier_prod.py` pour le `deployeur` (lot2-C, point 1).

**Voie.** ARCHITECTURE est `VALIDÉ` : un humain le repasse `EN_REVUE`, puis PR, décision et changelog (R11).

## 2. Listes blanches Bash des agents S2 (C)

**Intégration** : intégré (DEC-002 § 25).

**Quoi.** Dans `.claude/hooks/restreindre_bash.py`, ajouter à `LISTES_BLANCHES` et à `autorise_liste_blanche` :
- `analyste-prod` : `python|python3|py scripts/sonde_sante.py …` uniquement ;
- `gestionnaire-crise` : `python|python3|py scripts/sonde_sante.py …`, `git log …`, `git rev-parse …`, `gh run list …`, `gh run view …`. **Pas** `gh workflow run`.

Ajouter les cas correspondants dans `scripts/test_restreindre_bash.py`. `veilleur` et `support` n'ont pas l'outil Bash : rien à faire pour eux.

**Constat (vérifié à la livraison).** Le hook actuel **ne bloque pas à tort** les agents de D : sans liste blanche, ils ne subissent que les contrôles communs. La commande de la sonde et `git log` passent (code 0), `git push` est refusé (code 2). En revanche, rien ne les empêche aujourd'hui de lancer une autre commande : la limite n'est qu'une consigne (règle 3 de l'`analyste-prod`, règle 6 du `gestionnaire-crise`).

**Pourquoi.** Même raisonnement que lot2-B point 7 et lot2-C point 1 : le champ `tools` autorise Bash entier. Le `gestionnaire-crise` intervient en production pendant une crise, moment où une commande de trop coûte le plus cher.

**Voie.** PR de C ; entrée dans le changelog (nouvelle restriction).

## 3. `settings.json` : règles `allow` (C)

**Intégration** : intégré (DEC-002 § 26).

**Quoi.** Ajouter, en `python` et en `python3` :
- `Bash(python scripts/test_tableau.py)` ;
- `Bash(python scripts/sonde_sante.py *)` ;
- `Bash(python scripts/test_sonde_sante.py)`.

`scripts/tableau.py` est déjà autorisé.

**Pourquoi.** Sans règle `allow`, chaque lancement demande une confirmation, ce qui gêne le suivi de production et la procédure « vérifier ses hooks », que la sonde pourrait compléter.

**Voie.** PR de C.

## 4. R9 appliqué techniquement (C, B)

**Intégration** : intégré (DEC-002 § 27).

**Quoi.**
- Dans `proteger_valide.py` : refuser Write, Edit et MultiEdit sur `PORTFOLIO.md` à la racine et sur `projets/*/TABLEAU.md`, avec un message qui renvoie à `python scripts/tableau.py`. Le script, lui, écrit par Python et n'est pas concerné.
- Dans ARCHITECTURE § 6 : garde-fou « fichiers générés », et la précision que `TABLEAU.md` et `PORTFOLIO.md` **n'ont pas d'en-tête standard**. Ce ne sont pas des documents à valider, puisqu'ils changent à chaque génération. Ils commencent par `<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9) -->` et un encadré qui le rappelle.

**Pourquoi.** Aujourd'hui, R9 n'est appliquée que par consigne (C7 de chaque agent). Un tableau retouché à la main mentirait, et la règle « la validation est appliquée techniquement » (DEC-001 § 7) s'étend naturellement aux fichiers générés.

**Voie.** R11 : PR de C (hook et tests), PR de B (ARCHITECTURE), décision et changelog.

## 5. Champs facultatifs de date dans le ticket (A, avec D)

**Intégration** : intégré (DEC-002 § 28).

**Quoi.** Ajouter au frontmatter de `templates/ticket.md` trois champs **facultatifs** :
- `statut_depuis: AAAA-MM-JJ` : date du dernier changement de statut ;
- `debut_le: AAAA-MM-JJ` : date du premier passage `EN_COURS` ;
- `termine_le: AAAA-MM-JJ` : date du passage `TERMINE`.

Rappel : le champ `competence_requise` (lot2-B, point 5) reste à arbitrer dans la même PR.

**Pourquoi.** Le ticket n'a aucune date de travail. `tableau.py` doit donc estimer :
- l'ancienneté d'un `BLOQUE` ou d'un `ATTENTE_HUMAIN`, à partir de la dernière ligne de journal qui contient « bloqu » ou « attente », à défaut `maj_le` ;
- les barres des tickets terminés du Gantt, de `cree_le` à `maj_le`.

Ces estimations sont fragiles : une simple correction de faute change `maj_le`. **`tableau.py` lit déjà ces trois champs s'ils sont présents**, donc l'ajout ne demande aucun changement du script. Pour les tickets ouverts, aucun champ de date planifiée n'est proposé : le script calcule la fenêtre (dépendances, estimation, capacité de l'assigné depuis la date du jour), ce qui évite une date saisie et vite périmée.

**Voie.** Le format du ticket est figé par DEC-001 et lu par `tableau.py` : PR de A, décision et changelog (R11), puis mise à jour de la procédure `creer-ticket` (B) et des agents qui changent un statut.

## 6. Templates manquants et données simulées (A, lot 6)

**Intégration** : intégré (DEC-002 § 29) pour `rapport-suivi.md` et les conventions de nommage (S2 § 3) ; reporté au lot 6 pour `runbook.md` (facultatif) et les données simulées.

**Quoi.**
- `templates/rapport-suivi.md` pour l'`analyste-prod`. En attendant, sa structure est fixée dans l'agent : en-tête standard, puis Sources (réel ou simulé), Disponibilité et version, Performances, Erreurs et bugs, Tickets créés, Rien à signaler.
- `templates/runbook.md`, facultatif. Les 4 runbooks suivent déjà une structure commune : Déclencheurs et sévérité, Rôles, Détection, Minutes 0–15, Escalade, Points de décision humaine, Retour à la normale, Post-mortem, Ce que les agents ne font jamais, Points ouverts.
- Conventions des données simulées, pour le projet de démonstration (lot 6) :
  - `projets/<slug>/support/entrant/AAAA-MM-JJ-<n>.md` (date, canal, message, aucune donnée personnelle réelle) ;
  - `projets/<slug>/rapports/logs-AAAA-MM-JJ.log` ;
  - `projets/<slug>/rapports/metriques-AAAA-MM-JJ.csv`.

**Pourquoi.** R2 : chaque livrable suit son template. Sans convention de nommage, les agents S2 ne retrouvent pas leurs entrées.

**Voie.** PR de A pour les templates (R11) ; les conventions sont appliquées au lot 6.

## 7. Workflow `tableau.yml` et CI (C, lot 5)

**Intégration** : reporté (lot 5 : workflows ; DEC-002 § 30).

**Quoi.**
- `tableau.yml` :
  1. `actions/setup-python` puis `python -m pip install -r requirements.txt` ;
  2. `python scripts/tableau.py` ;
  3. commit de `PORTFOLIO.md` et `projets/*/TABLEAU.md` **seulement s'il y a des changements**, avec `[skip ci]` et un groupe `concurrency` (DEC-001 § 11).

  Déclencheurs : push sur `projets/**/tickets/**`, `projets/*/projet.md`, `equipe/**`, **et un `schedule` quotidien** (par exemple chaque jour ouvré à 6 h), parce que les alertes dépendent de la date : un ticket devient « sans mise à jour » sans que rien ne change dans le dépôt. Le script n'écrit un fichier que si son contenu change, et le contenu ne porte que la date (pas l'heure) : au plus un commit par jour.
- `ci.yml` : lancer `python scripts/test_tableau.py` et `python scripts/test_sonde_sante.py` (après installation de `requirements.txt`) sur les PR qui touchent `scripts/**`, `equipe/**` ou `templates/ticket.md`.

**Pourquoi.** Les workflows relèvent du lot 5 (C). PyYAML est la première dépendance hors bibliothèque standard du dépôt : un runner sans installation ferait échouer le script, qui sort alors avec le code 2 et un message explicite.

**Voie.** Lot 5 (C).

## 8. Hypothèses de calcul de `tableau.py` dans ARCHITECTURE § 7 (B)

**Intégration** : intégré (DEC-002 § 31).

**Quoi.** Compléter les formules du § 7 par les hypothèses appliquées. Elles sont aussi affichées dans chaque `TABLEAU.md`.
- **Capacité d'un agent : 7 h équivalent humain par jour ouvré, un ticket à la fois** ; des agents différents travaillent en parallèle. Arbitré par Ethan à la revue du plan. C'est la constante `CAPACITE_AGENT_H_JOUR`, révisable par décision.
- **Capacité d'un salarié** : `capacite_h_semaine ÷ 5 × allocation au projet × capacite_pct` du calendrier. Elle est nulle avant l'arrivée, après le départ, et pour un salarié `parti`.
- **Ordonnancement** à partir de la date du jour : dépendances, puis priorité (critique → basse), puis id ; un ticket à la fois par assigné et par projet (l'allocation sépare les projets, S1-R10). Les tickets `BLOQUE` et `ATTENTE_HUMAIN` sont supposés débloqués le jour même, ce qui rend la date optimiste. Un ticket est **non planifiable** s'il est sans capacité, s'il ne peut pas finir avant le départ de son assigné ou s'il est pris dans un cycle, et il lève une alerte.
- **Budget consommé** : compte aussi le temps des tickets `ANNULE`, puisqu'il a été dépensé. Nouveau : **coût projeté à terminaison** = consommé + Σ reste × taux.
- **Utilisation (AF9)** : heures restantes assignées ÷ capacité allouée, d'aujourd'hui à la deadline (ou à la fin projetée si la deadline est passée). Elle est signalée sous 50 % (information) et au-dessus de 100 % (surcharge).
- **Alertes ajoutées** : S1-R9 (fenêtre prévue d'un ticket salarié qui chevauche une absence), ticket non planifiable, surcharge, allocation totale supérieure à 100 % (S1-R10).
- **« Sans mise à jour »** : la date retenue est la plus récente entre `maj_le` et la dernière ligne du journal.
- **Préavis** : jours ouvrés de demain à la date de départ incluse (même calcul que le skill `depart-membre`).

**Pourquoi.** Un chiffre du tableau de bord doit pouvoir s'expliquer en soutenance. Une hypothèse écrite seulement dans le code n'est pas une règle de l'équipe.

**Voie.** R11, dans la même PR que le point 1.

## 9. Tickets internes à l'ESN (B, décision)

**Intégration** : intégré (DEC-023), après un report (DEC-002 § 32) :
- projet interne `projets/esn-interne/` (CLAUDE.md R19), avec le plan de formation (S1-R13), les outils et règles communs et les décisions d'événements d'équipe ;
- budget de fonctionnement, échéance et allocations décidés par DEC-024 ;
- la veille commune reste régie par S2.

**Quoi.** Certains travaux n'appartiennent à aucun projet client :
- la veille commune (`veille/`) ;
- une piste d'outil pour toute l'ESN ;
- une amélioration d'agent issue de plusieurs projets ;
- la mise à jour d'un runbook après un post-mortem.

Il faut une décision : un projet interne, par exemple `projets/esn-interne/` avec un budget de fonctionnement, ou une règle de répartition du temps entre projets. En attendant, le `veilleur` répartit son temps entre les tickets « Veille » des projets surveillés, et laisse les pistes transverses dans son rapport, d'où le coordinateur les présente à l'humain.

**Pourquoi.** `tableau.py` ne chiffre que les tickets d'un projet. Sans espace interne, le coût de la veille et des améliorations transverses est invisible, ou imputé arbitrairement à un client.

**Voie.** Décision humaine, puis R11 (ARCHITECTURE § 3, et CLAUDE.md si le coordinateur doit créer ces tickets).

## 10. S2 (B pour le fichier, D pour le système)

**Intégration** : intégré (DEC-002 § 33) : nouvelle S2-R7.

**Quoi.** Dans `docs/systemes/S2-maintenance.md` :
- **§ 2** : sources de l'`analyste-prod` = sonde `scripts/sonde_sante.py` (réel) et `rapports/logs-*` / `metriques-*` (simulé) ; sortie `rapports/suivi-AAAA-MM-JJ.md`.
- **§ 6** : remplacer « Les runbooks arrivent dans un lot ultérieur » par les liens vers `runbooks/*.md`. Préciser que le `gestionnaire-crise` reçoit aussi les incidents de rollback créés par le `deployeur` (lot2-C, point 7), et qu'il ne lance jamais de rollback lui-même : il le demande au `deployeur` via le coordinateur (R1).
- **§ 4 et § 5** : préciser qu'une régression constatée **après** un déploiement vérifié donne une décision humaine « rollback ou correctif », puisqu'elle revient sur un GO. Le rollback sans nouveau GO (S3-R6) ne vise que l'échec de vérification.
- **En-tête** : `responsable: B` alors que le README et ARCHITECTURE § 12 attribuent S2 à D. À aligner, avec B comme responsable du fichier ou D comme responsable du système, comme pour S3.

**Pourquoi.** S2 doit décrire ce qui est livré ; la distinction sur le rollback évite qu'un agent annule une mise en production validée par un humain.

**Voie.** S2 est `VALIDÉ` : un humain le repasse `EN_REVUE`, puis PR, décision et changelog (R11).

## 11. README et `equipe/agents.md` (B)

**Intégration** : intégré (DEC-002 § 34).

**Quoi.**
- `README.md`, section « Installer son poste » : `python -m pip install -r requirements.txt` (Mac : `python3 -m pip …`), et `python scripts/test_tableau.py` et `python scripts/test_sonde_sante.py` dans la liste des tests à garder verts. Section « État d'avancement » : lot 4 (`tableau.py`) livré en avance, avec le lot 2-D.
- `equipe/agents.md`, paragraphe « Disponibilité » : les fichiers des agents de D existent désormais, ils sont donc assignables (règle 7 du `chef-de-projet`).

**Pourquoi.** Sans PyYAML, `tableau.py` ne tourne pas (il le dit et sort avec le code 2). Le chef-de-projet ne doit pas refuser d'assigner un ticket « Suivi de production » ou « Support » à un agent qui existe.

**Voie.** PR de B.

## 12. Temps partiel (A, B, information)

**Intégration** : reporté (information sans suite tant que l'équipe ne demande pas `jours_travailles` ; DEC-002 § 35).

**Quoi.** La fiche salarié ne décrit pas de semaine type. La capacité de Nadia (28 h, pas de travail le mercredi) est donc **moyennée** à 5,6 h par jour ouvré. Si l'équipe veut un calcul exact, il faudrait un champ facultatif `jours_travailles: [lun, mar, jeu, ven]` dans `templates/membre.md` ; `tableau.py` serait alors adapté (D).

**Pourquoi.** Sur un projet d'une semaine, la différence peut décaler une fin projetée d'un jour. Il faut le savoir avant de défendre une date.

**Voie.** Information ; R11 si l'équipe veut le champ.
