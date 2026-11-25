---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-003
titre: Validation du CDC
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: TERMINE      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:analyste-besoin        # agent:<nom> | salarie:<prenom>
competence_requise: redaction-cdc (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-001]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: oui   # oui | non
decision:   DEC-006                # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:analyste-besoin
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le: 2026-11-24      # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-003 — Validation du CDC

## Description
**Question.** Le cahier des charges [cdc.md](../cdc.md) (version 0.1, `EN_REVUE`) du projet `reservation-coworking` peut-il être validé comme base de l'architecture, de la planification et du développement ?

**Options.**
1. **Valider en l'état** : le périmètre Must est F-01 (disponibilités et réservation), F-02 (annulation) et F-03 (vue de l'accueil). Les questions ouvertes restent suivies avec leurs hypothèses par défaut. Rapide, mais risque de reprise si une réponse change le périmètre.
2. **Faire répondre le client aux questions bloquantes (Q-01, Q-03, Q-04, Q-07, Q-08, Q-12) puis valider** : le CDC repasse par l'analyste (révision, v0.2) avant validation.
3. **Refuser et demander un changement de périmètre** (par exemple ajouter paiement, notifications en Must, ou retirer une fonctionnalité).

**Recommandation.** Option 2, avec réponses du client sous 3 jours (avant le 2026-11-27) : les six questions bloquantes conditionnent l'authentification, les règles métier, la vue de l'accueil et le RGPD, et donc l'architecture. La deadline du 2026-12-18 laisse peu de marge pour une reprise tardive. Les autres questions (Q-02, Q-05, Q-06, Q-09, Q-10, Q-11, Q-13) peuvent suivre avec leurs hypothèses (H-01 à H-09).

**Impact.**
- Questions ouvertes : **13**, dont **6 bloquantes**.
- 9 hypothèses listées au § 11 ; H-03 (base légale RGPD) et H-08 (maintenance non incluse) à confirmer.
- Délai : environ 18 jours ouvrés avant la deadline ; chaque jour sans réponse réduit le temps de développement et de recette.
- Budget : 6 000 € repris tels quels (HT ou TTC non précisé, Q-09). La validation du budget et des délais reste une étape distincte (planning).
- Tant que le CDC n'est pas `VALIDÉ`, l'`architecte` ne peut pas démarrer (R4, S4-R4).

### Mise à jour du 2026-11-24 (coordinateur) : option 2 retenue, CDC v0.2
Ethan a retenu l'option 2 ; les réponses du client (transmises par Claire) sont intégrées au [CDC v0.2](../cdc.md). La décision est préparée dans [DEC-006](../../../docs/decisions/2026-11-24-DEC-006-validation-cdc-coworking.md) (`EN_REVUE`).

**Question restante.** Le CDC v0.2 peut-il être validé ? Deux points sont à trancher en même temps :
1. **Nombre de Must : 6** (F-01 à F-04, F-07 rôle accueil, F-08 purge à 12 mois), contre 2 ou 3 visés par S4-R5.
   - **A.** Garder les 6 Must.
   - **B.** Passer F-08 (purge à 12 mois) en Should : aucune donnée n'aura 12 mois avant fin 2027 ; livrable avant la mise en ligne si le client l'exige.
   - *Recommandation : B*, qui allège le premier lot sans renoncer à l'obligation du client (à confirmer avec Claire auprès de Marie Lenoir).
2. **Hypothèses de l'ESN H-10 à H-17** (§ 11 du CDC) : avance de 14 jours comptée de J à J+14, créneau commencé non réservable, annulation qui libère le quota, 12 mois comptés depuis la date du créneau, effets de la suppression de compte, pas de modification ni de création de réservation par l'accueil, comptes accueil créés hors de l'application, fuseau Europe/Paris sans jours fériés. *Recommandation : les accepter telles quelles.*

**Points restés ouverts, non bloquants pour la validation** : Q-14 (comptes accueil) et Q-18 (réinitialisation du mot de passe, forcément par l'accueil sans e-mail) à trancher avant les tickets d'authentification ; Q-15, Q-16, Q-17.

**Impact mis à jour.** 13 questions initiales répondues ou acceptées ; 5 nouvelles questions non bloquantes. L'authentification et le rôle accueil ajoutent environ 15 à 25 h (estimation indicative de l'analyste, à confirmer par le `chef-de-projet`) et des revues humaines obligatoires (S3-R2). Budget précisé : 6 000 € HT, maintenance hors budget.

## Critères d'acceptation
- [ ] `cdc.md` passé `VALIDÉ` par un humain (`valide_par` renseigné).
- [ ] Fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` créé et référencé dans le champ `decision`.
- [ ] Questions ouvertes répondues ou arbitrées (au minimum les 6 bloquantes).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 14:30 · agent:analyste-besoin · création, statut ATTENTE_HUMAIN · 0 h
- 2026-11-24 16:00 · agent:analyste-besoin · CDC révisé en v0.2 (réponses du client transmises par Claire, option 2) ; statut du ticket inchangé, validation humaine de la v0.2 en attente · 0 h
- 2026-11-24 16:10 · agent:coordinateur · description mise à jour pour la v0.2 (points F-08 et H-10 à H-17), DEC-006 préparée en EN_REVUE ; statut inchangé · 0 h
- 2026-11-24 17:00 · agent:analyste-besoin · CDC révisé en v0.3 (arbitrages d'Ethan, DEC-006) ; statut du ticket inchangé, validation humaine de la v0.3 en attente · 0 h
- 2026-11-24 18:00 · agent:analyste-besoin · CDC révisé en v0.4 ; statut du ticket inchangé, validation humaine de la v0.4 en attente · 0 h
- 2026-11-24 · salarie:ethan · décision prise (DEC-006) · 0 h
- 2026-11-24 18:30 · agent:coordinateur · suivi après déblocage humain (DEC-006) : termine_le renseigné, bloque_par vidé (ticket TERMINE) · 0 h
