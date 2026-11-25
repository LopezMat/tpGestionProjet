---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-048
titre: Mise en service (compte accueil initial, tâche planifiée de sauvegarde)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-047]          # ex. [T-001, T-002]
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

# T-048 — Mise en service (compte accueil initial, tâche planifiée de sauvegarde)

## Description
Deux actions de l'humain d'exploitation, juste après le déploiement vérifié (T-047) :
1. **Compte accueil initial** (F-07, Q-14 ; DEC-007 point B) : `init_accueil` lancé **une fois** selon la procédure pas à pas de l'[architecture](../architecture.md) § 7, dans un terminal ordinaire dédié, **hors de toute session Claude Code** ; mot de passe initial généré, jamais écrit ; contrôles de non-fuite ; puis première connexion et changement obligatoire du mot de passe. Le compte est ensuite remis à l'accueil du client (via Claire).
2. **Tâche planifiée Windows** de sauvegarde quotidienne (20 h 30) selon l'architecture § 8, documentée par T-029, et premier contrôle.

Nadia (`docker` et `sauvegarde-restauration` confirmés) est l'humain d'exploitation. **Ticket salarié (AF11, R15)** : à faire par un humain ; aucun agent ne lance `init_accueil` ni ne voit le mot de passe. **Affectation conditionnelle** à l'allocation de Nadia proposée dans T-007.

## Critères d'acceptation
- [ ] `init_accueil` a rendu le code 0 et « compte accueil créé », sans l'e-mail ni le mot de passe dans la sortie.
- [ ] Les contrôles de non-fuite de l'architecture § 7 (étape 3) sont faits : variable effacée, historique sans valeur, `docker inspect` et `docker exec … env` sans `ACCUEIL`, journaux de l'app sans e-mail ni mot de passe.
- [ ] À la première connexion, l'écran de changement obligatoire s'affiche ; après le changement, le mot de passe initial est refusé.
- [ ] La tâche « ESN reservation-coworking - sauvegarde quotidienne » existe ; une exécution manuelle rend `LastTaskResult` à 0 et produit un fichier dans `sauvegardes-quotidiennes/`.
- [ ] Le rapport de déploiement (ou le README de l'app) indique que l'initialisation et la tâche ont été faites, par qui et quand, sans aucune valeur.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (exploitation)
- **Commentaires** :
- **Revue humaine requise** : non (action humaine)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création ; affectation conditionnelle à l'allocation de Nadia proposée dans T-007 · 0 h
