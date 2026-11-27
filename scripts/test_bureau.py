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
        # un ticket assigné à un membre humain de l'équipe projet l'attend lui-même (DEC-017)
        self.assertEqual(self.contrib("ATTENTE_HUMAIN", "humain:ethan"), [("humain:ethan", "attente", None)])

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
                  ("humain:ethan", "humain", "humain"), ("visiteur:prof", "visiteur", "visiteur")]
        _, poste = self.verifier(self.persos(specs))
        for pid in ("humain:ethan", "visiteur:prof"):                    # accueil, sans bureau
            self.assertEqual((poste[pid]["piece"], poste[pid]["y"], poste[pid]["bureau"]), ("couloir", 14, False))
        dans_s3 = [i for i in range(7) if poste["agent:s3-{}".format(i)]["piece"] == "s3"]
        self.assertEqual(len(dans_s3), 4)                                # capacité de S3 : 4 bureaux (DEC-027)
        self.assertEqual(poste["agent:s3-6"]["piece"], "realisation")    # débordement
        self.assertEqual(poste["agent:maison"]["piece"], "realisation")  # hors catalogue : annexe
        self.assertEqual(poste["agent:chef"]["piece"], "s1")
        self.assertEqual(poste["salarie:lea"]["piece"], "salaries")
        self.assertEqual(poste["coordinateur"]["piece"], "couloir")

    def test_beaucoup_de_personnages(self):
        specs = [("agent:a{}".format(i), "agent", "S2") for i in range(40)]
        specs += [("salarie:s{}".format(i), "salarie", "salarie") for i in range(15)]
        self.verifier(self.persos(specs))


# ---------------------------------------------------------------------------- DEC-027 : S3, halos, info-bulle

def rect_perso(x, y):
    """Sprite 16 × 24 px d'un personnage à la tuile (x, y) : pieds au bas de la tuile (formule du ticket T-025)."""
    return (x * 16, (y + 1) * 16 - 24, 16, 24)


def rect_bureau(x, y):
    return ((x - 0.5) * 16, (y - 1) * 16 + 3, 32, 12)


def chevauche(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


class VerifPlan:
    """Contrôles de non-chevauchement communs au catalogue réel et aux plans synthétiques."""

    def controler(self, plan, n_visiteurs=None):
        postes = plan["postes"]
        persos = [("poste " + p["id"], rect_perso(p["x"], p["y"])) for p in postes]
        bureaux = [("bureau " + p["id"], rect_bureau(p["x"], p["y"]), p["id"]) for p in postes if p["bureau"]]
        visiteurs = []
        for p in postes:
            for v in p.get("visites", []):
                visiteurs.append(("visite {} ({},{})".format(p["id"], v["x"], v["y"]), rect_perso(v["x"], v["y"])))
        for i, f in enumerate(plan["file"]):
            visiteurs.append(("file {} ({},{})".format(i, f["x"], f["y"]), rect_perso(f["x"], f["y"])))
        tous = persos + visiteurs
        for i, (na, ra) in enumerate(tous):
            for nb, rb in tous[i + 1:]:
                self.assertFalse(chevauche(ra, rb), "{} chevauche {}".format(na, nb))
        for nom, r in tous:
            for nb, rb, proprio in bureaux:
                if nom == "poste " + proprio:
                    continue                    # on est assis à son propre bureau
                self.assertFalse(chevauche(r, rb), "{} chevauche {}".format(nom, nb))
            self.assertTrue(0 <= r[0] and r[0] + r[2] <= plan["largeur"] * 16 and 0 <= r[1] and
                            r[1] + r[3] <= plan["hauteur"] * 16, nom)
        positions = [(v[0], v[1]) for v in
                     [(p["x"], p["y"], "poste") for p in postes] + [(q["x"], q["y"], "") for q in plan["file"]]
                     + [(q["x"], q["y"], "") for p in postes for q in p.get("visites", [])]]
        self.assertEqual(len(positions), len(set(positions)), "deux places identiques")
        return visiteurs


class TestPlanS3(unittest.TestCase, VerifPlan):

    def persos(self, specs):
        return [{"id": i, "nature": n, "systeme": s} for i, n, s in specs]

    def specs_s3(self, n_s3=4):
        noms = ["agent:relecteur-code", "agent:testeur", "agent:securite", "agent:deployeur", "agent:autre-s3"]
        specs = [("coordinateur", "coordinateur", "coordinateur")]
        specs += [("humain:" + h, "humain", "humain") for h in ("ethan", "johan", "stephane", "matthieu")]
        specs += [(n, "agent", "S3") for n in noms[:n_s3]]
        specs += [("agent:dev-backend", "agent", "realisation"), ("agent:dev-frontend", "agent", "realisation"),
                  ("agent:veilleur", "agent", "S2"), ("agent:analyste-besoin", "agent", "S4"),
                  ("salarie:lea", "salarie", "salarie"), ("visiteur:equipe", "visiteur", "visiteur")]
        return specs

    def test_grille_2x2_espacee(self):
        persos = self.persos(self.specs_s3())
        plan = bureau.construire_plan(persos)
        postes = {p["id"]: p for p in plan["postes"]}
        s3 = [postes[p["poste"]] for p in persos if p["id"].startswith("agent:") and postes[p["poste"]]["piece"] == "s3"]
        self.assertEqual(len(s3), 4)
        self.assertEqual(len({p["x"] for p in s3}), 2)
        self.assertEqual(len({p["y"] for p in s3}), 2)
        xs = sorted({p["x"] for p in s3})
        self.assertGreaterEqual(xs[1] - xs[0], 5)             # bureaux de 2 tuiles : de la place entre les colonnes
        self.verifier_aucun_doublon(s3)

    def verifier_aucun_doublon(self, postes):
        self.assertEqual(len({(p["x"], p["y"]) for p in postes}), len(postes))

    def test_cinquieme_agent_s3_deborde(self):
        persos = self.persos(self.specs_s3(5))
        plan = bureau.construire_plan(persos)
        postes = {p["id"]: p for p in plan["postes"]}
        self.assertEqual(sum(postes[p["poste"]]["piece"] == "s3" for p in persos if p["systeme"] == "S3"), 4)
        self.assertEqual(postes[persos[[p["id"] for p in persos].index("agent:autre-s3")]["poste"]]["piece"],
                         "realisation")
        self.controler(plan)

    def test_places_de_visite(self):
        persos = self.persos(self.specs_s3())
        plan = bureau.construire_plan(persos)
        postes = {p["id"]: p for p in plan["postes"]}
        relecteur = postes["p-agent-relecteur-code"]
        testeur = postes["p-agent-testeur"]
        for poste in (relecteur, testeur):
            self.assertGreaterEqual(len(poste["visites"]), 3)
            self.assertLessEqual(len(poste["visites"]), bureau.VISITES_MAX)
            for v in poste["visites"]:
                self.assertEqual(v["y"] // 11, 0, "place de visite hors de S3")     # S3 : y de 0 à 10
                self.assertTrue(36 <= v["x"] < 48)
        lieux = [(v["x"], v["y"]) for p in (relecteur, testeur) for v in p["visites"]]
        self.assertEqual(len(lieux), len(set(lieux)), "places de visite distinctes")
        self.assertNotIn("visites", postes["p-agent-securite"])                       # seulement relecteur et testeur
        self.assertNotIn("visites", postes["p-coordinateur"])
        self.controler(plan)

    def test_file_dans_le_couloir_devant_la_porte(self):
        persos = self.persos(self.specs_s3())
        plan = bureau.construire_plan(persos)
        piece = {p["id"]: p for p in plan["pieces"]}
        porte = piece["s3"]["porte"]["x"]
        self.assertGreaterEqual(len(plan["file"]), 4)
        for f in plan["file"]:
            self.assertEqual(f["y"], plan["rang_couloir"])
            self.assertNotIn(f["x"], (porte - 1, porte, porte + 1))                   # le passage reste libre
            self.assertNotEqual((f["x"], f["y"]), (24, 14))                           # ni le coordinateur
        self.assertLessEqual(abs(plan["file"][0]["x"] - porte), 3)                    # elle commence devant la porte

    def test_sans_chevauchement_beaucoup_de_monde(self):
        specs = self.specs_s3(5) + [("agent:x{}".format(i), "agent", "S2") for i in range(12)]
        specs += [("salarie:s{}".format(i), "salarie", "salarie") for i in range(6)]
        self.controler(bureau.construire_plan(self.persos(specs)))


class TestPlanCatalogueReel(unittest.TestCase, VerifPlan):
    """Le plan calculé sur le dépôt réel (agents, salariés et membres humains) en lecture seule."""

    @classmethod
    def setUpClass(cls):
        racine = os.path.dirname(ICI)
        site = console.Site(racine, console.tableau.en_date(DATE))
        # lecture seule : mêmes lectures que Site.generer(), sans en appeler l'écriture
        site.equipe, site.projets, site.anomalies = console.tableau.charger(site.racine, site.auj)
        site.inventaire()
        cls.donnees = bureau.Donnees(site).calculer()
        cls.plan = cls.donnees["plan"]
        cls.persos = {p["id"]: p for p in cls.donnees["personnages"]}
        cls.postes = {p["id"]: p for p in cls.plan["postes"]}

    def test_s3_du_catalogue(self):
        s3 = [p for p in self.donnees["personnages"] if p["nature"] == "agent" and p["systeme"] == "S3"]
        self.assertGreaterEqual(len(s3), 4)
        self.assertEqual(sum(self.postes[p["poste"]]["piece"] == "s3" for p in s3), 4)

    def test_quatre_visiteurs_sans_chevauchement(self):
        relecteur = self.postes[self.persos["agent:relecteur-code"]["poste"]]
        testeur = self.postes[self.persos["agent:testeur"]["poste"]]
        self.assertEqual((relecteur["piece"], testeur["piece"]), ("s3", "s3"))
        for poste in (relecteur, testeur):
            self.assertGreaterEqual(len(poste["visites"]) + len(self.plan["file"]), 4)
        # tous les visiteurs possibles à la fois (places de visite des deux postes, puis la file), pas seulement 4
        self.controler(self.plan)
        # 4 agents en revue chez le relecteur : ses places, puis la file
        places = [(v["x"], v["y"]) for v in relecteur["visites"]] + [(f["x"], f["y"]) for f in self.plan["file"]]
        rects = [rect_perso(x, y) for x, y in places[:4]]
        autres = [rect_perso(p["x"], p["y"]) for p in self.plan["postes"]]
        autres += [rect_bureau(p["x"], p["y"]) for p in self.plan["postes"] if p["bureau"]]
        for i, r in enumerate(rects):
            for o in autres:
                self.assertFalse(chevauche(r, o), r)
            for r2 in rects[i + 1:]:
                self.assertFalse(chevauche(r, r2))


class TestHalos(unittest.TestCase):

    def test_statut_vers_etat_vers_halo(self):
        attendus = {"EN_COURS": "travail", "BLOQUE": "bloque", "ATTENTE_HUMAIN": "attente", "EN_REVUE": None,
                    "A_FAIRE": None, "TERMINE": None, "ANNULE": None}
        self.assertEqual(set(attendus), set(console.tableau.STATUTS))
        for statut, halo in attendus.items():
            self.assertEqual(bureau.HALOS.get(bureau.etat_statut(statut)), halo, statut)

    def test_table(self):
        self.assertEqual(bureau.HALOS, {"tape": "travail", "bloque": "bloque", "attente": "attente",
                                        "attend": "attente"})
        self.assertNotIn("revue", bureau.HALOS)                    # EN_REVUE : pas de halo de travail
        self.assertNotIn("cafe", bureau.HALOS)
        self.assertEqual(len(set(bureau.HALOS.values())), 3)       # trois halos distincts

    def test_etats_des_personnages_connus(self):
        self.assertTrue(set(bureau.HALOS) <= set(bureau.LIBELLES_ETATS))


# ---------------------------------------------------------------------------- JSON

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

    def test_mode_direct_present_et_desactive_par_defaut(self):
        """DEC-018 : bouton Direct désactivé dans le HTML (file://), avec son explication ; zones masquées."""
        bouton = re.search(r'<button[^>]*id="b-mode-direct"[^>]*>', self.page)
        self.assertIsNotNone(bouton)
        self.assertIn(" disabled", bouton.group(0))
        self.assertIn('aria-describedby="b-direct-aide"', bouton.group(0))
        aide = re.search(r'<p id="b-direct-aide"[^>]*>(.*?)</p>', self.page, re.S).group(1)
        self.assertIn("python scripts/bureau_direct.py --installer", aide)
        self.assertIn("relancer Claude Code", aide)
        self.assertIn("127.0.0.1:8765/bureau.html#mode=direct", aide)
        self.assertRegex(self.page, r'<div class="bureau-direct" id="b-direct" hidden>')
        self.assertRegex(self.page, r'<section id="b-direct-evenements" hidden>')
        for ident in ("b-direct-etat", "b-direct-alerte", "b-direct-liste", "b-direct-sessions"):
            self.assertIn('id="{}"'.format(ident), self.page)
        self.assertIn('role="status"', self.page)

    def test_mode_direct_js(self):
        with open(bureau.SCRIPT_JS, encoding="utf-8") as f:
            js = f.read()
        # un seul flux, relatif (même origine), ouvert seulement quand la page est servie en local
        self.assertEqual(len(re.findall(r"EventSource\(", js)), 1)
        self.assertIn('new EventSource("direct/flux")', js)
        self.assertRegex(js, r'location\.protocol === "http:"')
        self.assertIn('"127.0.0.1"', js)
        self.assertIn('mode === "direct" && !DIRECT_DISPO', js)          # repli si file://
        self.assertIn("reduit", js)
        icones = re.search(r"var ICONES_ACT = \{(.*?)\};", js, re.S).group(1)
        for cat in ("lit:", "tape:", "terminal:", "web:"):                  # Read/Grep/Glob, Edit/Write, Bash
            self.assertIn(cat, icones)
        for evenement in ("demande", "outil_debut", "outil_fin", "autorisation", "attente", "agent_debut",
                          "agent_fin", "fin_tour", "session_debut", "session_fin"):
            self.assertIn('case "{}"'.format(evenement), js)

    # -- DEC-027 : info-bulle, halos, places de visite ------------------------------------------------
    def js(self):
        with open(bureau.SCRIPT_JS, encoding="utf-8") as f:
            return f.read()

    def test_infobulle_dans_le_cadre(self):
        m = re.search(r'<div class="bureau-cadre" id="b-cadre">(.*?)</div><aside', self.page, re.S)
        self.assertIsNotNone(m)
        self.assertIn('<div id="b-infobulle" class="b-infobulle" hidden aria-hidden="true"></div>', m.group(1))
        self.assertEqual(self.page.count('id="b-infobulle"'), 1)
        css = bureau.CSS
        self.assertRegex(css, r"\.b-infobulle\s*\{[^}]*position:\s*absolute")        # dans le cadre, visible en plein écran
        self.assertRegex(css, r"\.b-infobulle\[hidden\]\s*\{\s*display:\s*none")
        self.assertIn("pointer-events: none", css)

    def test_infobulle_js_sans_html(self):
        js = self.js()
        corps = re.search(r"function remplirInfobulle\(id\) \{(.*?)\n  function masquerInfobulle", js, re.S).group(1)
        self.assertIn("function ib(parent, tag, classe, texte)", js)
        self.assertNotRegex(corps, r"innerHTML|outerHTML|innerText|insertAdjacent")
        self.assertIn("mouseleave", js)
        self.assertRegex(js, r"function masquerInfobulle\(\) \{\s*infoId = null;\s*if \(infobulle\) \{ infobulle\.hidden = true;")
        self.assertRegex(js, r'(?s)"mousemove".*?if \(id\) \{ afficherInfobulle\(id, ev\); \} else \{ masquerInfobulle\(\); \}')
        # Replay : « dernier événement », pas de statut affirmé
        self.assertIn("Dernier événement du replay", corps)
        self.assertNotRegex(corps.split('"replay"')[1].split("} else {")[0], r"\.statut|libelleEtat")

    def test_infobulle_direct_ne_lit_que_la_liste_blanche(self):
        """DEC-018 § 3 : le code de l'info-bulle en mode Direct ne lit que acteur, outil, categorie, detail, ts."""
        js = self.js()
        bloc = re.search(r"// <info-bulle-direct>.*?// </info-bulle-direct>", js, re.S)
        self.assertIsNotNone(bloc)
        champs = set(re.findall(r"\bev\.(\w+)", bloc.group(0)))
        self.assertTrue(champs, "le bloc doit lire l'événement")
        self.assertLessEqual(champs, {"acteur", "outil", "categorie", "detail", "ts"})
        code = re.sub(r"//[^\n]*", "", bloc.group(0))
        for interdit in ("message", "prompt", "texte", "chemin", "fichier", "commande", "sortie", "cwd", "input",
                         "evenement", "session", "instance", "JSON", "m.data"):
            self.assertNotIn(interdit, code, interdit)
        # l'affichage ne relit que ce que le bloc a retenu
        corps = re.search(r"function remplirInfobulle\(id\) \{(.*?)\n  function masquerInfobulle", js, re.S).group(1)
        direct = corps.split('"direct"')[1].split("} else if")[0]
        self.assertLessEqual(set(re.findall(r"\bdd\.(\w+)", direct)), {"categorie", "outil", "heure"})
        self.assertNotIn("instantane", direct)
        self.assertNotIn("tickets", direct)
        # la fonction n'est appelée que sur un événement déjà validé par evValide
        self.assertEqual(js.count("infobulleDirect(p, ev);"), 1)
        self.assertLess(js.index("function evValide"), js.index("function infobulleDirect"))
        self.assertRegex(js, r"if \(evValide\(ev\)\) \{ appliquerDirect\(ev, DR\.pret\); \}")

    def test_halos_dans_les_donnees(self):
        self.assertEqual(self.d["halos"], bureau.HALOS)
        self.assertIn('"halos":', self.json_brut)
        for h in ("travail", "bloque", "attente"):
            self.assertIn('class="b-halo b-halo-{}"'.format(h), self.page)           # légende
        css = bureau.CSS
        for h in ("travail", "bloque", "attente"):
            self.assertIn(".b-halo-" + h, css)
        js = self.js()
        self.assertIn("D.halos", js)                                  # la table vient de bureau.py
        self.assertNotRegex(js, r"revue\s*:\s*\"(travail|bloque|attente)\"")
        corps = re.search(r"function dessinerHalo\((.*?)\n  \}", js, re.S).group(0)
        self.assertIn("PERIODE_HALO", corps)
        self.assertRegex(corps, r"reduit \? 0\.95 :")                 # prefers-reduced-motion : fixe
        self.assertGreaterEqual(int(re.search(r"var PERIODE_HALO = (\d+);", js).group(1)), 1500)
        styles = re.search(r"var STYLES_HALO = \{(.*?)\n  \};", js, re.S).group(1)
        formes = re.findall(r"tirets: (\[[^\]]*\])", styles)
        self.assertEqual(len(set(formes)), 3)                         # trois formes distinctes (pas la couleur seule)
        self.assertIn("var halo = haloDe(p);", js)
        self.assertLess(js.index("dessinerHalo(sc,"), js.index("sc.drawImage(s, sx, sy)"))   # sous le sprite

    def test_replay_et_halos_par_dernier_evenement(self):
        js = self.js()
        corps = re.search(r"function haloReplay\(ev\) \{(.*?)\n  \}", js, re.S).group(1)
        self.assertIn('EN_COURS: "tape"', corps)
        self.assertIn('BLOQUE: "bloque"', corps)
        self.assertIn('ATTENTE_HUMAIN: "attend"', corps)
        for statut in ("EN_REVUE", "TERMINE", "ANNULE", "A_FAIRE"):
            self.assertNotIn(statut, corps)                           # aucun halo
        self.assertIn("p.halo = haloReplay(ev);", js)

    def test_places_de_visite_dans_le_js(self):
        js = self.js()
        self.assertNotIn("DECALAGES", js)
        self.assertNotIn("function aCote", js)
        self.assertIn("reserverPlace(id, i.cible)", js)                                       # instantané
        self.assertIn('reserverPlace(ev.perso, "agent:relecteur-code")', js)                  # replay : place libre
        self.assertIn("c.poste.visites", js)
        self.assertIn("P.file", js)
        self.assertEqual(js.count("libererPlace(ev.perso);"), 1)

    def test_aucune_donnee_ajoutee(self):
        """Hors table des halos et places du plan, les entrées de la page ont les mêmes clés qu'avant (DEC-027)."""
        self.assertEqual(set(self.d), {"version", "date", "plan", "personnages", "projets", "evenements", "etats",
                                       "halos", "anomalies"})
        self.assertEqual(set(self.d["plan"]), {"largeur", "hauteur", "tuile", "rang_couloir", "pieces", "postes",
                                               "file", "cafe", "reunion"})
        for p in self.d["plan"]["postes"]:
            self.assertLessEqual(set(p), {"id", "piece", "x", "y", "bureau", "visites"})
        for pr in self.d["projets"]:
            self.assertEqual(set(pr), {"slug", "libelle", "page", "instantane"})
            for i in pr["instantane"]:
                self.assertEqual(set(i), {"perso", "etat", "cible", "bulle", "tickets"})
                for t in i["tickets"]:
                    self.assertEqual(set(t), {"id", "titre", "statut", "projet", "page", "role"})
        base = {"projet", "date", "heure", "estimee", "sans_heure", "perso", "note", "ticket", "type", "statut",
                "texte", "temps", "page", "n", "quand", "jalon"}
        for ev in self.d["evenements"]:
            self.assertLessEqual(set(ev), base | {"dec", "valide", "valide_par"})
            self.assertGreaterEqual(set(ev), base)
        for p in self.d["personnages"]:
            self.assertNotIn("halo", p)
            self.assertNotIn("visites", p)

    @unittest.skipUnless(shutil.which("node"), "node absent : syntaxe JavaScript non vérifiée")
    def test_syntaxe_js(self):
        r = subprocess.run(["node", "--check", bureau.SCRIPT_JS], capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))

    def test_listes_texte(self):
        self.assertEqual(self.page.count('class="b-etats"'), len(self.d["projets"]))
        self.assertIn('data-perso="agent:testeur"', self.page)
        self.assertIn('id="b-jalons" checked', self.page)               # jalons seulement, par défaut
        self.assertIn('aria-live="polite"', self.page)


# ---------------------------------------------------------------------------- membres humains (DEC-017)

def humains_md(*prenoms):
    return "---\ntitre: Membres humains\nstatut: EN_REVUE\nresponsable: B\nversion: 0.1\nmaj_le: 2026-11-26\n" \
           "valide_par:\ndecision:\nhumains:\n{}---\n# Membres humains\n".format(
               "".join("  - prenom: {}\n".format(p) for p in prenoms))


QUATRE = ("Ethan", "Johan", "Stéphane", "Matthieu")

TICKET_HUMAINS = """
    ---
    id: T-030
    titre: Arbitrage humain
    projet: demo
    type: tache
    statut: ATTENTE_HUMAIN
    priorite: normale
    assigne: salarie:ethan
    estimation_h: 1
    temps_passe_h: 0
    depend_de: []
    bloque_par: arbitrage attendu
    validation_humaine_requise: oui
    decision:
    cree_par: agent:coordinateur
    cree_le: 2026-11-18
    maj_le: 2026-11-24
    ---
    # T-030 — arbitrage humain

    ## Journal
    - 2026-11-18 09:00 · agent:testeur · création · 0 h
    - 2026-11-18 10:00 · Ethan · avis 1 · 0 h
    - 2026-11-18 10:05 · salarie:ethan · avis 2 · 0 h
    - 2026-11-18 10:10 · ETHAN · avis 3 · 0 h
    - 2026-11-18 10:15 · Stéphane · avis 4 · 0 h
    - 2026-11-18 10:20 · stephane · avis 5 · 0 h
    - 2026-11-18 10:25 · salarie:Stéphane · avis 6 · 0 h
    - 2026-11-18 10:30 · coordinateur pour Johan · avis 7 · 0 h
    - 2026-11-18 10:35 · Le professeur · avis 8 · 0 h
    - 2026-11-18 10:40 · Stéphane Martin (Johan) · avis 9 · 0 h
    - 2026-11-18 10:45 · agent:testeur · passage ATTENTE_HUMAIN · 0 h
    """


def generer(racine, *prenoms):
    """Données du bureau d'un dépôt de test, avec equipe/humains.md si des prénoms sont donnés."""
    if prenoms:
        ecrire(racine, "equipe/humains.md", humains_md(*prenoms))
    code, sortie = tc.lancer(racine, "--date", DATE)
    if code != 0:
        raise AssertionError(sortie)
    page = tc.lire(racine, "bureau.html")
    return page, json.loads(extraire_json(page))


class TestLireHumains(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.racine = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def lire(self, contenu):
        ecrire(self.racine, "equipe/humains.md", contenu)
        return bureau.lire_humains(self.racine)

    def test_fichier_absent(self):
        self.assertEqual(bureau.lire_humains(self.racine), ([], []))

    def test_quatre_humains(self):
        humains, anomalies = self.lire(humains_md(*QUATRE))
        self.assertEqual(humains, [("ethan", "Ethan"), ("johan", "Johan"), ("stephane", "Stéphane"),
                                   ("matthieu", "Matthieu")])
        self.assertEqual(anomalies, [])

    def test_doublons_et_entrees_invalides(self):
        humains, anomalies = self.lire("---\nhumains:\n  - prenom: Stéphane\n  - stephane\n  - prenom: STÉPHANE\n"
                                       "  - prenom:\n  - 42\n  - Ethan\n---\n")
        self.assertEqual(humains, [("stephane", "Stéphane"), ("ethan", "Ethan")])
        self.assertEqual(sum("en double" in a for a in anomalies), 2)
        self.assertEqual(sum("sans prénom" in a for a in anomalies), 2)

    def test_fichier_mal_forme(self):
        for contenu in ("---\nhumains: [Ethan\n---\n", "---\nhumains: Ethan\n---\n", "# pas d'en-tête\n",
                        "---\ntitre: x\n---\n", "---\nhumains:\n---\n", ""):
            humains, anomalies = self.lire(contenu)
            self.assertEqual(humains, [], contenu)
            self.assertEqual(len(anomalies), 1, contenu)
            self.assertIn("equipe/humains.md", anomalies[0])


class TestHumainsGeneration(unittest.TestCase):
    """Les membres humains de l'équipe projet dans la page générée (DEC-017)."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.racine = cls._tmp.name
        tc.creer_depot(cls.racine)
        ecrire(cls.racine, "projets/demo/tickets/T-030-humains.md", TICKET_HUMAINS)
        cls.page, cls.d = generer(cls.racine, *QUATRE)
        cls.persos = {p["id"]: p for p in cls.d["personnages"]}
        cls.postes = {p["id"]: p for p in cls.d["plan"]["postes"]}

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_quatre_humains_a_l_accueil(self):
        for cle, prenom in (("ethan", "Ethan"), ("johan", "Johan"), ("stephane", "Stéphane"),
                            ("matthieu", "Matthieu")):          # Matthieu n'est cité par aucun journal
            p = self.persos["humain:" + cle]
            self.assertEqual((p["nom"], p["nature"], p["modele"]), (prenom, "humain", "humain"))
            poste = self.postes[p["poste"]]
            self.assertEqual((poste["piece"], poste["y"], poste["bureau"]), ("couloir", 14, False))
            self.assertIn('data-perso="humain:{}"'.format(cle), self.page)
        ids = [p["id"] for p in self.d["personnages"]]
        self.assertEqual(ids[:5], ["coordinateur", "humain:ethan", "humain:johan", "humain:stephane",
                                   "humain:matthieu"])

    def test_rattachement_sans_doublon(self):
        evs = [e for e in self.d["evenements"] if e["ticket"] == "T-030"]
        self.assertEqual([e["perso"] for e in evs],
                         ["agent:testeur"] + ["humain:ethan"] * 3 + ["humain:stephane"] * 3 +
                         ["humain:johan", "visiteur:le-professeur", "humain:stephane", "agent:testeur"])
        self.assertEqual(evs[7]["note"], "saisi par le coordinateur")
        for nom in ("ethan", "stephane", "johan", "matthieu"):
            self.assertEqual(sum(bureau.normal(p["nom"]) == nom for p in self.d["personnages"]), 1, nom)
            self.assertNotIn("visiteur:" + nom, self.persos)
        dec = {e["dec"]: e for e in self.d["evenements"] if e["type"] == "decision"}
        self.assertEqual(dec["DEC-002"]["perso"], "humain:ethan")                   # decide_par: Ethan

    def test_autres_acteurs_restent_visiteurs(self):
        for pid, nom in (("visiteur:le-professeur", "Le professeur"), ("visiteur:equipe", "Équipe ESN")):
            self.assertEqual((self.persos[pid]["nature"], self.persos[pid]["nom"]), ("visiteur", nom))

    def test_instantane(self):
        demo = next(p for p in self.d["projets"] if p["slug"] == "demo")
        etat = {i["perso"]: i for i in demo["instantane"]}
        self.assertEqual(etat["humain:ethan"]["etat"], "attente")         # T-030 assigné à salarie:ethan
        self.assertEqual([t["id"] for t in etat["humain:ethan"]["tickets"]], ["T-030"])
        self.assertNotIn("humain:matthieu", etat)                         # rien en cours : à l'accueil

    def test_humain_ajoute_apparait(self):
        with tempfile.TemporaryDirectory() as racine:
            tc.creer_depot(racine)
            _, d = generer(racine, *(QUATRE + ("Zoé",)))
            persos = {p["id"]: p for p in d["personnages"]}
            self.assertEqual((persos["humain:zoe"]["nom"], persos["humain:zoe"]["nature"]), ("Zoé", "humain"))
            self.assertEqual(sum(p["nature"] == "humain" for p in d["personnages"]), 5)

    def test_fichier_absent_sans_plantage(self):
        with tempfile.TemporaryDirectory() as racine:
            tc.creer_depot(racine)
            _, d = generer(racine)                                     # aucun equipe/humains.md
            persos = {p["id"]: p for p in d["personnages"]}
            self.assertFalse([i for i in persos if i.startswith("humain:")])
            self.assertEqual(persos["visiteur:ethan"]["nature"], "visiteur")   # comportement d'avant DEC-017
            self.assertFalse([a for a in d["anomalies"] if "humains.md" in a])

    def test_fichier_mal_forme_sans_plantage(self):
        with tempfile.TemporaryDirectory() as racine:
            tc.creer_depot(racine)
            ecrire(racine, "equipe/humains.md", "---\nhumains: [Ethan\n---\n")
            _, d = generer(racine)
            self.assertTrue(any("equipe/humains.md : YAML invalide" in a for a in d["anomalies"]))


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
