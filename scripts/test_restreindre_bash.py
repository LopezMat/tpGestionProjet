#!/usr/bin/env python3
"""Tests du hook .claude/hooks/restreindre_bash.py (Bash par agent, R17). Responsable : C · Lot 2 (C), lot 5.

Lancement : python scripts/test_restreindre_bash.py
Le hook est lancé comme par Claude Code : JSON sur stdin, avec ou sans `agent_type`.
Le hook ne fait que décider : aucune commande testée n'est exécutée.
Bibliothèque standard uniquement.
"""
import hashlib
import json
import os
import subprocess
import sys
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(RACINE, ".claude", "hooks", "restreindre_bash.py")
DEC_007 = "docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md"


def lancer(commande, agent=None, args=(), brut=None):
    entree = {"tool_name": "Bash", "tool_input": {"command": commande}}
    if agent:
        entree["agent_type"] = agent
    donnees = brut if brut is not None else json.dumps(entree).encode("utf-8")
    r = subprocess.run([sys.executable, HOOK, *args], input=donnees, capture_output=True)
    return r.returncode, r.stderr.decode("utf-8", errors="replace")


def decision(commande, agent=None):
    """Décision JSON écrite sur stdout (ou None) et code de sortie."""
    entree = {"tool_name": "Bash", "tool_input": {"command": commande}}
    if agent:
        entree["agent_type"] = agent
    r = subprocess.run([sys.executable, HOOK], input=json.dumps(entree).encode("utf-8"), capture_output=True)
    sortie = r.stdout.decode("utf-8", errors="replace").strip()
    return r.returncode, (json.loads(sortie)["hookSpecificOutput"] if sortie else None)


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
        # DEC-003 : production locale Docker ; deploy.yml et gh run n'existent plus pour lui.
        d = "deployeur"
        self.ok("python scripts/deployer_local.py --projet demo --sha abc1234", d)
        self.ok("python3 ./scripts/deployer_local.py --projet reservation-salle --sha 0123456789abcdef", d)
        self.ok("py scripts/rollback_local.py --projet demo", d)
        self.ok("python scripts/rollback_local.py --projet demo --sha abc1234", d)
        self.ko("gh workflow run deploy.yml -f projet=demo -f sha=abc1234", d, d)
        self.ko("gh run view 123 --log", d, d)
        self.ko("gh run list", d, d)
        self.ko("docker compose -p esn-demo down -v", d, d)
        self.ko("docker run --rm postgres:16-alpine", d, d)
        self.ko("python scripts/deployer_local.py --projet demo --sha abc1234; docker rm -f x", d, d)
        self.ko("python scripts/deployer_local.py --projet demo --sha $(git rev-parse HEAD)", d, d)
        self.ko("ESN_DOCKER_SIMULATION=x.py python scripts/deployer_local.py --projet demo --sha abc1234", d, d)
        self.ko("python scripts/prod_locale.py", d, d)
        self.ko("python -c 'import scripts.deployer_local'", d, d)
        self.ko("python scripts/deployer_local.py --projet 'demo x' --sha abc1234", d, d)
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
        # le gestionnaire-crise ne déploie ni ne rétablit jamais lui-même (runbook rollback)
        self.ko("python scripts/rollback_local.py --projet demo", g, g)
        self.ko("python scripts/deployer_local.py --projet demo --sha abc1234", g, g)

    # -- confirmation humaine du déploiement local (DEC-003, S3-R3) -------------
    def test_deploiement_ask(self):
        for agent in ("deployeur", None):
            for commande in ("python scripts/deployer_local.py --projet demo --sha abc1234",
                             "python3 scripts/rollback_local.py --projet demo"):
                code, dec = decision(commande, agent)
                self.assertEqual(code, 0, commande)
                self.assertIsNotNone(dec, "{!r} ({}) aurait dû demander une confirmation".format(commande, agent))
                self.assertEqual(dec["permissionDecision"], "ask")
                self.assertIn("S3-R3", dec["permissionDecisionReason"])
        # session principale : variantes de chemin et enveloppes
        for commande in ("python ./scripts/deployer_local.py --projet demo --sha abc1234",
                         "cd . && python C:/depot/scripts/rollback_local.py --projet demo",
                         "bash -c 'python scripts/deployer_local.py --projet demo --sha abc1234'",
                         "timeout 600 py -u scripts/deployer_local.py --projet demo --sha abc1234"):
            code, dec = decision(commande)
            self.assertEqual(code, 0, commande)
            self.assertIsNotNone(dec, commande)
            self.assertEqual(dec["permissionDecision"], "ask")
        # rien à confirmer pour les autres commandes
        self.assertEqual(decision("python scripts/test_prod_locale.py"), (0, None))
        self.assertEqual(decision("git rev-parse HEAD", "deployeur"), (0, None))
        self.assertEqual(decision("python .claude/skills/verifier-prod/verifier_prod.py --url "
                                  "http://localhost:8080 --sha abc1234", "deployeur"), (0, None))

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


class TestR17(unittest.TestCase):
    """R17 (DEC-010, DEC-015) : aucun document Markdown de docs/ ou projets/ modifié par Bash.

    Chaque forme est testée pour la session principale (auteur de l'incident DEC-007) et pour un agent."""

    APPELANTS = (None, "dev-backend")

    def refuse(self, commande, forme=""):
        for agent in self.APPELANTS:
            code, err = lancer(commande, agent)
            self.assertEqual(code, 2, "{!r} ({}) aurait dû être refusé (R17)".format(commande, agent or "session principale"))
            self.assertIn("Refusé (R17)", err)
            self.assertIn("Edit ou Write", err)        # le message renvoie vers les outils contrôlés
            self.assertIn(forme, err)

    def permet(self, commande):
        for agent in self.APPELANTS:
            code, err = lancer(commande, agent)
            self.assertEqual(code, 0, "{!r} ({}) aurait dû passer ; stderr={}".format(
                commande, agent or "session principale", err))

    # -- une forme refusée par test ----------------------------------------------
    def test_sed_i(self):
        self.refuse("sed -i 's/EN_REVUE/VALIDÉ/' docs/decisions/2026-11-26-DEC-015-regle-r17.md", "sed -i")
        self.refuse("sed -i.bak 's/a/b/' projets/demo/cdc.md", "sed -i")
        self.refuse("sed -Ei 's/a/b/' ./docs/ARCHITECTURE.md", "sed -i")
        self.refuse("sed --in-place 's/a/b/' projets/demo/tickets/T-001-x.md", "sed -i")
        self.refuse("sed -e 's/a/b/' -i 'docs\\systemes\\S1-gestion-projet.md'", "sed -i")   # séparateurs Windows
        self.refuse("perl -pi -e 's/a/b/' docs/VISION.md", "perl -i")

    def test_redirection_ecrase(self):
        self.refuse("echo 'statut: VALIDÉ' > docs/decisions/x.md", "redirection >")
        self.refuse("cat /tmp/nouveau.txt >./projets/demo/cdc.md", "redirection >")
        self.refuse("printf x 1>projets/demo/tickets/T-002-y.md", "redirection >")
        self.refuse('echo x > "projets/demo/rapports/a b.md"', "redirection >")
        self.refuse("echo x >| docs/VISION.md", "redirection >|")
        self.refuse("ls &> projets/demo/rapports/suivi.md", "redirection &>")
        self.refuse("cat > docs/decisions/x.md <<'EOF'\nstatut: VALIDÉ\nEOF", "redirection >")

    def test_redirection_ajoute(self):
        self.refuse("echo '- [x] critère' >> projets/demo/tickets/T-001-x.md", "redirection >>")
        self.refuse("echo ligne >>docs/CHANGELOG-REGLES.md", "redirection >>")

    def test_tee(self):
        self.refuse("echo x | tee docs/decisions/README.md", "tee")
        self.refuse("echo x | tee -a projets/demo/retex.md > /dev/null", "tee")
        self.refuse("tee projets/demo/cdc.md < /tmp/cdc.txt", "tee")

    def test_python_c(self):
        self.refuse("python -c \"open('docs/decisions/x.md', 'w').write('x')\"", "python -c")
        self.refuse("python3 -c \"from pathlib import Path; p = Path('projets/demo/cdc.md'); "
                    "p.write_text(p.read_text().replace('a', 'b'))\"", "python -c")
        self.refuse("py -3 -c \"open('docs/VISION.md', mode='a').write('x')\"", "python -c")
        self.refuse("python -X utf8 -c \"import os; os.replace('/tmp/x', os.path.join('docs', 'VISION.md'))\"",
                    "python -c")
        self.refuse("python -c \"import pathlib; [f.write_text('x') for f in pathlib.Path('docs').glob('*.md')]\"",
                    "python -c")

    def test_python_heredoc(self):
        script = ("from pathlib import Path\n"
                  "p = Path('projets/demo/tickets/T-001-x.md')\n"
                  "p.write_text(p.read_text(encoding='utf-8').replace('A_FAIRE', 'TERMINE'), encoding='utf-8')\n")
        self.refuse("python - <<'EOF'\n" + script + "EOF", "heredoc")
        self.refuse("python3 <<EOF\n" + script + "EOF\necho fini", "heredoc")
        self.refuse("cd /c/depot && python -u - << \"FIN\"\n" + script + "FIN", "heredoc")
        self.refuse("cat <<'EOF' | python -\n" + script + "EOF", "heredoc")

    def test_python_tube(self):
        self.refuse("echo \"open('docs/VISION.md', 'w').write('x')\" | python -", "entrée standard")
        self.refuse("python <<< \"open('docs/VISION.md', 'w').write('x')\"", "entrée standard")

    # -- contournements par imbrication ------------------------------------------
    def test_imbrications(self):
        self.refuse("bash -c \"sed -i 's/a/b/' docs/VISION.md\"", "sed -i")
        self.refuse("sh -c 'echo x >> projets/demo/cdc.md'", "redirection >>")
        self.refuse("eval \"echo x > docs/VISION.md\"", "redirection >")
        self.refuse("bash <<'EOF'\nsed -i 's/a/b/' docs/VISION.md\nEOF", "sed -i")
        self.refuse("echo ok\nsed -i 's/a/b/' docs/VISION.md", "sed -i")
        self.refuse("echo $(sed -i 's/a/b/' docs/VISION.md)", "sed -i")
        self.refuse("find docs -name '*.md' -exec sed -i 's/a/b/' {} +", "find ou xargs")
        self.refuse("find projets -name '*.md' | xargs sed -i 's/a/b/'", "find ou xargs")
        self.refuse("timeout 5 sed -i 's/a/b/' docs/VISION.md", "sed -i")

    # -- ce qui reste permis ------------------------------------------------------
    def test_lectures_permises(self):
        for commande in (
                "grep -n 'statut' docs/decisions/*.md",
                "grep -rn R17 docs/ projets/ > /tmp/occurrences.txt",
                "cat docs/decisions/README.md",
                "cat projets/demo/cdc.md | head -20",
                "head -12 docs/systemes/S1-gestion-projet.md docs/CHANGELOG-REGLES.md",
                "tail -5 projets/demo/tickets/T-001-x.md",
                "sed -n '1,10p' docs/ARCHITECTURE.md",
                "wc -l docs/*.md 2>/dev/null",
                "python -c \"print(open('docs/VISION.md', encoding='utf-8').read()[:200])\"",
                "git diff -- docs/ARCHITECTURE.md",
                "git log --oneline -- projets/demo/cdc.md"):
            self.permet(commande)

    def test_autres_ecritures_permises(self):
        for commande in (
                "sed -i 's/a/b/' projets/demo/app/src/main.py",      # code : pas un document Markdown
                "echo x > /tmp/brouillon.md",                          # hors docs/ et projets/
                "python scripts/tableau.py",                           # générateur versionné (R9)
                "python scripts/console.py",
                "python scripts/test_restreindre_bash.py > /tmp/resultat.txt 2>&1",
                "python -m pytest projets/demo/app",
                "git commit -m \"R17 : sed -i et > docs/x.md refusés\"",
                "git commit -F - <<'EOF'\nR17 : echo x > docs/VISION.md est refusé\nEOF",
                "git commit -m \"$(cat <<'EOF'\nR17 : sed -i docs/x.md\nEOF\n)\""):
            self.permet(commande)

    def test_deploiement_toujours_confirme(self):
        code, dec = decision("python scripts/deployer_local.py --projet demo --sha abc1234")
        self.assertEqual((code, dec["permissionDecision"]), (0, "ask"))

    # -- rejeu de l'incident DEC-007 (2026-11-24) ----------------------------------
    def test_rejeu_incident_dec007(self):
        """Le coordinateur avait modifié DEC-007, VALIDÉ, par un script Python lancé par Bash ;
        proteger_valide.py (Write/Edit) ne l'avait pas vu. Le hook Bash le refuse désormais."""
        chemin = os.path.join(RACINE, *DEC_007.split("/"))
        with open(chemin, "rb") as f:
            avant = f.read()
        entete = avant.decode("utf-8").split("---")[1]
        self.assertRegex(entete, r"(?m)^statut:\s*VALIDÉ", "précondition : DEC-007 est VALIDÉ")
        rejeu = ("python - <<'EOF'\n"
                 "from pathlib import Path\n"
                 "p = Path('" + DEC_007 + "')\n"
                 "texte = p.read_text(encoding='utf-8')\n"
                 "texte = texte.replace('sauvegarde quotidienne', 'sauvegarde quotidienne et purge au déploiement')\n"
                 "p.write_text(texte, encoding='utf-8')\n"
                 "EOF")
        for commande in (rejeu,
                         "python -c \"import pathlib; p = pathlib.Path('" + DEC_007 + "'); "
                         "p.write_text(p.read_text(encoding='utf-8') + 'ajout')\"",
                         "sed -i 's/sauvegarde quotidienne/purge/' " + DEC_007):
            code, err = lancer(commande)                       # session principale, comme le 2026-11-24
            self.assertEqual(code, 2, commande)
            self.assertIn("Refusé (R17)", err)
            self.assertIn("proteger_valide.py", err)
        with open(chemin, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), hashlib.sha256(avant).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)
