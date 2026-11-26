---
name: nouveau-projet
description: Ouvre l'espace d'un nouveau projet client (projets/<slug>/) à partir d'une demande : demande.md, projet.md, ticket de travail de l'analyste, ticket de décision sur l'interlocuteur client et l'allocation initiale, puis lancement d'analyste-besoin. À utiliser dès qu'une nouvelle demande client arrive.
---

<!-- Skill ESN · système S1 · responsable : B · Lot 2 (B) -->

# nouveau-projet

## Quand l'utiliser
À la réception d'une nouvelle demande client (étape 1 du pipeline, CLAUDE.md § 1). Jamais pour le projet interne `projets/esn-interne/`, qui existe déjà et n'a ni demande ni CDC (R19).

## Entrées
- le texte de la demande du client (tel que donné par l'humain) ;
- `equipe/membres/*.md` et `equipe/calendrier.md`, pour proposer l'interlocuteur client.

## Procédure
1. **Choisir le slug** : court, minuscules, tirets, sans accents ; vérifier que `projets/<slug>/` n'existe pas.
2. **Créer `projets/<slug>/demande.md`** à partir de `templates/demande.md` : transcription fidèle, sans interprétation ; ce qui manque va dans « Premières questions identifiées ». `statut: EN_REVUE`, `responsable: B`.
3. **Créer `projets/<slug>/projet.md`** à partir de `templates/projet.md` :
   - `type_projet` déduit de la demande (`vitrine | ecommerce | api | metier | modernisation`) ; en cas de doute, le noter dans les questions ;
   - `etat_projet: cadrage`, `hebergement: local` (production locale Docker, DEC-003 ; un autre hébergeur exige une décision humaine), `url_prod: http://localhost:<port>`, port fixe propre au projet (8080 par défaut, ARCHITECTURE § 9) ;
   - `budget_eur` et `deadline` repris de la demande ; s'ils sont absents, les laisser vides et en faire une question ;
   - `agents_mobilises: [analyste-besoin]`, `salaries_affectes: []` ;
   - « Pourquoi ces agents et ces salariés » : la sélection initiale et sa justification (grille S4 § 4).
4. **Créer T-001** (procédure `creer-ticket`) : « Rédaction du CDC », ou « Analyse de l'existant » pour une modernisation ; `type: tache`, `assigne: agent:analyste-besoin`, `estimation_h` (repère : 4 h pour un vitrine, 7 h pour une application métier), `cree_par: agent:coordinateur`.
5. **Créer T-002** `decision` « Interlocuteur client et allocation initiale », en `ATTENTE_HUMAIN` : recommandation d'un salarié `relation-client` (au moins `confirme`), disponible (calendrier) et dont l'allocation totale permet de prendre le projet (AF1, AF8) ; options : autre salarié, pourcentage d'allocation ; impact : coût horaire, capacité restante sur les autres projets.
6. **Lancer `analyste-besoin`** avec le slug et le chemin de T-001.
7. **Annoncer** : fichiers créés, T-002 à trancher, prochaine étape (validation du CDC).

## Règles
- **`demande.md` est une transcription, jamais une analyse.**
  *Pourquoi :* l'analyste doit distinguer ce que le client a dit de ce que l'ESN suppose (S4-R3).
- **Le travail de l'analyste a son ticket dès le départ (T-001).**
  *Pourquoi :* sinon son temps n'est rattaché à aucun ticket et le budget consommé est sous-estimé (lot2-A, point 3).
- **L'interlocuteur client est un salarié, choisi par un humain (T-002).**
  *Pourquoi :* le contact client relève d'un humain (AF1) et l'allocation entre projets est une décision humaine (S1-R10).
- **T-002 est tranché à la même pause que le CDC.**
  *Pourquoi :* on n'ajoute pas d'arrêt supplémentaire ; l'humain décide les deux en une fois.

## Produit
- `projets/<slug>/demande.md` (EN_REVUE) et `projets/<slug>/projet.md` (BROUILLON) ;
- `projets/<slug>/tickets/T-001-*.md` et `T-002-*.md` ;
- le lancement d'`analyste-besoin`.

## Point d'arrêt humain
- Validation du CDC (ticket créé par `analyste-besoin`) et T-002 (interlocuteur client et allocation), présentés ensemble.

## Contrôles
- [ ] Slug unique et conforme ; `demande.md` et `projet.md` suivent leur template avec la ligne de provenance.
- [ ] Budget et deadline repris ou posés en question, jamais inventés.
- [ ] T-001 assigné à `agent:analyste-besoin` avec une estimation ; T-002 en `ATTENTE_HUMAIN` avec `bloque_par`.
