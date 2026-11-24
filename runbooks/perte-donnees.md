---
titre: Runbook — Perte de données
statut: EN_REVUE
responsable: D
version: 0.1
maj_le: 2026-11-24
valide_par:
decision:
---
<!-- Runbook ESN · système S2 · responsable : D · Lot 2 · structure commune décrite dans docs/a-integrer/lot2-D.md -->

# Runbook — Perte de données

> Conduit par l'agent `gestionnaire-crise` ([.claude/agents/gestionnaire-crise.md](../.claude/agents/gestionnaire-crise.md)). Règles applicables : S2-R1 à S2-R5 ([S2](../docs/systemes/S2-maintenance.md)), R7, S3-R4.
> **Aucune restauration n'est jamais lancée par un agent** : c'est une action sensible sur les données (S2-R4).

## Déclencheurs et sévérité
| Situation | Sévérité |
|---|---|
| Données de production supprimées, corrompues ou incohérentes (lignes manquantes, valeurs écrasées) | `critique` |
| Données exposées à un tiers (fuite) | `critique` ; enchaîner avec [intrusion.md](intrusion.md) |
| Perte limitée à un utilisateur, avec contournement et sans fuite | `haute` (pas de crise : triage S1) |

## Rôles
| Rôle | Qui | Ce qu'il fait |
|---|---|---|
| Conduite | `agent:gestionnaire-crise` | déroule ce runbook, journalise, prépare les décisions |
| Orchestration | coordinateur | lance les agents, présente les décisions aux humains (R7) |
| Restauration | salarié `sauvegarde-restauration` ≥ confirme (aujourd'hui : Nadia, voir `equipe/membres/`) | exécute la restauration **après décision** |
| Données | salarié `base-de-donnees-sql` expert (aujourd'hui : Karim) | évalue l'étendue et la cohérence |
| Communication | salarié `relation-client` (aujourd'hui : Claire) | informe le client, après décision |
| Décision | humain de l'équipe | tranche les tickets `ATTENTE_HUMAIN` |

## 1. Détection
- `analyste-prod` : erreurs 5xx liées à la base dans les logs simulés, compteurs de métriques qui chutent brutalement (`rapports/metriques-*`), `/health` qui répond mais avec une version inattendue après une migration.
- `support` : remontées du type « mes données ont disparu », « ma réservation n'existe plus ».
- `deployeur` : un déploiement qui comportait une migration de schéma, suivi d'erreurs.
- Chacun crée un ticket `incident` `critique`, `assigne: agent:gestionnaire-crise` (S2-R3).

## 2. Minutes 0–15
| Minute | Action | Par |
|---|---|---|
| 0 | Le coordinateur lance `gestionnaire-crise` sur le ticket `incident` ; ticket `EN_COURS`, runbook noté au journal | coordinateur, agent |
| 0–5 | **Figer le périmètre** : quelles données (tables, entités), depuis quand (premier symptôme), combien d'utilisateurs ; s'il y a fuite → [intrusion.md](intrusion.md) en parallèle | agent |
| 5–10 | **Identifier la dernière sauvegarde** : section « Déploiement » du dernier `rapports/deploiement-*.md` (porte 5, S3-R4) ; noter sa référence et son heure ; calculer la fenêtre de perte (heure de la sauvegarde → maintenant) | agent |
| 5–10 | Relier à un changement : dernier déploiement (`git log`, `gh run list`), migration, opération manuelle | agent |
| 10–15 | **Préparer les décisions** (§ 4) : tickets `decision` en `ATTENTE_HUMAIN` avec options, recommandation et impact ; ticket `incident` → `BLOQUE` (`bloque_par: attente décision T-NNN`) | agent |
| 15 | Message de retour au coordinateur, qui s'arrête et présente les décisions (R7) | agent, coordinateur |

**À ne pas faire** : restaurer, purger, « réparer » des lignes à la main, relancer une migration, supprimer des logs.

## 3. Escalade
| Niveau | Qui | Quand |
|---|---|---|
| 1 | coordinateur et humain de l'équipe | dès la prise de l'incident |
| 2 | salarié `sauvegarde-restauration` et salarié `base-de-donnees-sql` | dès qu'une restauration est envisagée |
| 3 | salarié `relation-client`, puis compétence `juridique` | données personnelles touchées, ou indisponibilité visible par le client |

## 4. Points de décision humaine
| Décision | Options | Qui tranche | Trace |
|---|---|---|---|
| Restaurer | (a) restaurer la sauvegarde X (perte des écritures depuis HH:MM) ; (b) restauration partielle (tables ciblées) ; (c) ne pas restaurer, reconstruire à la main | humain de l'équipe | ticket `decision` `ATTENTE_HUMAIN` + `DEC-NNN` |
| Mettre l'application en maintenance pendant l'opération | oui / non (durée estimée) | humain | ticket `decision` + `DEC-NNN` |
| Informer le client | message proposé par l'agent, envoyé par le salarié `relation-client` | humain | ticket `decision` + `DEC-NNN` |
| Notifier la CNIL | obligatoire sous 72 h si une violation de données personnelles présente un risque (RGPD, art. 33) | humain (`juridique`) | ticket `decision` + `DEC-NNN` |

## 5. Retour à la normale
- [ ] Restauration exécutée par le salarié désigné, selon la décision tracée.
- [ ] La sonde confirme l'application en ligne au bon SHA : `python scripts/sonde_sante.py --url <url_prod> --sha <sha du dernier déploiement réussi>` → `DISPONIBLE ET À JOUR`.
- [ ] Contrôle de cohérence des données restaurées (échantillon, compteurs) noté au journal.
- [ ] Utilisateurs touchés et données définitivement perdues listés dans le ticket.
- [ ] Ticket `incident` → `EN_REVUE` une fois le post-mortem rédigé.

## 6. Post-mortem
Dans les **2 jours ouvrés** (S2-R5), sans blâme, selon [templates/post-mortem.md](../templates/post-mortem.md) : `projets/<slug>/rapports/post-mortem-AAAA-MM-JJ-perte-donnees.md`. Questions à traiter : pourquoi la perte a été possible (migration non testée, absence de contrainte, sauvegarde trop ancienne), pourquoi elle n'a pas été détectée plus tôt. Chaque action corrective devient un ticket.

## Ce que les agents ne font jamais
Restaurer, purger, modifier des données de production, mettre l'application en maintenance, contacter le client (S2-R1, S2-R4, AF1).

## Points ouverts
- **Sauvegarde Postgres** : base retenue, emplacement et durée de rétention des sauvegardes (`pg_dump` en artefact GitHub Actions proposé) à trancher au lot 5 ([ARCHITECTURE § 10.2](../docs/ARCHITECTURE.md#10-à-trancher-au-lot-workflows)). **Tant que ce mécanisme n'existe pas, aucune restauration n'est possible** : la seule décision humaine est d'accepter la perte ou de reconstruire à la main.
- Procédure de restauration elle-même (commande, durée, test) : à écrire ici au lot 5, et à tester avant la soutenance (S3-R7, DEC-001 § 14).
