---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-075
titre: Contrôle statique du front par analyse HTML (constat 20)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: tests-unitaires (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-055]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-075 — Contrôle statique du front par analyse HTML (constat 20)

## Description
**Origine.** Constat 20 (bas) de l'audit [securite-2026-11-26.md](../rapports/securite-2026-11-26.md) et remarques 1 et 2 du `relecteur-code` sur [T-055](T-055-page-disponibilites-lecture.md) (commit `dc53a1d`). Créé sans être traité : périmètre gelé avant la soutenance du 2026-11-27, à trier par le `chef-de-projet`.

`app/tests/test_front_statique.py`, qui remplace le test supprimé de `test_en_tetes_hote.py`, contrôle les pages par expressions régulières. Il couvre plus de cas que l'ancien test mais laisse passer :
- un attribut `on…=` ou `style=` sans espace devant (`<svg/onload=…>`, `<p id="a"onclick="…">`, `<p/style=…>`), que l'ancien test refusait ;
- un `<script src=//hote/x.js>` sans guillemets ou un `<script src="data:…">` ;
- tout fichier de `static/` d'une autre extension que `.html`, `.js` et `.css` (`.svg`, `.htm`, `.mjs`).

Rien d'exploitable aujourd'hui : la page livrée ne contient aucun de ces motifs, et la CSP du serveur les bloque dans le navigateur. Le risque est qu'une régression de T-022 ou T-023 passe le contrôle automatique. À faire avant T-022 et T-023 (le `chef-de-projet` décide s'il faut l'inscrire dans leur `depend_de`).

## Critères d'acceptation
- [ ] Les pages sont analysées avec `html.parser` (bibliothèque standard), sans nouvelle dépendance : tout attribut `on*` ou `style`, tout `<style>`, tout `<script>` à corps non vide et tout `src`/`href` qui ne désigne pas une ressource du même site sont refusés, quelle que soit la façon dont l'attribut est écrit.
- [ ] Des cas négatifs sont testés : au minimum `<svg/onload=…>`, `<p id="a"onclick="…">`, `<p/style=…>`, `<script src=//hote/x.js>` (sans guillemets) et `<script src="data:…">` sont refusés.
- [ ] Tout fichier de `static/` est contrôlé ou explicitement refusé selon son extension (`.svg`, `.htm`, `.mjs` compris).
- [ ] Les pages actuelles passent le contrôle et la suite complète reste verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 14:00 · agent:coordinateur · création (constat 20 de securite-2026-11-26, remarques 1 et 2 du relecteur-code sur T-055), non traité : périmètre gelé · 0 h
