---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-006
titre: Formation Léa — recette-fonctionnelle en binôme avec Claire
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:lea        # agent:<nom> | salarie:<prenom>
competence_requise: recette-fonctionnelle (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-017]          # ex. [T-001, T-002]
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

# T-006 — Formation Léa — recette-fonctionnelle en binôme avec Claire

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-06). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 5 de priorité**. À terminer **au plus tard le 2026-12-18** : la formatrice (T-007) n'a plus d'allocation à `esn-interne` en P2.

- **Compétence** : `recette-fonctionnelle` ; **niveau actuel** : aucun ; **niveau visé** : confirmé, attesté par Claire, puis décidé par un humain.
- **Candidate** : Léa. Elle n'est l'auteure d'aucun ticket de `reservation-coworking`, condition d'un recetteur (règle 6 du `chef-de-projet`, S3-R1), et son expérience `accessibilite` et `html-css` la place du côté de l'utilisateur.
- **Formatrice** : Claire (temps compté dans [T-007](T-007-encadrement-recette-claire.md)).
- **Déclencheur** : DEC-009 point E (« Claire seule ; un empêchement bloquerait la recette, donc le GO ») ; `reservation-coworking/T-045` (recette de la livraison).
- **Modalité** : binôme interne pendant la recette réelle de `reservation-coworking/T-045`, prévue du 2026-12-10 au 2026-12-15 : lecture du skill `recette` et du CDC (1 h), puis exécution d'au moins 2 parcours aux côtés de Claire (3 h).
  - **Claire reste seule recetteuse et seule signataire** du rapport `rapports/recette-*.md` (R16) ; Léa n'écrit rien dans le projet client, ses constats passent par Claire.
  - La recette est sur le chemin critique (GO le 2026-12-15, 2 jours ouvrés de marge) : Claire peut réduire ou suspendre le binôme à tout moment.
- **Fenêtre unique** : c'est la seule recette prévue dans l'ESN avant le prochain contrat.
- **Coût** : 4 h × 64,29 €/h = **257,14 €** ; formatrice : voir T-007 (78,57 €) ; frais externes : 0 €.

## Critères d'acceptation
- [ ] Léa a exécuté au moins 2 parcours de recette avec Claire ; les parcours (sans donnée personnelle) et ses constats sont notés au journal.
- [ ] Claire atteste au journal le niveau atteint (atteint ou non, avec la raison).
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
- 2026-11-27 10:20 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-06 ; DEC-009 E) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 5) ; fenêtre inchangée (pendant T-045, 2026-12-10 → 2026-12-15), au plus tard le 2026-12-18 (Claire à 0 % en P2) (T-016) · 0 h
