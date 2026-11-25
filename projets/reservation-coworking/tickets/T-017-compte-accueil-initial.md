---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-017
titre: Compte accueil initial (init_accueil) et commande forcer_changement (F-07)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-015]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-017 — Compte accueil initial (init_accueil) et commande forcer_changement (F-07)

## Description
Commandes `python -m reservation.init_accueil` (Q-14, DEC-006 ; décision 11 de l'architecture, DEC-007 point B) et `python -m reservation.forcer_changement` (crise « fuite », architecture § 6), plus l'avertissement au démarrage tant qu'aucun compte accueil n'existe. Le code ne fait qu'écrire la commande : son exécution en production est faite **par un humain** selon la procédure de l'architecture § 7 (ticket T-048) ; pour la recette, par T-044.

**Touche la sécurité** (secret d'initialisation) : revue humaine obligatoire, ticket compagnon **T-034** (Karim).

## Critères d'acceptation
- [ ] **Compte accueil initial** : un seul compte accueil est créé par la commande ; son mot de passe initial est lu dans `ACCUEIL_MOT_DE_PASSE_INITIAL` (et l'e-mail dans `ACCUEIL_EMAIL`) ; il n'apparaît dans aucun fichier du dépôt, aucun journal ni aucune réponse d'API (test qui capture la sortie avec des valeurs de test, contrôle du dépôt).
- [ ] La commande ne crée pas de second compte et n'échoue pas à tort si elle est relancée alors qu'un compte accueil existe : pas de doublon, mot de passe non écrasé, code 0 et message explicite (test).
- [ ] Sans ces variables, aucun compte accueil n'est créé, un message le signale et le code de sortie est non nul (test).
- [ ] Au démarrage, l'app journalise un avertissement tant qu'aucun compte accueil n'existe.
- [ ] **Changement obligatoire à la première connexion** du compte accueil initial : toute autre page ou appel d'API est refusé tant que ce n'est pas fait ; le mot de passe initial cesse alors de fonctionner (test).
- [ ] `forcer_changement --tous` (et sa forme ciblée sur un compte) met `doit_changer_mdp` à vrai et révoque les sessions concernées (test).
- [ ] La procédure d'initialisation de l'architecture § 7 est reprise dans le README de l'app, sans aucune valeur.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (secret d'initialisation, authentification, S3-R2 ; ticket compagnon T-034)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
