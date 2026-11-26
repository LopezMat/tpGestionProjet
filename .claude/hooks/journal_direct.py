#!/usr/bin/env python3
"""Hook d'observation du mode « Direct » de la page « Le bureau » (DEC-018). Responsable : D.

Optionnel et local à chaque poste : il est déclaré dans `.claude/settings.local.json` (hors Git) par
`python scripts/bureau_direct.py --installer`, jamais dans `.claude/settings.json` (partagé).

Pour chaque événement de Claude Code retenu, il ajoute UNE ligne JSON à `direct/evenements.jsonl`
(hors Git) : heure, session hachée, acteur (coordinateur ou nom de l'agent), type d'événement, nom de
l'outil (liste blanche) et catégorie. La ligne est CONSTRUITE à partir de listes blanches, jamais
copiée depuis l'entrée : ni texte des messages, ni chemin ou contenu de fichier, ni commande, ni
sortie d'outil, ni dossier de travail.

Politique inverse des hooks de sécurité (proteger_valide.py, restreindre_bash.py, qui ferment par
défaut) : un hook d'observation ne doit JAMAIS gêner le travail. Il rend toujours la main avec le
code 0, n'écrit rien sur stdout (aucune décision), avale toute erreur et abandonne l'événement si le
verrou n'est pas obtenu en 200 ms. Il ne lit ni ne modifie les autres hooks.

Désactivation ponctuelle : variable d'environnement ESN_DIRECT=off.
Bibliothèque standard uniquement.
"""
import datetime
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import time

VERSION = 1
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))          # .claude/hooks/ -> racine du dépôt
NOM_DOSSIER = "direct"
NOM_FICHIER = "evenements.jsonl"
NOM_ARCHIVE = "evenements.1.jsonl"
MAX_OCTETS = 1024 * 1024                                  # rotation au-delà de 1 Mio
ATTENTE_VERROU = 0.2                                      # secondes

# Événement Claude Code -> type d'événement écrit.
EVENEMENTS = {
    "SessionStart": "session_debut",
    "UserPromptSubmit": "demande",
    "PreToolUse": "outil_debut",
    "PostToolUse": "outil_fin",
    "PostToolUseFailure": "outil_fin",
    "PermissionRequest": "autorisation",
    "Notification": "attente",
    "SubagentStart": "agent_debut",
    "SubagentStop": "agent_fin",
    "Stop": "fin_tour",
    "SessionEnd": "session_fin",
}
TYPES = frozenset(EVENEMENTS.values())
# Événements qui portent un nom d'outil.
AVEC_OUTIL = {"PreToolUse", "PostToolUse", "PostToolUseFailure", "PermissionRequest"}

# Outils connus -> catégorie. Tout autre nom devient « autre » (outil MCP : « mcp »).
OUTILS = {
    "Read": "lit", "Grep": "lit", "Glob": "lit", "NotebookRead": "lit", "LS": "lit",
    "Edit": "tape", "Write": "tape", "MultiEdit": "tape", "NotebookEdit": "tape",
    "Bash": "terminal", "PowerShell": "terminal", "BashOutput": "terminal", "KillShell": "terminal",
    "Agent": "delegue", "Task": "delegue",
    "WebSearch": "web", "WebFetch": "web",
    "TodoWrite": "autre", "Skill": "autre", "ToolSearch": "autre", "AskUserQuestion": "autre",
    "EnterPlanMode": "autre", "ExitPlanMode": "autre", "SendMessage": "autre", "Monitor": "autre",
    "TaskStop": "autre", "TaskOutput": "autre",
}
NOMS_OUTILS = frozenset(OUTILS) | {"mcp", "autre", ""}
CATEGORIES = frozenset(OUTILS.values()) | {"autre", ""}

SOURCES_SESSION = {"startup", "resume", "clear", "compact", "fork"}
NOTIFICATIONS = {"permission_prompt", "idle_prompt", "elicitation_dialog"}   # auth_success : ignoré

RE_AGENT = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")
RE_ACTEUR = re.compile(r"^(?:coordinateur|agent-inconnu|[a-z0-9][a-z0-9-]{0,39})$")
RE_TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$")
RE_SESSION = re.compile(r"^[0-9a-f]{12}$")
RE_INSTANCE = re.compile(r"^(?:[0-9a-f]{8})?$")
RE_DETAIL = re.compile(r"^[a-z_]{0,32}$")
CLES = ("v", "ts", "session", "acteur", "instance", "evenement", "outil", "categorie", "detail")


# --------------------------------------------------------------------------- liste blanche
def outil_et_categorie(nom):
    """Nom d'outil publiable et sa catégorie (jamais le nom brut d'un outil inconnu)."""
    nom = nom if isinstance(nom, str) else ""
    if nom in OUTILS:
        return nom, OUTILS[nom]
    if nom.startswith("mcp__"):
        return "mcp", "autre"
    return "autre", "autre"


def acteur(donnees):
    """« coordinateur » pour la session principale, sinon le nom de l'agent (filtré)."""
    if not donnees.get("agent_id"):
        return "coordinateur"
    nom = donnees.get("agent_type")
    nom = nom.strip().lower() if isinstance(nom, str) else ""
    return nom if RE_AGENT.match(nom) and nom != "coordinateur" else "agent-inconnu"


def valider(ligne):
    """Revalide une ligne (dict) : renvoie un NOUVEAU dict limité aux clés connues, ou None.
    Utilisé par le hook avant écriture et par scripts/bureau_direct.py avant envoi (même code)."""
    if not isinstance(ligne, dict):
        return None
    try:
        sortie = {
            "v": ligne.get("v"), "ts": ligne.get("ts"), "session": ligne.get("session"),
            "acteur": ligne.get("acteur"), "instance": ligne.get("instance", ""),
            "evenement": ligne.get("evenement"), "outil": ligne.get("outil", ""),
            "categorie": ligne.get("categorie", ""), "detail": ligne.get("detail", ""),
        }
        if sortie["v"] != VERSION or isinstance(sortie["v"], bool):
            return None
        for cle in CLES[1:]:
            if not isinstance(sortie[cle], str):
                return None
        if not (RE_TS.match(sortie["ts"]) and RE_SESSION.match(sortie["session"])
                and RE_ACTEUR.match(sortie["acteur"]) and RE_INSTANCE.match(sortie["instance"])
                and sortie["evenement"] in TYPES and sortie["outil"] in NOMS_OUTILS
                and sortie["categorie"] in CATEGORIES and RE_DETAIL.match(sortie["detail"])):
            return None
        return sortie
    except Exception:
        return None


def hacher(sel, valeur, n):
    return hmac.new(sel, str(valeur).encode("utf-8", "replace"), hashlib.sha256).hexdigest()[:n]


def construire(donnees, sel, maintenant=None):
    """Ligne (dict) pour une entrée de hook, ou None si l'événement n'est pas retenu."""
    if not isinstance(donnees, dict):
        return None
    nom = donnees.get("hook_event_name")
    if nom not in EVENEMENTS:
        return None
    detail, outil, categorie = "", "", ""
    if nom in AVEC_OUTIL:
        outil, categorie = outil_et_categorie(donnees.get("tool_name"))
        if nom == "PostToolUseFailure":
            detail = "echec"
    elif nom == "SessionStart":
        source = donnees.get("source")
        detail = source if source in SOURCES_SESSION else ""
    elif nom == "Notification":
        type_ = donnees.get("notification_type")
        if type_ not in NOTIFICATIONS:
            return None
        detail = type_
    elif nom == "SessionEnd":
        raison = donnees.get("reason")
        detail = raison if isinstance(raison, str) and RE_DETAIL.match(raison) else "autre"
    session = donnees.get("session_id")
    agent_id = donnees.get("agent_id")
    moment = maintenant or datetime.datetime.now().astimezone()
    ligne = {
        "v": VERSION,
        "ts": moment.isoformat(timespec="milliseconds"),
        "session": hacher(sel, session if isinstance(session, str) and session else "?", 12),
        "acteur": acteur(donnees),
        "instance": hacher(sel, agent_id, 8) if isinstance(agent_id, str) and agent_id else "",
        "evenement": EVENEMENTS[nom],
        "outil": outil,
        "categorie": categorie,
        "detail": detail,
    }
    return valider(ligne)


# --------------------------------------------------------------------------- écriture
class Verrou:
    """Verrou exclusif inter-processus sur direct/.verrou (msvcrt sous Windows, fcntl ailleurs)."""

    def __init__(self, chemin, attente):
        self.chemin, self.attente, self.f = chemin, attente, None

    def __enter__(self):
        self.f = open(self.chemin, "a+b")
        fin = time.monotonic() + self.attente
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    self.f.seek(0)
                    msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.monotonic() >= fin:
                    self.f.close()
                    self.f = None
                    raise TimeoutError("verrou non obtenu")
                time.sleep(0.01)

    def __exit__(self, *exc):
        if self.f is None:
            return False
        try:
            if os.name == "nt":
                import msvcrt
                self.f.seek(0)
                msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.f.fileno(), fcntl.LOCK_UN)
        finally:
            self.f.close()
        return False


def lire_sel(dossier):
    """Sel local (direct/.sel), créé au premier passage. Appelé sous le verrou."""
    chemin = os.path.join(dossier, ".sel")
    try:
        with open(chemin, "rb") as f:
            sel = f.read().strip()
        if len(sel) >= 32:
            return sel
    except FileNotFoundError:
        pass
    sel = secrets.token_hex(32).encode("ascii")
    with open(chemin, "wb") as f:
        f.write(sel)
    return sel


def max_octets():
    try:
        return max(256, int(os.environ.get("ESN_DIRECT_MAX_OCTETS", MAX_OCTETS)))
    except ValueError:
        return MAX_OCTETS


def journaliser(donnees, racine=RACINE):
    """Écrit la ligne de l'événement (rotation comprise). Lève une exception en cas de problème :
    c'est main() qui garantit le code 0."""
    dossier = os.path.join(racine, NOM_DOSSIER)
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)      # échoue si un fichier occupe la place : abandon
    with Verrou(os.path.join(dossier, ".verrou"), ATTENTE_VERROU):
        sel = lire_sel(dossier)
        ligne = construire(donnees, sel)
        if ligne is None:
            return None
        fichier = os.path.join(dossier, NOM_FICHIER)
        try:
            if os.path.getsize(fichier) >= max_octets():
                os.replace(fichier, os.path.join(dossier, NOM_ARCHIVE))
        except OSError:          # absent, ou ouvert par un lecteur sous Windows : rotation au prochain passage
            pass
        texte = json.dumps(ligne, ensure_ascii=True, separators=(",", ":")) + "\n"
        with open(fichier, "ab") as f:
            f.write(texte.encode("ascii"))
        return ligne


def main():
    try:
        if os.environ.get("ESN_DIRECT", "").strip().lower() in ("off", "0", "non", "false"):
            return
        brut = sys.stdin.buffer.read(16 * 1024 * 1024)
        donnees = json.loads(brut.decode("utf-8-sig", "replace"))
        journaliser(donnees)
    except BaseException:       # jamais d'erreur visible, jamais de blocage
        pass


if __name__ == "__main__":
    try:
        main()
    finally:
        os._exit(0)
