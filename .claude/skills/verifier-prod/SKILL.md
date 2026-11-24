---
name: verifier-prod
description: Vérifie qu'une application est en ligne ET à jour - sonde url_prod/health (lu dans projets/<slug>/projet.md) à intervalles réguliers (en production locale, toutes les 5 s pendant 120 s au plus) et compare le SHA renvoyé au SHA attendu, puis écrit les tentatives et le résultat dans le rapport de déploiement. Appelé par scripts/deployer_local.py et scripts/rollback_local.py ; utilisable seul pour relancer une vérification EN COURS ou constater la version en ligne. Porte 7 de S3.
---

<!-- Skill ESN · système S3 · responsable : C · Lot 2 (C) -->

# verifier-prod

## Quand l'utiliser
- Porte 7 de S3 : **`scripts/deployer_local.py` et `scripts/rollback_local.py` l'appellent eux-mêmes** (production locale Docker, DEC-003), avec un fichier d'état neuf ; le `deployeur` n'a qu'à recopier leur sortie ;
- seul : pour relancer une vérification `EN COURS` (code 3, commande affichée par le script), ou pour constater quelle version tourne, à la demande de l'humain ou de l'`analyste-prod`.

## Entrées
- `slug` du projet ;
- **SHA attendu** : celui cité par la décision GO (ou, après un rollback, le SHA précédent), en hexadécimal de 7 à 40 caractères ;
- `projets/<slug>/projet.md` : `url_prod` et `hebergement` ;
- le rapport de déploiement en cours : `projets/<slug>/rapports/deploiement-AAAA-MM-JJ.md`.

## Procédure
1. **Lire `url_prod` et `hebergement`** dans `projets/<slug>/projet.md`.
   - `url_prod` vide : arrêt, ticket « Déploiement » `BLOQUE`, `bloque_par: url_prod absente, vérification impossible (S3-R5)`.
2. **Production locale** : si l'hôte de `url_prod` est `localhost`, `127.0.0.1` ou `::1`, le mécanisme est **identique**. Il faut seulement que `projet.md` porte `hebergement: local` (choix couvert par une décision humaine). Sinon, arrêt pour incohérence entre `url_prod` et `hebergement`. Le script affiche `Mode : local`.
3. **Lancer le script**, avec un timeout de l'outil Bash de 600 000 ms :
   ```
   python .claude/skills/verifier-prod/verifier_prod.py --url <url_prod> --sha <sha_attendu> --etat projets/<slug>/rapports/verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json --intervalle 5 --timeout 120
   ```
   Sur macOS ou Linux sans `python`, utiliser `python3` (même script, mêmes options ; les deux formes sont autorisées).
   **Un fichier d'état par vérification, jamais réutilisé d'un déploiement ou d'un rollback à l'autre** : le script reprend un état déjà conclu sans sonder, et donnerait un faux « EN LIGNE » après un rollback vers un SHA déjà vérifié. On ne réutilise le même fichier que pour relancer une vérification `EN COURS`.
   Valeurs : en production locale, `--intervalle 5` et `--timeout 120` (ARCHITECTURE § 10.1, passées par les scripts de déploiement) ; les valeurs par défaut du script, `--intervalle 30` et `--timeout 900`, restent celles d'un hébergeur distant. `--max-appel 540` (9 min au plus par appel, sous la limite de 10 min de Bash).
4. **Lire le code retour** :
   | Code | Sens | Suite |
   |---|---|---|
   | 0 | `EN LIGNE ET À JOUR` : `/health` renvoie le SHA attendu | étape 5 |
   | 3 | `EN COURS` : le délai global n'est pas épuisé | **relancer exactement la même commande** : le script reprend l'état (heure de début, tentatives) |
   | 1 | `ÉCHEC` : 15 min écoulées sans concordance | étape 5, puis rollback par le `deployeur` (S3-R6) |
   | 2 | erreur d'usage (URL, SHA, fichier d'état d'un autre SHA) | corriger l'appel ; ne jamais conclure |
5. **Écrire le résultat dans le rapport de déploiement** : recopier les lignes du tableau affiché dans le § « Vérification en ligne (verifier-prod) », puis `**Résultat : EN LIGNE ET À JOUR**` ou `**Résultat : ÉCHEC**`. En production locale, indiquer « mode local » à la ligne « Hébergeur / service ».

## Ce que fait le script
- Une requête GET sur `<url_prod>/health` (sans double `/`), avec un timeout réseau de 20 s et un User-Agent générique ; seuls `http` et `https` sont acceptés.
- Lecture du champ JSON `commit` (repli sur `sha`). C'est le format de `/health` fixé pour les développeurs : `{ "status": "ok", "commit": "<sha>" }`.
- Comparaison en minuscules : égalité, ou préfixe si l'application renvoie un SHA court d'au moins 7 caractères (le résultat affiche alors `OK (préfixe)`).
- Une ligne par tentative : n°, heure, code HTTP, SHA renvoyé (12 premiers caractères), résultat (`OK`, `SHA_DIFFERENT`, `HTTP_503`, `INJOIGNABLE`, `JSON_INVALIDE`).
- Le fichier d'état JSON garde la trace complète. Il est commité avec le rapport.

## Règles
- **Seule la concordance du SHA compte.** Un code 200 sur `/health` ou un run de déploiement vert ne suffisent pas.
  *Pourquoi :* « un push ne suffit pas » (consigne S3, S3-R5, R13) ; l'ancienne version peut très bien répondre 200.
- **Des retries espacés, avec un délai global.** En production locale : 5 s entre deux tentatives et 120 s au total (ARCHITECTURE § 10.1, DEC-003).
  *Pourquoi :* l'app et sa base mettent quelques secondes à démarrer ; sans retries, on déclarerait de faux échecs. Le build est fait avant la vérification, donc 2 minutes suffisent largement.
- **Délai dépassé = ÉCHEC**, et le `deployeur` déclenche le rollback (S3-R6).
  *Pourquoi :* on rétablit d'abord le service, on analyse ensuite.
- **Le même mécanisme en production locale.** Seule l'URL change.
  *Pourquoi :* la preuve reste identique si l'équipe est dispensée d'hébergement réel.
- **Aucun secret dans la commande ni dans le rapport** : `url_prod` est l'URL de l'app, jamais une URL qui porte un jeton.
  *Pourquoi :* le rapport et le fichier d'état sont commités (S3-R8).

## Produit
- les lignes « Vérification en ligne » et le « Résultat » dans `projets/<slug>/rapports/deploiement-AAAA-MM-JJ.md` ;
- `projets/<slug>/rapports/verifier-prod-<sha7>-<AAAAMMJJ-HHMMSS>.json` (état et tentatives), un par vérification.

## Point d'arrêt humain
- Aucun en cas de succès.
- En cas d'`ÉCHEC` : le `deployeur` lance le rollback, puis crée le ticket incident ; toute restauration de données est une décision humaine.
- `url_prod` absente ou incohérente avec `hebergement` : le coordinateur le présente à l'humain.

## Contrôles
- [ ] `url_prod` lue dans `projet.md` ; mode (distant ou local) cohérent avec `hebergement`.
- [ ] Le SHA attendu est celui de la décision GO (ou le SHA précédent après un rollback).
- [ ] Le script a été relancé tant qu'il rendait le code 3.
- [ ] Toutes les tentatives et le résultat final sont recopiés dans le rapport.
