# Ticket Ledger YB

Date : 2026-05-27

## Sprint 12 - ordre canonique

| Ordre | ID | Statut | Objet | Sortie attendue |
|---:|---|---|---|---|
| 1 | YB-S12-001 | DONE | Boss Delta Bridge | Canon Sprint 12 absorbe en docs, pilote en pause, tickets ordonnes. |
| 2 | YB-S12-002 | READY | Multi-contextes multi-bureaux | Spec des users autorises, contextes separes par bureau, pas de vue fusionnee. |
| 3 | YB-S12-003 | QUEUED | Modele multi-blocs Lead / Atelier / Relance | Spec fonctionnelle des blocs, transitions et ownership. |
| 4 | YB-S12-004 | QUEUED | REFAIS_AG + relance telepro | Flow v2 REFAIS_AG, historique telepro visible, pas de retour prospection brute. |
| 5 | YB-S12-005 | QUEUED | Relance boss | Etat `RELANCE_BOSS`, lecture seule telepro, messagerie autorisee, ACL. |
| 6 | YB-S12-006 | QUEUED | Affectation atelier par bureau | File manuelle d'attribution atelier, aucun fallback auto. |
| 7 | YB-S12-007 | BLOCKED | Rebuild pilote / UAT | Pilote/UAT reconstruits apres absorption des tickets 002 a 006. |

## Regles de sequence

- Ne pas inverser l'ordre metier sans justification PM explicite.
- Ne pas lancer `YB-S12-007` tant que le modele multi-bureaux et les flows
  relance/refaitage/affectation ne sont pas specifies.
- Ne pas lancer de code produit dans `YB-S12-001`.
