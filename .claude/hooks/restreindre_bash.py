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
  stdout), en doublon des règles `ask` de settings.json (S3-R3, DEC-003).

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
