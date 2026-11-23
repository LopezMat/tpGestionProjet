---
titre: Cahier des charges — <projet>
statut: BROUILLON
responsable: agent:analyste-besoin
version: 0.1
maj_le: AAAA-MM-JJ
valide_par:
decision:
---
<!-- modèle : templates/cdc.md v0.1 · responsable du modèle : A -->

# Cahier des charges — <projet>

Source : [demande.md](demande.md)

## 1. Contexte et objectifs
<pourquoi ce projet, objectifs mesurables>

## 2. Périmètre
- **Inclus** :
- **Exclu** :

## 3. Utilisateurs
| Profil | Besoin principal | Volume estimé |
|---|---|---|

## 4. Exigences fonctionnelles
| Id | Exigence | Priorité (MoSCoW) | Critères d'acceptation |
|---|---|---|---|
| F-01 | | Must | - [ ] … |

## 5. Exigences non fonctionnelles
| Domaine | Exigence |
|---|---|
| Performance | |
| Disponibilité | |
| Accessibilité | |
| Compatibilité (navigateurs, mobile) | |

## 6. Système d'information envisagé
<type de SI recommandé et justification courte ; le détail est dans architecture.md (S4)>

## 7. Exigences de tests (obligatoire, mis en œuvre par S3 et S1)
- Parcours critiques à couvrir :
- Niveau de tests attendu (unitaires, intégration, bout en bout) :
- Les critères d'acceptation de la section 4 deviennent les critères des tickets (S1).

## 8. Exigences de sécurité (obligatoire, mis en œuvre par S3 et S2)
- Données personnelles et sensibles, base légale RGPD :
- Authentification et autorisations :
- Niveau d'audit attendu avant mise en production :
- Gestion des secrets :
- Scénarios de crise à couvrir (perte de données, coupure, intrusion) :

## 9. Exigences de maintenance (obligatoire, mis en œuvre par S2, S1 et S3)
- Disponibilité attendue et fenêtre de support :
- Canal de support utilisateurs :
- Veille (stack à surveiller) :
- Sauvegardes (fréquence, rétention) et rollback :
- Durée de maintenance après livraison :

## 10. Budget et délais (S1)
- Budget :
- Deadline :
- Jalons souhaités :

## 11. Hypothèses et risques
| Type | Description | Impact | Mitigation |
|---|---|---|---|
| Hypothèse | | | |
| Risque | | | |

## 12. Questions ouvertes
- [ ] <question> → <réponse / décision>

## 13. Validation
Validé par l'humain via l'en-tête (`statut`, `valide_par`, `decision`).
