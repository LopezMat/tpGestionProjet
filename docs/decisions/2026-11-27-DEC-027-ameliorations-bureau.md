---
titre: esn-interne — améliorations de la page « Le bureau » (info-bulle, halos, pièce S3) confiées à dev-frontend avec une dérogation de périmètre limitée à T-025 ; son d'alerte sorti en T-026
statut: VALIDÉ
responsable: D
version: 1.0
maj_le: 2026-11-27
valide_par:     Ethan            # rempli par l'humain qui valide
decision: DEC-027           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-027
date: 2026-11-27
decide_par: Ethan
projet: esn-interne
ticket: T-025
modifie_une_regle: non      # dérogation ponctuelle (T-025 seulement) ; la règle 9 de dev-frontend, DEC-016 et DEC-018 sont inchangées
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-027 — Améliorations de la page « Le bureau »

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la demande d'Ethan du 2026-11-27 (branche `esn-interne/bureau-ameliorations`), du plan présenté le même jour et de la réponse d'Ethan, dont le *pourquoi* est repris mot pour mot. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et qui renseigne `valide_par`.
>
> **Numérotation.** Le 2026-11-27, avant l'écriture, DEC-027 était libre dans `docs/decisions/` et sur toutes les branches locales et distantes (après `git fetch --all`).

## Contexte
La page « Le bureau » ([DEC-016](2026-11-26-DEC-016-page-le-bureau.md), [DEC-017](2026-11-26-DEC-017-membres-humains-equipe.md), [DEC-018](2026-11-26-DEC-018-mode-direct-bureau.md)) montre l'ESN vue de dessus. Ethan a demandé quatre améliorations :
1. une info-bulle au survol d'un personnage ;
2. un halo pour un personnage au travail, et un halo différent pour `BLOQUE` et `ATTENTE_HUMAIN` ;
3. une pièce S3 sans personnages qui se chevauchent ;
4. un son court quand un ticket passe `BLOQUE` ou `ATTENTE_HUMAIN`.

C'est un outil interne. Son coût est donc porté par le projet interne `esn-interne` (R19), dont le budget de fonctionnement est de 4 360 €, avec un seuil d'alerte à 90 %, soit 3 924 € ([DEC-024](2026-11-27-DEC-024-plan-formation-initial.md)).

Le coordinateur a créé le ticket de travail [T-025](../../projets/esn-interne/tickets/T-025-ameliorations-page-le-bureau.md) et présenté un plan. Ce plan soulève trois questions :
- le chiffrage des quatre points, soit 9,5 h et 142,50 €, porterait le coût projeté d'`esn-interne` à 3 910,71 € (89,7 %), avec 13,29 € de marge sous le seuil ;
- en mode Direct, le journal de DEC-018 ne contient aucun statut de ticket : un passage à `BLOQUE` n'y est pas observable ;
- `agent:coordinateur` n'est pas au catalogue, et `tableau.py` ne compterait pas son coût. Or `dev-frontend`, qui a les compétences voulues (`javascript`, `accessibilite`), limite ses écritures à `projets/<slug>/app/` (règle 9 de `.claude/agents/dev-frontend.md`), alors que la page vit dans `scripts/`.

**DEC-016 et DEC-018 ne sont pas modifiées.** Les ajouts restent dans la règle d'outillage de DEC-016 : lecture seule, états tirés des tickets, aucune ressource externe. Ils restent aussi dans la liste blanche de DEC-018 : l'info-bulle n'affiche en Direct que des champs déjà journalisés.

## Options étudiées
| Question | Option | Avantages | Inconvénients |
|---|---|---|---|
| Périmètre du ticket | A. Les quatre points dans T-025 (9,5 h) | une seule livraison | projeté à 89,7 %, marge de 13,29 € (moins d'une heure) ; question ouverte sur le Direct |
| | **B. Info-bulle, halos et S3 dans T-025 ; son dans un ticket séparé, non planifié (retenue)** | marge de 39,54 € sous le seuil ; la question du son en Direct est traitée à part | deux livraisons |
| Son en mode Direct | **a. Son « attente » quand Claude Code attend un humain : `autorisation`, `attente` de type `permission_prompt` ou `elicitation_dialog`, sans `idle_prompt` (retenue)** | aucune donnée nouvelle ; DEC-018 inchangée | ne suit pas les statuts des tickets |
| | b. Le serveur Direct lit les statuts des tickets | suit vraiment les tickets | modifie DEC-018 (R11) ; coût et risque plus élevés |
| Qui réalise T-025 | **a. `agent:dev-frontend`, avec une dérogation de périmètre à `scripts/` pour T-025 seulement ; revue `relecteur-code` puis `testeur` (retenue)** | temps compté par `tableau.py` ; travail relu comme le reste (R13) | une dérogation à tracer |
| | b. Le coordinateur, comme pour DEC-016 et DEC-018 | aucune dérogation | temps non rattaché à un agent du catalogue ; pas de revue indépendante |

## Décision
1. **T-025 porte l'info-bulle, les halos et la nouvelle pièce S3**, selon le plan présenté le 2026-11-27 et décrit dans le ticket. Il est ré-estimé à **7,75 h, soit 116,25 €** (`imputation: esn`, R19). Avec T-025, le coût projeté d'`esn-interne` est de **3 884,46 € sur 4 360 € (89,1 %)**, calculé par `tableau.py` le 2026-11-27.
2. **Le son sort de T-025.** Il est porté par [T-026](../../projets/esn-interne/tickets/T-026-son-alerte-bureau.md), `A_FAIRE`, non planifié et non chiffré, qu'Ethan chiffrera plus tard. Il couvre :
   - le Replay ;
   - en Direct, l'**option a** : `autorisation`, et `attente` avec `permission_prompt` ou `elicitation_dialog`, **sans `idle_prompt`**.

   T-026 ne commence pas avant son chiffrage et un accord humain. La dérogation du point 3 ne le couvre pas.
3. **T-025 est assigné à `agent:dev-frontend`, avec une dérogation de périmètre limitée à ce ticket.** Par exception à sa règle 9, `dev-frontend` peut écrire dans `scripts/bureau.py`, `scripts/bureau.js`, `scripts/test_bureau.py`, dans la section « Le bureau » de `README.md` et dans son ticket, et dans aucun autre fichier. Toutes ses autres règles s'appliquent : jamais de push, jamais de `TERMINE`, R5, R6, R17. La revue est faite par `relecteur-code`, puis par `testeur`, qui passe le ticket `TERMINE` aux conditions de R13. La règle 9 n'est pas modifiée.
4. **Arrêt obligatoire.** Le coordinateur s'arrête et pose la question à Ethan avant de continuer dans deux cas :
   - le temps passé sur T-025 dépasse son estimation de 7,75 h ;
   - le coût projeté d'`esn-interne` atteint 90 % du budget de fonctionnement (3 924 €).
5. **Aucune PR n'est ouverte avant la validation de cette décision.**

## Pourquoi
*(Ethan, 2026-11-27)*

« On améliore le bureau parce que c'est l'outil qui rend le système lisible pour l'équipe : voir qui fait quoi au survol, voir qui est bloqué, et ne plus avoir de personnages empilés dans S3. On sort le son parce qu'il ajoutait 1,5 h et une question sur le mode Direct, alors qu'avec lui la marge sous le seuil de 90 % aurait été inférieure à une heure, trop faible après les dépassements constatés cette semaine. On confie le ticket à dev-frontend avec une dérogation limitée à ce ticket plutôt qu'au coordinateur, pour que son temps soit compté et que son travail soit relu comme le reste. »

## Impacts
- **Fichiers** :
  - créés : ce fichier, `projets/esn-interne/tickets/T-025-ameliorations-page-le-bureau.md`, `projets/esn-interne/tickets/T-026-son-alerte-bureau.md` ;
  - modifiés : `docs/decisions/README.md` (index) ; `projets/esn-interne/TABLEAU.md` et `PORTFOLIO.md`, régénérés par `tableau.py` (R9) ;
  - prévus par T-025 après validation : `scripts/bureau.py`, `scripts/bureau.js`, `scripts/test_bureau.py`, `README.md` ;
  - non modifiés : DEC-016, DEC-018, `.claude/agents/dev-frontend.md`, `CLAUDE.md`, `console.py`, `bureau_direct.py`, `journal_direct.py`, `.claude/settings*.json`.
- **Règles** : aucune modification. La dérogation vaut pour T-025 seulement et n'entre pas dans `docs/CHANGELOG-REGLES.md`.
- **Budget d'`esn-interne`** :
  - consommé : 131,25 € (3,0 %) ;
  - projeté : 3 884,46 € (89,1 %) ;
  - marge sous le seuil : 39,54 €, soit environ 2,6 h d'agent.

  Une fois chiffré, T-026 s'ajoutera au projeté. Au-delà de 2,6 h, il franchirait le seuil, sauf si un autre poste baisse.
- **Tickets** :
  - T-025 (`A_FAIRE`) démarre après la validation de cette décision et la mise à jour de son champ `decision` par l'humain ;
  - T-026 (`A_FAIRE`) attend son chiffrage.
