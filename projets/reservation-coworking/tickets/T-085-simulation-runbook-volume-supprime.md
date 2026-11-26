---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-085
titre: SIMULATION — Runbook perte-donnees, cas « volume supprimé » et « sauvegarde absente des traces »
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
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
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-1 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-085 — SIMULATION — Runbook perte-donnees, cas « volume supprimé » et « sauvegarde absente des traces »

## Description
Proposition **P-1** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md). Le runbook [perte-donnees](../../../runbooks/perte-donnees.md) (v0.2, `EN_REVUE`, responsable D) suppose une base vivante. Il ne décrit ni la perte du volume entier, ni le cas où aucune trace versionnée n'établit la dernière sauvegarde. Pendant la crise, la procédure a dû être reconstituée dans [T-081](T-081-simulation-decision-restauration-base.md) (étapes 1 à 6). L'outillage actuel recréerait une base vide sans alerte (voir T-087).

**Attendu** (contenu déjà rédigé dans T-081 et dans le détail de P-1 du post-mortem, à reprendre et à vérifier) :
- **le constat** : volume absent, conteneurs présents ou absents ;
- **les interdits** : ni `deployer_local.py` ni `rollback_local.py` sur un volume absent ;
- **la recréation du seul service `db`**, avec le mot de passe existant (rôle `esn` et base `app` recréés par l'image) ;
- **la restauration avant tout démarrage de l'app** ;
- **l'option sans `session`** (`pg_restore -l`, puis `-L`) ;
- **le rôle applicatif** à recréer si [T-058](T-058-role-applicatif-non-superutilisateur.md) est réalisé ;
- **le rejeu des suppressions**, à partir du registre du client (voir T-091) ;
- **la reconstruction sans sauvegarde** (`init_accueil`, comptes recréés par l'accueil) ;
- **à l'étape « minutes 5-10 »** : la vérification physique des dossiers et `pg_restore --list` par un humain quand aucune trace versionnée n'établit la sauvegarde.

Fichier modifié : `runbooks/perte-donnees.md`, hors du périmètre d'écriture des agents (C9). La modification passe par une PR acceptée par D.

**Affectation : `salarie:nadia`, proposition du `gestionnaire-crise` conservée.**
- **Pourquoi pas un agent (AF6 écarté, règle 7).** Aucun agent n'écrit dans `runbooks/`. Les deux agents qui ont `sauvegarde-restauration` (`deployeur`, `gestionnaire-crise`) n'écrivent que dans `projets/<slug>/`. Le `gestionnaire-crise` a déjà fourni le brouillon (T-081, post-mortem), et il ne reste qu'à le mettre en forme et le vérifier.
- **Pourquoi Nadia.** C'est la seule salariée qui a `sauvegarde-restauration` (`confirme`, niveau requis atteint, AF7). Elle est `actif`, allouée à 20 % (DEC-009) et sans `date_depart` (AF8). Elle est aussi la porteuse de T-081, c'est-à-dire l'exécutante de la procédure.
- **Dépendance à une seule personne (AF10 b).** Elle est constatée, mais aucun ticket `formation` n'est créé : DEC-009, point E, renvoie ce besoin au plan de formation de l'ESN (voir le message de retour du `chef-de-projet` du 2026-11-26).
- **Charge.** La capacité de Nadia est dépassée si T-085 à T-089 s'ajoutent à ses tickets. L'analyse et les propositions sont dans [T-090](T-090-simulation-planning-sans-sauvegarde.md).
- **Fenêtres à éviter** : les mercredis (4/5) et le 2026-12-03 (EV-002).
- **Ticket salarié (AF11, R15)** : à faire par un humain. Il peut s'aider de Claude Code dans une session dédiée en citant ce ticket ; il reste l'auteur, il valide le résultat et il note son temps.

**Ordre.** Aucune dépendance : le brouillon existe, et ce ticket peut être traité en premier à la reprise. Les commandes ne sont vérifiées pour de vrai que par l'exercice [T-089](T-089-simulation-exercice-restauration-chronometre.md), qui dépend de ce ticket. Pour éviter un blocage réciproque, cette vérification est un critère de T-089 et non de T-085. Si [T-086](T-086-simulation-proteger-volume-production.md) rend le volume `external`, il met à jour la section « Volume supprimé » (critère de T-086).

**Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] Le runbook contient une section « Volume de la base supprimé », avec le constat, les interdits et les commandes dans l'ordre (recréation de `db`, restauration avant le démarrage de l'app, option sans `session`, rôle applicatif, rejeu des suppressions, reconstruction sans sauvegarde).
- [ ] L'étape « minutes 5-10 » décrit le cas « aucune sauvegarde tracée » : vérification physique en lecture seule par un humain, `pg_restore --list`, relevé du dernier SHA vérifié de `historique.json`, sans aucun contenu de données au journal.
- [ ] Aucune valeur de secret dans le runbook (le mot de passe est désigné par son chemin, jamais recopié).
- [ ] La PR est acceptée par D ; la ligne « Revue humaine » ci-dessous est remplie ; le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (procédure d'exploitation, pas de code)
- **Commentaires** :
- **Revue humaine requise** : oui (procédure sur les données de production). **Le ticket compagnon « Revue humaine T-085 » sera créé au triage, à la reprise du développement.** Relecteur pressenti : Karim (`base-de-donnees-sql` expert) pour les commandes PostgreSQL (`pg_restore`, rôles). Personne d'autre que Nadia n'a `sauvegarde-restauration` ; c'est le même choix que pour T-038 (DEC-009, point E).
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-1 ; assignée à Nadia (seule salariée sauvegarde-restauration, aucun agent n'écrit dans runbooks/) ; sans dépendance ; non planifié (développement en pause) · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
