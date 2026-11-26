---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-082
titre: SIMULATION — Décision mise en maintenance pendant l'opération (T-080)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ATTENTE_HUMAIN      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: critique          # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine requise (S2-R4, coupure volontaire ou mise en maintenance)
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:gestionnaire-crise
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Exercice de crise (scénario 5, S2) demandé par l'humain le 2026-11-26, ticket incident [T-080](T-080-simulation-perte-base-production.md). Aucun événement réel : aucune commande Docker n'est exécutée ; `deploiement/local/` n'a été ni lu ni modifié par l'agent. Heures simulées.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-082 — SIMULATION — Décision mise en maintenance pendant l'opération (T-080)

## Description
Runbook [perte-donnees](../../../runbooks/perte-donnees.md) § 4, ligne « Mettre l'application en maintenance pendant l'opération ». Porteuse et exécutante (AF2) : Nadia, humaine d'exploitation (`docker` confirmé). Peut être tranchée **en même temps que [T-081](T-081-simulation-decision-restauration-base.md)** : elle ne dépend pas du choix de restauration, seulement de sa durée.

**Constat (SIMULATION).** L'application est déjà indisponible depuis 10:00. Sonde simulée, non exécutée : `python scripts/sonde_sante.py --url http://localhost:8080` rendrait `RESULTAT: INDISPONIBLE` (code 4). Deux cas sont possibles :
- les conteneurs ont été supprimés avec le volume, et le port ne répond plus ;
- l'app tourne encore sans base, et `/health` répond 503 `{"status": "ko"}`.

La stack n'a **pas de page de maintenance** : pas de reverse proxy, une seule image. « Maintenance » signifie donc ici **garder l'app arrêtée et interdire tout relancement** jusqu'au retour à la normale, avec un repli manuel de l'accueil.

**Question** : faut-il maintenir volontairement l'application arrêtée pendant la restauration ou la reconstruction ?

**Options**
- **(1) Oui, maintenance jusqu'au retour à la normale prouvé par la sonde.**
  - Nadia arrête ou laisse arrêté le service `app` (`docker compose -p esn-reservation-coworking -f deploiement/docker-compose.yml stop app`, étape 1 de la procédure du runbook).
  - Aucun `deployer_local.py` ni `rollback_local.py` ne tourne pendant ce temps : sur un volume absent, ils recréeraient une base vide sans alerte (voir T-081).
  - L'accueil tient les réservations du jour à la main (repli du runbook `coupure-serveur`) et les ressaisit après.
- **(2) Non : relancer tout de suite l'app sur une base vide.** Les migrations recréent le schéma et les 3 salles, mais **aucun compte n'existe** : personne ne peut se connecter tant que `init_accueil` n'a pas tourné. Tout compte ou toute réservation créé avant une restauration serait **écrasé** par `pg_restore --clean`, donc perdu une seconde fois. Aucun bénéfice pour les utilisateurs, risque de double saisie.

**Recommandation** : **(1)**. L'indisponibilité est déjà totale, et la maintenance ne fait que figer l'état pour que la restauration ou la reconstruction parte d'une base propre. Elle protège aussi les sauvegardes éventuelles : aucune exécution de l'outillage (déploiement, sauvegarde) ne doit en supprimer pendant la crise.

**Impact chiffré**
- **Durée de maintenance** depuis la décision :
  - environ **45 min** si T-081 retient (a) ou (b) ;
  - environ **1 h** si T-081 retient (c), jusqu'à une app qui répond avec un compte accueil, puis un service ouvert mais vide.
  - En tout depuis 10:00 : environ 1 h 45 à 2 h si les décisions sont prises avant 11:00.
- **Utilisateurs touchés** : tous les membres et l'accueil (quelques dizaines de comptes, H-05). Ils sont déjà touchés par la panne, la décision n'en ajoute aucun.
- **Coût** : Nadia 0,25 h (environ 16 €) ; accueil du client, tenue manuelle des réservations sur la durée de la maintenance (temps du client, hors budget ESN).
- **Communication** : le message 1 de [T-083](T-083-simulation-decision-communication-client.md) annonce la maintenance et l'heure de la prochaine information.

## Critères d'acceptation
- [ ] Un humain a tranché ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [ ] Si (1) : le journal note l'heure de début de la maintenance, l'état constaté par Nadia (`docker compose -p esn-reservation-coworking ps`, conteneurs présents ou absents, sans aucune valeur secrète) et l'heure de fin, qui est celle de la sonde `DISPONIBLE ET À JOUR` de T-081.
- [ ] Aucun `deployer_local.py` ni `rollback_local.py` n'a été lancé pendant la maintenance, sauf décision explicite de T-081 option (c) (vérifiable dans `historique.json`, constat humain).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 10:14 · agent:gestionnaire-crise · SIMULATION · création (ATTENTE_HUMAIN), runbook perte-donnees § 4 « maintenance », recommandation (1) maintenance jusqu'au retour à la normale · 0 h
