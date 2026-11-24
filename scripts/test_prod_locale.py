#!/usr/bin/env python3
"""Tests de la production locale Docker : deployer_local.py, rollback_local.py (DEC-003).

Responsable : C · Lot 5 · voir ARCHITECTURE § 10, S3-R4 à S3-R7.

Lancement : python scripts/test_prod_locale.py

- TestSimulation : sans Docker. Un faux Docker (scripts/fixtures/faux_docker.py) tient son
  état dans un JSON ; un serveur /health local renvoie le SHA de l'image « lancée ». Les
  scripts tournent sur un dépôt Git temporaire avec de vrais commits.
- TestReel : avec Docker, s'il répond (sinon ignoré, avec la raison). Mini-app de
  scripts/fixtures/app-demo, vraie base Postgres, vrai pg_dump : v1, v2, v3 en panne, puis
  rollback vers v2. C'est la répétition automatisée du test de rollback (S3-R7).
  ESN_TEST_DOCKER=0 l'ignore volontairement.

Bibliothèque standard uniquement.
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPLOYER = os.path.join(RACINE, "scripts", "deployer_local.py")
ROLLBACK = os.path.join(RACINE, "scripts", "rollback_local.py")
FAUX_DOCKER = os.path.join(RACINE, "scripts", "fixtures", "faux_docker.py")
APP_DEMO = os.path.join(RACINE, "scripts", "fixtures", "app-demo")
sys.path.insert(0, os.path.join(RACINE, "scripts"))
import prod_locale as pl  # noqa: E402

RAPIDE = ["--intervalle", "0.2", "--timeout", "1.5"]


def git(depot, *args):
    r = subprocess.run(["git", "-C", depot, "-c", "user.name=test", "-c", "user.email=test@exemple.org",
                        "-c", "commit.gpgsign=false", *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace"))
    return r.stdout.decode("utf-8").strip()


def commiter(depot, fichiers, message):
    for chemin, contenu in fichiers.items():
        complet = os.path.join(depot, chemin)
        os.makedirs(os.path.dirname(complet), exist_ok=True)
        with open(complet, "w", encoding="utf-8", newline="\n") as f:
            f.write(contenu)
    git(depot, "add", "-A")
    git(depot, "commit", "-q", "-m", message)
    return git(depot, "rev-parse", "HEAD")


def ecrire_projet(depot, slug, hebergement, url):
    chemin = os.path.join(depot, "projets", slug, "projet.md")
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write("---\ntitre: Fiche projet\nstatut: BROUILLON\nslug: {}\nhebergement: {}   # DEC-003\n"
                "url_prod: {}\n---\n".format(slug, hebergement, url))


def lancer(script, *args, env=None):
    r = subprocess.run([sys.executable, script, *args], capture_output=True, env=env)
    return r.returncode, r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")


def port_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class TestSimulation(unittest.TestCase):
    SLUG = "demo"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.depot = os.path.join(self.tmp.name, "depot")
        os.makedirs(self.depot)
        git(self.depot, "init", "-q")
        app = "projets/{}/app/".format(self.SLUG)
        self.v1 = commiter(self.depot, {app + "Dockerfile": "FROM scratch\n", app + "app.py": "v = 1\n"}, "v1")
        self.v2 = commiter(self.depot, {app + "app.py": "v = 2\n"}, "v2")
        self.v3 = commiter(self.depot, {app + "Dockerfile": "FROM scratch\n# PANNE\n"}, "v3 en panne")
        self.v4 = commiter(self.depot, {app + "Dockerfile": "FROM scratch\n# CASSE\n"}, "v4 cassée")
        self.etat = os.path.join(self.tmp.name, "faux-docker.json")
        self.ecrire_etat({"images": {}, "volumes": [], "lancee": None})
        self.env = dict(os.environ, ESN_DOCKER_SIMULATION=FAUX_DOCKER, ESN_DOCKER_SIMULATION_ETAT=self.etat)
        self.httpd = self.serveur_sante()
        self.url = "http://127.0.0.1:{}".format(self.httpd.server_address[1])
        ecrire_projet(self.depot, self.SLUG, "local", self.url)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def ecrire_etat(self, etat):
        with open(self.etat, "w", encoding="utf-8") as f:
            json.dump(etat, f)

    def lire_etat(self):
        with open(self.etat, "r", encoding="utf-8") as f:
            return json.load(f)

    def modifier_etat(self, **valeurs):
        etat = self.lire_etat()
        etat.update(valeurs)
        self.ecrire_etat(etat)

    def serveur_sante(self):
        parent = self

        class Sante(BaseHTTPRequestHandler):
            def do_GET(self):
                etat = parent.lire_etat()
                img = etat["images"].get(etat.get("lancee") or "")
                if not img or img["panne"]:
                    code, corps = 503, "{}"
                else:
                    code, corps = 200, json.dumps({"status": "ok", "commit": img["commit"]})
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(corps.encode("utf-8"))

            def log_message(self, *args):
                pass

        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Sante)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        return httpd

    def deployer(self, sha, *options):
        return lancer(DEPLOYER, "--projet", self.SLUG, "--sha", sha, "--racine", self.depot,
                      *(options or RAPIDE), env=self.env)

    def rollback(self, *options):
        return lancer(ROLLBACK, "--projet", self.SLUG, "--racine", self.depot, *(options or RAPIDE),
                      env=self.env)

    def historique(self):
        return pl.charger_historique(self.depot, self.SLUG)

    def dumps(self):
        return pl.sauvegardes(self.depot, self.SLUG)

    # -- cas nominaux ----------------------------------------------------------
    def test_premier_deploiement(self):
        code, out = self.deployer(self.v1[:7])
        self.assertEqual(code, 0, out)
        self.assertIn("VERSION_PRECEDENTE: aucune", out)
        self.assertIn("SAUVEGARDE: aucune (première mise en service", out)
        self.assertIn("IMAGE: esn-demo:{} (construite)".format(self.v1), out)
        self.assertIn("RESULTAT: EN LIGNE ET À JOUR", out)
        self.assertEqual(self.lire_etat()["lancee"], "esn-demo:" + self.v1)
        self.assertEqual(self.historique()[-1]["resultat"], pl.RESULTAT_OK)
        self.assertTrue(os.path.exists(os.path.join(self.depot, "deploiement", "local", "demo", "db_password")))
        self.assertTrue(os.path.exists(os.path.join(self.depot, self.historique()[-1]["etat"])))

    def test_deuxieme_deploiement_sauvegarde(self):
        self.assertEqual(self.deployer(self.v1)[0], 0)
        code, out = self.deployer(self.v2)
        self.assertEqual(code, 0, out)
        self.assertIn("VERSION_PRECEDENTE: " + self.v1, out)
        self.assertEqual(len(self.dumps()), 1)
        self.assertTrue(os.path.basename(self.dumps()[0]).endswith("-{}.dump".format(self.v1[:7])))
        self.assertIn("SAUVEGARDE: deploiement/local/demo/sauvegardes/", out)
        # l'image est construite à partir du commit : le build-arg porte le SHA complet
        build = [a for a in self.lire_etat()["appels"] if a[:1] == ["build"]][-1]
        self.assertIn("GIT_COMMIT=" + self.v2, build)

    def test_panne_puis_rollback(self):
        self.assertEqual(self.deployer(self.v1)[0], 0)
        self.assertEqual(self.deployer(self.v2)[0], 0)
        code, out = self.deployer(self.v3)
        self.assertEqual(code, 1, out)
        self.assertIn("HTTP_503", out)
        self.assertIn("SUITE: rollback (S3-R6)", out)
        code, out = self.rollback()
        self.assertEqual(code, 0, out)
        self.assertIn("VERSION_RESTAUREE: " + self.v2, out)
        self.assertIn("(relancée sans rebuild)", out)
        self.assertIn("non restaurée : décision humaine", out)
        self.assertIn("RESULTAT: EN LIGNE ET À JOUR", out)
        self.assertEqual(self.lire_etat()["lancee"], "esn-demo:" + self.v2)
        builds = [a for a in self.lire_etat()["appels"] if a[:1] == ["build"]]
        self.assertEqual(len(builds), 3)  # aucun rebuild au rollback
        etats = [e["etat"] for e in self.historique()]
        self.assertEqual(len(etats), len(set(etats)), "un fichier d'état par vérification")
        self.assertEqual(self.historique()[-1]["type"], "rollback")

    def test_redeploiement_meme_sha_sans_faux_succes(self):
        self.assertEqual(self.deployer(self.v1)[0], 0)
        self.assertEqual(self.deployer(self.v2)[0], 0)
        self.modifier_etat(lancee=None)  # l'app s'arrête
        code, out = self.deployer(self.v2)
        self.assertIn("(déjà construite)", out)
        self.assertEqual(code, 0, out)  # relancée par compose up, puis vérifiée pour de vrai
        etats = [e["etat"] for e in self.historique()]
        self.assertEqual(len(etats), len(set(etats)))

    # -- échecs avant le lancement : rien ne change -------------------------------
    def test_build_casse(self):
        self.assertEqual(self.deployer(self.v1)[0], 0)
        code, out = self.deployer(self.v4)
        self.assertEqual(code, 5, out)
        self.assertIn("ÉCHEC DU BUILD, production inchangée", out)
        self.assertEqual(self.lire_etat()["lancee"], "esn-demo:" + self.v1)
        code, out = self.rollback()
        self.assertEqual(code, 2, out)
        self.assertIn("rien à annuler", out)

    def test_sauvegarde_en_echec(self):
        self.assertEqual(self.deployer(self.v1)[0], 0)
        self.modifier_etat(pg_dump_echec=True)
        code, out = self.deployer(self.v2)
        self.assertEqual(code, 4, out)
        self.assertIn("rien n'a été déployé (S3-R4)", out)
        self.assertEqual(self.dumps(), [])
        self.assertEqual(self.lire_etat()["lancee"], "esn-demo:" + self.v1)
        self.assertFalse([a for a in self.lire_etat()["appels"] if a[:1] == ["build"] and self.v2 in " ".join(a)])

    def test_retention(self):
        self.assertEqual(self.deployer(self.v1)[0], 0)
        dossier = os.path.join(self.depot, "deploiement", "local", "demo", "sauvegardes")
        os.makedirs(dossier, exist_ok=True)
        for k in range(12):
            with open(os.path.join(dossier, "20250101-0000{:02d}-ancien.dump".format(k)), "wb") as f:
                f.write(b"x")
        code, out = self.deployer(self.v2)
        self.assertEqual(code, 0, out)
        restantes = [os.path.basename(c) for c in self.dumps()]
        self.assertEqual(len(restantes), pl.RETENTION)
        self.assertTrue(restantes[-1].endswith(self.v1[:7] + ".dump"))  # la nouvelle est gardée
        self.assertIn("Rétention : sauvegarde supprimée", out)

    # -- préconditions (code 2) -------------------------------------------------
    def test_preconditions(self):
        self.assertEqual(self.deployer("abcdef0")[0], 2)                       # SHA inconnu
        self.assertEqual(self.deployer("pas-un-sha")[0], 2)
        self.assertEqual(lancer(DEPLOYER, "--projet", "Pas_Un_Slug", "--sha", self.v1, "--racine", self.depot,
                                env=self.env)[0], 2)
        ecrire_projet(self.depot, self.SLUG, "render", self.url)
        code, out = self.deployer(self.v1)
        self.assertEqual(code, 2, out)
        self.assertIn("hebergement doit valoir « local »", out)
        ecrire_projet(self.depot, self.SLUG, "local", "https://demo.onrender.com")
        code, out = self.deployer(self.v1)
        self.assertEqual(code, 2, out)
        self.assertIn("url_prod doit être http://localhost", out)
        ecrire_projet(self.depot, self.SLUG, "local", self.url)
        self.modifier_etat(docker_absent=True)
        code, out = self.deployer(self.v1)
        self.assertEqual(code, 2, out)
        self.assertIn("Docker ne répond pas", out)
        self.assertEqual(self.lire_etat()["lancee"], None)

    def test_dockerfile_absent(self):
        sha = commiter(self.depot, {"README.md": "x\n"}, "autre")
        git(self.depot, "rm", "-q", "-r", "projets/demo/app")
        git(self.depot, "-c", "user.name=t", "commit", "-q", "-m", "sans app")
        sans_app = git(self.depot, "rev-parse", "HEAD")
        self.assertNotEqual(sha, sans_app)
        code, out = self.deployer(sans_app)
        self.assertEqual(code, 2, out)
        self.assertIn("Dockerfile absent", out)

    def test_rollback_refus(self):
        code, out = self.rollback()
        self.assertEqual(code, 2, out)
        self.assertIn("aucun déploiement local connu", out)
        self.assertEqual(self.deployer(self.v1)[0], 0)
        code, out = self.rollback()
        self.assertEqual(code, 2, out)
        self.assertIn("S2-R7", out)                                   # dernier déploiement vérifié
        code, out = self.rollback("--sha", self.v2, *RAPIDE)
        self.assertEqual(code, 2, out)
        self.assertIn("absente en local", out)                         # image jamais construite
        code, out = self.rollback("--sha", self.v1, *RAPIDE)           # cible explicite après décision
        self.assertEqual(code, 0, out)

    def test_premier_deploiement_en_panne_sans_rollback(self):
        code, out = self.deployer(self.v3)
        self.assertEqual(code, 1, out)
        code, out = self.rollback()
        self.assertEqual(code, 2, out)
        self.assertIn("aucune version précédente vérifiée", out)


def docker_reel_disponible():
    if os.environ.get("ESN_TEST_DOCKER") == "0":
        return False, "ESN_TEST_DOCKER=0"
    try:
        r = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"], capture_output=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, "docker indisponible ({})".format(e)
    return (r.returncode == 0, "docker ne répond pas" if r.returncode else "")


DISPO, RAISON = docker_reel_disponible()


@unittest.skipUnless(DISPO, "test réel ignoré : " + RAISON)
class TestReel(unittest.TestCase):
    """Déploiement, sauvegarde, panne et rollback avec un vrai Docker (S3-R7)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.depot = os.path.join(self.tmp.name, "depot")
        self.slug = "test-" + uuid.uuid4().hex[:8]
        self.port = port_libre()
        app = os.path.join(self.depot, "projets", self.slug, "app")
        shutil.copytree(APP_DEMO, app)
        git(self.depot, "init", "-q")
        git(self.depot, "add", "-A")
        git(self.depot, "commit", "-q", "-m", "v1")
        self.v1 = git(self.depot, "rev-parse", "HEAD")
        with open(os.path.join(app, "app.py"), "a", encoding="utf-8", newline="\n") as f:
            f.write("# v2\n")
        self.v2 = commiter(self.depot, {}, "v2")
        with open(os.path.join(app, "Dockerfile"), "a", encoding="utf-8", newline="\n") as f:
            f.write('CMD ["python", "-c", "raise SystemExit(1)"]\n')   # v3 : s'arrête au démarrage
        self.v3 = commiter(self.depot, {}, "v3 en panne")
        ecrire_projet(self.depot, self.slug, "local", "http://localhost:{}".format(self.port))
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("ESN_DOCKER_SIMULATION")}

    def tearDown(self):
        try:
            mdp = pl.mot_de_passe(self.depot, self.slug, creer=False)
        except pl.Erreur:
            mdp = "absent"
        env = pl.env_compose(self.slug, self.port, mdp)
        subprocess.run(["docker", "compose", "-p", pl.nom_projet(self.slug), "-f", pl.COMPOSE, "down", "-v",
                        "--remove-orphans"], capture_output=True, env=env)
        for sha in (self.v1, self.v2, self.v3):
            subprocess.run(["docker", "image", "rm", "-f", pl.image(self.slug, sha)], capture_output=True)
        self.tmp.cleanup()

    def deployer(self, sha, timeout):
        return lancer(DEPLOYER, "--projet", self.slug, "--sha", sha, "--racine", self.depot,
                      "--intervalle", "2", "--timeout", str(timeout), env=self.env)

    def test_deploiement_panne_rollback(self):
        code, out = self.deployer(self.v1, 120)
        self.assertEqual(code, 0, out)
        code, out = self.deployer(self.v2, 90)
        self.assertEqual(code, 0, out)
        dumps = pl.sauvegardes(self.depot, self.slug)
        self.assertEqual(len(dumps), 1, out)
        with open(dumps[0], "rb") as f:
            self.assertEqual(f.read(5), b"PGDMP")                       # vrai dump au format custom
        code, out = self.deployer(self.v3, 20)
        self.assertEqual(code, 1, out)
        code, out = lancer(ROLLBACK, "--projet", self.slug, "--racine", self.depot, "--intervalle", "2",
                           "--timeout", "90", env=self.env)
        self.assertEqual(code, 0, out)
        self.assertIn("VERSION_RESTAUREE: " + self.v2, out)
        self.assertIn("RESULTAT: EN LIGNE ET À JOUR", out)
        # commande de restauration du runbook perte-donnees (exécutée par un humain après décision)
        env = pl.env_compose(self.slug, self.port, pl.mot_de_passe(self.depot, self.slug, creer=False))
        with open(dumps[0], "rb") as f:
            r = subprocess.run(["docker", "compose", "-p", pl.nom_projet(self.slug), "-f", pl.COMPOSE, "exec", "-T",
                                "db", "pg_restore", "--clean", "--if-exists", "-U", "esn", "-d", "app"],
                               stdin=f, capture_output=True, env=env)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        sys.stderr.write("\n[test reel] v1 {} -> v2 {} (sauvegarde {} o) -> v3 {} en ECHEC -> rollback vers v2 "
                         "verifie\n".format(self.v1[:7], self.v2[:7], os.path.getsize(dumps[0]), self.v3[:7]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
