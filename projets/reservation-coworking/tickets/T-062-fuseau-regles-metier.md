---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-062
titre: Instant hors fuseau de Paris non converti dans « regles » (constat 12)
projet: reservation-coworking
type: bug                   # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-012]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-062 — Instant hors fuseau de Paris non converti dans « regles » (constat 12)

## Description
Constat 12 (bas) du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), qui recoupe les remarques 1, 2 et 3 du `relecteur-code` sur [T-012](T-012-regles-metier-horloge.md). `regles._heure_murale` (`app/reservation/regles.py:24-26`) retire le fuseau **sans convertir** : un `maintenant` avec fuseau, exprimé dans un autre fuseau que Paris, est comparé comme une heure de Paris. Le défaut est latent (aucun appelant aujourd'hui), mais T-018 et T-019 l'exposeraient : psycopg renvoie un `timestamptz` dans le fuseau de la session (`Etc/UTC` par défaut dans l'image `postgres`). La règle F-02 (H-15) et la règle « créneau commencé » de F-01 (H-11) seraient alors contournées. **À corriger avant T-018**, qui en dépend désormais.

- **Étapes de reproduction** (constatées par le `securite` au commit `2852fe7`, Python 3.14) : un jour ouvré, à 10 h 30 heure de Paris, appeler `verifier_annulation` pour un créneau de 10 h-11 h, par un membre, avec `maintenant` égal au même instant exprimé en UTC (09 h 30 UTC).
- **Résultat attendu** : refus (créneau commencé), comme avec `maintenant` exprimé en heure de Paris.
- **Résultat obtenu** : annulation acceptée ; de même, réservation possible d'un créneau commencé depuis 1 à 2 h.
- **Environnement** : `app/` au commit `2852fe7`, tests unitaires (aucune base).

Le même ticket traite la remarque 3 de T-012 (même fichier `tests/test_regles.py`), pour éviter deux reprises successives du même fichier.

## Critères d'acceptation
- [ ] `_heure_murale` convertit un instant avec fuseau en heure de Paris (`astimezone(horloge.FUSEAU)`) avant de retirer le fuseau ; un instant sans fuseau lève une erreur de programmation explicite, distincte de `ReglePasRespectee` (test).
- [ ] Test du cas reproduit : à 10 h 30 heure de Paris exprimé en UTC, l'annulation par un membre du créneau de 10 h est refusée, et la réservation de ce créneau aussi ; mêmes résultats qu'avec l'instant exprimé en heure de Paris.
- [ ] Tests au changement d'heure (remarque 2 de T-012) : le lundi 2026-03-30 et le lundi 2026-10-26, avec `maintenant` exprimé en UTC, le créneau de 8 h est « non commencé » à 7 h 59 heure de Paris et « commencé » à 8 h 00 heure de Paris.
- [ ] `test_regles_nappellent_pas_lhorloge` (remarque 3 de T-012) est remplacé par un test qui échoue réellement si une règle lit l'horloge système (par exemple un double de `datetime` dans l'espace de noms de `regles` qui lève une erreur sur `now` ou `today`) ; l'assertion sur le texte source est retirée.
- [ ] Couverture de `regles` d'au moins 80 % ; suite complète verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (règle métier pure, comme T-012 ; ni authentification ni données personnelles)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage du constat 12 et des remarques 1, 2 et 3 de T-012) ; T-018 en dépend désormais · 0 h
