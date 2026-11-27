---
titre: Fiche projet — ESN (projet interne)
statut: BROUILLON
responsable: B
version: 0.2
maj_le: 2026-11-27
valide_par:
decision:
# Champs propres au projet (lus par scripts/tableau.py, ne pas renommer)
slug: esn-interne
client: ESN (projet interne)
type_projet: interne        # vitrine | ecommerce | api | metier | modernisation | interne (projet interne de l'ESN, R19)
etat_projet: en_cours       # cadrage | en_cours | en_pause | livre | maintenance | clos
budget_eur: 4360            # budget de fonctionnement de l'ESN (DEC-024 : 3 633,21 € de temps + marge 20 %) ; frais externes hors budget, enveloppe séparée de 700 € HT suivie dans planning.md
deadline: 2027-01-15        # échéance du plan de formation initial (DEC-024)
hebergement: aucun          # projet interne : aucune application déployée (R19)
url_prod:
agents_mobilises: [chef-de-projet]
salaries_affectes: [claire, karim, lea, nadia]   # allocations à esn-interne décidées par DEC-024 (S1-R10), appliquées par le coordinateur dans equipe/ (P1 le 2026-11-27, P2 le 2026-12-21)
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
- [planning.md](planning.md) (plan de formation et registre des compétences à risque, T-001, mis à jour pour l'option B par T-016) · [TABLEAU.md](TABLEAU.md)

## Pourquoi ces agents et ces salariés
- `chef-de-projet` : il rédige le plan de formation et les tickets `formation`, et analyse les événements d'équipe (S1-R13, CLAUDE.md § 5).
- Claire, Karim, Léa et Nadia : stagiaires ou formateurs des formations T-002 à T-014 retenues par [DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B).

  | Salarié | `esn-interne` P1 (2026-11-30 → 2026-12-18) | `esn-interne` P2 (2026-12-21 → 2027-01-15) | Rôle |
  |---|---|---|---|
  | Claire | 5 % | 0 % | formatrice recette et relation client (T-007, T-014) |
  | Karim | 5 % | 10 % | formateur sécurité et revue humaine (T-005), stagiaire sauvegarde-restauration (T-008) |
  | Léa | 25 % | 10 % | stagiaire sécurité, revue humaine, recette, docker, relation client (T-003, T-004, T-006, T-010, T-013) |
  | Nadia | 10 % | 20 % | stagiaire supervision et documentation (T-002, T-012), formatrice sauvegarde et docker (T-009, T-011) |

  Les allocations de P2 sont appliquées le 2026-12-21 : `tableau.py` ne connaît qu'une valeur par projet.
- `reservation-coworking` garde la priorité : un binôme peut être suspendu sans délai pour le chemin critique du GO (DEC-024, point 6).

## Historique des décisions
| Date | Décision | Fichier |
|---|---|---|
| 2026-11-26 | Création du projet interne : imputation des coûts (R18), projet interne (R19), plan de formation (S1-R13) | [DEC-023](../../docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md) |
| 2026-11-27 | Plan de formation initial, option B : budget de fonctionnement 4 360 €, échéance 2027-01-15, allocations P1/P2, enveloppe de frais externes de 700 € HT hors budget (T-017) | [DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) |
