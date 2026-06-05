# EURL — Inventaire des modèles tokenisés

> **Statut : AUCUN MODÈLE EURL TROUVÉ.**
> Scan effectué le 2026-06-05 sur le Drive source
> `C:\Users\Gad\Downloads\Documents avec variables-20260604T122837Z-3-001`
> (lecture seule). Méthode : glob récursif de tous les `.docx` + lecture du **contenu**
> de chaque fichier (python-docx / unzip `word/document.xml`), pas seulement du nom de fichier
> (conformément à Phase 1 du `WORKFLOW_TYPE_ENTREPRISE_V1.md` : « vérifier qu'on a tous les cas
> en lisant le CONTENU, pas le nom de fichier »).

## Résultat du scan

| Critère | Résultat |
|---|---|
| Fichiers `.docx` totaux scannés sur le Drive | **125** |
| Fichiers dont le **nom** contient « EURL » (toutes graphies / accents) | **0** |
| Fichiers dont le **contenu** mentionne « EURL » (regex `\bE\.?U\.?R\.?L\.?\b`) | **0** |
| Dossier `Création EURL` sur le Drive | **absent** |

Les dossiers présents sur le Drive sont : `Création SCI`, `Création SAS`, `Création SCP`,
`Création SCS`, `Création SELARL`, `Création SELAS`, `Création SPFPL`, `création scm`,
`Variables finales`. **Aucun dossier EURL.**

## Tableau des modèles EURL

| Modèle | Variables tokenisées `[..]` qu'il contient | Ce que le document paraît être |
|---|---|---|
| _(aucun)_ | _(n/a)_ | _(n/a)_ |

**Aucun modèle EURL à inventorier.** Le tableau reste vide tant que les modèles n'ont pas été
fournis. Aucun dossier `project/source_documents/eurl/` n'a été créé (rien à y ranger).

## Conséquence

La fondation EURL **ne peut pas démarrer** côté moteur : il n'y a ni modèle source tokenisé, ni
carte cas→documents (voir `CARTOGRAPHIE_TENTATIVE.md` et `STATUT.md`). Le premier livrable attendu
est la **fourniture des modèles EURL** (prompt n°1 de `NOTEBOOKLM_PROMPTS.md`), puis la **carte
officielle cas→documents** (prompt n°2).

## Note de méthode (anti-confusion)

« EURL » et « SELARL » sont des structures **distinctes**. La présence du segment « ...ARL » dans
SELARL ne doit jamais faire prendre un modèle SELARL pour un modèle EURL. Le scan a explicitement
exclu les correspondances SELARL/SELAS. De même, le canon `Documents_a_generer_par_cas_V3.docx`
mentionne SELARL 23 fois et EURL **0 fois** : ce n'est pas un canon EURL.
