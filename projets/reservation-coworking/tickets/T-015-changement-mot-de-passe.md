---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-015
titre: Profil et changement de mot de passe (F-04, F-07)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 4             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-013]          # ex. [T-001, T-002]
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

# T-015 — Profil et changement de mot de passe (F-04, F-07)

## Description
Composant `api.moi` et dépendance globale « changement de mot de passe obligatoire » de [architecture.md](../architecture.md) § 3, § 6 et § 7 : critère F-04 « changement de son propre mot de passe » et mécanisme commun aux critères F-07 « changement obligatoire à la première connexion » (compte accueil initial, comptes membres) et « réinitialisation par l'accueil ». Règle de robustesse provisoire (DEC-007, G) : 12 à 128 caractères, différent de l'e-mail et de l'ancien.

**Touche la sécurité** : revue humaine obligatoire, ticket compagnon **T-032** (Karim), qui confirme la règle de robustesse (DEC-007, G).

## Critères d'acceptation
- [ ] `GET /api/moi` renvoie le nom, le rôle et `doit_changer_mdp`, sans champ mot de passe ni empreinte.
- [ ] **Changement de son propre mot de passe (F-04)** : un utilisateur connecté (membre ou accueil) peut changer son propre mot de passe en saisissant l'ancien ; un mot de passe erroné est refusé ; le nouveau mot de passe est haché, et l'ancien ne permet plus de se connecter (test). Il ne peut changer que son propre mot de passe (test d'autorisation par appel direct à l'API).
- [ ] Robustesse : 11 et 129 caractères refusés, 12 et 128 acceptés ; un mot de passe égal à l'e-mail ou à l'ancien est refusé (tests).
- [ ] Tant que `doit_changer_mdp` est vrai, toute route est refusée (403 `changement_mot_de_passe_requis`) sauf `GET /api/moi`, `PUT /api/moi/mot-de-passe`, `DELETE /api/session` et `/health` (test par appel direct à l'API).
- [ ] Après un changement : `doit_changer_mdp` passe à faux, le jeton de session est renouvelé et les autres sessions de l'utilisateur sont révoquées (test).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (authentification, S3-R2 ; ticket compagnon T-032)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
