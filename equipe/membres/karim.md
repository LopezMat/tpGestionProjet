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
allocation: { reservation-coworking: 20, esn-interne: 5 }   # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10) ; DEC-009, DEC-020 (+5 % pour les revues imputées à l'ESN), puis DEC-024 (esn-interne 5 % en P1, 10 % à partir du 2026-12-21)
responsable: B
maj_le: 2026-11-27
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Karim — Lead développeur, architecte

## Notes
- Revue humaine des tickets backend critiques ou liés à la sécurité (AF3) et binôme des tickets `critique` (AF5).
- Relit les choix techniques de l'`architecte` avant leur présentation à l'équipe.
- **Seul salarié** avec `securite-applicative` (confirme) : dépendance à une personne, qui justifie un ticket `formation` dès le premier projet sensible (AF10 b).
- Congés prévus du 2026-12-21 au 2026-12-31 (EV-003).
- 2026-11-26 : allocation portée de 15 % à 20 % ([DEC-020](../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md), révision du budget, SIMULATION) : +5 % pour les revues humaines des tickets imputés à l'ESN (crise et outillage commun).
- 2026-11-27 : allocation à `esn-interne` de 5 % du 2026-11-30 au 2026-12-18 (P1), puis 10 % à partir du 2026-12-21 (P2, hors congés) ([DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md), plan de formation initial). Total P1 : 25 %.

## Formations suivies / prévues
- formateur : sécurité applicative et revue humaine de Léa, second relecteur (`esn-interne/T-005`, pour T-003 et T-004), DEC-024
- sauvegarde-restauration → confirmé, binôme avec Nadia (`esn-interne/T-008`), DEC-024
