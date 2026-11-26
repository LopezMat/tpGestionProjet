---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-086
titre: SIMULATION — Protéger le volume de base de production contre une suppression accidentelle
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-029]          # ex. [T-001, T-002]
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
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-2 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-086 — SIMULATION — Protéger le volume de base de production contre une suppression accidentelle

## Description
Proposition **P-2** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md), **cause 2**. Le modèle commun `deploiement/docker-compose.yml` (DEC-003, responsable C) déclare le volume de base comme un volume nommé ordinaire. Il est donc supprimé sans confirmation particulière par `docker compose … down -v` ou par `docker volume prune`. Les projets de test (`esn-test-…`) et la production (`esn-<slug>`) partagent le même moteur Docker et le même préfixe : une erreur sur le nom de projet suffit à perdre la base.

**Mesures attendues :**
- déclarer le volume de base `external`, créé par `deployer_local.py` à la première mise en service, pour que `docker compose down -v` ne le supprime plus ;
- lui ajouter un label `esn.production` ;
- écrire dans le commentaire d'en-tête du modèle, et dans le runbook `perte-donnees` (section créée par [T-085](T-085-simulation-runbook-volume-supprime.md)), que `down -v`, `docker volume rm` et `docker volume prune` sont interdits sur un volume `esn-<slug>_pgdata`, sauf décision de fin de démonstration ([T-049](T-049-fin-de-demonstration.md)).

**Effets à vérifier** :
- **T-049** : avec un volume `external`, l'option 2 (suppression de la base) demandera un `docker volume rm` explicite. La procédure de l'[architecture](../architecture.md) § 8 « Fin de la démonstration » est à relire.
- **Documents `VALIDÉ`** : `architecture.md` du projet (DEC-007, DEC-008) et `docs/ARCHITECTURE.md` § 10 sont figés pour les agents (R6). Si leur texte doit changer, un humain les repasse d'abord en `EN_REVUE`.
- **DEC-003** : si C estime que le changement modifie le comportement décidé par DEC-003, il le soumet à une décision humaine avant la PR.

**Affectation : `salarie:nadia`, proposition du `gestionnaire-crise` conservée.**
- **Pourquoi pas un agent (AF6 écarté, règle 7).** Le modèle commun et `scripts/` sont hors du périmètre d'écriture de tous les agents. Le `dev-backend` n'écrit que dans `app/`. Le `deployeur` exécute l'outillage sans le modifier et n'appelle jamais `docker`. Aucun agent n'a `docker`.
- **Pourquoi Nadia.** C'est la seule salariée qui a `docker` (`confirme`, AF7). Elle est allouée à 20 % (AF8), et c'est le même choix que pour T-029, T-058, T-072 et T-078, qui touchent les mêmes fichiers.
- **Dépendance à une seule personne (AF10 b).** Elle est constatée ; le besoin de formation est renvoyé au plan de formation de l'ESN (DEC-009, point E).
- **Charge.** La capacité de Nadia est dépassée ; voir [T-090](T-090-simulation-planning-sans-sauvegarde.md).
- **Fenêtres à éviter** : les mercredis et le 2026-12-03 (EV-002).
- **Ticket salarié (AF11, R15)** : à faire par un humain, qui reste l'auteur et le responsable. La PR est acceptée par C.

**Dépendances.**
- `depend_de: [T-029]` : T-029 modifie `scripts/deployer_local.py` et `prod_locale.py`, comme T-058 et T-072 qui en dépendent déjà.
- **Coordination** : le même fichier `deploiement/docker-compose.yml` est modifié par T-058, T-072 et T-078. Les regrouper dans une même PR se décide au triage.
- [T-087](T-087-simulation-refus-base-vide.md) (refus d'une base vide) dépend de ce ticket, parce que les deux changent la façon dont `deployer_local.py` traite un volume absent.

**Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] Sur un projet jetable, `docker compose -p esn-test-… down -v` laisse le volume de base en place (test de `scripts/`).
- [ ] `deployer_local.py` crée le volume, avec le label `esn.production`, s'il manque à la première mise en service (historique vide) ; test avec le faux Docker.
- [ ] Les interdits figurent dans le commentaire d'en-tête du modèle commun et dans le runbook `perte-donnees`.
- [ ] La procédure de T-049 (option 2) et celle de l'architecture § 8 « Fin de la démonstration » restent exécutables ; l'écart est noté au journal et signalé pour les documents `VALIDÉ`.
- [ ] Tous les tests de `scripts/` sont verts (déploiement, `rollback_local.py`, sauvegarde de T-029).
- [ ] La PR est acceptée par C ; la ligne « Revue humaine » ci-dessous est remplie ; le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (outillage de production commun DEC-003, protection des données). **Ticket compagnon : [T-096](T-096-revue-humaine-t-086.md)** (Karim, créé au triage le 2026-11-26). Relecteur pressenti : Karim (`backend-python` et `base-de-donnees-sql` expert), pour le code Python et les tests. Personne d'autre que Nadia n'a `docker` ; c'est le même choix que pour T-038 et T-059.
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-2 ; assignée à Nadia (seule salariée docker, modèle commun hors du périmètre des agents) ; dépend de T-029 (mêmes scripts) ; non planifié (développement en pause) · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
- 2026-11-26 22:45 · agent:chef-de-projet · SIMULATION · triage (T-080, T-090) : ticket compagnon de revue humaine T-096 créé (Karim, 0,5 h, imputé à l'ESN, DEC-020) · 0 h
