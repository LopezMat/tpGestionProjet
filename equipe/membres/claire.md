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
allocation: { reservation-coworking: 20, esn-interne: 5 }   # % de la capacité par projet ; total ≤ 100 ; décidée par un humain (S1-R10) ; DEC-005, DEC-009, puis DEC-024 (esn-interne 5 % en P1, 0 % à partir du 2026-12-21)
responsable: B
maj_le: 2026-11-27
---
<!-- modèle : templates/membre.md v0.1 · responsable du modèle : A -->

# Claire — Cheffe de projet, consultante fonctionnelle

## Notes
- Interlocutrice client par défaut (critère AF1) : réunions de cadrage, réponses aux questions ouvertes du CDC, recette avec le client.
- Porte les tickets `decision` côté ESN (AF2) : elle prépare et présente, la validation formelle reste humaine (R5).
- Seule salariée `expert` en `relation-client` : une deuxième personne formée réduirait la dépendance (AF10 b).
- 2026-11-27 : allocation à `esn-interne` de 5 % du 2026-11-30 au 2026-12-18 (P1), puis 0 % à partir du 2026-12-21 (P2) ([DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md), plan de formation initial). Total P1 : 25 %.

## Formations suivies / prévues
- formatrice : recette fonctionnelle de Léa pendant `reservation-coworking/T-045` (`esn-interne/T-007`) et relation client de Léa (`esn-interne/T-014`), DEC-024
- formation juridique non retenue par DEC-024 (`esn-interne/T-015`) : conseil externe au cas par cas
