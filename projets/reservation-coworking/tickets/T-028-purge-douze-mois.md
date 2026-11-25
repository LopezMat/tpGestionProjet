---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-028
titre: Purge des réservations à 12 mois (F-08, Should)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-014, T-020, T-025, T-026]   # fin de tous les Must (DEC-009) ; couvre T-010 à T-026, dont T-011 et T-012
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-028 — Purge des réservations à 12 mois (F-08, Should)

## Description
**Should, abandonnable (DEC-009).** Décision (Ethan, 2026-11-24, DEC-009) : les Should sont planifiés après tous les Must et retirés, sans toucher aux Must, si la marge avant la deadline passe sous 2 jours ouvrés (règle d'abandon : [planning.md](../planning.md)). Ce ticket est le **second abandonné**, après T-027 : F-08 répond à une obligation RGPD du client, et son abandon demande de lui proposer une seconde livraison (point à porter par Claire, AF1). `depend_de` couvre la fin de tous les Must (T-010 à T-026) : T-014, T-020, T-025, T-026. S'il est abandonné, sa revue humaine [T-037](T-037-revue-humaine-t-028.md) passe aussi `ANNULE`.

F-08 « Conservation limitée des réservations » (obligation RGPD du client) ; composant `purge` de [architecture.md](../architecture.md) § 3 et § 4 et décision 12 : `DELETE FROM reservation WHERE date_creneau < :limite`, limite calculée par `regles` (T-012). Lancée au démarrage, toutes les 24 h par une tâche de fond, et sur demande par `python -m reservation.purge`. La même tâche supprime les sessions expirées. La cohérence des sauvegardes (dernier critère de F-08) est assurée par T-029. Option A2 (sortie de F-08 de la livraison) non retenue par DEC-009 : seul l'abandon sur alerte de marge s'applique.

**Touche la sécurité** (suppression de données personnelles) : revue humaine obligatoire (CDC § 8), ticket compagnon **T-037** (Karim).

## Critères d'acceptation
- [ ] Un traitement automatique (au démarrage, puis toutes les 24 h) supprime les réservations dont le créneau date de plus de 12 mois (H-13).
- [ ] Test sur jeu de données : une réservation datée de 12 mois et 1 jour est supprimée ; une réservation datée de 11 mois et 29 jours est conservée.
- [ ] Le traitement est exécutable sur demande (`python -m reservation.purge`, pour la recette) et il écrit une trace sans nom ni e-mail (nombre de lignes supprimées seulement) (test sur la sortie capturée).
- [ ] La même tâche quotidienne supprime les sessions expirées (test).
- [ ] Les sauvegardes ne conservent pas les données au-delà de leur rétention propre, cohérente avec ce délai : vérifié par T-029 (30 jours au plus, 14 jours pour les quotidiennes).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (suppression de données personnelles, CDC § 8 ; ticket compagnon T-037)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 09:00 · agent:chef-de-projet · marqué « Should, abandonnable » (Ethan, 2026-11-24, DEC-009) ; depend_de [T-011, T-012] → [T-014, T-020, T-025, T-026] (après tous les Must) ; temps compté dans T-008 · 0 h
