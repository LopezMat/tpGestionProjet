---
name: recette
description: Procédure du salarié recetteur (humain) pour la recette d'une livraison au regard du CDC, porte 3 bis de S3 - liste des critères d'acceptation du CDC, test de l'app au SHA candidat, tickets bug via creer-ticket pour chaque KO, re-test sur le nouveau SHA, puis rapports/recette-AAAA-MM-JJ.md avec le verdict CONFORME ou NON CONFORME. À utiliser par l'humain qui porte le ticket « Recette », dans une session dédiée, quand les rapports de tests (CONFORME) et de sécurité (NON BLOQUANT) portent sur le SHA candidat. Jamais par un agent.
---

<!-- Skill ESN · système S3 · responsable : C · DEC-002 -->

# recette

## Quand l'utiliser
Quand le ticket « Recette » d'une livraison devient prenable : ses dépendances (tickets de réalisation et ticket « Tests ») sont `TERMINE`, et les rapports de tests et de sécurité de la livraison sont verts sur le même SHA. Le skill sert **le salarié recetteur**, un humain qui travaille dans une session dédiée en citant le ticket (CLAUDE.md R15, AF11). Claude l'assiste : il liste, prépare, rédige sous sa dictée et crée les tickets. **Il ne teste pas à sa place.**

## Entrées
- le ticket « Recette » `projets/<slug>/tickets/T-NNN-recette*.md`, assigné à `salarie:<prenom>` ;
- `projets/<slug>/cdc.md` **VALIDÉ** : exigences `F-NN`, priorité MoSCoW, critères d'acceptation ;
- le dernier `rapports/tests-*.md` (`CONFORME`) et le dernier `rapports/securite-*.md` (`NON BLOQUANT`), qui donnent le **SHA candidat** ;
- `projets/<slug>/projet.md` : `url_prod`, `hebergement` ; l'URL de recette si l'architecture en prévoit une ;
- références : `templates/rapport-recette.md`, `.claude/skills/creer-ticket/SKILL.md`, `docs/systemes/S3-deploiement.md` (porte 3 bis, S3-R9).

## Procédure
1. **Vérifier les préconditions.** Le ticket « Recette » est prenable (dépendances `TERMINE`) ; `cdc.md` est `VALIDÉ` ; les rapports de tests et de sécurité portent sur le même SHA, qui devient le SHA candidat ; le recetteur n'est l'auteur d'aucun ticket de la livraison. Sinon, s'arrêter et le dire au coordinateur. Passer le ticket « Recette » `EN_COURS`, avec `statut_depuis` et `debut_le`.
2. **Lister les critères.** Recopier dans le tableau du rapport chaque exigence `F-NN` du CDC qui fait partie de la livraison, **Must d'abord**, avec chacun de ses critères d'acceptation, mot pour mot. Une ligne par critère.
3. **Préparer l'environnement.** L'app doit tourner **au SHA candidat** : en local, lancée avec `GIT_COMMIT=$(git rev-parse HEAD)` sur ce commit, ou sur l'URL de recette. Constater la version avec `python scripts/sonde_sante.py --url <url> --sha <sha candidat> --mesures 1` (Mac : `python3`), et recopier le résultat dans le rapport. Si le SHA diffère, s'arrêter : on ne recette pas une autre version.
4. **Tester.** Le recetteur exécute chaque critère comme le ferait le client et **donne lui-même** le résultat : `OK`, `KO` ou `Non testé` (avec la raison), plus une observation. Claude recopie ce qui est dicté.
5. **Traiter chaque KO.** Créer un ticket `bug` selon `creer-ticket` : `cree_par: salarie:<prenom>`, étapes de reproduction, résultat attendu (le critère du CDC), résultat obtenu, environnement (SHA, URL), priorité proposée (grille de S2 § 4). Lier le ticket dans la ligne du critère.
6. **Re-tester après correction.** Une correction produit un nouveau SHA : il faut alors de nouveaux rapports de tests et de sécurité, puis un **nouveau rapport de recette** sur ce SHA. Re-tester au minimum les critères KO et tous les critères des Must (non-régression), et reporter l'historique dans le tableau « Re-tests ».
7. **Conclure.** Appliquer la règle du verdict (S3-R9) :
   - **CONFORME** si tous les critères des exigences **Must** sont `OK` et qu'aucun bug `critique` ou `haute` issu de la recette n'est ouvert ; un KO sur un Should ou un Could est admis s'il a son ticket bug ;
   - **NON CONFORME** dans tous les autres cas, y compris un critère Must `Non testé`.

   Rapport en `statut: EN_REVUE`. Dans le ticket « Recette » : ligne de journal (verdict, SHA, nombre de critères OK/KO, temps en heures équivalent humain) et `temps_passe_h`. Si le verdict est CONFORME et que tous ses critères sont cochés, **le recetteur** passe le ticket `TERMINE` (`termine_le`, R13) ; sinon il reste `EN_COURS`.
8. **Rendre la main au coordinateur** : verdict, SHA, tickets bug créés. Avec un verdict CONFORME, le coordinateur peut présenter le ticket GO (R16).

## Règles
- **Claude n'écrit jamais un résultat que l'humain n'a pas constaté.** Il ne coche rien, ne déduit aucun `OK` des tests automatisés et ne choisit pas le verdict.
  *Pourquoi :* la valeur de la recette est le regard humain sur l'app, comme le client l'utilisera ; un résultat rédigé par l'IA la viderait de son sens (S3-R9, R15).
- **Un rapport par SHA.** Un rapport ne vaut que pour le SHA qu'il cite ; toute correction impose une nouvelle recette.
  *Pourquoi :* le `deployeur` compare le SHA du GO à celui de la recette (porte 3 bis) ; un rapport sur un autre commit n'a rien recetté de ce qui part en ligne.
- **Le recetteur n'est pas l'auteur du code** de la livraison.
  *Pourquoi :* celui qui écrit le code ne le valide pas (S3-R1).
- **Les critères viennent du CDC `VALIDÉ`, mot pour mot.** Un critère ambigu est signalé dans l'observation et au coordinateur ; il n'est pas réinterprété.
  *Pourquoi :* la recette vérifie l'engagement pris envers le client, pas une version reformulée.
- **Un rapport NON CONFORME bloque le GO** ; seul un nouveau rapport CONFORME le débloque.
  *Pourquoi :* « pas de GO sans rapport de recette CONFORME » (S3-R9, CLAUDE.md R16).

## Produit
- `projets/<slug>/rapports/recette-AAAA-MM-JJ.md` (template `rapport-recette.md`, `EN_REVUE`) ;
- un ticket `bug` par KO ;
- le ticket « Recette » mis à jour (journal, temps, statut).

## Point d'arrêt humain
- Toute la recette est humaine : résultats, tickets bug et verdict viennent du recetteur.
- Le verdict ouvre ou bloque le GO, qui reste lui-même une décision humaine (S3-R3).

## Contrôles
- [ ] Le SHA candidat est le même dans les rapports de tests, de sécurité et de recette, et dans la sonde.
- [ ] Chaque critère des exigences de la livraison a une ligne ; les Must sont tous `OK` ou `KO`, jamais vides.
- [ ] Chaque KO a son ticket bug lié.
- [ ] Le verdict suit S3-R9 ; le rapport est en `EN_REVUE`.
- [ ] Le ticket « Recette » porte le journal, le temps et les dates de statut.
