# tpGestionProjet — ESN virtuelle orchestrée par des agents IA

Projet de semaine du Mastère « Manager de projets informatiques » (L'Idem, 23–27 novembre 2026).
Notre équipe joue une **ESN** dont les missions sont assurées par des agents IA configurés dans ce dépôt.

> **Le produit, c'est le système multi-agents**, pas une application. Les projets clients
> (le premier est une plateforme de réservation minimale) servent à le démontrer.

## Par où commencer

| Je veux… | Lire |
|---|---|
| Comprendre le **quoi** et le **pourquoi** | [docs/VISION.md](docs/VISION.md) |
| Comprendre le **comment** (structure, agents, circuit des fichiers) | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Connaître les règles du coordinateur | [CLAUDE.md](CLAUDE.md) |
| Voir le détail d'un des 4 systèmes | [docs/systemes/](docs/systemes/) |
| Connaître les décisions prises et leur justification | [docs/decisions/](docs/decisions/) |
| Savoir comment une règle a évolué | [docs/CHANGELOG-REGLES.md](docs/CHANGELOG-REGLES.md) |
| Produire un livrable | [templates/](templates/) |

## Les 4 systèmes

| Système | Document | Responsable |
|---|---|---|
| 1 · Gestion de projet | [S1-gestion-projet.md](docs/systemes/S1-gestion-projet.md) | B |
| 2 · Suivi et maintenance | [S2-maintenance.md](docs/systemes/S2-maintenance.md) | D |
| 3 · Déploiement automatisé | [S3-deploiement.md](docs/systemes/S3-deploiement.md) | C |
| 4 · Cahier des charges | [S4-cahier-des-charges.md](docs/systemes/S4-cahier-des-charges.md) | A |

## Utilisation

1. Ouvrir le dépôt dans Claude Code : la session principale devient le **coordinateur** (règles dans `CLAUDE.md`).
2. Lui donner une demande client, par exemple : « Nouveau client : une salle de sport veut une réservation de créneaux en ligne. »
3. Le coordinateur crée l'espace `projets/<slug>/`, mobilise les agents utiles et **s'arrête à chaque validation humaine**.
4. Les humains valident en modifiant eux-mêmes l'en-tête des documents (`statut: VALIDÉ`, `valide_par`, `decision`) et en traçant la décision dans `docs/decisions/`.

## Projet interne de l'ESN

[`projets/esn-interne/`](projets/esn-interne/projet.md) porte le travail de l'ESN qui n'a pas de livrable client : le plan de formation, les outils et règles communs, et les tickets `decision` des événements d'équipe. Il n'a ni CDC, ni architecture, ni recette, ni GO : le `chef-de-projet` y propose les tickets, et un humain les arbitre. Le texte des règles fait foi : R18 et R19 de [CLAUDE.md](CLAUDE.md), S1-R13 de [S1](docs/systemes/S1-gestion-projet.md).

| Sujet | En bref | Références |
|---|---|---|
| Imputation `client` / `esn` | Un ticket est imputé au client par défaut. L'ESN ne prend un coût à sa charge que sur une décision humaine validée, citée dans le ticket. `tableau.py` sépare le coût client de la part ESN, et `PORTFOLIO.md` consolide les deux. | R18, [DEC-023](docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md) |
| Plan de formation | Les formations retenues, le budget de fonctionnement, l'échéance et les allocations à `esn-interne` sont décidés par un humain. Le registre des compétences à risque est tenu dans le [planning](projets/esn-interne/planning.md). | S1-R13, [DEC-024](docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) |
| Rétrospective | Pas de cérémonie à date fixe : la rétrospective prend la forme d'un `retex.md` suivi de tickets `amelioration` et `formation`. Celle de la semaine projet (23 au 27/11) a produit le [retex de l'ESN](projets/esn-interne/retex.md), validé, et les actions retenues par DEC-025. | [DEC-022](docs/decisions/2026-11-26-DEC-022-methodologie-retenue.md), [DEC-025](docs/decisions/2026-11-27-DEC-025-actions-retrospective-semaine.md) |

## Installer son poste

À faire une fois par membre de l'équipe, puis après chaque mise à jour de Python ou de Claude Code.

1. **Python 3.10 ou plus.** Les hooks de protection n'utilisent que la bibliothèque standard. `scripts/tableau.py` a besoin de PyYAML : `python -m pip install -r requirements.txt` (macOS : `python3 -m pip install -r requirements.txt`).
   - Windows : installateur de [python.org](https://www.python.org/downloads/), en cochant **« Add python.exe to PATH »**. Ne pas compter sur le raccourci « python3 » du Microsoft Store.
   - macOS : `brew install python`.
   - Vérifier : `python --version` (Windows) ou `python3 --version` (macOS). Les hooks utilisent `python` s'il existe, sinon `python3`.
2. **Git.** Sous Windows, Git for Windows fournit **Git Bash**, le shell dans lequel Claude Code lance les hooks.
3. **Claude Code, lancé depuis la racine du dépôt** (dans VS Code : ouvrir le dossier du dépôt). Les règles de `.claude/settings.json` dont le chemin commence par `/` (par exemple `Edit(/templates/**)`) sont relatives au dossier de lancement.
4. **Docker** (Docker Desktop sous Windows et macOS), pour la production locale (DEC-003) et pour le test réel de `scripts/test_prod_locale.py`. Sans Docker, ce test est ignoré et le reste de la suite passe, mais le poste de démonstration doit l'avoir. **Avant la soutenance**, sur ce poste, précharger les images de base pour ne dépendre d'aucun réseau : `docker pull postgres:16-alpine`, `docker pull python:3.12-alpine`, ainsi que l'image de base du `Dockerfile` de l'app de démonstration.
5. **Vérifier ses hooks.** Si Python est introuvable, Claude Code n'affiche qu'un avertissement et **laisse passer** les écritures : les protections R5 et R6 et la restriction du Bash des agents disparaissent sans bruit. Sur Mac, remplacer `python` par `python3` dans les commandes ci-dessous si `python` n'existe pas.

| # | Commande (Git Bash sous Windows, terminal sous macOS, à la racine du dépôt) | Résultat attendu |
|---|---|---|
| 1 | `python --version` (Windows) ou `python3 --version` (macOS) | `Python 3.10` ou plus |
| 2 | `printf '%s' '{"tool_name":"Write","tool_input":{"file_path":"docs/essai.md","content":"---\nstatut: validé\nvalide_par:\n---\n"}}' \| python .claude/hooks/proteger_valide.py; echo "code=$?"` | `Refusé (R5) : seul un humain passe un document à VALIDÉ…` puis `code=2` |
| 3 | Dans Claude Code : « ajoute une espace à la fin de docs/ARCHITECTURE.md » | l'édition est refusée avec un message qui contient `Refusé (R6)` (le préfixe `PreToolUse:Edit hook error` est normal). Si l'édition passe, ou si le message parle de `command not found` ou de `non-blocking status code`, la protection est **inactive** : reprendre l'étape 1. |

Dans Claude Code, `/hooks` doit lister deux hooks PreToolUse (`Write|Edit|MultiEdit` et `Bash`). Les tests doivent tous passer :

```
python scripts/test_proteger_valide.py     # macOS : python3 scripts/test_proteger_valide.py
python scripts/test_restreindre_bash.py    # macOS : python3 …
python scripts/test_verifier_prod.py       # macOS : python3 …
python scripts/test_tableau.py             # macOS : python3 …  (demande PyYAML)
python scripts/test_sonde_sante.py         # macOS : python3 …
python scripts/test_prod_locale.py         # macOS : python3 …  (test réel si Docker répond, environ 1 min 30)
python scripts/test_verifier_validations.py  # macOS : python3 …
python scripts/test_console.py             # macOS : python3 …  (demande PyYAML)
python scripts/test_bureau.py              # macOS : python3 …  (demande PyYAML ; syntaxe JS vérifiée si node est installé)
python scripts/test_qui_fait_quoi.py       # macOS : python3 …
python scripts/test_journal_direct.py      # macOS : python3 …  (hook d'observation du mode Direct)
python scripts/test_bureau_direct.py       # macOS : python3 …  (serveur local et installation du mode Direct)
```

La CI (`.github/workflows/ci.yml`) lance les mêmes tests à chaque push ; `validations.yml`, `securite.yml` et `tableau.yml` complètent le contrôle (ARCHITECTURE § 3).

Détail des risques et des parades : [docs/a-integrer/lot2-C.md](docs/a-integrer/lot2-C.md) (points 10 et 11).

## Console

Une console de consultation permet de suivre l'ESN sans lire les fichiers Markdown bruts ([DEC-012](docs/decisions/2026-11-25-DEC-012-console-consultation.md)). C'est un outil interne, comme `tableau.py`, et non un projet client.

```
python scripts/console.py                  # macOS : python3 scripts/console.py   (demande PyYAML)
```

Ensuite, ouvrir **`console/index.html`** dans un navigateur, par double-clic : aucun serveur n'est nécessaire.

| Page | Contenu |
|---|---|
| Notre système | vision, chiffres clés, les 4 systèmes, circuit des agents (Mermaid d'ARCHITECTURE § 5, avec un lien vers `circuit.html` en plein écran pour la projection), points d'arrêt humains, garde-fous |
| Portefeuille | projets, avancement, budget, fin projetée, alertes, tickets BLOQUE et ATTENTE_HUMAIN |
| Le bureau | l'ESN vue de dessus en pixel art : une pièce par système, open space, bureaux des salariés, accueil, coin café ; mode instantané (état tiré des tickets), mode replay (journaux des tickets et décisions) et mode Direct, optionnel (activité en temps réel de Claude Code, serveur local) ; voir ci-dessous |
| Fiche projet | synthèse, Kanban des tickets par statut, Gantt coloré par statut (avec légende), utilisation AF9 ; tickets, CDC, architecture et planning rendus en HTML |
| Équipe | salariés, compétences, allocations, utilisation, calendrier (absences, arrivées, départs) |
| Agents et skills | agents regroupés par système : rôle, quand l'appeler, outils, modèle, points d'arrêt, phrase à taper au coordinateur |
| Décisions | registre lu dans l'en-tête de chaque fichier `DEC`, contrôle des validations (même contrôle que `validations.yml`) |

- **Lecture seule.** Le script n'écrit que dans `console/`, qui est ignoré par Git. Il ne modifie ni les tickets, ni `TABLEAU.md`, ni `PORTFOLIO.md` (R9). Pour rafraîchir la console, relancer la commande.
- **Mêmes chiffres que les tableaux de bord.** Les calculs viennent des fonctions de `scripts/tableau.py`.
- **Hors ligne.** Les diagrammes Mermaid utilisent la copie locale `scripts/vendor/mermaid.min.js` (Mermaid 12.3.0, licence MIT dans `scripts/vendor/mermaid-LICENSE`), copiée dans `console/assets/` à chaque génération. Aucun réseau n'est nécessaire en soutenance. Pour utiliser le CDN à la place : `--mermaid-src https://cdn.jsdelivr.net/npm/mermaid@12.3.0/dist/mermaid.min.js`.
- **Options.** `--date AAAA-MM-JJ` fixe la date de calcul ; `--racine DIR` désigne un autre dépôt.

### Le bureau

La page `console/bureau.html` ([DEC-016](docs/decisions/2026-11-26-DEC-016-page-le-bureau.md)) montre l'ESN vue de dessus. Elle est dessinée en Canvas 2D par `scripts/bureau.js`, à partir des données calculées par `scripts/bureau.py`. Tout est dessiné par le code : aucun sprite, aucune police ni ressource externe, et la page fonctionne en `file://`, hors ligne.

- **Personnages.** Un par agent (`.claude/agents/`), un par salarié fictif (`equipe/membres/`), le coordinateur à l'accueil et, à côté de lui, les membres humains de l'équipe projet listés dans `equipe/humains.md` (Ethan, Johan, Stéphane, Matthieu ; [DEC-017](docs/decisions/2026-11-26-DEC-017-membres-humains-equipe.md)). La couleur dépend du système et l'accessoire du rôle. Un agent ou un membre ajouté plus tard apparaît sans changer le code. Au survol ou au clic, une fiche s'ouvre : rôle, modèle, outils, tickets en cours et lien vers sa page.
- **Membres humains de l'équipe projet.** Ils sont toujours à l'accueil, même si aucun journal ne les cite. Un acteur de journal, un assigné ou un `decide_par` qui leur correspond est rattaché à leur personnage, sans doublon : la casse et les accents sont ignorés, et le préfixe `salarie:` est accepté (« Ethan », « salarie:ethan », « Stéphane », « stephane »). Les autres humains inconnus (« Le professeur », « Équipe ESN ») restent des visiteurs de l'accueil. Sans `equipe/humains.md`, la page se génère quand même ; une entrée mal formée ou en double est signalée dans « Anomalies de données ».
- **Instantané** (projet choisi, ou « Toute l'ESN ») : l'état vient des tickets (R9).
  - `EN_COURS` : il tape à son bureau.
  - `EN_REVUE` : il va chez le relecteur, ou chez le testeur si la revue est `APPROUVÉ`.
  - `ATTENTE_HUMAIN` : « ! » au-dessus de l'humain attendu (le salarié ou le membre de l'équipe projet assigné).
  - `BLOQUE` : bulle rouge.
  - Sinon : coin café.
- **Replay** : la chronologie des lignes « Journal » des tickets et des décisions DEC. Commandes : lecture, pause, pas à pas, vitesse, curseur.
  - Le filtre **« jalons seulement »** (création, changements de statut, décisions) est actif par défaut, pour un film d'environ 1 min 30 à ×1 ; décocher pour tout voir.
  - Une décision s'affiche par une bannière « ✔ DEC-NNN · décidé par … ».
  - Les lignes de journal mal formées sont ignorées et listées dans « Anomalies de données ».
- **Accessibilité.** `prefers-reduced-motion` est respecté : aucun déplacement animé ni clignotement. Les listes « Personnages et état » et « Événements du replay » sont l'alternative texte au dessin ; la seconde suit la lecture.
- **Lien direct.** `bureau.html#projet=<slug>&mode=replay&ev=<n>&perso=<id>` ouvre un projet, un mode, un événement ou une fiche (utile pour les captures et la projection).
- **Échappement.** Les données sont injectées en JSON sans `<`, `>`, `&`, U+2028 ni U+2029 bruts ; le JS n'affiche les textes que par `textContent` et `fillText` (vérifié par `test_bureau.py`).

#### Mode Direct (optionnel, local à chaque poste)

Le mode **Direct** ([DEC-018](docs/decisions/2026-11-26-DEC-018-mode-direct-bureau.md)) montre en temps réel ce que font le coordinateur et les sous-agents dans Claude Code. Il est **optionnel** : rien ne change sur un poste qui ne l'active pas, et `.claude/settings.json` (partagé) n'est pas modifié.

**Activer, une fois par poste :**

```
python scripts/bureau_direct.py --installer      # macOS : python3 …
```

Puis **relancer Claude Code**. La commande déclare le hook d'observation `.claude/hooks/journal_direct.py` dans `.claude/settings.local.json`, qui est personnel et ignoré par Git :
- elle n'ajoute que ses propres groupes et ne touche pas au reste du fichier ;
- relancée, elle ne change rien ;
- elle fait une sauvegarde `settings.local.json.sauvegarde-…` avant toute écriture ;
- elle refuse un JSON invalide sans y toucher ;
- elle ajoute `async` seulement à partir de Claude Code 2.1.332 ; `--sans-async` force des hooks synchrones.

Dans `/hooks`, les deux hooks PreToolUse partagés restent présents, et les hooks `journal_direct.py` s'y ajoutent.

**Ouvrir le mode Direct :**

```
python scripts/bureau_direct.py --generer        # régénère la console puis sert http://127.0.0.1:8765
```

Puis ouvrir **http://127.0.0.1:8765/bureau.html#mode=direct**. Les options : `--port N` choisit un autre port, et sans `--generer`, il faut avoir lancé `scripts/console.py` avant. Ctrl+C arrête le serveur. Ouverte par double-clic (`file://`), la page garde le bouton Direct désactivé, avec cette explication.

**Désactiver :** `python scripts/bureau_direct.py --desinstaller`, puis relancer Claude Code. `ESN_DIRECT=off` suspend le journal sans désinstaller. Le dossier `direct/` peut être supprimé à tout moment.

- **Ce qui est enregistré** (`direct/evenements.jsonl`, hors Git, 2 Mio au plus avec la rotation) : l'heure, la session hachée, l'acteur (`coordinateur` ou nom de l'agent), le type d'événement, le nom de l'outil (Read, Edit, Bash… ; un outil MCP devient `mcp`) et sa catégorie.
- **Ce qui ne l'est jamais** : le texte des messages, le contenu ou le chemin des fichiers, les commandes, les sorties d'outils, le dossier de travail.
- **Le hook ne bloque jamais Claude.** Il rend toujours la main avec le code 0, abandonne l'événement en cas de doute et ne touche pas aux hooks R5, R6 et R17.
- **Animations** :

  | Ce qui se passe dans Claude Code | Ce que montre le bureau |
  |---|---|
  | message reçu | bulle « nouvelle demande » sur le coordinateur |
  | Read, Grep, Glob | icône « lit » |
  | Edit, Write | icône « écrit » |
  | Bash | icône « terminal » |
  | lancement d'un sous-agent | l'agent va à son poste |
  | fin du sous-agent | retour au café |
  | autorisation ou réponse attendue | « ! » |
  | fin du tour | le coordinateur revient à l'accueil |

- **Une seule personne au coordinateur.** Si deux sessions de coordinateur sont actives en même temps (activité dans les 15 dernières minutes), un avertissement s'affiche.
- **Sécurité du serveur.** Il écoute uniquement sur 127.0.0.1 et n'accepte que GET. L'en-tête Host est contrôlé (protection contre le DNS rebinding), aucun en-tête CORS n'est envoyé, et il est impossible de sortir de `console/`. Il n'écrit rien et n'exécute aucune commande (vérifié par `test_bureau_direct.py`).
- **Accessibilité.** `prefers-reduced-motion` est respecté. La liste « Derniers événements (direct) » est l'alternative texte au dessin.

## Page « qui fait quoi »

Une page de pilotage d'un projet, complémentaire de la console : qui travaille en ce moment, qui est attendu (humains), ce qui vient de finir et l'étape de chaque ticket de l'incrément ([DEC-014](docs/decisions/2026-11-26-DEC-014-page-qui-fait-quoi.md)). C'est un outil interne, comme la console.

```
python scripts/qui_fait_quoi.py projets/<slug>     # macOS : python3 …   (bibliothèque standard seule)
```

Ensuite, ouvrir **`qui-fait-quoi.html`**, créé à la racine du dépôt, par double-clic. Un second argument choisit un autre fichier de sortie.

- **Sources.** Les statuts viennent des tickets `projets/<slug>/tickets/T-*.md`, seule source de vérité (R9) ; les chiffres viennent de `TABLEAU.md`. L'instantané `projets/<slug>/qui-fait-quoi.json` (qui travaille, qui est attendu, étape de chaque ticket, personnages) est **tenu par le coordinateur** : le mettre à jour, puis relancer la commande.
- **Lecture seule.** Le script n'écrit que la page de sortie. `qui-fait-quoi.html` est **ignoré par Git** ; seuls le modèle `scripts/qui_fait_quoi_modele.html` et l'instantané sont versionnés.
- **Échappement.** Les textes des tickets et de l'instantané ne peuvent pas injecter de balise : en-tête échappé en HTML, JSON sans `<`, `>` ni `&` bruts, personnages échappés dans le modèle (vérifié par `test_qui_fait_quoi.py`).

## État d'avancement

Construction par lots. Le contenu de chaque lot est décrit dans [docs/ARCHITECTURE.md § 11](docs/ARCHITECTURE.md#11-plan-de-construction-par-lots).

| Lot | Objet | État |
|---|---|---|
| 1 | Socle documentaire | en revue (intégration du lot 2 : DEC-002) |
| 2 | Agents (13) | livré, en revue ; points transverses intégrés par DEC-002 |
| 3 | Skills | livré en avance avec le lot 2-B (8 skills) et le lot 2-C (`verifier-prod`) ; skill `recette` ajouté par DEC-002 |
| 4 | `tableau.py` et tests | livré en avance avec le lot 2-D, avec la sonde `sonde_sante.py` |
| 5 | Settings, hooks, workflows | `settings.json` et les deux hooks livrés avec le lot 2-C ; production locale Docker (`deployer_local.py`, `rollback_local.py`), workflows de contrôle (`ci`, `securite`, `validations`, `tableau`) et ARCHITECTURE § 10 livrés, en revue (DEC-003) ; `onFailure: "block"` en attente de Claude Code 2.1.295 |
| 6 | Projet de démonstration | à venir |
