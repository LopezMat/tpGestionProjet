---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-024
titre: Front accueil (vue du jour, gestion des comptes) (F-03, F-07)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-022]          # ex. [T-001, T-002]
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

# T-024 — Front accueil (vue du jour, gestion des comptes) (F-03, F-07)

## Description
Écrans du rôle accueil : vue des réservations du jour (F-03) avec annulation (F-02), et gestion des comptes (F-07), sur l'API de T-016 et T-019 (architecture § 3). Le contrôle du rôle reste côté serveur ; l'écran se contente de ne pas proposer ces fonctions à un membre.

## Critères d'acceptation
- [ ] Un utilisateur accueil voit la liste des réservations du jour des 3 salles, triée par heure, avec salle, créneau, nom du membre et e-mail ; un jour sans réservation affiche « aucune réservation » ; la liste reflète les créations et annulations au rafraîchissement de la page.
- [ ] L'accueil annule une réservation depuis cette vue, après confirmation.
- [ ] L'accueil liste les comptes et crée un compte membre ou accueil ; un mot de passe initial de 12 caractères au moins est proposé par génération ; un e-mail déjà utilisé affiche le message de l'API.
- [ ] L'accueil supprime un compte membre après une confirmation explicite qui rappelle que l'action est irréversible ; aucune suppression n'est proposée pour un compte accueil.
- [ ] L'accueil réinitialise le mot de passe d'un compte : un mot de passe temporaire est généré et affiché une seule fois.
- [ ] Les écrans accueil ne sont pas proposés à un membre ; données insérées avec `textContent` ; accessibilité de base (labels, clavier, focus).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (interface ; les contrôles d'accès sont côté serveur, revus avec T-016, T-019 et T-020)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
