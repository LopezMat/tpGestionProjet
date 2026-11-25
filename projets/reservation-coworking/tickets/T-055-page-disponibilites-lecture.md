---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-055
titre: Page de consultation des disponibilités (F-01, lecture seule)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010, T-054]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-055 — Page de consultation des disponibilités (F-01, lecture seule)

## Description
**Origine.** Changement de priorité d'Ethan du 2026-11-25 (option « Lecture seule ») : une page permet de voir les disponibilités avant que la connexion et la réservation existent. Ce ticket détache de [T-023](T-023-front-membres-reservation.md) l'affichage des disponibilités ; la réservation, l'annulation et la liste « mes réservations » restent dans T-023 (qui dépend de l'écran de connexion T-022).

Front HTML/CSS/JS sans framework ni build, servi par l'application (architecture § 2 et § 3, DEC-007), sur l'API de [T-054](T-054-api-consultation-disponibilites.md). Le code doit pouvoir être repris par T-022 et T-023 (même structure de fichiers, pas de page jetable).

## Critères d'acceptation
- [ ] Pour une date choisie (par défaut aujourd'hui), la page affiche pour chacune des 3 salles les créneaux d'une heure de 8 h-9 h à 19 h-20 h, chacun marqué « libre » ou « occupé » ; un samedi ou un dimanche, elle affiche un message « aucun créneau ce jour-là ».
- [ ] « Libre » et « occupé » se distinguent autrement que par la couleur seule (texte ou icône avec libellé).
- [ ] Changer de date recharge l'affichage sans recharger toute la page.
- [ ] Une erreur de l'API affiche un message compréhensible, sans détail technique.
- [ ] Aucun bouton « réserver » n'est affiché (la réservation viendra avec T-023).
- [ ] Affichage utilisable sur ordinateur et sur téléphone (émulation mobile), navigation au clavier.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 09:30 · agent:coordinateur · création, détachée de T-023 (priorité d'Ethan du 2026-11-25, option « Lecture seule ») · 0 h
