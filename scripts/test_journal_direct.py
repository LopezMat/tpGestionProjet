#!/usr/bin/env python3
"""Tests du hook d'observation .claude/hooks/journal_direct.py (mode Direct, DEC-018). Responsable : D.

Lancement : python scripts/test_journal_direct.py   (Mac : python3 …). Bibliothèque standard uniquement.
Le hook déduit la racine de son propre emplacement : chaque test le copie dans un faux dépôt temporaire
(<tmp>/.claude/hooks/) et le lance comme Claude Code (JSON sur stdin), sans jamais écrire dans le vrai
dépôt. Vérifie : code de sortie 0 dans tous les cas, stdout vide, aucun contenu interdit écrit,
correspondance des événements, rotation, dossier ou fichier absent, écritures concurrentes, et que
.claude/settings.json (partagé) ne déclare pas ce hook.
"""
import concurrent.futures
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
HOOK = os.path.join(RACINE, ".claude", "hooks", "journal_direct.py")
SETTINGS = os.path.join(RACINE, ".claude", "settings.json")

spec = importlib.util.spec_from_file_location("journal_direct", HOOK)
journal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journal)

MARQUEUR = "ZZSECRETZZ"
CHAMPS_INTERDITS = {
    "prompt": MARQUEUR + " texte du message",
    "message": MARQUEUR + " Claude needs your permission",
    "title": MARQUEUR,
    "cwd": "C:/Users/" + MARQUEUR + "/projet",
    "transcript_path": "/home/" + MARQUEUR + "/t.jsonl",
    "agent_transcript_path": "/home/" + MARQUEUR + "/a.jsonl",
    "last_assistant_message": MARQUEUR + " réponse",
    "tool_input": {"file_path": "docs/" + MARQUEUR + ".md", "command": "echo " + MARQUEUR,
                   "content": MARQUEUR, "old_string": MARQUEUR, "pattern": MARQUEUR},
    "tool_response": {"stdout": MARQUEUR, "content": MARQUEUR},
    "session_id": "session-" + MARQUEUR,
    "prompt_id": MARQUEUR,
    "permission_mode": MARQUEUR,
    "permission_suggestions": [MARQUEUR],
    "error": MARQUEUR,
}


def entree(evenement, **champs):
    d = {"hook_event_name": evenement, "session_id": "s-1", "transcript_path": "/t", "cwd": "/c"}
    d.update(champs)
    return d


class FauxDepot:
    """Dépôt temporaire avec une copie du hook."""

    def __init__(self):
        self.racine = tempfile.mkdtemp(prefix="direct-")
        os.makedirs(os.path.join(self.racine, ".claude", "hooks"))
        self.hook = os.path.join(self.racine, ".claude", "hooks", "journal_direct.py")
        shutil.copy(HOOK, self.hook)
        self.dossier = os.path.join(self.racine, "direct")
        self.fichier = os.path.join(self.dossier, "evenements.jsonl")

    def lancer(self, donnees, env=None, brut=None):
        e = dict(os.environ)
        e.pop("ESN_DIRECT", None)
        e.update(env or {})
        stdin = brut if brut is not None else json.dumps(donnees).encode("utf-8")
        debut = time.monotonic()
        r = subprocess.run([sys.executable, self.hook], input=stdin, capture_output=True, env=e, timeout=30)
        return r, time.monotonic() - debut

    def lignes(self, chemin=None):
        try:
            with open(chemin or self.fichier, encoding="utf-8") as f:
                return [json.loads(l) for l in f if l.strip()]
        except FileNotFoundError:
            return []

    def tout_le_contenu(self):
        texte = ""
        for base, _, fichiers in os.walk(self.dossier):
            for n in fichiers:
                with open(os.path.join(base, n), "rb") as f:
                    texte += f.read().decode("utf-8", "replace")
        return texte

    def nettoyer(self):
        shutil.rmtree(self.racine, ignore_errors=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.depot = FauxDepot()

    def tearDown(self):
        self.depot.nettoyer()

    def lancer_ok(self, donnees=None, **kw):
        r, duree = self.depot.lancer(donnees, **kw)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, b"", "le hook ne doit jamais émettre de décision")
        return duree


class TestToujoursZero(Base):
    def test_entrees_invalides(self):
        for brut in (b"", b"{", b"[1, 2]", b"null", b"\xff\xfe\x00garbage", b'"chaine"', b"{}",
                     b'{"hook_event_name": 42}'):
            r, _ = self.depot.lancer(None, brut=brut)
            self.assertEqual(r.returncode, 0, brut)
            self.assertEqual(r.stdout, b"")
            self.assertEqual(r.stderr, b"")
        self.assertEqual(self.depot.lignes(), [])

    def test_entree_enorme(self):
        donnees = entree("UserPromptSubmit", prompt="x" * (6 * 1024 * 1024))
        self.lancer_ok(donnees)
        self.assertEqual(len(self.depot.lignes()), 1)

    def test_fichier_a_la_place_du_dossier(self):
        with open(os.path.join(self.depot.racine, "direct"), "w") as f:
            f.write("occupé")
        self.lancer_ok(entree("Stop"))
        self.assertTrue(os.path.isfile(os.path.join(self.depot.racine, "direct")))

    def test_journal_inscriptible(self):
        os.makedirs(self.depot.fichier)          # un dossier à la place du fichier : écriture impossible
        self.lancer_ok(entree("Stop"))

    def test_desactive(self):
        self.lancer_ok(entree("Stop"), env={"ESN_DIRECT": "off"})
        self.assertFalse(os.path.exists(self.depot.dossier))

    def test_dossier_absent_cree(self):
        self.assertFalse(os.path.exists(self.depot.dossier))
        self.lancer_ok(entree("SessionStart", source="startup"))
        self.assertEqual(len(self.depot.lignes()), 1)

    def test_rapide(self):
        self.lancer_ok(entree("Stop"))           # premier passage : création du dossier et du sel
        duree = self.lancer_ok(entree("PreToolUse", tool_name="Read", tool_input={}, tool_use_id="t"))
        self.assertLess(duree, 2.0)


class TestContenuInterdit(Base):
    def test_aucun_contenu_interdit(self):
        evenements = ["SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "PostToolUseFailure",
                      "PermissionRequest", "Notification", "SubagentStart", "SubagentStop", "Stop", "SessionEnd"]
        for ev in evenements:
            for agent in (None, "dev-backend"):
                d = entree(ev, **CHAMPS_INTERDITS)
                d.update({"tool_name": MARQUEUR, "source": MARQUEUR, "reason": MARQUEUR,
                          "notification_type": "permission_prompt"})
                if agent:
                    d.update({"agent_id": "agent-" + MARQUEUR, "agent_type": agent})
                self.lancer_ok(d)
        lignes = self.depot.lignes()
        self.assertEqual(len(lignes), 2 * len(evenements))
        contenu = self.depot.tout_le_contenu()
        self.assertNotIn(MARQUEUR.lower(), contenu.lower())
        for ligne in lignes:
            self.assertEqual(set(ligne), set(journal.CLES))
            self.assertEqual(journal.valider(ligne), ligne)
            self.assertLess(len(json.dumps(ligne)), 300)

    def test_nom_d_outil_mcp_et_inconnu(self):
        self.lancer_ok(entree("PreToolUse", tool_name="mcp__claude_ai_Notion__notion-fetch"))
        self.lancer_ok(entree("PreToolUse", tool_name="OutilInconnu"))
        l1, l2 = self.depot.lignes()
        self.assertEqual((l1["outil"], l1["categorie"]), ("mcp", "autre"))
        self.assertEqual((l2["outil"], l2["categorie"]), ("autre", "autre"))
        self.assertNotIn("notion", self.depot.tout_le_contenu().lower())

    def test_agent_piege(self):
        for nom in ("../../x</script>", "a" * 60, "", 42, "coordinateur"):
            self.lancer_ok(entree("SubagentStart", agent_id="x1", agent_type=nom))
        self.assertEqual({l["acteur"] for l in self.depot.lignes()}, {"agent-inconnu"})


class TestCorrespondance(unittest.TestCase):
    SEL = b"0" * 64

    def c(self, donnees):
        return journal.construire(donnees, self.SEL)

    def test_table(self):
        cas = [
            (entree("SessionStart", source="resume"), ("coordinateur", "session_debut", "", "", "resume")),
            (entree("SessionStart", source="bizarre"), ("coordinateur", "session_debut", "", "", "")),
            (entree("UserPromptSubmit", prompt="x"), ("coordinateur", "demande", "", "", "")),
            (entree("PreToolUse", tool_name="Read"), ("coordinateur", "outil_debut", "Read", "lit", "")),
            (entree("PreToolUse", tool_name="Grep"), ("coordinateur", "outil_debut", "Grep", "lit", "")),
            (entree("PreToolUse", tool_name="Glob"), ("coordinateur", "outil_debut", "Glob", "lit", "")),
            (entree("PreToolUse", tool_name="Edit"), ("coordinateur", "outil_debut", "Edit", "tape", "")),
            (entree("PreToolUse", tool_name="Write"), ("coordinateur", "outil_debut", "Write", "tape", "")),
            (entree("PreToolUse", tool_name="Bash"), ("coordinateur", "outil_debut", "Bash", "terminal", "")),
            (entree("PreToolUse", tool_name="Agent"), ("coordinateur", "outil_debut", "Agent", "delegue", "")),
            (entree("PreToolUse", tool_name="WebFetch"), ("coordinateur", "outil_debut", "WebFetch", "web", "")),
            (entree("PostToolUse", tool_name="Edit"), ("coordinateur", "outil_fin", "Edit", "tape", "")),
            (entree("PostToolUseFailure", tool_name="Bash"), ("coordinateur", "outil_fin", "Bash", "terminal",
                                                               "echec")),
            (entree("PermissionRequest", tool_name="Bash"), ("coordinateur", "autorisation", "Bash", "terminal", "")),
            (entree("Notification", notification_type="permission_prompt"),
             ("coordinateur", "attente", "", "", "permission_prompt")),
            (entree("Notification", notification_type="idle_prompt"), ("coordinateur", "attente", "", "", "idle_prompt")),
            (entree("SubagentStart", agent_id="a1", agent_type="testeur"), ("testeur", "agent_debut", "", "", "")),
            (entree("SubagentStop", agent_id="a1", agent_type="testeur"), ("testeur", "agent_fin", "", "", "")),
            (entree("PreToolUse", tool_name="Read", agent_id="a1", agent_type="Explore"),
             ("explore", "outil_debut", "Read", "lit", "")),
            (entree("Stop"), ("coordinateur", "fin_tour", "", "", "")),
            (entree("SessionEnd", reason="prompt_input_exit"), ("coordinateur", "session_fin", "", "", "prompt_input_exit")),
            (entree("SessionEnd", reason="Bizarre Raison!"), ("coordinateur", "session_fin", "", "", "autre")),
        ]
        for donnees, attendu in cas:
            l = self.c(donnees)
            self.assertIsNotNone(l, donnees)
            self.assertEqual((l["acteur"], l["evenement"], l["outil"], l["categorie"], l["detail"]), attendu, donnees)

    def test_ignores(self):
        for d in (entree("Notification", notification_type="auth_success"), entree("Notification"),
                  entree("PreCompact"), entree("Inconnu"), {"session_id": "s"}, [], None):
            self.assertIsNone(self.c(d), d)

    def test_instance(self):
        self.assertEqual(self.c(entree("Stop"))["instance"], "")
        l = self.c(entree("SubagentStart", agent_id="a1", agent_type="testeur"))
        self.assertRegex(l["instance"], r"^[0-9a-f]{8}$")

    def test_hachage(self):
        a = self.c(entree("Stop", session_id="abc"))["session"]
        self.assertEqual(a, self.c(entree("UserPromptSubmit", session_id="abc"))["session"])
        self.assertNotEqual(a, self.c(entree("Stop", session_id="abd"))["session"])
        self.assertNotEqual(a, journal.construire(entree("Stop", session_id="abc"), b"1" * 64)["session"])
        self.assertRegex(a, r"^[0-9a-f]{12}$")

    def test_valider(self):
        bonne = self.c(entree("Stop"))
        self.assertEqual(journal.valider(dict(bonne, extra="x")), bonne)       # clé inconnue retirée
        for cle, val in (("v", 2), ("v", True), ("evenement", "autre"), ("acteur", "Un Nom"), ("outil", "Rm"),
                         ("ts", "hier"), ("session", "xyz"), ("detail", "<b>"), ("categorie", 3)):
            self.assertIsNone(journal.valider(dict(bonne, **{cle: val})), cle)
        self.assertIsNone(journal.valider("chaine"))


class TestFichier(Base):
    def test_rotation(self):
        for _ in range(8):
            self.lancer_ok(entree("PreToolUse", tool_name="Read"), env={"ESN_DIRECT_MAX_OCTETS": "500"})
        archive = os.path.join(self.depot.dossier, "evenements.1.jsonl")
        self.assertTrue(os.path.isfile(archive))
        self.assertLess(os.path.getsize(self.depot.fichier), 800)
        self.assertLess(os.path.getsize(archive), 800)
        total = len(self.depot.lignes()) + len(self.depot.lignes(archive))
        self.assertGreaterEqual(total, 4)
        self.assertFalse(os.path.exists(os.path.join(self.depot.dossier, "evenements.2.jsonl")))

    def test_ecritures_concurrentes(self):
        def un(i):
            return self.depot.lancer(entree("PreToolUse", tool_name="Read", session_id="s{}".format(i)))[0].returncode
        self.lancer_ok(entree("Stop"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            codes = list(ex.map(un, range(10)))
        self.assertEqual(codes, [0] * 10)
        with open(self.depot.fichier, encoding="utf-8") as f:
            brut = f.read().splitlines()
        # chaque ligne est intacte (aucun entrelacement) ; une ligne peut manquer si le verrou a expiré
        self.assertGreaterEqual(len(brut), 8)
        for l in brut:
            self.assertIsNotNone(journal.valider(json.loads(l)), l)

    def test_sel_stable(self):
        self.lancer_ok(entree("Stop", session_id="meme"))
        self.lancer_ok(entree("Stop", session_id="meme"))
        a, b = self.depot.lignes()
        self.assertEqual(a["session"], b["session"])


class TestSettingsPartage(unittest.TestCase):
    """Le mode Direct est optionnel et local : .claude/settings.json (partagé par Git) ne le déclare pas."""

    def test_settings_json_sans_hook_d_observation(self):
        with open(SETTINGS, encoding="utf-8") as f:
            texte = f.read()
        self.assertNotIn("journal_direct", texte)
        self.assertNotIn('"async"', texte)
        hooks = json.loads(texte)["hooks"]["PreToolUse"]
        groupes = {g["matcher"]: g["hooks"][0]["command"] for g in hooks}
        self.assertIn("proteger_valide.py", groupes["Write|Edit|MultiEdit"])     # R5, R6, R9
        self.assertIn("restreindre_bash.py", groupes["Bash"])                     # garde-fous 7 et 9 (R17)

    @unittest.skipUnless(shutil.which("git"), "git absent")
    def test_branche_ne_modifie_pas_settings_json(self):
        """Tant que la branche n'est pas fusionnée : settings.json identique à son point de départ sur main."""
        def git(*args):
            return subprocess.run(["git", "-C", RACINE] + list(args), capture_output=True, text=True)
        branche = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if branche != "outil/bureau-direct":
            self.skipTest("contrôle propre à la branche outil/bureau-direct")
        base = None
        for ref in ("main", "origin/main"):
            r = git("merge-base", "HEAD", ref)
            if r.returncode == 0:
                base = r.stdout.strip()
                break
        if not base:
            self.skipTest("main introuvable (clone superficiel)")
        attendu = git("show", "{}:.claude/settings.json".format(base)).stdout
        with open(SETTINGS, encoding="utf-8", newline="") as f:
            self.assertEqual(f.read().replace("\r\n", "\n"), attendu.replace("\r\n", "\n"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
