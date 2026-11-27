---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-016
titre: Pilotage du plan de formation de l'ESN
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: suivi-budget (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné ; ré-estimé après DEC-024 (option B), voir Description
temps_passe_h: 1            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002] ; T-017 retiré le 2026-11-27 (DEC-024 VALIDÉ), voir Journal
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le: 2026-11-27        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-016 — Pilotage du plan de formation de l'ESN

## Description
Ticket « Pilotage » du projet interne (règles 14 et 16 du `chef-de-projet`) : le temps de suivi du `chef-de-projet` sur `esn-interne` y est compté, jamais dans le pilotage d'un projet client. Le travail de rédaction du plan initial est compté dans [T-001](T-001-plan-de-formation-initial.md).

Après DEC-024 ([T-017](T-017-decision-plan-formation-initial.md), [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md), option B) :
- passage des tickets non retenus en `ANNULE`, avec une ligne de journal qui cite DEC-024 (T-015) ;
- mise à jour de [planning.md](../planning.md) pour l'option B : plan, jalons, allocations P1/P2, enveloppe de frais externes (suivi manuel, critère 3 de [T-018](T-018-suivi-frais-externes.md)), analyse des alertes de `TABLEAU.md` ;
- suivi hebdomadaire jusqu'à l'échéance (skill `avancement`) : tickets `formation` en retard, utilisation des salariés (AF9), consommé comparé au budget de fonctionnement (S1-R11), mouvements de l'enveloppe de frais externes ;
- signalement au coordinateur du passage de P1 à P2 des allocations, le 2026-12-21, puis contrôle de la projection recalculée par `tableau.py` ;
- mise à jour du registre des compétences à risque de `planning.md` à chaque retex, arrivée, départ ou détection AF10 (S1-R13), chaque mise à jour passant par un ticket `decision`.

**Estimation : 3 h, maintenue pour l'option B** (c'est le chiffre de T-017 pour A et B, compté dans les 3 633,21 € de DEC-024) :
- 1 h le 2026-11-27 : application de DEC-024 (T-015 `ANNULE`, `planning.md` v0.2, analyse des 4 alertes de `TABLEAU.md` et projection P1/P2) ;
- 1,75 h de suivi hebdomadaire : 7 semaines du 2026-11-30 au 2027-01-15, environ 0,25 h chacune ;
- 0,25 h pour la bascule P1 → P2 du 2026-12-21 (contrôle de la projection, alertes qui doivent disparaître).

Un dépassement (ticket `decision` d'alerte S1-R11, mise à jour du registre) sera ré-estimé à ce moment, avec une ligne de journal.

## Critères d'acceptation
- [x] Les tickets non retenus par DEC-024 sont `ANNULE`, avec une ligne de journal qui cite la décision (T-015, le 2026-11-27).
- [ ] Une ligne de journal par intervention, avec le temps passé (heures équivalent humain).
- [ ] Un état du plan est donné au coordinateur au moins une fois par semaine jusqu'à l'échéance.
- [ ] Toute alerte S1-R11 (90 % du budget de fonctionnement, ou fin projetée après l'échéance) donne lieu à un ticket `decision` `ATTENTE_HUMAIN` avec au moins 2 scénarios chiffrés.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (pilotage)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:10 · agent:chef-de-projet · création (T-001, règle 16) ; démarre après DEC-024 (T-017) · 0 h
- 2026-11-27 14:00 · agent:chef-de-projet · A_FAIRE → EN_COURS (DEC-024 VALIDÉ, option B). `depend_de: [T-017]` retiré : la décision est prise, et T-017 attend ce ticket pour son critère 3 (cycle de fait) · 0 h
- 2026-11-27 14:00 · agent:chef-de-projet · T-015 → ANNULE (DEC-024, option B : conseil juridique externe au cas par cas) ; estimation maintenue à 3 h (détail en Description) · 0,1 h
- 2026-11-27 14:50 · agent:chef-de-projet · planning.md v0.2 (option B retenue, options A, C et D écartées, enveloppe de frais externes, analyse des 4 alertes de TABLEAU.md et projection P1/P2) ; tickets T-002 à T-014 marqués « retenus par DEC-024 » avec leur rang, fenêtres de T-010 à T-012 recalées sur P2 ; contrôle par tableau.py · 0,9 h
