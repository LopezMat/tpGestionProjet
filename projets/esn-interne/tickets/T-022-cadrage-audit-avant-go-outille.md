---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-022
titre: Cadrage « Audit avant GO outillé » (action A7, DEC-025) — préparation de la PR de règles (R11)
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: planification (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné ; cadrage seulement, la réalisation (2 h) est estimée en Description
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

# T-022 — Cadrage « Audit avant GO outillé » (action A7, DEC-025)

## Description
Ticket créé en application de [DEC-025](../../../docs/decisions/2026-11-27-DEC-025-actions-retrospective-semaine.md) (option 2, action **A7**, priorité **haute**), à partir du constat **P7** du [retex de l'ESN](../retex.md) : les 7 audits de `reservation-coworking/T-043` ont été faits sans `pip-audit`, `bandit` ni `gitleaks` (absents du poste), la revue des dépendances s'est faite à la main (OSV), et `.github/workflows/securite.yml` ne lance `bandit` que sur `scripts` et `.claude`, pas sur `projets/*/app`.

**Échéance.** La réalisation qui découle de ce cadrage doit être `TERMINE` **avant l'audit avant GO de `reservation-coworking`** : ticket `tache` « Audit sécurité avant GO » (`agent:securite`, 5 h, au client) créé dans ce projet en application de [DEC-026](../../../docs/decisions/2026-11-27-DEC-026-audit-securite-increments-esn.md) ([reservation-coworking/T-108](../../reservation-coworking/tickets/T-108-audit-securite-avant-go.md)), à tenir avant la recette du 2026-12-10, pour un GO le 2026-12-15. **Si ce ticket, ou le ticket de réalisation qui en découlera, n'est pas `TERMINE` à temps, l'« Audit sécurité avant GO » passe `BLOQUE`** avec `bloque_par: amelioration esn-interne/T-022` (ou l'id du ticket de réalisation), comme le prévoit DEC-026 (Impacts) : `depend_de` ne traverse pas les projets.

**Attendu (cadrage du `chef-de-projet`).**
1. Comparer les options de DEC-025 pour que l'agent `securite` dispose des résultats des outils sur le **SHA candidat** au GO :
   - **(a) lecture des résultats de `securite.yml`** sur le SHA candidat : commande en lecture seule ajoutée à la liste blanche de l'agent `securite` dans `.claude/hooks/restreindre_bash.py` (forme exacte de la commande, refus de toute variante d'écriture, tests dans `scripts/test_restreindre_bash.py`), et rapports des outils publiés par le workflow sous une forme lisible (artefact ou résumé). Variante sans liste blanche : rapport de l'exécution CI joint par le coordinateur au ticket d'audit ;
   - **(b) outils installés sur le poste** (`pip-audit`, `bandit`, `gitleaks`) : qui installe, avec quelles versions, comment l'agent vérifie leur présence, et la reproductibilité d'un poste à l'autre ;
   - pour chaque option : fichiers touchés (`.github/workflows/securite.yml`, `.claude/agents/securite.md`, `.claude/hooks/restreindre_bash.py`), effet sur les garde-fous (ARCHITECTURE § 6), coût en h et €, délai, risques (élargissement de la liste blanche d'un agent, secrets dans les journaux de CI).
2. Spécifier l'**extension de `bandit` à `projets/*/app`** dans `securite.yml` : périmètre, seuil de sévérité, exclusions éventuelles, et effet attendu sur la CI actuelle (constats existants qui feraient échouer le workflow).
3. Recommander une option et **estimer la réalisation** : **2 h** prévus par DEC-025 (`agent:dev-backend`, compétence `backend-python`), relecture humaine par **C** (hooks et workflows, S3-R2) dans la PR de règles. Tout écart avec les 2 h est chiffré, avec son effet sur le seuil S1-R11 d'`esn-interne` (3 924 €).
4. Préparer le ticket `decision` « Modification de règle » `ATTENTE_HUMAIN` (R7, R11), qui fixe une date limite de réalisation antérieure au début de l'audit avant GO.

**Hors périmètre (R11).** Aucune modification de `.github/`, de `.claude/` ni de `scripts/` dans ce ticket : il prépare la PR de règles (branche dédiée, fichier `DEC-NNN` avec `modifie_une_regle: oui`, lignes de `docs/CHANGELOG-REGLES.md`, revalidation humaine des documents touchés).

## Critères d'acceptation
- [ ] Les options (a) lecture des résultats de `securite.yml` sur le SHA candidat (liste blanche ou rapport joint) et (b) outils installés sur le poste sont comparées dans ce ticket : fichiers touchés, effet sur la liste blanche de `restreindre_bash.py`, coût (h et €), délai, risques.
- [ ] L'extension de `bandit` à `projets/*/app` est spécifiée : commande proposée pour `securite.yml`, seuil de sévérité, exclusions, effet attendu sur la CI actuelle.
- [ ] Une option est recommandée ; la réalisation est estimée en heures équivalent humain (référence : 2 h, DEC-025) et affectée (`agent:dev-backend`, relecture humaine C) ; tout écart est chiffré avec son effet sur le seuil de 3 924 €.
- [ ] Un ticket `decision` « Modification de règle » est créé en `ATTENTE_HUMAIN` dans `projets/esn-interne/tickets/`, au format R7 (question, options, recommandation, impact), avec une date limite de réalisation antérieure au début de l'« Audit sécurité avant GO » de `reservation-coworking`.
- [ ] Aucune modification de `.github/`, `.claude/` ni `scripts/` dans ce ticket (R11).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (cadrage ; la réalisation sera relue dans la PR de règles)
- **Commentaires** :
- **Revue humaine requise** : non pour ce cadrage (aucun code) ; la réalisation touche la sécurité (hook, workflow) : revue humaine par C dans la PR de règles (S3-R2)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:52 · agent:chef-de-projet · création (DEC-025, action A7, priorité haute) ; échéance liée à l'audit avant GO de reservation-coworking (DEC-026) · 0 h
