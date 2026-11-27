---
titre: Coûts pris en charge par l'ESN (imputation des tickets) et projet interne de l'ESN (plan de formation)
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-26
valide_par:   Ethan              # rempli par l'humain qui valide
decision: DEC-023           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-023
date: 2026-11-26
decide_par: Ethan
projet: ESN
ticket:                     # aucun ticket débloqué ; répond aux questions ouvertes de DEC-020 et DEC-021, et au point 9 de lot2-D
modifie_une_regle: oui      # R18, R19 (CLAUDE.md) ; S1-R6, S1-R11, S1-R13 ; ticket.md v0.3, projet.md v0.3, membre.md v0.2 ; tableau.py
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-023 — Coûts pris en charge par l'ESN et projet interne de l'ESN

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de l'accord d'Ethan du 2026-11-26 sur le plan de la PR de règles `regles/couts-esn-formation` (options 1A et 2A), de ses réponses et de son « Pourquoi ». Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par` (skill `tracer-decision`).
>
> **Numérotation.** Le 2026-11-26, avant le commit, DEC-023 et DEC-024 étaient libres dans `docs/decisions/` et sur toutes les branches locales et distantes.

## Contexte
Les scénarios SIMULATION du 2026-11-26 ont ouvert deux questions qu'une PR de règles devait trancher (R11).

**1. Les coûts pris en charge par l'ESN.**
- [DEC-020](2026-11-26-DEC-020-simulation-budget-4200.md) a mis à la charge de l'ESN la crise et l'outillage commun de `reservation-coworking`, [DEC-021](2026-11-26-DEC-021-simulation-absence-lea-depart-hugo.md) les analyses d'événements d'équipe, et DEC-020 v0.3 le bug T-105 (garantie de livraison).
- Faute de mécanisme, ces tickets ne portaient qu'une ligne de journal « imputé à l'ESN ». `tableau.py` comptait tout dans le projet, et le `chef-de-projet` recalculait le coût client à la main dans T-008 (DEC-020, question ouverte, pistes (a) et (b)).
- Ce calcul manuel a dérivé :
  - deux chiffres pour le même coût client : 4 158,93 € (DEC-020 v0.3) et 4 173,93 € (T-008), soit 15 € d'écart dus à T-104 ;
  - une part ESN de 1 782,50 € dans T-008, alors que les mêmes tickets n'en représentent plus que 1 607,50 € (voir « Écart de 175 € » ci-dessous) ;
  - l'alerte à 90 % de S1-R11 portait sur le coût total, et non sur ce que paie le client.

**2. Le plan de formation de l'ESN.**
- [DEC-009](2026-11-24-DEC-009-budget-delais-coworking.md) point E et DEC-021 interdisent les tickets `formation` dans le projet client. Ils renvoient les besoins à un « plan de formation de l'ESN » qui n'existait pas.
- Besoins restés ouverts :
  - dépendance à Nadia (`sauvegarde-restauration`, `docker`) et à Karim (`securite-applicative`, revue humaine) ;
  - `documentation` sans titulaire après le départ de Hugo ;
  - second relecteur sécurité sans candidat ;
  - formation « supervision » de Nadia (EV-002) sans ticket.
- Le point 9 de `docs/a-integrer/lot2-D.md` (« Tickets internes à l'ESN ») était reporté depuis DEC-002.

### Écart de 175 € (vérifié dans l'historique Git)
- T-008 a calculé 1 782,50 € pour la part ESN au commit `e496641` (2026-11-26, 16:05). Ce montant comprend T-081 et T-083, cités par DEC-020 § 3.
- Ces deux tickets `decision` étaient alors `ATTENTE_HUMAIN`, avec `temps_passe_h: 0`. Leur reste à faire était donc projeté :
  - T-081, Nadia, 1,5 h × 450/7 = 96,43 € ;
  - T-083, Claire, 1 h × 550/7 = 78,57 €.
- Le commit `712b04d` (16:16, validations humaines de DEC-019 à DEC-021) les a passés `TERMINE` sans temps passé. Leur projection est tombée à 0 €.
- Aucune estimation des tickets de DEC-020 n'a changé entre ces deux commits. La baisse de 175 € vient donc de la clôture de T-081 et de T-083, et non d'une ré-estimation. La même baisse se retrouve sur le coût total projeté : 5 903,93 € sans T-105 dans T-008, puis 5 728,93 €.
- **Le chiffre du tableau fait foi.** Si Nadia et Claire ont réellement passé du temps sur T-081 et T-083, c'est à elles de le reporter dans `temps_passe_h` (R15). Le tableau le comptera alors dans la part ESN.

## Options étudiées
**Question 1, les coûts pris en charge par l'ESN**

| Option | Avantages | Inconvénients |
|---|---|---|
| **1A · Champ `imputation: client \| esn` + `imputation_decision: DEC-NNN`, lu par `tableau.py`** (retenue) | Les tickets restent dans le projet de leur code et de leurs dépendances (le GO T-046 dépend de T-029, T-087, T-092). Le coût client est calculé à partir des tickets (R9). On voit ce que chaque client coûte à l'ESN. Valeur par défaut `client` : sortie inchangée sans le champ | Pas de budget ESN unique (compensé par une section consolidée dans `PORTFOLIO.md`). Les heures ESN restent prises sur l'allocation du projet client |
| 1B · Déplacer les tickets vers un projet interne | Séparation nette, un seul budget ESN | `tableau.py` ne suit pas `depend_de` d'un projet à l'autre : le GO perdrait ses prérequis. Renumérotation et références cassées (DEC-019 à DEC-021, journaux). Code du client hors de son projet. Allocations à redécouper |
| 1C · Convention de journal et calcul manuel, écrits dans `avancement` | Aucun code | Le calcul a déjà dérivé. Le chiffre n'est pas tiré des tickets (contraire à R9). L'alerte reste faussée. Rien n'empêche d'imputer sans décision |

**Question 2, les formations hors projet client**

| Option | Avantages | Inconvénients |
|---|---|---|
| **2A · Projet interne `projets/esn-interne/` (`type_projet: interne`)** (retenue) | Réutilise tout le système : tickets, capacité par l'allocation, Gantt, alertes, utilisation AF9, section des formations. Les formations deviennent planifiées, chiffrées et arbitrées. Règle aussi lot2-D point 9 | Allocations et budget de fonctionnement à décider. Pas de CDC ni de GO : il faut une règle dédiée. Pas de dépendance calculée d'un ticket client vers une formation (remplacée par `BLOQUE`) |
| 2B · Registre `equipe/plan-formation.md` | Simple | Ni chiffré ni planifié par `tableau.py`. Double le rôle des tickets. Tenu à la main |
| 2C · Tickets `formation` dans les projets clients, avec `imputation: esn` | Aucune structure nouvelle | Contredit DEC-009 E et DEC-021. Stagiaire non alloué au projet, donc non planifiable. Une formation dure plus longtemps que le projet qui la porte |

## Décision
1. **Options 1A et 2A.**
   - Un travail sur l'application ou la livraison d'un client, même payé par l'ESN, reste dans le projet du client avec `imputation: esn`.
   - Un travail sans livrable client (formation, outils et règles communs, décisions d'événements d'équipe) va dans `projets/esn-interne/`.
   - `PORTFOLIO.md` consolide les deux.
2. **Nouvelles règles et règles modifiées** (texte complet et Pourquoi dans CLAUDE.md et S1) :
   - **R18**, imputation des coûts : `client` par défaut. `esn` seulement si `imputation_decision` cite une décision **`VALIDÉ`** de `docs/decisions/`. Sinon, le ticket est compté au client et une anomalie est signalée : décision absente, introuvable ou « décision non validée (R18) ». Le budget du client n'est comparé qu'au coût client.
   - **R19**, projet interne `projets/esn-interne/`.
   - **S1-R6**, ticket `formation` uniquement dans `esn-interne`. Un ticket client qui en dépend passe `BLOQUE` avec `bloque_par: formation esn-interne/T-NNN`.
   - **S1-R11**, alerte sur le coût imputé au budget du projet.
   - **S1-R13**, plan de formation de l'ESN.
3. **Les tickets `decision` d'événements d'équipe** (arrivée, départ, absence) sont créés dans `esn-interne` (CLAUDE.md § 5). La révision du budget d'un client reste dans le projet du client.
4. **`scripts/tableau.py`** sépare le coût client de la part ESN. Il ajoute les sections « Coûts pris en charge par l'ESN » et « Plan de formation de l'ESN » à `PORTFOLIO.md`. **Sa sortie est inchangée** pour un dépôt sans ticket `esn` ni projet `interne` (test, et `diff` sur le dépôt au 2026-11-26).
5. **Migration de `reservation-coworking`** : `imputation: esn` est renseigné dans les tickets déjà pris en charge par l'ESN, avec une ligne de journal.
   - `imputation_decision: DEC-020` : T-029, T-038, T-058, T-059, T-072, T-078, T-081, T-083, T-085, T-086, T-087, T-089, T-090, T-091, T-092, T-095 à T-099, et T-105 (v0.3, garantie de livraison) ;
   - `imputation_decision: DEC-021` : T-102, T-103.

   **T-104 reste au client** (support des utilisateurs du client). Le coût client confirmé est donc celui de T-008 (4 173,93 € avant le tri de T-105), et non 4 158,93 € : cela clôt l'écart signalé dans DEC-020 v0.3. T-080, T-093, T-094, T-100 et T-101 restent au client.
6. **`projets/esn-interne/` est créé** en `cadrage`, avec `budget_eur: 0` et une deadline vide jusqu'à **DEC-024**. Il contient le ticket de travail T-001 « Plan de formation initial » (`chef-de-projet`, à lancer après la validation de cette décision). DEC-024 décidera du budget de fonctionnement, de l'échéance, des allocations à `esn-interne` et des formations retenues, à partir de la proposition chiffrée de T-001. Celle-ci couvre `documentation`, le second relecteur `securite-applicative`, une deuxième personne sur `sauvegarde-restauration`, `docker` et la revue humaine, la formation « supervision » de Nadia (EV-002) et les besoins de DEC-009 E.
7. **Le chiffre du tableau fait foi** pour le coût client et pour la part ESN. Les calculs manuels de T-008 cessent : son critère « Condition 1 » lit le coût client projeté de `TABLEAU.md`.

## Pourquoi
Les mots d'Ethan : « Les scénarios ont montré que le calcul manuel du coût client dérive et fausse l'alerte budget : le tableau doit le calculer lui-même, et l'ESN ne prend un coût à sa charge que sur une décision humaine validée. Les formations doivent être planifiées et chiffrées comme le reste du travail, sans être facturées au client : d'où un projet interne de l'ESN. »

Sur T-104 : « support des utilisateurs du client » ; il reste donc au client.

Arguments retenus du plan :
- 1A garde les tickets à côté du code et des dépendances qu'ils servent ;
- exiger une décision **validée** empêche qu'une imputation à l'ESN masque un dépassement (condition 1 de DEC-020) ;
- 2A réutilise un outillage qui fonctionne déjà et rend les formations arbitrables comme le reste du travail.

## Impacts
- **Règles** :
  - CLAUDE.md v1.4 (R18, R19, § 1, § 2, arrêts humains, § 4, § 5) ;
  - S1 v1.2 (§ 3, § 4, S1-R6, S1-R11, S1-R13, § 6, § 7, § 8) ;
  - ARCHITECTURE v1.7 (§ 3, § 7, § 12).

  Ethan a repassé ces trois documents en `EN_REVUE`. Ils sont à revalider avec `decision: DEC-023`.
- **Agent et skills** : `chef-de-projet` (AF4, AF7, AF10, règles 6, 8, 9, 11, 15, 16, C9) ; `creer-ticket`, `avancement`, `revision-budget`, `absence`, `arrivee-membre`, `depart-membre`, `nouveau-projet`.
- **Modèles** (signalés à A et D, ARCHITECTURE § 12) : `ticket.md` v0.3 (`imputation`, `imputation_decision`), `projet.md` v0.3 (`type_projet: interne`), `membre.md` v0.2.
- **Scripts** : `scripts/tableau.py` et `scripts/test_tableau.py` (27 tests). `console.py` est inchangé : il affiche le coût client.
- **Projets** : `projets/esn-interne/` (projet.md, T-001). La migration de `reservation-coworking` porte sur 23 tickets, T-008 (critère « Condition 1 ») et `projet.md` (commentaire de `budget_eur`).
- **Non modifiés** : DEC-009, DEC-020 et DEC-021 (cette décision répond à leurs questions ouvertes) ; `cdc.md` et `planning.md` de `reservation-coworking` ; S2, S3, S4.
- **`docs/a-integrer/lot2-D.md`**, point 9 : intégré.
- **Reste manuel** : l'audit avant le GO (T-043, 5 h estimées pour 12,5 h passées, soit un reste de 0) n'est pas compté par le tableau (environ 75 €). Le `chef-de-projet` doit ré-estimer T-043 au prochain triage.
- **Suite** : validation humaine de DEC-023, de CLAUDE.md, de S1 et d'ARCHITECTURE ; puis T-001, le ticket `decision` « Plan de formation initial » et DEC-024 ; enfin, application des allocations à `esn-interne` dans `equipe/` par le coordinateur.
