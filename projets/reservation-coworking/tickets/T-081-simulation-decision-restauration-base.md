---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-081
titre: SIMULATION — Décision restauration de la base de production (T-080)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: critique          # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine requise (S2-R4, restauration de données) ; préalable, vérification physique des dossiers de sauvegardes par Nadia
validation_humaine_requise: oui   # oui | non
decision:     DEC-019              # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:gestionnaire-crise
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:     2026-11-26             # facultatif : date du passage TERMINE
---
> **SIMULATION** — Exercice de crise (scénario 5, S2) demandé par l'humain le 2026-11-26, ticket incident [T-080](T-080-simulation-perte-base-production.md). Aucun événement réel : aucune commande Docker ni restauration n'est exécutée ; `deploiement/local/` n'a été ni lu ni modifié par l'agent. Heures simulées.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-081 — SIMULATION — Décision restauration de la base de production (T-080)

## Description
**Première décision à trancher** : elle conditionne la durée de la maintenance ([T-082](T-082-simulation-decision-mise-en-maintenance.md)), le second message au client ([T-083](T-083-simulation-decision-communication-client.md)) et l'évaluation CNIL ([T-084](T-084-simulation-decision-notification-cnil.md)). Runbook [perte-donnees](../../../runbooks/perte-donnees.md) § 4, ligne « Restaurer ». Porteuse et exécutante (AF2) : Nadia, seule salariée `sauvegarde-restauration` (confirmé), disponible aujourd'hui (jeudi).

**Contexte (SIMULATION).** Le 2026-11-26 à 10:00, le volume Docker `esn-reservation-coworking_pgdata` est supprimé. Les quatre tables (`utilisateur`, `salle`, `reservation`, `session`) sont perdues, et avec elles tous les comptes, toutes les réservations et toutes les sessions.

**Préalable, action humaine en lecture seule (à faire avant de trancher).** Nadia liste `deploiement/local/reservation-coworking/sauvegardes/` et `sauvegardes-quotidiennes/`, sans rien y supprimer. Pour le fichier le plus récent, elle relève le nom (horodatage), la taille et le résultat de `pg_restore --list <fichier>`, qui lit le fichier sans rien restaurer. Elle reporte ces valeurs au journal, sans aucun contenu de données. Elle note aussi le dernier SHA `EN LIGNE ET À JOUR` de `historique.json`, que la sonde utilisera pour prouver le retour à la normale. L'agent n'a pas pu faire ce constat : consigne de l'humain pendant la simulation, et Bash limité au diagnostic.

**Dernière sauvegarde utilisable**
- **Ce que promettent les règles** (DEC-003, DEC-007, DEC-008, [architecture.md](../architecture.md) § 8) :
  - la sauvegarde quotidienne du **2026-11-25 à 20:30** (`sauvegardes-quotidiennes/20261125-2030xx-quotidienne.dump`) ;
  - plus les `pg_dump` pris avant chacun des 10 derniers déploiements, de moins de 30 jours.
  
  La fenêtre de perte serait alors de 20:30 la veille à 10:00, soit 13 h 30. En pratique, ce sont les écritures du matin (ouverture à 8 h, donc environ 2 h d'activité) qui seraient perdues : l'app n'est joignable que depuis le poste (R-01) et l'espace est fermé la nuit.
- **Ce que les traces versionnées établissent** : **aucune sauvegarde.**
  - Aucun `rapports/deploiement-*.md`, donc aucune ligne « Sauvegarde » (porte 5, S3-R4).
  - T-046 (GO), T-047 (déploiement) et T-048 (mise en service, tâche planifiée) sont `A_FAIRE`.
  - T-029 (sauvegarde quotidienne) est `A_FAIRE`, et `scripts/sauvegarder_local.py` n'existe ni dans l'arbre ni dans l'historique Git (`git log --all -- scripts/sauvegarder_local.py` ne renvoie rien). Aucune sauvegarde quotidienne ne peut donc exister.
  - Les seuls dumps tracés ce jour (`rapports/test-rollback-2026-11-26.md`) appartiennent au projet jetable `esn-test-dd1be5ec`, détruit par le test (`down -v`). Ils ne contiennent pas les données du projet.
  - Un `pg_dump` d'avant déploiement n'existe que si au moins un second déploiement a eu lieu sur le volume existant : à la première mise en service, `deployer_local.py` écrit « aucune (première mise en service, aucune base existante) ».
- **Conclusion** : on ne peut parler de « dernière sauvegarde utilisable » qu'après le constat de Nadia. Sans fichier valide, la fenêtre de perte couvre **toutes les données depuis la mise en service**, dont la date n'est pas tracée.

**Effet de la suppression du volume sur la procédure du runbook.** La procédure « Restauration » du runbook suppose une base vivante. Ici, les conteneurs ont très probablement été supprimés avec le volume : Docker refuse de supprimer un volume utilisé, donc il y a eu `down -v` ou suppression après arrêt. Points à respecter :
1. **Ne pas lancer `deployer_local.py` ni `rollback_local.py`.** Le volume étant absent, le déploiement le traiterait comme une première mise en service, sans sauvegarde et sans alerte, et recréerait une base vide. L'app y appliquerait alors les migrations (schéma et 3 salles) puis accepterait des écritures qu'une restauration écraserait ensuite.
2. Recréer **seulement le service `db`** du projet compose `esn-reservation-coworking`, avec le mot de passe existant (`deploiement/local/reservation-coworking/db_password`). Au premier démarrage sur un volume vide, l'image `postgres` recrée le rôle `esn` et la base `app`, qui sont les cibles de `pg_restore -U esn -d app`. Garder l'image actuelle : la montée de version [T-078](T-078-image-postgresql-16-16.md) ne se fait pas pendant la crise.
3. Restaurer sur cette base vide avant tout démarrage de l'app. `--clean --if-exists` reste sans effet nuisible. La révision Alembic restaurée évite toute migration au démarrage.
4. Démarrer l'app. La purge de 12 mois est rejouée automatiquement ([architecture.md](../architecture.md) § 8, « Restauration »).
5. Rejouer les suppressions de comptes demandées depuis l'heure de la sauvegarde, à partir du registre du client (responsable du traitement), par l'accueil.
6. Si [T-058](T-058-role-applicatif-non-superutilisateur.md) a été réalisé entre-temps (il ne l'est pas : `A_FAIRE`), recréer le rôle applicatif avant la restauration.

Ce cas manque au runbook : proposition P-1 du post-mortem.

**Question** : quelle stratégie de restauration de la base de production faut-il appliquer ?

**Options**
- **(a) Restaurer intégralement la sauvegarde valide la plus récente** trouvée par Nadia, puis appliquer les étapes 2 à 5 ci-dessus. On perd les écritures faites entre l'heure du fichier et 10:00. Les sessions de la sauvegarde sont restaurées : des sessions fermées depuis redeviennent valides jusqu'à leur expiration (12 h au plus).
- **(b) Restauration partielle : tout sauf les données de `session`**, par `pg_restore -l` puis `-L` avec la ligne `TABLE DATA session` mise en commentaire. Comptes, salles et réservations sont restaurés ; personne n'a de session et chacun se reconnecte. C'est l'adaptation de l'option (b) du runbook : une restauration « par tables » n'a de sens ici que pour écarter `session`, puisque toutes les tables sont perdues.
- **(c) Ne pas restaurer, reconstruire.** C'est l'option **imposée si aucune sauvegarde valide n'existe**, et elle suit l'ordre ci-dessous :
  1. Base neuve : le service `db` est recréé, puis un nouveau déploiement de l'image en ligne passe par un GO humain. Les migrations recréent le schéma et les 3 salles.
  2. Compte accueil initial par `init_accueil`, selon la procédure de l'architecture § 7 (comme dans T-048).
  3. L'accueil recrée les comptes membres (mot de passe temporaire, changement obligatoire).
  4. Les membres ressaisissent leurs réservations à venir.
  
  Les données sont définitivement perdues.
- (d) Récupération sur le disque (le volume supprimé se trouvait dans le disque virtuel de Docker Desktop) : **écartée**. Les chances sont faibles, le coût élevé, et elle demande une compétence absente de l'équipe.

**Recommandation** : **(b) si Nadia trouve une sauvegarde valide** (`pg_restore --list` sans erreur), sinon **(c)**. Les traces versionnées rendent (c) probable. (b) plutôt que (a), parce qu'on ne réactive aucune session qu'un utilisateur aurait fermée depuis la sauvegarde, pour un coût nul : il suffit de se reconnecter.

**Impact chiffré**
| | (a) ou (b) | (c) |
|---|---|---|
| Données perdues | écritures entre l'heure de la sauvegarde et 10:00 (si la quotidienne du 2026-11-25 à 20:30 existait : environ 2 h d'activité du matin) | **toutes** : comptes (quelques dizaines de membres, H-05, et les comptes accueil), réservations à venir (au plus 36 créneaux par jour sur J à J+14, soit 540 au maximum), sessions |
| Indisponibilité supplémentaire, après la décision | environ 45 min : recréation de `db` 10 min, restauration de quelques Mo moins de 5 min, démarrage et contrôles 15 min, sonde 5 min, rejeu des suppressions 10 min | environ 1 h avant que l'app réponde avec un compte accueil (déploiement après GO, `init_accueil`) ; ensuite, service ouvert mais vide jusqu'à la ressaisie |
| Utilisateurs touchés | tous (reconnexion en (b)) | tous : comptes à recréer, environ 3 min par compte pour l'accueil (environ 1 h 30 pour 30 comptes, temps du client), réservations à ressaisir |
| Coût ESN | Nadia environ 1,5 h (64,29 €/h, soit environ 96 €) et Karim 0,5 h de contrôle de cohérence (78,57 €/h, soit environ 39 €) | Nadia environ 1,5 h (environ 96 €) et nouveau GO à présenter (Claire, 0,25 h, environ 20 €) |
| Risque RGPD | comptes supprimés sur demande depuis l'heure de la sauvegarde **réintroduits** jusqu'au rejeu : registre du client indispensable | aucun compte réintroduit |

## Critères d'acceptation
- [x] Le constat de Nadia figure au journal : fichiers présents ou absents dans les deux dossiers, nom, horodatage et taille du plus récent, résultat de `pg_restore --list`, dernier SHA vérifié de `historique.json`. Aucun contenu de données n'y figure.
- [x] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [x] La restauration ou la reconstruction décidée est exécutée par Nadia selon les étapes ci-dessus. Le journal donne la sauvegarde utilisée (ou « aucune »), l'heure et la fenêtre de perte.
- [x] Le contrôle de cohérence est noté (Karim, `base-de-donnees-sql`) : nombre de lignes par table, 3 salles, au moins un compte accueil, aucune réservation de plus de 12 mois (purge rejouée).
- [x] Les suppressions de comptes postérieures à la sauvegarde sont rejouées d'après le registre du client, ou l'absence de registre est notée.
- [x] La sonde `python scripts/sonde_sante.py --url http://localhost:8080 --sha <dernier SHA vérifié>` rend `DISPONIBLE ET À JOUR`, et sa sortie est collée au journal de T-080.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet. La décision est humaine (R7) ; le contrôle de cohérence de Karim fait partie des critères.
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 10:13 · agent:gestionnaire-crise · SIMULATION · création (ATTENTE_HUMAIN), runbook perte-donnees § 4 « Restaurer », options (a) à (d), recommandation (b) si une sauvegarde valide existe, sinon (c) · 0 h
