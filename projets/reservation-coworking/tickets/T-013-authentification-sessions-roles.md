---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-013
titre: Authentification, sessions et rôles (F-04)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-011]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-25
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-013 — Authentification, sessions et rôles (F-04)

## Description
Composant `auth` de [architecture.md](../architecture.md) § 3, § 6 et § 7 pour F-04 (identification des membres) et le contrôle des rôles de F-07 : hachage Argon2id, sessions opaques en base, `POST` et `DELETE /api/session`, dépendances `utilisateur_connecte` et `exiger_role("accueil")`, protections CSRF et en-têtes de sécurité. La limitation des tentatives est dans T-014, le changement de mot de passe dans T-015.

**Touche la sécurité** : revue humaine obligatoire (S3-R2, CDC § 8, DEC-006), ticket compagnon **T-030** (Karim), qui confirme aussi les seuils d'expiration de session (DEC-007, point G).

## Critères d'acceptation
- [ ] **Hachage (F-04)** : les mots de passe ne sont jamais stockés en clair ; un contrôle de la base montre uniquement des empreintes salées Argon2id (argon2-cffi, paramètres RFC 9106, format PHC), et aucun mot de passe en clair n'apparaît dans les journaux ni dans les réponses de l'API (test).
- [ ] Un utilisateur dont le compte existe se connecte avec son e-mail (normalisé en minuscules, espaces retirés) et son mot de passe ; `DELETE /api/session` le déconnecte et révoque la session (test).
- [ ] Un e-mail ou un mot de passe incorrect est refusé avec le même message « E-mail ou mot de passe incorrect » dans les deux cas ; pour un e-mail inconnu, une vérification Argon2 factice égalise le temps de réponse (test).
- [ ] Session opaque : jeton aléatoire de 256 bits, seule son empreinte SHA-256 est en base ; cookie `HttpOnly`, `SameSite=Strict`, `Path=/`, `Secure` en HTTPS ; expiration après 2 h d'inactivité et 12 h au maximum (seuils provisoires G), testée avec l'horloge injectée.
- [ ] Toute route `/api/*` sauf `POST /api/session` refuse un visiteur non connecté (401) ; les routes `/api/accueil/*` exigent le rôle accueil, lu en base à chaque requête (tests par appel direct à l'API).
- [ ] Il n'existe aucune route ni aucun formulaire d'inscription libre.
- [ ] CSRF : corps JSON obligatoire sur toute requête qui modifie, contrôle de l'en-tête `Origin`, pas de CORS (tests).
- [ ] Toutes les réponses portent la CSP de l'architecture § 6, `X-Content-Type-Options: nosniff` et `Referrer-Policy: no-referrer` (en-têtes posés par T-063 depuis le 2026-11-25 ; T-013 vérifie qu'ils sont présents sur ses routes) ; les schémas Pydantic refusent les champs inconnus (`extra="forbid"`).
- [ ] **E-mail et empreinte (constat 11, rapport securite-2026-11-25-3)** : l'e-mail est normalisé (minuscules, espaces retirés) avant toute recherche en base ; un compte `a@x.fr` se connecte avec ` A@X.FR ` (test) ; une empreinte absente ou invalide en base donne le refus générique « E-mail ou mot de passe incorrect », jamais une erreur 500 (test).
- [ ] Les journaux capturés pendant les tests ne contiennent ni l'e-mail ni le mot de passe de test.
- [ ] **Aucune donnée personnelle ni aucun secret dans l'URL (constat 15, rapport securite-2026-11-25-4)** : aucune route de T-013 ne prend l'e-mail, le mot de passe ni le jeton de session dans le chemin ou la chaîne de requête (corps JSON en `POST`) ; un test parcourt `docs/openapi.json` et échoue si un paramètre `query` ou `path` de ces routes s'appelle `email`, `mot_de_passe`, `password` ou `token`.
- [ ] Couverture d'au moins 80 % des lignes de `auth`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (authentification, S3-R2 ; ticket compagnon T-030)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
- 2026-11-25 23:50 · agent:chef-de-projet · triage du rapport securite-2026-11-25-3 : critère ajouté (constat 11 : normalisation de l'e-mail avant recherche, casse, empreinte invalide sans erreur 500) ; critère des en-têtes précisé (posés par T-063). Constat 10 : la décision T-057 (rôle PostgreSQL non superutilisateur) est attendue avant le début de ce ticket ; ne rien écrire qui exige des droits de superutilisateur. Temps compté dans T-008 · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage du constat 15 (rapport securite-2026-11-25-4), partie (c) : critère ajouté (aucune donnée personnelle ni secret dans l'URL), règle à respecter aussi par T-014 à T-019 ; estimation de 7 h maintenue (le `POST` à corps JSON est déjà prévu, seul le test de garde s'ajoute). Parties (a) et (b) : T-071 et T-072. Temps compté dans T-008 · 0 h
