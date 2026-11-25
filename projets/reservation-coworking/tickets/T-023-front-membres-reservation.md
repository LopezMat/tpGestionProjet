---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-023
titre: Front membres (disponibilités, réservation, annulation) (F-01, F-02)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-022, T-055]   # ex. [T-001, T-002]
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

# T-023 — Front membres (disponibilités, réservation, annulation) (F-01, F-02)

## Description
Écrans membres de F-01 (consulter les disponibilités et réserver) et F-02 (annuler), sur l'API de T-018 et T-019 (architecture § 3). Les règles sont appliquées par le serveur ; l'écran affiche ses messages. Parcours 1, 3, 4 et 5 du CDC § 7 côté interface.

## Critères d'acceptation
- *(Affichage des disponibilités déplacé dans [T-055](T-055-page-disponibilites-lecture.md) le 2026-11-25 ; T-023 le reprend et y ajoute la réservation.)*
- [ ] Un membre réserve un créneau libre ; un refus (créneau indisponible, limite de 2 par jour, au-delà de 14 jours, créneau commencé) affiche le message explicite renvoyé par l'API.
- [ ] Après la réservation, le créneau apparaît « occupé » sans rechargement manuel de la page.
- [ ] Le membre voit la liste de ses réservations à venir et en annule une après confirmation ; un refus (créneau commencé) affiche le message de l'API ; après annulation, le créneau redevient « libre ».
- [ ] Affichage utilisable sur ordinateur et sur téléphone (émulation mobile), navigation au clavier.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 09:30 · agent:coordinateur · affichage des disponibilités détaché dans T-055 (priorité d'Ethan du 2026-11-25, option « Lecture seule ») ; dépend aussi de T-055 ; estimation ramenée de 7 à 5,5 h · 0 h
