---
titre: Runbook — Intrusion
statut: EN_REVUE
responsable: D
version: 0.1
maj_le: 2026-11-24
valide_par:
decision:
---
<!-- Runbook ESN · système S2 · responsable : D · Lot 2 · structure commune décrite dans docs/a-integrer/lot2-D.md -->

# Runbook — Intrusion

> Conduit par l'agent `gestionnaire-crise` ([.claude/agents/gestionnaire-crise.md](../.claude/agents/gestionnaire-crise.md)). Règles applicables : S2-R1 à S2-R5 ([S2](../docs/systemes/S2-maintenance.md)), S3-R2, S3-R8, R7.
> **Revue humaine immédiate** : une intrusion confirmée ou fortement suspectée passe à un humain avant toute autre étape.

## Déclencheurs et sévérité
| Situation | Sévérité |
|---|---|
| Accès non autorisé avéré (compte pris, données lues ou modifiées, code ou configuration altérés) | `critique` |
| Secret exposé (dans les logs, le dépôt, une page publique) | `critique` |
| CVE activement exploitée sur une dépendance en production (veille) | `critique` |
| Tentatives répétées sans succès constaté (rafales de 401, scans) | `haute` (pas de crise : triage S1 et `securite`) |

## Rôles
| Rôle | Qui | Ce qu'il fait |
|---|---|---|
| Conduite | `agent:gestionnaire-crise` | préserve les preuves, journalise, prépare les décisions |
| Orchestration | coordinateur | lance les agents, présente les décisions (R7) |
| Revue humaine sécurité | salarié `securite-applicative` ≥ confirme (aujourd'hui : Karim) | qualifie l'intrusion, décide des mesures |
| Audit | `agent:securite` | audite le SHA en production, propose les correctifs (tickets) |
| Secrets | salarié d'exploitation (aujourd'hui : Nadia) | fait la rotation des secrets **après décision** |
| Communication | salarié `relation-client`, compétence `juridique` | client, CNIL |

## 1. Détection
- `analyste-prod` : logs simulés anormaux (rafales de 401 ou 403, accès à des routes d'administration, requêtes inhabituelles), secret visible dans un log.
- `veilleur` : CVE exploitée activement sur une dépendance en production.
- `securite` : constat critique dans un rapport d'audit.
- `support` : « mon compte a été modifié », « je reçois des messages étranges ».

## 2. Minutes 0–15
| Minute | Action | Par |
|---|---|---|
| 0 | Ticket `incident` `EN_COURS` ; **escalade immédiate** à la revue humaine sécurité (via le coordinateur) | agent, coordinateur |
| 0–5 | **Préserver les preuves** : ne supprimer ni ne modifier aucun log ; recopier dans le ticket les extraits utiles (heures, routes, codes), **secrets et données personnelles masqués** | agent |
| 5–10 | **Évaluer l'exposition** : quelles données, quels comptes, quels secrets (GitHub, deploy hook, base) ont pu être lus ; depuis quand ; le SHA en production (`python scripts/sonde_sante.py --url <url_prod> --sha <sha attendu>`) est-il bien celui du dernier déploiement ? | agent |
| 5–10 | Relier à une cause : CVE connue (`veille/`), dernier rapport `securite`, changement récent (`git log`, `gh run list`) | agent |
| 10–15 | Préparer les décisions (§ 4) ; ticket `incident` → `BLOQUE` ; message de retour | agent |

**À ne pas faire** : coller un secret dans un ticket ou un rapport, couper le service, faire la rotation des secrets, corriger le code, contacter l'attaquant ou le client.

## 3. Escalade
| Niveau | Qui | Quand |
|---|---|---|
| 1 | humain de l'équipe et revue humaine sécurité | **immédiatement** |
| 2 | salarié d'exploitation | dès qu'une coupure ou une rotation de secrets est envisagée |
| 3 | salarié `relation-client` et compétence `juridique` | données personnelles touchées |

## 4. Points de décision humaine
| Décision | Options | Qui tranche | Trace |
|---|---|---|---|
| Couper le service ou le passer en maintenance | oui / non, durée | humain (S2-R4) | ticket `decision` + `DEC-NNN` |
| Rotation des secrets | lesquels (secrets GitHub, URL du deploy hook, mot de passe de la base, clés d'API), dans quel ordre | humain (S2-R4) | ticket `decision` + `DEC-NNN` |
| Révocation des sessions et réinitialisation des mots de passe | tous les comptes / comptes touchés | humain | ticket `decision` + `DEC-NNN` |
| Informer le client | message proposé par l'agent | humain | ticket `decision` + `DEC-NNN` |
| Notifier la CNIL | obligatoire sous 72 h si une violation de données personnelles présente un risque (RGPD, art. 33) | humain (`juridique`) | ticket `decision` + `DEC-NNN` |

## 5. Retour à la normale
- [ ] La faille est corrigée par le circuit S3 complet : ticket `bug` sécurité, développeur, `relecteur-code`, **revue humaine** (S3-R2), `testeur`, `securite` (NON BLOQUANT), GO humain, `deployeur`.
- [ ] `verifier-prod` puis la sonde confirment le nouveau SHA en ligne.
- [ ] Les secrets décidés ont été changés (le ticket le confirme, sans les écrire).
- [ ] Aucune activité anormale dans les logs suivants (rapport de suivi de l'`analyste-prod`).
- [ ] Ticket `incident` → `EN_REVUE` une fois le post-mortem rédigé.

## 6. Post-mortem
Dans les **2 jours ouvrés** (S2-R5), sans blâme, selon [templates/post-mortem.md](../templates/post-mortem.md) : `projets/<slug>/rapports/post-mortem-AAAA-MM-JJ-intrusion.md`. Questions à traiter : comment l'accès a été possible, pourquoi la veille ou l'audit ne l'ont pas vu, délai de détection. Chaque action corrective devient un ticket (dont `formation` si une compétence sécurité manque).

## Ce que les agents ne font jamais
Écrire un secret, couper le service, changer un secret, corriger le code hors du circuit S3, contacter le client ou l'attaquant (S2-R1, S2-R4, S3-R8, AF1).

## Points ouverts
- Où sont tracées les rotations de secrets (sans les révéler) : à préciser au lot 5 avec la gestion des secrets GitHub.
- Logs réels : aujourd'hui simulés (DEC-001 § 3) ; un vrai journal d'accès changerait les étapes de détection.
