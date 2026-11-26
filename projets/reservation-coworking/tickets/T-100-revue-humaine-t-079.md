---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-100
titre: SIMULATION — Revue humaine T-079 (verrou des dépendances, image figée)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
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
---
> **SIMULATION** — Revue humaine annoncée dans T-079 (veille 2026-S48), créée au triage demandé par Ethan le 2026-11-26 ; au budget client (T-079 n'est pas imputé à l'ESN par DEC-020).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-100 — SIMULATION — Revue humaine T-079 (verrou des dépendances, image figée)

## Description
Revue humaine (S3-R2, AF3) de [T-079](T-079-verrou-dependances-image-figee.md), écrit par `agent:dev-backend` : fichier de verrouillage avec empreintes (`pip install --require-hashes`), image `python:3.14-slim` fixée par digest, pip 26.2.0 ou plus, règle de reconstruction dans `app/README.md` (chaîne d'approvisionnement, constats 1 et 5 des rapports `securite`). Karim n'en est pas l'auteur (S3-R1) ; il a `securite-applicative` (confirme) et `backend-python` (expert). L'avis de Nadia (`docker` confirme) sur la ligne `FROM` peut être demandé si besoin, sans ticket séparé.

**Pas de `depend_de` vers T-079** (AF3) : **prenable quand T-079 passe `EN_REVUE`.** T-079 n'a lui-même aucune dépendance.

**Imputation** : T-079 porte sur l'app du client (`app/`) et reste au budget client (DEC-020 ne l'impute pas à l'ESN) ; cette revue aussi (39,29 €).

**Disponibilité (AF8)** : Karim est `actif`, alloué à 20 % (DEC-020), sans `date_depart` ; revue attendue avant le 2026-12-18, hors EV-003 (2026-12-21 au 31).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-079 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Le fichier de verrouillage contient toutes les transitives avec empreintes, Starlette ≥ 1.3.1 et Pydantic ≥ 2.9.0 ; le `Dockerfile` installe avec `--require-hashes` ; le digest de l'image de base est fixé ou son absence justifiée.
- [ ] Chaque réserve donne un commentaire à traiter dans T-079 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · création (triage demandé par Ethan, revue annoncée dans T-079) ; au budget client ; Karim : 20 %, actif, revue attendue avant le 2026-12-18, hors EV-003 ; pas de depend_de vers T-079 (AF3) · 0 h
