---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-096
titre: SIMULATION — Revue humaine T-086 (volume de production protégé)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-029]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn (R18, DEC-023)
imputation_decision: DEC-020   # décision VALIDÉ qui met ce ticket à la charge de l'ESN
---
> **SIMULATION** — Revue humaine annoncée dans T-086 (action corrective de l'exercice de crise T-080), créée au triage demandé par Ethan le 2026-11-26 ; imputée à l'ESN (DEC-020).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-096 — SIMULATION — Revue humaine T-086 (volume de production protégé)

## Description
Revue humaine (S3-R2, AF3) de [T-086](T-086-simulation-proteger-volume-production.md), écrit par Nadia : volume de base `external` et label `esn.production` dans le modèle commun `deploiement/docker-compose.yml` (DEC-003), création du volume par `scripts/deployer_local.py`, interdits documentés. Karim n'en est pas l'auteur (S3-R1) ; il relit le code Python et les tests de `scripts/` (`backend-python` et `revue-code` expert). Personne d'autre que Nadia n'a `docker` (AF10 b, DEC-009 point E) ; c'est le même choix que pour [T-038](T-038-revue-humaine-t-029.md) et [T-059](T-059-revue-humaine-t-058.md). L'acceptation de la PR par C reste un critère de T-086.

**Pas de `depend_de` vers T-086** (AF3) : **prenable quand T-086 passe `EN_REVUE`.** `depend_de: [T-029]` reprend la dépendance de T-086, pour que le tableau ne place pas cette revue avant que T-086 soit réalisable.

**Imputation (DEC-020)** : T-086 relève de la crise, imputée à l'ESN ; cette revue l'est aussi (coût hors budget client, 39,29 €).

**Disponibilité (AF8)** : Karim est `actif`, alloué à 20 % (DEC-020), sans `date_depart` ; revue attendue avant le 2026-12-18, hors EV-003 (2026-12-21 au 31).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-086 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Les tests de `scripts/` montrent que `down -v` sur un projet jetable laisse le volume en place, et que la création du volume (avec label) n'a lieu qu'à la première mise en service.
- [ ] L'effet sur la procédure de fin de démonstration (T-049, option 2) est vérifié et noté dans la ligne de revue.
- [ ] Chaque réserve donne un commentaire à traiter dans T-086 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · création (triage demandé par Ethan, T-090 point 3) ; Karim : 20 %, actif, revue attendue avant le 2026-12-18, hors EV-003 ; depend_de [T-029] (celle de T-086), pas de depend_de vers T-086 (AF3) · 0 h
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
