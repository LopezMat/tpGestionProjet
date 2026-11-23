---
name: avancement
description: Régénère les tableaux de bord avec scripts/tableau.py et présente à l'humain une synthèse de l'avancement, du budget, des délais, des blocages, des attentes humaines, de l'utilisation des salariés et des besoins de formation. À utiliser après chaque étape du pipeline, sur demande de l'équipe, ou avant une décision.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# avancement

## Quand l'utiliser
- Après chaque étape du pipeline (CLAUDE.md § 1) ;
- quand l'équipe demande « où en est-on ? » ;
- avant de présenter une décision de budget, de délai ou d'événement d'équipe.

## Entrées
- `projets/*/tickets/`, `projets/*/projet.md` ;
- `equipe/membres/*.md`, `equipe/agents.md`, `equipe/calendrier.md`.

## Procédure
1. **Coordinateur** : lancer `python scripts/tableau.py`.
   - Si le script n'existe pas encore (Lot 4) : appliquer à la main les formules d'ARCHITECTURE § 7 en lisant les tickets, **sans écrire** `TABLEAU.md` ni `PORTFOLIO.md`, et le dire dans la synthèse.
2. **Lire** `PORTFOLIO.md` et le `TABLEAU.md` du ou des projets concernés.
3. **Rédiger la synthèse** pour l'humain, par projet :
   - avancement (% des heures estimées terminées) et tickets par statut ;
   - budget consommé / prévu (€ et %) ; temps restant ; fin projetée / deadline ;
   - tickets `ATTENTE_HUMAIN`, triés par priorité, avec la question posée ;
   - tickets `BLOQUE`, avec `bloque_par` et l'ancienneté ;
   - alertes : budget > 90 %, deadline dépassée en projection, ticket critique ouvert, ticket `EN_COURS` sans mise à jour depuis plus de 2 jours ouvrés, préavis de départ < 5 jours ouvrés ;
   - **utilisation des salariés** : h assignées / capacité allouée sur la période, en signalant les taux < 50 % (indicateur AF9) ;
   - **tickets `salarie:` en attente d'un humain** (AF11) ;
   - tickets `formation` et `amelioration` ouverts ;
   - événements d'équipe à venir (calendrier).
4. **Si une alerte S1-R11 est levée** (budget > 90 % ou fin projetée après la deadline) : lancer `chef-de-projet` pour les scénarios ; il crée le ticket `decision` en `ATTENTE_HUMAIN`.
5. **Annoncer** : ce qui a été produit, ce qui bloque, ce qui attend une décision, la prochaine étape (CLAUDE.md § 2).

## Règles
- **Personne n'écrit `TABLEAU.md` ni `PORTFOLIO.md` à la main** (R9).
  *Pourquoi :* les tickets sont la seule source de vérité ; un tableau retouché ment.
- **La synthèse reprend les chiffres du script, sans les arrondir à son avantage** ; un écart avec la deadline ou le budget est dit tel quel.
  *Pourquoi :* le contrôle du budget et des délais n'a de valeur que s'il est honnête.
- **Les tickets salariés en attente sont toujours listés à part.**
  *Pourquoi :* le coordinateur ne les réalise pas (AF11) ; s'ils ne sont pas visibles, ils bloquent le projet en silence.

## Produit
- `TABLEAU.md` et `PORTFOLIO.md` régénérés par le script (jamais à la main) ;
- une synthèse à l'humain, en conversation ;
- le cas échéant, un ticket `decision` d'alerte créé par le `chef-de-projet`.

## Point d'arrêt humain
- Alerte S1-R11 : arrêt sur le ticket `decision` de scénarios.
- Tout ticket `ATTENTE_HUMAIN` ouvert : le coordinateur le présente (R7) et attend.

## Contrôles
- [ ] Script lancé (ou calcul manuel signalé) ; aucun fichier généré écrit à la main.
- [ ] Toutes les rubriques de la synthèse sont présentes, même vides (« aucun »).
- [ ] Chaque alerte a une suite : ticket existant, ticket créé ou décision demandée.
