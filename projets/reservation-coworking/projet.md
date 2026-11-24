---
titre: Fiche projet — Espace de coworking (Perpignan)
statut: BROUILLON
responsable: B
version: 0.2
maj_le: 2026-11-24
valide_par:
decision:
# Champs propres au projet (lus par scripts/tableau.py, ne pas renommer)
slug: reservation-coworking
client: Coworking Les Arcades (Perpignan)
type_projet: metier         # vitrine | ecommerce | api | metier | modernisation
etat_projet: cadrage        # cadrage | en_cours | en_pause | livre | maintenance | clos
budget_eur: 6000
deadline: 2026-12-18
hebergement: local          # production locale Docker (DEC-003) ; autre hébergeur = décision humaine
url_prod: http://localhost:8080   # port fixe, propre à chaque projet
agents_mobilises: [analyste-besoin, architecte]
salaries_affectes: [claire]
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
- **Salariés** : Claire, interlocutrice client à 10 % (DEC-005) : seule salariée `relation-client` (AF1). Karim fera la revue humaine des tickets d'authentification (AF3, DEC-006) : son affectation sera posée au planning.
- **`architecte`** mobilisé après la validation du CDC (DEC-006) : authentification, rôles et données personnelles rendent le choix de stack structurant.
- **Point d'attention délai** : environ 18 jours ouvrés entre la demande et la deadline, avec les congés de Karim à partir du 2026-12-21 (après la deadline) et l'absence de Léa les 26 et 27 novembre.

## Historique des décisions
| Date | Décision | Fichier |
|---|---|---|
| 2026-11-24 | Claire interlocutrice client, allocation 10 % (T-002) | [DEC-005](../../docs/decisions/2026-11-24-DEC-005-interlocutrice-client-coworking.md) |
| 2026-11-24 | Réponses du client, arbitrages, CDC v1.0 validé : 5 Must, F-08 en Should (T-003) | [DEC-006](../../docs/decisions/2026-11-24-DEC-006-validation-cdc-coworking.md) |
