---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-061
titre: Contraintes sur l'e-mail et les champs vides de « utilisateur » (constat 11)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: base-de-donnees-sql (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-011, T-060]   # ex. [T-001, T-002]
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

# T-061 — Contraintes sur l'e-mail et les champs vides de « utilisateur » (constat 11)

## Description
Constat 11 (bas) du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md). Dans la migration `0001` de [T-011](T-011-modele-donnees-migrations.md), `UNIQUE (email)` est sensible à la casse, alors que l'[architecture](../architecture.md) (§ 4 et § 7) prévoit un e-mail normalisé en minuscules : `a@x.fr` et `A@X.FR` coexistent. `nom = ''`, `email = ''` et `mot_de_passe_hash = ''` sont aussi acceptés. Conséquences : comptes en double, suppression RGPD incomplète, et une empreinte vide qui provoquerait une erreur 500 à la vérification Argon2.

Filet en base par une **migration additive** (règle « étendre puis contracter », architecture § 8). La normalisation côté application relève de T-013 (connexion) et de T-016 (création de compte), où un critère a été ajouté le 2026-11-25.

## Critères d'acceptation
- [ ] Une nouvelle migration `0002` ajoute les contraintes sans modifier `0001` ni rien supprimer : e-mail en minuscules et sans espace en bordure (`CHECK (email = lower(btrim(email)))`, ou index unique sur `lower(email)` ; choix noté au journal), `CHECK (email <> '')`, `CHECK (btrim(nom) <> '')`, `CHECK (mot_de_passe_hash LIKE '$argon2id$%')`.
- [ ] Tests d'intégration sur PostgreSQL 16 réel : après `a@x.fr`, l'insertion de `A@X.FR` est refusée par la base ; un nom vide, un e-mail vide, une empreinte vide ou non Argon2id sont refusés ; une ligne valide est acceptée.
- [ ] `upgrade head` reste idempotent ; une base à la révision `0001` qui contient des lignes valides passe à `0002` sans erreur ; le démarrage tolérant de T-011 (base en avance sur l'image) reste vérifié.
- [ ] `test_aucune_migration_descendante` reste vert.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (contraintes d'intégrité additives sur le schéma, comme T-011 ; aucune authentification ni manipulation de données)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage du constat 11) · 0 h
