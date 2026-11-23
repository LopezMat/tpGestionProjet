---
titre: Lot 2 (périmètre C) — changements à intégrer ailleurs
statut: EN_REVUE
responsable: C
version: 0.1
maj_le: 2026-11-23
valide_par:
decision:
---

# Lot 2 (périmètre C) — changements à intégrer ailleurs

Le périmètre C de ce lot comprend 4 agents (`relecteur-code`, `testeur`, `securite`, `deployeur`) et le skill `verifier-prod` avec son script. Il comprend aussi `.claude/settings.json`, deux hooks (`proteger_valide.py` et `restreindre_bash.py`) et leurs trois scripts de test. Leur création fait apparaître onze changements hors de ces fichiers. **Aucun fichier partagé n'a été modifié** : chaque point est à porter par son responsable, par PR (R11 quand une règle ou un format change). Les points 8 et 10 relèvent du lot 5. La section finale donne la procédure « vérifier ses hooks », à appliquer par chaque membre de l'équipe.

| # | Changement | Fichier | Responsable | Voie |
|---|---|---|---|---|
| 1 | Catalogue : outils de `securite` (+ Edit) et de `deployeur` (+ Glob, Grep) ; `curl` remplacé par `verifier_prod.py` ; restrictions Bash désormais appliquées par hook | `docs/ARCHITECTURE.md` § 4 | B | R11 (ARCHITECTURE est VALIDÉ) |
| 2 | Arborescence (nouveaux fichiers de C) et nouveau garde-fou « Bash par agent » | `docs/ARCHITECTURE.md` § 3 et § 6 | B | R11 |
| 3 | Qui passe un ticket `TERMINE` : le `testeur` (réalisation), le `deployeur` (déploiement) ; mention « hook (Lots à venir) » de R5 à actualiser | `CLAUDE.md` | B | R11 |
| 4 | S3 : porte 2 et passage `TERMINE` ; permissions réelles (§ 5) ; production locale (§ 6) | `docs/systemes/S3-deploiement.md` | B (fichier), C (système) | R11 (S3 est VALIDÉ) |
| 5 | Ticket transverse « Revue de code » ; règle 12 (Bash) désormais appliquée techniquement | `.claude/agents/chef-de-projet.md` | B | PR |
| 6 | `/health` en production locale (sans `RENDER_GIT_COMMIT`) ; fichier d'exemple `env.example` plutôt que `.env.example` | `.claude/agents/dev-backend.md`, `architecte.md` | A | PR (+ R11 si le comportement change) |
| 7 | Incidents de rollback pour `gestionnaire-crise` ; runbook `rollback` et `analyste-prod` s'appuient sur `verifier-prod` | `runbooks/`, agents S2 | D | information, au fil de leur lot |
| 8 | Workflows et points d'ARCHITECTURE § 10 | `.github/workflows/`, `scripts/verifier_validations.py` | C | **lot 5** |
| 9 | Plan B si `agent_type` est absent à l'exécution : hooks dans le frontmatter des agents | `.claude/agents/*.md` | B, C | conditionnel (voir § 9) |
| 10 | **Risque : un hook introuvable ne bloque rien** ; parades | postes de l'équipe, `.claude/settings.json` | toute l'équipe ; C | procédure + **lot 5** |
| 11 | Procédure « vérifier ses hooks » dans le README | `README.md` | C | **fait** (section « Installer son poste ») |

---

## 1. Catalogue des agents de C (B)

**Quoi.** Dans `docs/ARCHITECTURE.md` § 4 :
- `securite` : ajouter **Edit** aux outils. Il met à jour son ticket « Audit sécurité » (statut, journal, temps) et ne modifie jamais `app/`.
- `deployeur` : ajouter **Glob** et **Grep** pour retrouver les tickets et les rapports de la livraison. Remplacer `Bash(curl)` par le script `python .claude/skills/verifier-prod/verifier_prod.py`.
- Les mentions `Bash(git diff, git log)` (`relecteur-code`), `Bash(python scripts/tableau.py)` (`chef-de-projet`) et `Bash(gh workflow run, curl)` (`deployeur`) ne sont plus de simples consignes : le hook `.claude/hooks/restreindre_bash.py` les applique. Le relecteur a aussi `git show`, `git status` et `git blame`.

**Pourquoi.** Le champ `tools` d'un subagent n'accepte que des outils entiers. La documentation officielle de Claude Code le confirme : un `Bash(...)` placé dans `disallowedTools` retire tout l'outil. Le catalogue doit décrire ce qui est réellement appliqué. Sans Edit, `securite` devrait réécrire son ticket entier avec Write, ce qui risque d'abîmer le journal.

**Voie.** ARCHITECTURE est `VALIDÉ` : un humain le repasse `EN_REVUE`, puis PR, décision et changelog (R11).

## 2. Arborescence et garde-fous (B)

**Quoi.**
- § 3 : ajouter `.claude/hooks/restreindre_bash.py` (C), `.claude/skills/verifier-prod/verifier_prod.py` (C) et, dans `scripts/`, `test_proteger_valide.py`, `test_restreindre_bash.py` et `test_verifier_prod.py` (C).
- § 6 : ajouter un garde-fou n° 7 « Bash par agent ». Mécanisme : hook PreToolUse `restreindre_bash.py`, qui lit le champ `agent_type` fourni par Claude Code quand un subagent appelle un outil. Effets :
  - pour tout subagent : pas de `git push` (même `git -C . push` ou `bash -c '…'`), pas de `git reset --hard`, pas de `rm` récursif forcé, aucun argument désignant un `.env*` ;
  - listes blanches pour `chef-de-projet`, `relecteur-code` et `deployeur`.
- § 6, garde-fou 1 : la règle R5 vise le **passage** à `VALIDÉ`. Un statut déjà `VALIDÉ` et laissé tel quel n'est pas une écriture de `VALIDÉ` : pour un document, R6 l'a déjà bloqué ; pour un journal, il est exclu de R6.
- § 6, garde-fou 6 : **deux barrières**.
  - Règle `Edit(/templates/**)` dans `settings.json`. Une règle `Edit(...)` couvre aussi Write et MultiEdit (documentation officielle). Le `/` initial ancre le chemin au dossier de lancement de la session, ce qui suppose de lancer Claude Code depuis la racine du dépôt. Sans le `/`, une règle ask viserait tout dossier `templates` à n'importe quelle profondeur, y compris les gabarits d'une app (`projets/x/app/templates/`).
  - **Test réel du 2026-11-23 : cette règle seule n'a pas déclenché de confirmation** (Windows, session en mode auto), alors que la règle deny `Read(**/.env*)` était bien appliquée. Le hook `proteger_valide.py` renvoie donc lui-même une décision `ask` pour tout fichier sous `templates/` à la racine. Il calcule le chemin à partir de `CLAUDE_PROJECT_DIR`, ce qui ne dépend ni du dossier de lancement ni de l'OS. Le nouveau test réel a bien demandé une confirmation, et Ethan l'a refusée. Les gabarits d'une app (`projets/x/app/templates/`) ne sont pas concernés.

**Pourquoi.** Les règles Bash de `settings.json` se contournent : une option avant la sous-commande (`git -C . push`), `bash -c`, ou `cat .env`, qu'une règle `Read` ne couvre pas. Le hook analyse la commande, ce qui en fait une deuxième barrière. Les précisions sur R5 et sur le `/` décrivent le comportement réellement livré et testé.

**Voie.** R11, dans la même PR que le point 1.

## 3. Qui passe un ticket `TERMINE` (B)

**Quoi.** Dans `CLAUDE.md` (§ 1, étape 6, ou R13) :
- **ticket de réalisation** : c'est le `testeur` qui le passe `TERMINE`, et seulement si l'avis `relecteur-code` est `APPROUVÉ`, que la ligne « Revue humaine » est remplie quand elle est requise, que tous les critères sont cochés et que toutes les suites sont vertes ;
- **ticket de déploiement** : c'est le `deployeur` qui le passe `TERMINE`, et seulement si `verifier-prod` a constaté que le SHA en ligne est le SHA attendu ;
- les agents S3 ne passent jamais **leur propre** ticket de travail (« Tests », « Audit sécurité », « Revue de code ») à `TERMINE` : c'est le coordinateur qui conclut.

Dans R5, remplacer « appliquée techniquement par un hook PreToolUse et un contrôle CI (Lots à venir) » par un lien vers `.claude/hooks/proteger_valide.py` (livré) ; le contrôle CI reste prévu au lot 5.

**Pourquoi.** Aujourd'hui, ni CLAUDE.md, ni S3, ni les agents d'A ne disent qui passe un ticket de réalisation `TERMINE` : les dev ne le font jamais, et le coordinateur n'a pas de consigne. Ethan a arbitré à la revue du plan du Lot 2-C. Le `testeur` est la dernière porte par ticket, et il est indépendant de l'auteur (S3-R1).

**Voie.** R11 : PR, décision (qui cite l'arbitrage de la revue du plan) et entrée dans le changelog.

## 4. S3 (B pour le fichier, C pour le système)

**Quoi.** Dans `docs/systemes/S3-deploiement.md` :
- **§ 3, porte 2** : ajouter « le `testeur` coche les critères qu'il a constatés et passe le ticket `TERMINE` (R13) ».
- **§ 5** :
  - remplacer `Write(templates/**)`, `Edit(templates/**)` par `Edit(/templates/**)`, qui couvre aussi Write ;
  - ajouter la ligne « Bash des subagents » (hook `restreindre_bash.py`) ;
  - préciser que la règle `Read(**/.env*)` ne couvre pas Bash, et que c'est le hook qui s'en charge pour les subagents ;
  - noter que `MultiEdit` est un outil ancien, couvert par les règles `Edit`.
- **§ 6** : production locale. Elle est admise si `projet.md` porte `hebergement: local` et `url_prod: http://localhost:<port>`, après une décision humaine (« hébergeur différent de Render »). `verifier-prod` fonctionne à l'identique.

**Pourquoi.** S3 doit décrire ce qui est appliqué. Pour la production locale, le professeur peut dispenser l'équipe d'hébergement réel ; la preuve par le SHA reste la même.

**Voie.** S3 est `VALIDÉ` : un humain le repasse `EN_REVUE`, puis PR, décision et changelog (R11).

## 5. `chef-de-projet` : ticket « Revue de code » et règle 12 (B)

**Quoi.**
- **Règle 6** (tickets transverses obligatoires) : ajouter un ticket `tache` « Revue de code », un par projet, assigné à `agent:relecteur-code`, estimé à environ 0,5 h par ticket de réalisation.
- **Règle 12** : le *Pourquoi* peut indiquer que la limite est désormais appliquée par le hook `restreindre_bash.py` (seule la commande `python scripts/tableau.py [options]` est acceptée, sans opérateur ni redirection).

**Pourquoi.** Le `relecteur-code` n'écrit que la section « Revue » du ticket relu : son temps ne peut pas aller dans le ticket du développeur, sinon il serait imputé au taux de l'assigné (un salarié, peut-être). Sans ticket dédié, le temps de revue n'est rattaché à rien et le budget consommé est sous-estimé. C'est le même principe que le ticket « Pilotage » du chef (règle 14).

**Voie.** PR de B (comportement du chef : entrée dans le changelog si l'équipe le juge nécessaire).

## 6. `/health` en production locale et fichier d'exemple (A)

**Quoi.**
- **`dev-backend`, règle 6** : `/health` renvoie `commit` à partir de `RENDER_GIT_COMMIT`, avec un repli sur une variable `GIT_COMMIT` fournie au lancement local (`GIT_COMMIT=$(git rev-parse HEAD) …`). Sans l'une ni l'autre, le champ vaut `"inconnu"`, et `verifier-prod` conclura à un échec.
- **`architecte`, `dev-*`** : la règle `deny` sur `**/.env*` interdit aussi `.env.example`. Le fichier d'exemple s'appelle donc `env.example`, sans point initial.

**Pourquoi.** Sans repli, une app lancée en local ne peut pas prouver sa version, et la vérification en ligne serait impossible si l'équipe est dispensée d'hébergement réel. Le nom `.env.example` serait refusé en lecture comme en écriture.

**Voie.** PR de A ; R11 si l'équipe considère que c'est un changement de règle.

## 7. Interfaces avec S2 (D, information)

**Quoi.**
- Le `deployeur` crée, en cas d'échec de vérification, un ticket `incident` `critique` assigné à `agent:gestionnaire-crise`, qui cite le runbook `rollback` et le rapport de déploiement.
- Le runbook `rollback` peut s'appuyer sur `verifier-prod` (script, codes retour 0, 1, 2 et 3) et sur son fichier d'état `projets/<slug>/rapports/verifier-prod-<sha7>.json`.
- L'`analyste-prod` lit le rapport de déploiement (SHA, URL) comme point de départ du suivi (S3 § 8), et peut relancer `verifier-prod` pour constater la version en ligne.

**Pourquoi.** Les interfaces S3 → S2 décrites en S3 § 8 doivent correspondre aux fichiers et outils réellement livrés.

**Voie.** À prendre en compte par D dans ses agents et runbooks.

## 8. Lot 5 (C)

**Quoi.** Hors de ce lot, à livrer au lot 5 :
- **workflows** :
  - `ci.yml` et `securite.yml` (filtrés sur `projets/<slug>/app/**`) ;
  - `deploy.yml`, avec les entrées `projet` et `sha`, la sauvegarde `pg_dump` en artefact, le deploy hook Render en secret, puis l'appel de `verifier_prod.py` et le rollback si échec ;
  - `tableau.yml` ;
  - `validations.yml` avec `scripts/verifier_validations.py`. C'est le filet contre une écriture sur un document `VALIDÉ` faite par Bash (`sed -i`, redirection), que les hooks Write/Edit ne voient pas.
- **ARCHITECTURE § 10** :
  - 10.1 : valeurs définitives des retries (30 s et 15 min sont proposées et paramétrables dans `verifier_prod.py`) et comportement au timeout (actuellement : ÉCHEC, donc rollback) ;
  - 10.2 : base persistante, emplacement et durée de rétention des sauvegardes ;
  - 10.3 : mécanisme de rollback, et son test tracé dans un rapport (S3-R7).
- **Production locale** : procédure de « déploiement » local (démarrer l'app au SHA attendu, avec `GIT_COMMIT`) et de sauvegarde locale.
- **`onFailure: "block"`** sur les deux hooks (voir le point 10).

**Pourquoi.** Ces points relèvent du lot workflows (ARCHITECTURE § 11) ; le `deployeur` s'arrête proprement tant qu'ils n'existent pas.

**Voie.** Lot 5 (C), avec une décision pour chaque point de § 10.

## 9. Plan B si `agent_type` manque (B, C — conditionnel)

**Quoi.** Si le test réel montre que Claude Code ne transmet pas `agent_type` aux hooks, chaque agent restreint déclare son propre hook dans son frontmatter :
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: command -v python >/dev/null 2>&1 && P=python || P=python3; "$P" "$CLAUDE_PROJECT_DIR/.claude/hooks/restreindre_bash.py" --agent chef-de-projet
```
Cela vaut pour `chef-de-projet` (B), `relecteur-code` et `deployeur` (C). Le script accepte déjà l'option `--agent`, qui est testée.

**Pourquoi.** La documentation officielle de Claude Code indique que les hooks du frontmatter ne tournent que pendant l'exécution de l'agent. C'est la voie de repli documentée ; elle exige seulement de modifier des fichiers d'agents.

**Résultat du test réel (2026-11-23) : plan B inutile.** Un subagent `Explore` a lancé `echo .env` ; `restreindre_bash.py` l'a refusé (S3-R8), ce qui prouve que `agent_type` est transmis aux hooks de `settings.json`. Dans le même test, `git -C . status` est passé : seules les commandes interdites sont bloquées. Le refus de `echo .env` est volontairement large : tout argument qui contient `.env` est refusé, même sans lecture de fichier. C'est la fermeture par défaut, à assouplir par R11 si cela gêne.

**Voie.** Seulement si un test ultérieur (nouvelle version de Claude Code) montre que `agent_type` n'est plus transmis.

## 10. Risque : un hook introuvable ne bloque rien (toute l'équipe ; C)

**Quoi.** Selon la documentation officielle des hooks, un hook qui ne démarre pas (commande `python` introuvable, script absent) ou qui sort avec un code autre que 0 ou 2 est une **erreur non bloquante** : l'action continue, avec un simple avis `hook error` dans la conversation. Si `python` manque sur un poste, R5, R6 et la restriction Bash **disparaissent en silence** sur ce poste.

**Parades.**
1. **Commande Python résolue sur chaque OS (parade appliquée).** Les noms diffèrent selon le système :
   - sous **Windows** (installateur python.org), seul `python` existe ; `python3` est absent, ou n'est qu'un raccourci du Microsoft Store qui ne lance rien ;
   - sous **macOS** (et souvent Linux), c'est l'inverse : `python3` existe, `python` souvent pas.

   Une commande fixe désactiverait donc les hooks en silence sur une partie des postes. Les deux hooks utilisent maintenant :
   ```
   command -v python >/dev/null 2>&1 && P=python || P=python3; "$P" "$CLAUDE_PROJECT_DIR/.claude/hooks/<hook>.py"
   ```
   `python` est essayé en premier, à cause du raccourci du Store. La commande a été testée sous Git Bash sur le poste d'Ethan (`C:\Python312\python.exe`, 3.12.6) :
   - le JSON arrive bien sur stdin ;
   - les codes 0 et 2 et la sortie JSON `ask` sont transmis tels quels ;
   - avec un PATH sans `python`, le repli sur `python3` fonctionne ;
   - sans aucun des deux, l'échec donne le code 127, une erreur non bloquante. C'est le cas que le test 1 de la procédure permet de repérer.

   Les règles `allow` de `settings.json` et les listes blanches de `restreindre_bash.py` acceptent `python` et `python3` (et `py` pour le hook).
2. **Les hooks se ferment en cas de doute** : JSON illisible ou erreur interne donnent un refus (code 2), jamais un passage.
3. **Lot 5** : ajouter `"onFailure": "block"` aux deux hooks, pour que leur échec bloque l'action. Ce champ demande Claude Code **2.1.295 ou plus** ; le poste d'Ethan a la 2.1.285. Il n'est pas ajouté maintenant, parce qu'un champ inconnu risquerait d'invalider tout `settings.json`.
4. **Filet CI** : `validations.yml` (lot 5) détecte après coup un document passé `VALIDÉ` sans `valide_par` ni `decision` valide.

**Pourquoi.** Une protection qui peut tomber sans bruit n'est pas une protection. L'équipe doit savoir comment vérifier qu'elle est active.

**Voie.** Procédure appliquée par chaque membre dès maintenant ; `onFailure` au lot 5.

## 11. Procédure « vérifier ses hooks » dans le README (fait)

**Quoi.** La section « Installer son poste » de `README.md` reprend la procédure ci-dessous, avec les prérequis (Python 3.10+, Git, Claude Code lancé à la racine) et les variantes `python3` pour macOS.

**Pourquoi.** Chaque nouveau poste et chaque mise à jour de Python ou de Claude Code peuvent désactiver les hooks sans bruit (point 10). Le README est le premier fichier qu'ouvre un nouveau membre.

**Voie.** Ajoutée dans la PR du Lot 2-C. Le README n'est pas un document validé (pas d'en-tête) ; B en reste responsable pour la suite.

---

## Procédure : vérifier ses hooks (chaque membre de l'équipe)

Prérequis : **lancer Claude Code depuis la racine du dépôt**. Les chemins de `settings.json` qui commencent par `/` (par exemple `Edit(/templates/**)`) sont relatifs au dossier de lancement.

Sous Windows, les commandes se tapent dans Git Bash ; sous macOS et Linux, dans le terminal. **Sur Mac, remplacer `python` par `python3`** dans les commandes ci-dessous si `python` n'existe pas.

| # | Commande (à la racine du dépôt) | Résultat attendu |
|---|---|---|
| 1 | `python --version` (Windows) ou `python3 --version` (Mac) | `Python 3.10` ou plus. Si **aucune** des deux commandes ne répond, installer Python ou corriger le PATH : sans Python, les hooks échouent **sans rien bloquer**. |
| 2 | `printf '%s' '{"tool_name":"Write","tool_input":{"file_path":"docs/essai.md","content":"---\nstatut: validé\nvalide_par:\n---\n"}}' \| python .claude/hooks/proteger_valide.py; echo "code=$?"` (Mac : `python3`) | le message `Refusé (R5) : seul un humain passe un document à VALIDÉ…` puis `code=2` |
| 3 | Dans Claude Code : « ajoute une espace à la fin de docs/ARCHITECTURE.md » | l'édition est refusée, avec un message qui contient `Refusé (R6) : docs/architecture.md est VALIDÉ…`. Claude Code préfixe ce refus par `PreToolUse:Edit hook error`, ce qui est **normal**. La protection est **inactive** si l'édition passe, ou si le message ne contient pas `Refusé` (par exemple `Failed with non-blocking status code`, `command not found`, `No such file or directory`) : revoir le test 1. |

En complément, la commande `/hooks` dans Claude Code doit lister les deux hooks PreToolUse (`Write|Edit|MultiEdit` et `Bash`). Les trois commandes suivantes doivent être entièrement vertes :
```
python scripts/test_proteger_valide.py      # Mac : python3 scripts/test_proteger_valide.py
python scripts/test_restreindre_bash.py     # Mac : python3 …
python scripts/test_verifier_prod.py        # Mac : python3 …
```
