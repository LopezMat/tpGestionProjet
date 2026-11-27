---
name: arrivee-membre
description: Traite l'arrivée d'un salarié dans l'ESN : fiche equipe/membres/<prenom>.md en intégration, événement au calendrier, ticket decision, analyse d'impact du chef-de-projet (intégration, formation, affectation progressive, allocation), puis décision humaine. À utiliser quand l'équipe annonce une arrivée.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# arrivee-membre

## Quand l'utiliser
Quand un humain annonce l'arrivée d'un salarié (recrutement, renfort, retour de longue absence).

## Entrées
- prénom, rôle, niveau (`debutant | confirme | expert`), compétences avec niveau, date d'arrivée, capacité (h/semaine), projet(s) visé(s) ;
- `templates/membre.md`, `equipe/agents.md` (référentiel des compétences), `equipe/calendrier.md`, tickets des projets visés.

## Procédure
1. **Collecter les informations** ; demander à l'humain ce qui manque (jamais inventer une compétence ni un niveau).
2. **Coordinateur : créer `equipe/membres/<prenom>.md`** à partir de `templates/membre.md` : `statut: en_integration`, `cout_journalier_eur` selon le niveau (350, 450 ou 550), `date_arrivee`, compétences nommées selon le référentiel, `allocation: {}` (décidée à l'étape 6).
3. **Coordinateur : ajouter l'événement** `arrivee` dans `equipe/calendrier.md` (id `EV-NNN` suivant, `statut: prevu`).
4. **Coordinateur : créer le ticket `decision`** « Arrivée de <prénom> : intégration et affectation » dans `projets/esn-interne/` (procédure `creer-ticket` ; CLAUDE.md § 5, R19), en citant le ou les projets visés : `statut: A_FAIRE`, `assigne: agent:chef-de-projet`, `validation_humaine_requise: oui`.
5. **Lancer `chef-de-projet`** avec le ticket. Il écrit dans la Description :
   - les tickets d'intégration proposés, dans `esn-interne` : environnement, lecture du socle (CLAUDE.md, ARCHITECTURE, S1–S4), binôme avec un salarié confirmé ou expert (repère : 7 h en tout) ;
   - les écarts entre ses compétences et les besoins du projet → tickets `formation` proposés dans `esn-interne` (AF10, S1-R6), et la mise à jour du plan de formation (S1-R13) ;
   - un plan d'affectation progressive : la première semaine, tickets `basse` ou `normale`, à son niveau, en binôme, jamais `critique` (AF7) ;
   - l'allocation proposée par projet, `esn-interne` compris pour l'intégration et les formations, la capacité recalculée, l'effet sur la fin projetée et sur le budget ;
   - puis il passe le ticket `ATTENTE_HUMAIN`.
6. **Arrêt humain.** Après la décision : `tracer-decision` ; le coordinateur applique l'allocation décidée dans la fiche et passe l'événement en `confirme` ; le `chef-de-projet` crée les tickets d'intégration et de formation retenus.
7. **Fin de l'intégration** : quand les tickets d'intégration sont `TERMINE`, le coordinateur passe la fiche en `statut: actif`.

## Règles
- **Le chef-de-projet propose, le coordinateur écrit `equipe/`, l'humain décide.**
  *Pourquoi :* séquence imposée par S1 § 6 ; `equipe/` est hors du périmètre d'écriture des agents (C9).
- **Un salarié `en_integration` ne reçoit ni ticket `critique` ni ticket sans binôme.**
  *Pourquoi :* il ne connaît pas encore les règles ni le code ; une erreur coûterait plus que le temps gagné (AF7).
- **L'allocation reste vide tant que l'humain n'a pas décidé.**
  *Pourquoi :* la répartition entre projets est une décision humaine (S1-R10).
- **L'intégration et les formations sont dans `esn-interne`**, jamais dans un projet client.
  *Pourquoi :* le client ne paie pas la montée en compétence des salariés (DEC-009 E, S1-R6, DEC-023).

## Produit
- `equipe/membres/<prenom>.md` (`en_integration`) et un événement `arrivee` dans le calendrier ;
- un ticket `decision` contenant l'analyse d'impact ;
- après la décision : allocation renseignée, tickets d'intégration et de formation, fichier DEC.

## Point d'arrêt humain
- Allocation et plan d'intégration (ticket `decision` en `ATTENTE_HUMAIN`).

## Contrôles
- [ ] Fiche conforme à `templates/membre.md` (champs non renommés) ; coût cohérent avec le niveau.
- [ ] Événement ajouté au calendrier avec un id unique.
- [ ] Analyse complète : intégration, formations, affectation progressive, allocation, capacité, budget.
- [ ] Aucun ticket critique ni sans binôme pendant l'intégration.
