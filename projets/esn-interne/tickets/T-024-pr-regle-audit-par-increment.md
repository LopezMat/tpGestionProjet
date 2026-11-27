---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-024
titre: Préparation de la PR de règles A6 (DEC-025) — règle 6 du chef-de-projet, un audit sécurité par incrément plus l'audit avant GO (R11)
projet: esn-interne
type: amelioration          # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:chef-de-projet   # agent:<nom> | salarie:<prenom>
competence_requise: gestion-projet (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné (DEC-025, A6)
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
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

# T-024 — Préparation de la PR de règles A6 (DEC-025) : audit sécurité par incrément

## Description
Ticket créé en application de [DEC-025](../../../docs/decisions/2026-11-27-DEC-025-actions-retrospective-semaine.md) (option 2, action **A6**, priorité normale), à partir du constat **P6** du [retex de l'ESN](../retex.md) : `reservation-coworking/T-043` était estimé à 5 h pour un seul passage, et 12,5 h ont été passées en 7 audits d'incrément (DEC-011), sans ré-estimation ; l'audit avant GO n'était alors compté nulle part. Le cas a été arbitré dans le projet client par [DEC-026](../../../docs/decisions/2026-11-27-DEC-026-audit-securite-increments-esn.md) (T-043 « Audits d'incrément », nouveau ticket « Audit sécurité avant GO »), qui renvoie la règle à cette action.

**Contenu retenu par DEC-025.** Règle 6 de `.claude/agents/chef-de-projet.md` : un ticket « Audit sécurité » par livraison incrémentale (méthode de DEC-022), **plus** l'audit avant GO, estimés séparément ; une décision qui ajoute un incrément (comme DEC-011) entraîne une ré-estimation au même triage.

**Attendu (préparation du `chef-de-projet`).**
1. Le texte proposé, avant / après, de la règle 6 et de la case correspondante des « Contrôles avant de rendre la main ».
2. Le recensement des autres documents qui décrivent un seul audit par projet (`docs/systemes/`, `.claude/agents/`, skills), avec le texte proposé pour chacun, ou « aucun ».
3. La vérification que la règle proposée ne fixe **aucune imputation d'office** : la prise en charge par l'ESN d'audits d'incrément reste décidée au cas par cas, comme DEC-026 (R18).
4. La ligne proposée de `docs/CHANGELOG-REGLES.md` et le ticket `decision` « Modification de règle » `ATTENTE_HUMAIN` (R7, R11). La PR est faite par le coordinateur, relue par B (DEC-025).

**Hors périmètre (R11).** Aucune modification de `.claude/` ni de `docs/` dans ce ticket (ni du fichier de cet agent : règle 11 du `chef-de-projet`) : il prépare la PR de règles.

## Critères d'acceptation
- [ ] Le texte proposé (avant / après) de la règle 6 et de la case correspondante des « Contrôles avant de rendre la main » de `.claude/agents/chef-de-projet.md` est écrit dans ce ticket.
- [ ] Les autres documents qui décrivent un seul audit par projet sont recensés (recherche dans `docs/systemes/`, `.claude/agents/` et `.claude/skills/`), avec le texte proposé pour chacun ou la mention « aucun ».
- [ ] Le texte proposé ne contient aucune imputation d'office (`imputation: esn` reste soumis à une décision `VALIDÉ`, R18).
- [ ] La ligne proposée de `docs/CHANGELOG-REGLES.md` est écrite, et un ticket `decision` « Modification de règle » est créé en `ATTENTE_HUMAIN` dans `projets/esn-interne/tickets/`, au format R7.
- [ ] Aucune modification de `.claude/` ni de `docs/` dans ce ticket (R11).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (préparation de règle ; relecture humaine par B dans la PR)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:56 · agent:chef-de-projet · création (DEC-025, action A6) · 0 h
