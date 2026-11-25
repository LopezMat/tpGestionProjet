---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-044
titre: Environnement de recette (app au SHA candidat, compte accueil de recette)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: docker (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-017, T-021]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-044 — Environnement de recette (app au SHA candidat, compte accueil de recette)

## Description
Le skill `recette` (étape 3) exige que l'app tourne **au SHA candidat** et que le recetteur le constate avec `scripts/sonde_sante.py`. Claire n'a pas Claude Code (DEC-004) et n'est pas technicienne : Nadia (`docker` confirmé) prépare et documente le lancement local de l'app à un SHA donné, distinct de la production locale, avec le jeu de données fictif (`donnees_demo`, T-021) et un compte accueil de recette créé par `init_accueil` selon la procédure de l'architecture § 7 (terminal dédié, hors session Claude Code, aucune valeur écrite). Le jour de la recette, elle relance l'environnement au SHA candidat lu dans les rapports T-042 et T-043.

**Ticket salarié (AF11, R15)** : à faire par un humain. **Affectation conditionnelle** à l'allocation de Nadia proposée dans T-007.

## Critères d'acceptation
- [ ] La procédure de lancement de l'environnement de recette à un SHA donné est écrite dans le README de l'app (sans aucune valeur de secret) et a été essayée une fois.
- [ ] Le jour de la recette, l'app tourne au SHA candidat : `python scripts/sonde_sante.py --url <url> --sha <sha candidat> --mesures 1` le confirme, résultat transmis à Claire.
- [ ] Le jeu de données fictif est chargé et un compte accueil de recette existe ; ses identifiants sont remis à Claire hors du dépôt et hors de toute conversation avec un agent.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création ; affectation conditionnelle à l'allocation de Nadia proposée dans T-007 · 0 h
