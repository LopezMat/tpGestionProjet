---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-010
titre: Formation Léa — docker (autoformation et binôme avec Nadia)
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:lea        # agent:<nom> | salarie:<prenom>
competence_requise: docker (debutant)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-012]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-010 — Formation Léa — docker (autoformation et binôme avec Nadia)

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-05). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 6 de priorité**. Allocation de Léa à `esn-interne` : 10 % en P2 (0,7 h par jour ouvré), soit 10 jours ouvrés pour les 7 h : **c'est le ticket le plus tardif du plan** (fin projetée le 2027-01-14 pour une échéance au 2027-01-15, voir `planning.md`).

- **Compétence** : `docker` ; **niveau actuel** : aucun ; **niveau visé à la fin de ce ticket** : débutant, c'est-à-dire autonome sur les procédures écrites (monter un environnement, lire des journaux, arrêter et relancer un service). Le niveau confirmé demandera un déploiement réel en binôme sur un prochain projet.
- **Candidate** : Léa. Elle a la capacité, et un environnement de recette Docker (comme `reservation-coworking/T-044`) complète son rôle de recetteuse de secours (T-006).
- **Formatrice** : Nadia (temps compté dans [T-011](T-011-encadrement-docker-nadia.md)).
- **Déclencheur** : DEC-019 et DEC-021 (Nadia seule en `docker`, alors que toute la production de l'ESN est en Docker local, DEC-003) ; Nadia ne travaille pas le mercredi.
- **Modalité** :
  1. autoformation sur la documentation officielle de Docker et de Compose (images, conteneurs, volumes, réseaux, journaux) : 3 h ;
  2. binôme avec Nadia : 4 h. Léa monte **seule** un environnement de recette à partir du guide de [T-012](T-012-formation-documentation-nadia.md), puis Nadia la fait travailler sur les volumes, les journaux et l'arrêt propre. Jamais sur la production d'un client.
- **Fenêtre** : du 2026-12-30 au 2027-01-14 (après T-012, attendu le 2026-12-30 ; Nadia libérée de `reservation-coworking` après le 2026-12-18). Recalée le 2026-11-27 sur les allocations de P2 (T-016). Marge : 1 jour ouvré avant l'échéance ; si T-012 glisse, voir les leviers de `planning.md` (« Risques planning »).
- **Coût** : 7 h × 64,29 €/h = **450,00 €** ; formatrice : voir T-011 (192,86 €) ; frais externes : 0 €.

## Critères d'acceptation
- [ ] Léa a monté seule un environnement de recette à partir du guide de T-012 ; les étapes où le guide ne suffisait pas sont notées au journal et transmises à Nadia (T-011).
- [ ] Léa sait, devant Nadia, lister les conteneurs et les volumes, lire les journaux d'un service et arrêter l'environnement sans perdre de volume (attestation de Nadia au journal).
- [ ] Le niveau atteint est proposé ; la fiche de Léa est mise à jour par le coordinateur après décision humaine.
- [ ] Le temps passé (heures équivalent humain) est reporté au journal.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:40 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-05 ; DEC-019, DEC-021) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 6) ; fenêtre recalée sur P2 : 2026-12-30 → 2027-01-14 (Léa à 10 %, après T-012) (T-016) · 0 h
