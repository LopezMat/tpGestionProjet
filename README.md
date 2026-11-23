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

## État d'avancement

Construction par lots. Le contenu de chaque lot est décrit dans [docs/ARCHITECTURE.md § 11](docs/ARCHITECTURE.md#11-plan-de-construction-par-lots).

| Lot | Objet | État |
|---|---|---|
| 1 | Socle documentaire | en revue |
| 2 | Agents | à venir |
| 3 | Skills | à venir |
| 4 | `tableau.py` et tests | à venir |
| 5 | Settings, hooks, workflows | à venir |
| 6 | Projet de démonstration | à venir |
