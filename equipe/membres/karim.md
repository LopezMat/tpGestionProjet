---
# Fiche salarié (lue par scripts/tableau.py, ne pas renommer les champs)
prenom: karim
role: Lead développeur, architecte
niveau: expert                # debutant (350 €/j) | confirme (450 €/j) | expert (550 €/j)
cout_journalier_eur: 550      # converti en €/h sur une base de 7 h/jour
capacite_h_semaine: 35
statut: actif                 # actif | conges | depart_prevu | parti | en_integration
date_arrivee: 2020-09-01
date_depart:                  # vide si aucun départ prévu
competences:                  # niveau : debutant | confirme | expert
  - nom: backend-python
    niveau: expert
  - nom: base-de-donnees-sql
    niveau: expert
  - nom: architecture-logicielle
    niveau: expert
  - nom: revue-code
    niveau: expert
  - nom: securite-applicative
    niveau: confirme
allocation: { reservation-coworking: 15 }   # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10) ; DEC-009
responsable: B
maj_le: 2026-11-25
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Karim — Lead développeur, architecte

## Notes
- Revue humaine des tickets backend critiques ou liés à la sécurité (AF3) et binôme des tickets `critique` (AF5).
- Relit les choix techniques de l'`architecte` avant leur présentation à l'équipe.
- **Seul salarié** avec `securite-applicative` (confirme) : dépendance à une personne, qui justifie un ticket `formation` dès le premier projet sensible (AF10 b).
- Congés prévus du 2026-12-21 au 2026-12-31 (EV-003).

## Formations suivies / prévues
- aucune prévue pour l'instant
