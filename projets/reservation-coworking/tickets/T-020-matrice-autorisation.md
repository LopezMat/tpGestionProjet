---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-020
titre: Matrice d'autorisation et tests sur toutes les routes
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-016, T-017, T-019]   # ex. [T-001, T-002]
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

# T-020 — Matrice d'autorisation et tests sur toutes les routes

## Description
Contrôle transversal des autorisations de F-02, F-03, F-04 et F-07 (CDC § 8 « rôles contrôlés côté serveur à chaque requête » ; architecture § 6 et § 7) : matrice versionnée (route × profil → code attendu) et test automatique qui parcourt **toutes** les routes de l'API avec quatre profils : visiteur, membre, membre qui doit changer son mot de passe, accueil. Couvre les parcours 6, 8, 9, 12 et 13 du CDC § 7 par appel direct à l'API, et le contrôle des journaux sur l'ensemble des parcours.

**Touche la sécurité** : revue humaine obligatoire, ticket compagnon **T-036** (Karim).

## Critères d'acceptation
- [ ] La matrice d'autorisation est versionnée dans `app/` et couvre chaque route de l'API pour les quatre profils.
- [ ] Un test parcourt toutes les routes déclarées dans l'application ; une route ajoutée sans règle dans la matrice fait échouer le test.
- [ ] Les parcours 6, 8, 9, 12 et 13 du CDC § 7 sont couverts par appel direct à l'API (tests verts).
- [ ] La suppression d'un compte accueil et toute route `/api/accueil/*` appelée par un membre sont refusées dans la matrice.
- [ ] Sur l'ensemble des parcours testés, les journaux capturés ne contiennent ni l'e-mail, ni le nom, ni le mot de passe de test.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (autorisations, S3-R2 ; ticket compagnon T-036)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-26 00:30 · coordinateur · à couvrir par la matrice d'autorisation (critère 7 de T-054, DEC-011) : `GET /api/salles` et `GET /api/disponibilites` sont accessibles sans connexion à titre provisoire (commentaire `PROVISOIRE` dans `app/reservation/api.py`) ; la matrice doit fixer leur règle d'accès définitive (connexion exigée, F-04) avant tout GO (T-046) · 0 h
