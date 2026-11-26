---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-087
titre: SIMULATION — deployer_local.py et rollback_local.py refusent de recréer une base vide après un déploiement vérifié
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: ci-cd (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-029, T-086]   # ex. [T-001, T-002]
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
> **SIMULATION** — Action corrective issue de l'exercice de crise T-080 (scénario 5, S2), proposition P-3 du post-mortem du 2026-11-26.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-087 — SIMULATION — deployer_local.py et rollback_local.py refusent de recréer une base vide après un déploiement vérifié

## Description
Proposition **P-3** du [post-mortem](../rapports/post-mortem-2026-11-26-perte-donnees.md) de l'incident simulé [T-080](T-080-simulation-perte-base-production.md), **cause 4**. Aujourd'hui, `scripts/deployer_local.py` et `scripts/rollback_local.py` traitent un volume `esn-<slug>_pgdata` absent comme une première mise en service. Ils recréent une base vide sans alerte : les migrations s'appliquent, l'app accepte des écritures, et la perte est masquée par une base neuve que la restauration écraserait ensuite ([T-081](T-081-simulation-decision-restauration-base.md), point 1).

**Comportement attendu.** Si `deploiement/local/<slug>/historique.json` contient au moins une entrée `EN LIGNE ET À JOUR` et que le volume est absent, les deux scripts :
- sortent avec le code 2 (précondition, « rien n'a changé ») sans rien lancer ;
- affichent le message « volume de production absent alors que l'historique contient N déploiements vérifiés : runbook perte-donnees ».

Une option explicite permet de passer outre. Elle est réservée à la reconstruction décidée par un humain (option (c) de T-081) : elle doit citer le `DEC-NNN`, et le rapport de déploiement la mentionne. Le code 2 garde son sens actuel pour le `deployeur` (ticket `BLOQUE`, pas de nouvel essai au hasard). Aucune règle d'agent ne change.

**Affectation : `salarie:nadia`, proposition du `gestionnaire-crise` conservée.**
- **Pourquoi pas un agent (AF6 écarté, règle 7).** `scripts/` est hors du périmètre d'écriture des agents (outillage commun, responsable C). Le `deployeur` a `ci-cd`, mais il exécute ces scripts sans les modifier.
- **Pourquoi pas Karim.** Il a `backend-python` expert, mais pas `ci-cd`. Le confier à Karim aurait réparti la charge, mais il aurait été sous le niveau requis sans binôme `expert` possible (aucun salarié n'est expert en `ci-cd`, AF7). Il aurait aussi fallu un relecteur pour son code : Nadia ne relit pas du `backend-python` (AF3).
- **Pourquoi Nadia.** C'est la seule salariée qui a `ci-cd` (`confirme`). Elle est allouée à 20 % (AF8) et elle connaît ces scripts par T-029.
- **Dépendance à une seule personne (AF10 b).** Elle est constatée ; le besoin est renvoyé au plan de formation de l'ESN (DEC-009, point E).
- **Charge.** La capacité de Nadia est dépassée ; voir [T-090](T-090-simulation-planning-sans-sauvegarde.md).
- **Fenêtres à éviter** : les mercredis et le 2026-12-03 (EV-002).
- **Ticket salarié (AF11, R15)** : à faire par un humain. La PR est acceptée par C.

**Dépendances.**
- `depend_de: [T-029, T-086]` : les trois tickets modifient `deployer_local.py`.
- [T-086](T-086-simulation-proteger-volume-production.md) fixe la création du volume à la première mise en service ; ce ticket fixe le refus quand il manque après un déploiement vérifié.
- L'ajout de ce ticket à `depend_de` du GO [T-046](T-046-go-mise-en-production.md) est proposé dans [T-090](T-090-simulation-planning-sans-sauvegarde.md).

**Développement en pause** : ticket non planifié, trié à la reprise.

## Critères d'acceptation
- [ ] Test avec le faux Docker : historique non vide et volume absent → code 2, aucun `compose up`, message attendu.
- [ ] Première mise en service (historique vide) inchangée : le volume est créé (T-086) et le déploiement passe.
- [ ] Le même contrôle existe dans `rollback_local.py`, avec un test.
- [ ] Avec l'option explicite, le déploiement passe et la sortie la mentionne (ligne recopiée dans le rapport de déploiement).
- [ ] Les docstrings des deux scripts et le runbook `perte-donnees` décrivent le refus et l'option.
- [ ] Tous les tests de `scripts/` sont verts ; la PR est acceptée par C ; la ligne « Revue humaine » ci-dessous est remplie ; le temps passé est noté.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (outillage de déploiement de production, protection des données). **Le ticket compagnon « Revue humaine T-087 » sera créé au triage, à la reprise du développement.** Relecteur pressenti : Karim (`backend-python` expert), pour le code et les tests.
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 17:30 · agent:chef-de-projet · SIMULATION · création à partir de l'incident T-080 et du post-mortem rapports/post-mortem-2026-11-26-perte-donnees.md, proposition P-3 ; assignée à Nadia (seule salariée ci-cd ; Karim écarté par AF7 et AF3) ; dépend de T-029 et T-086 (mêmes scripts) ; non planifié (développement en pause) · 0 h
