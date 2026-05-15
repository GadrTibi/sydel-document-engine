# Lot 05 - preparation sources SCM satellites V1

## Objet

Ce document cloture le ticket `PREP-SCM-SAT-001`.

Perimetre respecte :

- preparation de sources uniquement ;
- aucun code Python modifie ;
- aucune UI modifiee ;
- aucun wording juridique modifie ;
- `docs/project/01_EXECUTION_BOARD.md` non modifie ;
- `docs/project/04_LAST_STATE.md` non modifie ;
- copie limitee aux sources SCM satellites identifiees en matching `HIGH`.

## Sources consultees

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- `project/source_import/raw_drive_dump/`
- `project/source_documents/lot_05/`

ADR reperes : `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0005`.

## Methode

Les sources ont ete retenues uniquement si les conditions suivantes etaient reunies :

1. le document est cite dans le bloc `SCM` de la source de verite ;
2. le fichier existe dans `project/source_import/raw_drive_dump/creation scm/` ;
3. le rattachement SCM ne presente pas d'ambiguite metier ;
4. la copie conserve un hash identique entre la source brute et la cible Lot 05.

Le niveau `HIGH` qualifie uniquement l'appariement `source de verite -> raw dump` pour ce ticket de preparation. Il ne vaut pas specification, analyse juridique ou autorisation de codage.

## Verification de presence initiale Lot 05

Avant copie, les quatre sources SCM satellites demandees etaient absentes de `project/source_documents/lot_05/`.

Le dossier contenait deja des sources SPFPL Lot 05, sans lien direct avec ce ticket.

## Sources copiees

Les fichiers suivants ont ete copies dans `project/source_documents/lot_05/`.

| Source cible Lot 05 | Source brute | Confiance | Taille | SHA-256 |
|---|---|---|---:|---|
| `Pacte d_associes SCM.docx` | `project/source_import/raw_drive_dump/creation scm/Pacte d_associes SCM.docx` | HIGH | 531768 | `F5FB8F042F50B22E266E1B7E1CF6B253EB48BFC9C6B8484D30B3C52B43D3568E` |
| `Liste depenses communes SCM.doc` | `project/source_import/raw_drive_dump/creation scm/Liste depenses communes SCM.doc` | HIGH | 23040 | `EF210A05C40C251F44969F7450060AC113496371A9FFA64677755EA2DCC770C6` |
| `CONTRAT FRAIS COMMUNS.docx` | `project/source_import/raw_drive_dump/creation scm/CONTRAT FRAIS COMMUNS.docx` | HIGH | 513893 | `CB8E0B477AB6D41A214BB3F4C7D6EDBFB90202203B92AAF72020D047BEF03E50` |
| `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx` | `project/source_import/raw_drive_dump/creation scm/2024 REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx` | HIGH avec ecart de nom documente | 216795 | `656A11671F834954B5A85C8B8093DCAB6BB93D892B7AB791D194707C732D3784` |

Note : les chemins ci-dessus sont normalises sans accents pour la lisibilite. Les fichiers physiques conservent leurs noms exacts sur disque, sauf le reglement interieur dont la source brute portait le prefixe `2024` et dont la cible reprend le nom demande par le ticket.

## Sources manquantes

Aucune source demandee n'est manquante apres preparation.

## Validations techniques

- les quatre copies ont un hash identique a leur source brute ;
- les trois fichiers `.docx` copies contiennent `word/document.xml` ;
- le fichier `Liste depenses communes SCM.doc` est une source legacy `.doc`, conforme au nom demande par la source de verite et par le ticket ;
- aucun fichier Python n'a ete modifie ;
- `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` n'ont pas ete modifies.

## Points bloquants eventuels

- `Liste depenses communes SCM.doc` est un format legacy `.doc` : une conversion ou un remplacement DOCX propre sera necessaire avant toute analyse fine ou automatisation.
- Le reglement interieur a ete trouve dans le raw dump avec le prefixe `2024`. Le contenu a ete copie sans modification, mais l'ecart de nom doit rester visible lors de la future specification.

## Prochaine etape recommandee

Ouvrir un ticket de specification limite aux satellites SCM, sans codage, pour analyser separement :

- le pacte d'associes SCM ;
- la liste des depenses communes SCM ;
- le contrat de frais communs ;
- le reglement interieur SCM.
