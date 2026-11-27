---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-023
titre: Préparation de la PR de règles A2-A3-A4 (DEC-025) — skill tracer-decision et procédure du registre des décisions (R11)
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné ; A2 0,5 + A3 0,5 + A4 0,5 (DEC-025)
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
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

# T-023 — Préparation de la PR de règles A2-A3-A4 (DEC-025)

## Description
Ticket créé en application de [DEC-025](../../../docs/decisions/2026-11-27-DEC-025-actions-retrospective-semaine.md) (option 2), qui regroupe les actions **A2**, **A3** et **A4** dans **une seule PR de règles** sur `.claude/skills/tracer-decision/SKILL.md` et la procédure de `docs/decisions/README.md`. Constats d'origine dans le [retex de l'ESN](../retex.md) : P5 (A2), P4 (A3), P1 (A4).

**Contenu retenu par DEC-025.**
- **A2** (P5, priorité normale) : à la clôture d'un ticket `decision`, le temps du porteur est noté dans `temps_passe_h` (heures équivalent humain) ; 0 seulement s'il est assumé, avec une ligne de journal. Aucune correction rétroactive des 9 tickets déjà clos à 0 h, sauf si un porteur a réellement passé du temps (R15, DEC-023).
- **A3** (P4, priorité basse) : plus de bandeau d'état (« En attente de validation humaine ») dans le corps d'un document : l'en-tête fait foi (R3). Le bandeau est remplacé par une ligne neutre (« Rédigé par le coordinateur le … à partir de … ») ; le registre reçoit la phrase « en cas d'écart, l'en-tête fait foi ». **Les 21 fichiers DEC existants ne sont pas modifiés.**
- **A4** (P1, priorité normale) : la validation se fait dans la PR du contenu, avant son merge, après le message de fin de l'agent (rubrique « Produit »), avec un message de commit `validation: DEC-NNN <document>`. L'option « `validations.yml` obligatoire avant le merge sur `main` » est un réglage GitHub, non chiffré, signalé à un humain.

**Attendu (préparation du `chef-de-projet`).**
1. Le texte proposé, avant / après, de chaque modification : `tracer-decision` (étapes 3 et 6) et procédure de `docs/decisions/README.md` (étape 6 « Commit dans une PR »).
2. Les lignes proposées de `docs/CHANGELOG-REGLES.md` et la liste des documents à revalider.
3. La cohérence avec A1 ([T-019](T-019-tableau-allocations-par-periode.md)) : l'anomalie (b) de `tableau.py` signale un ticket `decision` `TERMINE` à 0 h ; la façon de distinguer un 0 h assumé (A2) d'un oubli est convenue avec le cadrage de T-019.
4. Le ticket `decision` « Modification de règle » `ATTENTE_HUMAIN` (R7, R11). La PR elle-même est faite par le coordinateur (DEC-025, assigné proposé), relue par B.

**Hors périmètre (R11).** Aucune modification de `.claude/` ni de `docs/` dans ce ticket : il prépare la PR de règles (branche dédiée, fichier `DEC-NNN` avec `modifie_une_regle: oui`, lignes du changelog, revalidation humaine des documents touchés).

## Critères d'acceptation
- [ ] Le texte proposé (avant / après) pour A2, A3 et A4 est écrit dans ce ticket, pour `.claude/skills/tracer-decision/SKILL.md` (étapes 3 et 6) et `docs/decisions/README.md` (procédure, étape 6).
- [ ] La liste des fichiers touchés par la PR se limite à ces deux documents et à `docs/CHANGELOG-REGLES.md` ; aucun des 21 fichiers DEC existants n'y figure (A3).
- [ ] Les lignes proposées de `docs/CHANGELOG-REGLES.md` (une par règle touchée) et la liste des documents à revalider sont écrites dans ce ticket.
- [ ] La règle de distinction entre 0 h assumé (A2) et oubli est notée dans ce ticket et dans T-019 (anomalie (b) d'A1).
- [ ] Un ticket `decision` « Modification de règle » est créé en `ATTENTE_HUMAIN` dans `projets/esn-interne/tickets/`, au format R7 (question, options, recommandation, impact).
- [ ] Aucune modification de `.claude/` ni de `docs/` dans ce ticket (R11).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (préparation de règles ; relecture humaine par B dans la PR)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:54 · agent:chef-de-projet · création (DEC-025, actions A2, A3 et A4 regroupées dans une PR de règles) · 0 h
