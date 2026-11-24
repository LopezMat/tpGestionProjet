"""Mini-app de test : GET /health -> {"status": "ok", "commit": GIT_COMMIT, "base": "ok"|"injoignable"}.

Fixture de scripts/test_prod_locale.py (responsable : C · Lot 5). Bibliothèque standard uniquement.
"""
import json
import os
import socket
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def base_joignable():
    url = urllib.parse.urlparse(os.environ.get("DATABASE_URL", ""))
    try:
        with socket.create_connection((url.hostname or "db", url.port or 5432), timeout=2):
            return "ok"
    except OSError:
        return "injoignable"


class Sante(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
        corps = json.dumps({"status": "ok", "commit": os.environ.get("GIT_COMMIT") or "inconnu",
                            "base": base_joignable()}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(corps)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    # 0.0.0.0 dans le conteneur ; côté hôte, compose ne publie le port que sur 127.0.0.1.
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8000"))), Sante).serve_forever()  # nosec B104
