---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-046
titre: GO mise en production
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-042, T-043, T-045, T-069, T-029, T-087, T-092, T-078]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-26
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-046 — GO mise en production

## Description
Point d'arrêt humain obligatoire (S3-R3, porte 4). Créé dès le planning en `A_FAIRE` pour figurer au budget et au chemin critique ; il passe `ATTENTE_HUMAIN` (avec `bloque_par`) quand le coordinateur le présente, **seulement** avec un rapport de recette `CONFORME` sur le SHA du GO (CLAUDE.md R16). Porteur salarié (AF2) : Claire, interlocutrice client, qui a fait la recette et présente la décision ; la validation formelle reste humaine (R5).

Description à compléter au format R7 au moment de la présentation :
- **Question** : mettre en production locale le SHA `<sha40>` ?
- **Options** : GO sur ce SHA ; pas de GO (corrections, nouveau SHA, nouvelle recette).
- **Recommandation** et **impact** : rapports de tests (T-042), sécurité (T-043) et recette (T-045) sur ce SHA ; T-029 (sauvegarde), T-087 (refus d'une base vide), T-092 (vérification quotidienne des sauvegardes) et T-078 (image PostgreSQL 16.16) terminés (DEC-019, DEC-020), revues humaines T-038, T-097, T-098 et T-099 comprises (R13) ; mise en service (T-048) prévue le jour du déploiement ; marge restante avant le 2026-12-18.

## Critères d'acceptation
- [ ] Les rapports de tests `CONFORME`, de sécurité `NON BLOQUANT` et de recette `CONFORME` portent sur le SHA proposé.
- [ ] Un humain a décidé ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` cite le SHA attendu et est référencé dans `decision`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création (A_FAIRE, à présenter avec une recette CONFORME) · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage (S1-R5) : dépend aussi de T-069 (API sans réponse si une connexion poolée gèle ; constat 14 du rapport securite-2026-11-25-4), dont le testeur demande la correction avant tout GO. Temps compté dans T-008 · 0 h
- 2026-11-26 18:45 · agent:chef-de-projet · SIMULATION · T-029 (sauvegarde quotidienne, désormais critique) ajouté à depend_de, à la demande d'Ethan (DEC-019, retour d'expérience de l'exercice T-080 : pas de mise en production sans outillage de sauvegarde) ; absence de cycle vérifiée (T-029 → T-007, qui ne dépend de rien) ; statut inchangé (A_FAIRE) · 0 h (temps compté dans T-008)
- 2026-11-26 22:50 · agent:chef-de-projet · SIMULATION · triage (T-080, T-090) : T-087 (refus d'une base vide), T-092 (vérification quotidienne des sauvegardes) et T-078 (image PostgreSQL 16.16) ajoutés à depend_de, conformément à DEC-020 point 3 (« T-029, T-087 et T-092 sont faits avant le GO, et T-078 aussi ») ; T-029 y était déjà. Absence de cycle vérifiée : T-087 → T-029, T-086 → T-007 ; T-092 → T-021, T-029 → T-013 → T-011, T-073 → T-010 → T-007 ; T-078 → aucun ; aucun ne remonte à T-046. Statut inchangé (A_FAIRE). T-086 non ajouté directement, mais prérequis de fait par T-087 ; T-089 et T-079 non ajoutés (non retenus par DEC-020, à arbitrer) · 0 h (temps compté dans T-008)
