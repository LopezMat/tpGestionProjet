---
titre: Système 1 — Gestion de projet
statut: VALIDÉ
responsable: B
version: 1.1
maj_le: 2026-11-24
valide_par: Ethan
decision: DEC-002
---

# Système 1 — Gestion de projet

## 1. Objectifs (consigne)
- Découper un projet en tâches et organiser leur réalisation : répartition entre **agents et salariés**, ordre des tâches, durées.
- Contrôler le respect du budget et des délais.
- Identifier les besoins en formation des salariés et les améliorations à apporter aux agents IA.

## 2. Acteurs
| Acteur | Rôle dans S1 |
|---|---|
| `chef-de-projet` (agent) | découpage, estimation, assignation, triage, suivi, analyse d'impact des événements, retour d'expérience |
| Coordinateur | lance le chef de projet aux bons moments, présente les arbitrages |
| Humains (B en premier lieu) | valident le planning, le budget, les arbitrages et les événements d'équipe |
| `scripts/tableau.py` (D) | calcule l'avancement, les projections et les alertes |

## 3. Entrées et sorties
- **Entrées** : `cdc.md` et `architecture.md` **VALIDÉS** ; `equipe/membres/*.md`, `equipe/agents.md`, `equipe/calendrier.md` ; tickets existants ; `retex.md`.
- **Sorties** : `tickets/T-NNN-*.md`, `planning.md`, mises à jour de `projet.md`, `TABLEAU.md` et `PORTFOLIO.md` (générés), `retex.md`, tickets `formation` et `amelioration`.

## 4. Étapes
1. **Découpage.** À partir du CDC VALIDÉ, une fonctionnalité donne un ou plusieurs tickets, chacun avec des critères d'acceptation vérifiables.
2. **Estimation** en heures équivalent humain (R12), avec les dépendances (`depend_de`).
3. **Assignation** à un agent ou à un salarié selon les compétences, le niveau, l'allocation et le calendrier. La compétence requise est portée par le champ `competence_requise` du ticket. Les critères d'affectation, appliqués dans l'ordre (le premier qui s'applique décide), sont détaillés avec leur Pourquoi dans [chef-de-projet.md](../../.claude/agents/chef-de-projet.md) :
   - **AF1** contact client → salarié `relation-client` (au moins `confirme`) ;
   - **AF2** ticket `decision` → porteur salarié ; la validation formelle reste humaine (R5) ;
   - **AF3** revue humaine (S3-R2) → ticket « Revue humaine T-NNN » assigné à un salarié compétent qui n'est pas l'auteur ;
   - **AF4** compétence hors périmètre des agents → salarié qui la possède, sinon ticket `formation` ;
   - **AF5** ticket `critique` → binôme agent + salarié `expert` ou `confirme` ;
   - **AF6** par défaut → agent ;
   - **AF7** niveau au moins égal au niveau requis, sinon binôme et ticket `formation` ; jamais de `critique` pour un `debutant` ou un salarié `en_integration` ;
   - **AF8** disponibilité : allocation > 0, pas d'absence sur la fenêtre (S1-R9), pas après le départ ;
   - **AF9** utilisation des salariés : un indicateur (alerte sous 50 %), jamais une obligation ;
   - **AF10** détection des besoins de formation (compétence absente, dépendance à une seule personne, affectation sous le niveau) ;
   - **AF11** ticket salarié = responsabilité humaine (CLAUDE.md R15).
4. **Planification.** `planning.md` contient les jalons et les hypothèses de capacité ; le Gantt est généré par `tableau.py`.
5. **Arrêt humain** : ticket `ATTENTE_HUMAIN` « Validation budget et délais ».
6. **Suivi** à chaque étape du pipeline : `tableau.py` puis synthèse (skill [avancement](../../.claude/skills/avancement/SKILL.md)).
7. **Triage** des tickets créés par S2 et S3 (bug, incident, support, amelioration) : priorité et assignation.
8. **Retour d'expérience** en fin de jalon ou de projet : `retex.md`, puis tickets `amelioration` (agents) et `formation` (salariés).

## 5. Règles du ticketing

**S1-R1 · Le chef de projet crée les tickets uniquement à partir d'un CDC `VALIDÉ`**, avec une estimation, des dépendances et un assigné.
*Pourquoi :* découper un besoin non validé, c'est planifier du travail potentiellement inutile.

**S1-R2 · Un ticket n'est pris que si toutes ses dépendances sont `TERMINE`.** L'agent ou le salarié le passe alors `EN_COURS` et note son temps dans le journal.
*Pourquoi :* l'ordre des tâches est respecté, et le temps passé est mesuré pour le budget.

**S1-R3 · `bloque_par` est obligatoire en `BLOQUE` et en `ATTENTE_HUMAIN`.**
*Pourquoi :* un blocage sans raison ne peut être levé par personne.

**S1-R4 · Un ticket ne passe `TERMINE` que si tous ses critères d'acceptation sont cochés** (et, pour un déploiement, après vérification en ligne : R13).
*Pourquoi :* « terminé » doit vouloir dire « vérifié ».

**S1-R5 · Les tickets bug, incident et support créés par S2 sont triés par le chef de projet** avant toute réalisation, sauf les incidents `critique`, que le `gestionnaire-crise` traite immédiatement.
*Pourquoi :* priorité et assignation restent cohérentes avec le planning, sans retarder une crise.

**S1-R6 · Si aucun salarié n'a la compétence requise, le chef de projet crée un ticket `formation`.**
*Pourquoi :* la consigne demande d'identifier les besoins en formation ; on les rend visibles et chiffrés.

**S1-R7 · Les améliorations d'agents passent par des tickets `amelioration`**, issus du `retex.md` ou des incidents, avant toute modification d'un fichier d'agent (R11).
*Pourquoi :* la consigne demande d'identifier les améliorations des agents ; un ticket les trace, les chiffre et les soumet à validation.

## 6. Événements d'équipe et de budget

Chaque événement suit la même séquence, telle que les skills l'appliquent :
1. **le coordinateur crée le ticket `decision`** (`A_FAIRE`, assigné à `agent:chef-de-projet`) ;
2. **le chef de projet y écrit l'analyse d'impact et sa proposition**, puis le passe `ATTENTE_HUMAIN` ;
3. **un humain décide**, et la décision est tracée dans `docs/decisions/` (skill `tracer-decision`) ;
4. **le coordinateur applique les changements d'`equipe/`** après la décision ; il est le seul à écrire dans `equipe/`.

*Pourquoi :* le coordinateur crée bien le ticket (texte initial de S1), l'analyse circule par fichier (R2) et le temps du chef est compté dans le ticket ; personne ne modifie l'équipe avant la décision humaine.

| Événement | Skill | Traitement |
|---|---|---|
| Arrivée | [`arrivee-membre`](../../.claude/skills/arrivee-membre/SKILL.md) | crée la fiche (`statut: en_integration`), ajoute des tickets d'intégration et de formation, puis affecte progressivement des tickets adaptés au niveau |
| Départ | [`depart-membre`](../../.claude/skills/depart-membre/SKILL.md) | plan de passation **au moins 5 jours ouvrés avant** le départ : tickets et connaissances du partant, tickets de transfert (documentation, binôme), réaffectation selon les compétences, recalcul du planning ; si la compétence manque, ticket formation ou recrutement |
| Absence | [`absence`](../../.claude/skills/absence/SKILL.md) | impact sur les tickets de la période ; réaffecter ou décaler ; recalculer la date de fin ; alerte si un ticket critique ou la deadline est touché |
| Budget revu | [`revision-budget`](../../.claude/skills/revision-budget/SKILL.md) | recalcul de la projection ; scénarios (retirer des fonctionnalités, réaffecter, décaler) ; arbitrage humain |

**S1-R8 · La passation démarre au moins 5 jours ouvrés avant un départ.** Si le préavis est plus court : passation accélérée, alerte au tableau de bord et ticket `ATTENTE_HUMAIN`.
*Pourquoi :* 5 jours ouvrés, soit une semaine de travail, suffisent pour documenter, faire travailler un binôme et réaffecter. En dessous, le risque de perte de connaissance doit être arbitré par un humain.

**S1-R9 · Un salarié ne peut pas être affecté à un ticket qui tombe pendant son absence.**
*Pourquoi :* sa capacité est nulle sur la période ; l'affectation fausserait le planning.

**S1-R10 · La capacité d'un salarié est répartie entre projets par une allocation en %** dans sa fiche. La priorité entre projets est une décision humaine.
*Pourquoi :* l'ESN mène plusieurs projets ; sans allocation explicite, la même heure serait comptée deux fois.

## 7. Budget et délais
- Unités et taux : [ARCHITECTURE § 8](../ARCHITECTURE.md#8-unités-et-coûts) (7 h/j ; agents à 15 €/h ; salariés de 350 à 550 €/j).
- Formules et alertes : [ARCHITECTURE § 7](../ARCHITECTURE.md#7-ticketing-résumé).

**S1-R11 · Au-delà de 90 % du budget consommé, ou si la date de fin projetée dépasse la deadline,** le chef de projet crée un ticket `ATTENTE_HUMAIN` avec des scénarios.
*Pourquoi :* le contrôle du budget et des délais est un objectif de la consigne ; l'alerte doit arriver tant qu'il reste des marges de manœuvre.

**S1-R12 · Un ticket `EN_COURS` sans mise à jour depuis plus de 2 jours ouvrés déclenche une alerte.**
*Pourquoi :* sur un projet d'une semaine, 2 jours sans nouvelles représentent 40 % du temps disponible.

## 8. Contrôles
- Chaque ticket est conforme au template (skill [creer-ticket](../../.claude/skills/creer-ticket/SKILL.md)) et porte `competence_requise`.
- Pas de dépendance circulaire ; pas d'affectation pendant une absence.
- Cohérence entre `projet.md` (budget, deadline) et `TABLEAU.md`.

## 9. Interfaces
- **S4 →** fournit `cdc.md` et `architecture.md` VALIDÉS.
- **S3 →** crée des tickets bug et des avis de revue, et confirme le TERMINE des déploiements.
- **S2 →** crée des tickets bug, incident, support et amelioration (veille), que S1 trie.
