---
name: tracer-decision
description: Prépare le fichier docs/decisions/AAAA-MM-JJ-DEC-NNN-<sujet>.md à partir d'une décision exprimée par un humain (validation de document, arbitrage, événement d'équipe, GO de mise en production, modification de règle), ajoute la ligne d'index et remet à l'humain sa liste de vérification. À utiliser dès qu'un humain a tranché un ticket ATTENTE_HUMAIN.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# tracer-decision

## Quand l'utiliser
Quand un humain a exprimé sa décision sur un ticket `ATTENTE_HUMAIN` (R7) ou sur un arbitrage d'équipe, et qu'il faut la tracer dans `docs/decisions/`.

## Entrées
- la décision **telle que l'humain l'a formulée** : qui décide, ce qui est décidé, pourquoi ;
- le ticket `decision` concerné (question, options, recommandation) ;
- `templates/decision.md`, `docs/decisions/README.md`.

## Procédure
1. **Vérifier que la décision vient d'un humain** et qu'elle contient un *pourquoi*. S'il manque, le demander ; ne jamais le rédiger à sa place.
2. **Calculer l'id** : plus grand `DEC-NNN` présent dans `docs/decisions/` + 1 ; un numéro n'est jamais réutilisé.
3. **Créer `docs/decisions/AAAA-MM-JJ-DEC-NNN-<sujet-court>.md`** à partir du template :
   - `statut: EN_REVUE`, `valide_par` vide, `decision: DEC-NNN`, `responsable` = lettre de la personne concernée ;
   - `decide_par`, `projet` (slug ou `ESN`), `ticket` (T-NNN), `modifie_une_regle` ;
   - Contexte (repris du ticket), Options étudiées (celles du ticket), Décision (formulée comme une règle applicable), Pourquoi (celui de l'humain), Impacts (fichiers, règles, tickets).
4. **Ajouter une ligne à l'index** de `docs/decisions/README.md` (statut « EN_REVUE »).
5. **Si `modifie_une_regle: oui`** : préparer la ligne de `docs/CHANGELOG-REGLES.md` (date, règle, ancien, nouveau, pourquoi, déclencheur, décision) et rappeler que la modification passe par une PR (R11).
6. **Remettre à l'humain sa liste de vérification** :
   - relire le fichier DEC, puis y écrire soi-même `statut: VALIDÉ` et `valide_par` ;
   - dans le ou les documents concernés : `statut: VALIDÉ`, `valide_par`, `decision: DEC-NNN`, `version` incrémentée ;
   - dans le ticket : `decision: DEC-NNN`, puis le débloquer (statut suivant, ligne de journal) ;
   - mettre à jour la ligne d'index ; commit dans une PR.
7. **Après le déblocage par l'humain** : appliquer ce que la décision prévoit (réaffectations, mises à jour d'`equipe/`, tickets à créer) ou relancer l'agent concerné, en citant le `DEC-NNN`.

## Règles
- **On ne trace qu'une décision réellement prise par un humain, avec ses mots.**
  *Pourquoi :* une décision rédigée par l'IA et présentée comme humaine détruirait la supervision (R5, R7).
- **Le fichier DEC est créé en `EN_REVUE` ; seul l'humain le passe `VALIDÉ`.**
  *Pourquoi :* R5 ; le hook bloque de toute façon l'écriture de `VALIDÉ`.
- **Le coordinateur ne débloque jamais le ticket et ne remplit pas son champ `decision`.**
  *Pourquoi :* seul un humain débloque une attente humaine (R7, procédure du registre).
- **Une décision peut couvrir plusieurs documents ou tickets** ; on ne la duplique pas.
  *Pourquoi :* une seule trace par arbitrage, liée par l'id (DEC-001 § 9).

## Produit
- `docs/decisions/AAAA-MM-JJ-DEC-NNN-<sujet>.md` (EN_REVUE) ;
- une ligne dans l'index de `docs/decisions/README.md` ;
- le cas échéant, une ligne préparée pour `docs/CHANGELOG-REGLES.md` ;
- la liste de vérification remise à l'humain.

## Point d'arrêt humain
- Toujours : l'humain valide le DEC et les documents, renseigne le ticket et le débloque. Le coordinateur attend avant d'appliquer la décision.

## Contrôles
- [ ] Id séquentiel, jamais réutilisé ; nom de fichier conforme.
- [ ] Le *pourquoi* est celui de l'humain ; options et contexte repris du ticket.
- [ ] Aucun `statut: VALIDÉ` ni `valide_par` écrit par le coordinateur.
- [ ] Index mis à jour ; changelog préparé si une règle change.
