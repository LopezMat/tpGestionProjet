---
titre: Membres humains de l'équipe projet (equipe/humains.md) et leur place dans « Le bureau »
statut: VALIDÉ
responsable: D
version: 1.0
maj_le: 2026-11-26
valide_par:    Ethan             # rempli par l'humain qui valide
decision: DEC-018           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-017
date: 2026-11-26
decide_par: Ethan
projet: ESN
ticket:                     # outil interne et données d'équipe : aucun ticket client (DEC-009, point D)
modifie_une_regle: oui      # DEC-016 point 3 : un humain cité hors equipe/membres/ n'est plus toujours un visiteur
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-017 — Membres humains de l'équipe projet

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision d'Ethan du 2026-11-26 (branche `equipe/membres-humains`). Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`.
>
> **Numérotation.** Le 2026-11-26, avant le commit, DEC-017 était libre dans `docs/decisions/` et sur toutes les branches locales et distantes (après `git fetch --all`).

## Contexte
L'équipe projet compte quatre humains : Ethan, Johan, Stéphane et Matthieu. Ce sont eux qui décident et valident (R5, R7) et qui jouent les salariés aux arrêts humains. Aucun fichier ne les listait. Ils ne figurent pas dans `equipe/membres/`, qui décrit les salariés fictifs de l'ESN simulée (Claire, Hugo, Karim, Léa, Nadia), avec un coût, une capacité et une allocation.

Conséquence dans la page « Le bureau » (DEC-016, point 3) : un humain n'apparaissait que s'il était cité par un journal ou un `decide_par`, comme visiteur créé à la volée. Selon la graphie, il pouvait apparaître en double (« Stéphane » et « stephane », « Ethan » et « salarie:ethan » quand le prénom différait d'un salarié). Un membre jamais cité, comme Matthieu, n'apparaissait pas du tout.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| 1. Fichier `equipe/humains.md` (en-tête standard, liste `humains:`), lu par `bureau.py` (retenue) | une seule source, lisible par les humains et par le code ; un membre ajouté apparaît sans modifier le code ; rien ne change pour `tableau.py` | un fichier de plus dans `equipe/` |
| 2. Fiches dans `equipe/membres/` | format déjà lu | ils deviendraient des salariés comptés par `tableau.py` (coût, capacité, allocation, utilisation AF9) : confusion avec les salariés fictifs |
| 3. Liste des prénoms écrite dans `bureau.py` | rien à créer | ajouter un membre demande de modifier le code ; la composition de l'équipe n'est pas une donnée de code |

## Décision
1. **`equipe/humains.md`** liste les membres humains de l'équipe projet : Ethan, Johan, Stéphane et Matthieu. Il porte l'en-tête standard et un champ `humains:` (une entrée `- prenom: <Prénom>` par membre). Ce sont les vrais membres du groupe : ils décident, valident (R5, R7) et jouent les salariés aux arrêts humains. On ne leur attribue **ni lettre A à D, ni salarié joué**. Ils n'ont ni coût, ni capacité, ni allocation, et `tableau.py` ne lit pas ce fichier. Comme tout `equipe/`, il n'est écrit que par le coordinateur, après décision humaine (CLAUDE.md § 5).
2. **Dans « Le bureau »**, chaque membre listé est un personnage de nature « membre de l'équipe projet » (`humain:<prénom>`, accessoire tampon, couleur propre), **toujours présent à l'accueil**, même s'il n'est cité par aucun journal ni aucune décision.
3. **Rattachement des acteurs.** Un acteur de journal, un assigné ou un `decide_par` qui correspond à un membre est rattaché à son personnage, sans doublon :
   - la casse et les accents sont ignorés (« Ethan », « ETHAN », « Stéphane », « stephane ») ;
   - le préfixe `salarie:` est accepté (« salarie:ethan ») quand aucun salarié fictif ne porte ce prénom ;
   - les formes déjà reconnues par DEC-016 restent valables (« X (saisi par Y) », « coordinateur pour X ») ; un prénom suivi d'un nom (« Stéphane Martin ») désigne le membre.
   - Si un salarié fictif porte le même prénom qu'un membre, `salarie:<prénom>` désigne le salarié et le prénom seul désigne le membre ; le cas est signalé dans les anomalies de la page.
4. **Les autres acteurs inconnus restent des visiteurs** (« Le professeur », « Équipe ESN »), comme le prévoit DEC-016.
5. **Un membre ajouté plus tard** à `equipe/humains.md` apparaît sans modifier le code. Un fichier absent ne fait pas échouer la génération (comportement de DEC-016) ; une entrée vide, mal formée ou en double est ignorée et signalée dans les anomalies.
6. **Instantané** : un ticket `ATTENTE_HUMAIN` assigné à un membre (`salarie:ethan`, par exemple) place le « ! » au-dessus de ce membre.

## Pourquoi
*(Ethan, 2026-11-26)*
- Les humains qui décident doivent être visibles dans le bureau, même avant d'avoir signé une décision : c'est le cœur de la supervision humaine.
- Ils ne doivent pas être confondus avec les salariés fictifs, qui sont des données de simulation (coût, capacité), ni avec des visiteurs de passage.
- Une seule personne doit donner un seul personnage, quelle que soit la graphie utilisée dans les journaux.

## Impacts
- **Fichiers** :
  - nouveaux : `equipe/humains.md`, ce fichier ;
  - modifiés : `scripts/bureau.py` (lecture d'`equipe/humains.md`, personnages `humain:`, rattachement des acteurs), `scripts/bureau.js` (accueil et fiche du membre), `scripts/test_bureau.py`, `README.md` (section « Le bureau »), `docs/decisions/README.md`, `docs/CHANGELOG-REGLES.md`.
  - **À faire par un humain** : `docs/ARCHITECTURE.md` est `VALIDÉ` (DEC-016), donc figé pour le coordinateur (R6). Sa ligne § 3 sur `equipe/` (« membres/<prenom>.md, agents.md, calendrier.md ») devra mentionner `humains.md` quand un humain le repassera en `EN_REVUE`.
- **Règle** : DEC-016 point 3 est précisé : « un humain cité hors d'`equipe/membres/` devient un visiteur, **sauf s'il est listé dans `equipe/humains.md`** ; il est alors le membre de l'équipe projet correspondant ». Entrée dans le CHANGELOG (R11).
- **Tickets** : aucun. Outil interne et données d'équipe ; le client ne paie pas l'outillage de l'ESN (DEC-009, point D).
