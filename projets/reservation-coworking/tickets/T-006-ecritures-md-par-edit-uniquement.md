---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-006
titre: Écritures Markdown par Edit/Write uniquement (hook R5/R6)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-006 — Écritures Markdown par Edit/Write uniquement (hook R5/R6)

## Description
**Règle proposée (Ethan, 2026-11-24).** « Le coordinateur et les agents ne modifient jamais un document Markdown par Bash (sed, redirection, script) : uniquement par Edit/Write, pour que le hook R5/R6 s'applique. »

**Pourquoi (Ethan).** Incident du 2026-11-24 : [DEC-007](../../../docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md) a été modifié par le coordinateur au moyen d'un script Python lancé par Bash alors qu'il était déjà `VALIDÉ` (R6). Le hook `proteger_valide.py` ne surveille que Write et Edit : il n'a pas pu bloquer l'écriture. Elle n'a été détectée qu'après coup par `scripts/verifier_validations.py` (anomalie « VALIDÉ sans valide_par »). Voir [retex.md](../retex.md).

**Correction proposée.**
1. **Règle R17 dans `CLAUDE.md`**, par une PR, avec un fichier de décision et une entrée dans `docs/CHANGELOG-REGLES.md` (R11). La règle s'applique au coordinateur et à tous les agents.
2. **Si possible, détection dans `.claude/hooks/restreindre_bash.py`** des écritures sur des fichiers `.md` de `docs/` et de `projets/` : `sed -i`, redirections `>` et `>>`, `tee`, et scripts en ligne (`python -c`, `python -` avec heredoc) qui écrivent dans ces fichiers. Le hook refuse la commande et renvoie vers Edit/Write.
3. **Tests du hook** : un test par forme d'écriture refusée, et un test qui vérifie qu'une lecture (`grep`, `head`, `cat`) reste permise.

**Triage attendu (`chef-de-projet`).** Affecter la réalisation du hook et de ses tests (compétences `backend-python` et `securite-applicative`), et préparer le ticket `decision` « Modification de règle R17 » (point d'arrêt humain : modification d'une règle, R7, R11). Ce ticket porte sur l'outillage de l'ESN, au-delà du seul projet.

## Critères d'acceptation
- [ ] R17 est ajoutée à `CLAUDE.md` par une PR, avec un fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` validé par un humain et une entrée dans `docs/CHANGELOG-REGLES.md`.
- [ ] `restreindre_bash.py` refuse `sed -i`, `>`, `>>`, `tee` et les scripts en ligne qui écrivent dans un fichier `.md` de `docs/` ou de `projets/`, avec un message qui renvoie vers Edit/Write (ou bien le ticket documente pourquoi une forme ne peut pas être détectée).
- [ ] Les tests du hook couvrent chaque forme refusée et vérifient qu'une lecture de ces fichiers reste permise ; toutes les suites sont vertes.
- [ ] Rejouer l'incident (modification par Bash d'un fichier `VALIDÉ` de `docs/decisions/`) est refusé par le hook.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (garde-fou de sécurité de l'outillage : la modification du hook touche la sécurité, S3-R2)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 20:00 · agent:coordinateur · création, à la demande d'Ethan après l'incident DEC-007 · 0 h
