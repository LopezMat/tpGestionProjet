#!/usr/bin/env python3
"""Bibliothèque commune de la production locale Docker (DEC-003).

Responsable : C · Lot 5 · voir docs/ARCHITECTURE.md § 9 et § 10, S3 § 6.
Utilisée par scripts/deployer_local.py et scripts/rollback_local.py ; jamais lancée seule.

- Docker : commande `docker`, ou, pour les tests, le faux Docker désigné par la variable
  d'environnement ESN_DOCKER_SIMULATION (chemin d'un script Python). Un agent ne peut pas
  la positionner : le hook restreindre_bash.py refuse tout préfixe VAR=… au deployeur.
- Données locales (ignorées par Git) : <racine>/deploiement/local/<slug>/
  sauvegardes/*.dump, historique.json, db_password.
- Fichier d'état de verifier-prod : un par vérification, horodaté, jamais réutilisé
  (sinon un état déjà conclu donnerait un faux « EN LIGNE » après un rollback).

Bibliothèque standard uniquement.
"""
import json
import os
import re
import secrets
import subprocess
import sys
import urllib.parse
from datetime import datetime

RACINE_ESN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPOSE = os.path.join(RACINE_ESN, "deploiement", "docker-compose.yml")
VERIFIER = os.path.join(RACINE_ESN, ".claude", "skills", "verifier-prod", "verifier_prod.py")

RE_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
RE_SHA = re.compile(r"^[0-9a-fA-F]{7,40}$")
HOTES_LOCAUX = {"localhost", "127.0.0.1", "::1"}
RETENTION = 10                       # sauvegardes gardées par projet (ARCHITECTURE § 10.2)
INTERVALLE_LOCAL = 5.0               # secondes entre deux sondes (ARCHITECTURE § 10.1)
TIMEOUT_LOCAL = 120.0                # délai global de vérification en local
RESULTAT_OK = "EN LIGNE ET À JOUR"


class Erreur(Exception):
    """Précondition ou usage : rien n'a été modifié (code 2)."""


def ecrire(texte=""):
    sys.stdout.buffer.write((texte + "\n").encode("utf-8"))
    sys.stdout.flush()


def maintenant():
    return datetime.now().astimezone()


# -- Git -----------------------------------------------------------------------

def git(racine, *args, **kw):
    return subprocess.run(["git", "-C", racine, *args], capture_output=True, **kw)


def resoudre_sha(racine, sha):
    if not RE_SHA.match(sha or ""):
        raise Erreur("SHA invalide (7 à 40 caractères hexadécimaux) : {}".format(sha))
    r = git(racine, "rev-parse", "--verify", "--quiet", sha.lower() + "^{commit}")
    complet = r.stdout.decode("utf-8", "replace").strip()
    if r.returncode != 0 or not re.match(r"^[0-9a-f]{40}$", complet):
        raise Erreur("SHA inconnu du dépôt : {}".format(sha))
    return complet


# -- Projet ----------------------------------------------------------------------

def verifier_slug(slug):
    if not RE_SLUG.match(slug or ""):
        raise Erreur("slug invalide (minuscules, chiffres, tirets) : {}".format(slug))


def lire_projet(racine, slug):
    """Champs `hebergement` et `url_prod` du frontmatter de projets/<slug>/projet.md."""
    chemin = os.path.join(racine, "projets", slug, "projet.md")
    try:
        with open(chemin, "r", encoding="utf-8-sig") as f:
            lignes = f.read().replace("\r\n", "\n").split("\n")
    except OSError:
        raise Erreur("projets/{}/projet.md introuvable".format(slug))
    champs = {}
    if lignes and lignes[0].strip() == "---":
        for ligne in lignes[1:]:
            if ligne.strip() == "---":
                break
            m = re.match(r"^([A-Za-z_]\w*)\s*:\s*(.*)$", ligne)
            if m:
                valeur = re.split(r"(?:^|\s)#", m.group(2), maxsplit=1)[0]
                champs[m.group(1).lower()] = valeur.strip().strip("'\"").strip()
    return champs


def url_locale(racine, slug):
    """Retourne (url_prod, port) ; production locale exigée (DEC-003, S3 § 6)."""
    champs = lire_projet(racine, slug)
    if champs.get("hebergement", "").lower() != "local":
        raise Erreur("projet.md : hebergement doit valoir « local » (lu : « {} ») ; "
                     "un autre hébergeur exige une décision humaine".format(champs.get("hebergement", "")))
    url = champs.get("url_prod", "")
    p = urllib.parse.urlparse(url)
    if p.scheme != "http" or (p.hostname or "").lower() not in HOTES_LOCAUX or not p.port:
        raise Erreur("projet.md : url_prod doit être http://localhost:<port> (lu : « {} »)".format(url))
    return url, p.port


# -- Docker ----------------------------------------------------------------------

def commande_docker():
    simulation = os.environ.get("ESN_DOCKER_SIMULATION")
    return [sys.executable, simulation] if simulation else ["docker"]


def docker(*args, env=None, **kw):
    kw.setdefault("stdout", subprocess.PIPE)
    kw.setdefault("stderr", subprocess.PIPE)
    try:
        return subprocess.run([*commande_docker(), *args], env=env, **kw)
    except FileNotFoundError:
        return subprocess.CompletedProcess(args, 127, b"", b"docker introuvable")


def docker_disponible():
    return docker("version", "--format", "{{.Server.Version}}").returncode == 0


def nom_projet(slug):
    return "esn-" + slug


def image(slug, sha):
    return "esn-{}:{}".format(slug, sha)


def image_existe(slug, sha):
    return docker("image", "inspect", image(slug, sha)).returncode == 0


def volume_existe(slug):
    return docker("volume", "inspect", nom_projet(slug) + "_pgdata").returncode == 0


def env_compose(slug, port, mot_de_passe, sha_image=None):
    env = dict(os.environ)
    env.update({"APP_PORT": str(port), "PG_PASSWORD": mot_de_passe,
                "APP_IMAGE": image(slug, sha_image) if sha_image else "esn-inconnu:aucune"})
    return env


def compose(slug, env, *args, **kw):
    return docker("compose", "-p", nom_projet(slug), "-f", COMPOSE, *args, env=env, **kw)


def construire(racine, slug, sha):
    """git archive <sha>:projets/<slug>/app | docker build … - ; retourne (code, message)."""
    source = "{}:projets/{}/app".format(sha, slug)
    archive = subprocess.Popen(["git", "-C", racine, "archive", "--format=tar", source],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        r = subprocess.run([*commande_docker(), "build", "-t", image(slug, sha),
                            "--build-arg", "GIT_COMMIT=" + sha,
                            "--label", "org.opencontainers.image.revision=" + sha, "-"],
                           stdin=archive.stdout, capture_output=True)
    except FileNotFoundError:
        archive.kill()
        return 127, "docker introuvable"
    finally:
        archive.stdout.close()
    err_git = archive.stderr.read().decode("utf-8", "replace")
    archive.stderr.close()
    if archive.wait() != 0:
        return 1, "git archive : " + err_git.strip()
    sortie = (r.stdout + r.stderr).decode("utf-8", "replace").strip().splitlines()
    return r.returncode, "\n".join(sortie[-15:])


# -- Données locales (ignorées par Git) ------------------------------------------

def dossier_local(racine, slug):
    return os.path.join(racine, "deploiement", "local", slug)


def relatif(racine, chemin):
    return os.path.relpath(chemin, racine).replace("\\", "/")


def mot_de_passe(racine, slug, creer):
    chemin = os.path.join(dossier_local(racine, slug), "db_password")
    if os.path.exists(chemin):
        with open(chemin, "r", encoding="utf-8") as f:
            return f.read().strip()
    if not creer:
        raise Erreur("mot de passe de la base introuvable ({}) : aucun déploiement local "
                     "connu pour ce projet".format(relatif(racine, chemin)))
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    valeur = secrets.token_urlsafe(24)
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(valeur + "\n")
    try:
        os.chmod(chemin, 0o600)
    except OSError:
        pass
    return valeur


def charger_historique(racine, slug):
    chemin = os.path.join(dossier_local(racine, slug), "historique.json")
    if not os.path.exists(chemin):
        return []
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def ajouter_historique(racine, slug, entree):
    historique = charger_historique(racine, slug)
    historique.append(entree)
    os.makedirs(dossier_local(racine, slug), exist_ok=True)
    with open(os.path.join(dossier_local(racine, slug), "historique.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)
        f.write("\n")


def derniere_version_verifiee(historique):
    for e in reversed(historique):
        if e.get("resultat") == RESULTAT_OK:
            return e.get("sha")
    return None


def dernier_deploiement(historique):
    for e in reversed(historique):
        if e.get("type") == "deploiement":
            return e
    return None


def sauvegardes(racine, slug):
    dossier = os.path.join(dossier_local(racine, slug), "sauvegardes")
    if not os.path.isdir(dossier):
        return []
    return sorted(os.path.join(dossier, n) for n in os.listdir(dossier) if n.endswith(".dump"))


def purger_sauvegardes(racine, slug, garder=RETENTION):
    """Garde les `garder` dernières sauvegardes ; retourne les chemins supprimés."""
    liste = sauvegardes(racine, slug)
    supprimees = liste[:-garder] if len(liste) > garder else []
    for chemin in supprimees:
        os.remove(chemin)
    return supprimees


# -- Vérification en ligne -------------------------------------------------------

def chemin_etat(racine, slug, sha):
    """projets/<slug>/rapports/verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json, jamais réutilisé."""
    dossier = os.path.join(racine, "projets", slug, "rapports")
    base = "verifier-prod-{}-{}".format(sha[:7], maintenant().strftime("%Y%m%d-%H%M%S"))
    chemin, n = os.path.join(dossier, base + ".json"), 2
    while os.path.exists(chemin):
        chemin, n = os.path.join(dossier, "{}-{}.json".format(base, n)), n + 1
    return chemin


def verifier(racine, url, sha, etat, intervalle, timeout):
    """Lance verifier_prod.py, recopie sa sortie ; retourne (code, commande à relancer)."""
    options = ["--intervalle", "{:g}".format(intervalle), "--timeout", "{:g}".format(timeout)]
    r = subprocess.run([sys.executable, VERIFIER, "--url", url, "--sha", sha, "--etat", etat, *options],
                       capture_output=True)
    for ligne in r.stdout.decode("utf-8", "replace").rstrip("\n").split("\n"):
        ecrire(ligne)
    commande = "python .claude/skills/verifier-prod/verifier_prod.py --url {} --sha {} --etat {} {}".format(
        url, sha, relatif(racine, etat), " ".join(options))
    return r.returncode, commande
