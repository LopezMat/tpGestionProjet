---
titre: Réponses du client et validation du CDC du projet reservation-coworking
statut: VALIDÉ
responsable: A
version: 1.0
maj_le: 2026-11-24
valide_par:     Ethan            # rempli par l'humain qui valide
decision: DEC-006           # pour un fichier de décision : son propre id
# Champs propres à la décision
id: DEC-006
date: 2026-11-24
decide_par: Ethan
projet: reservation-coworking
ticket: T-003
modifie_une_regle: non      # oui → entrée obligatoire dans docs/CHANGELOG-REGLES.md
---
<!-- modèle : templates/decision.md v0.1 · responsable du modèle : A -->

# DEC-006 — Réponses du client et validation du CDC (reservation-coworking)

> **En attente de validation humaine.** Le coordinateur a rédigé ce fichier à partir de la décision d'Ethan du 2026-11-24 (T-003 : option 2, réponses du client transmises par Claire). Conformément à R5, c'est un membre de l'équipe qui le passe lui-même à `VALIDÉ` et renseigne `valide_par`, **après avoir relu le CDC v0.4**. Le « Pourquoi » est celui formulé par Ethan le 2026-11-24 (skill `tracer-decision`, étape 1).

## Contexte
L'`analyste-besoin` a livré le [CDC](../../projets/reservation-coworking/cdc.md) v0.1 avec 13 questions ouvertes, dont 6 bloquantes (Q-01, Q-03, Q-04, Q-07, Q-08, Q-12), et le ticket [T-003](../../projets/reservation-coworking/tickets/T-003-validation-du-cdc.md) « Validation du CDC ». Ethan a retenu l'option 2 : faire répondre le client, réviser le CDC en v0.2, puis valider. Claire a transmis les réponses du client le 2026-11-24.

## Options étudiées
| Option | Avantages | Inconvénients |
|---|---|---|
| 1. Valider le CDC v0.1 en l'état, avec les hypothèses par défaut | rapide | risque de reprise si une réponse change le périmètre (authentification, règles, RGPD) |
| **2. Réponses du client aux questions bloquantes, CDC v0.2, puis validation (retenue)** | architecture construite sur des règles confirmées par le client | un tour de révision de plus avant l'architecture |
| 3. Refuser le CDC et changer le périmètre | — | aucun besoin de changer le périmètre exprimé |

## Décision
1. **Les réponses du client (Coworking Les Arcades, interlocutrice Marie Lenoir, gérante ; client fictif pour la démonstration) sont intégrées au CDC v0.2 :**
   - Q-01 : compte membre (nom, e-mail, mot de passe) créé par l'accueil ; connexion par e-mail et mot de passe. **F-04 (identification) passe en Must.**
   - Q-03 : du lundi au vendredi, 8 h – 20 h, créneaux d'une heure pile ; une réservation par salle et par créneau ; au plus 2 créneaux par membre et par jour, jusqu'à 14 jours à l'avance.
   - Q-04 : un membre annule ses propres réservations jusqu'au début du créneau ; l'accueil peut annuler n'importe quelle réservation.
   - Q-07 : compte « accueil » dans la même application (rôle distinct) : réservations du jour de toutes les salles, gestion des comptes membres, annulation.
   - Q-08 : le coworking est responsable du traitement ; réservations conservées 12 mois puis supprimées ; compte supprimé sur demande via l'accueil ; mots de passe jamais stockés en clair.
   - Q-09 : budget de **6 000 € HT**.
   - H-08 confirmée : la maintenance après livraison n'est pas comprise dans les 6 000 € (devis séparé).
   - **F-05 (notifications e-mail) est exclu** du projet (pas d'envoi d'e-mail en production locale).
   - **F-06 (fiches des salles : nom, capacité, équipements) est en Should.**
   - Les autres questions : les hypothèses par défaut de l'analyste sont acceptées et listées dans le CDC.
2. **Arbitrages d'Ethan sur la v0.2** (2026-11-24), reportés par l'`analyste-besoin` dans le CDC v0.3 :
   - **F-08 (purge à 12 mois) passe en Should** (option B). Le CDC compte **5 Must** : F-01, F-02, F-03, F-04, F-07. **L'écart à S4-R5 (2 ou 3 Must visés) est accepté** : le client exige des comptes membres et un rôle accueil, l'authentification (F-04) et F-07 ne sont donc plus optionnelles.
   - **Les hypothèses de l'ESN H-10 à H-17 sont acceptées telles quelles.**
   - **Q-14** : un seul compte accueil est créé à l'installation par un script d'initialisation ; son mot de passe initial est fourni par variable d'environnement au premier lancement (jamais dans le dépôt) et doit être changé à la première connexion. L'accueil peut ensuite créer d'autres comptes accueil.
   - **Q-18** : la réinitialisation du mot de passe se fait par l'accueil uniquement (mot de passe temporaire, à changer à la connexion suivante).
   - **La revue humaine des tickets d'authentification revient à Karim** (AF3), et non à Claire comme l'indiquait la v0.2 ; l'affectation est corrigée au planning.
   - **Arbitrages sur la v0.3**, reportés dans le CDC v0.4 :
     - **Changement obligatoire du mot de passe à la première connexion pour tous les comptes, membres compris.** Pourquoi : l'accueil ne doit pas connaître le mot de passe des membres, sinon il pourrait se connecter à leur place. *(Ethan, 2026-11-24)*
     - **Q-15, Q-16 et Q-17** (fiches des salles, mention RGPD, jours fériés) : les hypothèses par défaut de l'analyste sont acceptées.
3. **Le CDC v0.4, une fois relu et passé `VALIDÉ` par un humain avec `decision: DEC-006`, est la base de l'architecture, du planning et du développement.**

## Pourquoi
Les réponses du client lèvent les 6 questions bloquantes ; F-08 passe en Should car aucune donnée n'aura 12 mois avant fin 2027 ; l'écart à S4-R5 est imposé par l'exigence d'authentification du client. *(Ethan, 2026-11-24)*

## Impacts
- Fichiers ou règles à mettre à jour :
  - `projets/reservation-coworking/cdc.md` : v0.2, v0.3 puis v0.4 par l'`analyste-besoin`, puis `VALIDÉ` par un humain (`valide_par`, `decision: DEC-006`, version 1.0) ;
  - `projets/reservation-coworking/projet.md` : `client: Coworking Les Arcades`, ligne dans l'historique des décisions.
- Tickets créés ou débloqués :
  - T-003 débloqué par l'humain (`decision: DEC-006`) ;
  - T-001 (« Rédaction du CDC ») conclu par le coordinateur une fois le CDC validé ;
  - création du ticket de travail « Architecture » de l'`architecte` (R14), puis lancement de l'`architecte`.
- Sécurité : l'authentification par mot de passe et la gestion des rôles rendent la revue humaine obligatoire pour les tickets correspondants (S3-R2, par Karim, AF3) et l'audit `securite` avant la mise en production.
- Règles : aucune règle modifiée. L'écart à S4-R5 est une dérogation propre à ce projet, justifiée ci-dessus.
