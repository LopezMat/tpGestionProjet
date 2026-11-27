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
allocation: { esn-interne: 25 }   # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10) ; DEC-024 (esn-interne 25 % en P1, 10 % à partir du 2026-12-21)
responsable: B
maj_le: 2026-11-27
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Léa — Développeuse front

## Notes
- Revue humaine des tickets frontend critiques (AF3) et contrôle de l'accessibilité.
- **Absente les 2026-11-26 et 2026-11-27 (congés, EV-001)** : aucun ticket ne peut lui être affecté sur cette période (S1-R9). Fiche passée `conges` le 2026-11-26, jour du début de l'absence (skill `absence`, scénario 3, SIMULATION) ; à repasser `actif` au retour, le 2026-11-30.
- `tests-e2e` au niveau débutant, alors que les tests de bout en bout sont obligatoires en e-commerce : besoin de formation probable (AF7, AF10 c).
- 2026-11-27 : allocation à `esn-interne` de 25 % du 2026-11-30 au 2026-12-18 (P1), puis 10 % à partir du 2026-12-21 (P2) ([DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md), plan de formation initial).

## Formations suivies / prévues
- securite-applicative → débutante, autoformation (`esn-interne/T-003`), DEC-024
- revue humaine et sécurité → confirmée, binôme avec Karim : 3 revues en double (`esn-interne/T-004`), DEC-024
- recette-fonctionnelle → confirmée, binôme avec Claire pendant `reservation-coworking/T-045` (`esn-interne/T-006`), DEC-024
- docker → débutante, autoformation et binôme avec Nadia (`esn-interne/T-010`), DEC-024
- relation-client → débutante, binôme avec Claire (`esn-interne/T-013`), DEC-024
