#!/usr/bin/env python3
"""Déploiement en production locale Docker d'un SHA approuvé (portes 5 à 7 de S3, DEC-003).

Responsable : C · Lot 5 · voir S3 § 3 et § 6, ARCHITECTURE § 9 et § 10, agent deployeur.

Usage (racine du dépôt) :
  python scripts/deployer_local.py --projet <slug> --sha <sha du GO>

Étapes :
  1. préconditions : Docker répond, SHA connu, Dockerfile présent au SHA,
     projet.md avec hebergement: local et url_prod http://localhost:<port> ;
  2. version précédente : dernier SHA vérifié de l'historique local ;
  3. sauvegarde pg_dump horodatée (deploiement/local/<slug>/sauvegardes/, ignoré par Git),
     rétention des 10 dernières ; « aucune » seulement à la première mise en service ;
  4. build de l'image esn-<slug>:<sha40> à partir du commit (git archive), jamais de
     l'arbre de travail ; GIT_COMMIT est figé dans l'image (build-arg) ;
  5. lancement par docker compose (deploiement/docker-compose.yml) ;
  6. verifier-prod sur un fichier d'état neuf : /health doit renvoyer le SHA attendu.

Codes de sortie :
  0  EN LIGNE ET À JOUR
  1  ÉCHEC après le lancement : lancer scripts/rollback_local.py (S3-R6)
  2  précondition ou usage : rien n'a changé
  3  vérification EN COURS : relancer la commande verifier_prod affichée
  4  sauvegarde en échec : rien n'a changé
  5  build en échec : production inchangée

Toute exécution demande une confirmation humaine (règle ask de settings.json, doublée par
le hook restreindre_bash.py). Bibliothèque standard uniquement.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prod_locale as pl  # noqa: E402


def sauvegarder(racine, slug, env, precedente):
    """Retourne (code, ligne SAUVEGARDE) ; code 0 si sauvegarde faite ou sans objet."""
    if not pl.volume_existe(slug):
        return 0, "aucune (première mise en service, aucune base existante)"
    r = pl.compose(slug, env, "up", "-d", "--wait", "db")
    if r.returncode != 0:
        return 4, "ÉCHEC : la base ne démarre pas ({})".format(
            r.stderr.decode("utf-8", "replace").strip()[-300:])
    dossier = os.path.join(pl.dossier_local(racine, slug), "sauvegardes")
    os.makedirs(dossier, exist_ok=True)
    nom = "{}-{}.dump".format(pl.maintenant().strftime("%Y%m%d-%H%M%S"),
                              (precedente or "aucune")[:7])
    chemin = os.path.join(dossier, nom)
    with open(chemin, "wb") as f:
        r = pl.compose(slug, env, "exec", "-T", "db", "pg_dump", "-U", "esn", "-d", "app", "-Fc",
                       stdout=f)
    if r.returncode != 0 or os.path.getsize(chemin) == 0:
        os.remove(chemin)
        return 4, "ÉCHEC : pg_dump a rendu le code {} ou un fichier vide".format(r.returncode)
    for ancien in pl.purger_sauvegardes(racine, slug):
        pl.ecrire("Rétention : sauvegarde supprimée {}".format(pl.relatif(racine, ancien)))
    return 0, "{} ({} octets)".format(pl.relatif(racine, chemin), os.path.getsize(chemin))


def deployer(a):
    racine = os.path.abspath(a.racine)
    pl.verifier_slug(a.projet)
    slug = a.projet
    url, port = pl.url_locale(racine, slug)
    sha = pl.resoudre_sha(racine, a.sha)
    if pl.git(racine, "cat-file", "-e", "{}:projets/{}/app/Dockerfile".format(sha, slug)).returncode != 0:
        raise pl.Erreur("projets/{}/app/Dockerfile absent au SHA {} (contrat de l'app, "
                        "ARCHITECTURE § 9)".format(slug, sha[:7]))
    if not pl.docker_disponible():
        raise pl.Erreur("Docker ne répond pas : démarrer Docker Desktop (ou le démon), puis relancer")

    historique = pl.charger_historique(racine, slug)
    precedente = pl.derniere_version_verifiee(historique)
    # Base existante sans mot de passe local : on ne le régénère pas (la base le refuserait).
    env = pl.env_compose(slug, port, pl.mot_de_passe(racine, slug, creer=not pl.volume_existe(slug)), sha)
    entree = {"type": "deploiement", "sha": sha, "date": pl.maintenant().isoformat(timespec="seconds"),
              "version_precedente": precedente, "sauvegarde": None, "etat": None, "resultat": None}

    pl.ecrire("PROJET: {} · URL: {}".format(slug, url))
    pl.ecrire("SHA_ATTENDU: {}".format(sha))
    pl.ecrire("VERSION_PRECEDENTE: {}".format(precedente or "aucune"))

    # Porte 5 : sauvegarde (S3-R4)
    code, ligne = sauvegarder(racine, slug, env, precedente)
    pl.ecrire("SAUVEGARDE: " + ligne)
    if code:
        entree["resultat"] = "SAUVEGARDE_ECHEC"
        pl.ajouter_historique(racine, slug, entree)
        pl.ecrire("RESULTAT: ÉCHEC DE LA SAUVEGARDE, rien n'a été déployé (S3-R4)")
        return 4
    entree["sauvegarde"] = ligne

    # Porte 6 : build au SHA exact, puis lancement
    if pl.image_existe(slug, sha):
        pl.ecrire("IMAGE: {} (déjà construite)".format(pl.image(slug, sha)))
    else:
        code, sortie = pl.construire(racine, slug, sha)
        if code != 0:
            entree["resultat"] = "BUILD_ECHEC"
            pl.ajouter_historique(racine, slug, entree)
            pl.ecrire(sortie)
            pl.ecrire("RESULTAT: ÉCHEC DU BUILD, production inchangée")
            return 5
        pl.ecrire("IMAGE: {} (construite)".format(pl.image(slug, sha)))
    r = pl.compose(slug, env, "up", "-d")
    if r.returncode != 0:
        pl.ecrire("LANCEMENT: ÉCHEC ({})".format(r.stderr.decode("utf-8", "replace").strip()[-300:]))
    else:
        pl.ecrire("LANCEMENT: OK (docker compose -p {} up -d)".format(pl.nom_projet(slug)))

    # Porte 7 : vérification en ligne (S3-R5)
    etat = pl.chemin_etat(racine, slug, sha)
    entree["etat"] = pl.relatif(racine, etat)
    pl.ecrire("ETAT_VERIFICATION: " + entree["etat"])
    pl.ecrire()
    code, commande = pl.verifier(racine, url, sha, etat, a.intervalle, a.timeout)
    entree["resultat"] = {0: pl.RESULTAT_OK, 1: "ÉCHEC", 3: "EN COURS"}.get(code, "ERREUR_VERIFICATION")
    pl.ajouter_historique(racine, slug, entree)
    if code == 0:
        return 0
    if code == 3:
        pl.ecrire("SUITE: relancer exactement : " + commande)
        return 3
    if code == 1:
        pl.ecrire("SUITE: rollback (S3-R6) : python scripts/rollback_local.py --projet {}".format(slug))
        return 1
    pl.ecrire("SUITE: erreur d'usage de verifier_prod (code {}) ; ne jamais conclure".format(code))
    return 2


def main(argv=None):
    p = argparse.ArgumentParser(description="Déploie un SHA en production locale Docker (DEC-003).")
    p.add_argument("--projet", required=True, help="slug du projet (projets/<slug>/)")
    p.add_argument("--sha", required=True, help="SHA cité par la décision GO")
    p.add_argument("--racine", default=pl.RACINE_ESN, help=argparse.SUPPRESS)
    p.add_argument("--intervalle", type=float, default=pl.INTERVALLE_LOCAL, help=argparse.SUPPRESS)
    p.add_argument("--timeout", type=float, default=pl.TIMEOUT_LOCAL, help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    try:
        return deployer(a)
    except pl.Erreur as e:
        pl.ecrire("ERREUR: {}".format(e))
        pl.ecrire("RESULTAT: RIEN N'A ÉTÉ DÉPLOYÉ")
        return 2


if __name__ == "__main__":
    sys.exit(main())
