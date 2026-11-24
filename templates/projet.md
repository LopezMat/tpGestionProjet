---
titre: Fiche projet — <client>
statut: BROUILLON
responsable: B
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
# Champs propres au projet (lus par scripts/tableau.py, ne pas renommer)
slug: <slug-client>
client: <nom>
type_projet: vitrine        # vitrine | ecommerce | api | metier | modernisation
etat_projet: cadrage        # cadrage | en_cours | en_pause | livre | maintenance | clos
budget_eur: 0
deadline: AAAA-MM-JJ
hebergement: local          # production locale Docker (DEC-003) ; autre hébergeur = décision humaine
url_prod: http://localhost:8080   # port fixe, propre à chaque projet
agents_mobilises: []        # ex. [analyste-besoin, architecte, dev-backend]
salaries_affectes: []       # ex. [prenom1, prenom2]
---
<!-- modèle : templates/projet.md v0.2 · responsable du modèle : A -->

# Fiche projet — <client>

## Résumé
<une phrase : quoi, pour qui>

## Documents
- [demande.md](demande.md) · [cdc.md](cdc.md) · [architecture.md](architecture.md) · [planning.md](planning.md) · [TABLEAU.md](TABLEAU.md) · [retex.md](retex.md)

## Pourquoi ces agents et ces salariés
<justification de la sélection par le coordinateur>

## Historique des décisions
| Date | Décision | Fichier |
|---|---|---|
