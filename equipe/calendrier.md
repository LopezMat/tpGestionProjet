---
# Calendrier de l'équipe (lu par scripts/tableau.py, ne pas renommer les champs)
responsable: B
maj_le: 2026-11-26
jours_feries: [2026-12-25, 2027-01-01]   # jours non ouvrés, en plus des samedis et dimanches
evenements:
  - id: EV-001
    type: absence              # absence | arrivee | depart
    qui: salarie:lea
    debut: 2026-11-26
    fin: 2026-11-27            # incluse
    motif: conges              # conges | maladie | formation | autre (absence) ; vide pour arrivee et depart
    capacite_pct: 0            # % de capacité restante sur la période (0 = indisponible)
    statut: prevu              # prevu | confirme | annule
    decision: DEC-021          # DEC-NNN quand l'événement a été arbitré (SIMULATION, scénario 3)
  - id: EV-002
    type: absence
    qui: salarie:nadia
    debut: 2026-12-03
    fin: 2026-12-03
    motif: formation
    capacite_pct: 0
    statut: prevu
    decision:
  - id: EV-003
    type: absence
    qui: salarie:karim
    debut: 2026-12-21
    fin: 2026-12-31
    motif: conges
    capacite_pct: 0
    statut: prevu
    decision:
  - id: EV-004                 # SIMULATION (scénario 3, skill depart-membre, 2026-11-26)
    type: depart
    qui: salarie:hugo
    debut: 2026-12-04          # date de départ (dernier jour travaillé)
    fin: 2026-12-04
    motif:
    capacite_pct: 0
    statut: prevu
    decision: DEC-021
---

# Calendrier de l'équipe

Source de la **capacité réelle** des salariés : un salarié a une capacité nulle (ou réduite à `capacite_pct`) sur la période d'un événement (S1-R9, ARCHITECTURE § 7).

| Id | Qui | Type | Du | Au | Motif | Statut |
|---|---|---|---|---|---|---|
| EV-001 | Léa | absence | 2026-11-26 | 2026-11-27 | congés | prévu |
| EV-002 | Nadia | absence | 2026-12-03 | 2026-12-03 | formation (supervision) | prévu |
| EV-003 | Karim | absence | 2026-12-21 | 2026-12-31 | congés | prévu |
| EV-004 | Hugo | départ | 2026-12-04 | 2026-12-04 | — | prévu (**SIMULATION**, scénario 3) |

## Règles
- **Le calendrier est mis à jour uniquement par les skills d'événements** (`absence`, `arrivee-membre`, `depart-membre`), exécutés par le coordinateur.
  *Pourquoi :* chaque événement passe par une analyse d'impact et une décision humaine (S1 § 6) ; une saisie directe la contournerait.
- **Le motif reste générique** (`conges`, `maladie`, `formation`, `autre`).
  *Pourquoi :* aucune donnée personnelle ou de santé dans un dépôt versionné.
- **Les dates sont incluses et au format `AAAA-MM-JJ`** ; les jours ouvrés excluent samedis, dimanches et `jours_feries`.
  *Pourquoi :* `tableau.py` et le calcul du préavis de départ (S1-R8) doivent compter les mêmes jours.
- **Un événement n'est jamais supprimé** : il passe `annule`.
  *Pourquoi :* l'historique de capacité reste explicable.
- **Le tableau ci-dessus reflète le frontmatter**, qui fait foi en cas d'écart.
  *Pourquoi :* `tableau.py` ne lit que le frontmatter.
