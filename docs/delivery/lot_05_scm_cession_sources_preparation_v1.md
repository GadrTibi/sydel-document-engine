# Lot 05 - preparation sources SCM cession V1

## Objet

Ce document cloture le ticket `PREP-SCM-CESSION-SOURCES-001`.

Perimetre respecte :

- preparation de sources uniquement ;
- aucun code Python modifie ;
- aucune UI modifiee ;
- aucun wording juridique modifie ;
- copie limitee aux 6 sources SCM cession demandees avec matching `HIGH`.

## Sources consultees

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_05_scm_satellites_preparation_v1.md`
- `project/source_import/raw_drive_dump/`
- `project/source_documents/lot_05/`

ADR reperes : `ADR-0001`, `ADR-0003`, `ADR-0005`.

## Methode

Les sources ont ete retenues uniquement si les conditions suivantes etaient reunies :

1. le fichier cible etait absent de `project/source_documents/lot_05/` ;
2. le fichier existait dans `project/source_import/raw_drive_dump/` avec le nom attendu exact ;
3. le dossier source brut correspondait explicitement a la famille SCM cession SELARL ou SCM SELAS ;
4. la copie conservait un hash identique entre la source brute et la cible Lot 05.

Le niveau `HIGH` qualifie uniquement l'appariement `nom attendu -> raw dump` pour ce ticket de preparation. Il ne vaut pas specification, analyse juridique ou autorisation de codage.

## Verification de presence initiale Lot 05

Avant copie, les 6 sources SCM cession demandees etaient absentes de `project/source_documents/lot_05/`.

## Fichiers deja presents

Aucun des 6 fichiers attendus n'etait deja present dans `project/source_documents/lot_05/`.

## Sources copiees

| Source cible Lot 05 | Source brute | Confiance | Taille | SHA-256 |
|---|---|---|---:|---|
| `PV AGE cession part SCM.docx` | `project/source_import/raw_drive_dump/Creation SELARL/scm cession/PV AGE cession part SCM.docx` | HIGH | 514611 | `3F4487DD57AD0B9C756513ABCC1FEFD542749CB602C795C3B5A3644C6BD1B424` |
| `Courrier SDE.docx` | `project/source_import/raw_drive_dump/Creation SELARL/scm cession/Courrier SDE.docx` | HIGH | 561161 | `29A29529E376B74CC5AE15A36E4F7B77D4D9B02B1302AB032638DE25E08492D4` |
| `Acte de cession des parts de la SCM à la SELARL - transforme.docx` | `project/source_import/raw_drive_dump/Creation SELARL/scm cession/Acte de cession des parts de la SCM à la SELARL - transforme.docx` | HIGH | 330330 | `28797A38C49FF5884127490745D06A052BC27E10FC00CB527B6BCC430AA9473E` |
| `PV AGE cession part SCM - SELAS.docx` | `project/source_import/raw_drive_dump/Creation SELAS/SCM/PV AGE cession part SCM - SELAS.docx` | HIGH | 512407 | `100EC9C178EC8177220269BD890553BFDDFAC408F018E59825632A112FD5809C` |
| `Courrier SDE - SELAS.docx` | `project/source_import/raw_drive_dump/Creation SELAS/SCM/Courrier SDE - SELAS.docx` | HIGH | 561231 | `850210A6099BCAA5C709D81003B1767A39A5163465A80B4DF5B5BB7322AF58A1` |
| `Acte_cession_parts_SCM_SEL_modele.docx` | `project/source_import/raw_drive_dump/Creation SELAS/SCM/Acte_cession_parts_SCM_SEL_modele.docx` | HIGH | 330234 | `216823E3EDFC6A4B100B1069E3CBCDA7918A5455A731E5253781E5FA062F75BE` |

Note : les chemins du tableau sont normalises sans accents pour la lisibilite. Les fichiers physiques conservent leurs noms exacts sur disque.

## Sources manquantes

Aucune source demandee n'est manquante apres preparation.

## Validations techniques

- les 6 copies ont un hash identique a leur source brute ;
- les 6 fichiers copies sont des `.docx` ;
- aucun fichier Python n'a ete modifie ;
- aucun wording juridique n'a ete modifie.

## Prochaine etape recommandee

Ouvrir un ticket de specification limite au bloc SCM cession, avant tout code documentaire.
