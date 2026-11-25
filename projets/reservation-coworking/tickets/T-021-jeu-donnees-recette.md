---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-021
titre: Jeu de données de recette (donnees_demo)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: base-de-donnees-sql (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-013]          # ex. [T-001, T-002]
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

# T-021 — Jeu de données de recette (donnees_demo)

## Description
CDC § 7 « Jeu de données de recette : 3 salles, quelques membres fictifs, un compte accueil fictif ; aucune donnée réelle de membre » ; architecture § 6 : commande de développement `python -m reservation.donnees_demo`, absente du chemin de démarrage de production. Le compte accueil de recette passe par `init_accueil` (T-017, T-044). Utilisée par les tests de bout en bout (T-026) et la recette (T-045).

## Critères d'acceptation
- [ ] `python -m reservation.donnees_demo` n'insère que des données fictives : quelques membres fictifs (noms et e-mails manifestement fictifs) et des réservations réparties de J à J+14 sur les 3 salles ; elle ne crée aucun compte accueil.
- [ ] Le mot de passe des membres fictifs est lu dans une variable d'environnement ; aucune valeur n'est écrite dans le dépôt ni affichée.
- [ ] La commande refuse de s'exécuter si la base contient déjà des réservations (pas d'écrasement) et n'est appelée par aucun chemin de démarrage de production (test).
- [ ] Son usage est documenté dans le README de l'app.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (données fictives, hors démarrage de production)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
