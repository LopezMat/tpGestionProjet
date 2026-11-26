#!/usr/bin/env python3
"""Tests de scripts/qui_fait_quoi.py (page « qui fait quoi », DEC-014). Responsable : D.

Lancement : python scripts/test_qui_fait_quoi.py   (macOS : python3 …). Bibliothèque standard uniquement.
Le projet de test est créé dans un dossier temporaire ; le script est lancé comme par un membre
de l'équipe (sous-processus). On vérifie :
- la génération (page complète, statuts lus dans les tickets, R9) ;
- la lecture seule : seul le fichier de sortie est créé, rien d'autre n'est créé, modifié ni supprimé ;
- l'échappement HTML : en-tête échappé, aucune donnée ne ferme la balise <script>, personnages
  échappés dans le modèle ;
- la sortie par défaut à la racine du dépôt, ignorée par Git.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE_DEPOT = os.path.dirname(ICI)
SCRIPT = os.path.join(ICI, "qui_fait_quoi.py")
MODELE = os.path.join(ICI, "qui_fait_quoi_modele.html")

sys.dont_write_bytecode = True  # pas de __pycache__ dans scripts/

CLIENT = "<b>Coworking & Cie</b>"
TITRE_PIEGE = '</script><script>alert("titre")</script> <!-- & fin'
NOM_PIEGE = '"><script>alert("nom")</script>'
QUOI_PIEGE = "<img src=x onerror=alert(1)>"


def ecrire(racine, chemin, texte):
    complet = os.path.join(racine, *chemin.split("/"))
    os.makedirs(os.path.dirname(complet), exist_ok=True)
    with open(complet, "w", encoding="utf-8", newline="\n") as f:
        f.write(textwrap.dedent(texte).lstrip("\n"))


def ticket(id_, titre, statut, assigne, est, passe):
    return """
    ---
    id: {id}
    titre: {titre}
    projet: demo
    type: fonctionnalite
    statut: {statut}            # commentaire ignoré
    priorite: normale
    assigne: {assigne}
    competence_requise: backend-python (confirme)
    estimation_h: {est}
    temps_passe_h: {passe}
    depend_de: []
    bloque_par:
    cree_le: 2026-11-24
    maj_le: 2026-11-25
    termine_le:
    ---
    <!-- modèle : templates/ticket.md v0.2 -->

    # {id} — {titre}

    ## Critères d'acceptation
    - [x] premier critère
    - [ ] second critère
    """.format(id=id_, titre=titre, statut=statut, assigne=assigne, est=est, passe=passe)


def creer_projet(racine):
    ecrire(racine, "projets/demo/projet.md", """
    ---
    titre: Fiche projet
    statut: EN_REVUE
    slug: demo
    client: {client}
    deadline: 2026-12-15
    ---
    # Fiche projet
    """.format(client=CLIENT))
    ecrire(racine, "projets/demo/TABLEAU.md", """
    <!-- FICHIER GÉNÉRÉ par scripts/tableau.py -->
    | Indicateur | Valeur |
    |---|---|
    | Budget consommé / prévu | 30,00 € / 100,00 € |
    | Fin projetée | 2026-12-01 |
    | Deadline | 2026-12-15 |
    | Coût projeté à terminaison (consommé + reste × taux) | 80,00 € |
    """)
    ecrire(racine, "projets/demo/tickets/T-001-socle.md", ticket("T-001", "Socle", "TERMINE", "agent:dev-backend", 4, 4))
    ecrire(racine, "projets/demo/tickets/T-002-piege.md",
           ticket("T-002", TITRE_PIEGE, "EN_COURS", "salarie:karim", 2, 0.5))
    instantane = {
        "_note": "instantané de test",
        "maintenant": [{"qui": "dev-backend", "ticket": "T-002", "quoi": "travaille"}],
        "a_vous": [{"qui": "Karim", "ticket": "T-002", "quoi": QUOI_PIEGE, "quand": "maintenant", "simple": "x"}],
        "recent": [],
        "etapes": ["Développement", "Revue de code", "Tests", "Terminé"],
        "increment": [{"id": "T-001", "titre": "Socle", "etape": 3, "note": ""},
                      {"id": "T-002", "titre": TITRE_PIEGE, "etape": 0, "note": ""}],
        "equipe": [{"qui": "dev-backend", "nom": NOM_PIEGE, "role": "code", "nature": "agent",
                    "haut": "#5b8def", "peau": "#f2c7a5", "cheveux": "#3b2a20", "outil": "portable"}],
    }
    ecrire(racine, "projets/demo/qui-fait-quoi.json", json.dumps(instantane, ensure_ascii=False, indent=2))


def empreinte(racine):
    """{chemin relatif : sha256} de tous les fichiers sous racine."""
    res = {}
    for dossier, _, noms in os.walk(racine):
        for n in noms:
            chemin = os.path.join(dossier, n)
            with open(chemin, "rb") as f:
                res[os.path.relpath(chemin, racine).replace("\\", "/")] = hashlib.sha256(f.read()).hexdigest()
    return res


def lancer(script, *args, cwd=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")  # messages accentués lisibles, même sous Windows
    r = subprocess.run([sys.executable, "-B", script, *args], capture_output=True, cwd=cwd, env=env)
    return r.returncode, r.stdout.decode("utf-8", errors="replace") + r.stderr.decode("utf-8", errors="replace")


def donnees(page):
    """Objet D de la page, relu comme le ferait le navigateur (JSON valide)."""
    m = re.search(r"^const D = (.*);$", page, re.M)
    return json.loads(m.group(1))


class TestQuiFaitQuoi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.racine = cls._tmp.name
        creer_projet(cls.racine)
        cls.sortie = os.path.join(cls.racine, "sortie", "page.html")
        os.makedirs(os.path.dirname(cls.sortie))
        cls.scripts_avant = sorted(os.listdir(ICI))
        cls.avant = empreinte(cls.racine)
        cls.code, cls.texte = lancer(SCRIPT, os.path.join(cls.racine, "projets", "demo"), cls.sortie)
        cls.apres = empreinte(cls.racine)
        cls.scripts_apres = sorted(os.listdir(ICI))
        with open(cls.sortie, encoding="utf-8") as f:
            cls.page = f.read()
        with open(MODELE, encoding="utf-8") as f:
            cls.modele = f.read()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    # -- génération ------------------------------------------------------------
    def test_generation(self):
        self.assertEqual(self.code, 0, self.texte)
        self.assertIn("2 tickets", self.texte)
        self.assertTrue(self.page.startswith("<!DOCTYPE html") or self.page.lower().startswith("<!doctype html"))
        self.assertNotRegex(self.page, r"\{\{[A-Z]+\}\}", "un champ du modèle n'a pas été remplacé")
        for chiffre in ("30,00 € / 100,00 €", "2026-12-01", "2026-12-15", "80,00 €"):
            self.assertIn(chiffre, self.page)

    def test_statuts_lus_dans_les_tickets(self):
        """R9 : les statuts viennent des tickets, pas de l'instantané."""
        d = donnees(self.page)
        par_id = {t["id"]: t for t in d["tickets"]}
        self.assertEqual(sorted(par_id), ["T-001", "T-002"])
        self.assertEqual(par_id["T-001"]["statut"], "TERMINE")
        self.assertEqual(par_id["T-002"]["statut"], "EN_COURS")
        self.assertEqual((par_id["T-002"]["qui"], par_id["T-002"]["nature"]), ("Karim", "salarie"))
        self.assertEqual((par_id["T-001"]["qui"], par_id["T-001"]["nature"]), ("dev-backend", "agent"))
        self.assertEqual(par_id["T-002"]["est"], 2.0)
        self.assertEqual(par_id["T-002"]["passe"], 0.5)
        self.assertEqual(d["a_vous"][0]["ticket"], "T-002")

    # -- lecture seule ---------------------------------------------------------
    def test_lecture_seule(self):
        """Seul le fichier de sortie apparaît ; aucun autre fichier n'est créé, modifié ni supprimé."""
        nouveaux = set(self.apres) - set(self.avant)
        self.assertEqual(nouveaux, {"sortie/page.html"})
        self.assertEqual({k: v for k, v in self.apres.items() if k in self.avant}, self.avant)

    def test_pas_de_trace_dans_scripts(self):
        self.assertEqual(self.scripts_avant, self.scripts_apres)

    def test_instantane_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            creer_projet(tmp)
            os.remove(os.path.join(tmp, "projets", "demo", "qui-fait-quoi.json"))
            sortie = os.path.join(tmp, "page.html")
            avant = empreinte(tmp)
            code, texte = lancer(SCRIPT, os.path.join(tmp, "projets", "demo"), sortie)
            self.assertNotEqual(code, 0)
            self.assertIn("Instantané absent", texte)
            self.assertEqual(empreinte(tmp), avant)

    # -- échappement HTML ------------------------------------------------------
    def test_echappement_entete(self):
        self.assertIn("&lt;b&gt;Coworking &amp; Cie&lt;/b&gt;", self.page)
        self.assertNotIn(CLIENT, self.page)

    def test_aucune_donnee_ne_ferme_la_balise_script(self):
        """Le JSON des données ne contient ni `<`, ni `>`, ni `&` bruts : pas de </script> ni de <!-- injectés."""
        for motif in ("</script", "<script", "<!--"):
            self.assertEqual(self.page.lower().count(motif), self.modele.lower().count(motif), motif)
        ligne = re.search(r"^const D = .*$", self.page, re.M).group(0)
        self.assertNotRegex(ligne[len("const D = "):], r"[<>&]")
        self.assertNotIn(QUOI_PIEGE, self.page)

    def test_donnees_intactes_apres_echappement(self):
        """L'échappement \\uXXXX garde un JSON valide : le navigateur relit les textes d'origine."""
        d = donnees(self.page)
        self.assertEqual({t["id"]: t["titre"] for t in d["tickets"]}["T-002"], TITRE_PIEGE)
        self.assertEqual(d["a_vous"][0]["quoi"], QUOI_PIEGE)
        self.assertEqual(d["equipe"][0]["nom"], NOM_PIEGE)

    def test_modele_echappe_les_personnages(self):
        """Les dessins SVG passent par innerHTML : nom et couleurs d'un personnage passent par attr()."""
        for fonction in ("debout", "auLit"):
            corps = re.search(r"function " + fonction + r"\((\w+)[^)]*\) \{\n(.*?)\n", self.modele)
            self.assertIsNotNone(corps, fonction)
            self.assertEqual(corps.group(1), "brut", fonction)
            self.assertIn("const p = perso(brut);", corps.group(2), fonction)
        self.assertIn("(attr(p.haut))", self.modele)
        perso = re.search(r"const perso = .*$", self.modele, re.M).group(0)
        for champ in ("nom", "haut", "peau", "cheveux"):
            self.assertIn("{}: attr(p.{})".format(champ, champ), perso)
        attr = re.search(r"const attr = .*$", self.modele, re.M).group(0)
        for entite in ("&amp;", "&lt;", "&gt;", "&quot;", "&#39;"):
            self.assertIn(entite, attr)

    def test_accolades_dans_les_donnees(self):
        """Une donnée qui contient « {{DONNEES}} » n'est pas remplacée une seconde fois."""
        with tempfile.TemporaryDirectory() as tmp:
            creer_projet(tmp)
            chemin = os.path.join(tmp, "projets", "demo", "projet.md")
            with open(chemin, encoding="utf-8") as f:
                texte = f.read().replace(CLIENT, "Client {{DONNEES}}")
            with open(chemin, "w", encoding="utf-8", newline="\n") as f:
                f.write(texte)
            sortie = os.path.join(tmp, "page.html")
            code, texte = lancer(SCRIPT, os.path.join(tmp, "projets", "demo"), sortie)
            self.assertEqual(code, 0, texte)
            with open(sortie, encoding="utf-8") as f:
                page = f.read()
            self.assertIn("Client {{DONNEES}}", page)
            self.assertEqual(len(re.findall(r"^const D = ", page, re.M)), 1)

    # -- sortie par défaut et Git ------------------------------------------------
    def test_sortie_par_defaut_a_la_racine(self):
        """Sans argument de sortie, la page va à la racine du dépôt, quel que soit le dossier courant."""
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "scripts"))
            shutil.copy(SCRIPT, os.path.join(tmp, "scripts"))
            shutil.copy(MODELE, os.path.join(tmp, "scripts"))
            creer_projet(tmp)
            code, texte = lancer(os.path.join(tmp, "scripts", "qui_fait_quoi.py"), "demo",
                                 cwd=os.path.join(tmp, "projets"))
            self.assertEqual(code, 0, texte)
            self.assertTrue(os.path.isfile(os.path.join(tmp, "qui-fait-quoi.html")))
            self.assertFalse(os.path.exists(os.path.join(tmp, "projets", "qui-fait-quoi.html")))

    def test_page_generee_hors_git(self):
        """DEC-014 : la page générée est ignorée par Git et n'est plus suivie ; le modèle reste suivi."""
        if shutil.which("git") is None or not os.path.isdir(os.path.join(RACINE_DEPOT, ".git")):
            self.skipTest("dépôt Git indisponible")

        def git(*args):
            return subprocess.run(["git", "-C", RACINE_DEPOT, *args], capture_output=True, text=True)

        self.assertEqual(git("check-ignore", "-q", "qui-fait-quoi.html").returncode, 0)
        self.assertEqual(git("ls-files", "--", "qui-fait-quoi.html").stdout.strip(), "")
        self.assertEqual(git("ls-files", "--", "scripts/qui_fait_quoi_modele.html").stdout.strip(),
                         "scripts/qui_fait_quoi_modele.html")


if __name__ == "__main__":
    unittest.main(verbosity=2)
