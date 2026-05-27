# Current State

Date : 2026-05-27

## Etat Git et projet

- Branche de travail du bridge : `docs/pm/yb-s12-001-boss-delta-bridge`.
- Branche source au depart : `track-b/clean-rebuild`.
- Dirty state preexistant avant bridge : `.gitignore`, `README.md`,
  `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et un
  rapport `docs/review/track_b_selarl_field_dedup_audit_001_report_v1.md`.
- Ces changements preexistants ne font pas partie du bridge YB-S12-001.

## Canon actuel avant absorption

- Track B expose un front propre centre sur une slice SELARL V1.
- Le modele front existant sait travailler avec `DossierRecord`, roles,
  adresses typees, reuse rules et statuts documentaires.
- La surface recente reste orientee test/pilote SELARL et generation
  documentaire, avec exclusions honnetes pour documents manuels ou incomplets.
- Le repo ne contient pas de fichiers `Current-State.md`, `Decision-Log.md`,
  `Open-Debts-And-Risks.md`, `Ticket-Ledger-YB.md`, `docs/spec-functional.md`,
  `docs/flows/**`, `docs/reviews/**` ou `_assistant/**` avant ce bridge.
- Le literal `USER-ONE-BUREAU` n'a pas ete trouve, mais le canon de fait reste
  mono-contexte cote parcours visible ; il est remplace par multi-bureaux
  autorise avec contextes separes.

## Nouveau canon Sprint 12

- Modele prioritaire : `LEAD + ATELIER + RELANCE`.
- Multi-bureaux autorise avec contextes strictement separes.
- Dossier ouvert distinct d'un lead de prospection.
- `RELANCE_TELEPRO` et `RELANCE_BOSS` visibles.
- `REFAIS_AG` conserve son statut et son historique, sans retour prospection
  brute.
- Atelier non attribue : file manuelle.
- Aucun role `chef telepro`, aucune logique produit speciale
  `interne / externe`.

## Pause explicite

- Le pilote cobayes est en pause.
- Naomi, provisioning, launch, UAT reelle et tout test cobaye sont en pause.
- Aucun travail Claude Design, production, hook ou cleanup gouvernance Phase 2/3
  n'est lance par ce bridge.

## Prochaine etape recommandee

Lancer `YB-S12-002 Multi-contextes multi-bureaux` avant tout code Sprint 12.
