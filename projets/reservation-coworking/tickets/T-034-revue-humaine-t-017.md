---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-034
titre: Revue humaine T-017 (compte accueil initial)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:karim      # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
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

# T-034 — Revue humaine T-017 (compte accueil initial)

## Description
Revue humaine obligatoire (S3-R2, AF3) du ticket [T-017](T-017-compte-accueil-initial.md), écrit par `agent:dev-backend` : commande `init_accueil` (secret lu dans l'environnement, idempotence, non-fuite) et `forcer_changement`. **Pas de `depend_de` vers T-017** : prenable quand T-017 passe `EN_REVUE`.

**Ticket salarié (AF11, R15)** : à faire par un humain. **Affectation conditionnelle** à l'allocation de Karim proposée dans T-007.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-017 est remplie par Karim : prénom, date, avis.
- [ ] L'absence de l'e-mail et du mot de passe dans la sortie, les journaux et le dépôt est vérifiée sur le test de capture.
- [ ] Chaque réserve donne un commentaire dans T-017 ou un ticket `bug`.
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
