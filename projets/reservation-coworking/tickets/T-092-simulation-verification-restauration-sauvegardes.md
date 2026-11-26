---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-092
titre: SIMULATION — Vérification quotidienne des sauvegardes (existence, restauration dans une base jetable, alerte)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-021, T-029]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
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
> **SIMULATION** — Retour d'expérience de l'exercice de crise T-080 (scénario 5, S2), DEC-019.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-092 — SIMULATION — Vérification quotidienne des sauvegardes (existence, restauration dans une base jetable, alerte)

## Description
Décision [DEC-019](../../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md), point 3.2, après l'incident simulé [T-080](T-080-simulation-perte-base-production.md) : « un ticket est créé pour vérifier régulièrement qu'une sauvegarde existe et qu'elle se restaure (test de restauration), avec une alerte si elle manque ». Leçon principale de la décision : **une règle sans preuve d'exécution n'est pas une garantie**. Les règles de sauvegarde (DEC-003, DEC-007, DEC-008) étaient validées, mais [T-029](T-029-sauvegarde-quotidienne-limite-age.md) n'avait jamais été réalisé, et personne ne l'a su avant d'en avoir besoin. Ce ticket produit la preuve : chaque jour, une commande vérifie que la sauvegarde existe et se restaure, et prévient un humain quand ce n'est pas le cas.

**Attendu : une commande `scripts/verifier_sauvegarde.py --projet <slug>`, lancée par sa propre tâche planifiée.** Elle est indépendante de la sauvegarde (T-029). Une vérification intégrée à `sauvegarder_local.py` ne verrait pas le cas de la crise, une tâche de sauvegarde qui ne tourne pas du tout.
1. **Fréquence.** Tous les jours à 07:00, par une tâche planifiée Windows distincte de celle de 20 h 30 (`-StartWhenAvailable`), soit environ 10 h 30 après la sauvegarde ; à la demande, en plus.
2. **Existence.** La sauvegarde la plus récente de `deploiement/local/<slug>/sauvegardes-quotidiennes/` (préfixe `AAAAMMJJ-HHMMSS` fixé par T-029) a moins de 26 h et n'est pas vide. Le seuil de 26 h tient compte d'une sauvegarde par jour et de 2 h de marge pour un poste allumé en retard : une sauvegarde manquée est détectée dès le lendemain matin.
3. **Restauration réelle.** Le fichier est restauré par `pg_restore` dans un conteneur PostgreSQL jetable, de la même image que la production (voir [T-078](T-078-image-postgresql-16-16.md)) et au nom distinct `esn-verif-sauvegarde-<slug>`. Le conteneur est lancé par `docker run --rm`, sans volume nommé, sans port publié et sans mot de passe écrit ; il est supprimé à la fin, même en cas d'échec. Le script ne lance jamais `docker compose`, `docker volume rm`, `docker volume prune` ni `down -v`, et ne lit jamais `db_password`. **Pourquoi :** la cause présumée de T-080 est un nettoyage lancé sous le mauvais nom de projet, sur le moteur Docker de la production.
4. **Contrôle de cohérence** sur la base restaurée, repris du critère 4 de [T-081](T-081-simulation-decision-restauration-base.md) : nombre de lignes par table, 3 salles, au moins un compte accueil. Une base restaurée vide ou sans compte accueil est une **sauvegarde suspecte** et déclenche l'alerte. C'est le cas d'une base recréée vide après la perte du volume, puis sauvegardée chaque soir sans erreur, jusqu'à ce que la rétention de 14 jours efface la dernière bonne sauvegarde.
5. **Alerte** quand la sauvegarde manque, est trop ancienne ou vide, quand la restauration échoue ou quand le contrôle de cohérence échoue :
   - code de sortie non nul, visible dans `LastTaskResult` de la tâche ;
   - notification Windows dans la session du poste de production (celle où tourne Docker Desktop) ;
   - fichier `deploiement/local/<slug>/ALERTE-SAUVEGARDE.txt` (date et motif, sans donnée ni secret), qui reste en place jusqu'à la vérification réussie suivante.
6. **Destinataire de l'alerte : l'humain d'exploitation, Nadia.** Elle ouvre un ticket `incident` `haute` le jour même. Si la vérification échoue deux jours de suite, le coordinateur prévient Claire, qui porte la communication avec le client (AF1). **En l'absence de Nadia** (mercredis, 2026-12-03), la vérification tourne quand même et le fichier d'alerte reste en place jusqu'à son retour ; personne d'autre ne sait restaurer (AF10 b, ci-dessous). Un canal hors du poste (e-mail, messagerie) est un point de conception à trancher dans la PR : il exige un secret, qui n'entre jamais dans le dépôt (S3-R8).
7. **Preuve consignée.**
   - **À chaque exécution** : une ligne dans `deploiement/local/<slug>/verifications-sauvegarde.log`, hors Git comme les sauvegardes : date, nom du fichier vérifié, âge, taille, durée de la restauration, nombre de lignes par table, verdict. Aucun contenu de données, aucun secret.
   - **Trace versionnée** : la première exécution réelle donne `rapports/verification-sauvegarde-AAAA-MM-JJ.md`. Ensuite, au contrôle hebdomadaire de l'humain d'exploitation (architecture § 8, déjà budgété), la dernière ligne du journal local est reportée dans `rapports/verification-sauvegardes.md`. C'est la trace qui a manqué pendant la crise (cause 5 du post-mortem).

**Positionnement par rapport à T-088 et T-089.**
- **Ce ticket couvre [T-088](T-088-simulation-fraicheur-sauvegardes-suivi.md), qui passe `ANNULE`.** T-088 (P-4) demandait que l'`analyste-prod` relève l'âge de la dernière sauvegarde à chaque rapport de suivi, alerte au-delà de 26 h et laisse une trace versionnée. Ce ticket fait les trois, et mieux :
  - la vérification tourne chaque jour, sans attendre qu'une session lance l'`analyste-prod` ;
  - elle prouve que la sauvegarde se restaure, et pas seulement qu'un fichier existe ;
  - elle ne demande ni modification de règle d'agent (R11), ni accès d'un agent au dossier qui contient `db_password` ;
  - elle reste au projet, parce qu'elle protège la production de ce client avant son GO, alors que T-090 recommandait de sortir T-088 du projet (DEC-009, point D).
  
  Si un humain veut en plus une ligne « Sauvegarde » dans les rapports de suivi de tous les projets, c'est une amélioration des outils de l'ESN, à traiter dans la PR de règles, hors de ce projet.
- **Ce ticket complète [T-089](T-089-simulation-exercice-restauration-chronometre.md), qui reste.** T-089 est un exercice ponctuel, humain et chronométré de la procédure complète « volume supprimé » ([T-085](T-085-simulation-runbook-volume-supprime.md)), avec deux exécutants. Ce ticket ne supprime rien et ne joue pas la procédure : il vérifie chaque jour, sans intervention, que la sauvegarde du jour se restaure. T-089 prouve que l'équipe sait restaurer ; ce ticket prouve que la matière à restaurer existe.

**Affectation : `salarie:nadia`.**
- **Pourquoi pas un agent (AF6 écarté, règle 7).** Le travail porte sur `scripts/` et sur une tâche planifiée, hors du périmètre d'écriture de tous les agents. Il exécute de vraies commandes `docker` et `pg_restore` ; aucun agent n'a `docker`, et aucun agent ne restaure de données (S2-R1).
- **Pourquoi Nadia.** C'est la seule salariée qui a `sauvegarde-restauration` et `docker` (`confirme`, AF7). Elle est `actif`, allouée à 20 % (DEC-009), sans `date_depart` (AF8). Elle est l'auteure de T-029, dont elle réutilise le format des noms et les fonctions de `prod_locale`.
- **Pourquoi pas Karim.** Il a `backend-python` et `base-de-donnees-sql` (`expert`), mais ni `sauvegarde-restauration` ni `docker`, et aucun `expert` de ces compétences ne peut l'encadrer en binôme (AF7). Il est le relecteur pressenti.
- **Dépendance à une seule personne (AF10 b)** : constatée à nouveau. Aucun ticket `formation` n'est créé, puisque DEC-009, point E, renvoie ce besoin au plan de formation de l'ESN (voir [T-090](T-090-simulation-planning-sans-sauvegarde.md)).
- **Charge (AF9), recalculée le 2026-11-26 sur la période de T-090.** Avec ce ticket (+ 4 h) et l'annulation de T-088 (− 1 h), la charge de Nadia passe de 18,5 h à **21,5 h** pour 16,8 h de capacité, soit **128 %** (140 % avec les décisions simulées T-081 et T-082). Avec l'option (A) de T-090 (Nadia à 30 %, 25,2 h), l'utilisation est de 85 % (93 %). L'option (B) ne tient plus : 19,5 h, soit 116 %. À trancher au triage. Si la charge n'est pas levée, un humain peut décider de découper ce ticket : le script et ses tests à Karim, la restauration réelle et la tâche planifiée à Nadia. Ce serait une exception explicite à AF7.
- **Fenêtres à éviter** : les mercredis et le 2026-12-03 (EV-002).
- **Ticket salarié (AF11, R15)** : à faire par un humain. Il peut s'aider de Claude Code dans une session dédiée en citant ce ticket ; il reste l'auteur, il valide le résultat et il note son temps.

**Estimation : 4 h.**
- Commande, contrôle d'existence et alerte : 1 h.
- Restauration dans le conteneur jetable et contrôle de cohérence : 1,5 h.
- Tests avec le faux Docker : 1 h.
- Documentation de la tâche planifiée, exécution réelle sur un projet jetable et rapport : 0,5 h.

**Coût** : 257,14 € (4 h à 64,29 €/h). Net de l'annulation de T-088 (64,29 €), le surcoût est de 192,86 €, plus 39,29 € pour la revue compagnon (0,5 h de Karim).

**Dépendances.**
- **T-029** : `sauvegarder_local.py`, le dossier `sauvegardes-quotidiennes/`, le format des noms et les fonctions de `prod_locale` réutilisées.
- **[T-021](T-021-jeu-donnees-recette.md)** : le jeu de données fictif, pour l'exécution réelle sur un projet jetable (3 salles, un compte accueil).
- **À arbitrer au triage (T-090)** :
  - l'ajout de ce ticket à `depend_de` du GO [T-046](T-046-go-mise-en-production.md), à la place de T-088 ; recommandé, puisque DEC-019 fait de la preuve d'exécution sa leçon principale ;
  - l'ajout à [T-048](T-048-mise-en-service.md) de la création de la tâche de vérification en production, avec une première vérification réussie avant la remise des comptes au client.

**Fichiers touchés** : `scripts/verifier_sauvegarde.py` (nouveau) et son fichier de test, éventuellement `scripts/prod_locale.py` (fonctions partagées), le README de l'app ou le runbook pour la tâche planifiée. C'est de l'outillage commun : PR relue par C. `docs/ARCHITECTURE.md` § 10.2 est `VALIDÉ` : s'il faut y mentionner la vérification, un humain le repasse d'abord en `EN_REVUE` (R6).

**Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] `python scripts/verifier_sauvegarde.py --projet <slug>` rend le code 0 et « SAUVEGARDE VÉRIFIÉE » quand la sauvegarde quotidienne la plus récente a moins de 26 h, se restaure sans erreur dans le conteneur jetable et passe le contrôle de cohérence ; la sortie cite le nom du fichier, son âge, la durée de la restauration et le nombre de lignes par table, sans aucun contenu.
- [ ] Chaque cas d'échec a son code de sortie et son test avec le faux Docker (`ESN_DOCKER_SIMULATION`) : dossier absent ou vide ; sauvegarde de plus de 26 h ; fichier vide ; `pg_restore` en échec ; contrôle de cohérence en échec (0 salle, ou aucun compte accueil) ; slug invalide (code 2, aucune commande Docker lancée).
- [ ] Dans chaque cas d'échec, `ALERTE-SAUVEGARDE.txt` est créé (date et motif, sans donnée ni secret) et une notification Windows est émise ; la vérification réussie suivante supprime le fichier.
- [ ] Le faux Docker montre que le script ne vise que `esn-verif-sauvegarde-<slug>` (`run --rm`, sans volume nommé ni port publié) ; il ne lance jamais `compose`, `volume rm`, `volume prune` ni `down` ; le conteneur jetable est supprimé même quand la restauration échoue ; `db_password` n'est jamais lu.
- [ ] Chaque exécution ajoute une ligne à `verifications-sauvegarde.log` (date, fichier, âge, taille, durée, compteurs, verdict), sans contenu de données ni secret.
- [ ] Sont documentés à côté de la tâche de sauvegarde quotidienne : la commande de création de la tâche « ESN <slug> - vérification des sauvegardes » (07:00, `-StartWhenAvailable`), le destinataire de l'alerte, la conduite à tenir (ticket `incident` `haute` le jour même, Claire prévenue au second échec consécutif) et le report hebdomadaire dans `rapports/verification-sauvegardes.md`.
- [ ] Une exécution réelle (vrai Docker), sur un projet compose jetable au nom distinct de la production (comme T-089) et avec le jeu de données de T-021, rend « SAUVEGARDE VÉRIFIÉE » ; après vidage du dossier de sauvegardes du projet jetable, elle rend une alerte. `docker volume ls`, relevé avant et après, montre le volume de production intact (ou absent). Le tout est consigné dans `rapports/verification-sauvegarde-AAAA-MM-JJ.md`.
- [ ] Tous les tests de `scripts/` sont verts ; la PR est acceptée par C ; la ligne « Revue humaine » ci-dessous est remplie ; le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (outillage de production : commandes Docker sur le moteur de la production, lecture des sauvegardes qui contiennent des données personnelles). **Ticket compagnon : [T-098](T-098-revue-humaine-t-092.md)** (Karim, créé au triage le 2026-11-26), comme pour T-085 à T-087. Relecteur pressenti : Karim (`backend-python` et `base-de-donnees-sql` expert), pour le code Python, les tests et la restauration PostgreSQL ; c'est le même choix que pour T-038.
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 18:45 · agent:chef-de-projet · SIMULATION · création à la demande d'Ethan (DEC-019, point 3.2, retour d'expérience de l'exercice T-080) ; couvre T-088 (passé ANNULE), complète T-089 ; assignée à Nadia (seule salariée sauvegarde-restauration et docker) ; dépend de T-021 et T-029 ; charge de Nadia recalculée à 128 %, allocation à trancher au triage (T-090) ; non planifié (développement en pause) · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 22:45 · agent:chef-de-projet · SIMULATION · triage (T-080, T-090) : ticket compagnon de revue humaine T-098 créé (Karim, 0,5 h, imputé à l'ESN, DEC-020) ; ce ticket ajouté à depend_de du GO T-046 (DEC-020, point 3) · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
