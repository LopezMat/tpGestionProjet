#!/usr/bin/env python3
"""Tests de scripts/console.py (console de consultation, DEC-012). Responsable : D.

Lancement : python scripts/test_console.py   (Mac : python3 …) ; nécessite PyYAML (requirements.txt).
Toutes les données sont créées dans un dossier temporaire, avec les jeux de données de test_tableau.py
(réutilisés, pas recopiés) complétés par des agents, skills, décisions et documents. Date fixée au 2026-11-25.
"""
import hashlib
import html
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(ICI, "console.py")
DATE = "2026-11-25"

sys.dont_write_bytecode = True  # pas de __pycache__ dans scripts/


def _module(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


console = _module("console")
tt = _module("test_tableau")        # fixtures : creer_donnees, ecrire
tableau = console.tableau
ecrire = tt.ecrire


# ---------------------------------------------------------------------------- données de test

def creer_depot(racine):
    tt.creer_donnees(racine)
    ecrire(racine, "equipe/agents.md", """
    ---
    cout_horaire_eur: 15
    responsable: B
    maj_le: 2026-11-23
    agents:
      - nom: analyste-besoin
        systeme: S4
      - nom: dev-backend
        systeme: realisation
      - nom: dev-frontend
        systeme: realisation
      - nom: testeur
        systeme: S3
      - nom: gestionnaire-crise
        systeme: S2
    ---
    # Agents
    """)
    # Description avec « : » : en-tête lu par Claude Code, mais pas du YAML strict.
    ecrire(racine, ".claude/agents/testeur.md", """
    ---
    name: testeur
    description: Testeur (S3). À appeler par le coordinateur : quand un ticket est EN_REVUE.
    tools: Read, Glob, Bash
    model: sonnet
    ---

    # testeur

    ## Rôle
    Tu lances les **tests** et tu coches les critères.

    ## Quand s'arrêter et demander un humain
    - Une suite échoue sans explication.

    ## Choix du modèle : sonnet
    Raisons.
    """)
    ecrire(racine, ".claude/agents/agent-maison.md", """
    ---
    name: agent-maison
    description: Agent de test absent du catalogue.
    tools: Read
    model: haiku
    ---
    # agent-maison

    ## Rôle
    Rien.
    """)
    ecrire(racine, ".claude/skills/avancement/SKILL.md", """
    ---
    name: avancement
    description: Régénère les tableaux de bord.
    ---

    # avancement

    ## Quand l'utiliser
    Après chaque étape du pipeline.

    ## Point d'arrêt humain
    Aucun : synthèse seulement.
    """)
    ecrire(racine, "docs/decisions/2026-11-23-DEC-001-essai.md", """
    ---
    titre: Décision validée d'essai
    statut: VALIDÉ
    responsable: B
    version: 1.0
    maj_le: 2026-11-23
    valide_par: Ethan
    decision: DEC-001
    id: DEC-001
    date: 2026-11-23
    decide_par: équipe
    projet: ESN
    ticket:
    modifie_une_regle: oui
    ---
    # DEC-001 — Essai
    """)
    ecrire(racine, "docs/decisions/2026-11-25-DEC-002-en-revue.md", """
    ---
    titre: Décision en revue
    statut: EN_REVUE
    responsable: D
    version: 0.1
    maj_le: 2026-11-25
    valide_par:
    decision: DEC-002
    id: DEC-002
    date: 2026-11-25
    decide_par: Ethan
    projet: demo
    ticket: T-005
    modifie_une_regle: non
    ---
    # DEC-002 — En revue
    """)
    ecrire(racine, "docs/VISION.md", """
    # VISION

    ## 1. Contexte
    Notre produit est le **système multi-agents**.

    ---

    ## 2. Les systèmes

    ### Système 1 : la gestion de projet
    - Découper en tâches.

    ### Système 3 : le déploiement
    - Contrôler la sécurité.
    """)
    ecrire(racine, "docs/ARCHITECTURE.md", """
    ---
    titre: Architecture
    statut: VALIDÉ
    responsable: B
    version: 1.0
    maj_le: 2026-11-23
    valide_par: Ethan
    decision: DEC-001
    ---
    # ARCHITECTURE

    ## 5. Circuit des fichiers

    ```mermaid
    flowchart LR
      DEM["demande.md"] --> AB["analyste-besoin"]
    ```

    ## 6. Modèle de validation

    **Garde-fous** :

    | # | Garde-fou | Mécanisme |
    |---|---|---|
    | 1 | Personne ne passe `VALIDÉ` | hook `proteger_valide.py` |
    | 2 | Bash \\| filtré | hook |
    """)
    ecrire(racine, "CLAUDE.md", """
    # CLAUDE

    **Points d'arrêt humains obligatoires :**
    - le cahier des charges ;
    - la mise en production.

    **R8 · suite.**
    """)
    ecrire(racine, "docs/systemes/S1-gestion-projet.md", """
    ---
    titre: Système 1 — Gestion de projet
    statut: EN_REVUE
    responsable: B
    version: 0.1
    maj_le: 2026-11-23
    valide_par:
    decision:
    ---
    # S1
    Voir [l'architecture](../ARCHITECTURE.md#5-circuit-des-fichiers).
    """)
    ecrire(racine, "projets/demo/cdc.md", """
    ---
    titre: Cahier des charges démo
    statut: VALIDÉ
    responsable: agent:analyste-besoin
    version: 1.0
    maj_le: 2026-11-24
    valide_par: Ethan
    decision: DEC-001
    ---
    <!-- commentaire à ne pas afficher -->
    # Cahier des charges démo

    Voir [T-001](tickets/T-001-test.md), [S1](../../docs/systemes/S1-gestion-projet.md),
    [piège](javascript:alert(1)) et [site](https://example.org).

    <script>alert('x')</script>

    ```mermaid
    flowchart TD
      A --> B
    ```
    """)
    # Ticket illisible : tableau.py l'ignore (anomalie), la console l'affiche quand même.
    ecrire(racine, "projets/demo/tickets/T-013-casse.md", """
    ---
    id: T-013
    titre: [non fermé
    ---
    # T-013
    """)


def empreinte(racine):
    """{chemin relatif : sha256} de tous les fichiers hors de console/."""
    res = {}
    for dossier, sous, noms in os.walk(racine):
        rel = os.path.relpath(dossier, racine).replace("\\", "/")
        if rel == "console" or rel.startswith("console/"):
            continue
        for n in noms:
            with open(os.path.join(dossier, n), "rb") as f:
                res[(rel + "/" + n).lstrip("./")] = hashlib.sha256(f.read()).hexdigest()
    return res


def lancer(racine, *args):
    r = subprocess.run([sys.executable, "-B", SCRIPT, "--racine", racine, *args], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", errors="replace") + r.stderr.decode("utf-8", errors="replace")


def lire(racine, chemin):
    with open(os.path.join(racine, "console", *chemin.split("/")), encoding="utf-8") as f:
        return f.read()


def colonnes_kanban(page):
    """{statut : [ids]} lu dans le Kanban d'une fiche projet."""
    res = {}
    for bloc in page.split('<div class="k-col ')[1:]:
        statut = re.search(r'data-statut="([^"]+)"', bloc).group(1)
        res[statut] = re.findall(r'data-ticket="(T-\d+)"', bloc)
    return res


# ---------------------------------------------------------------------------- tests

class TestConsoleScript(unittest.TestCase):
    """La console générée sur un dépôt de test, comme par un membre de l'équipe."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.racine = cls._tmp.name
        creer_depot(cls.racine)
        # Page obsolète d'un ticket supprimé et fichier non HTML : seule la page disparaît.
        ecrire(cls.racine, "console/projets/demo/tickets/T-999-vieux.html", "<p>vieux</p>")
        ecrire(cls.racine, "console/notes.txt", "à garder")
        cls.avant = empreinte(cls.racine)
        cls.code, cls.sortie = lancer(cls.racine, "--date", DATE)
        cls.apres = empreinte(cls.racine)
        cls.equipe, cls.projets, _ = tableau.charger(cls.racine, tableau.en_date(DATE))
        cls.demo = next(p for p in cls.projets if p.slug == "demo")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_code_retour(self):
        self.assertEqual(self.code, 0, self.sortie)

    def test_pages_attendues(self):
        for page in ["index.html", "portefeuille.html", "equipe.html", "agents.html", "decisions.html", "style.css",
                     "projets/demo/index.html", "projets/demo/cdc.html", "projets/demo/projet.html",
                     "projets/demo/tickets/T-001-test.html", "projets/demo/tickets/T-013-casse.html",
                     "projets/vide/index.html", "agents/testeur.html", "skills/avancement.html",
                     "decisions/2026-11-23-DEC-001-essai.html", "docs/VISION.html", "docs/ARCHITECTURE.html",
                     "docs/CLAUDE.html", "docs/systemes/S1-gestion-projet.html", "assets/mermaid.min.js"]:
            self.assertTrue(os.path.isfile(os.path.join(self.racine, "console", *page.split("/"))), page)

    def test_lecture_seule(self):
        """Aucun fichier hors de console/ n'est créé, modifié ni supprimé (ni TABLEAU.md, ni PORTFOLIO.md)."""
        self.assertEqual(self.avant, self.apres)
        self.assertFalse(os.path.exists(os.path.join(self.racine, "PORTFOLIO.md")))
        self.assertFalse(os.path.exists(os.path.join(self.racine, "projets", "demo", "TABLEAU.md")))

    def test_pages_obsoletes_supprimees(self):
        self.assertFalse(os.path.exists(os.path.join(self.racine, "console", "projets", "demo", "tickets",
                                                     "T-999-vieux.html")))
        self.assertTrue(os.path.exists(os.path.join(self.racine, "console", "notes.txt")))

    def test_chiffres_de_tableau(self):
        """Les chiffres affichés sont ceux de tableau.py (fonctions réutilisées, pas recopiées)."""
        p = self.demo
        fiche = lire(self.racine, "projets/demo/index.html")
        porte = lire(self.racine, "portefeuille.html")
        for valeur in [tableau.fmt_pct(p.avancement), tableau.fmt_pct(p.part_budget), tableau.fmt_eur(p.projete),
                       tableau.libelle_fin(p), tableau.fmt_h(p.temps_restant)]:
            self.assertIn(html.escape(valeur), fiche, valeur)
        self.assertIn(html.escape(tableau.fmt_pct(p.avancement)), porte)
        self.assertTrue(p.alertes)
        for _, detail in p.alertes:
            self.assertIn(html.escape(detail), fiche, detail)
        for _, _, detail in tableau.alertes_equipe(self.equipe, tableau.en_date(DATE)):
            self.assertIn(html.escape(detail), porte)
            self.assertIn(html.escape(detail), lire(self.racine, "equipe.html"))

    def test_kanban(self):
        cols = colonnes_kanban(lire(self.racine, "projets/demo/index.html"))
        self.assertEqual(list(cols)[:7], tableau.STATUTS)
        for t in self.demo.tickets:
            self.assertIn(t.id, cols[t.statut], t.id)
        self.assertEqual(sum(len(v) for v in cols.values()), len(self.demo.tickets))

    def test_bloque_et_attente_humain(self):
        fiche = lire(self.racine, "projets/demo/index.html")
        porte = lire(self.racine, "portefeuille.html")
        for texte in ["attente de l&#x27;API T-002", "validation humaine du budget et des délais"]:
            self.assertIn(texte, fiche)
            self.assertIn(texte, porte)

    def test_gantt_mermaid_local(self):
        fiche = lire(self.racine, "projets/demo/index.html")
        self.assertRegex(fiche, r'<pre class="mermaid">gantt')
        self.assertIn('src="../../assets/mermaid.min.js"', fiche)
        with open(os.path.join(self.racine, "console", "assets", "mermaid.min.js"), "rb") as f, \
                open(console.MERMAID_LOCAL, "rb") as g:
            self.assertEqual(f.read(), g.read())

    def test_gantt_couleurs_par_statut(self):
        """done = TERMINE, active = EN_COURS et EN_REVUE, crit = BLOQUE et ATTENTE_HUMAIN, rien sinon."""
        fiche = lire(self.racine, "projets/demo/index.html")
        source = html.unescape(re.search(r'<pre class="mermaid">(gantt.*?)</pre>', fiche, re.S).group(1))
        attendus = {"T-001": "done, ", "T-002": "active, ", "T-009": "active, ", "T-004": "crit, ",
                    "T-005": "crit, ", "T-003": "", "T-006": ""}       # T-006 : critique mais A_FAIRE
        for tid, marqueur in attendus.items():
            self.assertRegex(source, r"(?m)^\s+{} [^\n]* :{}{}, ".format(tid, marqueur, tid.lower().replace("-", "")),
                             tid)
        self.assertIn('class="legende-gantt"', fiche)
        for libelle in ["Terminé", "En cours ou en revue", "Bloqué ou en attente", "À faire"]:
            self.assertIn(libelle, fiche.split('class="legende-gantt"')[1].split("</ul>")[0])

    def test_gantt_de_tableau_inchange(self):
        """La couleur par statut est propre à la console : tableau.gantt (donc TABLEAU.md) garde ses marqueurs."""
        ligne = next(l for l in tableau.gantt(self.demo) if l.strip().startswith("T-006 "))
        self.assertIn(":crit, t006", ligne)

    def test_circuit_plein_ecran(self):
        index = lire(self.racine, "index.html")
        self.assertIn('href="circuit.html"', index)
        self.assertIn("Ouvrir le schéma en plein écran", index)
        self.assertIn("useMaxWidth: false", index)                 # taille réelle dans la page
        page = lire(self.racine, "circuit.html")
        self.assertIn('<pre class="mermaid">flowchart LR', page)
        self.assertNotIn('class="nav"', page)                      # rien d'autre que le diagramme
        self.assertNotIn("<h1", page)
        self.assertNotIn("useMaxWidth: false", page)               # ajusté à l'écran
        self.assertIn('src="assets/mermaid.min.js"', page)

    def test_ticket_rendu(self):
        page = lire(self.racine, "projets/demo/tickets/T-009-test.html")
        self.assertIn("Liste des salles", page)
        self.assertIn('href="T-002-test.html"', page)        # dépendance liée
        self.assertIn('class="tache"', page)                   # case à cocher
        casse = lire(self.racine, "projets/demo/tickets/T-013-casse.html")
        self.assertIn("YAML invalide", casse)

    def test_document_rendu_et_liens(self):
        page = lire(self.racine, "projets/demo/cdc.html")
        self.assertIn("VALIDÉ", page)
        self.assertNotIn("commentaire à ne pas afficher", page)
        self.assertIn('href="tickets/T-001-test.html"', page)
        self.assertIn('href="../../docs/systemes/S1-gestion-projet.html"', page)
        self.assertIn('href="https://example.org"', page)
        self.assertNotIn('href="javascript', page)
        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn('<pre class="mermaid">flowchart TD', page)
        s1 = lire(self.racine, "docs/systemes/S1-gestion-projet.html")
        self.assertIn('href="../ARCHITECTURE.html#5-circuit-des-fichiers"', s1)
        self.assertIn('id="5-circuit-des-fichiers"', lire(self.racine, "docs/ARCHITECTURE.html"))

    def test_notre_systeme(self):
        page = lire(self.racine, "index.html")
        self.assertIn('class="actif" aria-current="page">Notre système', page)
        self.assertIn("système multi-agents", page)                                    # vision
        self.assertRegex(page, r'<div class="stat-val">2</div><div class="stat-lib">agents IA')
        self.assertRegex(page, r'<div class="stat-val">1</div><div class="stat-lib">skills')
        self.assertRegex(page, r'<div class="stat-val">2</div><div class="stat-lib">décisions')
        self.assertIn('href="docs/systemes/S1-gestion-projet.html"', page)
        self.assertIn('<pre class="mermaid">flowchart LR', page)                        # circuit
        self.assertIn('src="assets/mermaid.min.js"', page)
        self.assertIn("la mise en production", page)                                     # points d'arrêt
        self.assertIn("proteger_valide.py", page)                                        # garde-fous
        self.assertIn("Bash | filtré", page)

    def test_agents_par_systeme(self):
        page = lire(self.racine, "agents.html")
        s3 = page.split('id="sys-s3"')[1].split("</section>")[0]
        self.assertIn('id="agent-testeur"', s3)
        autres = page.split('id="sys-autres"')[1].split("</section>")[0]
        self.assertIn('id="agent-agent-maison"', autres)
        carte = page.split('id="agent-testeur"')[1].split("</article>")[0]
        for attendu in ["Bash", "modèle sonnet", "Une suite échoue", html.escape(console.PHRASES["testeur"]),
                        "<strong>tests</strong>", "À appeler par le coordinateur : quand"]:
            self.assertIn(attendu, carte)
        maison = page.split('id="agent-agent-maison"')[1].split("</article>")[0]
        self.assertIn("Phrase générique", maison)
        skill = page.split('id="skill-avancement"')[1].split("</article>")[0]
        self.assertIn("Après chaque étape", skill)
        self.assertIn(html.escape(console.PHRASES["avancement"]), skill)

    def test_decisions(self):
        page = lire(self.racine, "decisions.html")
        self.assertIn('href="decisions/2026-11-25-DEC-002-en-revue.html"', page)
        ligne = page.split("DEC-002</a>")[1].split("</tr>")[0]
        self.assertIn("EN REVUE", ligne)
        self.assertIn("aucune anomalie", page)

    def test_equipe(self):
        page = lire(self.racine, "equipe.html")
        self.assertIn('id="membre-hugo"', page)
        self.assertIn("EV-001", page)
        self.assertNotIn("EV-002", page)          # événement annulé


class TestConsoleOptions(unittest.TestCase):

    def test_mermaid_src(self):
        with tempfile.TemporaryDirectory() as racine:
            creer_depot(racine)
            code, sortie = lancer(racine, "--date", DATE, "--mermaid-src", "https://cdn.example/mermaid.js")
            self.assertEqual(code, 0, sortie)
            self.assertIn('src="https://cdn.example/mermaid.js"', lire(racine, "projets/demo/index.html"))
            self.assertFalse(os.path.exists(os.path.join(racine, "console", "assets", "mermaid.min.js")))

    def test_depot_vide(self):
        with tempfile.TemporaryDirectory() as racine:
            code, sortie = lancer(racine, "--date", DATE)
            self.assertEqual(code, 0, sortie)
            self.assertIn("Aucun projet", lire(racine, "portefeuille.html"))
            self.assertEqual(sorted(os.listdir(racine)), ["console"])

    def test_date_invalide(self):
        with tempfile.TemporaryDirectory() as racine:
            code, _ = lancer(racine, "--date", "25/11/2026")
            self.assertEqual(code, 2)
            self.assertEqual(os.listdir(racine), [])


class TestEcritureBornee(unittest.TestCase):

    def test_refuse_hors_console(self):
        with tempfile.TemporaryDirectory() as racine:
            site = console.Site(racine, tableau.en_date(DATE))
            for chemin in ["../x.html", "../../x.html", "a/../../x.html", ""]:
                with self.assertRaises(ValueError, msg=chemin):
                    site.ecrire(chemin, "x")
            site.ecrire("a/b.html", "ok")
            self.assertTrue(os.path.isfile(os.path.join(racine, "console", "a", "b.html")))
            self.assertEqual(os.listdir(racine), ["console"])


class TestMarkdown(unittest.TestCase):

    def conv(self, texte, resoudre=None):
        return console.Markdown(resoudre).convertir(texte)

    def test_titres_et_ancres(self):
        h = self.conv("## 6. Événements d'équipe\n## Bis\n## Bis")
        self.assertIn('<h2 id="6-événements-déquipe">', h)
        self.assertIn('id="bis-1"', h)

    def test_tableau(self):
        h = self.conv("| A | B |\n|---|---|\n| `x\\|y` | **gras** |")
        self.assertIn("<th>A</th>", h)
        self.assertIn("<code>x|y</code>", h)
        self.assertIn("<strong>gras</strong>", h)

    def test_listes_imbriquees_et_cases(self):
        h = self.conv("- un\n  - deux\n- [x] fait\n- [ ] à faire\n\n1. premier\n2. second")
        self.assertIn("<ul><li>un<ul><li>deux</li></ul></li>", h)
        self.assertIn('<li class="tache faite">', h)
        self.assertIn('<li class="tache">', h)
        self.assertIn("<ol><li>premier</li><li>second</li></ol>", h)

    def test_code_mermaid_citation(self):
        h = self.conv("```python\nx = '<b>'\n```\n```mermaid\nA-->B\n```\n> *cité*\n\n---")
        self.assertIn("<pre class=\"code\"><code>x = &#x27;&lt;b&gt;&#x27;</code></pre>", h)
        self.assertIn('<pre class="mermaid">A--&gt;B</pre>', h)
        self.assertIn("<blockquote><p><em>cité</em></p></blockquote>", h)
        self.assertIn("<hr>", h)

    def test_echappement_et_liens(self):
        h = self.conv('<img src=x onerror="alert(1)"> [a](javascript:alert(1)) [b](https://x.org) <br>')
        self.assertNotIn("<img", h)
        self.assertNotIn('href="javascript', h)
        self.assertIn('href="https://x.org"', h)
        self.assertIn("<br>", h)

    def test_section_et_sans_hr(self):
        corps = "# T\n## 1. A\ntexte\n\n---\n\n## 2. B\nautre"
        self.assertEqual(console.section(corps, r"^1\."), "texte")
        self.assertEqual(console.section(corps, r"^3\."), "")

    def test_entete_tolerant(self):
        fm, corps, err = console.entete_tolerant("---\nname: x\ndescription: a : b\n---\ncorps")
        self.assertEqual(fm["description"], "a : b")
        self.assertEqual(corps, "corps")


if __name__ == "__main__":
    unittest.main(verbosity=1)
