---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-049
titre: Fin de démonstration (suppression des données sur le poste)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-048]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-049 — Fin de démonstration (suppression des données sur le poste)

## Description
Ticket `decision` prévu par [DEC-008](../../../docs/decisions/2026-11-24-DEC-008-architecture-coherente-coworking.md) (point 4) : « la suppression de données se décide au moment de les supprimer, après la soutenance ». Action sensible sur les données (point d'arrêt humain), **irréversible**, exécutée par un humain, jamais par un agent. Créé en `A_FAIRE` dès le planning ; il passe `ATTENTE_HUMAIN` (avec `bloque_par`) **après la soutenance**, quand le coordinateur le présente. Porteur salarié (AF2) : Nadia, humain d'exploitation, qui exécute ensuite la décision.

**Question** : après la soutenance, quelles données de démonstration supprimer du poste ?

**Options** (à présenter, une ou plusieurs) :
1. **Sauvegardes** : supprimer la tâche planifiée puis les dossiers `deploiement/local/reservation-coworking/sauvegardes/` et `sauvegardes-quotidiennes/`, selon la procédure « Fin de la démonstration » de l'architecture § 8 (déjà décidée sur le principe par DEC-008), avec le contrôle de l'étape 4.
2. **Base** : supprimer le volume `esn-reservation-coworking_pgdata` (après arrêt du projet compose `esn-reservation-coworking`), seule copie restante des données de démonstration ; ensuite plus aucune restauration ni rollback avec données n'est possible.
3. **Traces d'exploitation** : supprimer `deploiement/local/reservation-coworking/historique.json` (historique des déploiements, utilisé par `rollback_local.py`) et `db_password` (mot de passe de la base, inutile une fois le volume supprimé).
4. **Tout conserver** pour une démonstration ultérieure, avec une date de réexamen.

**Recommandation (préliminaire)** : options 1, 2 et 3 ensemble, dans cet ordre (tâche, sauvegardes, conteneurs et volume, puis fichiers), si aucune autre démonstration n'est prévue : aucune donnée de démonstration ne reste sur le poste (pourquoi de DEC-008, R-05). À confirmer au moment de la décision.

**Impact** : irréversible ; plus de rollback ni de restauration ; images Docker `esn-reservation-coworking:<sha>` sans données (à supprimer ou non, sans enjeu de données personnelles) ; 0,5 h de Nadia ; trace dans `retex.md` (date, nom, résultat des contrôles, sans contenu).

## Critères d'acceptation
- [ ] Un humain a décidé quelles données supprimer ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [ ] Les suppressions décidées sont faites par un humain, avec les contrôles de l'architecture § 8 (étape 4) ; `docker volume ls` ne liste plus `esn-reservation-coworking_pgdata` si l'option 2 est retenue.
- [ ] La date, le nom de l'exécutant et le résultat des contrôles sont notés dans `retex.md`, sans contenu de données.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création (A_FAIRE, à présenter après la soutenance, DEC-008) ; affectation conditionnelle à l'allocation de Nadia proposée dans T-007 · 0 h
