#!/usr/bin/env python3
"""Tests de .claude/skills/verifier-prod/verifier_prod.py. Responsable : C · Lot 2 (C).

Lancement : python scripts/test_verifier_prod.py
Un petit serveur /health local (thread) simule la production ; les délais sont réduits.
Bibliothèque standard uniquement.
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RACINE, ".claude", "skills", "verifier-prod", "verifier_prod.py")
SHA = "0123456789abcdef0123456789abcdef01234567"
AUTRE = "fedcba9876543210fedcba9876543210fedcba98"


class Serveur:
    """Réponses programmées : liste de (code, corps) ; la dernière se répète."""

    def __init__(self, reponses):
        self.reponses, self.appels = list(reponses), 0
        parent = self

        class Gestion(BaseHTTPRequestHandler):
            def do_GET(self):
                k = min(parent.appels, len(parent.reponses) - 1)
                parent.appels += 1
                code, corps = parent.reponses[k]
                if self.path != "/health":
                    code, corps = 404, "{}"
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(corps.encode("utf-8"))

            def log_message(self, *args):
                pass

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Gestion)
        self.url = "http://127.0.0.1:{}".format(self.httpd.server_address[1])
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def arreter(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def sante(sha):
    return 200, json.dumps({"status": "ok", "commit": sha})


def lancer(*args):
    r = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


class TestVerifierProd(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.etat = os.path.join(self.tmp.name, "rapports", "verifier-prod-0123456.json")
        self.serveurs = []

    def tearDown(self):
        for s in self.serveurs:
            s.arreter()
        self.tmp.cleanup()

    def serveur(self, reponses):
        s = Serveur(reponses)
        self.serveurs.append(s)
        return s

    def test_concordance_immediate(self):
        s = self.serveur([sante(SHA)])
        code, out = lancer("--url", s.url + "/", "--sha", SHA, "--etat", self.etat)
        self.assertEqual(code, 0, out)
        self.assertIn("RESULTAT: EN LIGNE ET À JOUR", out)
        self.assertIn("Mode : local", out)
        self.assertIn("| 1 |", out)

    def test_reveil_puis_concordance(self):
        s = self.serveur([(503, "{}"), sante(AUTRE), sante(SHA)])
        code, out = lancer("--url", s.url, "--sha", SHA, "--intervalle", "0.2", "--timeout", "10")
        self.assertEqual(code, 0, out)
        self.assertIn("HTTP_503", out)
        self.assertIn("SHA_DIFFERENT", out)
        self.assertIn("| 3 |", out)

    def test_prefixe(self):
        s = self.serveur([sante(SHA[:7])])
        code, out = lancer("--url", s.url, "--sha", SHA)
        self.assertEqual(code, 0, out)
        self.assertIn("OK (préfixe)", out)

    def test_sha_different_jusquau_timeout(self):
        s = self.serveur([sante(AUTRE)])
        code, out = lancer("--url", s.url, "--sha", SHA, "--intervalle", "0.5", "--timeout", "2",
                           "--etat", self.etat)
        self.assertEqual(code, 1, out)
        self.assertIn("RESULTAT: ÉCHEC", out)

    def test_reprise_code_3(self):
        s = self.serveur([sante(AUTRE), sante(AUTRE), sante(AUTRE), sante(SHA)])
        args = ["--url", s.url, "--sha", SHA, "--intervalle", "0.3", "--timeout", "30",
                "--max-appel", "0.5", "--etat", self.etat]
        code, out = lancer(*args)
        self.assertEqual(code, 3, out)
        self.assertIn("EN COURS", out)
        for _ in range(10):
            code, out = lancer(*args)
            if code != 3:
                break
        self.assertEqual(code, 0, out)
        with open(self.etat, encoding="utf-8") as f:
            etat = json.load(f)
        self.assertEqual(etat["resultat"], "EN LIGNE ET À JOUR")
        self.assertGreaterEqual(len(etat["tentatives"]), 4)  # les tentatives des appels successifs sont cumulées

    def test_injoignable(self):
        code, out = lancer("--url", "http://127.0.0.1:9", "--sha", SHA, "--intervalle", "0.2",
                           "--timeout", "0.5", "--delai-reseau", "0.5")
        self.assertEqual(code, 1, out)
        self.assertIn("INJOIGNABLE", out)

    def test_json_invalide(self):
        s = self.serveur([(200, "pas du json")])
        code, out = lancer("--url", s.url, "--sha", SHA, "--intervalle", "0.2", "--timeout", "0.5")
        self.assertEqual(code, 1, out)
        self.assertIn("JSON_INVALIDE", out)

    def test_erreurs_usage(self):
        self.assertEqual(lancer("--url", "ftp://x", "--sha", SHA)[0], 2)
        self.assertEqual(lancer("--url", "http://localhost:8000", "--sha", "pas-un-sha")[0], 2)

    def test_etat_dun_autre_sha(self):
        s = self.serveur([sante(SHA)])
        self.assertEqual(lancer("--url", s.url, "--sha", SHA, "--etat", self.etat)[0], 0)
        code, out = lancer("--url", s.url, "--sha", AUTRE, "--etat", self.etat)
        self.assertEqual(code, 2, out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
