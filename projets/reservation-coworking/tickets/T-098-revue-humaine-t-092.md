---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-098
titre: SIMULATION — Revue humaine T-092 (vérification quotidienne des sauvegardes)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: revue-code (expert)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-021, T-029]   # ex. [T-001, T-002]
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
> **SIMULATION** — Revue humaine annoncée dans T-092 (retour d'expérience de l'exercice de crise T-080, DEC-019), créée au triage demandé par Ethan le 2026-11-26 ; imputée à l'ESN (DEC-020).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-098 — SIMULATION — Revue humaine T-092 (vérification quotidienne des sauvegardes)

## Description
Revue humaine (S3-R2, AF3) de [T-092](T-092-simulation-verification-restauration-sauvegardes.md), écrit par Nadia : `scripts/verifier_sauvegarde.py` (existence de la sauvegarde de moins de 26 h, restauration dans un conteneur jetable, contrôle de cohérence, alerte) et sa tâche planifiée. Le script exécute des commandes Docker sur le moteur de la production et lit des sauvegardes qui contiennent des données personnelles. Karim n'en est pas l'auteur (S3-R1) ; il relit le code Python, les tests et la restauration PostgreSQL (`backend-python`, `base-de-donnees-sql` et `revue-code` expert). C'est le même choix que pour [T-038](T-038-revue-humaine-t-029.md). L'acceptation de la PR par C reste un critère de T-092.

**T-092 est un prérequis du GO [T-046](T-046-go-mise-en-production.md)** (DEC-020, point 3) : cette revue est donc sur le chemin du GO.

**Pas de `depend_de` vers T-092** (AF3) : **prenable quand T-092 passe `EN_REVUE`.** `depend_de: [T-021, T-029]` reprend les dépendances de T-092, pour le placement dans le tableau.

**Imputation (DEC-020)** : T-092 relève de la crise, imputée à l'ESN ; cette revue l'est aussi (coût hors budget client, 39,29 €).

**Disponibilité (AF8)** : Karim est `actif`, alloué à 20 % (DEC-020), sans `date_depart` ; revue attendue avant le GO, hors EV-003 (2026-12-21 au 31).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-092 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Le faux Docker montre que le script ne vise que `esn-verif-sauvegarde-<slug>` (`run --rm`, sans volume nommé ni port publié), ne lance jamais `compose`, `volume rm`, `volume prune` ni `down`, et ne lit jamais `db_password` ; chaque cas d'échec a son test.
- [ ] Le contrôle de cohérence (lignes par table, 3 salles, au moins un compte accueil) et l'absence de contenu de données dans le journal local sont vérifiés.
- [ ] Chaque réserve donne un commentaire à traiter dans T-092 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · création (triage demandé par Ethan, T-090 point 3, T-092 à la place de T-088) ; Karim : 20 %, actif, revue attendue avant le GO, hors EV-003 ; depend_de [T-021, T-029] (celles de T-092), pas de depend_de vers T-092 (AF3) · 0 h
- 2026-11-26 22:40 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client · 0 h
