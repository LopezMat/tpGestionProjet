---
name: absence
description: Traite une absence de salarié (congés, maladie, formation) : événement au calendrier, ticket decision, analyse d'impact du chef-de-projet sur les tickets de la période (réaffecter, décaler, binôme), date de fin recalculée, alerte si un ticket critique ou la deadline est touché, puis décision humaine. À utiliser dès qu'une absence est connue.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# absence

## Quand l'utiliser
Dès qu'une absence d'un salarié est connue, qu'elle soit prévue ou imprévue.

## Entrées
- prénom, date de début, date de fin, type (`conges | maladie | formation | autre`), sans aucun détail personnel ;
- `equipe/membres/<prenom>.md`, `equipe/calendrier.md`, tickets des projets où il est alloué.

## Procédure
1. **Collecter** le prénom, les dates et le type.
2. **Coordinateur : ajouter l'événement** `absence` dans `equipe/calendrier.md` (id `EV-NNN` suivant, `capacite_pct: 0`, `statut: prevu`).
   - Si l'absence commence aujourd'hui : fiche en `statut: conges` ; sinon, la fiche reste `actif` (le calendrier fait foi pour la capacité).
3. **Coordinateur : créer un ticket `decision`** « Absence de <prénom> du <début> au <fin> » dans `projets/esn-interne/` (CLAUDE.md § 5, R19) : `statut: A_FAIRE`, `assigne: agent:chef-de-projet`. La Description liste les projets où le salarié est alloué.
4. **Lancer `chef-de-projet`.** Il écrit dans la Description, pour chaque projet où le salarié est alloué :
   - les tickets du salarié dont la fenêtre prévue chevauche l'absence (S1-R9) ;
   - pour chacun, les options : réaffecter (agent ou salarié selon AF1 à AF10), décaler après le retour, binôme ;
   - la date de fin projetée recalculée et l'écart avec la deadline ;
   - une **alerte** si un ticket `critique` ou la deadline est touché ;
   - « aucun impact » si aucun ticket n'est concerné ;
   - puis il passe le ticket `ATTENTE_HUMAIN`.
5. **Arrêt humain.** Après la décision : `tracer-decision` ; le `chef-de-projet` applique les réaffectations ou décalages (ligne de journal citant le `DEC-NNN`).
6. **Au retour** : le coordinateur repasse la fiche en `statut: actif` et l'événement en `confirme`.

## Règles
- **Un salarié n'est jamais affecté à un ticket qui tombe pendant son absence** (S1-R9).
  *Pourquoi :* sa capacité est nulle sur la période ; l'affectation fausserait le planning.
- **Une décision humaine est demandée même quand l'impact est nul.**
  *Pourquoi :* CLAUDE.md § 5 impose une décision pour tout événement d'équipe ; elle confirme aussi que l'absence est bien enregistrée.
- **Le motif n'est enregistré que sous sa forme générique** (`conges`, `maladie`, `formation`, `autre`).
  *Pourquoi :* une donnée de santé ou personnelle n'a rien à faire dans un dépôt versionné.
- **Le ticket `decision` est dans `esn-interne`**, jamais dans un projet client.
  *Pourquoi :* un événement d'équipe relève de la vie interne de l'ESN ; son analyse n'a pas à peser sur un budget client (DEC-021, DEC-023).

## Produit
- un événement `absence` dans le calendrier (et la fiche en `conges` si l'absence a commencé) ;
- un ticket `decision` dans `esn-interne` avec l'analyse d'impact, projet par projet ;
- après la décision : réaffectations ou décalages, fichier DEC.

## Point d'arrêt humain
- Toujours, même lorsque l'impact est nul.

## Contrôles
- [ ] Événement ajouté avec des dates `AAAA-MM-JJ` et un id unique.
- [ ] Tous les tickets qui chevauchent la période sont listés avec une option.
- [ ] Fin projetée recalculée ; alerte levée si un ticket critique ou la deadline est touché.
- [ ] Aucune donnée personnelle au-delà du type générique.
