---
titre: Lot 2 (périmètre B) — changements à intégrer ailleurs
statut: EN_REVUE
responsable: B
version: 0.2
maj_le: 2026-11-24
valide_par:
decision:
---

# Lot 2 (périmètre B) — changements à intégrer ailleurs

La création du `chef-de-projet`, des 8 skills (`creer-ticket`, `avancement`, `nouveau-projet`, `tracer-decision`, `arrivee-membre`, `depart-membre`, `absence`, `revision-budget`) et des données `equipe/` fait apparaître neuf changements hors de ces fichiers. **Aucun fichier partagé n'a été modifié** : chaque point est à porter par son responsable, par PR (R11 quand une règle ou un format change).

| # | Changement | Fichier | Responsable | Voie | Intégration |
|---|---|---|---|---|---|
| 1 | Le coordinateur crée un ticket de travail avant de lancer l'analyste ou l'architecte (repris de lot2-A, point 3) | `CLAUDE.md` | B | R11 (PR + décision + changelog) | intégré (DEC-002 § 4) : règle R14 |
| 2 | Ajustements AF9 et AF11 demandés à la revue du plan : utilisation des salariés = indicateur ; ticket salarié = responsabilité humaine | `CLAUDE.md` | B | R11 | intégré (DEC-002 § 5) : AF9 en CLAUDE.md § 2, AF11 = R15 |
| 3 | Remplacer les mentions « arrivent au Lot 2 / Lot 3 » par des liens vers les agents et skills livrés | `CLAUDE.md` | B | R11 | intégré (DEC-002 § 6) |
| 4 | Critères d'affectation AF1–AF11 dans S1 § 4 ; précision sur qui crée le ticket d'un événement (S1 § 6) | `docs/systemes/S1-gestion-projet.md` | B | R11 (S1 est VALIDÉ) | intégré (DEC-002 § 7) |
| 5 | Champ `competence_requise` dans le ticket | `templates/ticket.md` | A (+ D) | R11 | intégré (DEC-002 § 8) : le champ remplace la ligne de la Description |
| 6 | Lecture d'`equipe/agents.md` et `equipe/calendrier.md` ; jours ouvrés ; contrôle S1-R9 ; indicateurs AF9 et formation | `scripts/tableau.py` | D | Lot 4 | intégré (DEC-002 § 9), constaté : déjà livré par D (lot 4 en avance) |
| 7 | Limiter le Bash du `chef-de-projet` à `python scripts/tableau.py` | `.claude/settings.json` | C | Lot settings/hooks | intégré (DEC-002 § 10), constaté : déjà appliqué par le hook de C |
| 8 | Catalogue : outil Bash du chef-de-projet ; le coordinateur écrit `equipe/` | `docs/ARCHITECTURE.md` | B | R11 (ARCHITECTURE est VALIDÉ) | intégré (DEC-002 § 11) |
| 9 | Renvoyer au skill `creer-ticket` dans les agents de A | `.claude/agents/analyste-besoin.md`, `architecte.md` | A | PR (+ R11 si le comportement change) | intégré (DEC-002 § 12) |

---

## 1. Ticket de travail avant l'analyste et l'architecte (B)

**Intégration** : intégré (DEC-002 § 4) : règle R14.

**Quoi.** Reprise du point 3 de `lot2-A.md`. Ajouter dans `CLAUDE.md` (§ 1 ou § 4) : avant de lancer `analyste-besoin` ou `architecte`, le coordinateur crée un ticket de travail (« Rédaction du CDC », « Architecture »), `type: tache`, assigné à l'agent, avec une estimation. Le skill `nouveau-projet` le fait déjà pour l'analyste (T-001) ; il reste à l'écrire comme règle du coordinateur, y compris pour l'architecte.

**Pourquoi.** Les tickets de réalisation sont créés par le `chef-de-projet` après la validation du CDC et de l'architecture (S1-R1). Sans ticket de travail, le temps de l'analyste et de l'architecte n'est rattaché à rien, et le budget consommé calculé par `tableau.py` est sous-estimé. Les fichiers d'agents de A prévoient déjà ce cas.

**Voie.** Modification d'une règle du coordinateur : PR, décision et entrée dans `docs/CHANGELOG-REGLES.md` (R11).

## 2. Ajustements AF9 et AF11 demandés à la revue du plan (B)

**Intégration** : intégré (DEC-002 § 5) : AF9 en CLAUDE.md § 2, AF11 = R15.

**Quoi.** Deux critères d'affectation du `chef-de-projet` ont été précisés par Ethan à la revue du plan du Lot 2 (B). Ils sont déjà appliqués dans `.claude/agents/chef-de-projet.md` et doivent être repris dans `CLAUDE.md` (§ 2, « Choix des agents »), parce qu'ils s'imposent aussi au coordinateur.
- **AF9 devient un indicateur, pas une obligation.** Le chef calcule l'utilisation de chaque salarié (h assignées / capacité allouée) et la signale si elle est inférieure à 50 %, en proposant d'ajuster l'allocation. Il n'assigne jamais un ticket à un salarié pour atteindre un taux.
  *Pourquoi :* on évite les tickets artificiels ; l'allocation s'ajuste à la réalité du projet.
- **AF11 : ticket salarié = responsabilité humaine.** Le coordinateur ne réalise jamais de sa propre initiative un ticket `salarie:` ; il le signale comme « à faire par un humain ». L'humain qui joue le salarié peut s'aider de Claude Code dans une session dédiée, en citant le ticket ; il reste l'auteur et le responsable du résultat, valide lui-même ce qui est produit et note son temps en heures équivalent humain.
  *Pourquoi :* la responsabilité humaine est réelle (c'est l'humain qui décide et vérifie), l'outil n'y change rien ; c'est aussi la réalité d'une ESN où les salariés utilisent l'IA.

**Pourquoi le porter dans CLAUDE.md.** AF11 limite ce que fait le coordinateur, pas seulement le chef-de-projet. Une règle qui n'est écrite que dans le fichier d'un agent ne lie pas la session principale.

**Voie.** R11 : PR, décision (qui cite la revue du plan) et entrée dans le changelog.

## 3. Références aux agents et skills livrés dans CLAUDE.md (B)

**Intégration** : intégré (DEC-002 § 6).

**Quoi.** Remplacer « Les fichiers `.claude/agents/*.md` arrivent au Lot 2 » (§ 2), « Le skill `nouveau-projet` arrive au Lot 3 » (§ 4) et « skills dédiés (Lot 3) » (§ 5) par des liens vers `.claude/agents/` et `.claude/skills/<nom>/SKILL.md`. Ajouter au § 4 l'appel du skill `nouveau-projet` et, au § 5, le renvoi vers `arrivee-membre`, `depart-membre`, `absence` et `revision-budget`.

**Pourquoi.** Le coordinateur doit savoir que ces procédures existent pour les utiliser ; une mention « à venir » l'inciterait à improviser.

**Voie.** R11 (modification du fichier de règles du coordinateur), même PR que les points 1 et 2.

## 4. Critères d'affectation et événements dans S1 (B)

**Intégration** : intégré (DEC-002 § 7).

**Quoi.**
- **S1 § 4, étape 3** : remplacer la note « À définir au Lot 2 (B) : critères d'affectation agent / salarié » par un résumé des critères AF1 à AF11 et un renvoi vers `.claude/agents/chef-de-projet.md`.
- **S1 § 6** : préciser la séquence telle que les skills l'appliquent. Le coordinateur crée le ticket `decision` (`A_FAIRE`, assigné à `agent:chef-de-projet`) ; le chef y écrit l'analyse d'impact et le passe `ATTENTE_HUMAIN` ; l'humain décide ; le coordinateur applique les changements d'`equipe/` après la décision.

**Pourquoi.** Les critères sont la pièce manquante de S1 identifiée par DEC-001. La précision sur le § 6 garde le texte de S1 (« le coordinateur crée le ticket ») tout en respectant R2 (l'analyse circule par fichier) et en comptant le temps du chef.

**Voie.** S1 est `VALIDÉ` : un humain le repasse `EN_REVUE`, puis PR, décision et changelog (R11).

## 5. Champ `competence_requise` dans le ticket (A, avec D)

**Intégration** : intégré (DEC-002 § 8) : le champ remplace la ligne de la Description.

**Quoi.** Ajouter au frontmatter de `templates/ticket.md` un champ `competence_requise: <nom> (<niveau>)`, dont le nom vient du référentiel d'`equipe/agents.md`. En attendant, la convention est une ligne `**Compétence requise** : <nom> (<niveau>)` en tête de la Description (skill `creer-ticket`).

**Pourquoi.** Les critères AF1 à AF10 et la détection des besoins de formation reposent sur la compétence requise. Un champ structuré la rend lisible par `tableau.py` (taux de couverture, compétences manquantes), alors qu'une ligne dans le corps ne l'est pas de façon fiable.

**Voie.** Le format du ticket est figé par DEC-001 et lu par `tableau.py` : PR, décision et changelog (R11), à signaler à D (ARCHITECTURE § 12).

## 6. `tableau.py` et les données d'`equipe/` (D)

**Intégration** : intégré (DEC-002 § 9), constaté : déjà livré par D (lot 4 en avance).

**Quoi.** Au Lot 4, `scripts/tableau.py` lit :
- `equipe/agents.md` : `cout_horaire_eur`, la liste `agents` (`nom`, `fichier`, `competences`) et `hors_perimetre_agents` ;
- `equipe/calendrier.md` : `jours_feries` et `evenements` (`qui`, `debut`, `fin` incluse, `capacite_pct`, `statut` ; les événements `annule` sont ignorés) ;
- les fiches salariés avec `allocation: {}` (aucun projet alloué : capacité nulle partout).

Calculs attendus : jours ouvrés (hors week-ends et jours fériés) ; fenêtre prévue de chaque ticket (dépendances, estimations, capacité) pour signaler toute affectation pendant une absence (S1-R9) ; préavis de départ en jours ouvrés (S1-R8) ; indicateur **utilisation des salariés** (h assignées / capacité allouée, alerte informative en dessous de 50 %, AF9) ; liste des tickets `formation` ouverts ; liste des tickets `salarie:` en attente d'un humain (AF11). L'`assigne` `salarie:<prenom>` correspond au nom de fichier `equipe/membres/<prenom>.md` (prénom en minuscules, sans accent).

**Pourquoi.** Les skills `avancement`, `absence` et `depart-membre` s'appuient sur ces chiffres. Sans eux, le chef-de-projet doit tout recalculer à la main.

**Voie.** Lot 4 (D) ; les formats sont figés dans les fichiers d'`equipe/` (responsable B). Toute évolution se coordonne entre B et D.

## 7. Bash du chef-de-projet limité à `tableau.py` (C)

**Intégration** : intégré (DEC-002 § 10), constaté : déjà appliqué par le hook de C.

**Quoi.** Dans `.claude/settings.json`, faire en sorte que le `chef-de-projet` ne puisse lancer que `python scripts/tableau.py` (permission `allow` sur cette commande, `ask` ou `deny` sur les autres, ou hook propre à l'agent si le format le permet).

**Pourquoi.** Le catalogue donne au chef « Bash(`python scripts/tableau.py`) », mais le champ `tools` d'un subagent autorise l'outil entier (constat déjà fait par A pour les `dev-*`). Aujourd'hui la limite n'est qu'une consigne (règle 12 du chef) ; une permission la rend effective.

**Voie.** Lot settings/hooks (C), avec le point 2 de `lot2-A.md`.

## 8. Catalogue et circuit d'`equipe/` dans ARCHITECTURE (B)

**Intégration** : intégré (DEC-002 § 11).

**Quoi.**
- § 4, ligne `chef-de-projet` : outil « Bash, limité à `python scripts/tableau.py` par consigne et permission ».
- § 3 ou § 5 : préciser que `equipe/` est écrit **uniquement par le coordinateur**, via les skills d'événements et après décision humaine ; les agents le lisent.

**Pourquoi.** La syntaxe `Bash(python scripts/tableau.py)` laisse croire à une restriction technique qui n'existe pas encore. La règle d'écriture d'`equipe/` découle de C9 et de S1 § 6, mais elle n'est écrite nulle part dans ARCHITECTURE.

**Voie.** ARCHITECTURE est `VALIDÉ` : un humain le repasse `EN_REVUE`, puis PR, décision et changelog (R11).

## 9. Renvoi au skill `creer-ticket` dans les agents de A (A)

**Intégration** : intégré (DEC-002 § 12).

**Quoi.** Dans `analyste-besoin.md` et `architecte.md`, remplacer « en suivant `templates/ticket.md` (en attendant le skill `creer-ticket`) » par « selon la procédure `.claude/skills/creer-ticket/SKILL.md` ». Le skill ajoute la ligne `**Compétence requise**` en tête de la Description.

**Pourquoi.** Le skill existe désormais ; une seule procédure de création évite des tickets de formats différents selon l'agent.

**Voie.** PR de A. Si la ligne « Compétence requise » est considérée comme un changement de comportement, entrée dans le changelog (R11).
