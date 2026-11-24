#!/usr/bin/env python3
"""Faux Docker pour scripts/test_prod_locale.py (simulation, sans Docker). Responsable : C · Lot 5.

Désigné par la variable ESN_DOCKER_SIMULATION ; son état (images, image lancée, volumes,
pannes programmées) est un JSON désigné par ESN_DOCKER_SIMULATION_ETAT.
Une image dont le Dockerfile contient « CASSE » ne se construit pas ; « PANNE » se construit
mais l'app répond 503 (le serveur /health du test lit cet état).
"""
import io
import json
import os
import sys
import tarfile

ETAT = os.environ["ESN_DOCKER_SIMULATION_ETAT"]


def charger():
    with open(ETAT, "r", encoding="utf-8") as f:
        return json.load(f)


def sauver(etat):
    with open(ETAT, "w", encoding="utf-8") as f:
        json.dump(etat, f)


def sortir(etat, code, message=""):
    sauver(etat)
    if message:
        sys.stderr.write(message + "\n")
    sys.exit(code)


def main(args):
    etat = charger()
    etat.setdefault("appels", []).append(args)
    if etat.get("docker_absent"):
        sortir(etat, 1, "Cannot connect to the Docker daemon")
    if args[:1] == ["version"]:
        sys.stdout.write("27.0-simulation\n")
        sortir(etat, 0)
    if args[:2] == ["image", "inspect"]:
        sortir(etat, 0 if args[2] in etat["images"] else 1)
    if args[:2] == ["volume", "inspect"]:
        sortir(etat, 0 if args[2] in etat["volumes"] else 1)
    if args[:1] == ["build"]:
        tag = args[args.index("-t") + 1]
        commit = args[args.index("--build-arg") + 1].split("=", 1)[1]
        with tarfile.open(fileobj=io.BytesIO(sys.stdin.buffer.read())) as tar:
            dockerfile = tar.extractfile("Dockerfile").read()
        if b"CASSE" in dockerfile:
            sortir(etat, 1, "ERROR: failed to solve: process did not complete successfully")
        etat["images"][tag] = {"commit": commit, "panne": b"PANNE" in dockerfile}
        sortir(etat, 0)
    if args[:1] == ["compose"]:
        projet = args[args.index("-p") + 1]
        reste = args[args.index("-f") + 2:]
        if reste[:1] == ["up"]:
            services = [a for a in reste[1:] if not a.startswith("-")]
            if etat.get("up_echec"):
                sortir(etat, 1, "Error response from daemon: simulated")
            if not services or "db" in services:
                if projet + "_pgdata" not in etat["volumes"]:
                    etat["volumes"].append(projet + "_pgdata")
            if not services or "app" in services:
                image = os.environ.get("APP_IMAGE", "")
                if image not in etat["images"]:
                    sortir(etat, 1, "No such image: " + image)
                etat["lancee"] = image
            sortir(etat, 0)
        if reste[:1] == ["exec"] and "pg_dump" in reste:
            if etat.get("pg_dump_echec"):
                sortir(etat, 1, "pg_dump: error: connection failed")
            sys.stdout.buffer.write(b"PGDMP-simulation")
            sortir(etat, 0)
        if reste[:1] == ["down"]:
            etat["lancee"] = None
            sortir(etat, 0)
    sortir(etat, 2, "faux_docker : commande non simulée : " + " ".join(args))


if __name__ == "__main__":
    main(sys.argv[1:])
