---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-099
titre: SIMULATION — Revue humaine T-078 (image PostgreSQL 16.16)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
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
> **SIMULATION** — Revue humaine annoncée dans T-078 (veille 2026-S48), créée au triage demandé par Ethan le 2026-11-26 ; imputée à l'ESN (DEC-020, outillage commun).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-099 — SIMULATION — Revue humaine T-078 (image PostgreSQL 16.16)

## Description
Revue humaine (S3-R2, AF3) de [T-078](T-078-image-postgresql-16-16.md), écrit par Nadia : passage de l'image du modèle commun `deploiement/docker-compose.yml` (DEC-003) à PostgreSQL 16.16 ou plus, qui corrige 43 CVE dont des exécutions de code à CVSS 8,8. Karim n'en est pas l'auteur (S3-R1) ; il a `securite-applicative` (confirme) et `base-de-donnees-sql` (expert), comme pour [T-059](T-059-revue-humaine-t-058.md). L'acceptation de la PR par C reste un critère de T-078.

**T-078 est un prérequis du GO [T-046](T-046-go-mise-en-production.md)** (DEC-020, point 3) : cette revue est donc sur le chemin du GO.

**Pas de `depend_de` vers T-078** (AF3) : **prenable quand T-078 passe `EN_REVUE`.** T-078 n'a lui-même aucune dépendance.

**Imputation (DEC-020)** : T-078 relève de l'outillage commun, imputé à l'ESN ; cette revue l'est aussi (coût hors budget client, 39,29 €).

**Disponibilité (AF8)** : Karim est `actif`, alloué à 20 % (DEC-020), sans `date_depart` ; revue attendue avant le GO, hors EV-003 (2026-12-21 au 31).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-078 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] La sortie `SELECT version()` (avant et après) montre 16.16 ou plus ; la version de l'image est fixée ou documentée dans le modèle commun.
- [ ] Le constat sur les index (GIN, btree sur `bpchar`, `gist_trgm_ops`) et sur les extensions est vérifié ; la suite de tests de l'app passe sur la nouvelle image.
- [ ] Chaque réserve donne un commentaire à traiter dans T-078 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · création (triage demandé par Ethan, revue annoncée dans T-078) ; Karim : 20 %, actif, revue attendue avant le GO, hors EV-003 ; pas de depend_de vers T-078 (AF3) · 0 h
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
