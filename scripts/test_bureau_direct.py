#!/usr/bin/env python3
"""Tests de scripts/bureau_direct.py (serveur local et installation du mode Direct, DEC-018). Responsable : D.

Lancement : python scripts/test_bureau_direct.py   (Mac : python3 …). Bibliothèque standard uniquement.
Le serveur est lancé dans le processus de test, sur un port libre de 127.0.0.1, avec un faux console/
et un faux journal dans un dossier temporaire. L'installation est testée sur un settings.local.json
temporaire : le vrai fichier du poste n'est jamais touché.
"""
import ast
import http.client
import importlib.util
import io
import json
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
import unittest
import unittest.mock
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(ICI, "bureau_direct.py")

spec = importlib.util.spec_from_file_location("bureau_direct", SCRIPT)
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)
journal = bd.journal

SECRET = "SECRET-HORS-CONSOLE"


def ligne(evenement="outil_debut", acteur="coordinateur", outil="Read", categorie="lit", ts=None, **extra):
    d = {"v": 1, "ts": ts or bd.datetime.datetime.now().astimezone().isoformat(timespec="milliseconds"),
         "session": "0123456789ab", "acteur": acteur, "instance": "", "evenement": evenement,
         "outil": outil, "categorie": categorie, "detail": ""}
    d.update(extra)
    return d


def ajouter(chemin, *objets, brut=None):
    with open(chemin, "ab") as f:
        for o in objets:
            f.write((json.dumps(o) + "\n").encode("utf-8"))
        if brut:
            f.write(brut)


class AvecServeur(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="bureau-direct-")
        cls.racine = os.path.join(cls.tmp, "depot")
        console = os.path.join(cls.racine, "console")
        os.makedirs(os.path.join(console, "assets"))
        os.makedirs(os.path.join(console, "projets", "demo"))
        os.makedirs(os.path.join(console, ".cache"))
        os.makedirs(os.path.join(cls.racine, "direct"))
        for rel, texte in (("bureau.html", "<h1>Le bureau</h1>"), ("assets/bureau.js", "var x = 1;"),
                           ("projets/demo/index.html", "<p>demo</p>"), (".cache/x.html", "cache"),
                           ("notes.exe", "binaire"), ("style.css", "body{}")):
            with open(os.path.join(console, rel), "w", encoding="utf-8") as f:
                f.write(texte)
        with open(os.path.join(cls.racine, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write(SECRET)
        with open(os.path.join(cls.tmp, "secret.txt"), "w", encoding="utf-8") as f:
            f.write(SECRET)
        cls.journal = os.path.join(cls.racine, "direct", "evenements.jsonl")
        cls.serveur = bd.Serveur(cls.racine, 0, silencieux=True)
        cls.serveur.intervalle, cls.serveur.ping = 0.05, 0.4
        cls.port = cls.serveur.server_address[1]
        cls.fil = threading.Thread(target=cls.serveur.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        cls.fil.start()

    @classmethod
    def tearDownClass(cls):
        cls.serveur.arreter()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def requete(self, chemin, methode="GET", host=None, entetes=None):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.putrequest(methode, chemin, skip_host=True, skip_accept_encoding=True)
        if host is not False:
            c.putheader("Host", "127.0.0.1:{}".format(self.port) if host is None else host)
        for k, v in (entetes or {}).items():
            c.putheader(k, v)
        c.endheaders()
        r = c.getresponse()
        corps = r.read() if methode != "HEAD" else b""
        c.close()
        return r, corps


class TestServeur(AvecServeur):
    def test_ecoute_locale_seulement(self):
        self.assertEqual(self.serveur.server_address[0], "127.0.0.1")
        self.assertEqual(bd.HOTE, "127.0.0.1")
        with self.assertRaises(SystemExit), redirect_stdout(io.StringIO()), \
                unittest.mock.patch("sys.stderr", io.StringIO()):
            bd.main(["--hote", "0.0.0.0"])  # nosec B104 : test du refus de l'option --hote

    def test_page_servie(self):
        r, corps = self.requete("/bureau.html")
        self.assertEqual(r.status, 200)
        self.assertEqual(corps, b"<h1>Le bureau</h1>")
        self.assertTrue(r.getheader("Content-Type").startswith("text/html"))
        self.assertEqual(r.getheader("X-Content-Type-Options"), "nosniff")
        self.assertIn("frame-ancestors 'none'", r.getheader("Content-Security-Policy"))
        r, corps = self.requete("/projets/demo/")
        self.assertEqual((r.status, corps), (200, b"<p>demo</p>"))
        r, _ = self.requete("/")
        self.assertEqual((r.status, r.getheader("Location")), (302, "/bureau.html#mode=direct"))

    def test_controle_host(self):
        for host in ("evil.com:{}".format(self.port), "evil.com", "127.0.0.1:1", "127.0.0.1", "localhost",
                     "127.0.0.1:{}.evil.com".format(self.port), ""):
            r, corps = self.requete("/bureau.html", host=host)
            self.assertEqual(r.status, 403, host)
            self.assertNotIn(b"Le bureau", corps)
        r, _ = self.requete("/bureau.html", host=False)
        self.assertEqual(r.status, 403)
        for host in ("localhost:{}".format(self.port), "LOCALHOST:{}".format(self.port)):
            self.assertEqual(self.requete("/bureau.html", host=host)[0].status, 200, host)
        r, _ = self.requete("/bureau.html", entetes={"Sec-Fetch-Site": "cross-site"})
        self.assertEqual(r.status, 403)
        self.assertEqual(self.requete("/bureau.html", entetes={"Sec-Fetch-Site": "same-origin"})[0].status, 200)

    def test_methodes_refusees(self):
        for m in ("POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "PROPFIND"):
            r, _ = self.requete("/bureau.html", methode=m)
            self.assertEqual(r.status, 405, m)
            self.assertEqual(r.getheader("Allow"), "GET")

    def test_aucun_en_tete_cors(self):
        cas = [("/bureau.html", {}), ("/introuvable.html", {}), ("/bureau.html", {"Origin": "http://evil.com"}),
               ("/../CLAUDE.md", {})]
        for chemin, ent in cas:
            r, _ = self.requete(chemin, entetes=ent)
            self.assertFalse([h for h, _ in r.getheaders() if h.lower().startswith("access-control-")], chemin)
        r, _ = self.requete("/bureau.html", methode="OPTIONS", entetes={"Origin": "http://evil.com",
                                                                         "Access-Control-Request-Method": "GET"})
        self.assertFalse([h for h, _ in r.getheaders() if h.lower().startswith("access-control-")])

    def test_path_traversal(self):
        chemins = ["/../CLAUDE.md", "/..%2fCLAUDE.md", "/%2e%2e/CLAUDE.md", "/%2e%2e%2fCLAUDE.md",
                   "/assets/../../CLAUDE.md", "/..%5cCLAUDE.md", "/assets%5c..%5c..%5cCLAUDE.md",
                   "/../../secret.txt", "/%2e%2e/%2e%2e/secret.txt", "/bureau.html%00.png", "//etc/passwd",
                   "/C:/Windows/win.ini", "/c%3a/Windows/win.ini", "/.cache/x.html", "/notes.exe",
                   "/%252e%252e/CLAUDE.md", "/%ff%fe", "/assets/./bureau.js"]
        for chemin in chemins:
            r, corps = self.requete(chemin)
            self.assertIn(r.status, (400, 403, 404), chemin)
            self.assertNotIn(SECRET.encode(), corps, chemin)
            self.assertNotIn(b"cache", corps, chemin)

    def test_lien_symbolique_vers_l_exterieur(self):
        lien = os.path.join(self.racine, "console", "fuite.html")
        try:
            os.symlink(os.path.join(self.tmp, "secret.txt"), lien)
        except (OSError, NotImplementedError):
            self.skipTest("liens symboliques indisponibles sur ce poste")
        try:
            r, corps = self.requete("/fuite.html")
            self.assertEqual(r.status, 403)
            self.assertNotIn(SECRET.encode(), corps)
        finally:
            os.remove(lien)

    def test_resoudre(self):
        base = os.path.join(self.racine, "console")
        self.assertEqual(bd.resoudre(base, "/bureau.html"), os.path.realpath(os.path.join(base, "bureau.html")))
        self.assertEqual(bd.resoudre(base, "/../CLAUDE.md"), 403)
        self.assertEqual(bd.resoudre(base, "/absent.html"), 404)


class TestFluxSSE(AvecServeur):
    def setUp(self):
        if os.path.exists(self.journal):
            os.remove(self.journal)
        archive = os.path.join(self.racine, "direct", "evenements.1.jsonl")
        if os.path.exists(archive):
            os.remove(archive)

    def ouvrir(self, entetes=None):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.putrequest("GET", "/direct/flux", skip_host=True, skip_accept_encoding=True)
        c.putheader("Host", "127.0.0.1:{}".format(self.port))
        for k, v in (entetes or {}).items():
            c.putheader(k, v)
        c.endheaders()
        return c, c.getresponse()

    def lire_evenements(self, r, jusqua, delai=4.0):
        """Lit le flux jusqu'à `jusqua` (prédicat sur la liste des blocs) ; renvoie les blocs."""
        blocs, bloc, fin = [], [], time.monotonic() + delai
        while time.monotonic() < fin:
            l = r.fp.readline().decode("utf-8")
            if l == "":
                break
            l = l.rstrip("\n")
            if l == "":
                if bloc:
                    blocs.append(bloc)
                    bloc = []
                    if jusqua(blocs):
                        return blocs
                continue
            bloc.append(l)
        self.fail("flux incomplet : {}".format(blocs))

    @staticmethod
    def donnees(blocs):
        return [json.loads(b[2][6:]) for b in blocs if len(b) == 3 and b[1] == "event: evenement"]

    def test_format_et_rattrapage(self):
        vieux = (bd.datetime.datetime.now().astimezone() - bd.datetime.timedelta(minutes=30)) \
            .isoformat(timespec="milliseconds")
        ajouter(self.journal, ligne(ts=vieux, outil="Glob"), ligne(outil="Read"),
                dict(ligne(outil="Edit", categorie="tape"), cle_inconnue="FUITE"),
                brut=b"pas du json\n" + json.dumps(ligne(evenement="evil")).encode() + b"\n")
        ajouter(self.journal, ligne(evenement="fin_tour", outil="", categorie=""))
        c, r = self.ouvrir()
        try:
            self.assertEqual(r.status, 200)
            self.assertTrue(r.getheader("Content-Type").startswith("text/event-stream"))
            self.assertFalse([h for h, _ in r.getheaders() if h.lower().startswith("access-control-")])
            blocs = self.lire_evenements(r, lambda b: b[-1][0] == "event: pret")
            self.assertEqual(blocs[0], ["retry: 3000"])
            evs = [b for b in blocs if b[1:2] == ["event: evenement"]]
            for b in evs:
                self.assertRegex(b[0], r"^id: \d+-\d+$")
                self.assertTrue(b[2].startswith("data: {"))
            d = self.donnees(blocs)
            self.assertEqual([x["outil"] for x in d], ["Read", "Edit", ""])     # vieux, mal formé, invalide : écartés
            self.assertNotIn("cle_inconnue", d[1])
            # une ligne ajoutée arrive en moins de 2 s
            debut = time.monotonic()
            ajouter(self.journal, ligne(evenement="agent_debut", acteur="testeur", outil="", categorie=""))
            blocs = self.lire_evenements(r, lambda b: any("agent_debut" in "".join(x) for x in b), delai=2.0)
            self.assertLess(time.monotonic() - debut, 2.0)
            # ping de maintien
            self.lire_evenements(r, lambda b: any(x == [": ping"] for x in b), delai=2.0)
        finally:
            c.close()

    def test_fichier_absent_puis_cree(self):
        c, r = self.ouvrir()
        try:
            self.lire_evenements(r, lambda b: b[-1][0] == "event: pret")
            ajouter(self.journal, ligne(outil="Bash", categorie="terminal"))
            blocs = self.lire_evenements(r, lambda b: bool(self.donnees(b)))
            self.assertEqual(self.donnees(blocs)[0]["outil"], "Bash")
        finally:
            c.close()

    def test_rotation_suivie(self):
        ajouter(self.journal, ligne(outil="Read"))
        c, r = self.ouvrir()
        try:
            self.lire_evenements(r, lambda b: b[-1][0] == "event: pret")
            ajouter(self.journal, ligne(outil="Grep"))
            os.replace(self.journal, os.path.join(self.racine, "direct", "evenements.1.jsonl"))
            ajouter(self.journal, ligne(outil="Write", categorie="tape"))
            blocs = self.lire_evenements(r, lambda b: "Write" in [x["outil"] for x in self.donnees(b)])
            self.assertEqual([x["outil"] for x in self.donnees(blocs)], ["Grep", "Write"])
        finally:
            c.close()

    def test_reprise_last_event_id(self):
        ajouter(self.journal, ligne(outil="Read"), ligne(outil="Grep"))
        c, r = self.ouvrir()
        blocs = self.lire_evenements(r, lambda b: b[-1][0] == "event: pret")
        c.close()
        dernier = [b for b in blocs if b[1:2] == ["event: evenement"]][-1][0][4:]
        ajouter(self.journal, ligne(outil="Glob"))
        c, r = self.ouvrir({"Last-Event-ID": dernier})
        try:
            blocs = self.lire_evenements(r, lambda b: bool(self.donnees(b)))
            self.assertEqual([x["outil"] for x in self.donnees(blocs)], ["Glob"])
        finally:
            c.close()

    def test_flux_refuse_sans_bon_host(self):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.putrequest("GET", "/direct/flux", skip_host=True)
        c.putheader("Host", "attaquant.example:{}".format(self.port))
        c.endheaders()
        r = c.getresponse()
        self.assertEqual(r.status, 403)
        c.close()


class TestAucuneExecution(unittest.TestCase):
    def test_serveur_n_execute_rien(self):
        with open(SCRIPT, encoding="utf-8") as f:
            source = f.read()
        arbre = ast.parse(source)
        for interdit in ("os.system", "os.popen", "os.exec", "os.spawn", "eval(", "exec(", "shell=True"):
            self.assertNotIn(interdit, source)
        # subprocess n'apparaît que dans version_claude() (installation : « claude --version »)
        fonctions = [n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef) and n.name == "version_claude"]
        self.assertEqual(len(fonctions), 1)
        dans_fonction = {id(n) for n in ast.walk(fonctions[0])}
        for n in ast.walk(arbre):
            if isinstance(n, ast.Name) and n.id == "subprocess" or \
                    isinstance(n, ast.alias) and n.name == "subprocess":
                self.assertIn(id(n), dans_fonction, "subprocess hors de version_claude()")


class TestInstallation(unittest.TestCase):
    def setUp(self):
        self.racine = tempfile.mkdtemp(prefix="direct-installation-")
        self.chemin = os.path.join(self.racine, ".claude", "settings.local.json")
        self.partage = os.path.join(self.racine, ".claude", "settings.json")
        os.makedirs(os.path.dirname(self.chemin))
        with open(self.partage, "w", encoding="utf-8") as f:
            f.write('{"hooks": {}}\n')

    def tearDown(self):
        shutil.rmtree(self.racine, ignore_errors=True)

    def lire(self):
        with open(self.chemin, encoding="utf-8") as f:
            return json.load(f)

    def octets(self):
        with open(self.chemin, "rb") as f:
            return f.read()

    def sauvegardes(self):
        return [n for n in os.listdir(os.path.dirname(self.chemin)) if ".sauvegarde-" in n]

    def test_ajout_sur_fichier_absent(self):
        change, sauvegarde = bd.modifier_local(self.racine, True, avec_async=True)
        self.assertTrue(change)
        self.assertIsNone(sauvegarde)                         # rien à sauvegarder
        hooks = self.lire()["hooks"]
        self.assertEqual(set(hooks), {e for e, _ in bd.EVENEMENTS_HOOK})
        for evenement, groupes in hooks.items():
            self.assertEqual(len(groupes), 1)
            h = groupes[0]["hooks"][0]
            self.assertIn("journal_direct.py", h["command"])
            self.assertTrue(h["command"].rstrip().endswith("exit 0"))
            if evenement == "SessionEnd":
                self.assertNotIn("async", h)
            else:
                self.assertIs(h["async"], True)
        self.assertEqual(hooks["PreToolUse"][0]["matcher"], "*")
        self.assertNotIn("matcher", hooks["Stop"][0])
        with open(self.partage, encoding="utf-8") as f:
            self.assertEqual(f.read(), '{"hooks": {}}\n')      # settings.json jamais touché

    def test_sans_async(self):
        bd.modifier_local(self.racine, True, avec_async=False)
        self.assertNotIn('"async"', json.dumps(self.lire()))

    def test_idempotence(self):
        bd.modifier_local(self.racine, True, avec_async=True)
        avant = self.octets()
        change, sauvegarde = bd.modifier_local(self.racine, True, avec_async=True)
        self.assertEqual((change, sauvegarde), (False, None))
        self.assertEqual(self.octets(), avant)
        self.assertEqual(self.sauvegardes(), [])
        # passage async -> sans async : les groupes sont remplacés, jamais dupliqués
        bd.modifier_local(self.racine, True, avec_async=False)
        self.assertEqual(len(self.lire()["hooks"]["PreToolUse"]), 1)
        bd.modifier_local(self.racine, False)
        self.assertEqual(bd.modifier_local(self.racine, False), (False, None))

    def test_reinstallation_ne_reordonne_pas(self):
        """Un hook personnel ajouté après l'installation reste à sa place ; réinstaller ne réécrit rien."""
        bd.modifier_local(self.racine, True, avec_async=True)
        d = self.lire()
        d["hooks"]["Stop"].append({"hooks": [{"type": "command", "command": "echo perso"}]})
        with open(self.chemin, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        avant = self.octets()
        self.assertEqual(bd.modifier_local(self.racine, True, avec_async=True), (False, None))
        self.assertEqual(self.octets(), avant)
        self.assertEqual(self.sauvegardes(), [])

    def test_contenu_existant_conserve(self):
        existant = {
            "permissions": {"allow": ["Bash(npm test)"]},
            "env": {"X": "1"},
            "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo perso"}]}],
                      "Stop": [{"hooks": [{"type": "command", "command": "notify-send fini"}]}]},
            "model": "opus",
        }
        with open(self.chemin, "w", encoding="utf-8") as f:
            json.dump(existant, f)
        change, sauvegarde = bd.modifier_local(self.racine, True, avec_async=True)
        self.assertTrue(change)
        self.assertTrue(os.path.isfile(sauvegarde))
        with open(sauvegarde, encoding="utf-8") as f:
            self.assertEqual(json.load(f), existant)
        d = self.lire()
        self.assertEqual(d["permissions"], existant["permissions"])
        self.assertEqual(d["env"], existant["env"])
        self.assertEqual(d["model"], "opus")
        self.assertEqual(d["hooks"]["PreToolUse"][0], existant["hooks"]["PreToolUse"][0])
        self.assertEqual(d["hooks"]["Stop"][0], existant["hooks"]["Stop"][0])
        self.assertEqual(len(d["hooks"]["PreToolUse"]), 2)
        # retrait : retour exact au contenu d'origine
        change, sauvegarde2 = bd.modifier_local(self.racine, False)
        self.assertTrue(change)
        self.assertTrue(os.path.isfile(sauvegarde2))
        self.assertEqual(self.lire(), existant)

    def test_json_invalide_refuse_sans_ecraser(self):
        for contenu in (b'{"hooks": ', b"[1, 2]", b'{"hooks": []}', b'{"hooks": {"Stop": {}}}', b'{"hooks": null}'):
            with open(self.chemin, "wb") as f:
                f.write(contenu)
            with self.assertRaises(bd.ErreurSettings):
                bd.modifier_local(self.racine, True, avec_async=True)
            self.assertEqual(self.octets(), contenu)
            with self.assertRaises(bd.ErreurSettings):
                bd.modifier_local(self.racine, False)
            self.assertEqual(self.octets(), contenu)
        self.assertEqual(self.sauvegardes(), [])

    def test_ligne_de_commande(self):
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            self.assertEqual(bd.main(["--installer", "--sans-async", "--racine", self.racine]), 0)
        self.assertIn("Relancez Claude Code", sortie.getvalue())
        self.assertTrue(bd.est_installe(self.racine))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(bd.main(["--desinstaller", "--racine", self.racine]), 0)
        self.assertFalse(bd.est_installe(self.racine))
        with open(self.chemin, "w", encoding="utf-8") as f:
            f.write("{ invalide")
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            self.assertEqual(bd.main(["--installer", "--sans-async", "--racine", self.racine]), 1)
        self.assertIn("Fichier laissé intact", sortie.getvalue())
        with open(self.chemin, encoding="utf-8") as f:
            self.assertEqual(f.read(), "{ invalide")

    def test_version_minimale_async(self):
        self.assertEqual(bd.ASYNC_VERSION_MIN, (2, 1, 332))
        self.assertTrue((2, 1, 332) >= bd.ASYNC_VERSION_MIN)
        self.assertFalse((2, 1, 285) >= bd.ASYNC_VERSION_MIN)


class TestLancementSansConsole(unittest.TestCase):
    def test_console_absente(self):
        racine = tempfile.mkdtemp(prefix="direct-vide-")
        try:
            sortie = io.StringIO()
            with redirect_stdout(sortie):
                self.assertEqual(bd.main(["--racine", racine, "--port", "0"]), 2)
            self.assertIn("console/bureau.html absent", sortie.getvalue())
        finally:
            shutil.rmtree(racine, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=1)
