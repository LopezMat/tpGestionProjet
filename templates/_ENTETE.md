---
titre: En-tête standard des documents
statut: EN_REVUE
responsable: A
version: 0.3
maj_le: 2026-11-24
valide_par:
decision:
---

# En-tête standard des documents

**C'est la définition unique de l'en-tête.** Tous les templates de documents livrables la reprennent telle quelle. Toute modification passe par la règle R11 (PR, décision et changelog).

## Format

```yaml
---
titre: <titre du document>
statut: BROUILLON            # BROUILLON | EN_REVUE | VALIDÉ
responsable: <A|B|C|D, agent:<nom> ou salarie:<prenom>>
version: 0.1                 # +0.1 à chaque révision, 1.0 à la première validation
maj_le: AAAA-MM-JJ
valide_par:                  # prénom de l'humain qui valide ; vide tant que non VALIDÉ
decision:                    # DEC-NNN ; vide tant que non VALIDÉ
---
```

## Champs

| Champ | Obligatoire | Qui le remplit | Règle |
|---|---|---|---|
| `titre` | oui | auteur | — |
| `statut` | oui | auteur, puis **humain uniquement pour `VALIDÉ`** | `BROUILLON` pendant la rédaction ; `EN_REVUE` quand c'est prêt à relire ; `VALIDÉ` par un humain |
| `responsable` | oui | auteur | lettre de la personne responsable (A, B, C, D), agent producteur (`agent:<nom>`) ou salarié producteur (`salarie:<prenom>`, par exemple pour un rapport de recette ; DEC-002) |
| `version` | oui | auteur | incrémentée à chaque modification significative |
| `maj_le` | oui | auteur | date de la dernière modification |
| `valide_par` | si `VALIDÉ` | humain | prénom de l'humain qui valide |
| `decision` | si `VALIDÉ` | humain | id du fichier `docs/decisions/` qui trace la validation (pour un fichier de décision : son propre id) |

## Règles associées
- **Seul un humain écrit `statut: VALIDÉ`**, et il remplit alors `valide_par` et `decision` (R5).
- **Valeurs autorisées strictes : `BROUILLON`, `EN_REVUE`, `VALIDÉ`.** Le hook et la CI normalisent la valeur (accents supprimés, majuscules) : `VALIDE`, `validé` ou `Validé` sont traités comme `VALIDÉ`. Toute autre valeur est refusée par la CI.
  *Pourquoi :* sinon, écrire `VALIDE` sans accent contournerait le hook et ferait passer un document pour validé.
- **Un document `VALIDÉ` est figé pour les agents.** Pour le modifier, un humain le repasse en `EN_REVUE` (R6).
- **Exception, les journaux.** `docs/CHANGELOG-REGLES.md` et `docs/decisions/README.md` ne passent **jamais** `VALIDÉ` : leur en-tête reste `statut: EN_REVUE` avec le commentaire `# journal, jamais VALIDÉ`. Ils évoluent uniquement par PR et sont exclus de R6.
  *Pourquoi :* un journal figé empêcherait de tracer les décisions suivantes.
- **Les tickets n'utilisent pas cet en-tête.** Ils ont leur propre frontmatter et leur propre cycle (voir [ticket.md](ticket.md)). Les fiches de données (`membre.md`) ont aussi leur format propre.

*Pourquoi un en-tête unique :* le statut et le responsable se lisent de la même façon partout. Le hook et le contrôle CI peuvent vérifier les validations automatiquement, et la cohérence des livrables est un critère d'évaluation.

## Ligne de provenance
Sous l'en-tête, chaque document issu d'un template garde la ligne `<!-- modèle : templates/<nom>.md vX.Y · responsable du modèle : A -->`.
*Pourquoi :* on sait à quelle version de template un document se conforme quand le template évolue.
