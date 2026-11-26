---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-072
titre: Rotation des journaux dans le modèle compose commun (constat 15)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-029]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn (R18, DEC-023)
imputation_decision: DEC-020   # décision VALIDÉ qui met ce ticket à la charge de l'ESN
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-072 — Rotation des journaux dans le modèle compose commun (constat 15)

## Description
Constat 15 (bas, A09 Journalisation ; A05) du rapport [securite-2026-11-25-4.md](../rapports/securite-2026-11-25-4.md), partie (b) : le modèle commun `deploiement/docker-compose.yml` (DEC-003, responsable C) n'a aucune option `logging` ; le pilote `json-file` y tourne sans `max-size`, si bien qu'une route anonyme peut remplir le disque du poste par ses journaux. La partie (a), propre à l'app (journal d'accès sans chaîne de requête), est dans [T-071](T-071-journal-acces-sans-requete.md).

**Pourquoi un salarié (AF6 écarté).** Comme T-029 (sauvegarde quotidienne) et [T-058](T-058-role-applicatif-non-superutilisateur.md), le travail porte sur l'outillage commun de tous les projets locaux (`deploiement/`), hors du périmètre d'écriture des agents de réalisation (`app/` seulement) et du `deployeur`. Nadia a `docker` au niveau `confirme`. **Ticket salarié (AF11, R15)** : à faire par un humain ; la PR est relue et acceptée par C. Après T-029, qui modifie les mêmes fichiers ; si T-058 est réalisé (décision T-057), les deux changements du modèle commun peuvent partir dans la même PR. Fenêtre à éviter : le 2026-12-03 (Nadia en formation, EV-002).

**Revue humaine non requise** : options de journalisation, sans droit, secret ni donnée personnelle ; la PR est relue par C.

## Critères d'acceptation
- [ ] Chaque service du modèle commun (`app` et base) a une option `logging` avec le pilote `json-file`, `max-size` et `max-file` (par exemple `10m` et `3`, valeurs notées dans le commentaire d'en-tête du modèle) ; `docker compose config` les affiche (test de `scripts/`).
- [ ] Sur une instance déployée jetable, `docker inspect` du conteneur de l'app montre `LogConfig` avec ces valeurs.
- [ ] Les tests de `scripts/` restent verts (déploiement, `rollback_local.py`, sauvegarde de T-029).
- [ ] PR acceptée par C ; le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (options de journalisation de l'outillage commun ; PR relue par C)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 14:45 · agent:chef-de-projet · création (triage du constat 15, partie b, rapport securite-2026-11-25-4) · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 · agent:coordinateur · migration DEC-023 : imputation reportée dans le frontmatter (`imputation: esn`, `imputation_decision: DEC-020`), d'après la ligne « imputé à l'ESN (DEC-020) » ; coût client et part ESN désormais calculés par `tableau.py` (R18) · 0 h
