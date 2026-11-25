---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-016
titre: Gestion des comptes par l'accueil (F-07)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 6             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-015]          # ex. [T-001, T-002]
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

# T-016 — Gestion des comptes par l'accueil (F-07)

## Description
Composant `api.comptes` de [architecture.md](../architecture.md) § 3 et § 7 : routes `/api/accueil/comptes` (liste, création d'un compte membre ou accueil, suppression d'un compte membre, réinitialisation du mot de passe). Pas de suppression de compte accueil (DEC-007, point F). Le compte accueil initial est traité par T-017.

**Touche la sécurité** (comptes, rôles, données personnelles) : revue humaine obligatoire, ticket compagnon **T-033** (Karim).

## Critères d'acceptation
- [ ] Les comptes sont distingués par rôle (membre, accueil) ; le rôle est contrôlé côté serveur à chaque appel.
- [ ] L'accueil crée un compte membre (nom, e-mail, mot de passe initial) ; un e-mail déjà utilisé est refusé (409, test).
- [ ] **Changement obligatoire à la première connexion pour les comptes membres** : un compte membre créé par l'accueil doit changer son mot de passe initial à sa première connexion, avant tout autre accès ; tant que ce n'est pas fait, aucun appel d'API autre que le changement de mot de passe n'est accessible (test par appel direct) ; le mot de passe initial cesse alors de fonctionner (test).
- [ ] **Autres comptes accueil** : un utilisateur accueil peut créer d'autres comptes accueil ; un membre ne le peut pas (test d'autorisation par appel direct).
- [ ] **Suppression sur demande** : l'accueil supprime le compte d'un membre ; ensuite le nom, l'e-mail et l'empreinte du mot de passe n'existent plus en base, le membre ne peut plus se connecter, ses réservations ne subsistent pas sous une forme nominative et ses réservations à venir libèrent leurs créneaux (contrôle en base, H-14).
- [ ] La suppression d'un compte accueil est refusée (DEC-007, F).
- [ ] **Réinitialisation par l'accueil uniquement** : l'accueil génère ou fixe un mot de passe temporaire pour un compte ; il est stocké haché ; l'utilisateur concerné doit le changer à sa connexion suivante, avant tout autre accès ; le mot de passe temporaire ne fonctionne plus après ce changement ; les sessions de la cible sont révoquées (tests).
- [ ] Un membre ne peut ni créer, ni supprimer, ni lister des comptes, ni réinitialiser le mot de passe d'un autre membre, de l'accueil ou le sien par ce biais (tests d'autorisation par appel direct) ; il n'existe aucune réinitialisation en libre-service.
- [ ] Entrées validées : nom de 100 caractères au plus, e-mail de 254 au plus, champs inconnus refusés.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (comptes et rôles, S3-R2 ; ticket compagnon T-033)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
