---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-003
titre: Formation Léa — securite-applicative (1/2) autoformation guidée
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:lea        # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (debutant)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 7             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-017]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: esn             # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-003 — Formation Léa — securite-applicative (1/2) autoformation guidée

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-02). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 1 de priorité**. Allocation de Léa à `esn-interne` : 25 % en P1, appliquée le 2026-11-27.

- **Compétence** : `securite-applicative` ; **niveau actuel** : aucun ; **niveau visé à la fin de ce ticket** : débutant. Le niveau confirmé est visé à la fin de [T-004](T-004-formation-revue-humaine-lea.md).
- **Candidate** : Léa. Elle est la seule salariée sans allocation (capacité disponible), elle n'est l'auteure d'aucun ticket de `reservation-coworking` (relectrice indépendante possible), et la sécurité du front (XSS, CSP, en-têtes, sessions côté navigateur) prolonge ses compétences `javascript` et `react`.
- **Déclencheur** : DEC-021 (le candidat de l'ex-`reservation-coworking/T-053`, Hugo, part le 2026-12-04) ; AF10 b (Karim seul titulaire) ; EV-003 (congés de Karim du 2026-12-21 au 31).
- **Modalité** : autoformation guidée, sans frais : OWASP Top 10, aide-mémoire OWASP (authentification, sessions, stockage des mots de passe, en-têtes HTTP), OWASP ASVS (chapitres authentification, sessions, contrôle d'accès), exercices gratuits en ligne (laboratoires d'injection et de XSS) ; lecture des rapports `securite-*` de `reservation-coworking`. Variante non chiffrée : formation externe inter-entreprises, sur devis.
- **Fenêtre** : du 2026-11-30 (retour de Léa, EV-001) au 2026-12-04.
- **Coût** : 7 h × 64,29 €/h = **450,00 €** ; frais externes : 0 €.

## Critères d'acceptation
- [ ] Léa a rédigé une grille de relecture « authentification, sessions, autorisations, en-têtes » d'une page, dans `projets/esn-interne/` ; Karim l'a relue (ligne au journal).
- [ ] Léa a lu au moins deux rapports `securite-*` de `reservation-coworking` et note au journal, pour chacun, un constat qu'elle saurait retrouver seule.
- [ ] Le temps passé (heures équivalent humain) est reporté au journal ; le niveau atteint (débutant) est proposé.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:05 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-02 ; DEC-021, ex-T-053) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 1) ; fenêtre inchangée, du 2026-11-30 au 2026-12-04 (T-016) · 0 h
