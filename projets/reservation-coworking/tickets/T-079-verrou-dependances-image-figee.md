---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-079
titre: Verrou des dépendances avec empreintes, image Python figée, pip à jour (veille P-2)
projet: reservation-coworking
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-079 — Verrou des dépendances avec empreintes, image Python figée, pip à jour (veille P-2)

## Description
Proposition **P-2** et constats 5 et 6 de la veille [2026-S48](../../../veille/2026-S48.md) (ticket de travail [T-077](T-077-veille.md)). Le ticket reprend et complète les constats 1 (moyen, dépendances transitives non verrouillées, `app/requirements.txt` et `app/Dockerfile:14`) et 5 (bas, image de base non épinglée par empreinte, `app/Dockerfile:3`) des rapports `securite` ([securite-2026-11-25-3.md](../rapports/securite-2026-11-25-3.md), toujours ouverts au rapport [securite-2026-11-26.md](../rapports/securite-2026-11-26.md)), qui n'avaient fait l'objet que de propositions. **Dédoublonnage** (2026-11-26) : aucun ticket du projet ne couvre le verrouillage avec empreintes, `--require-hashes`, l'épinglage par digest de `python:3.14-slim` ni la version de pip ; T-043 ne mentionne que l'usage de `pip-audit` lors de l'audit. Ticket créé en `A_FAIRE` pendant la pause du développement : **ni traité ni planifié** ; il sera trié à la reprise.

**Ce qui est en cause.**
- **Paquets** : Starlette, Pydantic et toutes les dépendances transitives ; pip de l'image ; image de base `python:3.14-slim` (tag flottant, mis à jour le 2026-11-24).
- **Versions installées de référence** : Starlette 1.10.0 et Pydantic 2.14.4 (observées le 2026-11-25 dans l'image d'aperçu ; `requirements.txt` inchangé depuis). FastAPI 0.162.7 déclare `starlette>=0.46.0` et `pydantic>=2.9.0` sans borne haute. Version de pip de l'image : **non lue** (à confirmer).
- **Versions corrigées des avis** : Starlette 1.3.1 (CVE-2026-54283, DoS par formulaires urlencoded), 1.1.0 (CVE-2026-48818, StaticFiles sous Windows ; CVE-2026-48817), 1.0.1 (CVE-2026-48710, validation de l'en-tête `Host`, sur laquelle s'appuie `TrustedHostMiddleware` de T-063) ; pip 26.2.0 (CVE-2026-13346, URLs doublement encodées) et 26.1.2 (CVE-2026-8643, chemin des scripts d'entrée), sévérité moyenne.
- **Sources** : [GitHub Advisory Database, Starlette](https://api.github.com/advisories?ecosystem=pip&affects=starlette&per_page=20) ; [GitHub Advisory Database, pip](https://api.github.com/advisories?ecosystem=pip&affects=pip&per_page=10) ; [PyPI fastapi 0.162.7](https://pypi.org/pypi/fastapi/0.162.7/json) ; [PyPI starlette 1.10.0](https://pypi.org/pypi/starlette/1.10.0/json) ; [PyPI pip](https://pypi.org/project/pip/) (consultés le 2026-11-26).
- **Impact** : aucune faille connue sur les versions résolues aujourd'hui ; le risque est la **dérive à la reconstruction**. Une image reconstruite (cache ou index figé, autre poste) pourrait embarquer une Starlette antérieure à 1.3.1, donc vulnérable, sans que rien ne le signale ; un pip ancien n'expose que la chaîne de construction (`pip install` au build).
- **Preuve** : métadonnées de FastAPI (`starlette>=0.46.0`), absence de fichier de verrouillage dans `app/`, `FROM python:3.14-slim` sans digest.

**Priorité `normale`** (proposition du `veilleur`, conservée) : aucune faille connue sur les versions résolues ; risque de dérive et pip à confirmer (`normale` au plus) ; application hors production.

**Affectation : `agent:dev-backend` (AF6).** `Dockerfile`, `requirements.txt` et `README.md` sont dans `app/`, périmètre d'écriture du `dev-backend` (règle 8), qui a écrit l'image en T-010.

**Compétence ajustée : `backend-python (confirme)` au lieu de `docker (confirme)`.** L'essentiel du travail est de l'outillage Python (fichier de verrouillage avec empreintes, `pip install --require-hashes`, mise à jour de pip) ; la partie Docker se limite à deux lignes du `Dockerfile` (`FROM` avec digest, installation). Aucun agent du catalogue ne possède `docker` : garder ce nom aurait imposé un salarié (Nadia, seule à l'avoir) sur un travail que l'agent peut faire, à 15 €/h. La partie Docker est contrôlée par la revue humaine (ci-dessous).

**Estimation : 2 h** (proposition conservée) : 1 h de verrou avec empreintes, 0,5 h d'image et de pip, 0,5 h de documentation de la règle de reconstruction.

**Recommandation pour le triage à la reprise du développement** (aucune dépendance ajoutée aujourd'hui, consigne du coordinateur) : ce ticket devrait être `TERMINE` **avant le GO [T-046](T-046-go-mise-en-production.md)**, et avant l'audit sécurité préalable au GO (T-043 ou son successeur), pour que `pip-audit` porte sur le fichier de verrouillage. Le chef-de-projet proposera alors de l'ajouter à `depend_de` de T-046.

**Revue humaine** : requise (chaîne d'approvisionnement, sécurité). **Ticket compagnon de revue humaine à créer au triage, à la reprise du développement** (non créé aujourd'hui, ticket non planifié). Relecteur pressenti : Karim (`backend-python` expert, `securite-applicative` confirme), avec l'avis de Nadia (`docker` confirme) sur la ligne `FROM` si besoin.

## Critères d'acceptation
- [ ] Un fichier de verrouillage complet (transitives comprises, avec empreintes `--hash=sha256:…`) existe dans `app/`, et le `Dockerfile` installe avec `pip install --require-hashes -r <fichier>`.
- [ ] Le fichier de verrouillage contient Starlette ≥ 1.3.1 et Pydantic ≥ 2.9.0 ; la sortie `pip freeze` de l'image construite est collée au journal.
- [ ] L'image de base est fixée par digest (`FROM python:3.14-slim@sha256:…`), ou le maintien du tag flottant est justifié par écrit dans `app/README.md`.
- [ ] `pip --version` dans l'image construite affiche 26.2.0 ou plus (sortie au journal), au besoin par une mise à jour de pip dans le `Dockerfile`.
- [ ] La règle de reconstruction (quand regénérer le verrou et le digest, avec quelle commande, qui lance `pip-audit` sur le fichier de verrouillage) est écrite dans `app/README.md`.
- [ ] L'image se construit (`docker build --build-arg GIT_COMMIT=<sha40> …`), `/health` répond avec le SHA, et la suite de tests passe (résultat `pytest` au journal).
- [ ] La ligne « Revue humaine » ci-dessous est remplie par le relecteur humain.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : oui (chaîne d'approvisionnement, sécurité ; ticket compagnon [T-100](T-100-revue-humaine-t-079.md), Karim, créé au triage le 2026-11-26)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 16:35 · agent:chef-de-projet · création (veille 2026-S48, proposition P-2, constats 5 et 6 ; reprend les constats 1 et 5 des rapports securite ; compétence portée de docker à backend-python ; non planifié, développement en pause) · 0 h
- 2026-11-26 22:45 · agent:chef-de-projet · SIMULATION · triage : ticket compagnon de revue humaine T-100 créé (Karim, 0,5 h, au budget client) ; l'ajout de ce ticket à depend_de du GO T-046 n'est pas fait (non retenu par DEC-020), proposé à l'arbitrage humain · 0 h
