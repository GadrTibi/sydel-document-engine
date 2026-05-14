# DAAT x SYDEL - PREPARATION SOURCES V1
## Famille `derogations`

## 1. Objet

Ce fichier cloture la preparation documentaire du ticket `PREP-DEROG-001`.

Perimetre respecte :

- preparation de sources uniquement ;
- aucun code Python modifie ;
- aucune UI modifiee ;
- `docs/project/01_EXECUTION_BOARD.md` non modifie ;
- `docs/project/04_LAST_STATE.md` non modifie ;
- aucun wording juridique source modifie.

## 2. Sources HIGH copiees en Lot 03

Les sources suivantes ont ete retrouvees dans le raw dump et copiees dans :

- `project/source_documents/lot_03/`

| Source Lot 03 | Statut | Taille | SHA256 |
|---|---|---:|---|
| `Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL.docx` | copiee | 510440 | `F7C2DA89A5DCC9B30BF5C10DB82CE2D80157239FA6B73A8E87B1C1A43742E6B1` |
| `Demande de dérogation cumul SELARL - BNC.docx` | copiee | 344781 | `8EEB261EB3CFF7D5D3C0EFD477A997EDD5C140BA204E74DB94CAEC7793B024E9` |

Validation technique :

- les deux fichiers sont des DOCX lisibles ;
- `word/document.xml` est present dans chaque fichier ;
- les placeholders attendus restent detectables.

Placeholders observes :

| Source | Placeholders detectes |
|---|---:|
| `Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL.docx` | 11 |
| `Demande de dérogation cumul SELARL - BNC.docx` | 15 |

## 3. Fichier legacy `.doc`

Fichier traite :

- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`

Statut :

- source legacy identifiee ;
- conversion locale fiable impossible dans ce ticket ;
- aucun DOCX cible n'est produit ;
- rapport detaille disponible dans `docs/delivery/lot_03_derogations_legacy_conversion_report_v1.md`.

La sous-famille `cumul_salariee` reste bloquee avant code.

## 4. Pret pour futur code

Les elements suivants sont prets comme sources placees :

- `multi_sites_sel` : source DOCX SELARL placee dans `project/source_documents/lot_03/` ;
- `cumul_sel_bnc` : source DOCX placee dans `project/source_documents/lot_03/`.

Ces sources ne suffisent pas seules a lancer un generateur finalise. Les futures taches de code devront toujours respecter :

- la spec canonique V1 ;
- la spec texte V1 ;
- les arbitrages V1 ;
- le mode de rendu explicite `document finalise` ou `formulaire a completer` ;
- les blocages sur zones narratives, cases cochees et explications obligatoires.

## 5. Pas encore pret

Restent non prets pour code :

- `cumul_salariee` : source encore en `.doc` legacy, DOCX propre absent ;
- `site_distinct_manual` : formulaire manuel selon la source de verite ;
- `sel_bnc_manual` : piece manuelle, hors automatisation initiale ;
- toutes les zones narratives sensibles non fournies explicitement par contexte dossier.

## 6. Recommandation suivante

Prochaine etape recommandee :

- ouvrir un ticket de code limite a `multi_sites_sel` ou `cumul_sel_bnc`, en portant explicitement le mode de rendu ;
- traiter `cumul_salariee` seulement apres fourniture ou conversion validee d'un DOCX propre.
