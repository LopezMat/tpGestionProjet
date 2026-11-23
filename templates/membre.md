---
# Fiche salarié (lue par scripts/tableau.py, ne pas renommer les champs)
prenom: <prenom>
role: <rôle>
niveau: confirme              # debutant (350 €/j) | confirme (450 €/j) | expert (550 €/j)
cout_journalier_eur: 450      # converti en €/h sur une base de 7 h/jour
capacite_h_semaine: 35
statut: actif                 # actif | conges | depart_prevu | parti | en_integration
date_arrivee: AAAA-MM-JJ
date_depart:                  # vide si aucun départ prévu
competences:                  # niveau : debutant | confirme | expert
  - nom: <compétence>
    niveau: confirme
allocation:                   # % de la capacité par projet ; total ≤ 100
  <slug-projet>: 100
responsable: B
maj_le: AAAA-MM-JJ
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# <Prénom> — <rôle>

## Notes
<préférences, contraintes, historique d'intégration ou de passation>

## Formations suivies / prévues
- T-… <formation>
