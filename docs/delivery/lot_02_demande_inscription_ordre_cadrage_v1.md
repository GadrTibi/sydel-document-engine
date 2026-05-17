# Cadrage métier — Lot 2 — Demande d'inscription à l'ordre V1

## Position dans le projet

Ticket : `ANALYSE-ORDRE-001`.

Ce document est un cadrage d'analyse. Il ne vaut pas spec canonique codable et ne déclenche aucun développement Python.

Objectif : préparer le ticket suivant `SPEC-ORDRE-001`, en isolant le texte fixe, les variables, les accords, les blocs mutualisables et les ambiguïtés de la source.

## Sources lues

Le ticket mentionne le fichier source suivant :

- `project/source_documents/lot_02/Demande d'inscription à l'ordre.docx`

Ce chemin n'existe pas littéralement dans le dépôt au moment de l'analyse. La source Lot 2 correspondante réellement présente et lue en lecture seule est :

- `project/source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx`

Référentiels projet lus avant analyse :

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`

ADR applicables :

- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0003-lot-based-delivery.md`
- `docs/adr/0005-codex-working-mode.md`

## État du pipeline documentaire

| Étape | Statut | Note |
|---|---|---|
| Inventorié | Oui | Présent dans l'arbre document-centré V1 après `PV nomination gérant` pour les branches ordinales. |
| Validé | À confirmer | Le cadrage ne vaut pas validation métier finale. |
| Source reçue | Oui | Source DOCX transformée présente dans `project/source_documents/lot_02/`. |
| Analysé | Oui | Présent cadrage. |
| Spécifié | Non | À formaliser dans `SPEC-ORDRE-001`. |
| Codé | Non | Aucun code à ce stade. |
| Testé | Non | Non applicable avant spec/code. |
| Validé | Non | Validation humaine à obtenir après spec et rendu. |

## Analyse visible du document

### Structure observée

Le document source est une lettre courte adressée au Conseil départemental de l'Ordre.

Structure :

1. bloc expéditeur ;
2. bloc destinataire ordinal ;
3. lieu/date ;
4. objet ;
5. formule d'appel ;
6. corps de lettre en trois paragraphes ;
7. formule de politesse ;
8. signature.

### Texte fixe

Blocs fixes observés, hors placeholders :

- préfixe d'expéditeur : `Dr`
- destinataire : `Conseil départemental de l’Ordre`
- objet : `Demande d’inscription au tableau de l’Ordre`
- formule d'appel : `Monsieur le Président,`
- annonce du dossier de constitution de la société ;
- sollicitation d'inscription de la société au tableau de l'Ordre ;
- pouvoir donné à `Monsieur Jordan ELBAZ, gérant du cabinet SYDEL` pour effectuer les formalités ;
- formule de politesse : `Je vous prie d’agréer, Monsieur le Président, l’expression de mes sentiments dévoués.`
- signature finale avec préfixe `Dr`.

Le wording source contient aussi la séquence suivante dans le corps de lettre :

- `Je précise que je ne serai associé et praticien et exerçant que dans une seule structure. Dérogation ?`

Cette séquence doit être traitée comme point ouvert avant spec, car elle semble mélanger formulation juridique et note/question métier.

### Variables / zones variables

| Placeholder source | Rôle canonique candidat | Type | Note de cadrage |
|---|---|---|---|
| `[prenom]` | `signataire.prenom` | existant | Utilisé dans l'expéditeur et la signature. |
| `[nom]` | `signataire.nom` | existant | Utilisé dans l'expéditeur et la signature. |
| `[profession]` | à créer / confirmer | nouveau | Profession affichée sous le nom ; ne pas confondre avec `fonction_dirigeant`. |
| `[adresse_personnelle]` | `signataire.adresse_personnelle.affichee` ou dérivé de `signataire.adresse_personnelle.*` | à arbitrer | La source attend une adresse complète affichée, pas des champs séparés. |
| `[profession_reglementee]` | à créer / confirmer, possiblement `ordre.profession_reglementee` | nouveau | Utilisé dans `Ordre des ...`; probablement forme plurielle. |
| `[adresse_ordre]` | à créer / confirmer, possiblement `ordre.adresse_affichee` | nouveau | Adresse complète du Conseil départemental de l'Ordre. |
| `[lieu_signature]` | `signature.lieu` | existant | Lieu de signature. |
| `[date_signature]` | `signature.date` | existant | Date de signature. |
| `[denomination_societe]` | `societe.denomination` | existant | Société dont l'inscription à l'Ordre est demandée. |

### Accords de genre / nombre

Accords ou variantes à arbitrer avant spec :

- `Dr` est fixe dans la source ; confirmer si ce titre vaut pour toutes les professions concernées.
- `Monsieur le Président` est fixe ; confirmer s'il faut gérer `Madame la Présidente`.
- `associé`, `praticien`, `exerçant` sont au masculin singulier dans la source ; confirmer la règle si la signataire est une femme.
- `[profession_reglementee]` est utilisé après `des`, donc la valeur attendue semble plurielle ou collective.
- La phrase `je ne serai associé et praticien et exerçant que dans une seule structure` demande une validation grammaticale et métier avant toute automatisation.

### Blocs potentiellement mutualisables

Blocs candidats à mutualisation future :

- bloc identité professionnelle du signataire : `Dr`, prénom, nom, profession, adresse personnelle ;
- bloc destinataire ordinal : Conseil départemental, profession réglementée, adresse ordinale ;
- bloc signature simple : lieu, date, identité du signataire ;
- bloc pouvoir SYDEL : mention fixe de Jordan ELBAZ / cabinet SYDEL ;
- blocs de formule d'appel et formule de politesse, si d'autres lettres ordinales utilisent le même destinataire.

Mutualisation recommandée : modérée. Le document est suffisamment spécifique pour conserver un générateur dédié, mais il pourra réutiliser des helpers de rendu et un pack de variables ordinales.

### Anomalies / ambiguïtés source

Points à trancher dans `SPEC-ORDRE-001` avant tout code :

1. Le fichier demandé dans le ticket n'existe pas littéralement ; le fichier lu est la version transformée présente dans le dépôt.
2. La phrase `Dérogation ?` semble être une note ou question résiduelle dans le corps de la source.
3. Le wording `associé et praticien et exerçant` paraît grammaticalement instable ; ne pas le corriger sans validation métier.
4. La source ne décrit pas la variante avec dérogation, site distinct ou exercice dans plusieurs structures.
5. Le titre `Dr` est fixe et non variable.
6. Le destinataire `Monsieur le Président` est fixe.
7. `[profession]` et `[profession_reglementee]` sont deux zones distinctes ; leur relation doit être spécifiée.
8. `[adresse_personnelle]` et `[adresse_ordre]` sont des zones affichées complètes ; le mapping depuis les champs d'adresse structurés doit être décidé.

## Suffisance du cadrage

Le cadrage est suffisant pour créer le ticket `SPEC-ORDRE-001`.

Il n'est pas suffisant pour coder le document, car les points suivants restent ouverts :

- traitement ou suppression validée de `Dérogation ?` ;
- accords de genre autour de `associé`, `praticien`, `exerçant` ;
- règle de titre `Dr` ;
- règle de destinataire ordinal ;
- mapping canonique exact des données ordinales.

## Prochain livrable attendu

`SPEC-ORDRE-001 | Formaliser la spec canonique Demande d'inscription à l'ordre`

La spec devra produire au minimum :

- structure canonique du document ;
- texte fixe validé ;
- table de mapping source -> variables canoniques ;
- règles de genre/nombre ;
- règles de blocage en cas de dérogation non arbitrée ;
- critères de recette avant code.
