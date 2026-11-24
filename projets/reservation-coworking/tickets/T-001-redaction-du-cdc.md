---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-001
titre: Rédaction du CDC
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:analyste-besoin        # agent:<nom> | salarie:<prenom>
competence_requise: redaction-cdc (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 8            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision: DEC-006           # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le: 2026-11-24                # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-24      # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-001 — Rédaction du CDC

## Description
Ticket de travail de l'`analyste-besoin` (R14, étape 2 du pipeline). À partir de [demande.md](../demande.md), rédiger `projets/reservation-coworking/cdc.md` selon `templates/cdc.md` : besoins fonctionnels des membres (réservation par créneau d'une heure, disponibilités, annulation) et de l'accueil (réservations du jour), contraintes (budget 6 000 €, deadline 2026-12-18, données personnelles limitées au nom et à l'e-mail), exigences de sécurité et RGPD, critères d'acceptation vérifiables, et questions ouvertes pour le client.

Repère d'estimation : 7 h pour une application métier (skill `nouveau-projet`).

## Critères d'acceptation
- [x] `cdc.md` existe, suit `templates/cdc.md` avec l'en-tête standard et la ligne de provenance, en `EN_REVUE`.
- [x] Chaque besoin exprimé dans `demande.md` est repris dans le CDC avec au moins un critère d'acceptation vérifiable.
- [x] Les contraintes de budget, de délai et de données personnelles sont reprises sans modification.
- [x] Les questions ouvertes de `demande.md` sont traitées ou reprises dans le CDC.
- [x] Un ticket `decision` « Validation du CDC » est créé en `ATTENTE_HUMAIN`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 13:49 · agent:coordinateur · création · 0 h
- 2026-11-24 14:00 · agent:analyste-besoin · passage EN_COURS, lecture de demande.md et projet.md · 0 h
- 2026-11-24 14:30 · agent:analyste-besoin · rédaction de cdc.md v0.1 (3 Must, 13 questions ouvertes dont 6 bloquantes, 9 hypothèses) et création du ticket T-003 (ATTENTE_HUMAIN) · 5 h
- 2026-11-24 14:30 · agent:analyste-besoin · passage EN_REVUE (jamais TERMINE : validation humaine à suivre) · 0 h
- 2026-11-24 16:00 · agent:analyste-besoin · révision de cdc.md en v0.2 avec les réponses du client transmises par Claire (arbitrage humain sur T-003, option 2) : F-04 en Must, F-05 exclue, F-06 en Should, F-07 et F-08 ajoutées, règles chiffrées, § 8 à 11 mis à jour, 13 questions tranchées ou acceptées, 5 nouvelles questions (Q-14 à Q-18) · 1,5 h
- 2026-11-24 16:00 · agent:analyste-besoin · ticket laissé EN_REVUE (validation humaine du CDC v0.2 à suivre via T-003) · 0 h
- 2026-11-24 17:00 · agent:analyste-besoin · révision de cdc.md en v0.3 (arbitrages d'Ethan, DEC-006) : F-08 en Should (5 Must, écart à S4-R5 justifié), H-10 à H-17 acceptées, Q-14 et Q-18 tranchées avec critères vérifiables (compte accueil initial, réinitialisation par l'accueil, changement de son propre mot de passe), revue humaine d'authentification attribuée à Karim (AF3) · 1 h
- 2026-11-24 17:00 · agent:analyste-besoin · ticket laissé EN_REVUE (validation humaine du CDC v0.3 à suivre via T-003) · 0 h
- 2026-11-24 18:00 · agent:analyste-besoin · révision de cdc.md en v0.4 (arbitrages d'Ethan, DEC-006) : changement obligatoire du mot de passe à la première connexion étendu aux comptes membres (critère en F-07, § 7 et § 8 ajustés), Q-15, Q-16 et Q-17 closes par hypothèses acceptées (H-17, H-20, H-21) · 0,5 h
- 2026-11-24 18:00 · agent:analyste-besoin · ticket laissé EN_REVUE (validation humaine du CDC v0.4 à suivre via T-003) · 0 h
- 2026-11-24 18:30 · agent:coordinateur · critères d'acceptation vérifiés (cdc.md v1.0 VALIDÉ par Ethan, DEC-006 ; T-003 créé puis tranché) ; passage TERMINE · 0 h
