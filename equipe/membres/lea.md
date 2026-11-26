---
# Fiche salarié (lue par scripts/tableau.py, ne pas renommer les champs)
prenom: lea
role: Développeuse front
niveau: confirme              # debutant (350 €/j) | confirme (450 €/j) | expert (550 €/j)
cout_journalier_eur: 450      # converti en €/h sur une base de 7 h/jour
capacite_h_semaine: 35
statut: conges                # actif | conges | depart_prevu | parti | en_integration
date_arrivee: 2022-01-10
date_depart:                  # vide si aucun départ prévu
competences:                  # niveau : debutant | confirme | expert
  - nom: html-css
    niveau: expert
  - nom: javascript
    niveau: confirme
  - nom: react
    niveau: confirme
  - nom: accessibilite
    niveau: confirme
  - nom: tests-e2e
    niveau: debutant
allocation: {}                # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10)
responsable: B
maj_le: 2026-11-26
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Léa — Développeuse front

## Notes
- Revue humaine des tickets frontend critiques (AF3) et contrôle de l'accessibilité.
- **Absente les 2026-11-26 et 2026-11-27 (congés, EV-001)** : aucun ticket ne peut lui être affecté sur cette période (S1-R9). Fiche passée `conges` le 2026-11-26, jour du début de l'absence (skill `absence`, scénario 3, SIMULATION) ; à repasser `actif` au retour, le 2026-11-30.
- `tests-e2e` au niveau débutant, alors que les tests de bout en bout sont obligatoires en e-commerce : besoin de formation probable (AF7, AF10 c).

## Formations suivies / prévues
- aucune prévue pour l'instant
