---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-002
titre: Formation Nadia — supervision (journée du 2026-12-03, EV-002)
projet: esn-interne
type: formation             # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:nadia      # agent:<nom> | salarie:<prenom>
competence_requise: supervision (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
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

# T-002 — Formation Nadia — supervision (journée du 2026-12-03, EV-002)

## Description
Ticket du plan de formation de l'ESN (S1-R13, [planning.md](../planning.md), registre R-09). Proposé par T-001, **retenu par [DEC-024](../../../docs/decisions/2026-11-27-DEC-024-plan-formation-initial.md) (option B), rang 3 de priorité**. Allocation de Nadia à `esn-interne` : 10 % en P1, appliquée le 2026-11-27. Prenable dès que T-017 est `TERMINE` (à conclure par le coordinateur **avant le 2026-12-03**).

- **Compétence** : `supervision` ; **niveau actuel** : débutant ; **niveau visé** : confirmé (fiche de Nadia).
- **Candidate** : Nadia.
- **Déclencheur** : EV-002 (journée de formation au calendrier, le 2026-12-03) ; DEC-009 point E (« elle ne sert pas ce client », donc hors `reservation-coworking`).
- **Pourquoi** : aucun salarié n'est `confirme` en `supervision` (AF10 a). La crise T-080 (DEC-019) a montré qu'une sauvegarde non vérifiée n'est pas une garantie ; la vérification quotidienne avec alerte (`reservation-coworking/T-092`) relève de cette compétence.
- **Modalité** : formation externe d'une journée, le **2026-12-03** (date fixe). Nadia travaille 7 h ce jeudi (temps partiel 4/5, pas de travail le mercredi).
- **Coût** :
  - temps salarié : 7 h × 64,29 €/h = **450,00 €** (compté par `tableau.py`) ;
  - frais externes : **inconnus**, à confirmer par devis (0 € si la session est déjà réglée ou gratuite). Ils ne sont pas comptés par `tableau.py` : **enveloppe séparée de 700 € HT** (DEC-024 point 4), suivie dans la section « Enveloppe de frais externes » de [planning.md](../planning.md). Chaque mouvement (devis, engagement, facture) y est reporté avec une ligne de journal ici ; toute dépense au-delà de l'enveloppe passe par une nouvelle décision humaine.
- **Note de calcul** : EV-002 met la capacité de Nadia à 0 le 2026-12-03 ; `tableau.py` place donc ce ticket sur d'autres jours (alerte « Absence » de `TABLEAU.md`, artefact analysé dans `planning.md`). Le coût est juste ; la date réelle est le 2026-12-03. **Pour que le tableau soit juste**, Nadia passe ce ticket `EN_COURS` puis `TERMINE` avec `debut_le` et `termine_le` au 2026-12-03 : le Gantt utilise alors ces dates et l'alerte disparaît.
- **Si DEC-024 n'est pas prise avant le 2026-12-03**, ce ticket ne peut pas être pris (`depend_de: T-017`) : le coordinateur peut demander un arbitrage séparé et anticipé de ce seul point.

## Critères d'acceptation
- [ ] Nadia a suivi la journée du 2026-12-03 ; l'attestation de présence est mentionnée au journal (sans donnée personnelle).
- [ ] Une restitution de 10 lignes au plus est écrite au journal : ce qui s'applique à la vérification des sauvegardes et aux alertes de la production locale Docker.
- [ ] Le temps passé (heures équivalent humain) et les frais externes réels sont reportés au journal.
- [ ] Le niveau atteint est proposé ; la fiche de Nadia est mise à jour par le coordinateur après décision humaine (CLAUDE.md § 5).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (formation)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:00 · agent:chef-de-projet · création (T-001, plan de formation initial ; registre R-09 ; EV-002) ; en attente de DEC-024 (T-017) · 0 h
- 2026-11-27 14:30 · agent:chef-de-projet · retenu par DEC-024 (option B, rang 3) ; frais externes dans l'enveloppe séparée de 700 € HT (devis à obtenir avant le 2026-12-03, 0 € engagé) ; date réelle 2026-12-03 (debut_le, termine_le) (T-016) · 0 h
