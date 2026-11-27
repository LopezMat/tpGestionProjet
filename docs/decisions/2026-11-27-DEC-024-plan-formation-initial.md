---
titre: Plan de formation initial de l'ESN — option B, budget de fonctionnement, échéance, allocations à esn-interne et enveloppe de frais externes
statut: EN_REVUE
responsable: B
version: 0.1
maj_le: 2026-11-27
valide_par:                 # rempli par l'humain qui valide
decision: DEC-024           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-024
date: 2026-11-27
decide_par: Ethan
projet: esn-interne
ticket: T-017
modifie_une_regle: non
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-024 — Plan de formation initial de l'ESN

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier le 2026-11-27 à partir de la décision d'Ethan sur [T-017](../../projets/esn-interne/tickets/T-017-decision-plan-formation-initial.md) (option B, frais externes dans une enveloppe séparée) et de son « Pourquoi », reproduit mot pour mot. Conformément à R5, c'est un membre de l'équipe qui passe lui-même ce fichier à `VALIDÉ` et renseigne `valide_par` (skill `tracer-decision`).
>
> **Numérotation.** Le 2026-11-27, DEC-024 n'était utilisé par aucun fichier de `docs/decisions/` ; il était réservé à cette décision par DEC-023 (point 6).

## Contexte
- [DEC-023](2026-11-26-DEC-023-imputation-esn-plan-formation.md) a créé le projet interne `projets/esn-interne/` (R19), avec `budget_eur: 0` et une échéance vide jusqu'à cette décision. Il y a placé le ticket de travail T-001 « Plan de formation initial ».
- Le `chef-de-projet` a réalisé T-001 le 2026-11-27 :
  - [planning.md](../../projets/esn-interne/planning.md) v0.1 (`EN_REVUE`), avec le registre des compétences à risque R-01 à R-17 ;
  - les tickets `formation` T-002 à T-015 (dont les tickets d'encadrement T-005, T-007, T-009, T-011, T-014) et le ticket de pilotage T-016 ;
  - le ticket `decision` T-017, avec quatre options chiffrées.
- Risques à l'origine du plan (DEC-009 E, DEC-019, DEC-021, EV-002, EV-004) :
  - Karim est le seul relecteur `securite-applicative` et le seul à faire la revue humaine ; il est en congés du 21 au 31/12 (EV-003) ;
  - Nadia est la seule sur `sauvegarde-restauration` et `docker` ;
  - `documentation` n'a plus de titulaire après le départ de Hugo le 2026-12-04 ;
  - Claire est la seule sur `recette-fonctionnelle` et `relation-client` ; `juridique` est absente ;
  - la formation « supervision » de Nadia du 2026-12-03 (EV-002) n'avait pas de ticket.

Les coûts sont en heures équivalent humain × taux (R12), calculés comme `tableau.py` : Claire et Karim 78,57 €/h, Léa et Nadia 64,29 €/h, agent 15 €/h. P1 va du 2026-11-30 au 2026-12-18, P2 du 2026-12-21 au 2027-01-15.

## Options étudiées
| Option | Contenu | Coût temps | `budget_eur` (marge 20 %) | Échéance | Avantages | Inconvénients |
|---|---|---|---|---|---|---|
| A · Plan complet | T-002 à T-015 | 4 183,21 € | 5 020 € | 2027-01-15 | Tous les risques du registre traités sauf R-12 (backend) | Formation juridique (T-015) : 550 € de temps et environ 700 € HT de frais pour un niveau débutant, sur un besoin rare |
| **B · Plan sans juridique** (retenue) | T-002 à T-014 | **3 633,21 €** | **4 360 €** | **2027-01-15** | Tous les risques critiques et hauts couverts sauf R-12 ; utilise la recette de `reservation-coworking` (T-045) et forme un second relecteur sécurité avant les congés de Karim | `juridique` reste absente : conseil externe au cas par cas |
| C · Plan resserré | T-002 à T-005, T-008, T-009, T-012 | 2 368,21 € | 2 850 € | 2027-01-15 | Coût réduit de 1 265 € par rapport à B | Claire seule en recette et en relation client, Nadia seule sur Docker ; la fenêtre de la recette T-045 est perdue |
| D · Plan minimal | T-002, T-003 | 967,50 € | 1 170 € | 2026-12-18 | Coût minimal | Pas de second relecteur sécurité pendant les congés de Karim ; Nadia seule à savoir restaurer (leçon de DEC-019 sans suite) ; `documentation` orpheline |

Le détail (coût par salarié, contrôle de capacité, risques résiduels) est dans T-017 § 3.

**Frais externes** (provisions à confirmer par devis, que `tableau.py` ne compte pas) : soit dans une enveloppe séparée de `budget_eur` (retenu), soit inclus dans `budget_eur` (écarté : l'alerte à 90 % de S1-R11 se déclencherait trop tard).

## Décision
1. **Option B.** Les formations retenues sont T-002 à T-014. **T-015 (juridique) n'est pas retenu** : un besoin juridique est traité par un conseil externe, saisi au cas par cas sur décision humaine (comme pour `reservation-coworking/T-084`).
2. **Projet `esn-interne`** (`projet.md`) :
   - `budget_eur: 4360` (coût temps de 3 633,21 € + marge de 20 %) ; seuil d'alerte S1-R11 à 3 924 € ;
   - `deadline: 2027-01-15` ;
   - `salaries_affectes: [claire, karim, lea, nadia]` ;
   - `etat_projet: en_cours`.
3. **Allocations à `esn-interne`** (S1-R10), en % de la capacité :

   | Salarié | P1 (2026-11-30 → 2026-12-18) | Total P1 | P2 (2026-12-21 → 2027-01-15) | Total P2 |
   |---|---|---|---|---|
   | Claire | 5 % | 25 % | 0 % | 20 % |
   | Karim | 5 % | 25 % | 10 % | 30 % au plus |
   | Léa | 25 % | 25 % | 10 % | 10 % |
   | Nadia | 10 % | 60 % | 20 % | 25 % |

   Aucun total (`reservation-coworking` + `esn-interne`) ne dépasse 100 %. Les allocations de P1 sont appliquées dès la validation de cette décision ; celles de P2 le 2026-12-21, car `tableau.py` ne connaît qu'une valeur par projet.
4. **Frais externes : enveloppe séparée de 700 € HT**, hors `budget_eur`, pour la formation « supervision » de Nadia (T-002, 2026-12-03), engagée sur devis. Elle est suivie dans `planning.md` d'`esn-interne` tant qu'aucun outil ne la suit (ticket `amelioration` T-018). Toute dépense au-delà de l'enveloppe passe par une nouvelle décision humaine.
5. **Ordre de priorité des formations** (risque d'abord, puis fenêtre) ; en cas de manque de capacité, on retire dans l'ordre inverse :
   1. T-003, T-004, T-005 : sécurité et revue humaine ;
   2. T-008, T-009 : sauvegarde-restauration ;
   3. T-002 : supervision (date fixe, EV-002) ;
   4. T-012 : documentation ;
   5. T-006, T-007 : recette ;
   6. T-010, T-011 : docker ;
   7. T-013, T-014 : relation client.
6. **`reservation-coworking` garde la priorité** : un binôme peut être suspendu sans délai si le chemin critique du GO l'exige. Aucun ticket du projet client n'est modifié, et aucun coût n'est imputé au client.

## Pourquoi
Les mots d'Ethan : « Je retiens B parce qu'il casse les dépendances révélées par les scénarios : Léa devient la deuxième personne sur la sécurité et les revues humaines avec Karim, Karim secourt Nadia sur la sauvegarde, et Nadia reprend la documentation de Hugo. A ajoute 1 250 € pour un besoin juridique rare, qu'un conseil externe au cas par cas couvre mieux ; C et D laissent des points uniques de défaillance que la crise simulée a montrés dangereux. La marge de 20 % est voulue : on a vu hier qu'un budget sans marge se fait dépasser. Les frais externes vont dans une enveloppe séparée parce que tableau.py ne compte que les heures : les mélanger au budget fausserait l'alerte à 90 %, le problème que R18 vient de corriger. »

## Impacts
- **Fichiers à mettre à jour par le coordinateur, après la validation** (CLAUDE.md § 5) :
  - `projets/esn-interne/projet.md` : `budget_eur`, `deadline`, `salaries_affectes`, `etat_projet`, historique des décisions ;
  - `equipe/membres/claire.md`, `karim.md`, `lea.md`, `nadia.md` : allocation `esn-interne` de P1, puis de P2 le 2026-12-21 ; section des formations prévues ;
  - `equipe/calendrier.md` : **EV-002 est conservé** (la capacité nulle de Nadia le 2026-12-03 reste juste pour `reservation-coworking`).
- **Tickets** :
  - T-017 : débloqué par un humain, `decision: DEC-024` ;
  - T-001 : à conclure (critères cochés, `EN_REVUE`) ;
  - T-016 : le `chef-de-projet` passe T-015 `ANNULE` en citant DEC-024, ré-estime T-016 et met `planning.md` à jour pour l'option B ;
  - T-002 à T-014 : à faire par des humains (AF11, R15), planifiables dès l'application des allocations de P1 ; T-002 doit être prenable le 2026-12-03 ;
  - T-018 (`amelioration`, créé le 2026-11-27 à la demande d'Ethan) : proposer un suivi des frais externes, que `tableau.py` ne compte pas.
- **Budget de l'ESN** : 3 633,21 € s'ajoutent à la part ESN consolidée dans `PORTFOLIO.md`, plus 700 € HT de frais externes hors tableau.
- **Règles** : aucune modifiée.
- **Points à confirmer par un humain** : congés de fin d'année de Claire, Léa et Nadia (non déclarés ; sinon P2 glisse dans la marge du 11 au 15/01) ; devis de la formation « supervision » ; accord de Claire pour présenter Léa au client (T-013).
- **Restent ouverts** : R-12 (backend : Karim seul à pouvoir piloter un ticket critique backend en binôme ; recrutement ou plan 2027, à décider à part) ; R-16 (`porter-une-decision` et `revue-humaine` absentes des fiches d'équipe).
