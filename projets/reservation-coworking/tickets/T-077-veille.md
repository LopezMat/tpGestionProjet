---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-077
titre: Veille
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:veilleur     # agent:<nom> | salarie:<prenom>
competence_requise: veille-technologique (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 2.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-077 — Veille

## Description
Ticket de travail du `veilleur` sur le projet (S2, S2-R6 ; règle 9 de [veilleur.md](../../../.claude/agents/veilleur.md)). Il porte le temps de la veille technologique et CVE ciblée sur la stack du projet : Python 3.14, FastAPI, Uvicorn, Starlette, Pydantic, SQLAlchemy, Alembic, psycopg, argon2-cffi, tzdata, images `python:3.14-slim` et `postgres:16-alpine` ([architecture.md](../architecture.md) § 2 et § 6, ligne « § 9 Veille » ; [cdc.md](../cdc.md) § 9), avec les versions installées lues dans `app/requirements.txt` et `app/requirements-dev.txt`.

Il reste ouvert pendant la vie du projet ; chaque passage du `veilleur` ajoute une ligne de journal et met à jour `temps_passe_h`. Première veille demandée par l'humain le 2026-11-26 (semaine 2026-S48), alors que le développement est en pause : l'application n'est pas en production (aucun rapport de déploiement `EN LIGNE ET À JOUR`).

## Critères d'acceptation
- [ ] Chaque passage produit ou complète `veille/AAAA-Sxx.md` conforme à `templates/rapport-veille.md`, en `EN_REVUE`.
- [ ] Chaque constat qui demande une action a une proposition de ticket, créé en `A_FAIRE` après dédoublonnage.
- [ ] Chaque passage a une ligne de journal et `temps_passe_h` à jour.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 15:00 · agent:coordinateur · création (ticket de travail du veilleur, première veille demandée par l'humain) · 0 h
- 2026-11-26 16:00 · agent:veilleur · veille 2026-S48 : `veille/2026-S48.md` (14 constats, 2 propositions P-1 PostgreSQL 16.16 et P-2 verrou des dépendances, aucun ticket créé sur consigne de l'humain, transmis au chef-de-projet) · 2.5 h
- 2026-11-26 17:00 · agent:coordinateur · tickets T-078 (P-1) et T-079 (P-2) créés par le chef-de-projet et reportés dans `veille/2026-S48.md` v0.2 ; rapport lu par l'humain, en `EN_REVUE` : ticket passé `EN_REVUE` (livrable en attente de validation humaine). Pas de `TERMINE` : le ticket porte aussi les passages suivants et ses critères ne sont pas tous cochés (R13) · 0 h
