---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-001
titre: Plan de formation initial de l'ESN
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 3            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut (TERMINE)
debut_le: 2026-11-27        # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-27      # facultatif : date du passage TERMINE
imputation: esn             # projet interne : toujours esn (R19)
imputation_decision:        # vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-001 — Plan de formation initial de l'ESN

## Description
Ticket de travail du `chef-de-projet` (même principe que CLAUDE.md R14), créé avec le projet interne par [DEC-023](../../../docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md). **À lancer seulement après la validation de DEC-023 (R4).**

Attendu, selon S1-R13 et la règle 16 du `chef-de-projet` :
1. **`projets/esn-interne/planning.md`** (template `planning.md`, `EN_REVUE`), qui contient le **registre des compétences à risque**, établi à partir d'`equipe/membres/*.md` : compétence absente, un seul titulaire au niveau `confirme` ou plus, ou titulaire sur le départ. Au minimum :
   - `documentation` : plus de titulaire après le départ de Hugo, le 2026-12-04 (DEC-021) ;
   - second relecteur `securite-applicative` : Karim est le seul titulaire, et le candidat prévu par l'ancien T-053 (Hugo) part (DEC-021) ;
   - revue humaine : Karim seul (DEC-021) ;
   - `sauvegarde-restauration` et `docker` : Nadia seule (DEC-019, DEC-021) ;
   - `relation-client` et `recette-fonctionnelle` : Claire seule ; `juridique` : absente (DEC-009 E) ;
   - formation « supervision » de Nadia, le 2026-12-03 (EV-002), qui attend son ticket.
2. **Tickets `formation` proposés** dans ce projet, un par besoin retenu dans la recommandation : compétence, niveau visé, salarié, modalité (binôme interne, autoformation, formation externe), estimation, déclencheur (`<slug>/T-NNN`, `EV-NNN` ou `DEC-NNN`). Ils sont en `A_FAIRE` et ne sont pas planifiables tant qu'aucune allocation n'existe.
3. **Ticket `decision` « Plan de formation initial »** en `ATTENTE_HUMAIN` (format R7 : question, options, recommandation, impact). Il couvre les points suivants :
   - le budget de fonctionnement (`budget_eur`) et l'échéance (`deadline`) de ce projet ;
   - les allocations proposées à `esn-interne` par salarié, avec la capacité restante sur `reservation-coworking` jusqu'au 2026-12-18 (Nadia est à 50 % et Karim à 20 % ; congés de Karim à partir du 2026-12-21, EV-003) ;
   - l'ordre de priorité des formations.

   La décision attendue est DEC-024.

Le temps de ce ticket est à la charge de l'ESN (R19), jamais du client.

## Critères d'acceptation
- [x] `projets/esn-interne/planning.md` existe, en `EN_REVUE`, avec le registre des compétences à risque (au minimum les 6 points ci-dessus).
- [x] Chaque besoin retenu a son ticket `formation` dans `projets/esn-interne/tickets/`, conforme à `creer-ticket` (compétence, niveau visé, salarié, modalité, estimation, déclencheur) ; aucun ticket `formation` n'est créé dans un projet client (S1-R6).
- [x] Un ticket `decision` « Plan de formation initial » est en `ATTENTE_HUMAIN`, avec `bloque_par`, les options chiffrées (coût au taux de chaque salarié), la recommandation, le budget de fonctionnement et l'échéance proposés.
- [x] Aucune modification d'`equipe/` (règle 13 du `chef-de-projet`) ; aucune allocation appliquée avant DEC-024.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 · agent:coordinateur · création avec le projet interne (DEC-023, PR de règles `regles/couts-esn-formation`) ; à lancer après la validation de DEC-023 · 0 h
- 2026-11-27 09:00 · agent:chef-de-projet · A_FAIRE → EN_COURS (DEC-023 `VALIDÉ`, R4) ; lecture d'`equipe/` (fiches, calendrier, agents), de DEC-009 E, DEC-019, DEC-020, DEC-021, DEC-023, S1, `reservation-coworking` (projet.md, planning.md v1.1, TABLEAU.md du 2026-11-27, T-103) · 0 h
- 2026-11-27 11:20 · agent:chef-de-projet · `planning.md` v0.1 (`EN_REVUE`) : registre de 17 compétences à risque (R-01 à R-17), plan proposé (option B), jalons, contrôle des allocations ≤ 100 % et de la capacité par période (P1 et P2) ; tickets `formation` T-002, T-003, T-004, T-006, T-008, T-010, T-012, T-013, T-015, tickets d'encadrement T-005, T-007, T-009, T-011, T-014, pilotage T-016 ; ticket `decision` T-017 en ATTENTE_HUMAIN (options A, B recommandée, C, D ; DEC-024 attendue) ; aucune écriture dans `equipe/` ni dans `projet.md` · 3 h
- 2026-11-27 11:25 · agent:chef-de-projet · `python scripts/tableau.py` lancé pour contrôle ; EN_COURS → EN_REVUE (conclusion par le coordinateur, R13). Dépassement de l'estimation (3 h passées pour 1,5 h) : registre plus large que les 6 points demandés, 4 options chiffrées par période · 0 h
- 2026-11-27 · agent:coordinateur · critères vérifiés (planning.md EN_REVUE, tickets formation T-002 à T-015 dans esn-interne, T-017 présenté en ATTENTE_HUMAIN et tranché par Ethan dans DEC-024 VALIDÉ, equipe/ intact avant la décision) ; EN_REVUE → TERMINE à la demande d'Ethan · 0 h
