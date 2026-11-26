---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-076
titre: "Page de consultation : message sur réponse inattendue et commande des tests JS"
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: basse             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.3           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-055]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-076 — Page de consultation : message sur réponse inattendue et commande des tests JS

## Description
**Origine.** Remarque 3 du `relecteur-code` sur [T-055](T-055-page-disponibilites-lecture.md) (commit `dc53a1d`) et remarque hors sécurité de l'audit [securite-2026-11-26.md](../rapports/securite-2026-11-26.md). Créé sans être traité : périmètre gelé avant la soutenance du 2026-11-27, à trier par le `chef-de-projet`.

1. Dans `app/reservation/static/js/disponibilites.js`, une réponse 200 de forme inattendue affiche « Impossible de joindre le service », alors que le service a répondu : le message induit l'utilisateur en erreur.
2. La commande indiquée en tête de `app/tests/front/creneaux.test.mjs` (`node --test tests/front/`) échoue sous Node 24 ; la commande qui fonctionne est celle du `README` (`node --no-warnings --test "tests/front/*.test.mjs"`).

## Critères d'acceptation
- [ ] Une réponse 200 dont le corps n'a pas la forme attendue affiche un message distinct de l'indisponibilité du service, sans détail technique (test JS).
- [ ] La commande indiquée en tête du fichier de test est identique à celle du `README` et fonctionne sous Node 24.
- [ ] Les tests JS et la suite Python restent verts.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 14:00 · agent:coordinateur · création (remarque 3 du relecteur-code sur T-055, remarque de l'audit securite-2026-11-26), non traité : périmètre gelé · 0 h
- 2026-11-26 22:00 · agent:chef-de-projet · SIMULATION · A_FAIRE → ANNULE par DEC-020 (révision du budget à 4 200 € HT, scénario B : gêne mineure, hors Must et hors sécurité). Valeur de `titre` mise entre guillemets doubles, sans changer le texte : le « : » rendait le YAML invalide et `tableau.py` ignorait le ticket. Aucun ticket n'en dépend ; aucune revue ni vérification ne le couvrait. Temps compté dans T-008 · 0 h
