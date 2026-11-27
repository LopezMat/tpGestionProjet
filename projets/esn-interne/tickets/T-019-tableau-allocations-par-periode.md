---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-019
titre: tableau.py — allocations par période et absence pour formation rattachée à un ticket (PR de règles, R11)
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: planification (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné ; triage et cadrage seulement, la réalisation est estimée dans la PR de règles
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-019 — tableau.py : allocations par période et absence pour formation rattachée à un ticket

## Description
Ticket créé le 2026-11-27 à la demande d'Ethan, à partir de l'analyse des alertes de `TABLEAU.md` par le `chef-de-projet` (T-016, [planning.md](../planning.md) v1.0, [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md)).

**Constat.** Deux limites de `scripts/tableau.py` produisent de fausses alertes dans `esn-interne` depuis l'application de DEC-024 :
1. **Une seule allocation par projet.** Le champ `allocation` d'`equipe/membres/*.md` ne porte qu'une valeur par projet. DEC-024 décide pourtant une allocation en deux périodes (P1 du 2026-11-30 au 2026-12-18, P2 du 2026-12-21 au 2027-01-15). Le tableau projette donc P1 sur toute la durée : fin projetée au 2027-01-26 au lieu du 2027-01-14 avec P2 (fausse alerte S1-R11), Nadia en « surcharge » à 102,8 % (66,5 % en réalité), Léa à 43,3 % (64,4 % en réalité). Le coordinateur doit changer la valeur à la main le 2026-12-21, ce qui est un calcul manuel du type que R9 et DEC-023 cherchent à éviter.
2. **Absence pour formation non rattachée au ticket qu'elle sert.** EV-002 (Nadia, formation « supervision » du 2026-12-03) met sa capacité à 0 ce jour-là, ce qui est juste pour `reservation-coworking`. Mais le tableau place alors T-002, qui *est* cette formation, sur d'autres jours, et signale un chevauchement T-002 / EV-002 (alerte S1-R9) qui n'en est pas un.

**Attendu dans ce ticket (triage et cadrage du `chef-de-projet`).**
- Proposer le format :
  - des allocations datées dans les fiches d'équipe (par exemple, une liste de périodes `du`/`au`/`%` par projet, avec repli sur la valeur actuelle) ;
  - du rattachement d'un événement d'absence à un ticket (par exemple, un champ `ticket: esn-interne/T-NNN` sur l'événement, qui compte la journée sur ce ticket au lieu de l'exclure) ;
  - avec leur effet sur `templates/membre.md`, `equipe/calendrier.md`, `scripts/tableau.py`, `scripts/test_tableau.py`, `console.py` et les skills qui écrivent `equipe/` (`absence`, `arrivee-membre`, `depart-membre`, `revision-budget`).
- Exiger la compatibilité : **sortie inchangée** de `tableau.py` pour un dépôt sans allocation datée ni événement rattaché (test, et `diff` sur le dépôt), comme pour DEC-023.
- Estimer et proposer l'affectation de la réalisation (compétence `backend-python`, tests), en dehors des tickets client.
- Préparer le ticket `decision` « Modification de règle » `ATTENTE_HUMAIN` (R7, R10/R11 : modification de modèle, d'outil et de règle).

**À traiter par une PR de règles (R11)** : branche dédiée, fichier `DEC-NNN`, entrée dans `docs/CHANGELOG-REGLES.md`, revalidation humaine des documents touchés. Aucune modification de `tableau.py`, de `templates/` ni d'`equipe/` dans ce ticket.

**En attendant :** le coordinateur applique les allocations de P2 le 2026-12-21 (jalon de planning.md), et les alertes listées ci-dessus sont des artefacts connus (analyse dans planning.md).

## Critères d'acceptation
- [ ] La proposition est écrite dans ce ticket : format des allocations datées et du rattachement d'une absence à un ticket, fichiers touchés, règle de compatibilité (sortie inchangée sans les nouveaux champs), tests prévus.
- [ ] La réalisation est estimée (heures équivalent humain) et une affectation est proposée (`backend-python`), hors projet client.
- [ ] Un ticket `decision` « Modification de règle » est créé en `ATTENTE_HUMAIN` dans `projets/esn-interne/tickets/`, au format R7 (question, options, recommandation, impact).
- [ ] Aucune modification de `scripts/`, `templates/` ni `equipe/` dans ce ticket (R11).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (cadrage ; la réalisation sera relue dans la PR de règles)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 · agent:coordinateur · création à la demande d'Ethan (alertes de TABLEAU.md analysées par T-016, DEC-024) ; à traiter par une PR de règles (R11) · 0 h
