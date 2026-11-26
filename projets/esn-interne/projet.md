---
titre: Fiche projet — ESN (projet interne)
statut: BROUILLON
responsable: B
version: 0.1
maj_le: 2026-11-26
valide_par:
decision:
# Champs propres au projet (lus par scripts/tableau.py, ne pas renommer)
slug: esn-interne
client: ESN (projet interne)
type_projet: interne        # vitrine | ecommerce | api | metier | modernisation | interne (projet interne de l'ESN, R19)
etat_projet: cadrage        # cadrage | en_cours | en_pause | livre | maintenance | clos
budget_eur: 0               # budget de fonctionnement de l'ESN : 0 jusqu'à DEC-024 (plan de formation initial), DEC-023
deadline:                   # échéance du plan de formation : fixée par DEC-024
hebergement: aucun          # projet interne : aucune application déployée (R19)
url_prod:
agents_mobilises: [chef-de-projet]
salaries_affectes: []       # allocations à esn-interne décidées par DEC-024 (S1-R10), appliquées par le coordinateur dans equipe/
---
<!-- modèle : templates/projet.md v0.3 · responsable du modèle : A -->

# Fiche projet — ESN (projet interne)

## Résumé
Le travail de l'ESN qui n'a pas de livrable client (CLAUDE.md R19, [DEC-023](../../docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md)) :
- le **plan de formation de l'ESN** : tickets `formation` et `planning.md`, qui tient le registre des compétences à risque (S1-R13) ;
- les outils et règles communs à l'ESN ;
- les tickets `decision` des événements d'équipe : arrivée, départ, absence (CLAUDE.md § 5).

Ce projet n'a ni demande, ni CDC, ni architecture, ni recette, ni GO. Le `chef-de-projet` y propose les tickets, et un humain les arbitre par un ticket `decision` `ATTENTE_HUMAIN`. Tous ses tickets sont à la charge de l'ESN (`imputation: esn`). Un travail sur l'application ou la livraison d'un client, même payé par l'ESN, reste dans le projet du client avec `imputation: esn` (R18).

## Documents
- [planning.md](planning.md) (plan de formation, à rédiger : T-001) · [TABLEAU.md](TABLEAU.md)

## Pourquoi ces agents et ces salariés
- `chef-de-projet` : il rédige le plan de formation et les tickets `formation`, et analyse les événements d'équipe (S1-R13, CLAUDE.md § 5).
- Aucun salarié n'est encore alloué. Les allocations à `esn-interne`, le budget de fonctionnement et l'échéance seront décidés par DEC-024, à partir de la proposition chiffrée de T-001.

## Historique des décisions
| Date | Décision | Fichier |
|---|---|---|
| 2026-11-26 | Création du projet interne : imputation des coûts (R18), projet interne (R19), plan de formation (S1-R13) | [DEC-023](../../docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md) |
