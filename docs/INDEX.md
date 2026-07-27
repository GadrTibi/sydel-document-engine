# Carte de `docs/` — SYDEL Document Engine

Index d'une page pour s'orienter dans la documentation. Commence par la section **ÉTAT VIVANT** ci-dessous.

## ÉTAT VIVANT (à lire en premier)

La photo réelle du projet au jour le jour vit dans `docs/returns/` :

- [`returns/DASHBOARD.md`](returns/DASHBOARD.md) — **photo vivante du jour** : où en est le projet, ce qui est livré, ce qui reste. **Point de départ d'une reprise à froid.**
- [`returns/CARNET.md`](returns/CARNET.md) — carnet des retours client en cours (Traité vs Validé).
- [`returns/README.md`](returns/README.md) — mode d'emploi du bureau des retours (pipeline intake → classer → dispatcher → suivre).

## Cadrage (orientation projet)

- [`../AGENTS.md`](../AGENTS.md) — contrat de travail du repo (rôles, garde-fous, conventions).
- [`project/00_MASTER_PLAN.md`](project/00_MASTER_PLAN.md) — plan maître et architecture cible.
- [`project/05_NEW_CHAT_PROMPT.md`](project/05_NEW_CHAT_PROMPT.md) — prompt copiable de reprise à froid (ordre de lecture).
- ⚠️ [`project/04_LAST_STATE.md`](project/04_LAST_STATE.md) — **ARCHIVE figée 2026-06-03**, ne pas s'y fier pour l'état courant.
- ⚠️ [`delivery/work_status.md`](delivery/work_status.md) — **ARCHIVE périmée (~2026-06-03)**, état de démarrage dépassé.

## Sous-dossiers de `docs/`

| Dossier | À quoi il sert |
|---|---|
| `returns/` | **État vivant + retours client** (dashboard, carnet, journal, sources de vérité, verdicts). Source courante. |
| `project/` | Docs de **cadrage projet** (master plan, execution board, handoff, prompt de reprise). Inclut des archives figées (04_LAST_STATE). |
| `delivery/` | Suivi de **livraison** au démarrage du dépôt (work_status). Aujourd'hui archive. |
| `review/` | **Rapports de revue / audit de fidélité** par ticket et par lot (verbatim client, packs, vérifications). |
| `adr/` | **Décisions d'architecture** (Architecture Decision Records). |
| `architecture/` | **Conventions et mode opératoire** technique du moteur. |
| `sprints/` | Documents de **cadrage et clôture de sprint**. |
| `operations/` | Procédures **d'exploitation / process** récurrents. |
| `docssource_truth/` | Référence **métier source** (documents à générer par cas). |
| `_archive/` | Documents **archivés** sortis du flux courant. |

> Règle d'orientation : pour l'état RÉEL aujourd'hui → `returns/DASHBOARD.md`. Pour le cadrage et l'architecture → `project/00_MASTER_PLAN.md` + `AGENTS.md`. Les fichiers marqués ⚠️ ARCHIVE ne reflètent pas l'état courant.
