---
name: verifier-prod
description: Vérifie qu'une application est en ligne ET à jour - sonde url_prod/health (lu dans projets/<slug>/projet.md) toutes les 30 s pendant 15 min au plus et compare le SHA renvoyé au SHA attendu, puis écrit les tentatives et le résultat dans le rapport de déploiement. Fonctionne aussi en production locale (url_prod en localhost). À utiliser par le deployeur à la porte 7 de S3, après chaque déploiement et après chaque rollback.
---

<!-- Skill ESN · système S3 · responsable : C · Lot 2 (C) -->

# verifier-prod

## Quand l'utiliser
- Porte 7 de S3 : juste après le déclenchement d'un déploiement ;
- après un rollback, pour vérifier que la version précédente est bien revenue en ligne ;
- à la demande de l'humain ou de l'`analyste-prod`, pour constater quelle version tourne.

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
   python .claude/skills/verifier-prod/verifier_prod.py --url <url_prod> --sha <sha_attendu> --etat projets/<slug>/rapports/verifier-prod-<sha7>.json
   ```
   Sur macOS ou Linux sans `python`, utiliser `python3` (même script, mêmes options ; les deux formes sont autorisées).
   Valeurs par défaut : `--intervalle 30` (secondes entre deux tentatives), `--timeout 900` (15 min au total), `--max-appel 540` (9 min au plus par appel, sous la limite de 10 min de Bash).
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
- **Des retries espacés, avec un délai global.** 30 s entre deux tentatives et 15 min au total, valeurs proposées par ARCHITECTURE § 10.1 et paramétrables ; les valeurs définitives sont tranchées au lot 5.
  *Pourquoi :* l'offre gratuite de Render met l'app en veille, et un build prend plusieurs minutes ; sans retries, on déclarerait de faux échecs.
- **Délai dépassé = ÉCHEC**, et le `deployeur` déclenche le rollback (S3-R6).
  *Pourquoi :* on rétablit d'abord le service, on analyse ensuite.
- **Le même mécanisme en production locale.** Seule l'URL change.
  *Pourquoi :* la preuve reste identique si l'équipe est dispensée d'hébergement réel.
- **Aucun secret dans la commande ni dans le rapport** : `url_prod` est une URL publique, jamais l'URL du deploy hook.
  *Pourquoi :* le rapport et le fichier d'état sont commités (S3-R8).

## Produit
- les lignes « Vérification en ligne » et le « Résultat » dans `projets/<slug>/rapports/deploiement-AAAA-MM-JJ.md` ;
- `projets/<slug>/rapports/verifier-prod-<sha7>.json` (état et tentatives).

## Point d'arrêt humain
- Aucun en cas de succès.
- En cas d'`ÉCHEC` : le `deployeur` lance le rollback, puis crée le ticket incident ; toute restauration de données est une décision humaine.
- `url_prod` absente ou incohérente avec `hebergement` : le coordinateur le présente à l'humain.

## Contrôles
- [ ] `url_prod` lue dans `projet.md` ; mode (distant ou local) cohérent avec `hebergement`.
- [ ] Le SHA attendu est celui de la décision GO (ou le SHA précédent après un rollback).
- [ ] Le script a été relancé tant qu'il rendait le code 3.
- [ ] Toutes les tentatives et le résultat final sont recopiés dans le rapport.
