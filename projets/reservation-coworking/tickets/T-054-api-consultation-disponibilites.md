---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-054
titre: API de consultation des disponibilités (F-01, lecture seule)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 1.5            # heures équivalent humain
depend_de: [T-011, T-012]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-054 — API de consultation des disponibilités (F-01, lecture seule)

## Description
**Origine.** Changement de priorité d'Ethan du 2026-11-25 : développer d'abord le socle et la partie de F-01 réalisable sans authentification (option « Lecture seule »). La réservation reste dans [T-018](T-018-disponibilites-reservation.md), qui dépend de l'authentification (T-013). Ce ticket détache de T-018 la partie consultation : `GET /api/salles` et `GET /api/disponibilites?date=` (architecture § 3 et § 4, composant `api.reservations`), sur le modèle de T-011 et les règles de T-012.

**Caractère provisoire de l'accès.** En attendant T-013 et la matrice d'autorisation de T-020, ces deux routes répondent sans connexion. C'est un écart temporaire au CDC (F-04 : « toute page ou appel d'API de réservation sans connexion est refusé ») : T-013 et T-020 devront les placer derrière l'authentification. Les réponses ne contiennent aucune donnée personnelle.

## Critères d'acceptation
- [ ] `GET /api/salles` renvoie les 3 salles (nom ; capacité et équipements facultatifs).
- [ ] Pour une date donnée, `GET /api/disponibilites?date=AAAA-MM-JJ` renvoie pour chacune des 3 salles les créneaux d'une heure, chacun marqué « libre » ou « occupé », **sans aucun nom ni e-mail** d'occupant.
- [ ] **Horaires** : les créneaux renvoyés vont de 8 h-9 h à 19 h-20 h (12 par salle et par jour) du lundi au vendredi ; aucun créneau n'est renvoyé pour un samedi ou un dimanche (tests sur un jour ouvré, un samedi et un dimanche).
- [ ] Une réservation présente en base pour un créneau (insérée par le test) fait apparaître ce créneau « occupé » ; les autres restent « libres ».
- [ ] Une date invalide (format incorrect) renvoie une erreur 422 explicite, sans erreur serveur.
- [ ] Le temps de `GET /api/disponibilites` est mesuré en test d'intégration et reste sous 2 s (H-05).
- [ ] Le caractère provisoire de l'accès sans connexion est signalé dans le code (commentaire renvoyant à T-013 et T-020) et une ligne est ajoutée au journal de T-020 pour que la matrice d'autorisation couvre ces deux routes.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (lecture seule, aucune donnée personnelle ; les autorisations sont revues avec T-020, revue humaine T-036)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 09:30 · agent:coordinateur · création, détachée de T-018 (priorité d'Ethan du 2026-11-25, option « Lecture seule ») · 0 h
- 2026-11-25 10:00 · agent:dev-backend · prise en charge (T-011 et T-012 TERMINE, architecture et CDC VALIDÉS) ; lecture de DEC-011 et de l'audit securite-2026-11-25-3 · 0,2 h
- 2026-11-25 11:15 · agent:dev-backend · **touche la sécurité** (routes anonymes provisoires, DEC-011 ; aucune donnée de membre exposée). Réalisé : `app/reservation/api.py` (routeur, 2 routes, 404 JSON pour tout `/api/*` inconnu), `app.py` (routeur, gestionnaires d'erreurs JSON), `bdd.py` (`moteur_applicatif` : `pool_timeout=3`, `statement_timeout=5000`), tests `tests/test_api_consultation.py`, `tests/test_livraison.py` (le schéma contient les 2 routes), `docs/openapi.json` régénéré · 1,0 h
- 2026-11-25 11:30 · agent:dev-backend · conception : (1) `date` validée par regex AAAA-MM-JJ puis `date.fromisoformat` (ni timestamp ni datetime), 422 JSON `{erreur, message}` à message fixe, sans écho de la valeur ; (2) fenêtre J à J+14 : passé → 422 `date_passee`, au-delà → 422 `date_hors_fenetre` (`regles.verifier_avance`) ; (3) « maintenant » vient uniquement de `horloge` (Europe/Paris, dépendance `fournir_horloge`), jamais de la base ni d'UTC (constat 12 non corrigé ici) ; (4) samedi et dimanche : 200 avec 3 salles et `creneaux: []` ; (5) base indisponible, pool saturé ou délai dépassé → 503 JSON fixe sans détail, journal sans paramètre ; (6) la requête ne lit que `salle_id, heure_debut` (jamais `utilisateur_id` ni `reservation.id`) ; (7) accès au moteur paresseux, après validation du paramètre · 0 h
- 2026-11-25 11:40 · agent:dev-backend · tests : suite complète sous Python 3.14 (python:3.14-slim) avec PostgreSQL 16 jetable (`TEST_DATABASE_URL` vers `app_test`) : `python -m pytest -q -rs` → 140 passed, 0 skipped (intégration comprise) ; `test_schema_openapi_versionne_est_a_jour` vert avec `docs/openapi.json` régénéré (`REGENERER_OPENAPI=1`). Conteneurs et réseau d'essai supprimés (`apercu-*` non touchés) · 0,3 h
- 2026-11-25 11:45 · agent:dev-backend · couverture des critères (non cochés) : C1 `test_salles_renvoie_les_trois_salles` ; C2 `test_jour_ouvre_12_creneaux_par_salle_tous_libres` et `test_reservation_rend_le_creneau_occupe_sans_donnee_de_membre` (aucun nom, e-mail ni id) ; C3 les mêmes (12 créneaux de 8 h à 20 h) et `test_week_end_aucun_creneau` (samedi, dimanche) ; C4 `test_reservation_rend_le_creneau_occupe_sans_donnee_de_membre` (2 occupés, 34 libres, réservation d'un autre jour sans effet) ; C5 `test_date_invalide_422_sans_echo` (12 formes), `test_date_absente_ou_trop_longue_422`, `test_date_hors_fenetre_422` ; C6 `test_temps_de_reponse_sous_2_s_h05` (36 créneaux occupés) ; C7 **partiel** : commentaire PROVISOIRE renvoyant à T-013 et T-020 en tête de `api.py` (`test_acces_provisoire_signale_dans_le_code`) ; la ligne au journal de T-020 n'est **pas** écrite (je ne modifie que mon ticket, règle 8) : à faire par le coordinateur · 0 h
- 2026-11-25 11:50 · agent:dev-backend · points de l'audit : `moteur_applicatif()` seul (`test_les_routes_n_utilisent_pas_la_sonde`) ; `pool_timeout` 3 s traduit en 503 et `statement_timeout` 5 s ; constat 4 (`TrustedHostMiddleware`, « au plus tard avec T-054 ») **non traité** : il demande une liste d'hôtes autorisés (hôtes de l'aperçu et de la production locale), donc un choix de configuration à valider · 0 h
- 2026-11-25 11:50 · agent:dev-backend · livré pour revue ; aucun commit (consigne du coordinateur) · total 1,5 h
