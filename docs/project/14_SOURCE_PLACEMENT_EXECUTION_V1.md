# Journal execution placement sources V1

## Objet
Ce journal documente l'execution du ticket `PLACEMENT-HIGH-001`.

Objectif : placer dans `project/source_documents/` uniquement les cas `HIGH` valides par `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`, sans toucher aux cas `MEDIUM`, `LOW`, hors perimetre, ni au raw dump.

## Date
2026-05-14

## Sources consultees
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`
- `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`
- `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`
- `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- `project/source_import/raw_drive_dump/`
- `project/source_documents/`

ADR reperes : `ADR-0001`, `ADR-0003`, `ADR-0005`.

## Cas HIGH traites

| Cas HIGH | Source brute de reference | Cible | Action | Hash cible SHA-256 |
|---|---|---|---|---|
| DOC-001 - Declaration de non-condamnation | `project/source_import/raw_drive_dump/Creation SAS/Document de base/Declaration sur l_honneur de non condamnation - transforme.docx` | `project/source_documents/lot_01/declaration_non_condamnation_transforme.docx` | no-op ; fichier deja present | `447596AF2B61DC409FD29BF264529DA8F4765B0CD02B4DBEFB1049E192A67827` |
| DOC-002 - Autorisation de domiciliation | `project/source_import/raw_drive_dump/Creation SAS/Document de base/Autorisation de domiciliation - transforme.docx` | `project/source_documents/lot_01/autorisation_domiciliation_transforme.docx` | no-op ; fichier deja present | `E4F98C307EEA4CCA9A0071DA6226D70D74C37995020131B72236C0D66C18BA2B` |
| DOC-003 - Procuration | `project/source_import/raw_drive_dump/Creation SAS/Document de base/Procuration - transforme.docx` | `project/source_documents/lot_01/procuration_transforme.docx` | no-op ; fichier deja present | `CC0324CE523DDECD7780267B040F9037C3C817B19C99CA5524105A22608723F0` |
| PV nomination gerant | `project/source_import/raw_drive_dump/Creation SCI/PV nomination gerant - transforme.docx` | `project/source_documents/lot_02/PV nomination gerant - transforme.docx` | no-op ; source canonique deja presente | `E1D0570A4563C9F8B45986C8E2ABB00922BFFDDE1C825176D5CE6794F3CD98A9` |

Note : les chemins de source brute ci-dessus sont normalises sans accents pour le journal. Les fichiers physiques conservent leurs noms source et leur encodage de nom existant.

## Resultat
- Cas HIGH dans le plan : 4.
- Cas HIGH places ou confirmes en place : 4.
- Nouvelles copies effectuees : 0.
- Fichiers supprimes du raw dump : 0.
- Fichiers renommes : 0.
- Cas `MEDIUM` modifies : 0.
- Cas `LOW` modifies : 0.
- Hors perimetre modifies : 0.
- Cas HIGH restants non places : 0.

## Repertoires cibles
- `project/source_documents/lot_01/` : 3 sources HIGH deja presentes et confirmees.
- `project/source_documents/lot_02/` : 1 source HIGH deja presente et confirmee.
- `project/source_documents/lot_03/` : aucun cas HIGH a placer selon le plan V1.
- `project/source_documents/lot_04/` : aucun cas HIGH a placer selon le plan V1.
- `project/source_documents/lot_05/` : aucun cas HIGH a placer selon le plan V1.

## Controle Git
Avant intervention, `git status --short` indiquait deja des modifications et fichiers non suivis hors perimetre strict du placement HIGH, notamment `project/source_import/` et des sources/cadrages non suivis.

Consequence : aucun commit ni push ne doivent etre effectues tant que le perimetre Git n'est pas arbitre proprement.

