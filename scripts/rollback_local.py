#!/usr/bin/env python3
"""Rollback en production locale Docker : relance l'image étiquetée du SHA précédent (porte 8 de S3).

Responsable : C · Lot 5 · voir S3-R6, S2-R7, ARCHITECTURE § 10.3, runbook rollback, DEC-003.

Usage (racine du dépôt) :
  python scripts/rollback_local.py --projet <slug>               # après un déploiement en ÉCHEC
  python scripts/rollback_local.py --projet <slug> --sha <sha>   # cible explicite

- Cible par défaut : la version précédente du dernier déploiement, seulement si celui-ci
  n'a pas été vérifié (S3-R6). Revenir sur un déploiement vérifié est une décision humaine
  (S2-R7) : --sha est alors obligatoire.
- L'image esn-<slug>:<sha> doit exister en local : elle est relancée SANS rebuild ni
  git revert ; elle porte son SHA dans GIT_COMMIT (build-arg), donc /health dit la vérité.
- Aucune restauration de base : le chemin de la dernière sauvegarde est affiché pour
  information ; restaurer des données est une décision humaine (deployeur, règle 5).
- Puis verifier-prod, sur un fichier d'état neuf.

Codes de sortie :
  0  version restaurée, EN LIGNE ET À JOUR
  1  vérification en ÉCHEC après le rollback : crise (runbook coupure-serveur)
  2  précondition ou usage : rien n'a changé
  3  vérification EN COURS : relancer la commande verifier_prod affichée

Toute exécution demande une confirmation humaine (ask). Bibliothèque standard uniquement.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prod_locale as pl  # noqa: E402


def cible(racine, slug, historique, sha_demande):
    if sha_demande:
        return pl.resoudre_sha(racine, sha_demande)
    dernier = pl.dernier_deploiement(historique)
    if dernier is None:
        raise pl.Erreur("aucun déploiement local connu pour {} : rien à annuler".format(slug))
    if dernier.get("resultat") == pl.RESULTAT_OK:
        raise pl.Erreur("le dernier déploiement ({}) a été vérifié EN LIGNE ET À JOUR : revenir "
                        "dessus est une décision humaine (S2-R7). Relancer avec --sha <sha> après "
                        "la décision".format(dernier["sha"][:7]))
    if dernier.get("resultat") in ("SAUVEGARDE_ECHEC", "BUILD_ECHEC"):
        raise pl.Erreur("le dernier déploiement s'est arrêté avant le lancement ({}) : la "
                        "production n'a pas changé, rien à annuler".format(dernier["resultat"]))
    if not dernier.get("version_precedente"):
        raise pl.Erreur("aucune version précédente vérifiée : premier déploiement, pas de rollback "
                        "possible (crise : runbook coupure-serveur)")
    return dernier["version_precedente"]


def rollback(a):
    racine = os.path.abspath(a.racine)
    pl.verifier_slug(a.projet)
    slug = a.projet
    url, port = pl.url_locale(racine, slug)
    historique = pl.charger_historique(racine, slug)
    sha = cible(racine, slug, historique, a.sha)
    if not pl.docker_disponible():
        raise pl.Erreur("Docker ne répond pas : démarrer Docker Desktop (ou le démon), puis relancer")
    if not pl.image_existe(slug, sha):
        raise pl.Erreur("image {} absente en local : rollback immédiat impossible ; les humains "
                        "décident (nouveau GO sur ce SHA, ou crise)".format(pl.image(slug, sha)))
    env = pl.env_compose(slug, port, pl.mot_de_passe(racine, slug, creer=False), sha)
    dernier = pl.dernier_deploiement(historique)

    pl.ecrire("PROJET: {} · URL: {}".format(slug, url))
    pl.ecrire("VERSION_REFUSEE: {}".format(dernier["sha"] if dernier else "inconnue"))
    pl.ecrire("VERSION_RESTAUREE: {}".format(sha))
    pl.ecrire("IMAGE: {} (relancée sans rebuild)".format(pl.image(slug, sha)))
    dumps = pl.sauvegardes(racine, slug)
    pl.ecrire("DERNIERE_SAUVEGARDE: {} (non restaurée : décision humaine, deployeur règle 5)".format(
        pl.relatif(racine, dumps[-1]) if dumps else "aucune"))

    r = pl.compose(slug, env, "up", "-d")
    pl.ecrire("LANCEMENT: " + ("OK" if r.returncode == 0 else "ÉCHEC ({})".format(
        r.stderr.decode("utf-8", "replace").strip()[-300:])))

    etat = pl.chemin_etat(racine, slug, sha)
    entree = {"type": "rollback", "sha": sha, "date": pl.maintenant().isoformat(timespec="seconds"),
              "version_refusee": dernier["sha"] if dernier else None,
              "etat": pl.relatif(racine, etat), "resultat": None}
    pl.ecrire("ETAT_VERIFICATION: " + entree["etat"])
    pl.ecrire()
    code, commande = pl.verifier(racine, url, sha, etat, a.intervalle, a.timeout)
    entree["resultat"] = {0: pl.RESULTAT_OK, 1: "ÉCHEC", 3: "EN COURS"}.get(code, "ERREUR_VERIFICATION")
    pl.ajouter_historique(racine, slug, entree)
    if code == 3:
        pl.ecrire("SUITE: relancer exactement : " + commande)
    elif code == 1:
        pl.ecrire("SUITE: rollback non vérifié : crise, runbook coupure-serveur, escalade humaine")
    elif code != 0:
        pl.ecrire("SUITE: erreur d'usage de verifier_prod (code {}) ; ne jamais conclure".format(code))
        return 2
    return code


def main(argv=None):
    p = argparse.ArgumentParser(description="Rollback en production locale Docker (DEC-003).")
    p.add_argument("--projet", required=True, help="slug du projet (projets/<slug>/)")
    p.add_argument("--sha", default="", help="SHA à restaurer (défaut : version précédente du dernier "
                                             "déploiement en échec)")
    p.add_argument("--racine", default=pl.RACINE_ESN, help=argparse.SUPPRESS)
    p.add_argument("--intervalle", type=float, default=pl.INTERVALLE_LOCAL, help=argparse.SUPPRESS)
    p.add_argument("--timeout", type=float, default=pl.TIMEOUT_LOCAL, help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    try:
        return rollback(a)
    except pl.Erreur as e:
        pl.ecrire("ERREUR: {}".format(e))
        pl.ecrire("RESULTAT: AUCUN ROLLBACK EFFECTUÉ")
        return 2


if __name__ == "__main__":
    sys.exit(main())
