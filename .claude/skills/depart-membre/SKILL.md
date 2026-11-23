---
name: depart-membre
description: Traite le départ annoncé d'un salarié : calcul du préavis en jours ouvrés, fiche en depart_prevu, événement au calendrier, plan de passation du chef-de-projet (tickets, connaissances, transfert, réaffectation, formation ou recrutement), puis décision humaine. À utiliser dès qu'un départ est connu, au moins 5 jours ouvrés avant la date.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# depart-membre

## Quand l'utiliser
Dès qu'un humain annonce le départ d'un salarié (démission, fin de mission, mutation).

## Entrées
- prénom et date de départ (aucun motif personnel n'est enregistré) ;
- `equipe/membres/<prenom>.md`, `equipe/membres/*.md`, `equipe/calendrier.md` ;
- tickets de tous les projets où il est alloué.

## Procédure
1. **Collecter** le prénom et la date de départ.
2. **Calculer le préavis** en jours ouvrés, de demain à la date de départ incluse, hors samedis, dimanches et `jours_feries` du calendrier.
   - Si le préavis est **inférieur à 5 jours ouvrés** : passation accélérée et ticket `decision` dédié « Préavis court : <prénom> » en `ATTENTE_HUMAIN`, `priorite: haute` (S1-R8). L'alerte apparaît aussi au tableau de bord.
3. **Coordinateur : mettre à jour la fiche** : `statut: depart_prevu`, `date_depart`, `maj_le` ; ajouter l'événement `depart` au calendrier.
4. **Coordinateur : créer un ticket `decision`** « Départ de <prénom> : plan de passation » dans chaque projet où il est alloué : `statut: A_FAIRE`, `assigne: agent:chef-de-projet`.
5. **Lancer `chef-de-projet`, une fois par projet.** Il écrit dans la Description :
   - les tickets ouverts du partant (statut, reste à faire, fenêtre prévue) ;
   - ses connaissances : tickets terminés dont il est l'auteur, compétences où il est le seul au niveau `confirme` ou plus (risque de perte) ;
   - les tickets de transfert proposés : documentation, binôme avec le repreneur, revue croisée ;
   - la réaffectation de chaque ticket selon AF1 à AF10 (aucun ticket ne doit rester au partant au-delà de sa date) ;
   - le planning recalculé (capacité, fin projetée, budget) ;
   - si une compétence n'existe plus dans l'équipe : ticket `formation` ou option « recrutement » ;
   - puis il passe le ticket `ATTENTE_HUMAIN`.
6. **Arrêt humain.** Après la décision : `tracer-decision` ; le `chef-de-projet` applique les réaffectations (ligne de journal citant le `DEC-NNN`) et crée les tickets de transfert retenus.
7. **À la date de départ** : le coordinateur passe la fiche en `statut: parti`, `allocation: {}`, et l'événement en `confirme`.

## Règles
- **La passation démarre au moins 5 jours ouvrés avant le départ** ; en dessous, un humain arbitre le risque (S1-R8).
  *Pourquoi :* une semaine de travail permet de documenter, de faire travailler un binôme et de réaffecter.
- **Aucune réaffectation avant la décision humaine.**
  *Pourquoi :* le choix du repreneur engage la charge d'un autre salarié et le budget.
- **Le motif du départ n'est jamais écrit dans le dépôt.**
  *Pourquoi :* donnée personnelle sans utilité pour le pilotage, et le dépôt est versionné de façon permanente.
- **Une compétence portée par le seul partant devient un ticket `formation` ou une option de recrutement.**
  *Pourquoi :* la consigne demande de rendre visibles les manques de compétences (S1-R6).

## Produit
- fiche en `depart_prevu` puis `parti`, événement `depart` au calendrier ;
- un ticket `decision` par projet avec le plan de passation ; le cas échéant, le ticket « Préavis court » ;
- après la décision : réaffectations, tickets de transfert, tickets `formation`, fichier DEC.

## Point d'arrêt humain
- Toujours : plan de passation.
- Préavis inférieur à 5 jours ouvrés : ticket `decision` dédié.

## Contrôles
- [ ] Préavis calculé en jours ouvrés, jours fériés exclus.
- [ ] Tous les tickets ouverts du partant ont une proposition de repreneur ou de décalage.
- [ ] Aucun ticket ne reste assigné au partant au-delà de sa date de départ.
- [ ] Compétences orphelines identifiées et traitées (formation ou recrutement).
