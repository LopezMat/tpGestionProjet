"""T-055 : le front statique respecte la CSP de l'architecture § 6 et est bien servi.

CSP : `default-src 'self'; script-src 'self'; style-src 'self'` -> aucun script ni style en
ligne, aucun attribut `on…`, aucune ressource externe, aucun `innerHTML` (données par
`textContent` uniquement). Ces contrôles parcourent TOUS les fichiers de `static/`, pour
qu'une page ajoutée par T-022 ou T-023 soit contrôlée sans modifier ce test.
"""

import re

import pytest

from reservation.app import DOSSIER_STATIQUE

PAGES = sorted(DOSSIER_STATIQUE.rglob("*.html"))
SCRIPTS = sorted(DOSSIER_STATIQUE.rglob("*.js"))
STYLES = sorted(DOSSIER_STATIQUE.rglob("*.css"))
TOUS = PAGES + SCRIPTS + STYLES


def _lire(chemin):
    return chemin.read_text(encoding="utf-8")


def _nom(chemin):
    return chemin.relative_to(DOSSIER_STATIQUE).as_posix()


def test_le_front_contient_la_page_son_script_et_sa_feuille_de_style():
    noms = {_nom(c) for c in TOUS}
    assert {"index.html", "js/disponibilites.js", "js/creneaux.js", "css/style.css"} <= noms


@pytest.mark.parametrize("page", PAGES, ids=_nom)
def test_page_sans_script_ni_style_en_ligne(page):
    html = _lire(page)
    # <script> sans src (script en ligne) ; <script src=...> du même site est permis.
    for balise in re.findall(r"<script\b[^>]*>", html, flags=re.IGNORECASE):
        assert re.search(r"\bsrc\s*=", balise, flags=re.IGNORECASE), balise
    for corps in re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.IGNORECASE | re.DOTALL):
        assert corps.strip() == ""
    assert not re.search(r"<style\b", html, flags=re.IGNORECASE)
    assert not re.search(r"\sstyle\s*=", html, flags=re.IGNORECASE)
    assert not re.search(r"\son[a-z]+\s*=", html, flags=re.IGNORECASE)
    assert not re.search(r"javascript:", html, flags=re.IGNORECASE)


@pytest.mark.parametrize("fichier", TOUS, ids=_nom)
def test_aucune_ressource_externe(fichier):
    contenu = _lire(fichier)
    # Aucune URL absolue ni relative au protocole (http:, https:, //hote), aucun @import.
    assert not re.search(r"https?://", contenu), _nom(fichier)
    assert not re.search(r"""["'(]//[\w.-]""", contenu), _nom(fichier)
    assert "@import" not in contenu


@pytest.mark.parametrize("script", SCRIPTS, ids=_nom)
def test_script_sans_insertion_de_html(script):
    code = _lire(script)
    for interdit in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write",
                     "eval(", "new Function", "setAttribute(\"style\"", "setAttribute('style'",
                     ".style.", "cssText", "createContextualFragment"):
        assert interdit not in code, f"{_nom(script)} : {interdit}"
    # Les données de l'API passent par textContent.
    assert not re.search(r"\.on[a-z]+\s*=", code), _nom(script)
    assert "setAttribute(\"on" not in code and "setAttribute('on" not in code


def test_page_donnees_inserees_par_textcontent():
    assert "textContent" in _lire(DOSSIER_STATIQUE / "js" / "disponibilites.js")


@pytest.mark.parametrize(
    ("chemin", "type_attendu"),
    [
        ("/", "text/html"),
        ("/js/disponibilites.js", "javascript"),
        ("/js/creneaux.js", "javascript"),
        ("/js/api.js", "javascript"),
        ("/css/style.css", "text/css"),
    ],
)
def test_fichiers_servis_avec_le_bon_type_et_la_csp(client_base_ok, chemin, type_attendu):
    """`nosniff` + module ES : un mauvais type MIME empêcherait l'exécution du script."""
    r = client_base_ok.get(chemin)
    assert r.status_code == 200
    assert type_attendu in r.headers["content-type"]
    assert "script-src 'self'" in r.headers["content-security-policy"]


def test_la_page_reference_ses_fichiers_du_meme_site(client_base_ok):
    html = client_base_ok.get("/").text
    assert 'src="js/disponibilites.js"' in html
    assert 'href="css/style.css"' in html
    assert 'lang="fr"' in html
