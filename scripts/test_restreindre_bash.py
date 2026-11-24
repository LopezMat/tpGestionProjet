#!/usr/bin/env python3
"""Tests du hook .claude/hooks/restreindre_bash.py (Bash par agent). Responsable : C · Lot 2 (C).

Lancement : python scripts/test_restreindre_bash.py
Le hook est lancé comme par Claude Code : JSON sur stdin, avec ou sans `agent_type`.
Bibliothèque standard uniquement.
"""
import json
import os
import subprocess
import sys
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(RACINE, ".claude", "hooks", "restreindre_bash.py")


def lancer(commande, agent=None, args=(), brut=None):
    entree = {"tool_name": "Bash", "tool_input": {"command": commande}}
    if agent:
        entree["agent_type"] = agent
    donnees = brut if brut is not None else json.dumps(entree).encode("utf-8")
    r = subprocess.run([sys.executable, HOOK, *args], input=donnees, capture_output=True)
    return r.returncode, r.stderr.decode("utf-8", errors="replace")


class TestRestreindreBash(unittest.TestCase):

    def ok(self, commande, agent=None, args=()):
        code, err = lancer(commande, agent, args)
        self.assertEqual(code, 0, "{!r} ({}) aurait dû passer ; stderr={}".format(commande, agent, err))

    def ko(self, commande, agent=None, extrait="", args=()):
        code, err = lancer(commande, agent, args)
        self.assertEqual(code, 2, "{!r} ({}) aurait dû être refusé".format(commande, agent))
        self.assertIn(extrait, err)

    # -- session principale ---------------------------------------------------
    def test_session_principale_libre(self):
        self.ok("git push origin main")          # l'ask de settings.json s'applique ensuite
        self.ok("cat README.md | head -5")

    # -- chef-de-projet -------------------------------------------------------
    def test_chef_tableau(self):
        self.ok("python scripts/tableau.py", "chef-de-projet")
        self.ok("python ./scripts/tableau.py --projet reservation-salle", "chef-de-projet")

    def test_chef_tableau_python3(self):
        self.ok("python3 scripts/tableau.py", "chef-de-projet")
        self.ok("python3 ./scripts/tableau.py --projet reservation-salle", "chef-de-projet")
        self.ok("/usr/bin/python3 scripts/tableau.py", "chef-de-projet")
        self.ko("python3 scripts/tableau.py && ls", "chef-de-projet", "chef-de-projet")
        self.ko("python3 -c 'import os'", "chef-de-projet", "chef-de-projet")
        self.ko("python2 scripts/tableau.py", "chef-de-projet", "chef-de-projet")

    def test_chef_autres_commandes(self):
        self.ko("ls", "chef-de-projet", "chef-de-projet")
        self.ko("python scripts/tableau.py && rm x", "chef-de-projet", "chef-de-projet")
        self.ko("python scripts/tableau.py > TABLEAU.md", "chef-de-projet", "chef-de-projet")
        self.ko("python scripts/tableau.py $(whoami)", "chef-de-projet", "chef-de-projet")
        self.ko("python scripts/autre.py", "chef-de-projet", "chef-de-projet")
        self.ko("python scripts/tableau.py\nls", "chef-de-projet", "chef-de-projet")

    # -- relecteur-code -------------------------------------------------------
    def test_relecteur(self):
        self.ok("git diff HEAD~1", "relecteur-code")
        self.ok("git log --oneline --grep T-003", "relecteur-code")
        self.ok("git show abc1234", "relecteur-code")
        self.ko("git commit -m x", "relecteur-code", "relecteur-code")
        self.ko("git diff --output=patch.txt", "relecteur-code", "relecteur-code")
        self.ko("git log | head", "relecteur-code", "relecteur-code")

    # -- deployeur ------------------------------------------------------------
    def test_deployeur(self):
        self.ok("gh workflow run deploy.yml -f projet=demo -f sha=abc1234", "deployeur")
        self.ok("gh run view 123 --log", "deployeur")
        self.ok("git rev-parse HEAD", "deployeur")
        self.ok("python .claude/skills/verifier-prod/verifier_prod.py --url https://x.onrender.com --sha abc1234",
                "deployeur")
        self.ok("python3 .claude/skills/verifier-prod/verifier_prod.py --url https://x.onrender.com --sha abc1234",
                "deployeur")
        self.ok("python3 ./.claude/skills/verifier-prod/verifier_prod.py --url http://localhost:8000 --sha abc1234",
                "deployeur")
        self.ko("python3 scripts/tableau.py", "deployeur", "deployeur")
        self.ko("curl https://exemple.org", "deployeur", "deployeur")
        self.ko("gh secret list", "deployeur", "deployeur")

    def test_deployeur_git_sans_ecriture(self):
        # DEC-002 § 37 : même filtre que relecteur-code et gestionnaire-crise
        d = "deployeur"
        self.ok("git log --oneline -5", d)
        self.ok("git rev-parse HEAD", d)
        self.ko("git log --output=deploiement.txt", d, d)
        self.ko("git log --ext-diff -p", d, d)
        self.ko("git rev-parse --output=x HEAD", d, d)

    # -- analyste-prod (lot2-D point 2, DEC-002) -------------------------------
    def test_analyste_prod(self):
        a = "analyste-prod"
        self.ok("python scripts/sonde_sante.py --url https://x.onrender.com --sha abc1234", a)
        self.ok("python3 scripts/sonde_sante.py --url https://x.onrender.com --sha abc1234", a)
        self.ok("py ./scripts/sonde_sante.py --url http://localhost:8000 --mesures 1", a)
        self.ok("python3 ./scripts/sonde_sante.py --url http://localhost:8000", a)
        self.ko("curl https://x.onrender.com/health", a, a)
        self.ko("python scripts/tableau.py", a, a)
        self.ko("git log --oneline -5", a, a)
        self.ko("python scripts/sonde_sante.py --url https://x.onrender.com && ls", a, a)
        self.ko("python scripts/sonde_sante.py --url https://x.onrender.com > suivi.md", a, a)
        self.ko("python scripts/sonde_sante.py --url $(cat url.txt)", a, a)
        self.ko("python -c 'import urllib.request'", a, a)
        self.ko("git push", a, "S3-R3")

    # -- gestionnaire-crise (lot2-D point 2, DEC-002) --------------------------
    def test_gestionnaire_crise(self):
        g = "gestionnaire-crise"
        self.ok("python scripts/sonde_sante.py --url https://x.onrender.com --sha abc1234", g)
        self.ok("python3 scripts/sonde_sante.py --url http://localhost:8000", g)
        self.ok("git log --oneline -5", g)
        self.ok("git rev-parse HEAD", g)
        self.ok("gh run list --limit 5", g)
        self.ok("gh run view 123 --log", g)
        self.ko("gh workflow run deploy.yml -f projet=demo -f sha=abc1234", g, g)
        self.ko("gh run rerun 123", g, g)
        self.ko("gh run watch 123", g, g)
        self.ko("git log --output=chronologie.txt", g, g)
        self.ko("git log --ext-diff", g, g)
        self.ko("git revert HEAD", g, g)
        self.ko("curl https://x.onrender.com/health", g, g)
        self.ko("rm app/tmp.txt", g, g)
        self.ko("git log | head", g, g)
        self.ko("git push origin main", g, "S3-R3")
        self.ko("rm -rf app/", g, "rm")

    # -- règles communes (dev, testeur, securite…) ----------------------------
    def test_dev_git_local(self):
        self.ok("git commit -m 'T-003 : bouton push notification'", "dev-backend")
        self.ok("npm test", "dev-frontend")
        self.ok("python -m venv .venv", "dev-backend")

    def test_push_interdit(self):
        self.ko("git push", "dev-backend", "S3-R3")
        self.ko("git push origin main", "testeur", "S3-R3")
        self.ko("git -C . push", "dev-backend", "S3-R3")
        self.ko("git -c push.default=current push", "dev-backend", "S3-R3")
        self.ko("npm test && git push", "dev-frontend", "S3-R3")
        self.ko("bash -c 'git push origin main'", "dev-backend", "S3-R3")
        self.ko("/usr/bin/git push", "securite", "S3-R3")

    def test_env_interdit(self):
        self.ko("cat .env", "dev-backend", "S3-R8")
        self.ko("cp app/.env.local /tmp/x", "securite", "S3-R8")
        self.ko("echo $(cat .env)", "testeur", "S3-R8")
        self.ko("python -c 'print(1)' > .env", "dev-backend", "S3-R8")

    def test_destructeurs(self):
        self.ko("git reset --hard HEAD~1", "dev-backend", "reset --hard")
        self.ko("rm -rf app/", "dev-backend", "rm")
        self.ko("rm -r -f app/", "testeur", "rm")
        self.ok("rm app/tmp.txt", "dev-backend")

    def test_agent_force_plan_b(self):
        self.ko("ls", None, "chef-de-projet", args=("--agent", "chef-de-projet"))
        self.ok("python scripts/tableau.py", None, args=("--agent", "chef-de-projet"))

    def test_json_invalide(self):
        code, err = lancer("", brut=b"{pas du json")
        self.assertEqual(code, 2)
        self.assertIn("par prudence", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
