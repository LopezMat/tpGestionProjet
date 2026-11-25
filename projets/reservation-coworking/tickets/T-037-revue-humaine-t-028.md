---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-037
titre: Revue humaine T-028 (purge à 12 mois)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
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
maj_le: 2026-11-25
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-037 — Revue humaine T-028 (purge à 12 mois)

## Description
Revue humaine du ticket de purge F-08 exigée par le CDC § 8 (suppression de données), AF3 : [T-028](T-028-purge-douze-mois.md), écrit par `agent:dev-backend`. **Pas de `depend_de` vers T-028** : prenable quand T-028 passe `EN_REVUE`. Priorité alignée sur T-028 (Should). **Abandonnable avec T-028 (DEC-009)** : si T-028 est retiré sur alerte de marge, ce ticket passe aussi `ANNULE`.

**Ticket salarié (AF11, R15)** : à faire par un humain. Allocation de Karim à 15 % décidée (Ethan, 2026-11-24, DEC-009), à reporter dans `equipe/` par le coordinateur.

## Critères d'acceptation
- [ ] La ligne « Revue humaine » de T-028 est remplie par Karim : prénom, date, avis.
- [ ] La requête de purge et le calcul de la date limite (bornes 12 mois et 1 jour, 11 mois et 29 jours, 29 février) sont vérifiés ; la trace ne contient que des compteurs.
- [ ] La revue couvre aussi `regles.date_limite_purge` et `regles.doit_etre_purgee`, livrées par T-012 sans revue humaine, qui fixent la frontière de suppression (recommandation du rapport securite-2026-11-25-3) ; l'avis le mentionne.
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
- 2026-11-25 09:00 · agent:chef-de-projet · marqué abandonnable avec T-028 (Ethan, 2026-11-24, DEC-009) ; temps compté dans T-008 · 0 h
- 2026-11-25 23:50 · agent:chef-de-projet · triage du rapport securite-2026-11-25-3 : critère ajouté, la revue couvre aussi `regles.date_limite_purge` et `regles.doit_etre_purgee` (T-012) ; estimation inchangée (fonctions courtes, déjà testées) ; temps compté dans T-008 · 0 h
