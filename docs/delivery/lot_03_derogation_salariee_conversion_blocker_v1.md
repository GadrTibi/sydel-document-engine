# DAAT x SYDEL - BLOCAGE CONVERSION SOURCE V1
## Ticket `CONVERT-DEROG-SALARIEE-001`

## 1. Objet

Ce document cloture la tentative de conversion du fichier legacy :

- `Demande_derogation_cumul_SELARL_salariee.doc`

Conclusion :

- aucune version DOCX exploitable n'a pu etre produite ;
- aucun fichier `project/source_documents/lot_03/Demande_derogation_cumul_SELARL_salariee.docx` n'est livre ;
- la sous-famille documentaire `cumul_salariee` reste bloquee pour tout codage tant qu'une source DOCX propre n'est pas fournie ou qu'un convertisseur headless fiable n'est pas disponible.

## 2. Source legacy controlee

Source lue en lecture seule :

- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`

Dans le worktree Git propre de la branche, le `raw_drive_dump` n'est pas versionne. La tentative a donc utilise le chemin absolu de la source locale existante :

- `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\project\source_import\raw_drive_dump\Creation SELAS\Derogation\Demande_derogation_cumul_SELARL_salariee.doc`

Controle fichier :

| Fichier | Taille | SHA256 | Signature binaire |
|---|---:|---|---|
| `Demande_derogation_cumul_SELARL_salariee.doc` | 21504 | `F5CA40CAA9116C52C7AC10FAAEDB08272D8747D30D53DA2CA51300F5F63594CF` | OLE compound document, debut `D0 CF 11 E0 A1 B1 1A E1` |

## 3. Outils de conversion disponibles

Controle local :

| Outil | Resultat |
|---|---|
| Microsoft Word / `WINWORD.EXE` | installe dans `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE` |
| `LibreOffice` / `soffice` | non trouve dans le PATH ni dans les emplacements standards `Program Files` |
| `pandoc` | non trouve |
| `antiword` | non trouve |
| `catdoc` | non trouve |

Un processus Word utilisateur etait deja ouvert avant la tentative (`demande_inscription_ordre - Mode de compatibilite - Word`). Il n'a pas ete arrete.

## 4. Tentative effectuee

Commande de conversion :

- pilotage Word par COM via `Word.Application` ;
- ouverture du `.doc` en lecture seule ;
- `DisplayAlerts = 0` ;
- `AutomationSecurity = 3` ;
- `ConfirmConversions = false` ;
- `UpdateLinksAtOpen = false` ;
- conversion cible par `SaveAs2(..., wdFormatXMLDocument)` vers :
  - `project/source_documents/lot_03/Demande_derogation_cumul_SELARL_salariee.docx`.

Resultat :

- la tentative s'est terminee sans produire de DOCX ;
- Word COM a leve l'erreur suivante :
  - `Echec de l'appel de procedure distante. (Exception de HRESULT : 0x800706BE)` ;
- le fichier cible `project/source_documents/lot_03/Demande_derogation_cumul_SELARL_salariee.docx` n'existe pas apres tentative ;
- aucun nouveau processus Word persistant issu de la tentative n'a ete conserve.

## 5. Blocage retenu

La source n'est pas convertible de facon fiable dans l'environnement local actuel.

Motifs :

- la seule voie locale disponible est Word COM ;
- Word COM echoue avant production du DOCX ;
- aucun convertisseur headless fiable n'est disponible localement ;
- aucun document converti ne peut etre relu ni compare au wording source ;
- une conversion approximative serait contraire aux garde-fous du projet.

## 6. Impact

Document concerne :

- demande de derogation cumul SELARL salariee.

Sous-famille :

- `cumul_salariee`.

Statut documentaire :

- source legacy identifiee ;
- conversion retentee ;
- source DOCX exploitable non disponible ;
- codage interdit tant qu'une source propre n'est pas fournie.

## 7. Prochaine etape recommandee

Fournir une version DOCX propre depuis une session Word humaine controlee, ou installer un convertisseur headless fiable puis relancer le ticket de conversion avec controle du texte et des placeholders.

