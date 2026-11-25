---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-070
titre: Test manquant T-054 (503 sur statement_timeout)
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: normale           # critique | haute | normale | basse
assigne: agent:dev-backend  # agent:<nom> | salarie:<prenom>
competence_requise: backend-python (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 0.5           # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-054]          # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:testeur
cree_le: 2026-11-25
maj_le: 2026-11-25
statut_depuis: 2026-11-25   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
---
<!-- modèle : templates/ticket.md v0.2 · responsable du modèle : A -->

# T-070 — Test manquant T-054 (503 sur statement_timeout)

## Description
Remarque 6 du relecteur-code sur [T-054](T-054-api-consultation-disponibilites.md) : `test_moteur_applicatif_borne_attente_et_requete` cherche `statement_timeout` dans le source ; le déclenchement réel du 503 n'est couvert par aucun test (aucun critère de T-054 ne l'exige, donc T-054 n'est pas bloqué). Le testeur l'a constaté à la main sur le SHA 4674c76 : une session PostgreSQL tient `LOCK TABLE reservation IN ACCESS EXCLUSIVE MODE` pendant 14 s ; `GET /api/disponibilites?date=2026-12-01` → 503 JSON `{"erreur":"indisponible",...}` en 5,02 s, journal « Base indisponible pour /api/disponibilites » sans détail, `/health` 200 pendant ce temps, retour à 200 après libération du verrou. À écrire par le développeur : un test d'intégration (`TEST_DATABASE_URL`) qui provoque ce cas (verrou tenu par une 2e connexion, ou `statement_timeout` abaissé) et vérifie 503 JSON sans détail en moins de 8 s.

## Critères d'acceptation
- [ ] Un test d'intégration prouve que `GET /api/disponibilites` renvoie 503 JSON à message fixe (sans URL ni détail SQL) quand la requête dépasse `statement_timeout`, en moins de 8 s.
- [ ] Le test est vert sur le code actuel de `api.py` et rouge si `statement_timeout` est retiré de `moteur_applicatif()`.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : 
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-25 13:30 · agent:testeur · création · 0 h
- 2026-11-25 14:45 · agent:chef-de-projet · triage (S1-R5) : assigné `agent:dev-backend` confirmé (AF6), priorité `normale`, estimation 0,5 h et `depend_de: [T-054]` maintenus ; à faire avant T-065, qui modifie le même fichier `tests/test_api_consultation.py` (remarques 4 et 5 du relecteur sur T-054) ; revue de code dans T-066, vérification dans T-067. Temps compté dans T-008 · 0 h
