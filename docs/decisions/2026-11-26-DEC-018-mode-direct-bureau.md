---
titre: Mode « Direct » de la page « Le bureau » (activité en temps réel, optionnel et local à chaque poste)
statut: EN_REVUE
responsable: D
version: 0.1
maj_le: 2026-11-26
valide_par:                 # rempli par l'humain qui valide
decision:                   # pour un fichier de décision : son propre id, rempli à la validation
# Champs propres à la décision
id: DEC-018
date: 2026-11-26
decide_par: Ethan
projet: ESN
ticket:                     # outil interne : aucun ticket client (DEC-009, point D)
modifie_une_regle: oui      # nouvelle règle d'outillage : hook d'observation non bloquant, local, liste blanche
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-018 — Mode « Direct » de la page « Le bureau »

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la demande d'Ethan du 2026-11-26 (branche `outil/bureau-direct`), du plan qu'il a accepté et de sa modification : le mode Direct est optionnel et local à chaque poste. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ`, et qui renseigne `valide_par` et `decision`.
>
> **Numérotation.** Le 2026-11-26, avant le commit, DEC-018 était libre dans `docs/decisions/` et sur toutes les branches locales et distantes (après `git fetch --all`).

## Contexte
La page « Le bureau » (DEC-016, DEC-017) montre l'état des tickets (Instantané) et rejoue leurs journaux (Replay). Ethan veut un troisième mode, « Direct », qui montre en temps réel ce que font le coordinateur et les sous-agents dans Claude Code : qui lit, qui écrit, qui lance un terminal, quel agent est lancé, qui attend une autorisation. C'est un outil interne, en lecture seule. C'est la phase 1 : on observe, on n'agit pas.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| 1. Hook d'observation déclaré dans `.claude/settings.local.json` (personnel, hors Git) par `bureau_direct.py --installer`, journal local, serveur local SSE (retenue) | optionnel ; aucun effet sur les postes qui ne l'installent pas ; une clé inconnue d'une version ancienne de Claude Code ne peut pas désactiver les hooks partagés (R5, R6) ; installation et retrait en une commande | une étape d'installation par poste, puis un redémarrage de Claude Code |
| 2. Hook déclaré dans `.claude/settings.json` (partagé) | actif partout sans installation | un poste avec une version plus ancienne de Claude Code pourrait ignorer **tous** les hooks si une clé (`async`) lui est inconnue, R5 et R6 compris ; impose un journal à toute l'équipe |
| 3. Lecture des transcripts de Claude Code par le serveur | aucun hook | les transcripts contiennent le texte des messages, les fichiers et les commandes : contraire à l'exigence de ne rien en exposer |

## Décision
1. **Optionnel et local à chaque poste.** `.claude/settings.json` (partagé) n'est pas modifié. Le hook d'observation est déclaré dans **`.claude/settings.local.json`**, personnel et ignoré par Git : la ligne est ajoutée au `.gitignore` du dépôt pour toute l'équipe, au lieu de compter sur le gitignore global de chaque poste.
   - `python scripts/bureau_direct.py --installer` ajoute **uniquement** les groupes `journal_direct.py`, sans toucher au reste du fichier, et de façon idempotente : une réinstallation identique ne réécrit rien et ne réordonne pas les hooks personnels. Il fait une sauvegarde (`settings.local.json.sauvegarde-AAAAMMJJ-HHMMSS`) avant toute écriture, écrit de façon atomique, et refuse un JSON invalide sans écraser le fichier.
   - `--desinstaller` retire ces groupes, et eux seulement.
   - Après l'une ou l'autre commande, il faut relancer Claude Code.
   - **`async` seulement si la version locale le prend en charge.** L'installateur lit `claude --version` et ajoute `"async": true` à partir de **2.1.332**, version dont le schéma des hooks a été vérifié dans le binaire (le 2026-11-26). Avec une version plus ancienne ou introuvable, ou avec `--sans-async`, les hooks sont synchrones. `SessionEnd` est toujours synchrone (timeout de 3 s), car un hook async risque d'être tué à la sortie.
2. **Événements observés** (schémas vérifiés dans le binaire 2.1.332) : `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `Notification` (`permission_prompt`, `idle_prompt`, `elicitation_dialog` ; `auth_success` est ignoré), `SubagentStart`, `SubagentStop`, `Stop` et `SessionEnd`.
3. **Journal par liste blanche.** `.claude/hooks/journal_direct.py` ajoute une ligne JSON par événement dans `direct/evenements.jsonl` (hors Git). Chaque ligne contient :
   - version, heure, session et instance d'agent **hachées** (HMAC avec un sel local `direct/.sel`) ;
   - acteur : `coordinateur`, ou nom de l'agent filtré ;
   - type d'événement ;
   - nom d'outil connu (un outil MCP devient `mcp`, un outil inconnu `autre`) ;
   - catégorie (`lit`, `tape`, `terminal`, `delegue`, `web`, `autre`) et un détail tiré d'une énumération.

   La ligne est **construite**, jamais copiée depuis l'entrée. **Ne sont jamais écrits** : le texte des messages, le contenu ou le chemin des fichiers, les commandes, les sorties d'outils, le dossier de travail, les transcripts. Rotation au-delà de 1 Mio (une archive, `evenements.1.jsonl`). Les écritures concurrentes passent par un verrou ; au-delà de 200 ms d'attente, l'événement est abandonné. `ESN_DIRECT=off` suspend le journal.
4. **Le hook ne bloque jamais.** C'est la politique inverse des hooks de sécurité, qui ferment par défaut : il rend toujours le code 0, n'écrit rien sur stdout (aucune décision), avale toute erreur et ne lit ni ne modifie les autres hooks. R5, R6 et R17 restent appliqués par `proteger_valide.py` et `restreindre_bash.py`, inchangés.
5. **Serveur local** `scripts/bureau_direct.py` (bibliothèque standard) :
   - il écoute **uniquement sur 127.0.0.1** (adresse fixée dans le code, port configurable, 8765 par défaut) ;
   - il n'accepte que **GET** (toute autre méthode reçoit 405) ;
   - il **contrôle l'en-tête Host** contre le DNS rebinding (`127.0.0.1:<port>` ou `localhost:<port>`) et refuse `Sec-Fetch-Site: cross-site` ;
   - il n'envoie **aucun en-tête CORS** ;
   - il sert `console/` en lecture seule et **ne permet jamais d'en sortir** : décodage unique, refus des octets nuls, des `\`, des `:` et des segments cachés ou `..`, contrôle du chemin réel, liens symboliques compris, et types de fichiers en liste blanche ;
   - il ajoute des en-têtes de sécurité (CSP, `nosniff`, `no-store`, `DENY`) ;
   - il diffuse le journal en **SSE** (`/direct/flux`) : les 15 dernières minutes à la connexion, puis le fil de l'eau, avec reprise par `Last-Event-ID` et suivi de la rotation ; chaque ligne est revalidée par la liste blanche du hook (code partagé) ;
   - il n'écrit rien et n'exécute aucune commande. La seule commande lancée par le script est `claude --version`, par l'installateur.
6. **Rendu.** La page « Le bureau » a un troisième mode, « Direct ». Il n'est disponible que si la page est servie par ce serveur ; en `file://`, le bouton est désactivé avec une explication.
   - **Interface** : un indicateur connecté / déconnecté, avec reconnexion automatique.
   - **Animations** :

     | Événement | Animation |
     |---|---|
     | message reçu | bulle « nouvelle demande » |
     | Read, Grep, Glob | icône « lit » |
     | Edit, Write | icône « écrit », et la pose de frappe au poste |
     | Bash | icône « terminal » |
     | lancement d'un sous-agent | l'agent va à son poste |
     | fin du sous-agent | retour au café |
     | autorisation ou attente | main levée « ! » |
     | fin du tour | le coordinateur revient à l'accueil |

   - **Deux coordinateurs** : si deux sessions ou plus sont actives en même temps (un événement dans les 15 dernières minutes, sans fin de session), un avertissement s'affiche : « une seule personne au coordinateur ».
   - **Accessibilité** : `prefers-reduced-motion` est respecté. Une liste texte présente les 30 derniers événements, et une région `aria-live` annonce les faits marquants, au plus une annonce toutes les 3 s.
7. **Tests** :
   - `scripts/test_journal_direct.py` couvre le hook : code 0 dans tous les cas, aucun contenu interdit écrit, correspondance des événements, rotation, dossier ou fichier absent, écritures concurrentes. Il vérifie aussi que `settings.json` ne déclare pas ce hook et n'est pas modifié par la branche ;
   - `scripts/test_bureau_direct.py` couvre le serveur (écoute locale, Host, méthodes, CORS, path traversal, format SSE, rotation, reprise, aucune exécution) et l'installateur (ajout, retrait, idempotence, contenu conservé, JSON invalide refusé sans écraser) ;
   - les ajouts à `test_bureau.py` couvrent le mode Direct dans la page générée et le JS ;
   - les trois suites sont reprises automatiquement par `ci.yml`.

## Pourquoi
*(Ethan, 2026-11-26)*
- Voir en direct ce que font le coordinateur et les agents rend la supervision concrète, pour l'équipe comme pour la soutenance.
- Le mode doit rester optionnel et local : un poste avec une version plus ancienne de Claude Code ne doit jamais risquer de perdre ses hooks de sécurité (R5, R6) à cause d'une clé inconnue dans le fichier partagé.
- On n'observe que des métadonnées : rien de ce qui est dit, lu, écrit ou exécuté ne doit sortir de Claude Code.

## Impacts
- **Fichiers** :
  - nouveaux : `.claude/hooks/journal_direct.py`, `scripts/bureau_direct.py`, `scripts/test_journal_direct.py`, `scripts/test_bureau_direct.py`, ce fichier ;
  - modifiés : `scripts/bureau.py` et `scripts/bureau.js` (mode Direct), `scripts/test_bureau.py`, `.gitignore` (`/direct/`, `/.claude/settings.local.json` et ses sauvegardes), `README.md`, `docs/ARCHITECTURE.md` (§ 3 et § 6, document repassé `EN_REVUE` par Ethan), `docs/decisions/README.md`, `docs/CHANGELOG-REGLES.md`.
  - **Non modifiés** : `.claude/settings.json` (partagé) et `CLAUDE.md` (aucune règle R1 à R17 ne change).
- **Règle** : nouvelle règle d'outillage, « le mode Direct est optionnel et local : son hook est déclaré seulement dans `settings.local.json`, n'enregistre que des métadonnées en liste blanche, hors Git, et ne bloque jamais ; son serveur n'écoute qu'en local, en lecture seule ». Elle figure dans le CHANGELOG (R11).
- **Risques suivis** :
  - une session fermée brutalement reste comptée comme active 15 min au plus, d'où un faux avertissement « deux coordinateurs » possible ;
  - les hooks async peuvent arriver dans le désordre (traité par les horodatages et l'effacement automatique des icônes) ;
  - les autres comptes du même poste peuvent lire `127.0.0.1:8765`, qui ne donne que des métadonnées.
- **Tickets** : aucun. Outil interne ; le client ne paie pas l'outillage de l'ESN (DEC-009, point D).
