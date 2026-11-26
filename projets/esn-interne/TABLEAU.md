<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). Régénérer : python scripts/tableau.py -->

# Tableau de bord — ESN (projet interne) (`esn-interne`)

> **Fichier généré** le 2026-11-26 par `scripts/tableau.py` à partir des tickets, seule source de vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.

## Synthèse

| Indicateur | Valeur |
|---|---|
| Type · état | interne · cadrage |
| Avancement (h estimées terminées / h estimées hors ANNULE) | 0,0 % (0,0 h / 1,5 h) |
| Temps restant (Σ max(0, estimation − passé), DEC-001 § 4) | 1,5 h |
| Budget de fonctionnement consommé / prévu (projet interne, R19) | 0,00 € / non renseigné |
| Coût projeté à terminaison (consommé + reste × taux) | 22,50 € |
| Fin projetée | 2026-11-26 |
| Deadline | non renseignée |
| Écart avec la deadline | — |

## Alertes

Aucune alerte.

## Tickets par statut

| Statut | Nombre |
|---|---|
| A_FAIRE | 1 |
| EN_COURS | 0 |
| EN_REVUE | 0 |
| BLOQUE | 0 |
| ATTENTE_HUMAIN | 0 |
| TERMINE | 0 |
| ANNULE | 0 |
| **Total** | 1 |

## Tickets BLOQUE

Aucun ticket bloqué.

## En attente d'une décision humaine (ATTENTE_HUMAIN)

Aucune décision attendue.

## Tickets salariés à faire par un humain (AF11)

Aucun.

## Tickets formation ouverts

Aucun.

## Utilisation des salariés (AF9, indicateur)

Aucun salarié alloué ni assigné.

## Planning prévisionnel (Gantt)

```mermaid
gantt
    title Planning — esn-interne (calculé le 2026-11-26)
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    section agent chef-de-projet
    T-001 Plan de formation initial de l'ESN :t001, 2026-11-26, 2026-11-27
```

## Hypothèses de calcul

- Taux : agent 15,00 €/h ; salarié : coût journalier ÷ 7 (ARCHITECTURE § 8). Le budget consommé compte aussi le temps passé sur les tickets ANNULE.
- Ordonnancement à partir du 2026-11-26 : dépendances, puis priorité (critique → basse), puis id ; un ticket à la fois par assigné.
- Capacité : agent 7,0 h par jour ouvré ; salarié capacite_h_semaine ÷ 5 × allocation au projet × capacité restante du calendrier (temps partiel moyenné sur 5 jours) ; nulle avant l'arrivée et après le départ.
- Jours ouvrés : hors samedis, dimanches et jours fériés d'`equipe/calendrier.md`.
- Les tickets BLOQUE et ATTENTE_HUMAIN sont supposés débloqués aujourd'hui ; leur date de fin est donc optimiste.
- Tickets TERMINE dans le Gantt : de `cree_le` à `maj_le` (ou `debut_le` / `termine_le` s'ils existent).
- Projet interne de l'ESN (R19, DEC-023) : tous les tickets sont à la charge de l'ESN et comparés au budget de fonctionnement (`budget_eur`).

## Anomalies de données

- projet.md : budget_eur absent ou nul ; pas de contrôle budgétaire
- projet.md : deadline absente ou invalide ; pas de contrôle des délais
