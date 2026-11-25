---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-007
titre: Validation du budget et des délais
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: validation humaine du budget et des délais
validation_humaine_requise: oui   # oui | non
decision:     DEC-009              # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:   2026-11-25              # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-007 — Validation du budget et des délais

## Description
Point d'arrêt humain obligatoire de l'étape 4 (CLAUDE.md § 1, S1 § 4 étape 5). Analyse rédigée par le `chef-de-projet` à partir du [CDC v1.0](../cdc.md) (DEC-006), de l'[architecture v1.1](../architecture.md) (DEC-007, DEC-008), de `equipe/` et du calendrier ; détail dans [planning.md](../planning.md) (`EN_REVUE`). Porteur salarié (AF2) : Claire, qui présente ; la décision reste humaine (R5). Taux : agents 15 €/h ; Claire et Karim 550 €/j soit 78,57 €/h ; Nadia 450 €/j soit 64,29 €/h ; Hugo 350 €/j soit 50,00 €/h (ARCHITECTURE § 8).

**Question.** Le planning du projet `reservation-coworking` (T-008 à T-049 : 42 tickets, dont 20 de réalisation) peut-il être validé, avec le budget prévisionnel, les jalons et les allocations de salariés ci-dessous ? Cinq points sont à trancher (A à E).

### A. Périmètre de la livraison et budget
| Poste | Heures | Coût |
|---|---|---|
| Déjà consommé : T-001 (8 h), T-004 (11,5 h), agents | 19,5 h | 292,50 € |
| `dev-backend` (T-010 à T-021, T-026, T-028) | 60,5 h | 907,50 € |
| `dev-frontend` (T-022 à T-025, T-027) | 22 h | 330,00 € |
| `relecteur-code` (T-039, T-040) | 10 h | 150,00 € |
| `testeur` (T-041, T-042) | 8 h | 120,00 € |
| `securite` (T-043) | 5 h | 75,00 € |
| `deployeur` (T-047) | 1,5 h | 22,50 € |
| `chef-de-projet` (T-008, dont 4 h passées aujourd'hui) | 8 h | 120,00 € |
| Claire : T-007, T-009, T-045 (recette), T-046 (GO) | 8,5 h | 667,86 € |
| Karim : revues humaines T-030 à T-038 | 7,5 h | 589,29 € |
| Nadia : T-029 (sauvegarde), T-044, T-048, T-049 | 7 h | 450,00 € |
| **Total prévu (budget client)** | **157,5 h** | **3 724,64 €, soit 62,1 % de 6 000 € HT** |
| Marge de risque : 25 % du reste à faire (3 372,14 €) | | + 843,04 € |
| **Total avec marge** | | **4 567,68 €, soit 76,1 %** ; reste 1 432,32 € |

Marge de 25 % : T-004 a dépassé de 64 % (quatre révisions) et T-001 de 14 % ; elle couvre les reprises après `CHANGEMENTS_DEMANDÉS`, les bugs de recette, un re-test et un nouveau rapport sur un nouveau SHA.

- **A1 (recommandée)** : une livraison avec les 5 Must et les Should F-06 (T-027) et F-08 (T-028), planifiés après les Must : **3 724,64 €**.
- **A2** : Must seuls ; F-06 et F-08 reportés : environ 130 € et une demi-journée de `dev-backend` en moins, mais il faudrait ensuite une seconde livraison (tests, recette, GO, déploiement, au moins 400 €). À retenir seulement si le client confirme (T-009) que F-08 n'est pas exigée à la mise en ligne.

### B. Allocation des salariés (S1-R10 ; `equipe/` est modifié par le coordinateur après la décision)
Période du 2026-11-25 au 2026-12-18 : 18 jours ouvrés (17 pour Nadia, en formation le 2026-12-03). Utilisation = heures assignées ÷ capacité allouée (AF9, indicateur).

| Salarié | Aujourd'hui | Proposé | h/jour | Heures assignées | Utilisation | Pourquoi |
|---|---|---|---|---|---|---|
| Claire | 10 % (DEC-005) | **20 %** | 1,4 h | 8,5 h | 34 % | Recette de 5 h (T-045), seule `recette-fonctionnelle` ; à 10 %, elle s'étale sur 8 jours et le GO tombe le 2026-12-18 (B2). DEC-005 prévoyait de relever l'allocation pour la recette. |
| Karim | 0 % | **15 %** | 1,05 h | 7,5 h (+ 1,5 h lot ESN) | 40 % (48 % avec le lot ESN) | Chemin critique : aucun ticket d'authentification ne passe `TERMINE` sans sa revue (R13, architecture R-02). Les auth arrivent en revue du 2026-11-27 au 2026-12-04 : à 15 %, il les suit avec un jour de décalage au plus ; à 10 %, environ trois jours. Congés à partir du 2026-12-21, après la deadline. |
| Nadia | 0 % | **20 %** | 1,12 h | 7 h | 37 % | T-029 (4,5 h) fini vers le 2026-12-01, environnement de recette (T-044) prêt avant le 2026-12-09, mise en service (T-048) le jour du déploiement. À 10 %, T-029 finit vers le 2026-12-08 et T-044 retarde la recette. |
| Hugo | 0 % | **10 %**, seulement si le lot ESN reste dans ce projet (point D) | 0,7 h | 8 h (T-006, T-052, T-053) | 63 % | Lot ESN ; sinon allocation au projet interne. |

- **B1 (recommandée)** : allocations du tableau. Les utilisations sous 50 % sont **signalées** (AF9) : elles viennent de temps concentrés sur le chemin critique (revues, recette, mise en service), pas de tickets à ajouter. **Réductions proposées ensuite** (nouvelles décisions, coordinateur) : Karim à 5 % après le 2026-12-09 (revues terminées), Claire à 10 % après le GO, Nadia à 5 % après la mise en service (jusqu'à T-049).
- **B2** : allocations minimales (Claire, Karim et Nadia à 10 %) : utilisation entre 60 et 80 %, mais recette du 2026-12-09 au 2026-12-18 et déploiement après la deadline : **alerte S1-R11**. Déconseillée.

### C. Jalons et délais (détail dans planning.md)
Fin de réalisation 2026-12-07 ; rapports de tests et de sécurité 2026-12-08 ; recette du 2026-12-09 au 2026-12-14 ; **GO 2026-12-14** ; **déploiement et mise en service 2026-12-15** ; **marge de 3 jours ouvrés** (16 au 18) avant la deadline du 2026-12-18.
- **C1 (recommandée)** : ces dates. Le CDC (§ 10) proposait un GO une semaine avant la deadline (2026-12-11) : il n'est atteignable que si Claire concentre la recette sur les 9 et 10 décembre (environ 2,5 h par jour).
- **C2** : viser le GO au 2026-12-11 : Claire bloque ces deux demi-journées (allocation de 40 % cette semaine-là).
- Point de vigilance : une recette `NON CONFORME` demande environ 3 à 4 jours ouvrés (correction, nouveaux rapports, re-recette, GO, déploiement), soit l'essentiel de la marge.

### D. Lot ESN : T-006 et ses suites (T-050, T-051, T-052) et la formation T-053
Ce lot (517,86 €) porte sur l'outillage commun, une règle de l'ESN et des formations : il **ne relève pas du budget du client**.
- **D1 (recommandée)** : le coordinateur le transfère dans un projet interne de l'ESN (par exemple `projets/esn-outillage/`), avec ses propres allocations (Hugo, Karim).
- **D2** : le laisser ici : `tableau.py` affichera **4 242,50 €** (70,7 %) au lieu de 3 724,64 €, dont 517,86 € qui ne concernent pas le client.

### E. Formations et compétences (AF10)
- **Créées (lot ESN)** : T-052 (Hugo, `backend-python`, binôme T-006, AF10 c), 50 € ; T-053 (Hugo, `securite-applicative`, second relecteur, AF10 b), 150 €.
- **Repérées, non créées, à arbitrer** (une seule personne ou aucune) : `relation-client` et `recette-fonctionnelle` (Claire seule ; un empêchement bloque la recette, donc le GO) ; `sauvegarde-restauration` (Nadia seule ; la revue humaine de T-029 porte donc sur le code Python, par Karim) ; `juridique` (absente ; la mention RGPD est validée par le client, responsable du traitement) ; formation « supervision » de Nadia du 2026-12-03 (EV-002 ; sa fiche prévoit de la créer dans son premier projet alloué, mais elle ne sert pas ce client, 7 h, 450 €). Recommandation : les inscrire au plan de formation de l'ESN (projet interne), pas dans ce projet.
- **Option non retenue au budget** : revue d'accessibilité par Léa (architecture § 6), 1,5 h, 96,43 €, allocation de 5 % ; les bonnes pratiques de base (H-07) sont vérifiées par `relecteur-code`, le test de bout en bout et la recette.

**Recommandation.** **A1, B1, C1, D1** ; formations comme au point E. Budget client prévu à 3 724,64 € (62 %), 4 567,68 € avec la marge (76 %) ; GO le 2026-12-14 ; mise en production le 2026-12-15 ; 3 jours ouvrés de marge. Aucune alerte S1-R11.

**Impact.**
- **Budget** : 6 000 € HT tenus avec une marge de 1 432 € après la marge de risque.
- **Délais** : deadline tenue avec 3 jours ouvrés de marge (C1) ; sans les allocations de B1, plus de marge (B2).
- **Tickets** : les tickets de Karim (T-030 à T-038, T-050, T-051), de Nadia (T-029, T-044, T-048, T-049) et de Hugo (T-006, T-052, T-053) sont **conditionnels** à ces allocations ; si elles sont refusées, le `chef-de-projet` réaffecte.
- **Tickets salariés sur le chemin critique** (AF11, à faire par des humains) : revues de Karim (T-030 à T-036, puis T-037 et T-038), T-029 et T-044 (Nadia), T-045 et T-046 (Claire), T-048 (Nadia).
- **Capacité** : Claire garde 80 %, Karim 85 % et Nadia 80 % pour les autres projets.
- **Après décision** : le coordinateur met à jour `equipe/membres/*.md` (allocations) et `projet.md` ; un humain passe `planning.md` en `VALIDÉ`.

## Critères d'acceptation
- [ ] Un humain a arbitré les points A à E (options retenues tracées).
- [ ] Le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé (skill `tracer-decision`) et référencé dans `decision`.
- [ ] `planning.md` est passé `VALIDÉ` par un humain (`valide_par`, `decision`), ou renvoyé au `chef-de-projet` avec les corrections demandées.
- [ ] Les allocations décidées sont reportées par le coordinateur dans `equipe/membres/*.md`, et `projet.md` est cohérent.
- [ ] Si D1 est retenue : le lot ESN est transféré par le coordinateur et les tickets d'ici passent `ANNULE` avec un renvoi.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création, analyse au format R7 (points A à E), statut ATTENTE_HUMAIN ; temps compté dans T-008 · 0 h
