---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-102
titre: SIMULATION — Absence de Léa du 2026-11-26 au 2026-11-27
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ATTENTE_HUMAIN      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur l'absence de Léa (EV-001)   # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Événement d'équipe (scénario 3, S1), skill `absence`, demandé par l'humain le 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-102 — SIMULATION — Absence de Léa du 2026-11-26 au 2026-11-27

## Description
Skill [absence](../../../.claude/skills/absence/SKILL.md). **Léa** (développeuse front, `equipe/membres/lea.md`) est absente du **2026-11-26 au 2026-11-27 inclus**, motif `conges`. L'événement **EV-001** existait déjà au calendrier (`equipe/calendrier.md`, `capacite_pct: 0`, `prevu`) : il n'a pas été dupliqué. Comme l'absence commence aujourd'hui, la fiche est passée `statut: conges` ; elle repassera `actif` au retour, le 2026-11-30.

**Constat du coordinateur** : Léa a `allocation: {}` (aucun projet) et aucun ticket ne lui est assigné. Ses compétences (`html-css` expert, `accessibilite` confirmé) sont citées pour la revue d'accessibilité éventuelle (architecture § 6, « si le `chef-de-projet` l'affecte »). Ce ticket est créé dans `reservation-coworking`, seul projet actif, parce qu'une décision humaine est requise **même si l'impact est nul** (CLAUDE.md § 5).

**Attendu du `chef-de-projet`** (étape 4 du skill) : les tickets qui chevauchent la période (S1-R9), les options pour chacun (réaffecter, décaler, binôme), la fin projetée recalculée et l'écart avec la deadline, une alerte si un ticket `critique` ou la deadline est touché, ou « aucun impact ». Il passe ensuite le ticket `ATTENTE_HUMAIN`.

## Analyse d'impact
<!-- Remplie par le chef-de-projet -->
*`chef-de-projet`, 2026-11-26, SIMULATION. Sources : `equipe/membres/*.md`, `equipe/calendrier.md` (EV-001), `equipe/agents.md`, tous les tickets du projet (recherche de `salarie:lea` et de « Léa »), `planning.md` v1.1, architecture § 6, DEC-009 (point E), DEC-020. Chiffres : `python scripts/tableau.py --date 2026-11-26`, lancé avant cette analyse.*

### 1. Tickets qui chevauchent l'absence (S1-R9)
**Aucun.** Léa a `allocation: {}` et aucun ticket de `reservation-coworking`, seul projet actif, ne lui est assigné, quel que soit son statut. Elle n'a donc aucune fenêtre prévue les 26 et 27 novembre.

**Usages implicites vérifiés**, tous sans effet sur la période :
| Usage possible de Léa | Constat | Effet sur le 26 et le 27/11 |
|---|---|---|
| Revue d'accessibilité (architecture § 6, « si le `chef-de-projet` l'affecte ») | **Non retenue** par DEC-009 (point E : 1,5 h, 96,43 €). Les bonnes pratiques de base (H-07) sont vérifiées par le `relecteur-code`, le test de bout en bout T-026 et la recette T-045. Le journal de T-055 le note : « pas de revue Léa ». | aucun : rien n'est planifié |
| Revue humaine d'un ticket frontend `critique` (AF3, AF5) | Aucun ticket frontend n'est `critique` : les tickets `critique` sont T-029 et T-080 à T-083, aucun n'est du front. T-022, T-023, T-024, T-025, T-055 et T-075 portent « Revue humaine requise : non », parce que les contrôles d'accès sont côté serveur et revus par Karim (T-030 à T-036). | aucun |
| Tickets du front sur la période | T-022 et T-024 sont placés les 26 et 27/11, mais ils sont assignés à `agent:dev-frontend` (AF6). | aucun |

### 2. Options par ticket
Sans objet, puisqu'aucun ticket n'est concerné : il n'y a rien à réaffecter, à décaler ni à mettre en binôme.

### 3. Fin projetée et deadline
- `tableau.py` compte déjà EV-001 dans la capacité. **Fin projetée : 2026-12-16** (mise en service T-048). Deadline : 2026-12-18. **Marge : 2 jours ouvrés**, comme dans `planning.md` v1.1.
- **Budget** : l'absence ne change aucun coût. Le seul coût de l'événement est cette analyse (0,5 h × 15 € = 7,50 €), voir la question d'imputation au point 5.

### 4. Alerte
**Aucun impact.** Aucun ticket `critique` n'est touché, la deadline non plus. Pas d'alerte S1-R11 : coût client projeté sous 4 200 €, consommé client à 32,3 %, mise en service avant la deadline.

### 5. Décision demandée (R7)
**Question** : prendre acte de l'absence de Léa du 2026-11-26 au 2026-11-27 (EV-001), sans changement de planning ?

| Option | Coût | Délai | Risque |
|---|---|---|---|
| **A. Prendre acte, sans changer aucun ticket (recommandée)** | 0 € (en plus des 7,50 € d'analyse) | aucun ; fin projetée le 2026-12-16 | nul |
| B. Profiter du retour de Léa pour réintroduire la revue d'accessibilité refusée par DEC-009 E (1,5 h, à partir du 2026-11-30, après T-022 à T-024 et avant la recette T-045 du 2026-12-09), ce qui demande une allocation de 5 % (décision humaine, S1-R10) | 96,43 € (Léa, 64,29 €/h). **Au budget client** : coût client de 4 181,43 € à 4 277,86 €, soit **un dépassement de 4 200 €** qui déclenche la condition 1 de DEC-020 (avenant ou retrait de périmètre, discussion avec le client par Claire). **Imputée à l'ESN** : coût client inchangé | aucun : la revue est hors du chemin critique si elle est faite avant la recette | elle revient sur DEC-009 E ; budget client dépassé si elle n'est pas imputée à l'ESN |

**Recommandation : A.** Aucun ticket n'est concerné, et l'option B rouvre une décision déjà prise (DEC-009 E) alors que le budget client ne laisse aucune marge.

**Question annexe, à trancher avec T-103 : imputation des analyses d'événements.** Léa et Hugo ne sont pas alloués à ce client. T-102 (0,5 h) et T-103 (1 h) ne sont créés dans ce projet que parce qu'il n'existe pas de projet interne (`docs/a-integrer/lot2-D.md` point 9 ; question ouverte de DEC-020). Coût client (formule de DEC-020, `tableau.py` du 2026-11-26) :
- **au budget client** : 5 888,93 − 1 782,50 + 75,00 = **4 181,43 € HT** (99,6 % de 4 200 €, marge 18,57 €) ;
- **imputés à l'ESN**, comme le principe de DEC-020 point 3 : 4 181,43 − 22,50 = **4 158,93 € HT** (99,0 %, marge 41,07 €).

Recommandation : **imputer T-102 et T-103 à l'ESN**, avec la ligne de journal « imputé à l'ESN » ajoutée après la décision. L'écart avec les 4 151,43 € de `planning.md` v1.1 (+30,00 €) vient de T-101 (révision du CDC, 0,5 h, 7,50 €), de T-102 (7,50 €) et de T-103 (15,00 €), tous créés après la v1.1.

**Après la décision** : tracer la décision (`tracer-decision`). Au retour de Léa, le 2026-11-30, le coordinateur repasse sa fiche en `actif` et EV-001 en `confirme` (skill `absence`, étape 6). `planning.md` n'a pas à changer : la v1.1 indique déjà « Léa : absente les 2026-11-26 et 27 (EV-001). Sans effet : aucun ticket ».

## Critères d'acceptation
- [ ] L'analyse d'impact est écrite (tickets concernés, options, fin projetée, alerte ou « aucun impact »).
- [ ] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [ ] Au retour : fiche de Léa repassée `actif` et EV-001 `confirme`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 20:40 · agent:coordinateur · SIMULATION · création (skill absence, étapes 1 à 3) : EV-001 déjà présent, fiche de Léa passée `conges` · 0 h
- 2026-11-26 23:20 · agent:chef-de-projet · SIMULATION · A_FAIRE → EN_COURS ; lecture de `equipe/`, des tickets du projet (`salarie:lea`, « Léa »), de `planning.md` v1.1, de DEC-009 E et de DEC-020 ; `tableau.py` lancé · 0 h
- 2026-11-26 23:35 · agent:chef-de-projet · SIMULATION · analyse d'impact écrite : aucun ticket ne chevauche l'absence, aucun usage implicite planifié (revue d'accessibilité non retenue par DEC-009 E, aucun ticket frontend critique), fin projetée le 2026-12-16 (marge de 2 jours ouvrés), aucune alerte ; options A (recommandée) et B ; question d'imputation à l'ESN de T-102 et T-103 ; EN_COURS → ATTENTE_HUMAIN · 0,5 h
- 2026-11-26 23:59 · agent:coordinateur · SIMULATION · décision d'Ethan tracée dans DEC-021 (EN_REVUE) : option A, prise d'acte sans changement ; imputé à l'ESN (DEC-021, règle provisoire de DEC-020) : coût hors budget client. Ticket laissé ATTENTE_HUMAIN : `decision` à renseigner par Ethan · 0 h
