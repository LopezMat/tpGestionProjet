---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-018
titre: Disponibilités et réservation (F-01)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4.75          # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-012, T-013, T-062]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-018 — Disponibilités et réservation (F-01)

## Description
F-01 « Consulter les disponibilités et réserver une salle » (Must), composant `api.reservations` de [architecture.md](../architecture.md) § 3 et § 4 : `GET /api/salles`, `GET /api/disponibilites?date=`, `POST /api/reservations`. Unicité garantie par la contrainte `UNIQUE` (409 « créneau indisponible ») et quota par `SELECT … FOR UPDATE` sur la ligne de l'utilisateur ; règles de T-012. L'annulation (et le critère « après annulation, une nouvelle réservation est acceptée ») est dans T-019. Les contrôles d'autorisation de toutes les routes sont vérifiés par la matrice de T-020 (revue humaine T-036).

## Critères d'acceptation
- *(Déplacé dans [T-054](T-054-api-consultation-disponibilites.md) le 2026-11-25 : `GET /api/salles` et `GET /api/disponibilites`. T-018 les place derrière l'authentification avec T-013 et T-020.)*
- [ ] **Horaires** : les créneaux proposés vont de 8 h-9 h à 19 h-20 h (12 par salle et par jour), du lundi au vendredi ; aucun créneau n'est proposé le samedi et le dimanche ; une réservation forcée hors de ces plages (appel direct à l'API) est refusée (test : 7 h-8 h, 20 h-21 h, samedi, dimanche refusés ; 8 h-9 h et 19 h-20 h un jour ouvré acceptés).
- [ ] **Unicité** : si deux membres réservent simultanément le même créneau de la même salle, une seule réservation est enregistrée et l'autre reçoit un message d'indisponibilité (test de concurrence à deux connexions sur PostgreSQL réel).
- [ ] **Limite quotidienne** : un membre a au plus 2 réservations actives pour une même date, toutes salles confondues ; la 3e est refusée avec un message explicite ; la limite d'un membre n'affecte pas un autre membre ; deux réservations simultanées du même membre sont sérialisées (tests).
- [ ] **Avance maximale** : date du jour + 14 jours acceptée, + 15 jours refusée avec message (H-10).
- [ ] Un créneau déjà commencé ou passé ne peut pas être réservé (refus avec message clair, H-11).
- [ ] Seul un membre connecté peut réserver ; la réservation est enregistrée au nom du membre connecté (identité tirée de la session, jamais d'un identifiant fourni dans la requête).
- [ ] Après la réservation, le créneau apparaît « occupé » pour tous les utilisateurs.
- [ ] **Instant de référence (constat 12, rapport securite-2026-11-25-3)** : le « maintenant » passé aux règles vient toujours de l'horloge injectée, jamais de la base (`SELECT now()`, `timestamptz` lu) ; un test d'API avec une horloge qui renvoie un instant en UTC refuse la réservation d'un créneau commencé.
- [ ] **Contrôle « date passée » dans `regles` (remarque 2 du relecteur sur T-062 ; rapport securite-2026-11-25-5, `api.py:127`)** : une fonction de `regles` (par exemple `verifier_pas_passee(jour, maintenant)`), fondée sur `_heure_murale`, décide si une date est passée ; `GET /api/disponibilites` (aujourd'hui `jour < maintenant.date()` en `api.py:127`) et `POST /api/reservations` l'utilisent, et aucune comparaison de date avec `maintenant.date()` ne reste dans `api.py` ; le code et le message d'erreur de la consultation (`date_passee`, 422) sont inchangés (tests : fonction de `regles` avec un instant en UTC à 23 h 30 Z la veille, soit 00 h 30 à Paris, où la veille de Paris est refusée et le jour de Paris accepté ; test d'API de la consultation existant toujours vert).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (règles métier ; les autorisations de toutes les routes sont revues avec T-020)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 09:30 · agent:coordinateur · consultation (`GET /api/salles`, `GET /api/disponibilites`, mesure de temps) détachée dans T-054 (priorité d'Ethan du 2026-11-25, option « Lecture seule ») ; estimation ramenée de 6 à 4,5 h · 0 h
- 2026-11-25 23:50 · agent:chef-de-projet · triage du rapport securite-2026-11-25-3 : dépend aussi de T-062 (constat 12, conversion du fuseau dans `regles`, à corriger avant ce ticket) ; critère ajouté sur l'instant de référence. Points de vigilance du `securite` pour ce ticket : verrou `SELECT … FOR UPDATE` du quota (H-12), contrôle de propriété et 404 identique pour l'annulation (T-019), interception de `ReglePasRespectee` seulement, jamais de `ValueError`. Temps compté dans T-008 · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage des remarques sur T-054 (relecteur-code, remarque 7 ; audit securite-2026-11-25-4) : `GET /api/disponibilites` renvoie « libre » les créneaux déjà commencés du jour J ; le refus de les réserver est couvert par le critère H-11 existant (à tester par appel direct à l'API, sans s'appuyer sur l'affichage) ; l'affichage « passé » est traité côté page dans T-055 (critère ajouté). Le message `date_hors_fenetre` (« réserver ») reste correct pour `POST /api/reservations` : seule sa version de consultation est reformulée (T-065). Aucun critère ni estimation modifiés. Temps compté dans T-008 · 0 h
- 2026-11-25 16:40 · agent:chef-de-projet · triage (S1-R5) de la remarque `api.py:127` (relecteur de T-062, remarque 2 ; rapport securite-2026-11-25-5 : sans risque réel, horloge en Europe/Paris) : critère ajouté (contrôle « date passée » déplacé dans `regles`, fondé sur `_heure_murale`) ; regroupé ici plutôt que dans T-065 (priorité basse, après les Must) parce que ce ticket écrit les contrôles de date semblables de `POST /api/reservations` et touche `api.py` et `regles.py` ; estimation 4,5 → 4,75 h. Temps compté dans T-008 · 0 h
