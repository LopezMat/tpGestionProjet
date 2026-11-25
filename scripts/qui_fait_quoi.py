#!/usr/bin/env python3
"""Génère une page HTML autonome « La maison de l'équipe » pour un projet.

Usage (depuis la racine du dépôt) :
    python3 scripts/qui_fait_quoi.py projets/<slug> [sortie.html]

Sortie par défaut : qui-fait-quoi.html à la racine du dépôt.

Sources :
- les tickets `projets/<slug>/tickets/T-*.md`, seule source de vérité des statuts (R9) ;
- `projets/<slug>/projet.md` et `TABLEAU.md` (généré par scripts/tableau.py) pour les chiffres ;
- `projets/<slug>/qui-fait-quoi.json`, l'instantané tenu par le coordinateur : qui travaille
  en ce moment, qui est attendu, ce qui vient de finir, l'étape de chaque ticket de l'incrément
  et les personnages. Le mettre à jour, puis relancer ce script.

La page est en lecture seule : elle n'écrit rien et ne modifie aucun ticket.
"""
import glob
import html
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ICI = Path(__file__).resolve().parent
LIB = {"TERMINE": "Terminé", "EN_COURS": "En cours", "EN_REVUE": "En revue", "A_FAIRE": "À faire",
       "ATTENTE_HUMAIN": "Attend un humain", "BLOQUE": "Bloqué", "ANNULE": "Annulé"}


def frontmatter(texte):
    d = {}
    for ligne in texte.split("---")[1].splitlines():
        m = re.match(r"^(\w+):\s*(.*?)\s*(#.*)?$", ligne)
        if m:
            d[m.group(1)] = m.group(2)
    return d


def lire_tickets(projet, sortie):
    tickets = []
    for f in sorted(glob.glob(str(projet / "tickets" / "T-*.md"))):
        brut = open(f, encoding="utf-8").read()
        d = frontmatter(brut)
        corps = re.sub(r"<!--.*?-->", "", brut.split("---", 2)[2], flags=re.S).strip()
        nature, qui = d["assigne"].split(":", 1)
        tickets.append({
            "id": d["id"], "titre": d["titre"], "type": d["type"], "statut": d["statut"],
            "priorite": d["priorite"], "qui": qui.capitalize() if nature == "salarie" else qui,
            "nature": "salarie" if nature == "salarie" else "agent",
            "est": float(d.get("estimation_h") or 0), "passe": float(d.get("temps_passe_h") or 0),
            "fichier": os.path.relpath(Path(f).resolve(), sortie.resolve().parent),
            "corps": corps, "depend_de": re.findall(r"T-\d{3}", d.get("depend_de", "")),
            "bloque_par": d.get("bloque_par", ""), "cree_le": d.get("cree_le", ""),
            "maj_le": d.get("maj_le", ""), "termine_le": d.get("termine_le", ""),
        })
    return tickets


def lire_synthese(projet):
    synthese = {}
    tableau = projet / "TABLEAU.md"
    if tableau.exists():
        for ligne in tableau.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\| (.+?) \| (.+?) \|$", ligne)
            if m:
                synthese[m.group(1)] = m.group(2)
    return synthese


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    projet = Path(sys.argv[1])
    sortie = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("qui-fait-quoi.html")
    instantane_f = projet / "qui-fait-quoi.json"
    if not instantane_f.exists():
        sys.exit(f"Instantané absent : {instantane_f}")
    inst = json.loads(instantane_f.read_text(encoding="utf-8"))

    tickets = lire_tickets(projet, sortie)
    p = frontmatter(open(projet / "projet.md", encoding="utf-8").read())
    synthese = lire_synthese(projet)

    donnees = {
        "tickets": tickets, "maintenant": inst.get("maintenant", []), "a_vous": inst.get("a_vous", []),
        "prochain": inst.get("recent", []), "etapes": inst["etapes"], "increment": inst["increment"],
        "equipe": inst["equipe"], "lib": LIB,
    }
    remplacements = {
        "{{CLIENT}}": html.escape(p.get("client", "Projet")),
        "{{GENERE}}": date.today().strftime("%d/%m/%Y"),
        "{{BUDGET}}": html.escape(synthese.get("Budget consommé / prévu", "—")),
        "{{FIN}}": html.escape(synthese.get("Fin projetée", "—")),
        "{{DEADLINE}}": html.escape(synthese.get("Deadline", p.get("deadline", "—"))),
        "{{PROJETE}}": html.escape(synthese.get("Coût projeté à terminaison (consommé + reste × taux)", "—")),
        "{{DONNEES}}": json.dumps(donnees, ensure_ascii=False).replace("</", "<\\/"),
    }
    page = (ICI / "qui_fait_quoi_modele.html").read_text(encoding="utf-8")
    for cle, val in remplacements.items():
        page = page.replace(cle, val)
    sortie.write_text(page, encoding="utf-8")
    print(f"{sortie} · {len(tickets)} tickets")


if __name__ == "__main__":
    main()
