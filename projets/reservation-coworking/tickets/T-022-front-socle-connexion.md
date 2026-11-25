---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-022
titre: Front socle (connexion, mot de passe, navigation) (F-04)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: html-css (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010]          # ex. [T-001, T-002]
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

# T-022 — Front socle (connexion, mot de passe, navigation) (F-04)

## Description
Front HTML/CSS/JavaScript sans framework ni build, servi par l'app (`static/`), selon [architecture.md](../architecture.md) § 2, § 3, § 6 (accessibilité, compatibilité, XSS, CSRF) et décision 3. Ce ticket pose la structure commune et les écrans d'authentification de F-04 et F-07 : connexion, déconnexion, changement de mot de passe (obligatoire et volontaire). Il travaille sur le contrat d'API de l'architecture § 3 et sur le schéma OpenAPI versionné par T-010, en parallèle des tickets backend ; l'intégration complète est vérifiée par T-026. Le contrôle des droits reste côté serveur.

## Critères d'acceptation
- [ ] Pages statiques en modules ES natifs, sans framework, sans étape de build ni dépendance npm, `lang="fr"`.
- [ ] Client d'API commun : corps JSON et `Content-Type: application/json` sur toute requête qui modifie ; une réponse 401 redirige vers la connexion ; une réponse 403 `changement_mot_de_passe_requis` redirige vers l'écran de changement de mot de passe.
- [ ] Écran de connexion (e-mail, mot de passe) et déconnexion ; le message d'échec affiché est celui renvoyé par l'API, identique pour un e-mail ou un mot de passe incorrect.
- [ ] Écran de changement de mot de passe (ancien, nouveau, confirmation), utilisé pour le changement obligatoire et volontaire, avec rappel de la règle de 12 à 128 caractères.
- [ ] Les données sont insérées uniquement avec `textContent` (jamais `innerHTML`) ; aucun script ni style en ligne (compatible avec la CSP `script-src 'self'; style-src 'self'`).
- [ ] CSS adaptatif (la grille passe en liste sous 600 px) ; formulaires natifs avec `<label>`, focus visible, navigation au clavier, erreurs liées aux champs (`aria-describedby`), contraste AA visé.
- [ ] Pied de page avec un lien vers la page de confidentialité (T-025) et l'adresse de support (fournie par T-009).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (interface ; les contrôles d'accès sont côté serveur, revus avec T-013, T-015 et T-020)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
