---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-008
titre: Formation Karim — sauvegarde-restauration (restauration réelle en binôme avec Nadia)
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: sauvegarde-restauration (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
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

# T-008 — Formation Karim — sauvegarde-restauration (restauration réelle en binôme avec Nadia)

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-04). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 2 de priorité**. Allocation de Karim à `esn-interne` : 10 % en P2 (0,7 h par jour ouvré), appliquée par le coordinateur le 2026-12-21. Avec cette allocation, les 5 h tiennent du 2027-01-04 au 2027-01-13, à condition que T-012 soit `TERMINE` au plus tard le 2026-12-31 (projection dans `planning.md`).

- **Compétence** : `sauvegarde-restauration` (avec les commandes `docker` qu'elle demande : volumes, `compose exec`) ; **niveau actuel** : aucun ; **niveau visé** : confirmé, attesté par Nadia, puis décidé par un humain.
- **Candidat** : Karim. Il est expert `base-de-donnees-sql` (PostgreSQL), ce qui raccourcit la formation, et il travaille le mercredi, jour où Nadia ne travaille pas.
- **Formatrice** : Nadia (temps compté dans [T-009](T-009-encadrement-sauvegarde-nadia.md)).
- **Déclencheur** : DEC-019 (crise T-080 : « une règle sans preuve d'exécution n'est pas une garantie » ; dépendance à une seule personne pour la restauration) ; DEC-009 point E ; DEC-021.
- **Modalité** : binôme interne, dans une **base jetable**, jamais sur une production :
  1. lecture du runbook `perte-donnees`, des scripts de sauvegarde et du guide de [T-012](T-012-formation-documentation-nadia.md) (1 h) ;
  2. commandes Docker utiles à la restauration (1 h) ;
  3. **restauration complète faite par Karim seul**, en suivant le runbook et le guide, Nadia en observatrice, durée mesurée (2 h) ;
  4. retour d'expérience : écarts entre la procédure écrite et la réalité, transmis à Nadia (1 h).
- **Fenêtre** : du 2027-01-04 au 2027-01-13 (retour de congés de Karim ; après T-012). Ce report après le 2026-12-18 ne coûte que 3 jours ouvrés de couverture (du 16 au 18/12), puisque Karim est en congés du 21 au 31/12, et il libère Karim et Nadia pendant la semaine du GO de `reservation-coworking`.
- **Indépendance** : Karim reste relecteur humain possible des tickets de sauvegarde de Nadia ; il n'en devient pas l'auteur.
- **Coût** : 5 h × 78,57 €/h = **392,86 €** ; formatrice : voir T-009 (128,57 €) ; frais externes : 0 €.

## Critères d'acceptation
- [ ] Karim a restauré seul une sauvegarde dans une base jetable, en suivant le runbook ; la durée et le résultat (nombre de lignes par table, contrôle d'intégrité) sont notés au journal, sans donnée personnelle.
- [ ] Les écarts entre la procédure écrite et la réalité sont listés au journal et transmis à Nadia (T-009).
- [ ] Nadia atteste au journal le niveau atteint (atteint ou non, avec la raison).
- [ ] Le niveau atteint est proposé ; la fiche de Karim est mise à jour par le coordinateur après décision humaine.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:30 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-04 ; DEC-019, DEC-009 E) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 2) ; fenêtre inchangée (2027-01-04 → 2027-01-13). La date du 2027-01-26 affichée par TABLEAU.md vient de l'allocation de P1 (5 %) appliquée sur toute la durée : artefact jusqu'à la bascule P2 du 2026-12-21 (T-016) · 0 h
