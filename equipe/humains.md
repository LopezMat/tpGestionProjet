---
titre: Membres humains de l'équipe projet
statut: VALIDÉ
responsable: B
version: 1.0
maj_le: 2026-11-26
valide_par: Ethan
decision: DEC-017
# Champs propres à ce fichier (lus par scripts/bureau.py, ne pas renommer) : un prénom par membre, tel qu'il
# s'écrit. Un membre ajouté ici apparaît dans « Le bureau » sans modifier le code (DEC-017).
humains:
  - prenom: Ethan
  - prenom: Johan
  - prenom: Stéphane
  - prenom: Matthieu
---

# Membres humains de l'équipe projet

Ethan, Johan, Stéphane et Matthieu sont les membres de l'équipe projet : ils décident, valident (R5, R7) et jouent les salariés aux arrêts humains.

| Membre | Rôle |
|---|---|
| Ethan | membre de l'équipe projet |
| Johan | membre de l'équipe projet |
| Stéphane | membre de l'équipe projet |
| Matthieu | membre de l'équipe projet |

**À ne pas confondre avec les salariés fictifs** d'[equipe/membres/](membres/) (Claire, Hugo, Karim, Léa, Nadia). Ceux-ci sont des personnages de l'ESN simulée, avec un coût, une capacité et une allocation lus par `tableau.py`. Les membres listés ici sont les personnes réelles du groupe : ils n'ont ni coût, ni capacité, ni allocation, et on ne leur attribue ni lettre A à D, ni salarié joué (DEC-017).
*Pourquoi :* la page « Le bureau » de la console doit montrer les humains qui décident, même quand aucun journal ne les cite encore. Sans ce fichier, ils n'apparaissaient que comme des visiteurs créés à la volée, en double selon la graphie (« Stéphane », « stephane », « salarie:ethan »).

**Mise à jour.** Ce fichier est dans `equipe/` : seul le coordinateur l'écrit, après une décision humaine tracée dans `docs/decisions/` (CLAUDE.md § 5). Pour ajouter un membre, ajouter une ligne `- prenom: <Prénom>` dans `humains:` ; aucun code n'est à modifier.
