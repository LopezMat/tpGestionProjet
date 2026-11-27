---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-004
titre: Formation Léa — revue humaine et securite-applicative (2/2) revues en double avec Karim
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:lea        # agent:<nom> | salarie:<prenom>
competence_requise: revue-humaine (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-003]          # ex. [T-001, T-002]
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

# T-004 — Formation Léa — revue humaine et securite-applicative (2/2) revues en double avec Karim

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registres R-02 et R-03). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 1 de priorité**. Suite de [T-003](T-003-formation-securite-autoformation-lea.md).

- **Compétences** : `revue-humaine` (méthode de S3-R2 : grille, indépendance, signature) et `securite-applicative` ; **niveau visé** : confirmé pour les deux, attesté par Karim, puis décidé par un humain.
- **Candidate** : Léa. **Formateur** : Karim (temps compté dans [T-005](T-005-encadrement-revue-securite-karim.md)).
- **Déclencheur** : DEC-021 (« Karim le seul en `securite-applicative` et en revue humaine ») ; `reservation-coworking/T-030` à `T-038`, `T-064`, `T-074`, `T-095` à `T-100` (toutes les revues humaines du projet sont de Karim).
- **Modalité** : binôme interne. Léa fait **en double** au moins 3 revues humaines réelles de Karim portant sur la sécurité, par exemple `reservation-coworking/T-064`, `T-074`, `T-097` ou `T-099`, fenêtre du 2026-12-07 au 2026-12-11 : elle relit seule avec sa grille, puis compare son avis à celui de Karim.
  - **Karim reste seul assigné et seul signataire** des revues du projet client ; Léa n'écrit rien dans les tickets clients. Ses notes vont au journal de ce ticket, sans secret.
  - Le binôme ne doit jamais retarder une revue sur le chemin critique de `reservation-coworking` (T-037, T-097 à T-099, GO du 2026-12-15) : Karim peut le suspendre.
- **Limite** : Karim est `confirme` (et non `expert`) en `securite-applicative`. Une relecture « un niveau en dessous en binôme avec un expert » (AF7) n'est donc pas possible : Léa ne relit seule qu'une fois `confirme` attesté. Ce ticket ne la rend pas relectrice des tickets `critique` `backend-python` (binôme AF5, registre R-12).
- **Échéance impérative** : attestation avant le **2026-12-18** (congés de Karim du 21 au 31/12, EV-003).
- **Coût** : 4 h × 64,29 €/h = **257,14 €** ; formateur : voir T-005 (157,14 €) ; frais externes : 0 €.

## Critères d'acceptation
- [ ] Au moins 3 revues humaines faites en double, citées au journal (id du ticket relu, avis de Léa, écart avec l'avis de Karim).
- [ ] Sur la dernière revue, l'avis de Léa ne manque aucun point bloquant relevé par Karim (attestation de Karim au journal).
- [ ] Le niveau atteint en `securite-applicative` et en `revue-humaine` est proposé ; la fiche de Léa est mise à jour par le coordinateur après décision humaine.
- [ ] Le temps passé (heures équivalent humain) est reporté au journal.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:10 · agent:chef-de-projet · création (T-001, plan de formation initial ; registres R-02, R-03 ; DEC-021) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 1) ; fenêtre inchangée (2026-12-07 → 2026-12-11), attestation avant le 2026-12-18 (T-016) · 0 h
