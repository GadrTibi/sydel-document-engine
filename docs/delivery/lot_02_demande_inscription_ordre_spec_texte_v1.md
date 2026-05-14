# DAAT x SYDEL — SPEC TEXTE V1
## Famille `Demande d'inscription à l'ordre`

## 1. Objet

Stabiliser le texte canonique et les variantes structurelles de la famille documentaire `Demande d'inscription à l'ordre`, sans coder.

Cette spec texte complète :
- `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`

Elle vise à préparer un générateur déterministe qui :
- couvre SELARL, SELAS, SPFPL cession, SPFPL apport et SCM ;
- distingue le tronc commun des overlays par famille ;
- ne transforme pas la mention source `Dérogation ?` en wording juridique automatique ;
- traite le titre `Dr`, l'appel `Monsieur le Président`, la profession ordinale et l'adresse ordinale comme variables ou blocs variables ;
- rend le mandataire SYDEL configurable lorsqu'il est présent dans la source.

## 2. Sources lues

Mémoire projet et référentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`

Source de vérité métier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Source Lot 2 présente et lue :
- `project/source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx`

Note de chemin :
- le chemin demandé `project/source_documents/lot_02/Demande d'inscription à l'ordre.docx` n'existe pas littéralement dans le dépôt ;
- la source équivalente placée dans `source_documents` est le fichier transformé ci-dessus.

Variantes raw dump lues :
- `project/source_import/raw_drive_dump/Création SELARL/Documents de base/Demande d_inscription à l_ordre.docx`
- `project/source_import/raw_drive_dump/Création SELAS/Documents de base/Demande d_inscription à l_ordre_SELAS.docx`
- `project/source_import/raw_drive_dump/Création SPFPL/Demande d_inscription à l_ordre - transforme.docx`
- `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Documents de base/Demande d_inscription à l_ordre.docx`
- `project/source_import/raw_drive_dump/Création SPFPL/apport/Documents de base/Copie de Demande d_inscription à l_ordre.docx`

ADR applicables :
- ADR-0001 : source de vérité documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : génération DOCX propre from-scratch pour le futur ticket code ;
- ADR-0005 : mode Codex repo-first.

## 3. Périmètre famille

Structures couvertes en V1 :
- SELARL ;
- SELAS ;
- SPFPL cession ;
- SPFPL apport ;
- SCM.

Structures hors périmètre de cette famille :
- SAS ;
- SCS ;
- SCI / SCI IRIS.

Décision V1 :
- SELARL et SELAS partagent un overlay texte identique ;
- SPFPL cession et SPFPL apport partagent un overlay texte identique avec la source Lot 2 ;
- SCM est couverte par le tronc commun paramétré, même sans variante raw dédiée retrouvée.

## 4. Texte source extrait

### 4.1 Source Lot 2 / SPFPL

```text
Dr [prenom] [nom]
[profession]
[adresse_personnelle]

Conseil départemental de l’Ordre
Des [profession_reglementee]
[adresse_ordre]

[lieu_signature], le [date_signature]

Objet : Demande d’inscription au tableau de l’Ordre

Monsieur le Président,

Vous trouverez ci-joint le dossier de constitution de ma société dénommée [denomination_societe].

Je sollicite l’inscription de ma société au tableau de l’Ordre des [profession_reglementee]. Je précise que je ne serai associé et praticien et exerçant que dans une seule structure. Dérogation ?

Je donne pouvoir à Monsieur Jordan ELBAZ, gérant du cabinet SYDEL pour effectuer les formalités.

Je vous prie d’agréer, Monsieur le Président, l’expression de mes sentiments dévoués.

Dr [prenom] [nom]
```

### 4.2 Variantes SELARL / SELAS

```text
Dr [prenom] [nom]
[profession_reglementee]
[adresse_personnelle]

Conseil départemental de l’Ordre
Des [profession_reglementee_pluriel]
[adresse_conseil_ordre]
[cp_ordre] [ville_ordre]

[lieu_signature], le [date_signature]

Objet : Demande d’inscription au tableau de l’Ordre

Monsieur le Président,

Vous trouverez ci-joint le dossier de constitution de ma société dénommée [denomination_societe].

Je sollicite l’inscription de ma société au tableau de l’Ordre des [profession_reglementee_pluriel]. Je précise que je ne serai associé et praticien et exerçant que dans une seule structure.

Je donne pouvoir à [civilite_mandataire] [prenom_mandataire] [nom_mandataire], [fonction_mandataire] du cabinet [denomination_cabinet_mandataire] pour effectuer les formalités.

Je vous prie d’agréer, Monsieur le Président, l’expression de mes sentiments dévoués.

Dr [prenom] [nom]
```

## 5. Tronc commun texte fixe

Le tronc commun ci-dessous reprend le wording source visible. Les variations observées sont isolées dans les overlays de la section 6.

```text
{signataire.titre_affichage} {signataire.prenom} {signataire.nom}
{ordre.profession_signataire_affichee}
{signataire.adresse_personnelle_affichee}

{ordre.conseil_departemental_libelle}
Des {ordre.profession_ligne_destinataire}
{ordre.adresse_bloc_affiche}

{signature.lieu}, le {signature.date}

Objet : Demande d’inscription au tableau de l’Ordre

{ordre.destinataire_appel},

Vous trouverez ci-joint le dossier de constitution de ma société dénommée {societe.denomination}.

Je sollicite l’inscription de ma société au tableau de l’Ordre des {ordre.profession_reglementee_pluriel}. Je précise que je ne serai associé et praticien et exerçant que dans une seule structure.{ordre.derogation_suffixe}

Je donne pouvoir à {mandataire.libelle_affiche} pour effectuer les formalités.

Je vous prie d’agréer, {ordre.destinataire_appel}, l’expression de mes sentiments dévoués.

{signataire.titre_affichage} {signataire.prenom} {signataire.nom}
```

Règles de fidélité :
- `associé et praticien et exerçant` est conservé en V1 malgré sa lourdeur grammaticale ;
- `Objet : Demande d’inscription au tableau de l’Ordre` conserve la casse source ;
- la formule de politesse conserve l'appel ordinal fourni par `ordre.destinataire_appel` ;
- aucune féminisation automatique de `associé`, `praticien`, `exerçant`, `Président` ou `Dr` n'est introduite en V1.

## 6. Variantes structurelles par famille

### 6.1 Overlay SELARL / SELAS

Familles :
- SELARL ;
- SELAS.

Source :
- variantes raw dump SELARL et SELAS, texte visible identique.

Règles de rendu :
- `ordre.profession_signataire_affichee` provient de l'alias source `[profession_reglementee]` ;
- `ordre.profession_ligne_destinataire` et `ordre.profession_reglementee_pluriel` proviennent de `[profession_reglementee_pluriel]` ;
- `ordre.adresse_bloc_affiche` est rendu sur deux lignes :

```text
{ordre.adresse.ligne_1}
{ordre.adresse.cp} {ordre.adresse.ville}
```

- `mandataire.libelle_affiche` est assemblé depuis :

```text
{mandataire.civilite_affichage} {mandataire.prenom} {mandataire.nom}, {mandataire.fonction} du cabinet {mandataire.cabinet}
```

- `ordre.derogation_suffixe` est vide, sauf si un bloc manuel de dérogation est explicitement fourni.

### 6.2 Overlay SPFPL cession / SPFPL apport

Familles :
- SPFPL cession ;
- SPFPL apport.

Source :
- source Lot 2 ;
- variantes raw dump SPFPL racine, cession SPFPL et apport SPFPL, copies visibles identiques.

Règles de rendu :
- `ordre.profession_signataire_affichee` provient de l'alias source `[profession]` ;
- `ordre.profession_ligne_destinataire` et `ordre.profession_reglementee_pluriel` proviennent de l'alias source `[profession_reglementee]`, dont le nom est ambigu mais l'emplacement est pluriel après `Des` / `Ordre des` ;
- `ordre.adresse_bloc_affiche` est rendu depuis `ordre.adresse_affichee`, en une ou plusieurs lignes déjà préparées par le contexte ;
- le mandataire source `Monsieur Jordan ELBAZ, gérant du cabinet SYDEL` devient une configuration par défaut possible de `mandataire.libelle_affiche` ;
- le générateur ne doit pas coder `Jordan ELBAZ` ou `SYDEL` en dur.

### 6.3 Overlay SCM

Famille :
- SCM.

Source :
- la source de vérité métier et l'arbre moteur V1 rattachent la demande d'inscription à l'ordre à SCM ;
- aucune variante SCM dédiée n'a été retrouvée dans le raw dump.

Règles de rendu :
- utiliser le tronc commun paramétré ;
- accepter `ordre.adresse_affichee` ou le triplet `ordre.adresse.ligne_1`, `ordre.adresse.cp`, `ordre.adresse.ville` ;
- ne pas ajouter de wording SCM spécifique sans source reçue ;
- ne pas imposer le mandataire SYDEL hard-codé si une configuration mandataire différente est fournie ;
- bloquer la génération si les variables ordinales SCM ne sont pas fournies.

## 7. Blocs conditionnels

### 7.1 Bloc dérogation

Constat source :
- SELARL et SELAS ne contiennent aucune mention `Dérogation ?` ;
- SPFPL/source Lot 2 contiennent `Dérogation ?` à la fin du paragraphe d'inscription ;
- la source de vérité contient des documents de dérogation distincts.

Décision V1 :
- ne pas rendre le littéral `Dérogation ?` comme texte juridique final ;
- traiter cette zone comme un bloc conditionnel manuel piloté par `dossier.options.derogation`.

Règles de génération :
- si `dossier.options.derogation == false` ou absent : `ordre.derogation_suffixe` est vide ;
- si `dossier.options.derogation == true` et `ordre.derogation_mention_manuelle` est absent : bloquer la génération avec une erreur explicite ;
- si `dossier.options.derogation == true` et `ordre.derogation_mention_manuelle` est fourni : rendre cette mention après la phrase `une seule structure.` avec une espace préalable.

Exemple de forme technique, sans wording imposé :

```text
... une seule structure. {ordre.derogation_mention_manuelle}
```

### 7.2 Bloc mandataire

Constat source :
- le pouvoir au mandataire existe dans toutes les variantes ;
- SELARL/SELAS le paramètrent ;
- SPFPL/source Lot 2 le figent sur SYDEL.

Décision V1 :
- bloc commun obligatoire ;
- `mandataire.libelle_affiche` peut être assemblé depuis `mandataire.*` ou fourni par configuration ;
- une configuration par défaut SYDEL peut exister hors générateur ;
- si aucun mandataire n'est résolu, bloquer la génération.

## 8. Variables canoniques attendues

### 8.1 Dossier

- `dossier.structure`
- `dossier.options.derogation`

Valeurs `dossier.structure` acceptées en V1 :
- `SELARL`
- `SELAS`
- `SPFPL_CESSION`
- `SPFPL_APPORT`
- `SCM`

### 8.2 Signataire

- `signataire.titre_affichage`
- `signataire.prenom`
- `signataire.nom`
- `signataire.adresse_personnelle_affichee`

Règles :
- `signataire.titre_affichage` vaut `Dr` dans les sources lues, mais reste une variable affichable ;
- `signataire.genre` peut exister dans le contexte, mais ne pilote aucune variation de wording en V1.

### 8.3 Société

- `societe.denomination`

### 8.4 Ordre professionnel

- `ordre.conseil_departemental_libelle`
- `ordre.destinataire_appel`
- `ordre.profession_signataire_affichee`
- `ordre.profession_ligne_destinataire`
- `ordre.profession_reglementee_pluriel`
- `ordre.adresse_affichee`
- `ordre.adresse.ligne_1`
- `ordre.adresse.cp`
- `ordre.adresse.ville`
- `ordre.adresse_bloc_affiche`
- `ordre.derogation_mention_manuelle`
- `ordre.derogation_suffixe`

Règles :
- `ordre.conseil_departemental_libelle` vaut `Conseil départemental de l’Ordre` dans les sources lues ;
- `ordre.destinataire_appel` vaut `Monsieur le Président` dans les sources lues, mais reste variable ;
- `ordre.adresse_bloc_affiche` est soit fourni directement, soit construit depuis l'adresse complète ou les champs séparés selon l'overlay.

### 8.5 Mandataire

- `mandataire.civilite_affichage`
- `mandataire.prenom`
- `mandataire.nom`
- `mandataire.fonction`
- `mandataire.cabinet`
- `mandataire.libelle_affiche`

Règles :
- `mandataire.libelle_affiche` peut être fourni directement ;
- sinon il est assemblé depuis les champs détaillés ;
- une configuration externe peut préremplir `Monsieur Jordan ELBAZ, gérant du cabinet SYDEL` ;
- aucune valeur SYDEL ne doit être une constante magique dans le générateur.

### 8.6 Signature

- `signature.lieu`
- `signature.date`

## 9. Mapping texte source vers canonique

| Source | Variable canonique texte | Familles |
|---|---|---|
| `Dr` | `signataire.titre_affichage` | toutes |
| `[prenom]` | `signataire.prenom` | toutes |
| `[nom]` | `signataire.nom` | toutes |
| `[adresse_personnelle]` | `signataire.adresse_personnelle_affichee` | toutes |
| `[profession]` | `ordre.profession_signataire_affichee` | SPFPL |
| `[profession_reglementee]` en expéditeur | `ordre.profession_signataire_affichee` | SELARL / SELAS |
| `[profession_reglementee]` après `Des` ou `Ordre des` | `ordre.profession_reglementee_pluriel` | SPFPL |
| `[profession_reglementee_pluriel]` | `ordre.profession_reglementee_pluriel` | SELARL / SELAS |
| `[adresse_ordre]` | `ordre.adresse_affichee` ou `ordre.adresse_bloc_affiche` | SPFPL |
| `[adresse_conseil_ordre]` | `ordre.adresse.ligne_1` | SELARL / SELAS |
| `[cp_ordre]` | `ordre.adresse.cp` | SELARL / SELAS |
| `[ville_ordre]` | `ordre.adresse.ville` | SELARL / SELAS |
| `[lieu_signature]` | `signature.lieu` | toutes |
| `[date_signature]` | `signature.date` | toutes |
| `[denomination_societe]` | `societe.denomination` | toutes |
| `[civilite_mandataire]` | `mandataire.civilite_affichage` | SELARL / SELAS |
| `[prenom_mandataire]` | `mandataire.prenom` | SELARL / SELAS |
| `[nom_mandataire]` | `mandataire.nom` | SELARL / SELAS |
| `[fonction_mandataire]` | `mandataire.fonction` | SELARL / SELAS |
| `[denomination_cabinet_mandataire]` | `mandataire.cabinet` | SELARL / SELAS |
| `Monsieur Jordan ELBAZ, gérant du cabinet SYDEL` | valeurs de configuration `mandataire.*` ou `mandataire.libelle_affiche` | SPFPL |
| `Dérogation ?` | `ordre.derogation_mention_manuelle` sous condition, jamais littéral automatique | SPFPL source |

## 10. Éléments manuels

Doivent être fournis par le contexte dossier, une configuration de référence ou une saisie humaine :
- profession affichée du signataire ;
- profession réglementée affichée après `Des` et `Ordre des` ;
- adresse du Conseil départemental de l'Ordre ;
- appel ordinal si différent de `Monsieur le Président` ;
- mandataire si la configuration SYDEL par défaut n'est pas disponible ;
- mention manuelle de dérogation lorsque `dossier.options.derogation == true` ;
- lieu et date de signature.

Doivent rester hors automatisation V1 :
- rédaction juridique d'une dérogation non fournie ;
- féminisation ou variation de l'appel ordinal ;
- adaptation du paragraphe `une seule structure` à un exercice multi-structures ;
- wording SCM spécifique non sourcé.

## 11. Règles de blocage avant génération

Le futur générateur doit bloquer si :
- `dossier.structure` n'est pas dans le périmètre V1 ;
- une variable obligatoire du tronc commun est absente ;
- les variables ordinales ne permettent pas de rendre `profession_signataire_affichee`, `profession_reglementee_pluriel` et `adresse_bloc_affiche` ;
- aucun mandataire complet ne peut être résolu ;
- `dossier.options.derogation == true` sans `ordre.derogation_mention_manuelle` ;
- `dossier.structure == SCM` sans données ordinales explicites.

Le futur générateur ne doit pas bloquer uniquement parce que :
- la famille est SCM, dès lors que les variables communes sont fournies ;
- le mandataire est SYDEL, dès lors qu'il vient d'une configuration ou d'un contexte et non d'une constante en dur.

## 12. Critères avant implémentation

Le ticket de code peut démarrer si :
- le générateur reste limité à cette famille documentaire ;
- aucun code ne lit les DOCX source comme template d'exécution ;
- la sélection de l'overlay dépend explicitement de `dossier.structure` ;
- les tests couvrent SELARL, SELAS, SPFPL cession, SPFPL apport et SCM ;
- les tests couvrent l'absence de dérogation, la dérogation manuelle fournie et le blocage si elle est requise mais absente ;
- les tests couvrent un mandataire fourni par champs détaillés et un mandataire fourni par configuration ;
- les tests vérifient l'absence du littéral résiduel `Dérogation ?` ;
- les tests vérifient qu'aucun placeholder source `[` / `]` ne reste dans le DOCX généré ;
- aucune formulation juridique source n'est modifiée hors variables et blocs explicités dans cette spec.

## 13. Points ouverts restants

Points ouverts non bloquants pour `CODE-ORDRE-001`, car ils sont couverts par variables ou règles de blocage :

1. SCM : aucune source SCM dédiée n'a été retrouvée ; une revue humaine du premier DOCX SCM généré restera nécessaire.
2. Dérogation : aucune phrase juridique n'est validée ; la V1 bloque ou rend uniquement une mention manuelle fournie.
3. Valeurs ordinales : les professions et adresses ordinales relèvent d'un référentiel ou d'une saisie, pas d'un wording codé en dur.
4. Mandataire SYDEL : la valeur par défaut peut être configurée, mais elle n'est pas une vérité absolue imposée à toute la famille.
5. Appel `Monsieur le Président` et titre `Dr` : conservés comme valeurs sources variables ; aucune variation automatique n'est introduite.

## 14. Statut de la spec texte

`SPEC-TEXTE-ORDRE-001` est complète pour ouvrir le ticket suivant :

- `CODE-ORDRE-001 | Implémenter le générateur canonique Demande d'inscription à l'ordre`

Le ticket de code devra rester limité à cette famille documentaire et ne devra modifier aucun autre document métier.
