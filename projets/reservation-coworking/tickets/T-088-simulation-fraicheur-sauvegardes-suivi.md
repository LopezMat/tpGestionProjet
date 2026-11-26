---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-088
titre: SIMULATION — Contrôle de fraîcheur des sauvegardes dans le suivi de production (analyste-prod, R11)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: supervision (debutant)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-029]          # ex. [T-001, T-002]
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
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-4 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-088 — SIMULATION — Contrôle de fraîcheur des sauvegardes dans le suivi de production (analyste-prod, R11)

## Description
Proposition **P-4** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md), **cause 5**. Aucun contrôle ne vérifie qu'une sauvegarde récente existe. La sonde ne regarde que `/health`, l'`analyste-prod` ne regarde pas les sauvegardes, et les sauvegardes ne laissent aucune trace versionnée. En crise, la dernière sauvegarde n'a pu être établie qu'en lisant à la main un dossier hors Git.

**Attendu (modification de règle, R11)** : à chaque rapport de suivi, l'`analyste-prod` relève le nom de la sauvegarde quotidienne la plus récente, sans en lire le contenu. Le nom a le préfixe `AAAAMMJJ-HHMMSS`, fixé par [T-029](T-029-sauvegarde-quotidienne-limite-age.md). L'agent reporte une ligne « Sauvegarde » dans `rapports/suivi-*.md`, et il crée un ticket `incident` `haute` si la sauvegarde a plus de 26 h ou si le dossier est vide. Le rapport de suivi devient la trace versionnée qui a manqué pendant la crise.

Fichiers touchés : `.claude/agents/analyste-prod.md` et `templates/rapport-suivi.md` (responsable D). Ce sont des fichiers de règles et de modèles, hors du périmètre de tous les agents (C9). Il faut une PR, un fichier `DEC-NNN` et une entrée dans `docs/CHANGELOG-REGLES.md`.

**Points de conception à trancher dans la PR** :
- l'`analyste-prod` n'a qu'une commande Bash (la sonde) ; la lecture des noms de fichiers se ferait par Glob sur `deploiement/local/<slug>/sauvegardes-quotidiennes/` uniquement ;
- ce dossier voisine `db_password`, que l'agent ne doit jamais lire ; il faut écrire cette interdiction, et décider si une protection technique (hook) s'impose.

**Imputation à arbitrer (DEC-009, point D).** C'est une amélioration d'un agent de l'ESN, utile à tous les projets. Elle est de même nature que le lot R17 (T-050), que DEC-009 a sorti du projet client parce que « le client ne paie pas l'amélioration de nos outils internes ». Le ticket est créé ici parce que la règle 11 du `chef-de-projet` demande de tracer chaque amélioration d'agent par un ticket `amelioration`. Si un humain le sort du projet client, il passe `ANNULE` avec la mention « déplacé vers les règles de l'ESN (PR de règles) », comme T-050.

**Affectation : `salarie:nadia`, proposition du `gestionnaire-crise` conservée.**
- **Pourquoi pas un agent (AF6 écarté).** Une modification de règle se fait par un humain, par PR (R11).
- **Pourquoi Nadia.** C'est la seule salariée qui a `supervision`, au niveau `debutant`, qui est le niveau requis (AF7). Elle a aussi `sauvegarde-restauration` `confirme` : elle fixe le seuil de 26 h et le format du nom avec T-029.
- **Après sa formation « supervision » du 2026-12-03 (EV-002).** Ce n'est pas une condition (son niveau suffit), mais c'est préférable.
- **Charge.** La capacité de Nadia est dépassée ; ce ticket `normale` est le premier à décaler, ou à sortir du projet (voir [T-090](T-090-simulation-planning-sans-sauvegarde.md)).
- **Ticket salarié (AF11, R15)** : à faire par un humain.

**Dépendance** : `depend_de: [T-029]`, qui fixe le dossier et le format du nom des sauvegardes quotidiennes. **À réaliser avant le GO [T-046](T-046-go-mise-en-production.md)**, puisque la production n'existe pas encore (ajout à `depend_de` du GO à arbitrer, T-090).

**Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] Une règle et un contrôle sont ajoutés à `.claude/agents/analyste-prod.md` (lecture du seul nom du fichier le plus récent, interdiction de lire `db_password` et le contenu des sauvegardes), et une ligne « Sauvegarde » au modèle `templates/rapport-suivi.md`.
- [ ] Une décision `DEC-NNN` est créée et une entrée est ajoutée dans `docs/CHANGELOG-REGLES.md` (R11).
- [ ] Sur un rapport de suivi d'essai, une sauvegarde de plus de 26 h, ou un dossier vide, produit un ticket `incident` `haute`.
- [ ] La PR est acceptée par D ; la ligne « Revue humaine » ci-dessous est remplie ; le temps passé est noté.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (règle d'agent et modèle)
- **Commentaires** :
- **Revue humaine requise** : oui (modification d'une règle d'agent de supervision de la production, R11 ; accès en lecture à un dossier qui contient un secret). **Le ticket compagnon « Revue humaine T-088 » sera créé au triage, à la reprise du développement**, sauf si la PR R11 et sa décision humaine sont jugées suffisantes.
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-4 ; assignée à Nadia (seule salariée supervision) ; dépend de T-029 ; imputation client ou ESN à arbitrer (DEC-009, point D) ; non planifié (développement en pause) · 0 h
- 2026-11-26 18:45 · agent:chef-de-projet · SIMULATION · ANNULE : couvert par T-092 (vérification quotidienne de l'existence et de la restauration des sauvegardes, avec alerte et trace versionnée), créé à la demande d'Ethan (DEC-019, point 3.2). T-092 détecte aussi une sauvegarde de plus de 26 h, sans modification de règle d'agent ni accès d'un agent au dossier qui contient db_password. Une ligne « Sauvegarde » dans les rapports de suivi de tous les projets, si elle est encore voulue, relève de la PR de règles de l'ESN (DEC-009, point D). Le ticket compagnon « Revue humaine T-088 » n'est plus à créer · 0 h (temps compté dans T-008)
