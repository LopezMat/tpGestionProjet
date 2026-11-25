---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-012
titre: Règles métier et horloge (F-01, F-02, F-08)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 3            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-012 — Règles métier et horloge (F-01, F-02, F-08)

## Description
Module pur `regles` (sans base ni HTTP) et composant `horloge` injectable de [architecture.md](../architecture.md) § 3 et § 4 : règles de date et d'heure de F-01 (plages, avance, créneau commencé, quota), F-02 (délai d'annulation) et F-08 (date limite de purge), hypothèses H-10 à H-13, H-15, H-17. La garantie sous concurrence (contrainte `UNIQUE`, verrou de ligne) relève de T-018. Tests unitaires paramétrés, horloge remplacée dans les tests (CDC § 7).

## Critères d'acceptation
- [ ] `horloge` fournit « maintenant » en Europe/Paris (`zoneinfo` et `tzdata`), est injectée par dépendance FastAPI et remplaçable dans les tests ; aucune règle n'appelle `datetime.now()` directement.
- [ ] **Horaires (F-01)** : les créneaux vont de 8 h-9 h à 19 h-20 h (12 par salle et par jour), du lundi au vendredi ; 7 h-8 h, 20 h-21 h, samedi et dimanche sont refusés ; 8 h-9 h et 19 h-20 h un jour ouvré sont acceptés (tests paramétrés).
- [ ] **Avance maximale (F-01, H-10)** : date du jour + 14 jours acceptée, + 15 jours refusée (tests aux bornes).
- [ ] **Créneau commencé ou passé (F-01, H-11)** : refusé avec un message clair ; cas de bord à minuit et au changement de semaine.
- [ ] **Limite quotidienne (F-01, H-12)** : la règle refuse une 3e réservation active pour une même date, toutes salles confondues ; une réservation annulée ne compte plus.
- [ ] **Délai d'annulation (F-02, H-15)** : un membre annule jusqu'au début du créneau (réservation de 10 h-11 h annulable à 9 h 59, refusée à 10 h 00) ; l'accueil annule tant que le créneau n'est pas terminé.
- [ ] **Date limite de purge (F-08, H-13)** : même jour 12 mois plus tôt (29 février → 28 février) ; une réservation de 12 mois et 1 jour est à supprimer, une de 11 mois et 29 jours est conservée.
- [ ] Chaque refus a un message explicite en français ; couverture d'au moins 80 % des lignes de `regles` (architecture § 6).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25)
- **Commentaires** :
  Passe 1. Grille examinée : architecture (§ 3 `regles`/`horloge`, § 4 « Règles de date » et purge), lisibilité, duplication, erreurs, tests, sécurité de base, commits, périmètre. Aucun écart bloquant. Les quatre choix d'interprétation sont conformes : (a) créneau refusé si début <= maintenant = `maintenant >= date_creneau + heure_debut` de l'architecture § 4 et H-11 ; (b) purge `jour < limite` = `DELETE ... WHERE date_creneau < :limite` de l'architecture § 4 (12 mois et 1 jour supprimé, 11 mois et 29 jours conservé, exactement 12 mois conservé) ; (c) heure murale de Paris : correct tant que `maintenant` vient de l'horloge (Paris), aucun risque aux changements d'heure car les créneaux (8 h-20 h) ne tombent jamais dans l'heure sautée ou répétée (2 h-3 h) ; (d) quota reçoit un nombre de réservations actives : cohérent avec « annulation = suppression de la ligne » (architecture § 4) et avec le verrou de ligne de T-018.
  Remarques (non bloquantes, l'avis reste APPROUVÉ) :
  1. `regles.py:25` `_heure_murale` retire le fuseau sans le vérifier : un `datetime` en UTC passé par erreur serait comparé tel quel, sans erreur. Suggestion : convertir via `.astimezone(FUSEAU)` si `tzinfo` est présent, ou lever une erreur si `maintenant` est naïf/non-Paris. À traiter éventuellement dans T-018 qui appelle ces fonctions.
  2. `test_regles.py` : aucun test ne couvre explicitement un changement d'heure (dernier dimanche de mars/octobre). Un cas aux dates 2026-03-29 et 2026-10-25 (créneau de 8 h juste après) documenterait le choix « heure murale ».
  3. `test_regles.py:183` : l'assertion sur le texte source (`"now(" not in source`) est fragile ; le `monkeypatch` de `horloge.maintenant` ne prouve rien puisque `regles` n'importe pas `horloge`. Préférence de test, sans impact.
  4. `verifier_creneau_valide` accepte `heure_debut` entier uniquement ; la validation du type (rejet d'un flottant ou d'une chaîne) relève de la couche API (Pydantic), à vérifier dans T-018.
  5. Diff : fichiers livrés non commités (consigne du coordinateur), donc la vérification « commits préfixés T-012 » est en attente ; périmètre vérifié par `git status` : horloge.py, regles.py, test_regles.py sont les seuls fichiers T-012 (les autres modifiés/non suivis relèvent de T-011). Le commit préfixé `T-012` reste à faire par le coordinateur avant le passage du testeur.
  6. Les tests n'ont pas été relancés par le relecteur (Bash limité à git) ; le développeur annonce 75 passed, couverture `regles` 100 %. Vérification d'exécution laissée au testeur.
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 10:00 · agent:dev-backend · prise en charge (T-010 TERMINE, architecture et CDC VALIDÉS) · 0 h
- 2026-11-25 11:30 · agent:dev-backend · livré pour revue (non commité, consigne du coordinateur). Fichiers : app/reservation/horloge.py, app/reservation/regles.py, app/tests/test_regles.py. Aucun fichier partagé modifié (requirements, conftest, app.py intacts). Pas de « touche la sécurité ». Choix : refus = exception ReglePasRespectee (message français) ; créneau commencé : début <= maintenant refusé ; purge : créneau strictement antérieur à la date limite (exactement 12 mois conservé) ; comparaisons en heure murale de Paris ; le quota reçoit le nombre de réservations actives (l'appelant exclut les annulées, T-018). Tests : docker run python:3.14-slim, requirements-dev.txt + pytest-cov (installé à la volée, hors requirements), `pytest --cov=reservation.regles` : 75 passed, 13 skipped ; couverture regles 100 %, horloge 89 %. 3 échecs et 14 erreurs, tous dans test_migrations.py / test_demarrer.py = T-011 en cours, non traités. Couverture des critères : horloge/injection/pas de now() dans regles → test_horloge_paris_et_injection, test_regles_nappellent_pas_lhorloge ; horaires → test_creneaux_valides, test_creneaux_refuses, test_douze_creneaux_par_jour ; avance → test_avance_bornes ; créneau commencé → test_creneau_commence (minuit, changement de semaine) ; quota → test_quota, test_reservation_annulee_ne_compte_plus ; annulation → test_annulation ; purge → test_date_limite_purge, test_purge ; messages français → match sur les messages dans les tests ; couverture ≥ 80 % → 100 %. · 3 h
