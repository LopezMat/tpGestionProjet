---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-012
titre: Formation Nadia — documentation (guide d'exploitation Docker et restauration)
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: documentation (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
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

# T-012 — Formation Nadia — documentation (guide d'exploitation Docker et restauration)

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-01). Proposé par T-001, **soumis à l'arbitrage de [T-017](T-017-decision-plan-formation-initial.md) (DEC-024)**.

- **Compétence** : `documentation` ; **niveau actuel** : aucun ; **niveau visé** : confirmé, décidé par un humain après la mise à l'épreuve du livrable par T-008 et T-010.
- **Candidate** : Nadia. C'est elle qui détient les connaissances les plus concentrées de l'ESN (`docker`, `sauvegarde-restauration`, `ci-cd`) et elle rédige déjà les runbooks (`reservation-coworking/T-085`). La former à documenter, c'est aussi **transmettre ce qu'elle seule sait** : le livrable sert de support aux formations de Karim (T-008) et de Léa (T-010).
- **Déclencheur** : DEC-021 et EV-004 (Hugo, seul titulaire de `documentation`, part le 2026-12-04 ; aucun agent ne déclare la compétence).
- **Modalité** : autoformation, sans frais (2 h) : principes de la documentation technique (types de documents : tutoriel, procédure, référence, explication), rédaction d'une procédure vérifiable pas à pas. Puis exercice pratique (5 h) : **guide d'exploitation de la production locale Docker** (démarrage, arrêt, journaux, volumes, sauvegarde, restauration dans une base jetable), dans `projets/esn-interne/`, sans secret (S3-R8) et sans donnée d'un client.
- **Fenêtre** : du 2026-12-21 au 2026-12-29, après la fin de l'allocation de 50 % de Nadia à `reservation-coworking` (2026-12-18).
- **Coût** : 7 h × 64,29 €/h = **450,00 €** ; frais externes : 0 €.
- **Mise à l'épreuve, sans dépendance circulaire** : T-008 et T-010 appliquent le guide sans l'aide de Nadia ; leurs écarts sont corrigés dans T-009 et T-011. Ce ticket ne les attend pas pour passer `TERMINE`.
- **Variante moins chère, non retenue seule** (T-103, option A) : déclarer `documentation` pour les agents qui en produisent déjà, par une PR sur `equipe/agents.md` (R11, environ 7,50 €). Elle ne transmet pas les connaissances de Nadia.

## Critères d'acceptation
- [ ] Le guide est publié dans `projets/esn-interne/`, avec l'en-tête standard (R3) ; chaque procédure a un résultat attendu vérifiable.
- [ ] Nadia a déroulé elle-même la procédure de restauration du guide dans une base jetable, sans s'en écarter (ligne au journal).
- [ ] Le guide ne contient ni secret ni donnée d'un client (contrôle noté au journal).
- [ ] Le temps passé (heures équivalent humain) est reporté au journal ; le niveau atteint est proposé, puis décidé par un humain après T-008 et T-010.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:50 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-01 ; DEC-021, EV-004) ; en attente de DEC-024 (T-017) · 0 h
