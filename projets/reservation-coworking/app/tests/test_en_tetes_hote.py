"""T-063 : en-têtes de sécurité sur toutes les réponses et contrôle de l'en-tête Host."""

import pytest

CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self'; "
    "frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
)
CHEMINS = ["/", "/api/salles", "/health", "/inconnu"]


@pytest.mark.parametrize("chemin", CHEMINS)
def test_en_tetes_de_securite_sur_chaque_type_de_reponse(client_base_ok, chemin):
    reponse = client_base_ok.get(chemin, headers={"Host": "localhost"})
    assert reponse.headers["content-security-policy"] == CSP
    assert reponse.headers["x-content-type-options"] == "nosniff"
    assert reponse.headers["referrer-policy"] == "no-referrer"


def test_404_porte_les_en_tetes(client_base_ok):
    reponse = client_base_ok.get("/inconnu", headers={"Host": "localhost"})
    assert reponse.status_code == 404
    assert reponse.headers["content-security-policy"] == CSP


def test_page_statique_sans_script_ni_style_en_ligne():
    from reservation.app import DOSSIER_STATIQUE

    html = (DOSSIER_STATIQUE / "index.html").read_text(encoding="utf-8").lower()
    for interdit in ("<script", "<style", "style=", "onclick=", "onload="):
        assert interdit not in html


@pytest.mark.parametrize(
    "hote",
    ["localhost", "127.0.0.1", "localhost:8080", "127.0.0.1:8090", "LOCALHOST:8000"],
)
def test_hotes_acceptes(client_base_ok, hote):
    assert client_base_ok.get("/health", headers={"Host": hote}).status_code == 200


@pytest.mark.parametrize(
    "hote",
    [
        "rebind.evil.example",
        "rebind.evil.example:8080",
        "localhost.evil.example",
        "evil.example/localhost",
        "0.0.0.0",
        "127.0.0.2",
        "[::1]:8080",
    ],
)
@pytest.mark.parametrize("chemin", ["/health", "/api/salles", "/"])
def test_hote_etranger_refuse_400_avec_en_tetes(client_base_ok, chemin, hote):
    reponse = client_base_ok.get(chemin, headers={"Host": hote})
    assert reponse.status_code == 400
    assert reponse.headers["content-security-policy"] == CSP
    assert "rebind" not in reponse.text


def test_health_joignable_comme_les_sondes(client_base_ok):
    """verifier-prod et deployer_local.py appellent http://localhost:<port>/health."""
    reponse = client_base_ok.get("http://localhost:8080/health")
    assert reponse.status_code == 200
    assert reponse.json()["status"] == "ok"


def test_x_forwarded_host_ne_change_pas_le_controle(client_base_ok):
    reponse = client_base_ok.get(
        "/health", headers={"Host": "evil.example", "X-Forwarded-Host": "localhost"}
    )
    assert reponse.status_code == 400
