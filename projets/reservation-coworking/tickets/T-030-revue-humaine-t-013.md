---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-030
titre: Revue humaine T-013 (authentification, sessions, rôles)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
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

# T-030 — Revue humaine T-013 (authentification, sessions, rôles)

## Description
Revue humaine obligatoire (S3-R2, porte 1 bis ; CDC § 8 ; DEC-006 : Karim) du ticket [T-013](T-013-authentification-sessions-roles.md), écrit par `agent:dev-backend` : Karim n'en est pas l'auteur (S3-R1, AF3). **Pas de `depend_de` vers T-013** (sinon dépendance circulaire, AF3) : ce ticket devient prenable quand T-013 passe `EN_REVUE`.

À cette occasion, Karim **confirme ou ajuste les seuils G** de DEC-007 qui concernent T-013 : expiration de session après 2 h d'inactivité et 12 h au maximum, et les choix d'authentification (Argon2id, sessions opaques en base, CSRF). Si sa revue remet en cause un choix d'authentification au-delà d'un seuil, l'architecture est rouverte par un humain (R6, architecture R-02).

**Ticket salarié (AF11, R15)** : à faire par un humain. **Affectation conditionnelle** : l'allocation de Karim au projet est aujourd'hui nulle ; elle est proposée dans T-007 (S1-R10, AF8).

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-013 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Les seuils d'expiration de session (2 h, 12 h) sont confirmés, ou la nouvelle valeur est notée dans T-013 et au journal de ce ticket.
- [ ] Chaque réserve donne un commentaire à traiter dans T-013 ou un ticket `bug`.
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
