#!/usr/bin/env python3
"""Tests de scripts/bureau.py et de la page « Le bureau » de la console (DEC-016). Responsable : D.

Lancement : python scripts/test_bureau.py   (Mac : python3 …) ; nécessite PyYAML (requirements.txt).
Les données sont créées dans un dossier temporaire avec les jeux de données de test_console.py et
test_tableau.py (réutilisés, pas recopiés), complétés par un ticket piégé (échappement) et un journal
volontairement mal formé. Date fixée au 2026-11-25. Le test de syntaxe JavaScript utilise `node` s'il est
installé (sinon il est ignoré).
"""
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True  # pas de __pycache__ dans scripts/


def _module(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tc = _module("test_console")       # fixtures : creer_depot, empreinte, lancer, lire
console = tc.console
bureau = console.bureau
ecrire = tc.ecrire
DATE = tc.DATE

PIEGE = "</script><img src=x onerror=alert(1)>"
PIEGE_BLOQUE = "attente de lea <!-- & </script>  "

JOURNAL_MIXTE = """\
---
id: T-001
---
# T-001

## Description
- 2026-11-20 08:00 · agent:dev-backend · ligne hors journal · 1 h

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps -->
- 2026-11-24 14:00 · agent:dev-backend · passage EN_COURS · 2 h
- 2026-11-24 · salarie:ethan · décision prise (DEC-005) · 0 h
- 2026-11-23 09:00 · agent:analyste-besoin · étape A · étape B · 1,5 h
- 2026-11-25 13:30 · agent:dev-backend · livré pour revue · 4.2 h. Fichiers : a, b
- 2026-11-25 17:00 · agent:testeur · vérification · temps compté dans T-041
- 2026-11-25 déplacé vers les règles de l'ESN
- 2026-13-40 · agent:testeur · date impossible · 1 h
- 2026-11-25 25:00 · agent:testeur · heure impossible · 1 h
- 2026-11-25 10:00 · agent:testeur
- 2026-11-25 10:00 ·  ·  · 1 h
- 2026-11-25 10:00 · agent:testeur · 2 h
- décision prise (DEC-007)
texte libre sans puce, ignoré

## Autre
- 2026-11-26 10:00 · agent:dev-backend · hors section · 1 h
"""


def ticket_piege():
    return """
    ---
    id: T-020
    titre: "{t}"
    projet: demo
    type: tache
    statut: ATTENTE_HUMAIN
    priorite: normale
    assigne: agent:testeur
    estimation_h: 1
    temps_passe_h: 0
    depend_de: []
    bloque_par: "{b}"
    validation_humaine_requise: non
    decision:
    cree_par: agent:coordinateur
    cree_le: 2026-11-18
    maj_le: 2026-11-24
    ---
    # T-020 — piège

    ## Journal
    - 2026-11-18 09:00 · agent:testeur · création · 0 h
    - 2026-11-19 10:00 · coordinateur pour agent:testeur · {t} & co suite · 0,5 h
    - 2026-11-19 · salarie:karim (Ethan) · avis donné · 0 h
    - 2026-11-19 11:00 · agent:inconnu · essai · 0 h
    - 2026-11-19 12:00 · agent:testeur · passage ATTENTE_HUMAIN · 0 h
    - 2026-11-19 sans séparateur
    """.format(t=PIEGE.replace('"', '\\"'), b=PIEGE_BLOQUE.replace(" ", "\\u2029"))


def extraire_json(page):
    m = re.search(r'<script type="application/json" id="donnees-bureau">(.*?)</script>', page, re.S)
    return m.group(1)


# ---------------------------------------------------------------------------- unitaires

class TestJournal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.entrees, cls.anomalies = bureau.analyser_journal(JOURNAL_MIXTE, "T-001.md")
        cls.par_quoi = {e["quoi"]: e for e in cls.entrees}

    def test_lignes_valides(self):
        e = self.par_quoi["passage EN_COURS"]
        self.assertEqual((e["date"].isoformat(), e["heure"], e["qui"], e["temps"]),
                         ("2026-11-24", "14:00", "agent:dev-backend", 2.0))

    def test_sans_heure(self):
        e = self.par_quoi["décision prise (DEC-005)"]
        self.assertIsNone(e["heure"])
        self.assertEqual(e["qui"], "salarie:ethan")

    def test_point_median_dans_le_texte(self):
        e = self.par_quoi["étape A · étape B"]
        self.assertEqual(e["temps"], 1.5)

    def test_texte_apres_le_temps(self):
        e = self.par_quoi["livré pour revue · Fichiers : a, b"]
        self.assertEqual(e["temps"], 4.2)

    def test_temps_absent(self):
        e = self.par_quoi["vérification · temps compté dans T-041"]
        self.assertIsNone(e["temps"])

    def test_heure_invalide_gardee_sans_heure(self):
        self.assertIsNone(self.par_quoi["heure impossible"]["heure"])
        self.assertTrue(any("heure invalide 25:00" in a for a in self.anomalies))

    def test_lignes_mal_formees_signalees(self):
        attendus = ["ligne 16 du journal mal formée", "ligne 17 du journal, date invalide 2026-13-40",
                    "ligne 19 du journal incomplète", "ligne 20 du journal incomplète", "ligne 21 du journal incomplète",
                    "ligne 22 du journal sans date"]
        for a in attendus:
            self.assertTrue(any(a in x for x in self.anomalies), a)
        self.assertEqual(len(self.entrees), 6)

    def test_seule_la_section_journal(self):
        self.assertNotIn("ligne hors journal", self.par_quoi)
        self.assertNotIn("hors section", self.par_quoi)

    def test_jamais_d_exception(self):
        for texte in ["", "## Journal", "## Journal\n-", "## Journal\n- 2026-11-24", "## Journal\n- 2026-11-24 ·",
                      "## Journal\n- 9999-99-99 · · · ·", "## Journal\n```\n- 2026-11-24 · a · b\n", None,
                      "## Journal\n- 2026-11-24 99:99 · ·   · h"]:
            bureau.analyser_journal(texte, "x")

    def test_classer(self):
        self.assertEqual(bureau.classer("création"), ("creation", None))
        self.assertEqual(bureau.classer("passage EN_REVUE (jamais TERMINE)"), ("statut", "EN_REVUE"))
        self.assertEqual(bureau.classer("8/8 critères → TERMINE"), ("statut", "TERMINE"))
        self.assertEqual(bureau.classer("passé à `BLOQUE` faute d'API"), ("statut", "BLOQUE"))
        self.assertEqual(bureau.classer("ticket laissé EN_REVUE"), ("travail", None))
        self.assertEqual(bureau.classer("rédaction"), ("travail", None))


class TestEtats(unittest.TestCase):
    persos = {"agent:relecteur-code": {}, "agent:testeur": {}, "agent:dev-backend": {}}
    salaries = {"karim": "karim", "lea": "lea", "claire": "Claire"}

    def test_statut_vers_etat(self):
        attendus = {"A_FAIRE": "cafe", "EN_COURS": "tape", "EN_REVUE": "revue", "BLOQUE": "bloque",
                    "ATTENTE_HUMAIN": "attente", "TERMINE": "cafe", "ANNULE": "cafe", "": "cafe", "INCONNU": "cafe"}
        for statut, etat in attendus.items():
            self.assertEqual(bureau.etat_statut(statut), etat, statut)
        self.assertEqual(set(bureau.ETAT_PAR_STATUT) | {"A_FAIRE", "TERMINE", "ANNULE"}, set(console.tableau.STATUTS))

    def contrib(self, statut, assigne, approuve=False, bloque_par=""):
        return bureau.contributions(statut, assigne, approuve, bloque_par, self.persos, self.salaries)

    def test_en_revue_relecteur_puis_testeur(self):
        self.assertEqual(self.contrib("EN_REVUE", "agent:dev-backend"),
                         [("agent:dev-backend", "revue", "agent:relecteur-code")])
        self.assertEqual(self.contrib("EN_REVUE", "agent:dev-backend", approuve=True),
                         [("agent:dev-backend", "revue", "agent:testeur")])
        self.assertEqual(self.contrib("EN_REVUE", "agent:relecteur-code"), [("agent:relecteur-code", "revue", None)])
        self.assertEqual(bureau.contributions("EN_REVUE", "agent:dev-backend", False, "", {}, {}),
                         [("agent:dev-backend", "revue", None)])          # relecteur absent : reste à son poste

    def test_attente_humain(self):
        self.assertEqual(self.contrib("ATTENTE_HUMAIN", "salarie:karim"), [("salarie:karim", "attente", None)])
        self.assertEqual(self.contrib("ATTENTE_HUMAIN", "agent:dev-backend", bloque_par="avis de Claire puis Léa"),
                         [("salarie:claire", "attente", None), ("agent:dev-backend", "attend", None)])
        self.assertEqual(self.contrib("ATTENTE_HUMAIN", "agent:dev-backend", bloque_par="validation du budget"),
                         [("visiteur:equipe", "attente", None), ("agent:dev-backend", "attend", None)])
        # un prénom inclus dans un mot (« Claireval ») ne compte pas
        self.assertEqual(bureau.humain_attendu("agent:x", "voir Claireval", self.salaries), "visiteur:equipe")

    def test_autres_statuts(self):
        self.assertEqual(self.contrib("BLOQUE", "agent:dev-backend"), [("agent:dev-backend", "bloque", None)])
        self.assertEqual(self.contrib("EN_COURS", "agent:dev-backend"), [("agent:dev-backend", "tape", None)])
        for statut in ("A_FAIRE", "TERMINE", "ANNULE", "?"):
            self.assertEqual(self.contrib(statut, "agent:dev-backend"), [])
        self.assertEqual(self.contrib("EN_COURS", None), [])

    def test_revue_approuvee(self):
        modele = "## Revue\n- **Avis relecteur-code** : <APPROUVÉ | CHANGEMENTS_DEMANDÉS>\n- **Revue humaine requise** : oui"
        self.assertFalse(bureau.revue_approuvee(modele))
        self.assertTrue(bureau.revue_approuvee("## Revue\n- **Avis relecteur-code** : APPROUVÉ (2026-11-25)"))
        self.assertFalse(bureau.revue_approuvee("## Revue\n- Avis : APPROUVÉ\n- Avis : CHANGEMENTS_DEMANDÉS"))
        self.assertTrue(bureau.revue_approuvee("## Revue\n- Avis : CHANGEMENTS_DEMANDÉS\n- Avis : APPROUVE"))
        self.assertFalse(bureau.revue_approuvee("## Description\n- Avis : APPROUVÉ"))


class TestPlan(unittest.TestCase):

    def persos(self, specs):
        return [{"id": i, "nature": n, "systeme": s} for i, n, s in specs]

    def verifier(self, persos):
        plan = bureau.construire_plan(persos)
        pieces = {p["id"]: p for p in plan["pieces"]}
        postes = {p["id"]: p for p in plan["postes"]}
        self.assertEqual(len(postes), len(persos))
        positions = [(p["x"], p["y"]) for p in plan["postes"]]
        self.assertEqual(len(positions), len(set(positions)), "deux postes au même endroit")
        for p in plan["postes"]:
            pc = pieces[p["piece"]]
            self.assertTrue(pc["x"] <= p["x"] < pc["x"] + pc["l"] and pc["y"] <= p["y"] < pc["y"] + pc["h"], p)
            self.assertTrue(0 <= p["x"] < plan["largeur"] and 0 <= p["y"] < plan["hauteur"])
        self.assertGreaterEqual(len(plan["cafe"]), len(persos))
        return plan, {p["id"]: postes[p["poste"]] for p in persos}

    def test_accessoires(self):
        self.assertEqual(bureau.accessoire("testeur"), "coche")
        self.assertEqual(bureau.accessoire("agent-nouveau", "Auditeur de sécurité"), "bouclier")   # mots-clés
        self.assertEqual(bureau.accessoire("x", "Lead développeur, architecte"), "plans")
        self.assertEqual(bureau.accessoire("x", "rien de connu"), "tasse")

    def test_piece_par_systeme_et_debordement(self):
        specs = [("coordinateur", "coordinateur", "coordinateur")]
        specs += [("agent:s3-{}".format(i), "agent", "S3") for i in range(7)]
        specs += [("agent:dev", "agent", "realisation"), ("agent:maison", "agent", "autres"),
                  ("agent:chef", "agent", "S1"), ("salarie:lea", "salarie", "salarie"),
                  ("visiteur:ethan", "visiteur", "visiteur")]
        _, poste = self.verifier(self.persos(specs))
        dans_s3 = [i for i in range(7) if poste["agent:s3-{}".format(i)]["piece"] == "s3"]
        self.assertEqual(len(dans_s3), 6)
        self.assertEqual(poste["agent:s3-6"]["piece"], "realisation")    # débordement
        self.assertEqual(poste["agent:maison"]["piece"], "realisation")  # hors catalogue : annexe
        self.assertEqual(poste["agent:chef"]["piece"], "s1")
        self.assertEqual(poste["salarie:lea"]["piece"], "salaries")
        self.assertEqual(poste["visiteur:ethan"]["piece"], "couloir")
        self.assertEqual(poste["coordinateur"]["piece"], "couloir")

    def test_beaucoup_de_personnages(self):
        specs = [("agent:a{}".format(i), "agent", "S2") for i in range(40)]
        specs += [("salarie:s{}".format(i), "salarie", "salarie") for i in range(15)]
        self.verifier(self.persos(specs))


class TestJsonPourScript(unittest.TestCase):

    def test_echappement(self):
        donnees = {"t": PIEGE + " <!-- & >    é", "l": ["</SCRIPT>"]}
        texte = bureau.json_pour_script(donnees)
        for interdit in ("<", ">", "&", " ", " "):
            self.assertNotIn(interdit, texte)
        self.assertEqual(json.loads(texte), donnees)
        self.assertIn("é", texte)     # le reste du texte n'est pas converti


# ---------------------------------------------------------------------------- génération

class TestBureauGeneration(unittest.TestCase):
    """La page générée par console.py sur un dépôt de test, comme par un membre de l'équipe."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.racine = cls._tmp.name
        tc.creer_depot(cls.racine)
        ecrire(cls.racine, "projets/demo/tickets/T-020-piege.md", ticket_piege())
        cls.avant = tc.empreinte(cls.racine)
        cls.code, cls.sortie = tc.lancer(cls.racine, "--date", DATE)
        cls.apres = tc.empreinte(cls.racine)
        cls.page = tc.lire(cls.racine, "bureau.html")
        cls.json_brut = extraire_json(cls.page)
        cls.d = json.loads(cls.json_brut)
        cls.persos = {p["id"]: p for p in cls.d["personnages"]}
        cls.projets = {p["slug"]: p for p in cls.d["projets"]}
        cls.postes = {p["id"]: p for p in cls.d["plan"]["postes"]}

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def etat(self, slug, perso):
        return next((i for i in self.projets[slug]["instantane"] if i["perso"] == perso), None)

    def test_code_retour_et_fichiers(self):
        self.assertEqual(self.code, 0, self.sortie)
        with open(os.path.join(self.racine, "console", "assets", "bureau.js"), "rb") as f, \
                open(bureau.SCRIPT_JS, "rb") as g:
            self.assertEqual(f.read(), g.read())
        self.assertIn('<script src="assets/bureau.js"></script>', self.page)

    def test_navigation(self):
        for page in ("index.html", "equipe.html", "projets/demo/index.html", "agents/testeur.html"):
            self.assertIn(">Le bureau</a>", tc.lire(self.racine, page), page)
        self.assertIn('class="actif" aria-current="page">Le bureau', self.page)
        self.assertIn('href="../../bureau.html#projet=demo"', tc.lire(self.racine, "projets/demo/index.html"))

    def test_lecture_seule(self):
        self.assertEqual(self.avant, self.apres)
        for dossier, sous, _ in os.walk(self.racine):
            self.assertNotIn("__pycache__", sous, dossier)

    def test_personnages(self):
        self.assertIn("coordinateur", self.persos)
        self.assertEqual(self.persos["agent:testeur"]["systeme"], "S3")
        self.assertEqual(self.persos["agent:testeur"]["modele"], "sonnet")
        self.assertEqual(self.persos["agent:testeur"]["outils"], ["Read", "Glob", "Bash"])
        self.assertEqual(self.persos["agent:testeur"]["page"], "agents/testeur.html")
        maison = self.persos["agent:agent-maison"]                  # absent d'equipe/agents.md
        self.assertEqual((maison["systeme"], maison["accessoire"]), ("autres", "coche"))  # « test » dans sa description
        self.assertEqual(self.persos["agent:dev-backend"]["nature"], "agent")    # au catalogue, sans fichier
        self.assertTrue(any("dev-backend au catalogue sans fichier" in a for a in self.d["anomalies"]))
        self.assertEqual(self.postes[maison["poste"]]["piece"], "realisation")
        self.assertEqual(self.persos["salarie:karim"]["page"], "equipe.html#membre-karim")
        for v in ("visiteur:ethan", "visiteur:equipe", "visiteur:inconnu"):
            self.assertIn(v, self.persos)

    def test_instantane_demo(self):
        self.assertEqual(self.etat("demo", "agent:dev-backend")["etat"], "tape")           # T-002 EN_COURS
        front = self.etat("demo", "agent:dev-frontend")                                    # T-004 BLOQUE, T-009 EN_REVUE
        self.assertEqual(front["etat"], "bloque")
        self.assertEqual({t["id"] for t in front["tickets"]}, {"T-004", "T-009"})
        self.assertEqual(self.etat("demo", "salarie:karim")["etat"], "attente")            # T-005 assigné à Karim
        self.assertEqual(self.etat("demo", "salarie:lea")["etat"], "attente")              # T-020 : Léa citée
        self.assertEqual(self.etat("demo", "agent:testeur")["etat"], "attend")
        self.assertIsNone(self.etat("demo", "agent:analyste-besoin"))                       # T-001 TERMINE : café
        self.assertIn(bureau.ESN, self.projets)
        self.assertEqual(self.projets[bureau.ESN]["libelle"], "Toute l'ESN")

    def test_evenements(self):
        evs = self.d["evenements"]
        self.assertEqual([e["n"] for e in evs], list(range(len(evs))))
        cles = [(e["date"], e["heure"]) for e in evs]
        self.assertEqual(cles, sorted(cles))
        piege = [e for e in evs if e["ticket"] == "T-020"]
        self.assertEqual([e["perso"] for e in piege],
                         ["agent:testeur", "agent:testeur", "salarie:karim", "visiteur:inconnu", "agent:testeur"])
        karim = piege[2]
        self.assertEqual((karim["note"], karim["heure"], karim["estimee"]), ("saisi par Ethan", "10:00", True))
        self.assertEqual(piege[1]["note"], "saisi par le coordinateur")
        self.assertEqual((piege[-1]["type"], piege[-1]["statut"], piege[-1]["jalon"]), ("statut", "ATTENTE_HUMAIN", True))
        self.assertFalse(piege[1]["jalon"])
        dec = {e["dec"]: e for e in evs if e["type"] == "decision"}
        self.assertEqual((dec["DEC-002"]["projet"], dec["DEC-002"]["perso"], dec["DEC-002"]["ticket"]),
                         ("demo", "visiteur:ethan", "T-005"))
        self.assertTrue(dec["DEC-002"]["sans_heure"])
        self.assertEqual((dec["DEC-001"]["projet"], dec["DEC-001"]["perso"], dec["DEC-001"]["valide"]),
                         (bureau.ESN, "visiteur:equipe", True))
        self.assertTrue(any("T-020-piege.md : ligne" in a and "mal formée" in a for a in self.d["anomalies"]))
        self.assertTrue(any("agent:inconnu" in a for a in self.d["anomalies"]))
        self.assertEqual(self.page.count('<li class="ev '), len(evs))

    def test_echappement(self):
        for interdit in ("<", ">", "&", " ", " "):
            self.assertNotIn(interdit, self.json_brut)
        titres = {t["id"]: t["titre"] for p in self.d["projets"] for i in p["instantane"] for t in i["tickets"]}
        self.assertEqual(titres["T-020"], PIEGE)                                  # restitué à l'identique
        texte = next(e["texte"] for e in self.d["evenements"] if e["ticket"] == "T-020" and "co" in e["texte"])
        self.assertIn(PIEGE + " & co suite", texte)
        self.assertNotIn("<img", self.page)
        self.assertNotIn("<!--", self.page)
        self.assertEqual(self.page.count("</script>"), 2)                         # données + bureau.js
        self.assertIn(html.escape(PIEGE), self.page)                              # listes HTML échappées

    def test_aucune_ressource_externe(self):
        for attr in re.findall(r'(?:src|href)="([^"]*)"', self.page):
            self.assertNotRegex(attr, r"^(?:[a-z][a-z0-9+.-]*:|//)", attr)
        self.assertNotRegex(self.page, r"url\(|@import")
        with open(bureau.SCRIPT_JS, encoding="utf-8") as f:
            js = f.read()
        self.assertNotRegex(js, r"https?://|//cdn|\bfetch\(|XMLHttpRequest|\bimport\(")
        for motif in (r"\.innerHTML", r"\.outerHTML", r"insertAdjacentHTML", r"document\.write", r"\beval\(",
                      r"new Function"):
            self.assertNotRegex(js, motif)

    @unittest.skipUnless(shutil.which("node"), "node absent : syntaxe JavaScript non vérifiée")
    def test_syntaxe_js(self):
        r = subprocess.run(["node", "--check", bureau.SCRIPT_JS], capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))

    def test_listes_texte(self):
        self.assertEqual(self.page.count('class="b-etats"'), len(self.d["projets"]))
        self.assertIn('data-perso="agent:testeur"', self.page)
        self.assertIn('id="b-jalons" checked', self.page)               # jalons seulement, par défaut
        self.assertIn('aria-live="polite"', self.page)


class TestDepotVide(unittest.TestCase):

    def test_bureau_sans_projet(self):
        with tempfile.TemporaryDirectory() as racine:
            code, sortie = tc.lancer(racine, "--date", DATE)
            self.assertEqual(code, 0, sortie)
            d = json.loads(extraire_json(tc.lire(racine, "bureau.html")))
            self.assertEqual([p["slug"] for p in d["projets"]], [bureau.ESN])
            self.assertEqual([p["id"] for p in d["personnages"]], ["coordinateur"])
            self.assertEqual(d["evenements"], [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
