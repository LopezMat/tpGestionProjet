---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-012
titre: Règles métier et horloge (F-01, F-02, F-08)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
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
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
