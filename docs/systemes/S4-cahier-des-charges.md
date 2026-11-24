---
titre: Système 4 — Cahier des charges
statut: EN_REVUE
responsable: B
version: 1.2
maj_le: 2026-11-24
valide_par: 
decision: 
---

# Système 4 — Cahier des charges

## 1. Objectifs (consigne)
- Choisir le système d'information adapté à la demande du client.
- Rédiger le cahier des charges en tenant compte de cette demande, et en garantissant la qualité, la sécurité et la maintenance du code grâce aux trois autres systèmes.

## 2. Acteurs
| Acteur | Rôle | Entrées | Sorties |
|---|---|---|---|
| `analyste-besoin` | comprend la demande, pose les questions, rédige le CDC ; analyse l'existant (modernisation) | `demande.md` | `cdc.md`, questions au client |
| `architecte` | choisit le SI et la stack, conçoit l'architecture | `cdc.md` VALIDÉ | `architecture.md` |
| Humains (A en premier lieu) | valident le CDC et les choix techniques | — | décisions |

## 3. Étapes
1. **Lecture de la demande** (`demande.md`) et repérage des manques.
2. **Questions au client** : listées dans le CDC (section « Questions ouvertes ») ; l'humain y répond ou les arbitre.
3. **Rédaction du CDC** à partir de `templates/cdc.md`, avec le statut `EN_REVUE`.
4. **Arrêt humain : validation du CDC.**
5. **Choix du SI et architecture** par l'`architecte` : `architecture.md`, avec le statut `EN_REVUE`.
6. **Arrêt humain : validation des choix techniques**, puis passage à S1.

Pour une **modernisation**, une étape 0 s'ajoute : l'analyse de l'existant (fonctionnalités, données, dette technique, risques), dans `existant.md` selon [templates/existant.md](../../templates/existant.md), validée avant toute proposition d'architecture et avant la rédaction du CDC.

## 4. Choix du système d'information (grille de départ)

| Type de demande | SI recommandé par défaut | Agents mobilisés |
|---|---|---|
| Site vitrine | site statique ou CMS léger | analyste, 1 dev, testeur, deployeur |
| E-commerce | solution e-commerce existante ou app sur mesure avec paiement externalisé | équipe complète, audit de sécurité renforcé |
| API | service backend + base relationnelle + documentation OpenAPI | dev-backend, architecte, securite |
| Application métier | app web (front + API + base) | équipe complète |
| Modernisation | selon l'analyse de l'existant (refonte, migration progressive, encapsulation) | analyste (existant), architecte |

Hébergement par défaut : **production locale Docker** sur le poste de démonstration ([DEC-003](../decisions/2026-11-24-DEC-003-production-locale-docker.md), [ARCHITECTURE § 9](../ARCHITECTURE.md#9-hébergement-et-vérification-en-ligne)) : l'app dans une image étiquetée par SHA, avec Postgres 16. Un autre hébergeur exige un ticket `ATTENTE_HUMAIN`, une décision et son propre outillage de déploiement. Ce n'est qu'un point de départ ; l'architecte justifie chaque écart.

## 5. Garantir qualité, sécurité et maintenance par les autres systèmes

Le template CDC impose trois **sections obligatoires**, qui transforment la demande en exigences que S1, S2 et S3 vérifieront :

| Section du CDC | Ce qu'elle fixe | Système qui la met en œuvre |
|---|---|---|
| **Exigences de tests** | niveau de tests attendu, parcours critiques à couvrir, critères d'acceptation | S3 (testeur, CI, recette humaine sur les critères d'acceptation : porte 3 bis) ; S1 (critères dans les tickets) |
| **Exigences de sécurité** | données sensibles, RGPD, authentification, niveau d'audit, gestion des secrets | S3 (securite, portes de contrôle) ; S2 (crise, veille CVE) |
| **Exigences de maintenance** | disponibilité attendue, support, veille, sauvegardes, durée de maintenance | S2 (suivi, support, runbooks) ; S1 (tickets post-déploiement) ; S3 (sauvegardes, rollback) |

## 6. Règles

**S4-R1 · Le CDC contient obligatoirement les sections Exigences de tests, Exigences de sécurité et Exigences de maintenance**, chacune avec un renvoi au système concerné.
*Pourquoi :* la consigne demande que le CDC garantisse qualité, sécurité et maintenance grâce aux trois autres systèmes ; ces sections rendent ce lien explicite et vérifiable.

**S4-R2 · Chaque exigence fonctionnelle a un identifiant (`F-NN`), une priorité MoSCoW et des critères d'acceptation vérifiables.**
*Pourquoi :* le chef de projet en tire directement les tickets, et le testeur sait quoi vérifier.

**S4-R3 · L'analyste n'invente pas de besoin.** Une information manquante devient une question ouverte, jamais une hypothèse silencieuse. Une hypothèse nécessaire est signalée comme telle.
*Pourquoi :* un CDC qui contient des suppositions non signalées produit le mauvais logiciel.

**S4-R4 · L'architecte justifie chaque choix technique** (alternatives étudiées, raison du choix, coût, impact sur la maintenance) et ne commence qu'à partir d'un CDC `VALIDÉ`.
*Pourquoi :* les choix techniques importants sont soumis à validation humaine et doivent pouvoir être défendus en soutenance.

**S4-R5 · Le périmètre de démonstration reste minimal** : 2 ou 3 fonctionnalités pour le client de démo.
*Pourquoi :* la vision le précise ; c'est le système qui est évalué, pas l'application.

## 7. Contrôles
- Le CDC est conforme au template et ses sections obligatoires sont remplies.
- Chaque exigence fonctionnelle a des critères d'acceptation.
- `architecture.md` couvre chaque exigence non fonctionnelle du CDC.

## 8. Interfaces
- **→ S1** : `cdc.md` et `architecture.md` VALIDÉS, base du découpage en tickets.
- **→ S3** : exigences de tests et de sécurité, base des portes de contrôle ; critères d'acceptation, base de la recette humaine.
- **→ S2** : exigences de maintenance et stack, base de la veille et du suivi.
