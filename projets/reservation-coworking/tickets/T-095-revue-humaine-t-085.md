---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-095
titre: SIMULATION — Revue humaine T-085 (runbook « volume supprimé »)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
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
> **SIMULATION** — Revue humaine annoncée dans T-085 (action corrective de l'exercice de crise T-080), créée au triage demandé par Ethan le 2026-11-26 ; imputée à l'ESN (DEC-020).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-095 — SIMULATION — Revue humaine T-085 (runbook « volume supprimé »)

## Description
Revue humaine (S3-R2, AF3) de [T-085](T-085-simulation-runbook-volume-supprime.md), écrit par Nadia : procédure sur les données de production (`runbooks/perte-donnees.md`, cas « volume supprimé » et « sauvegarde absente des traces »). Karim n'en est pas l'auteur (S3-R1). Il relit les commandes PostgreSQL (`pg_restore -l` puis `-L`, rôle `esn`, rôle applicatif de T-058) avec `base-de-donnees-sql` (expert) et `revue-code` (expert). Personne d'autre que Nadia n'a `sauvegarde-restauration` (AF10 b, renvoyé au plan de formation de l'ESN par DEC-009, point E) ; c'est le même choix que pour [T-038](T-038-revue-humaine-t-029.md). L'acceptation de la PR par D reste un critère de T-085.

**Pas de `depend_de` vers T-085** (AF3) : T-085 ne passe `TERMINE` qu'une fois la ligne « Revue humaine » remplie, une dépendance rendrait les deux tickets impossibles à prendre. **Ce ticket devient prenable quand T-085 passe `EN_REVUE`.** T-085 n'a lui-même aucune dépendance.

**Imputation (DEC-020)** : T-085 relève de la crise, imputée à l'ESN ; cette revue l'est aussi (coût hors budget client, 39,29 €).

**Disponibilité (AF8)** : Karim est `actif`, alloué à 20 % (DEC-020, dont 5 % pour les revues imputées à l'ESN), sans `date_depart`. Fenêtre attendue avant le 2026-12-18, hors de ses congés du 2026-12-21 au 2026-12-31 (EV-003).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-085 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Les commandes de la section « Volume de la base supprimé » sont vérifiées dans l'ordre (recréation du seul service `db`, restauration avant tout démarrage de l'app, option sans `session`, rôle applicatif) ; aucune valeur de secret n'apparaît dans le runbook.
- [ ] Chaque réserve donne un commentaire à traiter dans T-085 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · création (triage demandé par Ethan, T-090 point 3) ; Karim : 20 %, actif, revue attendue avant le 2026-12-18, hors EV-003 ; pas de depend_de vers T-085 (AF3) · 0 h
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
