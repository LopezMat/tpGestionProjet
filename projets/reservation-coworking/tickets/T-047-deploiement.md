---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-047
titre: Déploiement en production locale
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:deployeur    # agent:<nom> | salarie:<prenom>
competence_requise: ci-cd (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-046, T-029]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-047 — Déploiement en production locale

## Description
Ticket « Déploiement » du `deployeur` (portes 4 à 8 de S3, R13) : `python scripts/deployer_local.py --projet reservation-coworking --sha <sha du GO>` (sauvegarde, build de l'image au SHA, lancement, `verifier-prod`), confirmé par un humain ; rollback par `rollback_local.py` en cas d'échec de vérification. Production locale Docker (DEC-003), `url_prod: http://localhost:8080`. Dépend de T-029 : le déploiement applique la limite d'âge de 30 jours et le message « Limite d'âge » annoncés dans la page de confidentialité (DEC-007, DEC-008). Avant la soutenance, les images `python:3.14-slim` et `postgres:16-alpine` sont préchargées (ARCHITECTURE § 9).

## Critères d'acceptation
- [ ] Les portes 1 à 4 sont franchies et consignées dans le rapport : tickets de réalisation `TERMINE`, rapports de tests, de sécurité et de recette sur le SHA du GO, décision de GO qui cite ce SHA.
- [ ] `rapports/deploiement-AAAA-MM-JJ.md` existe, avec les lignes `SAUVEGARDE`, `IMAGE`, `ETAT_VERIFICATION` et `RESULTAT`.
- [ ] `verifier-prod` a constaté que le SHA en ligne sur `/health` est le SHA attendu (S3-R5).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (déploiement)
- **Commentaires** :
- **Revue humaine requise** : non (le GO humain T-046 précède)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
