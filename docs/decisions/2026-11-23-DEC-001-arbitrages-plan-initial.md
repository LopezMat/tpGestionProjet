---
titre: Arbitrages du plan initial (Lot 1)
statut: EN_REVUE
responsable: B
version: 0.2
maj_le: 2026-11-23
valide_par:
decision: DEC-001
id: DEC-001
date: 2026-11-23
decide_par: équipe
projet: ESN
ticket:
modifie_une_regle: oui
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-001 — Arbitrages du plan initial

> **En attente de validation humaine.** Ce fichier a été rédigé par le coordinateur à partir des arbitrages de l'équipe. Conformément à R5, c'est à un membre de l'équipe de le passer lui-même à `VALIDÉ` et de renseigner `valide_par`.

## Contexte
À partir de `docs/VISION.md`, le coordinateur a proposé une arborescence, un catalogue d'agents, un circuit des fichiers et une liste d'incohérences, d'oublis et de questions. L'équipe a arbitré chaque point le 2026-11-23. Ce fichier en garde la trace, une section par arbitrage. Les sections 23 à 25 ont été ajoutées le même jour, après la revue du Lot 1 par l'équipe.

---

## 1. Emplacement du code client
**Décision :** le code de chaque application cliente vit dans `projets/<slug>/app/`, dans ce dépôt. La CI filtre ses déclenchements par chemin.
**Pourquoi :** un seul dépôt reste simple à démontrer et à évaluer sur une semaine ; le filtrage par chemin évite de lancer les tests d'un projet quand un autre change.

## 2. Hébergement et vérification en ligne
**Décision :** Render (offre gratuite) par défaut, avec un déploiement via le deploy hook déclenché par `deploy.yml`. Chaque app expose `/health`, qui renvoie le SHA du commit déployé. `verifier-prod` compare ce SHA au commit attendu, **avec des retries espacés**. L'architecte peut proposer un autre hébergeur selon le projet, avec validation humaine.
**Pourquoi :** la consigne exige de vérifier que l'app est en ligne **et à jour** ; comparer le SHA le prouve. Les retries sont nécessaires parce que l'offre gratuite met l'app en veille. Le choix par défaut évite de rediscuter l'hébergement à chaque projet, tout en gardant la souplesse.

## 3. Sources de données du système 2
**Décision :** sources simulées pour le support (`support/entrant/`) et pour les logs et métriques (`rapports/`), healthcheck réel.
**Pourquoi :** une semaine ne permet pas de brancher un vrai monitoring ni d'avoir de vrais utilisateurs ; la simulation permet de rejouer des scénarios devant le jury, et le healthcheck réel prouve la mise en ligne.

## 4. Formule du temps restant
**Décision :** temps restant = Σ max(0, estimation_h − temps_passe_h) sur les tickets qui ne sont ni TERMINE ni ANNULE.
**Pourquoi :** la formule de la vision soustrayait aussi le temps des tickets terminés, ce qui sous-estimait le reste à faire ; le `max(0, …)` évite qu'un ticket en dépassement réduise artificiellement le total.

## 5. Unités et coûts
**Décision :** 1 jour = 7 h. Les salariés ont un coût journalier converti en €/h, selon la grille débutant 350 €/j, confirmé 450 €/j, expert 550 €/j (fourchette de l'équipe ; la répartition par niveau a été proposée dans le plan v2 et approuvée avec le Lot 1). Les agents ont un coût fictif de 15 €/h (API + supervision humaine), justifié dans `ARCHITECTURE.md` § 8.
**Pourquoi :** une unité commune est indispensable pour calculer un budget consommé. Le coût agent intègre la supervision humaine parce qu'un agent n'est jamais gratuit : il faut relire et valider ce qu'il produit.

## 6. Temps des agents en heures équivalent humain
**Décision :** `estimation_h` et `temps_passe_h` sont toujours en heures équivalent humain, quel que soit l'assigné. Le coût dépend du type d'assigné.
**Pourquoi :** les estimations restent comparables, et un ticket peut être réaffecté d'un agent à un salarié (ou l'inverse) sans être ré-estimé.

## 7. VALIDÉ réservé aux humains
**Décision :**
1. Un hook PreToolUse bloque toute écriture d'un en-tête `statut: VALIDÉ` par un agent ou par le coordinateur.
2. Tout document VALIDÉ doit avoir `valide_par` et `decision: DEC-NNN`, qui pointe vers un fichier de `docs/decisions/`.
3. Un contrôle CI vérifie cette correspondance.

Les humains valident en modifiant le fichier eux-mêmes.
**Pourquoi :** la supervision humaine est au cœur de la vision ; elle doit être appliquée techniquement, pas seulement écrite en consigne, et chaque validation doit être traçable.

## 8. Document VALIDÉ figé pour les agents
**Décision :** le hook bloque toute écriture sur un fichier dont l'en-tête est `VALIDÉ`. Pour le modifier, un humain le repasse en `EN_REVUE`.
**Pourquoi :** sans cette règle, un agent pourrait modifier le contenu d'un document validé sans toucher à son statut, ou contourner le hook par Bash (le contrôle CI servant alors de filet). Figer le fichier garantit que ce qui est appliqué est exactement ce que l'humain a validé.

## 9. Ticket `decision` et fichier de décision
**Décision :** le ticket porte l'attente, le fichier de `docs/decisions/` porte la trace. Ils sont liés par l'id.
**Pourquoi :** on évite le doublon. Le ticket apparaît dans le tableau de bord tant que la décision est attendue ; le fichier reste comme preuve permanente.

## 10. Développeurs : pôle réalisation
**Décision :** `dev-backend` et `dev-frontend` sont des agents d'exécution transverses (« pôle réalisation »), non rattachés à S4, sous la responsabilité de A.
**Pourquoi :** ils n'appartiennent à aucun des 4 systèmes de la consigne ; ils exécutent des tickets planifiés par S1 et contrôlés par S3. Les rattacher à S4 aurait brouillé le rôle du cahier des charges.

## 11. Régénération des tableaux de bord
**Décision :** le workflow commite TABLEAU et PORTFOLIO uniquement s'il y a des changements, avec `[skip ci]` et un groupe `concurrency`. En cas de conflit, on régénère au lieu de résoudre à la main.
**Pourquoi :** on évite les boucles de CI, les commits vides et les conflits entre exécutions parallèles. Comme les tableaux sont générés, les régénérer est toujours correct.

## 12. Type de ticket `amelioration` et retour d'expérience
**Décision :** ajout du type de ticket `amelioration` et d'un fichier `projets/<slug>/retex.md` en fin de projet ou de jalon. Le chef de projet en tire des tickets d'amélioration des agents et de formation.
**Pourquoi :** la consigne S1 demande d'identifier les améliorations des agents IA et les besoins de formation ; le retex les fait émerger, et les tickets les rendent visibles, chiffrées et suivies.

## 13. Revue de code
**Décision :** nouvel agent `relecteur-code` (responsable C), en lecture seule, qui donne un avis `APPROUVÉ` ou `CHANGEMENTS_DEMANDÉS` dans le ticket. Une revue humaine reste obligatoire pour les tickets critiques et ceux qui touchent la sécurité.
**Pourquoi :** le statut EN_REVUE n'avait pas de relecteur désigné. Un relecteur indépendant de l'auteur améliore la qualité ; sur les sujets critiques, l'humain garde la main.

## 14. Sauvegardes et rollback
**Décision :** S3 prend une sauvegarde avant chaque déploiement et dispose d'une procédure de rollback testée. Le runbook `perte-donnees` s'appuie dessus.
**Pourquoi :** sans sauvegarde, le runbook de perte de données serait inapplicable ; un rollback jamais testé ne fonctionne pas le jour J.

## 15. Sections obligatoires du CDC
**Décision :** le template CDC contient obligatoirement les sections Exigences de tests, Exigences de sécurité et Exigences de maintenance, qui renvoient aux systèmes 1, 2 et 3.
**Pourquoi :** la consigne S4 demande de garantir qualité, sécurité et maintenance grâce aux trois autres systèmes ; ces sections rendent ce lien explicite et vérifiable.

## 16. Modification des règles par les humains
**Décision :** toute modification de règle passe par une PR, avec un fichier de décision et une entrée dans `docs/CHANGELOG-REGLES.md` (date, règle modifiée, ancien / nouveau, pourquoi, événement déclencheur).
**Pourquoi :** la consigne veut que les humains modifient les règles quand la situation change ; la PR et le changelog prouvent qui a changé quoi, quand et pourquoi.

## 17. Multi-projets
**Décision :** chaque fiche membre contient une allocation en % par projet, utilisée par `tableau.py` pour calculer la capacité. La priorité entre projets est une décision humaine.
**Pourquoi :** sans allocation explicite, la même heure serait comptée sur plusieurs projets et les projections seraient fausses.

## 18. En-tête standard
**Décision :** un en-tête standard, défini une seule fois dans `templates/_ENTETE.md` : `statut`, `responsable`, `version`, `maj_le`, `valide_par`, `decision`. Les tickets gardent leur frontmatter propre.
**Pourquoi :** une lecture uniforme du statut et du responsable, et une vérification automatique possible (hook, CI) ; c'est aussi la condition de livrables cohérents entre eux.

## 19. Passation avant un départ
**Décision :** passation au moins 5 jours ouvrés avant la date de départ. Si le préavis est plus court : passation accélérée, alerte au tableau de bord et ticket `ATTENTE_HUMAIN`.
**Pourquoi :** une semaine de travail permet de documenter, de faire travailler un binôme et de réaffecter ; en dessous, le risque de perte de connaissance doit être arbitré par un humain.

## 20. Alerte ticket sans mise à jour
**Décision :** alerte au-delà de 2 jours ouvrés sans mise à jour d'un ticket `EN_COURS`.
**Pourquoi :** sur un projet d'une semaine, 2 jours de silence représentent 40 % du temps disponible ; c'est aussi le moyen de détecter un agent ou un salarié bloqué en silence.

## 21. Répartition rééquilibrée de l'équipe
**Décision :**
- A : analyste-besoin, architecte, dev-backend, dev-frontend, templates/.
- B : CLAUDE.md, chef-de-projet, skills de ticketing, équipe et événements, equipe/.
- C : testeur, securite, relecteur-code, deployeur, settings.json et hooks, workflows, sauvegardes et rollback.
- D : veilleur, analyste-prod, support, gestionnaire-crise, runbooks, scripts/tableau.py et ses tests.

**Pourquoi :** la répartition initiale chargeait A et B bien plus que D ; `tableau.py` passe à D et `relecteur-code` à C pour équilibrer la charge.

## 22. Construction par lots
**Décision :** la configuration se construit par lots ; à chaque lot, création, résumé, puis arrêt pour validation. Le Lot 1 est le socle documentaire.
**Pourquoi :** chaque lot reste relisable et défendable ; l'équipe garde la main sur chaque étape, conformément à la vision.

---

## Corrections issues de la revue du Lot 1

## 23. Normalisation du statut VALIDÉ
**Décision :** le hook et `verifier_validations.py` normalisent la valeur du statut (accents supprimés, majuscules) : `VALIDE`, `validé`, `Validé` sont traités comme `VALIDÉ`. La CI refuse tout statut de document hors `BROUILLON`, `EN_REVUE` et `VALIDÉ`. La règle figure dans `ARCHITECTURE.md` § 6 (garde-fou 5), dans `templates/_ENTETE.md` et dans R5.
**Pourquoi :** sinon, écrire « VALIDE » sans accent contourne le hook et fait passer un document pour validé.

## 24. Les journaux ne sont jamais validés
**Décision :** `docs/CHANGELOG-REGLES.md` et `docs/decisions/README.md` sont des journaux. Ils ne passent jamais `VALIDÉ`, évoluent uniquement par PR et sont exclus de R6. Leur en-tête reste `statut: EN_REVUE`, avec le commentaire « journal, jamais VALIDÉ ». La règle figure dans R6 (CLAUDE.md), dans `templates/_ENTETE.md` et dans `ARCHITECTURE.md` § 6. Pour la même raison, la colonne « État » des lots passe d'`ARCHITECTURE.md` § 11 au `README.md` ; ARCHITECTURE ne garde que le plan des lots.
**Pourquoi :** un journal figé empêcherait de tracer les décisions suivantes. De même, un document d'architecture qui contient un état d'avancement devrait être dévalidé à chaque lot.

## 25. Protection des templates
**Décision :** les permissions prévues (S3 § 5 et `ARCHITECTURE.md` § 6, garde-fou 6) incluent `ask` sur `Write(templates/**)` et `Edit(templates/**)`.
**Pourquoi :** les templates restent en `BROUILLON` par nature, donc R6 ne les protège pas ; or `tableau.py` et tous les agents dépendent de leur format.

---

## Points reportés (à trancher au lot workflows)
Délais de vérification Render, persistance des données et sauvegardes, mécanisme de rollback. Voir `docs/ARCHITECTURE.md` § 10.

## Impacts
- Fichiers créés au Lot 1 : `CLAUDE.md`, `README.md`, `.gitattributes`, `docs/ARCHITECTURE.md`, `docs/systemes/S1..S4`, `templates/`, `docs/decisions/README.md`, `docs/CHANGELOG-REGLES.md`.
- Règles créées : R1 à R13 (CLAUDE.md) et les règles S1-R*, S2-R*, S3-R*, S4-R*. Entrée initiale dans le CHANGELOG-REGLES.
- Sections 23 à 25 : R5, R6, `_ENTETE.md`, `ARCHITECTURE.md` § 6 et § 11, `README.md`, S3 § 5, en-têtes des deux journaux ; trois entrées dans le CHANGELOG-REGLES.
- Note ajoutée dans S1 (étape d'assignation) : « À définir au Lot 2 (B) : critères d'affectation agent / salarié ».
