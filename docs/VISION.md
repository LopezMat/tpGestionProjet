# VISION — ESN virtuelle orchestrée par des agents IA

> Document de référence du projet. Tous les agents et tous les membres de l'équipe s'y réfèrent.
> Il décrit **quoi** construire et **pourquoi**. Le **comment** est dans `CLAUDE.md`, `docs/ARCHITECTURE.md` et les fichiers d'agents.

---

## 1. Contexte

Nous sommes une équipe de 4 étudiants en Mastère « Manager de projets informatiques » (spécialité cybersécurité) à L'Idem.
Pendant une semaine (du lundi 23 au vendredi 27 novembre 2026, soutenance le vendredi), notre équipe joue une **ESN** (entreprise de services numériques). Les missions de l'ESN sont assurées par des systèmes d'agents IA configurés dans ce repo :

- **Claude Code** : le coordinateur et l'environnement d'exécution ;
- **subagents Claude Code** : les agents spécialisés.

**Notre produit n'est pas une application. C'est le système multi-agents.** Il doit pouvoir prendre en charge des projets clients très différents : site vitrine, e-commerce, API, application métier, modernisation d'un existant.
Le premier client de démonstration est une **plateforme de réservation**, volontairement minimale (2 ou 3 fonctionnalités). Elle sert à démontrer le système, elle n'est pas le produit.

---

## 2. Consigne du professeur : les 4 systèmes obligatoires

Chaque système est décrit dans des fichiers Markdown : rôles des agents, ordre des étapes, ce que chaque agent produit, contrôles à effectuer, moments où un humain doit décider. L'outil d'IA qui exécute ces règles est libre.

### Système 1 : la gestion de projet
- Découper un projet en tâches et organiser leur réalisation : répartition entre **agents ET salariés** (humains), ordre des tâches, durées.
- Contrôler le respect du budget et des délais.
- Identifier les besoins en formation des salariés et les améliorations à apporter aux agents IA.

### Système 2 : le suivi et la maintenance
- Assurer une veille technologique.
- Suivre les performances et les bugs de l'application, et transmettre ces informations à la gestion de projet après le déploiement.
- Suivre les remontées du support, c'est-à-dire les problèmes signalés par les utilisateurs finaux.
- Gérer une situation de crise : perte de données, coupure du serveur, intrusion.

### Système 3 : le déploiement automatisé
Avant toute mise en ligne, le système contrôle le code, directement par ses agents ou par des automatismes qu'ils déclenchent :
- les régressions ;
- la sécurité ;
- la mise en production effective : un push ne suffit pas, le système vérifie que l'application est bien en ligne et à jour.

### Système 4 : le cahier des charges
- Choisir le système d'information adapté à la demande du client.
- Rédiger le cahier des charges en tenant compte de cette demande, et en garantissant la qualité, la sécurité et la maintenance du code grâce aux trois systèmes précédents.

### Déroulé et évaluation
- Les 4 systèmes se construisent au fil de la semaine.
- **À tout moment, la situation peut changer** : budget revu, départ d'un membre de l'équipe, incident en production. Le système doit s'adapter, et ce sont les humains qui modifient ses règles.
- Le vendredi, chaque équipe présente son projet.
- Critères d'évaluation :
  1. **La configuration** : chaque règle est justifiée et répond à un besoin du projet.
  2. **Les livrables** : complets et cohérents entre eux.
  3. **La soutenance** : nous défendons nos choix.

---

## 3. Notre vision

### 3.1 Objectif
Pas 4 agents figés avec des prompts prédéfinis, mais une **architecture dynamique et évolutive**, capable de s'adapter à n'importe quelle demande client : comprendre le besoin, identifier les compétences nécessaires et organiser le travail.

### 3.2 Fonctionnement
Un **coordinateur** (la session principale Claude Code, pilotée par `CLAUDE.md`) choisit dans un **catalogue** les agents utiles, décide de l'ordre et organise le travail.

Pipeline type, **adapté à chaque projet et non figé** :
1. Réception de la demande client (contexte, besoins, contraintes).
2. Analyse du besoin et cahier des charges (système 4).
3. Gestion de projet : tickets, estimations, ressources, priorités (système 1).
4. Conception technique : agent architecte (technologies, architecture).
5. Développement : agents développeurs, en parallèle quand les tâches sont indépendantes.
6. Tests et cybersécurité : fonctionnalités, régressions, vulnérabilités (système 3).
7. Déploiement : préparation, mise en production, vérification en ligne (système 3).
8. Maintenance : incidents, bugs, support, veille (système 2).

Exemples d'adaptation :
- **Site vitrine** : peu d'agents, pas d'architecture complexe.
- **API** : priorité aux agents backend, architecture et sécurité.
- **E-commerce** : paiements, commandes, stocks et les tests associés.
- **Modernisation** : analyse de l'existant avant toute proposition d'architecture.

Les 4 systèmes du professeur forment le socle obligatoire. Nous ajoutons des agents spécialisés pour le compléter (analyste, architecte, développeurs, testeur, sécurité…).

### 3.3 Autonomie et supervision humaine
Le client fournit sa demande initiale et le système prend en charge le maximum de travail possible. **Restent soumis à validation humaine :**
- le cahier des charges ;
- le budget et les délais ;
- les choix techniques importants ;
- les actions sensibles sur les données ;
- la mise en production ;
- les événements d'équipe (arrivée, départ, congés, révision du budget).

Les agents doivent détecter leurs erreurs, demander de l'aide et se corriger quand c'est possible. **Un agent ne reste jamais bloqué en silence.**

### 3.4 Technologies
- GitHub : dépôt commun et gestion du code.
- Claude Code : coordinateur et exécution.
- Subagents Claude Code (`.claude/agents/*.md`) : agents spécialisés.
- Fichiers Markdown : rôles, instructions et règles.
- Skills (`.claude/skills/<nom>/SKILL.md`) : procédures réutilisables.
- Runbooks (`runbooks/`) : procédures de crise.
- Git et GitHub Actions : versions, tests, déploiements, régénération des tableaux de bord.

### 3.5 Méthodologie
**Notre méthode est un Kanban à portes de validation humaines, avec des livraisons incrémentales.** Ce n'est pas une méthode unique appliquée telle quelle. Nous avons combiné des méthodes reconnues, chacune là où elle répond à une exigence de la consigne. Le pipeline du § 3.2 en donne l'ordre, et les 4 systèmes en donnent le contenu.

| Méthode | Ce que nous en reprenons | Où c'est appliqué |
|---|---|---|
| **Kanban** | Flux tiré de tickets à travers des statuts (`A_FAIRE` → `EN_COURS` → `EN_REVUE` → `TERMINE`) ; un ticket n'est pris que si ses dépendances sont terminées ; blocages rendus visibles (`BLOQUE`, `ATTENTE_HUMAIN`) | § 5, [S1](systemes/S1-gestion-projet.md) (S1-R2, S1-R3, S1-R12), tableau Kanban de la console |
| **Agile, itératif et incrémental** | Livraison par incréments utilisables, avec un retour d'expérience en fin de jalon qui améliore les agents et les règles | DEC-011 (incrément de soutenance), `retex.md`, tickets `amelioration` (S1-R7) |
| **Portes de validation, inspirées du cycle en V** | Chaque étape de conception a sa vérification en face : le CDC est vérifié par la recette, l'architecture et le code par les tests et l'audit. On ne passe à l'étape suivante que sur une validation humaine. | § 3.3, [S3 § 3](systemes/S3-deploiement.md) (portes 1 à 8), R4, R16 |
| **MoSCoW** | Priorisation des exigences (Must, Should, Could, Won't) ; la recette est CONFORME si tous les Must sont OK | [S4](systemes/S4-cahier-des-charges.md) (S4-R2), S3-R9 |
| **Planification par dépendances (chemin critique, Gantt)** | Estimations en heures équivalent humain, dépendances entre tickets, date de fin projetée et Gantt calculés | S1 § 4 et § 7, `scripts/tableau.py` |
| **Suivi budgétaire à terminaison** | Coût consommé et coût projeté (consommé + reste à faire × taux), alerte à 90 % du budget ou en cas de dépassement de la deadline | S1-R11, R12, `TABLEAU.md` |
| **DevOps : intégration et déploiement continus** | Tests, audit de sécurité et contrôle des validations à chaque PR ; déploiement scripté, vérification du SHA en ligne, rollback testé | `.github/workflows/`, S3-R5 à S3-R7 |
| **Principe des quatre yeux** | L'auteur du code ne le valide jamais : relecteur, testeur, sécurité, puis un humain pour ce qui est critique ou touche la sécurité | S3-R1, S3-R2, R13 |
| **ADR (Architecture Decision Records)** | Chaque décision humaine est écrite avec son contexte, les options étudiées, la décision et le pourquoi | `docs/decisions/`, skill `tracer-decision` |
| **Gestion des incidents (ITIL, SRE)** | Qualification et triage des tickets bug, incident et support ; runbooks de crise ; post-mortem sans blâme | [S2](systemes/S2-maintenance.md) (S2-R1 à S2-R5), `runbooks/` |

*Pourquoi :* une semaine et des agents IA ne permettent pas de reproduire les cérémonies d'une méthode unique (sprints, réunions quotidiennes). Nous avons pris de chaque méthode la pratique qui répond à un besoin précis :
- Kanban pour suivre un flux de tickets réalisés en parallèle par des agents ;
- les portes de validation pour la supervision humaine exigée par la consigne ;
- l'incrémental pour livrer une démonstration avant la soutenance ;
- DevOps pour l'exigence « un push ne suffit pas » (S3).

#### Definition of Done
Un ticket est fini (`TERMINE`) quand les trois conditions suivantes sont réunies :
1. **Tous ses critères d'acceptation sont cochés** (S1-R4, R13). Chaque critère coché a sa preuve dans le journal du ticket : un test vert ou une vérification reproductible (règle 3 du [`testeur`](../.claude/agents/testeur.md)).
2. **Il a été vérifié par quelqu'un d'autre que son auteur** (R13, S3-R1) :
   - un ticket de réalisation : avis `relecteur-code` `APPROUVÉ`, ligne « Revue humaine » remplie si le ticket est critique ou touche la sécurité (S3-R2), suites de tests vertes ; c'est le `testeur` qui le passe `TERMINE` ;
   - un ticket de déploiement : le skill `verifier-prod` a constaté que `/health` renvoie le SHA attendu (S3-R5) ; c'est le `deployeur` qui le passe `TERMINE` ;
   - un ticket de travail d'un agent S3 : c'est le coordinateur qui le conclut, jamais l'agent ;
   - un ticket `salarie:` : c'est l'humain qui le porte (R15).
3. **Le passage à `TERMINE` est écrit dans le journal du ticket** : date et heure, qui, quoi, temps passé en heures équivalent humain (section « Journal » de [templates/ticket.md](../templates/ticket.md), R12).

Pour une **livraison**, la Definition of Done est celle des portes 1 à 8 de [S3](systemes/S3-deploiement.md) : tests, audit de sécurité, recette humaine CONFORME sur le SHA du GO (R16), GO humain (S3-R3), puis SHA en ligne confirmé par `verifier-prod`.

#### Équivalents des rituels
Nous n'avons pas de cérémonies à date fixe. Chaque rituel de Scrum a un équivalent, déclenché par le flux de tickets :

| Rituel | Notre équivalent | Quand | Où c'est écrit |
|---|---|---|---|
| **Point d'avancement** (mêlée quotidienne) | Skill `avancement` : `scripts/tableau.py` régénère `TABLEAU.md` et `PORTFOLIO.md`, puis le coordinateur présente l'avancement, le budget, les délais, les blocages et les attentes humaines. La CI régénère aussi les tableaux chaque jour. | Après chaque étape du pipeline, avant une décision, sur demande ; chaque jour à 6 h UTC pour la CI | [skill avancement](../.claude/skills/avancement/SKILL.md), [`tableau.yml`](../.github/workflows/tableau.yml), R9, S1-R11, S1-R12 |
| **Revue de fin d'incrément** (revue de sprint) | Recette humaine au regard du CDC par un salarié qui n'est pas l'auteur du code, puis ticket « GO mise en production » tranché par un humain | À chaque livraison, avant la mise en production | [skill recette](../.claude/skills/recette/SKILL.md), S3 porte 3 bis, S3-R9, R16, S3-R3 |
| **Rétrospective** | `retex.md` rédigé par le `chef-de-projet`, d'où sortent des tickets `amelioration` (agents, règles) et `formation` (salariés) ; après une crise, post-mortem sans blâme | En fin de jalon (étape 9 du pipeline, `CLAUDE.md` § 1) ; dans les 2 jours ouvrés après une crise | [templates/retex.md](../templates/retex.md), S1-R7, S2-R5 |

#### La méthode appliquée cette semaine
Les décisions de la semaine montrent la méthode en action. DEC-019 et DEC-020 sont des exercices simulés (marqués `SIMULATION`), mais traités par le circuit réel : tickets, agents, décision humaine tracée.
- **Incrément de soutenance** ([DEC-011](decisions/2026-11-25-DEC-011-increment-consultation-coworking.md)). Ethan a limité l'incrément au socle et à la consultation des disponibilités en lecture seule. Chaque ticket passe tout le circuit (développement, relecture, sécurité, tests). Au 2026-11-26, T-010, T-011, T-012 et T-054 sont `TERMINE` et T-055 est `EN_REVUE`. L'écart provisoire au CDC (F-04) a une condition : aucun GO tant que T-013 et T-020 ne protègent pas ces routes.
- **Arbitrage budgétaire avec effet sur le planning** ([DEC-020](decisions/2026-11-26-DEC-020-simulation-budget-4200.md)). Le budget passe de 6 000 à 4 200 € HT. F-06 est abandonné (T-027 `ANNULE`), le CDC et le planning passent en v1.1, validés sous DEC-020, et T-087, T-092 et T-078 deviennent des dépendances du GO (T-046). Au premier dépassement prévisible (le bug T-105, remonté par la recette), la condition 1 s'applique : arbitrage humain avant d'engager le correctif (T-106).
- **Post-mortem sans blâme** ([DEC-019](decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md), [post-mortem](../projets/reservation-coworking/rapports/post-mortem-2026-11-26-perte-donnees.md)). Après la perte de la base, le post-mortem cherche ce qui a permis l'erreur, pas un coupable. Leçon : « une règle sans preuve d'exécution n'est pas une garantie ». Les actions correctives deviennent des tickets `amelioration` (T-085, T-086, T-087, T-092), et T-029 (sauvegarde quotidienne) passe `critique` et devient une dépendance du GO.
- **Boucle d'amélioration : incident → règle → garde-fou.** Le 2026-11-24, [DEC-007](decisions/2026-11-24-DEC-007-choix-techniques-coworking.md), `VALIDÉ`, est modifié par un script lancé par Bash. `verifier_validations.py` le détecte après coup et l'incident est noté dans le `retex.md`. [DEC-010](decisions/2026-11-24-DEC-010-principe-r17.md) adopte la règle R17 sur le principe. [DEC-015](decisions/2026-11-26-DEC-015-regle-r17.md) l'écrit dans `CLAUDE.md` et la fait appliquer par le hook `restreindre_bash.py` (garde-fou 9 d'[ARCHITECTURE § 6](ARCHITECTURE.md)), avec un test qui rejoue l'incident.

---

## 4. Contraintes et conventions d'architecture

- **Seul le coordinateur orchestre.** Les subagents ne peuvent pas lancer d'autres subagents. Si un besoin n'est couvert par aucun agent du catalogue, le coordinateur propose un nouveau fichier d'agent, qu'un humain valide.
- **Les agents communiquent uniquement par les fichiers qu'ils produisent.** Chaque livrable suit un template (`templates/`).
- **Statuts des documents**, dans l'en-tête : `BROUILLON`, `EN_REVUE` ou `VALIDÉ`. Seul un humain passe un document à `VALIDÉ`. Un agent refuse de travailler à partir d'une entrée non validée quand une validation est requise.
- **Chaque règle s'écrit sous la forme « Règle » + « Pourquoi : … »**, pour qu'elle soit justifiable à l'oral.
- **Les validations humaines sont aussi appliquées techniquement** dans `.claude/settings.json` (permissions `ask`/`deny`, par exemple sur `git push`, les suppressions et les fichiers `.env`).
- **Toute décision humaine est tracée** dans `docs/decisions/` (date, décision, auteur, justification).

---

## 5. Système de ticketing par projet

Outil central du système 1, utilisé par tous les systèmes.

### 5.1 Principe
- Les agents sont communs à l'ESN. **Chaque projet client a son propre espace** : `projets/<slug-client>/`, par exemple `projets/vitrine-boulangerie/` ou `projets/reservation-salle/`.
- Les tickets sont des fichiers Markdown, **source de vérité unique** de l'avancement.
- Les tableaux de bord sont **générés** à partir des tickets. Personne ne les modifie à la main.

### 5.2 Structure d'un projet
```
projets/<slug>/
├── projet.md        # fiche : client, type, budget, deadline, statut, agents mobilisés, salariés affectés
├── cdc.md           # cahier des charges
├── planning.md
├── tickets/
│   └── T-001-<titre-court>.md
└── TABLEAU.md       # généré automatiquement
PORTFOLIO.md         # à la racine, généré : vue de tous les projets en cours
```

### 5.3 Format d'un ticket (frontmatter YAML + corps)
- `id`, `titre`, `projet`
- `type` : fonctionnalite | tache | bug | incident | support | decision | formation
- `statut` : A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
- `priorite` : critique | haute | normale | basse
- `assigne` : `agent:<nom>` ou `salarie:<prenom>`
- `estimation_h`, `temps_passe_h`
- `depend_de` : liste d'id
- `bloque_par` : texte, obligatoire si le statut est BLOQUE ou ATTENTE_HUMAIN
- `validation_humaine_requise` : oui/non
- `cree_par`, `cree_le`, `maj_le`

Corps : Description, Critères d'acceptation (cases à cocher), Journal (une ligne horodatée par action : qui, quoi, temps passé).

### 5.4 Règles du ticketing
- Le chef de projet crée les tickets à partir du CDC `VALIDÉ`, avec une estimation, des dépendances et un assigné.
- Les agents de maintenance et de support (système 2) créent des tickets bug, incident ou support. Le chef de projet les trie : priorité et assignation.
- Un agent ne prend un ticket que si toutes ses dépendances sont TERMINE. Il passe alors le ticket EN_COURS et note son temps dans le journal.
- Un agent bloqué passe le ticket BLOQUE et explique pourquoi.
- Toute validation humaine passe par un ticket ATTENTE_HUMAIN. Seul un humain le débloque, et la décision est tracée dans `docs/decisions/`.
- Un ticket passe TERMINE seulement si tous les critères d'acceptation sont cochés. Pour un déploiement, la vérification en ligne doit aussi être faite.
- Si aucun salarié n'a la compétence requise pour un ticket, le chef de projet crée un ticket de type formation.

### 5.5 Tableau de bord généré
Le script `scripts/tableau.py` (Python, sans dépendance lourde) génère `TABLEAU.md` pour chaque projet, plus `PORTFOLIO.md` :
- **Avancement** : % basé sur les heures estimées des tickets TERMINE, plus le nombre de tickets par statut.
- **Temps restant** : somme des estimations restantes, moins le temps déjà passé. Date de fin projetée selon la capacité réelle de l'équipe. Écart avec la deadline.
- **Budget** : consommé vs prévu (heures × coût, agent ou salarié).
- **Points bloquants** : tickets BLOQUE, avec leur raison et leur ancienneté.
- **Interventions humaines requises** : tickets ATTENTE_HUMAIN, triés par priorité.
- **Alertes** : deadline dépassée en projection, budget > 90 %, ticket critique ouvert, ticket EN_COURS sans mise à jour depuis longtemps.
- **Capacité de l'équipe** et événements à venir (congés, départs, arrivées).
- **Gantt Mermaid** des tickets, d'après les dépendances et les estimations.

Skills associés : `creer-ticket` (garantit le format) et `avancement` (lance le script et résume la situation). Une GitHub Action (`tableau.yml`) régénère les tableaux chaque jour à 6 h UTC, et à la demande.

---

## 6. Gestion de l'équipe de l'ESN

L'ESN a une équipe vivante : des membres arrivent, partent, prennent des congés, et les budgets changent. Le système gère ces événements et recalcule automatiquement plannings, tickets et prévisions.

### 6.1 Données
- `equipe/membres/<prenom>.md`, un fichier par salarié :
  - rôle ;
  - compétences avec un niveau (débutant / confirmé / expert) ;
  - coût journalier ;
  - capacité (heures par semaine) ;
  - statut : actif | conges | depart_prevu | parti | en_integration ;
  - date d'arrivée et date de départ éventuelle ;
  - projets affectés.
- `equipe/agents.md` : les agents IA, avec leurs compétences et un coût estimé.
- `equipe/calendrier.md` : absences et événements à venir.
- La capacité réelle est calculée à partir du calendrier. Un membre en congé a une capacité nulle sur la période.

### 6.2 Événements (un skill par événement)
- **Arrivée** (`arrivee-membre`) : créer la fiche, puis des tickets d'intégration et de formation. Affecter progressivement des tickets adaptés à son niveau.
- **Départ** (`depart-membre`) : préparer un plan de passation **avant** la date de départ. Ce plan contient la liste de ses tickets et connaissances, des tickets de transfert (documentation, binôme), la réaffectation selon les compétences, et le recalcul du planning. Si aucune compétence équivalente n'existe dans l'équipe : ticket formation ou recrutement.
- **Congés / absence** (`absence`) : vérifier l'impact sur les tickets de la période. Réaffecter ou décaler, puis recalculer la date de fin projetée. Alerte si un ticket critique ou une deadline est touché.
- **Budget revu** (`revision-budget`) : recalculer la projection, proposer des scénarios (retirer des fonctionnalités, réaffecter, décaler) et créer un ticket ATTENTE_HUMAIN pour l'arbitrage.

### 6.3 Règles
- Chaque événement est une **décision humaine** : l'agent prépare l'analyse d'impact et la proposition, un humain valide, et la décision est tracée dans `docs/decisions/`.
- Un salarié ne peut pas être affecté à un ticket qui tombe pendant son absence.
- Un départ déclenche la passation au moins X jours avant (X à définir et à justifier).

---

## 7. Répartition de l'équipe (vraie équipe étudiante)

| Personne | Système | Périmètre |
|---|---|---|
| **A** | 4 · Cahier des charges | Analyste-besoin, architecte, développeurs, templates CDC et choix techniques |
| **B** | 1 · Gestion de projet + coordinateur | `CLAUDE.md`, chef de projet, ticketing, tableaux de bord, équipe et événements, budget, formation |
| **C** | 3 · Déploiement | Testeur, sécurité, déployeur, `settings.json`, GitHub Actions, vérification post-déploiement |
| **D** | 2 · Maintenance | Veille, monitoring et bugs, support, runbooks de crise, circuit des tickets bug/incident/support |

Chaque fichier indique son responsable.

---

## 8. Objectif final

Donner une demande client à Claude Code et voir le coordinateur :
1. analyser le besoin ;
2. sélectionner les agents adaptés ;
3. créer et suivre les tickets ;
4. faire réaliser le développement ;
5. contrôler les résultats ;
6. s'arrêter aux validations humaines ;
7. préparer la livraison ;
8. s'adapter aux changements (équipe, budget, incident).

**En résumé : une ESN virtuelle orchestrée par l'IA, qui s'adapte à chaque projet au lieu de suivre un scénario prédéfini.**
