---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-014
titre: Limitation des tentatives et alerte de sécurité (F-04)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 3             # heures équivalent humain, quel que soit l'assigné
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

# T-014 — Limitation des tentatives et alerte de sécurité (F-04)

## Description
Critère F-04 « les tentatives de connexion répétées en échec sont limitées », avec les seuils et le format de [architecture.md](../architecture.md) § 6 (ligne « Limitation des tentatives ») et § 7, retenus provisoirement par DEC-007 (point G) : **blocage par compte seulement**, et alerte journalisée `ALERTE_SECURITE` sans blocage global (remontée par `analyste-prod`). Compteurs en mémoire, seuils en constantes du module `auth` (R-04).

**Touche la sécurité** : revue humaine obligatoire, ticket compagnon **T-031** (Karim), qui confirme les seuils 5/15 min et 30/15 min (DEC-007, G).

## Critères d'acceptation
- [ ] Après 5 échecs pour un même e-mail en 15 min, la connexion de cet e-mail est refusée pendant 15 min, avec le même message que le compte existe ou non (test avec horloge injectée).
- [ ] Aucun blocage global : après plus de 30 échecs toutes adresses confondues, un autre compte se connecte normalement (test).
- [ ] 30 échecs en 15 min (fenêtre glissante) n'émettent rien ; le 31e émet une ligne `ALERTE_SECURITE evenement=echecs_connexion_global echecs=<n> seuil=30 fenetre_min=15 comptes_bloques=<n> depuis=<AAAA-MM-JJTHH:MM:SS±HH:MM>` sur la sortie standard ; au plus une alerte par période de 15 min tant que le seuil reste dépassé (tests).
- [ ] La ligne d'alerte capturée ne contient ni l'e-mail, ni le mot de passe, ni un identifiant d'utilisateur, ni une adresse IP (test).
- [ ] Les seuils sont des constantes du module `auth`, modifiables en un seul endroit avec leurs tests.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (authentification, S3-R2 ; ticket compagnon T-031)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
