---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-017
titre: Plan de formation initial — budget de fonctionnement, échéance et allocations (DEC-024)
projet: esn-interne
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_COURS      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine sur le plan de formation initial de l'ESN (formations retenues, budget de fonctionnement, échéance, allocations à esn-interne), DEC-024   # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:       DEC-024            # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-017 — Plan de formation initial — budget de fonctionnement, échéance et allocations (DEC-024)

## Description
Ticket `decision` du plan de formation de l'ESN (S1-R13, règle 16 du `chef-de-projet`), préparé par [T-001](T-001-plan-de-formation-initial.md). **Décision attendue : DEC-024.** Le détail (registre des compétences à risque, jalons, contrôle de capacité) est dans [planning.md](../planning.md) v0.1 (`EN_REVUE`).

**Assignation.** Le ticket reste assigné au `chef-de-projet`, auteur de l'analyse (exception d'AF2). Claire, qui porte d'ordinaire les décisions, n'a pas d'allocation à `esn-interne` avant cette décision. La validation formelle est humaine (R5).

**Taux** (ARCHITECTURE § 8) : Claire et Karim 78,57 €/h ; Léa et Nadia 64,29 €/h ; agent 15 €/h. Tous les montants sont en heures équivalent humain × taux (R12), calculés comme `tableau.py`. Les frais externes, que `tableau.py` ne compte pas, sont à part.

**Périodes** : P1 du 2026-11-30 au 2026-12-18 ; P2 du 2026-12-21 au 2027-01-15. Allocations sur `reservation-coworking` prises en compte : Claire 20 %, Karim 20 %, Nadia 50 % jusqu'au 2026-12-18 puis 5 % (DEC-019, DEC-020, planning v1.1), Léa 0 %.

### 1. Question
Quel plan de formation initial l'ESN retient-elle, avec quel **budget de fonctionnement** (`budget_eur`), quelle **échéance** (`deadline`) et quelles **allocations à `esn-interne`** pour Claire, Karim, Léa et Nadia (Hugo exclu, départ le 2026-12-04) ? Dans quel **ordre de priorité** ?

### 2. Tickets proposés
| Ticket | Besoin (registre) | Candidat | Modalité | h | Coût temps (€) | Frais externes (€ HT) | Déclencheur |
|---|---|---|---|---|---|---|---|
| T-002 | `supervision` → confirmée (R-09) | Nadia | formation externe, 2026-12-03 | 7 | 450,00 | provision 700 | EV-002, DEC-009 E |
| T-003 | `securite-applicative` → débutante (R-02) | Léa | autoformation guidée | 7 | 450,00 | 0 | DEC-021, ex-`reservation-coworking/T-053` |
| T-004 | `revue-humaine` et `securite-applicative` → confirmée (R-02, R-03) | Léa | binôme : 3 revues en double avec Karim | 4 | 257,14 | 0 | DEC-021 |
| T-005 | encadrement de T-003 et T-004 | Karim (formateur) | — | 2 | 157,14 | 0 | — |
| T-006 | `recette-fonctionnelle` → confirmée (R-06) | Léa | binôme pendant `reservation-coworking/T-045` | 4 | 257,14 | 0 | DEC-009 E |
| T-007 | encadrement de T-006 | Claire (formatrice) | — | 1 | 78,57 | 0 | — |
| T-008 | `sauvegarde-restauration` → confirmé (R-04) | Karim | binôme : restauration réelle dans une base jetable | 5 | 392,86 | 0 | DEC-019, DEC-009 E |
| T-009 | encadrement de T-008 | Nadia (formatrice) | — | 2 | 128,57 | 0 | — |
| T-010 | `docker` → débutante (R-05) | Léa | autoformation et binôme | 7 | 450,00 | 0 | DEC-019, DEC-021 |
| T-011 | encadrement de T-010 | Nadia (formatrice) | — | 3 | 192,86 | 0 | — |
| T-012 | `documentation` → confirmée (R-01) | Nadia | autoformation et livrable (guide d'exploitation) | 7 | 450,00 | 0 | DEC-021, EV-004 |
| T-013 | `relation-client` → débutante (R-07) | Léa | binôme sur les échanges client de fin de projet | 3 | 192,86 | 0 | DEC-009 E |
| T-014 | encadrement de T-013 | Claire (formatrice) | — | 1 | 78,57 | 0 | — |
| T-015 | `juridique` → débutante (R-08) | Claire | formation externe d'une journée | 7 | 550,00 | provision 700 | DEC-009 E, `reservation-coworking/T-084` |
| T-016 | pilotage (3 h, 2 h ou 1 h selon l'option) | `chef-de-projet` | — | 1 à 3 | 15,00 à 45,00 | — | règle 16 |

S'y ajoutent dans toutes les options : T-001 (3 h passées, 45,00 €) et ce ticket (0,5 h, 7,50 €). Les frais externes sont des **provisions à confirmer par devis** (0 € si une session est déjà réglée ou gratuite).

### 3. Options
**Synthèse**

| | **A · Plan complet** | **B · Plan sans juridique (recommandée)** | **C · Plan resserré sur les risques critiques** | **D · Plan minimal, report** |
|---|---|---|---|---|
| Formations incluses | toutes (T-002 à T-015) | toutes sauf T-015 | T-002, T-003, T-004, T-005, T-008, T-009, T-012 | T-002, T-003 |
| Passent `ANNULE` | aucun | T-015 | T-006, T-007, T-010, T-011, T-013, T-014, T-015 | T-004 à T-015 |
| Heures | 66,5 h | 59,5 h | 39,5 h | 18,5 h |
| **Coût temps** | **4 183,21 €** | **3 633,21 €** | **2 368,21 €** | **967,50 €** |
| Marge (20 %, arrondie à la dizaine supérieure) | 836,79 € | 726,79 € | 481,79 € | 202,50 € |
| **`budget_eur` proposé** | **5 020 €** | **4 360 €** | **2 850 €** | **1 170 €** |
| Seuil d'alerte S1-R11 (90 %) | 4 518 € | 3 924 € | 2 565 € | 1 053 € |
| Enveloppe de frais externes (hors `budget_eur`) | 1 400 € HT | 700 € HT | 700 € HT | 700 € HT |
| **`deadline` proposée** | **2027-01-15** | **2027-01-15** | **2027-01-15** | **2026-12-18** |
| `salaries_affectes` | claire, karim, lea, nadia | claire, karim, lea, nadia | karim, lea, nadia | lea, nadia |

**Pourquoi une marge de 20 %** : aucun historique de formation dans l'ESN ; le rythme d'une autoformation varie d'une personne à l'autre ; une séance de binôme peut être à refaire si un ticket client glisse (T-045, revues de Karim) ; la marge couvre aussi les analyses d'événements d'équipe imputées à ce projet (environ 7,50 à 15 € chacune, CLAUDE.md § 5). Un outil commun plus coûteux passera par une révision du budget.

**Pourquoi les frais externes sont hors `budget_eur`** : `tableau.py` ne chiffre que des heures. Si on les incluait, le consommé affiché resterait sous le budget alors que l'argent serait dépensé, et l'alerte à 90 % arriverait trop tard. Ils sont suivis dans `planning.md` et dans DEC-024.

**Coût détaillé par salarié**

| Salarié | A | B | C | D |
|---|---|---|---|---|
| Claire | 9 h · 707,14 € (T-007, T-014, T-015) | 2 h · 157,14 € (T-007, T-014) | 0 | 0 |
| Karim | 7 h · 550,00 € (T-005, T-008) | 7 h · 550,00 € | 7 h · 550,00 € | 0 |
| Léa | 25 h · 1 607,14 € (T-003, T-004, T-006, T-010, T-013) | 25 h · 1 607,14 € | 11 h · 707,14 € (T-003, T-004) | 7 h · 450,00 € (T-003) |
| Nadia | 19 h · 1 221,43 € (T-002, T-009, T-011, T-012) | 19 h · 1 221,43 € | 16 h · 1 028,57 € (T-002, T-009, T-012) | 7 h · 450,00 € (T-002) |
| `chef-de-projet` (T-001, T-016, T-017) | 6,5 h · 97,50 € | 6,5 h · 97,50 € | 5,5 h · 82,50 € | 4,5 h · 67,50 € |
| **Total** | **4 183,21 €** | **3 633,21 €** | **2 368,21 €** | **967,50 €** |
| dont temps de formateur | 9 h · 635,71 € | 9 h · 635,71 € | 4 h · 285,71 € | 0 |

*Temps de formateur.* A et B : Karim 2 h (157,14 €), Nadia 5 h (321,43 €), Claire 2 h (157,14 €) ; T-015 n'a pas de formateur. C : Karim 2 h (157,14 €) et Nadia 2 h (128,57 €). D : aucun.

**Allocations proposées à `esn-interne` et total par salarié** (`reservation-coworking` + `esn-interne`, S1-R10)

| Salarié | Option | `esn-interne` P1 | Total P1 | `esn-interne` P2 | Total P2 |
|---|---|---|---|---|---|
| Claire | A | 5 % | 25 % | 10 % | 30 % (20 % si `reservation-coworking` passe à 10 % après le GO) |
| Claire | B | 5 % | 25 % | 0 % | 20 % |
| Claire | C, D | 0 % | 20 % | 0 % | 20 % |
| Karim | A, B, C | 5 % | 25 % | 10 % (congés du 21 au 31/12) | 30 % au plus |
| Karim | D | 0 % | 20 % | 0 % | 20 % |
| Léa | A, B | 25 % | 25 % | 10 % | 10 % |
| Léa | C | 20 % | 20 % | 0 % | 0 % |
| Léa | D | 10 % | 10 % | 0 % | 0 % |
| Nadia | A, B | 10 % | **60 %** | 20 % | 25 % (70 % si ses 50 % étaient prolongés) |
| Nadia | C | 10 % | 60 % | 15 % | 20 % |
| Nadia | D | 10 % | 60 % | 0 % | 5 % |

**Aucun total ne dépasse 100 %**, dans aucune option, y compris en P1 (Nadia à 50 % et Karim à 20 % sur `reservation-coworking` jusqu'au 2026-12-18) et après le retour de Nadia à 5 %.

**Contrôle de capacité** (h/jour = capacité hebdomadaire ÷ 5 × allocation ; capacité allouée ≥ heures planifiées) :

| Salarié | Option et période | Capacité allouée | h planifiées | Utilisation (AF9) |
|---|---|---|---|---|
| Claire | A, B · P1 | 0,35 h × 15 j = 5,25 h | 2 h | **38,1 %** (sous 50 %) |
| Claire | A · P2 | 0,70 h × 18 j = 12,6 h | 7 h | 55,6 % |
| Karim | A, B, C · P1 | 0,35 h × 15 j = 5,25 h | 2 h | **38,1 %** (sous 50 %) |
| Karim | A, B, C · P2 | 0,70 h × 10 j (hors congés) = 7,0 h | 5 h | 71,4 % |
| Léa | A, B · P1 | 1,75 h × 15 j = 26,25 h | 18 h | 68,6 % |
| Léa | A, B · P2 | 0,70 h × 18 j = 12,6 h | 7 h | 55,6 % |
| Léa | C · P1 | 1,40 h × 15 j = 21,0 h | 11 h | 52,4 % |
| Léa | D · P1 | 0,70 h × 15 j = 10,5 h | 7 h | 66,7 % |
| Nadia | toutes · P1 | 0,56 h × 14 j (EV-002 compté à 0) = 7,84 h | 7 h | 89,3 % |
| Nadia | A, B · P2 | 1,12 h × 18 j = 20,16 h | 12 h | 59,5 % |
| Nadia | C · P2 | 0,84 h × 18 j = 15,12 h | 9 h | 59,5 % |

Toutes les heures planifiées tiennent dans la capacité allouée. **Signalé (AF9)** : Claire et Karim à 38,1 % en P1. Leur besoin est de 2 h ; 5 % est la plus petite allocation qui laisse le binôme se faire dans sa fenêtre. Un humain peut retenir 3 % (63,5 %), avec une fenêtre plus serrée (pour Karim, fin vers le 2026-12-17, la veille de son dernier jour avant ses congés). Aucun ticket n'est ajouté pour atteindre un taux. **Léa** n'est allouée à aucun projet client : 75 à 90 % de sa capacité restent libres, ce qui relève de l'activité commerciale de l'ESN, hors de ce plan.

**Risques résiduels**

| Option | Risques qui restent ouverts |
|---|---|
| A | R-12 : `backend-python` et binôme AF5 chez Karim seul (hors de portée) ; `docker` et `relation-client` seconds au niveau débutant seulement ; concentration sur Léa ; frais externes non confirmés ; `juridique` au niveau débutant seulement |
| B | ceux de A, et `juridique` absente : **recours à un conseil juridique externe au cas par cas**, sur décision humaine à chaque besoin (comme pour T-084) |
| C | ceux de B, et : **Claire seule** recetteuse et interlocutrice client (un empêchement bloque le GO d'un prochain projet) ; **Nadia seule** en `docker` (déploiements, environnement de recette, mercredis non couverts) ; la fenêtre unique de la recette T-045 et des échanges client de fin de projet est perdue |
| D | ceux de C, et : **pas de second relecteur sécurité pendant les congés de Karim** (Léa reste débutante, non habilitée seule) ; **Nadia seule à savoir restaurer**, la leçon de DEC-019 reste sans suite ; `documentation` orpheline (palliatif possible : PR sur `equipe/agents.md`, environ 7,50 €, R11). Les autres besoins sont reportés à la mise à jour du plan au retex de `reservation-coworking`. Le critère de T-003 « grille relue par Karim » est retiré, faute d'allocation de Karim |

### 4. Recommandation : option B
1. **Elle couvre tous les risques critiques et élevés** du registre (R-01 à R-07, R-09), sauf R-12, hors de portée d'un plan de quelques semaines.
2. **Elle tient les fenêtres qui ne se représenteront pas** : la recette T-045 (10 au 15/12) et les échanges client de fin de `reservation-coworking`, seul projet client en cours ; le second relecteur sécurité avant les congés de Karim (21 au 31/12).
3. **Elle écarte la formation juridique** : pour 550 € de temps et environ 700 € de frais, elle ne donnerait que le niveau débutant, pour un besoin rare. Un conseil externe, saisi au cas par cas sur décision humaine, répond mieux à une responsabilité légale.
4. **Face à C**, les 1 265 € de plus achètent la seconde personne sur la recette, la relation client et Docker, c'est-à-dire tout ce qui bloque un GO ou une mise en service quand Claire ou Nadia est absente.
5. **Aucun coût pour le client** : les binômes ne changent ni l'assigné, ni le temps, ni le signataire d'aucun ticket de `reservation-coworking` ; le temps d'explication est compté ici (T-005, T-007, T-014).

**Ordre de priorité des formations** (risque d'abord, puis fenêtre) :
1. T-003, T-004, T-005 : sécurité et revue humaine (Karim seul ; ses congés du 21 au 31/12) ;
2. T-008, T-009 : sauvegarde-restauration (leçon de DEC-019) ;
3. T-002 : supervision (date fixe, EV-002) ;
4. T-012 : documentation (orpheline ; support de T-008 et T-010) ;
5. T-006, T-007 : recette (fenêtre unique de T-045) ;
6. T-010, T-011 : docker ;
7. T-013, T-014 : relation client ;
8. T-015 : juridique (option A seulement).

En cas de manque de capacité, on retire dans l'ordre inverse.

### 5. Impact
- **Calendrier de la décision** : idéalement **le 2026-11-30** (retour de Léa ; échange client T-094 utile à T-013) ; **au plus tard le 2026-12-02**, faute de quoi T-002 (2026-12-03), qui dépend de ce ticket, ne peut pas être pris. Si la décision d'ensemble tarde, T-002 peut être arbitré à part.
- **Tickets** : le `chef-de-projet` passe les tickets non retenus en `ANNULE` (T-016), avec une ligne de journal qui cite DEC-024, et ré-estime T-016. Les autres deviennent prenables et planifiables dès que les allocations sont appliquées.
- **À appliquer par le coordinateur après la décision** (CLAUDE.md § 5, règle 13 : rien n'est appliqué avant) :
  - `projets/esn-interne/projet.md` : `budget_eur`, `deadline`, `salaries_affectes`, `etat_projet: en_cours`, historique des décisions ;
  - `equipe/membres/*.md` : allocation `esn-interne` de P1 tout de suite, puis **celle de P2 le 2026-12-21** (`tableau.py` ne connaît qu'une valeur par projet) ; section « Formations suivies / prévues » ; sur la fiche de Nadia, la ligne « le ticket `formation` sera créé dans son premier projet alloué » renvoie désormais à `esn-interne/T-002` ;
  - `equipe/calendrier.md` : **ne pas annuler EV-002** ; sa capacité nulle le 2026-12-03 est juste pour `reservation-coworking`. `tableau.py` placera donc T-002 sur d'autres jours ; le coût reste juste.
- **`reservation-coworking`** : aucun ticket modifié, aucun coût client. Le risque est un ralentissement du chemin critique (recette T-045, revues T-037 et T-097 à T-099, GO du 2026-12-15) : Claire et Karim peuvent suspendre un binôme sans délai, et le GO garde la priorité.
- **Budget de l'ESN** : le coût de l'option retenue s'ajoute à la part ESN de `reservation-coworking` dans `PORTFOLIO.md` (1 652,50 € projetés au 2026-11-27).
- **Tickets salariés à faire par des humains (AF11, R15)** : T-002 à T-015. Sur le chemin critique du plan : T-003 → T-004 (avant le 2026-12-18), T-002 (2026-12-03), puis T-012 → T-008 et T-010.
- **Points à confirmer par un humain** : congés de fin d'année de Claire, Léa et Nadia (aucun n'est déclaré ; sinon P2 glisse vers janvier, dans la marge du 11 au 15/01) ; devis des frais externes ; accord de Claire pour présenter Léa au client (T-013).
- **Données d'équipe** (registre R-16) : `porter-une-decision` et `revue-humaine` ne figurent sur aucune fiche, si bien qu'AF2 et AF3 ne sont pas vérifiables par `tableau.py`. Une mise à jour des fiches est à décider à part.

## Critères d'acceptation
- [x] Un humain a tranché (option, formations retenues, `budget_eur`, `deadline`, allocations par salarié et par période, enveloppe de frais externes) ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-024-*.md` est créé et référencé dans `decision`.
- [ ] Allocations de P1 appliquées dans equipe/ ; P2 suivie par T-016 et le jalon du 2026-12-21 (planning.md).*
- [x] Les tickets non retenus sont `ANNULE`, avec une ligne de journal qui cite DEC-024 (T-016).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:15 · agent:chef-de-projet · création en ATTENTE_HUMAIN (T-001) : options A, B (recommandée), C et D chiffrées ; ordre de priorité ; contrôle des allocations ≤ 100 % et de la capacité par période ; décision attendue DEC-024 · 0 h
- 2026-11-27 09:30 · Ethan · décision prise et tracée dans DEC-024 (option B, enveloppe de frais séparée), ticket débloqué pour application · 0,25 h
- 2026-11-27 · agent:coordinateur · DEC-024 appliquée : `projet.md` (budget 4 360 €, deadline 2027-01-15, salariés affectés, en_cours) et allocations de P1 dans `equipe/membres/` (Claire 5 %, Karim 5 %, Léa 25 %, Nadia 10 % sur esn-interne) ; T-015 ANNULE par le chef-de-projet (T-016). Critères 1 et 3 cochés ; critère 2 incomplet tant que les allocations de P2 ne sont pas appliquées (2026-12-21) : reste EN_COURS (R13) · 0 h
- 2026-11-27 09:45 · Ethan · critère 2 reformulé : P2 sortie du périmètre de T-017 (suivie par T-016 et le jalon du 21/12), pour ne pas bloquer T-002 (formation du 03/12) ; décision humaine · 0,1 h