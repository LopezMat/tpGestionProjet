---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-043
titre: Audit sécurité
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:securite     # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 3.0          # heures équivalent humain
depend_de: [T-010, T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026, T-027, T-028]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-043 — Audit sécurité

## Description
Ticket « Audit sécurité » de l'agent `securite` (porte 3 de S3) : audit du code et des dépendances sur le SHA candidat, au niveau fixé par le CDC § 8 (OWASP Top 10, contrôle d'accès, authentification, RGPD ; pas de test d'intrusion externe), avec `pip-audit`, `bandit` et `gitleaks` (`securite.yml`). L'audit **confirme ou ajuste les seuils G** provisoires de DEC-007 (mot de passe, tentatives, alerte, sessions), en cohérence avec les revues de Karim (T-030 à T-032), et examine l'écart de forme « clé de signature des sessions » (DEC-007, C ; architecture R-06). Le coordinateur conclut (R13).

## Critères d'acceptation
- [ ] `rapports/securite-AAAA-MM-JJ.md` existe, en `EN_REVUE`, sur le même SHA que le rapport de tests, avec un verdict `NON BLOQUANT` ou `BLOQUANT`.
- [ ] Chaque seuil G est déclaré confirmé ou à ajuster, avec la justification.
- [ ] Toute vulnérabilité critique ou haute a son ticket `bug` ou `incident`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 15:30 · agent:securite · audit d'incrément T-010 (socle), demandé par Ethan (DEC-011, `EN_REVUE`), sur l'état de travail non commité de `app/` (base `6c53d31`, empreintes des fichiers dans le rapport) : verdict NON BLOQUANT, 0 critique, 0 haute, 1 moyenne (dépendances transitives non verrouillées), 6 basses, aucun ticket `bug` ; rapport [securite-2026-11-25.md](../rapports/securite-2026-11-25.md). Outils absents du poste : `pip-audit`, `bandit`, `gitleaks` (revue manuelle des versions) ; image non construite. Statut laissé `A_FAIRE` sur consigne du coordinateur : l'audit avant mise en production reste à faire sur le SHA candidat · 1.5 h
- 2026-11-25 21:30 · agent:securite · ré-audit d'incrément après la reprise de T-010 et la réalisation de T-056 (état de travail non commité de `app/`, base `6c53d31`, 8 fichiers modifiés, empreintes dans le rapport) : verdict NON BLOQUANT, 0 critique, 0 haute ; constat 3 (`server_header`) traité ; constats 1 (moyen), 2, 4, 5, 6 et 7 (bas) toujours ouverts ; 2 nouveaux constats bas (8 : `/health` sans mise en commun des sondes, d'où une amplification vers la base et des faux 503 sous rafale ; 9 : une sonde bloquée après l'ouverture de la connexion n'a pas de borne si le pair disparaît sans fermer, faute de keepalive court) ; aucun ticket `bug` (T-057 reste libre) ; nouveau rapport [securite-2026-11-25-2.md](../rapports/securite-2026-11-25-2.md), sans réécrire le premier (règle 5). Outils toujours absents : `pip-audit`, `bandit`, `gitleaks`, `trivy` ; aucune vérification dynamique (dépendances de l'app absentes du poste). Statut laissé `A_FAIRE`, comme au premier audit : l'audit avant mise en production reste à faire sur le SHA candidat · 1.5 h
