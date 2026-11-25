---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-050
titre: Modification de règle R17 (écritures Markdown par Edit/Write uniquement)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur la règle R17 et le durcissement de restreindre_bash.py (R11)
validation_humaine_requise: oui   # oui | non
decision:        DEC-010           # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:    2026-11-25             # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-050 — Modification de règle R17 (écritures Markdown par Edit/Write uniquement)

## Description
Point d'arrêt humain « modification d'une règle » (R7, R11), issu du tri de [T-006](T-006-ecritures-md-par-edit-uniquement.md) (`amelioration`, incident du 2026-11-24 sur DEC-007, voir [retex.md](../retex.md)). Analyse rédigée par le `chef-de-projet` ; porteur salarié (AF2) : Karim, lead développeur et seul `securite-applicative` de l'équipe, binôme de la réalisation (T-051). La validation formelle reste humaine (R5). **Affectation conditionnelle** à l'allocation de Karim proposée dans T-007.

**Question.** Adopter la règle R17 « Le coordinateur et les agents ne modifient jamais un document Markdown par Bash (sed, redirection, script) : uniquement par Edit/Write, pour que le hook R5/R6 s'applique » et la faire appliquer techniquement par `.claude/hooks/restreindre_bash.py` ?

**Options.**
1. **R17 dans `CLAUDE.md` + détection dans le hook** (T-006 complet) : refus de `sed -i`, `>`, `>>`, `tee` et des scripts en ligne (`python -c`, `python -` avec heredoc) qui écrivent dans un `.md` de `docs/` ou de `projets/`, avec un message qui renvoie vers Edit/Write ; tests par forme refusée ; lecture (`grep`, `head`, `cat`) toujours permise ; rejeu de l'incident refusé.
2. **R17 seule** (consigne écrite, sans hook) : coût minimal (PR de règle), mais c'est exactement la faiblesse de l'incident : une consigne non appliquée techniquement a déjà été contournée.
3. **Hook seul, sans règle écrite** : la protection existe mais n'est justifiée nulle part ; contraire à R11 (toute règle de l'équipe doit être tracée et défendable).
4. **Statu quo** : le filet CI `validations.yml` ne détecte qu'un statut `VALIDÉ` incohérent, pas une modification du contenu d'un document correctement validé.

**Recommandation.** **Option 1.** La règle dit pourquoi, le hook l'applique, comme R5/R6 avec `proteger_valide.py`. Limite à écrire dans R17 : un script Python enregistré dans un fichier puis lancé ne peut pas être analysé de façon fiable par le hook ; la règle reste la référence et le filet CI reste en place.

**Impact.**
- **Fichiers** : `CLAUDE.md` (`VALIDÉ` : un humain le repasse d'abord `EN_REVUE`, R6), `.claude/hooks/restreindre_bash.py` et `scripts/test_restreindre_bash.py`, nouveau fichier de décision, entrée dans `docs/CHANGELOG-REGLES.md` ; PR relue par B (`CLAUDE.md`) et C (hooks), ARCHITECTURE § 12.
- **Réalisation** : aucun agent ne peut écrire dans `.claude/` ni `CLAUDE.md` (C9) ; T-006 réaffecté à Hugo (4 h, `backend-python` débutant, et `documentation` confirmé pour le texte de la règle) en binôme avec Karim (T-051, 1 h, revue humaine), d'où la formation T-052 (AF7, AF10 c).
- **Coût** : T-006 200,00 € + T-051 78,57 € + T-052 50,00 € + ce ticket 39,29 € = **367,86 €**.
- **Budget** : outillage commun et règle de l'ESN, **hors budget du client** ; recommandation de transférer T-006, T-050, T-051 et T-052 dans un projet interne de l'ESN (voir T-007, point D).
- **Délai** : aucun impact sur le chemin critique du projet client (aucun ticket client ne dépend de ce lot).

## Critères d'acceptation
- [ ] Un humain a choisi une option ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` (`modifie_une_regle: oui`) est créé et référencé dans `decision`.
- [ ] Si l'option 1 ou 2 est retenue : entrée dans `docs/CHANGELOG-REGLES.md` et PR de modification de `CLAUDE.md` (R11).
- [ ] Si l'option 4 est retenue : T-006, T-051 et T-052 passent `ANNULE` avec la raison.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création au tri de T-006, analyse au format R7, statut ATTENTE_HUMAIN · 0 h
- 2026-11-25 déplacé vers les règles de l'ESN (PR de règles)