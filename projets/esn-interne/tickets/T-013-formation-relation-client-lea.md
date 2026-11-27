---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-013
titre: Formation Léa — relation-client en binôme avec Claire
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: salarie:lea        # agent:<nom> | salarie:<prenom>
competence_requise: relation-client (debutant)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
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

# T-013 — Formation Léa — relation-client en binôme avec Claire

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-07). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 7 de priorité** (premier retiré en cas de manque de capacité). **À terminer au plus tard le 2026-12-18** : la fenêtre se ferme avec `reservation-coworking`, et la formatrice (T-014) est à 0 % en P2. `tableau.py` le place après T-010 (en janvier), parce qu'il ordonne les tickets de Léa par priorité puis par id ; ce placement est un artefact, la date réelle est en P1.

- **Compétence** : `relation-client` ; **niveau actuel** : aucun ; **niveau visé à la fin de ce ticket** : débutant. Le niveau confirmé, exigé par AF1, demandera un projet complet en binôme.
- **Candidate** : Léa, pour en faire, avec T-006, une seconde personne capable de mener une recette avec le client (AF1 et règle 6 du `chef-de-projet`).
- **Formatrice** : Claire (temps compté dans [T-014](T-014-encadrement-relation-client-claire.md)).
- **Déclencheur** : DEC-009 point E (Claire seule interlocutrice client et seule recetteuse).
- **Modalité** : binôme interne. Léa suit, **avec l'accord de Claire, qui la présente au client**, au moins 2 échanges de fin de projet de `reservation-coworking` : par exemple l'information du client sur le budget (`T-094`, prévue le 2026-11-30, si DEC-024 est prise à temps), les points client (`T-009`), l'annonce du GO et de la mise en service (2026-12-15 et 16) ou le registre des demandes de suppression (`T-091`). Elle prépare chaque échange avec Claire et rédige un compte rendu.
  - **Claire reste seule interlocutrice et seule responsable** des échanges (AF1) ; Léa n'engage pas l'ESN et n'écrit rien dans le projet client.
- **Fenêtre unique** : du 2026-11-30 au 2026-12-18, la fin du seul projet client en cours.
- **Coût** : 3 h × 64,29 €/h = **192,86 €** ; formatrice : voir T-014 (78,57 €) ; frais externes : 0 €.

## Critères d'acceptation
- [ ] Léa a suivi au moins 2 échanges client avec Claire ; un compte rendu de chacun (sans donnée personnelle) est au journal.
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
- 2026-11-27 10:55 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-07 ; DEC-009 E) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 7) ; TERMINE au plus tard le 2026-12-18 (sinon, ticket decision : report au prochain contrat ou ANNULE) (T-016) · 0 h
