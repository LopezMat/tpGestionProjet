---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-107
titre: "Arbitrage : dépassement de T-043 (audit sécurité) et comptage de l'audit avant GO"
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.25          # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: arbitrage humain sur le dépassement de T-043 et le comptage de l'audit avant GO, avant d'engager l'audit (condition 1 de DEC-020)
validation_humaine_requise: oui   # oui | non
decision:        DEC-026           # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:     2026-11-27            # facultatif : date du passage TERMINE
imputation: client          # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-107 — Arbitrage : dépassement de T-043 (audit sécurité) et comptage de l'audit avant GO

## Description

### Contexte
- [T-043](T-043-audit-securite.md) « Audit sécurité » (`agent:securite`) est estimé à **5 h**. **12,5 h** ont été passées en 7 audits d'incrément, faits à la suite de [DEC-011](../../../docs/decisions/2026-11-25-DEC-011-increment-consultation-coworking.md), où chaque ticket de l'incrément passait par `securite`. Les 7 rapports (`securite-2026-11-25` à `-6`, `securite-2026-11-26`) sont `NON BLOQUANT`, sans constat critique ni haut.
- L'**audit avant GO** (porte 3 de S3, critères actuels de T-043 : rapport sur le SHA du rapport de tests, seuils G, vulnérabilités critiques ou hautes suivies) **reste entier**. Il porte surtout sur du code jamais audité : l'authentification, les sessions et les rôles (T-013 à T-017), la réservation et l'annulation (T-018, T-019), la matrice d'autorisation (T-020), le front (T-022 à T-025), la purge (T-028) et les correctifs (T-058, T-061, T-069, T-075, T-079, T-105).
- Comme `temps_passe_h` (12,5 h) dépasse `estimation_h` (5 h), `tableau.py` compte un reste de 0 h. L'audit avant GO (environ 5 h × 15 € = **75 €**) n'est donc **compté nulle part** dans le coût client projeté. La proposition du `chef-de-projet` du 2026-11-25 14:45 (journal de T-043, options A et B) n'a jamais été arbitrée. Le retex de l'ESN l'a relevé ([esn-interne/retex.md](../../esn-interne/retex.md), constat P6, action A6), comme DEC-023 (Impacts, « Reste manuel »).
- [T-045](T-045-recette.md) (recette) et [T-046](T-046-go-mise-en-production.md) (GO) dépendent tous les deux de T-043.
- **Condition 1 de [DEC-020](../../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md)** : tout dépassement prévisible du budget client de 4 200 € HT (SIMULATION) est arbitré **avant** d'être engagé, et l'ESN n'en absorbe aucun d'office. L'alerte S1-R11 est levée dès 90 % de coût client.

### Coût client de départ (R18, DEC-023)
`tableau.py` n'a pas pu être relancé : le hook n'accepte que `python scripts/tableau.py` avec un chemin relatif, et le répertoire courant de l'agent n'est pas la racine du dépôt (constat P11 du retex). Le chiffre part donc du `TABLEAU.md` généré le 2026-11-27, auquel j'ajoute à la main deux effets de cette intervention. Le coordinateur doit le confirmer en relançant le script.

| Poste | Coût client projeté |
|---|---|
| `TABLEAU.md` du 2026-11-27, « Coût client projeté à terminaison » | 4 098,93 € |
| + T-008, pilotage : 1 h passée pour cette analyse, alors qu'il restait 0,75 h à l'estimation | + 3,75 € |
| + T-107, ce ticket : 0,25 h de Claire (550 € ÷ 7 = 78,57 €/h) | + 19,64 € |
| **Base B0, sans l'audit avant GO** | **4 122,32 € (98,2 %, marge 77,68 €)** |
| *Pour mémoire, chiffre du coordinateur (4 098,93 € + 75 €), avant cette intervention* | *4 173,93 € (99,4 %)* |

Consommé client : 1 386,29 € (33,0 %), loin du seuil de 3 780 €. Fin projetée : 2026-12-16, deadline : 2026-12-18. Part ESN projetée : 1 652,50 €.

**Second sous-comptage, du même type que T-043 (à arbitrer aussi, question 2).** Après cette intervention, le pilotage [T-008](T-008-pilotage.md) a 13,5 h passées pour 13,25 h estimées. Son reste est donc de 0 h, alors qu'il reste à faire jusqu'au 2026-12-18 le retex (1 h, critère de T-008) et le suivi : triage des suites de l'audit et de la recette, passages `avancement` de la condition 1. Ces deux postes représentent **au moins 2 h, soit 30 €**. Ne pas les montrer reproduirait l'erreur de T-043 (P6). Dans le tableau des options, la colonne « avec pilotage » les inclut.

### Question
1. **Comment traiter le dépassement de T-043 et compter l'audit avant GO**, avant de l'engager ?
2. **Faut-il ré-estimer le pilotage T-008 de +2 h (30 €)** pour le retex et le suivi jusqu'à la livraison ?

### Options (question 1)
L'audit avant GO est réalisé dans toutes les options (porte 3 de S3, prérequis de T-045 et T-046). Aucune ne touche aux Must, à F-08, aux revues humaines ni à la recette.

- **A · Découpage, tout au client.** L'estimation de T-043 passe à 12,5 h (= temps passé). Le ticket est renommé « Audits d'incrément (DEC-011) », ses critères sont adaptés aux 7 rapports existants, et le coordinateur le conclut (R13). Un nouveau ticket `tache` « Audit sécurité avant GO » (`agent:securite`, 5 h, `securite-applicative (confirme)`) reprend les critères actuels de T-043 et remplace T-043 dans `depend_de` de T-045 **et** de T-046. C'est la proposition A du 2026-11-25, et elle respecte la règle 3 (7 h au plus par ticket).
- **B · Un seul ticket porté à 17,5 h.** Même coût que A. C'est contraire à la règle 3 du `chef-de-projet` (7 h au plus par ticket) : l'audit avant GO n'a plus de ligne propre dans le tableau, et l'on ne voit plus quand il commence.
- **C · Découpage, audit avant GO imputé à l'ESN** (`imputation: esn`, qui exige une décision `VALIDÉ`, R18). Au regard de DEC-020, ce n'est pas une absorption d'office si un humain le décide : la condition 1 n'est donc pas violée dans la forme. Mais c'est **difficile à justifier sur le fond**. L'audit avant GO n'est ni une faute de l'ESN ni un outil commun : c'est une porte S3 prévue depuis le planning v1.0 (DEC-009), et le CDC § 8 en fixe le niveau. Le client recevrait gratuitement un service qu'il a acheté. Surtout, on imputerait à l'ESN le mauvais ticket : l'écart vient des audits d'incrément, pas de l'audit final.
- **D · Découpage, audits d'incrément (T-043) imputés à l'ESN, audit avant GO au client.** Le découpage est celui de A. T-043 (12,5 h passées, 187,50 €) passe en `imputation: esn` sur décision `VALIDÉ`, et le nouveau ticket « Audit sécurité avant GO » (5 h) reste au client. Le client paie ainsi **exactement l'audit qu'il a acheté** (5 h, planning v1.0). L'ESN paie les audits d'incrément nés de **son propre choix** : DEC-011 a été décidé par Ethan pour la soutenance (« montrer le fonctionnement du système »), pas à la demande du client. Elle paie aussi son **erreur d'estimation** : DEC-011 a été appliqué sans ré-estimation (P6). C'est la logique « l'ESN paie ses fautes » de DEC-020. *Limite* : ces audits ont aussi amélioré le code du client (20 constats, dont 13 fermés) et allègent l'audit avant GO. On peut donc soutenir qu'une partie revient au client. Comme l'imputation se fait par ticket, la seule façon de la partager serait de déplacer du temps déjà journalisé, ce que je ne propose pas.
- **E · Découpage, audit avant GO réduit à 3 h** (au client). L'audit se limite au code non encore audité et aux seuils G, avec une simple vérification de non-régression sur le reste, au SHA candidat. Le niveau du CDC § 8 reste le même, mais la plus grosse part non auditée est aussi la plus sensible (authentification, sessions, autorisation). 3 h, c'est un pari d'estimation : s'il est perdu, la condition 1 se redéclenche **juste avant le GO**, au plus mauvais moment. Option déconseillée.
- *Avenant au client* : il n'est nécessaire que si A ou B est retenu **et** que la réserve de pilotage (question 2) est confirmée. Le dépassement serait alors de 27,32 €, et Claire en discuterait avec le client (AF1). Ce n'est pas une option à part entière pour la question 1.

### Chiffrage
Coûts en € HT, budget de 4 200 € (SIMULATION, DEC-020). « Avec pilotage » ajoute les 30 € de la question 2.

| Option | Coût client | % du budget | Marge | Avec pilotage : coût · % · marge | Part ESN projetée | Effet sur le chemin critique du GO (2026-12-15) |
|---|---|---|---|---|---|---|
| Base B0 (rien de décidé, audit non compté) | 4 122,32 € | 98,2 % | 77,68 € | 4 152,32 € · 98,9 % · 47,68 € | 1 652,50 € | chiffre faux de 75 € |
| **A** · découpage, tout au client | 4 197,32 € | 99,9 % | 2,68 € | 4 227,32 € · 100,7 % · **−27,32 €** | 1 652,50 € | aucun (voir ci-dessous) |
| **B** · un ticket de 17,5 h | 4 197,32 € | 99,9 % | 2,68 € | 4 227,32 € · 100,7 % · **−27,32 €** | 1 652,50 € | aucun ; audit invisible dans le Gantt |
| **C** · audit avant GO à l'ESN | 4 122,32 € | 98,2 % | 77,68 € | 4 152,32 € · 98,9 % · 47,68 € | 1 727,50 € | aucun |
| **D** · audits d'incrément à l'ESN | 4 009,82 € | 95,5 % | 190,18 € | 4 039,82 € · 96,2 % · 160,18 € | 1 840,00 € | aucun |
| **E** · audit avant GO réduit à 3 h | 4 167,32 € | 99,2 % | 32,68 € | 4 197,32 € · 99,9 % · 2,68 € | 1 652,50 € | aucun, mais risque de dépassement juste avant le GO |

Pour D, le consommé client passe de 1 386,29 € à 1 198,79 € (28,5 %), et le consommé ESN de 22,50 € à 210,00 €. Pour les autres options, le consommé ne change pas.

**Chemin critique.** L'audit avant GO (5 h, ou 3 h pour E) est le seul ticket ouvert de l'agent `securite` ; il tient en un jour ouvré (7 h par jour). Le Gantt place T-043 du 2026-12-07 au 2026-12-08, après les tickets de réalisation et en parallèle de T-042, soit **avant le début de la recette T-045 (2026-12-10)** et du GO (2026-12-15). La fin projetée (2026-12-16) ne bouge donc pas, quelle que soit l'option. À confirmer par `tableau.py` après l'application. Un risque est commun à toutes les options : un verdict `BLOQUANT` imposerait des correctifs avant la recette. Il ne dépend pas de l'option choisie.

### Recommandation
1. **Question 1 : option D.** C'est la seule qui respecte à la fois la règle 3 (découpage), le planning accepté par le client (un audit de 5 h, payé par lui) et la logique de DEC-020 : l'ESN paie ses choix et ses fautes, ici DEC-011 et l'absence de ré-estimation (P6). Elle ne masque aucun dépassement : la part ESN reste visible dans `TABLEAU.md` et `PORTFOLIO.md` (R18), et elle est décidée par un humain, pas absorbée d'office. **Si D est refusé** (au motif que les audits d'incrément ont servi le client), je recommande **A**. La marge tombe alors à 2,68 €, et la question 2 crée un dépassement prévisible de 27,32 € : il faut un arbitrage selon la condition 1 (avenant porté par Claire, AF1, ou prise en charge explicite par l'ESN) **avant** d'engager l'audit avant GO. Je déconseille B (règle 3), C (mauvais ticket imputé) et E (risque juste avant le GO).
2. **Question 2 : oui.** Estimation de T-008 portée de 13,25 h à 15,25 h (+2 h, 30 €), au client, comme le reste du pilotage du projet.
3. **Hors de ce projet, à signaler** : l'action A7 du retex de l'ESN (outils de l'agent `securite` : `pip-audit`, `bandit`, `gitleaks`, lecture de `securite.yml`) devrait être faite avant l'audit avant GO. Sinon, cet audit se fera comme les 7 autres, avec une revue manuelle des dépendances. `depend_de` ne traverse pas les projets : si A7 est retenu (`esn-interne/T-021`), le nouveau ticket passera `BLOQUE` avec `bloque_par` vers le ticket `esn-interne` concerné.

### Impact
Rien n'est modifié avant la décision. Après la décision, le `chef-de-projet` appliquera :
- **T-043** (A, C, D, E) : estimation 5 → 12,5 h ; titre « Audits d'incrément (DEC-011) » ; critères réécrits sur les 7 rapports existants (verdicts `NON BLOQUANT`, aucun constat critique ou haut sans ticket) ; conclusion par le coordinateur (R13). Pour D : `imputation: esn`, `imputation_decision: DEC-NNN`, avec une ligne de journal qui cite la décision. Pour B : estimation 5 → 17,5 h, rien d'autre.
- **Nouveau ticket « Audit sécurité avant GO »** (A, C, D, E) : `tache`, `agent:securite`, `securite-applicative (confirme)`, 5 h (3 h pour E), `depend_de` : celles de T-043 ; reprend les 3 critères actuels de T-043 et l'examen de l'écart « clé de signature des sessions » (DEC-007). Pour C : `imputation: esn` avec la décision.
- **T-045 et T-046** (A, C, D, E) : T-043 remplacé par le nouveau ticket dans `depend_de`, après vérification de l'absence de cycle.
- **T-008** (question 2) : estimation 13,25 → 15,25 h, avec une ligne de journal qui cite la décision.
- **Suite** : `tableau.py` relancé ; le coût client du tableau compte alors l'audit avant GO ; le critère « Condition 1 » de T-008 n'a plus d'ajout manuel.
- **Si A ou B, avec la question 2** : ticket `decision` de dépassement (condition 1) avant d'engager l'audit avant GO.

## Critères d'acceptation
- [x] Un humain a tranché les deux questions ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [x] Si C ou D est retenu, la décision cite les tickets passés en `imputation: esn` et elle est `VALIDÉ` avant que le champ soit écrit (R18).
- [x] T-043, le nouveau ticket éventuel, T-045, T-046 et T-008 portent une ligne de journal qui cite la décision ; aucun audit avant GO n'est engagé avant elle.
- [x] `TABLEAU.md` régénéré : le coût client projeté compte l'audit avant GO, sans ajout manuel.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 · agent:chef-de-projet · création (ATTENTE_HUMAIN), à la demande du coordinateur : condition 1 de DEC-020, alerte S1-R11 sur le coût client projeté. Porteur Claire (AF2 ; allocation de 20 % au projet, active, aucune absence au calendrier). Temps d'analyse compté dans T-008 · 0 h
- 2026-11-27 · agent:coordinateur · base B0 de 4 122,32 € confirmée par `tableau.py` relancé depuis la racine. Décision d'Ethan reçue (question 1 : option D ; question 2 : oui), avec son « pourquoi », et tracée dans DEC-026 (`EN_REVUE`) ; ticket laissé `ATTENTE_HUMAIN` : le champ `decision` et le déblocage reviennent à l'humain (R7) ; `imputation: esn` de T-043 non écrit avant la validation de DEC-026 (R18) · 0 h
- 2026-11-27 · Ethan · Option D retenue, DEC-026 validée, ticket débloqué · 0,5 h
