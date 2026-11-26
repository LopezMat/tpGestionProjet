---
titre: SIMULATION — Absence de Léa (26-27/11) et départ de Hugo (04/12) - prise d'acte, sans réaffectation
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-26
valide_par:  Ethan               # rempli par l'humain qui valide
decision: DEC-021           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-021
date: 2026-11-26
decide_par: Ethan
projet: reservation-coworking
ticket: T-102, T-103
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
> **SIMULATION** — Décision prise dans l'exercice d'événements d'équipe (scénario 3, S1) du 2026-11-26. Hugo ne part pas en réalité.

<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-021 — SIMULATION — Absence de Léa et départ de Hugo

## Contexte
Deux événements d'équipe ont été traités par les skills `absence` et `depart-membre` :
- **Léa** est absente du 2026-11-26 au 2026-11-27, pour congés (EV-001, déjà au calendrier). Sa fiche est passée `conges`. Ticket [T-102](../../projets/reservation-coworking/tickets/T-102-simulation-absence-lea.md).
- **Hugo** quitte l'ESN le 2026-12-04, avec un préavis de 6 jours ouvrés, sans ticket « Préavis court » (EV-004 ajouté). Sa fiche est passée `depart_prevu`. Ticket [T-103](../../projets/reservation-coworking/tickets/T-103-simulation-depart-hugo.md).

Analyses du `chef-de-projet` :
- **Léa** : aucun impact. Elle n'est allouée à aucun projet et n'a aucun ticket. La revue d'accessibilité a été refusée par DEC-009 E, et aucun ticket frontend n'est critique. Fin projetée le 2026-12-16, soit 2 jours ouvrés avant la deadline.
- **Hugo** :
  - aucun ticket ouvert (T-006, T-051 à T-053 `ANNULE`), aucun ticket terminé à son nom, aucun effet sur le planning ni sur le budget client ;
  - deux besoins restent sans titulaire : la compétence `documentation` (personne d'autre ne l'a), et le second relecteur `securite-applicative` prévu par l'ancien T-053.

## Options étudiées
| Ticket | Option | Avantages | Inconvénients |
|---|---|---|---|
| T-102 | **A · prendre acte sans rien changer** | 0 €, aucun délai, aucun risque | — |
| T-102 | B · réintroduire la revue d'accessibilité (1,5 h, 96,43 €) | meilleure accessibilité | revient sur DEC-009 E ; dépasse 4 200 € si elle est payée par le client |
| T-103 | **A · aucune réaffectation, l'analyse sert de note de connaissances, besoins renvoyés au plan de formation de l'ESN** | 0 € pour le projet | les besoins restent ouverts hors projet |
| T-103 | B · A et une note de passation (1 h, environ 50 €, payée par l'ESN) | trace écrite | peu utile : rien n'est à transmettre |
| T-103 | C · A et une formation `documentation` ou un recrutement (environ 450 € ou plus, payés par l'ESN) | ferme le manque de compétence | coûteux ; le recrutement aboutirait après la deadline |
| Imputation | **ESN** | coût client de 4 158,93 €, marge de 41,07 € | — |
| Imputation | budget client | — | coût client de 4 181,43 €, marge de 18,57 € |

## Décision
1. **T-102, option A** : on prend acte de l'absence de Léa, sans changer aucun ticket. Au retour, le 2026-11-30, le coordinateur repasse sa fiche en `actif` et EV-001 en `confirme`.
2. **T-103, option A** : aucune réaffectation, puisque Hugo n'a rien d'ouvert ; l'analyse de T-103 sert de note de connaissances. Les deux besoins sont renvoyés au **plan de formation de l'ESN**, hors de ce projet (DEC-009 E) : la compétence `documentation`, et un nouveau candidat au second relecteur `securite-applicative`. Le 2026-12-04, le coordinateur passe la fiche de Hugo en `parti` (`allocation: {}`) et EV-004 en `confirme`.
3. **Imputation** : le coût des analyses de T-102 (0,5 h) et de T-103 (1 h), soit 22,50 €, est **pris en charge par l'ESN**, selon la règle provisoire de DEC-020 (ligne de journal « imputé à l'ESN »).

## Pourquoi
Les mots d'Ethan : « Léa et Hugo n'ont ni ticket ni allocation sur ce projet ; les événements d'équipe relèvent de la vie interne de l'ESN, pas du client. Le vrai risque révélé est la dépendance à deux personnes (Nadia, Karim), à traiter dans le plan de formation de l'ESN. »

Les raisons du `chef-de-projet` (T-102 et T-103, § 5), retenues par Ethan :
- aucun ticket n'est touché par l'absence de Léa ; l'option B rouvrirait DEC-009 E alors que le budget client n'a aucune marge ;
- Hugo n'a rien d'ouvert ni rien produit à transmettre ;
- ni Léa ni Hugo ne travaillent pour ce client : le coût des analyses relève de l'ESN.

**Plan de formation de l'ESN** : en plus des besoins `documentation` et du second relecteur sécurité, il doit traiter la dépendance à deux personnes. Nadia est la seule à savoir restaurer (`sauvegarde-restauration`, `docker`), et Karim le seul en `securite-applicative` et en revue humaine.

## Impacts
- `equipe/calendrier.md` : `decision: DEC-021` sur EV-001 et EV-004. `equipe/membres/lea.md` (`conges`, retour le 2026-11-30) et `hugo.md` (`depart_prevu`) sont à jour ; leur fin de cycle (actif, puis parti) se fera aux dates prévues.
- T-102 et T-103 : ligne de journal « imputé à l'ESN (DEC-021) ». Ils restent `ATTENTE_HUMAIN` jusqu'à ce qu'Ethan renseigne lui-même `decision: DEC-021`.
- Aucun ticket réaffecté ni créé. `planning.md` v1.1 ne change pas : il signale déjà l'absence de Léa.
- Plan de formation de l'ESN : `documentation` et second relecteur `securite-applicative`, à rattacher au futur projet interne de l'ESN (question ouverte de DEC-020).
- Coût client : 4 158,93 € HT pour 4 200 €, soit une marge de 41,07 €.
