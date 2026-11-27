---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-021
titre: Actions retenues de la rétrospective de la semaine projet (23 au 27/11)
projet: esn-interne
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur les actions A1 à A10 du retex de la semaine projet (projets/esn-interne/retex.md), à retenir, reporter ou écarter   # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:         DEC-025          # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:     2026-11-27            # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-021 — Actions retenues de la rétrospective de la semaine projet (23 au 27/11)

## Description
Ticket `decision` du rituel de rétrospective (S1-R7, S1-R13, VISION § 3.5), préparé par [T-020](T-020-retrospective-semaine-projet.md). Le détail de chaque constat, avec ses sources, est dans [retex.md](../retex.md) (`EN_REVUE`). **Décision attendue : un nouveau `DEC-NNN`.**

**Assignation.** Le ticket reste assigné au `chef-de-projet`, auteur de l'analyse (exception d'AF2, comme pour T-017). La validation formelle est humaine (R5).

**Taux** (ARCHITECTURE § 8, R12) : agent 15 €/h. Toutes les actions coûtées sont des heures d'agent, imputées à `esn-interne` (outils et règles communs, R19). Le temps des membres humains de l'équipe projet, relecture des PR comprise, n'est pas chiffré par `tableau.py`.

### 1. Question
Parmi les actions A1 à A10 proposées par le retex de la semaine, **lesquelles l'ESN retient-elle**, avec quelle priorité, et lesquelles reporte-t-elle ou écarte-t-elle ?

### 2. Actions proposées
| Id | Action | Constat (retex) | Classement | h | € | Assigné proposé | Priorité | Recommandation |
|---|---|---|---|---|---|---|---|---|
| A1 | `tableau.py` signale (a) un ticket encore `ATTENTE_HUMAIN` ou `BLOQUE` alors qu'une DEC `VALIDÉ` le cite (cas de T-057 depuis le 2026-11-25), et (b) un ticket `decision` `TERMINE` à 0 h (9 tickets, 342,50 € sortis de la projection) | P3, P5 | `amelioration` : **T-019 enrichi** (même PR de règles), pas de nouveau ticket | 2,5 | 37,50 | `agent:dev-backend` (réalisation de T-019) | haute | retenir |
| A2 | Skill `tracer-decision` : le temps du porteur (`temps_passe_h`) est noté à la clôture d'un ticket `decision`, ou 0 assumé avec une ligne de journal | P5 | PR R11 | 0,5 | 7,50 | cadrage `agent:chef-de-projet`, PR coordinateur | normale | retenir |
| A3 | Plus de bandeau « En attente de validation humaine » dans le corps des documents : l'en-tête fait foi (21 DEC `VALIDÉ` portent encore ce bandeau) | P4 | PR R11 (même PR que A2) | 0,5 | 7,50 | idem | basse | retenir |
| A4 | La validation se fait dans la PR du contenu, avant son merge, avec un message de commit explicite (4 PR sur 24 ne portaient qu'une validation faite après le merge) | P1 | PR R11 (même PR que A2) | 0,5 | 7,50 | idem | normale | retenir |
| A5 | Signal « révision en cours » : `BROUILLON` pendant une révision par un agent (13 agents, `_ENTETE.md`) | P2 | PR R11 | 1,5 | 22,50 | coordinateur | basse | **reporter** (2 cas du 2026-11-24, aucune récidive) |
| A6 | Règle 6 du `chef-de-projet` : un audit de sécurité par incrément, plus l'audit avant GO (T-043 : 5 h estimées, 12,5 h passées) | P6 | PR R11 | 0,5 | 7,50 | coordinateur | normale | retenir |
| A7 | Audit avant GO outillé : l'agent `securite` lit les résultats de `securite.yml` (ou les outils sont installés sur le poste) ; `bandit` étendu à `projets/*/app` | P7 | `amelioration` (cadrage 1 h), puis PR R11 (2 h) | 3 | 45,00 | cadrage `agent:chef-de-projet`, réalisation `agent:dev-backend` | **haute** (avant l'audit avant GO, GO le 2026-12-15) | retenir |
| A8 | Heure des journaux donnée par le coordinateur au lancement de chaque agent | P8 | rien (pratique) | 0 | 0 | coordinateur | basse | ne rien faire au-delà de la pratique |
| A9 | Lignes de journal `interruption` et `désaccord`, pour tracer les pistes non tracées (quota de l'outil, commandes concurrentes, désaccords) | pistes non tracées | rien (pratique) | 0 | 0 | tous | basse | ne rien faire au-delà de la pratique |
| A10 | Plan de formation (S1-R13) : aucun besoin nouveau, registre R-01 à R-17 inchangé ; P9 (corrigé par R18), P10 (occurrence unique) et P11 (résolu) sans suite | P9 à P11 | rien | 0 | 0 | — | — | ne rien faire |

### 3. Options
| | **1 · Tout retenir** | **2 · Sélection recommandée** | **3 · Minimum** | **4 · Rien** |
|---|---|---|---|---|
| Actions retenues | A1 à A7 | A1, A2, A3, A4, A6, A7 | A1, A7 | aucune |
| Reportées ou écartées | A8 à A10 (pratiques, sans coût) | A5 reporté ; A8 à A10 sans coût | A2 à A6 | A1 à A7 |
| Heures (agent) | 9,0 h | **7,5 h** | 5,5 h | 0 |
| **Coût** | **135,00 €** | **112,50 €** | **82,50 €** | **0 €** |
| PR de règles | 4 (T-019 ; `tracer-decision` et registre ; `chef-de-projet` ; outils d'audit) + 1 (13 agents et `_ENTETE.md`) | 4 | 2 (T-019 ; outils d'audit) | 0 |
| Ce qui reste ouvert | — | P2, couvert en partie par A4 et R6 | P1 à P6 : validations hors PR, bandeaux obsolètes, temps des décisions non noté, audits mal estimés | tout : T-057 et les clôtures à 0 h restent invisibles au tableau, et l'audit avant GO se fait sans outils |

### 4. Recommandation : option 2
1. **A1 et A7 d'abord** (priorité haute). A1 rend visibles au tableau les deux défauts qui ont faussé des chiffres cette semaine : 175 € de part ESN (DEC-023) et 7,50 € de projection ici. A7 évite un audit avant GO de `reservation-coworking` sans analyse automatique des dépendances, alors que la veille 2026-S48 a relevé des vulnérabilités (T-078, CVSS 8,8).
2. **A2, A3 et A4 dans une seule PR** sur `tracer-decision` et le registre : 22,50 € pour trois défauts tracés (P1, P4, P5), qui coûtent à chaque décision.
3. **A6** : 7,50 € pour qu'une livraison incrémentale, la méthode retenue par DEC-022, ne sous-estime plus l'audit.
4. **A5 reporté** : 22,50 € et 13 fichiers d'agent pour un cas qui ne s'est pas reproduit depuis le 2026-11-24. R6 a limité les dégâts, et A4 traite l'essentiel (valider après le message de fin de l'agent). À revoir au retex de `reservation-coworking`.
5. **Pas d'action artificielle** : A8 à A10 sont des pratiques sans coût. Le plan de formation n'appelle aucune mise à jour (S1-R13, A10).

### 5. Impact
- **Budget d'`esn-interne`** : 4 360 € (DEC-024) ; seuil d'alerte S1-R11 de 90 %, soit **3 924 €** ; coût projeté actuel **3 723,21 €** (85,4 %, `tableau.py` du 2026-11-27, T-020 et ce ticket compris ; planning.md v1.0 annonçait 3 655,71 €, l'écart est détaillé dans le retex).

  | Option | Projeté | % | Réserve sous le seuil |
  |---|---|---|---|
  | 1 · Tout retenir | 3 858,21 € | 88,5 % | 65,79 € |
  | **2 · Sélection recommandée** | **3 835,71 €** | **88,0 %** | **88,29 €** |
  | 3 · Minimum | 3 805,71 € | 87,3 % | 118,29 € |
  | 4 · Rien | 3 723,21 € | 85,4 % | 200,79 € |

  **Toutes les options passent sous le seuil, sans révision du budget.** Réserve : la réalisation de T-019 n'est pas encore estimée. Avec l'option 2, il reste environ 5,9 h d'agent avant le seuil. Si T-019 dépasse ce volume, sa propre décision de modification de règle devra comporter une révision du budget d'`esn-interne` (`revision-budget`) ou un report.
- **Échéance** (2027-01-15) : aucun effet sur le chemin critique du plan de formation (T-012 → T-010). Les actions sont des tickets d'agent, sans capacité salariée.
- **Allocations** : aucune modification. Aucun salarié n'est assigné à une action.
- **Projets clients** : aucun ticket modifié, aucun coût client. A6 conduit en plus à arbitrer la ré-estimation de T-043 dans `reservation-coworking` (+75 € au coût client, 99,4 % de 4 200 €). C'est une décision du pilotage du projet (T-008), à prendre à part.
- **Après la décision** (rien n'est fait avant, règle 13 ; R11) :
  - le `chef-de-projet` crée les tickets `amelioration` retenus dans `projets/esn-interne/tickets/` (A7 : cadrage), et ajoute A1 au périmètre de T-019, avec une ligne de journal qui cite le DEC ;
  - **toute modification de règle** (A2 à A7, et A1 pour `tableau.py`) passe par une **PR de règles** : branche dédiée, fichier `DEC-NNN`, ligne dans `docs/CHANGELOG-REGLES.md`, revalidation humaine des documents touchés (R11). Aucun ticket `formation` n'est créé (A10) ;
  - le retex passe `VALIDÉ` par un humain, s'il le juge conforme.
- **Hors décision, signalé au coordinateur** : T-057 attend que son champ `decision: DEC-013` soit renseigné par un humain ; T-080 peut être conclu (critère 2 rempli de fait).

## Critères d'acceptation
- [x] Un humain a tranché (actions retenues, reportées ou écartées, et leur priorité) ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [x] `temps_passe_h` de ce ticket est renseigné par l'humain qui décide (0 seulement si c'est assumé, avec une ligne de journal ; voir A2).
- [x] Les tickets `amelioration` retenus sont créés, ou T-019 est enrichi, avec une ligne de journal qui cite le DEC ; les actions écartées ou reportées sont notées au journal de ce ticket.
- [x] Aucune règle, aucun agent, aucun skill, aucun workflow ni aucun script n'est modifié en dehors d'une PR de règles (R11).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 · agent:chef-de-projet · création en ATTENTE_HUMAIN (T-020) : actions A1 à A10 chiffrées, options 1 à 4, option 2 recommandée (112,50 €), projeté d'esn-interne à 88,0 %, sous le seuil de 3 924 €. Heure non indiquée : l'agent n'a pas accès à l'horloge · 0 h
- 2026-11-27 · agent:coordinateur · décision d'Ethan reçue (option 2, avec son « pourquoi ») et tracée dans DEC-025 (`EN_REVUE`, skill `tracer-decision`) ; ticket laissé `ATTENTE_HUMAIN` : le champ `decision` et le déblocage reviennent à l'humain (R7) · 0 h
- 2026-11-27 · Ethan · 0,5 h · Actions de la rétro choisies (option 2), DEC-025 validée, ticket débloqué.
- 2026-11-27 10:58 · agent:chef-de-projet · application de DEC-025 : A1 ajoutée au périmètre de T-019 (priorité haute) ; tickets amelioration créés : T-022 (cadrage A7, haute, 1 h), T-023 (PR de règles A2-A3-A4, normale, 1,5 h), T-024 (PR de règles A6, normale, 0,5 h). A5 reporté au retex de reservation-coworking (ou plus tôt en cas de récidive) ; A8, A9 et A10 sans ticket (pratiques sans coût, plan de formation inchangé) · 0 h