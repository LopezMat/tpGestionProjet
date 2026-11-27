---
titre: Planning — ESN (projet interne) : plan de formation initial
statut: VALIDÉ
responsable: agent:chef-de-projet
version: 1.0
maj_le: 2026-11-27
valide_par: Ethan
decision: DEC-024
---
<!-- modèle : templates/planning.md v0.1 · responsable du modèle : A -->

# Planning — ESN (projet interne) : plan de formation initial

> Le Gantt détaillé est **généré** dans `TABLEAU.md` à partir des tickets. Ce document fixe les jalons et les hypothèses. Il tient aussi le **registre des compétences à risque** de l'ESN (S1-R13) et, en attendant [T-018](tickets/T-018-suivi-frais-externes.md), le **suivi de l'enveloppe de frais externes**.

Sources : `equipe/membres/*.md`, `equipe/agents.md` (référentiel, hors périmètre agents), `equipe/calendrier.md` (EV-001 à EV-004), [DEC-009](../../docs/decisions/2026-11-24-DEC-009-budget-delais-coworking.md) point E, [DEC-019](../../docs/decisions/2026-11-26-DEC-019-simulation-reconstruction-base.md), [DEC-020](../../docs/decisions/2026-11-26-DEC-020-simulation-budget-4200.md), [DEC-021](../../docs/decisions/2026-11-26-DEC-021-simulation-absence-lea-depart-hugo.md), [DEC-023](../../docs/decisions/2026-11-26-DEC-023-imputation-esn-plan-formation.md), [DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) ; `reservation-coworking` : `planning.md` v1.1, `TABLEAU.md` du 2026-11-27, T-103. Version 0.1 rédigée par [T-001](tickets/T-001-plan-de-formation-initial.md) ; version 0.2 par le ticket de pilotage [T-016](tickets/T-016-pilotage.md).

## Décision retenue : option B (DEC-024)
**Le plan est décidé** par [DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (Ethan, 2026-11-27, ticket [T-017](tickets/T-017-decision-plan-formation-initial.md)) : **option B, plan sans juridique**. Formations retenues : T-002 à T-014. `budget_eur` : **4 360 €** ; `deadline` : **2027-01-15** ; enveloppe de frais externes **séparée** de 700 € HT ; allocations P1 et P2 ci-dessous. Le coordinateur a appliqué `projet.md` et les allocations de P1 le 2026-11-27 ; celles de P2 seront appliquées le 2026-12-21.

Options écartées (détail chiffré dans T-017 § 3, rappel dans DEC-024) :

| Option | Contenu | `budget_eur` | Pourquoi elle est écartée (DEC-024, « Pourquoi ») |
|---|---|---|---|
| A · Plan complet | T-002 à T-015 | 5 020 € | 1 250 € de plus (temps et frais) pour un niveau `juridique` débutant, sur un besoin rare qu'un conseil externe au cas par cas couvre mieux. T-015 est passé `ANNULE` le 2026-11-27. |
| C · Plan resserré | T-002 à T-005, T-008, T-009, T-012 | 2 850 € | Laisse Claire seule en recette et en relation client, et Nadia seule en Docker : des points uniques de défaillance que la crise simulée a montrés dangereux. |
| D · Plan minimal | T-002, T-003 | 1 170 € | Pas de second relecteur sécurité pendant les congés de Karim, Nadia seule à savoir restaurer, `documentation` orpheline. |

## Registre des compétences à risque
Critères de S1-R13 : **compétence absente**, **un seul titulaire au niveau `confirme` ou plus**, **titulaire sur le départ**. Le registre retient les compétences pour lesquelles un humain est exigé (hors périmètre agents, revue humaine AF3, binôme AF5, recette, contact client) ou qu'aucun agent ne couvre. Les compétences couvertes par un agent et jamais soumises à une revue humaine sont regroupées à la fin.

État au 2026-11-27 (Hugo compté jusqu'au 2026-12-04, EV-004).

| # | Compétence | Titulaires `confirme`+ | Agents | Critère | Gravité | Déclencheur | Traitement (option B, DEC-024) |
|---|---|---|---|---|---|---|---|
| R-01 | `documentation` | Hugo (confirmé), **part le 2026-12-04** | aucun | titulaire sur le départ, puis absente | haute | EV-004, DEC-021 | [T-012](tickets/T-012-formation-documentation-nadia.md) : Nadia, autoformation et livrable mis à l'épreuve par T-008 et T-010 |
| R-02 | `securite-applicative` (second relecteur) | Karim seul (confirmé) ; candidat de l'ex-T-053 (Hugo) part | `securite`, `architecte` | un seul titulaire ; Karim en congés du 2026-12-21 au 31 (EV-003) | **critique** | DEC-021, ex-`reservation-coworking/T-053` | [T-003](tickets/T-003-formation-securite-autoformation-lea.md) puis [T-004](tickets/T-004-formation-revue-humaine-lea.md) : Léa ; encadrement de Karim [T-005](tickets/T-005-encadrement-revue-securite-karim.md) |
| R-03 | revue humaine (`revue-humaine`, AF3, AF5) des tickets backend et sécurité, et des travaux de Nadia | Karim seul | hors périmètre agents | un seul titulaire | **critique** | DEC-021 ; `reservation-coworking/T-030` à `T-038`, `T-095` à `T-100` | T-004 (Léa, revues en double avec Karim). **Reste** : binôme AF5 d'un ticket `critique` `backend-python`, voir R-12 |
| R-04 | `sauvegarde-restauration` | Nadia seule (confirmée) | `deployeur`, `gestionnaire-crise` | un seul titulaire ; Nadia ne travaille pas le mercredi | **critique** | DEC-019 (crise T-080, « une règle sans preuve d'exécution n'est pas une garantie »), DEC-009 E | [T-008](tickets/T-008-formation-sauvegarde-restauration-karim.md) : Karim (expert `base-de-donnees-sql`) ; encadrement de Nadia [T-009](tickets/T-009-encadrement-sauvegarde-nadia.md) |
| R-05 | `docker` | Nadia seule (confirmée) | **aucun** | un seul titulaire ; toute la production est en Docker local (DEC-003) | haute | DEC-019, DEC-021 | [T-010](tickets/T-010-formation-docker-lea.md) : Léa ; encadrement de Nadia [T-011](tickets/T-011-encadrement-docker-nadia.md) |
| R-06 | `recette-fonctionnelle` | Claire seule (confirmée) | `testeur` (ne remplace pas la recette humaine, R16) | un seul titulaire ; un empêchement bloque le GO | haute | DEC-009 E ; `reservation-coworking/T-045` | [T-006](tickets/T-006-formation-recette-lea.md) : Léa, en binôme pendant T-045 ; encadrement de Claire [T-007](tickets/T-007-encadrement-recette-claire.md) |
| R-07 | `relation-client` | Claire seule (experte) | hors périmètre agents | un seul titulaire ; nécessaire aussi pour une recette avec le client (AF1) | moyenne | DEC-009 E | [T-013](tickets/T-013-formation-relation-client-lea.md) : Léa, en binôme ; encadrement de Claire [T-014](tickets/T-014-encadrement-relation-client-claire.md) |
| R-08 | `juridique` | **aucun** | hors périmètre agents | absente | moyenne | DEC-009 E ; `reservation-coworking/T-084` (CNIL, tranché sans avis juridique, DEC-019 v0.2) | **Risque accepté par DEC-024** : pas de formation ; **conseil juridique externe saisi au cas par cas, sur décision humaine** (comme pour T-084). [T-015](tickets/T-015-formation-juridique-claire.md) `ANNULE` le 2026-11-27. À revoir au retex de `reservation-coworking` ou si les besoins juridiques deviennent fréquents |
| R-09 | `supervision` | **aucun** au niveau confirmé (Nadia débutante) | `analyste-prod` | absente au niveau `confirme` | moyenne | EV-002 (2026-12-03), DEC-009 E | [T-002](tickets/T-002-formation-supervision-nadia.md) : Nadia, formation externe du 2026-12-03 (frais dans l'enveloppe séparée) |
| R-10 | `rgpd` | Claire seule (confirmée) | aucun | un seul titulaire | moyenne | `reservation-coworking` F-08 (CDC § 8) | non traité dans ce plan ; à revoir au retex de `reservation-coworking` |
| R-11 | `html-css`, `javascript`, `react`, `accessibilite` (revue humaine des tickets frontend critiques) | Léa seule | `dev-frontend` | un seul titulaire | faible | aucun ticket frontend critique en cours | non traité ; à surveiller au prochain projet avec un front critique |
| R-12 | `backend-python`, `base-de-donnees-sql`, `architecture-logicielle`, `revue-code` (binôme AF5 des tickets `critique` backend) | Karim seul (expert) | `dev-backend`, `architecte`, `relecteur-code` | un seul titulaire ; Karim en congés du 21 au 31/12 | haute | DEC-021 | **hors de portée d'un plan de quelques semaines** (montée à `confirme` en `backend-python` : plusieurs mois) ; recrutement ou plan 2027, **à décider à part** (DEC-024, « Restent ouverts »). T-008 donne une seconde personne sur la base de données côté restauration |
| R-13 | `ci-cd`, `linux` | Nadia seule | `deployeur` (`ci-cd`) ; aucun pour `linux` | un seul titulaire | moyenne | — | réduit en partie par T-010 et T-008 ; non traité en propre |
| R-14 | `tests-e2e` | **aucun** au niveau confirmé (Léa débutante) | `testeur` | absente au niveau `confirme` ; obligatoire en e-commerce | faible aujourd'hui | fiche de Léa (AF7, AF10 c) | aucun ticket tant qu'aucun projet e-commerce n'est signé (pas de ticket artificiel) |
| R-15 | `paiement-en-ligne`, `tests-utilisateurs` | **aucun** | hors périmètre agents | absentes | faible aujourd'hui | aucun projet ne les demande | à traiter au premier projet e-commerce ou avec tests utilisateurs (AF4 : ticket `formation` ou recrutement) |
| R-16 | `porter-une-decision`, `revue-humaine` (données) | aucune fiche ne les déclare | hors périmètre agents | donnée absente des fiches | faible | AF2, AF3 | Claire porte les décisions et Karim fait les revues de fait : AF2 et AF3 ne sont pas vérifiables par `tableau.py`. Mise à jour des fiches **à décider à part** (DEC-024, « Restent ouverts ») |
| R-17 | ex-`reservation-coworking/T-052` (`backend-python`, Hugo) | — | — | besoin éteint (départ) | — | DEC-021 | retiré du plan |

**Couvertes par les agents, risque faible** (pas de revue humaine spécifique, aucun ticket) : `recueil-besoin`, `gestion-projet` (Claire seule, plus `analyste-besoin` et `chef-de-projet`), `tests-unitaires` (plus aucun salarié après Hugo ; `dev-backend`, `dev-frontend`, `testeur`), `redaction-cdc`, `analyse-existant`, `estimation`, `planification`, `suivi-budget`, `choix-stack`, `api-rest`, `deploiement-render`, `audit-dependances`, `analyse-logs`, `veille-technologique`, `support-utilisateur`, `gestion-de-crise` (la communication de crise relève de `relation-client`, R-07).

**Constat transverse.** Trois personnes concentrent les risques critiques : Karim (R-02, R-03, R-12), Nadia (R-04, R-05, R-13) et Claire (R-06, R-07, R-10). Léa, qui n'était allouée à aucun projet, est désormais allouée à `esn-interne` (25 % en P1, 10 % en P2, DEC-024) : le plan la rend seconde sur plusieurs compétences. C'est un risque de concentration connu (voir « Risques planning »), qui reste préférable à une personne unique par compétence.

## Plan retenu (option B, DEC-024)
| Rang DEC-024 | Besoin | Ticket(s) | Candidat | Modalité | Fenêtre | Niveau visé à la fin | h salarié | h formateur | Coût temps (€) | Frais externes (€ HT) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | second relecteur `securite-applicative`, revue humaine | T-003, T-004, T-005 | Léa (formateur : Karim) | autoformation guidée, puis revues humaines en double avec Karim | 2026-11-30 → 2026-12-11 ; attestation **avant le 2026-12-18** | `securite-applicative` et `revue-humaine` confirmées | 11 | 2 | 707,14 + 157,14 = 864,29 | 0 |
| 2 | `sauvegarde-restauration` | T-008, T-009 | Karim (formatrice : Nadia) | binôme interne : restauration réelle dans une base jetable, en suivant le runbook | 2027-01-04 → 2027-01-13 | confirmé | 5 | 2 | 392,86 + 128,57 = 521,43 | 0 |
| 3 | `supervision` | T-002 | Nadia | formation externe d'une journée (EV-002) | **2026-12-03** | confirmée | 7 | — | 450,00 | enveloppe séparée de 700 (sur devis) |
| 4 | `documentation` | T-012 | Nadia | autoformation et livrable (guide d'exploitation Docker et restauration), mis à l'épreuve par T-008 et T-010 | 2026-12-21 → **2026-12-30 au plus tard** | confirmée | 7 | — | 450,00 | 0 |
| 5 | `recette-fonctionnelle` | T-006, T-007 | Léa (formatrice : Claire) | binôme interne pendant la recette `reservation-coworking/T-045` | 2026-12-10 → 2026-12-15 ; **au plus tard le 2026-12-18** | confirmée | 4 | 1 | 257,14 + 78,57 = 335,71 | 0 |
| 6 | `docker` | T-010, T-011 | Léa (formatrice : Nadia) | autoformation et binôme interne, à partir du guide T-012 | 2026-12-30 → 2027-01-14 | débutante (autonome sur les procédures écrites) | 7 | 3 | 450,00 + 192,86 = 642,86 | 0 |
| 7 | `relation-client` | T-013, T-014 | Léa (formatrice : Claire) | binôme interne sur les échanges client de fin de projet | 2026-11-30 → **2026-12-18 au plus tard** | débutante | 3 | 1 | 192,86 + 78,57 = 271,43 | 0 |

**Ordre de priorité (DEC-024, point 5)** : risque d'abord, puis fenêtre. 1. T-003, T-004, T-005 (sécurité et revue humaine) ; 2. T-008, T-009 (sauvegarde-restauration) ; 3. T-002 (supervision, date fixe) ; 4. T-012 (documentation) ; 5. T-006, T-007 (recette) ; 6. T-010, T-011 (docker) ; 7. T-013, T-014 (relation client). **En cas de manque de capacité, on retire dans l'ordre inverse**, en commençant par le rang 7. Les rangs 1 à 4 portent `priorite: haute`, les rangs 5 à 7 `priorite: normale`.

**`reservation-coworking` garde la priorité** (DEC-024, point 6) : un binôme peut être suspendu sans délai si le chemin critique du GO l'exige. Aucun ticket du projet client n'est modifié, et aucun coût n'est imputé au client.

## Jalons
| Jalon | Date cible | Tickets inclus | Critère de passage |
|---|---|---|---|
| Plan de formation décidé | **2026-11-27** (fait) | T-017 | DEC-024 `VALIDÉ` ; `projet.md` et allocations de P1 appliqués par le coordinateur. **T-017 à conclure (`TERMINE`) par le coordinateur avant le 2026-12-03**, sans quoi T-002 n'est pas prenable (`depend_de: T-017`) |
| Sécurité : autoformation de Léa | 2026-11-30 → 2026-12-04 | T-003 | grille de relecture d'une page relue par Karim |
| Supervision de Nadia | **2026-12-03** (date fixe, EV-002) | T-002 | attestation de présence ; restitution écrite au journal ; `debut_le` et `termine_le` au 2026-12-03 ; frais reportés dans l'enveloppe |
| Revues humaines en double | 2026-12-07 → 2026-12-11 | T-004, T-005 | au moins 3 revues en double ; attestation de Karim ; **avant le 2026-12-18** (congés de Karim) |
| Recette en binôme | 2026-12-10 → 2026-12-15 | T-006, T-007 | Léa a déroulé au moins 2 parcours du rapport de recette de T-045 ; attestation de Claire |
| Relation client en binôme | 2026-11-30 → 2026-12-18 | T-013, T-014 | au moins 2 échanges client suivis avec Claire ; débriefing |
| **Fin de P1** | **2026-12-18** | T-002 à T-007, T-013, T-014 | tous `TERMINE`. Claire passe à 0 % en P2 : T-007 et T-014 ouverts après cette date deviennent non planifiables |
| **Bascule des allocations P1 → P2** | **2026-12-21** | — | le coordinateur applique les allocations de P2 dans `equipe/` (signalé par T-016) et relance `tableau.py` ; les alertes analysées plus bas doivent disparaître, et la fin projetée doit être au plus tard le 2027-01-14 |
| Documentation | 2026-12-21 → **2026-12-30 au plus tard** | T-012 | guide d'exploitation publié dans `projets/esn-interne/` ; **chemin critique du plan** |
| Sauvegarde-restauration | 2027-01-04 → 2027-01-13 | T-008, T-009 | Karim restaure seul, en suivant le runbook, dans une base jetable ; durée mesurée |
| Docker | 2026-12-30 → 2027-01-14 | T-010, T-011 | Léa monte seule un environnement de recette à partir du guide |
| **Fin du plan** | **2027-01-15** | tous | tickets `TERMINE` ; niveaux atteints proposés ; mise à jour des fiches par le coordinateur après décision humaine |

Dates en heures équivalent humain et en jours ouvrés (S1-R9). Le 2026-12-25 et le 2027-01-01 sont fériés.

## Hypothèses de capacité
**Périodes.** P1 : du 2026-11-30 au 2026-12-18 (15 jours ouvrés, fin de `reservation-coworking`). P2 : du 2026-12-21 au 2027-01-15 (18 jours ouvrés).

| Ressource | Type | Allocation à `esn-interne` décidée par DEC-024 (P1 / P2) | h/semaine disponibles (P1 / P2) | Taux €/h |
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
| Claire | P1 | 0,35 | 15 | 5,25 h | 2 h (T-007, T-014) | **38,1 %**, sous 50 % (accepté par DEC-024) |
| Karim | P1 | 0,35 | 15 | 5,25 h | 2 h (T-005) | **38,1 %**, sous 50 % (accepté par DEC-024) |
| Karim | P2 | 0,70 | 10 (congés du 21 au 31/12) | 7,0 h | 5 h (T-008) | 71,4 % |
| Léa | P1 | 1,75 | 15 (retour le 2026-11-30) | 26,25 h | 18 h (T-003, T-004, T-006, T-013) | 68,6 % |
| Léa | P2 | 0,70 | 18 | 12,6 h | 7 h (T-010) | 55,6 % |
| Nadia | P1 | 0,56 | 14 (EV-002 compté à 0 par `tableau.py`) | 7,84 h | 7 h (T-002) | 89,3 % |
| Nadia | P2 | 1,12 | 18 | 20,16 h | 12 h (T-012, T-011, T-009) | 59,5 % |

- **AF9, sous 50 %** : Claire et Karim en P1 (38,1 %). Le besoin réel est de 2 h chacun ; 5 % est la plus petite allocation qui laisse le binôme se faire dans sa fenêtre. DEC-024 a retenu 5 % en connaissance de cause. Aucun ticket n'est ajouté pour atteindre un taux.
- **Léa** : 75 % à 90 % de sa capacité ne sont alloués à aucun projet. C'est une question d'activité commerciale de l'ESN, hors de ce plan, déjà signalée au coordinateur. C'est aussi un levier sans coût si T-010 glisse (voir « Risques planning »).
- **Nadia, semaine du 2026-12-03** : 14 h sur `reservation-coworking` et 7 h de formation, soit 21 h sur 28 h. La charge tient.

**Limites du calcul de `tableau.py`** (origine des alertes analysées ci-dessous) :
- l'allocation est une seule valeur par projet : tant que le coordinateur n'a pas appliqué P2 (le 2026-12-21), `tableau.py` calcule **toute la durée du plan avec les allocations de P1** ;
- EV-002 met la capacité de Nadia à 0 le 2026-12-03, pour tous les projets : `tableau.py` étale donc T-002 sur d'autres jours. EV-002 est conservé (DEC-024), car sa capacité nulle est juste pour `reservation-coworking` ;
- l'ordonnancement place les tickets d'un même assigné l'un après l'autre, par priorité puis par id : il ne connaît pas les fenêtres (par exemple, T-013 est placé après T-010) ;
- les frais externes ne sont pas comptés (il ne chiffre que des heures) : ils sont suivis dans la section « Enveloppe de frais externes ».

## Analyse des alertes de `TABLEAU.md` (2026-11-27)
`tableau.py` relancé le 2026-11-27 après le passage de T-015 en `ANNULE` : **5 alertes**. Les 4 alertes signalées par le coordinateur sont toujours là, et une cinquième (Claire) est apparue, parce que T-015 (7 h de Claire) ne compte plus.

| # | Alerte | Cause | Artefact ou vrai risque | Ce qui la fait disparaître |
|---|---|---|---|---|
| 1 | **Délais** : fin projetée le 2027-01-26, +7 j ouvrés après la deadline | T-008 (Karim, 5 h) est calculé à **5 %** (0,35 h/jour, soit 14 jours ouvrés) au lieu de 10 % en P2. Il attend T-012, calculé à **10 %** de Nadia (0,56 h/jour) au lieu de 20 %, et lui-même retardé par T-002 étalé jusqu'au 2026-12-16 | **Artefact de l'allocation unique.** Avec les allocations de P2, la fin projetée est le **2027-01-14** (voir la projection ci-dessous). Le **vrai risque** qui reste, c'est une marge d'un seul jour ouvré sur la chaîne T-012 → T-010 | La bascule P2 du 2026-12-21. Le passage de T-002 `TERMINE` le 2026-12-03 avance aussi la projection, mais il ne suffit pas : à 5 %, T-008 finit encore vers le 2027-01-22 |
| 2 | **Absence (S1-R9)** : la fenêtre de T-002 (2026-11-27 → 2026-12-16) chevauche EV-002 | EV-002 **est** la journée de formation de T-002. Le calendrier met Nadia à 0 ce jour-là pour tous les projets, et `tableau.py` étale donc les 7 h à 0,56 h/jour sur les autres jours | **Artefact.** Aucun conflit réel : le 2026-12-03, Nadia est absente de `reservation-coworking` et présente à la formation | Nadia passe T-002 `EN_COURS` puis `TERMINE`, avec `debut_le` et `termine_le` au **2026-12-03** (le Gantt utilise alors ces dates). Il ne faut ni annuler EV-002 ni changer le calendrier |
| 3 | **Utilisation (info)** : Léa à 43,3 % | 25 h sur 57,8 h de capacité, calculée à 25 % sur toute la période, alors qu'elle passe à 10 % en P2 | **Artefact.** Avec P1 et P2 : 25 h sur 38,85 h, soit **64,4 %** (68,6 % en P1, 55,6 % en P2) | La bascule P2 : au 2026-12-21, il reste 7 h (T-010) sur 12,6 h, soit 55,6 %. D'ici là, rien à corriger : c'est un indicateur, et on n'ajoute aucun ticket pour atteindre un taux (AF9) |
| 4 | **Surcharge** : Nadia à 102,8 % (19 h pour 18,5 h) | La capacité est calculée à 10 % sur toute la période, et EV-002 est compté à 0 | **Artefact.** Avec P1 et P2 : 19 h sur 28,56 h (8,4 h en P1, 20,16 h en P2), soit **66,5 %** (P1 89,3 %, P2 59,5 %). Pas de surcharge | La bascule P2 : au 2026-12-21, il reste 12 h (T-012, T-009, T-011) sur 20,16 h, soit 59,5 % |
| 5 | **Utilisation (info)** : Claire à 16,8 % (nouvelle) | 2 h sur 11,9 h, calculée à 5 % sur toute la période, alors qu'elle passe à 0 % en P2 | **Indicateur déjà arbitré** : 38,1 % en P1 réel, signalé dans T-017 et accepté par DEC-024 (5 % pour tenir la fenêtre). **Vrai risque** si T-007 ou T-014 ne sont pas `TERMINE` le 2026-12-18 : à 0 % en P2, ils deviendraient non planifiables | T-007 et T-014 `TERMINE` au plus tard le 2026-12-18. Après la bascule, Claire n'a plus ni allocation ni ticket ouvert à `esn-interne` et sort du tableau |

**Projection avec les allocations de P2** (calcul à la main, selon les formules d'ARCHITECTURE § 7 et la méthode de `tableau.py` : capacité hebdomadaire ÷ 5 × allocation, un ticket à la fois par assigné). Hypothèses : les tickets de P1 sont `TERMINE` le 2026-12-18, T-002 compris (2026-12-03), et T-012 commence le 2026-12-21.

| Ticket | Assigné | h | h/jour (P2) | Début | Fin projetée |
|---|---|---|---|---|---|
| T-012 | Nadia | 7 | 1,12 | 2026-12-21 | **2026-12-30** |
| T-009 | Nadia | 2 | 1,12 | 2026-12-30 | 2027-01-04 |
| T-011 | Nadia | 3 | 1,12 | 2027-01-04 | 2027-01-06 (en réalité avec la partie binôme de T-010, jusqu'au 2027-01-14) |
| T-008 | Karim | 5 | 0,70 (0 du 21 au 31/12, EV-003) | 2027-01-04 | **2027-01-13** |
| T-010 | Léa | 7 | 0,70 | 2026-12-30 | **2027-01-14** |
| **Fin projetée** | | | | | **2027-01-14**, 1 jour ouvré avant la deadline |

- **La fin projetée tient avant le 2027-01-15**, et **Nadia ne dépasse pas sa capacité** (59,5 % en P2). Aucune alerte S1-R11 réelle, donc **aucun ticket `decision` d'alerte n'est créé**. Si, après la bascule du 2026-12-21, `tableau.py` projette toujours une fin après le 2027-01-15, T-016 en crée un, avec au moins 2 scénarios chiffrés (règle 9).
- **Chemin critique du plan : T-012 → T-010.** Pour que T-010 finisse au plus tard le 2027-01-14, T-012 doit être `TERMINE` **au plus tard le 2026-12-30** ; le 2026-12-31 est la limite absolue, et ne laisse plus aucune marge. T-008 a un peu plus de jeu : Karim n'est disponible qu'à partir du 2027-01-04.
- Les heures et le coût ne changent pas d'une hypothèse à l'autre : seules les dates bougent.
- **Jusqu'au 2026-12-21, les alertes 1, 3 et 4 resteront dans `TABLEAU.md`.** Le suivi hebdomadaire (T-016) les compare à cette projection plutôt qu'au tableau, et signale tout écart.

## Charge et budget prévisionnels
*Taux (ARCHITECTURE § 8) : agent 15 €/h ; Claire et Karim 550 €/j ÷ 7 = 78,57 €/h ; Léa et Nadia 450 €/j ÷ 7 = 64,29 €/h.*

**Option B (retenue)**, coût projeté par `tableau.py` le 2026-11-27 :

| Ressource | Tickets | h | € |
|---|---|---|---|
| Léa | T-003, T-004, T-006, T-010, T-013 | 25,0 | 1 607,14 |
| Nadia | T-002, T-009, T-011, T-012 | 19,0 | 1 221,43 |
| Karim | T-005, T-008 | 7,0 | 550,00 |
| Claire | T-007, T-014 | 2,0 | 157,14 |
| agent:chef-de-projet | T-001 (3 h passées), T-016 (pilotage, 3 h), T-017 (0,5 h), T-018 (amélioration, 1,5 h, créé après DEC-024) | 8,0 | 120,00 |
| **Total temps** | | **61,0** | **3 655,71** |

- **Écart avec DEC-024** : +22,50 €, soit T-018 (1,5 h d'agent), créé par le coordinateur à la demande d'Ethan après le chiffrage de T-017. Il est couvert par la marge.
- **T-015 `ANNULE`** : 0 h passée, donc 0 € consommé.
- **Budget de fonctionnement (`budget_eur`)** : **4 360 €** (DEC-024). Coût projeté : 3 655,71 €, soit **83,8 %**. Marge restante : **704,29 €**.
- **Consommé au 2026-11-27** : 60,00 € (T-001 : 45,00 € ; T-016 : 15,00 €), soit 1,4 %.
- **Seuil d'alerte S1-R11** : 90 % de 4 360 €, soit **3 924 €** consommés. Le coût projeté reste en dessous, avec 268,29 € de réserve.
- **Marge** : elle couvre le rythme des autoformations (aucun historique dans l'ESN), une séance de binôme à refaire si un ticket client glisse, et les analyses d'événements d'équipe imputées à ce projet (CLAUDE.md § 5, environ 7,50 à 15 € chacune).
- **Échéance (`deadline`)** : **2027-01-15**.

## Enveloppe de frais externes
**Montant : 700 € HT**, hors `budget_eur` ([DEC-024](../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md), point 4), pour la formation « supervision » de Nadia ([T-002](tickets/T-002-formation-supervision-nadia.md), 2026-12-03), **engagée sur devis**. `tableau.py` ne suit pas ces frais : ce suivi manuel tient lieu de critère 3 de [T-018](tickets/T-018-suivi-frais-externes.md), en attendant sa proposition et la décision qui la suivra.

**Règles du suivi** :
- **Toute dépense au-delà de l'enveloppe passe par une nouvelle décision humaine** (DEC-024), prise **avant** l'engagement : un devis supérieur au reste de l'enveloppe donne lieu à un ticket `decision` `ATTENTE_HUMAIN`, avant toute commande.
- **Aucun engagement sans devis.** On appelle « engagé » un devis accepté ou une commande passée, et « facturé » une facture reçue.
- **Reste de l'enveloppe** = 700 € − le plus élevé des deux montants, engagé ou facturé, cumulé sur toutes les lignes.
- **Une ligne par mouvement** (devis reçu, engagement, facture), avec une ligne de journal dans le ticket concerné. Le `chef-de-projet` (T-016) tient ce tableau à partir des informations transmises par le coordinateur ; il donne le reste de l'enveloppe dans chaque état hebdomadaire.
- **Pas de pièce dans le dépôt** si elle contient des données personnelles ou bancaires : on n'écrit ici que le montant, la date et une référence (S3-R8).
- Une dépense externe qui ne concerne pas T-002, comme un conseil juridique au cas par cas (R-08), **n'entre pas dans cette enveloppe** : elle demande sa propre décision humaine.

| Date | Ticket | Objet | Devis (€ HT) | Engagé (€ HT) | Facturé (€ HT) | Reste de l'enveloppe (€ HT) | Qui | Référence |
|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | T-002 | Ouverture de l'enveloppe : formation « supervision » de Nadia, 2026-12-03. **Devis à obtenir avant le 2026-12-03** | à obtenir | 0 | 0 | **700** | agent:chef-de-projet (report de DEC-024) | DEC-024 point 4 |

## Risques planning
| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| **T-012 en retard** (chemin critique du plan) | moyenne | T-010 finit après le 2027-01-15 si T-012 n'est pas `TERMINE` le 2026-12-31 ; T-008 suit de près | T-012 en `priorite: haute`, dès le 2026-12-21. Leviers, dans l'ordre : (1) Nadia avance l'autoformation de T-012 (2 h) sur le reliquat de P1 (8,4 h allouées, 7 h pour T-002, soit 1,4 h de reste), **sans coût** ; (2) **proposition, sur décision humaine** : passer Léa de 10 % à 15 % en P2 (mêmes heures, même coût ; T-010 gagne environ 3 jours ouvrés), et Karim de 10 % à 15 % (total 35 % au plus) ; (3) DEC-024, point 5 : reporter T-010 et T-011 (rang 6) après l'échéance. Un ticket `decision` est créé si la projection du 2026-12-21 dépasse le 2027-01-15 |
| T-017 non conclu avant le 2026-12-03 | faible | T-002 n'est pas prenable le jour de la formation (`depend_de: T-017`) | coordinateur : passer T-017 `TERMINE` dès l'application de DEC-024 (critère 3 rempli par T-016 le 2026-11-27) |
| Tickets de P1 non terminés le 2026-12-18 (T-006, T-007, T-013, T-014) | moyenne | Claire passe à 0 % en P2 : T-007 et T-014 deviennent non planifiables. Les fenêtres de T-006 (recette T-045) et de T-013 (fin de `reservation-coworking`) se ferment | suivi hebdomadaire ; au 2026-12-16, si l'un d'eux reste ouvert : ticket `decision` (prolonger Claire à 5 % quelques jours en P2, ou reporter ou annuler T-013 et T-014, rang 7, dans l'ordre inverse de DEC-024) |
| Alertes « artefacts » de `TABLEAU.md` jusqu'au 2026-12-21 | certaine | lecture erronée du tableau (fausse alerte de délai, fausse surcharge de Nadia) | analyse ci-dessus ; chaque état hebdomadaire de T-016 compare à la projection P1/P2. Amélioration de `tableau.py` (allocation par période, absence pour formation rattachée à un ticket) à proposer au coordinateur par un ticket `amelioration` (R11) |
| Les binômes gênent le chemin critique de `reservation-coworking` (recette T-045, revues de Karim T-037, T-097 à T-099, GO du 2026-12-15) | moyenne | retard du GO : marge de 2 jours ouvrés seulement | Léa observe et ne signe rien ; Claire et Karim restent seuls responsables de la recette et des revues ; le formateur peut suspendre le binôme sans délai (DEC-024, point 6) ; temps d'explication compté à part (T-005, T-007) |
| Karim n'atteint pas l'attestation de Léa avant le 2026-12-18 | moyenne | pas de second relecteur pendant ses congés (21 au 31/12) | rang 1 ; T-003 dès le 2026-11-30 ; sinon, poursuite en janvier, et aucun ticket sécurité livré pendant les congés sans revue reportée |
| Karim n'est que `confirme` en `securite-applicative` | certaine | le binôme « sous le niveau avec un expert » (AF7) n'est pas possible : Léa ne relit seule qu'une fois `confirme` | jusqu'à l'attestation, Karim signe seul les revues ; l'attestation est une décision humaine |
| Concentration sur Léa (seconde sur 5 compétences) | moyenne | une absence de Léa rouvre plusieurs risques à la fois | elle reste « seconde » : chaque compétence garde son titulaire ; à revoir au retex |
| Congés de fin d'année non déclarés (Claire, Léa, Nadia) | moyenne | P2 décalée, sur une marge d'un jour ouvré seulement | à confirmer par le coordinateur (DEC-024, « Points à confirmer ») ; un congé de Nadia avant le 2026-12-30 ou de Léa en janvier déclenche le levier (2) de T-012, ou un report de rang 6 |
| Frais externes de la supervision inconnus | moyenne | devis supérieur à l'enveloppe de 700 € HT | devis à obtenir avant le 2026-12-03 ; au-delà de l'enveloppe, nouvelle décision humaine **avant** l'engagement |
| `juridique` absente (R-08), risque accepté par DEC-024 | faible | une question juridique (contrat, RGPD du sous-traitant, violation de données) sans compétence interne | conseil juridique externe, saisi au cas par cas sur décision humaine ; frais hors de l'enveloppe de T-002 ; à revoir au retex |
| Niveaux visés surestimés (`docker` et `relation-client` à `debutant` seulement) | moyenne | R-05 et R-07 restent ouverts au niveau `confirme` | réévaluation au retex ; un binôme sur un projet réel au prochain contrat |
| `backend-python` et le binôme AF5 restent chez Karim seul (R-12) | certaine | aucun ticket `critique` backend ne peut être piloté pendant ses congés | hors de portée du plan ; recrutement ou plan 2027, à arbitrer à part par un humain (DEC-024) |
