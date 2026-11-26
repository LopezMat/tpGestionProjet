---
# Fiche salarié (lue par scripts/tableau.py, ne pas renommer les champs)
prenom: nadia
role: Ingénieure DevOps
niveau: confirme              # debutant (350 €/j) | confirme (450 €/j) | expert (550 €/j)
cout_journalier_eur: 450      # converti en €/h sur une base de 7 h/jour
capacite_h_semaine: 28        # 4/5 de temps (pas de travail le mercredi)
statut: actif                 # actif | conges | depart_prevu | parti | en_integration
date_arrivee: 2023-05-15
date_depart:                  # vide si aucun départ prévu
competences:                  # niveau : debutant | confirme | expert
  - nom: ci-cd
    niveau: confirme
  - nom: docker
    niveau: confirme
  - nom: linux
    niveau: confirme
  - nom: sauvegarde-restauration
    niveau: confirme
  - nom: supervision
    niveau: debutant
allocation: { reservation-coworking: 50 }   # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10) ; DEC-009, DEC-019, puis DEC-020 (10 % client + 40 % imputés à l'ESN, jusqu'au 2026-12-18)
responsable: B
maj_le: 2026-11-26
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Nadia — Ingénieure DevOps

## Notes
- Revue humaine des tickets de déploiement, de sauvegarde et de rollback (AF3) ; binôme du `deployeur` sur les mises en production critiques (AF5).
- Temps partiel à 80 % (28 h/semaine), déjà pris en compte dans `capacite_h_semaine`.
- Journée de formation « supervision » prévue le 2026-12-03 (EV-002), pour passer de débutante à confirmée.
- 2026-11-26 : allocation à `reservation-coworking` portée de 20 % à 30 % **jusqu'à la mise en service**, retour à 5 % ensuite (option A de T-090, [DEC-019](../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md), décision d'Ethan prise dans l'exercice de crise SIMULATION T-080). Motif : charge à 128 % de sa capacité avec les actions correctives, et dépendance à une seule personne pour la restauration.
- 2026-11-26 : allocation portée à 50 % jusqu'au 2026-12-18 ([DEC-020](../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md), révision du budget, SIMULATION) : 10 % pour la part client et 40 % pour les tickets imputés à l'ESN (crise et outillage commun). Ces tickets restent dans `reservation-coworking` tant qu'aucun projet interne n'existe (lot2-D point 9, R11).

## Formations suivies / prévues
- supervision (2026-12-03, EV-002) : le ticket `formation` sera créé dans son premier projet alloué
