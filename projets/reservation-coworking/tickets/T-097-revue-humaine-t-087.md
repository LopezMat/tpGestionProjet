---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-097
titre: SIMULATION — Revue humaine T-087 (refus de recréer une base vide)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-029, T-086]   # ex. [T-001, T-002]
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
> **SIMULATION** — Revue humaine annoncée dans T-087 (action corrective de l'exercice de crise T-080), créée au triage demandé par Ethan le 2026-11-26 ; imputée à l'ESN (DEC-020).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-097 — SIMULATION — Revue humaine T-087 (refus de recréer une base vide)

## Description
Revue humaine (S3-R2, AF3) de [T-087](T-087-simulation-refus-base-vide.md), écrit par Nadia : `scripts/deployer_local.py` et `scripts/rollback_local.py` sortent en code 2 quand le volume de production manque alors que l'historique contient un déploiement vérifié, avec une option explicite réservée à une reconstruction décidée par un humain. Karim n'en est pas l'auteur (S3-R1) ; il relit le code et les tests (`backend-python` et `revue-code` expert). L'acceptation de la PR par C reste un critère de T-087.

**T-087 est un prérequis du GO [T-046](T-046-go-mise-en-production.md)** (DEC-020, point 3) : T-087 ne passe `TERMINE` qu'avec la ligne « Revue humaine » remplie. Cette revue est donc sur le chemin du GO.

**Pas de `depend_de` vers T-087** (AF3) : **prenable quand T-087 passe `EN_REVUE`.** `depend_de: [T-029, T-086]` reprend les dépendances de T-087, pour le placement dans le tableau.

**Imputation (DEC-020)** : T-087 relève de la crise, imputée à l'ESN ; cette revue l'est aussi (coût hors budget client, 39,29 €).

**Disponibilité (AF8)** : Karim est `actif`, alloué à 20 % (DEC-020), sans `date_depart` ; revue attendue avant le GO, donc avant le 2026-12-18, hors EV-003 (2026-12-21 au 31).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-087 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Les tests avec le faux Docker couvrent les deux scripts (historique non vide et volume absent → code 2, aucun `compose up`) et l'option explicite, dont l'usage est tracé dans la sortie.
- [ ] Chaque réserve donne un commentaire à traiter dans T-087 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · création (triage demandé par Ethan, T-090 point 3) ; Karim : 20 %, actif, revue attendue avant le GO, hors EV-003 ; depend_de [T-029, T-086] (celles de T-087), pas de depend_de vers T-087 (AF3) · 0 h
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client · 0 h
