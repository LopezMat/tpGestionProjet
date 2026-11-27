---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-015
titre: Formation Claire — juridique (RGPD du sous-traitant, contrats, violations)
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: basse             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: juridique (debutant)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
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

# T-015 — Formation Claire — juridique (RGPD du sous-traitant, contrats, violations)

## Description
> **ANNULE le 2026-11-27 : non retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B).** Un besoin juridique est traité par un conseil externe, saisi au cas par cas sur décision humaine (comme pour `reservation-coworking/T-084`). Le risque R-08 (`juridique` absente) est accepté par DEC-024 ; il reste suivi au registre de [planning.md](../planning.md). Le fichier est conservé pour la traçabilité (jamais supprimé).

Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-08). Proposé par T-001, soumis à l'arbitrage de [T-017](T-017-decision-plan-formation-initial.md) (DEC-024). Retenu seulement dans l'option A ; l'option B, retenue, le remplace par un recours à un conseil juridique externe au cas par cas.

- **Compétence** : `juridique` ; **niveau actuel** : aucun dans l'ESN ; **niveau visé** : débutant, c'est-à-dire savoir qualifier une question juridique et décider quand saisir un conseil. Le niveau confirmé n'est pas réaliste par la formation seule.
- **Candidate** : Claire. Elle a déjà `rgpd` (confirmé), elle est l'interlocutrice des clients et elle porte les décisions (AF2).
- **Déclencheur** : DEC-009 point E (« `juridique` : compétence absente ; la mention RGPD est validée par le client ») ; `reservation-coworking/T-084` (notification CNIL tranchée sans avis juridique, DEC-019 v0.2).
- **Modalité** : formation externe d'une journée : obligations du sous-traitant (RGPD, art. 28), clauses contractuelles, violations de données (art. 33 et 34), mentions légales. Organisme et date à choisir ; session au plus tard le 2027-01-15.
- **Coût** :
  - temps salarié : 7 h × 78,57 €/h = **550,00 €** (compté par `tableau.py`) ;
  - frais externes : **provision de 700 € HT**, à confirmer par devis (enveloppe séparée de DEC-024, non comptée par `tableau.py`).

## Critères d'acceptation
- [ ] Claire a suivi la journée ; l'attestation de présence est mentionnée au journal.
- [ ] Une fiche réflexe d'une page « quand saisir un conseil juridique » est publiée dans `projets/esn-interne/`.
- [ ] Le temps passé et les frais externes réels sont reportés au journal ; le niveau atteint est proposé, puis décidé par un humain.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:05 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-08 ; DEC-009 E) ; retenu seulement dans l'option A de T-017 ; en attente de DEC-024 · 0 h
- 2026-11-27 14:00 · agent:chef-de-projet · A_FAIRE → ANNULE : non retenu par DEC-024 (option B) ; conseil juridique externe au cas par cas, sur décision humaine ; risque R-08 accepté (T-016) · 0 h
