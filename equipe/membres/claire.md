---
# Fiche salarié (lue par scripts/tableau.py, ne pas renommer les champs)
prenom: claire
role: Cheffe de projet, consultante fonctionnelle
niveau: expert                # debutant (350 €/j) | confirme (450 €/j) | expert (550 €/j)
cout_journalier_eur: 550      # converti en €/h sur une base de 7 h/jour
capacite_h_semaine: 35
statut: actif                 # actif | conges | depart_prevu | parti | en_integration
date_arrivee: 2019-03-04
date_depart:                  # vide si aucun départ prévu
competences:                  # niveau : debutant | confirme | expert
  - nom: relation-client
    niveau: expert
  - nom: recueil-besoin
    niveau: expert
  - nom: gestion-projet
    niveau: expert
  - nom: recette-fonctionnelle
    niveau: confirme
  - nom: rgpd
    niveau: confirme
allocation: { reservation-coworking: 10 }   # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10) ; DEC-005
responsable: B
maj_le: 2026-11-24
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Claire — Cheffe de projet, consultante fonctionnelle

## Notes
- Interlocutrice client par défaut (critère AF1) : réunions de cadrage, réponses aux questions ouvertes du CDC, recette avec le client.
- Porte les tickets `decision` côté ESN (AF2) : elle prépare et présente, la validation formelle reste humaine (R5).
- Seule salariée `expert` en `relation-client` : une deuxième personne formée réduirait la dépendance (AF10 b).

## Formations suivies / prévues
- aucune prévue pour l'instant
