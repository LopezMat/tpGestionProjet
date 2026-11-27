---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-016
titre: Pilotage du plan de formation de l'ESN
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: suivi-budget (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-017]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-016 — Pilotage du plan de formation de l'ESN

## Description
Ticket « Pilotage » du projet interne (règles 14 et 16 du `chef-de-projet`) : le temps de suivi du `chef-de-projet` sur `esn-interne` y est compté, jamais dans le pilotage d'un projet client. Le travail de rédaction du plan initial est compté dans [T-001](T-001-plan-de-formation-initial.md).

Après DEC-024 ([T-017](T-017-decision-plan-formation-initial.md)) :
- passage des tickets non retenus en `ANNULE`, avec une ligne de journal qui cite DEC-024 ;
- suivi hebdomadaire jusqu'à l'échéance (skill `avancement`) : tickets `formation` en retard, utilisation des salariés (AF9), consommé comparé au budget de fonctionnement (S1-R11) ;
- signalement au coordinateur du passage de P1 à P2 des allocations, le 2026-12-21 ;
- mise à jour du registre des compétences à risque de `planning.md` à chaque retex, arrivée, départ ou détection AF10 (S1-R13), chaque mise à jour passant par un ticket `decision`.

**Estimation** : 3 h pour les options A et B (environ 0,5 h par semaine jusqu'au 2027-01-15) ; 2 h pour l'option C ; 1 h pour l'option D. Ré-estimée après DEC-024.

## Critères d'acceptation
- [ ] Les tickets non retenus par DEC-024 sont `ANNULE`, avec une ligne de journal qui cite la décision.
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
