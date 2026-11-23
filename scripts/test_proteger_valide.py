#!/usr/bin/env python3
"""Tests du hook .claude/hooks/proteger_valide.py (R5, R6). Responsable : C · Lot 2 (C).

Lancement : python scripts/test_proteger_valide.py
Chaque test crée un faux projet dans un dossier temporaire et lance le hook comme
Claude Code le fait : JSON sur stdin, CLAUDE_PROJECT_DIR pointé sur le projet.
Bibliothèque standard uniquement.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(RACINE, ".claude", "hooks", "proteger_valide.py")

DOC_VALIDE = """---
titre: Architecture
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-23
valide_par: Ethan
decision: DEC-001
---

# Corps
Texte validé.
"""

DOC_EN_REVUE = """---
titre: CDC
statut: EN_REVUE
responsable: agent:analyste-besoin
version: 0.2
maj_le: 2026-11-23
valide_par:
decision:
---

# CDC
Contenu.
"""

JOURNAL = """---
titre: Historique des modifications de règles
statut: EN_REVUE          # journal, jamais VALIDÉ (évolue uniquement par PR, exclu de R6)
responsable: B
version: 0.2
maj_le: 2026-11-23
valide_par:
decision:
---

| Date | Règle |
|---|---|
"""

TICKET = """---
id: T-004
titre: GO mise en production
projet: demo
type: decision
statut: TERMINE
priorite: haute
assigne: salarie:ethan
estimation_h: 1
temps_passe_h: 1
depend_de: []
bloque_par:
validation_humaine_requise: oui
decision: DEC-001
cree_par: agent:chef-de-projet
cree_le: 2026-11-23
maj_le: 2026-11-23
---

# T-004 — GO
"""

MEMBRE = """---
prenom: Ethan
statut: actif
niveau: confirme
---
"""

ENTETE_EXEMPLE = """---
titre: En-tête standard des documents
statut: BROUILLON
responsable: A
version: 0.2
maj_le: 2026-11-23
valide_par:
decision:
---

```yaml
statut: VALIDÉ
```
"""


def nouveau_doc(statut, valide_par=True):
    lignes = ["---", "titre: Essai", "statut: " + statut, "responsable: C", "version: 0.1",
              "maj_le: 2026-11-23"]
    if valide_par:
        lignes += ["valide_par:", "decision:"]
    return "\n".join(lignes + ["---", "", "# Essai", ""])


class TestProtegerValide(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.racine = self.tmp.name
        for d in ("docs/decisions", "projets/demo/tickets", "projets/demo/app", "equipe/membres", "templates"):
            os.makedirs(os.path.join(self.racine, d), exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    # -- outils --------------------------------------------------------------
    def chemin(self, rel):
        return os.path.join(self.racine, *rel.split("/"))

    def fichier(self, rel, contenu, bom=False, crlf=False):
        if crlf:
            contenu = contenu.replace("\n", "\r\n")
        donnees = contenu.encode("utf-8")
        if bom:
            donnees = b"\xef\xbb\xbf" + donnees
        with open(self.chemin(rel), "wb") as f:
            f.write(donnees)

    def lancer(self, entree, brut=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=self.racine)
        donnees = brut if brut is not None else json.dumps(entree).encode("utf-8")
        r = subprocess.run([sys.executable, HOOK], input=donnees, capture_output=True, env=env)
        self.sortie = r.stdout.decode("utf-8", errors="replace")
        return r.returncode, r.stderr.decode("utf-8", errors="replace")

    def demande_confirmation(self, resultat):
        self.accepte(resultat)
        decision = json.loads(self.sortie)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "ask")
        self.assertIn("garde-fou 6", decision["permissionDecisionReason"])

    def write(self, rel, contenu):
        return self.lancer({"tool_name": "Write", "tool_input": {"file_path": self.chemin(rel), "content": contenu}})

    def edit(self, rel, vieux, neuf, tout=False, chemin=None):
        return self.lancer({"tool_name": "Edit", "tool_input": {
            "file_path": chemin or self.chemin(rel), "old_string": vieux, "new_string": neuf, "replace_all": tout}})

    def refuse(self, resultat, regle):
        code, err = resultat
        self.assertEqual(code, 2, "aurait dû être refusé ; stderr=" + err)
        self.assertIn("(" + regle + ")", err)

    def accepte(self, resultat):
        code, err = resultat
        self.assertEqual(code, 0, "aurait dû être accepté ; stderr=" + err)

    # -- R5 -----------------------------------------------------------------
    def test_01_write_valide_accentue(self):
        self.refuse(self.write("projets/demo/cdc.md", nouveau_doc("VALIDÉ")), "R5")

    def test_02_valide_sans_accent(self):
        self.refuse(self.write("projets/demo/cdc.md", nouveau_doc("VALIDE")), "R5")

    def test_03_valide_minuscules(self):
        self.refuse(self.write("projets/demo/cdc.md", nouveau_doc("validé")), "R5")

    def test_04_valide_guillemets_et_commentaire(self):
        self.refuse(self.write("projets/demo/cdc.md", nouveau_doc('"Validé"   # par l\'agent')), "R5")

    def test_05_edit_fragment_seul(self):
        self.fichier("projets/demo/cdc.md", DOC_EN_REVUE)
        self.refuse(self.edit("projets/demo/cdc.md", "EN_REVUE", "VALIDÉ"), "R5")

    def test_06_multiedit_deuxieme_edit(self):
        self.fichier("projets/demo/cdc.md", DOC_EN_REVUE)
        r = self.lancer({"tool_name": "MultiEdit", "tool_input": {
            "file_path": self.chemin("projets/demo/cdc.md"),
            "edits": [{"old_string": "Contenu.", "new_string": "Contenu revu."},
                      {"old_string": "statut: EN_REVUE", "new_string": "statut: VALIDE"}]}})
        self.refuse(r, "R5")

    def test_07_suppression_valide_par(self):
        self.fichier("projets/demo/cdc.md", DOC_EN_REVUE)
        self.refuse(self.edit("projets/demo/cdc.md", "statut: EN_REVUE\nresponsable: agent:analyste-besoin\n"
                              "version: 0.2\nmaj_le: 2026-11-23\nvalide_par:\n",
                              "statut: Validé\nresponsable: agent:analyste-besoin\n"
                              "version: 0.2\nmaj_le: 2026-11-23\n"), "R5")

    # -- R6 -----------------------------------------------------------------
    def test_08_edit_corps_document_valide(self):
        self.fichier("docs/ARCHITECTURE.md", DOC_VALIDE)
        self.refuse(self.edit("docs/ARCHITECTURE.md", "Texte validé.", "Texte modifié."), "R6")

    def test_09_write_devalide(self):
        self.fichier("docs/ARCHITECTURE.md", DOC_VALIDE)
        self.refuse(self.write("docs/ARCHITECTURE.md", DOC_VALIDE.replace("VALIDÉ", "EN_REVUE")), "R6")

    def test_10_crlf_et_bom(self):
        self.fichier("docs/S3.md", DOC_VALIDE, bom=True, crlf=True)
        self.refuse(self.edit("docs/S3.md", "Corps", "Nouveau corps"), "R6")

    # -- journaux -------------------------------------------------------------
    def test_11_journal_commentaire_ignore(self):
        self.fichier("docs/CHANGELOG-REGLES.md", JOURNAL)
        self.accepte(self.edit("docs/CHANGELOG-REGLES.md", "|---|---|\n", "|---|---|\n| 2026-11-24 | R14 |\n"))

    def test_12_journal_exclu_de_r6(self):
        self.fichier("docs/decisions/README.md", DOC_VALIDE)
        self.accepte(self.edit("docs/decisions/README.md", "Texte validé.", "Texte validé.\n| DEC-002 |"))

    def test_13_journal_r5_sapplique(self):
        self.fichier("docs/CHANGELOG-REGLES.md", JOURNAL)
        self.refuse(self.edit("docs/CHANGELOG-REGLES.md", "statut: EN_REVUE", "statut: VALIDÉ"), "R5")

    # -- hors champ -----------------------------------------------------------
    def test_14_ticket(self):
        self.fichier("projets/demo/tickets/T-004-go.md", TICKET)
        self.accepte(self.edit("projets/demo/tickets/T-004-go.md", "# T-004 — GO", "# T-004 — GO mise en prod"))

    def test_15_md_sans_entete(self):
        self.accepte(self.write("projets/demo/app/README.md", "# App\nstatut: VALIDÉ\n"))

    def test_16_fichier_non_md(self):
        self.accepte(self.write("projets/demo/app/config.py", nouveau_doc("VALIDÉ")))

    def test_17_document_en_revue(self):
        self.fichier("projets/demo/cdc.md", DOC_EN_REVUE)
        self.accepte(self.edit("projets/demo/cdc.md", "Contenu.", "Contenu enrichi."))

    def test_18_exemple_dans_le_corps(self):
        # Pas de R5 pour l'exemple du corps ; templates/ demande toutefois une confirmation (test 22).
        self.demande_confirmation(self.write("templates/_ENTETE.md", ENTETE_EXEMPLE))

    # -- garde-fou 6 : templates/ ------------------------------------------------
    def test_22_templates_racine_ask(self):
        self.fichier("templates/ticket.md", TICKET.replace("id: T-004", "id: T-NNN"))
        self.demande_confirmation(self.edit("templates/ticket.md", "# T-004 — GO", "# T-NNN — <titre>"))

    def test_23_templates_dans_une_app_libre(self):
        os.makedirs(self.chemin("projets/demo/app/templates"), exist_ok=True)
        self.accepte(self.write("projets/demo/app/templates/index.html", "<h1>ok</h1>"))
        self.assertEqual(self.sortie, "")

    def test_24_templates_r5_prime(self):
        self.refuse(self.write("templates/cdc.md", nouveau_doc("VALIDÉ")), "R5")

    def test_19_fiche_membre(self):
        self.fichier("equipe/membres/ethan.md", MEMBRE)
        self.accepte(self.edit("equipe/membres/ethan.md", "statut: actif", "statut: en_integration"))

    def test_20_json_invalide(self):
        code, err = self.lancer(None, brut=b"{pas du json")
        self.assertEqual(code, 2)
        self.assertIn("par prudence", err)

    def test_21_chemin_windows_journal(self):
        self.fichier("docs/CHANGELOG-REGLES.md", DOC_VALIDE)  # en-tête VALIDÉ : seul l'exclusion R6 le sauve
        chemin = (self.racine + "\\DOCS\\changelog-regles.md").replace("/", "\\")
        if os.name != "nt":
            self.skipTest("chemins insensibles à la casse : Windows uniquement")
        self.accepte(self.edit(None, "Texte validé.", "Texte validé, ligne ajoutée.", chemin=chemin))


if __name__ == "__main__":
    unittest.main(verbosity=2)
