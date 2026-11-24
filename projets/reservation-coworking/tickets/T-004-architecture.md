---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-004
titre: Architecture
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:architecte   # agent:<nom> | salarie:<prenom>
competence_requise: architecture-logicielle (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 11.5         # heures équivalent humain
depend_de: [T-003]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le: 2026-11-24        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-004 — Architecture

## Description
Ticket de travail de l'`architecte` (R14, étape 3 du pipeline). À partir du [CDC v1.0](../cdc.md) (`VALIDÉ`, DEC-006), rédiger `projets/reservation-coworking/architecture.md` selon `templates/architecture.md` : choix du système d'information et de la stack, modèle de données, découpage des composants, authentification et rôles (membre, accueil), hébergement en production locale Docker (DEC-003, `url_prod: http://localhost:8080`), `/health` renvoyant le SHA, sécurité et RGPD (§ 8 du CDC).

Points structurants du CDC : 5 Must (F-01 à F-04, F-07) ; authentification par e-mail et mot de passe haché, changement obligatoire du mot de passe à la première connexion pour tous les comptes ; compte accueil initial créé par script d'initialisation (mot de passe par variable d'environnement, jamais dans le dépôt) ; unicité d'une réservation par salle et par créneau sous concurrence ; règles horaires (lun-ven, 8 h-20 h, 2 créneaux par jour, 14 jours d'avance) ; Should : F-06 (fiches des salles) et F-08 (purge à 12 mois). Budget 6 000 € HT et deadline 2026-12-18 : privilégier une stack simple et maîtrisée par l'équipe.

Repère d'estimation : 7 h pour une application métier.

## Critères d'acceptation
- [ ] `architecture.md` existe, suit `templates/architecture.md` avec l'en-tête standard et la ligne de provenance, en `EN_REVUE`.
- [ ] Chaque exigence Must du CDC (F-01, F-02, F-03, F-04, F-07) est rattachée à au moins un composant ou une décision d'architecture.
- [ ] Chaque choix technique important est justifié et accompagné d'au moins une alternative écartée.
- [ ] Le § 8 du CDC (sécurité, RGPD) est couvert : hachage des mots de passe, contrôle des rôles côté serveur, gestion des secrets, conservation des données.
- [ ] L'hébergement suit DEC-003 (production locale Docker) ou, s'il en diffère, le point est posé comme décision humaine.
- [ ] Un ticket `decision` « Choix techniques » est créé en `ATTENTE_HUMAIN`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail, pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 18:30 · agent:coordinateur · création · 0 h
- 2026-11-24 18:40 · agent:architecte · passage EN_COURS ; lecture du CDC v1.0 (VALIDÉ, DEC-006), de DEC-003, du modèle `deploiement/docker-compose.yml`, de `scripts/prod_locale.py` et des fiches de l'équipe · 1 h
- 2026-11-24 19:00 · agent:architecte · vérification des versions par recherche web (Python, FastAPI, Uvicorn, SQLAlchemy, Alembic, psycopg, argon2-cffi, tzdata, PostgreSQL 16, pytest, httpx, Playwright) · 1 h
- 2026-11-24 19:25 · agent:architecte · rédaction de `architecture.md` v0.1 (EN_REVUE) : stack, modèle de données, sécurité, couverture des exigences non fonctionnelles, déploiement, sauvegardes, 17 décisions · 4,5 h
- 2026-11-24 19:30 · agent:architecte · création de T-005 « Choix techniques » (ATTENTE_HUMAIN) ; passage EN_REVUE · 0,5 h
- 2026-11-24 21:00 · agent:architecte · révision de `architecture.md` en v0.2 (EN_REVUE) selon les arbitrages d'Ethan sur T-005 (DEC-007) : stack A1 retenue, procédure pas à pas de `init_accueil` (PowerShell 7.1+, 5.1, bash/Git Bash, contrôles de non-fuite), écart « clé de signature » pris en compte, sauvegarde quotidienne par commande réutilisant `prod_locale.py` avec rétention 14 jours et tâche planifiée Windows (limite v0.1 de 30 jours retirée), limites et risques au nouveau § 11 ; ticket reste EN_REVUE · 1,5 h
- 2026-11-24 22:00 · agent:architecte · révision de `architecture.md` en v0.3 (EN_REVUE) selon trois corrections d'Ethan (DEC-007) : seuil global de 30 échecs transformé en alerte journalisée `ALERTE_SECURITE` sans blocage (format défini pour `analyste-prod`) ; R-03 traité par une limite d'âge de 30 jours sur toute sauvegarde du projet, appliquée par `sauvegarder_local.py` avec ajout additif dans `prod_locale.py` (tests existants inchangés, tests complétés) et durée réelle de 30 jours dans la page de confidentialité ; « Pourquoi » de C repris (décision 6, § 6, R-06) ; ticket reste EN_REVUE · 1 h
- 2026-11-24 23:00 · agent:architecte · révision v0.4 de `architecture.md` selon deux décisions d'Ethan (DEC-007) : limite de 30 jours appliquée aussi au déploiement (`purger_sauvegardes()`), `test_retention` daté par rapport à `maintenant()` ; revue de Karim reportée aux tickets d'authentification (S3-R2). **Révision interrompue** : pendant le travail, le fichier est passé `VALIDÉ` (v1.0, `valide_par: Ethan`, `decision: DEC-007`). Une partie des changements avait déjà été enregistrée : historique v0.4, schéma, § 6, § 7, première puce « Sauvegardes » du § 8. Le reste n'a pas été appliqué (R6) : fin du § 8, décision 14, § 9, § 10, R-02 à R-05. Le document validé est donc incohérent sur la limite au déploiement. Un humain doit le repasser en `EN_REVUE` pour que la révision soit terminée. Ticket reste EN_REVUE · 0,5 h
- 2026-11-24 23:45 · agent:architecte · `architecture.md` repassé `EN_REVUE` par Ethan (v1.0) ; révision **v1.1** (EN_REVUE, `valide_par` et `decision` vides) qui complète la v0.4 interrompue et intègre DEC-008 (EN_REVUE) : limite de 30 jours au déploiement via `purger_sauvegardes()` reportée partout (§ 8 limite d'âge, modification de `prod_locale.py`, tests dont `test_retention` daté par rapport à `pl.maintenant()` et nouveau test au déploiement, liste « Rétention cohérente » ; § 9 statut et décision 14, option (d) retenue, « commande quotidienne seule » écartée ; § 10 ticket de sauvegarde 3,5 à 4,5 h ; § 11 R-02 à R-05) ; limite R-05 écrite telle quelle ; procédure PowerShell de suppression des dossiers de sauvegardes en fin de démonstration ; message « Limite d'âge » distinct de « Rétention » dans `deployer_local.py` (désormais modifié) et `sauvegarder_local.py` ; relecture de cohérence du document entier. Ticket reste EN_REVUE · 1,5 h
