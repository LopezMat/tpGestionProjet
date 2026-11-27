---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-026
titre: Page « Le bureau » — son court d'alerte BLOQUE / ATTENTE_HUMAIN (Replay, et attente d'un humain en Direct), coupé par défaut, Web Audio
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom> ; provisoire : la dérogation de périmètre de DEC-027 ne couvre pas ce ticket
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0             # non chiffré : Ethan le chiffrera plus tard (DEC-027) ; non planifié
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-025]          # ex. [T-001, T-002]
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

# T-026 — Son d'alerte de la page « Le bureau »

## Description
Ticket sorti de [T-025](T-025-ameliorations-page-le-bureau.md) par [DEC-027](../../../docs/decisions/2026-11-27-DEC-027-ameliorations-bureau.md) (en attente de validation) : le son ajoutait 1,5 h estimées et une question sur le mode Direct, et la marge sous le seuil de 90 % du budget d'`esn-interne` serait passée sous une heure. **Non planifié et non chiffré** : Ethan le chiffrera plus tard. Il ne commence pas avant ce chiffrage et l'accord humain (arrêt obligatoire), ni avant que T-025 soit `TERMINE` (même fichiers).

**Attendu.**
- **Replay** : un son court quand l'événement courant fait passer un ticket à `BLOQUE` ou à `ATTENTE_HUMAIN`. Il est joué seulement pendant la lecture ou au pas à pas, jamais quand on déplace le curseur ni quand le replay se reconstruit, et au plus une fois toutes les 2 s.
- **Direct (option a de DEC-027)** : le journal de DEC-018 ne contient aucun statut de ticket. Le son « attente » joue donc quand Claude Code attend un humain : événements `autorisation`, et `attente` avec `detail` `permission_prompt` ou `elicitation_dialog`. **Pas pour `idle_prompt`**, qui se déclenche à chaque fin de tour. Le son ne joue que pour les événements reçus en direct, jamais pour l'historique rejoué à la connexion.
- **Contraintes** :
  - coupé à chaque chargement ;
  - activé par un bouton (`aria-pressed`) ;
  - produit par Web Audio (`AudioContext` créé au clic, oscillateur et enveloppe, moins de 0,4 s, un son distinct pour BLOQUE et pour l'attente) ;
  - aucun fichier son, `data:audio`, `new Audio`, `fetch` ni requête réseau ;
  - la page reste utilisable hors ligne en `file://` (DEC-016 § 2).
- **Fichiers probables** : `scripts/bureau.py` (bouton, table des statuts qui déclenchent le son), `scripts/bureau.js`, `scripts/test_bureau.py`, `README.md`.

**Avant le début** :
1. chiffrage par Ethan ;
2. décision sur le périmètre de l'assigné : la dérogation de DEC-027 vaut pour T-025 seulement, et la règle 9 de `dev-frontend` limite ses écritures à `projets/<slug>/app/` ;
3. contrôle du projeté d'`esn-interne` sous 90 %.

## Critères d'acceptation
- [ ] Le son est coupé au chargement ; un bouton (`aria-pressed`) l'active et le coupe.
- [ ] Le son est produit par Web Audio (`AudioContext` créé au clic) : aucun `new Audio`, `data:audio`, fichier `.mp3`, `.wav` ou `.ogg`, ni `fetch` dans `bureau.js` (test statique).
- [ ] En Replay, le son joue sur un événement courant `BLOQUE` ou `ATTENTE_HUMAIN` pendant la lecture ou au pas à pas, jamais lors d'un déplacement du curseur ni de la reconstruction, au plus une fois toutes les 2 s.
- [ ] En Direct, le son joue sur `autorisation` et sur `attente` de type `permission_prompt` ou `elicitation_dialog` reçus en direct, jamais sur `idle_prompt` ni sur l'historique rejoué à la connexion ; la table des déclencheurs est définie dans `bureau.py` et testée.
- [ ] La page générée s'ouvre et fonctionne en `file://` sans réseau ; `test_bureau.py` et `node --check scripts/bureau.js` passent.
- [ ] La section « Le bureau » du `README.md` décrit le bouton Son.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:20 · agent:coordinateur · création (DEC-027 : son sorti de T-025, option a en Direct sans idle_prompt) ; non planifié, chiffrage par Ethan attendu · 0 h
