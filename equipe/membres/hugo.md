---
# Fiche salarié (lue par scripts/tableau.py, ne pas renommer les champs)
prenom: hugo
role: Développeur junior
niveau: debutant              # debutant (350 €/j) | confirme (450 €/j) | expert (550 €/j)
cout_journalier_eur: 350      # converti en €/h sur une base de 7 h/jour
capacite_h_semaine: 35
statut: depart_prevu          # actif | conges | depart_prevu | parti | en_integration
date_arrivee: 2026-09-01
date_depart: 2026-12-04       # SIMULATION (scénario 3, EV-004) ; vide si aucun départ prévu
competences:                  # niveau : debutant | confirme | expert
  - nom: backend-python
    niveau: debutant
  - nom: javascript
    niveau: debutant
  - nom: tests-unitaires
    niveau: debutant
  - nom: documentation
    niveau: confirme
allocation: {}                # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10)
responsable: B
maj_le: 2026-11-26
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Hugo — Développeur junior

## Notes
- Arrivé en septembre 2026, intégration terminée.
- Tickets `basse` ou `normale` à son niveau ; au-dessus, uniquement en binôme avec un expert (Karim), ce qui crée un ticket `formation` (AF7, AF10 c). Jamais de ticket `critique`.
- Point fort : documentation (confirmé), utile pour les tickets de transfert lors d'un départ.
- **SIMULATION (scénario 3)** : départ annoncé le 2026-11-26 pour le **2026-12-04** (EV-004), préavis de 6 jours ouvrés (du 2026-11-27 au 2026-12-04 inclus). Skill `depart-membre` : plan de passation en attente de décision humaine. Aucun motif n'est enregistré.

## Formations suivies / prévues
- aucune prévue pour l'instant
