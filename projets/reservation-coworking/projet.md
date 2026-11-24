---
titre: Fiche projet — Espace de coworking (Perpignan)
statut: BROUILLON
responsable: B
version: 0.1
maj_le: 2026-11-24
valide_par:
decision:
# Champs propres au projet (lus par scripts/tableau.py, ne pas renommer)
slug: reservation-coworking
client: Espace de coworking (Perpignan)
type_projet: metier         # vitrine | ecommerce | api | metier | modernisation
etat_projet: cadrage        # cadrage | en_cours | en_pause | livre | maintenance | clos
budget_eur: 6000
deadline: 2026-12-18
hebergement: local          # production locale Docker (DEC-003) ; autre hébergeur = décision humaine
url_prod: http://localhost:8080   # port fixe, propre à chaque projet
agents_mobilises: [analyste-besoin]
salaries_affectes: []
---
<!-- modèle : templates/projet.md v0.2 · responsable du modèle : A -->

# Fiche projet — Espace de coworking (Perpignan)

## Résumé
Application web de réservation des 3 salles de réunion d'un espace de coworking de Perpignan, par créneau d'une heure, pour ses membres, avec une vue des réservations du jour pour l'accueil.

## Documents
- [demande.md](demande.md) · [cdc.md](cdc.md) · [architecture.md](architecture.md) · [planning.md](planning.md) · [TABLEAU.md](TABLEAU.md) · [retex.md](retex.md)

## Pourquoi ces agents et ces salariés
- **Type `metier`** : il s'agit d'une petite application de gestion (réservations, disponibilités, annulations, vue de l'accueil), avec une logique métier (conflits de créneaux) et des données personnelles. Ce n'est ni un site vitrine (il y a des données et des règles), ni une API seule (il y a des écrans pour les membres et l'accueil), ni un e-commerce (aucun paiement n'est mentionné). À confirmer par l'analyste si un paiement s'avère attendu.
- **`analyste-besoin`** mobilisé seul pour l'instant (étape 2) : la demande laisse de nombreuses questions ouvertes (accès des membres, règles d'annulation, horaires).
- **Prévus ensuite** (grille S4, à confirmer après le CDC) : `architecte` (stack et hébergement local, DEC-003), `chef-de-projet`, `dev-backend` et `dev-frontend`, puis `relecteur-code`, `testeur`, `securite` (données personnelles et authentification) et `deployeur`.
- **Salariés** : aucun affecté tant que T-002 (interlocuteur client et allocation initiale) n'est pas tranché par un humain.
- **Point d'attention délai** : environ 18 jours ouvrés entre la demande et la deadline, avec les congés de Karim à partir du 2026-12-21 (après la deadline) et l'absence de Léa les 26 et 27 novembre.

## Historique des décisions
| Date | Décision | Fichier |
|---|---|---|
