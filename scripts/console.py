#!/usr/bin/env python3
"""console.py : génère la console de consultation de l'ESN, un site statique en lecture seule.

Responsable : D · outil interne de l'ESN (DEC-012), comme tableau.py ; ce n'est pas un projet client.

La console présente le système (vision, 4 systèmes, circuit des agents, points d'arrêt, garde-fous), le
portefeuille, le bureau vu de dessus (scripts/bureau.py et bureau.js, DEC-016), chaque projet (synthèse,
Kanban, Gantt, tickets et documents rendus en HTML), l'équipe, les agents et skills, et le registre des
décisions. Elle s'ouvre directement dans un navigateur
(console/index.html), sans serveur.

Lecture seule : le script n'écrit QUE dans <racine>/console/ (dossier ignoré par Git). Tous les chiffres
viennent des fonctions de scripts/tableau.py (charger, Projet.calculer, alertes_equipe, libelle_fin, gantt) :
ils sont identiques à ceux de TABLEAU.md et PORTFOLIO.md, que la console ne réécrit jamais (R9).

Usage :
  python scripts/console.py [--racine DIR] [--date AAAA-MM-JJ] [--mermaid-src URL]     (Mac : python3 …)
    --racine      : racine du dépôt (par défaut : le dossier parent de scripts/)
    --date        : date du calcul (par défaut : aujourd'hui), comme tableau.py
    --mermaid-src : URL du script Mermaid (par exemple le CDN) ; par défaut, la copie locale
                    scripts/vendor/mermaid.min.js est copiée dans console/assets/ (fonctionne hors ligne)

Codes de sortie : 0 ; 2 = erreur d'usage ou PyYAML absent.
Dépendance : PyYAML (python -m pip install -r requirements.txt).
"""
import argparse
import html
import importlib.util
import os
import posixpath
import re
import sys
import unicodedata
from datetime import date
from urllib.parse import quote

sys.dont_write_bytecode = True  # aucun __pycache__ hors de console/ (lecture seule)

ICI = os.path.dirname(os.path.abspath(__file__))


def _module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tableau = _module("tableau", os.path.join(ICI, "tableau.py"))
try:  # contrôle des validations (garde-fou 4) ; facultatif si le hook est absent
    validations = _module("verifier_validations", os.path.join(ICI, "verifier_validations.py"))
except Exception:  # pragma: no cover - dépôt incomplet
    validations = None
bureau = _module("bureau", os.path.join(ICI, "bureau.py"))    # page « Le bureau » (DEC-016)

MERMAID_VERSION = "12.3.0"
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@{}/dist/mermaid.min.js".format(MERMAID_VERSION)
MERMAID_LOCAL = os.path.join(ICI, "vendor", "mermaid.min.js")
MERMAID_LICENCE = os.path.join(ICI, "vendor", "mermaid-LICENSE")

DOCS_PROJET = [("demande", "Demande"), ("existant", "Existant"), ("cdc", "Cahier des charges"),
               ("architecture", "Architecture"), ("planning", "Planning"), ("projet", "Fiche projet"),
               ("retex", "Retour d'expérience")]
DOCS_REFERENCE = [("docs/VISION.md", "Vision"), ("docs/ARCHITECTURE.md", "Architecture"),
                  ("CLAUDE.md", "Règles du coordinateur"), ("README.md", "README"),
                  ("docs/CHANGELOG-REGLES.md", "Historique des règles")]
RE_DECISION = re.compile(r"^(\d{4}-\d{2}-\d{2})-(DEC-\d{3,})-(.+)\.md$")

LIBELLES_STATUT = {"A_FAIRE": "À faire", "EN_COURS": "En cours", "EN_REVUE": "En revue", "BLOQUE": "Bloqué",
                   "ATTENTE_HUMAIN": "Attente humain", "TERMINE": "Terminé", "ANNULE": "Annulé"}

SYSTEMES = [
    ("S1", "Gestion de projet",
     "Découpe les projets en tickets, répartit le travail entre agents et salariés, suit le budget et les délais."),
    ("S2", "Suivi et maintenance",
     "Après la mise en ligne : veille technologique, supervision, support des utilisateurs et gestion de crise."),
    ("S3", "Déploiement automatisé",
     "Rien ne part en production sans revue de code, tests, audit de sécurité, recette humaine et vérification "
     "en ligne du SHA."),
    ("S4", "Cahier des charges",
     "Transforme la demande du client en cahier des charges, puis en architecture, toutes deux validées par "
     "un humain."),
    ("realisation", "Pôle réalisation",
     "Agents d'exécution transverses : ils réalisent les tickets planifiés par S1 et contrôlés par S3."),
]

# Phrases à taper au coordinateur : elles ne figurent dans aucun fichier du dépôt. Un agent ou un skill absent
# de ce dictionnaire reçoit une phrase générique, signalée comme telle sur la page.
PHRASES = {
    "analyste-besoin": "Nouvelle demande pour <slug> : lance l'analyste-besoin pour rédiger le CDC.",
    "architecte": "Le CDC de <slug> est validé : lance l'architecte.",
    "chef-de-projet": "L'architecture de <slug> est validée : lance le chef-de-projet pour les tickets et le "
                      "planning.",
    "dev-backend": "Réalise le ticket T-NNN de <slug> avec dev-backend.",
    "dev-frontend": "Réalise le ticket T-NNN de <slug> avec dev-frontend.",
    "relecteur-code": "Le ticket T-NNN de <slug> est EN_REVUE : lance la revue de code.",
    "testeur": "La revue de T-NNN est APPROUVÉ : lance le testeur.",
    "securite": "Lance l'audit de sécurité de <slug> avant la mise en production.",
    "deployeur": "GO donné (DEC-NNN) pour <slug> au SHA <sha> : lance le déployeur.",
    "veilleur": "Lance la veille technologique de la semaine.",
    "analyste-prod": "Fais le point de production de <slug>.",
    "support": "De nouvelles remontées sont arrivées dans support/entrant/ de <slug> : lance le support.",
    "gestionnaire-crise": "Incident critique T-NNN sur <slug> : lance le gestionnaire de crise.",
    "nouveau-projet": "Nouveau client : <résumé de la demande>.",
    "avancement": "Où en est <slug> ?",
    "creer-ticket": "Crée un ticket <type> pour <slug> : <description>.",
    "tracer-decision": "Pour T-NNN, je décide <décision>, parce que <pourquoi>.",
    "absence": "<Prénom> sera absent·e du <date> au <date> (congés).",
    "arrivee-membre": "<Prénom> arrive le <date> comme <rôle>.",
    "depart-membre": "<Prénom> quitte l'ESN le <date>.",
    "revision-budget": "Le client de <slug> révise le budget à <montant> € (ou la deadline au <date>).",
    "recette": "(salarié recetteur, session dédiée) Je fais la recette de <slug> au SHA <sha> (T-NNN).",
    "verifier-prod": "Vérifie la version en ligne de <slug> (SHA attendu <sha>).",
}
SKILLS_HUMAINS = {"recette"}


# ============================================================================ utilitaires

def e(valeur):
    return html.escape("" if valeur is None else str(valeur), quote=True)


def classe(valeur):
    t = tableau.sans_accents(valeur).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "vide"


def statut_document(valeur):
    """Statut d'un document normalisé (garde-fou 5) : BROUILLON, EN_REVUE, VALIDE ou autre."""
    if validations is not None:
        return validations.HOOK.normaliser(valeur)
    return tableau.sans_accents(valeur).strip().upper()


def lire_texte(chemin):
    try:
        with open(chemin, "r", encoding="utf-8-sig") as f:
            return f.read().replace("\r\n", "\n").replace("\r", "\n")
    except (OSError, UnicodeDecodeError):
        return None


def lire_md(chemin, tolerant=False):
    """(frontmatter ou {}, corps, erreur). Sans frontmatter, le corps est le fichier entier.
    `tolerant` : pour les agents et les skills, dont l'en-tête est lu par Claude Code ligne à ligne
    (une description qui contient « : » n'est pas du YAML strict) ; on lit alors « clé: valeur » par ligne."""
    fm, corps, err = tableau.lire_frontmatter(chemin)
    if err == "pas de frontmatter YAML":
        return {}, corps, None
    if err:
        brut = lire_texte(chemin) or ""
        if tolerant:
            lu = entete_tolerant(brut)
            if lu:
                return lu
        return {}, brut, err
    return fm, corps, None


def entete_tolerant(brut):
    lignes = brut.split("\n")
    if not lignes or lignes[0].strip() != "---":
        return None
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            fm = {}
            for l in lignes[1:i]:
                m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s?(.*)$", l)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
            return fm, "\n".join(lignes[i + 1:]), None
    return None


def section(corps, motif):
    """Texte Markdown de la première section dont le titre correspond à `motif` (regex), sans le titre."""
    lignes = corps.split("\n")
    debut, niveau = None, 0
    dans_code = False
    for i, l in enumerate(lignes):
        if l.strip().startswith("```"):
            dans_code = not dans_code
        if dans_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if not m:
            continue
        if debut is None:
            if re.search(motif, m.group(2), re.I):
                debut, niveau = i + 1, len(m.group(1))
        elif len(m.group(1)) <= niveau:
            return _sans_hr_final(lignes[debut:i])
    return _sans_hr_final(lignes[debut:]) if debut is not None else ""


def _sans_hr_final(lignes):
    """Texte d'une section sans le séparateur `---` qui la termine souvent."""
    return re.sub(r"\n\s*([-*_])(\s*\1){2,}\s*$", "", "\n".join(lignes).strip()).strip()


def bloc_mermaid(corps):
    m = re.search(r"```mermaid\s*\n(.*?)\n\s*```", corps, re.S)
    return m.group(1) if m else ""


def premier_tableau(corps):
    lignes, pris = corps.split("\n"), []
    for l in lignes:
        if l.strip().startswith("|"):
            pris.append(l)
        elif pris:
            break
    return "\n".join(pris)


def ancre(texte):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    t = re.sub(r"[`*]", "", t).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


# ============================================================================ Markdown → HTML

RE_TITRE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_LISTE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
RE_HR = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
RE_FENCE = re.compile(r"^\s*(```+|~~~+)\s*([\w+-]*)")
RE_CODE = re.compile(r"(`+)(.+?)\1")
RE_LIEN = re.compile(r"!?\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\s*\)")
RE_JETON = re.compile("\x00(\\d+)\x00")


def emphase(t):
    t = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\w)__(?=\S)(.+?)(?<=\S)__(?!\w)", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w])_(?=\S)(.+?)(?<=\S)_(?![\w])", r"<em>\1</em>", t)
    return t


class Markdown:
    """Convertisseur Markdown → HTML volontairement simple. Tout le texte est échappé : aucun HTML du
    fichier source n'est repris tel quel (seul <br> est reconnu). `resoudre(href)` renvoie l'URL à
    utiliser pour un lien, ou None pour l'afficher sans lien (javascript:, data:, hors dépôt…)."""

    def __init__(self, resoudre=None):
        self.resoudre = resoudre or (lambda href: href if re.match(r"^(https?:|mailto:|#)", href) else None)
        self.ancres = {}

    def convertir(self, texte):
        texte = re.sub(r"<!--.*?-->", "", texte or "", flags=re.S)
        return "\n".join(self._blocs(texte.replace("\r\n", "\n").split("\n")))

    # -- inline -------------------------------------------------------------------
    def inline(self, texte):
        jetons = []

        def garder(h):
            jetons.append(h)
            return "\x00{}\x00".format(len(jetons) - 1)

        t = RE_CODE.sub(lambda m: garder("<code>{}</code>".format(e(m.group(2).strip()))), texte)
        t = e(t)
        t = re.sub(r"&lt;br\s*/?&gt;", lambda m: garder("<br>"), t)
        t = re.sub(r"&lt;(https?://[^\s&]+)&gt;", lambda m: garder(self._lien(m.group(1), e(m.group(1)))), t)
        t = RE_LIEN.sub(lambda m: garder(self._lien(html.unescape(m.group(2)), emphase(m.group(1)))), t)
        t = emphase(t)
        for _ in range(6):
            if "\x00" not in t:
                break
            t = RE_JETON.sub(lambda m: jetons[int(m.group(1))], t)
        return t

    def _lien(self, href, texte_html):
        cible = self.resoudre(href)
        if not cible:
            return '<span class="lien-inactif">{}</span>'.format(texte_html)
        externe = cible.startswith(("http://", "https://"))
        return '<a href="{}"{}>{}</a>'.format(
            e(cible), ' target="_blank" rel="noopener noreferrer"' if externe else "", texte_html)

    # -- blocs --------------------------------------------------------------------
    def _debut_bloc(self, lignes, i):
        l = lignes[i]
        return bool(RE_FENCE.match(l) or RE_TITRE.match(l) or RE_HR.match(l) or l.lstrip().startswith(">")
                    or RE_LISTE.match(l) or self._est_tableau(lignes, i))

    @staticmethod
    def _est_tableau(lignes, i):
        return ("|" in lignes[i] and i + 1 < len(lignes) and "|" in lignes[i + 1]
                and bool(RE_SEP.match(lignes[i + 1])))

    @staticmethod
    def _cellules(ligne):
        l = ligne.strip()
        if l.startswith("|"):
            l = l[1:]
        if l.endswith("|") and not l.endswith("\\|"):
            l = l[:-1]
        return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l)]

    def _id(self, texte):
        base = ancre(texte) or "section"
        n = self.ancres.get(base, 0)
        self.ancres[base] = n + 1
        return base if n == 0 else "{}-{}".format(base, n)

    def _blocs(self, lignes):
        out, i, n = [], 0, len(lignes)
        while i < n:
            l = lignes[i]
            if not l.strip():
                i += 1
                continue
            m = RE_FENCE.match(l)
            if m:
                cloture, langage = m.group(1)[0] * 3, m.group(2).lower()
                i += 1
                code = []
                while i < n and not lignes[i].strip().startswith(cloture):
                    code.append(lignes[i])
                    i += 1
                i += 1
                source = "\n".join(code)
                if langage == "mermaid":
                    out.append('<pre class="mermaid">{}</pre>'.format(e(source)))
                else:
                    out.append('<pre class="code"><code>{}</code></pre>'.format(e(source)))
                continue
            m = RE_TITRE.match(l)
            if m:
                niv = len(m.group(1))
                out.append('<h{n} id="{i}">{t}</h{n}>'.format(n=niv, i=e(self._id(m.group(2))),
                                                              t=self.inline(m.group(2))))
                i += 1
                continue
            if RE_HR.match(l):
                out.append("<hr>")
                i += 1
                continue
            if l.lstrip().startswith(">"):
                bloc = []
                while i < n and lignes[i].lstrip().startswith(">"):
                    bloc.append(re.sub(r"^\s*>\s?", "", lignes[i]))
                    i += 1
                out.append("<blockquote>{}</blockquote>".format("\n".join(self._blocs(bloc))))
                continue
            if self._est_tableau(lignes, i):
                entetes = self._cellules(l)
                i += 2
                corps = []
                while i < n and lignes[i].strip() and "|" in lignes[i]:
                    corps.append(self._cellules(lignes[i]))
                    i += 1
                th = "".join("<th>{}</th>".format(self.inline(c)) for c in entetes)
                tr = "".join("<tr>{}</tr>".format("".join("<td>{}</td>".format(self.inline(c)) for c in r))
                             for r in corps)
                out.append('<div class="table-wrap"><table><thead><tr>{}</tr></thead><tbody>{}</tbody>'
                           '</table></div>'.format(th, tr))
                continue
            if RE_LISTE.match(l):
                i, h = self._liste(lignes, i)
                out.append(h)
                continue
            para = []
            while i < n and lignes[i].strip() and (not para or not self._debut_bloc(lignes, i)):
                para.append(lignes[i].strip())
                i += 1
            out.append("<p>{}</p>".format("<br>".join(self.inline(p) for p in para)))
        return out

    def _liste(self, lignes, i):
        n, items = len(lignes), []
        while i < n:
            l = lignes[i]
            m = RE_LISTE.match(l)
            if m:
                items.append([len(m.group(1).expandtabs(4)), m.group(2)[0].isdigit(), m.group(3)])
                i += 1
            elif l.strip() and items and l[:1] in (" ", "\t") and not RE_FENCE.match(l):
                items[-1][2] += " " + l.strip()
                i += 1
            elif not l.strip() and i + 1 < n and RE_LISTE.match(lignes[i + 1]):
                i += 1
            else:
                break
        out, pile = [], []
        for retrait, ordonnee, texte_item in items:
            balise = "ol" if ordonnee else "ul"
            if not pile or retrait > pile[-1][0]:
                out.append("<{}>".format(balise))
                pile.append((retrait, balise))
            else:
                while len(pile) > 1 and retrait < pile[-1][0]:
                    out.append("</li></{}>".format(pile.pop()[1]))
                out.append("</li>")
                if pile[-1][1] != balise:
                    out.append("</{}><{}>".format(pile[-1][1], balise))
                    pile[-1] = (pile[-1][0], balise)
            m = re.match(r"^\[([ xX])\]\s+(.*)$", texte_item)
            if m:
                coche = m.group(1).lower() == "x"
                out.append('<li class="tache{}"><span class="case" aria-label="{}">{}</span> {}'.format(
                    " faite" if coche else "", "fait" if coche else "à faire", "✓" if coche else "",
                    self.inline(m.group(2))))
            else:
                out.append("<li>{}".format(self.inline(texte_item)))
        while pile:
            out.append("</li></{}>".format(pile.pop()[1]))
        return i, "".join(out)


# ============================================================================ Gantt par statut

# Marqueur Mermaid selon le statut du ticket (console seulement : TABLEAU.md garde ceux de tableau.gantt,
# qui marque aussi « crit » les tickets de priorité critique).
MARQUEURS_GANTT = {"TERMINE": "done", "EN_COURS": "active", "EN_REVUE": "active", "BLOQUE": "crit",
                   "ATTENTE_HUMAIN": "crit"}
RE_TACHE_GANTT = re.compile(r"^(\s+)(T-\d+)( .*? :)((?:(?:done|active|crit), )*)(\w+, \d{4}-\d{2}-\d{2}, "
                            r"\d{4}-\d{2}-\d{2})$")
LEGENDE_GANTT = ('<ul class="legende-gantt" aria-label="Légende du Gantt">'
                 '<li><span class="pastille g-afaire"></span>À faire</li>'
                 '<li><span class="pastille g-active"></span>En cours ou en revue</li>'
                 '<li><span class="pastille g-crit"></span>Bloqué ou en attente d\'une décision humaine</li>'
                 '<li><span class="pastille g-done"></span>Terminé</li>'
                 '<li><span class="pastille g-jalon"></span>Deadline</li></ul>')


def gantt_par_statut(p):
    """Source Mermaid du Gantt de tableau.gantt(p) (dates et sections réutilisées), dont seuls les marqueurs
    sont remplacés selon le statut : done, active, crit. None s'il n'y a aucun ticket à représenter."""
    lignes = tableau.gantt(p)
    if not lignes or not lignes[0].startswith("```mermaid"):
        return None
    sortie = []
    for l in lignes[1:-1]:
        m = RE_TACHE_GANTT.match(l)
        if m and m.group(2) in p.par_id:
            marqueur = MARQUEURS_GANTT.get(p.par_id[m.group(2)].statut)
            l = m.group(1) + m.group(2) + m.group(3) + (marqueur + ", " if marqueur else "") + m.group(5)
        sortie.append(l)
    return "\n".join(sortie)


# ============================================================================ site

class Site:
    def __init__(self, racine, aujourdhui, mermaid_src=None):
        self.racine = os.path.realpath(racine)
        self.sortie = os.path.join(self.racine, "console")
        self.auj = aujourdhui
        self.mermaid_src = mermaid_src
        self.ecrits = set()
        self.pages = {}            # chemin du dépôt (posix) -> page de la console
        self.avertissements = []

    # -- écriture : le seul point de sortie du script ----------------------------------
    def ecrire(self, rel, contenu):
        """Écrit console/<rel>. Refuse tout chemin qui sortirait de console/ (lecture seule)."""
        base = os.path.realpath(self.sortie)
        chemin = os.path.realpath(os.path.join(base, *rel.split("/")))
        if chemin == base or os.path.commonpath([chemin, base]) != base:
            raise ValueError("écriture refusée hors de console/ : {}".format(rel))
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        if isinstance(contenu, bytes):
            with open(chemin, "wb") as f:
                f.write(contenu)
        else:
            with open(chemin, "w", encoding="utf-8", newline="\n") as f:
                f.write(contenu)
        self.ecrits.add(os.path.normcase(chemin))

    def nettoyer(self):
        """Supprime les pages .html de console/ qui n'ont pas été produites à ce passage."""
        base, supprimes = os.path.realpath(self.sortie), 0
        for dossier, _, noms in os.walk(base):
            for nom in noms:
                chemin = os.path.realpath(os.path.join(dossier, nom))
                if (nom.endswith(".html") and os.path.commonpath([chemin, base]) == base
                        and os.path.normcase(chemin) not in self.ecrits):
                    os.remove(chemin)
                    supprimes += 1
        return supprimes

    # -- liens ------------------------------------------------------------------------
    @staticmethod
    def lien(depuis, vers):
        """Lien relatif d'une page de la console vers une autre (chemins posix relatifs à console/)."""
        vers, _, fragment = vers.partition("#")
        r = posixpath.relpath(vers, posixpath.dirname(depuis) or ".")
        r = "/".join(quote(p) for p in r.split("/"))
        return r + ("#" + fragment if fragment else "")

    def resoudre(self, href, source, page):
        """Lien d'un fichier Markdown du dépôt (`source`) affiché sur la page `page`."""
        href = href.strip()
        if href.startswith("#"):
            return href
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
            return href if re.match(r"^(https?|mailto):", href, re.I) else None
        chemin, _, fragment = href.partition("#")
        if not chemin:
            return "#" + fragment
        cible = posixpath.normpath(posixpath.join(posixpath.dirname(source), chemin.replace("\\", "/")))
        if cible.startswith("..") or cible.startswith("/"):
            return None
        cible = cible.rstrip("/")
        if cible in self.pages:
            dest = self.pages[cible]
            if fragment and "#" not in dest:
                dest += "#" + fragment
            return self.lien(page, dest)
        return self.lien(page, "../" + cible) + ("#" + fragment if fragment else "")

    def md(self, texte, source, page):
        return Markdown(lambda h: self.resoudre(h, source, page)).convertir(texte)

    # -- gabarit ------------------------------------------------------------------------
    def script_mermaid(self, racine, ajuste=False):
        """Chargement de Mermaid (copie locale par défaut). `ajuste` : le schéma tient dans la largeur de
        l'écran (page plein écran) ; sinon un grand schéma garde sa taille réelle, avec défilement horizontal."""
        src = self.mermaid_src or (racine + "assets/mermaid.min.js")
        flowchart = "" if ajuste else ", flowchart: {useMaxWidth: false}"
        return ('<script src="{}"></script>\n<script>\n'
                'if (window.mermaid) {{\n'
                '  mermaid.initialize({{startOnLoad: true, securityLevel: "strict", theme: "neutral"{}}});\n'
                '}} else {{\n'
                '  document.querySelectorAll("pre.mermaid").forEach(function (b) {{\n'
                '    var n = document.createElement("p"); n.className = "avert";\n'
                '    n.textContent = "Diagramme non dessiné : script Mermaid introuvable (voir README, '
                'section Console). Source affichée ci-dessous.";\n'
                '    b.parentNode.insertBefore(n, b); b.classList.add("mermaid-brut");\n'
                '  }});\n}}\n</script>').format(e(src), flowchart)

    def page_plein_ecran(self, rel, titre, source_mermaid):
        """Page qui ne contient que le diagramme, ajusté à l'écran (projection au jury)."""
        racine = self.lien(rel, "index.html").rsplit("index.html", 1)[0]
        contenu = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre} · Console ESN</title>
<link rel="stylesheet" href="{racine}style.css">
</head>
<body class="plein-ecran">
<pre class="mermaid">{source}</pre>
{script}
</body>
</html>
""".format(titre=e(titre), racine=e(racine), source=e(source_mermaid), script=self.script_mermaid(racine, True))
        self.ecrire(rel, contenu)

    def page(self, rel, titre, corps, actif=None, fil=None):
        racine = self.lien(rel, "index.html").rsplit("index.html", 1)[0]
        nav = [("index.html", "Notre système", "systeme"), ("portefeuille.html", "Portefeuille", "portefeuille"),
               ("bureau.html", "Le bureau", "bureau"), ("equipe.html", "Équipe", "equipe"), ("agents.html", "Agents et skills", "agents"),
               ("decisions.html", "Décisions", "decisions")]
        liens = "".join('<a href="{}"{}>{}</a>'.format(e(self.lien(rel, h)),
                                                         ' class="actif" aria-current="page"' if c == actif else "",
                                                         e(t)) for h, t, c in nav)
        fil_html = ""
        if fil:
            fil_html = '<nav class="fil" aria-label="Fil d\'Ariane">{}</nav>'.format(" › ".join(
                '<a href="{}">{}</a>'.format(e(self.lien(rel, h)), e(t)) if h else e(t) for t, h in fil))
        script = self.script_mermaid(racine) if 'class="mermaid"' in corps else ""
        return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre} · Console ESN</title>
<link rel="stylesheet" href="{racine}style.css">
</head>
<body>
<header class="entete">
  <div class="entete-in">
    <a class="marque" href="{accueil}"><span class="logo" aria-hidden="true">◆</span> ESN <span>console</span></a>
    <nav class="nav" aria-label="Navigation principale">{liens}</nav>
  </div>
</header>
<main>
{fil}
{corps}
</main>
<footer class="pied">
  Données au {date} · générée par <code>scripts/console.py</code> à partir des fichiers du dépôt, en lecture
  seule. La source de vérité reste les fichiers (R9) ; pour rafraîchir : <code>python scripts/console.py</code>.
</footer>
{script}
</body>
</html>
""".format(titre=e(titre), racine=e(racine), accueil=e(self.lien(rel, "index.html")), liens=liens, fil=fil_html,
           corps=corps, date=e(self.auj.isoformat()), script=script)

    # -- composants -----------------------------------------------------------------------
    @staticmethod
    def badge(texte, famille, valeur=None):
        return '<span class="badge {}-{}">{}</span>'.format(famille, classe(valeur if valeur is not None else texte),
                                                          e(texte))

    def badge_statut(self, statut):
        return self.badge(LIBELLES_STATUT.get(statut, statut or "?"), "st", statut)

    def badge_doc(self, statut):
        n = statut_document(statut)
        libelle = {"VALIDE": "VALIDÉ", "EN_REVUE": "EN REVUE", "BROUILLON": "BROUILLON"}.get(n, statut or "sans statut")
        return self.badge(libelle, "doc", n or "aucun")

    def badge_prio(self, prio):
        return self.badge(prio or "normale", "prio")

    @staticmethod
    def barre(fraction, mode="avancement"):
        if fraction is None:
            return '<div class="barre vide"><span style="width:0"></span></div>'
        niveau = "ok"
        if mode == "budget":
            niveau = "danger" if fraction > 1.0 else ("alerte" if fraction > tableau.SEUIL_BUDGET else "ok")
        largeur = max(0.0, min(100.0, 100.0 * fraction))
        return '<div class="barre {}" role="img" aria-label="{}"><span style="width:{:.1f}%"></span></div>'.format(
            niveau, e(tableau.fmt_pct(fraction)), largeur)

    @staticmethod
    def tableau_html(entetes, lignes, vide="Aucun."):
        """Lignes déjà converties en HTML (chaque donnée a été échappée par l'appelant)."""
        if not lignes:
            return '<p class="vide">{}</p>'.format(e(vide))
        th = "".join("<th>{}</th>".format(e(x)) for x in entetes)
        tr = "".join("<tr>{}</tr>".format("".join("<td>{}</td>".format(c) for c in l)) for l in lignes)
        return '<div class="table-wrap"><table><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(
            th, tr)

    @staticmethod
    def stat(libelle, valeur, detail="", lien=None):
        contenu = ('<div class="stat-val">{}</div><div class="stat-lib">{}</div>{}'.format(
            valeur, e(libelle), '<div class="stat-det">{}</div>'.format(detail) if detail else ""))
        if lien:
            return '<a class="carte stat" href="{}">{}</a>'.format(e(lien), contenu)
        return '<div class="carte stat">{}</div>'.format(contenu)

    def alertes_html(self, lignes, avec_projet):
        if not lignes:
            return '<p class="vide ok">Aucune alerte.</p>'
        rangs = []
        for l in lignes:
            projet, type_, detail = (l if avec_projet else (None,) + tuple(l))
            rangs.append(([e(projet)] if avec_projet else []) + [self.badge(type_, "al"), e(detail)])
        return self.tableau_html((["Projet"] if avec_projet else []) + ["Type", "Détail"], rangs)

    # ======================================================================== inventaire
    def inventaire(self):
        r = self.racine
        self.agents = []
        for nom in tableau.lister(os.path.join(r, ".claude", "agents")):
            fm, corps, err = lire_md(os.path.join(r, ".claude", "agents", nom), tolerant=True)
            cle = (fm.get("name") if isinstance(fm, dict) else None) or nom[:-3]
            self.agents.append({"nom": str(cle), "fm": fm, "corps": corps, "err": err,
                                "source": ".claude/agents/" + nom, "page": "agents/{}.html".format(nom[:-3])})
        self.skills = []
        dossier = os.path.join(r, ".claude", "skills")
        for nom in sorted(os.listdir(dossier)) if os.path.isdir(dossier) else []:
            chemin = os.path.join(dossier, nom, "SKILL.md")
            if os.path.isfile(chemin):
                fm, corps, err = lire_md(chemin, tolerant=True)
                self.skills.append({"nom": str(fm.get("name") or nom), "fm": fm, "corps": corps, "err": err,
                                    "source": ".claude/skills/{}/SKILL.md".format(nom),
                                    "page": "skills/{}.html".format(nom)})
        self.decisions = []
        dossier = os.path.join(r, "docs", "decisions")
        for nom in tableau.lister(dossier):
            m = RE_DECISION.match(nom)
            if m:
                fm, corps, err = lire_md(os.path.join(dossier, nom))
                self.decisions.append({"id": m.group(2), "date": m.group(1), "fm": fm, "corps": corps, "err": err,
                                       "source": "docs/decisions/" + nom,
                                       "page": "decisions/{}.html".format(nom[:-3])})
        self.decisions.sort(key=lambda d: int(d["id"][4:]))
        self.par_dec = {d["id"]: d for d in self.decisions}
        self.docs = []
        for source, libelle in DOCS_REFERENCE:
            if os.path.isfile(os.path.join(r, *source.split("/"))):
                self.docs.append((source, "docs/{}.html".format(posixpath.basename(source)[:-3]), libelle))
        self.systemes = []
        for nom in tableau.lister(os.path.join(r, "docs", "systemes")):
            source = "docs/systemes/" + nom
            fm, corps, err = lire_md(os.path.join(r, "docs", "systemes", nom))
            self.systemes.append({"source": source, "page": "docs/systemes/{}.html".format(nom[:-3]), "fm": fm,
                                  "corps": corps, "code": nom[:2].upper()})
            self.docs.append((source, "docs/systemes/{}.html".format(nom[:-3]), (fm or {}).get("titre") or nom))
        # Agents d'equipe/agents.md (système, compétences)
        fm, _, _ = lire_md(os.path.join(r, "equipe", "agents.md"))
        self.catalogue = {}
        for a in (fm or {}).get("agents") or []:
            if isinstance(a, dict) and a.get("nom"):
                self.catalogue[str(a["nom"])] = a
        # Fiches salariés (rôle et compétences, que tableau.Equipe ne garde pas)
        self.fiches = {}
        for nom in tableau.lister(os.path.join(r, "equipe", "membres")):
            fm, _, err = lire_md(os.path.join(r, "equipe", "membres", nom))
            self.fiches[tableau.sans_accents(nom[:-3]).lower()] = fm if not err else {}
        # Projets : documents et tickets
        self.docs_projet, self.tickets_fichiers = {}, {}
        for p in self.projets:
            base = "projets/" + p.slug
            self.docs_projet[p.slug] = [(d, lib) for d, lib in DOCS_PROJET
                                        if os.path.isfile(os.path.join(p.dossier, d + ".md"))]
            self.tickets_fichiers[p.slug] = tableau.lister(os.path.join(p.dossier, "tickets"), prefixe="T-")
            self.pages[base] = base + "/index.html"
            self.pages[base + "/TABLEAU.md"] = base + "/index.html"
            self.pages[base + "/tickets"] = base + "/index.html#kanban"
            for d, _ in self.docs_projet[p.slug]:
                self.pages["{}/{}.md".format(base, d)] = "{}/{}.html".format(base, d)
            for nom in self.tickets_fichiers[p.slug]:
                self.pages["{}/tickets/{}".format(base, nom)] = "{}/tickets/{}.html".format(base, nom[:-3])
        # Table des pages pour la réécriture des liens Markdown
        for a in self.agents + self.skills + self.decisions:
            self.pages[a["source"]] = a["page"]
        for source, page, _ in self.docs:
            self.pages[source] = page
        for cle in self.fiches:
            self.pages["equipe/membres/{}.md".format(cle)] = "equipe.html#membre-" + cle
        self.pages.update({
            ".claude/agents": "agents.html", ".claude/skills": "agents.html#skills", "docs/decisions": "decisions.html",
            "docs/decisions/README.md": "decisions.html", "equipe": "equipe.html", "equipe/agents.md": "agents.html",
            "equipe/calendrier.md": "equipe.html#calendrier", "equipe/membres": "equipe.html",
            "PORTFOLIO.md": "portefeuille.html", "projets": "portefeuille.html", "docs/systemes": "index.html#systemes",
        })

    # ======================================================================== génération
    def generer(self):
        self.equipe, self.projets, self.anomalies = tableau.charger(self.racine, self.auj)
        self.inventaire()
        self.ecrire("style.css", CSS + bureau.CSS)
        if not self.mermaid_src:
            if os.path.isfile(MERMAID_LOCAL):
                with open(MERMAID_LOCAL, "rb") as f:
                    self.ecrire("assets/mermaid.min.js", f.read())
                if os.path.isfile(MERMAID_LICENCE):
                    with open(MERMAID_LICENCE, "rb") as f:
                        self.ecrire("assets/mermaid-LICENSE.txt", f.read())
            else:
                self.mermaid_src = MERMAID_CDN
                self.avertissements.append("scripts/vendor/mermaid.min.js absent : Mermaid chargé depuis le CDN "
                                           "(réseau nécessaire)")
        self.page_systeme()
        self.page_portefeuille()
        for p in self.projets:
            self.page_projet(p)
        self.page_equipe()
        self.page_agents()
        self.page_decisions()
        self.page_bureau()
        for source, page, libelle in self.docs:
            self.page_document(source, page, [("Notre système", "index.html"), (libelle, None)])
        return self.nettoyer()

    # -- documents rendus ------------------------------------------------------------------
    def bandeau_doc(self, fm, page):
        if not fm or "statut" not in fm:
            return ""
        morceaux = [self.badge_doc(fm.get("statut"))]
        for cle, lib in (("version", "v"), ("responsable", "resp."), ("maj_le", "mis à jour le")):
            if tableau.texte(fm.get(cle)):
                morceaux.append('<span class="meta">{} {}</span>'.format(e(lib), e(fm.get(cle))))
        if tableau.texte(fm.get("valide_par")):
            morceaux.append('<span class="meta">validé par {}</span>'.format(e(fm.get("valide_par"))))
        dec = tableau.texte(fm.get("decision"))
        if dec:
            morceaux.append('<span class="meta">décision {}</span>'.format(self.lien_dec(dec, page)))
        return '<div class="bandeau">{}</div>'.format(" ".join(morceaux))

    def lien_dec(self, dec, page):
        d = self.par_dec.get(dec)
        if d:
            return '<a href="{}">{}</a>'.format(e(self.lien(page, d["page"])), e(dec))
        return e(dec)

    def page_document(self, source, page, fil, avant=""):
        fm, corps, err = lire_md(os.path.join(self.racine, *source.split("/")), tolerant=source.startswith(".claude/"))
        titre = tableau.texte(fm.get("titre")) or tableau.texte(fm.get("name"))
        m = re.search(r"^#\s+(.+)$", corps, re.M)
        if not titre:
            titre = m.group(1) if m else posixpath.basename(source)
        contenu = ""
        if err:
            contenu = '<p class="avert">En-tête illisible ({}) : fichier affiché tel quel.</p><pre class="code">' \
                      '<code>{}</code></pre>'.format(e(err), e(corps))
        else:
            contenu = self.md(corps, source, page)
        tete = "" if m else "<h1>{}</h1>".format(e(titre))
        corps_html = ('<article class="doc">{tete}{bandeau}{avant}<div class="md">{contenu}</div>'
                      '<p class="source">Fichier : <a href="{src}"><code>{nom}</code></a></p></article>').format(
            tete=tete, bandeau=self.bandeau_doc(fm, page), avant=avant, contenu=contenu,
            src=e(self.lien(page, "../" + source)), nom=e(source))
        self.ecrire(page, self.page(page, titre, corps_html, fil=fil))

    # ======================================================================== Notre système
    def page_systeme(self):
        rel = "index.html"
        r = self.racine
        _, vision, _ = lire_md(os.path.join(r, "docs", "VISION.md"))
        _, archi, _ = lire_md(os.path.join(r, "docs", "ARCHITECTURE.md"))
        _, claude, _ = lire_md(os.path.join(r, "CLAUDE.md"))
        L = ['<section class="hero"><h1>ESN virtuelle orchestrée par des agents IA</h1>',
             '<p class="sous-titre">Un coordinateur, des agents spécialisés, des humains qui valident chaque étape '
             'clé. Les projets clients servent à démontrer le système.</p></section>']
        n_tickets = sum(len(p.tickets) for p in self.projets)
        L.append('<section class="grille stats">')
        L.append(self.stat("agents IA", e(len(self.agents)), "dans <code>.claude/agents/</code>", "agents.html"))
        L.append(self.stat("skills", e(len(self.skills)), "procédures réutilisables", "agents.html#skills"))
        L.append(self.stat("projets", e(len(self.projets)), "{} ticket(s)".format(n_tickets), "portefeuille.html"))
        L.append(self.stat("décisions humaines", e(len(self.decisions)), "tracées dans <code>docs/decisions/</code>",
                           "decisions.html"))
        L.append(self.stat("salariés", e(len(self.equipe.membres)), "fiches <code>equipe/membres/</code>",
                           "equipe.html"))
        L.append("</section>")
        vis = section(vision, r"^1\.") or section(vision, r"contexte")
        if vis:
            L.append('<section class="carte"><h2>Vision</h2><div class="md">{}</div>'
                     '<p class="plus"><a href="docs/VISION.html">Lire la vision complète →</a></p></section>'.format(
                         self.md(vis, "docs/VISION.md", rel)))
        # Les 4 systèmes
        L.append('<section id="systemes"><h2>Les 4 systèmes</h2><div class="grille systemes">')
        for s in self.systemes:
            fm = s["fm"] or {}
            num = re.sub(r"\D", "", s["code"])
            puces = section(vision, r"^Système\s+{}\b".format(num)) if num else ""
            agents = [n for n, a in sorted(self.catalogue.items()) if str(a.get("systeme", "")).upper() == s["code"]]
            chips = "".join('<a class="chip" href="agents.html#agent-{0}">{1}</a>'.format(e(n), e(n)) for n in agents)
            L.append('<article class="carte systeme sys-{c}"><div class="sys-code">{code}</div>'
                     '<h3><a href="{page}">{titre}</a></h3><div class="meta-ligne">{badge} <span class="meta">'
                     'responsable {resp}</span></div><div class="md">{puces}</div><div class="chips">{chips}</div>'
                     '</article>'.format(c=classe(s["code"]), code=e(s["code"]), page=e(s["page"]),
                                         titre=e(fm.get("titre") or s["source"]), badge=self.badge_doc(fm.get("statut")),
                                         resp=e(fm.get("responsable") or "—"),
                                         puces=self.md(puces, "docs/VISION.md", rel), chips=chips))
        if not self.systemes:
            L.append('<p class="vide">Aucun fichier dans <code>docs/systemes/</code>.</p>')
        L.append("</div></section>")
        circuit = bloc_mermaid(section(archi, r"^5\.") or "")
        if circuit:
            L.append('<section class="carte"><h2>Le circuit des agents</h2><p class="intro">De la demande du client '
                     'à la production : chaque flèche est un fichier versionné (R2) ; les losanges jaunes sont des '
                     'validations humaines. Source : <a href="docs/ARCHITECTURE.html#5-circuit-des-fichiers">'
                     'ARCHITECTURE § 5</a>.</p><pre class="mermaid">{}</pre><p class="plus"><a href="circuit.html" '
                     'target="_blank" rel="noopener">Ouvrir le schéma en plein écran ⤢</a></p></section>'.format(
                         e(circuit)))
            self.page_plein_ecran("circuit.html", "Circuit des agents", circuit)
        arrets = []
        if claude:
            lignes = claude.split("\n")
            for i, l in enumerate(lignes):
                if "Points d'arrêt humains" in l:
                    for l2 in lignes[i + 1:]:
                        if l2.startswith("- "):
                            arrets.append(l2)
                        elif arrets:
                            break
                    break
        garde_fous = premier_tableau(section(archi, r"^6\.") or "")
        L.append('<section class="carte"><h2>Points d\'arrêt humains</h2><p class="intro">Le coordinateur '
                 's\'arrête et présente la question, les options, sa recommandation et l\'impact (R7). Seul un humain '
                 'passe un document à VALIDÉ (R5).</p><div class="md arrets">{}</div><p class="plus">'
                 '<a href="docs/CLAUDE.html">Toutes les règles du coordinateur →</a></p></section>'.format(
                     self.md("\n".join(arrets), "CLAUDE.md", rel) if arrets else '<p class="vide">Liste introuvable '
                     'dans CLAUDE.md.</p>'))
        L.append('<section class="carte"><h2>Garde-fous techniques</h2><p class="intro">Les règles de validation ne '
                 'sont pas qu\'une consigne : des hooks Claude Code et la CI les appliquent.</p><div class="md '
                 'petit">{}</div><p class="plus"><a href="docs/ARCHITECTURE.html#6-modèle-de-validation">ARCHITECTURE '
                 '§ 6 →</a></p></section>'.format(self.md(garde_fous, "docs/ARCHITECTURE.md", rel) if garde_fous
                                                    else '<p class="vide">Tableau introuvable.</p>'))
        L.append('<section class="carte"><h2>Documents de référence</h2><div class="chips grandes">{}</div>'
                 '</section>'.format("".join('<a class="chip" href="{}">{}</a>'.format(e(page), e(lib))
                                             for _, page, lib in self.docs)))
        self.ecrire(rel, self.page(rel, "Notre système", "\n".join(L), actif="systeme"))

    # ======================================================================== Portefeuille
    def anciennete(self, t, mot):
        dep = t.depuis(mot)
        if not dep:
            return "inconnue"
        return "{} (depuis {})".format(tableau.fmt_jo(tableau.jours_ouvres_entre(dep, self.auj, self.equipe.feries)),
                                       dep.isoformat())

    def lien_ticket(self, p, t, page):
        return '<a href="{}">{}</a>'.format(e(self.lien(page, "projets/{}/tickets/{}.html".format(
            p.slug, t.fichier[:-3]))), e(t.id))

    def ecart_html(self, p):
        if p.ecart is None:
            return '<span class="meta">—</span>'
        texte = tableau.fmt_jo(p.ecart, signe=bool(p.ecart))
        return self.badge(texte, "ecart", "retard" if p.ecart > 0 else "ok")

    def carte_projet(self, p, rel):
        lien = self.lien(rel, "projets/{}/index.html".format(p.slug))
        bloques = sum(1 for t in p.tickets if t.statut == "BLOQUE")
        attentes = sum(1 for t in p.tickets if t.statut == "ATTENTE_HUMAIN")
        budget = "{} / {}".format(tableau.fmt_eur(p.consomme), tableau.fmt_eur(p.budget) if p.budget else "—")
        return """<a class="carte projet" href="{lien}">
  <div class="projet-tete"><h3>{client}</h3><code>{slug}</code></div>
  <div class="meta-ligne">{type_} {etat}</div>
  <div class="jauge"><div class="jauge-lib"><span>Avancement</span><strong>{av}</strong></div>{barre_av}</div>
  <div class="jauge"><div class="jauge-lib"><span>Budget {budget}</span><strong>{pb}</strong></div>{barre_b}</div>
  <dl class="mini"><div><dt>Fin projetée</dt><dd>{fin}</dd></div><div><dt>Deadline</dt><dd>{dl}</dd></div>
  <div><dt>Écart</dt><dd>{ecart}</dd></div></dl>
  <div class="compteurs"><span class="cpt {cb}">{b} bloqué(s)</span><span class="cpt {ca}">{a} attente(s) humaine(s)</span>
  <span class="cpt {cal}">{al} alerte(s)</span></div>
</a>""".format(lien=e(lien), client=e(p.client), slug=e(p.slug), type_=self.badge(p.type_projet, "type"),
               etat=self.badge(p.etat, "etat"), av=e(tableau.fmt_pct(p.avancement)), barre_av=self.barre(p.avancement),
               budget=e(budget), pb=e(tableau.fmt_pct(p.part_budget)), barre_b=self.barre(p.part_budget, "budget"),
               fin=e(p.fin_projetee.isoformat() if p.fin_projetee else "—"),
               dl=e(p.deadline.isoformat() if p.deadline else "—"), ecart=self.ecart_html(p),
               cb="rouge" if bloques else "", b=bloques, ca="ambre" if attentes else "", a=attentes,
               cal="orange" if p.alertes else "", al=len(p.alertes))

    def page_portefeuille(self):
        rel = "portefeuille.html"
        L = ['<h1>Portefeuille des projets</h1>',
             '<p class="intro">Calculs de <code>scripts/tableau.py</code> au {} : les mêmes chiffres que '
             '<code>PORTFOLIO.md</code>.</p>'.format(e(self.auj.isoformat()))]
        if self.projets:
            L.append('<section class="grille projets">{}</section>'.format(
                "".join(self.carte_projet(p, rel) for p in self.projets)))
            lignes = []
            for p in self.projets:
                lignes.append([
                    '<a href="{}">{}</a>'.format(e(self.lien(rel, "projets/{}/index.html".format(p.slug))), e(p.slug)),
                    e(p.client), self.badge(p.type_projet, "type"), self.badge(p.etat, "etat"),
                    e(tableau.fmt_pct(p.avancement)),
                    e("{} / {}".format(tableau.fmt_eur(p.consomme), tableau.fmt_eur(p.budget) if p.budget else "—")),
                    e(tableau.fmt_pct(p.part_budget)), e(tableau.fmt_eur(p.projete)), e(tableau.libelle_fin(p)),
                    e(p.deadline.isoformat() if p.deadline else "—"), self.ecart_html(p),
                    e(sum(1 for t in p.tickets if t.statut == "BLOQUE")),
                    e(sum(1 for t in p.tickets if t.statut == "ATTENTE_HUMAIN")), e(len(p.alertes))])
            L.append('<section><h2>Vue d\'ensemble</h2>{}</section>'.format(self.tableau_html(
                ["Projet", "Client", "Type", "État", "Avancement", "Budget consommé / prévu", "%", "Coût projeté",
                 "Fin projetée", "Deadline", "Écart", "BLOQUE", "ATTENTE_HUMAIN", "Alertes"], lignes)))
        else:
            L.append('<p class="vide">Aucun projet dans <code>projets/</code>.</p>')
        alertes = [[p.slug, a, d] for p in self.projets for a, d in p.alertes] + \
            tableau.alertes_equipe(self.equipe, self.auj)
        L.append('<section><h2>Alertes</h2>{}</section>'.format(self.alertes_html(alertes, True)))
        att = sorted([(t.rang, p, t) for p in self.projets for t in p.tickets if t.statut == "ATTENTE_HUMAIN"],
                     key=lambda x: (x[0], x[1].slug, x[2].id))
        L.append('<section><h2>Décisions humaines attendues</h2>{}</section>'.format(self.tableau_html(
            ["Priorité", "Projet", "Ticket", "Titre", "Porteur", "Question (bloque_par)", "Ancienneté"],
            [[self.badge_prio(t.priorite), e(p.slug), self.lien_ticket(p, t, rel), e(t.titre), e(t.assigne),
              e(t.bloque_par or "non renseigné (S1-R3)"), e(self.anciennete(t, "attente"))] for _, p, t in att],
            "Aucune décision attendue.")))
        blo = [(p, t) for p in self.projets for t in p.tickets if t.statut == "BLOQUE"]
        L.append('<section><h2>Tickets bloqués</h2>{}</section>'.format(self.tableau_html(
            ["Projet", "Ticket", "Titre", "Assigné", "Raison (bloque_par)", "Ancienneté"],
            [[e(p.slug), self.lien_ticket(p, t, rel), e(t.titre), e(t.assigne),
              e(t.bloque_par or "non renseigné (S1-R3)"), e(self.anciennete(t, "bloqu"))] for p, t in blo],
            "Aucun ticket bloqué.")))
        an = list(self.anomalies) + ["{} : {}".format(p.slug, a) for p in self.projets for a in sorted(set(p.anomalies))]
        L.append(self.anomalies_html(an))
        self.ecrire(rel, self.page(rel, "Portefeuille", "\n".join(L), actif="portefeuille"))

    @staticmethod
    def anomalies_html(anomalies):
        if not anomalies:
            return '<section><h2>Anomalies de données</h2><p class="vide ok">Aucune.</p></section>'
        return ('<section><details class="carte"><summary>Anomalies de données ({})</summary><ul>{}</ul></details>'
                '</section>').format(len(anomalies), "".join("<li>{}</li>".format(e(a)) for a in anomalies))

    # ======================================================================== Fiche projet
    def page_projet(self, p):
        base = "projets/" + p.slug
        rel = base + "/index.html"
        fil = [("Portefeuille", "portefeuille.html"), (p.client, None)]
        L = ['<div class="titre-projet"><h1>{}</h1><code>{}</code> {} {}</div>'.format(
            e(p.client), e(p.slug), self.badge(p.type_projet, "type"), self.badge(p.etat, "etat"))]
        # Documents du projet
        chips = []
        for d, lib in self.docs_projet[p.slug]:
            fm, _, _ = lire_md(os.path.join(p.dossier, d + ".md"))
            chips.append('<a class="chip doc" href="{}">{} {}</a>'.format(
                e(self.lien(rel, "{}/{}.html".format(base, d))), e(lib),
                self.badge_doc(fm.get("statut")) if fm.get("statut") else ""))
        chips.append('<a class="chip doc" href="{}">Le bureau (vue de dessus, replay)</a>'.format(
            e(self.lien(rel, "bureau.html#projet=" + quote(p.slug)))))
        L.append('<div class="chips grandes">{}</div>'.format("".join(chips)))
        # Synthèse
        budget_det = "{} sur {}".format(tableau.fmt_eur(p.consomme), tableau.fmt_eur(p.budget)) if p.budget \
            else "{} · budget non renseigné".format(tableau.fmt_eur(p.consomme))
        L.append('<section class="grille stats">')
        L.append(self.stat("avancement", e(tableau.fmt_pct(p.avancement)), self.barre(p.avancement) + e(
            "{} terminées / {} estimées".format(tableau.fmt_h(p.est_termine), tableau.fmt_h(p.est_total)))))
        L.append(self.stat("budget consommé", e(tableau.fmt_pct(p.part_budget)),
                           self.barre(p.part_budget, "budget") + e(budget_det)))
        L.append(self.stat("coût projeté à terminaison", e(tableau.fmt_eur(p.projete)),
                           e("temps restant {}".format(tableau.fmt_h(p.temps_restant)))))
        L.append(self.stat("fin projetée", e(tableau.libelle_fin(p)), "deadline {} · écart {}".format(
            e(p.deadline.isoformat() if p.deadline else "non renseignée"), self.ecart_html(p))))
        L.append("</section>")
        L.append('<section><h2>Alertes</h2>{}</section>'.format(self.alertes_html(p.alertes, False)))
        attentes = sorted([t for t in p.tickets if t.statut == "ATTENTE_HUMAIN"], key=lambda t: (t.rang, t.id))
        bloques = [t for t in p.tickets if t.statut == "BLOQUE"]
        L.append('<div class="grille deux">')
        L.append('<section><h2>En attente d\'une décision humaine</h2>{}</section>'.format(self.tableau_html(
            ["Ticket", "Priorité", "Titre", "Question", "Ancienneté"],
            [[self.lien_ticket(p, t, rel), self.badge_prio(t.priorite), e(t.titre),
              e(t.bloque_par or "non renseigné (S1-R3)"), e(self.anciennete(t, "attente"))] for t in attentes],
            "Aucune décision attendue.")))
        L.append('<section><h2>Tickets bloqués</h2>{}</section>'.format(self.tableau_html(
            ["Ticket", "Titre", "Assigné", "Raison", "Ancienneté"],
            [[self.lien_ticket(p, t, rel), e(t.titre), e(t.assigne), e(t.bloque_par or "non renseigné (S1-R3)"),
              e(self.anciennete(t, "bloqu"))] for t in bloques], "Aucun ticket bloqué.")))
        L.append("</div>")
        L.append(self.kanban(p, rel))
        gantt = gantt_par_statut(p)
        if gantt:
            g = '<pre class="mermaid">{}</pre>{}'.format(e(gantt), LEGENDE_GANTT)
        else:
            g = '<p class="vide">Aucun ticket à représenter.</p>'
        L.append('<section class="carte" id="gantt"><h2>Planning prévisionnel (Gantt)</h2><p class="intro">'
                 'Ordonnancement de <code>tableau.py</code> à partir du {} : dépendances, priorité, un ticket à la '
                 'fois par assigné ; les tickets BLOQUE et ATTENTE_HUMAIN sont supposés débloqués aujourd\'hui.</p>'
                 '<div class="gantt">{}</div></section>'.format(e(self.auj.isoformat()), g))
        util = []
        for u in p.utilisation:
            if u["raison"]:
                obs = u["raison"]
            elif u["taux"] is None:
                obs = "capacité nulle sur la période"
            elif u["taux"] > 1.0:
                obs = "surcharge"
            elif u["taux"] < tableau.SEUIL_UTILISATION:
                obs = "sous {} : ajuster l'allocation ?".format(tableau.fmt_pct(tableau.SEUIL_UTILISATION))
            else:
                obs = "—"
            util.append(['<a href="{}">{}</a>'.format(e(self.lien(rel, "equipe.html#membre-" + u["cle"])),
                                                      e(u["prenom"].capitalize())),
                         e(tableau.fmt_nb(u["allocation"], 0) + " %"), e(tableau.fmt_h(u["heures"])),
                         e(tableau.fmt_h(u["capacite"])),
                         self.barre(u["taux"], "budget") + e(tableau.fmt_pct(u["taux"])), e(obs)])
        L.append('<section><h2>Utilisation des salariés (AF9, indicateur)</h2>{}</section>'.format(self.tableau_html(
            ["Salarié", "Allocation", "h restantes assignées", "Capacité allouée", "Utilisation", "Observation"], util,
            "Aucun salarié alloué ni assigné.")))
        sal = [t for t in p.ouverts if tableau.decouper_assigne(t.assigne)[0] == "salarie"]
        L.append('<section><h2>Tickets à faire par un humain (AF11, R15)</h2>{}</section>'.format(self.tableau_html(
            ["Ticket", "Titre", "Assigné", "Statut", "Reste", "Fenêtre prévue"],
            [[self.lien_ticket(p, t, rel), e(t.titre), e(t.assigne), self.badge_statut(t.statut),
              e(tableau.fmt_h(t.reste)), e("{} → {}".format(t.debut_prevu.isoformat(), t.fin_prevue.isoformat())
                                          if t.fin_prevue else "non planifiable")] for t in sal])))
        L.append(self.anomalies_html(sorted(set(p.anomalies))))
        self.ecrire(rel, self.page(rel, p.client, "\n".join(L), actif="portefeuille", fil=fil))
        for d, lib in self.docs_projet[p.slug]:
            self.page_document("{}/{}.md".format(base, d), "{}/{}.html".format(base, d),
                               [("Portefeuille", "portefeuille.html"), (p.client, rel), (lib, None)])
        for nom in self.tickets_fichiers[p.slug]:
            self.page_ticket(p, nom)

    def kanban(self, p, rel):
        colonnes = list(tableau.STATUTS)
        if any(t.statut not in tableau.STATUTS for t in p.tickets):
            colonnes.append("?")
        html_cols = []
        for s in colonnes:
            cartes = []
            for t in p.tickets:
                if (t.statut if t.statut in tableau.STATUTS else "?") != s:
                    continue
                nature = tableau.decouper_assigne(t.assigne)[0]
                attente = ('<div class="k-bloque">{}</div>'.format(e(t.bloque_par))
                           if t.statut in ("BLOQUE", "ATTENTE_HUMAIN") and t.bloque_par else "")
                cartes.append(
                    '<a class="k-carte prio-bord-{prio}" href="{lien}" data-ticket="{id}"><div class="k-tete">'
                    '<strong>{id}</strong>{badge}</div><div class="k-titre">{titre}</div>{attente}'
                    '<div class="k-pied"><span class="qui {nat}">{qui}</span><span>{passe} / {est}</span>'
                    '<span class="type">{type_}</span></div></a>'.format(
                        prio=classe(t.priorite), id=e(t.id), titre=e(t.titre), attente=attente,
                        lien=e(self.lien(rel, "projets/{}/tickets/{}.html".format(p.slug, t.fichier[:-3]))),
                        badge=self.badge_prio(t.priorite), nat="salarie" if nature == "salarie" else "agent",
                        qui=e(t.assigne.split(":", 1)[-1] if t.assigne else "sans assigné"),
                        passe=e(tableau.fmt_nb(t.temps_passe, 1)), est=e(tableau.fmt_h(t.estimation)),
                        type_=e(t.type or "—")))
            html_cols.append('<div class="k-col st-col-{c}" data-statut="{s}"><div class="k-col-tete">{badge}'
                             '<span class="k-nb">{n}</span></div><div class="k-cartes">{cartes}</div></div>'.format(
                                 c=classe(s), s=e(s), badge=self.badge_statut(s if s != "?" else "statut inconnu"),
                                 n=len(cartes), cartes="".join(cartes) or '<p class="k-vide">—</p>'))
        return ('<section id="kanban"><h2>Tickets par statut</h2><p class="intro">{} ticket(s). Les tickets sont la '
                'source de vérité de l\'avancement (R9).</p><div class="kanban">{}</div></section>').format(
            len(p.tickets), "".join(html_cols))

    def page_ticket(self, p, nom):
        base = "projets/" + p.slug
        source, rel = "{}/tickets/{}".format(base, nom), "{}/tickets/{}.html".format(base, nom[:-3])
        fm, corps, err = lire_md(os.path.join(p.dossier, "tickets", nom))
        t = next((x for x in p.tickets if x.fichier == nom), None)
        tid = tableau.texte(fm.get("id")) or nom[:5]
        champs = []
        if err:
            champs.append(("Anomalie", '<span class="avert">{}</span>'.format(e(err))))
        statut = tableau.texte(fm.get("statut")).upper()
        if fm:
            champs.append(("Statut", self.badge_statut(statut)))
            champs.append(("Priorité", self.badge_prio(tableau.texte(fm.get("priorite")).lower())))
            for cle, lib in (("type", "Type"), ("assigne", "Assigné"), ("competence_requise", "Compétence requise")):
                champs.append((lib, e(tableau.texte(fm.get(cle)) or "—")))
            champs.append(("Temps", e("{} passées / {} estimées".format(
                tableau.fmt_h(tableau.en_nombre(fm.get("temps_passe_h")) or 0),
                tableau.fmt_h(tableau.en_nombre(fm.get("estimation_h")) or 0)))))
            deps = t.depend_de if t else []
            champs.append(("Dépend de", ", ".join(
                self.lien_ticket(p, p.par_id[d], rel) if d in p.par_id else e(d) for d in deps) or "—"))
            if tableau.texte(fm.get("bloque_par")):
                champs.append(("Bloqué par", e(fm.get("bloque_par"))))
            if tableau.texte(fm.get("decision")):
                champs.append(("Décision", self.lien_dec(tableau.texte(fm.get("decision")), rel)))
            champs.append(("Validation humaine requise", e(tableau.texte(fm.get("validation_humaine_requise")) or "—")))
            if t and t.fin_prevue:
                champs.append(("Fenêtre prévue", e("{} → {}".format(t.debut_prevu.isoformat(), t.fin_prevue.isoformat()))))
            elif t and t.non_planifiable:
                champs.append(("Planification", '<span class="avert">{}</span>'.format(e(t.non_planifiable))))
            dates = ["{} {}".format(lib, tableau.texte(fm.get(cle))) for cle, lib in
                     (("cree_le", "créé le"), ("maj_le", "mis à jour le"), ("statut_depuis", "statut depuis"),
                      ("debut_le", "commencé le"), ("termine_le", "terminé le")) if tableau.texte(fm.get(cle))]
            champs.append(("Dates", e(" · ".join(dates)) or "—"))
            champs.append(("Créé par", e(tableau.texte(fm.get("cree_par")) or "—")))
        fiche = '<dl class="fiche">{}</dl>'.format("".join("<div><dt>{}</dt><dd>{}</dd></div>".format(e(a), b)
                                                           for a, b in champs))
        corps_md = corps if not err else ""
        brut = '<pre class="code"><code>{}</code></pre>'.format(e(corps)) if err else ""
        contenu = ('<article class="doc ticket"><div class="ticket-tete"><span class="tid">{tid}</span><h1>{titre}</h1>'
                   '</div>{fiche}<div class="md">{md}{brut}</div><p class="source">Fichier : <a href="{src}"><code>'
                   '{nom}</code></a></p></article>').format(
            tid=e(tid), titre=e(tableau.texte(fm.get("titre")) or nom), fiche=fiche,
            md=self.md(re.sub(r"^#\s+.*$", "", corps_md, count=1, flags=re.M), source, rel), brut=brut,
            src=e(self.lien(rel, "../" + source)), nom=e(source))
        fil = [("Portefeuille", "portefeuille.html"), (p.client, base + "/index.html#kanban"), (tid, None)]
        self.ecrire(rel, self.page(rel, "{} · {}".format(tid, p.slug), contenu, actif="portefeuille", fil=fil))

    # ======================================================================== Équipe
    def page_equipe(self):
        rel = "equipe.html"
        eq = self.equipe
        L = ['<h1>Équipe</h1><p class="intro">Salariés, allocations décidées par un humain (S1-R10), capacité et '
             'calendrier. <code>equipe/</code> n\'est écrit que par le coordinateur, après décision humaine.</p>']
        L.append('<section><h2>Alertes de l\'équipe</h2>{}</section>'.format(
            self.alertes_html([l[1:] for l in tableau.alertes_equipe(eq, self.auj)], False)))
        cartes = []
        for cle in sorted(eq.membres):
            m, fiche = eq.membres[cle], self.fiches.get(cle) or {}
            total = sum(m["allocation"].values())
            allocs = []
            for slug, pct in sorted(m["allocation"].items()):
                util = next((u for p in self.projets if p.slug == slug for u in p.utilisation if u["cle"] == cle), None)
                det = '<div class="meta">utilisation (AF9) : {}</div>'.format(e(tableau.fmt_pct(util["taux"]))) \
                    if util and util["taux"] is not None else ""
                allocs.append('<div class="jauge"><div class="jauge-lib"><span>{}</span><strong>{}</strong></div>{}{}'
                              '</div>'.format(e(slug), e(tableau.fmt_nb(pct, 0) + " %"), self.barre(pct / 100.0), det))
            comp = "".join('<span class="chip niv-{}">{} <small>{}</small></span>'.format(
                classe(c.get("niveau")), e(c.get("nom")), e(c.get("niveau") or "")) for c in fiche.get("competences") or []
                if isinstance(c, dict))
            taux_h = m["cout_j"] / tableau.HEURES_JOUR if m["cout_j"] else None
            dates = "arrivé·e le {}".format(m["arrivee"].isoformat()) if m["arrivee"] else ""
            dep = eq.date_depart(cle)
            if dep:
                dates += " · départ le {}".format(dep.isoformat())
            cartes.append("""<article class="carte membre" id="membre-{cle}">
  <div class="membre-tete"><div class="avatar" aria-hidden="true">{init}</div><div><h3>{prenom}</h3>
  <div class="meta">{role}</div></div></div>
  <div class="meta-ligne">{niveau} {statut}</div>
  <dl class="mini"><div><dt>Coût</dt><dd>{cout}</dd></div><div><dt>Capacité</dt><dd>{cap}</dd></div>
  <div><dt>Allocation totale</dt><dd class="{cl_total}">{total}</dd></div></dl>
  {allocs}
  <div class="chips">{comp}</div>
  <p class="meta">{dates}</p>
</article>""".format(cle=e(cle), init=e(m["prenom"][:1].upper()), prenom=e(m["prenom"].capitalize()),
                     role=e(fiche.get("role") or ""), niveau=self.badge(m["niveau"] or "—", "niv"),
                     statut=self.badge(m["statut"] or "—", "mbr"),
                     cout=e("{} /j ({} /h)".format(tableau.fmt_eur(m["cout_j"]), tableau.fmt_eur(taux_h))
                            if m["cout_j"] else "—"),
                     cap=e("{} /semaine".format(tableau.fmt_h(m["cap_sem"]))),
                     cl_total="rouge" if total > 100 else "", total=e(tableau.fmt_nb(total, 0) + " %"),
                     allocs="".join(allocs) or '<p class="vide">Aucune allocation.</p>', comp=comp, dates=e(dates)))
        L.append('<section><h2>Salariés</h2><div class="grille membres">{}</div></section>'.format(
            "".join(cartes) or '<p class="vide">Aucune fiche dans <code>equipe/membres/</code>.</p>'))
        L.append('<section class="carte"><h2>Agents IA</h2><p>{} agent(s) au catalogue, au coût fictif de {} par heure '
                 'équivalent humain (ARCHITECTURE § 8). <a href="agents.html">Voir les agents et les skills →</a></p>'
                 '</section>'.format(e(len(self.catalogue) or len(self.agents)), e(tableau.fmt_eur(eq.taux_agent))))
        evs = sorted(eq.evenements, key=lambda ev: (ev["debut"], ev["id"]))
        lignes = []
        for ev in evs:
            passe = ev["fin"] < self.auj
            lignes.append([e(ev["id"]), e(ev["qui"].split(":", 1)[-1].capitalize()), self.badge(ev["type"], "ev"),
                           e(ev["debut"].isoformat()), e(ev["fin"].isoformat()), e(ev["motif"] or "—"),
                           e("{} %".format(tableau.fmt_nb(ev["capacite_pct"], 0))), e(ev["statut"] or "—"),
                           self.badge("passé" if passe else "à venir", "quand", "passe" if passe else "avenir")])
        feries = ", ".join(d.isoformat() for d in sorted(eq.feries)) or "aucun"
        L.append('<section id="calendrier"><h2>Calendrier : absences, arrivées et départs</h2>{}<p class="meta">'
                 'Jours fériés : {}. Les événements annulés ne sont pas affichés.</p></section>'.format(
                     self.tableau_html(["Id", "Qui", "Type", "Du", "Au", "Motif", "Capacité restante", "Statut",
                                        ""], lignes, "Aucun événement."), e(feries)))
        L.append(self.anomalies_html(eq.anomalies))
        self.ecrire(rel, self.page(rel, "Équipe", "\n".join(L), actif="equipe"))

    # ======================================================================== Agents et skills
    def phrase(self, nom):
        if nom in PHRASES:
            return '<blockquote class="phrase">{}</blockquote>'.format(e(PHRASES[nom]))
        return ('<blockquote class="phrase generique">Lance {} sur le projet &lt;slug&gt;.</blockquote>'
                '<p class="meta">Phrase générique : à préciser dans <code>PHRASES</code> de '
                '<code>scripts/console.py</code>.</p>').format(e(nom))

    def carte_agent(self, a, rel):
        fm = a["fm"] or {}
        role = section(a["corps"], r"^Rôle")
        arrets = section(a["corps"], r"Quand s'arrêter")
        outils = [o.strip() for o in str(fm.get("tools") or "").split(",") if o.strip()]
        return """<article class="carte agent" id="agent-{id}">
  <div class="agent-tete"><h3>{nom}</h3>{modele}</div>
  <div class="md role">{role}</div>
  <h4>Quand l'appeler</h4><p class="desc">{desc}</p>
  <h4>Outils</h4><div class="chips">{outils}</div>
  <details><summary>Points d'arrêt humains</summary><div class="md">{arrets}</div></details>
  <h4>Phrase à taper au coordinateur</h4>{phrase}
  <p class="plus"><a href="{page}">Fichier complet →</a></p>
</article>""".format(id=e(a["nom"]), nom=e(a["nom"]),
                     modele=self.badge("modèle " + str(fm.get("model") or "?"), "modele", fm.get("model") or "aucun"),
                     role=self.md(role, a["source"], rel) if role else "", desc=e(fm.get("description") or "—"),
                     outils="".join('<span class="chip">{}</span>'.format(e(o)) for o in outils) or "—",
                     arrets=self.md(arrets, a["source"], rel) if arrets else '<p class="vide">Section absente.</p>',
                     phrase=self.phrase(a["nom"]), page=e(a["page"]))

    def carte_skill(self, s, rel):
        fm = s["fm"] or {}
        quand = section(s["corps"], r"^Quand l'utiliser")
        arret = section(s["corps"], r"^Point d'arrêt")
        humain = self.badge("humain", "modele", "humain") if s["nom"] in SKILLS_HUMAINS else \
            self.badge("coordinateur", "modele", "coordinateur")
        return """<article class="carte agent skill" id="skill-{id}">
  <div class="agent-tete"><h3>{nom}</h3>{humain}</div>
  <p class="desc">{desc}</p>
  <h4>Quand l'utiliser</h4><div class="md">{quand}</div>
  <details><summary>Point d'arrêt humain</summary><div class="md">{arret}</div></details>
  <h4>Phrase à taper au coordinateur</h4>{phrase}
  <p class="plus"><a href="{page}">Procédure complète →</a></p>
</article>""".format(id=e(s["nom"]), nom=e(s["nom"]), humain=humain, desc=e(fm.get("description") or "—"),
                     quand=self.md(quand, s["source"], rel) if quand else "—",
                     arret=self.md(arret, s["source"], rel) if arret else '<p class="vide">Section absente.</p>',
                     phrase=self.phrase(s["nom"]), page=e(s["page"]))

    def page_agents(self):
        rel = "agents.html"
        L = ['<h1>Agents et skills</h1><p class="intro">Le coordinateur (session principale de Claude Code) choisit '
             'les agents, décide de l\'ordre et s\'arrête à chaque validation humaine. Aucun agent ne lance un autre '
             'agent (R1).</p>']
        par_sys, autres = {}, []
        for a in self.agents:
            sys_ = str((self.catalogue.get(a["nom"]) or {}).get("systeme") or "")
            sys_ = "realisation" if tableau.sans_accents(sys_).lower() == "realisation" else sys_.upper()
            if any(code == sys_ for code, _, _ in SYSTEMES):
                par_sys.setdefault(sys_, []).append(a)
            else:
                autres.append(a)
        sommaire = []
        for code, titre, intro in SYSTEMES + [("autres", "Autres agents", "Agents absents d'equipe/agents.md.")]:
            agents = par_sys.get(code, []) if code != "autres" else autres
            if not agents:
                continue
            page_sys = next((s["page"] for s in self.systemes if s["code"] == code), None)
            entete = "{} · {}".format(code, titre) if code not in ("realisation", "autres") else titre
            lien_sys = ' <a class="petit-lien" href="{}">lire le système →</a>'.format(e(page_sys)) if page_sys else ""
            sommaire.append('<a class="chip" href="#sys-{}">{} ({})</a>'.format(e(classe(code)), e(entete), len(agents)))
            L.append('<section class="groupe sys-{c}" id="sys-{c}"><h2>{t}</h2><p class="intro">{i}{l}</p>'
                     '<div class="grille agents">{cartes}</div></section>'.format(
                         c=e(classe(code)), t=e(entete), i=e(intro), l=lien_sys,
                         cartes="".join(self.carte_agent(a, rel) for a in agents)))
        if not self.agents:
            L.append('<p class="vide">Aucun agent dans <code>.claude/agents/</code>.</p>')
        sommaire.append('<a class="chip" href="#skills">Skills ({})</a>'.format(len(self.skills)))
        L.insert(1, '<nav class="chips grandes sommaire">{}</nav>'.format("".join(sommaire)))
        L.append('<section class="groupe" id="skills"><h2>Skills</h2><p class="intro">Procédures réutilisables du '
                 'coordinateur (<code>.claude/skills/</code>) ; le skill <code>recette</code> est suivi par un salarié, '
                 'jamais par un agent.</p><div class="grille agents">{}</div></section>'.format(
                     "".join(self.carte_skill(s, rel) for s in self.skills) or '<p class="vide">Aucun skill.</p>'))
        self.ecrire(rel, self.page(rel, "Agents et skills", "\n".join(L), actif="agents"))
        for a in self.agents:
            self.page_document(a["source"], a["page"], [("Agents et skills", "agents.html"), (a["nom"], None)])
        for s in self.skills:
            self.page_document(s["source"], s["page"], [("Agents et skills", "agents.html#skills"), (s["nom"], None)])

    # ======================================================================== Le bureau
    def page_bureau(self):
        """Page « Le bureau » (DEC-016) : données et HTML calculés par scripts/bureau.py, rendu Canvas par
        scripts/bureau.js copié dans console/assets/. Comme toute la console, écrit seulement dans console/."""
        rel = "bureau.html"
        if os.path.isfile(bureau.SCRIPT_JS):
            with open(bureau.SCRIPT_JS, "rb") as f:
                self.ecrire("assets/bureau.js", f.read())
        else:
            self.avertissements.append("scripts/bureau.js absent : la vue dessinée du bureau est indisponible")
        donnees = bureau.Donnees(self, rel).calculer()
        self.ecrire(rel, self.page(rel, "Le bureau", bureau.page_html(self, donnees), actif="bureau"))

    # ======================================================================== Décisions
    def page_decisions(self):
        rel = "decisions.html"
        comptes = {}
        lignes = []
        for d in self.decisions:
            fm = d["fm"] or {}
            n = statut_document(fm.get("statut"))
            comptes[n] = comptes.get(n, 0) + 1
            regle = tableau.texte(fm.get("modifie_une_regle")).lower()
            lignes.append(['<a class="nowrap" href="{}">{}</a>'.format(e(d["page"]), e(d["id"])),
                           '<span class="nowrap">{}</span>'.format(e(fm.get("date") or d["date"])),
                           e(fm.get("titre") or "—"), e(fm.get("projet") or "—"), e(fm.get("ticket") or "—"),
                           e(fm.get("decide_par") or "—"), self.badge_doc(fm.get("statut")),
                           e(fm.get("valide_par") or "—"),
                           self.badge("oui", "regle", "oui") if regle.startswith("oui") else e("non")])
        L = ['<h1>Registre des décisions</h1><p class="intro">Chaque validation, arbitrage, événement d\'équipe, GO de '
             'mise en production ou modification de règle est tracé dans <code>docs/decisions/</code> (R7). Le statut '
             'affiché est celui de l\'en-tête de chaque fichier.</p>']
        L.append('<section class="grille stats">{}{}{}</section>'.format(
            self.stat("décisions", e(len(self.decisions))),
            self.stat("validées", e(comptes.get("VALIDE", 0))),
            self.stat("en revue", e(comptes.get("EN_REVUE", 0)), "à valider par un humain (R5)")))
        L.append('<section>{}</section>'.format(self.tableau_html(
            ["Id", "Date", "Sujet", "Projet", "Ticket", "Décidé par", "Statut", "Validé par", "Règle modifiée"],
            lignes, "Aucune décision.")))
        if validations is not None:
            try:
                n, anomalies = validations.controler(self.racine)
                contenu = ('<p class="vide ok">{} document(s) contrôlé(s) : aucune anomalie.</p>'.format(n)
                           if not anomalies else '<ul>{}</ul>'.format("".join("<li>{}</li>".format(e(a))
                                                                               for a in anomalies)))
            except Exception as ex:  # pragma: no cover - robustesse
                contenu = '<p class="avert">Contrôle impossible : {}</p>'.format(e(ex))
            L.append('<section class="carte"><h2>Contrôle des validations (garde-fous 3 à 5)</h2><p class="intro">'
                     'Même contrôle que la CI <code>validations.yml</code> : chaque document VALIDÉ a '
                     '<code>valide_par</code> et une décision existante.</p>{}</section>'.format(contenu))
        self.ecrire(rel, self.page(rel, "Décisions", "\n".join(L), actif="decisions"))
        for d in self.decisions:
            self.page_document(d["source"], d["page"], [("Décisions", "decisions.html"), (d["id"], None)])


# ============================================================================ feuille de style

CSS = """/* Console de l'ESN : feuille de style générée par scripts/console.py (aucun framework). */
:root {
  --fond: #f5f7fb; --carte: #ffffff; --texte: #1b2333; --doux: #5b6576; --ligne: #e3e8f0;
  --marque: #1e3a8a; --marque-2: #3b5bdb; --ok: #16a34a; --alerte: #d97706; --danger: #dc2626;
  --rayon: 12px; --ombre: 0 1px 2px rgba(16,24,40,.06), 0 4px 14px rgba(16,24,40,.06);
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--fond); color: var(--texte); line-height: 1.55;
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
a { color: var(--marque-2); text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace; font-size: .88em;
  background: #eef1f7; padding: .1em .35em; border-radius: 5px; }
h1 { font-size: 1.75rem; margin: .2em 0 .4em; letter-spacing: -.01em; }
h2 { font-size: 1.2rem; margin: 1.6em 0 .6em; }
h3 { font-size: 1.05rem; margin: 0; }
h4 { font-size: .8rem; text-transform: uppercase; letter-spacing: .05em; color: var(--doux); margin: 1em 0 .35em; }
.entete { background: linear-gradient(90deg, #0f1f4d, var(--marque)); color: #fff; position: sticky; top: 0; z-index: 10;
  box-shadow: 0 2px 10px rgba(15,31,77,.25); }
.entete-in { max-width: 1320px; margin: 0 auto; padding: .7rem 1.2rem; display: flex; align-items: center; gap: 1.5rem;
  flex-wrap: wrap; }
.marque { color: #fff; font-weight: 700; font-size: 1.1rem; letter-spacing: .02em; }
.marque span:not(.logo) { font-weight: 400; opacity: .7; }
.marque:hover { text-decoration: none; }
.logo { color: #93c5fd; }
.nav { display: flex; gap: .25rem; flex-wrap: wrap; }
.nav a { color: #dbe4ff; padding: .4rem .75rem; border-radius: 8px; font-size: .93rem; }
.nav a:hover { background: rgba(255,255,255,.1); text-decoration: none; }
.nav a.actif { background: #fff; color: var(--marque); font-weight: 600; }
main { max-width: 1320px; margin: 0 auto; padding: 1.4rem 1.2rem 3rem; }
.pied { max-width: 1320px; margin: 0 auto; padding: 1rem 1.2rem 2rem; color: var(--doux); font-size: .85rem;
  border-top: 1px solid var(--ligne); }
.fil { font-size: .88rem; color: var(--doux); margin-bottom: .6rem; }
.intro { color: var(--doux); margin-top: 0; }
.meta { color: var(--doux); font-size: .87rem; }
.vide { color: var(--doux); font-style: italic; }
.nowrap { white-space: nowrap; }
.vide.ok { color: var(--ok); font-style: normal; }
.avert { background: #fff7ed; border: 1px solid #fed7aa; color: #9a3412; padding: .5rem .75rem; border-radius: 8px; }
.plus { margin: .8rem 0 0; font-weight: 600; font-size: .92rem; }
.carte { background: var(--carte); border: 1px solid var(--ligne); border-radius: var(--rayon); box-shadow: var(--ombre);
  padding: 1.1rem 1.2rem; margin: 1rem 0; }
a.carte { color: inherit; display: block; transition: transform .12s ease, box-shadow .12s ease; }
a.carte:hover { text-decoration: none; transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(16,24,40,.08), 0 10px 24px rgba(16,24,40,.10); }
.carte > h2:first-child { margin-top: 0; }
.grille { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.grille > .carte { margin: 0; }
.grille.deux { grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 1.2rem; }
.grille.stats { grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); margin: 1rem 0; }
.grille.projets { grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
.grille.agents { grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); }
.grille.membres { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
.grille.systemes { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.stat-val { font-size: 1.7rem; font-weight: 700; color: var(--marque); line-height: 1.2; }
.stat-lib { color: var(--doux); font-size: .9rem; }
.stat-det { font-size: .84rem; color: var(--doux); margin-top: .5rem; }
.hero { background: linear-gradient(120deg, #1e3a8a, #3b5bdb 60%, #6d28d9); color: #fff; border-radius: 16px;
  padding: 2rem 1.8rem; margin-bottom: 1rem; box-shadow: var(--ombre); }
.hero h1 { margin: 0 0 .3rem; font-size: 2rem; }
.sous-titre { margin: 0; opacity: .9; max-width: 60rem; font-size: 1.05rem; }
.badge { display: inline-block; font-size: .74rem; font-weight: 600; padding: .16em .6em; border-radius: 999px;
  border: 1px solid transparent; white-space: nowrap; vertical-align: middle; background: #eef1f7; color: #334155; }
.st-a-faire { background: #f1f5f9; color: #334155; border-color: #cbd5e1; }
.st-en-cours { background: #dbeafe; color: #1d4ed8; }
.st-en-revue { background: #ede9fe; color: #6d28d9; }
.st-bloque { background: #fee2e2; color: #b91c1c; }
.st-attente-humain { background: #fef3c7; color: #92400e; }
.st-termine { background: #dcfce7; color: #15803d; }
.st-annule { background: #f3f4f6; color: #6b7280; text-decoration: line-through; }
.doc-valide { background: #dcfce7; color: #15803d; }
.doc-en-revue { background: #ede9fe; color: #6d28d9; }
.doc-brouillon { background: #f1f5f9; color: #475569; }
.prio-critique { background: #dc2626; color: #fff; }
.prio-haute { background: #ffedd5; color: #c2410c; }
.prio-normale { background: #e0e7ff; color: #3730a3; }
.prio-basse { background: #f1f5f9; color: #64748b; }
.al-budget, .al-delais, .al-critique, .al-surcharge, .al-non-planifiable { background: #fee2e2; color: #b91c1c; }
.al-preavis-de-depart, .al-absence-s1-r9, .al-sans-mise-a-jour, .al-allocation { background: #ffedd5; color: #c2410c; }
.al-utilisation-info { background: #e0f2fe; color: #0369a1; }
.ecart-retard { background: #fee2e2; color: #b91c1c; }
.ecart-ok { background: #dcfce7; color: #15803d; }
.modele-opus { background: #ede9fe; color: #6d28d9; }
.modele-sonnet { background: #dbeafe; color: #1d4ed8; }
.modele-haiku { background: #dcfce7; color: #15803d; }
.modele-humain { background: #fef3c7; color: #92400e; }
.regle-oui { background: #fef3c7; color: #92400e; }
.quand-passe { background: #f3f4f6; color: #6b7280; }
.quand-avenir { background: #dbeafe; color: #1d4ed8; }
.niv-expert, .chip.niv-expert { background: #ede9fe; color: #5b21b6; }
.niv-confirme, .chip.niv-confirme { background: #dbeafe; color: #1e40af; }
.niv-debutant, .chip.niv-debutant { background: #f1f5f9; color: #475569; }
.mbr-actif { background: #dcfce7; color: #15803d; }
.mbr-depart-prevu, .mbr-conges { background: #ffedd5; color: #c2410c; }
.mbr-parti { background: #f3f4f6; color: #6b7280; }
.mbr-en-integration { background: #e0f2fe; color: #0369a1; }
.barre { height: 8px; background: #e8edf5; border-radius: 999px; overflow: hidden; margin: .35rem 0; }
.barre span { display: block; height: 100%; background: linear-gradient(90deg, #3b82f6, #2563eb); border-radius: 999px; }
.barre.ok span { background: linear-gradient(90deg, #22c55e, #16a34a); }
.barre.alerte span { background: linear-gradient(90deg, #f59e0b, #d97706); }
.barre.danger span { background: linear-gradient(90deg, #ef4444, #dc2626); }
.stat .barre.ok span { background: linear-gradient(90deg, #3b82f6, #2563eb); }
.stat .barre.ok.budget span { background: var(--ok); }
.jauge { margin: .55rem 0; }
.jauge-lib { display: flex; justify-content: space-between; font-size: .86rem; color: var(--doux); gap: .5rem; }
.jauge-lib strong { color: var(--texte); }
.projet-tete { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; }
.meta-ligne { display: flex; gap: .35rem; flex-wrap: wrap; align-items: center; margin: .45rem 0; }
dl.mini { display: grid; grid-template-columns: repeat(3, 1fr); gap: .5rem; margin: .7rem 0; }
dl.mini dt { font-size: .74rem; color: var(--doux); text-transform: uppercase; letter-spacing: .04em; }
dl.mini dd { margin: 0; font-weight: 600; font-size: .92rem; }
.compteurs { display: flex; gap: .4rem; flex-wrap: wrap; }
.cpt { font-size: .78rem; padding: .2em .6em; border-radius: 6px; background: #f1f5f9; color: var(--doux); }
.cpt.rouge, .rouge { color: #b91c1c; }
.cpt.rouge { background: #fee2e2; }
.cpt.ambre { background: #fef3c7; color: #92400e; }
.cpt.orange { background: #ffedd5; color: #c2410c; }
.table-wrap { overflow-x: auto; background: var(--carte); border: 1px solid var(--ligne); border-radius: var(--rayon);
  box-shadow: var(--ombre); }
.carte .table-wrap, .md .table-wrap { box-shadow: none; }
table { border-collapse: collapse; width: 100%; font-size: .9rem; }
th { text-align: left; background: #f3f6fb; color: #334155; font-weight: 600; font-size: .8rem; text-transform: uppercase;
  letter-spacing: .03em; }
th, td { padding: .55rem .75rem; border-bottom: 1px solid var(--ligne); vertical-align: top; }
tbody tr:nth-child(even) { background: #fafbfe; }
tbody tr:hover { background: #f0f4ff; }
tbody tr:last-child td { border-bottom: 0; }
.chips { display: flex; flex-wrap: wrap; gap: .35rem; margin: .4rem 0; }
.chip { display: inline-flex; align-items: center; gap: .35rem; font-size: .8rem; background: #eef2ff; color: #3730a3;
  padding: .22em .65em; border-radius: 999px; border: 1px solid #e0e7ff; }
a.chip:hover { text-decoration: none; background: #e0e7ff; }
.chips.grandes .chip { font-size: .9rem; padding: .4em .85em; background: #fff; border-color: var(--ligne); color: var(--texte);
  box-shadow: var(--ombre); }
.chip small { opacity: .75; }
.titre-projet { display: flex; align-items: center; gap: .6rem; flex-wrap: wrap; }
.titre-projet h1 { margin-right: .3rem; }
.kanban { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(172px, 1fr); gap: .6rem; overflow-x: auto;
  padding-bottom: .6rem; }
.k-col { background: #eef2f8; border-radius: var(--rayon); padding: .6rem; display: flex; flex-direction: column;
  min-height: 120px; border-top: 4px solid #cbd5e1; }
.st-col-en-cours { border-top-color: #3b82f6; } .st-col-en-revue { border-top-color: #8b5cf6; }
.st-col-bloque { border-top-color: #ef4444; } .st-col-attente-humain { border-top-color: #f59e0b; }
.st-col-termine { border-top-color: #22c55e; } .st-col-annule { border-top-color: #9ca3af; }
.k-col-tete { display: flex; justify-content: space-between; align-items: center; margin-bottom: .5rem; }
.k-nb { font-weight: 700; color: var(--doux); font-size: .85rem; }
.k-cartes { display: flex; flex-direction: column; gap: .5rem; max-height: 72vh; overflow-y: auto; padding-right: 2px; }
.k-carte { display: block; background: #fff; border: 1px solid var(--ligne); border-left: 4px solid #a5b4fc;
  border-radius: 9px; padding: .55rem .65rem; color: inherit; box-shadow: 0 1px 2px rgba(16,24,40,.05); }
.k-carte:hover { text-decoration: none; border-color: #c7d2fe; box-shadow: 0 4px 12px rgba(16,24,40,.10); }
.prio-bord-critique { border-left-color: #dc2626; } .prio-bord-haute { border-left-color: #f97316; }
.prio-bord-basse { border-left-color: #cbd5e1; }
.k-tete { display: flex; justify-content: space-between; align-items: center; font-size: .82rem; }
.k-titre { font-size: .9rem; margin: .25rem 0; font-weight: 500; }
.k-bloque { font-size: .78rem; background: #fff7ed; color: #9a3412; border-radius: 6px; padding: .25rem .4rem; margin: .3rem 0; }
.k-pied { display: flex; flex-wrap: wrap; justify-content: space-between; gap: .1rem .4rem; font-size: .75rem;
  color: var(--doux); }
.k-pied .type { width: 100%; opacity: .8; }
.qui.salarie { color: #92400e; font-weight: 600; } .qui.agent { color: #1d4ed8; }
.k-vide { color: var(--doux); text-align: center; margin: .4rem 0; }
.gantt { overflow-x: auto; }
/* Couleurs du Gantt (les styles de Mermaid sont internes au SVG, d'où !important) */
.gantt svg rect.task { fill: #bfdbfe !important; stroke: #3b82f6 !important; }
.gantt svg rect.active0, .gantt svg rect.active1, .gantt svg rect.active2, .gantt svg rect.active3 {
  fill: #ddd6fe !important; stroke: #7c3aed !important; }
.gantt svg rect.crit0, .gantt svg rect.crit1, .gantt svg rect.crit2, .gantt svg rect.crit3 {
  fill: #fecaca !important; stroke: #dc2626 !important; }
.gantt svg rect.done0, .gantt svg rect.done1, .gantt svg rect.done2, .gantt svg rect.done3 {
  fill: #bbf7d0 !important; stroke: #16a34a !important; }
.gantt svg rect.milestone { fill: #f59e0b !important; stroke: #b45309 !important; }
.gantt svg text.taskText { fill: #1e293b !important; }
.legende-gantt { list-style: none; display: flex; flex-wrap: wrap; gap: .4rem 1.2rem; padding: 0; margin: .6rem 0 0;
  font-size: .86rem; color: var(--doux); }
.legende-gantt li { display: flex; align-items: center; gap: .4rem; }
.pastille { width: 1.3rem; height: .8rem; border-radius: 3px; border: 1.5px solid; display: inline-block; }
.g-afaire { background: #bfdbfe; border-color: #3b82f6; } .g-active { background: #ddd6fe; border-color: #7c3aed; }
.g-crit { background: #fecaca; border-color: #dc2626; } .g-done { background: #bbf7d0; border-color: #16a34a; }
.g-jalon { background: #f59e0b; border-color: #b45309; width: .8rem; transform: rotate(45deg); }
body.plein-ecran { background: #fff; }
body.plein-ecran pre.mermaid { margin: 0; padding: 2vh 2vw; overflow: auto; }
pre.mermaid { background: #fff; text-align: left; margin: .6rem 0; overflow-x: auto; }
pre.mermaid svg { display: block; margin: 0 auto; }
pre.mermaid-brut, pre.code { text-align: left; background: #0f172a; color: #e2e8f0; padding: .9rem 1rem; border-radius: 10px;
  overflow-x: auto; font-size: .82rem; }
pre.code code { background: none; padding: 0; color: inherit; }
.doc { background: var(--carte); border: 1px solid var(--ligne); border-radius: var(--rayon); box-shadow: var(--ombre);
  padding: 1.4rem 1.8rem; max-width: 1100px; }
.bandeau { display: flex; flex-wrap: wrap; gap: .6rem; align-items: center; padding: .6rem .8rem; background: #f6f8fc;
  border: 1px solid var(--ligne); border-radius: 10px; margin: .4rem 0 1.2rem; }
.md h1 { font-size: 1.6rem; } .md h2 { border-bottom: 1px solid var(--ligne); padding-bottom: .25rem; }
.md blockquote { margin: .8rem 0; padding: .5rem 1rem; border-left: 4px solid #a5b4fc; background: #f5f7ff; color: #334155;
  border-radius: 0 8px 8px 0; }
.md hr { border: 0; border-top: 1px solid var(--ligne); margin: 1.5rem 0; }
.md li { margin: .15rem 0; }
.md .table-wrap { margin: .8rem 0; }
.md.petit { font-size: .88rem; }
li.tache { list-style: none; margin-left: -1.3rem; }
.case { display: inline-flex; width: 1.05em; height: 1.05em; border: 2px solid #94a3b8; border-radius: 4px;
  align-items: center; justify-content: center; font-size: .8em; vertical-align: -.15em; color: #fff; }
li.tache.faite .case { background: var(--ok); border-color: var(--ok); }
.lien-inactif { border-bottom: 1px dotted #94a3b8; }
.source { margin-top: 1.5rem; font-size: .85rem; color: var(--doux); }
.ticket-tete { display: flex; align-items: center; gap: .7rem; flex-wrap: wrap; }
.ticket-tete h1 { margin: 0; }
.tid { font-weight: 700; color: #fff; background: var(--marque); border-radius: 8px; padding: .2rem .6rem; }
dl.fiche { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: .6rem 1.2rem;
  background: #f6f8fc; border: 1px solid var(--ligne); border-radius: 10px; padding: .9rem 1rem; margin: 1rem 0 1.4rem; }
dl.fiche dt { font-size: .74rem; text-transform: uppercase; letter-spacing: .04em; color: var(--doux); }
dl.fiche dd { margin: .1rem 0 0; }
.agent-tete { display: flex; justify-content: space-between; align-items: center; gap: .5rem; }
.agent .role p { margin: .5rem 0; }
.agent .desc { font-size: .88rem; color: #334155; margin: 0; }
.agent details, .carte details { margin-top: .7rem; }
details summary { cursor: pointer; font-weight: 600; color: var(--marque); }
details .md { font-size: .88rem; }
.phrase { margin: .2rem 0; padding: .6rem .8rem; background: #0f172a; color: #e2e8f0; border-radius: 9px; font-family:
  ui-monospace, SFMono-Regular, Consolas, monospace; font-size: .84rem; border-left: 4px solid #60a5fa; }
.phrase::before { content: "› "; color: #60a5fa; }
.phrase.generique { border-left-color: #f59e0b; }
.groupe { margin-top: 2rem; }
.groupe > h2 { display: inline-block; margin-bottom: .2rem; }
.petit-lien { font-size: .88rem; font-weight: 600; }
.sommaire { margin: 1rem 0; }
.systeme { position: relative; overflow: hidden; }
.sys-code { position: absolute; right: .9rem; top: .6rem; font-size: 2.2rem; font-weight: 800; color: #e0e7ff; }
.systeme h3 { padding-right: 3rem; }
.systeme .md ul { padding-left: 1.1rem; font-size: .88rem; margin: .4rem 0; }
.arrets ul { columns: 2 340px; column-gap: 2.5rem; padding-left: 1.2rem; }
.membre-tete { display: flex; gap: .7rem; align-items: center; }
.avatar { width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(135deg, #3b5bdb, #6d28d9); color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; flex: none; }
@media (max-width: 720px) {
  .grille.deux, .grille.agents, .grille.projets { grid-template-columns: 1fr; }
  .doc { padding: 1rem; }
  dl.mini { grid-template-columns: 1fr 1fr; }
  .hero { padding: 1.4rem 1.1rem; }
  .hero h1 { font-size: 1.5rem; }
  .entete { position: static; }
}
@media print { .entete, .pied { display: none; } body { background: #fff; } .carte, .doc { box-shadow: none; } }
"""


# ============================================================================ programme principal

def main(argv=None):
    defaut = os.path.dirname(ICI)
    ap = argparse.ArgumentParser(description="Génère la console de consultation (site statique, lecture seule) "
                                             "dans console/ (DEC-012).")
    ap.add_argument("--racine", default=defaut, help="racine du dépôt (défaut : parent de scripts/)")
    ap.add_argument("--date", default="", help="date du calcul AAAA-MM-JJ (défaut : aujourd'hui)")
    ap.add_argument("--mermaid-src", default="", help="URL du script Mermaid (défaut : copie locale de "
                                                      "scripts/vendor/, sinon le CDN {})".format(MERMAID_CDN))
    a = ap.parse_args(argv)
    if tableau.yaml is None:
        tableau.ecrire_stdout("ERREUR: le module PyYAML est absent. Installer : python -m pip install -r "
                              "requirements.txt (Mac : python3 -m pip …)")
        return 2
    aujourdhui = date.today()
    if a.date:
        aujourdhui = tableau.en_date(a.date)
        if aujourdhui is None:
            tableau.ecrire_stdout("ERREUR: --date invalide (AAAA-MM-JJ attendu) : {}".format(a.date))
            return 2
    racine = os.path.abspath(a.racine)
    if not os.path.isdir(racine):
        tableau.ecrire_stdout("ERREUR: --racine introuvable : {}".format(racine))
        return 2
    site = Site(racine, aujourdhui, a.mermaid_src.strip() or None)
    supprimees = site.generer()
    for av in site.avertissements:
        tableau.ecrire_stdout("ATTENTION: " + av)
    pages = sum(1 for c in site.ecrits if c.endswith(".html"))
    tableau.ecrire_stdout("console/ : {} page(s) générée(s), {} page(s) obsolète(s) supprimée(s) · {} projet(s)".format(
        pages, supprimees, len(site.projets)))
    tableau.ecrire_stdout("Ouvrir : {}".format(os.path.join(site.sortie, "index.html")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
