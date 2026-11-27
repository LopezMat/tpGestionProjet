---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-027
titre: Page « Le bureau » — info-bulle non rafraîchie en Replay souris immobile, « Dernier outil » non remis à zéro en Direct (remarques de revue de T-025)
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: basse             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom> ; provisoire : la dérogation de périmètre de DEC-027 ne couvre que T-025
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0             # non chiffré : à chiffrer par Ethan ; non planifié
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

# T-027 — Remarques de revue de T-025 sur l'info-bulle de « Le bureau »

## Description
Ticket créé à la demande d'Ethan (2026-11-27) à partir des remarques non bloquantes 1 et 2 du `relecteur-code` sur [T-025](T-025-ameliorations-page-le-bureau.md) (section « Revue »), livré par la PR #27. Le `testeur` les a jugées sans écart aux critères de T-025. **Non planifié et non chiffré** : il ne commence pas avant le chiffrage, l'accord d'Ethan et une décision sur le périmètre de l'assigné. La dérogation de DEC-027, qui autorise `dev-frontend` à écrire dans `scripts/`, vaut pour T-025 seulement.

**Remarque 1 : info-bulle non rafraîchie en Replay quand la souris reste immobile.** Dans `scripts/bureau.js` (vers la ligne 789, commit `9d4697a`), `afficherInfobulle` ne remplit l'info-bulle que si `id !== infoId`. Pendant la lecture du Replay, ou à l'arrivée d'un événement Direct, l'état du personnage survolé change sans que le contenu de l'info-bulle suive. Le relecteur propose deux pistes :
- réinitialiser `infoId` (ou rafraîchir le contenu) quand l'état du personnage survolé change ;
- accepter la limite et la noter dans le README.

**Remarque 2 : « Dernier outil » non remis à zéro en Direct.** Dans `scripts/bureau.js` (vers les lignes 962 et 1132), `p.dernierDirect` n'est pas remis à zéro dans `entrerDirect`. Quand on revient en Direct, l'info-bulle peut afficher le dernier outil d'une session précédente. Aucune fuite DEC-018 n'en résulte, puisque seuls des champs de la liste blanche sont affichés, mais le libellé est trompeur.

**Fichiers probables** : `scripts/bureau.js`, `scripts/test_bureau.py`, et éventuellement la section « Le bureau » de `README.md`.

## Critères d'acceptation
- [ ] En Replay, la souris restant immobile sur un personnage pendant la lecture, l'info-bulle affiche le dernier événement de ce personnage après chaque événement qui le concerne (vérifié en exécution, par exemple avec Edge headless).
- [ ] À l'entrée en mode Direct, aucun personnage n'affiche de « Dernier outil » antérieur à cette entrée (`dernierDirect` remis à zéro dans `entrerDirect`, vérifié par un test).
- [ ] L'info-bulle Direct ne lit toujours que les champs de la liste blanche (`acteur`, `outil`, `categorie`, `detail`, `ts`) : le test existant reste vert.
- [ ] `python scripts/test_bureau.py`, `test_console.py`, `test_bureau_direct.py`, `test_journal_direct.py` et `node --check scripts/bureau.js` passent.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:57 · agent:coordinateur · création (demande d'Ethan : remarques 1 et 2 de la revue de T-025) ; non planifié, chiffrage par Ethan attendu · 0 h
