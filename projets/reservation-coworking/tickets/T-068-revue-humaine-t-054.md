---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-068
titre: Revue humaine T-054 (API de consultation sans connexion)
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
cree_par: coordinateur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-068 — Revue humaine T-054 (API de consultation sans connexion)

## Description
Revue humaine (S3-R2, AF3) de [T-054](T-054-api-consultation-disponibilites.md) (`GET /api/salles`, `GET /api/disponibilites`), écrit par `agent:dev-backend` et marqué « touche la sécurité » : Karim n'en est pas l'auteur (S3-R1). Le relecteur-code a passé « Revue humaine requise » à `oui` (commit 4674c76). **Pas de `depend_de` vers T-054** (dépendance circulaire, AF3) : ce ticket est prenable dès maintenant, T-054 étant `EN_REVUE`.

Ticket dédié plutôt que rattachement à T-036 (revue humaine de T-020) : T-020 n'est réalisé qu'après la soutenance, et T-054 doit être `TERMINE` avant T-055, la page de la soutenance du 2026-11-27 (DEC-011). La revue de T-020 (T-036) reste chargée de la règle d'accès définitive de ces deux routes.

Points à examiner : aucune donnée de membre exposée (DEC-011) ; validation de `date` et erreurs sans écho de l'entrée ; accès sans connexion provisoire, signalé dans le code (`PROVISOIRE`) et au journal de T-020 ; rapports [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md) et [securite-2026-11-25-4.md](../rapports/securite-2026-11-25-4.md) (audit de T-054 : NON BLOQUANT, constats bas 14 et 15).

**Ticket salarié (AF11, R15)** : à faire par un humain.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-054 est remplie par Karim : prénom, date, avis (favorable, ou réserves listées).
- [ ] Aucune réponse des deux routes ne contient de donnée de membre, et l'accès sans connexion est bien limité à la lecture (DEC-011).
- [ ] Chaque réserve donne un commentaire à traiter dans T-054 ou un ticket `bug`.
- [ ] Le temps passé est noté (journal, `temps_passe_h`).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de revue)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:55 · coordinateur · création (revue humaine requise sur T-054 par le relecteur-code, S3-R2) · 0 h
