#!/usr/bin/env python3
"""Tests de scripts/sonde_sante.py. Responsable : D · Lot 2 (D).

Lancement : python scripts/test_sonde_sante.py   (Mac : python3 …)
Un petit serveur /health local (thread) simule la production ; les délais sont réduits.
Bibliothèque standard uniquement.
"""
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RACINE, "scripts", "sonde_sante.py")
SHA = "0123456789abcdef0123456789abcdef01234567"
AUTRE = "fedcba9876543210fedcba9876543210fedcba98"


class Serveur:
    """Réponses programmées : liste de (code, corps) ; la dernière se répète. `pause` en secondes."""

    def __init__(self, reponses, pause=0.0):
        self.reponses, self.appels, self.pause = list(reponses), 0, pause
        parent = self

        class Gestion(BaseHTTPRequestHandler):
            def do_GET(self):
                k = min(parent.appels, len(parent.reponses) - 1)
                parent.appels += 1
                code, corps = parent.reponses[k]
                if self.path != "/health":
                    code, corps = 404, "{}"
                if parent.pause:
                    time.sleep(parent.pause)
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


def lancer(*args, cwd=None):
    r = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, cwd=cwd)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


def port_ferme():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return "http://127.0.0.1:{}".format(port)


class TestSondeSante(unittest.TestCase):

    def avec_serveur(self, reponses, *args, pause=0.0):
        srv = Serveur(reponses, pause)
        try:
            return lancer("--url", srv.url, "--intervalle", "0", *args)
        finally:
            srv.arreter()

    def test_disponible_et_a_jour(self):
        code, out = self.avec_serveur([sante(SHA)], "--sha", SHA)
        self.assertEqual(code, 0, out)
        self.assertIn("RESULTAT: DISPONIBLE ET À JOUR", out)
        self.assertIn("Disponibilité : 3/3", out)
        self.assertIn("| Mesure | Heure | Code HTTP | SHA renvoyé | Temps (ms) | Résultat |", out)
        self.assertIn("Mode : local", out)

    def test_prefixe_accepte(self):
        code, out = self.avec_serveur([sante(SHA[:7])], "--sha", SHA)
        self.assertEqual(code, 0, out)
        self.assertIn("OK (préfixe)", out)

    def test_sha_different(self):
        code, out = self.avec_serveur([sante(AUTRE)], "--sha", SHA)
        self.assertEqual(code, 1, out)
        self.assertIn("RESULTAT: SHA DIFFÉRENT", out)
        self.assertIn("SHA_DIFFERENT", out)

    def test_sans_sha(self):
        code, out = self.avec_serveur([sante(AUTRE)], "--mesures", "2")
        self.assertEqual(code, 0, out)
        self.assertIn("RESULTAT: DISPONIBLE", out)
        self.assertNotIn("À JOUR", out)
        self.assertIn("(non fourni)", out)

    def test_lent(self):
        code, out = self.avec_serveur([sante(SHA)], "--sha", SHA, "--mesures", "1", "--seuil-ms", "50", pause=0.2)
        self.assertEqual(code, 1, out)
        self.assertIn("RESULTAT: DÉGRADÉ (lent)", out)

    def test_injoignable(self):
        code, out = lancer("--url", port_ferme(), "--sha", SHA, "--mesures", "2", "--intervalle", "0",
                           "--delai-reseau", "2")
        self.assertEqual(code, 4, out)
        self.assertIn("INJOIGNABLE", out)
        self.assertIn("RESULTAT: INDISPONIBLE", out)

    def test_http_503(self):
        code, out = self.avec_serveur([(503, "{}")], "--sha", SHA, "--mesures", "2")
        self.assertEqual(code, 4, out)
        self.assertIn("HTTP_503", out)

    def test_json_invalide(self):
        code, out = self.avec_serveur([(200, "pas du json")], "--sha", SHA, "--mesures", "1")
        self.assertEqual(code, 4, out)
        self.assertIn("JSON_INVALIDE", out)

    def test_disponibilite_partielle(self):
        code, out = self.avec_serveur([(503, "{}"), sante(SHA)], "--sha", SHA, "--mesures", "3")
        self.assertEqual(code, 1, out)
        self.assertIn("Disponibilité : 2/3", out)
        self.assertIn("RESULTAT: DÉGRADÉ (disponibilité partielle)", out)

    def test_erreurs_usage(self):
        for args, extrait in (
                (["--url", "ftp://exemple.org", "--sha", SHA], "URL invalide"),
                (["--url", "pas-une-url"], "URL invalide"),
                (["--url", "http://127.0.0.1:1", "--sha", "xyz"], "SHA invalide"),
                (["--url", "http://127.0.0.1:1", "--mesures", "0"], "paramètres invalides"),
                (["--url", "http://127.0.0.1:1", "--mesures", "20", "--intervalle", "60"], "durée maximale")):
            code, out = lancer(*args)
            self.assertEqual(code, 2, (args, out))
            self.assertIn(extrait, out)

    def test_aucun_fichier_ecrit(self):
        srv = Serveur([sante(SHA)])
        try:
            with tempfile.TemporaryDirectory() as tmp:
                code, out = lancer("--url", srv.url, "--sha", SHA, "--intervalle", "0", cwd=tmp)
                self.assertEqual(code, 0, out)
                self.assertEqual(os.listdir(tmp), [])
        finally:
            srv.arreter()


if __name__ == "__main__":
    unittest.main(verbosity=2)
