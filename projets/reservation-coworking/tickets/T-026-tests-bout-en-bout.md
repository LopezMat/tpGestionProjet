---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-026
titre: Tests de bout en bout Playwright (parcours 1, 5, 7)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: tests-e2e (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-019, T-021, T-023, T-024]   # ex. [T-001, T-002]
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

# T-026 — Tests de bout en bout Playwright (parcours 1, 5, 7)

## Description
CDC § 7 « au moins un test de bout en bout sur les parcours 1, 5 et 7 » ; architecture § 6 et décision 17 : Playwright pour Python sur l'image construite, viewport ordinateur et mobile.

**Affectation.** Le `testeur` a la compétence `tests-e2e` mais n'écrit rien dans `app/` (sa règle 1, S3-R1). Le test est donc écrit par un développeur : `dev-backend`, parce que la suite est en Python (pytest + Playwright Python). Ni `dev-backend` ni `dev-frontend` n'ont `tests-e2e` dans `equipe/agents.md` : écart signalé pour le retour d'expérience (amélioration d'agent possible). Le `testeur` vérifie et coche les critères.

## Critères d'acceptation
- [ ] Parcours 1 automatisé : un membre se connecte, consulte les disponibilités, réserve un créneau libre et le voit « occupé ».
- [ ] Parcours 5 automatisé : un membre annule avant le début du créneau (accepté) et au début du créneau (refusé), avec une horloge de test activée uniquement dans l'environnement de test (jamais dans l'image de production).
- [ ] Parcours 7 automatisé : l'accueil voit les réservations du jour, y compris après une annulation, et annule la réservation d'un membre.
- [ ] Les trois parcours passent en viewport ordinateur et en viewport mobile (émulation).
- [ ] Playwright reste dans `requirements-dev.txt` et n'est pas dans l'image de production ; la commande de lancement est documentée dans le README de l'app ; la suite est verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
