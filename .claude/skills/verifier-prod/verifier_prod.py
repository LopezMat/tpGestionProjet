#!/usr/bin/env python3
"""verifier-prod : sonde <url>/health jusqu'à ce que le SHA en ligne soit le SHA attendu.

Responsable : C · Lot 2 (C) · voir S3-R5, R13, ARCHITECTURE § 9 et § 10.1.

Chaque appel sonde au plus --max-appel secondes (sous la limite de 10 min de l'outil Bash),
puis rend la main avec le code 3 ; l'état (début, tentatives) est gardé dans --etat,
si bien que le délai --timeout est global, quel que soit le nombre d'appels.

Codes de sortie :
  0  EN LIGNE ET À JOUR (SHA renvoyé = SHA attendu)
  1  ÉCHEC (délai global dépassé sans concordance)
  2  erreur d'usage (URL, SHA, fichier d'état)
  3  EN COURS : relancer la même commande

Sortie : les lignes du tableau « Vérification en ligne » de templates/rapport-deploiement.md,
puis une ligne `RESULTAT: ...`. Bibliothèque standard uniquement.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

RE_SHA = re.compile(r"^[0-9a-f]{7,40}$")
HOTES_LOCAUX = {"localhost", "127.0.0.1", "::1"}


def ecrire(texte):
    sys.stdout.buffer.write((texte + "\n").encode("utf-8"))
    sys.stdout.flush()


def url_sante(url):
    return url.rstrip("/") + "/health"


def sonder(url, delai_reseau):
    """Retourne (code_http, sha_renvoye, resultat_brut)."""
    req = urllib.request.Request(url, headers={"User-Agent": "esn-verifier-prod",
                                               "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=delai_reseau) as rep:
            code, corps = rep.status, rep.read(65536)
    except urllib.error.HTTPError as e:
        return e.code, "", "HTTP_{}".format(e.code)
    except Exception:
        return None, "", "INJOIGNABLE"
    try:
        donnees = json.loads(corps.decode("utf-8"))
        sha = str(donnees.get("commit") or donnees.get("sha") or "").strip().lower()
    except Exception:
        return code, "", "JSON_INVALIDE"
    return code, sha, None


def comparer(sha_renvoye, attendu):
    """'OK', 'OK (préfixe)' ou 'SHA_DIFFERENT'."""
    if not sha_renvoye:
        return "SHA_DIFFERENT"
    if sha_renvoye == attendu:
        return "OK"
    if len(sha_renvoye) >= 7 and len(attendu) >= 7 and (
            attendu.startswith(sha_renvoye) or sha_renvoye.startswith(attendu)):
        return "OK (préfixe)"
    return "SHA_DIFFERENT"


def charger_etat(chemin, url, sha):
    if chemin and os.path.exists(chemin):
        with open(chemin, "r", encoding="utf-8") as f:
            etat = json.load(f)
        if etat.get("url") != url or etat.get("sha_attendu") != sha:
            raise ValueError("le fichier d'état concerne une autre URL ou un autre SHA : "
                             "supprime-le ou choisis un autre --etat")
        return etat
    return {"url": url, "sha_attendu": sha, "debut": time.time(), "tentatives": [], "resultat": None}


def sauver_etat(chemin, etat):
    if not chemin:
        return
    dossier = os.path.dirname(os.path.abspath(chemin))
    os.makedirs(dossier, exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        json.dump(etat, f, ensure_ascii=False, indent=2)
        f.write("\n")


def afficher(etat, mode, resultat):
    ecrire("Mode : {} · URL : {} · SHA attendu : {}".format(mode, url_sante(etat["url"]), etat["sha_attendu"]))
    ecrire("")
    ecrire("| Tentative | Heure | Code HTTP | SHA renvoyé | Résultat |")
    ecrire("|---|---|---|---|---|")
    for t in etat["tentatives"]:
        ecrire("| {n} | {h} | {c} | {s} | {r} |".format(
            n=t["n"], h=t["heure"], c=t["code"] if t["code"] is not None else "—",
            s=(t["sha"][:12] if t["sha"] else "—"), r=t["resultat"]))
    ecrire("")
    ecrire("RESULTAT: " + resultat)


def main(argv=None):
    p = argparse.ArgumentParser(description="Vérifie que <url>/health renvoie le SHA attendu.")
    p.add_argument("--url", required=True, help="url_prod de projet.md (sans /health)")
    p.add_argument("--sha", required=True, help="SHA attendu (7 à 40 caractères hexadécimaux)")
    p.add_argument("--etat", default="", help="fichier JSON d'état (reprise entre appels)")
    p.add_argument("--intervalle", type=float, default=30.0, help="secondes entre deux tentatives")
    p.add_argument("--timeout", type=float, default=900.0, help="délai global en secondes")
    p.add_argument("--max-appel", type=float, default=540.0, help="durée maximale d'un appel en secondes")
    p.add_argument("--delai-reseau", type=float, default=20.0, help="timeout d'une requête en secondes")
    a = p.parse_args(argv)

    sha = a.sha.strip().lower()
    parse = urllib.parse.urlparse(a.url.strip())
    if parse.scheme not in ("http", "https") or not parse.hostname:
        ecrire("ERREUR: URL invalide (http ou https attendu) : {}".format(a.url))
        return 2
    if not RE_SHA.match(sha):
        ecrire("ERREUR: SHA invalide (7 à 40 caractères hexadécimaux) : {}".format(a.sha))
        return 2
    mode = "local" if parse.hostname.lower() in HOTES_LOCAUX else "distant"
    url = a.url.strip()

    try:
        etat = charger_etat(a.etat, url, sha)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        ecrire("ERREUR: fichier d'état : {}".format(e))
        return 2

    if etat.get("resultat") in ("EN LIGNE ET À JOUR", "ÉCHEC"):
        afficher(etat, mode, etat["resultat"])
        return 0 if etat["resultat"] == "EN LIGNE ET À JOUR" else 1

    debut_appel = time.time()
    while True:
        code, sha_renvoye, erreur = sonder(url_sante(url), a.delai_reseau)
        resultat = erreur or comparer(sha_renvoye, sha)
        etat["tentatives"].append({
            "n": len(etat["tentatives"]) + 1,
            "heure": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "code": code, "sha": sha_renvoye, "resultat": resultat})
        if resultat.startswith("OK"):
            etat["resultat"] = "EN LIGNE ET À JOUR"
            sauver_etat(a.etat, etat)
            afficher(etat, mode, etat["resultat"])
            return 0
        maintenant = time.time()
        if maintenant - etat["debut"] + a.intervalle > a.timeout:
            etat["resultat"] = "ÉCHEC"
            sauver_etat(a.etat, etat)
            afficher(etat, mode, "ÉCHEC (délai global de {:.0f} s dépassé)".format(a.timeout))
            return 1
        if maintenant - debut_appel + a.intervalle > a.max_appel:
            sauver_etat(a.etat, etat)
            afficher(etat, mode, "EN COURS (relancer la même commande)")
            return 3
        sauver_etat(a.etat, etat)
        time.sleep(a.intervalle)


if __name__ == "__main__":
    sys.exit(main())
