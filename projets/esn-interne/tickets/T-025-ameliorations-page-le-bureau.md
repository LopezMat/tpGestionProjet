---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-025
titre: Améliorations de la page « Le bureau » — info-bulle au survol, halos d'état, pièce S3 sans chevauchement
projet: esn-interne
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: EN_REVUE            # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom> ; dérogation de périmètre à scripts/ pour ce seul ticket (DEC-027, en attente de validation)
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7.75          # heures équivalent humain, quel que soit l'assigné (ré-estimé sans le son, sorti en T-026)
temps_passe_h: 5.5          # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:       DEC-027            # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le: 2026-11-27        # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-025 — Améliorations de la page « Le bureau »

## Description
Ticket de travail (R14, par analogie) créé par le coordinateur à la demande d'Ethan du 2026-11-27, sur la branche `esn-interne/bureau-ameliorations`. La page « Le bureau » ([DEC-016](../../../docs/decisions/2026-11-26-DEC-016-page-le-bureau.md), [DEC-017](../../../docs/decisions/2026-11-26-DEC-017-membres-humains-equipe.md), [DEC-018](../../../docs/decisions/2026-11-26-DEC-018-mode-direct-bureau.md)) est un outil interne de l'ESN : son coût est porté par le projet interne (R19), `imputation: esn`. Le plan et le périmètre sont arbitrés par [DEC-027](../../../docs/decisions/2026-11-27-DEC-027-ameliorations-bureau.md) (en attente de validation). Le son d'alerte est sorti de ce ticket et porté par [T-026](T-026-son-alerte-bureau.md).

**Attendu : trois améliorations.**
1. **Info-bulle au survol** d'un personnage (agent, salarié, humain, coordinateur) : nom, rôle, système, ticket le plus urgent avec son statut et son projet. Uniquement des données déjà présentes dans les tickets ; aucune donnée nouvelle n'est injectée par `bureau.py`. En Replay, elle affiche « dernier événement du replay » et jamais un statut affirmé (DEC-016 § 5). En mode Direct, elle n'affiche rien de plus que ce que le journal contient déjà (catégorie, nom d'outil, heure) : jamais de texte de message, de chemin, de commande ni de sortie d'outil (DEC-018 § 3). Construite par `textContent` uniquement, `aria-hidden` (la fiche `aria-live` porte déjà l'information).
2. **Halo** autour d'un personnage au travail (`EN_COURS`, ou actif en mode Direct), et un halo distinct pour `BLOQUE` et pour `ATTENTE_HUMAIN` (forme et couleur différentes). Correspondance état → halo définie dans `bureau.py` et injectée dans le JSON. Fixe si `prefers-reduced-motion` (DEC-016 § 6). Légende mise à jour.
3. **Pièce S3** : grille 2 × 2 plus espacée et places de visite calculées par `construire_plan` auprès du `relecteur-code` et du `testeur`, au lieu des décalages fixes `DECALAGES` du JS ; file d'attente dans le couloir au-delà. Le Replay réserve une place libre au lieu de la place 0. Capacité de S3 : 4 bureaux (un 5ᵉ agent S3 déborde vers l'open space, DEC-016 § 3).

**Fichiers touchés** : `scripts/bureau.py`, `scripts/bureau.js`, `scripts/test_bureau.py`, `README.md` (section « Le bureau »). Ni `console.py`, ni `bureau_direct.py`, ni `journal_direct.py`, ni `.claude/settings*.json`.

**Dérogation de périmètre (DEC-027).** La règle 9 de `dev-frontend` limite ses écritures à `projets/<slug>/app/`. Pour ce seul ticket, et une fois DEC-027 validée, `dev-frontend` peut écrire dans les quatre fichiers ci-dessus, et seulement eux, en plus de ce ticket. Revue par `relecteur-code` puis `testeur` (R13).

**Arrêt obligatoire (Ethan, 2026-11-27).** Si `temps_passe_h` dépasse `estimation_h`, ou si le coût projeté d'`esn-interne` atteint 90 % du budget de fonctionnement (3 924 €), le travail s'arrête et la question est posée à Ethan avant de continuer.

**Estimation (7,75 h, 116,25 €).** Ticket, plan et décision 0,5 h · S3 et places de visite (Instantané et Replay) 2,0 h · info-bulle 1,5 h · halos 1,0 h · tests 1,25 h · captures Edge headless et corrections 1,0 h · README 0,5 h.

## Critères d'acceptation
<!-- Cases cochées par dev-frontend sur instruction du coordinateur (DEC-027) pour ce qu'il a réellement vérifié ; les deux cases laissées vides sont à vérifier par la revue et le testeur. -->
- [ ] Le survol d'un personnage affiche une info-bulle (nom, rôle, système, ticket le plus urgent, son statut et son projet), construite uniquement par `textContent`, et masquée quand la souris quitte le personnage ou le canvas. *(Affichage vu en capture ; le masquage au `mouseleave` n'est vérifié que par lecture du code et test statique, pas observé.)*
- [x] En mode Direct, l'info-bulle n'affiche que des champs du journal validés par la liste blanche (`acteur`, `outil`, `categorie`, `detail`, `ts`) : un test vérifie que le code de l'info-bulle Direct ne lit aucun autre champ.
- [x] Un halo « au travail » entoure un personnage dont l'état est `tape` (ou actif en Direct) ; un halo distinct entoure un personnage `bloque`, un autre un personnage `attente` ou `attend` ; la correspondance état → halo est définie dans `bureau.py` et testée ; aucun halo ne pulse quand `prefers-reduced-motion` est actif.
- [x] Dans la pièce S3, avec les 4 agents du catalogue et jusqu'à 4 agents en revue chez le `relecteur-code` et le `testeur`, aucun rectangle de personnage (16 × 24 px) ne chevauche un autre personnage ni un bureau : vérifié par un test sur `construire_plan` ; au-delà, les visiteurs attendent dans le couloir sans chevauchement.
- [ ] Le Replay n'empile plus deux agents en revue sur la même place. *(Logique de réservation écrite et testée statiquement ; non exécutée avec deux agents simultanément en revue dans un vrai replay.)*
- [x] Aucune donnée de ticket ni du journal Direct n'est ajoutée à la page par rapport à la version précédente, hors table des halos (test).
- [x] `python scripts/test_bureau.py`, `test_console.py`, `test_bureau_direct.py` et `test_journal_direct.py` passent ; `node --check scripts/bureau.js` passe.
- [x] Captures Edge headless de la page générée (Instantané `reservation-coworking`, Replay en cours, info-bulle ouverte, mouvements réduits) relues avant la revue (DEC-016 § 9).
- [x] La section « Le bureau » du `README.md` décrit l'info-bulle, les halos et la nouvelle pièce S3.
- [x] Seuls les quatre fichiers de la dérogation et ce ticket sont modifiés par `dev-frontend` (vérifié sur le diff).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non (aucune donnée nouvelle exposée ; les garanties de DEC-018 restent appliquées par la liste blanche du hook et vérifiées par test)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 11:16 · agent:coordinateur · création (demande d'Ethan, branche esn-interne/bureau-ameliorations) ; plan présenté, accord humain attendu avant le début · 0 h
- 2026-11-27 11:20 · agent:coordinateur · plan accepté par Ethan avec un changement : le son sort du ticket (T-026) ; ré-estimé de 9,5 h à 7,75 h ; dérogation de périmètre et arrêt obligatoire repris ; DEC-027 rédigée en EN_REVUE ; temps de lecture, plan et décision · 0.5 h
- 2026-11-27 11:05 · agent:dev-frontend · prise en charge (A_FAIRE → EN_COURS) ; dérogation de périmètre DEC-027 (VALIDÉ) : scripts/bureau.py, bureau.js, test_bureau.py, README « Le bureau » et ce ticket seulement ; cadre DEC-016 et DEC-018 respecté (aucune ressource externe, textContent/fillText, pas d'innerHTML) · 0 h
- 2026-11-27 11:15 · agent:dev-frontend · pièce S3 : grille 2 × 2 (colonnes 38 et 44, rangées 4 et 8, capacité 4) ; `_places_visite` dans bureau.py calcule, pour les postes du relecteur-code et du testeur, jusqu'à 4 places de visite chacun (sans chevauchement avec personnages, bureaux, étiquettes, vestibule de la porte) et une file de 8 places dans le couloir devant la porte de S3 (champs `visites` du poste et `file` du plan) ; le JS n'a plus de `DECALAGES` : `reserverPlace` / `libererPlace` (Instantané et Replay : première place libre, puis la file) · 1.5 h
- 2026-11-27 11:25 · agent:dev-frontend · halos : constante `HALOS` dans bureau.py injectée en `D.halos` ; dessin sous le sprite (continu bleu, tirets rouges, pointillé ambre), pulsation de 2 s, fixe avec prefers-reduced-motion ; Direct : travail si `p.act` ou instance active, attente si `p.marque` ; Replay : état du halo selon le dernier événement de la personne (`haloReplay`) ; légende et CSS des halos ajoutés · 0.5 h
- 2026-11-27 11:30 · agent:dev-frontend · info-bulle : `<div id="b-infobulle" hidden aria-hidden="true">` dans `#b-cadre` (visible en plein écran), remplie par textContent, bornée au cadre, masquée au mouseleave et hors personnage ; Instantané (ticket le plus urgent, +N autres), Replay (dernier événement), Direct (`infobulleDirect` : catégorie, outil, heure seulement) · 0.9 h
- 2026-11-27 11:36 · agent:dev-frontend · tests ajoutés dans test_bureau.py : non-chevauchement 16 × 24 px sur le catalogue réel et sur des plans synthétiques, 5ᵉ agent S3, places distinctes, file, table des halos, page (#b-infobulle, D.halos, légende), pas d'innerHTML, test statique du bloc Direct, clés des données inchangées. Le test existant « 6 places en S3 » devient « 4 » (capacité DEC-027). Résultats : test_bureau 60 tests OK, test_console 28 OK, test_bureau_direct 23 OK, test_journal_direct 20 OK (1 ignoré), `node --check scripts/bureau.js` OK · 1.0 h
- 2026-11-27 11:40 · agent:dev-frontend · captures Edge headless (2x, mouvements réduits) relues : Instantané reservation-coworking (4 agents en revue séparés sur les places de visite de S3), Replay ev=90 et ev=131 (halo ambre), jeu de test avec BLOQUE (halos bleu, rouge, ambre), info-bulle ouverte sur « veilleur » (événement synthétique injecté dans une copie de la page, hors dépôt) ; non vus : le masquage de l'info-bulle, le halo en pulsation (mouvements non réduits), le mode Direct réel · 0.6 h
- 2026-11-27 11:41 · agent:dev-frontend · README « Le bureau » : info-bulle, halos, pièce S3 · 0.5 h
- 2026-11-27 11:42 · agent:dev-frontend · livré pour revue (EN_COURS → EN_REVUE). Fichiers : scripts/bureau.py, scripts/bureau.js, scripts/test_bureau.py, README.md, ce ticket. Couverture des critères : Direct → test_infobulle_direct_ne_lit_que_la_liste_blanche ; halos → TestHalos, test_halos_dans_les_donnees, test_replay_et_halos_par_dernier_evenement, captures ; S3 → TestPlanS3, TestPlanCatalogueReel ; aucune donnée ajoutée → test_aucune_donnee_ajoutee ; Replay sans empilement → test_places_de_visite_dans_le_js (statique) ; ne touche pas la sécurité (aucune authentification, autorisation ni donnée personnelle ; la liste blanche de DEC-018 est vérifiée par test). Total du ticket : 0.5 h + 5.0 h = 5.5 h sur 7.75 h estimées (temps déjà compté dans les lignes ci-dessus) · 0 h
