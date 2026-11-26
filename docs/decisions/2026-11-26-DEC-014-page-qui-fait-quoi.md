---
titre: Page de pilotage « qui fait quoi » (outil interne, régularisation)
statut: VALIDÉ
responsable: D
version: 1.0
maj_le: 2026-11-26
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-014           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-014
date: 2026-11-26
decide_par: Ethan
projet: ESN
ticket:                     # outil interne : aucun ticket client (DEC-009, point D)
modifie_une_regle: oui      # nouvel outil et sa règle : sortie générée hors Git, statuts lus dans les tickets
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-014 — Page de pilotage « qui fait quoi »

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision d'Ethan du 2026-11-26 (PR de règles `regles/coherence`). Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`. Le « Pourquoi » reprend les mots d'Ethan (skill `tracer-decision`, étape 1).
>
> **Numérotation.** Le 2026-11-26, avant le commit, DEC-014 était libre dans `docs/decisions/` et sur toutes les branches locales et distantes.

## Contexte
La PR #14 (`demo/increment-consultation`, commit `1350ccb`) a ajouté, sans décision, `scripts/qui_fait_quoi.py`, son modèle `scripts/qui_fait_quoi_modele.html`, l'instantané `projets/reservation-coworking/qui-fait-quoi.json` et la page générée `qui-fait-quoi.html`, versionnée à la racine du dépôt. Or toute modification de l'outillage de l'ESN passe par une décision et une entrée du changelog (R11), comme la console l'a fait avec [DEC-012](2026-11-25-DEC-012-console-consultation.md). À la relecture, deux points d'échappement étaient aussi à corriger : les données JSON n'étaient protégées que contre `</` dans la balise `<script>`, et le nom et les couleurs des personnages entraient dans du SVG passé par `innerHTML` sans échappement, contrairement à ce qu'annonçait un commentaire du modèle.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| 1. Garder l'outil et le régulariser : décision, tests, README, changelog, page générée hors Git (retenue) | la page sert déjà au pilotage de l'incrément ; même traitement que la console | une décision et des tests à écrire après coup |
| 2. Retirer l'outil | rien à régulariser | perte d'une vue utile pour la soutenance |
| 3. Le fusionner dans la console | un seul outil | travail important avant la soutenance ; la console couvre l'ESN, cette page suit un incrément |

## Décision
1. **`scripts/qui_fait_quoi.py` est un outil interne de l'ESN** : une page de pilotage « qui fait quoi », **complémentaire de la console** (DEC-012). La console présente l'ESN entière ; cette page montre, pour un projet, qui travaille, qui est attendu et où en est chaque ticket de l'incrément.
2. **Les statuts viennent des tickets** `projets/<slug>/tickets/T-*.md`, seule source de vérité (R9). Les chiffres viennent de `TABLEAU.md`, généré par `tableau.py`.
3. **L'instantané `projets/<slug>/qui-fait-quoi.json` est tenu par le coordinateur** : ce qui tourne, ce qui attend un humain, ce qui vient de finir, l'étape de chaque ticket de l'incrément et les personnages. Il est versionné. Il ne porte aucun statut de ticket.
4. **La page générée sort de Git.** `qui-fait-quoi.html` (racine du dépôt, sortie par défaut quel que soit le dossier courant) est ajouté à `.gitignore` et retiré de l'index (`git rm --cached`). Le modèle `scripts/qui_fait_quoi_modele.html` reste versionné.
5. **Lecture seule et échappement.** Le script n'écrit que son fichier de sortie. Les champs de l'en-tête sont échappés en HTML ; le JSON inséré dans `<script>` n'a aucun `<`, `>` ni `&` brut (échappements `\uXXXX`, JSON toujours valide) ; le remplacement des champs du modèle se fait en un seul passage ; dans le modèle, le nom et les couleurs d'un personnage passent par `attr()` avant d'entrer dans le SVG.
6. **Tests** : `scripts/test_qui_fait_quoi.py` (génération, statuts lus dans les tickets, lecture seule hors fichier de sortie, échappement HTML, sortie par défaut, page hors Git), repris automatiquement par `ci.yml` comme tous les `scripts/test_*.py`.

## Pourquoi
*(Ethan, 2026-11-26)*
- L'outil a été ajouté dans la PR #14 sans décision : on le garde et on le régularise.
- C'est une page de pilotage complémentaire de la console ; l'instantané est tenu par le coordinateur et les statuts viennent des tickets (R9).
- page utile pour savoir qui doit agir, faite par Johan ; on la garde et on la sécurise

## Impacts
- **Fichiers** :
  - nouveaux : `scripts/test_qui_fait_quoi.py`, ce fichier ;
  - modifiés : `scripts/qui_fait_quoi.py` (sortie par défaut à la racine du dépôt, JSON échappé, remplacement en un passage, docstring), `scripts/qui_fait_quoi_modele.html` (`attr()` et `perso()` pour les personnages), `.gitignore` (`/qui-fait-quoi.html`), `README.md` (section « Page qui fait quoi » et test ajouté), `docs/decisions/README.md`, `docs/CHANGELOG-REGLES.md` ;
  - retiré de l'index Git : `qui-fait-quoi.html` (le fichier local reste et se régénère).
- **Documents** : `docs/ARCHITECTURE.md` § 3 liste le script, son modèle et son test (même PR, document repassé `EN_REVUE` par Ethan).
- **Règle** : nouvelle règle d'outillage, « la page qui fait quoi est en lecture seule, sa sortie n'est pas versionnée, ses statuts viennent des tickets ». Elle figure dans le CHANGELOG (R11).
- **Tickets** : aucun. C'est un outil interne, et le client ne paie pas l'outillage de l'ESN (DEC-009, point D).
