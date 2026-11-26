---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-103
titre: "SIMULATION — Départ de Hugo : plan de passation"
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 1            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur le plan de passation du départ de Hugo (EV-004)   # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:        DEC-021           # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le: 2026-11-26        # facultatif : date du premier passage EN_COURS
termine_le:     2026-11-26            # facultatif : date du passage TERMINE
imputation: esn             # client | esn (R18, DEC-023)
imputation_decision: DEC-021   # décision VALIDÉ qui met ce ticket à la charge de l'ESN
---
> **SIMULATION** — Événement d'équipe (scénario 3, S1), skill `depart-membre`, demandé par l'humain le 2026-11-26. Hugo ne part pas en réalité.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-103 — SIMULATION — Départ de Hugo : plan de passation

## Description
Skill [depart-membre](../../../.claude/skills/depart-membre/SKILL.md). **Hugo** (développeur junior, `equipe/membres/hugo.md`) quitte l'ESN le **2026-12-04**. Aucun motif n'est enregistré.

**Préavis** (étape 2) : du 2026-11-27 au 2026-12-04 inclus, hors samedis, dimanches et `jours_feries` (aucun sur la période), soit 27/11, 30/11, 01/12, 02/12, 03/12 et 04/12 : **6 jours ouvrés**. C'est au moins 5 : **pas de ticket « Préavis court »** (S1-R8).

**Fait par le coordinateur** (étape 3) :
- fiche de Hugo passée `statut: depart_prevu`, `date_depart: 2026-12-04` ;
- événement **EV-004** (`depart`, `prevu`) ajouté au calendrier.

**Constat du coordinateur** : Hugo a `allocation: {}` (0 % sur ce projet depuis DEC-009, point D1). Ses tickets dans le projet sont tous `ANNULE` : T-006, T-052, T-053, et T-051 (binôme, Karim). Il est le salarié de l'équipe qui a `documentation` au niveau confirmé ; vérifier s'il est le seul.

**Attendu du `chef-de-projet`** (étape 5 du skill) :
- ses tickets ouverts ;
- ses connaissances : tickets terminés dont il est l'auteur, compétences où il est le seul au niveau `confirme` ou plus ;
- les tickets de transfert proposés ;
- la réaffectation de chaque ticket selon AF1 à AF10 ;
- le planning recalculé (capacité, fin projetée, budget) ;
- pour une compétence orpheline, un ticket `formation` ou une option « recrutement ». Attention : DEC-009, point E, interdit les tickets `formation` dans ce projet.

Il passe ensuite le ticket `ATTENTE_HUMAIN`. **Aucune réaffectation avant la décision humaine.**

## Analyse d'impact
<!-- Remplie par le chef-de-projet -->
*`chef-de-projet`, 2026-11-26, SIMULATION. Sources : `equipe/membres/*.md`, `equipe/agents.md`, `equipe/calendrier.md` (EV-004), `equipe/humains.md`, tous les tickets du projet (recherche de `salarie:hugo` et de « Hugo »), `docs/` (recherche de « Hugo », DEC-009, DEC-010, DEC-015, DEC-017, DEC-020), `planning.md` v1.1. Chiffres : `python scripts/tableau.py --date 2026-11-26`.*

Préavis vérifié : 6 jours ouvrés, du 2026-11-27 au 2026-12-04 inclus, sans jour férié. C'est au moins 5 : pas de ticket « Préavis court » (S1-R8).

### 1. Tickets ouverts de Hugo
**Aucun.** `reservation-coworking` est le seul projet, et Hugo y est à 0 % depuis DEC-009 (point B1). Tous les tickets qui le concernent sont `ANNULE` :

| Ticket | Assigné | Statut | Reste à faire | Fenêtre | Devenir du besoin |
|---|---|---|---|---|---|
| T-006 Écritures Markdown par Edit/Write (hook R5/R6) | Hugo | `ANNULE` (DEC-009 D1) | 0 h | aucune | **déjà réalisé sans lui** par la PR de règles de l'ESN (DEC-015, `projet: ESN`) : R17 dans `CLAUDE.md`, détection dans `restreindre_bash.py`, tests `TestR17`. Aucun travail interne ne l'attend. |
| T-051 Binôme T-006 | Karim | `ANNULE` | 0 h | aucune | sans objet (T-006 fait ailleurs) |
| T-052 Formation `backend-python` (binôme T-006) | Hugo | `ANNULE` (DEC-009 D1, E) | 0 h | aucune | **le besoin disparaît** avec le départ : à retirer du plan de formation de l'ESN |
| T-053 Formation `securite-applicative` (second relecteur) | Hugo | `ANNULE` (DEC-009 D1, E) | 0 h | aucune | **le besoin demeure** (AF10 b : Karim est le seul relecteur `securite-applicative`, en congés du 21 au 31/12, EV-003), mais **son candidat part**. À redésigner au plan de formation de l'ESN, voir le point 6. |

**Réaffectation (AF1 à AF10)** : aucune n'est nécessaire, aucun ticket ouvert n'est assigné à Hugo. Je recommande de **laisser `assigne: salarie:hugo` sur T-006, T-052 et T-053** : ce sont des tickets `ANNULE`, donc de l'historique, et `tableau.py` ne les compte ni dans la charge ni dans la capacité. Le critère « aucun ticket ne reste assigné à Hugo au-delà du 2026-12-04 » vaut pour le travail ouvert, et il est rempli. Contrôle à faire après le passage de la fiche en `parti` : relancer `tableau.py` et vérifier que la section « Anomalies de données » reste vide.

### 2. Connaissances
- **Tickets terminés dont il est l'auteur : aucun.** Aucune ligne de journal `salarie:hugo` dans le projet ; T-006 n'a jamais démarré. Aucun livrable de `docs/` ne le cite comme auteur.
- **Compétences**, comparées à toutes les fiches salariés et au catalogue des agents :

| Compétence de Hugo | Autres salariés | Agents | Risque après le 2026-12-04 |
|---|---|---|---|
| `backend-python` (débutant) | Karim (expert) | `dev-backend` | aucun |
| `javascript` (débutant) | Léa (confirmée) | `dev-frontend` | aucun |
| `tests-unitaires` (débutant) | **aucun** | `dev-backend`, `dev-frontend`, `testeur` | faible : plus aucun salarié, mais Hugo n'était pas `confirme` (hors AF10 b), et les agents couvrent la compétence |
| **`documentation` (confirmé)** | **aucun** : Claire, Karim, Léa et Nadia ne l'ont pas | **aucun** : aucun agent ne la déclare dans `equipe/agents.md` | **compétence orpheline** dans le référentiel (AF10 a) |

- **Effet de la compétence orpheline sur ce projet : nul.** Aucun ticket n'a `competence_requise: documentation`. Les documents du projet (README, runbooks T-085, rapports) sont produits par les agents et par Nadia, sous d'autres compétences.
- **Effet sur l'ESN** : la fiche de Hugo le décrit comme la ressource « utile pour les tickets de transfert lors d'un départ ». Après lui, une passation documentaire reposera sur des agents qui n'ont pas la compétence au référentiel, ou sur un salarié qui ne l'a pas.

### 3. Tickets de transfert
**Aucun n'est utile pour ce projet**, puisque rien n'est à transmettre : ni ticket ouvert, ni livrable, ni connaissance du code (Hugo n'a pas travaillé sur `app/`). Ni binôme ni revue croisée ne sont nécessaires. Un ticket « Note de passation » est chiffré en option B, mais il n'est pas recommandé.

### 4. Planning, capacité, budget
- **Capacité** : la capacité allouée au projet ne change pas (Hugo à 0 %). L'utilisation de Claire (38,9 %, signalée, AF9), de Karim (51,5 %) et de Nadia (53,6 %) est inchangée.
- **Fin projetée : 2026-12-16** (T-048), deadline le 2026-12-18, **marge de 2 jours ouvrés**, inchangée.
- **Budget** (4 200 € HT, DEC-020) :

| Indicateur (`tableau.py` du 2026-11-26) | Valeur |
|---|---|
| Consommé total | 1 356,29 € (32,3 %), avant le temps de T-102 et de T-103 |
| Coût projeté à terminaison | 5 888,93 € |
| Coût client si T-102 et T-103 restent au budget client | 5 888,93 − 1 782,50 + 75,00 = **4 181,43 €** (99,6 %, marge 18,57 €) |
| Coût client si T-102 et T-103 sont imputés à l'ESN (recommandé) | 4 181,43 − 22,50 = **4 158,93 €** (99,0 %, marge 41,07 €) |
| Rappel de `planning.md` v1.1 | 4 151,43 € ; +30,00 € dus à T-101 (7,50 €), T-102 (7,50 €) et T-103 (15,00 €), tous créés après la v1.1 |

  Le départ lui-même ne coûte rien au client. Seule cette analyse est un coût (1 h × 15 € = 15 €). Pas d'alerte S1-R11 : coût client sous 4 200 €, consommé client loin des 3 780 €, mise en service avant la deadline. **Attention** : si T-102 et T-103 restent au budget client, la marge tombe à 18,57 €, soit environ 1,2 h d'agent ou 0,2 h de Claire ou de Karim.

### 5. Effet sur le travail interne de l'ESN
- **Lot R17** (DEC-009 D1, DEC-010) : déjà livré par la PR de règles DEC-015, sans Hugo. Rien ne reste en attente.
- **Plan de formation de l'ESN** (DEC-009 E). Il n'a ni fichier ni projet : le projet interne n'existe pas (`docs/a-integrer/lot2-D.md` point 9 ; question ouverte (a) de DEC-020). Il perd :
  - la formation `backend-python` de Hugo (ex-T-052) : le besoin s'éteint ;
  - le candidat au second relecteur `securite-applicative` (ex-T-053) : le besoin AF10 b demeure ;
  - la seule compétence `documentation` de l'équipe.
- **Capacité de l'ESN** : −35 h par semaine de développeur junior non alloué. Sans effet sur ce projet.

### 6. Compétence orpheline : formation ou recrutement
DEC-009 E interdit tout ticket `formation` dans ce projet. Un ticket `formation` `documentation` irait donc **au plan de formation de l'ESN, dans le futur projet interne** (par exemple `projets/esn-interne/`, lot2-D point 9). En attendant ce projet, le besoin est inscrit dans le fichier DEC de cette décision, comme pour DEC-009 E. Il en va de même pour le second relecteur `securite-applicative` (ex-T-053), dont il faut désigner un nouveau candidat. Le choix de la personne est une décision humaine.

### 7. Décision demandée (R7)
**Question** : quel plan de passation retenir pour le départ de Hugo le 2026-12-04, sachant qu'aucun ticket ouvert ne lui est assigné et que la compétence `documentation` n'existera plus dans l'équipe ?

| Option | Contenu | Coût | Délai | Risque |
|---|---|---|---|---|
| **A. Aucune réaffectation, note de connaissances, besoins renvoyés au plan de l'ESN (recommandée)** | Cette analyse tient lieu de note de connaissances. Pas de ticket de transfert. Le fichier DEC inscrit au plan de formation de l'ESN : (1) `documentation`, orpheline, avec la piste la moins chère, déclarer `documentation` pour les agents qui en produisent déjà (`analyste-besoin`, `dev-backend`) par une PR sur `equipe/agents.md` (R11, fichier de B) ; (2) le second relecteur `securite-applicative`, candidat à redésigner ; (3) le retrait de la formation `backend-python` de Hugo. | projet : 0 € ; ESN : environ 0,5 h d'agent (7,50 €) pour la PR, si elle est retenue | aucun ; fin projetée le 2026-12-16 | faible : la compétence `documentation` n'est requise par aucun ticket du projet |
| B. Option A, plus un ticket de transfert « Note de passation de Hugo » (1 h, Hugo, avant le 2026-12-04), imputé à l'ESN | Il faut une allocation temporaire de Hugo de 3 % jusqu'au 2026-12-04 (AF8, S1-R10, décision humaine), ou un projet interne | ESN : 50,00 € (Hugo, 50 €/h) ; client : 0 € | aucun sur le projet ; fenêtre du 2026-11-27 au 2026-12-04 | valeur faible, puisqu'il n'a rien produit à transmettre ; crée une allocation et un ticket dans un projet client pour un salarié qui part |
| C. Option A, plus un remplacement de la compétence par une personne : formation `documentation` d'un salarié (1 jour, 7 h, par exemple Léa, à 0 % et disponible) ou recrutement d'un profil junior avec `documentation` | Au plan de l'ESN, hors de ce projet (DEC-009 E) | formation : environ 450 € (7 h × 64,29 €/h) ; recrutement : coût de l'ESN, hors projet | aucun sur le projet ; un recrutement aboutirait après la deadline | aucun pour le client ; c'est un arbitrage de capacité de l'ESN, pas de ce projet |

**Recommandation : A.** Le départ n'a aucun effet sur le planning, la capacité, la fin projetée ni le budget du client. Le seul vrai manque, la compétence `documentation` et le candidat au second relecteur sécurité, concerne l'ESN : il doit être arbitré dans son plan de formation, pas financé par ce projet. Je recommande aussi d'**imputer T-102 et T-103 à l'ESN** (coût client de 4 158,93 € au lieu de 4 181,43 €), même question que dans T-102.

**Après la décision** :
- tracer la décision (`tracer-decision`) ;
- le `chef-de-projet` ajoute, si l'humain le souhaite, une ligne de journal dans T-052 et T-053 qui cite le `DEC-NNN`, sans changer leur statut ni leur assigné ;
- si l'option B est retenue, il crée le ticket de transfert, et le coordinateur applique l'allocation ;
- le 2026-12-04, le coordinateur passe la fiche en `parti`, `allocation: {}`, et EV-004 en `confirme` (skill `depart-membre`, étape 7) ;
- `planning.md` n'a pas à changer pour le départ (la v1.1 indique déjà « sans effet »). En revanche, il faut une v1.2 si l'imputation de T-102 et de T-103 change le tableau « Imputation à l'ESN ».

## Critères d'acceptation
- [x] Le plan de passation est écrit (tickets, connaissances, transfert, réaffectations, planning, compétences orphelines).
- [x] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [x] Aucun ticket ne reste assigné à Hugo au-delà du 2026-12-04.
- [x] À la date de départ : fiche en `statut: parti`, `allocation: {}`, EV-004 `confirme`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 20:40 · agent:coordinateur · SIMULATION · création (skill depart-membre, étapes 1 à 4) : préavis de 6 jours ouvrés, fiche `depart_prevu`, EV-004 au calendrier · 0 h
- 2026-11-26 23:35 · agent:chef-de-projet · SIMULATION · A_FAIRE → EN_COURS ; lecture des fiches de `equipe/membres/`, de `equipe/agents.md`, des tickets du projet (`salarie:hugo`, « Hugo »), de `docs/` (DEC-009, DEC-010, DEC-015, DEC-017, DEC-020, lot2-D point 9) ; `tableau.py` lancé · 0 h
- 2026-11-26 23:55 · agent:chef-de-projet · SIMULATION · plan de passation écrit : aucun ticket ouvert (T-006, T-051 à T-053 ANNULE ; lot R17 livré par DEC-015 sans Hugo), aucun ticket terminé dont il est l'auteur, `documentation` orpheline (aucun salarié ni agent), second relecteur `securite-applicative` (ex-T-053) sans candidat ; fin projetée le 2026-12-16, coût client de 4 181,43 € (4 158,93 € si T-102 et T-103 sont imputés à l'ESN) ; options A (recommandée), B et C ; aucune réaffectation ni création de ticket ; EN_COURS → ATTENTE_HUMAIN · 1 h
- 2026-11-26 23:59 · agent:coordinateur · SIMULATION · décision d'Ethan tracée dans DEC-021 (EN_REVUE) : option A, aucune réaffectation, `documentation` et second relecteur `securite-applicative` renvoyés au plan de formation de l'ESN ; imputé à l'ESN (DEC-021, règle provisoire de DEC-020) : coût hors budget client. Le 2026-12-04 : fiche en `parti`, EV-004 `confirme`. Ticket laissé ATTENTE_HUMAIN : `decision` à renseigner par Ethan · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-021`), d'après la ligne « imputé à l'ESN (DEC-021) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
