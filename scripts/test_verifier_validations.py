#!/usr/bin/env python3
"""Tests de scripts/verifier_validations.py (contrôle CI des validations). Responsable : C · Lot 5.

Lancement : python scripts/test_verifier_validations.py
Dépôts temporaires construits pour chaque cas ; le dépôt réel doit passer.
Bibliothèque standard uniquement.
"""
import os
import subprocess
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RACINE, "scripts", "verifier_validations.py")


def entete(statut, valide_par="", decision="", extra=""):
    return ("---\ntitre: Essai\nstatut: {}\nresponsable: C\nversion: 0.1\nmaj_le: 2026-11-24\n"
            "valide_par: {}\ndecision: {}\n{}---\n\n# Essai\n").format(statut, valide_par, decision, extra)


class TestVerifierValidations(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.racine = self.tmp.name
        self.ecrire("docs/decisions/2026-11-24-DEC-007-essai.md",
                    entete("VALIDÉ", "Ethan", "DEC-007", "id: DEC-007\n"))

    def tearDown(self):
        self.tmp.cleanup()

    def ecrire(self, rel, contenu):
        chemin = os.path.join(self.racine, rel)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "w", encoding="utf-8", newline="\n") as f:
            f.write(contenu)

    def lancer(self, racine=None):
        r = subprocess.run([sys.executable, SCRIPT, "--racine", racine or self.racine], capture_output=True)
        return r.returncode, r.stdout.decode("utf-8", "replace")

    def test_conforme(self):
        self.ecrire("docs/a.md", entete("VALIDÉ", "Léa", "DEC-007"))
        self.ecrire("docs/b.md", entete("EN_REVUE"))
        self.ecrire("docs/c.md", entete("BROUILLON"))
        code, out = self.lancer()
        self.assertEqual(code, 0, out)
        self.assertIn("4 document(s) contrôlé(s), 0 anomalie(s)", out)

    def test_graphies_de_valide(self):
        for k, graphie in enumerate(("validé", "Validé", "VALIDE", '"VALIDÉ"')):
            self.ecrire("docs/g{}.md".format(k), entete(graphie, "", "DEC-007"))
        code, out = self.lancer()
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count("VALIDÉ sans valide_par"), 4, out)

    def test_statut_hors_liste(self):
        self.ecrire("docs/a.md", entete("APPROUVE"))
        self.ecrire("docs/b.md", entete(""))
        code, out = self.lancer()
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count("hors de BROUILLON, EN_REVUE, VALIDÉ"), 2, out)

    def test_decision_absente_ou_mal_formee(self):
        self.ecrire("docs/a.md", entete("VALIDÉ", "Léa", ""))
        self.ecrire("docs/b.md", entete("VALIDÉ", "Léa", "DEC-7"))
        self.ecrire("docs/c.md", entete("VALIDÉ", "Léa", "DEC-999"))
        code, out = self.lancer()
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count("sans decision: DEC-NNN valide"), 2, out)
        self.assertIn("docs/c.md : DEC-999 ne correspond à aucun fichier", out)

    def test_commentaire_yaml(self):
        self.ecrire("docs/a.md", entete("EN_REVUE          # journal, jamais VALIDÉ"))
        self.ecrire("docs/b.md", entete("VALIDÉ", "Léa   # humain", "DEC-007   # décision"))
        self.assertEqual(self.lancer()[0], 0)

    def test_journal_jamais_valide(self):
        self.ecrire("docs/CHANGELOG-REGLES.md", entete("VALIDÉ", "Léa", "DEC-007"))
        code, out = self.lancer()
        self.assertEqual(code, 1, out)
        self.assertIn("un journal ne passe jamais VALIDÉ", out)

    def test_tickets_et_fiches_ignores(self):
        self.ecrire("projets/demo/tickets/T-001-x.md",
                    "---\nid: T-001\nstatut: TERMINE\nvalide_par:\n---\n")
        self.ecrire("equipe/membres/lea.md", "---\nprenom: lea\nstatut: actif\n---\n")
        self.ecrire("projets/demo/app/docs/notes.md", entete("N_IMPORTE_QUOI"))
        self.ecrire("README.md", "# Sans en-tête\n")
        code, out = self.lancer()
        self.assertEqual(code, 0, out)
        self.assertIn("1 document(s) contrôlé(s)", out)

    def test_racine_absente(self):
        self.assertEqual(self.lancer(os.path.join(self.racine, "absente"))[0], 2)

    def test_depot_reel(self):
        code, out = self.lancer(RACINE)
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
