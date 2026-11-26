#!/usr/bin/env python3
"""bureau.py : données et HTML de la page « Le bureau » de la console (DEC-016).

Responsable : D · outil interne de l'ESN, comme console.py (DEC-012) ; ce n'est pas un projet client.

La page montre l'ESN vue de dessus, en pixel art : une pièce par système, l'open space du pôle réalisation,
les bureaux des salariés, l'accueil du coordinateur et un coin café. Elle a deux modes :
- instantané : l'état de chaque personnage vient des tickets du projet choisi (R9) ;
- replay : une chronologie construite à partir des lignes « Journal » des tickets et des décisions DEC.

Ce module ne fait que des calculs : il n'écrit aucun fichier. console.py lui passe son objet Site (inventaire
déjà lu) et écrit lui-même la page dans console/ (seule fonction d'écriture, bornée à console/). Le rendu
Canvas est dans scripts/bureau.js, copié dans console/assets/.

Sécurité : tout le HTML produit ici passe par e() ; les données sont injectées en JSON dans
<script type="application/json"> sans aucun « < », « > », « & », U+2028 ni U+2029 bruts (json_pour_script).
"""
import hashlib
import html
import importlib.util
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # aucun __pycache__ hors de console/ (lecture seule)

ICI = os.path.dirname(os.path.abspath(__file__))


def _module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tableau = _module("tableau_bureau", os.path.join(ICI, "tableau.py"))

SCRIPT_JS = os.path.join(ICI, "bureau.js")
ESN = "_esn"                       # entrée « Toute l'ESN » du sélecteur
STATUTS = tableau.STATUTS
FERMES = tableau.FERMES

# ============================================================================ personnages

COULEURS = {"S1": "#2563eb", "S2": "#16a34a", "S3": "#dc2626", "S4": "#7c3aed", "realisation": "#0d9488",
            "coordinateur": "#1e293b", "salarie": "#d97706", "humain": "#be185d", "visiteur": "#64748b",
            "autres": "#78716c"}

# Membres humains de l'équipe projet (DEC-017) : ils décident et valident (R5, R7). Ce ne sont ni les salariés
# fictifs d'equipe/membres/, ni des visiteurs ; ils sont toujours à l'accueil.
FICHIER_HUMAINS = "equipe/humains.md"
ROLE_HUMAIN = ("Membre de l'équipe projet : décide et valide (R5, R7), et joue les salariés aux arrêts "
               "humains.")

ACCESSOIRES = {
    "analyste-besoin": "bloc-notes", "architecte": "plans", "chef-de-projet": "presse-papiers",
    "dev-backend": "portable", "dev-frontend": "palette", "relecteur-code": "loupe", "testeur": "coche",
    "securite": "bouclier", "deployeur": "fusee", "veilleur": "longue-vue", "analyste-prod": "courbe",
    "support": "casque", "gestionnaire-crise": "gyrophare", "coordinateur": "talkie",
}
# Mots-clés (sans accents, en minuscules) cherchés dans le nom puis dans le rôle : un agent ajouté plus tard
# reçoit un accessoire sans modifier le code ; à défaut, une tasse.
MOTS_CLES = [("crise", "gyrophare"), ("secur", "bouclier"), ("deploi", "fusee"), ("test", "coche"),
             ("recett", "coche"), ("relect", "loupe"), ("revue", "loupe"), ("veill", "longue-vue"),
             ("support", "casque"), ("client", "casque"), ("prod", "courbe"), ("archi", "plans"),
             ("analys", "bloc-notes"), ("chef", "presse-papiers"), ("projet", "presse-papiers"),
             ("front", "palette"), ("design", "palette"), ("dev", "portable"), ("lead", "portable"),
             ("backend", "portable"), ("coordin", "talkie")]

SYSTEMES_CONNUS = ("S1", "S2", "S3", "S4", "realisation")


def e(valeur):
    return html.escape("" if valeur is None else str(valeur), quote=True)


def normal(texte):
    return tableau.sans_accents("" if texte is None else str(texte)).lower().strip()


def tronquer(texte, n):
    texte = re.sub(r"\s+", " ", texte or "").strip()
    return texte if len(texte) <= n else texte[:n - 1].rstrip() + "…"


def accessoire(nom, role=""):
    if nom in ACCESSOIRES:
        return ACCESSOIRES[nom]
    for texte in (normal(nom), normal(role)):
        for mot, acc in MOTS_CLES:
            if mot in texte:
                return acc
    return "tasse"


def empreinte(nom):
    """Entier stable tiré du nom : teint, cheveux et coiffure identiques d'une génération à l'autre."""
    return int(hashlib.sha256(nom.encode("utf-8")).hexdigest()[:8], 16)


def premiere_phrase(texte):
    t = re.sub(r"\s+", " ", texte or "").strip()
    m = re.match(r"^(.+?\.)(\s|$)", t)
    return m.group(1) if m else t


def cle_visiteur(nom):
    t = re.sub(r"\([^)]*\)", " ", nom or "")
    t = re.split(r"[;,]|\bet\b", t)[0]
    t = re.sub(r"\s+", " ", t).strip(" .:-")
    return t


def cle_personne(nom):
    """Clé d'un humain : sans accents, en minuscules, mots séparés par « - » (« Stéphane » -> « stephane »)."""
    return re.sub(r"[^a-z0-9]+", "-", normal(nom)).strip("-")


def lire_humains(racine):
    """([(clé, prénom)], anomalies) des membres humains de l'équipe projet, lus dans equipe/humains.md
    (champ `humains` : liste de `{prenom: …}` ou de prénoms). Fichier absent : aucun humain, aucune anomalie.
    Entrée vide, mal formée ou en double (casse et accents ignorés) : ignorée et signalée. Jamais d'exception."""
    chemin = os.path.join(racine, *FICHIER_HUMAINS.split("/"))
    if not os.path.isfile(chemin):
        return [], []
    fm, _, err = tableau.lire_frontmatter(chemin)
    if err:
        return [], ["{} : {}".format(FICHIER_HUMAINS, err)]
    liste = fm.get("humains")
    if not isinstance(liste, list):
        return [], ["{} : champ « humains » absent ou mal formé (liste attendue)".format(FICHIER_HUMAINS)]
    humains, vus, anomalies = [], set(), []
    for n, entree in enumerate(liste, 1):
        prenom = entree.get("prenom") if isinstance(entree, dict) else entree
        prenom = tronquer(prenom, 40) if isinstance(prenom, str) else ""
        cle = cle_personne(prenom)
        if not cle:
            anomalies.append("{} : entrée {} sans prénom, ignorée".format(FICHIER_HUMAINS, n))
        elif cle in vus:
            anomalies.append("{} : « {} » en double, ignoré".format(FICHIER_HUMAINS, prenom))
        else:
            vus.add(cle)
            humains.append((cle, prenom))
    return humains, anomalies


# ============================================================================ journaux

RE_TITRE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RE_CANDIDAT = re.compile(r"^\s*-\s*\d{4}-\d{2}-\d{2}")
# Même détection que tableau.RE_JOURNAL (date, heure facultative, puis « · »), avec l'heure capturée.
RE_LIGNE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}):(\d{2}))?\s*·\s*(.*)$")
RE_TEMPS = re.compile(r"^(?:total\s+)?(\d+(?:[.,]\d+)?)\s*h\b\.?\s*(.*)$", re.I)
RE_PASSAGE = re.compile(r"(?:passage|passé|passe|repass[ée]|→|->)\s*(?:en\s+|à\s+)?[`*]*"
                        r"(A_FAIRE|EN_COURS|EN_REVUE|BLOQUE|ATTENTE_HUMAIN|TERMINE|ANNULE)\b")
RE_DEC = re.compile(r"\bDEC-\d{3,}\b")
RE_TICKET = re.compile(r"\bT-\d+\b")


def lignes_section(texte, motif):
    """[(numéro de ligne dans le fichier, ligne)] de la première section dont le titre correspond à `motif`."""
    lignes = (texte or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    debut, niveau, dans_code = None, 0, False
    for i, l in enumerate(lignes):
        if l.strip().startswith("```"):
            dans_code = not dans_code
        if dans_code:
            continue
        m = RE_TITRE.match(l)
        if not m:
            continue
        if debut is None:
            if re.search(motif, m.group(2), re.I):
                debut, niveau = i + 1, len(m.group(1))
        elif len(m.group(1)) <= niveau:
            return [(j + 1, lignes[j]) for j in range(debut, i)]
    if debut is None:
        return []
    return [(j + 1, lignes[j]) for j in range(debut, len(lignes))]


def analyser_journal(texte, source):
    """Lignes « date-heure · qui · quoi · temps » de la section Journal d'un ticket.
    Retourne (entrées, anomalies). Une ligne mal formée est ignorée et signalée ; jamais d'exception."""
    entrees, anomalies = [], []
    dans_commentaire = False
    for num, l in lignes_section(texte, r"^journal\b"):
        s = l.strip()
        if dans_commentaire or s.startswith("<!--"):
            dans_commentaire = "-->" not in s
            continue
        if not s:
            continue
        if not RE_CANDIDAT.match(l):
            if re.match(r"^\s*[-*+]\s+\S", l):
                anomalies.append("{} : ligne {} du journal sans date (« {} »)".format(source, num, tronquer(s, 60)))
            continue
        m = RE_LIGNE.match(l)
        if not m:
            anomalies.append("{} : ligne {} du journal mal formée, séparateur « · » absent (« {} »)".format(
                source, num, tronquer(s, 60)))
            continue
        d = tableau.en_date(m.group(1))
        if d is None:
            anomalies.append("{} : ligne {} du journal, date invalide {}".format(source, num, m.group(1)))
            continue
        heure = None
        if m.group(2):
            h, mi = int(m.group(2)), int(m.group(3))
            if h < 24 and mi < 60:
                heure = "{:02d}:{:02d}".format(h, mi)
            else:
                anomalies.append("{} : ligne {} du journal, heure invalide {}:{}".format(
                    source, num, m.group(2), m.group(3)))
        parts = [p.strip() for p in re.split(r"\s*·\s*", m.group(4))]
        qui, reste = parts[0], [p for p in parts[1:]]
        temps = None
        if reste:
            mt = RE_TEMPS.match(reste[-1])
            if mt and (len(reste) >= 2 or not mt.group(2).strip()):
                temps = float(mt.group(1).replace(",", "."))
                suite = mt.group(2).strip(" .;")
                reste = reste[:-1] + ([suite] if suite else [])
        quoi = " · ".join(p for p in reste if p)
        if not qui or not quoi:
            anomalies.append("{} : ligne {} du journal incomplète, « date · qui · quoi » attendu (« {} »)".format(
                source, num, tronquer(s, 60)))
            continue
        entrees.append({"date": d, "heure": heure, "qui": qui, "quoi": quoi, "temps": temps, "ligne": num})
    return entrees, anomalies


def classer(quoi):
    """(type, statut) d'une action de journal : creation, statut (passage vers un statut) ou travail."""
    if normal(quoi).startswith("creation"):
        return "creation", None
    m = RE_PASSAGE.search(quoi or "")
    if m:
        return "statut", m.group(1)
    return "travail", None


def revue_approuvee(texte):
    """Vrai si le dernier avis de la section « Revue » est APPROUVÉ (le modèle « <APPROUVÉ | …> » est ignoré)."""
    avis = None
    for _, l in lignes_section(texte, r"^revue\b"):
        n = tableau.sans_accents(l).upper()
        if "AVIS" not in n or "<" in l:
            continue
        if "CHANGEMENTS" in n:
            avis = False
        elif "APPROUVE" in n:
            avis = True
    return bool(avis)


# ============================================================================ états (mode instantané)

ETAT_PAR_STATUT = {"EN_COURS": "tape", "EN_REVUE": "revue", "ATTENTE_HUMAIN": "attente", "BLOQUE": "bloque"}
# Le plus urgent l'emporte quand un personnage porte plusieurs tickets.
ORDRE_ETATS = ["bloque", "attente", "tape", "revue", "attend", "cafe"]
LIBELLES_ETATS = {"tape": "au travail", "revue": "en revue", "attente": "décision humaine attendue",
                  "attend": "attend un humain", "bloque": "bloqué", "cafe": "à la machine à café",
                  "accueil": "à l'accueil"}


def etat_statut(statut):
    """État du personnage assigné, selon le statut du ticket ; tout autre statut : café."""
    return ETAT_PAR_STATUT.get(statut, "cafe")


def humain_attendu(assigne_id, bloque_par, salaries):
    """Humain attendu par un ticket ATTENTE_HUMAIN : l'assigné s'il est humain (salarié, membre de l'équipe
    projet ou visiteur) ; sinon le premier salarié cité dans bloque_par ; sinon le personnage « Équipe ESN ».
    `salaries` : {clé : prénom}."""
    if assigne_id and assigne_id.startswith(("salarie:", "humain:", "visiteur:")):
        return assigne_id
    texte = " " + normal(bloque_par) + " "
    trouves = []
    for cle, prenom in salaries.items():
        m = re.search(r"(?<![a-z]){}(?![a-z])".format(re.escape(normal(prenom) or cle)), texte)
        if m:
            trouves.append((m.start(), cle))
    if trouves:
        return "salarie:" + sorted(trouves)[0][1]
    return "visiteur:equipe"


def contributions(statut, assigne_id, approuve, bloque_par, persos, salaries):
    """[(personnage, état, personnage cible)] d'un ticket ouvert. La cible est le poste où se rendre
    (relecteur ou testeur pour EN_REVUE), None pour rester à son poste."""
    etat = etat_statut(statut)
    if etat == "cafe" or not assigne_id:
        return []
    if etat == "revue":
        cible = "agent:testeur" if approuve else "agent:relecteur-code"
        if assigne_id in ("agent:relecteur-code", "agent:testeur") or cible not in persos or cible == assigne_id:
            cible = None
        return [(assigne_id, "revue", cible)]
    if etat == "attente":
        humain = humain_attendu(assigne_id, bloque_par, salaries)
        res = [(humain, "attente", None)]
        if humain != assigne_id:
            res.append((assigne_id, "attend", None))
        return res
    return [(assigne_id, etat, None)]


# ============================================================================ plan du bureau

LARGEUR, HAUTEUR, TUILE = 48, 30, 16
RANG_COULOIR = 12          # rangée de marche dans le couloir

# id, type, titre, x, y, largeur, hauteur, système, rangées des personnages, colonnes de départ
PIECES = [
    ("s4", "reunion", "S4 · Salle de réunion client", 0, 0, 12, 11, "S4", [7], None),
    ("s1", "chef", "S1 · Bureau du chef de projet", 12, 0, 12, 11, "S1", [4, 7], None),
    ("s2", "supervision", "S2 · Supervision", 24, 0, 12, 11, "S2", [4, 7], None),
    ("s3", "serveur", "S3 · Salle serveur et déploiement", 36, 0, 12, 11, "S3", [4, 7], None),
    ("couloir", "couloir", "Couloir · accueil", 0, 11, 48, 5, None, [], None),
    ("realisation", "openspace", "Open space · pôle réalisation", 0, 16, 14, 14, "realisation", [20, 23, 26], None),
    ("salaries", "salaries", "Bureaux des salariés", 14, 16, 14, 14, "salarie", [20, 23, 26], None),
    ("cafe", "cafe", "Coin café", 28, 16, 20, 14, None, [], None),
]
REUNION = [(3, 4), (5, 4), (7, 4), (2, 3), (9, 3)]       # autour de la table de S4
POSTE_COORDINATEUR = (24, 14)


def _places(piece):
    """Positions des personnages assis (tuile du personnage ; le bureau est dessiné au-dessus)."""
    _, _, _, x, _, l, _, _, rangs, _ = piece
    cols = [c for c in range(x + 2, x + l - 1, 3) if c + 1.5 <= x + l - 1]
    return [(c, r) for r in rangs for c in cols]


def construire_plan(personnages):
    """Plan du bureau et poste de chaque personnage (modifie `personnages` : champ « poste »).
    Un agent va dans la pièce de son système ; au-delà de la capacité, ou sans système connu, il va dans
    l'open space, puis dans les bureaux des salariés, puis dans le couloir. Rien n'est codé par agent."""
    pieces = {p[0]: p for p in PIECES}
    libres = {pid: list(_places(p)) for pid, p in pieces.items()}
    postes = []
    debordement = ["realisation", "salaries"]

    def couloir_libre(i):
        xs = [x for x in range(2, LARGEUR - 1, 2) if abs(x - POSTE_COORDINATEUR[0]) > 1]
        return (xs[i % len(xs)], 15 if i < len(xs) else 12)     # les visiteurs sont sur la rangée 14

    n_couloir = [0]

    def attribuer(p, piece_pref):
        ordre = [piece_pref] + [d for d in debordement if d != piece_pref]
        for pid in ordre:
            if pid and libres.get(pid):
                x, y = libres[pid].pop(0)
                return pid, x, y
        x, y = couloir_libre(n_couloir[0])
        n_couloir[0] += 1
        return "couloir", x, y

    visiteurs_x = [28, 20, 31, 17, 34, 14, 37, 11, 40, 8, 43, 5]
    n_visiteurs = 0
    for p in personnages:
        if p["nature"] == "coordinateur":
            pid, x, y = "couloir", POSTE_COORDINATEUR[0], POSTE_COORDINATEUR[1]
        elif p["nature"] in ("humain", "visiteur"):          # à l'accueil ; les humains passent en premier
            pid, y = "couloir", 14
            x = visiteurs_x[n_visiteurs] if n_visiteurs < len(visiteurs_x) else 2 + (n_visiteurs % 15) * 3
            if n_visiteurs >= len(visiteurs_x):
                y = 12
            n_visiteurs += 1
        elif p["nature"] == "salarie":
            pid, x, y = attribuer(p, "salaries")
        else:
            pref = {"S1": "s1", "S2": "s2", "S3": "s3", "S4": "s4", "realisation": "realisation"}.get(p["systeme"])
            pid, x, y = attribuer(p, pref or "realisation")
        poste = {"id": "p-" + re.sub(r"[^a-z0-9-]+", "-", p["id"]), "piece": pid, "x": x, "y": y,
                 "bureau": p["nature"] not in ("humain", "visiteur")}
        postes.append(poste)
        p["poste"] = poste["id"]
    # Coin café : 6 colonnes × 3 rangées, puis le couloir : au moins une place par personnage.
    cafe = [(x, y) for y in (20, 23, 26) for x in (30, 33, 36, 39, 42, 45)]
    i = 0
    while len(cafe) < len(personnages):
        cafe.append((45 - (i % 14) * 3, 28 if i < 6 else 12))
        i += 1
    return {
        "largeur": LARGEUR, "hauteur": HAUTEUR, "tuile": TUILE, "rang_couloir": RANG_COULOIR,
        "pieces": [{"id": p[0], "type": p[1], "titre": p[2], "x": p[3], "y": p[4], "l": p[5], "h": p[6],
                    "couleur": COULEURS.get(p[7] or "", "#94a3b8"),
                    "porte": None if p[0] == "couloir" else {"x": p[3] + p[5] // 2,
                                                             "y": p[4] + p[6] - 1 if p[4] < 11 else p[4]}}
                   for p in PIECES],
        "postes": postes,
        "cafe": [{"x": x, "y": y} for x, y in cafe],
        "reunion": [{"x": x, "y": y} for x, y in REUNION],
    }


# ============================================================================ données de la page

class Donnees:
    """Toutes les données de la page, calculées à partir de l'inventaire de console.Site."""

    def __init__(self, site, rel="bureau.html"):
        self.site = site
        self.rel = rel
        self.anomalies = []
        self.persos = {}           # id -> dict
        self.ordre = []
        self.salaries = {}         # clé -> prénom
        self.humains = {}          # clé -> id du personnage (equipe/humains.md)
        self._personnages()

    # -- liens ---------------------------------------------------------------------
    def lien(self, vers):
        return self.site.lien(self.rel, vers)

    def page_ticket(self, p, t):
        return self.lien("projets/{}/tickets/{}.html".format(p.slug, t.fichier[:-3]))

    # -- personnages ----------------------------------------------------------------
    def _ajouter(self, p):
        h = empreinte(p["id"])
        p.setdefault("teint", h % 4)
        p.setdefault("cheveux", (h // 4) % 6)
        p.setdefault("coiffure", (h // 24) % 3)
        self.persos[p["id"]] = p
        self.ordre.append(p["id"])
        return p

    def _personnages(self):
        s = self.site
        self._ajouter({"id": "coordinateur", "nom": "coordinateur", "nature": "coordinateur",
                       "systeme": "coordinateur", "couleur": COULEURS["coordinateur"], "accessoire": "talkie",
                       "role": "Session principale de Claude Code : orchestre les agents et s'arrête à chaque "
                               "validation humaine (CLAUDE.md).", "description": "", "modele": "session principale",
                       "outils": [], "page": self.lien("docs/CLAUDE.html" if "CLAUDE.md" in s.pages else "agents.html"),
                       "hors_catalogue": False})
        # Membres humains de l'équipe projet : toujours présents, même s'ils ne sont cités nulle part.
        humains, anomalies = lire_humains(s.racine)
        self.anomalies.extend(anomalies)
        for cle, prenom in humains:
            self.humains[cle] = "humain:" + cle
            self._ajouter({"id": "humain:" + cle, "nom": prenom, "nature": "humain", "systeme": "humain",
                           "couleur": COULEURS["humain"], "accessoire": "tampon", "role": ROLE_HUMAIN,
                           "description": "Lu dans {} : ni salarié fictif d'equipe/membres/, ni lettre A à D."
                                          .format(FICHIER_HUMAINS),
                           "modele": "humain", "outils": [], "page": self.lien("decisions.html"),
                           "hors_catalogue": False})
        rang = {code: i for i, code in enumerate(SYSTEMES_CONNUS)}
        agents = []
        for a in s.agents:
            fm = a["fm"] or {}
            sys_ = str((s.catalogue.get(a["nom"]) or {}).get("systeme") or "")
            sys_ = "realisation" if normal(sys_) == "realisation" else sys_.upper()
            connu = sys_ in SYSTEMES_CONNUS
            desc = str(fm.get("description") or "")
            agents.append((rang.get(sys_, 99), a["nom"], {
                "id": "agent:" + a["nom"], "nom": a["nom"], "nature": "agent",
                "systeme": sys_ if connu else "autres", "couleur": COULEURS[sys_ if connu else "autres"],
                "accessoire": accessoire(a["nom"], desc), "role": premiere_phrase(desc) or "—",
                "description": tronquer(desc, 420), "modele": str(fm.get("model") or "?"),
                "outils": [o.strip() for o in str(fm.get("tools") or "").split(",") if o.strip()],
                "page": self.lien(a["page"]), "hors_catalogue": not connu}))
        # Agents du catalogue (equipe/agents.md) sans fichier dans .claude/agents/ : affichés, signalés.
        fichiers = {a["nom"] for a in s.agents}
        for nom, entree in sorted(s.catalogue.items()):
            if nom in fichiers:
                continue
            sys_ = str(entree.get("systeme") or "")
            sys_ = "realisation" if normal(sys_) == "realisation" else sys_.upper()
            connu = sys_ in SYSTEMES_CONNUS
            self.anomalies.append("agent {} au catalogue sans fichier .claude/agents/{}.md".format(nom, nom))
            agents.append((rang.get(sys_, 99), nom, {
                "id": "agent:" + nom, "nom": nom, "nature": "agent", "systeme": sys_ if connu else "autres",
                "couleur": COULEURS[sys_ if connu else "autres"], "accessoire": accessoire(nom),
                "role": "Agent du catalogue (equipe/agents.md), sans fichier d'agent.", "description": "",
                "modele": "?", "outils": [], "page": self.lien("agents.html"), "hors_catalogue": not connu}))
        for _, _, p in sorted(agents, key=lambda x: (x[0], x[1])):
            self._ajouter(p)
        for cle in sorted(s.equipe.membres):
            m = s.equipe.membres[cle]
            if m["statut"] == "parti":
                continue
            fiche = s.fiches.get(cle) or {}
            role = str(fiche.get("role") or "")
            self.salaries[cle] = m["prenom"]
            if cle_personne(cle) in self.humains:
                self.anomalies.append("{} : « {} » porte le prénom d'un salarié fictif ; « salarie:{} » désigne "
                                      "le salarié, le prénom seul désigne le membre de l'équipe projet".format(
                                          FICHIER_HUMAINS, m["prenom"], cle))
            comp =[str(c.get("nom")) for c in fiche.get("competences") or [] if isinstance(c, dict) and c.get("nom")]
            self._ajouter({"id": "salarie:" + cle, "nom": m["prenom"].capitalize(), "nature": "salarie",
                           "systeme": "salarie", "couleur": COULEURS["salarie"], "accessoire": accessoire("", role),
                           "role": role or "Salarié", "description": "niveau {} · statut {}".format(
                               m["niveau"] or "?", m["statut"] or "?"),
                           "modele": "humain", "outils": comp,
                           "page": self.lien("equipe.html#membre-" + cle), "hors_catalogue": False})

    def humain(self, nom):
        """Id du membre humain de l'équipe projet désigné par `nom` (casse, accents, parenthèses et
        « et … » ignorés ; « Stéphane Martin » désigne Stéphane), sinon None."""
        cle = cle_personne(cle_visiteur(nom))
        if not cle:
            return None
        return self.humains.get(cle) or self.humains.get(cle.split("-")[0])

    def visiteur(self, nom):
        """Personnage d'un humain absent d'equipe/membres/ (decide_par, salarie:ethan…) : le membre de
        l'équipe projet qui lui correspond (equipe/humains.md), sinon un visiteur créé à la demande."""
        humain = self.humain(nom)
        if humain:
            return humain
        libelle = cle_visiteur(nom) or "inconnu"
        cle = cle_personne(libelle) or "inconnu"
        if cle in ("equipe", "l-equipe", "equipe-esn"):
            cle, libelle = "equipe", "Équipe ESN"
        pid = "visiteur:" + cle
        if pid not in self.persos:
            equipe = cle == "equipe"
            self._ajouter({"id": pid, "nom": libelle if equipe else libelle[:1].upper() + libelle[1:],
                           "nature": "visiteur", "systeme": "visiteur", "couleur": COULEURS["visiteur"],
                           "accessoire": "tampon",
                           "role": "Les humains de l'équipe qui valident et décident (R5, R7)." if equipe else
                                   "Humain de l'équipe, hors equipe/ : décide et valide (R5, R7).",
                           "description": "", "modele": "humain", "outils": [],
                           "page": self.lien("decisions.html"), "hors_catalogue": False})
        return pid

    def acteur(self, qui):
        """(id du personnage, note) pour un « qui » de journal ou un decide_par."""
        q = (qui or "").strip().strip("*`")
        note = ""
        m = re.match(r"^coordinateur\s+pour\s+(.+)$", q, re.I)
        if m:
            pid, _ = self.acteur(m.group(1))
            return pid, "saisi par le coordinateur"
        m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", q)
        if m and m.group(1):
            q, note = m.group(1).strip(), "saisi par " + m.group(2).strip()
        if normal(q) in ("coordinateur", "agent:coordinateur", "le coordinateur"):
            return "coordinateur", note
        nature, nom = tableau.decouper_assigne(q)
        if nature == "agent":
            pid = "agent:" + nom
            if pid not in self.persos:
                self.anomalies.append("acteur inconnu du catalogue : {} (affiché comme visiteur)".format(q))
                return self.visiteur(nom), note
            return pid, note
        if nature == "salarie":
            pid = "salarie:" + nom
            return (pid if pid in self.persos else self.visiteur(nom)), note
        humain = self.humain(q)            # prénom seul : le membre de l'équipe projet d'abord
        if humain:
            return humain, note
        cle = normal(q)
        if "salarie:" + cle in self.persos:
            return "salarie:" + cle, note
        return self.visiteur(q), note

    def id_assigne(self, assigne):
        return self.acteur(assigne)[0] if tableau.texte(assigne) else None

    # -- tickets -------------------------------------------------------------------
    def lire_ticket(self, p, t):
        chemin = os.path.join(p.dossier, "tickets", t.fichier)
        try:
            with open(chemin, "r", encoding="utf-8-sig") as f:
                return f.read()
        except (OSError, UnicodeDecodeError):
            self.anomalies.append("projets/{}/tickets/{} : illisible".format(p.slug, t.fichier))
            return ""

    def calculer(self):
        s = self.site
        self.projets, self.evenements = [], []
        brut = []                  # événements avant tri
        jours_dec = {}             # (DEC, date) -> heure, pour placer les décisions
        instants = {}
        for p in s.projets:
            contrib = []
            for t in p.tickets:
                texte = self.lire_ticket(p, t)
                source = "projets/{}/tickets/{}".format(p.slug, t.fichier)
                entrees, anomalies = analyser_journal(texte, source)
                self.anomalies.extend(anomalies)
                precedente = None
                for i, en in enumerate(entrees):
                    heure, estimee = en["heure"], False
                    if heure is None:
                        estimee = True
                        heure = precedente[1] if precedente and precedente[0] == en["date"] else "00:00"
                    precedente = (en["date"], heure)
                    pid, note = self.acteur(en["qui"])
                    type_, statut = classer(en["quoi"])
                    for dec in RE_DEC.findall(en["quoi"]):
                        jours_dec.setdefault((dec, en["date"].isoformat()), heure)
                    brut.append({"projet": p.slug, "date": en["date"].isoformat(), "heure": heure,
                                 "estimee": estimee, "sans_heure": False, "perso": pid, "note": note,
                                 "ticket": t.id, "type": type_, "statut": statut, "texte": en["quoi"],
                                 "temps": en["temps"], "page": self.page_ticket(p, t), "_cle": (source, i)})
                if t.statut not in FERMES:
                    assigne = self.id_assigne(t.assigne)
                    approuve = revue_approuvee(texte) if t.statut == "EN_REVUE" else False
                    for perso, etat, cible in contributions(t.statut, assigne, approuve, t.bloque_par,
                                                            self.persos, self.salaries):
                        if perso == "visiteur:equipe":
                            self.visiteur("équipe")
                        contrib.append((perso, etat, cible, p, t))
            instants[p.slug] = contrib
        # Décisions DEC : événement « decision » visible, rattaché au projet (ou à toute l'ESN).
        slugs = {p.slug for p in s.projets}
        for d in s.decisions:
            fm = d["fm"] or {}
            jour = tableau.en_date(fm.get("date")) or tableau.en_date(d["date"])
            if not jour:
                continue
            projet = tableau.texte(fm.get("projet"))
            projet = projet if projet in slugs else ESN
            tickets = RE_TICKET.findall(tableau.texte(fm.get("ticket")))
            qui = tableau.texte(fm.get("decide_par")) or "équipe"
            pid, _ = self.acteur(qui)
            heure = jours_dec.get((d["id"], jour.isoformat()))
            statut_doc = tableau.sans_accents(tableau.texte(fm.get("statut"))).upper()
            valide = tableau.texte(fm.get("valide_par"))
            texte = "{} · {}".format(d["id"], tableau.texte(fm.get("titre")) or d["id"])
            brut.append({"projet": projet, "date": jour.isoformat(), "heure": heure or "23:59",
                         "estimee": False, "sans_heure": heure is None, "perso": pid,
                         "note": "décidé par {}".format(qui), "ticket": tickets[0] if tickets else "",
                         "type": "decision", "statut": None, "texte": texte, "temps": None,
                         "page": self.lien(d["page"]), "dec": d["id"],
                         "valide": statut_doc == "VALIDE", "valide_par": valide, "_cle": ("~" + d["id"], 0)})
        brut.sort(key=lambda ev: (ev["date"], ev["heure"], ev["_cle"]))
        for n, ev in enumerate(brut):
            ev.pop("_cle")
            ev["n"] = n
            ev["quand"] = "{} {}".format(ev["date"], ev["heure"])
            ev["jalon"] = ev["type"] in ("creation", "statut", "decision")
        self.evenements = brut
        # Instantané par projet, puis pour toute l'ESN.
        for p in s.projets:
            self.projets.append(self._projet(p.slug, p.client, self.lien("projets/{}/index.html".format(p.slug)),
                                             instants[p.slug]))
        tous = [c for p in s.projets for c in instants[p.slug]]
        self.projets.append(self._projet(ESN, "Toute l'ESN", self.lien("portefeuille.html"), tous))
        plan = construire_plan([self.persos[i] for i in self.ordre])
        return {"version": 1, "date": s.auj.isoformat(), "plan": plan,
                "personnages": [self.persos[i] for i in self.ordre], "projets": self.projets,
                "evenements": self.evenements, "etats": LIBELLES_ETATS,
                "anomalies": sorted(set(self.anomalies))}

    def _projet(self, slug, libelle, page, contrib):
        par_perso = {}
        for perso, etat, cible, p, t in contrib:
            entree = par_perso.setdefault(perso, {"perso": perso, "etat": "cafe", "cible": None, "bulle": "",
                                                  "tickets": []})
            if ORDRE_ETATS.index(etat) < ORDRE_ETATS.index(entree["etat"]):
                entree["etat"], entree["cible"] = etat, cible
                entree["bulle"] = self._bulle(etat, t)
            entree["tickets"].append({"id": t.id, "titre": t.titre, "statut": t.statut, "projet": p.slug,
                                      "page": self.page_ticket(p, t), "role": etat})
        return {"slug": slug, "libelle": libelle, "page": page,
                "instantane": [par_perso[k] for k in self.ordre if k in par_perso]}

    @staticmethod
    def _bulle(etat, t):
        if etat == "bloque":
            return tronquer("{} · {}".format(t.id, t.bloque_par or "bloqué"), 48)
        if etat == "attente":
            return tronquer("! {} · {}".format(t.id, t.bloque_par or "décision attendue"), 48)
        if etat == "attend":
            return "{} · attend un humain".format(t.id)
        if etat == "revue":
            return "{} · en revue".format(t.id)
        return tronquer("{} · {}".format(t.id, t.titre), 40)


def json_pour_script(donnees):
    """JSON à insérer dans <script type="application/json"> : aucun « < », « > », « & », U+2028 ni U+2029
    bruts (échappements \\uXXXX), donc ni « </script> » ni « <!-- » possibles ; le JSON reste valide."""
    texte = json.dumps(donnees, ensure_ascii=False, separators=(",", ":"))
    for car, rempl in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                       (" ", "\\u2028"), (" ", "\\u2029")):
        texte = texte.replace(car, rempl)
    return texte


# ============================================================================ HTML

LEGENDE = [("tape", "au travail (EN_COURS)"), ("revue", "en revue (EN_REVUE) : chez le relecteur ou le testeur"),
           ("attente", "« ! » décision humaine attendue (ATTENTE_HUMAIN)"), ("attend", "attend un humain"),
           ("bloque", "bulle rouge : bloqué (BLOQUE)"), ("cafe", "machine à café : rien en cours")]


# Mode Direct (DEC-018) : optionnel, local au poste, disponible seulement quand la page est servie par
# scripts/bureau_direct.py (http://127.0.0.1). En file://, le bouton reste désactivé et l'aide l'explique.
DIRECT_AIDE = (
    '<p id="b-direct-aide" class="b-aide">Le mode <strong>Direct</strong> montre en temps réel le coordinateur '
    'et les sous-agents de Claude Code. Il est optionnel et local à chaque poste, et n\'est disponible que si '
    'la page est servie par le serveur local : <code>python scripts/bureau_direct.py --installer</code> (une '
    'fois, puis relancer Claude Code), puis <code>python scripts/bureau_direct.py</code> et ouvrir '
    '<code>127.0.0.1:8765/bureau.html#mode=direct</code>.</p>')
DIRECT_LEGENDE = [("livre", "lit (Read, Grep, Glob)"), ("crayon", "écrit (Edit, Write)"),
                  ("terminal", "terminal (Bash)"), ("globe", "web"), ("main", "« ! » attend une autorisation ou "
                                                                          "une réponse")]
DIRECT_ZONE = (
    '<div class="bureau-direct" id="b-direct" hidden>'
    '<p class="b-direct-ligne"><span id="b-direct-etat" class="b-direct-etat" role="status">○ déconnecté</span> '
    '<span id="b-direct-sessions" class="meta"></span></p>'
    '<p id="b-direct-alerte" class="avert" role="alert" hidden>Deux sessions de coordinateur sont actives en même '
    'temps : une seule personne au coordinateur.</p>'
    '<ul class="legende-bureau" aria-label="Légende du mode Direct">'
    + "".join('<li><span class="b-icone b-icone-{}" aria-hidden="true"></span>{}</li>'.format(e(k), e(v))
              for k, v in DIRECT_LEGENDE) +
    '</ul></div>')
DIRECT_LISTE = (
    '<section id="b-direct-evenements" hidden><details class="carte b-liste" open>'
    '<summary>Derniers événements (direct)</summary>'
    '<p class="intro">Métadonnées seulement : qui, quel type d\'outil, quand. Jamais le texte des messages, ni '
    'les fichiers, ni les commandes.</p><ol id="b-direct-liste" class="b-direct-liste"></ol></details></section>')


def page_html(site, donnees):
    """Corps HTML de bureau.html (le gabarit commun est ajouté par console.Site.page)."""
    projets = donnees["projets"]
    persos = {p["id"]: p for p in donnees["personnages"]}
    defaut = next((p["slug"] for p in projets if p["slug"] != ESN and p["instantane"]), None) or \
        (projets[0]["slug"] if projets else ESN)
    options = "".join('<option value="{}"{}>{}</option>'.format(
        e(p["slug"]), " selected" if p["slug"] == defaut else "", e(p["libelle"])) for p in projets)
    L = ['<h1>Le bureau</h1>',
         '<p class="intro">L\'ESN vue de dessus : une pièce par système, l\'open space du pôle réalisation, les '
         'bureaux des salariés et le coin café. <strong>Instantané</strong> : l\'état de chaque personnage vient des '
         'tickets du projet choisi (R9). <strong>Replay</strong> : l\'histoire racontée par les lignes « Journal » '
         'des tickets et par les décisions ; il raconte, il n\'affirme aucun statut. <strong>Direct</strong> : ce que '
         'font en ce moment le coordinateur et les sous-agents dans Claude Code (optionnel, serveur local).</p>',
         '<div class="bureau-barre">'
         '<label>Projet <select id="b-projet">{}</select></label>'
         '<div class="b-modes" role="group" aria-label="Mode">'
         '<button type="button" id="b-mode-instantane" aria-pressed="true">Instantané</button>'
         '<button type="button" id="b-mode-replay" aria-pressed="false">Replay</button>'
         '<button type="button" id="b-mode-direct" aria-pressed="false" disabled '
         'aria-describedby="b-direct-aide">Direct</button></div>'
         '<button type="button" id="b-plein" class="b-discret">Plein écran ⤢</button></div>'.format(options),
         DIRECT_AIDE,
         DIRECT_ZONE,
         '<div class="bureau-replay" id="b-replay" hidden>'
         '<button type="button" id="b-prec" aria-label="Événement précédent">◀</button>'
         '<button type="button" id="b-lecture" aria-label="Lecture">▶ Lecture</button>'
         '<button type="button" id="b-suiv" aria-label="Événement suivant">▶</button>'
         '<label>Vitesse <select id="b-vitesse"><option value="1">×1</option><option value="2">×2</option>'
         '<option value="5">×5</option><option value="10">×10</option></select></label>'
         '<label class="b-case"><input type="checkbox" id="b-jalons" checked> Jalons seulement</label>'
         '<input type="range" id="b-curseur" min="0" max="0" value="0" aria-label="Position dans le replay">'
         '<span id="b-horloge" class="b-horloge"></span></div>',
         '<div class="bureau-scene"><div class="bureau-cadre" id="b-cadre">'
         '<canvas id="b-canvas" width="768" height="480" role="img" aria-label="Vue de dessus du bureau">'
         '</canvas></div>'
         '<aside class="carte bureau-fiche" id="b-fiche" aria-live="polite"><p class="vide">Survolez ou cliquez '
         'un personnage, ou choisissez-le dans la liste ci-dessous.</p></aside></div>',
         DIRECT_LISTE,
         '<noscript><p class="avert">La vue dessinée demande JavaScript ; les listes ci-dessous (personnages, '
         'événements) restent lisibles.</p></noscript>',
         '<p id="b-annonce" class="b-sr" aria-live="polite"></p>',
         '<ul class="legende-bureau" aria-label="Légende des états">{}</ul>'.format("".join(
             '<li><span class="b-pastille b-{}"></span>{}</li>'.format(e(k), e(v)) for k, v in LEGENDE))]
    # Personnages et état, par projet (alternative texte au dessin ; filtrée par le sélecteur).
    blocs = []
    for p in projets:
        etat = {i["perso"]: i for i in p["instantane"]}
        lignes = []
        for pid in [x["id"] for x in donnees["personnages"]]:
            i = etat.get(pid)
            per = persos[pid]
            tickets = ", ".join('<a href="{}">{}</a>'.format(e(t["page"]), e(t["id"])) for t in (i or {}).get(
                "tickets", [])) or "—"
            repos = "accueil" if per["nature"] in ("coordinateur", "humain", "visiteur") else "cafe"
            etat_lib = LIBELLES_ETATS[i["etat"]] if i else LIBELLES_ETATS[repos]
            if i and i["cible"] and i["cible"] in persos:
                etat_lib += " (chez {})".format(persos[i["cible"]]["nom"])
            lignes.append('<tr><td><button type="button" class="b-perso" data-perso="{}">{}</button></td><td>{}</td>'
                          '<td><span class="b-pastille b-{}"></span>{}</td><td>{}</td></tr>'.format(
                              e(pid), e(per["nom"]), e(per["role"]), e(i["etat"] if i else "cafe"), e(etat_lib),
                              tickets))
        blocs.append('<div class="b-etats" data-projet="{}"><h3>{}</h3><div class="table-wrap"><table><thead><tr>'
                     '<th>Personnage</th><th>Rôle</th><th>État</th><th>Tickets</th></tr></thead><tbody>{}</tbody>'
                     '</table></div></div>'.format(e(p["slug"]), e(p["libelle"]), "".join(lignes)))
    L.append('<section><h2>Personnages et état</h2><p class="intro">Alternative texte à la vue dessinée : un bouton '
             'par personnage ouvre sa fiche.</p>{}</section>'.format("".join(blocs)))
    # Événements du replay (liste texte complète).
    items = []
    for ev in donnees["evenements"]:
        per = persos.get(ev["perso"], {"nom": ev["perso"]})
        heure = "heure non renseignée" if ev["sans_heure"] else ("~" if ev["estimee"] else "") + ev["heure"]
        ticket = '<a href="{}">{}</a> '.format(e(ev["page"]), e(ev["ticket"] or ev.get("dec") or "")) \
            if ev["page"] else ""
        items.append('<li class="ev ev-{t}" data-n="{n}" data-projet="{p}" data-jalon="{j}"><time>{d} {h}</time> '
                     '<strong>{qui}</strong> {tk}<span>{txt}</span>{note}</li>'.format(
                         t=e(ev["type"]), n=ev["n"], p=e(ev["projet"]), j="1" if ev["jalon"] else "0",
                         d=e(ev["date"]), h=e(heure), qui=e(per["nom"]), tk=ticket, txt=e(ev["texte"]),
                         note=' <span class="meta">({})</span>'.format(e(ev["note"])) if ev["note"] else ""))
    L.append('<section><details class="carte b-liste" open><summary>Événements du replay ({n})</summary>'
             '<p class="intro">Lignes « Journal » des tickets et décisions DEC, dans l\'ordre chronologique. « ~ » : '
             'heure absente du journal, reprise de la ligne précédente du même ticket.</p>'
             '<ol id="b-evenements">{items}</ol></details></section>'.format(n=len(items), items="".join(items)))
    L.append(site.anomalies_html(donnees["anomalies"]))
    L.append('<script type="application/json" id="donnees-bureau">{}</script>'.format(json_pour_script(donnees)))
    L.append('<script src="assets/bureau.js"></script>')
    return "\n".join(L)


CSS = """
/* ---- Le bureau (scripts/bureau.py, DEC-016) ---- */
.bureau-barre, .bureau-replay { display: flex; flex-wrap: wrap; gap: .5rem .9rem; align-items: center; margin: .6rem 0; }
.bureau-barre select, .bureau-replay select { font: inherit; padding: .25rem .4rem; border-radius: 7px;
  border: 1px solid var(--ligne); background: #fff; }
.bureau-barre button, .bureau-replay button { font: inherit; padding: .35rem .8rem; border-radius: 8px;
  border: 1px solid #c7d2fe; background: #fff; color: var(--marque); cursor: pointer; }
.bureau-barre button[aria-pressed="true"] { background: var(--marque); color: #fff; border-color: var(--marque); }
.bureau-replay button:disabled { opacity: .45; cursor: default; }
.bureau-replay[hidden] { display: none; }
.b-modes { display: inline-flex; gap: .25rem; }
.b-discret { margin-left: auto; }
.b-case { display: inline-flex; gap: .35rem; align-items: center; }
#b-curseur { flex: 1 1 220px; min-width: 160px; }
.b-horloge { font-family: ui-monospace, Consolas, monospace; font-size: .88rem; color: var(--doux); }
.bureau-scene { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 1rem; align-items: start; }
.bureau-cadre { background: #1f2430; border-radius: var(--rayon); padding: 6px; box-shadow: var(--ombre);
  line-height: 0; position: relative; }
.bureau-cadre canvas { display: block; width: 100%; height: auto; image-rendering: pixelated;
  image-rendering: crisp-edges; border-radius: 6px; cursor: default; }
.bureau-cadre:fullscreen { display: flex; align-items: center; justify-content: center; padding: 0; border-radius: 0; }
.bureau-cadre:fullscreen canvas { width: auto; height: auto; max-width: 100vw; max-height: 100vh; }
.bureau-fiche { margin: 0; position: sticky; top: 4.5rem; font-size: .9rem; }
.bureau-fiche h3 { display: flex; align-items: center; gap: .5rem; }
.bureau-fiche dl { margin: .5rem 0; }
.bureau-fiche dt { font-size: .74rem; text-transform: uppercase; letter-spacing: .04em; color: var(--doux); margin-top: .45rem; }
.bureau-fiche dd { margin: .1rem 0 0; }
.bureau-fiche ul { margin: .2rem 0; padding-left: 1.1rem; }
.b-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.legende-bureau { list-style: none; display: flex; flex-wrap: wrap; gap: .3rem 1.1rem; padding: 0; margin: .7rem 0;
  font-size: .86rem; color: var(--doux); }
.legende-bureau li { display: flex; align-items: center; gap: .35rem; }
.b-pastille { display: inline-block; width: .8rem; height: .8rem; border-radius: 3px; margin-right: .35rem;
  vertical-align: -.1em; border: 1px solid rgba(0,0,0,.15); }
.b-tape { background: #3b82f6; } .b-revue { background: #8b5cf6; } .b-attente { background: #f59e0b; }
.b-attend { background: #fde68a; } .b-bloque { background: #ef4444; } .b-cafe { background: #a8a29e; }
.b-perso { font: inherit; font-weight: 600; color: var(--marque-2); background: none; border: 0; padding: 0;
  cursor: pointer; text-align: left; }
.b-perso:hover, .b-perso:focus-visible { text-decoration: underline; }
.b-etats h3 { margin: 1rem 0 .4rem; }
.b-liste ol { position: relative; max-height: 26rem; overflow-y: auto; margin: .4rem 0 0; padding-left: 2.6rem; font-size: .86rem; }
.b-liste li { margin: .12rem 0; padding: .1rem .3rem; border-radius: 5px; }
.b-liste li time { font-family: ui-monospace, Consolas, monospace; color: var(--doux); font-size: .82rem; }
.b-liste li.ev-decision { background: #fef3c7; }
.b-liste li.ev-statut strong { color: #6d28d9; }
.b-liste li[aria-current="true"] { outline: 2px solid var(--marque-2); background: #e0e7ff; }
.b-masque { display: none !important; }
/* ---- mode Direct (DEC-018) ---- */
.bureau-barre button:disabled { opacity: .45; cursor: not-allowed; }
.b-aide { font-size: .86rem; color: var(--doux); margin: .2rem 0 .6rem; }
.b-aide.b-dispo { color: #166534; }
.bureau-direct[hidden], .b-aide[hidden], #b-direct-evenements[hidden] { display: none; }
.b-direct-ligne { display: flex; flex-wrap: wrap; gap: .4rem 1rem; align-items: center; margin: .4rem 0; }
.b-direct-etat { font-weight: 700; padding: .15rem .6rem; border-radius: 999px; background: #fee2e2; color: #991b1b; }
.b-direct-etat.b-connecte { background: #dcfce7; color: #166534; }
.b-direct-liste { list-style: none; padding-left: .2rem !important; max-height: 16rem !important; }
.b-direct-liste li.ev-attente strong { color: #b45309; }
.b-icone { display: inline-block; width: .95rem; height: .95rem; border-radius: 3px; border: 1px solid #1f2430;
  background: #f8fafc; vertical-align: -.15em; }
.b-icone-livre { background: linear-gradient(90deg, #2563eb 45%, #1f2430 45% 55%, #60a5fa 55%); }
.b-icone-crayon { background: linear-gradient(135deg, #f8fafc 35%, #f59e0b 35% 65%, #f8fafc 65%); }
.b-icone-terminal { background: #111827; box-shadow: inset 2px -2px 0 #111827, inset 3px -4px 0 #22c55e; }
.b-icone-globe { background: radial-gradient(circle, #60a5fa 55%, #16a34a 56%); border-radius: 50%; }
.b-icone-main { background: #facc15; }
@media (max-width: 1000px) { .bureau-scene { grid-template-columns: 1fr; } .bureau-fiche { position: static; } }
"""
