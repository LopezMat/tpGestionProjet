---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-011
titre: Modèle de données et migrations
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: base-de-donnees-sql (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-011 — Modèle de données et migrations

## Description
Schéma PostgreSQL 16 de [architecture.md](../architecture.md) § 4, créé uniquement par migrations Alembic, et démarrage tolérant du § 8 (compatibilité avec le rollback, règle « étendre puis contracter »). Base de F-01 à F-08 ; insertion des 3 salles (H-20, F-06).

## Critères d'acceptation
- [ ] Une migration Alembic crée les tables `utilisateur`, `salle`, `reservation` et `session` avec les colonnes du § 4 et les contraintes : `UNIQUE (email)`, `CHECK role IN ('membre', 'accueil')`, `UNIQUE (salle_id, date_creneau, heure_debut)`, `CHECK heure_debut BETWEEN 8 AND 19`, `CHECK EXTRACT(ISODOW FROM date_creneau) <= 5`, `ON DELETE CASCADE` de `reservation` et `session` vers `utilisateur`, index `(utilisateur_id, date_creneau)` et `(date_creneau)` (test d'intégration sur le schéma).
- [ ] Les 3 salles « Salle 1 », « Salle 2 » et « Salle 3 » sont insérées par migration (H-20).
- [ ] Au démarrage, `reservation.demarrer` lance `alembic upgrade head` si la révision de la base est connue de l'image ; si la base est à une révision plus récente, il journalise un avertissement et démarre sans migrer (test).
- [ ] Les migrations sont uniquement additives ; aucune migration descendante n'est lancée automatiquement.
- [ ] Les tests d'intégration tournent sur un PostgreSQL 16 réel (conteneur jetable), jamais sur SQLite.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
