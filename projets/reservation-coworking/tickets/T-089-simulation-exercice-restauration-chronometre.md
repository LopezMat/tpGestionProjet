---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-089
titre: SIMULATION — Exercice de restauration réel, cas « volume supprimé », chronométré
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-021, T-029, T-085, T-086, T-087]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn (R18, DEC-023)
imputation_decision: DEC-020   # décision VALIDÉ qui met ce ticket à la charge de l'ESN
---
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-5 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-089 — SIMULATION — Exercice de restauration réel, cas « volume supprimé », chronométré

## Description
Proposition **P-5** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md). La durée réelle d'une restauration est un point ouvert du runbook `perte-donnees`. Le test de rollback du 2026-11-26 ([test-rollback-2026-11-26.md](../rapports/test-rollback-2026-11-26.md)) portait sur la mini-app de démonstration, pas sur l'app du projet. Il faut mesurer avant la soutenance, sur l'app du projet, la procédure de [T-085](T-085-simulation-runbook-volume-supprime.md) avec l'outillage final ([T-029](T-029-sauvegarde-quotidienne-limite-age.md), [T-086](T-086-simulation-proteger-volume-production.md), [T-087](T-087-simulation-refus-base-vide.md)).

**Déroulé :**
1. Sur un projet compose jetable, au nom distinct de la production (par exemple `esn-test-restauration-…`), déployer l'app du projet.
2. Charger le jeu de données fictif ([T-021](T-021-jeu-donnees-recette.md)) et faire une sauvegarde avec `sauvegarder_local.py`.
3. Vérifier que `deployer_local.py` refuse de recréer une base vide (T-087).
4. Supprimer le volume du projet jetable, puis dérouler la procédure de T-085.
5. Mesurer chaque étape.
6. Consigner le tout dans `rapports/test-restauration-AAAA-MM-JJ.md`, sans aucun contenu de données.

**Précaution, qui découle de la cause présumée de l'incident.** L'exercice tourne sur le même moteur Docker que la production, et l'hypothèse de T-080 est justement un nettoyage avec le mauvais nom de projet. Avant toute commande destructrice, le second exécutant relit la commande et le nom du projet à voix haute (quatre yeux). On relève `docker volume ls` avant et après : le volume de production, s'il existe, doit rester intact.

**Affectation : `salarie:nadia`, avec Karim en second exécutant.**
- **Pourquoi pas un agent (AF6 écarté).** C'est une restauration réelle avec des commandes `docker` et `pg_restore`. Aucun agent ne restaure de données (S2-R1, règle 5 du `deployeur`), et aucun agent n'a `docker`.
- **Pourquoi Nadia.** C'est la seule salariée qui a `sauvegarde-restauration` (`confirme`, AF7). Elle est allouée à 20 % (AF8), et c'est elle qui exécuterait une vraie restauration (T-081).
- **Rôle de Karim : contrôle de cohérence (0,5 h, inclus dans l'estimation).** Karim (`base-de-donnees-sql` expert, alloué à 15 %) fait le contrôle de cohérence prévu par la vraie procédure (critère 4 de T-081) : nombre de lignes par table, 3 salles, au moins un compte accueil. L'exercice répète donc la procédure complète, avec ses deux exécutants. Ce n'est pas une formation déguisée : la formation de Karim à `sauvegarde-restauration` (P-7 du post-mortem) n'est pas créée, parce que DEC-009, point E, renvoie ce besoin au plan de formation de l'ESN. L'exercice reste malgré tout la première occasion pour Karim de voir la procédure (AF10 b).
- **Écart de coût.** `tableau.py` valorise ce ticket au taux de l'assignée (64,29 €/h). Les 0,5 h de Karim (78,57 €/h) sont donc sous-évaluées d'environ 7,14 €. L'écart est accepté pour ne pas créer un ticket de 0,5 h. Karim note son temps au journal sous son nom.
- **Charge.** La capacité de Nadia est dépassée ; voir [T-090](T-090-simulation-planning-sans-sauvegarde.md).
- **Fenêtre.** Un jour où les deux sont présents : pas un mercredi (Nadia), pas le 2026-12-03 (EV-002, Nadia), avant le 2026-12-21 (EV-003, Karim).
- **Ticket salarié (AF11, R15)** : à faire par des humains, jamais par le coordinateur ni un agent.

**Dépendances.**
- **T-021** : le jeu de données fictif.
- **T-029** : `sauvegarder_local.py`.
- **T-085** : la procédure à jouer.
- **T-086 et T-087** : l'outillage final, pour que l'exercice prouve ce qui sera réellement en place.
- L'ajout de ce ticket à `depend_de` du GO est à arbitrer au triage (T-090).

**Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] `rapports/test-restauration-AAAA-MM-JJ.md` donne la durée de chaque étape, et le nombre de lignes par table avant et après (identiques), sans contenu de données ni secret.
- [ ] Sur le projet jetable, `deployer_local.py` rend le code 2 avec le message de T-087 quand le volume est absent et l'historique non vide.
- [ ] La sonde rend `DISPONIBLE ET À JOUR` sur le SHA jetable après la restauration.
- [ ] `docker volume ls`, relevé avant et après, montre le volume de production intact (ou absent s'il n'existe pas encore), et le nom du projet jetable est noté.
- [ ] Le contrôle de cohérence a été fait par Karim, et il a exécuté lui-même au moins une étape de la restauration.
- [ ] Le runbook est corrigé (PR, T-085 rouvert ou nouveau ticket) si un écart apparaît, ou l'absence d'écart est notée.
- [ ] Le temps passé est noté (journal, `temps_passe_h`), par exécutant.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (exercice d'exploitation)
- **Commentaires** :
- **Revue humaine requise** : non (base jetable, données fictives ; les deux exécutants humains se contrôlent l'un l'autre avant chaque commande destructrice)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-5 ; assignée à Nadia (seule salariée sauvegarde-restauration), Karim en second exécutant pour le contrôle de cohérence (0,5 h incluse, estimation portée de 2 h à 2,5 h) ; dépend de T-021, T-029, T-085, T-086 et T-087 ; précaution sur le nom du projet jetable ; non planifié (développement en pause) · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
