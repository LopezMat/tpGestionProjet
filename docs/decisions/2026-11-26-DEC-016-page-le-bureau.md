---
titre: Page « Le bureau » de la console (vue de dessus et replay, outil interne, lecture seule)
statut: EN_REVUE
responsable: D
version: 0.1
maj_le: 2026-11-26
valide_par:                 # rempli par l'humain qui valide
decision: DEC-016           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-016
date: 2026-11-26
decide_par: Ethan
projet: ESN
ticket:                     # outil interne : aucun ticket client (DEC-009, point D)
modifie_une_regle: oui      # nouvelle page d'outillage : lecture seule, états lus dans les tickets (R9)
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-016 — Page « Le bureau » de la console

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la demande d'Ethan du 2026-11-26 (branche `outil/bureau`) et du plan qu'il a accepté, avec ses trois ajouts. Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`.
>
> **Numérotation.** Le 2026-11-26, avant le commit, DEC-016 était libre dans `docs/decisions/` et sur toutes les branches locales et distantes (après `git fetch --all`).

## Contexte
La console (DEC-012) présente l'ESN sous forme de tableaux, et la page « qui fait quoi » (DEC-014) montre qui doit agir sur un incrément. Ethan a demandé une vue d'ensemble plus parlante pour la soutenance : l'ESN vue de dessus, en pixel art, où l'on voit qui travaille, qui attend un humain et qui est bloqué, et qui sait rejouer l'histoire d'un projet à partir des journaux des tickets. C'est un outil interne, comme la console, et non un projet client.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| 1. Module séparé `scripts/bureau.py` (calculs) et `scripts/bureau.js` (rendu), appelés par `console.py` (retenue) | logique testable en Python sans navigateur ; `console.py` ne grossit que de quelques lignes ; JS vérifiable par `node --check` ; même gabarit, même navigation et même écriture bornée à `console/` | deux fichiers de plus à maintenir |
| 2. Tout intégrer dans `console.py`, JS dans une chaîne Python | un seul fichier | fichier de plus de 2 500 lignes ; JS illisible et non vérifiable |
| 3. Page autonome, comme `qui_fait_quoi.py` | indépendante de la console | navigation et gabarit dupliqués ; une troisième sortie à gérer |

## Décision
1. **Une page « Le bureau » dans la console** (`console/bureau.html`, entrée de navigation entre « Portefeuille » et « Équipe ») est générée par `scripts/console.py`. Les données et le HTML viennent de **`scripts/bureau.py`**, qui n'écrit aucun fichier. Le rendu Canvas 2D vient de **`scripts/bureau.js`**, copié dans `console/assets/`. La seule fonction d'écriture reste celle de la console, bornée à `console/` (DEC-012). Chaque fiche projet porte un lien vers `bureau.html#projet=<slug>`.
2. **Hors ligne et sans ressource externe.** Toutes les données sont incluses dans la page : il n'y a aucune requête réseau, aucun `fetch()` (bloqué en `file://`), aucune police, image ni sprite externe. Les personnages et le décor sont dessinés par le code, en pixel art 16 bits, ce qui évite toute question de licence.
3. **Plan construit dans le code** :
   - une pièce par système (S4 salle de réunion client, S1 bureau du chef de projet, S2 supervision, S3 salle serveur et déploiement), l'open space du pôle réalisation, les bureaux des salariés, l'accueil du coordinateur et un coin café ;
   - un agent va dans la pièce de son `systeme` (`equipe/agents.md`). Au-delà de la capacité de la pièce, ou s'il est hors catalogue, il va dans l'open space. **Un agent ajouté plus tard apparaît donc sans modifier le code**, et son accessoire est choisi par mots-clés dans son nom et sa description ;
   - un humain qui n'est pas dans `equipe/` (`decide_par`, `salarie:ethan`…) devient un visiteur de l'accueil.
4. **Mode instantané : l'état vient des tickets (R9).**
   - `EN_COURS` : au bureau, il tape.
   - `EN_REVUE` : il se rend chez le `relecteur-code`, ou chez le `testeur` si l'avis de revue est `APPROUVÉ`.
   - `ATTENTE_HUMAIN` : un « ! » apparaît au-dessus de l'humain attendu, c'est-à-dire le salarié assigné, sinon le premier salarié cité dans `bloque_par`, sinon « Équipe ESN ».
   - `BLOQUE` : bulle rouge.
   - Sinon : machine à café (l'accueil pour le coordinateur et les visiteurs).
   - Quand un personnage a plusieurs tickets, le plus urgent l'emporte. La page n'utilise pas `qui-fait-quoi.json` (DEC-014).
5. **Mode replay : chronologie des lignes « Journal » des tickets et des décisions DEC.**
   - L'analyse accepte les variantes réelles : pas d'heure, « · » dans le texte, texte après le temps, `qui (saisi par)`, `coordinateur pour agent:x`.
   - Une ligne mal formée est ignorée et listée dans les anomalies de la page, sans jamais interrompre la génération.
   - Une ligne sans heure reprend celle de la ligne précédente du même ticket et du même jour (marque « ~ »).
   - Une DEC prend l'heure de la première ligne du journal du ticket lié qui la cite le même jour ; sinon, elle est placée en fin de journée et marquée « heure non renseignée ».
   - Commandes : lecture, pause, pas à pas, vitesse ×1 à ×10, curseur.
   - **Filtre « jalons seulement » activé par défaut** : création, changements de statut et décisions. La cadence s'adapte pour un film d'environ 90 s à ×1. Le mode « tout » reste disponible.
   - Une validation humaine s'affiche comme un événement visible : l'humain va à la salle de réunion et une bannière « ✔ DEC-NNN · décidé par … » apparaît.
   - Le replay raconte, il n'affirme aucun statut : seul l'instantané dit l'état.
6. **Accessibilité.**
   - `prefers-reduced-motion` est respecté : déplacements instantanés, aucun clignotement, aucune animation de décor, rien ne démarre seul. La lecture lancée par l'utilisateur reste possible, sans mouvement.
   - Deux listes texte générées côté serveur servent d'alternative au dessin : « Personnages et état », avec un bouton par personnage qui ouvre sa fiche, et « Événements du replay », qui suit la lecture (`aria-current`).
   - Une région `aria-live` annonce l'événement courant en pas à pas ; le canvas porte un résumé dans `aria-label`.
7. **Sécurité.**
   - Tout le HTML produit en Python est échappé.
   - Les données sont injectées dans `<script type="application/json">` sans aucun `<`, `>`, `&`, U+2028 ni U+2029 bruts, et le JSON reste valide.
   - Le JS n'affiche les textes que par `textContent` et `fillText`, sans `innerHTML` ni `eval`, et revalide chaque lien (chemin relatif `.html` de la console).
   - **Pas de CSP par `<meta>`** : en `file://`, la source `'self'` est traitée différemment selon les navigateurs et pourrait bloquer `assets/bureau.js`.
8. **Tests** : `scripts/test_bureau.py`, repris automatiquement par `ci.yml`, et les ajouts à `test_console.py`. Ils couvrent :
   - la génération et la lecture seule ;
   - l'analyse des journaux, y compris les lignes mal formées ;
   - la correspondance statut → état et l'humain attendu ;
   - le plan, avec débordement et agent hors catalogue ;
   - l'échappement, avec un ticket piégé ;
   - l'absence de ressource externe et de construction dangereuse dans le JS ;
   - la syntaxe JS (`node --check` si `node` est présent).
9. **Vérification visuelle** : captures Edge en mode headless de la page générée sur les vrais projets (instantané, replay en cours, fiche ouverte, mouvements réduits), avec corrections avant le commit.

## Pourquoi
*(Ethan, 2026-11-26)*
- Une vue d'ensemble plus parlante que des tableaux pour suivre l'ESN et la présenter en soutenance.
- C'est un outil interne de l'ESN, en lecture seule, qui s'appuie uniquement sur les tickets (R9), leurs journaux et les décisions.
- Le replay doit tenir en un film court (jalons par défaut), sans perdre le détail (mode « tout »).

## Impacts
- **Fichiers** :
  - nouveaux : `scripts/bureau.py`, `scripts/bureau.js`, `scripts/test_bureau.py`, ce fichier ;
  - modifiés : `scripts/console.py` (navigation, page, copie du JS, CSS, lien depuis la fiche projet), `scripts/test_console.py`, `README.md` (section Console et liste des tests), `docs/decisions/README.md`, `docs/CHANGELOG-REGLES.md`, `docs/ARCHITECTURE.md` § 3 (arborescence : `bureau.py`, `bureau.js`, `test_bureau.py`), document repassé `EN_REVUE` par Ethan.
- **Règle** : nouvelle règle d'outillage, « la page Le bureau est en lecture seule, n'écrit que dans `console/`, tire ses états des tickets et n'utilise aucune ressource externe ». Elle figure dans le CHANGELOG (R11).
- **Tickets** : aucun. C'est un outil interne, et le client ne paie pas l'outillage de l'ESN (DEC-009, point D).
