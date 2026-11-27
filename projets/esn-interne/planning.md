---
titre: Planning — ESN (projet interne) : plan de formation initial
statut: EN_REVUE
responsable: agent:chef-de-projet
version: 0.1
maj_le: 2026-11-27
valide_par:
decision:
---
<!-- modèle : templates/planning.md v0.1 · responsable du modèle : A -->

# Planning — ESN (projet interne) : plan de formation initial

> Le Gantt détaillé est **généré** dans `TABLEAU.md` à partir des tickets. Ce document fixe les jalons et les hypothèses. Il tient aussi le **registre des compétences à risque** de l'ESN (S1-R13).

Sources : `equipe/membres/*.md`, `equipe/agents.md` (référentiel, hors périmètre agents), `equipe/calendrier.md` (EV-001 à EV-004), [DEC-009](../../docs/decisions/2026-11-24-DEC-009-budget-delais-coworking.md) point E, [DEC-019](../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md), [DEC-020](../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md), [DEC-021](../../docs/decisions/2026-11-26-DEC-021-simulation-absence-lea-depart-hugo.md), [DEC-023](../../docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md) ; `reservation-coworking` : `planning.md` v1.1, `TABLEAU.md` du 2026-11-27, T-103. Rédigé par le ticket de travail [T-001](tickets/T-001-plan-de-formation-initial.md).

**Statut du plan : proposition.** Les allocations, le budget de fonctionnement (`budget_eur`) et l'échéance (`deadline`) sont soumis à l'arbitrage humain du ticket [T-017](tickets/T-017-decision-plan-formation-initial.md) (décision attendue : DEC-024). Rien n'est appliqué dans `equipe/` ni dans `projet.md` avant cette décision (règle 13 du `chef-de-projet`). Ce document décrit l'**option B, recommandée** ; les options A, C et D sont chiffrées dans T-017.

## Registre des compétences à risque
Critères de S1-R13 : **compétence absente**, **un seul titulaire au niveau `confirme` ou plus**, **titulaire sur le départ**. Le registre retient les compétences pour lesquelles un humain est exigé (hors périmètre agents, revue humaine AF3, binôme AF5, recette, contact client) ou qu'aucun agent ne couvre. Les compétences couvertes par un agent et jamais soumises à une revue humaine sont regroupées à la fin.

État au 2026-11-27 (Hugo compté jusqu'au 2026-12-04, EV-004).

| # | Compétence | Titulaires `confirme`+ | Agents | Critère | Gravité | Déclencheur | Traitement proposé (option B) |
|---|---|---|---|---|---|---|---|
| R-01 | `documentation` | Hugo (confirmé), **part le 2026-12-04** | aucun | titulaire sur le départ, puis absente | haute | EV-004, DEC-021 | [T-012](tickets/T-012-formation-documentation-nadia.md) : Nadia, autoformation et livrable mis à l'épreuve par T-008 et T-010 |
| R-02 | `securite-applicative` (second relecteur) | Karim seul (confirmé) ; candidat de l'ex-T-053 (Hugo) part | `securite`, `architecte` | un seul titulaire ; Karim en congés du 2026-12-21 au 31 (EV-003) | **critique** | DEC-021, ex-`reservation-coworking/T-053` | [T-003](tickets/T-003-formation-securite-autoformation-lea.md) puis [T-004](tickets/T-004-formation-revue-humaine-lea.md) : Léa ; encadrement de Karim [T-005](tickets/T-005-encadrement-revue-securite-karim.md) |
| R-03 | revue humaine (`revue-humaine`, AF3, AF5) des tickets backend et sécurité, et des travaux de Nadia | Karim seul | hors périmètre agents | un seul titulaire | **critique** | DEC-021 ; `reservation-coworking/T-030` à `T-038`, `T-095` à `T-100` | T-004 (Léa, revues en double avec Karim). **Reste** : binôme AF5 d'un ticket `critique` `backend-python`, voir R-12 |
| R-04 | `sauvegarde-restauration` | Nadia seule (confirmée) | `deployeur`, `gestionnaire-crise` | un seul titulaire ; Nadia ne travaille pas le mercredi | **critique** | DEC-019 (crise T-080, « une règle sans preuve d'exécution n'est pas une garantie »), DEC-009 E | [T-008](tickets/T-008-formation-sauvegarde-restauration-karim.md) : Karim (expert `base-de-donnees-sql`) ; encadrement de Nadia [T-009](tickets/T-009-encadrement-sauvegarde-nadia.md) |
| R-05 | `docker` | Nadia seule (confirmée) | **aucun** | un seul titulaire ; toute la production est en Docker local (DEC-003) | haute | DEC-019, DEC-021 | [T-010](tickets/T-010-formation-docker-lea.md) : Léa ; encadrement de Nadia [T-011](tickets/T-011-encadrement-docker-nadia.md) |
| R-06 | `recette-fonctionnelle` | Claire seule (confirmée) | `testeur` (ne remplace pas la recette humaine, R16) | un seul titulaire ; un empêchement bloque le GO | haute | DEC-009 E ; `reservation-coworking/T-045` | [T-006](tickets/T-006-formation-recette-lea.md) : Léa, en binôme pendant T-045 ; encadrement de Claire [T-007](tickets/T-007-encadrement-recette-claire.md) |
| R-07 | `relation-client` | Claire seule (experte) | hors périmètre agents | un seul titulaire ; nécessaire aussi pour une recette avec le client (AF1) | moyenne | DEC-009 E | [T-013](tickets/T-013-formation-relation-client-lea.md) : Léa, en binôme ; encadrement de Claire [T-014](tickets/T-014-encadrement-relation-client-claire.md) |
| R-08 | `juridique` | **aucun** | hors périmètre agents | absente | moyenne | DEC-009 E ; `reservation-coworking/T-084` (CNIL, tranché sans avis juridique, DEC-019 v0.2) | option B : **pas de formation**, conseil juridique externe au cas par cas, sur décision humaine. Option A : [T-015](tickets/T-015-formation-juridique-claire.md) (Claire, formation externe) |
| R-09 | `supervision` | **aucun** au niveau confirmé (Nadia débutante) | `analyste-prod` | absente au niveau `confirme` | moyenne | EV-002 (2026-12-03), DEC-009 E | [T-002](tickets/T-002-formation-supervision-nadia.md) : Nadia, formation externe du 2026-12-03 |
| R-10 | `rgpd` | Claire seule (confirmée) | aucun | un seul titulaire | moyenne | `reservation-coworking` F-08 (CDC § 8) | non traité dans ce plan ; à revoir au retex de `reservation-coworking` |
| R-11 | `html-css`, `javascript`, `react`, `accessibilite` (revue humaine des tickets frontend critiques) | Léa seule | `dev-frontend` | un seul titulaire | faible | aucun ticket frontend critique en cours | non traité ; à surveiller au prochain projet avec un front critique |
| R-12 | `backend-python`, `base-de-donnees-sql`, `architecture-logicielle`, `revue-code` (binôme AF5 des tickets `critique` backend) | Karim seul (expert) | `dev-backend`, `architecte`, `relecteur-code` | un seul titulaire ; Karim en congés du 21 au 31/12 | haute | DEC-021 | **hors de portée d'un plan de quelques semaines** (montée à `confirme` en `backend-python` : plusieurs mois) ; recrutement ou plan 2027 à arbitrer. T-008 donne une seconde personne sur la base de données côté restauration |
| R-13 | `ci-cd`, `linux` | Nadia seule | `deployeur` (`ci-cd`) ; aucun pour `linux` | un seul titulaire | moyenne | — | réduit en partie par T-010 et T-008 ; non traité en propre |
| R-14 | `tests-e2e` | **aucun** au niveau confirmé (Léa débutante) | `testeur` | absente au niveau `confirme` ; obligatoire en e-commerce | faible aujourd'hui | fiche de Léa (AF7, AF10 c) | aucun ticket tant qu'aucun projet e-commerce n'est signé (pas de ticket artificiel) |
| R-15 | `paiement-en-ligne`, `tests-utilisateurs` | **aucun** | hors périmètre agents | absentes | faible aujourd'hui | aucun projet ne les demande | à traiter au premier projet e-commerce ou avec tests utilisateurs (AF4 : ticket `formation` ou recrutement) |
| R-16 | `porter-une-decision`, `revue-humaine` (données) | aucune fiche ne les déclare | hors périmètre agents | donnée absente des fiches | faible | AF2, AF3 | Claire porte les décisions et Karim fait les revues de fait : AF2 et AF3 ne sont pas vérifiables par `tableau.py`. Mise à jour des fiches à proposer au coordinateur (après décision humaine) |
| R-17 | ex-`reservation-coworking/T-052` (`backend-python`, Hugo) | — | — | besoin éteint (départ) | — | DEC-021 | retiré du plan |

**Couvertes par les agents, risque faible** (pas de revue humaine spécifique, aucun ticket) : `recueil-besoin`, `gestion-projet` (Claire seule, plus `analyste-besoin` et `chef-de-projet`), `tests-unitaires` (plus aucun salarié après Hugo ; `dev-backend`, `dev-frontend`, `testeur`), `redaction-cdc`, `analyse-existant`, `estimation`, `planification`, `suivi-budget`, `choix-stack`, `api-rest`, `deploiement-render`, `audit-dependances`, `analyse-logs`, `veille-technologique`, `support-utilisateur`, `gestion-de-crise` (la communication de crise relève de `relation-client`, R-07).

**Constat transverse.** Trois personnes concentrent les risques critiques : Karim (R-02, R-03, R-12), Nadia (R-04, R-05, R-13) et Claire (R-06, R-07, R-10). Léa est la seule salariée sans allocation (0 % sur tous les projets) : c'est elle qui a la capacité de devenir la seconde personne. Le plan la rend seconde sur plusieurs compétences ; c'est un risque de concentration connu (voir « Risques planning »), qui reste préférable à une personne unique par compétence.

## Plan proposé (option B, recommandée)
| Ordre | Besoin | Ticket(s) | Candidat | Modalité | Niveau visé à la fin | h salarié | h formateur | Coût temps (€) | Frais externes (€ HT) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | second relecteur `securite-applicative`, revue humaine | T-003, T-004, T-005 | Léa (formateur : Karim) | autoformation guidée, puis revues humaines en double avec Karim | `securite-applicative` et `revue-humaine` confirmées | 11 | 2 | 707,14 + 157,14 = 864,29 | 0 |
| 2 | `sauvegarde-restauration` | T-008, T-009 | Karim (formatrice : Nadia) | binôme interne : restauration réelle dans une base jetable, en suivant le runbook | confirmé | 5 | 2 | 392,86 + 128,57 = 521,43 | 0 |
| 3 | `supervision` | T-002 | Nadia | formation externe d'une journée (EV-002) | confirmée | 7 | — | 450,00 | provision 700 (à confirmer par devis) |
| 4 | `documentation` | T-012 | Nadia | autoformation et livrable (guide d'exploitation Docker et restauration), mis à l'épreuve par T-008 et T-010 | confirmée | 7 | — | 450,00 | 0 |
| 5 | `recette-fonctionnelle` | T-006, T-007 | Léa (formatrice : Claire) | binôme interne pendant la recette `reservation-coworking/T-045` | confirmée | 4 | 1 | 257,14 + 78,57 = 335,71 | 0 |
| 6 | `docker` | T-010, T-011 | Léa (formatrice : Nadia) | autoformation et binôme interne, à partir du guide T-012 | débutante (autonome sur les procédures écrites) | 7 | 3 | 450,00 + 192,86 = 642,86 | 0 |
| 7 | `relation-client` | T-013, T-014 | Léa (formatrice : Claire) | binôme interne sur les échanges client de fin de projet | débutante | 3 | 1 | 192,86 + 78,57 = 271,43 | 0 |
| — | `juridique` | T-015 (option A seulement) | Claire | formation externe d'une journée | débutante | 7 | — | 550,00 | provision 700 |

**Ordre de priorité** (risque d'abord, puis fenêtre de temps) : 1. sécurité et revue humaine, avant les congés de Karim ; 2. sauvegarde-restauration (leçon de DEC-019) ; 3. supervision (date fixée, EV-002) ; 4. documentation (support de 2 et 6) ; 5. recette (fenêtre unique de T-045) ; 6. docker ; 7. relation client ; 8. juridique (reportée, conseil externe).

## Jalons
| Jalon | Date cible | Tickets inclus | Critère de passage |
|---|---|---|---|
| Plan de formation décidé | **2026-11-30** au mieux ; **2026-12-02 au plus tard** | T-017 | décision humaine DEC-024 ; allocations reportées dans `equipe/` et `projet.md` par le coordinateur |
| Sécurité : autoformation de Léa | 2026-11-30 → 2026-12-04 | T-003 | grille de relecture d'une page relue par Karim |
| Supervision de Nadia | **2026-12-03** (date fixe, EV-002) | T-002 | attestation de présence ; restitution écrite au journal |
| Revues humaines en double | 2026-12-07 → 2026-12-11 | T-004, T-005 | au moins 3 revues en double ; attestation de Karim ; **avant le 2026-12-18** (congés de Karim) |
| Recette en binôme | 2026-12-10 → 2026-12-15 | T-006, T-007 | Léa a déroulé au moins 2 parcours du rapport de recette de T-045 ; attestation de Claire |
| Relation client en binôme | 2026-11-30 → 2026-12-18 | T-013, T-014 | au moins 2 échanges client suivis avec Claire ; débriefing |
| Documentation | 2026-12-21 → 2026-12-29 | T-012 | guide d'exploitation publié dans `projets/esn-interne/` |
| Docker | 2026-12-29 → 2027-01-12 | T-010, T-011 | Léa monte seule un environnement de recette à partir du guide |
| Sauvegarde-restauration | 2027-01-04 → 2027-01-13 | T-008, T-009 | Karim restaure seul, en suivant le runbook, dans une base jetable ; durée mesurée |
| **Fin du plan** | **2027-01-15** | tous | tickets `TERMINE` ; niveaux atteints proposés ; mise à jour des fiches par le coordinateur après décision humaine |

Dates en heures équivalent humain et en jours ouvrés (S1-R9). Le 2026-12-25 et le 2027-01-01 sont fériés.

## Hypothèses de capacité
**Périodes.** P1 : du 2026-11-30 au 2026-12-18 (15 jours ouvrés, fin de `reservation-coworking`). P2 : du 2026-12-21 au 2027-01-15 (18 jours ouvrés).

| Ressource | Type | Allocation proposée à `esn-interne` (P1 / P2) | h/semaine disponibles (P1 / P2) | Taux €/h |
|---|---|---|---|---|
| agent:chef-de-projet | agent | — | — | 15 |
| salarie:claire | salarié | 5 % / 0 % | 1,75 / 0 | 78,57 |
| salarie:karim | salarié | 5 % / 10 % (congés du 21 au 31/12) | 1,75 / 3,5 | 78,57 |
| salarie:lea | salarié | 25 % / 10 % | 8,75 / 3,5 | 64,29 |
| salarie:nadia | salarié | 10 % / 20 % (temps partiel, 28 h) | 2,8 / 5,6 | 64,29 |

**Contrôle du total des allocations (S1-R10)** : `reservation-coworking` + `esn-interne` ≤ 100 % pour chacun.

| Salarié | `reservation-coworking` P1 | `esn-interne` P1 | **Total P1** | `reservation-coworking` P2 | `esn-interne` P2 | **Total P2** |
|---|---|---|---|---|---|---|
| Claire | 20 % | 5 % | **25 %** | 20 % (10 % proposé après le GO) | 0 % | **20 %** |
| Karim | 20 % | 5 % | **25 %** | 20 % (5 % proposé après ses revues) | 10 % | **30 %** au plus |
| Léa | 0 % | 25 % | **25 %** | 0 % | 10 % | **10 %** |
| Nadia | 50 % (jusqu'au 2026-12-18, DEC-020) | 10 % | **60 %** | 5 % (DEC-019, planning v1.1) | 20 % | **25 %** (70 % si les 50 % étaient prolongés) |

Aucun total ne dépasse 100 %, même dans le cas le plus chargé.

**Contrôle de capacité** (h disponibles sur `esn-interne` × période ≥ h planifiées) :

| Salarié | Période | h/jour (capacité ÷ 5 × allocation) | Jours ouvrés utiles | Capacité allouée | h planifiées | Utilisation (AF9) |
|---|---|---|---|---|---|---|
| Claire | P1 | 0,35 | 15 | 5,25 h | 2 h (T-007, T-014) | **38,1 %**, sous 50 % |
| Karim | P1 | 0,35 | 15 | 5,25 h | 2 h (T-005) | **38,1 %**, sous 50 % |
| Karim | P2 | 0,70 | 10 (congés du 21 au 31/12) | 7,0 h | 5 h (T-008) | 71,4 % |
| Léa | P1 | 1,75 | 15 (retour le 2026-11-30) | 26,25 h | 18 h (T-003, T-004, T-006, T-013) | 68,6 % |
| Léa | P2 | 0,70 | 18 | 12,6 h | 7 h (T-010) | 55,6 % |
| Nadia | P1 | 0,56 | 14 (EV-002 compté à 0 par `tableau.py`) | 7,84 h | 7 h (T-002) | 89,3 % |
| Nadia | P2 | 1,12 | 18 | 20,16 h | 12 h (T-012, T-011, T-009) | 59,5 % |

- **AF9, sous 50 %, signalé** : Claire et Karim en P1 (38,1 %). Le besoin réel est de 2 h chacun ; 5 % est la plus petite allocation qui laisse le binôme se faire dans la fenêtre (avant le 2026-12-15 pour Claire, avant le 2026-12-18 pour Karim). Un humain peut retenir 3 % (63,5 %), au prix d'une fenêtre plus serrée. Aucun ticket n'est ajouté pour atteindre un taux.
- **Léa** : 75 % à 90 % de sa capacité ne sont alloués à aucun projet. C'est une question d'activité commerciale de l'ESN, hors de ce plan, signalée au coordinateur.
- **Nadia, semaine du 2026-12-03** : 14 h sur `reservation-coworking` et 7 h de formation, soit 21 h sur 28 h. La charge tient.

**Limites du calcul de `tableau.py`** :
- l'allocation est une seule valeur par projet : le passage de P1 à P2 se fait par une mise à jour d'`equipe/` par le coordinateur, le 2026-12-21 (comme la fin des 50 % de Nadia sur `reservation-coworking`) ;
- EV-002 met la capacité de Nadia à 0 le 2026-12-03 : `tableau.py` placera T-002 sur d'autres jours. Le coût est juste, la date réelle est le 2026-12-03. Il ne faut pas annuler EV-002 : sa capacité nulle est juste pour `reservation-coworking` ;
- les frais externes ne sont pas comptés par `tableau.py` (il ne chiffre que des heures) : ils sont suivis ici et dans DEC-024, dans une enveloppe séparée.

## Charge et budget prévisionnels
*Taux (ARCHITECTURE § 8) : agent 15 €/h ; Claire et Karim 550 €/j ÷ 7 = 78,57 €/h ; Léa et Nadia 450 €/j ÷ 7 = 64,29 €/h.*

**Option B (recommandée)** :

| Ressource | Tickets | h | € |
|---|---|---|---|
| Léa | T-003, T-004, T-006, T-010, T-013 | 25,0 | 1 607,14 |
| Nadia | T-002, T-009, T-011, T-012 | 19,0 | 1 221,43 |
| Karim | T-005, T-008 | 7,0 | 550,00 |
| Claire | T-007, T-014 | 2,0 | 157,14 |
| agent:chef-de-projet | T-001 (3 h passées), T-016 (pilotage, 3 h), T-017 (0,5 h) | 6,5 | 97,50 |
| **Total temps** | | **59,5** | **3 633,21** |

- **Charge totale estimée** : 59,5 h équivalent humain, dont 53 h de salariés (9 h de formateurs : Karim 2 h, Nadia 5 h, Claire 2 h, soit 635,71 €).
- **Budget de fonctionnement proposé (`budget_eur`)** : **4 360 €** = 3 633,21 € + marge de 20 % (726,64 €), arrondi à la dizaine supérieure.
- **Marge** : 726,79 €, soit 20 %. Elle couvre : le rythme individuel des autoformations (aucun historique dans l'ESN) ; une séance de binôme à refaire si un ticket client glisse (T-045, revues de Karim) ; les analyses d'événements d'équipe imputées à ce projet (CLAUDE.md § 5, environ 7,50 à 15 € chacune). Un outil commun d'un montant plus élevé passera par une révision du budget, décidée par un humain.
- **Enveloppe de frais externes, séparée** : **700 € HT** (provision pour la journée « supervision » de Nadia, à confirmer par devis ; 0 € si elle est déjà réglée ou gratuite).
- **Seuil d'alerte S1-R11** : 90 % de 4 360 €, soit 3 924 € consommés.
- **Échéance proposée (`deadline`)** : **2027-01-15**.

## Risques planning
| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| DEC-024 prise après le 2026-12-02 | moyenne | T-002 (2026-12-03) n'est pas prenable (il dépend de T-017) ; T-003 et T-004 n'ont plus le temps de finir avant les congés de Karim | décision demandée pour le 2026-11-30 ; T-002 peut être arbitré à part, en premier |
| Les binômes gênent le chemin critique de `reservation-coworking` (recette T-045, revues de Karim T-037, T-097 à T-099, GO du 2026-12-15) | moyenne | retard du GO : marge de 2 jours ouvrés seulement | Léa observe et ne signe rien ; Claire et Karim restent seuls responsables de la recette et des revues ; le formateur peut suspendre le binôme sans délai ; temps d'explication compté à part (T-005, T-007) |
| Karim n'atteint pas l'attestation de Léa avant le 2026-12-18 | moyenne | pas de second relecteur pendant ses congés (21 au 31/12) | priorité 1 ; T-003 dès le 2026-11-30 ; sinon, poursuite en janvier, et aucun ticket sécurité livré pendant les congés sans revue reportée |
| Karim n'est que `confirme` en `securite-applicative` | certaine | le binôme « sous le niveau avec un expert » (AF7) n'est pas possible : Léa ne relit seule qu'une fois `confirme` | jusqu'à l'attestation, Karim signe seul les revues ; l'attestation est une décision humaine |
| Concentration sur Léa (seconde sur 5 compétences) | moyenne | une absence de Léa rouvre plusieurs risques à la fois | elle reste « seconde » : chaque compétence garde son titulaire ; à revoir au retex |
| Congés de fin d'année non déclarés (Claire, Léa, Nadia) | moyenne | P2 décalée | à confirmer par le coordinateur ; sinon, report de T-010, T-011 et T-012 en janvier, échéance inchangée (marge du 2027-01-11 au 15) |
| Documentation (T-012) en retard | faible | T-008 et T-010 attendent (`depend_de`) | T-012 en priorité haute en début de P2 ; à défaut, T-008 sur le runbook existant `perte-donnees` |
| Frais externes de la supervision inconnus | moyenne | enveloppe de 700 € fausse | devis à demander avant le 2026-12-03 ; enveloppe séparée du `budget_eur` |
| Niveaux visés surestimés (`docker` et `relation-client` à `debutant` seulement) | moyenne | R-05 et R-07 restent ouverts au niveau `confirme` | réévaluation au retex ; un binôme sur un projet réel au prochain contrat |
| `backend-python` et le binôme AF5 restent chez Karim seul (R-12) | certaine | aucun ticket `critique` backend ne peut être piloté pendant ses congés | hors de portée du plan ; recrutement ou plan 2027 à arbitrer par un humain |
