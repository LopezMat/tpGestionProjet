#!/usr/bin/env python3
"""Hook PreToolUse (Write, Edit, MultiEdit) : applique R5 et R6 techniquement.

Responsable : C · Lot 2 (C) · voir CLAUDE.md R5/R6, ARCHITECTURE § 6 (garde-fous 1, 2, 5).

- R5 : personne d'autre qu'un humain ne fait passer un en-tête à un statut normalisé
  (accents retirés, majuscules) VALIDE. S'applique à tout frontmatter qui n'est pas
  un ticket, journaux compris (pas seulement s'il porte `valide_par` : sinon il
  suffirait de retirer ce champ pour contourner le hook).
- R6 : aucune écriture sur un document (frontmatter avec `valide_par`) dont
  l'en-tête actuel est VALIDÉ. Les deux journaux sont exclus de R6.
- Les tickets (frontmatter `id: T-NNN`) ne sont pas concernés.
- R9 (garde-fou 8) : aucune écriture par Write/Edit/MultiEdit sur les fichiers générés
  `PORTFOLIO.md` (racine) et `projets/<slug>/TABLEAU.md` ; seul `scripts/tableau.py` les écrit.
- Garde-fou 6 : toute écriture sous `templates/` (racine du dépôt) demande une confirmation
  humaine (décision JSON `ask` sur stdout), en doublon de la règle `ask` de settings.json.

Code de sortie : 0 = laisse passer (ou `ask` en JSON) ; 2 = refus (message sur stderr, montré à l'agent).
En cas d'erreur interne : refus par prudence (un hook de sécurité qui laisse passer
en silence ne protège rien).

Bibliothèque standard uniquement.
"""
import json
import os
import re
import sys
import unicodedata

JOURNAUX = {"docs/changelog-regles.md", "docs/decisions/readme.md"}
RE_TICKET = re.compile(r"^T-\d+$", re.IGNORECASE)
RE_GENERE = re.compile(r"^(portfolio\.md|projets/[^/]+/tableau\.md)$")
RE_CLE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")


def normaliser(valeur):
    """'Validé', 'VALIDE', '"validé"' -> 'VALIDE'."""
    if valeur is None:
        return ""
    v = unicodedata.normalize("NFKD", str(valeur))
    v = "".join(c for c in v if not unicodedata.combining(c))
    return v.strip().strip("'\"").strip().upper()


def lire_entete(texte):
    """Retourne le frontmatter sous forme de dict (clés en minuscules), ou None."""
    if texte is None:
        return None
    texte = texte.lstrip("﻿")
    lignes = texte.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lignes or lignes[0].strip() != "---":
        return None
    entete = {}
    for ligne in lignes[1:]:
        if ligne.strip() == "---":
            return entete
        m = RE_CLE.match(ligne.strip())
        if not m:
            continue
        cle, val = m.group(1).lower(), m.group(2)
        # Commentaire YAML en fin de ligne : ' # ...' (ou valeur qui commence par #)
        val = re.split(r"(?:^|\s)#", val, maxsplit=1)[0]
        entete[cle] = val.strip().strip("'\"").strip()
    return None  # pas de ligne de fermeture : pas un frontmatter


def est_ticket(entete):
    return bool(entete) and bool(RE_TICKET.match(entete.get("id", "")))


def lire_fichier(chemin):
    try:
        with open(chemin, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
            return f.read()
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
        return None


def simuler(outil, entree, ancien):
    """Contenu du fichier après l'outil, ou None si non calculable."""
    if outil == "Write":
        return entree.get("content", "")
    if ancien is None:
        return None
    if outil == "Edit":
        edits = [entree]
    elif outil == "MultiEdit":
        edits = entree.get("edits") or []
    else:
        return None
    texte = ancien
    for e in edits:
        vieux, neuf = e.get("old_string", ""), e.get("new_string", "")
        if not vieux or vieux not in texte:
            return None  # l'outil échouera de lui-même
        texte = texte.replace(vieux, neuf) if e.get("replace_all") else texte.replace(vieux, neuf, 1)
    return texte


def chemin_relatif(chemin, racine):
    chemin_abs = os.path.abspath(chemin if os.path.isabs(chemin) else os.path.join(racine, chemin))
    try:
        rel = os.path.relpath(chemin_abs, os.path.abspath(racine))
    except ValueError:  # autre lecteur sous Windows
        rel = chemin_abs
    return chemin_abs, rel.replace("\\", "/").lower()


def refuser(message):
    sys.stderr.buffer.write((message + "\n").encode("utf-8"))
    sys.stderr.flush()
    sys.exit(2)


MESSAGE_TEMPLATES = ("Templates protégés (ARCHITECTURE § 6, garde-fou 6 ; DEC-001 § 25) : {rel} définit "
                     "le format lu par tableau.py et par tous les agents. Toute modification passe par R11 "
                     "(PR, décision, changelog). Confirmation humaine requise.")


def analyser(donnees):
    """Retourne None si autorisé, ("deny", message) ou ("ask", message)."""
    outil = donnees.get("tool_name", "")
    entree = donnees.get("tool_input") or {}
    chemin = entree.get("file_path") or ""
    if outil not in ("Write", "Edit", "MultiEdit") or not chemin:
        return None

    racine = os.environ.get("CLAUDE_PROJECT_DIR") or donnees.get("cwd") or os.getcwd()
    chemin_abs, rel = chemin_relatif(chemin, racine)
    # R9, garde-fou 8 : fichiers générés, jamais modifiés à la main (ni par un agent).
    if RE_GENERE.match(rel):
        return "deny", ("Refusé (R9) : {rel} est généré par scripts/tableau.py et ne se modifie jamais "
                        "à la main. Mets à jour les tickets, puis lance « python scripts/tableau.py ». "
                        "Voir CLAUDE.md R9, ARCHITECTURE § 6 garde-fou 8.").format(rel=rel)
    refus = analyser_md(outil, entree, chemin_abs, rel) if rel.endswith(".md") else None
    if refus:
        return "deny", refus
    # Garde-fou 6 : templates/ à la racine du dépôt -> confirmation humaine. Doublon de la règle
    # `ask` Edit(/templates/**) de settings.json, dont l'ancrage dépend du dossier de lancement.
    if rel.startswith("templates/"):
        return "ask", MESSAGE_TEMPLATES.format(rel=rel)
    return None


def analyser_md(outil, entree, chemin_abs, rel):
    """R5 et R6 sur un fichier Markdown : None si autorisé, sinon le message de refus."""
    journal = rel in JOURNAUX

    ancien = lire_fichier(chemin_abs)
    nouveau = simuler(outil, entree, ancien)
    ent_ancien, ent_nouveau = lire_entete(ancien), lire_entete(nouveau)

    if est_ticket(ent_ancien) or est_ticket(ent_nouveau):
        return None

    # R6 : document VALIDÉ figé (sauf journaux)
    if (not journal and ent_ancien is not None and "valide_par" in ent_ancien
            and normaliser(ent_ancien.get("statut")) == "VALIDE"):
        return ("Refusé (R6) : {rel} est VALIDÉ (valide_par: {vp}, decision: {dec}) et donc figé "
                "pour les agents. Un humain doit d'abord le repasser en EN_REVUE dans son éditeur. "
                "Voir CLAUDE.md R6, ARCHITECTURE § 6 garde-fou 2.").format(
                    rel=rel, vp=ent_ancien.get("valide_par") or "?",
                    dec=ent_ancien.get("decision") or "?")

    # R5 : personne d'autre qu'un humain ne fait passer un en-tête à VALIDÉ (journaux compris).
    # Un statut déjà VALIDÉ et laissé tel quel n'est pas une écriture de VALIDÉ : pour un
    # document, R6 l'a déjà bloqué ci-dessus ; pour un journal, il est exclu de R6.
    deja_valide = ent_ancien is not None and normaliser(ent_ancien.get("statut")) == "VALIDE"
    if ent_nouveau is not None and normaliser(ent_nouveau.get("statut")) == "VALIDE" and not deja_valide:
        return ("Refusé (R5) : seul un humain passe un document à VALIDÉ (valeur écrite : « {v} », "
                "lue comme VALIDÉ). Laisse statut: EN_REVUE et crée un ticket ATTENTE_HUMAIN (R7). "
                "Fichier : {rel}. Voir CLAUDE.md R5, ARCHITECTURE § 6 garde-fous 1 et 5.").format(
                    v=ent_nouveau.get("statut"), rel=rel)
    return None


def main():
    try:
        brut = sys.stdin.buffer.read().decode("utf-8-sig")
        donnees = json.loads(brut)
        if not isinstance(donnees, dict):
            raise ValueError("entrée JSON inattendue")
        decision = analyser(donnees)
    except SystemExit:
        raise
    except Exception as exc:  # fermeture par défaut
        refuser("Refusé : hook proteger_valide en erreur ({}), écriture bloquée par prudence "
                "(R5/R6). Signale-le à l'humain.".format(exc))
    if decision and decision[0] == "deny":
        refuser(decision[1])
    if decision and decision[0] == "ask":
        sortie = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                         "permissionDecisionReason": decision[1]}}
        sys.stdout.buffer.write(json.dumps(sortie, ensure_ascii=False).encode("utf-8"))
        sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    main()
