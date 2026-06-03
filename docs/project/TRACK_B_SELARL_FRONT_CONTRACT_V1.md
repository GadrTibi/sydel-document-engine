# Track B - Contrat metier-front SELARL V1

Ticket : `TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001`

Statut : contrat documentaire V1, sans implementation SELARL nouvelle.

Addendum 2026-06-01 : les passages historiques qui qualifiaient `DOC-006`
comme reserve source sont remplaces par la decision courante. Pour une SELARL
avec regime communautaire, le front doit generer `DOC-005` et `DOC-006`. La
source DOCX de `DOC-006` existe dans `project/source_documents/lot_02/` et le
batch regime communautaire des specs Lot 2 couvre les deux lettres.

## 1. Objet

Ce document fige le contrat entre le metier SELARL et le futur front Track B propre.
Il sert a brancher plus tard une vertical slice SELARL sans reprendre le vieux front
comme source de verite, et sans inventer de logique metier.

Ce contrat ne modifie pas le moteur documentaire, ne modifie pas le wording juridique
et ne code aucune generation SELARL.

## 2. Contexte prouve

Commandes executees depuis Track B :

```text
pwd
C:\Users\Gad\Desktop\Sydel\sydel-track-b

git rev-parse --show-toplevel
C:/Users/Gad/Desktop/Sydel/sydel-track-b

git branch --show-current
track-b/clean-rebuild
```

`git status --short --branch` a confirme la branche attendue avec un working tree
deja modifie par le ticket precedent de reset front. Ces changements preexistants
n'ont pas ete revertes.

## 3. Hierarchie appliquee

La hierarchie du ticket est appliquee pour ce contrat :

1. arbitrages humains explicites ;
2. mails / reponses metier ;
3. NotebookLM ;
4. documents source V2 / V3 ;
5. templates DOCX / registre moteur ;
6. code existant.

Note de reconciliation : `docs/project/SELARL_SOURCE_HIERARCHY_V2.md` donne une
hierarchie projet proche mais pas identique dans sa formulation. Le present ticket
est plus recent et plus precis ; il prime pour ce contrat. Les conclusions utiles
restent compatibles : les arbitrages humains et la reponse Albane priment sur
NotebookLM, et le code existant ne devient jamais source metier primaire.

## 4. Sources reellement lues

Sources de verite et arbitrages :

- `project/source_truth/albane_reponse_mail_selarl_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V2.docx`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`
- `docs/project/SELARL_FORM_SCHEMA_V1.md`
- `docs/project/SELARL_PROCESS_SPEC_V1.md`

Lots documentaires lus :

- `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`

Revues pertinentes consultees :

- `docs/review/selarl_source_verify_001_report_v1.md`
- `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`
- `docs/review/selarl_form_schema_impl_001_report_v1.md`
- `docs/review/selarl_flow_realign_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/review/track_b_front_architecture_reset_001_report_v1.md`

Verification de coherence uniquement, non source metier primaire :

- `src/sydel_doc_engine/domain/case_catalog.py`
- `src/sydel_doc_engine/front_data/test_prefill_presets.py`
- `src/sydel_doc_engine/front_app/legacy_boundary.py`
- `src/sydel_doc_engine/front_app/data_entry.py`
- `src/sydel_doc_engine/front_app/generation.py`

NotebookLM a ete utilise seulement pour consolider vocabulaire, ordre de saisie
et risques UX lorsque les sources superieures ne suffisaient pas. Il n'a pas ete
utilise pour contredire les arbitrages humains.

## 5. Promesse produit visible

Le front Track B SELARL V1 doit promettre uniquement ceci :

> Preparer une creation de SELARL simple, en partant de la Fiche Client /
> Praticien, en affichant clairement les documents generables, les documents
> manuels et les cas non couverts, puis en lancant la generation seulement quand
> les donnees requises sont presentes.

Le front ne doit pas promettre :

- une automatisation complete de tous les cas SELARL V2 / V3 ;
- la generation des dossiers cession cabinet, cession SCM, derogation ou site
  distinct ;
- la prise en charge automatique des statuts multi-associes ;
- un mode Projet, un filigrane ou une nouvelle couche produit lourde de statut
  documentaire ;
- une fusion entre SELARL et SELAS avec micro-holding.

## 6. Perimetre exact SELARL V1

Le perimetre SELARL V1 retenu est volontairement etroit.

Inclus :

- creation d'une SELARL ;
- profession `medecin` ou `chirurgien_dentiste` ;
- dossier unipersonnel explicite ;
- Praticien = associe unique = gerant = signataire seulement si l'option
  `Dossier unipersonnel` est active ;
- domiciliation = siege social, conformement a la reponse metier Albane ;
- generation des documents coeur listés en section 7 ;
- affichage honnete des exclusions, manuels et hors scope.

Exclus du coeur V1 :

- SELAS medecin avec personne morale / micro-holding ;
- SELARL avec associes multiples pour les statuts ;
- site distinct automatise ;
- derogation automatisee ;
- cession SCM automatisee depuis le front V1 ;
- cession de cabinet medical ou dentaire automatisee depuis le front V1 ;
- bail et appel de fonds dans le premier parcours visible ;
- dirigeant distinct de l'associe pour les statuts ;
- correction de wording juridique ou feminisation automatique non validee.

## 7. Documents inclus en generation SELARL V1

| Code | Document | Condition front V1 | Statut front V1 |
|---|---|---|---|
| `DOC-001` | Declaration sur l'honneur de non-condamnation | Toujours dans le dossier SELARL V1 | Generable si Fiche Client + signature completes |
| `DOC-002` | Autorisation de domiciliation | Toujours dans le dossier SELARL V1 | Generable si societe, siege et signataire complets ; domiciliation = siege |
| `DOC-003` | Procuration | Toujours dans le dossier SELARL V1 | Generable si signataire, societe, siege et mandataire resolu |
| `DOC-004` | PV nomination gerant | Toujours dans le dossier SELARL V1 | Generable en dossier unipersonnel avec associe/gerant/signataire resolus |
| `DOC-034` | Demande d'inscription a l'ordre | Toujours dans le dossier SELARL V1 | Generable si ordre, mandataire, societe et signataire complets |
| `DOC-016` | Statuts SELARL chirurgien-dentiste | Si profession = `chirurgien_dentiste` | Generable seulement associe unique |
| `DOC-017` | Statuts SELARL medecin | Si profession = `medecin` | Generable seulement associe unique |
| `DOC-005` | Lettre de renonciation a revendiquer la qualite d'associe | Si regime communautaire = oui | Generable si conjoint, apport, societe et signature complets |
| `DOC-006` | Lettre d'avertissement au conjoint | Si regime communautaire = oui | Generable si conjoint, apport, societe et signature complets ; adresse conjoint derivee depuis l'adresse personnelle de l'associe/signataire, sans champ front separe |

La generation V1 doit filtrer strictement sur ces documents. Les documents
techniquement presents dans le moteur mais hors contrat ne doivent pas etre
declenches par le front V1.

## 8. Documents manuels, exclus ou reportes

| Code | Document | Condition source | Decision front V1 | Message attendu |
|---|---|---|---|---|
| sans code | Formulaire declaration prealable site distinct CD94 avec la SEL | Site distinct | Manuel | Document attendu par la source, mais a remplir manuellement en V1. |
| `DOC-013` | Formulaire derogation plusieurs sites avec la SEL | Derogation | Manuel / hors generation | Document mentionne, variables non fournies ; preparation manuelle. |
| sans code | Derogation SEL BNC | Derogation | Manuel | Document indique comme a remplir a la main. |
| `DOC-014` | Derogation cumul SELARL BNC | Derogation | Manuel / hors generation | Document indique comme a remplir a la main. |
| `DOC-031` | PV AGE cession part SCM | SCM cession | Hors front V1 | Cas complexe non couvert par le premier parcours SELARL V1. |
| `DOC-032` | Courrier SDE cession SCM | SCM cession | Hors front V1 | Cas complexe non couvert par le premier parcours SELARL V1. |
| `DOC-033` | Acte de cession des parts de la SCM vers SELARL | SCM cession | Hors front V1 | Cas complexe non couvert par le premier parcours SELARL V1. |
| `DOC-007` | Avenant contrat de bail | Cession | Hors front V1 | Cession/bail non couverts par la saisie V1. |
| `DOC-008` | Appel de fonds SEL | Cession | Hors front V1 | Cession/financement non couverts par la saisie V1. |
| `DOC-009` | Acte de cession cabinet medical | Cession cabinet medical | Hors front V1 | Cession cabinet non couverte par la saisie V1. |
| `DOC-010` | Compromis cession cabinet medical | Cession cabinet medical | Hors front V1 | Cession cabinet non couverte par la saisie V1. |
| `DOC-011` | Acte de cession cabinet dentaire | Cession cabinet dentaire | Hors front V1 | Cession cabinet non couverte par la saisie V1. |
| `DOC-012` | Compromis cession cabinet dentaire | Cession cabinet dentaire | Hors front V1 | Cession cabinet non couverte par la saisie V1. |
| `DOC-018` | Statuts SELAS medecin | SELAS | Exclu SELARL V1 | Cas SELAS, distinct de la SELARL V1. |

## 9. Conditions de presence par document

### Documents coeur

- `DOC-001` : present pour tout dossier SELARL V1.
- `DOC-002` : present pour tout dossier SELARL V1 ; l'adresse de domiciliation
  est le siege social.
- `DOC-003` : present pour tout dossier SELARL V1 ; mandataire obligatoire,
  configurable, non deduit du signataire.
- `DOC-004` : present pour tout dossier SELARL V1 ; associe unique et gerant
  resolus via `Dossier unipersonnel`.
- `DOC-034` : present pour tout dossier SELARL V1 ; donnees ordinales et
  mandataire requis.

### Statuts

- `DOC-016` : present uniquement si profession = chirurgien-dentiste.
- `DOC-017` : present uniquement si profession = medecin.
- Si `associes.count >= 2`, les statuts sont bloques en V1 car le wording
  pluriel n'est pas stabilise.

### Regime communautaire

- `DOC-005` : present si regime communautaire = oui.
- `DOC-006` : present si regime communautaire = oui.

### Branches non couvertes V1

- site distinct = oui : afficher les documents attendus, bloquer la generation
  automatique des documents manuels.
- derogation = oui : afficher les documents attendus, bloquer la generation
  automatique des documents manuels.
- SCM cession = oui : afficher la branche comme hors front V1 ; ne pas lancer
  `DOC-031` a `DOC-033`.
- cession = oui : afficher la branche comme hors front V1 ; ne pas lancer
  `DOC-007` a `DOC-012`.

## 10. Donnees a saisir par etape d'interface

### Etape 1 - Qualification

- type de dossier : SELARL ;
- profession : medecin ou chirurgien-dentiste ;
- dossier unipersonnel : oui obligatoire pour la generation V1 ;
- regime communautaire : oui / non ;
- site distinct : oui / non, mais branche manuelle si oui ;
- derogation : oui / non, mais branche manuelle si oui ;
- SCM cession : non dans le parcours generable V1 ;
- cession cabinet / bail / financement : non dans le parcours generable V1.

### Etape 2 - Fiche Client / Praticien

- civilite d'affichage ;
- genre grammatical, sans feminisation automatique non validee ;
- prenom, nom ;
- date, ville et departement de naissance ;
- nationalite ;
- filiation pour `DOC-001` : nom du pere, nom de la mere ;
- profession ;
- adresse personnelle complete et/ou composants ;
- numero RPPS ;
- numero d'ordre si applicable ;
- ordre departemental ou ville d'ordre selon profession.

### Etape 3 - Fiche Societe

- denomination sociale ;
- forme sociale et forme sociale complete ;
- capital social en chiffres et en lettres ;
- siege social ;
- ville RCS si le document la consomme ;
- duree de societe si l'overlay statuts la consomme ;
- adresse de domiciliation derivee du siege social, sans champ separe ;
- lieu d'exercice, avec reutilisation du siege seulement par option explicite.

### Etape 4 - Capital et associes

- associe unique, relie au Praticien par `Dossier unipersonnel` ;
- nombre total de parts ;
- valeur nominale de la part ;
- apport en numeraire et montant en lettres ;
- banque de depot : nom et adresse si requis ;
- gerant : derive du Praticien seulement en dossier unipersonnel ;
- signataire : derive du Praticien seulement en dossier unipersonnel ;
- seuil achat materiel et seuil emprunt gerance pour statuts medecin ;
- nombre d'exemplaires en lettres si requis.

### Etape 5 - Ordre et mandataire

- profession reglementee affichee ;
- profession reglementee plurielle ;
- conseil departemental de l'ordre ;
- adresse du conseil de l'ordre, code postal et ville ;
- mandataire : civilite, prenom, nom, fonction, cabinet, ou configuration
  explicite ;
- aucune valeur mandataire magique dans le generateur.

### Etape 6 - Scenarios et generation

- conjoint, apport et date du courrier si regime communautaire = oui ;
- adresse du conjoint derivee depuis l'adresse personnelle de l'associe/signataire,
  jamais demandee comme champ front separe ;
- lieu de signature ;
- date de signature ;
- liste des documents generables ;
- liste des documents manuels ou reserves ;
- raisons de blocage par document.

## 11. Wording honnete a afficher

Messages standards a utiliser cote front :

| Cas | Message |
|---|---|
| Document manuel | `Ce document est attendu par la source, mais il reste a preparer manuellement en SELARL V1.` |
| Regime communautaire | `Regime communautaire actif : les lettres DOC-005 et DOC-006 seront generees.` |
| Cession / SCM / bail hors V1 | `Le moteur peut contenir une famille documentaire liee, mais le front SELARL V1 ne couvre pas encore les donnees metier necessaires. Generation bloquee pour ce document.` |
| Statuts multi-associes | `Les sources actuelles ne stabilisent pas le wording des statuts avec plusieurs associes. Generation automatique bloquee en V1.` |
| SELAS / micro-holding | `Ce cas releve d'une SELAS distincte, pas de la SELARL V1.` |
| Donnee manquante | `Generation impossible : donnees requises manquantes pour ce document.` |
| Option non couverte | `Option conservee dans le dossier, mais hors generation automatique SELARL V1.` |

## 12. Regles d'erreur, blocage et avertissement

Blocages :

- dossier hors SELARL ;
- profession autre que medecin ou chirurgien-dentiste ;
- dossier unipersonnel inactif pour les statuts ;
- plus d'un associe pour la generation des statuts V1 ;
- mandataire absent pour `DOC-003` ou `DOC-034` ;
- ordre professionnel incomplet pour `DOC-034` et statuts ;
- signature.lieu ou signature.date absent ;
- capital ou repartition des parts incoherent ;
- option cession, SCM, derogation ou site distinct demandee avec lancement
  automatique du document associe ;
- `cabinet_type` renseigne alors que cession = non ;
- second lieu d'exercice partiel si une future option le presente.

Avertissements :

- `DOC-005` et `DOC-006` sont generes quand le regime communautaire est actif ;
- des adresses peuvent etre identiques en pratique, mais ne doivent pas etre
  copiees silencieusement hors regle documentee ;
- siege social et lieu d'exercice peuvent coincider via option explicite ;
- bailleur, locataire, vendeur, cedant, acquereur et cessionnaire restent des
  roles distincts ;
- mandataire peut etre preconfigure mais reste un role de formalite separe.

## 13. Table source retenue

| Sujet | Sources en presence | Source retenue | Decision |
|---|---|---|---|
| SELAS avec personne morale / micro-holding | Albane mail, modele SELAS, NotebookLM | Albane mail | Ce n'est pas une SELARL V1 ; exclu. |
| Nom de l'ecran personne | Arbitrage humain, NotebookLM, schema | Arbitrage humain + NotebookLM | Utiliser `Fiche Client` et le terme pivot `Praticien`. |
| Ordre du parcours | NotebookLM, schema SELARL, reviews | NotebookLM consolide par schema | Qualification, Fiche Client, Fiche Societe, Capital/Associes, scenarios, generation. |
| Dossier unipersonnel | Arbitrage humain, schema, reviews | Arbitrage humain | Option explicite ; Praticien = associe unique = gerant = signataire seulement si active. |
| Domiciliation | Albane mail, V2/V3, registre | Albane mail | Domiciliation = siege social. |
| Siege vs lieu d'exercice | Albane mail, registre | Albane mail + registre | Peut coincider via option, pas de fusion silencieuse. |
| Liste documents coeur | V2/V3, process spec, catalogue | V2/V3 + process spec | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016` ou `DOC-017`. |
| Regime communautaire | Source verite, specs Lot 2, source DOCX, catalogue | Specs Lot 2 + source DOCX | `DOC-005` et `DOC-006` generables quand le regime communautaire est actif. |
| Site distinct | V2/V3, source verify | V2/V3 | Manuel, hors generation V1. |
| Derogation | V2/V3, source verify | V2/V3 | `DOC-013` et `DOC-014` manuels, hors generation V1. |
| Statuts multi-associes | Source verite 1 a 6, specs statuts, arbitrage statuts | Arbitrage statuts SEL | Generation V1 limitee a associe unique. |
| Cession SCM | Albane mail, V2/V3, registre, code | Albane mail + V2/V3 | Roles explicites ; hors premier front V1. |
| Cession cabinet | Albane mail, V2/V3, registre | Albane mail + V2/V3 | Vendeur = praticien BNC, acquereur = SEL en creation, mais hors premier front V1. |
| Mode Projet / filigrane | NotebookLM, arbitrage humain | Arbitrage humain | Non retenu en V1. |
| Couche statut documentaire lourde | NotebookLM, arbitrage humain, front_data | Arbitrage humain | Ne pas creer de nouveau systeme lourd ; utiliser blocages/avertissements existants. |

## 14. Contradictions detectees

1. `SELARL_SOURCE_HIERARCHY_V2.md` et le ticket ne formulent pas exactement la
   meme hierarchie. Resolution : appliquer le ticket pour ce contrat.
2. V2/V3 contiennent l'anomalie de libelle `Si medecin Statuts dentiste` tout
   en pointant le modele de statuts medecins. Resolution : profession medecin
   selectionne `DOC-017`.
3. Historique `DOC-006` : le contrat initial l'avait laisse en reserve par
   prudence. Resolution 2026-06-01 : reserve levee, car la source DOCX existe
   dans `project/source_documents/lot_02/` et le batch regime communautaire
   couvre les deux lettres.
4. V2/V3 listent des documents de derogation et site distinct, mais certains sont
   explicitement a remplir a la main ou sans variables fournies. Resolution :
   manuel / hors generation V1.
5. La source de verite signale une ambition 1 a 6 associes pour les statuts,
   tandis que les specs/arbitrages SEL limitent l'automatisation initiale a
   l'associe unique. Resolution : front V1 generable = unipersonnel.
6. NotebookLM propose des pistes de mode Projet, filigrane et statut documentaire
   plus riche. Resolution : non retenu par arbitrage humain.
7. Le vieux front et certains prefills montrent des generations partielles ou des
   scopes differents. Resolution : code existant utilise seulement comme controle
   de coherence, pas comme source du contrat.

## 15. Questions ouvertes necessitant arbitrage humain

Ces questions ne bloquent pas le GO de la vertical slice V1 bornee ci-dessus,
mais bloquent l'extension du perimetre :

- faut-il automatiser le site distinct CD94, et avec quelle source de variables ?
- faut-il automatiser les derogations SEL/BNC, et avec quel wording valide ?
- faut-il ouvrir les statuts SELARL a 2 a 6 associes, et quel wording exact
  retenir pour comparution, apports, capital et signatures ?
- faut-il integrer la cession SCM dans le front SELARL, et quel sous-formulaire
  metier retenir ?
- faut-il integrer la cession de cabinet, bail et appel de fonds dans le front
  SELARL, et quelle place donner aux roles bailleur/locataire ?
- faut-il rendre variable `Monsieur le President`, `Dr`, et les accords
  `associe/praticien/exercant` dans `DOC-034` ?
- faut-il autoriser un dirigeant non associe dans les statuts SELARL generes ?

## 16. Conclusion binaire

GO pour implementer la vraie vertical slice SELARL V1 si elle respecte strictement
ce contrat :

- creation SELARL ;
- medecin ou chirurgien-dentiste ;
- dossier unipersonnel ;
- documents coeur `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034` et
  `DOC-016` ou `DOC-017` ;
- `DOC-005` et `DOC-006` conditionnels regime communautaire ;
- documents manuels et complexes affiches mais non generes.

Ce GO ne vaut pas pour une SELARL complete couvrant cession, SCM, derogations,
site distinct ou statuts multi-associes.
