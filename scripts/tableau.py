#!/usr/bin/env python3
"""tableau.py : génère projets/<slug>/TABLEAU.md et PORTFOLIO.md à partir des tickets.

Responsable : D · Lot 2 (D) · voir R9, R12, ARCHITECTURE § 7 (formules, alertes) et § 8 (taux),
DEC-001 § 4 (temps restant), S1 (S1-R3, R8 à R13), critères AF9 et AF11 du chef-de-projet,
docs/a-integrer/lot2-B.md (point 6) et lot2-D.md.

Imputation des coûts (R18, DEC-023) : un ticket d'un projet client est compté au client, sauf
`imputation: esn` avec `imputation_decision: DEC-NNN` qui cite une décision VALIDÉ de docs/decisions/ ;
il sort alors du coût client (comparé au budget, S1-R11) et entre dans la part de l'ESN. Projet interne
(`type_projet: interne`, R19) : tous ses tickets sont à la charge de l'ESN, comparés à son budget de
fonctionnement. Sans ticket `esn` ni projet interne, la sortie est identique à celle d'avant DEC-023.

Les tickets sont la source de vérité (R9). Ce script est le SEUL à écrire TABLEAU.md et
PORTFOLIO.md, et il n'écrit RIEN d'autre. Un fichier n'est réécrit que si son contenu change.

Usage :
  python scripts/tableau.py [--racine DIR] [--date AAAA-MM-JJ]      (Mac : python3 …)
    --racine : racine du dépôt (par défaut : le dossier parent de scripts/)
    --date   : date du jour du calcul (par défaut : aujourd'hui), pour des sorties reproductibles

Codes de sortie : 0 (même avec des alertes) ; 2 = erreur d'usage ou PyYAML absent.
Dépendance : PyYAML (python -m pip install -r requirements.txt).
"""
import argparse
import heapq
import os
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta

try:
    import yaml
except ImportError:  # pragma: no cover - vérifié à l'exécution
    yaml = None

# --- Paramètres (ARCHITECTURE § 7 et § 8 ; hypothèses à reporter dans ARCHITECTURE, lot2-D point 8) ---
HEURES_JOUR = 7.0                 # 1 jour = 7 h (R12)
CAPACITE_AGENT_H_JOUR = 7.0       # un agent : 7 h équivalent humain par jour ouvré, un ticket à la fois
TAUX_AGENT_DEFAUT = 15.0          # €/h, si equipe/agents.md est illisible
SEUIL_BUDGET = 0.90               # alerte budget consommé > 90 %
SEUIL_SANS_MAJ_JO = 2             # alerte EN_COURS sans mise à jour depuis plus de 2 jours ouvrés
SEUIL_PREAVIS_JO = 5              # alerte préavis de départ < 5 jours ouvrés
SEUIL_UTILISATION = 0.50          # indicateur AF9
HORIZON_JOURS = 3 * 365           # au-delà, un ticket est déclaré non planifiable

STATUTS = ["A_FAIRE", "EN_COURS", "EN_REVUE", "BLOQUE", "ATTENTE_HUMAIN", "TERMINE", "ANNULE"]
FERMES = {"TERMINE", "ANNULE"}
PRIORITES = {"critique": 0, "haute": 1, "normale": 2, "basse": 3}
ETATS_PROJET = ["cadrage", "en_cours", "en_pause", "livre", "maintenance", "clos"]

EN_TETE = ("<!-- FICHIER GÉNÉRÉ par scripts/tableau.py — ne pas modifier à la main (R9). "
           "Régénérer : python scripts/tableau.py -->")
ENCADRE = ("> **Fichier généré** le {d} par `scripts/tableau.py` à partir des tickets, seule source de "
           "vérité (R9). Toute modification à la main sera écrasée à la prochaine génération.")

RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_JOURNAL = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})(?:\s+\d{1,2}:\d{2})?\s*·\s*(.*)$")
RE_TICKET_ID = re.compile(r"^T-\d+$")
RE_DEC_ID = re.compile(r"^DEC-\d{3}$")
RE_FICHIER_DEC = re.compile(r"^\d{4}-\d{2}-\d{2}-(DEC-\d{3})-.*\.md$")
TYPE_INTERNE = "interne"          # type_projet du projet interne de l'ESN (R19)


# ============================================================================ utilitaires

def ecrire_stdout(texte):
    sys.stdout.buffer.write((texte + "\n").encode("utf-8"))
    sys.stdout.flush()


def sans_accents(texte):
    t = unicodedata.normalize("NFKD", str(texte))
    return "".join(c for c in t if not unicodedata.combining(c))


def en_date(valeur):
    """date, datetime ou 'AAAA-MM-JJ' -> date ; sinon None (placeholder, vide, invalide)."""
    if isinstance(valeur, datetime):
        return valeur.date()
    if isinstance(valeur, date):
        return valeur
    if isinstance(valeur, str) and RE_DATE.match(valeur.strip()):
        try:
            return date.fromisoformat(valeur.strip())
        except ValueError:
            return None
    return None


def en_nombre(valeur):
    """Nombre ou None."""
    if isinstance(valeur, bool):
        return None
    if isinstance(valeur, (int, float)):
        return float(valeur)
    if isinstance(valeur, str):
        try:
            return float(valeur.strip().replace(",", "."))
        except ValueError:
            return None
    return None


def texte(valeur):
    return "" if valeur is None else str(valeur).strip()


def est_ouvre(d, feries):
    return d.weekday() < 5 and d not in feries


def jours_ouvres_entre(debut, fin, feries):
    """Nombre de jours ouvrés d tels que debut < d <= fin (0 si fin <= debut)."""
    if debut is None or fin is None or fin <= debut:
        return 0
    n, d = 0, debut + timedelta(days=1)
    while d <= fin:
        if est_ouvre(d, feries):
            n += 1
        d += timedelta(days=1)
    return n


def fmt_nb(x, dec=1):
    s = "{:,.{p}f}".format(x, p=dec)
    return s.replace(",", "\u202f").replace(".", ",")


def fmt_jo(n, signe=False):
    """« 1 j ouvré », « 3 j ouvrés », « +2 j ouvrés »."""
    return ("{:+d}" if signe else "{}").format(n) + " j ouvré" + ("s" if abs(n) > 1 else "")


def fmt_h(x):
    return fmt_nb(x, 1) + " h"


def fmt_eur(x):
    return fmt_nb(x, 2) + " €"


def fmt_pct(x):
    return "—" if x is None else fmt_nb(100 * x, 1) + " %"


def cellule(valeur):
    return texte(valeur).replace("|", "\\|").replace("\n", " ") or "—"


def lire_frontmatter(chemin):
    """Retourne (dict, corps, erreur). erreur vaut None si tout va bien."""
    try:
        with open(chemin, "r", encoding="utf-8-sig") as f:
            contenu = f.read().replace("\r\n", "\n").replace("\r", "\n")
    except (OSError, UnicodeDecodeError) as e:
        return None, "", "illisible ({})".format(e.__class__.__name__)
    lignes = contenu.split("\n")
    if not lignes or lignes[0].strip() != "---":
        return None, contenu, "pas de frontmatter YAML"
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            try:
                donnees = yaml.safe_load("\n".join(lignes[1:i]))
            except yaml.YAMLError as e:
                return None, "", "YAML invalide ({})".format(str(e).splitlines()[0])
            if not isinstance(donnees, dict):
                return None, "", "frontmatter vide ou mal formé"
            return donnees, "\n".join(lignes[i + 1:]), None
    return None, contenu, "frontmatter non fermé"


def lister(dossier, suffixe=".md", prefixe=""):
    try:
        noms = os.listdir(dossier)
    except OSError:
        return []
    return sorted(n for n in noms if n.endswith(suffixe) and n.startswith(prefixe)
                  and os.path.isfile(os.path.join(dossier, n)))


def decisions_connues(racine):
    """{'DEC-NNN': True si VALIDÉ} pour les fichiers AAAA-MM-JJ-DEC-NNN-*.md de docs/decisions/ (R18).
    Le statut est normalisé comme le hook (accents, casse) ; un frontmatter illisible vaut non validé."""
    dossier = os.path.join(racine, "docs", "decisions")
    connues = {}
    for nom in lister(dossier):
        m = RE_FICHIER_DEC.match(nom)
        if not m:
            continue
        fm, _, err = lire_frontmatter(os.path.join(dossier, nom))
        valide = not err and sans_accents(texte(fm.get("statut"))).upper() == "VALIDE"
        connues[m.group(1)] = connues.get(m.group(1), False) or valide
    return connues


# ============================================================================ équipe

class Equipe:
    def __init__(self, racine):
        self.anomalies = []
        self.membres = {}          # clé (prénom normalisé) -> dict
        self.agents = set()
        self.taux_agent = TAUX_AGENT_DEFAUT
        self.feries = set()
        self.evenements = []
        self._lire_agents(os.path.join(racine, "equipe", "agents.md"))
        self._lire_calendrier(os.path.join(racine, "equipe", "calendrier.md"))
        self._lire_membres(os.path.join(racine, "equipe", "membres"))

    def _lire_agents(self, chemin):
        if not os.path.exists(chemin):
            self.anomalies.append("equipe/agents.md absent : taux agent par défaut ({} €/h), "
                                  "agents non vérifiés".format(fmt_nb(TAUX_AGENT_DEFAUT, 0)))
            self.agents = None
            return
        fm, _, err = lire_frontmatter(chemin)
        if err:
            self.anomalies.append("equipe/agents.md : {}".format(err))
            self.agents = None
            return
        taux = en_nombre(fm.get("cout_horaire_eur"))
        if taux is None:
            self.anomalies.append("equipe/agents.md : cout_horaire_eur invalide, {} €/h retenu".format(
                fmt_nb(TAUX_AGENT_DEFAUT, 0)))
        else:
            self.taux_agent = taux
        for a in fm.get("agents") or []:
            if isinstance(a, dict) and texte(a.get("nom")):
                self.agents.add(texte(a.get("nom")).lower())

    def _lire_calendrier(self, chemin):
        if not os.path.exists(chemin):
            self.anomalies.append("equipe/calendrier.md absent : ni jours fériés ni absences pris en compte")
            return
        fm, _, err = lire_frontmatter(chemin)
        if err:
            self.anomalies.append("equipe/calendrier.md : {}".format(err))
            return
        for j in fm.get("jours_feries") or []:
            d = en_date(j)
            if d:
                self.feries.add(d)
            else:
                self.anomalies.append("equipe/calendrier.md : jour férié invalide « {} »".format(j))
        for ev in fm.get("evenements") or []:
            if not isinstance(ev, dict):
                continue
            if texte(ev.get("statut")).lower() == "annule":
                continue
            debut, fin = en_date(ev.get("debut")), en_date(ev.get("fin"))
            if debut is None:
                self.anomalies.append("equipe/calendrier.md : événement {} sans date de début valide".format(
                    texte(ev.get("id")) or "?"))
                continue
            pct = en_nombre(ev.get("capacite_pct"))
            self.evenements.append({
                "id": texte(ev.get("id")) or "?",
                "type": texte(ev.get("type")).lower(),
                "qui": texte(ev.get("qui")).lower(),
                "debut": debut,
                "fin": fin or debut,
                "motif": texte(ev.get("motif")),
                "capacite_pct": 0.0 if pct is None else max(0.0, min(100.0, pct)),
                "statut": texte(ev.get("statut")),
            })
        self.evenements.sort(key=lambda e: (e["debut"], e["id"]))

    def _lire_membres(self, dossier):
        for nom in lister(dossier):
            chemin = os.path.join(dossier, nom)
            fm, _, err = lire_frontmatter(chemin)
            cle = sans_accents(nom[:-3]).lower()
            if err:
                self.anomalies.append("equipe/membres/{} : {}".format(nom, err))
                continue
            allocation = {}
            alloc = fm.get("allocation")
            if isinstance(alloc, dict):
                for slug, pct in alloc.items():
                    v = en_nombre(pct)
                    if v is None:
                        self.anomalies.append("equipe/membres/{} : allocation invalide pour {}".format(nom, slug))
                    else:
                        allocation[str(slug)] = v
            elif alloc not in (None, ""):
                self.anomalies.append("equipe/membres/{} : allocation n'est pas un dictionnaire".format(nom))
            cout_j = en_nombre(fm.get("cout_journalier_eur"))
            cap = en_nombre(fm.get("capacite_h_semaine"))
            if cout_j is None:
                self.anomalies.append("equipe/membres/{} : cout_journalier_eur invalide".format(nom))
            if cap is None:
                self.anomalies.append("equipe/membres/{} : capacite_h_semaine invalide, 0 retenu".format(nom))
            self.membres[cle] = {
                "prenom": texte(fm.get("prenom")) or cle,
                "niveau": texte(fm.get("niveau")),
                "cout_j": cout_j,
                "cap_sem": cap or 0.0,
                "statut": texte(fm.get("statut")).lower(),
                "arrivee": en_date(fm.get("date_arrivee")),
                "depart": en_date(fm.get("date_depart")),
                "allocation": allocation,
            }

    # -- taux et capacité --------------------------------------------------------
    def taux(self, assigne):
        """(taux €/h, erreur)."""
        nature, nom = decouper_assigne(assigne)
        if nature == "agent":
            if self.agents is not None and nom not in self.agents:
                return None, "agent inconnu d'equipe/agents.md : {}".format(assigne)
            return self.taux_agent, None
        if nature == "salarie":
            m = self.membres.get(nom)
            if m is None:
                return None, "salarié sans fiche equipe/membres/{}.md : {}".format(nom, assigne)
            if m["cout_j"] is None:
                return None, "coût journalier inconnu pour {}".format(assigne)
            return m["cout_j"] / HEURES_JOUR, None
        return None, "assigné invalide « {} » (agent:<nom> ou salarie:<prenom>)".format(texte(assigne))

    def evenements_de(self, cle):
        qui = "salarie:" + cle
        return [e for e in self.evenements if sans_accents(e["qui"]) == qui]

    def date_depart(self, cle):
        m = self.membres.get(cle)
        dates = [m["depart"]] if m and m["depart"] else []
        dates += [e["debut"] for e in self.evenements_de(cle) if e["type"] == "depart"]
        return min(dates) if dates else None


def decouper_assigne(assigne):
    a = texte(assigne)
    if ":" not in a:
        return None, a
    nature, nom = a.split(":", 1)
    nature = sans_accents(nature).strip().lower()
    nom = sans_accents(nom).strip().lower()
    if nature not in ("agent", "salarie") or not nom:
        return None, a
    return nature, nom


class Ressource:
    """Capacité journalière d'un assigné sur UN projet (l'allocation partage la capacité, S1-R10)."""

    def __init__(self, assigne, slug, equipe):
        self.assigne = texte(assigne)
        self.nature, self.nom = decouper_assigne(assigne)
        self.equipe = equipe
        self.raison = None          # capacité nulle en permanence : raison
        self.limite = None          # capacité nulle après cette date (départ)
        self.base = 0.0
        self.evenements = []
        self.arrivee = None
        if self.nature == "agent":
            if equipe.agents is not None and self.nom not in equipe.agents:
                self.raison = "agent inconnu d'equipe/agents.md"
            self.base = CAPACITE_AGENT_H_JOUR
        elif self.nature == "salarie":
            m = equipe.membres.get(self.nom)
            if m is None:
                self.raison = "salarié sans fiche dans equipe/membres/"
                return
            if m["statut"] == "parti":
                self.raison = "salarié parti"
                return
            alloc = m["allocation"].get(slug, 0.0)
            if alloc <= 0:
                self.raison = "allocation au projet nulle (S1-R10)"
                return
            self.base = m["cap_sem"] / 5.0 * alloc / 100.0
            if self.base <= 0:
                self.raison = "capacité hebdomadaire nulle"
                return
            self.limite = equipe.date_depart(self.nom)
            self.arrivee = m["arrivee"]
            self.evenements = equipe.evenements_de(self.nom)
        else:
            self.raison = "assigné invalide"

    def capacite(self, d):
        if self.raison or not est_ouvre(d, self.equipe.feries):
            return 0.0
        if self.limite and d > self.limite:
            return 0.0
        if self.arrivee and d < self.arrivee:
            return 0.0
        facteur = 1.0
        for e in self.evenements:
            if e["type"] == "arrivee" and d < e["debut"]:
                return 0.0
            if e["type"] == "absence" and e["debut"] <= d <= e["fin"]:
                facteur = min(facteur, e["capacite_pct"] / 100.0)
        return self.base * facteur

    def absences_sur(self, debut, fin):
        return [e for e in self.evenements
                if e["type"] == "absence" and e["capacite_pct"] < 100 and e["debut"] <= fin and e["fin"] >= debut]


# ============================================================================ tickets et projets

class Ticket:
    def __init__(self, fm, corps, fichier):
        self.fichier = fichier
        self.id = texte(fm.get("id"))
        self.titre = texte(fm.get("titre")) or "(sans titre)"
        self.type = texte(fm.get("type")).lower()
        self.statut = texte(fm.get("statut")).upper()
        self.priorite = texte(fm.get("priorite")).lower() or "normale"
        self.assigne = texte(fm.get("assigne"))
        self.est = en_nombre(fm.get("estimation_h"))
        self.passe = en_nombre(fm.get("temps_passe_h"))
        dep = fm.get("depend_de") or []
        if isinstance(dep, str):
            dep = [x for x in re.split(r"[,\s]+", dep.strip("[] ")) if x]
        self.depend_de = [texte(x) for x in dep if texte(x)]
        self.bloque_par = texte(fm.get("bloque_par"))
        self.cree_le = en_date(fm.get("cree_le"))
        self.maj_le = en_date(fm.get("maj_le"))
        # Champs facultatifs proposés dans lot2-D (point 5) : lus s'ils existent.
        self.statut_depuis = en_date(fm.get("statut_depuis"))
        self.debut_le = en_date(fm.get("debut_le"))
        self.termine_le = en_date(fm.get("termine_le"))
        # Imputation (R18, DEC-023) : valeur brute ; l'imputation effective est fixée par le projet.
        self.imputation_brute = sans_accents(texte(fm.get("imputation"))).lower()
        self.imputation_decision = texte(fm.get("imputation_decision")).upper()
        self.imputation = "client"
        self.journal = []
        for ligne in corps.split("\n"):
            m = RE_JOURNAL.match(ligne)
            if m:
                d = en_date(m.group(1))
                if d:
                    self.journal.append((d, m.group(2)))
        # résultats de l'ordonnancement
        self.debut_prevu = None
        self.fin_prevue = None
        self.non_planifiable = None

    @property
    def ouvert(self):
        return self.statut not in FERMES

    @property
    def estimation(self):
        return self.est or 0.0

    @property
    def temps_passe(self):
        return self.passe or 0.0

    @property
    def reste(self):
        return max(0.0, self.estimation - self.temps_passe)

    @property
    def rang(self):
        return PRIORITES.get(self.priorite, 2)

    def derniere_maj(self):
        dates = [d for d in [self.maj_le] + [j[0] for j in self.journal] if d]
        return max(dates) if dates else None

    def depuis(self, mot):
        """Date d'entrée dans l'état courant : statut_depuis, sinon dernière ligne de journal
        contenant `mot`, sinon maj_le."""
        if self.statut_depuis:
            return self.statut_depuis
        for d, t in reversed(self.journal):
            if mot in sans_accents(t).lower():
                return d
        return self.maj_le


class Projet:
    def __init__(self, racine, dossier, equipe, aujourdhui, decisions=None):
        self.racine = racine
        self.dossier = dossier
        self.equipe = equipe
        self.aujourdhui = aujourdhui
        self.decisions = decisions_connues(racine) if decisions is None else decisions
        self.anomalies = []
        self.tickets = []
        nom_dossier = os.path.basename(dossier)
        fm, _, err = lire_frontmatter(os.path.join(dossier, "projet.md"))
        if err:
            self.anomalies.append("projet.md : {}".format(err))
            fm = {}
        self.slug = texte(fm.get("slug")) or nom_dossier
        if self.slug != nom_dossier:
            self.anomalies.append("projet.md : slug « {} » différent du dossier « {} » ; le dossier fait foi".format(
                self.slug, nom_dossier))
            self.slug = nom_dossier
        self.client = texte(fm.get("client")) or self.slug
        if self.client.startswith("<"):
            self.client = self.slug
        self.type_projet = texte(fm.get("type_projet")) or "—"
        self.interne = self.type_projet.lower() == TYPE_INTERNE
        self.etat = texte(fm.get("etat_projet")) or "—"
        self.budget = en_nombre(fm.get("budget_eur"))
        if self.budget is not None and self.budget <= 0:
            self.budget = None
        if self.budget is None:
            self.anomalies.append("projet.md : budget_eur absent ou nul ; pas de contrôle budgétaire")
        self.deadline = en_date(fm.get("deadline"))
        if self.deadline is None:
            self.anomalies.append("projet.md : deadline absente ou invalide ; pas de contrôle des délais")
        self._lire_tickets()

    def _lire_tickets(self):
        dossier = os.path.join(self.dossier, "tickets")
        vus = {}
        for nom in lister(dossier, prefixe="T-"):
            fm, corps, err = lire_frontmatter(os.path.join(dossier, nom))
            if err:
                self.anomalies.append("tickets/{} : {} ; ticket ignoré".format(nom, err))
                continue
            t = Ticket(fm, corps, nom)
            if not RE_TICKET_ID.match(t.id):
                self.anomalies.append("tickets/{} : id invalide « {} » ; ticket ignoré".format(nom, t.id))
                continue
            if t.id in vus:
                self.anomalies.append("tickets/{} : id {} déjà utilisé par {} ; ticket ignoré".format(
                    nom, t.id, vus[t.id]))
                continue
            vus[t.id] = nom
            if t.statut not in STATUTS:
                self.anomalies.append("{} : statut inconnu « {} » (traité comme ouvert)".format(t.id, t.statut))
            if t.priorite not in PRIORITES:
                self.anomalies.append("{} : priorité inconnue « {} » (traitée comme normale)".format(t.id, t.priorite))
            if t.est is None:
                self.anomalies.append("{} : estimation_h absente ou invalide (0 retenu)".format(t.id))
            if t.passe is None:
                self.anomalies.append("{} : temps_passe_h absent ou invalide (0 retenu)".format(t.id))
            if t.statut in ("BLOQUE", "ATTENTE_HUMAIN") and not t.bloque_par:
                self.anomalies.append("{} : {} sans bloque_par (S1-R3)".format(t.id, t.statut))
            self._imputer(t)
            self.tickets.append(t)
        self.tickets.sort(key=lambda t: (int(t.id[2:]), t.id))
        self.par_id = {t.id: t for t in self.tickets}
        for t in self.tickets:
            for dep in t.depend_de:
                if dep not in self.par_id:
                    self.anomalies.append("{} : dépendance {} introuvable (ignorée)".format(t.id, dep))

    def _imputer(self, t):
        """Imputation effective du ticket (R18, R19) ; tout doute compte au client (ou à l'ESN en interne)."""
        brute, dec = t.imputation_brute, t.imputation_decision
        if self.interne:
            t.imputation = "esn"
            if brute == "client":
                self.anomalies.append("{} : imputation client dans un projet interne (R19) ; esn retenu".format(t.id))
            elif brute not in ("", "esn"):
                self.anomalies.append("{} : imputation inconnue « {} » (esn retenu, R19)".format(t.id, brute))
            return
        t.imputation = "client"
        if brute in ("", "client"):
            return
        if brute != "esn":
            self.anomalies.append("{} : imputation inconnue « {} » (client retenu, R18)".format(t.id, brute))
        elif not RE_DEC_ID.match(dec):
            self.anomalies.append("{} : imputation esn sans imputation_decision valide (R18) ; "
                                  "compté au client".format(t.id))
        elif dec not in self.decisions:
            self.anomalies.append("{} : imputation esn, {} introuvable dans docs/decisions/ (R18) ; "
                                  "compté au client".format(t.id, dec))
        elif not self.decisions[dec]:
            self.anomalies.append("{} : imputation esn, {} : décision non validée (R18) ; "
                                  "compté au client".format(t.id, dec))
        else:
            t.imputation = "esn"

    # -- calculs ---------------------------------------------------------------------
    def calculer(self):
        eq = self.equipe
        actifs = [t for t in self.tickets if t.statut != "ANNULE"]
        self.est_total = sum(t.estimation for t in actifs)
        self.est_termine = sum(t.estimation for t in actifs if t.statut == "TERMINE")
        self.avancement = self.est_termine / self.est_total if self.est_total > 0 else None
        self.ouverts = [t for t in self.tickets if t.ouvert]
        self.temps_restant = sum(t.reste for t in self.ouverts)
        # consomme / projete : coût imputé au budget du projet (client ; tout pour un projet interne).
        # consomme_esn / projete_esn : part prise en charge par l'ESN sur un projet client (R18).
        self.consomme, self.projete = 0.0, 0.0
        self.consomme_esn, self.projete_esn = 0.0, 0.0
        esn = [t for t in self.tickets if t.imputation == "esn" and not self.interne]
        self.a_part_esn = bool(esn)
        self.decisions_esn = sorted({t.imputation_decision for t in esn})
        for t in self.tickets:
            taux, err = eq.taux(t.assigne)
            if err:
                self.anomalies.append("{} : {} ; temps non chiffré".format(t.id, err))
                continue
            consomme = t.temps_passe * taux
            projete = t.temps_passe * taux + (t.reste * taux if t.ouvert else 0.0)
            if t.imputation == "esn" and not self.interne:
                self.consomme_esn += consomme
                self.projete_esn += projete
            else:
                self.consomme += consomme
                self.projete += projete
        self.consomme_total = self.consomme + self.consomme_esn
        self.projete_total = self.projete + self.projete_esn
        self.part_budget = self.consomme / self.budget if self.budget else None
        self._ordonnancer()
        self._utilisation()
        self._alertes()

    def _ordonnancer(self):
        eq = self.equipe
        ressources = {}
        curseurs = {}
        fins = {}                       # id -> point de fin (date, fraction)
        depart = (self.aujourdhui, 0.0)
        ouverts = {t.id: t for t in self.ouverts}
        # graphe des dépendances entre tickets ouverts (une dépendance fermée est satisfaite)
        preds = {i: [d for d in t.depend_de if d in ouverts] for i, t in ouverts.items()}
        succs = {i: [] for i in ouverts}
        for i, ds in preds.items():
            for d in ds:
                succs[d].append(i)
        degre = {i: len(ds) for i, ds in preds.items()}
        tas = [(ouverts[i].rang, int(i[2:]), i) for i in ouverts if degre[i] == 0]
        heapq.heapify(tas)
        ordre = []
        while tas:
            _, _, i = heapq.heappop(tas)
            ordre.append(i)
            for s in succs[i]:
                degre[s] -= 1
                if degre[s] == 0:
                    heapq.heappush(tas, (ouverts[s].rang, int(s[2:]), s))
        for i in sorted(set(ouverts) - set(ordre), key=lambda x: int(x[2:])):
            ouverts[i].non_planifiable = "dépendance circulaire (ou dépend d'un cycle)"
            self.anomalies.append("{} : dépendance circulaire ou dépendant d'un cycle ; non planifié".format(i))

        for i in ordre:
            t = ouverts[i]
            bloquant = [d for d in preds[i] if ouverts[d].non_planifiable]
            if bloquant:
                t.non_planifiable = "dépend de {} non planifiable".format(", ".join(bloquant))
                continue
            if t.assigne not in ressources:
                ressources[t.assigne] = Ressource(t.assigne, self.slug, eq)
                curseurs[t.assigne] = depart
            r = ressources[t.assigne]
            if r.raison:
                t.non_planifiable = "{} : {}".format(t.assigne or "sans assigné", r.raison)
                continue
            debut = max([depart, curseurs[t.assigne]] + [fins[d] for d in preds[i]])
            resultat = consommer(r, debut, t.reste)
            if resultat is None:
                if r.limite:
                    t.non_planifiable = "{} : capacité insuffisante avant le départ du {}".format(
                        t.assigne, r.limite.isoformat())
                else:
                    t.non_planifiable = "{} : aucune capacité sur l'horizon de calcul".format(t.assigne)
                continue
            premier_jour, fin = resultat
            t.debut_prevu, t.fin_prevue = premier_jour, fin[0]
            fins[i] = fin
            curseurs[t.assigne] = fin
        self.ressources = ressources
        planifies = [t for t in self.ouverts if t.fin_prevue]
        self.non_planifiables = [t for t in self.ouverts if t.non_planifiable]
        self.fin_projetee = max((t.fin_prevue for t in planifies), default=None)
        if self.fin_projetee and self.deadline:
            if self.fin_projetee > self.deadline:
                self.ecart = jours_ouvres_entre(self.deadline, self.fin_projetee, eq.feries)
            else:
                self.ecart = -jours_ouvres_entre(self.fin_projetee, self.deadline, eq.feries)
        else:
            self.ecart = None

    def _utilisation(self):
        """AF9 : h restantes assignées / capacité allouée, d'aujourd'hui à la deadline (ou à la fin projetée)."""
        eq = self.equipe
        fin = self.deadline if (self.deadline and self.deadline >= self.aujourdhui) else self.fin_projetee
        self.fin_periode = fin
        cles = set()
        for cle, m in eq.membres.items():
            if m["allocation"].get(self.slug, 0) > 0:
                cles.add(cle)
        for t in self.ouverts:
            nature, nom = decouper_assigne(t.assigne)
            if nature == "salarie":
                cles.add(nom)
        self.utilisation = []
        for cle in sorted(cles):
            m = eq.membres.get(cle)
            r = Ressource("salarie:" + cle, self.slug, eq)
            heures = sum(t.reste for t in self.ouverts if decouper_assigne(t.assigne) == ("salarie", cle))
            capa = 0.0
            if fin and not r.raison:
                d = self.aujourdhui
                while d <= fin:
                    capa += r.capacite(d)
                    d += timedelta(days=1)
            taux = heures / capa if capa > 0 else None
            self.utilisation.append({
                "cle": cle,
                "prenom": m["prenom"] if m else cle,
                "allocation": m["allocation"].get(self.slug, 0.0) if m else 0.0,
                "heures": heures,
                "capacite": capa,
                "taux": taux,
                "raison": r.raison,
            })

    def _alertes(self):
        eq, auj = self.equipe, self.aujourdhui
        al = []
        if self.part_budget is not None and self.part_budget > SEUIL_BUDGET:
            quoi = "budget client consommé" if self.a_part_esn else (
                "budget de fonctionnement consommé" if self.interne else "budget consommé")
            al.append(("Budget", "{} {} sur {} ({}), au-delà de {} (S1-R11)".format(
                quoi, fmt_eur(self.consomme), fmt_eur(self.budget), fmt_pct(self.part_budget),
                fmt_pct(SEUIL_BUDGET))))
        if self.fin_projetee and self.deadline and self.fin_projetee > self.deadline:
            al.append(("Délais", "fin projetée le {} après la deadline du {} ({}) (S1-R11)".format(
                self.fin_projetee.isoformat(), self.deadline.isoformat(), fmt_jo(self.ecart, signe=True))))
        for t in self.ouverts:
            if t.priorite == "critique":
                al.append(("Critique", "{} « {} » est ouvert ({})".format(t.id, t.titre, t.statut)))
        for t in self.ouverts:
            if t.statut == "EN_COURS":
                derniere = t.derniere_maj()
                if derniere is None:
                    continue
                n = jours_ouvres_entre(derniere, auj, eq.feries)
                if n > SEUIL_SANS_MAJ_JO:
                    al.append(("Sans mise à jour", "{} EN_COURS sans mise à jour depuis {} j ouvrés (dernière : {}) "
                               "(S1-R12)".format(t.id, n, derniere.isoformat())))
        concernes = {u["cle"] for u in self.utilisation}
        for cle in sorted(concernes):
            m = eq.membres.get(cle)
            dep = eq.date_depart(cle)
            if m and dep and dep >= auj and m["statut"] != "parti":
                n = jours_ouvres_entre(auj, dep, eq.feries)
                if n < SEUIL_PREAVIS_JO:
                    al.append(("Préavis de départ", "{} part le {} : {} de préavis, moins de {} (S1-R8)".format(
                        m["prenom"], dep.isoformat(), fmt_jo(n), SEUIL_PREAVIS_JO)))
        for t in self.ouverts:
            nature, _ = decouper_assigne(t.assigne)
            if nature == "salarie" and t.debut_prevu and t.fin_prevue:
                r = self.ressources.get(t.assigne)
                for e in (r.absences_sur(t.debut_prevu, t.fin_prevue) if r else []):
                    al.append(("Absence (S1-R9)", "{} ({}) : fenêtre prévue du {} au {} chevauche {} ({} → {})".format(
                        t.id, t.assigne, t.debut_prevu.isoformat(), t.fin_prevue.isoformat(), e["id"],
                        e["debut"].isoformat(), e["fin"].isoformat())))
        for t in self.non_planifiables:
            al.append(("Non planifiable", "{} : {}".format(t.id, t.non_planifiable)))
        for u in self.utilisation:
            if u["allocation"] > 0 and u["taux"] is not None and u["taux"] < SEUIL_UTILISATION:
                al.append(("Utilisation (info)", "{} utilisé à {} de sa capacité allouée : ajuster l'allocation ? "
                           "(AF9, indicateur)".format(u["prenom"], fmt_pct(u["taux"]))))
            elif u["taux"] is not None and u["taux"] > 1.0:
                al.append(("Surcharge", "{} : {} assignées pour {} de capacité allouée ({})".format(
                    u["prenom"], fmt_h(u["heures"]), fmt_h(u["capacite"]), fmt_pct(u["taux"]))))
        self.alertes = al


def consommer(ressource, debut, heures):
    """Consomme `heures` sur la ressource à partir du point (date, fraction de journée).
    Retourne (premier jour travaillé, point de fin) ou None si impossible sur l'horizon."""
    d, f = debut
    if heures <= 1e-9:
        return d, (d, f)
    premier, restant = None, heures
    for _ in range(HORIZON_JOURS):
        if ressource.limite and d > ressource.limite:
            return None
        cap = ressource.capacite(d)
        if cap > 0 and f < 1.0:
            dispo = cap * (1.0 - f)
            if premier is None:
                premier = d
            if restant <= dispo + 1e-9:
                return premier, (d, min(1.0, f + restant / cap))
            restant -= dispo
        d, f = d + timedelta(days=1), 0.0
    return None


# ============================================================================ rendu

def tableau_md(entetes, lignes):
    sortie = ["| " + " | ".join(entetes) + " |", "|" + "---|" * len(entetes)]
    for l in lignes:
        sortie.append("| " + " | ".join(cellule(c) if not isinstance(c, Brut) else c for c in l) + " |")
    return sortie


class Brut(str):
    """Cellule déjà formatée (pas d'échappement)."""


def nom_mermaid(texte_brut):
    t = re.sub(r"[:#;]", " ", texte(texte_brut))
    return re.sub(r"\s+", " ", t).strip()[:60] or "?"


def gantt(p):
    taches = {}
    for t in p.tickets:
        if t.statut == "TERMINE":
            debut = t.debut_le or t.cree_le
            fin = t.termine_le or t.maj_le
            if not debut or not fin or fin < debut:
                continue
            tags = ["done"]
        elif t.ouvert and t.debut_prevu and t.fin_prevue:
            debut, fin = t.debut_prevu, t.fin_prevue
            tags = []
            if t.priorite == "critique" or t.statut in ("BLOQUE", "ATTENTE_HUMAIN"):
                tags.append("crit")
            if t.statut in ("EN_COURS", "EN_REVUE"):
                tags.append("active")
        else:
            continue
        section = nom_mermaid((t.assigne or "sans assigné").replace(":", " "))
        ligne = "    {} {} :{}{}, {}, {}".format(
            t.id, nom_mermaid(t.titre), "".join(x + ", " for x in tags), t.id.lower().replace("-", ""),
            debut.isoformat(), (fin + timedelta(days=1)).isoformat())   # fin exclusive dans Mermaid
        taches.setdefault(section, []).append(ligne)
    if not taches:
        return ["_Aucun ticket à représenter._"]
    out = ["```mermaid", "gantt",
           "    title Planning — {} (calculé le {})".format(nom_mermaid(p.slug), p.aujourdhui.isoformat()),
           "    dateFormat YYYY-MM-DD", "    axisFormat %d/%m"]
    for section in sorted(taches):
        out.append("    section {}".format(section))
        out.extend(taches[section])
    if p.deadline:
        out += ["    section Jalons", "    Deadline :milestone, deadline, {}, 0d".format(p.deadline.isoformat())]
    out.append("```")
    return out


def libelle_fin(p):
    """Texte de la fin projetée d'un projet calculé (aussi utilisé par scripts/console.py)."""
    fin = "—"
    if p.fin_projetee:
        fin = p.fin_projetee.isoformat()
        if p.non_planifiables:
            fin += " (hors {} ticket(s) non planifiable(s))".format(len(p.non_planifiables))
    elif p.non_planifiables:
        fin = "indéterminée ({} ticket(s) non planifiable(s))".format(len(p.non_planifiables))
    elif not p.tickets:
        fin = "— (aucun ticket)"
    elif not p.ouverts:
        fin = "— (aucun ticket ouvert)"
    return fin


def rendre_tableau(p):
    eq, auj = p.equipe, p.aujourdhui
    L = [EN_TETE, "", "# Tableau de bord — {} (`{}`)".format(p.client, p.slug), "",
         ENCADRE.format(d=auj.isoformat()), ""]

    fin = libelle_fin(p)
    ecart = "—" if p.ecart is None else fmt_jo(p.ecart, signe=bool(p.ecart))
    budget = "{} / {} ({})".format(fmt_eur(p.consomme), fmt_eur(p.budget), fmt_pct(p.part_budget)) \
        if p.budget else "{} / non renseigné".format(fmt_eur(p.consomme))
    if p.a_part_esn:
        couts = [
            ["Budget client consommé / prévu (imputation client, R18)", budget],
            ["Coût client projeté à terminaison (consommé + reste × taux)", fmt_eur(p.projete)],
            ["Pris en charge par l'ESN (imputation esn, {}) : consommé · projeté".format(
                ", ".join(p.decisions_esn)), "{} · {}".format(fmt_eur(p.consomme_esn), fmt_eur(p.projete_esn))],
            ["Coût total projeté (client + ESN)", fmt_eur(p.projete_total)],
        ]
    else:
        couts = [
            ["Budget de fonctionnement consommé / prévu (projet interne, R19)" if p.interne
             else "Budget consommé / prévu", budget],
            ["Coût projeté à terminaison (consommé + reste × taux)", fmt_eur(p.projete)],
        ]
    L += ["## Synthèse", ""]
    L += tableau_md(["Indicateur", "Valeur"], [
        ["Type · état", "{} · {}".format(p.type_projet, p.etat)],
        ["Avancement (h estimées terminées / h estimées hors ANNULE)",
         "{} ({} / {})".format(fmt_pct(p.avancement), fmt_h(p.est_termine), fmt_h(p.est_total))],
        ["Temps restant (Σ max(0, estimation − passé), DEC-001 § 4)", fmt_h(p.temps_restant)],
    ] + couts + [
        ["Fin projetée", fin],
        ["Deadline", p.deadline.isoformat() if p.deadline else "non renseignée"],
        ["Écart avec la deadline", ecart],
    ])

    L += ["", "## Alertes", ""]
    L += tableau_md(["Type", "Détail"], p.alertes) if p.alertes else ["Aucune alerte."]

    L += ["", "## Tickets par statut", ""]
    comptes = [[s, str(sum(1 for t in p.tickets if t.statut == s))] for s in STATUTS]
    autres = sum(1 for t in p.tickets if t.statut not in STATUTS)
    if autres:
        comptes.append(["(statut inconnu)", str(autres)])
    comptes.append(["**Total**", str(len(p.tickets))])
    L += tableau_md(["Statut", "Nombre"], comptes)

    L += ["", "## Tickets BLOQUE", ""]
    bloques = [t for t in p.tickets if t.statut == "BLOQUE"]
    if bloques:
        lignes = []
        for t in bloques:
            dep = t.depuis("bloqu")
            lignes.append([t.id, t.titre, t.assigne, t.bloque_par or "**non renseigné (S1-R3)**",
                           "{} (depuis {})".format(fmt_jo(jours_ouvres_entre(dep, auj, eq.feries)), dep.isoformat())
                           if dep else "inconnue"])
        L += tableau_md(["Ticket", "Titre", "Assigné", "Raison (bloque_par)", "Ancienneté"], lignes)
    else:
        L.append("Aucun ticket bloqué.")

    L += ["", "## En attente d'une décision humaine (ATTENTE_HUMAIN)", ""]
    attentes = sorted([t for t in p.tickets if t.statut == "ATTENTE_HUMAIN"], key=lambda t: (t.rang, t.id))
    if attentes:
        lignes = []
        for t in attentes:
            dep = t.depuis("attente")
            lignes.append([t.priorite, t.id, t.titre, t.assigne, t.bloque_par or "**non renseigné (S1-R3)**",
                           fmt_jo(jours_ouvres_entre(dep, auj, eq.feries)) if dep else "inconnue"])
        L += tableau_md(["Priorité", "Ticket", "Titre", "Porteur", "Question (bloque_par)", "Ancienneté"], lignes)
    else:
        L.append("Aucune décision attendue.")

    L += ["", "## Tickets salariés à faire par un humain (AF11)", ""]
    sal = [t for t in p.ouverts if decouper_assigne(t.assigne)[0] == "salarie"]
    if sal:
        L += tableau_md(["Ticket", "Titre", "Assigné", "Statut", "Reste", "Fenêtre prévue"], [
            [t.id, t.titre, t.assigne, t.statut, fmt_h(t.reste),
             "{} → {}".format(t.debut_prevu.isoformat(), t.fin_prevue.isoformat()) if t.fin_prevue
             else "non planifiable"] for t in sal])
    else:
        L.append("Aucun.")

    L += ["", "## Tickets formation ouverts", ""]
    form = [t for t in p.ouverts if t.type == "formation"]
    if form:
        L += tableau_md(["Ticket", "Titre", "Assigné", "Statut", "Estimation"],
                        [[t.id, t.titre, t.assigne, t.statut, fmt_h(t.estimation)] for t in form])
    else:
        L.append("Aucun.")

    L += ["", "## Utilisation des salariés (AF9, indicateur)", ""]
    if p.utilisation:
        periode = "du {} au {}".format(auj.isoformat(), p.fin_periode.isoformat()) if p.fin_periode else "indéterminée"
        L.append("Période : {}. Heures restantes assignées ÷ capacité allouée sur la période "
                 "(calendrier et jours fériés compris). Sous {}, proposer d'ajuster l'allocation ; "
                 "jamais de ticket artificiel.".format(periode, fmt_pct(SEUIL_UTILISATION)))
        L.append("")
        lignes = []
        for u in p.utilisation:
            if u["raison"]:
                obs = u["raison"]
            elif u["taux"] is None:
                obs = "capacité nulle sur la période"
            elif u["taux"] > 1.0:
                obs = "surcharge"
            elif u["taux"] < SEUIL_UTILISATION:
                obs = "sous {} : ajuster l'allocation ?".format(fmt_pct(SEUIL_UTILISATION))
            else:
                obs = "—"
            lignes.append([u["prenom"], fmt_nb(u["allocation"], 0) + " %", fmt_h(u["heures"]),
                           fmt_h(u["capacite"]), fmt_pct(u["taux"]), obs])
        L += tableau_md(["Salarié", "Allocation", "h restantes assignées", "Capacité allouée", "Utilisation",
                         "Observation"], lignes)
    else:
        L.append("Aucun salarié alloué ni assigné.")

    L += ["", "## Planning prévisionnel (Gantt)", ""]
    L += gantt(p)

    L += ["", "## Hypothèses de calcul", "",
          "- Taux : agent {} ; salarié : coût journalier ÷ {} (ARCHITECTURE § 8). Le budget consommé "
          "compte aussi le temps passé sur les tickets ANNULE.".format(
              fmt_eur(eq.taux_agent) + "/h", fmt_nb(HEURES_JOUR, 0)),
          "- Ordonnancement à partir du {} : dépendances, puis priorité (critique → basse), puis id ; "
          "un ticket à la fois par assigné.".format(auj.isoformat()),
          "- Capacité : agent {} par jour ouvré ; salarié capacite_h_semaine ÷ 5 × allocation au projet × "
          "capacité restante du calendrier (temps partiel moyenné sur 5 jours) ; nulle avant l'arrivée et "
          "après le départ.".format(fmt_h(CAPACITE_AGENT_H_JOUR)),
          "- Jours ouvrés : hors samedis, dimanches et jours fériés d'`equipe/calendrier.md`.",
          "- Les tickets BLOQUE et ATTENTE_HUMAIN sont supposés débloqués aujourd'hui ; leur date de fin est donc "
          "optimiste.",
          "- Tickets TERMINE dans le Gantt : de `cree_le` à `maj_le` (ou `debut_le` / `termine_le` s'ils existent)."]
    if p.a_part_esn:
        L.append("- Imputation (R18, DEC-023) : un ticket `imputation: esn` dont `imputation_decision` cite une "
                 "décision VALIDÉ de `docs/decisions/` est pris en charge par l'ESN : il sort du coût client, seul "
                 "comparé au budget (S1-R11), et reste compté dans la part ESN et le coût total. Sans décision "
                 "validée, il est compté au client.")
    if p.interne:
        L.append("- Projet interne de l'ESN (R19, DEC-023) : tous les tickets sont à la charge de l'ESN et "
                 "comparés au budget de fonctionnement (`budget_eur`).")

    L += ["", "## Anomalies de données", ""]
    an = sorted(set(p.anomalies))
    L += ["- " + a for a in an] if an else ["Aucune."]
    return "\n".join(L) + "\n"


def alertes_equipe(equipe, auj):
    """Alertes de l'équipe hors projet : préavis de départ (S1-R8), allocation > 100 % (S1-R10).
    Lignes [« (équipe) », type, détail] ; aussi utilisées par scripts/console.py."""
    alertes = []
    for cle in sorted(equipe.membres):
        m = equipe.membres[cle]
        dep = equipe.date_depart(cle)
        if dep and dep >= auj and m["statut"] != "parti":
            n = jours_ouvres_entre(auj, dep, equipe.feries)
            if n < SEUIL_PREAVIS_JO:
                alertes.append(["(équipe)", "Préavis de départ", "{} part le {} : {} de préavis (S1-R8)".format(
                    m["prenom"], dep.isoformat(), fmt_jo(n))])
        total = sum(m["allocation"].values())
        if total > 100:
            alertes.append(["(équipe)", "Allocation", "{} alloué(e) à {} au total, plus de 100 % (S1-R10)".format(
                m["prenom"], fmt_nb(total, 0) + " %")])
    return alertes


def sections_esn(projets):
    """Sections de PORTFOLIO.md propres à l'ESN (R18, R19, S1-R13), présentes seulement si elles ont un
    contenu : sans ticket `esn` ni projet interne, PORTFOLIO.md est inchangé."""
    concernes = [p for p in projets if p.a_part_esn or p.interne]
    if not concernes:
        return []
    L = ["", "## Coûts pris en charge par l'ESN", "",
         "Part ESN des projets clients (`imputation: esn` sur décision validée, R18) et projets internes de "
         "l'ESN (R19). Le coût client des projets clients n'en tient pas compte (S1-R11).", ""]
    lignes, conso, proj = [], 0.0, 0.0
    for p in concernes:
        lien = Brut("[{}](projets/{}/TABLEAU.md)".format(p.slug, p.slug))
        if p.interne:
            lignes.append([lien, "projet interne (R19)", fmt_eur(p.consomme), fmt_eur(p.projete),
                           fmt_eur(p.budget) if p.budget else "non renseigné", "—"])
            conso, proj = conso + p.consomme, proj + p.projete
        else:
            lignes.append([lien, "prise en charge sur projet client (R18)", fmt_eur(p.consomme_esn),
                           fmt_eur(p.projete_esn), "—", ", ".join(p.decisions_esn)])
            conso, proj = conso + p.consomme_esn, proj + p.projete_esn
    lignes.append(["**Total ESN**", "", fmt_eur(conso), fmt_eur(proj), "", ""])
    L += tableau_md(["Projet", "Nature", "Consommé", "Projeté à terminaison", "Budget de fonctionnement",
                     "Décisions"], lignes)
    internes = [p for p in projets if p.interne]
    if internes:
        L += ["", "## Plan de formation de l'ESN", "",
              "Tickets `formation` ouverts des projets internes (S1-R6, S1-R13).", ""]
        form = [(p, t) for p in internes for t in p.ouverts if t.type == "formation"]
        if form:
            L += tableau_md(["Projet", "Ticket", "Titre", "Assigné", "Statut", "Estimation", "Fin prévue"], [
                [p.slug, t.id, t.titre, t.assigne, t.statut, fmt_h(t.estimation),
                 t.fin_prevue.isoformat() if t.fin_prevue else "non planifiable"] for p, t in form])
        else:
            L.append("Aucun ticket `formation` ouvert.")
    return L


def rendre_portfolio(projets, equipe, auj, anomalies_globales):
    L = [EN_TETE, "", "# Portefeuille des projets", "", ENCADRE.format(d=auj.isoformat()), ""]
    L += ["## Vue d'ensemble", ""]
    if projets:
        lignes = []
        for p in projets:
            lignes.append([
                Brut("[{}](projets/{}/TABLEAU.md)".format(p.slug, p.slug)), p.client, p.type_projet, p.etat,
                fmt_pct(p.avancement),
                "{} / {}".format(fmt_eur(p.consomme), fmt_eur(p.budget) if p.budget else "—"),
                fmt_pct(p.part_budget),
                p.fin_projetee.isoformat() if p.fin_projetee else "—",
                p.deadline.isoformat() if p.deadline else "—",
                "—" if p.ecart is None else "{:+d}".format(p.ecart),
                str(sum(1 for t in p.tickets if t.statut == "BLOQUE")),
                str(sum(1 for t in p.tickets if t.statut == "ATTENTE_HUMAIN")),
                str(len(p.alertes))])
        L += tableau_md(["Projet", "Client", "Type", "État", "Avancement", "Budget consommé / prévu", "%",
                         "Fin projetée", "Deadline", "Écart (j ouvrés)", "BLOQUE", "ATTENTE_HUMAIN", "Alertes"],
                        lignes)
    else:
        L.append("Aucun projet dans `projets/`.")

    L += ["", "## Alertes", ""]
    alertes = [[p.slug, a, d] for p in projets for a, d in p.alertes] + alertes_equipe(equipe, auj)
    L += tableau_md(["Projet", "Type", "Détail"], alertes) if alertes else ["Aucune alerte."]

    L += ["", "## Décisions humaines attendues", ""]
    att = sorted([(t.rang, p.slug, t) for p in projets for t in p.tickets if t.statut == "ATTENTE_HUMAIN"],
                 key=lambda x: (x[0], x[1], x[2].id))
    if att:
        L += tableau_md(["Priorité", "Projet", "Ticket", "Titre", "Question (bloque_par)"],
                        [[t.priorite, slug, t.id, t.titre, t.bloque_par] for _, slug, t in att])
    else:
        L.append("Aucune.")

    L += sections_esn(projets)

    L += ["", "## Équipe : allocation et utilisation", ""]
    if equipe.membres:
        lignes = []
        for cle in sorted(equipe.membres):
            m = equipe.membres[cle]
            alloc = ", ".join("{} {}".format(s, fmt_nb(v, 0) + " %") for s, v in sorted(m["allocation"].items())) or "aucune"
            util = []
            for p in projets:
                for u in p.utilisation:
                    if u["cle"] == cle and u["taux"] is not None:
                        util.append("{} {}".format(p.slug, fmt_pct(u["taux"])))
            lignes.append([m["prenom"], m["statut"] or "—", m["niveau"] or "—",
                           fmt_nb(sum(m["allocation"].values()), 0) + " %", alloc, ", ".join(util) or "—"])
        L += tableau_md(["Salarié", "Statut", "Niveau", "Allocation totale", "Par projet", "Utilisation (AF9)"], lignes)
    else:
        L.append("Aucune fiche dans `equipe/membres/`.")

    L += ["", "## Événements d'équipe à venir", ""]
    evs = [e for e in equipe.evenements if e["fin"] >= auj]
    if evs:
        L += tableau_md(["Id", "Qui", "Type", "Du", "Au", "Motif", "Statut"],
                        [[e["id"], e["qui"], e["type"], e["debut"].isoformat(), e["fin"].isoformat(),
                          e["motif"], e["statut"]] for e in evs])
    else:
        L.append("Aucun.")

    L += ["", "## Anomalies de données", ""]
    an = list(anomalies_globales) + ["{} : {} anomalie(s), voir son TABLEAU.md".format(p.slug, len(set(p.anomalies)))
                                     for p in projets if p.anomalies]
    L += ["- " + a for a in an] if an else ["Aucune."]
    return "\n".join(L) + "\n"


def ecrire_si_change(chemin, contenu):
    try:
        with open(chemin, "r", encoding="utf-8", newline="") as f:
            if f.read() == contenu:
                return False
    except OSError:
        pass
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenu)
    return True


# ============================================================================ programme principal

def charger(racine, aujourdhui):
    """Lit l'équipe et tous les projets de `racine`, et calcule chaque projet.
    Retourne (equipe, projets, anomalies globales) ; aussi utilisé par scripts/console.py. N'écrit rien."""
    equipe = Equipe(racine)
    anomalies = list(equipe.anomalies)
    decisions = decisions_connues(racine)
    projets = []
    dossier_projets = os.path.join(racine, "projets")
    if os.path.isdir(dossier_projets):
        for nom in sorted(os.listdir(dossier_projets)):
            dossier = os.path.join(dossier_projets, nom)
            if not os.path.isdir(dossier):
                continue
            if not os.path.isfile(os.path.join(dossier, "projet.md")):
                anomalies.append("projets/{}/ : pas de projet.md, dossier ignoré".format(nom))
                continue
            p = Projet(racine, dossier, equipe, aujourdhui, decisions)
            p.calculer()
            projets.append(p)
    return equipe, projets, anomalies


def main(argv=None):
    defaut = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description="Génère TABLEAU.md (par projet) et PORTFOLIO.md (R9).")
    ap.add_argument("--racine", default=defaut, help="racine du dépôt (défaut : parent de scripts/)")
    ap.add_argument("--date", default="", help="date du calcul AAAA-MM-JJ (défaut : aujourd'hui)")
    a = ap.parse_args(argv)

    if yaml is None:
        ecrire_stdout("ERREUR: le module PyYAML est absent. Installer : python -m pip install -r requirements.txt "
                      "(Mac : python3 -m pip …)")
        return 2
    aujourdhui = date.today()
    if a.date:
        aujourdhui = en_date(a.date)
        if aujourdhui is None:
            ecrire_stdout("ERREUR: --date invalide (AAAA-MM-JJ attendu) : {}".format(a.date))
            return 2
    racine = os.path.abspath(a.racine)
    if not os.path.isdir(racine):
        ecrire_stdout("ERREUR: --racine introuvable : {}".format(racine))
        return 2

    equipe, projets, anomalies = charger(racine, aujourdhui)

    for p in projets:
        chemin = os.path.join(p.dossier, "TABLEAU.md")
        change = ecrire_si_change(chemin, rendre_tableau(p))
        ecrire_stdout("projets/{}/TABLEAU.md : {} · avancement {} · {} alerte(s)".format(
            p.slug, "écrit" if change else "inchangé", fmt_pct(p.avancement), len(p.alertes)))
    change = ecrire_si_change(os.path.join(racine, "PORTFOLIO.md"),
                              rendre_portfolio(projets, equipe, aujourdhui, anomalies))
    ecrire_stdout("PORTFOLIO.md : {} · {} projet(s)".format("écrit" if change else "inchangé", len(projets)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
