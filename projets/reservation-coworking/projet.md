---
titre: Fiche projet — Coworking Les Arcades (Perpignan)
statut: BROUILLON
responsable: B
version: 0.7
maj_le: 2026-11-27
valide_par:
decision:
# Champs propres au projet (lus par scripts/tableau.py, ne pas renommer)
slug: reservation-coworking
client: Coworking Les Arcades (Perpignan)
type_projet: metier         # vitrine | ecommerce | api | metier | modernisation
etat_projet: en_cours       # cadrage | en_cours | en_pause | livre | maintenance | clos
budget_eur: 4200           # SIMULATION, DEC-020 (6 000 € selon DEC-009) ; comparé au seul coût client, la part ESN est séparée par le tableau (R18, DEC-023)
deadline: 2026-12-18
hebergement: local          # production locale Docker (DEC-003) ; autre hébergeur = décision humaine
url_prod: http://localhost:8080   # port fixe, propre à chaque projet
agents_mobilises: [analyste-besoin, architecte, chef-de-projet, dev-backend, dev-frontend, relecteur-code, testeur, securite, deployeur]
salaries_affectes: [claire, karim, nadia]
---
<!-- modèle : templates/projet.md v0.2 · responsable du modèle : A -->

# Fiche projet — Coworking Les Arcades (Perpignan)

## Résumé
Application web de réservation des 3 salles de réunion de Coworking Les Arcades (Perpignan, client fictif pour la démonstration ; interlocutrice côté client : Marie Lenoir, gérante), par créneau d'une heure, pour ses membres, avec une vue des réservations du jour pour l'accueil.

## Documents
- [demande.md](demande.md) · [cdc.md](cdc.md) · [architecture.md](architecture.md) · [planning.md](planning.md) · [TABLEAU.md](TABLEAU.md) · [retex.md](retex.md)

## Pourquoi ces agents et ces salariés
- **Type `metier`** : il s'agit d'une petite application de gestion (réservations, disponibilités, annulations, vue de l'accueil), avec une logique métier (conflits de créneaux) et des données personnelles. Ce n'est ni un site vitrine (il y a des données et des règles), ni une API seule (il y a des écrans pour les membres et l'accueil), ni un e-commerce (aucun paiement n'est mentionné). À confirmer par l'analyste si un paiement s'avère attendu.
- **`analyste-besoin`** mobilisé seul pour l'instant (étape 2) : la demande laisse de nombreuses questions ouvertes (accès des membres, règles d'annulation, horaires).
- **Prévus ensuite** (grille S4, à confirmer après le CDC) : `architecte` (stack et hébergement local, DEC-003), `chef-de-projet`, `dev-backend` et `dev-frontend`, puis `relecteur-code`, `testeur`, `securite` (données personnelles et authentification) et `deployeur`.
- **Salariés** (allocations de DEC-009, en attente de validation) : Claire 20 %, interlocutrice client, recette et GO (AF1 ; 10 % selon DEC-005 jusqu'à la validation de DEC-009) ; Karim 20 % (15 % selon DEC-009, +5 % pour les revues imputées à l'ESN, DEC-020), revues humaines des tickets d'authentification et de sécurité (AF3) ; Nadia 50 % jusqu'au 2026-12-18 (20 % selon DEC-009, 30 % selon DEC-019, puis DEC-020 : 10 % pour la part client et 40 % pour la part imputée à l'ESN), sauvegarde, environnement de recette et mise en service. Hugo n'est pas affecté (0 %) : le lot R17 sort du projet client (DEC-009, D1).
- **`architecte`** mobilisé après la validation du CDC (DEC-006) : authentification, rôles et données personnelles rendent le choix de stack structurant.
- **Point d'attention délai** : environ 18 jours ouvrés entre la demande et la deadline, avec les congés de Karim à partir du 2026-12-21 (après la deadline) et l'absence de Léa les 26 et 27 novembre.

## Historique des décisions
| Date | Décision | Fichier |
|---|---|---|
| 2026-11-24 | Claire interlocutrice client, allocation 10 % (T-002) | [DEC-005](../../docs/decisions/2026-11-24-DEC-005-interlocutrice-client-coworking.md) |
| 2026-11-24 | Réponses du client, arbitrages, CDC v1.0 validé : 5 Must, F-08 en Should (T-003) | [DEC-006](../../docs/decisions/2026-11-24-DEC-006-validation-cdc-coworking.md) |
| 2026-11-24 | Choix techniques : stack A1, compte accueil initial, sauvegarde quotidienne, limite de démonstration (T-005) | [DEC-007](../../docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md) |
| 2026-11-24 | Architecture v1.1 revalidée : purge à 30 jours au déploiement, fin de démonstration (T-004) | [DEC-008](../../docs/decisions/2026-11-24-DEC-008-architecture-coherente-coworking.md) |
| 2026-11-26 | SIMULATION, crise T-080 : reconstruction sans sauvegarde, communication au client, recommandation CNIL laissée au client, T-029 critique et dépendance du GO, Nadia à 30 % (EN_REVUE) | [DEC-019](../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md) |
| 2026-11-26 | SIMULATION, révision du budget : 6 000 → 4 200 € HT, F-06 abandonné, F-08 gardé, crise et outillage commun imputés à l'ESN, alerte à 90 % et arbitrage avant tout dépassement (T-093, EN_REVUE) | [DEC-020](../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md) |
