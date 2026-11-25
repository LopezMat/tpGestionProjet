---
titre: Console de consultation de l'ESN (outil interne, lecture seule)
statut: EN_REVUE
responsable: D
version: 0.2
maj_le: 2026-11-25
valide_par:                 # rempli par l'humain qui valide
decision: DEC-012           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-012
date: 2026-11-25
decide_par: Ethan
projet: ESN
ticket:                     # outil interne : aucun ticket client (DEC-009, point D)
modifie_une_regle: oui      # nouvel outil et sa règle : la console n'écrit que dans console/
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-012 — Console de consultation de l'ESN

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la demande d'Ethan du 2026-11-25. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. Le « Pourquoi » est celui d'Ethan (skill `tracer-decision`, étape 1).
>
> **Numérotation.** DEC-011 est déjà pris sur la branche `demo/reservation` (projet `reservation-coworking`). Cette décision prend donc le numéro suivant. Le 2026-11-25, avant le commit, DEC-012 était libre dans le dossier de travail principal et sur toutes les branches distantes. Il faut le vérifier de nouveau avant la fusion, puisque la numérotation est globale et qu'un numéro n'est jamais réutilisé.

## Contexte
Pour suivre l'ESN, l'équipe lit aujourd'hui des fichiers Markdown bruts : tickets, `TABLEAU.md`, `PORTFOLIO.md`, fiches `equipe/`, agents, skills, décisions. Avant la soutenance, Ethan a demandé une console de consultation générée depuis le dépôt. C'est un outil interne, comme `scripts/tableau.py`, et non un projet client.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| 1. Site statique généré par `scripts/console.py`, lecture seule, ouvert sans serveur (retenue) | aucune installation au-delà de PyYAML ; mêmes calculs que `tableau.py` ; fonctionne hors ligne ; ne touche à aucune source de vérité | à régénérer après chaque changement (une commande) ; un convertisseur Markdown maison, volontairement simple |
| 2. Statu quo : lecture des fichiers Markdown, de `TABLEAU.md` et de `PORTFOLIO.md` | aucun coût | peu lisible pour l'équipe et le jury ; aucune vue Kanban ni vue d'ensemble des agents |
| 3. Traiter la console comme un projet client interne (CDC, architecture, tickets, circuit S3 complet) | démontrerait le pipeline une seconde fois | impossible dans le temps restant avant la soutenance |

## Décision
1. **`scripts/console.py`** génère un site statique dans **`console/`**, ignoré par Git. On l'ouvre par `console/index.html`, sans serveur. Le script n'utilise que la bibliothèque standard et PyYAML, et fonctionne avec `python` comme avec `python3`.
2. **Lecture seule.** La console n'écrit jamais en dehors de `console/` : une fonction d'écriture unique refuse tout autre chemin. Elle ne réécrit ni les tickets, ni `TABLEAU.md`, ni `PORTFOLIO.md` (R9), et ne laisse pas de `__pycache__`. Les seules pages qu'elle supprime sont les pages `.html` obsolètes de `console/`.
3. **Mêmes calculs que les tableaux de bord.** Les chiffres viennent des fonctions de `scripts/tableau.py`, sans recopie. Pour cela, trois fonctions ont été extraites dans `tableau.py`, sans aucun changement de sa sortie : `charger`, `alertes_equipe` et `libelle_fin`.
4. **Pages** :
   - « Notre système », en tête de la navigation : vision, chiffres clés, les 4 systèmes, circuit des agents (Mermaid d'ARCHITECTURE § 5), points d'arrêt humains (CLAUDE.md R7) et garde-fous (ARCHITECTURE § 6), tous lus dans les fichiers ;
   - Portefeuille ;
   - fiche projet (synthèse, Kanban par statut, Gantt, tickets et documents rendus) ;
   - Équipe ;
   - Agents et skills, avec les agents regroupés par système (S1, S2, S3, S4, réalisation) et une phrase d'introduction par système ;
   - Décisions ;
   - VISION, ARCHITECTURE, CLAUDE, README, CHANGELOG et S1 à S4 rendus en pages.
5. **Présentation soignée pour la démonstration** : feuille de style maison sans framework, thème clair, mise en page responsive, badges de couleur par statut et par priorité, barres de progression pour l'avancement et le budget.
6. **Mermaid hors ligne** : une copie épinglée, `scripts/vendor/mermaid.min.js` (Mermaid 12.3.0, licence MIT dans `scripts/vendor/mermaid-LICENSE`), est copiée dans `console/assets/` à chaque génération. L'option `--mermaid-src` permet d'utiliser le CDN à la place.
7. **Schéma du circuit en plein écran** : sous le diagramme de « Notre système », le lien « Ouvrir le schéma en plein écran » mène à `console/circuit.html`. Cette page ne contient que le diagramme, ajusté à la largeur de l'écran, pour la projection au jury. Dans « Notre système », le schéma garde sa taille réelle, avec défilement horizontal.
8. **Gantt en couleurs selon le statut**, propre à la console : `done` pour TERMINE, `active` pour EN_COURS et EN_REVUE, `crit` pour BLOQUE et ATTENTE_HUMAIN, sans marqueur pour les autres statuts, avec une légende sous le diagramme. La console réutilise `tableau.gantt()` (dates, sections, jalon) et remplace seulement les marqueurs. `tableau.py` n'est pas modifié : son Gantt marque aussi `crit` les tickets de priorité critique, et `TABLEAU.md` reste identique octet pour octet (vérifié).
9. **Phrases à taper au coordinateur** : comme elles ne figurent dans aucun fichier, elles sont définies dans le dictionnaire `PHRASES` de `console.py`. Un agent ou un skill absent de ce dictionnaire reçoit une phrase générique, signalée comme telle sur la page.

## Pourquoi
*(Ethan, 2026-11-25)*
- L'équipe doit pouvoir suivre les projets sans lire des fichiers bruts.
- C'est un outil interne et non un projet client, faute de temps avant la soutenance.

## Impacts
- **Fichiers** :
  - nouveaux : `scripts/console.py`, `scripts/test_console.py` (repris automatiquement par `ci.yml`), `scripts/vendor/mermaid.min.js`, `scripts/vendor/mermaid-LICENSE` ;
  - modifiés : `scripts/tableau.py` (extraction sans changement de sortie, vérifiée par comparaison avant/après et par `test_tableau.py`), `.gitignore` (`/console/`), `.gitattributes` (`scripts/vendor/*.js -diff`), `README.md` (section « Console » et test ajouté), `docs/decisions/README.md`, `docs/CHANGELOG-REGLES.md`.
- **Règle** : nouvelle règle d'outillage, « la console est en lecture seule et n'écrit que dans `console/`, non versionné ». Elle figure dans le CHANGELOG (R11).
- **À faire par un humain** : `docs/ARCHITECTURE.md` est `VALIDÉ` et donc figé (R6). Son arborescence (§ 3) sera complétée avec `console.py`, `test_console.py` et `vendor/` lors de sa prochaine révision.
- **Tickets** : aucun. C'est un outil interne, et le client ne paie pas l'outillage de l'ESN (DEC-009, point D).
