#!/usr/bin/env python3
"""Tests de scripts/tableau.py. Responsable : D · Lot 2 (D).

Lancement : python scripts/test_tableau.py   (Mac : python3 …) ; nécessite PyYAML (requirements.txt).
Toutes les données (équipe, projets, tickets) sont créées dans un dossier temporaire : aucun vrai
dossier projets/ n'est créé ni lu. Date de calcul fixée au 2026-11-25 (mercredi).
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RACINE, "scripts", "tableau.py")
DATE = "2026-11-25"

sys.dont_write_bytecode = True  # pas de __pycache__ dans scripts/
_spec = importlib.util.spec_from_file_location("tableau", SCRIPT)
tableau = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tableau)


# ---------------------------------------------------------------------------- données de test

def ecrire(racine, chemin, contenu):
    chemin = os.path.join(racine, *chemin.split("/"))
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(textwrap.dedent(contenu).lstrip("\n"))


def membre(prenom, niveau, cout, cap, statut, allocation, depart=""):
    alloc = "{}" if not allocation else "\n" + "\n".join("  {}: {}".format(k, v) for k, v in allocation.items())
    return """
    ---
    prenom: {p}
    role: test
    niveau: {n}
    cout_journalier_eur: {c}
    capacite_h_semaine: {cap}
    statut: {s}
    date_arrivee: 2020-01-01
    date_depart: {d}
    competences: []
    allocation: {a}
    responsable: B
    maj_le: 2026-11-23
    ---

    # {p}
    """.format(p=prenom, n=niveau, c=cout, cap=cap, s=statut, d=depart, a=alloc.replace("\n", "\n    "))


def projet(slug, budget, deadline):
    return """
    ---
    titre: Fiche projet — Client {s}
    statut: EN_REVUE
    responsable: B
    version: 0.1
    maj_le: 2026-11-20
    valide_par:
    decision:
    slug: {s}
    client: Client {s}
    type_projet: metier
    etat_projet: en_cours
    budget_eur: {b}
    deadline: {d}
    hebergement: render
    url_prod:
    agents_mobilises: []
    salaries_affectes: []
    ---
    # Fiche projet
    """.format(s=slug, b=budget, d=deadline)


def ticket(tid, titre, type_, statut, prio, assigne, est, passe, dep=(), bloque_par="",
           cree="2026-11-18", maj="2026-11-24", journal=()):
    lignes = ["- {} · {} · création · 0 h".format(cree + " 09:00", assigne)] + ["- " + j for j in journal]
    return """
    ---
    id: {id}
    titre: {t}
    projet: x
    type: {ty}
    statut: {st}
    priorite: {pr}
    assigne: {a}
    estimation_h: {e}
    temps_passe_h: {p}
    depend_de: [{dep}]
    bloque_par: {bp}
    validation_humaine_requise: non
    decision:
    cree_par: agent:coordinateur
    cree_le: {c}
    maj_le: {m}
    ---
    <!-- modèle : templates/ticket.md v0.1 · responsable du modèle : A -->

    # {id} — {t}

    ## Description
    test

    ## Critères d'acceptation
    - [ ] critère

    ## Journal
    {j}
    """.format(id=tid, t=titre, ty=type_, st=statut, pr=prio, a=assigne, e=est, p=passe,
               dep=", ".join(dep), bp=bloque_par, c=cree, m=maj, j="\n    ".join(lignes))


def creer_donnees(racine):
    ecrire(racine, "equipe/agents.md", """
    ---
    cout_horaire_eur: 15
    responsable: B
    maj_le: 2026-11-23
    agents:
      - nom: analyste-besoin
      - nom: dev-backend
      - nom: dev-frontend
      - nom: testeur
      - nom: gestionnaire-crise
    hors_perimetre_agents: [relation-client]
    ---
    # Agents
    """)
    ecrire(racine, "equipe/calendrier.md", """
    ---
    responsable: B
    maj_le: 2026-11-23
    jours_feries: [2026-12-25, 2027-01-01]
    evenements:
      - id: EV-001
        type: absence
        qui: salarie:lea
        debut: 2026-11-26
        fin: 2026-11-27
        motif: conges
        capacite_pct: 0
        statut: prevu
        decision:
      - id: EV-002
        type: absence
        qui: salarie:karim
        debut: 2026-11-25
        fin: 2026-11-25
        motif: autre
        capacite_pct: 0
        statut: annule
        decision:
    ---
    # Calendrier
    """)
    ecrire(racine, "equipe/membres/lea.md", membre("lea", "confirme", 450, 35, "actif", {"demo": 100}))
    ecrire(racine, "equipe/membres/karim.md", membre("karim", "expert", 550, 35, "actif", {"demo": 50}))
    ecrire(racine, "equipe/membres/hugo.md", membre("hugo", "debutant", 350, 35, "depart_prevu", {"demo": 50},
                                                    depart="2026-11-27"))
    ecrire(racine, "equipe/membres/nadia.md", membre("nadia", "confirme", 450, 28, "actif", {}))

    # Projet « demo » : 12 tickets variés
    ecrire(racine, "projets/demo/projet.md", projet("demo", 500, "2026-11-27"))
    tickets = [
        ticket("T-001", "Rédaction du CDC", "tache", "TERMINE", "normale", "agent:analyste-besoin", 4, 5,
               maj="2026-11-19"),
        ticket("T-002", "API réservations", "fonctionnalite", "EN_COURS", "normale", "agent:dev-backend", 6, 2,
               dep=["T-001"], maj="2026-11-20", journal=["2026-11-20 10:00 · agent:dev-backend · début · 2 h"]),
        ticket("T-003", "Écran de réservation", "fonctionnalite", "A_FAIRE", "normale", "salarie:lea", 10, 0),
        ticket("T-004", "Bug affichage créneaux", "bug", "BLOQUE", "haute", "agent:dev-frontend", 3, 4,
               bloque_par="attente de l'API T-002", maj="2026-11-23",
               journal=["2026-11-23 10:00 · agent:dev-frontend · passage BLOQUE · 0 h"]),
        ticket("T-005", "Validation budget et délais", "decision", "ATTENTE_HUMAIN", "haute", "salarie:karim", 1, 0,
               bloque_par="validation humaine du budget et des délais"),
        ticket("T-006", "Production indisponible", "incident", "A_FAIRE", "critique", "agent:gestionnaire-crise", 3, 0),
        ticket("T-007", "Formation tests-e2e", "formation", "A_FAIRE", "normale", "salarie:lea", 7, 0),
        ticket("T-008", "Tests abandonnés", "tache", "ANNULE", "normale", "agent:testeur", 4, 1),
        ticket("T-009", "Liste des salles", "fonctionnalite", "EN_REVUE", "normale", "agent:dev-frontend", 5, 5,
               dep=["T-002"]),
        ticket("T-010", "Revue humaine T-009", "tache", "A_FAIRE", "normale", "salarie:karim", 2, 0, dep=["T-009"]),
        ticket("T-011", "Revue architecture", "tache", "TERMINE", "normale", "salarie:karim", 3, 3),
        ticket("T-012", "Documentation de passation", "tache", "A_FAIRE", "normale", "salarie:hugo", 14, 0),
    ]
    for i, contenu in enumerate(tickets, start=1):
        ecrire(racine, "projets/demo/tickets/T-{:03d}-test.md".format(i), contenu)

    # Projet sans tickets
    ecrire(racine, "projets/vide/projet.md", projet("vide", 1000, "2026-12-31"))
    # Projet dont le salarié assigné n'a aucune allocation
    ecrire(racine, "projets/sansalloc/projet.md", projet("sansalloc", 1000, "2026-12-31"))
    ecrire(racine, "projets/sansalloc/tickets/T-001-test.md",
           ticket("T-001", "Pipeline CI", "tache", "A_FAIRE", "normale", "salarie:nadia", 3, 0))
    # Projet avec une dépendance circulaire
    ecrire(racine, "projets/cycle/projet.md", projet("cycle", 1000, "2026-12-31"))
    ecrire(racine, "projets/cycle/tickets/T-001-test.md",
           ticket("T-001", "A", "tache", "A_FAIRE", "normale", "agent:dev-backend", 2, 0, dep=["T-002"]))
    ecrire(racine, "projets/cycle/tickets/T-002-test.md",
           ticket("T-002", "B", "tache", "A_FAIRE", "normale", "agent:dev-backend", 2, 0, dep=["T-001"]))


def arborescence(racine):
    fichiers = set()
    for d, _, noms in os.walk(racine):
        for n in noms:
            fichiers.add(os.path.relpath(os.path.join(d, n), racine).replace("\\", "/"))
    return fichiers


def lancer(racine, *args):
    r = subprocess.run([sys.executable, SCRIPT, "--racine", racine, *args], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", errors="replace") + r.stderr.decode("utf-8", errors="replace")


def lire(racine, chemin):
    with open(os.path.join(racine, *chemin.split("/")), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------- tests

class TestTableauScript(unittest.TestCase):
    """Le script lancé comme par le chef-de-projet ou la CI."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.racine = cls._tmp.name
        creer_donnees(cls.racine)
        cls.avant = arborescence(cls.racine)
        cls.code, cls.sortie = lancer(cls.racine, "--date", DATE)
        cls.apres = arborescence(cls.racine)
        cls.demo = lire(cls.racine, "projets/demo/TABLEAU.md")
        cls.portfolio = lire(cls.racine, "PORTFOLIO.md")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_code_retour(self):
        self.assertEqual(self.code, 0, self.sortie)

    def test_n_ecrit_que_tableau_et_portfolio(self):
        self.assertEqual(self.apres - self.avant, {
            "PORTFOLIO.md", "projets/demo/TABLEAU.md", "projets/vide/TABLEAU.md",
            "projets/sansalloc/TABLEAU.md", "projets/cycle/TABLEAU.md"})
        self.assertEqual(self.avant - self.apres, set())

    def test_en_tete_fichier_genere(self):
        for contenu in (self.demo, self.portfolio):
            self.assertTrue(contenu.startswith("<!-- FICHIER GÉNÉRÉ par scripts/tableau.py"))
            self.assertIn("ne pas modifier à la main (R9)", contenu)
            self.assertNotIn("\r\n", contenu)

    def test_synthese_formules(self):
        # Avancement : 7 h TERMINE / 58 h hors ANNULE
        self.assertIn("12,1 % (7,0 h / 58,0 h)", self.demo)
        # Temps restant (DEC-001 § 4) : T-004 en dépassement compte 0
        self.assertIn("| 41,0 h |", self.demo)
        # Budget consommé : (5+2+4+1+5) h × 15 € + 3 h × 550/7 € = 490,71 €, ANNULE compris
        self.assertIn("490,71 € / 500,00 € (98,1 %)", self.demo)
        self.assertIn("Fin projetée | 2026-12-01 (hors 1 ticket(s) non planifiable(s))", self.demo)
        self.assertIn("| +2 j ouvrés |", self.demo)

    def test_alertes(self):
        self.assertIn("| Budget | budget consommé 490,71 €", self.demo)
        self.assertIn("| Délais | fin projetée le 2026-12-01 après la deadline du 2026-11-27 (+2 j ouvrés)", self.demo)
        self.assertIn("| Critique | T-006", self.demo)
        self.assertIn("| Sans mise à jour | T-002 EN_COURS sans mise à jour depuis 3 j ouvrés", self.demo)
        self.assertIn("| Préavis de départ | hugo part le 2026-11-27 : 2 j ouvrés de préavis", self.demo)
        self.assertIn("| Absence (S1-R9) | T-003 (salarie:lea) : fenêtre prévue du 2026-11-25 au 2026-11-30 "
                      "chevauche EV-001", self.demo)
        self.assertIn("| Non planifiable | T-012 : salarie:hugo : capacité insuffisante avant le départ du "
                      "2026-11-27", self.demo)
        self.assertIn("| Utilisation (info) | karim utilisé à 28,6 %", self.demo)
        self.assertIn("| Surcharge | lea", self.demo)
        # Les tickets ANNULE et TERMINE ne déclenchent rien
        self.assertNotIn("T-008", self.demo.split("## Alertes")[1].split("## Tickets par statut")[0])

    def test_bloque_et_attente_humain(self):
        self.assertIn("| T-004 | Bug affichage créneaux | agent:dev-frontend | attente de l'API T-002 | "
                      "2 j ouvrés (depuis 2026-11-23) |", self.demo)
        self.assertIn("| haute | T-005 | Validation budget et délais | salarie:karim | "
                      "validation humaine du budget et des délais |", self.demo)

    def test_af11_formation_utilisation(self):
        af11 = self.demo.split("## Tickets salariés à faire par un humain (AF11)")[1].split("## Tickets formation")[0]
        for tid in ("T-003", "T-005", "T-007", "T-010", "T-012"):
            self.assertIn(tid, af11)
        self.assertNotIn("T-011", af11)  # TERMINE
        self.assertIn("| T-003 | Écran de réservation | salarie:lea | A_FAIRE | 10,0 h | 2026-11-25 → 2026-11-30 |", af11)
        self.assertIn("| T-012 | Documentation de passation | salarie:hugo | A_FAIRE | 14,0 h | non planifiable |", af11)
        form = self.demo.split("## Tickets formation ouverts")[1].split("## Utilisation")[0]
        self.assertIn("T-007", form)
        util = self.demo.split("## Utilisation des salariés")[1].split("## Planning")[0]
        self.assertIn("Période : du 2026-11-25 au 2026-11-27", util)
        self.assertIn("| lea | 100 % | 17,0 h | 7,0 h | 242,9 % | surcharge |", util)
        self.assertIn("| karim | 50 % | 3,0 h | 10,5 h | 28,6 % |", util)

    def test_gantt_mermaid(self):
        g = self.demo.split("```mermaid")[1].split("```")[0]
        self.assertIn("gantt", g)
        self.assertIn("dateFormat YYYY-MM-DD", g)
        self.assertIn("section salarie lea", g)
        # fin exclusive dans Mermaid : fin prévue + 1 jour
        self.assertIn("T-003 Écran de réservation :t003, 2026-11-25, 2026-12-01", g)
        self.assertIn("T-006 Production indisponible :crit, t006, 2026-11-25, 2026-11-26", g)
        self.assertIn("T-002 API réservations :active, t002, 2026-11-25, 2026-11-26", g)
        self.assertIn("T-001 Rédaction du CDC :done, t001, 2026-11-18, 2026-11-20", g)
        self.assertIn("Deadline :milestone, deadline, 2026-11-27, 0d", g)
        self.assertNotIn("T-008", g)  # ANNULE
        self.assertNotIn("T-012", g)  # non planifiable

    def test_projets_limites(self):
        vide = lire(self.racine, "projets/vide/TABLEAU.md")
        self.assertIn("— (aucun ticket)", vide)
        self.assertIn("_Aucun ticket à représenter._", vide)
        sansalloc = lire(self.racine, "projets/sansalloc/TABLEAU.md")
        self.assertIn("T-001 : salarie:nadia : allocation au projet nulle (S1-R10)", sansalloc)
        self.assertIn("indéterminée (1 ticket(s) non planifiable(s))", sansalloc)
        cycle = lire(self.racine, "projets/cycle/TABLEAU.md")
        self.assertIn("T-001 : dépendance circulaire ou dépendant d'un cycle ; non planifié", cycle)
        self.assertIn("T-002 : dépendance circulaire ou dépendant d'un cycle ; non planifié", cycle)

    def test_portfolio(self):
        self.assertIn("| [demo](projets/demo/TABLEAU.md) | Client demo |", self.portfolio)
        for slug in ("vide", "sansalloc", "cycle"):
            self.assertIn("[{s}](projets/{s}/TABLEAU.md)".format(s=slug), self.portfolio)
        self.assertIn("| (équipe) | Préavis de départ | hugo part le 2026-11-27", self.portfolio)
        self.assertIn("| haute | demo | T-005 |", self.portfolio)
        self.assertIn("| EV-001 | salarie:lea | absence | 2026-11-26 | 2026-11-27 |", self.portfolio)
        self.assertNotIn("EV-002", self.portfolio)  # événement annulé ignoré

    def test_idempotence(self):
        code, sortie = lancer(self.racine, "--date", DATE)
        self.assertEqual(code, 0, sortie)
        self.assertIn("inchangé", sortie)
        self.assertNotIn("écrit ·", sortie)
        self.assertEqual(lire(self.racine, "projets/demo/TABLEAU.md"), self.demo)


class TestTableauModule(unittest.TestCase):
    """Calculs internes : jours ouvrés, capacité, ordonnancement autour de l'absence de Léa."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        creer_donnees(cls._tmp.name)
        cls.equipe = tableau.Equipe(cls._tmp.name)
        cls.projet = tableau.Projet(cls._tmp.name, os.path.join(cls._tmp.name, "projets", "demo"),
                                    cls.equipe, date(2026, 11, 25))
        cls.projet.calculer()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_jours_ouvres(self):
        feries = {date(2026, 12, 25)}
        # du jeudi 24/12 (exclu) au lundi 28/12 (inclus) : 25 férié, 26-27 week-end -> 1
        self.assertEqual(tableau.jours_ouvres_entre(date(2026, 12, 24), date(2026, 12, 28), feries), 1)
        self.assertEqual(tableau.jours_ouvres_entre(date(2026, 11, 20), date(2026, 11, 25), set()), 3)
        self.assertEqual(tableau.jours_ouvres_entre(date(2026, 11, 25), date(2026, 11, 25), set()), 0)

    def test_capacite_lea_pendant_absence(self):
        r = tableau.Ressource("salarie:lea", "demo", self.equipe)
        self.assertEqual(r.capacite(date(2026, 11, 25)), 7.0)
        self.assertEqual(r.capacite(date(2026, 11, 26)), 0.0)
        self.assertEqual(r.capacite(date(2026, 11, 27)), 0.0)
        self.assertEqual(r.capacite(date(2026, 11, 28)), 0.0)  # samedi
        self.assertEqual(r.capacite(date(2026, 11, 30)), 7.0)

    def test_capacite_salaries(self):
        self.assertEqual(tableau.Ressource("salarie:karim", "demo", self.equipe).capacite(date(2026, 11, 25)), 3.5)
        hugo = tableau.Ressource("salarie:hugo", "demo", self.equipe)
        self.assertEqual(hugo.capacite(date(2026, 11, 27)), 3.5)
        self.assertEqual(hugo.capacite(date(2026, 11, 30)), 0.0)  # après le départ
        self.assertEqual(tableau.Ressource("salarie:nadia", "demo", self.equipe).raison,
                         "allocation au projet nulle (S1-R10)")
        self.assertEqual(tableau.Ressource("agent:inconnu", "demo", self.equipe).raison,
                         "agent inconnu d'equipe/agents.md")

    def test_ordonnancement(self):
        t = self.projet.par_id
        self.assertEqual((t["T-003"].debut_prevu, t["T-003"].fin_prevue), (date(2026, 11, 25), date(2026, 11, 30)))
        self.assertEqual(t["T-007"].fin_prevue, date(2026, 12, 1))   # après T-003, sur la capacité de Léa
        self.assertEqual(t["T-010"].fin_prevue, date(2026, 11, 26))  # après T-009 (dépendance)
        self.assertIsNotNone(t["T-012"].non_planifiable)
        self.assertIsNone(t["T-001"].fin_prevue)                     # TERMINE : pas replanifié
        self.assertEqual(self.projet.fin_projetee, date(2026, 12, 1))
        self.assertEqual(self.projet.ecart, 2)

    def test_formules(self):
        p = self.projet
        self.assertAlmostEqual(p.avancement, 7 / 58)
        self.assertAlmostEqual(p.temps_restant, 41.0)
        self.assertAlmostEqual(p.consomme, 17 * 15 + 3 * 550 / 7)
        self.assertAlmostEqual(p.projete, p.consomme + (4 + 3 + 0 + 0) * 15 + (10 + 7) * 450 / 7
                               + (1 + 2) * 550 / 7 + 14 * 350 / 7)


class TestTableauSansDonnees(unittest.TestCase):

    def test_depot_vide(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, sortie = lancer(tmp, "--date", DATE)
            self.assertEqual(code, 0, sortie)
            self.assertEqual(arborescence(tmp), {"PORTFOLIO.md"})
            contenu = lire(tmp, "PORTFOLIO.md")
            self.assertIn("Aucun projet dans `projets/`.", contenu)
            self.assertIn("equipe/agents.md absent", contenu)

    def test_ticket_illisible(self):
        with tempfile.TemporaryDirectory() as tmp:
            ecrire(tmp, "projets/x/projet.md", projet("x", 100, "AAAA-MM-JJ"))
            ecrire(tmp, "projets/x/tickets/T-001-casse.md", "---\nid: [T-001\n---\n")
            ecrire(tmp, "projets/x/tickets/T-002-ok.md",
                   ticket("T-002", "ok", "tache", "BLOQUE", "normale", "agent:dev-backend", 1, 0))
            code, sortie = lancer(tmp, "--date", DATE)
            self.assertEqual(code, 0, sortie)
            contenu = lire(tmp, "projets/x/TABLEAU.md")
            self.assertIn("tickets/T-001-casse.md : YAML invalide", contenu)
            self.assertIn("T-002 : BLOQUE sans bloque_par (S1-R3)", contenu)
            self.assertIn("deadline absente ou invalide", contenu)

    def test_date_invalide(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, sortie = lancer(tmp, "--date", "25/11/2026")
            self.assertEqual(code, 2)
            self.assertIn("--date invalide", sortie)
            self.assertEqual(arborescence(tmp), set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
