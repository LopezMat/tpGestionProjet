#!/usr/bin/env python3
"""Serveur local du mode « Direct » de la page « Le bureau » (DEC-018). Responsable : D.

Optionnel et local à chaque poste. Trois usages :

  python scripts/bureau_direct.py --installer      déclare le hook d'observation dans
                                                   .claude/settings.local.json (hors Git), puis
                                                   relancer Claude Code
  python scripts/bureau_direct.py [--port 8765] [--generer]
                                                   sert console/ et le flux des événements sur
                                                   http://127.0.0.1:8765/bureau.html#mode=direct
  python scripts/bureau_direct.py --desinstaller   retire ce hook de settings.local.json

Le serveur :
- écoute uniquement sur 127.0.0.1 (adresse fixée dans le code, aucune option d'hôte) ;
- n'accepte que GET (toute autre méthode : 405) ; contrôle l'en-tête Host contre le DNS rebinding
  (127.0.0.1:<port> ou localhost:<port> uniquement) ; refuse Sec-Fetch-Site: cross-site ;
- n'envoie aucun en-tête CORS ;
- sert console/ en lecture seule, sans jamais en sortir (path traversal, liens symboliques, fichiers
  cachés, types hors liste blanche refusés) ;
- diffuse direct/evenements.jsonl en SSE (/direct/flux), lu au fil de l'eau ; chaque ligne est
  revalidée par la liste blanche du hook (même code, importé) avant d'être envoyée ;
- n'écrit rien et n'exécute aucune commande.

L'installateur n'écrit que .claude/settings.local.json (avec une sauvegarde avant écriture) et ne
touche qu'aux groupes du hook journal_direct.py, de façon idempotente. Il ne modifie jamais
.claude/settings.json (partagé par Git). Il n'ajoute « async » que si la version locale de Claude
Code le prend en charge (seule commande lancée par ce script : « claude --version », sans shell).

Bibliothèque standard uniquement (--generer demande PyYAML, comme scripts/console.py).
"""
import argparse
import datetime
import importlib.util
import json
import os
import re
import shutil
import socketserver
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.dont_write_bytecode = True  # pas de __pycache__ dans scripts/ ni .claude/hooks/

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE_DEPOT = os.path.dirname(ICI)
HOOK = os.path.join(RACINE_DEPOT, ".claude", "hooks", "journal_direct.py")


def _module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


journal = _module("journal_direct", HOOK)    # liste blanche partagée avec le hook

HOTE = "127.0.0.1"                 # jamais d'autre adresse d'écoute
PORT_DEFAUT = 8765
FENETRE_RATTRAPAGE = 15 * 60       # secondes d'historique envoyées à la connexion
MAX_RATTRAPAGE = 500
INTERVALLE = 0.25                  # relevé du fichier (secondes)
PING = 15.0                        # commentaire SSE de maintien (secondes)
MAX_CLIENTS = 8
MAX_LIGNE = 4096                   # une ligne valide fait moins de 300 octets

MIME = {
    ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon",
    ".txt": "text/plain; charset=utf-8",
}
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; "
       "form-action 'none'")
ENTETES_SECURITE = (
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "no-referrer"),
    ("Cache-Control", "no-store"),
    ("X-Frame-Options", "DENY"),
    ("Cross-Origin-Resource-Policy", "same-origin"),
    ("Content-Security-Policy", CSP),
)
RE_DERNIER_ID = re.compile(r"^(\d{1,24})-(\d{1,15})$")


def sortie(texte):
    """Affichage en UTF-8, même sur une console Windows en cp1252."""
    tampon = getattr(sys.stdout, "buffer", None)
    if tampon is None:
        sys.stdout.write(texte + "\n")
    else:
        tampon.write((texte + "\n").encode("utf-8"))
    sys.stdout.flush()


# ============================================================================ lecture du journal

class Lecteur:
    """Lit direct/evenements.jsonl (et son archive) sans jamais le garder ouvert : sous Windows, un
    fichier ouvert empêcherait la rotation faite par le hook. Un « état » vaut (identité, position)."""

    def __init__(self, dossier):
        self.fichier = os.path.join(dossier, journal.NOM_FICHIER)
        self.archive = os.path.join(dossier, journal.NOM_ARCHIVE)

    @staticmethod
    def _identite(chemin):
        try:
            st = os.stat(chemin)
        except OSError:
            return None, 0
        return st.st_ino or 0, st.st_size

    @staticmethod
    def _lire(chemin, debut, ident):
        """[(id, ligne validée)] des lignes complètes à partir de `debut`, et la nouvelle position."""
        try:
            with open(chemin, "rb") as f:
                f.seek(debut)
                brut = f.read()
        except OSError:
            return [], debut
        fin = brut.rfind(b"\n")
        if fin < 0:
            return [], debut
        res, pos = [], debut
        for morceau in brut[:fin + 1].split(b"\n")[:-1]:
            pos += len(morceau) + 1
            ligne = Lecteur.analyser(morceau)
            if ligne is not None:
                res.append(("{}-{}".format(ident, pos), ligne))
        return res, pos

    @staticmethod
    def analyser(morceau):
        if not morceau or len(morceau) > MAX_LIGNE:
            return None
        try:
            return journal.valider(json.loads(morceau.decode("utf-8")))
        except (ValueError, UnicodeDecodeError):
            return None

    def rattrapage(self, maintenant=None):
        """Événements des 15 dernières minutes (500 au plus) et état de fin du fichier courant."""
        ident_a, _ = self._identite(self.archive)
        ident, _ = self._identite(self.fichier)
        lignes = []
        if ident_a is not None:
            lignes += self._lire(self.archive, 0, ident_a)[0]
        pos = 0
        if ident is not None:
            courantes, pos = self._lire(self.fichier, 0, ident)
            lignes += courantes
        limite = (maintenant or datetime.datetime.now().astimezone()) - \
            datetime.timedelta(seconds=FENETRE_RATTRAPAGE)
        recentes = []
        for id_, ligne in lignes:
            try:
                if datetime.datetime.fromisoformat(ligne["ts"]) >= limite:
                    recentes.append((id_, ligne))
            except ValueError:
                continue
        return recentes[-MAX_RATTRAPAGE:], (ident, pos)

    def reprise(self, dernier_id):
        """État à partir d'un Last-Event-ID, s'il désigne encore une position du fichier courant."""
        m = RE_DERNIER_ID.match((dernier_id or "").strip())
        if not m:
            return None
        ident, taille = self._identite(self.fichier)
        if ident is None or int(m.group(1)) != ident or int(m.group(2)) > taille:
            return None
        return ident, int(m.group(2))

    def suivre(self, etat):
        """Nouvelles lignes depuis `etat` ; rotation (changement d'identité) et troncature suivies."""
        ancien, pos = etat
        ident, taille = self._identite(self.fichier)
        res = []
        if ident is None:
            return res, (None, 0)
        if ancien is not None and ident != ancien:
            ident_a, _ = self._identite(self.archive)
            if ident_a == ancien:                       # fin de l'ancien fichier, devenu l'archive
                res += self._lire(self.archive, pos, ancien)[0]
            pos = 0
        elif ancien is None or taille < pos:
            pos = 0
        if taille > pos:
            nouvelles, pos = self._lire(self.fichier, pos, ident)
            res += nouvelles
        return res, (ident, pos)


# ============================================================================ serveur HTTP

class Gestionnaire(BaseHTTPRequestHandler):
    server_version = "bureau-direct"
    sys_version = ""
    protocol_version = "HTTP/1.0"

    # -- réponses --------------------------------------------------------------------
    def _securite(self):
        for cle, val in ENTETES_SECURITE:
            self.send_header(cle, val)

    def _repondre(self, code, corps=b"", type_="text/plain; charset=utf-8", entetes=()):
        self.send_response(code)
        self._securite()
        for cle, val in entetes:
            self.send_header(cle, val)
        self.send_header("Content-Type", type_)
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        if self.command != "HEAD" and corps:
            self.wfile.write(corps)

    def send_error(self, code, message=None, explain=None):
        """Toutes les erreurs, y compris celles de http.server (requête mal formée, méthode
        inconnue : 501 devient 405), avec un corps minimal et les en-têtes de sécurité."""
        if code == 501:
            code = 405
        try:
            self.close_connection = True
            textes = {400: "Requête invalide", 403: "Interdit", 404: "Introuvable",
                      405: "Méthode non autorisée : GET uniquement", 503: "Trop de connexions"}
            corps = (textes.get(code, "Erreur") + "\n").encode("utf-8")
            self._repondre(code, corps, entetes=(("Allow", "GET"),) if code == 405 else ())
        except OSError:
            pass

    def log_message(self, format, *args):
        if not self.server.silencieux:
            super().log_message(format, *args)

    # -- contrôles -------------------------------------------------------------------
    def _controle(self):
        hote = (self.headers.get("Host") or "").strip().lower()
        if hote not in self.server.hotes_autorises:
            self.send_error(403)
            return False
        if (self.headers.get("Sec-Fetch-Site") or "").strip().lower() == "cross-site":
            self.send_error(403)
            return False
        return True

    def _refuser_methode(self):
        self.send_error(405)

    do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = do_OPTIONS = do_TRACE = do_CONNECT = _refuser_methode

    # -- GET -------------------------------------------------------------------------
    def do_GET(self):
        if not self._controle():
            return
        chemin = urllib.parse.urlsplit(self.path).path
        if not chemin.startswith("/"):
            self.send_error(400)
            return
        if chemin == "/":
            self._repondre(302, b"", entetes=(("Location", "/bureau.html#mode=direct"),))
        elif chemin == "/direct/flux":
            self._flux()
        else:
            self._fichier(chemin)

    def _fichier(self, chemin_url):
        cible = resoudre(self.server.dossier_console, chemin_url)
        if isinstance(cible, int):
            self.send_error(cible)
            return
        try:
            with open(cible, "rb") as f:
                corps = f.read()
        except OSError:
            self.send_error(404)
            return
        self._repondre(200, corps, MIME[os.path.splitext(cible)[1].lower()])

    def _envoyer(self, id_, ligne):
        data = json.dumps(ligne, ensure_ascii=True, separators=(",", ":"))
        self.wfile.write("id: {}\nevent: evenement\ndata: {}\n\n".format(id_, data).encode("ascii"))

    def _flux(self):
        serveur = self.server
        if not serveur.prendre_client():
            self.send_error(503)
            return
        try:
            self.send_response(200)
            self._securite()
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()
            self.wfile.write(b"retry: 3000\n\n")
            lecteur = serveur.lecteur
            etat = lecteur.reprise(self.headers.get("Last-Event-ID"))
            if etat is None:
                lignes, etat = lecteur.rattrapage()
                for id_, ligne in lignes:
                    self._envoyer(id_, ligne)
            self.wfile.write(b"event: pret\ndata: {}\n\n")
            self.wfile.flush()
            dernier_ping = time.monotonic()
            while not serveur.arret.is_set():
                lignes, etat = lecteur.suivre(etat)
                for id_, ligne in lignes:
                    self._envoyer(id_, ligne)
                if lignes:
                    self.wfile.flush()
                if time.monotonic() - dernier_ping >= serveur.ping:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    dernier_ping = time.monotonic()
                serveur.arret.wait(serveur.intervalle)
        except OSError:            # client parti (BrokenPipe, ConnectionReset, ConnectionAborted…)
            pass
        finally:
            serveur.rendre_client()
            self.close_connection = True


def resoudre(dossier, chemin_url):
    """Chemin réel d'un fichier de `dossier` désigné par `chemin_url`, ou un code HTTP (403, 404).
    Décodage unique ; refus des octets nuls, des « \\ », des « : » (lecteur Windows), des segments
    « . », « .. » ou cachés ; le chemin réel (liens symboliques résolus) doit rester sous `dossier`."""
    try:
        brut = urllib.parse.unquote(chemin_url, errors="strict")
    except UnicodeDecodeError:
        return 404
    if "\x00" in brut or "\\" in brut or ":" in brut:
        return 403
    segments = [s for s in brut.split("/") if s]
    if any(s.startswith(".") for s in segments):
        return 403
    base = os.path.realpath(dossier)
    reel = os.path.realpath(os.path.join(base, *segments))
    try:
        if os.path.commonpath([reel, base]) != base:
            return 403
    except ValueError:                 # autre lecteur sous Windows
        return 403
    if os.path.isdir(reel):
        reel = os.path.realpath(os.path.join(reel, "index.html"))
        try:
            if os.path.commonpath([reel, base]) != base:
                return 403
        except ValueError:
            return 403
    if not os.path.isfile(reel) or os.path.splitext(reel)[1].lower() not in MIME:
        return 404
    return reel


class Serveur(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False        # sous Windows, SO_REUSEADDR permettrait de voler le port

    def __init__(self, racine, port=PORT_DEFAUT, silencieux=False):
        self.racine = os.path.abspath(racine)
        self.dossier_console = os.path.join(self.racine, "console")
        self.lecteur = Lecteur(os.path.join(self.racine, journal.NOM_DOSSIER))
        self.silencieux = silencieux
        self.arret = threading.Event()
        self.intervalle, self.ping = INTERVALLE, PING
        self._clients, self._verrou = 0, threading.Lock()
        super().__init__((HOTE, port), Gestionnaire)
        p = self.server_address[1]
        self.hotes_autorises = {"127.0.0.1:{}".format(p), "localhost:{}".format(p)}
        if p == 80:
            self.hotes_autorises |= {"127.0.0.1", "localhost"}

    def server_bind(self):
        # Pas de socket.getfqdn() (lent sous Windows) : on garde l'adresse locale telle quelle.
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]

    def prendre_client(self):
        with self._verrou:
            if self._clients >= MAX_CLIENTS:
                return False
            self._clients += 1
            return True

    def rendre_client(self):
        with self._verrou:
            self._clients = max(0, self._clients - 1)

    def arreter(self):
        self.arret.set()
        self.shutdown()
        self.server_close()


# ============================================================================ installation locale

FICHIER_LOCAL = os.path.join(".claude", "settings.local.json")
MARQUE = "journal_direct.py"
COMMANDE = ('command -v python >/dev/null 2>&1 && P=python || P=python3; '
            '"$P" "$CLAUDE_PROJECT_DIR/.claude/hooks/journal_direct.py" 2>/dev/null; exit 0')
# (événement, matcher) : matcher « * » pour les événements d'outils, aucun pour les autres.
EVENEMENTS_HOOK = [("SessionStart", None), ("UserPromptSubmit", None), ("PreToolUse", "*"),
                   ("PostToolUse", "*"), ("PostToolUseFailure", "*"), ("PermissionRequest", "*"),
                   ("Notification", None), ("SubagentStart", None), ("SubagentStop", None),
                   ("Stop", None), ("SessionEnd", None)]
# Plus ancienne version où la prise en charge de « async » a été vérifiée dans le schéma des hooks
# (binaire 2.1.332, 2026-11-26). Une version plus ancienne, ou inconnue : hooks sans async.
ASYNC_VERSION_MIN = (2, 1, 332)


class ErreurSettings(Exception):
    pass


def version_claude():
    """Version de Claude Code installée (tuple), ou None. Seule commande lancée par ce script."""
    exe = shutil.which("claude")
    if not exe:
        return None
    import subprocess          # importé ici seulement : le serveur n'exécute jamais rien
    try:
        r = subprocess.run([exe, "--version"], capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", r.stdout.decode("utf-8", "replace"))
    return tuple(int(x) for x in m.groups()) if m else None


def groupes_direct(avec_async):
    """{événement: groupe} du hook d'observation."""
    res = {}
    for evenement, matcher in EVENEMENTS_HOOK:
        hook = {"type": "command", "command": COMMANDE}
        if evenement == "SessionEnd":
            hook["timeout"] = 3          # synchrone : un hook async risque d'être tué à la sortie
        else:
            hook["timeout"] = 5
            if avec_async:
                hook["async"] = True
        groupe = {"hooks": [hook]}
        if matcher is not None:
            groupe = {"matcher": matcher, "hooks": [hook]}
        res[evenement] = groupe
    return res


def _est_direct(hook):
    return isinstance(hook, dict) and MARQUE in str(hook.get("command") or "")


def retirer_direct(donnees):
    """Copie de `donnees` sans aucun hook journal_direct.py (le reste est conservé tel quel)."""
    donnees = json.loads(json.dumps(donnees))
    if "hooks" not in donnees:
        return donnees
    hooks = donnees["hooks"]
    if not isinstance(hooks, dict):
        raise ErreurSettings("« hooks » n'est pas un objet JSON")
    for evenement in list(hooks):
        groupes = hooks[evenement]
        if not isinstance(groupes, list):
            raise ErreurSettings("« hooks.{} » n'est pas une liste".format(evenement))
        garde = []
        for g in groupes:
            if isinstance(g, dict) and isinstance(g.get("hooks"), list) and any(_est_direct(h) for h in g["hooks"]):
                restants = [h for h in g["hooks"] if not _est_direct(h)]
                if restants:
                    g = dict(g, hooks=restants)
                    garde.append(g)
            else:
                garde.append(g)
        if garde:
            hooks[evenement] = garde
        else:
            del hooks[evenement]
    if not hooks:
        del donnees["hooks"]
    return donnees


def ajouter_direct(donnees, avec_async):
    """Copie de `donnees` avec exactement un groupe journal_direct.py par événement. Un événement qui
    porte déjà exactement ce groupe (et aucun autre hook journal_direct) est laissé tel quel, à sa place :
    une réinstallation ne réordonne jamais les hooks personnels ajoutés entre-temps."""
    retire = retirer_direct(donnees)
    origine = json.loads(json.dumps(donnees)).get("hooks") or {}
    hooks = retire.setdefault("hooks", {})
    for evenement, groupe in groupes_direct(avec_async).items():
        actuels = origine.get(evenement) or []
        directs = [g for g in actuels if isinstance(g, dict) and isinstance(g.get("hooks"), list)
                   and any(_est_direct(h) for h in g["hooks"])]
        if directs == [groupe]:
            hooks[evenement] = actuels                      # déjà installé à l'identique : inchangé
        else:
            hooks.setdefault(evenement, []).append(groupe)
    return retire


def lire_local(chemin):
    """Contenu de settings.local.json (dict), {} s'il est absent ; ErreurSettings s'il est illisible."""
    try:
        with open(chemin, "r", encoding="utf-8-sig") as f:
            texte = f.read()
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as exc:
        raise ErreurSettings("lecture impossible ({})".format(exc))
    if not texte.strip():
        return {}
    try:
        donnees = json.loads(texte)
    except ValueError as exc:
        raise ErreurSettings("JSON invalide ({})".format(exc))
    if not isinstance(donnees, dict):
        raise ErreurSettings("le fichier ne contient pas un objet JSON")
    return donnees


def ecrire_local(chemin, donnees, existait, maintenant=None):
    """Sauvegarde (si le fichier existait), puis écriture atomique. Renvoie le chemin de la sauvegarde."""
    sauvegarde = None
    if existait:
        horo = (maintenant or datetime.datetime.now()).strftime("%Y%m%d-%H%M%S")
        sauvegarde = "{}.sauvegarde-{}".format(chemin, horo)
        n = 1
        while os.path.exists(sauvegarde):
            n += 1
            sauvegarde = "{}.sauvegarde-{}-{}".format(chemin, horo, n)
        shutil.copy2(chemin, sauvegarde)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    temp = chemin + ".tmp"
    with open(temp, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n")
    os.replace(temp, chemin)
    return sauvegarde


def modifier_local(racine, installer, avec_async=False):
    """Installe ou désinstalle le hook dans settings.local.json. Renvoie (changé, sauvegarde)."""
    chemin = os.path.join(os.path.abspath(racine), FICHIER_LOCAL)
    actuel = lire_local(chemin)
    existait = actuel is not None
    base = actuel if existait else {}
    nouveau = ajouter_direct(base, avec_async) if installer else retirer_direct(base)
    if nouveau == base and (existait or not installer):
        return False, None
    return True, ecrire_local(chemin, nouveau, existait)


def est_installe(racine):
    try:
        donnees = lire_local(os.path.join(os.path.abspath(racine), FICHIER_LOCAL)) or {}
        return donnees != retirer_direct(donnees)
    except ErreurSettings:
        return False


# ============================================================================ programme principal

def generer_console(racine):
    console = _module("console", os.path.join(ICI, "console.py"))
    return console.main(["--racine", racine])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mode Direct de « Le bureau » (DEC-018) : serveur local "
                                             "(127.0.0.1) et installation du hook d'observation.")
    ap.add_argument("--port", type=int, default=PORT_DEFAUT, help="port d'écoute sur 127.0.0.1 (défaut 8765)")
    ap.add_argument("--racine", default=RACINE_DEPOT, help="racine du dépôt (défaut : parent de scripts/)")
    ap.add_argument("--generer", action="store_true", help="régénère d'abord la console (scripts/console.py)")
    ap.add_argument("--silencieux", action="store_true", help="n'affiche pas le journal des requêtes")
    action = ap.add_mutually_exclusive_group()
    action.add_argument("--installer", action="store_true",
                        help="déclare le hook d'observation dans .claude/settings.local.json (ce poste)")
    action.add_argument("--desinstaller", action="store_true",
                        help="retire le hook d'observation de .claude/settings.local.json")
    ap.add_argument("--sans-async", action="store_true", help="avec --installer : hooks synchrones")
    a = ap.parse_args(argv)
    racine = os.path.abspath(a.racine)
    chemin_local = os.path.join(racine, FICHIER_LOCAL)

    if a.installer or a.desinstaller:
        avec_async = False
        if a.installer and not a.sans_async:
            version = version_claude()
            avec_async = version is not None and version >= ASYNC_VERSION_MIN
            sortie("Claude Code : {} → hooks {}.".format(
                ".".join(map(str, version)) if version else "version introuvable",
                "asynchrones (async)" if avec_async else "synchrones (sans async)"))
        try:
            change, sauvegarde = modifier_local(racine, a.installer, avec_async)
        except ErreurSettings as exc:
            sortie("ERREUR: {} : {}. Fichier laissé intact.".format(chemin_local, exc))
            return 1
        if sauvegarde:
            sortie("Sauvegarde : {}".format(sauvegarde))
        if a.installer:
            sortie(("Hook d'observation déclaré dans {}." if change else "Déjà installé : {} inchangé.")
                   .format(chemin_local))
            sortie("Relancez Claude Code pour qu'il le prenne en compte. Le journal s'écrit dans direct/ "
                   "(hors Git) ; ESN_DIRECT=off le suspend.")
        else:
            sortie(("Hook d'observation retiré de {}." if change else "Rien à retirer : {} inchangé.")
                   .format(chemin_local))
            sortie("Relancez Claude Code. Le dossier direct/ peut être supprimé.")
        return 0

    if a.generer:
        code = generer_console(racine)
        if code:
            return code
    if not os.path.isfile(os.path.join(racine, "console", "bureau.html")):
        sortie("ERREUR: console/bureau.html absent. Lancez d'abord : python scripts/console.py "
               "(ou ajoutez --generer).")
        return 2
    if not (0 < a.port < 65536):
        sortie("ERREUR: --port invalide : {}".format(a.port))
        return 2
    try:
        serveur = Serveur(racine, a.port, a.silencieux)
    except OSError as exc:
        sortie("ERREUR: impossible d'écouter sur {}:{} ({}).".format(HOTE, a.port, exc))
        return 2
    if not est_installe(racine):
        sortie("ATTENTION: hook d'observation non installé sur ce poste : lancez "
               "« python scripts/bureau_direct.py --installer », puis relancez Claude Code.")
    sortie("Mode Direct : http://{}:{}/bureau.html#mode=direct   (Ctrl+C pour arrêter)".format(
        HOTE, serveur.server_address[1]))
    try:
        serveur.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        serveur.arret.set()
        serveur.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
