#!/usr/bin/env python3
"""Contrôle CI des validations humaines (ARCHITECTURE § 6, garde-fous 3, 4 et 5 ; R5, R6).

Responsable : C · Lot 5 · lancé par .github/workflows/validations.yml, voir DEC-001 § 7 et § 23, DEC-003.

C'est le filet derrière le hook proteger_valide.py : il voit aussi les écritures faites
hors des outils Write/Edit (Bash `sed -i`, redirection, éditeur, autre poste).

Un « document » est un fichier Markdown dont le frontmatter porte `valide_par` et qui
n'est pas un ticket (`id: T-NNN`). Pour chaque document :
  - statut normalisé (accents retirés, majuscules) dans BROUILLON, EN_REVUE, VALIDE ;
  - s'il est VALIDÉ : `valide_par` rempli, `decision: DEC-NNN` bien formé, et un fichier
    docs/decisions/*-DEC-NNN-*.md qui existe ;
  - un journal (CHANGELOG-REGLES, registre des décisions) n'est jamais VALIDÉ.
La lecture de l'en-tête et la normalisation sont celles du hook (même code, importé) :
le hook et la CI ne peuvent pas diverger (garde-fou 5).

Parcours : tous les .md du dépôt, sauf .git/ et le code des apps clientes (projets/*/app/).
Usage : python scripts/verifier_validations.py [--racine <dossier>]
Codes : 0 = conforme ; 1 = anomalies (listées) ; 2 = erreur d'usage.
Bibliothèque standard uniquement.
"""
import argparse
import importlib.util
import os
import re
import sys

RACINE_ESN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUTS = {"BROUILLON", "EN_REVUE", "VALIDE"}
RE_DEC = re.compile(r"^DEC-\d{3,}$")
EXCLUS = re.compile(r"^(\.git/|projets/[^/]+/app/)")


def charger_hook():
    chemin = os.path.join(RACINE_ESN, ".claude", "hooks", "proteger_valide.py")
    spec = importlib.util.spec_from_file_location("proteger_valide", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HOOK = charger_hook()


def fichiers_md(racine):
    for dossier, sous, fichiers in os.walk(racine):
        rel_dossier = os.path.relpath(dossier, racine).replace("\\", "/")
        rel_dossier = "" if rel_dossier == "." else rel_dossier + "/"
        sous[:] = sorted(d for d in sous if not EXCLUS.match(rel_dossier + d + "/"))
        for nom in sorted(fichiers):
            if nom.lower().endswith(".md"):
                yield rel_dossier + nom


def decisions_existantes(racine):
    dossier = os.path.join(racine, "docs", "decisions")
    ids = set()
    if os.path.isdir(dossier):
        for nom in os.listdir(dossier):
            m = re.match(r"^\d{4}-\d{2}-\d{2}-(DEC-\d{3,})-.+\.md$", nom)
            if m:
                ids.add(m.group(1))
    return ids


def controler(racine):
    """Retourne (nombre de documents contrôlés, liste d'anomalies 'fichier : message')."""
    anomalies, documents = [], 0
    decisions = decisions_existantes(racine)
    for rel in fichiers_md(racine):
        texte = HOOK.lire_fichier(os.path.join(racine, rel))
        entete = HOOK.lire_entete(texte)
        if entete is None or "valide_par" not in entete or HOOK.est_ticket(entete):
            continue
        documents += 1
        statut = HOOK.normaliser(entete.get("statut"))
        if statut not in STATUTS:
            anomalies.append("{} : statut « {} » hors de BROUILLON, EN_REVUE, VALIDÉ (garde-fou 5)".format(
                rel, entete.get("statut", "")))
            continue
        if statut != "VALIDE":
            continue
        if rel.lower() in HOOK.JOURNAUX:
            anomalies.append("{} : un journal ne passe jamais VALIDÉ (R6, DEC-001 § 24)".format(rel))
            continue
        if not entete.get("valide_par"):
            anomalies.append("{} : VALIDÉ sans valide_par (R5, garde-fou 3)".format(rel))
        decision = entete.get("decision", "")
        if not RE_DEC.match(decision):
            anomalies.append("{} : VALIDÉ sans decision: DEC-NNN valide (lu : « {} ») (R5, garde-fou 3)".format(
                rel, decision))
        elif decision not in decisions:
            anomalies.append("{} : {} ne correspond à aucun fichier de docs/decisions/ (garde-fou 4)".format(
                rel, decision))
    return documents, anomalies


def ecrire(texte):
    sys.stdout.buffer.write((texte + "\n").encode("utf-8"))


def main(argv=None):
    p = argparse.ArgumentParser(description="Contrôle VALIDÉ ⇔ valide_par + decision existante.")
    p.add_argument("--racine", default=RACINE_ESN, help="racine du dépôt (défaut : parent de scripts/)")
    a = p.parse_args(argv)
    if not os.path.isdir(a.racine):
        ecrire("ERREUR: racine introuvable : {}".format(a.racine))
        return 2
    documents, anomalies = controler(os.path.abspath(a.racine))
    for ligne in anomalies:
        ecrire("ANOMALIE: " + ligne)
    ecrire("{} document(s) contrôlé(s), {} anomalie(s).".format(documents, len(anomalies)))
    return 1 if anomalies else 0


if __name__ == "__main__":
    sys.exit(main())
