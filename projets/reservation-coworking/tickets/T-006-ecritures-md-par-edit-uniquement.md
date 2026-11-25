---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-006
titre: Écritures Markdown par Edit/Write uniquement (hook R5/R6)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:hugo       # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-050]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-006 — Écritures Markdown par Edit/Write uniquement (hook R5/R6)

## Description
> **ANNULE le 2026-11-25 : déplacé vers les règles de l'ESN (PR de règles).** Décision (Ethan, 2026-11-24, DEC-009, point D1) : la règle R17 et son outillage sortent du projet client, parce que le client ne paie pas l'amélioration des outils internes. R17 est adoptée sur le principe et sera réalisée après le développement du projet client, dans une PR de règles séparée (DEC-010) ; les tickets y seront recréés dans un projet interne de l'ESN. Ce ticket n'est pas supprimé (traçabilité).

**Règle proposée (Ethan, 2026-11-24).** « Le coordinateur et les agents ne modifient jamais un document Markdown par Bash (sed, redirection, script) : uniquement par Edit/Write, pour que le hook R5/R6 s'applique. »

**Pourquoi (Ethan).** Incident du 2026-11-24 : [DEC-007](../../../docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md) a été modifié par le coordinateur au moyen d'un script Python lancé par Bash alors qu'il était déjà `VALIDÉ` (R6). Le hook `proteger_valide.py` ne surveille que Write et Edit : il n'a pas pu bloquer l'écriture. Elle n'a été détectée qu'après coup par `scripts/verifier_validations.py` (anomalie « VALIDÉ sans valide_par »). Voir [retex.md](../retex.md).

**Correction proposée.**
1. **Règle R17 dans `CLAUDE.md`**, par une PR, avec un fichier de décision et une entrée dans `docs/CHANGELOG-REGLES.md` (R11). La règle s'applique au coordinateur et à tous les agents.
2. **Si possible, détection dans `.claude/hooks/restreindre_bash.py`** des écritures sur des fichiers `.md` de `docs/` et de `projets/` : `sed -i`, redirections `>` et `>>`, `tee`, et scripts en ligne (`python -c`, `python -` avec heredoc) qui écrivent dans ces fichiers. Le hook refuse la commande et renvoie vers Edit/Write.
3. **Tests du hook** : un test par forme d'écriture refusée, et un test qui vérifie qu'une lecture (`grep`, `head`, `cat`) reste permise.

**Triage attendu (`chef-de-projet`).** Affecter la réalisation du hook et de ses tests (compétences `backend-python` et `securite-applicative`), et préparer le ticket `decision` « Modification de règle R17 » (point d'arrêt humain : modification d'une règle, R7, R11). Ce ticket porte sur l'outillage de l'ESN, au-delà du seul projet.

**Tri (`chef-de-projet`, 2026-11-24, S1-R5).**
- **Priorité** : `haute`, inchangée (garde-fou contourné une fois ; tous les agents écrivent des Markdown) ; hors chemin critique du projet client.
- **Décision préalable** : ticket [T-050](T-050-modification-regle-r17.md) « Modification de règle R17 » (`ATTENTE_HUMAIN`, R7, R11) ; ce ticket en dépend : si la règle est refusée, il passe `ANNULE`.
- **Assigné** : aucun agent ne peut écrire dans `.claude/` ni `CLAUDE.md` (C9), donc un salarié (règle 7 du `chef-de-projet`). Seul Karim a `backend-python` et `securite-applicative` au niveau confirmé, mais personne ne pourrait alors relire son travail (S3-R1). Retenu : **Hugo** (`backend-python` débutant, `documentation` confirmé pour le texte de R17 et du changelog) **en binôme avec Karim** ([T-051](T-051-binome-t-006.md), 1 h), qui tient lieu de revue humaine (AF7, AF5 par analogie) ; formation [T-052](T-052-formation-hugo-backend-python.md) (AF10 c). Estimation portée de 3 à 4 h (hook, un test par forme refusée, rejeu de l'incident, texte de R17 et entrée du changelog). **Ticket salarié (AF11, R15)** : à faire par un humain.
- **Affectation conditionnelle** : l'allocation de Hugo est aujourd'hui nulle ; elle est proposée dans T-007 (point B).
- **Budget** : **relève de l'ESN, pas du client** (outillage commun et règle de l'ESN) : 367,86 € pour T-006, T-050, T-051 et T-052. Recommandation : transférer ce lot dans un projet interne de l'ESN (T-007, point D) ; tant qu'il reste ici, `tableau.py` le compte dans le budget du projet.

## Critères d'acceptation
- [ ] R17 est ajoutée à `CLAUDE.md` par une PR, avec un fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` validé par un humain et une entrée dans `docs/CHANGELOG-REGLES.md`.
- [ ] `restreindre_bash.py` refuse `sed -i`, `>`, `>>`, `tee` et les scripts en ligne qui écrivent dans un fichier `.md` de `docs/` ou de `projets/`, avec un message qui renvoie vers Edit/Write (ou bien le ticket documente pourquoi une forme ne peut pas être détectée).
- [ ] Les tests du hook couvrent chaque forme refusée et vérifient qu'une lecture de ces fichiers reste permise ; toutes les suites sont vertes.
- [ ] Rejouer l'incident (modification par Bash d'un fichier `VALIDÉ` de `docs/decisions/`) est refusé par le hook.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (garde-fou de sécurité de l'outillage : la modification du hook touche la sécurité, S3-R2 ; assurée par Karim dans le binôme T-051)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 20:00 · agent:coordinateur · création, à la demande d'Ethan après l'incident DEC-007 · 0 h
- 2026-11-24 23:55 · agent:chef-de-projet · triage : priorité haute maintenue ; réaffecté de agent:chef-de-projet à salarie:hugo (binôme Karim T-051, formation T-052), compétence backend-python (confirme), estimation 3 → 4 h ; dépend de la décision T-050 (R17) ; lot ESN hors budget client ; temps compté dans T-008 · 0 h
- 2026-11-25 09:00 · agent:chef-de-projet · statut A_FAIRE → ANNULE : déplacé vers les règles de l'ESN (PR de règles) (Ethan, 2026-11-24, DEC-009, point D1 ; DEC-010) ; temps compté dans T-008 · 0 h
