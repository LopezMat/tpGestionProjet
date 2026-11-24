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

## Installer son poste

À faire une fois par membre de l'équipe, puis après chaque mise à jour de Python ou de Claude Code.

1. **Python 3.10 ou plus.** Les hooks de protection n'utilisent que la bibliothèque standard. `scripts/tableau.py` a besoin de PyYAML : `python -m pip install -r requirements.txt` (macOS : `python3 -m pip install -r requirements.txt`).
   - Windows : installateur de [python.org](https://www.python.org/downloads/), en cochant **« Add python.exe to PATH »**. Ne pas compter sur le raccourci « python3 » du Microsoft Store.
   - macOS : `brew install python`.
   - Vérifier : `python --version` (Windows) ou `python3 --version` (macOS). Les hooks utilisent `python` s'il existe, sinon `python3`.
2. **Git.** Sous Windows, Git for Windows fournit **Git Bash**, le shell dans lequel Claude Code lance les hooks.
3. **Claude Code, lancé depuis la racine du dépôt** (dans VS Code : ouvrir le dossier du dépôt). Les règles de `.claude/settings.json` dont le chemin commence par `/` (par exemple `Edit(/templates/**)`) sont relatives au dossier de lancement.
4. **Vérifier ses hooks.** Si Python est introuvable, Claude Code n'affiche qu'un avertissement et **laisse passer** les écritures : les protections R5 et R6 et la restriction du Bash des agents disparaissent sans bruit. Sur Mac, remplacer `python` par `python3` dans les commandes ci-dessous si `python` n'existe pas.

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
```

Détail des risques et des parades : [docs/a-integrer/lot2-C.md](docs/a-integrer/lot2-C.md) (points 10 et 11).

## État d'avancement

Construction par lots. Le contenu de chaque lot est décrit dans [docs/ARCHITECTURE.md § 11](docs/ARCHITECTURE.md#11-plan-de-construction-par-lots).

| Lot | Objet | État |
|---|---|---|
| 1 | Socle documentaire | en revue (intégration du lot 2 : DEC-002) |
| 2 | Agents (13) | livré, en revue ; points transverses intégrés par DEC-002 |
| 3 | Skills | livré en avance avec le lot 2-B (8 skills) et le lot 2-C (`verifier-prod`) ; skill `recette` ajouté par DEC-002 |
| 4 | `tableau.py` et tests | livré en avance avec le lot 2-D, avec la sonde `sonde_sante.py` |
| 5 | Settings, hooks, workflows | `settings.json` et les deux hooks livrés avec le lot 2-C ; workflows et ARCHITECTURE § 10 à venir |
| 6 | Projet de démonstration | à venir |
