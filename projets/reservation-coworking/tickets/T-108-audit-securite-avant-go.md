---
# Frontmatter propre aux tickets (lu par scripts/tableau.py, ne pas renommer les champs)
id: T-108
titre: Audit sécurité avant GO
projet: reservation-coworking
type: tache                 # fonctionnalite | tache | bug | incident | support | decision | formation | amelioration
statut: A_FAIRE             # A_FAIRE | EN_COURS | EN_REVUE | BLOQUE | ATTENTE_HUMAIN | TERMINE | ANNULE
priorite: haute             # critique | haute | normale | basse
assigne: agent:securite     # agent:<nom> | salarie:<prenom>
competence_requise: securite-applicative (confirme)   # nom du référentiel d'equipe/agents.md ; niveau : debutant | confirme | expert
estimation_h: 5             # heures équivalent humain, quel que soit l'assigné
temps_passe_h: 0            # heures équivalent humain
depend_de: [T-010, T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026, T-028]   # ex. [T-001, T-002]
bloque_par:                 # obligatoire si BLOQUE ou ATTENTE_HUMAIN
validation_humaine_requise: non   # oui | non
decision:                   # DEC-NNN si le ticket porte une décision humaine
cree_par: agent:chef-de-projet
cree_le: 2026-11-27
maj_le: 2026-11-27
statut_depuis: 2026-11-27   # date du dernier changement de statut
debut_le:                   # facultatif : date du premier passage EN_COURS
termine_le:                 # facultatif : date du passage TERMINE
imputation: client          # client | esn ; esn seulement sur décision humaine VALIDÉ (R18) ; dans esn-interne : toujours esn (R19)
imputation_decision:        # DEC-NNN VALIDÉ de docs/decisions/, obligatoire si esn dans un projet client ; vide dans esn-interne
---
<!-- modèle : templates/ticket.md v0.3 · responsable du modèle : A -->

# T-108 — Audit sécurité avant GO

## Description
Créé en application de [DEC-026](../../../docs/decisions/2026-11-27-DEC-026-audit-securite-increments-esn.md) (option D, VALIDÉ par Ethan le 2026-11-27), point 2. Ce ticket reprend l'objet d'origine de [T-043](T-043-audit-securite.md), désormais réservé aux audits d'incrément de DEC-011 et pris en charge par l'ESN. Il reprend aussi ses dépendances et ses critères. L'audit avant GO reste **au client** (`imputation: client`) : c'est la porte prévue au planning et achetée par lui. Son **périmètre est complet** (5 h) : DEC-026 a écarté l'option d'un audit réduit.

Ticket « Audit sécurité avant GO » de l'agent `securite` (porte 3 de S3) : audit du code et des dépendances sur le **SHA candidat**, au niveau fixé par le CDC § 8 (OWASP Top 10, contrôle d'accès, authentification, RGPD ; pas de test d'intrusion externe), avec `pip-audit`, `bandit` et `gitleaks` (`securite.yml`). L'audit **confirme ou ajuste les seuils G** provisoires de DEC-007 (mot de passe, tentatives, alerte, sessions), en cohérence avec les revues de Karim (T-030 à T-032). Il examine aussi l'écart de forme « clé de signature des sessions » ([DEC-007](../../../docs/decisions/2026-11-24-DEC-007-choix-techniques-coworking.md), point C ; architecture R-06) : avec des sessions stockées en base, l'identifiant est un jeton aléatoire vérifié côté serveur, et il n'y a pas de clé de signature.

Le code jamais audité est surtout concentré ici : l'authentification, les sessions et les rôles (T-013 à T-017), la réservation et l'annulation (T-018, T-019), la matrice d'autorisation (T-020), le front (T-022 à T-025), la purge (T-028) et les correctifs (T-058, T-061, T-069, T-075, T-079, T-105). Les 7 rapports d'incrément de T-043 (`securite-2026-11-25` à `-6`, `securite-2026-11-26`) servent de point de départ : leurs constats ouverts sont revérifiés sur le SHA candidat. Les conditions qu'ils posent pour la porte 3 sont reprises : scan de l'image, constat 10, T-063 `TERMINE`, et les conditions de DEC-011 (T-013 et T-020 `TERMINE`, routes de consultation couvertes par la matrice d'autorisation).

**Prérequis hors projet : action A7 de [DEC-025](../../../docs/decisions/2026-11-27-DEC-025-actions-retrospective-semaine.md).** Elle outille l'agent `securite` : il lit les résultats de `securite.yml` sur le SHA candidat, ou les outils sont installés sur le poste, et `bandit` est étendu à `projets/*/app`. Son ticket `amelioration` dans `projets/esn-interne/` doit être `TERMINE` **avant** le début de cet audit. Sinon, l'audit se ferait comme les 7 précédents, avec une revue manuelle des dépendances. `depend_de` ne traverse pas les projets : si ce ticket n'est pas `TERMINE` au moment où les dépendances ci-dessus le sont, ce ticket passe `BLOQUE` avec `bloque_par: amelioration esn-interne/T-022` ([T-022](../../esn-interne/tickets/T-022-cadrage-audit-avant-go-outille.md), cadrage d'A7, créé le 2026-11-27 en application de DEC-025 ; ou l'id du ticket de réalisation qui en découlera).

Le coordinateur conclut ce ticket (R13) ; l'agent ne le passe pas `TERMINE` lui-même.

## Critères d'acceptation
- [ ] `rapports/securite-AAAA-MM-JJ.md` existe, en `EN_REVUE`, sur le même SHA que le rapport de tests, avec un verdict `NON BLOQUANT` ou `BLOQUANT`.
- [ ] Chaque seuil G est déclaré confirmé ou à ajuster, avec la justification.
- [ ] Toute vulnérabilité critique ou haute a son ticket `bug` ou `incident`.
- [ ] Le rapport examine l'écart « clé de signature des sessions » (DEC-007, point C ; architecture R-06). Il conclut, avec la justification, que la protection des sessions exigée par le CDC § 8 est couverte ou non par le jeton aléatoire vérifié côté serveur.

## Revue
<!-- Remplie par relecteur-code pour les tickets de réalisation -->
- **Avis relecteur-code** : sans objet (ticket de travail)
- **Commentaires** :
- **Revue humaine requise** : non
- **Revue humaine** :

## Journal
<!-- Une ligne par action : date-heure · qui · quoi · temps passé (h équivalent humain) -->
- 2026-11-27 10:58 · agent:chef-de-projet · création en application de DEC-026 (VALIDÉ par Ethan, option D), point 2 : `tache`, `agent:securite` (`.claude/agents/securite.md` présent), `securite-applicative (confirme)`, 5 h, `imputation: client`. Les `depend_de` sont ceux de T-043 (T-010 à T-028, sans T-027 annulé), et les 3 critères d'origine de T-043 sont repris, avec l'examen de l'écart DEC-007 C. Absence de cycle vérifiée : les descendants de T-108 sont T-045 et T-046, puis T-047 → T-048 → T-049, dont personne ne dépend ; aucun ticket de T-010 à T-028 n'en fait partie. Prérequis A7 de DEC-025 noté dans la Description ; `A_FAIRE`, puisque ses dépendances sont ouvertes. Temps compté dans T-008 · 0 h
