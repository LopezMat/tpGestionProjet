---
titre: Actions retenues de la rétrospective de la semaine projet (23 au 27/11), option 2
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-27
valide_par:       Ethan          # rempli par l'humain qui valide
decision: DEC-025           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-025
date: 2026-11-27
decide_par: Ethan
projet: esn-interne
ticket: T-021
modifie_une_regle: non      # aucune règle n'est modifiée par cette décision : chaque PR de règles portera sa propre décision et ses lignes du changelog (R11), comme DEC-010 puis DEC-015
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-025 — Actions retenues de la rétrospective de la semaine projet

Rédigé par le coordinateur le 2026-11-27 à partir de la décision d'Ethan sur [T-021](../../projets/esn-interne/tickets/T-021-decision-actions-retrospective.md). Le « Pourquoi » est celui formulé par Ethan (skill `tracer-decision`, étape 1). L'en-tête fait foi pour le statut de ce document.

## Contexte
Rituel de rétrospective de fin de semaine projet, au niveau de l'ESN (VISION § 3.5, S1-R7, S1-R13), demandé par Ethan le 2026-11-27. Le ticket de travail [T-020](../../projets/esn-interne/tickets/T-020-retrospective-semaine-projet.md) (`chef-de-projet`, R14) a produit le [retex de l'ESN](../../projets/esn-interne/retex.md) (`EN_REVUE`). Chaque constat y cite sa source : tickets, journaux, DEC, CHANGELOG, et les faits Git relevés par le coordinateur. Il en ressort 11 problèmes (P1 à P11), dont :
- 4 PR sur 24 ne portent qu'une validation faite après le merge (P1) ;
- des décisions validées ne sont pas reportées sur leur ticket : T-057, `ATTENTE_HUMAIN` depuis le 2026-11-25 alors que DEC-013 est `VALIDÉ` (P3) ;
- 21 DEC `VALIDÉ` portent encore le bandeau « En attente de validation humaine » (P4) ;
- 9 tickets `decision` sont passés `TERMINE` à 0 h, soit 342,50 € sortis de la projection (P5) ;
- l'audit de sécurité, estimé pour un seul passage, a consommé 12,5 h au lieu de 5 h (P6) ;
- l'agent `securite` audite sans ses outils (P7).

Le retex propose les actions A1 à A10, chiffrées et classées. Le ticket [T-021](../../projets/esn-interne/tickets/T-021-decision-actions-retrospective.md) demande lesquelles retenir.

Budget d'`esn-interne` : 4 360 € ([DEC-024](2026-11-27-DEC-024-plan-formation-initial.md)). Seuil d'alerte S1-R11 : 3 924 €. Coût projeté avant la décision : 3 723,21 € (85,4 %).

## Options étudiées
| Option (détail dans T-021 § 3) | Avantages | Inconvénients |
|---|---|---|
| 1 · Tout retenir (A1 à A7) : 9 h, 135,00 € | tous les constats traités | A5 modifie les 13 agents pour 2 cas du 2026-11-24, sans récidive ; réserve sous le seuil réduite à 65,79 € |
| **2 · Sélection recommandée (A1, A2, A3, A4, A6, A7 ; A5 reporté) : 7,5 h, 112,50 €** | corrige les défauts récurrents et outille l'audit avant GO ; projeté à 88,0 %, sous le seuil | P2 (validation pendant une révision) n'est couvert que par A4 et R6 |
| 3 · Minimum (A1, A7) : 5,5 h, 82,50 € | les chiffres sont justes au tableau ; l'audit avant GO est outillé | les validations hors PR, les bandeaux obsolètes, le temps des décisions non noté et les audits mal estimés restent en l'état |
| 4 · Rien | aucun coût | T-057 et les clôtures à 0 h restent invisibles ; l'audit avant GO se fait sans outils |

## Décision
**Option 2.**
1. **Actions retenues**, toutes imputées à `esn-interne` (outils et règles communs, R19) :

   | Action | Contenu | Forme | h | € | Priorité |
   |---|---|---|---|---|---|
   | A1 | `tableau.py` signale (a) un ticket `ATTENTE_HUMAIN` ou `BLOQUE` cité par une DEC `VALIDÉ`, et (b) un ticket `decision` `TERMINE` avec `temps_passe_h: 0` et une estimation non nulle | périmètre de [T-019](../../projets/esn-interne/tickets/T-019-tableau-allocations-par-periode.md) enrichi (même PR de règles), sans nouveau ticket | 2,5 | 37,50 | haute |
   | A2 | skill `tracer-decision` : le temps du porteur d'un ticket `decision` est noté à sa clôture (0 seulement s'il est assumé, avec une ligne de journal) | PR de règles (R11) | 0,5 | 7,50 | normale |
   | A3 | plus de bandeau d'état dans le corps d'un document : l'en-tête fait foi ; les 21 fichiers existants ne sont pas modifiés | même PR qu'A2 | 0,5 | 7,50 | basse |
   | A4 | la validation se fait dans la PR du contenu, avant son merge, après le message de fin de l'agent, avec un message de commit explicite | même PR qu'A2 | 0,5 | 7,50 | normale |
   | A6 | règle 6 du `chef-de-projet` : un ticket « Audit sécurité » par livraison incrémentale, plus l'audit avant GO, estimés séparément ; ré-estimation au triage d'une décision qui ajoute un incrément | PR de règles (R11) | 0,5 | 7,50 | normale |
   | A7 | audit avant GO outillé : l'agent `securite` lit les résultats de `securite.yml` sur le SHA candidat, ou les outils sont installés sur le poste ; `bandit` étendu à `projets/*/app` | ticket `amelioration` (cadrage, 1 h), puis PR de règles (2 h) | 3 | 45,00 | **haute** : avant l'audit avant GO de `reservation-coworking` (GO du 2026-12-15) |
   | **Total** | | | **7,5** | **112,50** | |

2. **A5 est reporté** (signal « révision en cours » dans les 13 agents et `_ENTETE.md`) : à revoir au retex de `reservation-coworking`, ou plus tôt en cas de récidive.
3. **A8, A9 et A10 sont des pratiques sans coût**, sans ticket ni règle :
   - A8 : le coordinateur donne la date et l'heure dans chaque lancement d'agent ;
   - A9 : lignes de journal `interruption · <cause>` et `désaccord · <consigne> · <raison> · <suite>`, et note d'un refus de hook quand il survient ;
   - A10 : le plan de formation et son registre R-01 à R-17 sont inchangés, et aucun ticket `formation` n'est créé.
4. **Aucune règle n'est modifiée par cette décision.** A1 à A4, A6 et A7 passent par des PR de règles : une branche dédiée, leur propre fichier de décision (`modifie_une_regle: oui`), leurs lignes dans `docs/CHANGELOG-REGLES.md` et la revalidation humaine des documents touchés (R11). A2, A3 et A4 sont regroupés dans une seule PR.

## Pourquoi
*(Ethan, 2026-11-27)* « On retient les actions qui corrigent des erreurs qu'on a réellement faites plusieurs fois cette semaine : validations faites après le merge, temps des décisions oublié, bandeaux d'état périmés, tickets bloqués alors que leur décision était validée (A1 à A4). On ajoute A6 et A7 parce que la sécurité doit être vérifiée avant le GO du 15/12, pas après. On reporte A5 : modifier les 13 agents pour deux cas isolés sans récidive coûte plus que ce que ça apporte. Le total (112,50 €, imputé ESN) garde esn-interne sous le seuil d'alerte de 90 % (88,0 %). »

## Impacts
- **Budget d'`esn-interne`** : coût projeté de 3 723,21 € à **3 835,71 €** (88,0 % de 4 360 €), soit 88,29 € sous le seuil de 3 924 €. Aucune révision du budget. **Point d'attention** : la réalisation de T-019 n'est pas encore estimée. Au-delà d'environ 5,9 h d'agent, sa décision de modification de règle comportera une révision du budget (`revision-budget`) ou un report.
- **Échéance et allocations** : aucun effet. Les actions sont des tickets d'agent, sans capacité salariée, et le chemin critique du plan de formation (T-012 → T-010) n'est pas touché.
- **Projets clients** : aucun ticket modifié, aucun coût client. Le dépassement de l'audit de `reservation-coworking` (T-043), relevé par P6, est arbitré à part par un ticket `decision` du projet client (demande d'Ethan du 2026-11-27).
- **Tickets, après la validation de ce fichier** (rien n'est fait avant) :
  - T-021 : `decision: DEC-025`, débloqué par l'humain ;
  - le `chef-de-projet` ajoute A1 au périmètre de T-019, avec une ligne de journal qui cite DEC-025 ;
  - il crée dans `projets/esn-interne/tickets/` : le ticket `amelioration` de cadrage d'A7 (priorité haute) ; un ticket `amelioration` pour la PR A2-A3-A4 ; un ticket `amelioration` pour A6 ;
  - le coordinateur conclut T-020 (R13).
- **Fichiers ou règles à mettre à jour, dans les PR de règles** :
  - `scripts/tableau.py` et `scripts/test_tableau.py` (A1, avec T-019) ;
  - `.claude/skills/tracer-decision/SKILL.md` et `docs/decisions/README.md` (A2, A3, A4) ;
  - `.claude/agents/chef-de-projet.md`, règle 6 (A6) ;
  - `.github/workflows/securite.yml`, `.claude/agents/securite.md` et `.claude/hooks/restreindre_bash.py` (A7, après le cadrage).
- **Retex** : `projets/esn-interne/retex.md` peut être passé `VALIDÉ` par un humain sous cette décision, s'il le juge conforme.
