---
titre: Lot 2 (périmètre A) — changements à intégrer ailleurs
statut: EN_REVUE
responsable: A
version: 0.1
maj_le: 2026-11-23
valide_par:
decision:
---

# Lot 2 (périmètre A) — changements à intégrer ailleurs

La création des 4 agents du périmètre A (`analyste-besoin`, `architecte`, `dev-backend`, `dev-frontend`) fait apparaître trois changements hors de ce périmètre. **Aucun fichier partagé n'a été modifié** : chaque point est à porter par son responsable, par PR (R11 quand une règle ou un format change).

| # | Changement | Fichier | Responsable | Voie |
|---|---|---|---|---|
| 1 | Créer le template de l'analyse de l'existant | `templates/existant.md` | A | R11 (PR + décision + changelog) |
| 2 | Interdire ou soumettre à confirmation `git push`, `--force`, `reset --hard` pour les agents | `.claude/settings.json` | C | Lot settings/hooks |
| 3 | Le coordinateur crée un ticket de travail avant de lancer l'analyste ou l'architecte | `CLAUDE.md` | B | R11 (PR + décision + changelog) |

---

## 1. `templates/existant.md` à créer (A)

**Quoi.** Un template pour `projets/<slug>/existant.md`, produit par `analyste-besoin` à l'étape 0 d'une modernisation : en-tête standard, ligne de provenance, et 4 sections : Fonctionnalités, Données, Dette technique, Risques.

**Pourquoi.** S4 § 3 et CLAUDE.md § 1 exigent une analyse de l'existant validée avant toute architecture, mais aucun template ne la définit. R2 impose que chaque livrable suive un template ; sans lui, l'agent improvise le format et l'architecte ne sait pas quoi lire. Le choix d'un fichier séparé du CDC (et non d'une section) permet de le valider avant d'écrire le CDC.

**Voie.** Les templates sont protégés (`ask` sur `templates/**`, DEC-001 § 25) et lus par les agents : ajout par PR, avec une décision et une entrée dans `docs/CHANGELOG-REGLES.md`.

## 2. Permissions sur les commandes git destructrices (C)

**Quoi.** Dans `.claude/settings.json` : `deny` sur `git push --force`, `git reset --hard` ; `ask` (ou `deny` pour les agents) sur `git push`. Ces règles complètent celles déjà prévues en S3 § 5.

**Pourquoi.** `dev-backend` et `dev-frontend` ont l'outil `Bash` (tests et git local). Le champ `tools` d'un subagent autorise l'outil entier : il ne filtre pas les sous-commandes. L'interdiction du `push` écrite dans les fichiers d'agents n'est donc qu'une consigne ; seule une permission la rend effective. C'est le même principe que pour `VALIDÉ` : appliqué techniquement, pas seulement écrit (DEC-001 § 7).

**Voie.** Lot settings/hooks (C). À vérifier au passage : si le format des subagents permet de déclarer des hooks ou des permissions propres à l'agent, on peut restreindre Bash au niveau de `dev-*` seulement.

## 3. Ticket de travail avant l'analyste et l'architecte (B)

**Quoi.** Ajouter dans `CLAUDE.md` (§ 1 ou § 4) : avant de lancer `analyste-besoin` ou `architecte`, le coordinateur crée un ticket de travail (« Rédaction du CDC », « Architecture »), `type: tache`, assigné à l'agent, avec une estimation.

**Pourquoi.** Les tickets sont créés par le `chef-de-projet` après la validation du CDC et de l'architecture (S1-R1). Le temps passé par l'analyste et l'architecte n'est donc rattaché à aucun ticket, et le budget consommé calculé par `tableau.py` le sous-estime. Les fichiers d'agents prévoient déjà ce cas : s'ils reçoivent un ticket de travail, ils le passent `EN_COURS` puis `EN_REVUE` et y notent leur temps.

**Voie.** Modification d'une règle du coordinateur : PR, décision et entrée dans `docs/CHANGELOG-REGLES.md` (R11).
