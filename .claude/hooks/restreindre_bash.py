#!/usr/bin/env python3
"""Hook PreToolUse (Bash) : restrictions par agent, à partir de `agent_type`.

Responsable : C · Lot 2 (C), lot 5 · voir ARCHITECTURE § 4 (outils du catalogue), S3-R3, S3-R8,
ARCHITECTURE § 6 (garde-fou 7), DEC-002 (lot2-A point 2, lot2-B point 7, lot2-D point 2), DEC-003.

Le champ `tools` d'un subagent autorise l'outil Bash entier ; les règles Bash de
settings.json se contournent (`git -C . push`, `bash -c '...'`). Ce hook est la
deuxième barrière, appliquée seulement aux subagents :

- session principale (pas d'`agent_type`) : rien, les permissions de settings.json s'appliquent ;
- tout subagent : pas de `git push`, pas de `git reset --hard`, pas de `rm` récursif forcé,
  aucun argument qui désigne un fichier `.env*` ;
- listes blanches strictes pour `chef-de-projet`, `relecteur-code`, `deployeur`,
  `analyste-prod` et `gestionnaire-crise` ;
- tout appelant, session principale comprise : `scripts/deployer_local.py` et
  `scripts/rollback_local.py` demandent une confirmation humaine (décision JSON `ask` sur
  stdout), en doublon des règles `ask` de settings.json (S3-R3, DEC-003) ;
- tout appelant, session principale comprise : R17 (DEC-010, DEC-015), aucune écriture par Bash
  dans un fichier `.md` de `docs/` ou de `projets/`. Formes refusées : `sed -i` (et `perl -i`),
  redirections `>`, `>>` (et `>|`, `&>`), `tee`, scripts Python en ligne (`python -c`, `python -`
  ou `python` lisant un heredoc ou un tube) qui écrivent dans ces fichiers ; aussi à l'intérieur de
  `bash -c`, `eval`, d'un heredoc lu par un shell, de `xargs` ou de `find -exec`. Le message renvoie
  vers Edit/Write, seuls outils que voit le hook R5/R6 (`proteger_valide.py`).
  Limites (documentées dans DEC-015) : un script enregistré dans un fichier puis lancé, `cp`, `mv`,
  `patch`, `git checkout` ou un chemin calculé à l'exécution ne sont pas analysés ; la règle R17
  s'applique quand même et `validations.yml` reste le filet pour le statut.

Usage en hook de frontmatter (plan B) : `python restreindre_bash.py --agent <nom>`.
Interpréteur accepté dans les listes blanches : `python`, `python3` (macOS, Linux) ou `py` (Windows).
Code de sortie : 0 = laisse passer (ou `ask` en JSON sur stdout) ; 2 = refus (message sur stderr).
Bibliothèque standard uniquement.
"""
import json
import posixpath
import re
import shlex
import sys

OPERATEURS = {";", "&&", "||", "|", "&", ">", ">>", "<", "<<", "(", ")", "|&", ";;", ">&", "<&", "&>"}
ENVELOPPES = {"timeout", "nohup", "nice", "time", "command", "builtin", "env", "stdbuf", "xargs", "sudo"}
SHELLS = {"bash", "sh", "zsh", "dash"}
RE_ENV = re.compile(r"(^|[\\/=:])\.env", re.IGNORECASE)
RE_ARG_SUR = re.compile(r"^[\w\-=./:@,+]+$")

LISTES_BLANCHES = {
    "chef-de-projet": "python (ou python3) scripts/tableau.py [options]",
    "relecteur-code": "git diff | git log | git show | git status | git blame (sans --output ni --ext-diff)",
    "deployeur": ("python (ou python3) scripts/deployer_local.py [options] | "
                  "python (ou python3) scripts/rollback_local.py [options] | "
                  "python (ou python3) .claude/skills/verifier-prod/verifier_prod.py [options] | "
                  "git rev-parse … | git log … (sans --output ni --ext-diff)"),
    "analyste-prod": "python (ou python3) scripts/sonde_sante.py [options]",
    "gestionnaire-crise": ("python (ou python3) scripts/sonde_sante.py [options] | git log … | git rev-parse … | "
                           "gh run list … | gh run view … (sans --output ni --ext-diff ; jamais gh workflow run)"),
}
GIT_OPTIONS_ECRITURE = ("--output", "--ext-diff")
INTERPRETES = ("python", "python3", "py")
SCRIPTS_DEPLOIEMENT = ("scripts/deployer_local.py", "scripts/rollback_local.py")
MESSAGE_DEPLOIEMENT = ("Mise en production locale (S3-R3, DEC-003) : {script} déploie ou rétablit une "
                       "version de l'application. Confirmation humaine requise : vérifier que le GO "
                       "(DEC-NNN) cite ce SHA, ou que le rollback suit un déploiement en ÉCHEC.")

# -- R17 : documents Markdown modifiés par Edit/Write uniquement (DEC-010, DEC-015) --------------
MESSAGE_R17 = ("Refusé (R17) : un document Markdown de docs/ ou de projets/ ne se modifie jamais par "
               "Bash ({forme}{cible}). Utilise l'outil Edit ou Write : c'est le seul chemin que contrôle "
               "le hook R5/R6 (proteger_valide.py), qui refuse d'écrire VALIDÉ et de toucher un document "
               "figé. Une lecture (cat, grep, head, sed -n) reste permise.")
# Chemin d'un fichier .md sous docs/ ou projets/ (relatif, ./, absolu, séparateur \ ou /, joker).
RE_CHEMIN_MD = re.compile(r"(?:^|[/=])(?:docs|projets)/(?:.*/)?[^/]*\.md$", re.IGNORECASE)
# Dans un script en ligne, le chemin peut être découpé (Path("docs") / "x.md", os.path.join…).
RE_CODE_DOSSIER = re.compile(r"\b(?:docs|projets)\b", re.IGNORECASE)
RE_CODE_MD = re.compile(r"\.md\b", re.IGNORECASE)
RE_CODE_ECRITURE = re.compile(
    r"write_text|write_bytes|\.write\s*\(|\.writelines\s*\(|\.truncate\s*\("
    r"|\bopen\s*\([^)]*?,\s*(?:mode\s*=\s*)?['\"][rbt]*[wax+]"      # open(p, "w" | "a" | "r+" | "x")
    r"|mode\s*=\s*['\"][rbt]*[wax+]"
    r"|O_WRONLY|O_RDWR|O_APPEND|O_TRUNC|O_CREAT"
    r"|\bshutil\.|\bos\.(?:replace|rename|remove|unlink|system|popen)\b|\bsubprocess\b|\bfileinput\b"
    r"|\.(?:replace|rename)\s*\(\s*[^,()]*\)"                         # Path.replace(cible), un seul argument
    r"|\.(?:unlink|touch)\s*\(")
# Heredoc : << MOT, <<- MOT, << 'MOT', << "MOT" (mais pas la here-string <<<).
RE_HEREDOC = re.compile(r"(?<!<)<<(?!<)(-?)[ \t]*(['\"]?)([A-Za-z_][\w.-]*)\2")
OPTIONS_INTERPRETE = r"(?:\s+(?:-[XW]\s*[^\s<|;&)]+|-[A-Za-z]+))*"
RE_PYTHON_STDIN = re.compile(r"(?:^|[\s;|&(`])(?:[^\s;|&(`]*[\\/])?(?:python3?|py)(?:\.exe)?"
                             + OPTIONS_INTERPRETE + r"(?:\s+-)?\s*(?=$|[|;&<)])", re.IGNORECASE)
RE_SHELL_STDIN = re.compile(r"(?:^|[\s;|&(`])(?:[^\s;|&(`]*[\\/])?(?:bash|sh|zsh|dash)(?:\.exe)?"
                            + OPTIONS_INTERPRETE + r"(?:\s+-)?\s*(?=$|[|;&<)])", re.IGNORECASE)
RE_SECOURS_ECRITURE = re.compile(r"(?<![<&\d])>{1,2}(?!&)|\btee\b|--in-place|\bsed\b[^\n]*\s-[A-Za-z]*i"
                                 r"|\bpython3?\b|\bpy\b", re.IGNORECASE)
EDITEURS_EN_PLACE = ("sed", "gsed", "perl")
LANCEURS_FIND = ("-exec", "-execdir", "-ok", "-okdir")


class Refus(Exception):
    pass


def decouper(commande):
    lex = shlex.shlex(commande, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    lex.commenters = ""
    return list(lex)


def segments(jetons):
    courant = []
    for j in jetons:
        if j in OPERATEURS or set(j) <= set(";&|<>()"):
            if courant:
                yield courant
            courant = []
        else:
            courant.append(j)
    if courant:
        yield courant


def nom_exe(jeton):
    base = posixpath.basename(jeton.replace("\\", "/")).lower()
    return base[:-4] if base.endswith(".exe") else base


def sans_prefixes(seg):
    """Retire les affectations VAR=val et les enveloppes (timeout 5, env, nohup…)."""
    i = 0
    while i < len(seg):
        j = seg[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", j):
            i += 1
        elif nom_exe(j) in ENVELOPPES:
            i += 1
            while i < len(seg) and (seg[i].startswith("-") or re.match(r"^\d+[smhd]?$", seg[i])):
                i += 1
        else:
            break
    return seg[i:]


def sous_commande_git(seg):
    """Pour ['git','-C','x','push',...] retourne ('push', reste)."""
    i = 1
    while i < len(seg):
        j = seg[i]
        if j in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            i += 2
        elif j.startswith("-"):
            i += 1
        else:
            return j.lower(), seg[i + 1:]
    return "", []


def controles_communs(commande, profondeur=0):
    """Refus valables pour tout subagent."""
    if profondeur > 3:
        raise Refus("Refusé : commande imbriquée trop profondément.")
    try:
        jetons = decouper(commande)
    except ValueError:
        raise Refus("Refusé : commande illisible (guillemets non fermés).")
    for j in jetons:
        if RE_ENV.search(j):
            raise Refus("Refusé (S3-R8) : un agent ne lit ni n'écrit de fichier .env* ; "
                        "les secrets restent dans les secrets GitHub.")
    for seg in segments(jetons):
        seg = sans_prefixes(seg)
        if not seg:
            continue
        exe = nom_exe(seg[0])
        if exe in SHELLS or exe == "eval":
            for k, j in enumerate(seg[1:], start=1):
                if j == "-c" and k + 1 < len(seg):
                    controles_communs(seg[k + 1], profondeur + 1)
            if exe == "eval":
                controles_communs(" ".join(seg[1:]), profondeur + 1)
        if exe == "git":
            sous, reste = sous_commande_git(seg)
            if sous == "push":
                raise Refus("Refusé (S3-R3) : un agent ne pousse jamais ; la publication du code "
                            "est une action humaine. Rends la main au coordinateur.")
            if sous == "reset" and "--hard" in reste:
                raise Refus("Refusé : git reset --hard est interdit (S3 § 5, action destructrice).")
        if exe == "rm":
            drapeaux = "".join(j[1:] for j in seg[1:] if j.startswith("-") and not j.startswith("--"))
            longs = {j for j in seg[1:] if j.startswith("--")}
            recursif = "r" in drapeaux.lower() or "--recursive" in longs
            force = "f" in drapeaux or "--force" in longs
            if recursif and force:
                raise Refus("Refusé : rm récursif forcé interdit (S3 § 5, action destructrice).")


def args_surs(args):
    return all(RE_ARG_SUR.match(a) for a in args)


def chemin(j):
    j = j.replace("\\", "/")
    return j[2:] if j.startswith("./") else j


def est_script(seg, script):
    """`python|python3|py <script> [options sûres]`, chemin relatif à la racine du dépôt."""
    return (nom_exe(seg[0]) in INTERPRETES and len(seg) >= 2
            and chemin(seg[1]) == script and args_surs(seg[2:]))


def script_deploiement(commande, profondeur=0):
    """Nom du script de déploiement lancé par la commande (même via bash -c), sinon None."""
    if profondeur > 3:
        return None
    try:
        jetons = decouper(commande)
    except ValueError:
        return None
    for seg in segments(jetons):
        seg = sans_prefixes(seg)
        if not seg:
            continue
        exe = nom_exe(seg[0])
        if exe in INTERPRETES:
            for j in seg[1:]:
                if not j.startswith("-"):
                    c = chemin(j)
                    for script in SCRIPTS_DEPLOIEMENT:
                        if c == script or c.endswith("/" + script):
                            return script
                    break
        if exe in SHELLS:
            for k, j in enumerate(seg[1:], start=1):
                if j == "-c" and k + 1 < len(seg):
                    trouve = script_deploiement(seg[k + 1], profondeur + 1)
                    if trouve:
                        return trouve
    return None


def est_sonde(seg):
    """`python|python3|py scripts/sonde_sante.py [options sûres]` (lot2-D point 2)."""
    return (nom_exe(seg[0]) in ("python", "python3", "py") and len(seg) >= 2
            and chemin(seg[1]) == "scripts/sonde_sante.py" and args_surs(seg[2:]))


def git_lecture(seg, sous_commandes):
    """`git <sous-commande de lecture> …`, sans option qui écrit un fichier ou lance un programme."""
    if nom_exe(seg[0]) != "git" or len(seg) < 2 or seg[1].lower() not in sous_commandes:
        return False
    return not any(a.startswith(GIT_OPTIONS_ECRITURE) for a in seg[2:])


def autorise_liste_blanche(agent, seg):
    exe = nom_exe(seg[0])
    if agent == "chef-de-projet":
        return (exe in ("python", "python3", "py") and len(seg) >= 2
                and chemin(seg[1]) == "scripts/tableau.py" and args_surs(seg[2:]))
    if agent == "relecteur-code":
        return git_lecture(seg, ("diff", "log", "show", "status", "blame"))
    if agent == "analyste-prod":
        return est_sonde(seg)
    if agent == "gestionnaire-crise":
        if est_sonde(seg) or git_lecture(seg, ("log", "rev-parse")):
            return True
        return exe == "gh" and len(seg) >= 3 and seg[1] == "run" and seg[2] in ("list", "view")
    if agent == "deployeur":
        # DEC-003 : production locale Docker ; plus de gh workflow run ni de gh run.
        if git_lecture(seg, ("rev-parse", "log")):
            return True
        return any(est_script(seg, s) for s in
                   SCRIPTS_DEPLOIEMENT + (".claude/skills/verifier-prod/verifier_prod.py",))
    return True


def controle_liste_blanche(agent, commande):
    if agent not in LISTES_BLANCHES:
        return
    message = ("Refusé : le Bash de {a} est limité à : {l} (ARCHITECTURE § 4 et § 6, "
               "garde-fou 7). Une seule commande, sans opérateur (; && || | > <), "
               "sans $( ) ni retour à la ligne.").format(a=agent, l=LISTES_BLANCHES[agent])
    if "\n" in commande or "$" in commande or "`" in commande:
        raise Refus(message)
    try:
        jetons = decouper(commande)
    except ValueError:
        raise Refus(message)
    segs = list(segments(jetons))
    if len(segs) != 1 or len(segs[0]) != len(jetons) or not autorise_liste_blanche(agent, segs[0]):
        raise Refus(message)


# -- R17 ------------------------------------------------------------------------------------------

def est_md_protege(jeton):
    """Le jeton désigne-t-il un fichier .md de docs/ ou de projets/ ?"""
    return bool(RE_CHEMIN_MD.search(jeton.replace("\\", "/").strip("'\"")))


def refus_r17(forme, cible=""):
    return Refus(MESSAGE_R17.format(forme=forme, cible=" sur " + cible if cible else ""))


def code_ecrit_md(code):
    """Script Python en ligne qui nomme un .md de docs/ ou projets/ et contient une écriture."""
    return bool(RE_CODE_DOSSIER.search(code) and RE_CODE_MD.search(code) and RE_CODE_ECRITURE.search(code))


def separer_heredocs(commande):
    """(commande sans les corps de heredoc, [(ligne qui ouvre le heredoc, corps)]).

    Un heredoc dont le mot de fin n'apparaît jamais n'en est pas un (par exemple « << » dans une
    chaîne) : ses lignes restent dans la commande analysée."""
    lignes = commande.split("\n")
    reste, heredocs, i = [], [], 0
    while i < len(lignes):
        ligne = lignes[i]
        reste.append(ligne)
        i += 1
        for m in RE_HEREDOC.finditer(ligne):
            fin, tabs = m.group(3), m.group(1) == "-"
            j = i
            while j < len(lignes):
                courante = lignes[j].rstrip("\r")
                if (courante.lstrip("\t") if tabs else courante).strip() == fin:
                    break
                j += 1
            if j < len(lignes):
                heredocs.append((ligne, "\n".join(lignes[i:j])))
                i = j + 1
    return "\n".join(reste), heredocs


def controle_en_place(seg, commande, liste_implicite):
    """`sed -i`, `perl -i` (en tête de segment, ou derrière `find -exec`)."""
    for k, j in enumerate(seg):
        exe = nom_exe(j.lstrip("`"))
        if exe not in EDITEURS_EN_PLACE or (k > 0 and seg[k - 1] not in LANCEURS_FIND):
            continue
        args = seg[k + 1:]
        if not any(a == "--in-place" or a.startswith("--in-place=") or re.match(r"^-[A-Za-z]*i", a)
                   for a in args):
            continue
        cibles = [a for a in args if est_md_protege(a)]
        if cibles:
            raise refus_r17(exe + " -i", cibles[0])
        # Fichiers fournis par find -exec ou par xargs : on se fie au texte de la commande.
        if (k > 0 or liste_implicite) and RE_CODE_DOSSIER.search(commande) and RE_CODE_MD.search(commande):
            raise refus_r17(exe + " -i sur des .md choisis par find ou xargs")


def controle_python(seg, reste, heredoc_python):
    """`python -c <code>` ; `python` ou `python -` qui lit un script sur un tube ou un `<`."""
    k = 1
    while k < len(seg):
        a = seg[k]
        if a == "-m":
            return                                   # module installé : pas un script en ligne
        if a in ("-X", "-W"):
            k += 2
            continue
        if a.startswith("-") and not a.startswith("--") and len(a) > 1 and a.endswith("c"):
            if k + 1 < len(seg) and code_ecrit_md(seg[k + 1]):
                raise refus_r17("script Python en ligne, python -c")
            return
        if a == "-":
            break
        if a.startswith("-"):
            k += 1
            continue
        return                                       # script enregistré : non analysé (limite R17)
    if not heredoc_python and code_ecrit_md(reste):
        raise refus_r17("script Python lu sur l'entrée standard")


def controle_r17(commande, profondeur=0):
    """Refuse toute écriture par Bash dans un .md de docs/ ou projets/ (R17), pour tout appelant."""
    if profondeur > 3:
        raise Refus("Refusé : commande imbriquée trop profondément.")
    reste, heredocs = separer_heredocs(commande)
    for ligne, corps in heredocs:
        if RE_SHELL_STDIN.search(ligne):
            controle_r17(corps, profondeur + 1)
        elif RE_PYTHON_STDIN.search(ligne) and code_ecrit_md(corps):
            raise refus_r17("script Python en ligne, python - avec heredoc")
    # Une fin de ligne sépare deux commandes, comme « ; » (la continuation « \ » les relie).
    a_decouper = re.sub(r"\\\r?\n", " ", reste).replace("\r", "").replace("\n", " ; ")
    try:
        jetons = decouper(a_decouper)
    except ValueError:
        if RE_CODE_DOSSIER.search(reste) and RE_CODE_MD.search(reste) and RE_SECOURS_ECRITURE.search(reste):
            raise refus_r17("commande illisible qui semble écrire un .md")
        return
    for k, j in enumerate(jetons[:-1]):              # > >> >| &> &>> <> vers un .md protégé
        if ">" in j and set(j) <= set("<>&|") and est_md_protege(jetons[k + 1]):
            raise refus_r17("redirection " + j, jetons[k + 1])
    heredoc_python = any(RE_PYTHON_STDIN.search(ligne) for ligne, _ in heredocs)
    for brut in segments(jetons):
        liste_implicite = any(nom_exe(j) == "xargs" for j in brut)
        seg = sans_prefixes(brut)
        if not seg:
            continue
        exe = nom_exe(seg[0].lstrip("`"))
        if exe in SHELLS or exe == "eval":
            for k, j in enumerate(seg[1:], start=1):
                if j == "-c" and k + 1 < len(seg):
                    controle_r17(seg[k + 1], profondeur + 1)
            if exe == "eval":
                controle_r17(" ".join(seg[1:]), profondeur + 1)
        if exe == "tee":
            for j in seg[1:]:
                if est_md_protege(j):
                    raise refus_r17("tee", j)
        controle_en_place(seg, a_decouper, liste_implicite)
        if exe in INTERPRETES:
            controle_python(seg, reste, heredoc_python)


def analyser(donnees, agent_force=None):
    """Retourne None si autorisé, ("deny", message) ou ("ask", message)."""
    if donnees.get("tool_name", "Bash") != "Bash":
        return None
    agent = agent_force or donnees.get("agent_type") or ""
    agent = agent.split(":")[-1].strip().lower()
    commande = (donnees.get("tool_input") or {}).get("command") or ""
    if agent:
        try:
            controles_communs(commande)
            controle_liste_blanche(agent, commande)
        except Refus as r:
            return "deny", str(r)
    # R17, pour tout appelant (l'incident DEC-007 venait de la session principale).
    try:
        controle_r17(commande)
    except Refus as r:
        return "deny", str(r)
    # Session principale : permissions de settings.json, plus la confirmation du déploiement.
    script = script_deploiement(commande)
    if script:
        return "ask", MESSAGE_DEPLOIEMENT.format(script=script)
    return None


def refuser(message):
    sys.stderr.buffer.write((message + "\n").encode("utf-8"))
    sys.stderr.flush()
    sys.exit(2)


def main():
    agent_force = None
    if "--agent" in sys.argv:
        k = sys.argv.index("--agent")
        agent_force = sys.argv[k + 1] if k + 1 < len(sys.argv) else None
    try:
        donnees = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
        if not isinstance(donnees, dict):
            raise ValueError("entrée JSON inattendue")
        decision = analyser(donnees, agent_force)
    except Exception as exc:  # fermeture par défaut
        refuser("Refusé : hook restreindre_bash en erreur ({}), commande bloquée par prudence. "
                "Signale-le à l'humain.".format(exc))
    if decision and decision[0] == "deny":
        refuser(decision[1])
    if decision and decision[0] == "ask":
        sortie = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                         "permissionDecisionReason": decision[1]}}
        sys.stdout.buffer.write(json.dumps(sortie, ensure_ascii=False).encode("utf-8"))
        sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    main()
