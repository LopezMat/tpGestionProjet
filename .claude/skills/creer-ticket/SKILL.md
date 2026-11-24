---
name: creer-ticket
description: Crée un ticket conforme à templates/ticket.md dans projets/<slug>/tickets/ (id, nom de fichier, champs, règles par type, contrôles d'assigné et de dépendances). À utiliser par le coordinateur, et comme procédure de référence par le chef-de-projet et les autres agents qui créent des tickets.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# creer-ticket

## Quand l'utiliser
Chaque fois qu'un ticket doit être créé : découpage, ticket de travail, ticket `decision`, `formation`, `amelioration`, bug, incident, support, revue humaine ou binôme.

## Entrées
- `slug` du projet (le dossier `projets/<slug>/` doit exister) ;
- `type`, `titre`, `priorite`, `assigne`, `estimation_h`, `depend_de`, critères d'acceptation ;
- la compétence requise (nom du référentiel d'`equipe/agents.md` et niveau) ;
- `cree_par` (`agent:<nom>` ou `salarie:<prenom>` ; le coordinateur écrit `agent:coordinateur`).

## Procédure
1. **Vérifier le dossier** `projets/<slug>/tickets/` (le créer s'il n'existe pas).
2. **Calculer l'id** : plus grand `T-NNN` présent dans `projets/<slug>/tickets/` + 1, sur 3 chiffres (`T-001` pour le premier). Un id n'est jamais réutilisé, même si un ticket est `ANNULE`.
3. **Nommer le fichier** `T-NNN-<titre-court>.md` : minuscules, tirets, sans accents, 5 mots au plus.
4. **Copier `templates/ticket.md`** (v0.2) : aucun champ du frontmatter renommé, ajouté ou supprimé ; la ligne de provenance est gardée ; `cree_le`, `maj_le` et `statut_depuis` à la date du jour ; `temps_passe_h: 0` ; **`competence_requise: <nom> (<niveau>)`** rempli avec un nom du référentiel d'`equipe/agents.md` ; `debut_le` et `termine_le` laissés vides (ils sont remplis au premier `EN_COURS` et au passage `TERMINE`).
5. **Écrire la Description** : le contexte et l'attendu. La compétence n'y est plus recopiée : elle est dans le champ `competence_requise`.
6. **Appliquer les règles du type** :
   - `decision` : `statut: ATTENTE_HUMAIN` (ou `A_FAIRE` s'il est créé vide pour une analyse d'impact du chef-de-projet), `validation_humaine_requise: oui`, `bloque_par` renseigné, `decision` vide. Description au format R7 : **question**, **options**, **recommandation**, **impact**. Critères : document ou arbitrage validé par un humain ; fichier `DEC-NNN` créé.
   - `formation` : `assigne: salarie:<prenom>`, compétence, niveau visé, ticket déclencheur, modalité proposée (binôme interne, autoformation, formation externe), coût estimé.
   - `bug` : étapes de reproduction, résultat attendu, résultat obtenu, environnement.
   - `incident` : symptôme, heure de détection, impact utilisateur, runbook concerné.
   - `priorite: critique` ou ticket qui touche la sécurité : dans la section Revue, « Revue humaine requise : oui », et création du ticket compagnon « Revue humaine T-NNN » ou « Binôme T-NNN » (critères AF3 et AF5 du `chef-de-projet`).
7. **Contrôler l'assigné** :
   - `agent:<nom>` : `.claude/agents/<nom>.md` existe ;
   - `salarie:<prenom>` : `equipe/membres/<prenom>.md` existe, `statut` différent de `parti`, allocation au projet > 0, pas d'absence du calendrier sur la fenêtre prévue (S1-R9), pas de `date_depart` dépassée.
8. **Contrôler les dépendances** : chaque id de `depend_de` existe dans le projet, et le nouveau ticket ne crée pas de cycle.
9. **Ajouter la ligne de journal** : `AAAA-MM-JJ HH:MM · <cree_par> · création · 0 h`.

## Règles
- **Le format du template est intouchable** : aucun champ renommé ni ajouté par rapport à `templates/ticket.md` v0.2 (DEC-002 a ajouté `competence_requise`, `statut_depuis`, `debut_le`, `termine_le`).
  *Pourquoi :* `scripts/tableau.py` lit ces champs ; un écart casse le tableau de bord. Toute évolution du format passe par R11.
- **Les dates de travail suivent le statut** : quiconque change le statut d'un ticket met `statut_depuis` à la date du jour, `debut_le` au premier `EN_COURS`, `termine_le` au passage `TERMINE`.
  *Pourquoi :* sans elles, `tableau.py` estime l'ancienneté d'un blocage et les barres du Gantt à partir de `maj_le`, qu'une simple correction de faute fait bouger.
- **`bloque_par` est obligatoire en `BLOQUE` et en `ATTENTE_HUMAIN`** (S1-R3).
  *Pourquoi :* un blocage sans raison ne peut être levé par personne.
- **Les critères d'acceptation sont vérifiables** (observable, mesurable, testable), jamais « fonctionne bien ».
  *Pourquoi :* un ticket ne passe `TERMINE` que si tous ses critères sont cochés (R13).
- **Personne n'écrit `statut: TERMINE` à la création**, et seul un humain renseigne `decision`.
  *Pourquoi :* « terminé » veut dire « vérifié », et la décision est humaine (R5, R7).

## Produit
- `projets/<slug>/tickets/T-NNN-<titre-court>.md` ;
- le cas échéant, le ticket compagnon de revue humaine ou de binôme.

## Point d'arrêt humain
- Aucun pour un ticket ordinaire.
- Ticket `decision` en `ATTENTE_HUMAIN` : le coordinateur s'arrête et présente à l'humain la question, les options, la recommandation et l'impact (R7).

## Contrôles
- [ ] Id unique et séquentiel ; nom de fichier conforme.
- [ ] Frontmatter identique au template, champs remplis, dates du jour (`cree_le`, `maj_le`, `statut_depuis`).
- [ ] `competence_requise` rempli avec un nom du référentiel ; critères vérifiables.
- [ ] Assigné existant et disponible ; dépendances existantes et sans cycle.
- [ ] `bloque_par` renseigné si `BLOQUE` ou `ATTENTE_HUMAIN` ; ligne de journal de création.
