---
# Agents IA de l'ESN (lu par scripts/tableau.py, ne pas renommer les champs)
cout_horaire_eur: 15          # tous les agents, en € par heure équivalent humain (ARCHITECTURE § 8)
responsable: B
maj_le: 2026-11-24
agents:
  - nom: analyste-besoin
    systeme: S4
    responsable: A
    fichier: .claude/agents/analyste-besoin.md
    competences: [recueil-besoin, redaction-cdc, analyse-existant]
  - nom: architecte
    systeme: S4
    responsable: A
    fichier: .claude/agents/architecte.md
    competences: [architecture-logicielle, choix-stack, deploiement-render, securite-applicative]
  - nom: chef-de-projet
    systeme: S1
    responsable: B
    fichier: .claude/agents/chef-de-projet.md
    competences: [gestion-projet, estimation, planification, suivi-budget]
  - nom: dev-backend
    systeme: realisation
    responsable: A
    fichier: .claude/agents/dev-backend.md
    competences: [backend-python, api-rest, base-de-donnees-sql, tests-unitaires]
  - nom: dev-frontend
    systeme: realisation
    responsable: A
    fichier: .claude/agents/dev-frontend.md
    competences: [html-css, javascript, react, accessibilite, tests-unitaires]
  - nom: relecteur-code
    systeme: S3
    responsable: C
    fichier: .claude/agents/relecteur-code.md
    competences: [revue-code]
  - nom: testeur
    systeme: S3
    responsable: C
    fichier: .claude/agents/testeur.md
    competences: [tests-unitaires, tests-e2e, recette-fonctionnelle]
  - nom: securite
    systeme: S3
    responsable: C
    fichier: .claude/agents/securite.md
    competences: [securite-applicative, audit-dependances]
  - nom: deployeur
    systeme: S3
    responsable: C
    fichier: .claude/agents/deployeur.md
    competences: [ci-cd, deploiement-render, sauvegarde-restauration]
  - nom: veilleur
    systeme: S2
    responsable: D
    fichier: .claude/agents/veilleur.md
    competences: [veille-technologique, audit-dependances]
  - nom: analyste-prod
    systeme: S2
    responsable: D
    fichier: .claude/agents/analyste-prod.md
    competences: [supervision, analyse-logs]
  - nom: support
    systeme: S2
    responsable: D
    fichier: .claude/agents/support.md
    competences: [support-utilisateur]
  - nom: gestionnaire-crise
    systeme: S2
    responsable: D
    fichier: .claude/agents/gestionnaire-crise.md
    competences: [gestion-de-crise, sauvegarde-restauration]
hors_perimetre_agents: [relation-client, porter-une-decision, revue-humaine, paiement-en-ligne, tests-utilisateurs, juridique]
---

# Agents IA de l'ESN

Les 13 agents du catalogue ([ARCHITECTURE § 4](../docs/ARCHITECTURE.md#4-catalogue-des-agents)), avec leurs compétences et leur coût. Le `chef-de-projet` s'en sert pour appliquer les critères d'affectation AF1 à AF11.
*Pourquoi ce fichier :* les compétences des agents et celles des salariés doivent être comparables pour choisir qui fait quoi ; le coût unique de 15 €/h est lu par `tableau.py`.

## Catalogue

| Agent | Système | Resp. | Compétences | Coût |
|---|---|---|---|---|
| `analyste-besoin` | S4 | A | recueil-besoin, redaction-cdc, analyse-existant | 15 €/h |
| `architecte` | S4 | A | architecture-logicielle, choix-stack, deploiement-render, securite-applicative | 15 €/h |
| `chef-de-projet` | S1 | B | gestion-projet, estimation, planification, suivi-budget | 15 €/h |
| `dev-backend` | réalisation | A | backend-python, api-rest, base-de-donnees-sql, tests-unitaires | 15 €/h |
| `dev-frontend` | réalisation | A | html-css, javascript, react, accessibilite, tests-unitaires | 15 €/h |
| `relecteur-code` | S3 | C | revue-code | 15 €/h |
| `testeur` | S3 | C | tests-unitaires, tests-e2e, recette-fonctionnelle | 15 €/h |
| `securite` | S3 | C | securite-applicative, audit-dependances | 15 €/h |
| `deployeur` | S3 | C | ci-cd, deploiement-render, sauvegarde-restauration | 15 €/h |
| `veilleur` | S2 | D | veille-technologique, audit-dependances | 15 €/h |
| `analyste-prod` | S2 | D | supervision, analyse-logs | 15 €/h |
| `support` | S2 | D | support-utilisateur | 15 €/h |
| `gestionnaire-crise` | S2 | D | gestion-de-crise, sauvegarde-restauration | 15 €/h |

**Disponibilité.** Un agent n'est assignable que si son `fichier` existe (règle 7 du `chef-de-projet`). Au 2026-11-24, les 13 agents du catalogue existent (lots 2-A à 2-D) et sont donc assignables.

**Coût.** 15 €/h fictifs pour tous les agents : consommation d'API et supervision humaine, justifiés dans [ARCHITECTURE § 8](../docs/ARCHITECTURE.md#8-unités-et-coûts). Les temps sont en heures équivalent humain (R12).

## Hors périmètre agents
Ces compétences ne sont **jamais** confiées à un agent seul. Le ticket va à un salarié qui les possède (AF4) ; si personne ne les a, un ticket `formation` est créé (S1-R6).

| Compétence | Ce qu'elle couvre | Pourquoi un humain |
|---|---|---|
| `relation-client` | réunions, réponses au client, recette avec lui, communication de crise | engage l'ESN et la relation de confiance (AF1) |
| `porter-une-decision` | préparer, présenter et défendre un ticket `decision` | responsabilité de l'ESN ; validation humaine (AF2, R5) |
| `revue-humaine` | revue obligatoire des tickets critiques ou liés à la sécurité | S3-R2 ; contrôle indépendant de l'agent auteur (AF3) |
| `paiement-en-ligne` | choix du prestataire, compte marchand, conformité PCI-DSS (l'intégration du code reste à `dev-backend`) | engagement contractuel et financier |
| `tests-utilisateurs` | tests avec de vrais utilisateurs, ergonomie | exige des personnes réelles |
| `juridique` | conformité RGPD au sens légal, mentions, contrats | responsabilité légale de l'ESN |

## Référentiel des compétences
Vocabulaire unique pour les fiches salariés, les agents et la ligne « Compétence requise » des tickets. Une compétence absente de cette liste s'ajoute ici, par PR (fichier de B).
*Pourquoi :* sans noms communs, le rapprochement entre ticket, agent et salarié est impossible à automatiser.

| Domaine | Compétences |
|---|---|
| Cadrage | `recueil-besoin`, `redaction-cdc`, `analyse-existant`, `relation-client`, `rgpd`, `juridique` |
| Pilotage | `gestion-projet`, `estimation`, `planification`, `suivi-budget`, `porter-une-decision` |
| Conception | `architecture-logicielle`, `choix-stack` |
| Développement | `backend-python`, `api-rest`, `base-de-donnees-sql`, `javascript`, `react`, `html-css`, `accessibilite`, `paiement-en-ligne`, `documentation` |
| Qualité | `tests-unitaires`, `tests-e2e`, `recette-fonctionnelle`, `tests-utilisateurs`, `revue-code`, `revue-humaine` |
| Sécurité | `securite-applicative`, `audit-dependances` |
| Exploitation | `ci-cd`, `docker`, `linux`, `deploiement-render`, `sauvegarde-restauration`, `supervision`, `analyse-logs` |
| Maintenance | `veille-technologique`, `support-utilisateur`, `gestion-de-crise` |

Niveaux : `debutant`, `confirme`, `expert` (ceux de `templates/membre.md`).
