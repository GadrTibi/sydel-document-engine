# DAAT x SYDEL - SPEC CANONIQUE V1
## Famille `Demande d'inscription a l'ordre`

## 1. Objet

Formaliser la spec canonique de la famille documentaire `Demande d'inscription a l'ordre`, a partir :
- de la source de verite metier ;
- de la source Lot 2 deja placee ;
- des variantes et collisions pertinentes presentes dans le raw dump.

Cette spec ne code rien et ne modifie aucun wording juridique source. Elle prepare une spec texte dediee avant tout ticket de code.

## 2. Sources lues

### Memoire projet et referentiels

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`
- `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`
- `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`
- `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire.
- ADR-0002 : moteur par document canonique.
- ADR-0003 : livraison par lots documentaires.
- ADR-0005 : mode Codex repo-first.

### Sources DOCX

La source demandee par le ticket, `project/source_documents/lot_02/Demande d'inscription a l'ordre.docx`, n'existe pas litteralement dans le depot.

La source Lot 2 presente et lue est :
- `project/source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx`

Source de verite metier lue :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Variantes raw dump lues :
- `project/source_import/raw_drive_dump/Création SELARL/Documents de base/Demande d_inscription à l_ordre.docx`
- `project/source_import/raw_drive_dump/Création SELAS/Documents de base/Demande d_inscription à l_ordre_SELAS.docx`
- `project/source_import/raw_drive_dump/Création SPFPL/Demande d_inscription à l_ordre - transforme.docx`
- `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Documents de base/Demande d_inscription à l_ordre.docx`
- `project/source_import/raw_drive_dump/Création SPFPL/apport/Documents de base/Copie de Demande d_inscription à l_ordre.docx`

Fichiers volontairement non retenus comme variantes de cette famille :
- les demandes ou formulaires de derogation, qui relevent d'une famille documentaire distincte ;
- aucun fichier SCM raw, car le repertoire `création scm` ne contient pas de source exploitable pour cette demande.

## 3. Perimetre documentaire retenu

La source de verite metier rattache `Demande d'inscription a l'ordre.docx` aux structures suivantes :

- SELARL ;
- SELAS ;
- SPFPL cession ;
- SPFPL apport ;
- SCM.

Structures hors perimetre de cette famille, d'apres la source de verite et l'arbre moteur V1 :

- SAS ;
- SCS ;
- SCI / SCI IRIS.

Observation importante :
- les variantes effectivement presentes dans le raw dump couvrent SELARL, SELAS et SPFPL ;
- SCM est retenue dans le perimetre car elle apparait dans la source de verite et l'arbre moteur V1, mais aucune variante SCM specifique n'a ete retrouvee dans le raw dump.

## 4. Comparaison des variantes

### 4.1 Groupes compares

| Groupe | Fichiers | Constat |
|---|---|---|
| SPFPL / source Lot 2 | source Lot 2 + SPFPL racine + SPFPL cession + SPFPL apport | Copies exactes, hash identique `bf98888134cb4960cdc3ac68b8e31b23f6c1ca21b930696b5c60e4afb3714826`. |
| SELARL | raw `Création SELARL/Documents de base` | Texte visible identique a SELAS, mais hash DOCX distinct. |
| SELAS | raw `Création SELAS/Documents de base` | Texte visible identique a SELARL, mais hash DOCX distinct. |

### 4.2 Noyau commun a toutes les variantes

Toutes les variantes contiennent :
- un bloc expediteur avec `Dr [prenom] [nom]` ;
- une profession affichee sous l'identite du signataire ;
- l'adresse personnelle du signataire ;
- un bloc destinataire `Conseil departemental de l'Ordre` ;
- une ligne de profession reglementee au pluriel ou assimilee ;
- une adresse du Conseil departemental de l'Ordre ;
- `Objet : Demande d'inscription au tableau de l'Ordre` ;
- `Monsieur le President,` ;
- la phrase d'envoi du dossier de constitution de la societe ;
- la demande d'inscription de la societe au tableau de l'Ordre ;
- la phrase indiquant que le signataire ne sera dans une seule structure ;
- un pouvoir donne a un mandataire SYDEL ;
- la formule de politesse ;
- une signature finale `Dr [prenom] [nom]`.

### 4.3 Differences observees

| Zone | SELARL / SELAS | SPFPL / source Lot 2 | Analyse |
|---|---|---|---|
| Profession expediteur | `[profession_reglementee]` | `[profession]` | Meme emplacement fonctionnel, nom de placeholder divergent. |
| Profession dans destinataire et corps | `[profession_reglementee_pluriel]` | `[profession_reglementee]` | SELARL/SELAS distinguent singulier/pluriel ; SPFPL reutilise un seul champ. |
| Adresse ordre | `[adresse_conseil_ordre]` + `[cp_ordre] [ville_ordre]` | `[adresse_ordre]` | Meme donnee fonctionnelle, granularite differente. |
| Mandataire | `[civilite_mandataire] [prenom_mandataire] [nom_mandataire], [fonction_mandataire] du cabinet [denomination_cabinet_mandataire]` | `Monsieur Jordan ELBAZ, gerant du cabinet SYDEL` | SELARL/SELAS permettent un mandataire configurable ; SPFPL fige SYDEL/Jordan ELBAZ. |
| Derogation | Aucune mention `Derogation ?` | Mention residuelle `Derogation ?` a la fin du paragraphe d'inscription | Anomalie source probable, non traitee comme texte canonique sans validation. |
| Nombre de lignes adresse ordre | Deux lignes | Une ligne | Difference de rendu et de mapping, pas de difference juridique evidente. |

## 5. Texte fixe canonique fonctionnel

Le noyau fonctionnel canonique est le suivant. Les formulations ci-dessous reprennent le wording source visible, sauf remplacement des placeholders locaux par des roles canoniques. Le ticket `SPEC-TEXTE-ORDRE-001` devra stabiliser le texte final exact avant code, notamment les apostrophes typographiques et les accents.

```text
Dr {signataire.prenom} {signataire.nom}
{ordre.profession_signataire_affichee}
{signataire.adresse_personnelle_affichee}

Conseil departemental de l'Ordre
Des {ordre.profession_reglementee_pluriel}
{ordre.adresse_affichee}

{signature.lieu}, le {signature.date}

Objet : Demande d’inscription au tableau de l’Ordre

Monsieur le Président,

Vous trouverez ci-joint le dossier de constitution de ma société dénommée {societe.denomination}.

Je sollicite l’inscription de ma société au tableau de l’Ordre des {ordre.profession_reglementee_pluriel}. Je précise que je ne serai associé et praticien et exerçant que dans une seule structure.

Je donne pouvoir à {mandataire.civilite_affichage} {mandataire.prenom} {mandataire.nom}, {mandataire.fonction} du cabinet {mandataire.cabinet} pour effectuer les formalités.

Je vous prie d’agréer, Monsieur le Président, l’expression de mes sentiments dévoués.

Dr {signataire.prenom} {signataire.nom}
```

Notes de canonisation :
- la formulation ci-dessus suit le variant SELARL/SELAS pour les variables ordinales et le mandataire, car il est plus explicite et ne contient pas la mention residuelle `Derogation ?` ;
- cette spec ne valide pas juridiquement la suppression de `Derogation ?` pour une future generation ; elle classe cette mention comme anomalie a arbitrer dans `SPEC-TEXTE-ORDRE-001` ;
- les accents et apostrophes typographiques devront etre controles dans la spec texte, a partir des sources DOCX et sans correction implicite.

## 6. Variables canoniques attendues

### 6.1 Dossier / structure

- `dossier.structure`
- `dossier.options.derogation`

### 6.2 Signataire

- `signataire.titre_affichage` : valeur source observee `Dr`.
- `signataire.genre`
- `signataire.prenom`
- `signataire.nom`
- `signataire.profession_affichee` ou `ordre.profession_signataire_affichee`
- `signataire.adresse_personnelle_affichee`

Note : le dictionnaire V1 contient des champs d'adresse personnelle separes. Pour ce document, la source attend une adresse affichee complete. La spec texte devra decider si elle est fournie directement ou assemblee depuis les champs structurés.

### 6.3 Societe

- `societe.denomination`

### 6.4 Ordre professionnel

- `ordre.profession_reglementee_singulier` ou `ordre.profession_signataire_affichee`
- `ordre.profession_reglementee_pluriel`
- `ordre.conseil_departemental_libelle`
- `ordre.adresse_affichee`
- `ordre.adresse.ligne_1` optionnel
- `ordre.adresse.cp` optionnel
- `ordre.adresse.ville` optionnel
- `ordre.destinataire_appel`

Decision V1 de spec :
- conserver un role canonique `ordre`, car les placeholders SELARL/SELAS et SPFPL nomment les memes donnees ordinales avec des granularites differentes ;
- ne pas encoder directement `[profession]`, `[profession_reglementee]`, `[profession_reglementee_pluriel]`, `[adresse_ordre]` ou `[adresse_conseil_ordre]` comme verite moteur.

### 6.5 Mandataire

- `mandataire.civilite_affichage`
- `mandataire.prenom`
- `mandataire.nom`
- `mandataire.fonction`
- `mandataire.cabinet`

Decision V1 de spec :
- le mandataire peut etre pre-rempli par configuration SYDEL avec `Monsieur Jordan ELBAZ, gerant du cabinet SYDEL` ;
- le generateur ne doit pas coder cette identite en dur si un bloc de configuration mandataire existe ou est introduit.

### 6.6 Signature

- `signature.lieu`
- `signature.date`

## 7. Mapping source vers canonique

| Placeholder / texte source | Variable canonique cible | Note |
|---|---|---|
| `Dr` | `signataire.titre_affichage` | Fixe dans toutes les sources, mais a conserver comme donnee affichable. |
| `[prenom]` | `signataire.prenom` | Existant. |
| `[nom]` | `signataire.nom` | Existant. |
| `[profession]` | `ordre.profession_signataire_affichee` | Variante SPFPL/source Lot 2. |
| `[profession_reglementee]` en ligne expediteur | `ordre.profession_signataire_affichee` | Variante SELARL/SELAS. |
| `[profession_reglementee]` apres `Des` ou `Ordre des` | `ordre.profession_reglementee_pluriel` | Variante SPFPL/source Lot 2, nom ambigu. |
| `[profession_reglementee_pluriel]` | `ordre.profession_reglementee_pluriel` | Variante SELARL/SELAS, nom le plus explicite. |
| `[adresse_personnelle]` | `signataire.adresse_personnelle_affichee` | Adresse source complete affichee. |
| `[adresse_ordre]` | `ordre.adresse_affichee` | Variante SPFPL/source Lot 2. |
| `[adresse_conseil_ordre]` | `ordre.adresse.ligne_1` ou `ordre.adresse_affichee` | Variante SELARL/SELAS. |
| `[cp_ordre]` | `ordre.adresse.cp` | Variante SELARL/SELAS. |
| `[ville_ordre]` | `ordre.adresse.ville` | Variante SELARL/SELAS. |
| `[lieu_signature]` | `signature.lieu` | Existant. |
| `[date_signature]` | `signature.date` | Existant. |
| `[denomination_societe]` | `societe.denomination` | Existant. |
| `[civilite_mandataire]` | `mandataire.civilite_affichage` | Variante SELARL/SELAS. |
| `[prenom_mandataire]` | `mandataire.prenom` | Variante SELARL/SELAS. |
| `[nom_mandataire]` | `mandataire.nom` | Variante SELARL/SELAS. |
| `[fonction_mandataire]` | `mandataire.fonction` | Variante SELARL/SELAS. |
| `[denomination_cabinet_mandataire]` | `mandataire.cabinet` | Variante SELARL/SELAS. |
| `Monsieur Jordan ELBAZ, gerant du cabinet SYDEL` | valeurs par defaut du role `mandataire` | Variante SPFPL/source Lot 2. |

## 8. Blocs conditionnels et structurels

### 8.1 Bloc derogation

Constat :
- les variantes SELARL/SELAS ne contiennent pas `Derogation ?` ;
- les variantes SPFPL/source Lot 2 contiennent `Derogation ?` comme suffixe du paragraphe d'inscription ;
- la source de verite contient par ailleurs des documents de derogation distincts.

Decision V1 de spec :
- ne pas traiter `Derogation ?` comme texte fixe canonique ;
- ne pas inventer de phrase de derogation dans cette demande ;
- si `dossier.options.derogation == true`, le comportement exact doit rester bloque jusqu'a `SPEC-TEXTE-ORDRE-001` ou arbitrage metier.

### 8.2 Bloc mandataire

Constat :
- toutes les variantes ont un pouvoir donne a un mandataire SYDEL ;
- SELARL/SELAS parametrent ce mandataire ;
- SPFPL/source Lot 2 figent Jordan ELBAZ / SYDEL.

Decision V1 de spec :
- bloc commun, non conditionnel ;
- rendu cible base sur `mandataire.*` ;
- configuration par defaut possible, mais pas de constante magique dans le generateur.

### 8.3 Bloc adresse ordre

Constat :
- SPFPL/source Lot 2 utilise une seule zone `[adresse_ordre]` ;
- SELARL/SELAS utilisent adresse + code postal + ville.

Decision V1 de spec :
- accepter un affichage canonique `ordre.adresse_affichee` ;
- permettre une construction depuis `ordre.adresse.ligne_1`, `ordre.adresse.cp`, `ordre.adresse.ville` si ces champs sont disponibles ;
- la spec texte devra fixer le rendu en une ou deux lignes.

## 9. Accords de genre et nombre

Les sources utilisent :
- `Dr` fixe ;
- `Monsieur le President` fixe ;
- `associe`, `praticien`, `exercant` au masculin singulier ;
- aucune variante feminine explicite.

Regles de prudence avant code :
- ne pas feminiser automatiquement `associe`, `praticien`, `exercant` sans validation ;
- ne pas remplacer automatiquement `Monsieur le President` par `Madame la Presidente` sans source ou decision ;
- conserver `signataire.genre` comme variable grammaticale disponible, mais bloquer toute variation non specifiee ;
- conserver `signataire.titre_affichage` pour eviter de coder `Dr` en dur si une decision ulterieure impose une variante.

## 10. Ce qui reste manuel ou reference

Doivent rester fournis par le contexte dossier, une configuration de reference ou une saisie humaine :
- profession affichee du signataire ;
- profession reglementee plurielle attendue apres `Ordre des` ;
- adresse du Conseil departemental de l'Ordre ;
- mandataire SYDEL si non preconfigure ;
- lieu et date de signature.

Doit rester hors automatisation a ce stade :
- toute phrase specifique de derogation ;
- toute adaptation au cas d'exercice dans plusieurs structures ;
- toute variation du destinataire ordinal non presente dans les sources.

## 11. Anomalies et ambiguites

1. La source Lot 2 est une copie exacte des variantes SPFPL, pas une source neutre couvrant toutes les structures.
2. Les variantes SELARL/SELAS sont plus explicites pour les variables, mais ne sont pas encore placees dans `source_documents`.
3. `Derogation ?` apparait uniquement dans le groupe SPFPL/source Lot 2 et ressemble a une note residuelle.
4. Les placeholders de profession divergent : `[profession]`, `[profession_reglementee]`, `[profession_reglementee_pluriel]`.
5. Les placeholders d'adresse ordinale divergent : `[adresse_ordre]` contre `[adresse_conseil_ordre]`, `[cp_ordre]`, `[ville_ordre]`.
6. Le mandataire est hard-code dans le groupe SPFPL/source Lot 2 et variable dans SELARL/SELAS.
7. SCM est dans le perimetre de la source de verite, mais aucune variante SCM n'a ete retrouvee.
8. Le wording `associe et praticien et exercant` est commun aux variantes, mais reste grammaticalement et juridiquement a valider.

## 12. Points ouverts avant code

Avant tout ticket de code, il faut trancher :

1. Faut-il supprimer, ignorer ou transformer la mention `Derogation ?` ?
2. Le texte final doit-il suivre strictement SELARL/SELAS, SPFPL/source Lot 2, ou une fusion canonique documentee ?
3. Le mandataire doit-il etre une configuration globale SYDEL ou une entree dossier ?
4. `Dr` est-il toujours applicable aux professions couvertes par SELARL, SELAS, SPFPL et SCM ?
5. `Monsieur le President` doit-il rester fixe ou devenir variable ?
6. Les accords feminins de `associe`, `praticien`, `exercant` doivent-ils etre pris en charge ?
7. Le rendu de l'adresse ordinale doit-il etre une zone complete ou trois champs assembles ?
8. SCM peut-elle utiliser le texte canonique commun sans source SCM dediee ?

## 13. Critere de completion de SPEC-ORDRE-001

`SPEC-ORDRE-001` est complet pour ouvrir le ticket suivant :

- `SPEC-TEXTE-ORDRE-001 | Stabiliser le texte canonique et les variantes de Demande d'inscription a l'ordre`

Le ticket de code ne doit pas demarrer avant cette spec texte, car les points de wording ci-dessus restent ouverts.
