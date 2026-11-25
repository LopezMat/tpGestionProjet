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
temps_passe_h: 8.5          # heures équivalent humain
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
- 2026-11-25 13:45 · agent:securite · audit d'incrément de T-011 et T-012 (DEC-011) sur le commit `2852fe746fb4be045fca1a70c876a3e02fdd0120` : verdict NON BLOQUANT, 0 critique, 0 haute ; nouveaux constats 10 (moyen : rôle PostgreSQL superutilisateur pour l'app et les migrations, décision humaine, modèle commun), 11 (bas : e-mail unique sensible à la casse), 12 (bas : fuseau retiré sans conversion dans `regles`), 13 (bas : fixture de test `DROP SCHEMA` sans garde-fou) ; constats 1 (moyen), 2, 4 à 9 (bas) inchangés ; vigilance du rapport -2 sur le moteur applicatif levée (pool borné) ; aucun ticket `bug` ; rapport [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md). Dépendances : `pip-audit` absent, non installé ; versions résolues (26 paquets, image d'aperçu) vérifiées sur OSV, aucune vulnérabilité connue. Vérifications dynamiques sur une base postgres:16 jetable (supprimée ensuite, conteneurs `apercu-*` non touchés). Statut laissé `A_FAIRE`, comme aux audits précédents : l'audit avant mise en production reste à faire sur le SHA candidat · 2 h
- 2026-11-25 14:20 · agent:securite · audit d'incrément de T-054 (DEC-011) sur le commit `4674c76dbf06dee18ca1d28d819a850f2d70f333` : verdict NON BLOQUANT, 0 critique, 0 haute ; nouveaux constats 14 (bas : moteur applicatif sans borne côté client si la base gèle, 5 requêtes sans réponse constatées) et 15 (bas : journal d'accès Uvicorn avec chaîne de requête brute et sans limite, journaux sans rotation) ; points du rapport -3 pour T-054 vérifiés (aucune donnée de membre, `date` validée sans écho, requêtes paramétrées, moteur applicatif seul, 503 sans fuite sous verrou, gel et arrêt de la base) ; accès sans connexion signalé comme écart provisoire DEC-011 ; report des constats 2 et 4 dans T-063 jugé acceptable sous conditions ; aucun ticket `bug` ; rapport [securite-2026-11-25-4.md](../rapports/securite-2026-11-25-4.md). Outils absents : `pip-audit`, `safety`, `bandit`, `semgrep`, `gitleaks`, `trivy` ; `requirements.txt` inchangé. Vérifications dynamiques sur une instance jetable (conteneurs, réseau et volume supprimés ; `apercu-*` et `t54test-*` non touchés). Statut laissé `A_FAIRE`, comme aux audits précédents ; estimation de 5 h dépassée (7 h) du fait des audits d'incrément de DEC-011, l'audit avant GO restant à faire · 2 h
- 2026-11-25 14:45 · agent:chef-de-projet · **proposition de ré-estimation** (statut, estimation et dépendances non modifiés ; à arbitrer par le coordinateur) : les 7 h passées sont toutes des audits d'incrément (DEC-011) ; l'audit avant GO prévu à 5 h reste entier, et l'auditeur annonce un audit d'incrément de T-055 (CSP, `textContent`), environ 1 h. Besoin restant : 6 h, soit 13 h au total, au-delà de la limite de 7 h par ticket (règle 3). Proposition A (recommandée) : estimation de T-043 portée à 7 h (= passé, « audits d'incrément de DEC-011 »), conclu par le coordinateur (R13), et nouveau ticket `tache` « Audit sécurité avant GO » (`agent:securite`, 6 h, critères actuels de T-043, audit d'incrément de T-055 compris), qui reprend la place de T-043 dans `depend_de` de T-046. Proposition B : estimation de T-043 portée à 13 h sans découpage (contraire à la règle 3). Impact des deux : +6 h agent, +90,00 € sur le coût projeté (le temps restant de T-043 est aujourd'hui compté à 0 h). Temps compté dans T-008 · 0 h
- 2026-11-25 16:20 · agent:securite · audit d'incrément de T-063 (commit `b8b0004117bee57e57742167332672bd3cb9e01d`) et T-062 (commit `16282cc9dfe9e10af529ebf607d579961c52e9ae`), DEC-011 : verdict NON BLOQUANT, 0 critique, 0 haute ; constats 2, 4 et 12 fermés ; nouveau constat 16 (bas : 500 interne sans en-têtes de sécurité) ; remarque `api.py:127` sans risque réel ; aucun ticket `bug` ; rapport [securite-2026-11-25-5.md](../rapports/securite-2026-11-25-5.md). Outils absents : `pip-audit`, `safety`, `bandit`, `semgrep`, `gitleaks`, `trivy`. Vérifications sur une instance jetable construite depuis `git archive b8b0004` (conteneurs, réseau, volume et image supprimés ; `apercu-*` et `t067-*` non touchés). Statut laissé `A_FAIRE`, comme aux audits précédents · 1.5 h
