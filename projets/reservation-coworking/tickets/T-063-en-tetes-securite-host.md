---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-063
titre: En-têtes de sécurité et contrôle de l'en-tête Host (constats 2 et 4)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: api-rest (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-063 — En-têtes de sécurité et contrôle de l'en-tête Host (constats 2 et 4)

## Description
Constats 2 et 4 (bas) des rapports `securite` du 2026-11-25 (repris dans [securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md)), toujours ouverts. `app/reservation/app.py` n'envoie ni CSP, ni `nosniff`, ni `Referrer-Policy`, ni `frame-ancestors` (constat 2), et ne valide pas l'en-tête `Host` : une page malveillante ouverte sur le poste pourrait lire les disponibilités de [T-054](T-054-api-consultation-disponibilites.md) par DNS rebinding sur `127.0.0.1` (constat 4). Recommandation du `securite` : à faire avant ou avec T-055, au plus tard avec T-054.

Les en-têtes étaient prévus dans T-013 (critère « Toutes les réponses portent la CSP… »), mais T-054 et T-055 publient des données avant T-013 (DEC-011). Ce ticket les pose dès l'incrément ; T-013 vérifie seulement qu'ils restent présents sur ses routes. **À réaliser dans l'incrément, juste après T-054** ; T-055 n'en dépend pas, pour ne pas bloquer la page de la soutenance, mais elle doit être compatible avec cette CSP (critère ajouté à T-055).

**Touche la sécurité** : revue humaine obligatoire, ticket compagnon **T-064** (Karim).

## Critères d'acceptation
- [ ] Toutes les réponses (page statique, `/api/*`, `/health`, une 404) portent la CSP de l'[architecture](../architecture.md) § 6 (`default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'`), `X-Content-Type-Options: nosniff` et `Referrer-Policy: no-referrer` (test sur ces 4 types de réponse).
- [ ] Une requête dont l'en-tête `Host` n'est pas `localhost` ni `127.0.0.1` (avec ou sans port) est refusée (400) ; ces deux hôtes sont acceptés (tests). La liste est fixée dans le code : aucune nouvelle variable d'environnement obligatoire (critère de T-010).
- [ ] `/health` reste joignable par `http://localhost:<port>` pour `verifier-prod` et `deployer_local.py` (test).
- [ ] La page actuelle (`static/index.html`) s'affiche sans erreur CSP dans la console du navigateur (vérification notée au journal).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (en-têtes de sécurité et contrôle d'accès par l'hôte, S3-R2 ; ticket compagnon T-064)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 23:50 · agent:chef-de-projet · création (triage des constats 2 et 4) · 0 h
