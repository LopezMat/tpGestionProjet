---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-055
titre: Page de consultation des disponibilités (F-01, lecture seule)
projet: reservation-coworking
type: fonctionnalite        # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:dev-frontend # agent:<nom> | salarie:<prenom>
competence_requise: javascript (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 2             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010, T-054]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:coordinateur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-055 — Page de consultation des disponibilités (F-01, lecture seule)

## Description
**Origine.** Changement de priorité d'Ethan du 2026-11-25 (option « Lecture seule ») : une page permet de voir les disponibilités avant que la connexion et la réservation existent. Ce ticket détache de [T-023](T-023-front-membres-reservation.md) l'affichage des disponibilités ; la réservation, l'annulation et la liste « mes réservations » restent dans T-023 (qui dépend de l'écran de connexion T-022).

Front HTML/CSS/JS sans framework ni build, servi par l'application (architecture § 2 et § 3, DEC-007), sur l'API de [T-054](T-054-api-consultation-disponibilites.md). Le code doit pouvoir être repris par T-022 et T-023 (même structure de fichiers, pas de page jetable).

## Critères d'acceptation
- [ ] Pour une date choisie (par défaut aujourd'hui), la page affiche pour chacune des 3 salles les créneaux d'une heure de 8 h-9 h à 19 h-20 h, chacun marqué « libre » ou « occupé » ; un samedi ou un dimanche, elle affiche un message « aucun créneau ce jour-là ».
- [ ] « Libre » et « occupé » se distinguent autrement que par la couleur seule (texte ou icône avec libellé).
- [ ] Changer de date recharge l'affichage sans recharger toute la page.
- [ ] Une erreur de l'API affiche un message compréhensible, sans détail technique.
- [ ] **Créneaux passés du jour J** (remarque 7 du `relecteur-code` sur T-054, remarque de l'audit securite-2026-11-25-4) : l'API renvoie « libre » un créneau déjà commencé ; pour la date du jour, la page affiche tout créneau dont l'heure de début est atteinte (heure de Paris, `Europe/Paris`, et non le fuseau du navigateur) comme « passé », jamais « libre », avec un libellé texte ; les créneaux à venir gardent l'état de l'API ; une autre date n'est pas concernée. Vérifié avec une heure simulée (fonction de calcul de l'état qui reçoit l'heure en paramètre) : à 13 h 30, 8 h-9 h à 13 h-14 h « passé », 14 h-15 h « libre » ou « occupé » selon l'API.
- [ ] Affichage utilisable sur ordinateur et sur téléphone (émulation mobile), navigation au clavier.
- [ ] **Compatible avec la CSP de l'architecture § 6** (posée par T-063, constat 2 du `securite`) : aucun script ni style en ligne, aucun attribut `on…`, aucune ressource externe ; données insérées par `textContent` uniquement (vérification au journal).

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** :
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 09:30 · agent:coordinateur · création, détachée de T-023 (priorité d'Ethan du 2026-11-25, option « Lecture seule ») · 0 h
- 2026-11-25 23:50 · agent:chef-de-projet · triage du rapport securite-2026-11-25-3 : critère ajouté (compatibilité avec la CSP posée par T-063, constat 2) ; pas de dépendance vers T-063, pour ne pas retarder la page de la soutenance ; temps compté dans T-008 · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage des remarques sur T-054 (relecteur-code, remarque 7 ; audit securite-2026-11-25-4) : critère ajouté (créneaux déjà commencés du jour J affichés « passé ») ; estimation 1,5 → 2 h ; aucune dépendance ajoutée, priorité `haute` maintenue (page de la soutenance du 2026-11-27, DEC-011). Le contrat de l'API n'est pas modifié (T-054 inchangé) ; le refus de réserver un créneau commencé reste dans T-018 (H-11). Le message `date_hors_fenetre` (« réserver ») sera reformulé côté API dans T-065 : la page ne doit pas recopier tel quel un message d'erreur de l'API qui parlerait de réservation. Temps compté dans T-008 · 0 h
