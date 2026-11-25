"""Critères 3, 5, 6 et 7 de T-010 : Dockerfile, dépendances, OpenAPI, env.example."""

import json
import os
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from reservation.app import creer_app

RACINE_APP = Path(__file__).resolve().parent.parent
FICHIER_OPENAPI = RACINE_APP / "docs" / "openapi.json"


def _lignes(nom: str) -> list[str]:
    texte = (RACINE_APP / nom).read_text(encoding="utf-8")
    return [l.strip() for l in texte.splitlines() if l.strip() and not l.strip().startswith("#")]


# --- Dockerfile -------------------------------------------------------------------------

def test_dockerfile_respecte_le_contrat_de_l_image():
    lignes = _lignes("Dockerfile")
    assert lignes[0] == "FROM python:3.14-slim"
    assert "ARG GIT_COMMIT" in lignes
    assert "ENV GIT_COMMIT=$GIT_COMMIT" in lignes
    assert lignes.index("ARG GIT_COMMIT") < lignes.index("ENV GIT_COMMIT=$GIT_COMMIT")
    assert 'CMD ["python", "-m", "reservation.demarrer"]' in lignes
    assert lignes[-1] == 'CMD ["python", "-m", "reservation.demarrer"]'


def test_dockerfile_installe_requirements_seul_et_tourne_sans_root():
    texte = "\n".join(_lignes("Dockerfile"))
    assert "pip install -r requirements.txt" in texte
    assert "requirements-dev" not in texte
    utilisateur = [l for l in texte.splitlines() if l.startswith("USER ")]
    assert utilisateur and utilisateur[-1] != "USER root"
    assert "COPY tests" not in texte


# --- Dépendances ------------------------------------------------------------------------

def test_requirements_epingles_sur_les_lignes_de_l_architecture():
    attendu = {
        "fastapi": "0.162.", "uvicorn": "0.52.", "sqlalchemy": "2.0.", "alembic": "1.18.",
        "psycopg": "3.3.", "argon2-cffi": "25.1.", "tzdata": "2026.6",
    }
    trouve = {}
    for ligne in _lignes("requirements.txt"):
        m = re.fullmatch(r"([A-Za-z0-9_.\-]+)(\[[a-z,]+\])?==([0-9][^\s=]*)", ligne)
        assert m, f"ligne non épinglée par == : {ligne}"
        trouve[m.group(1).lower()] = m.group(3)
    assert set(trouve) == set(attendu)
    for nom, prefixe in attendu.items():
        assert trouve[nom].startswith(prefixe), (nom, trouve[nom])


def test_outils_de_test_hors_de_l_image():
    prod = " ".join(_lignes("requirements.txt")).lower()
    dev = " ".join(_lignes("requirements-dev.txt")).lower()
    for nom in ("pytest", "httpx", "playwright"):
        assert nom not in prod
        assert nom in dev
    assert "-r requirements.txt" in dev


# --- Documentation OpenAPI --------------------------------------------------------------

@pytest.mark.parametrize("chemin", ["/docs", "/redoc", "/openapi.json"])
def test_documentation_non_servie_en_production(chemin):
    assert TestClient(creer_app(), base_url="http://localhost").get(chemin).status_code == 404


def test_schema_openapi_versionne_est_a_jour():
    """Génère le schéma ; REGENERER_OPENAPI=1 réécrit le fichier versionné pour le dev-frontend."""
    schema = creer_app(avec_documentation=True).openapi()
    attendu = json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if os.environ.get("REGENERER_OPENAPI") == "1":
        FICHIER_OPENAPI.parent.mkdir(exist_ok=True)
        FICHIER_OPENAPI.write_text(attendu, encoding="utf-8", newline="\n")
    assert FICHIER_OPENAPI.exists(), "lancer une fois avec REGENERER_OPENAPI=1"
    assert FICHIER_OPENAPI.read_text(encoding="utf-8") == attendu
    assert "/health" in schema["paths"]
    assert {"/api/salles", "/api/disponibilites"} <= set(schema["paths"])


# --- env.example ------------------------------------------------------------------------

def test_env_example_sans_valeur():
    assert not (RACINE_APP / ".env.example").exists()
    lignes = _lignes("env.example")
    variables = {}
    for ligne in lignes:
        nom, _, valeur = ligne.partition("=")
        variables[nom] = valeur
    assert variables == {
        "PORT": "", "DATABASE_URL": "", "ACCUEIL_EMAIL": "", "ACCUEIL_MOT_DE_PASSE_INITIAL": "",
    }
    texte = (RACINE_APP / "env.example").read_text(encoding="utf-8")
    assert "GIT_COMMIT" in texte and "argument de build" in texte
