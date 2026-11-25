---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-062
titre: Instant hors fuseau de Paris non converti dans « regles » (constat 12)
projet: reservation-coworking
type: bug                   # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE           # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 1.5            # heures équivalent humain
depend_de: [T-012]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le: 2026-11-25                   # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-25         # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-062 — Instant hors fuseau de Paris non converti dans « regles » (constat 12)

## Description
Constat 12 (bas) du rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), qui recoupe les remarques 1, 2 et 3 du `relecteur-code` sur [T-012](T-012-regles-metier-horloge.md). `regles._heure_murale` (`app/reservation/regles.py:24-26`) retire le fuseau **sans convertir** : un `maintenant` avec fuseau, exprimé dans un autre fuseau que Paris, est comparé comme une heure de Paris. Le défaut est latent (aucun appelant aujourd'hui), mais T-018 et T-019 l'exposeraient : psycopg renvoie un `timestamptz` dans le fuseau de la session (`Etc/UTC` par défaut dans l'image `postgres`). La règle F-02 (H-15) et la règle « créneau commencé » de F-01 (H-11) seraient alors contournées. **À corriger avant T-018**, qui en dépend désormais.

- **Étapes de reproduction** (constatées par le `securite` au commit `2852fe7`, Python 3.14) : un jour ouvré, à 10 h 30 heure de Paris, appeler `verifier_annulation` pour un créneau de 10 h-11 h, par un membre, avec `maintenant` égal au même instant exprimé en UTC (09 h 30 UTC).
- **Résultat attendu** : refus (créneau commencé), comme avec `maintenant` exprimé en heure de Paris.
- **Résultat obtenu** : annulation acceptée ; de même, réservation possible d'un créneau commencé depuis 1 à 2 h.
- **Environnement** : `app/` au commit `2852fe7`, tests unitaires (aucune base).

Le même ticket traite la remarque 3 de T-012 (même fichier `tests/test_regles.py`), pour éviter deux reprises successives du même fichier.

## Critères d'acceptation
- [x] `_heure_murale` convertit un instant avec fuseau en heure de Paris (`astimezone(horloge.FUSEAU)`) avant de retirer le fuseau ; un instant sans fuseau lève une erreur de programmation explicite, distincte de `ReglePasRespectee` (test).
- [x] Test du cas reproduit : à 10 h 30 heure de Paris exprimé en UTC, l'annulation par un membre du créneau de 10 h est refusée, et la réservation de ce créneau aussi ; mêmes résultats qu'avec l'instant exprimé en heure de Paris.
- [x] Tests au changement d'heure (remarque 2 de T-012) : le lundi 2026-03-30 et le lundi 2026-10-26, avec `maintenant` exprimé en UTC, le créneau de 8 h est « non commencé » à 7 h 59 heure de Paris et « commencé » à 8 h 00 heure de Paris.
- [x] `test_regles_nappellent_pas_lhorloge` (remarque 3 de T-012) est remplacé par un test qui échoue réellement si une règle lit l'horloge système (par exemple un double de `datetime` dans l'espace de noms de `regles` qui lève une erreur sur `now` ou `today`) ; l'assertion sur le texte source est retirée.
- [x] Couverture de `regles` d'au moins 80 % ; suite complète verte.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : APPROUVÉ (2026-11-25)
- **Commentaires** :
  Passe 1 (commit 16282cc). Grille examinée : architecture, lisibilité, duplication, erreurs, tests au niveau du § 7, sécurité de base, commits préfixés T-062, périmètre (seuls `app/reservation/regles.py`, `app/tests/test_regles.py` et le ticket sont touchés). Aucun écart bloquant. Remarques, sans effet sur l'avis :
  1. `app/reservation/regles.py:3-4` : le docstring de module dépasse la largeur des autres lignes (ligne 4 d'environ 130 caractères, coupure de ligne mal placée). À recouper au prochain passage sur le fichier.
  2. `app/reservation/api.py:127` : `jour < maintenant.date()` lit la date de l'instant tel que fourni par l'horloge, sans passer par `_heure_murale`. C'est correct tant que l'horloge est celle de `horloge.py` (aware, Europe/Paris, `FUSEAU`), mais ça reproduit le défaut corrigé ici si un test ou un appelant injecte un instant en UTC. À reprendre avec la route de consultation, ou à porter dans `regles` (par exemple une fonction `verifier_pas_passee`) lorsque T-018 y touchera. Pas de régression aujourd'hui.
  3. `TypeError` sur un instant naïf : choix justifié (pas d'hypothèse de fuseau) et bien distinct de `ReglePasRespectee` (qui hérite de `ValueError`, `TypeError` n'en hérite pas). Effet sur les appelants : `api.py` reçoit toujours un instant aware de `horloge()`, donc aucun changement ; T-018 devra ne pas intercepter `TypeError` avec les refus métier et le laisser remonter en erreur 500 (message générique, sans détail). Un `maintenant` naïf injecté dans un test d'API donnerait une 500, ce qui est voulu.
  4. `test_regles_nappellent_pas_lhorloge` : le double couvre `datetime.now/today/utcnow` et `date.today` dans l'espace de noms de `regles`, avec un garde-fou qui prouve qu'il est actif. Il ne verrait pas un appel indirect (par exemple `horloge.maintenant()` importé dans `regles`). Acceptable : `regles` n'importe que `FUSEAU` de `horloge`, et le test qui l'interdirait serait redondant avec la relecture.
  5. Tests : le dimanche du changement d'heure (2026-03-29 et 2026-10-25) ne vérifie que la conversion et un instant du soir. Aucun test à l'heure ambiguë (2026-10-25 entre 02 h et 03 h Paris, `fold`). Sans conséquence ici (créneaux du lundi au vendredi de 8 h à 20 h), seulement noté.
  Points vérifiés : `astimezone(horloge.FUSEAU)` correct à toute date (zoneinfo) ; `verifier_avance` passe par `_heure_murale` (jour de Paris, cas 23 h 30 UTC testé) ; garde `tzinfo is None or utcoffset() is None` couvre aussi un tzinfo dégénéré ; les 4 fonctions publiques à `maintenant` testées sur l'instant naïf ; cas du constat 12 testé en UTC et en heure de Paris (annulation, réservation, créneau commencé, accueil) ; tests 7 h 59 / 8 h 00 les lundis 2026-03-30 et 2026-10-26 (décalages UTC+2 et UTC+1 corrects) ; test de l'horloge sans assertion sur le texte source. Je n'ai pas relancé les tests (Bash limité à git) : je m'appuie sur le journal (55 passed dans `test_regles.py`, couverture 100 %), à confirmer par le `testeur`.
- **Revue humaine requise** : non (règle métier pure, comme T-012 ; ni authentification ni données personnelles)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage du constat 12 et des remarques 1, 2 et 3 de T-012) ; T-018 en dépend désormais · 0 h
- 2026-11-26 00:05 · agent:dev-backend · prise en charge (T-012 TERMINE, architecture et CDC VALIDÉS) · 0 h
- 2026-11-26 00:40 · agent:dev-backend · décision : un instant naïf lève TypeError (erreur de programmation, distincte de ReglePasRespectee), sans hypothèse de fuseau. Justification : deviner Paris rouvrirait le défaut du constat 12 pour tout appelant qui oublie le fuseau ; l'horloge (T-054) et psycopg fournissent toujours des instants aware, donc aucun appelant légitime n'est touché. `verifier_avance` utilisait aussi `maintenant.date()` sans conversion (même défaut, jour décalé de 0 h à 1-2 h) : corrigé via `_heure_murale`. Pas de « touche la sécurité » (règle métier pure) · 0 h
- 2026-11-26 01:15 · agent:dev-backend · livré pour revue (non commité, consigne du coordinateur). Fichiers : app/reservation/regles.py (import FUSEAU, `_heure_murale` en astimezone + TypeError si naïf, `verifier_avance` converti), app/tests/test_regles.py (7 tests ajoutés/remplacés, plus l'import UTC ; `inspect` retiré). Aucun autre fichier. Tests : docker python:3.14-slim + PostgreSQL 16 jetable (base coworking_test), pytest-cov installé à la volée. `tests/test_regles.py` : 55 passed ; couverture `reservation.regles` 100 % (49 lignes, 0 manquante). Suite complète : au premier lancement 135 passed / 48 failed, tous en 400 (contrôle de Host de T-063 en cours : app.py modifié et tests/test_en_tetes_hote.py non suivi, non traités) ; relancée sur une copie jetable avec app.py de HEAD et sans le test de T-063 : 145 passed, 4 failed (test_livraison : Dockerfile, docs, env.example absents de ma copie partielle, artefact de la copie, pas du code). Couverture des critères : (1) conversion + TypeError distinct → test_instant_naif_erreur_de_programmation (4 fonctions), test_instant_utc_accueil_et_avance (avance convertie) ; (2) cas reproduit → test_instant_utc_equivalent_a_paris_creneau_commence (UTC et Paris, annulation, réservation, créneau commencé) ; (3) changement d'heure → test_changement_d_heure_creneau_de_8h (lundi 2026-03-30 et 2026-10-26, 7 h 59 / 8 h 00 Paris exprimés en UTC) et test_dimanche_du_changement_d_heure_converti (2026-03-29, 2026-10-25) ; (4) remarque 3 → test_regles_nappellent_pas_lhorloge réécrit : doubles de datetime/date dans l'espace de noms de regles, now/today/utcnow lèvent, garde-fou vérifiant que le double est actif, assertion sur le source retirée ; (5) couverture 100 % ≥ 80 %. Conteneurs et réseau d'essai supprimés ; images postgres:16 et python:3.14-slim conservées (déjà utilisées par ailleurs) · 1.5 h
- 2026-11-25 16:10 · agent:testeur · vérifié sur le SHA 16282cc9dfe9e10af529ebf607d579961c52e9ae (arbre de `app/` propre, extrait par git archive ; python:3.14-slim 3.14.10 + PostgreSQL 16 jetable `app_test`) : suite complète 183 passed, 0 échec ; `tests/test_regles.py` 55 passed ; couverture `reservation.regles` 100 % (49 lignes, 0 manquante, pytest-cov installé dans le conteneur seulement). Preuves par critère, avec mutations sur copie jetable : (1) `_heure_murale` en `astimezone(FUSEAU)` lu ; sans la conversion, 4 tests échouent ; `TypeError` sur instant naïf testé pour les 4 fonctions (`test_instant_naif_erreur_de_programmation`), sans la garde 4 échecs ; (2) `test_instant_utc_equivalent_a_paris_creneau_commence` vert, rouge sans conversion ; (3) `test_changement_d_heure_creneau_de_8h` (lundis 2026-03-30 et 2026-10-26, 7 h 59 / 8 h 00 Paris en UTC) et `test_dimanche_du_changement_d_heure_converti` verts, rouges sans conversion ; (4) `test_regles_nappellent_pas_lhorloge` : plus d'assertion sur le source (aucun `inspect`/`getsource` dans le fichier), et il échoue réellement quand j'ajoute `datetime.now()` dans `regles` (1 échec) ; (5) 100 % ≥ 80 %, suite verte. Avis APPROUVÉ, revue humaine non requise. vérifié : 5/5 critères, suites vertes, SHA 16282cc → TERMINE · 0.5 h
- 2026-11-25 16:20 · agent:securite · audit sécurité : NON BLOQUANT, rapport [securite-2026-11-25-5.md](../rapports/securite-2026-11-25-5.md), commit `16282cc`. Constat 12 **fermé** : cas rejoué (10 h 30 Paris exprimé en UTC, annulation par un membre du créneau de 10 h) refusé, comme en heure de Paris ; réservation refusée ; UTC−5, minuit et changements d'heure corrects ; instant naïf → `TypeError`. `api.py:127` : pas de risque réel (horloge toujours en Europe/Paris, route en lecture seule) ; recommandation de cohérence : déplacer le contrôle « date passée » dans `regles` avant T-018. Temps compté dans T-043 · 0 h
