---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-060
titre: Garde-fou de la fixture destructrice des tests de migration (constat 13)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: tests-unitaires (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-011]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-060 — Garde-fou de la fixture destructrice des tests de migration (constat 13)

## Description
Constat 13 (bas) du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), qui rejoint la remarque 6 du `relecteur-code` sur [T-011](T-011-modele-donnees-migrations.md). Dans `app/tests/test_migrations.py` (lignes 21 à 36, fixture `base` et `_vider`), `DROP SCHEMA public CASCADE` est exécuté sur la base de `TEST_DATABASE_URL` au début et à la fin de chaque test, sans aucun contrôle. Une variable mal renseignée (par exemple vers la base `app` du conteneur d'aperçu ou de la production locale) effacerait toutes les réservations et tous les comptes.

À faire après le passage `TERMINE` de T-011 (le `testeur` y travaille), et avant T-061, qui ajoute des tests de migration sur cette même fixture.

## Critères d'acceptation
- [ ] Avant toute connexion, la fixture refuse de s'exécuter (échec explicite, sans aucune requête envoyée) si le nom de la base de `TEST_DATABASE_URL` ne contient pas `test` ; la base `app` du modèle commun est donc toujours refusée.
- [ ] Un test vérifie ce refus avec une URL qui désigne une base `app` sur un hôte injoignable (aucune base nécessaire), et vérifie qu'aucune instruction n'a été exécutée.
- [ ] Le README de `app/` indique comment nommer la base de test (`…_test`) ; la suite complète est verte sur un PostgreSQL 16 jetable avec une base ainsi nommée.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (code de test, aucune donnée réelle ; le risque couvert est une erreur de manipulation)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage du constat 13 et de la remarque 6 de T-011) · 0 h
