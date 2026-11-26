---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-038
titre: Revue humaine T-029 (sauvegarde et limite d'âge)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
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

# T-038 — Revue humaine T-029 (sauvegarde et limite d'âge)

## Description
Revue humaine de [T-029](T-029-sauvegarde-quotidienne-limite-age.md), écrit par Nadia : suppression de sauvegardes (données) et modification de l'outillage commun de déploiement. Karim n'en est pas l'auteur (S3-R1) et relit le code Python (`backend-python` expert) ; la compétence `sauvegarde-restauration` n'a pas de second détenteur dans l'équipe (AF10 b, signalé dans T-007). La relecture de la PR par C, responsable de l'outillage, reste un critère de T-029. **Pas de `depend_de` vers T-029** : prenable quand T-029 passe `EN_REVUE`.

**Ticket salarié (AF11, R15)** : à faire par un humain. **Affectation conditionnelle** à l'allocation de Karim proposée dans T-007.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-029 est remplie par Karim : prénom, date, avis.
- [ ] L'ordre « Limite d'âge » puis « Rétention », la non-application de la rétention de 14 jours en cas d'échec et l'absence de suppression sur un slug invalide sont vérifiés sur les tests.
- [ ] Chaque réserve donne un commentaire dans T-029 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création ; affectation conditionnelle à l'allocation de Karim proposée dans T-007 · 0 h
- 2026-11-26 22:10 · agent:chef-de-projet · SIMULATION · imputé à l'ESN (DEC-020) : coût hors budget client, ticket réalisé dans ce projet faute de projet interne · 0 h
