---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-027
titre: Fiches des salles (F-06, Should)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: html-css (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-014, T-020, T-025, T-026]   # fin de tous les Must (DEC-009) ; couvre T-010 à T-026, dont T-018 et T-023
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-027 — Fiches des salles (F-06, Should)

## Description
**Should, abandonnable (DEC-009).** Décision (Ethan, 2026-11-24, DEC-009) : les Should sont planifiés après tous les Must et retirés, sans toucher aux Must, si la marge avant la deadline passe sous 2 jours ouvrés (règle d'abandon : [planning.md](../planning.md)). Ce ticket est le **premier abandonné** (le moins utile à la mise en ligne). `depend_de` couvre la fin de tous les Must (T-010 à T-026) : T-014, T-020, T-025, T-026. S'il est abandonné, il passe `ANNULE` et T-042, T-043 et T-045 n'en dépendent plus (une dépendance `ANNULE` est satisfaite).

F-06 « Fiches des salles » : affichage du nom, de la capacité et des équipements sur l'écran de réservation, à partir de `GET /api/salles` (T-018) et de la table `salle` (T-011, décision 15 de l'architecture). Valeurs du client recueillies par T-009 ; à défaut, « Salle 1/2/3 » (H-20).

## Critères d'acceptation
- [ ] Chacune des 3 salles affiche son nom, sa capacité et ses équipements sur l'écran de réservation.
- [ ] Les valeurs affichées sont celles fournies par le client (Q-15, T-009) ; à défaut, seul le nom provisoire « Salle 1/2/3 » est affiché.
- [ ] Modifier ces informations ne nécessite pas de changer le code des réservations : la procédure (migration de données ou requête d'exploitation sur la table `salle`) est documentée dans le README de l'app.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 09:00 · agent:chef-de-projet · marqué « Should, abandonnable » (Ethan, 2026-11-24, DEC-009) ; depend_de [T-018, T-023] → [T-014, T-020, T-025, T-026] (après tous les Must) ; temps compté dans T-008 · 0 h
- 2026-11-26 22:00 · agent:chef-de-projet · SIMULATION · A_FAIRE → ANNULE : F-06 (Should) abandonné par DEC-020 (révision du budget à 4 200 € HT, scénario B en gardant F-08) ; retiré de depend_de de T-042, T-043 et T-045 ; sa revue de code (0,5 h) retirée de T-040 et son critère de recette retiré de T-045 ; à reprendre seulement par une nouvelle demande du client (CDC v1.1 à venir). Temps compté dans T-008 · 0 h
