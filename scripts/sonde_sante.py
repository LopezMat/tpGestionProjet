#!/usr/bin/env python3
"""sonde_sante : mesure la disponibilité, la version et le temps de réponse de <url>/health.

Responsable : D · Lot 2 (D) · voir S2 § 3 (sources réelles), agents analyste-prod et
gestionnaire-crise, runbooks/.

Réutilise le contrat /health de verifier-prod (fonctions url_sante, sonder, comparer de
.claude/skills/verifier-prod/verifier_prod.py) : une seule implémentation du format
{"status": "ok", "commit": "<sha>"}. Ajoute plusieurs mesures espacées et le temps de
réponse. N'écrit AUCUN fichier : la sortie va sur stdout uniquement.

Codes de sortie :
  0  DISPONIBLE ET À JOUR (ou DISPONIBLE si aucun --sha n'est fourni)
  1  anomalie : SHA DIFFÉRENT, DÉGRADÉ (lent) ou disponibilité partielle
  2  erreur d'usage (URL, SHA, paramètres)
  4  INDISPONIBLE : aucune mesure n'a obtenu de réponse valide

Bibliothèque standard uniquement.
"""
import argparse
import importlib.util
import os
import re
import statistics
import sys
import time
import urllib.parse
from datetime import datetime

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEMIN_VP = os.path.join(RACINE, ".claude", "skills", "verifier-prod", "verifier_prod.py")
RE_SHA = re.compile(r"^[0-9a-f]{7,40}$")
DUREE_MAX_S = 540  # sous la limite de 10 min de l'outil Bash


def charger_verifier_prod():
    sys.dont_write_bytecode = True  # pas de __pycache__ dans .claude/skills/verifier-prod/
    spec = importlib.util.spec_from_file_location("verifier_prod", CHEMIN_VP)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ecrire(texte):
    sys.stdout.buffer.write((texte + "\n").encode("utf-8"))
    sys.stdout.flush()


def main(argv=None):
    p = argparse.ArgumentParser(description="Mesure <url>/health : disponibilité, SHA, temps de réponse.")
    p.add_argument("--url", required=True, help="url_prod de projet.md (sans /health)")
    p.add_argument("--sha", default="", help="SHA attendu (7 à 40 caractères hexadécimaux), facultatif")
    p.add_argument("--mesures", type=int, default=3, help="nombre de mesures (1 à 20)")
    p.add_argument("--intervalle", type=float, default=10.0, help="secondes entre deux mesures")
    p.add_argument("--seuil-ms", type=float, default=2000.0, help="médiane au-delà de laquelle le service est DÉGRADÉ")
    p.add_argument("--delai-reseau", type=float, default=20.0, help="timeout d'une requête en secondes")
    a = p.parse_args(argv)

    url = a.url.strip()
    parse = urllib.parse.urlparse(url)
    if parse.scheme not in ("http", "https") or not parse.hostname:
        ecrire("ERREUR: URL invalide (http ou https attendu) : {}".format(a.url))
        return 2
    sha = a.sha.strip().lower()
    if sha and not RE_SHA.match(sha):
        ecrire("ERREUR: SHA invalide (7 à 40 caractères hexadécimaux) : {}".format(a.sha))
        return 2
    if not 1 <= a.mesures <= 20 or a.intervalle < 0 or a.seuil_ms <= 0 or a.delai_reseau <= 0:
        ecrire("ERREUR: paramètres invalides (--mesures 1 à 20, --intervalle ≥ 0, --seuil-ms et --delai-reseau > 0)")
        return 2
    if (a.mesures - 1) * a.intervalle + a.mesures * a.delai_reseau > DUREE_MAX_S:
        ecrire("ERREUR: durée maximale dépassée ({} s) : réduire --mesures, --intervalle ou --delai-reseau".format(DUREE_MAX_S))
        return 2

    try:
        vp = charger_verifier_prod()
    except Exception as exc:  # script de C introuvable ou cassé
        ecrire("ERREUR: impossible de charger {} ({})".format(CHEMIN_VP, exc))
        return 2

    cible = vp.url_sante(url)
    lignes, temps_ok, nb_ok, shas = [], [], 0, set()
    for n in range(1, a.mesures + 1):
        debut = time.perf_counter()
        code, sha_renvoye, erreur = vp.sonder(cible, a.delai_reseau)
        ms = (time.perf_counter() - debut) * 1000.0
        if erreur:
            resultat = erreur
        elif sha:
            resultat = vp.comparer(sha_renvoye, sha)
        else:
            resultat = "DISPONIBLE" if code is not None and 200 <= code < 300 else "HTTP_{}".format(code)
        repondu = erreur is None and code is not None and 200 <= code < 300
        if repondu:
            nb_ok += 1
            temps_ok.append(ms)
            shas.add(sha_renvoye)
        lignes.append("| {n} | {h} | {c} | {s} | {t:.0f} | {r} |".format(
            n=n, h=datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            c=code if code is not None else "—", s=(sha_renvoye[:12] if sha_renvoye else "—"),
            t=ms, r=resultat))
        if n < a.mesures:
            time.sleep(a.intervalle)

    ecrire("Mode : {} · URL : {} · SHA attendu : {}".format(
        "local" if parse.hostname.lower() in vp.HOTES_LOCAUX else "distant", cible, sha or "(non fourni)"))
    ecrire("")
    ecrire("| Mesure | Heure | Code HTTP | SHA renvoyé | Temps (ms) | Résultat |")
    ecrire("|---|---|---|---|---|---|")
    for ligne in lignes:
        ecrire(ligne)
    ecrire("")

    mediane = statistics.median(temps_ok) if temps_ok else None
    ecrire("Disponibilité : {}/{}".format(nb_ok, a.mesures))
    if temps_ok:
        ecrire("Temps de réponse : médiane {:.0f} ms · maximum {:.0f} ms (seuil {:.0f} ms)".format(
            mediane, max(temps_ok), a.seuil_ms))

    if nb_ok == 0:
        ecrire("RESULTAT: INDISPONIBLE")
        return 4
    version_ok = None
    if sha:
        version_ok = all(vp.comparer(s, sha).startswith("OK") for s in shas)
        ecrire("Version : {}".format("concordante" if version_ok else "DIFFÉRENTE ({})".format(
            ", ".join(sorted(s[:12] or "—" for s in shas)))))
    if version_ok is False:
        ecrire("RESULTAT: SHA DIFFÉRENT")
        return 1
    if mediane is not None and mediane > a.seuil_ms:
        ecrire("RESULTAT: DÉGRADÉ (lent)")
        return 1
    if nb_ok < a.mesures:
        ecrire("RESULTAT: DÉGRADÉ (disponibilité partielle)")
        return 1
    ecrire("RESULTAT: " + ("DISPONIBLE ET À JOUR" if sha else "DISPONIBLE"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
