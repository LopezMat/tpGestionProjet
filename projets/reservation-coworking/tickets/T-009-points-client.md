---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-009
titre: Points client (mention de confidentialité, F-08, recette)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: salarie:claire     # agent:<nom> | salarie:<prenom>
competence_requise: relation-client (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-007]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-24
maj_le: 2026-11-24
statut_depuis: 2026-11-24   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-009 — Points client (mention de confidentialité, F-08, recette)

## Description
Contact client (AF1) : Claire, interlocutrice côté ESN (DEC-005), traite avec Marie Lenoir, gérante de Coworking Les Arcades, les points que le CDC et l'architecture laissent au client.

1. **Mention d'information RGPD** (CDC § 8, H-21 ; architecture § 6) : l'ESN propose le texte, le client (responsable du traitement) le valide. Contenu attendu : finalité (réservation des salles, identification par l'accueil) ; base légale (H-03, à confirmer par le client) ; données (nom, e-mail, empreinte du mot de passe) ; conservation des réservations 12 mois ; **persistance au plus 30 jours dans les sauvegardes**, sous la condition R-05 de l'architecture (DEC-007, DEC-008) ; exercice des droits de suppression, d'accès et de rectification auprès de l'accueil ; adresse de support de l'ESN. Le texte validé est recopié sous « Texte validé » ci-dessous, pour le ticket T-025.
2. **F-08 avant la mise en ligne ?** (CDC § 4 et § 11) : le planning inclut la purge à 12 mois (T-028) dans la livraison du 2026-12-15 ; demander au client s'il l'exige à la mise en ligne ou s'il accepte une livraison ultérieure (avant fin 2027).
3. **Recette** (Q-12) : disponibilité de Marie Lenoir pour assister à la recette du 2026-12-09 au 2026-12-14 (facultatif ; la recette est faite par Claire, T-045).
4. **Adresse de support** de l'ESN (Q-09) : la communiquer au client ; elle figure dans le pied de page (T-022) et la page de confidentialité (T-025).
5. **Fiches des salles** (Q-15, facultatif) : noms, capacités et équipements ; à défaut, « Salle 1/2/3 » (H-20).

**Ticket salarié (AF11, R15)** : à faire par un humain (Claire) ; le coordinateur ne le réalise pas. Compétence `juridique` absente de l'équipe : la validation légale du texte relève du client, responsable du traitement ; Claire (`rgpd` confirmé) rédige la proposition.

**Texte validé** : *(à recopier par Claire après la réponse du client)*

## Critères d'acceptation
- [ ] Le texte de la mention de confidentialité est proposé par l'ESN, validé par Marie Lenoir (date et réponse notées au journal) et recopié sous « Texte validé ».
- [ ] Le texte indique la durée maximale de 30 jours dans les sauvegardes, avec la condition de l'architecture R-05, et l'exercice des droits auprès de l'accueil.
- [ ] La réponse du client sur F-08 (exigée ou non à la mise en ligne) est notée au journal.
- [ ] La disponibilité (ou non) de Marie Lenoir pour la recette est notée au journal.
- [ ] L'adresse e-mail de support est communiquée au client et notée au journal.
- [ ] Les valeurs des salles sont fournies, ou « Salle 1/2/3 » (H-20) est confirmé.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (pas de code)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-24 23:55 · agent:chef-de-projet · création · 0 h
