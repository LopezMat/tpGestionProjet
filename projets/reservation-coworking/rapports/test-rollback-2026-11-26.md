---
titre: Rapport de test du rollback — production locale Docker — 2026-11-26
statut: EN_REVUE
responsable: C
version: 0.1
maj_le: 2026-11-26
valide_par:
decision:
---
<!-- modèle : templates/rapport-deploiement.md v0.3, adapté (aucun template dédié au test de rollback) · responsable du modèle : A -->

# Rapport de test du rollback — production locale Docker — 2026-11-26

> **Objet.** Ce rapport trace le test de rollback exigé par S3-R7 et promis par [ARCHITECTURE § 10](../../../docs/ARCHITECTURE.md#10-décisions-du-lot-5--vérification-sauvegardes-rollback) (point 3). On a lancé le test réel de `scripts/test_prod_locale.py` (classe `TestReel`), avec Docker : déploiement de v1, puis de v2 avec une vraie sauvegarde, puis de v3 qui tombe en panne au démarrage, et rollback vers v2.
>
> **Périmètre.** Le test tourne sur un **dépôt Git temporaire** et sur la **mini-app de démonstration** `scripts/fixtures/app-demo` (contrat `/health` de l'ARCHITECTURE § 9), et non sur l'app de `reservation-coworking`. Il utilise un projet compose jetable (`esn-test-dd1be5ec`) et un port aléatoire. Il ne touche ni à la production locale du projet ni à ses données. Il démontre les mécanismes de S3 (`deployer_local.py`, `rollback_local.py`, `verifier-prod`, sauvegarde `pg_dump`), et ne vaut pas rapport de déploiement du projet.

## Conditions du test
| Élément | Valeur |
|---|---|
| Date et heure | 2026-11-26, de 09:51:39 à 09:53:12 (heure locale) |
| Poste | poste de démonstration, Windows 11, Docker Engine 27.3.1 |
| Dépôt de l'ESN | branche `regles/coherence`, commit `5ad576da6df81a7b9e0e5ce27f34aad576570dbb` |
| Commande | `python scripts/test_prod_locale.py`, classe `TestReel` (`test_deploiement_panne_rollback`), lancée par le coordinateur à la demande d'Ethan, avec un enregistreur externe qui consigne la sortie et la durée de chaque appel de script, sans rien changer au test |
| Application | `scripts/fixtures/app-demo` + `postgres:16-alpine` (modèle `deploiement/docker-compose.yml`) |
| Paramètres de `verifier-prod` | `--intervalle 2 --timeout 120` pour v1, `90` pour v2 et pour le rollback, **`20` pour v3**, afin d'abréger la panne. En production : 5 s et 120 s (ARCHITECTURE § 10.1) |
| Résultat global | **1 test, OK, en 91,5 s** ; aucun test ignoré |

## Versions déployées
| Version | SHA | Particularité |
|---|---|---|
| v1 | `46e92342cded5a51ff69ca723f02b9e669fc450b` | première mise en service |
| v2 | `a019941b1af518293d0c30d3dd641121b979bb12` | v1 + une ligne dans `app.py` |
| v3 | `2b910e690a982921a820415e3a904e9829600a28` | v2 + `CMD ["python", "-c", "raise SystemExit(1)"]` : l'app s'arrête dès le démarrage |

## Déroulé
| # | Étape | Début | Durée | Code retour | Résultat |
|---|---|---|---|---|---|
| 1 | `deployer_local.py --sha v1` | 09:51:41 | 12,8 s | 0 | sauvegarde « aucune (première mise en service, aucune base existante) » ; image `esn-test-dd1be5ec:46e9234…` construite ; **EN LIGNE ET À JOUR** |
| 2 | `deployer_local.py --sha v2` | 09:51:54 | 18,7 s | 0 | sauvegarde `20261126-095155-46e9234.dump` (796 octets, vrai dump `PGDMP`) ; image `a019941…` construite ; **EN LIGNE ET À JOUR** |
| 3 | `deployer_local.py --sha v3` | 09:52:12 | 39,3 s | **1** | sauvegarde `20261126-095214-a019941.dump` (796 octets) ; image `2b910e6…` construite ; lancement OK, puis **ÉCHEC** (délai global de 20 s dépassé) ; le script indique la suite : `rollback (S3-R6)` |
| 4 | `rollback_local.py` (sans `--sha` : il suit un déploiement en échec, S3-R6) | 09:52:52 | 4,6 s | 0 | `VERSION_REFUSEE: 2b910e6…` ; `VERSION_RESTAUREE: a019941…` ; image v2 **relancée sans rebuild** ; dernière sauvegarde non restaurée (décision humaine, règle 5 du `deployeur`) ; **EN LIGNE ET À JOUR** |
| 5 | Restauration de la sauvegarde de l'étape 2 (`pg_restore --clean --if-exists`, commande du runbook [perte-donnees](../../../runbooks/perte-donnees.md)) | après 09:52:56 | — | 0 | restauration réussie. Le test l'exécute pour valider la commande ; en exploitation, seul un humain la lance, après décision |

## Vérification en ligne (verifier-prod) : SHA vérifiés par `/health`
Chaque vérification a son propre fichier d'état `rapports/verifier-prod-<sha7>-<horodatage>.json` (dans le dépôt temporaire du test), jamais réutilisé (ARCHITECTURE § 10.1).

| Vérification | Fichier d'état | Tentative | Heure | Code HTTP | SHA renvoyé par `/health` | Résultat |
|---|---|---|---|---|---|---|
| v1 | `verifier-prod-46e9234-20261126-095151.json` | 1 | 09:51:54 | 200 | `46e92342cded5a51ff69ca723f02b9e669fc450b` | OK, SHA attendu |
| v2 | `verifier-prod-a019941-20261126-095210.json` | 1 | 09:52:12 | 200 | `a019941b1af518293d0c30d3dd641121b979bb12` | OK, SHA attendu |
| v3 | `verifier-prod-2b910e6-20261126-095229.json` | 1 | 09:52:33 | — | — | INJOIGNABLE |
| v3 | | 2 | 09:52:39 | — | — | INJOIGNABLE |
| v3 | | 3 | 09:52:46 | — | — | INJOIGNABLE |
| v3 | | 4 | 09:52:52 | — | — | INJOIGNABLE → **ÉCHEC** |
| rollback v2 | `verifier-prod-a019941-20261126-095254.json` | 1 | 09:52:56 | 200 | `a019941b1af518293d0c30d3dd641121b979bb12` | OK, SHA attendu |

Le SHA renvoyé par `/health` vient de `GIT_COMMIT`, figé dans l'image au build (ARCHITECTURE § 9). L'image v2 relancée par le rollback annonce donc bien son propre SHA, et pas celui de v3.

## Panne de v3 détectée, retour à v2
- **Détection** : `/health` ne répond pas (INJOIGNABLE) aux 4 tentatives, espacées de 6 à 7 s, de 09:52:33 à 09:52:52. `verifier-prod` conclut **ÉCHEC** au dépassement du délai global, et `deployer_local.py` sort avec le code 1 en indiquant la suite, le rollback (S3-R6). Aucun faux « EN LIGNE » : le fichier d'état de v3 est neuf.
- **Retour à v2** : `rollback_local.py` relance l'image `esn-test-dd1be5ec:a019941…`, déjà construite, et `/health` renvoie le SHA de v2 à la première tentative.
- **Historique** (`deploiement/local/<slug>/historique.json`) : quatre entrées, `deploiement` v1 et v2 (EN LIGNE ET À JOUR), `deploiement` v3 (ÉCHEC), puis `rollback` vers v2 avec `version_refusee` égale à v3.

## Durées
| Mesure | Durée |
|---|---|
| Déploiement de v1 (build, lancement, vérification) | 12,8 s |
| Déploiement de v2 (sauvegarde, build, lancement, vérification) | 18,7 s |
| Déploiement de v3 jusqu'au constat d'ÉCHEC | 39,3 s, dont environ 23 s de vérification (09:52:29 → 09:52:52) |
| **Rollback** (relance de l'image v2 et vérification) | **4,6 s** |
| Du constat d'ÉCHEC au retour vérifié de v2 | environ 4 s (09:52:52 → 09:52:56) |
| Indisponibilité de l'app pendant le test (lancement de v3 → v2 vérifiée) | environ 27 s (09:52:29 → 09:52:56) |
| Test complet | 91,5 s |

**À l'échelle de la production** : avec les paramètres réels (sonde toutes les 5 s, pendant 120 s au plus), une panne au démarrage serait constatée au plus tard 120 s après le lancement. Le rollback ajoute environ 5 s, puisqu'il n'y a ni rebuild ni réseau.

## Conclusion
**Rollback CONFORME à S3-R6 et S3-R7.** La panne de v3 est détectée par `verifier-prod`, le déploiement est déclaré en ÉCHEC, et le rollback rétablit v2 en moins de 5 s. Le SHA est vérifié par `/health`. La sauvegarde prise avant chaque déploiement est un vrai dump, restaurable par la commande du runbook.

**Limites** :
- Le test porte sur la mini-app de démonstration et non sur l'app de `reservation-coworking`. Le premier déploiement réel du projet produira son propre rapport de déploiement.
- Le délai de 20 s pour v3 est propre au test ; l'ordre de grandeur en production est donné ci-dessus.
- Les fichiers d'état et l'historique ont été lus dans le dépôt temporaire avant son nettoyage par le test. Ils ne sont pas conservés dans le dépôt : leurs valeurs sont reportées ici.
