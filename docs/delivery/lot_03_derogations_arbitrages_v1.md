# DAAT x SYDEL - ARBITRAGES V1
## Famille `derogations`

## 1. Objet

Ce fichier cloture le ticket `ARBITRAGE-DEROG-001` avant tout code.

Il tranche le perimetre V1 de la famille documentaire `derogations` :
- documents qui restent manuels ;
- documents ou blocs pre-remplissables ;
- sort du fichier legacy `.doc` salariee / activite externe ;
- frontiere exacte entre automatisation partielle, formulaire a completer et blocage.

Ce fichier ne modifie aucun wording juridique source, ne deplace aucune source et
ne modifie aucun fichier Python.

## 2. Sources relues

Memoire projet et workflow :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`

Specs Lot 03 :
- `docs/delivery/lot_03_derogations_spec_canonique_v1.md`
- `docs/delivery/lot_03_derogations_spec_texte_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Constat source :
- `project/source_documents/lot_03/` ne contient que `README.md` ;
- les sources Lot 03 relues par les specs restent dans
  `project/source_import/raw_drive_dump/`.

## 3. Points tranches

### 3.1 Familles canoniques conservees

Les sous-familles V1 restent distinctes :
- `site_distinct_manual`
- `multi_sites_sel`
- `cumul_sel_bnc`
- `cumul_salariee`
- `sel_bnc_manual`

Decision :
- ne pas fusionner le formulaire CD94 site distinct avec le formulaire
  multi-sites SEL ;
- ne pas fusionner `Derogation SEL BNC complet.docx` avec
  `Demande de derogation cumul SELARL - BNC.docx` ;
- ne pas renommer `cumul_salariee` en `cumul_activite_externe` cote moteur V1,
  car la source de verite rattache le document comme demande de derogation cumul
  SELARL salarie.

Le libelle fonctionnel peut mentionner `salariee / activite externe`, mais la cle
canonique V1 reste `cumul_salariee`.

### 3.2 Frontiere exacte d'automatisation V1

La V1 autorise uniquement un pre-remplissage deterministe de champs source
identifies par placeholder ou zone structuree.

Deux modes de rendu sont admis :
- document finalise : toutes les zones juridiquement obligatoires doivent etre
  fournies par le contexte dossier ; sinon la generation bloque ;
- formulaire pre-rempli a completer : les zones manuelles restent visibles et
  le document doit etre explicitement classe comme formulaire a completer, sans
  etre presente comme piece finalisee.

Decision :
- aucune zone narrative sensible n'est generee par defaut ;
- aucune case n'est cochee par inference ;
- aucune explication juridique n'est inventee ;
- aucun wording source n'est corrige, feminise ou enrichi sans ticket explicite.

### 3.3 Documents pre-remplissables

Sont candidats a un futur generateur partiel, apres placement de sources propres
dans `project/source_documents/lot_03/` :
- `multi_sites_sel` pour SELARL et SELAS ;
- `cumul_sel_bnc` ;
- `cumul_salariee`, uniquement apres conversion validee du `.doc` legacy en DOCX
  propre.

Pre-remplissage autorise :
- donnees societe / SEL ;
- inscription ordinale societe ;
- declarant ou signataire ;
- representant legal si le role est fourni explicitement ;
- associe exercant si le role est fourni explicitement ;
- adresse de siege ;
- adresse du site declare lorsqu'une variable source existe et que la donnee est
  fournie ;
- date de debut d'activite lorsqu'elle est fournie ;
- date et lieu de signature lorsqu'ils existent dans la source.

### 3.4 Roles `signataire`, `representant_legal`, `associe_exercant`

Decision :
- ne pas supposer que ces trois roles designent toujours la meme personne ;
- `personne_1` ne peut etre pre-remplie que si le contexte dossier fournit un
  mapping explicite vers le role attendu ;
- si le contexte indique que le representant legal, l'associe exercant et le
  signataire sont la meme personne, le pre-remplissage est autorise ;
- sinon, un document finalise doit bloquer et un formulaire a completer doit
  laisser les zones de role explicitement a completer.

### 3.5 Cases a cocher et motifs

Decision :
- les cases sont rendues uniquement depuis une donnee explicite ;
- toute case cochee doit avoir son explication fournie dans le contexte ;
- en absence d'explication, un document finalise bloque ;
- un formulaire a completer peut conserver les cases et explications vierges,
  avec statut explicite de formulaire incomplet.

### 3.6 Sort du `.doc` legacy salariee / activite externe

Le fichier `Demande_derogation_cumul_SELARL_salariee.doc` reste une source legacy
de lecture et d'arbitrage, mais ne peut pas servir de modele executable.

Decision :
- ne pas coder depuis le `.doc` binaire ;
- convertir ou remplacer la source par un DOCX propre avant tout ticket de code ;
- valider apres conversion que les placeholders et le wording source n'ont pas
  derive ;
- conserver la sous-famille canonique `cumul_salariee` en V1 ;
- documenter dans les futurs tickets que le contenu couvre aussi l'activite
  externe.

### 3.7 Sources Lot 03

Decision :
- les sources dans `raw_drive_dump` suffisent pour l'arbitrage et la spec ;
- elles ne suffisent pas comme base executable de code ;
- avant tout generateur Lot 03, les sources retenues doivent etre placees ou
  arbitrees explicitement dans `project/source_documents/lot_03/` ;
- ce ticket ne deplace aucune source.

### 3.8 Wording juridique

Decision :
- conserver les formulations source, y compris les anomalies deja identifiees ;
- ne pas corriger `Monsieur`, `soussigne(e)`, espaces manquants, accents ou
  formulations juridiques sans ticket explicite ;
- ne pas ajouter de feminisation automatique dans la famille `derogations`.

## 4. Manuel V1

Restent hors automatisation initiale :
- `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx` ;
- `Derogation SEL BNC complet.docx` ;
- toute piece marquee `A REMPLIR A LA MAIN` dans la source de verite ;
- signature manuscrite ;
- pieces jointes ;
- planning d'activites ;
- temps hebdomadaires si non fournis ;
- autres sites d'exercice si aucune liste structuree n'est fournie ;
- activite envisagee ;
- moyens en personnel ;
- materiels ;
- continuite des soins ;
- environnement professionnel ;
- reponse aux urgences ;
- criteres fondant la demande ;
- explication associee a chaque case cochee.

Ces elements peuvent etre listes comme pieces ou zones attendues dans un futur
ZIP dossier, mais ne doivent pas etre generes comme texte juridique par defaut.

## 5. Points bloquants restants

Bloquants pour tout code Lot 03 :
- aucune source executable n'est encore placee dans
  `project/source_documents/lot_03/` ;
- le mode de rendu doit etre porte dans le registre ou le nom de sortie :
  `document finalise` ou `formulaire a completer` ;
- les tests devront verifier qu'un document finalise bloque en cas de champ
  narratif obligatoire absent.

Bloquants specifiques :
- `cumul_salariee` bloque tant que le `.doc` legacy n'est pas converti ou
  remplace par un DOCX propre valide ;
- `multi_sites_sel` bloque pour rendu finalise si le mapping des roles
  `representant_legal` / `associe_exercant` / `signataire` n'est pas fourni ;
- `cumul_sel_bnc` bloque pour rendu finalise si les motifs, cases cochees,
  temps, lieux d'exercice et explications obligatoires ne sont pas fournis.

Aucun autre arbitrage metier n'est laisse ouvert pour cadrer la V1
pre-remplissable de `multi_sites_sel` et `cumul_sel_bnc`.

## 6. Statut de cloture

`ARBITRAGE-DEROG-001` est clos cote arbitrage documentaire V1.

Prochaine etape recommandee :
- placer les sources retenues dans `project/source_documents/lot_03/`, puis
  ouvrir un ticket de code limite a une seule sous-famille, de preference
  `cumul_sel_bnc` ou `multi_sites_sel`.
