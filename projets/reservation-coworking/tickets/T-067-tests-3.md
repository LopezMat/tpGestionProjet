---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-067
titre: Tests (3/3) — vérification des correctifs de l'audit d'incrément
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:testeur      # agent:<nom> | salarie:<prenom>
competence_requise: tests-unitaires (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 2.5          # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-26
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25         # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-067 — Tests (3/3) — vérification des correctifs de l'audit d'incrément

## Description
Ticket de travail du `testeur` (porte 2 de S3) pour vérifier les 6 tickets de réalisation issus du triage du 2026-11-25 : T-058, T-060, T-061, T-062, T-063 et T-065, environ 0,4 h par ticket ; ajout du triage de T-054 (2026-11-25, 14 h 45) : T-069, T-070, T-071 et T-072, soit 10 tickets et 4 h. T-041 (en cours) n'est pas modifié. Le `testeur` passe `TERMINE` les tickets vérifiés selon R13, à l'exception de T-058 et T-072, tickets salariés que Nadia passe elle-même `TERMINE` après la vérification (R13, R15). Il ne passe pas ce ticket de travail `TERMINE` : le coordinateur conclut.

Pas de `depend_de` vers les tickets vérifiés (le passage `TERMINE` en dépend).

## Critères d'acceptation
- [ ] Chacun des 10 tickets a une ligne de journal du `testeur` avec le SHA vérifié, les critères cochés ou non, et le résultat des suites (ou le ticket est `ANNULE`).
- [ ] Pour T-058 : le critère « rôle non superutilisateur » est constaté sur une instance déployée jetable, pas seulement par lecture.
- [ ] Pour T-069 : le scénario de la base gelée avec une connexion déjà poolée est rejoué sur une instance jetable (pas seulement le test automatisé).
- [ ] Une ligne de journal par campagne ici, avec le temps.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage des suites de T-054 : T-069, T-070, T-071 et T-072 ajoutés, critère T-069 ajouté ; estimation 2,5 → 4 h (sous 7 h, règle 3). Temps compté dans T-008 · 0 h
- 2026-11-25 16:15 · agent:testeur · campagne 5 (SHA 16282cc9dfe9e10af529ebf607d579961c52e9ae) : T-062 vérifié 5/5, passé TERMINE ; T-063 critères 1 à 3 cochés, critère 4 (console navigateur) non constaté, reste EN_REVUE (revue humaine T-064 manquante) ; suite complète 183 passed (Python 3.14.10, PostgreSQL 16) ; non-régression T-054, T-010, T-011 OK ; aucune régression ni bug créé, aucun test manquant. Détail : rapports/tests-2026-11-25.md, campagne 5. Reste à vérifier : T-058, T-060, T-061, T-065, T-069 à T-072 (ticket laissé EN_COURS) · 1 h
- 2026-11-25 15:30 · agent:testeur · campagne 6 (SHA 9114f9e4ff26b35c6fd219b05da94165b47c1a78) : T-060 vérifié 3/3 et T-071 vérifié 4/4, passés TERMINE ; suite complète 214 passés (Python 3.14.10, PostgreSQL 16) ; non-régression T-054, T-062, T-063, T-010, T-011 OK ; aucune régression ni bug créé, aucun test manquant. Détail : rapports/tests-2026-11-25.md, campagne 6. Reste à vérifier : T-058, T-061, T-065, T-069, T-070, T-072 (ticket laissé EN_COURS) · 0.6 h
- 2026-11-25 16:30 · agent:testeur · campagne 6 (suite) : T-073 vérifié sur le SHA 748c75e3a2b458d144f63d1327e7bcd83255f31c (216 passés, 4/4 critères cochés), laissé EN_REVUE (seule manque la revue humaine T-074) ; suite aussi rejouée sur 748c75e pour T-060 et T-071 (verdict maintenu sur 9114f9e) · 0.3 h
- 2026-11-26 10:30 · agent:testeur · campagne 7 (SHA 011ac347bd3674518d9592347125cd948580669b, code de app/ identique à 748c75e) : suite complète 216 passés, 0 ignoré, 0 échec ; T-054 vérifié 7/7 et passé TERMINE (revue humaine T-068 faite) ; T-063 critère 4 constaté dans Chrome headless via DevTools (0 erreur CSP, témoin positif OK), 4/4 cochés, reste EN_REVUE (revue humaine T-064 manquante) ; T-073 4/4 maintenus, reste EN_REVUE (revue humaine T-074 manquante) ; aucune régression, aucun bug ni tâche créé. Détail : rapports/tests-2026-11-25.md, campagne 7. Reste à vérifier : T-058, T-061, T-065, T-069, T-070, T-072 (ticket laissé EN_COURS) · 0.6 h
