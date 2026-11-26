---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-029
titre: Sauvegarde quotidienne et limite d'âge de 30 jours (outillage)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: critique          # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-26
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-029 — Sauvegarde quotidienne et limite d'âge de 30 jours (outillage)

## Description
Ticket de sauvegarde prévu par [DEC-007](../../../docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md) (point D) et [DEC-008](../../../docs/decisions/2026-11-24-DEC-008-architecture-coherente-coworking.md) (message distinct), comportement fixé par [architecture.md](../architecture.md) § 8 (« Quotidienne », « Modification de `scripts/prod_locale.py` », « Modification de `scripts/deployer_local.py` », « Tests », « Tâche planifiée quotidienne ») et décision 14 ; exigence CDC § 9 (sauvegarde quotidienne, rétention cohérente avec 12 mois) et dernier critère de F-08. Estimation de l'architecte : 3,5 à 4,5 h ; retenu 4,5 h (borne haute, car l'interface de `purger_sauvegardes()` change et plusieurs tests sont touchés).

**Pourquoi un salarié.** Le travail porte sur l'outillage commun (`scripts/`, `docs/ARCHITECTURE.md`), où aucun agent n'écrit (C9 ; règle 8 de `dev-backend`). Nadia a `sauvegarde-restauration` (confirmé) et `docker` (confirmé). **Ticket salarié (AF11, R15)** : à faire par un humain ; il peut s'aider de Claude Code dans une session dédiée en citant ce ticket, reste l'auteur et passe lui-même le ticket `TERMINE` (R13) après l'avis `APPROUVÉ` du `relecteur-code` (T-040) et la revue humaine **T-038** (Karim).

**Affectation conditionnelle** : l'allocation de Nadia au projet est aujourd'hui nulle ; elle est proposée dans T-007 (S1-R10, AF8). Si elle n'est pas accordée, le `chef-de-projet` réaffecte ce ticket.

**Fichiers touchés** : `scripts/sauvegarder_local.py` (nouveau), `scripts/prod_locale.py`, `scripts/deployer_local.py`, `scripts/test_prod_locale.py` (et un fichier de test de la nouvelle commande), `docs/ARCHITECTURE.md` § 10.2 (document `VALIDÉ` : un humain doit d'abord le repasser `EN_REVUE`, R6), README de l'app ou runbook pour la tâche planifiée. Le changement de comportement s'applique à tous les projets de production locale. Par PR relue par C (responsable de l'outillage).

## Critères d'acceptation
- [ ] `python scripts/sauvegarder_local.py --projet <slug>` (et `--racine` caché pour les tests) fait un `pg_dump -Fc` par `compose exec -T db` dans `deploiement/local/<slug>/sauvegardes-quotidiennes/AAAAMMJJ-HHMMSS-quotidienne.dump`, en réutilisant `prod_locale` ; il ne démarre rien.
- [ ] Volume absent : code 0 et « aucune base, rien à sauvegarder » ; service `db` arrêté, `pg_dump` en échec ou fichier vide : fichier partiel supprimé, code 4 ; slug invalide : code 2, rien supprimé.
- [ ] Rétention de 14 jours des sauvegardes quotidiennes, appliquée après une sauvegarde réussie seulement, avec une ligne « Rétention : sauvegarde supprimée … » par fichier.
- [ ] Limite d'âge de 30 jours sur `sauvegardes/` et `sauvegardes-quotidiennes/`, appliquée à chaque exécution de `sauvegarder_local.py` (succès, échec ou volume absent) et à chaque déploiement après un `pg_dump` réussi ; appliquée en premier ; une seule ligne par fichier, « Limite d'âge : sauvegarde supprimée … ».
- [ ] `prod_locale.py` : constante `AGE_MAX_SAUVEGARDES_JOURS = 30`, fonction `purger_sauvegardes_par_age(...)` ; `purger_sauvegardes()` renvoie des couples `(regle, chemin)`, libellés en constantes partagées ; `RETENTION = 10` et `sauvegardes()` inchangés ; `rollback_local.py` non modifié.
- [ ] `deployer_local.py` affiche « <regle> : sauvegarde supprimée <chemin relatif> » ; codes de sortie, ordre des portes, noms des fichiers de sauvegarde et ligne `SAUVEGARDE` de l'historique inchangés ; docstring à jour.
- [ ] Tests (a) à (e) de l'architecture § 8 : `test_retention` daté par rapport à `pl.maintenant()`, assertions inchangées ; test de la limite d'âge au déploiement (deux cas) ; tests unitaires de `purger_sauvegardes_par_age` et `purger_sauvegardes` ; tests de `sauvegarder_local.py` avec le faux Docker ; restauration d'essai (`pg_restore --list`) avec un vrai Docker. Tous les tests de `scripts/` sont verts.
- [ ] La commande de création de la tâche planifiée Windows (20 h 30, `-StartWhenAvailable`) et le contrôle hebdomadaire sont documentés ; la création effective est faite par T-048.
- [ ] `docs/ARCHITECTURE.md` § 10.2 mentionne la limite de 30 jours et la sauvegarde quotidienne, dans la même PR.
- [ ] La PR est relue par C, qui accepte le changement d'interface de `purger_sauvegardes()` (DEC-008).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (suppression de sauvegardes, outillage commun de déploiement ; ticket compagnon T-038)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création ; affectation conditionnelle à l'allocation de Nadia proposée dans T-007 · 0 h
- 2026-11-26 18:45 · agent:chef-de-projet · SIMULATION · priorité haute → critique, à la demande d'Ethan (DEC-019, retour d'expérience de l'exercice T-080) ; ticket ajouté à depend_de du GO T-046 ; section Revue déjà à « Revue humaine requise : oui », ticket compagnon T-038 (Karim) existant ; AF7 respecté (Nadia confirmée, actif) ; statut, assigné et estimation inchangés · 0 h (temps compté dans T-008)
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
