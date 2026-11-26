---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-084
titre: SIMULATION — Décision notification CNIL de la violation de données (T-080)
projet: reservation-coworking
type: decision              # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: ATTENTE_HUMAIN      # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: juridique (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 1             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: []               # ex. [T-001, T-002]
bloque_par: décision humaine requise (S2-R4, notification CNIL, compétence juridique) ; recommandation à transmettre au client avant le 2026-11-27 17:00
validation_humaine_requise: oui   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:gestionnaire-crise
cree_le: 2026-11-26
maj_le: 2026-11-26
statut_depuis: 2026-11-26   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
> **SIMULATION** — Exercice de crise (scénario 5, S2) demandé par l'humain le 2026-11-26, ticket incident [T-080](T-080-simulation-perte-base-production.md). Aucune notification n'est réellement faite. Heures simulées. Ceci n'est pas un avis juridique : la décision revient à un humain compétent.

<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-084 — SIMULATION — Décision notification CNIL de la violation de données (T-080)

## Description
Runbook [perte-donnees](../../../runbooks/perte-donnees.md) § 4, ligne « Notifier la CNIL », décision humaine relevant de la compétence `juridique`. **Aucun salarié de l'équipe n'a la compétence `juridique`** (`equipe/membres/`). Claire (`rgpd` confirmé, interlocutrice client, AF2) porte la décision. Un avis juridique externe est recommandé, et un ticket `formation` est proposé dans le post-mortem (P-8).

**Qualification (SIMULATION)**
- **Violation de données personnelles** (RGPD, art. 4.12) : oui. C'est une **perte de disponibilité**, peut-être définitive si aucune sauvegarde n'existe ([T-081](T-081-simulation-decision-restauration-base.md)).
- **Données concernées** :
  - nom, e-mail et empreinte Argon2id du mot de passe de chaque compte (membres et accueil, quelques dizaines, H-05) ;
  - réservations (salle, date, créneau, lien au compte) ;
  - sessions (empreinte SHA-256 du jeton).
  
  Aucune donnée sensible au sens de l'art. 9, aucune donnée bancaire.
- **Confidentialité** : non atteinte d'après les éléments connus. Le volume a été supprimé sur le poste, la base n'avait aucun port publié et l'app n'est joignable que sur `127.0.0.1`. Rien n'indique une copie ou un accès par un tiers. **À confirmer** : l'origine accidentelle doit être confirmée par l'humain qui a signalé l'incident (T-080). Si elle ne l'est pas, on enchaîne avec le runbook `intrusion` et cette qualification est revue.
- **Intégrité** : sans objet (rien n'a été modifié, tout a été perdu).
- **Rôles** : le client est **responsable du traitement**, l'ESN **sous-traitant** ([cdc.md](../cdc.md) § 8, Q-08). C'est le responsable du traitement qui notifie la CNIL (art. 33.1) **dans les 72 h** après en avoir pris connaissance, sauf si la violation est « peu susceptible d'engendrer un risque » pour les personnes. Le sous-traitant notifie le responsable du traitement dans les meilleurs délais (art. 33.2), ce que fait le message 1 de [T-083](T-083-simulation-decision-communication-client.md). Dans tous les cas, la violation est **inscrite au registre des violations du client** (art. 33.5).
- **Risque pour les personnes** : **faible selon l'agent**.
  - Il n'y a pas d'exposition des données. La conséquence est une gêne : impossibilité de réserver pendant l'incident, réservations à ressaisir et, en cas de reconstruction, nouveau compte et nouveau mot de passe.
  - Il n'y a ni préjudice financier, ni discrimination, ni usurpation d'identité possible du fait de l'incident.
  - L'art. 34 (communication aux personnes en cas de **risque élevé**) ne paraît pas applicable. Une information des membres par le client reste utile en pratique, puisqu'ils constatent la perte.

**Échéance** : si le client reçoit le message 1 le 2026-11-26 vers 11:00, le délai de 72 h expire le **2026-11-29 vers 11:00, un dimanche**. La recommandation de l'ESN doit donc lui parvenir **au plus tard le vendredi 2026-11-27 à 17:00**.

**Question** : quelle recommandation l'ESN transmet-elle au client (responsable du traitement) sur la notification de la violation à la CNIL ?

**Options**
- **(1) Pas de notification à la CNIL, inscription au registre du client**, avec la qualification ci-dessus et une information des membres par le client. Conditions : origine accidentelle confirmée et aucune copie hors du poste.
- **(2) Notification à la CNIL par le client sous 72 h** (téléservice de la CNIL), par prudence. Elle peut être faite en deux temps (notification initiale, puis complément après T-081). L'ESN fournit les éléments techniques.
- **(3) Notification par l'ESN elle-même** : **écartée**. Elle revient au responsable du traitement, sauf mandat écrit du client, dont aucune trace n'existe.

**Recommandation** : **(1)**, sous les deux conditions ci-dessus, à confirmer par un avis juridique. On bascule en **(2)** si l'origine accidentelle n'est pas confirmée, si une copie des données a pu quitter le poste, ou si l'avis juridique conclut à un risque (perte définitive des données sans sauvegarde, par exemple).

**Impact chiffré** :
- Claire, environ 1 h (note au client, échange, trace), environ 79 € ;
- avis juridique externe : coût non chiffré, à décider ;
- en (2), aide au formulaire de notification : environ 0,5 h de plus.

Le risque de non-conformité porte sur le client (sanction CNIL possible pour une violation non notifiée qui aurait dû l'être) et, par ricochet, sur la relation ESN-client. Personnes concernées : tous les comptes de la base (quelques dizaines).

## Critères d'acceptation
- [ ] Un humain compétent a tranché (avis juridique noté au journal : interne, externe ou absent, avec la justification) ; le fichier `docs/decisions/AAAA-MM-JJ-DEC-NNN-*.md` est créé et référencé dans `decision`.
- [ ] La recommandation est transmise au client par Claire avant le 2026-11-27 17:00 ; l'heure et le canal sont au journal.
- [ ] La décision du client est notée au journal : notification CNIL faite (date, sans numéro de dossier ni donnée personnelle) ou inscription au registre seule.
- [ ] La qualification est revue et notée si T-081 conclut à une perte définitive ou si l'origine accidentelle n'est pas confirmée.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de décision)
- **Commentaires** :
- **Revue humaine requise** : sans objet (décision humaine, R7 ; compétence `juridique` hors périmètre des agents)
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-26 10:15 · agent:gestionnaire-crise · SIMULATION · création (ATTENTE_HUMAIN), qualification RGPD (perte de disponibilité, sous-traitant, art. 33.2 et 33.5), recommandation (1) sous conditions, échéance de recommandation au client le 2026-11-27 17:00 · 0 h
