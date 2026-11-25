---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-041
titre: Tests (1/2) — vérification des tickets de réalisation
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS           # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:testeur      # agent:<nom> | salarie:<prenom>
competence_requise: tests-unitaires (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 6             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 2.5          # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-041 — Tests (1/2) — vérification des tickets de réalisation

## Description
Ticket « Tests » du `testeur` (porte 2 de S3), premier volet : vérification ticket par ticket des 19 tickets de réalisation T-010 à T-028 (environ 0,3 h chacun), dès qu'ils sont `EN_REVUE` avec l'avis `APPROUVÉ` ; le `testeur` coche les critères constatés et passe un ticket `TERMINE` quand les quatre conditions de R13 sont réunies (dont la ligne « Revue humaine » de Karim pour T-013 à T-017, T-019, T-020 et T-028). T-029 (ticket salarié) est conclu par Nadia (R13). Le second volet, le rapport de tests de la livraison, est T-042.

Pas de `depend_de` vers les tickets vérifiés : le `testeur` les fait passer `TERMINE`, une dépendance créerait un cycle. Le `testeur` passe ce ticket `EN_REVUE` en fin de campagne ; le coordinateur conclut (R13).

## Critères d'acceptation
- [ ] Chacun des tickets T-010 à T-028 a été vérifié : critères cochés seulement s'ils sont constatés, ligne de journal, statut `TERMINE` ou raison de non-passage.
- [ ] Toute régression a donné un ticket `bug`, et tout test manquant un ticket `tache` « Test manquant T-NNN ».
- [ ] Une ligne de journal par vérification ici, avec le temps.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 17:00 · agent:testeur · vérification de T-010 : build Docker, conteneur avec PostgreSQL 16 jetable, suite complète sous Python 3.14.10 (31 passés, 0 ignoré). Critères 2 à 7 cochés ; critère 1 NON CONFORME (délai de 1 s de `/health` non tenu sur base gelée) ; T-010 reste `EN_REVUE` ; ticket T-056 « Test manquant T-010 » créé ; rapport [tests-2026-11-25.md](../rapports/tests-2026-11-25.md) · 1.5 h
- 2026-11-25 22:00 · agent:testeur · campagne SHA 9c0f8a8 (T-010 critère 1, T-056) : BLOQUÉ avant tout test. La machine d'exécution n'a ni Docker/Podman (`docker: command not found`), ni Python 3.14 (3.9 système, 3.13 Homebrew), ni PostgreSQL ; impossible de construire l'image, de monter la base jetable, de faire `docker pause` / `docker stop`. Aucun critère coché, T-010 et T-056 restent EN_REVUE, aucun fichier de `app/` touché. Besoin : un poste avec Docker (ou autorisation d'installer Docker/PostgreSQL 16/Python 3.14) · 0.1 h
- 2026-11-25 22:30 · coordinateur · déblocage (BLOQUE → EN_COURS) : Docker Desktop installé par l'humain et démarré (serveur 29.9.3) ; Python 3.14 et PostgreSQL 16 fournis par conteneurs · 0 h
- 2026-11-25 12:15 · agent:testeur · campagne SHA 9c0f8a8 (reprise après blocage de 22:00) : T-010 TERMINE (7/7 critères, 44 tests verts sous Python 3.14.10, image construite avec `--build-arg`, mesures de `/health` sur base gelée 1,008 s / arrêtée 0,121 s) ; T-056 reste EN_REVUE (critère 2 coché ; critère 1 non coché, libellé « connexion déjà poolée » invérifiable avec `NullPool` : reformulation au coordinateur) ; 7 répétitions de `test_health_delai.py` stables ; aucune régression, aucun ticket `bug` créé ; conteneurs, réseau et image d'essai supprimés ; rapport [tests-2026-11-25.md](../rapports/tests-2026-11-25.md) complété (section campagne 2) · 1 h
