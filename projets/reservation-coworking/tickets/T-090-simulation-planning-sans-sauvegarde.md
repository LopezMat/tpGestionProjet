---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-090
titre: SIMULATION — Fermer la fenêtre « production sans sauvegarde » dans le planning (triage)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: planification (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-6 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-090 — SIMULATION — Fermer la fenêtre « production sans sauvegarde » dans le planning (triage)

## Description
Proposition **P-6** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md), **cause 4**. Le planning place bien [T-029](T-029-sauvegarde-quotidienne-limite-age.md) avant le déploiement [T-047](T-047-deploiement.md), mais rien n'empêche des données d'exister avant la première sauvegarde réussie :
- le GO [T-046](T-046-go-mise-en-production.md) ne dépend ni de T-029 ni de [T-048](T-048-mise-en-service.md) ;
- dans T-048, la tâche planifiée vient après la création des comptes.

**Ce ticket décrit les changements à appliquer au triage, à la reprise du développement. Ils ne sont pas appliqués le 2026-11-26** (consigne du coordinateur : développement en pause, aucun ticket existant modifié, `planning.md` intact).

### Changements à appliquer au triage
1. **`depend_de` du GO T-046** : aujourd'hui `[T-042, T-043, T-045, T-069]`.
   - **À ajouter (cause 4)** : **T-029** (outillage de sauvegarde) et **[T-087](T-087-simulation-refus-base-vide.md)** (refus de recréer une base vide).
   - **À arbitrer par un humain** :
     - [T-086](T-086-simulation-proteger-volume-production.md) (volume protégé, cause 2) : recommandé ;
     - [T-089](T-089-simulation-exercice-restauration-chronometre.md) (exercice de restauration) : recommandé, c'est la seule preuve que la restauration marche sur l'app du projet ;
     - [T-088](T-088-simulation-fraicheur-sauvegardes-suivi.md) (contrôle de fraîcheur), s'il reste dans le projet ;
     - [T-078](T-078-image-postgresql-16-16.md), déjà recommandé par T-078 lui-même.
   - **Contrôle des cycles, fait le 2026-11-26** : aucun de ces tickets ne dépend, directement ou non, de T-046. Les chaînes sont T-029 → T-007 ; T-086 → T-029 ; T-087 → T-029, T-086 ; T-089 → T-021, T-029, T-085, T-086, T-087 ; T-088 → T-029. Il n'y a pas de cycle.
2. **T-048, ordre des actions.**
   1. `init_accueil` (aucune donnée du client à ce stade).
   2. Tâche planifiée créée et **première sauvegarde manuelle réussie** : `LastTaskResult` à 0, fichier présent dans `sauvegardes-quotidiennes/`, `pg_restore --list` sans erreur.
   3. **Seulement ensuite**, remise des comptes au client (via Claire).
   
   **Critère à ajouter** : « un fichier de `sauvegardes-quotidiennes/` existe et est lisible par `pg_restore --list` avant la remise des comptes ; son nom (sans contenu) est cité dans le rapport de déploiement ou dans le README ». Ce critère répond aussi à la troisième proposition de P-6 (le rapport de déploiement cite la première sauvegarde réussie) sans modifier `templates/rapport-deploiement.md`, qui relève de C et de R11.
   
   **Proposé** : ajouter [T-091](T-091-simulation-registre-demandes-suppression.md) (registre des demandes de suppression) à `depend_de` de T-048.
3. **Tickets compagnons de revue humaine** à créer selon `creer-ticket` (AF3) : « Revue humaine T-085 », « Revue humaine T-086 », « Revue humaine T-087 » (Karim pressenti, 0,5 h chacune), « Revue humaine T-088 » si le ticket reste dans le projet, et celui de T-078 (déjà annoncé dans T-078).
4. **Ligne de journal « triage »** dans chaque ticket touché, qui cite T-080 et ce ticket.
5. **`planning.md`** v1.0 est `VALIDÉ` (DEC-009) et donc figé (R6). Plusieurs éléments changent :
   - le jalon « Sauvegarde quotidienne » et les prérequis du GO ;
   - la charge de Nadia ;
   - les nouveaux tickets.
   
   Un humain doit repasser le fichier en `EN_REVUE` pour une v1.1, dont le temps de rédaction est compté dans le ticket « Pilotage » T-008.

### Capacité et affectations (AF8, AF9, AF10), calculées le 2026-11-26
Période du 2026-11-27 à la deadline du 2026-12-18 (16 jours ouvrés). Les tickets `A_FAIRE` de la période sont comptés. T-049 (après la soutenance) ne l'est pas ; les décisions simulées T-081 à T-084 sont indiquées à part.

| Salarié | Capacité allouée | Charge actuelle | + tickets de ce lot | Utilisation |
|---|---|---|---|---|
| Nadia (20 %, 4/5, absente le 2026-12-03) | 12 jours × 1,4 h = **16,8 h** | 10,5 h (T-029 4,5 ; T-044 1 ; T-048 1 ; T-058 2 ; T-072 0,5 ; T-078 1,5), + 2 h simulées (T-081, T-082) | + 8 h (T-085 1,5 ; T-086 2 ; T-087 1,5 ; T-088 1 ; T-089 2) | **110 %** (122 % avec la simulation) |
| Karim (15 %) | 16 jours × 1,05 h = **16,8 h** | 8,75 h (T-030 à T-038 7,5 ; T-059 0,5 ; T-064 0,5 ; T-074 0,25) | + 0,5 h (T-089) + 1,5 h (revues compagnons de T-085 à T-087) + 0,5 h (revue de T-078) | **67 %** |
| Claire (20 %) | 16 jours × 1,4 h = **22,4 h** | 8 h (T-009 2,5 ; T-045 5 ; T-046 0,5), + 2 h simulées (T-083, T-084) | + 0,5 h (T-091) | **38 %** (47 % avec la simulation), sous 50 % : signalé (AF9), aucun ticket ajouté pour atteindre un taux |

**Pourquoi tout reste chez Nadia, malgré la charge.** Pour T-085 à T-089, j'ai cherché une autre affectation et n'en ai trouvé aucune conforme aux critères :
- **aucun agent** n'écrit dans `runbooks/`, `scripts/`, `deploiement/` ni `.claude/`, et aucun n'a `docker` (règle 7, AF6) ;
- **Karim** n'a ni `sauvegarde-restauration`, ni `docker`, ni `ci-cd`, et aucun salarié `expert` de ces compétences ne peut l'encadrer en binôme (AF7) ;
- **Claire, Léa et Hugo** n'ont aucune de ces compétences ; Léa et Hugo sont à 0 % (AF8).

Il en résulte une **dépendance à une seule personne (AF10 b)** sur `sauvegarde-restauration`, `docker`, `ci-cd` et `supervision`. Elle est confirmée par la crise : une perte de données un mercredi ou le 2026-12-03 n'aurait aucun exécutant. DEC-009, point E, interdit les tickets `formation` dans ce projet. P-7 (Karim) et P-8 (Claire) ne sont donc pas créés ; le choix entre garder le point E et le rouvrir revient à un humain.

**Propositions pour la décision au triage** (règle 13 : je propose, un humain décide, le coordinateur applique) :
- **(A) Recommandée.** Nadia passe à 30 % jusqu'à la mise en service : 25,2 h de capacité, soit 73 % d'utilisation (81 % avec la simulation). L'allocation ne coûte rien en elle-même : seules les heures passées sont facturées. Retour à 5 % après la mise en service, comme prévu par `planning.md`.
- **(B)** Nadia reste à 20 %. T-088 sort du projet (voir ci-dessous) et T-089 passe après la mise en service : 15,5 h, soit 92 %, mais la mise en service se ferait sans restauration éprouvée.
- **(C)** Nadia reste à 20 % sans rien retirer : la chaîne T-029 → T-086 → T-087 (8 h à 1,4 h par jour, soit environ 6 jours de Nadia) retarde le GO si elle en devient un prérequis. L'alerte S1-R11 est alors à évaluer.

**Imputation (DEC-009, point D).**
- T-086, T-087, T-089, T-091 et ce ticket protègent la production de ce client avant son GO. Ce sont les mêmes cas que T-058 et T-072 : ils restent au projet.
- T-085 (runbook) est un document commun de l'ESN, mais T-089 en dépend. Recommandation : il reste au projet.
- T-088 (règle d'agent) est de même nature que le lot R17 (T-050). Recommandation : il sort du projet client vers la PR de règles de l'ESN.

**Coût du lot** :
- tickets créés : 593,21 €, soit Nadia 8,5 h (546,43 €), ce ticket 0,5 h d'agent (7,50 €) et T-091 0,5 h de Claire (39,29 €) ;
- **711,07 €** avec les trois revues compagnons de T-085 à T-087 (1,5 h de Karim, 117,86 €) ;
- 646,79 € si T-088 sort du projet.

Le budget consommé et la fin projetée sont à recalculer par `scripts/tableau.py` au triage, avec l'alerte S1-R11 si le budget dépasse 90 % ou si la fin dépasse le 2026-12-18.

**Temps** : le temps de ce ticket est compté ici, et non dans le ticket « Pilotage » T-008, pour ne pas le compter deux fois.

## Critères d'acceptation
- [ ] `depend_de` de T-046 contient T-029 et T-087 ; les ajouts à arbitrer (T-086, T-088, T-089, T-078) sont tranchés par un humain (`DEC-NNN`), puis appliqués ou écartés, avec la raison au journal de T-046.
- [ ] L'ordre des actions de T-048 est modifié (`init_accueil`, puis tâche planifiée et première sauvegarde manuelle réussie, puis remise des comptes), avec le critère vérifiable « fichier quotidien présent et lisible par `pg_restore --list` avant la remise des comptes ».
- [ ] Les tickets compagnons de revue humaine de T-085, T-086 et T-087 (et de T-088 s'il reste dans le projet) existent, conformes à `creer-ticket`.
- [ ] Une ligne de journal « triage » qui cite T-080 et T-090 figure dans chaque ticket touché.
- [ ] L'allocation de Nadia (option A, B ou C) et l'imputation de T-088 sont tranchées par un humain (`DEC-NNN`) ; `planning.md` v1.1 est soumis en `EN_REVUE` après que l'humain l'a repassé dans ce statut.
- [ ] `python scripts/tableau.py` a été lancé après les changements ; le budget et la fin projetée sont notés au journal, avec l'alerte S1-R11 si besoin.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (planification)
- **Commentaires** :
- **Revue humaine requise** : non (les changements de dépendances du GO et l'allocation passent par une décision humaine)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-6 ; changements de T-046 et de T-048 décrits, non appliqués (développement en pause) ; capacité de Nadia calculée à 110 % avec ce lot, options A à C ; imputation de T-088 à arbitrer · 0 h
- 2026-11-26 18:45 · agent:chef-de-projet · SIMULATION · DEC-019 appliquée en partie, **à ne pas refaire au triage** : T-029 passé en priorité critique, et T-029 ajouté à depend_de du GO T-046. Reste à faire au triage : T-087 dans depend_de de T-046, et les arbitrages listés. T-088 passé ANNULE, couvert par T-092 (vérification quotidienne : existence de moins de 26 h, restauration dans une base jetable, alerte) : dans les arbitrages du GO et dans la liste des revues compagnons, lire T-092 à la place de T-088 ; à ajouter à T-048 : création de la tâche de vérification et première vérification réussie avant la remise des comptes. Charge de Nadia recalculée : 21,5 h pour 16,8 h (128 %, 140 % avec la simulation) ; option A 85 % (93 %) ; option B ne tient plus (116 %). Coût du lot : + 192,86 € net (T-092 257,14 € − T-088 64,29 €), + 39,29 € pour la revue compagnon de T-092 · 0 h (temps compté dans T-008)
- 2026-11-26 19:00 · agent:coordinateur · SIMULATION · allocation de Nadia tranchée par Ethan (DEC-019 v0.2) : **option (A)**, 30 % jusqu'à la mise en service ; `equipe/membres/nadia.md` mis à jour. T-088 est déjà annulé (couvert par T-092), son imputation n'est plus à trancher. Reste au triage : `planning.md` v1.1 (après repassage `EN_REVUE` par un humain) et les autres points de ce ticket · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 22:55 · agent:chef-de-projet · SIMULATION · triage demandé par Ethan, **fait, à ne pas refaire** : (point 3) revues humaines créées, Karim 0,5 h chacune, sans depend_de vers le ticket relu (AF3) : T-095 (T-085), T-096 (T-086), T-097 (T-087), T-098 (T-092, à la place de T-088), T-099 (T-078), toutes imputées à l'ESN (DEC-020), et T-100 (T-079, au budget client) ; aucune autre revue manquante (T-080 est un incident critique clos par le coordinateur, T-088 est ANNULE) ; (point 1) T-087, T-092 et T-078 ajoutés à depend_de du GO T-046 (DEC-020 point 3), T-029 y était déjà, sans cycle ; T-086 est prérequis de fait par T-087 ; T-089 et T-079 non ajoutés (à arbitrer) ; (point 4) ligne « triage » dans T-046, T-078, T-079, T-085 à T-087 et T-092 ; (point 5) planning.md v1.1 rédigé en EN_REVUE ; tableau.py lancé. **Reste à faire** : point 2 (ordre des actions de T-048 et ajout de T-091 à son depend_de, première sauvegarde et première vérification T-092 réussies avant la remise des comptes), non demandé dans ce triage. Temps compté dans T-008 · 0 h
