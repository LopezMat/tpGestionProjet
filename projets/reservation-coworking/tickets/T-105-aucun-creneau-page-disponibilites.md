---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-105
titre: "SIMULATION — Bug : « Aucun créneau » sur la page de consultation (recette)"
projet: reservation-coworking
type: bug                   # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: salarie:claire
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Bug issu de la note de recette simulée recette-2026-11-26-01 (scénario 4, S2).

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-105 — SIMULATION — Bug : « Aucun créneau » sur la page de consultation (recette)

## Description
**Source : recette (Claire)**. Note : [recette-2026-11-26-01.md](../support/entrant/recette-2026-11-26-01.md) (SIMULATION). Captures : aucune.

**Rapport de recette lié : aucun.** La note indique une recette partielle de [T-055](T-055-page-disponibilites-lecture.md) ; aucun `rapports/recette-*.md` ne la cite. **Information manquante** (signalée au coordinateur, qui la demandera au recetteur) : rapport de recette, URL testée.

**Exigence.** F-01 (disponibilités et réservation), **Must** dans le CDC ([cdc.md](../cdc.md)). Critère de consultation : [T-055](T-055-page-disponibilites-lecture.md), critère 1 : pour une date choisie, la page affiche pour chacune des 3 salles les créneaux d'une heure de 8 h-9 h à 19 h-20 h, « libre » ou « occupé ».

**Étapes de reproduction** (telles que notées par la recetteuse) :
1. Ouvrir la page de consultation des disponibilités.
2. Choisir la salle « Canigou » et la date de demain, soit le 2026-11-27 (un vendredi, à J+1, dans la fenêtre de J à J+14).

**Résultat attendu.** Les créneaux libres de la journée s'affichent pour chaque salle : du lundi au vendredi, 12 créneaux d'une heure par salle et par jour, de 8 h-9 h à 19 h-20 h (F-01, [T-012](T-012-regles-metier-horloge.md)).

**Résultat obtenu.** La page affiche « Aucun créneau », alors qu'aucune réservation n'existe pour cette journée (constat de la recetteuse).

**Environnement.** SHA testé : `dc53a1d` (commit de [T-055](T-055-page-disponibilites-lecture.md)). URL, navigateur et appareil : non renseignés (information manquante).

**Points à vérifier par les développeurs (sans conclusion ici).**
- La salle « Canigou » n'existe pas dans le modèle : les 3 salles sont « Salle 1 », « Salle 2 » et « Salle 3 » (H-20, migration `0001_schema_initial`, CDC v1.1). Soit le jeu de données de recette diffère ([T-021](T-021-jeu-donnees-recette.md)), soit la note contient une erreur. À trancher avant toute reproduction.
- Le message « Aucun créneau » s'affiche quand l'API renvoie une liste vide pour toutes les salles (fonction `aucunCreneau`, `static/js/creneaux.js`). Pour un vendredi sans réservation, la réponse attendue contient 12 créneaux par salle. Pistes à vérifier : la date envoyée à l'API, la réponse de `GET /api/disponibilites` ([T-054](T-054-api-consultation-disponibilites.md)), le jeu de données de recette.

**Doublons.** Recherche faite dans `tickets/` (« Canigou », « Aucun créneau », consultation et disponibilités, T-054, T-055) : aucun ticket `bug` ou `support` ouvert ne porte ce symptôme. [T-055](T-055-page-disponibilites-lecture.md) est la fonctionnalité recettée (`EN_REVUE`, critère 1 non coché) et non un ticket de défaut. [T-069](T-069-api-bloquee-connexion-poolee-gelee.md) (API qui ne répond plus) et [T-076](T-076-page-consultation-message-commande-tests.md) (`ANNULE`, message sur réponse inattendue) sont d'autres symptômes. Pas de doublon.

**Priorité proposée : haute.** Grille S2 § 4 : « fonctionnalité principale en échec ». F-01 est un Must, et la page est la seule consultation des disponibilités livrée. Pas `critique` : aucune production en ligne, pas d'indisponibilité ni de perte de données. Contournement : aucun connu (une autre date n'a pas été testée). Nombre d'utilisateurs touchés : inconnu (recette). La gravité « bloquant pour la recette » ressentie par la recetteuse est reportée telle quelle ; elle ne change pas la priorité.

**Assigné proposé : `agent:dev-frontend`** (la page et `aucunCreneau` sont livrés par [T-055](T-055-page-disponibilites-lecture.md)), à confirmer au triage par le `chef-de-projet`. `agent:dev-backend` si la réponse de l'API est en cause ([T-054](T-054-api-consultation-disponibilites.md)).

**Réponse proposée.** Sans objet : remontée interne de recette.

### Tri du `chef-de-projet` (S1-R5, 2026-11-26, SIMULATION)
**Statut : reste `A_FAIRE`.** Le développement est en pause et **le correctif n'est pas engagé** (condition 1 de DEC-020, voir « Effet budgétaire »).

**Priorité finale : `haute` (confirmée).** Grille S2 § 4 : si le symptôme se confirme, c'est la « fonctionnalité principale en échec » (F-01, Must, seule page de consultation livrée, page de la soutenance, DEC-011). Pas `critique` : aucune production en ligne, ni indisponibilité, ni perte ou fuite de données. **Révision après reproduction** : si le défaut n'est pas reproduit sur la page réelle (erreur de la note), le ticket est clos avec le constat, sans correctif.

**Le défaut n'est pas encore reproduit, et sa cause est incertaine.** Ce qu'on lit au SHA `dc53a1d`, sans conclure :
- **La page n'a pas de sélecteur de salle.** Elle n'a qu'un champ date (`static/index.html`), et elle affiche les 3 salles renvoyées par l'API (« Salle 1/2/3 », H-20, migration `0001_schema_initial`). L'étape 2 de la note (« choisir la salle Canigou ») ne peut donc pas être faite sur cette page. Soit un autre écran ou un autre environnement a été testé, soit la note est approximative.
- **Le message exact est « Aucun créneau ce jour-là. »** (`disponibilites.js`, `afficher`). Il s'affiche quand `aucunCreneau(donnees)` est vrai, c'est-à-dire quand toutes les salles ont une liste vide (en principe le samedi et le dimanche). Le 2026-11-27 est un vendredi, et l'API renvoie alors 12 créneaux par salle : le `testeur` l'a vérifié pour un jour ouvré sur T-054.
- **Une piste à vérifier** : `Array.every` est vrai sur une liste vide. Si l'API renvoie `salles: []` (base de l'environnement testé sans les 3 salles, par exemple une base reconstruite), la page affiche aussi « Aucun créneau ce jour-là. ». La cause serait alors l'environnement ou les données (côté `dev-backend`), et le message du front serait trompeur.
- **Autres pistes à écarter** : une date réellement envoyée qui tombe un samedi (2026-11-28), un autre SHA ou une autre URL.

**Assignation : `agent:dev-frontend` (AF6, confirmée).**
- **Pourquoi lui** : la page, `aucunCreneau` et la vérification dans le navigateur (instance jetable) viennent de T-055. AF1 à AF5 ne s'appliquent pas : pas de contact client, ni de décision, ni de compétence hors périmètre des agents, ni de ticket `critique`. `.claude/agents/dev-frontend.md` existe.
- **Première étape de réalisation : reproduire au SHA `dc53a1d`.** Instance jetable avec la base migrée, `GET /api/disponibilites?date=2026-11-27`, puis la page à la même date, dans le navigateur et l'environnement que Claire précisera. Le résultat est noté au journal (critère 1).
- **Si la cause est dans l'API, les données ou l'environnement**, le `dev-frontend` le note au journal sans toucher au backend et rend la main. Le `chef-de-projet` re-trie alors le ticket vers `agent:dev-backend` (`api-rest`, T-054), ou crée un ticket lié.

**Préalable de reproduction : informations à demander à Claire par le coordinateur.** Sans elles, le ticket passera `BLOQUE` à sa prise en charge (R8). Il faut :
1. le rapport de recette, ou la confirmation qu'il s'agit d'une recette partielle informelle de T-055 hors T-045 ;
2. l'URL testée (aperçu local, autre instance) et le SHA lu sur `/health`, si possible ;
3. le navigateur, sa version, et l'appareil (ordinateur ou téléphone) ;
4. le **nom de salle affiché** à l'écran (« Canigou » n'existe pas dans le modèle) et la façon dont la salle a été « choisie » ;
5. le texte exact du message, la date visible dans le champ, l'heure du test, et si une autre date (un lundi, par exemple) affiche des créneaux ;
6. une capture, si possible.

**Estimation : 1,5 h équivalent humain** (au lieu de 1 h). Détail : reproduction et constat 0,5 h, diagnostic 0,25 h, correctif et test de non-régression 0,5 h, livraison et journal 0,25 h. Si le défaut n'est pas reproduit : environ 0,5 h, sans revue ni vérification.

**Effet budgétaire (taux agent 15 €/h, formule de DEC-020).**
- **Ce ticket** : 1,5 h × 15 € = **22,50 €**.
- **Coûts induits**, non comptés par le tableau parce que les estimations de T-040 et T-066 (revue de code) et de T-041 et T-067 (tests) ne prévoient pas T-105 :
  - revue de code, environ 0,5 h, 7,50 € ;
  - vérification par le `testeur`, environ 0,5 h, 7,50 €.

  Total : **15,00 €**. Le nouveau test de F-01 par Claire est compris dans la recette T-045 (0 €).
- **Coût client avant ce tri** : 5 903,93 € (tableau du 2026-11-26 sans T-105) − 1 782,50 € (imputé à l'ESN, DEC-020) − 22,50 € (T-102 et T-103, DEC-021) + 75,00 € (audit avant le GO) = **4 173,93 €**, soit une marge de **26,07 €**.
  - C'est 15,00 € de plus que les 4 158,93 € de DEC-021, à cause de T-104 (support, 1 h, rangé au budget client).
- **Coût client avec T-105** : 4 173,93 + 22,50 = 4 196,43 € pour le ticket seul (marge de 3,57 €), puis **+ 15,00 € de coûts induits = 4 211,43 €**.
- **Résultat : dépassement prévisible de 11,43 € au-dessus de 4 200 € HT.** Le ticket coûte 37,50 € en tout, plus que la marge de 26,07 €.
- **Condition 1 de DEC-020 déclenchée.** Un ticket `decision` `ATTENTE_HUMAIN` est à créer par le coordinateur **avant d'engager le correctif** (avenant, retrait de périmètre, ou prise en charge explicite par l'ESN ; discussion avec le client portée par Claire, AF1). Aucun dépassement n'est absorbé d'office.
- **Ce qui tient dans la marge** : la reproduction seule (environ 0,5 h, 7,50 €), si un humain décide de l'engager avant l'arbitrage.

**Garantie de livraison (CDC § 9).** Si le défaut est confirmé, c'est un défaut constaté à la recette, dans le périmètre (F-01, Must, critère 1 de T-055). Il est donc couvert par la garantie de livraison, qui est **comprise dans les 4 200 € HT** et non dans la maintenance hors budget. Conséquences :
- un avenant au client est difficile à défendre pour ce défaut ;
- les options réalistes de l'arbitrage sont une prise en charge explicite par l'ESN (défaut de sa propre livraison) ou un retrait de périmètre. Ce retrait est très contraint : ni Must, ni F-08, ni sécurité, ni revues humaines, ni portes S3.

Si la note est erronée (aucun défaut), la garantie ne joue pas, et seuls les 0,5 h de reproduction sont consommés.

**Dépendances : `depend_de` vide.**
- T-054 est `TERMINE`.
- T-055 est `EN_REVUE`, et son critère 1 est justement celui en question : une dépendance vers lui bloquerait T-105.

**Propositions, sans modifier les tickets** (le planning ne change pas, le développement est en pause) :
- **T-045 (recette)** : si le défaut est confirmé, ajouter T-105 à `depend_de`. La recette porte alors sur un SHA qui contient le correctif. Un KO sur un critère de Must rend la recette `NON CONFORME`.
- **T-046 (GO)** : bloqué par transitivité via T-045 (R16) ; aucun ajout direct nécessaire. Si le défaut n'est pas reproduit, aucune dépendance n'est à ajouter.
- **T-055 reste `EN_REVUE`.** Le `testeur` ne doit pas cocher son critère 1, ni le passer `TERMINE`, tant que T-105 n'est pas clos : soit « non reproduit », constat au journal, soit corrigé et vérifié sur un SHA qui contient le correctif.

**Revue humaine requise : non** (S3-R2). Ce ticket n'est ni `critique` ni lié à la sécurité : affichage seul, sans authentification, droits, données personnelles ni secrets. À réévaluer si le correctif touche le backend.

## Critères d'acceptation
- [ ] Le motif de « Aucun créneau » est identifié et noté au journal (salle, date, réponse de l'API, jeu de données).
- [ ] Pour la date du lendemain ouvré, la page affiche les 12 créneaux de chaque salle existante, « libre » ou « occupé ».
- [ ] Le nom « Canigou » est soit remplacé par une salle existante du jeu de données, soit corrigé dans la note par la recetteuse (constat au journal).
- [ ] Si un défaut est corrigé, un test automatisé reproduit le cas qui l'a révélé, et les suites restent vertes. Si le défaut n'est pas reproduit, le constat le dit au journal, sans modification de `app/` (ajout du tri, 2026-11-26).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (S3-R2 : ni `critique` ni lié à la sécurité ; affichage seul ; à réévaluer si le correctif touche le backend)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 23:10 · salarie:claire · SIMULATION · création (saisie par agent:support depuis support/entrant/recette-2026-11-26-01.md) · 0 h
- 2026-11-26 23:30 · agent:chef-de-projet · SIMULATION · tri (S1-R5) : priorité `haute` confirmée (F-01 Must en échec si reproduit) ; assigné `agent:dev-frontend` confirmé (AF6), avec la reproduction au SHA `dc53a1d` comme première étape et un re-tri vers `dev-backend` si l'API, les données ou l'environnement sont en cause ; estimation 1 → 1,5 h ; `depend_de` vide ; revue humaine non requise. **Condition 1 de DEC-020 déclenchée** : coût client 4 173,93 € avant tri, + 22,50 € (T-105) + 15,00 € (revue et vérification induites) = 4 211,43 € > 4 200 € ; correctif **non engagé**, ticket `decision` à créer par le coordinateur. Préalable de reproduction demandé à Claire (rapport, URL et SHA, navigateur et appareil, nom de salle affiché, message exact). Propositions non appliquées : T-105 dans `depend_de` de T-045 si le défaut est confirmé ; T-055 reste `EN_REVUE`. Statut inchangé (`A_FAIRE`). Temps compté dans T-008 · 0 h
- 2026-11-27 00:10 · agent:coordinateur · SIMULATION · décision d'Ethan sur T-106, tracée dans DEC-020 v0.3 : on engage **d'abord la reproduction seule** (0,5 h, 7,50 €), **imputée à l'ESN** ; si le défaut est confirmé, le correctif, sa revue et sa vérification sont **imputés à l'ESN au titre de la garantie de livraison** (CDC § 9) ; sinon, le ticket est clos sans correctif. Statut inchangé (`A_FAIRE`, développement en pause) · 0 h
- 2026-11-27 00:10 · agent:coordinateur · SIMULATION · **relance de Claire** (recetteuse, `cree_par`), préalable à la reproduction : merci de compléter ce ticket ou d'en déposer une note dans `support/entrant/` avec (1) l'URL testée et, si possible, le SHA affiché par `/health` ; (2) le navigateur, sa version et l'appareil ; (3) le **nom de salle affiché** à l'écran et la manière dont il a été choisi (« Canigou » n'existe pas dans le modèle, qui prévoit « Salle 1/2/3 », H-20 ; la page n'a qu'un champ date) ; (4) une capture d'écran · 0 h
