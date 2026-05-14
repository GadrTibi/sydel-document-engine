# DAAT x SYDEL - SPEC CANONIQUE V1
## Batch `regime communautaire`

## 1. Objet

Formaliser le batch documentaire `regime communautaire` avant tout codage.

Cette spec canonique couvre deux documents distincts :
- `Lettre d'avertissement au conjoint en cas d'apport d'un bien commun` ;
- `Lettre de renonciation a revendiquer la qualite d'associe`.

Elle ne code rien et ne modifie aucun wording juridique source. Elle prepare un ticket de code unique pour produire les deux lettres dans le meme batch, avec un pack de variables commun.

## 2. Sources lues

Memoire projet et referentiels :
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
- `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour le futur ticket code ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources Lot 2 presentes et lues :
- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_documents/lot_02/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`

Note de chemin :
- les noms demandes sans suffixe n'existent pas litteralement dans `project/source_documents/lot_02/` ;
- les deux fichiers ci-dessus sont les sources placees disponibles pour le batch.

Variantes raw dump lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Regime communaute/Lettre de renonciation a revendiquer la qualite d_associe.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Regime communaute/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/Regime communaute/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/Regime communaute/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/Regime communaute/Lettre de renonciation a revendiquer la qualite d_associe.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/Regime communaute/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/regime communaute/Copie de Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/regime communaute/Copie de Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession + apport/regime communaute/Copie de Copie de Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession + apport/regime communaute/Copie de Copie de Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`

## 3. Perimetre documentaire V1

La source de verite rattache le bloc `Si regime communautaire` aux structures suivantes :
- SELARL ;
- SELAS ;
- SPFPL cession ;
- SPFPL apport.

Structures hors perimetre V1 de ce batch :
- SAS ;
- SCS ;
- SCI / SCI IRIS ;
- SCM.

Condition d'activation :
- `dossier.options.regime_communautaire == true`.

Decision V1 :
- le batch produit les deux lettres ensemble pour les structures couvertes ;
- les documents restent deux documents canoniques distincts, avec deux generateurs dedies possibles ;
- la mutualisation porte sur les roles, les variables, les validations et quelques helpers de rendu, pas sur un generateur unique.

Identifiants de travail pour le futur code :
- `RC-AVERTISSEMENT` : lettre d'avertissement au conjoint ;
- `RC-RENONCIATION` : lettre de renonciation du conjoint.

Les identifiants catalogue definitifs devront etre attribues dans `CODE-RC-001` sans renommer les documents metier.

## 4. Role de chaque lettre dans le batch

### 4.1 Lettre d'avertissement au conjoint

Role metier :
- informer le conjoint de l'apport projete d'un bien commun ou d'une somme dependant de la communaute ;
- rappeler l'article 1832-2 alinea 1er du Code civil ;
- poser la base du courrier auquel la lettre de renonciation repond ;
- imprimer l'instruction de mention manuscrite a faire preceder par le conjoint.

Auteur :
- `apporteur`, futur associe ou futur dirigeant.

Destinataire :
- `conjoint`.

Document source majoritaire :
- groupe exact `source_documents` / SELAS / SPFPL, hash prefix `e5ab70fea0303ae8`.

### 4.2 Lettre de renonciation

Role metier :
- formaliser la renonciation du conjoint a revendiquer personnellement la qualite d'associe ou qualite equivalente ;
- confirmer son consentement a l'apport effectue par son conjoint ;
- s'appuyer sur la date du courrier d'avertissement.

Auteur :
- `conjoint`, qui signe la renonciation.

Destinataire :
- `apporteur`.

Document source majoritaire :
- groupe exact `source_documents` / SELAS / SPFPL, hash prefix `cd1cd16e4d224bd9`.

## 5. Comparaison des variantes

### 5.1 Groupes exacts observes

| Document | Groupe exact | Constat |
|---|---|---|
| Avertissement | source Lot 2 + SELAS + SPFPL cession + SPFPL apport + SPFPL cession/apport | Copies exactes, hash prefix `e5ab70fea0303ae8`. |
| Renonciation | source Lot 2 + SELAS + SPFPL cession + SPFPL apport + SPFPL cession/apport | Copies exactes, hash prefix `cd1cd16e4d224bd9`. |

### 5.2 Variantes SELARL distinctes

Les deux variantes SELARL ne sont pas des copies exactes du groupe source Lot 2 / SELAS / SPFPL.

Differences de renonciation :
- `[date_du_jour]` remplace `[date_courrier]` ;
- `notre communaute` est fixe et remplace `[regime_matrimonial]` ;
- `associe` est fixe et remplace `[qualite_associe]` ;
- `En 2exemplaires` est fixe et remplace `[nombre_exemplaires_lettres] exemplaires` ;
- la phrase d'apport ne contient pas le point final observe dans le groupe source Lot 2 / SELAS / SPFPL.

Differences d'avertissement :
- le corps principal est identique ;
- le bloc de mention manuscrite final differe :
  - SELARL : `a la Societe [denomination_societe]` ;
  - SELAS / SPFPL : `a la [forme_sociale_abregee] [denomination_societe]` ;
- la variante SELARL ne contient pas `[forme_sociale_abregee]`.

Decision V1 de canonisation :
- la renonciation suit le groupe source Lot 2 / SELAS / SPFPL, plus parameterisable et deja place dans `source_documents` ;
- la variante SELARL de renonciation est documentee comme variante source non retenue comme overlay automatique en V1 ;
- l'avertissement conserve un overlay de mention manuscrite SELARL, car la difference est structurelle et limitee.

## 6. Variables canoniques attendues

### 6.1 Dossier

- `dossier.structure`
- `dossier.options.regime_communautaire`

Valeurs acceptees en V1 pour `dossier.structure` :
- `SELARL`
- `SELAS`
- `SPFPL_CESSION`
- `SPFPL_APPORT`

### 6.2 Societe

- `societe.denomination`
- `societe.forme_sociale`
- `societe.forme_sociale_complete`
- `societe.forme_sociale_abregee`
- `societe.capital_social`
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`

Regles :
- `societe.forme_sociale` rend la forme affichee dans l'en-tete et le corps de l'avertissement ;
- `societe.forme_sociale_complete` rend la forme longue dans la renonciation ;
- `societe.forme_sociale_abregee` est obligatoire pour la mention manuscrite SELAS / SPFPL, mais pas pour l'overlay SELARL.

### 6.3 Apporteur

- `apporteur.civilite_affichage`
- `apporteur.genre`
- `apporteur.prenom`
- `apporteur.nom`
- `apporteur.fonction_dirigeant`

Regles :
- l'apporteur est auteur de la lettre d'avertissement ;
- l'apporteur est destinataire de la lettre de renonciation ;
- `apporteur.genre` est conserve pour un futur arbitrage, mais ne pilote aucune feminisation automatique en V1.

### 6.4 Conjoint

- `conjoint.civilite_affichage`
- `conjoint.genre`
- `conjoint.prenom`
- `conjoint.nom`
- `conjoint.adresse.num_voie`
- `conjoint.adresse.voie`
- `conjoint.adresse.cp`
- `conjoint.adresse.ville`

Regles :
- `conjoint.nom` est obligatoire dans les deux lettres ;
- `conjoint.prenom` est obligatoire pour la signature de la renonciation ;
- le bloc destinataire de l'avertissement conserve la forme source `[civilite_conjoint] [nom_conjoint]`, sans ajout automatique du prenom.

### 6.5 Apport et regime matrimonial

- `apport.montant`
- `apport.montant_lettres`
- `regime_communautaire.regime_matrimonial`
- `regime_communautaire.qualite_renoncee`

Regles :
- `[apport_personne_1]` et `[montant_apport]` pointent vers `apport.montant` ;
- `[apport_lettres_personne_1]` et `[montant_apport_lettres]` pointent vers `apport.montant_lettres` ;
- `regime_communautaire.regime_matrimonial` rend la zone `[regime_matrimonial]` de la renonciation, typiquement `communaute` si aucune decision plus fine n'est fournie ;
- `regime_communautaire.qualite_renoncee` rend `[qualite_associe]` et doit etre fourni explicitement, par exemple `associe`, `associee` ou `actionnaire`.

### 6.6 Dates, signatures et exemplaires

- `regime_communautaire.avertissement.date_signature`
- `regime_communautaire.renonciation.lieu_signature`
- `regime_communautaire.renonciation.date_signature`
- `regime_communautaire.date_courrier_avertissement`
- `regime_communautaire.renonciation.nombre_exemplaires_lettres`

Regles :
- l'avertissement ne contient pas de `[lieu_signature]` source ;
- la renonciation contient un lieu et une date ;
- `regime_communautaire.date_courrier_avertissement` alimente la phrase `Par courrier en date du ...` ;
- si les deux lettres sont generees ensemble et que `date_courrier_avertissement` est absent, le futur generateur peut utiliser `regime_communautaire.avertissement.date_signature` ;
- si aucune de ces dates n'est disponible, la generation de la renonciation doit bloquer.

## 7. Mapping source vers canonique

| Source | Variable canonique |
|---|---|
| `[denomination_societe]` | `societe.denomination` |
| `[forme_sociale]` | `societe.forme_sociale` |
| `[forme_sociale_complete]` | `societe.forme_sociale_complete` |
| `[forme_sociale_abregee]` | `societe.forme_sociale_abregee` |
| `[capital_social]` | `societe.capital_social` |
| `[num_voie_siege]` | `societe.siege.num_voie` |
| `[voie_siege]` | `societe.siege.voie` |
| `[cp_siege]` | `societe.siege.cp` |
| `[ville_siege]` | `societe.siege.ville` |
| `[civilite]` | `apporteur.civilite_affichage` |
| `[prenom]` | `apporteur.prenom` |
| `[nom]` | `apporteur.nom` |
| `[fonction_dirigeant]` | `apporteur.fonction_dirigeant` |
| `[civilite_conjoint]` | `conjoint.civilite_affichage` |
| `[prenom_conjoint]` | `conjoint.prenom` |
| `[nom_conjoint]` | `conjoint.nom` |
| `[num_voie_conjoint]` | `conjoint.adresse.num_voie` |
| `[voie_conjoint]` | `conjoint.adresse.voie` |
| `[cp_conjoint]` | `conjoint.adresse.cp` |
| `[ville_conjoint]` | `conjoint.adresse.ville` |
| `[date_signature]` dans l'avertissement | `regime_communautaire.avertissement.date_signature` |
| `[lieu_signature]` dans la renonciation | `regime_communautaire.renonciation.lieu_signature` |
| `[date_signature]` dans la renonciation | `regime_communautaire.renonciation.date_signature` |
| `[date_courrier]` | `regime_communautaire.date_courrier_avertissement` |
| `[date_du_jour]` SELARL legacy | `regime_communautaire.date_courrier_avertissement` |
| `[montant_apport]` | `apport.montant` |
| `[montant_apport_lettres]` | `apport.montant_lettres` |
| `[apport_personne_1]` | `apport.montant` |
| `[apport_lettres_personne_1]` | `apport.montant_lettres` |
| `[regime_matrimonial]` | `regime_communautaire.regime_matrimonial` |
| `[qualite_associe]` | `regime_communautaire.qualite_renoncee` |
| `[nombre_exemplaires_lettres]` | `regime_communautaire.renonciation.nombre_exemplaires_lettres` |

## 8. Blocs conditionnels et variantes

### 8.1 Condition batch

Si `dossier.options.regime_communautaire != true`, aucun des deux documents du batch n'est selectionne.

Si `dossier.structure` est hors perimetre V1, le batch ne doit pas etre selectionne meme si l'option est vraie.

### 8.2 Overlay de mention manuscrite de l'avertissement

Condition :
- `dossier.structure == SELARL` : utiliser l'overlay SELARL ;
- `dossier.structure in {SELAS, SPFPL_CESSION, SPFPL_APPORT}` : utiliser l'overlay source Lot 2 / SELAS / SPFPL.

Effet :
- SELARL ne requiert pas `societe.forme_sociale_abregee` pour la mention manuscrite ;
- SELAS / SPFPL requierent `societe.forme_sociale_abregee`.

### 8.3 Renonciation SELARL legacy

Constat :
- la variante SELARL brute remplace plusieurs variables par des valeurs fixes et contient `En 2exemplaires`.

Decision V1 :
- ne pas creer d'overlay SELARL automatique pour cette renonciation ;
- utiliser le texte canonique du groupe place dans `source_documents` avec des valeurs explicites ;
- signaler la difference en revue humaine SELARL.

### 8.4 Mention manuscrite

La mention manuscrite de l'avertissement est une instruction imprimee.

Decision V1 :
- le generateur rend l'instruction source ;
- il ne simule pas une mention manuscrite ;
- il ne remplit pas une signature manuscrite.

## 9. Regles de blocage avant generation

Le futur generateur doit bloquer si :
- `dossier.structure` est hors perimetre V1 ;
- `dossier.options.regime_communautaire` n'est pas vrai ;
- une variable obligatoire du tronc commun manque ;
- le montant d'apport en chiffres ou en lettres manque ;
- la date de courrier d'avertissement ne peut pas etre resolue pour la renonciation ;
- `regime_communautaire.qualite_renoncee` est absent ;
- la structure SELAS / SPFPL requiert `societe.forme_sociale_abregee` et que cette valeur manque ;
- la renonciation ne peut pas rendre `lieu_signature`, `date_signature` ou `nombre_exemplaires_lettres`.

## 10. Criteres avant implementation

`CODE-RC-001` peut demarrer si :
- le code reste limite a ce batch et ne modifie aucun autre document metier ;
- aucun DOCX source n'est utilise comme template d'execution ;
- les tests couvrent SELARL, SELAS, SPFPL cession et SPFPL apport ;
- les tests couvrent les deux documents produits ensemble lorsque `regime_communautaire == true` ;
- les tests couvrent l'absence du batch lorsque l'option est fausse ;
- les tests couvrent l'overlay de mention manuscrite SELARL et l'overlay SELAS / SPFPL ;
- les tests verifient l'absence de placeholders source `[` / `]` dans les deux DOCX generes ;
- les tests verifient que les dates de courrier sont coherentes entre avertissement et renonciation ;
- aucun wording juridique n'est modifie hors variables et overlays documentes.

## 11. Points ouverts restants

Points ouverts non bloquants pour ouvrir `CODE-RC-001`, car ils sont soit variables, soit bloques par validation :

1. La variante SELARL de renonciation brute contient `En 2exemplaires`; la V1 retient le groupe source Lot 2 / SELAS / SPFPL, a relire humainement sur un premier rendu SELARL.
2. La feminisation de `futur [fonction_dirigeant]` n'est pas activee automatiquement ; si necessaire, elle devra passer par une valeur d'affichage fournie ou une decision metier.
3. `mon conjoint` reste le wording source dans la renonciation ; aucune variante `ma conjointe` n'est introduite sans source.
4. Le batch V1 couvre un apport d'une somme en numeraire ; aucune variante pour apport en nature ou bien autre qu'une somme n'est sourcee.
5. Les valeurs de forme sociale complete, affichee et abregee doivent etre fournies par contexte ou referentiel.

## 12. Statut de la spec canonique

`SPEC-RC-001` est complet cote canonique pour le batch regime communautaire V1, sous reserve de la spec texte jointe :

- `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`

Le prochain ticket recommande est :

- `CODE-RC-001 | Implémenter le batch régime communautaire v1`
