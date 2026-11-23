---
name: revision-budget
description: Traite une révision du budget (ou de la deadline) d'un projet : ticket decision, recalcul de la projection par le chef-de-projet, scénarios chiffrés (retirer des fonctionnalités, réaffecter, décaler, maintenir), arbitrage humain, puis mise à jour de projet.md et des tickets. À utiliser quand le client ou l'ESN change le budget ou la deadline.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# revision-budget

## Quand l'utiliser
Quand un humain annonce un nouveau budget ou une nouvelle deadline pour un projet (demande du client, décision de l'ESN).

## Entrées
- le nouveau budget en € (et la nouvelle deadline si elle change), avec sa source (client, direction) ;
- `projets/<slug>/projet.md`, `cdc.md`, `tickets/`, `TABLEAU.md` ;
- `equipe/` (taux et capacités).

## Procédure
1. **Collecter** le nouveau budget, la deadline éventuelle et la source.
2. **Coordinateur : lancer `avancement`** pour disposer de chiffres à jour.
3. **Coordinateur : créer le ticket `decision`** « Révision du budget : <ancien> € → <nouveau> € » : `statut: A_FAIRE`, `assigne: agent:chef-de-projet`, `priorite: haute`.
4. **Lancer `chef-de-projet`.** Il écrit dans la Description :
   - le consommé, le reste à faire (h et €, au taux de chaque assigné) et la projection face au nouveau budget et à la deadline ;
   - les scénarios chiffrés (coût, délai, périmètre, risque, qualité) :
     - **A · retirer des fonctionnalités** Should ou Could (liste des `F-NN`, tickets concernés, gain) ;
     - **B · réaffecter** des tickets d'un salarié vers un agent, uniquement là où AF1 à AF5 le permettent (gain, risque) ;
     - **C · décaler la deadline** (nouvelle date, effet sur la capacité) ;
     - **D · maintenir** le périmètre et dépasser le budget (montant du dépassement) ;
   - sa recommandation ;
   - puis il passe le ticket `ATTENTE_HUMAIN`.
5. **Arrêt humain.** Après la décision : `tracer-decision`, puis :
   - `budget_eur` (et `deadline`) mis à jour dans `projet.md` par le coordinateur ; si `projet.md` est `VALIDÉ`, c'est l'humain qui le repasse `EN_REVUE` ou le modifie lui-même ;
   - les tickets retirés passent `ANNULE` (jamais supprimés), avec une ligne de journal citant le `DEC-NNN` ;
   - les réaffectations sont appliquées par le `chef-de-projet` ;
   - si le périmètre du CDC change : l'humain repasse `cdc.md` en `EN_REVUE`, et l'`analyste-besoin` le révise.

## Règles
- **Au moins deux scénarios chiffrés, dont un qui respecte le nouveau budget.**
  *Pourquoi :* un arbitrage n'en est un que s'il y a un vrai choix (S1-R11).
- **Une réaffectation vers un agent ne contourne jamais AF1 à AF5.**
  *Pourquoi :* économiser sur le contact client, la décision ou la revue humaine reviendrait à supprimer la supervision.
- **Un ticket retiré est `ANNULE`, jamais supprimé.**
  *Pourquoi :* l'historique du périmètre reste lisible, et le tableau de bord exclut les tickets `ANNULE` de l'avancement.
- **Le CDC validé n'est modifié qu'après sa réouverture par un humain** (R6).
  *Pourquoi :* ce qui est appliqué doit rester ce qui a été validé.

## Produit
- un ticket `decision` avec la projection et les scénarios ;
- après la décision : `projet.md` mis à jour, tickets `ANNULE` ou réaffectés, fichier DEC, révision éventuelle du CDC.

## Point d'arrêt humain
- Toujours : arbitrage entre les scénarios.

## Contrôles
- [ ] Projection calculée avec les taux réels (15 €/h agent, coût journalier ÷ 7 pour un salarié).
- [ ] Chaque scénario a son coût, son délai, son périmètre et son risque.
- [ ] Après la décision : budget, tickets et CDC cohérents entre eux.
