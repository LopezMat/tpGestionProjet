---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-053
titre: Formation Hugo — securite-applicative (second relecteur)
projet: reservation-coworking
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ANNULE              # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: basse             # critique | haute | normale | basse
assigne: salarie:hugo       # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (debutant)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-053 — Formation Hugo — securite-applicative (second relecteur)

## Description
> **ANNULE le 2026-11-25 : déplacé vers les règles de l'ESN (PR de règles)**, avec le lot ESN (Ethan, 2026-11-24, DEC-009, points D1 et E ; DEC-010). Le besoin (second relecteur `securite-applicative`, AF10 b) reste à inscrire au plan de formation de l'ESN (projet interne), hors budget client. Le risque correspondant (Karim seul relecteur, en congés du 21 au 31 décembre) reste suivi dans [planning.md](../planning.md).

Besoin de formation détecté par AF10 (b) : **Karim est le seul salarié** avec `securite-applicative` (confirmé) ; sa fiche demande un ticket `formation` « dès le premier projet sensible », et ce projet l'est (authentification par mot de passe, données personnelles). Il est sur le chemin critique (T-030 à T-036) et en congés du 2026-12-21 au 2026-12-31 (EV-003) : une correction d'authentification pendant la garantie de livraison ne pourrait pas être revue avant janvier.
- **Compétence** : `securite-applicative` ; **niveau actuel** : aucun ; **niveau visé** : débutant (premier pas vers un second relecteur humain des tickets d'authentification).
- **Tickets déclencheurs** : T-030 et T-033 (revues de Karim).
- **Modalité** : binôme d'observation sur deux revues humaines de Karim (T-030, T-033 : Karim commente sa grille de relecture), puis autoformation guidée (aide-mémoire OWASP « Authentication », « Session Management » et « Password Storage » ; ASVS chapitres authentification et sessions).
- **Coût estimé** : 3 h × 50,00 €/h = **150,00 €** (Hugo) ; le temps d'explication de Karim reste dans ses tickets de revue.
- **Budget** : investissement de l'ESN, hors budget client (T-007, point D). **Affectation conditionnelle** à l'allocation de Hugo proposée dans T-007.

## Critères d'acceptation
- [ ] Hugo a assisté aux revues T-030 et T-033 ; ses notes de relecture (sans secret) sont résumées au journal.
- [ ] L'autoformation est faite ; Hugo rédige une grille de relecture « authentification » d'une page, relue par Karim.
- [ ] La fiche de Hugo (section « Formations ») est mise à jour par le coordinateur, avec le niveau atteint décidé par un humain.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création (AF10 b, fiche de Karim) ; affectation conditionnelle à l'allocation de Hugo proposée dans T-007 · 0 h
- 2026-11-25 09:00 · agent:chef-de-projet · statut A_FAIRE → ANNULE : déplacé vers les règles de l'ESN (PR de règles) (Ethan, 2026-11-24, DEC-009, points D1 et E ; DEC-010) ; Hugo à 0 % sur ce projet ; temps compté dans T-008 · 0 h
