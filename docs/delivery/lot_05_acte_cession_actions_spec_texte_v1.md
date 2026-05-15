# DAAT x SYDEL - SPEC TEXTE V1
## Acte de cession d'actions SPFPL

Ticket : `SPEC-ACTE-ACTIONS-001`

## 1. Objet

Stabiliser la structure texte et les regles de fidelite de l'acte de cession d'actions SPFPL, sans coder.

Cette spec texte complete :
- `docs/delivery/lot_05_acte_cession_actions_spec_canonique_v1.md`

Source analysee :
- `project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx`

Cette spec ne corrige pas le wording juridique source. Les squelettes ci-dessous servent a positionner les variables et les blocs ; le futur code devra reprendre le texte juridique source sans correction silencieuse.

## 2. Sources lues

Memoire projet :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`

Specs et audit :
- `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_05_acte_cession_actions_spec_canonique_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Extraction source :
- 115 paragraphes non vides extraits du DOCX ;
- placeholders source inventories dans la spec canonique associee ;
- aucune modification du DOCX source.

## 3. Nature texte retenue

Le texte source est un acte contractuel complet de cession d'actions.

Le document doit etre rendu comme :
- `Cession d'actions` ;
- acte entre le cedant et la SPFPL cessionnaire ;
- cession de la pleine propriete d'actions de la societe cible ;
- prix global et prix unitaire par action ;
- transfert de propriete et jouissance a compter de la date de realisation ;
- garantie d'actif et de passif ;
- clauses finales, enregistrement, ordre professionnel et signature electronique.

Le document ne doit pas etre rendu comme :
- cession de parts ;
- apport de titres ;
- PV d'agrement ;
- acte de cession de cabinet.

## 4. Structure texte source

Structure visible :

1. Bandeau et titre `Cession d'actions`.
2. Identification courte des parties : cedant / societe cessionnaire.
3. Comparution detaillee du cedant.
4. Comparution detaillee de la SPFPL cessionnaire.
5. Expose de l'operation et de la societe cible.
6. Repartition du capital actuel.
7. Origine de propriete.
8. Bloc `OBJET DU CONTRAT : CESSION D'ACTIONS`.
9. Nantissement, pacte d'associes et agrement.
10. Propriete et jouissance.
11. Prix et modalites de paiement.
12. Declarations des parties.
13. Garantie d'actif et de passif / GAP.
14. Clauses generales : unicite, renonciation, negociation, autonomie.
15. Signification de la cession.
16. Declaration pour l'enregistrement.
17. Pouvoirs.
18. Communication au Conseil de l'Ordre.
19. Frais.
20. Affirmation de sincerite.
21. Loi applicable et attribution de juridiction.
22. Convention sur la preuve et signature electronique.
23. Lieu, date, nombre d'exemplaires, signatures.
24. Cadre reserve a l'administration.

## 5. Texte canonique V1

### 5.1 Titre et parties

Squelette de tete :

```text
Cession d'actions

ENTRE
{cedant.civilite_affichage} {cedant.prenom} {cedant.nom}

ET
La Societe {societe_spfpl.denomination}
```

Regle de fidelite :
- le titre doit rester `Cession d'actions` ;
- aucune substitution par `Cession de parts` n'est autorisee.

### 5.2 Comparution du cedant

Squelette variable :

```text
{cedant.civilite_affichage} {cedant.prenom} {cedant.nom}, {cedant.profession}, ne le {cedant.date_naissance} a {cedant.ville_naissance} ({cedant.departement_naissance}), de nationalite {cedant.nationalite}, demeurant {cedant.adresse_personnelle.adresse_affichee}, {cedant.situation_maritale} sous le regime de {cedant.regime_matrimonial} avec {cedant.conjoint.civilite_affichage} {cedant.conjoint.prenom} {cedant.conjoint.nom}, inscrit au tableau de l'Ordre des {cedant.profession_reglementee_pluriel} du {cedant.ordre.departemental}, et sous le numero RPPS {cedant.ordre.numero_rpps}.

Ci-apres denomme "LE CEDANT",
```

Point de blocage :
- les accords `ne`, `inscrit`, `denomme` sont masculins dans la source. La variante feminine doit etre arbitree avant code ou bloquer.

### 5.3 Comparution de la SPFPL cessionnaire

Squelette variable :

```text
La Societe {societe_spfpl.denomination}
{societe_spfpl.forme_sociale} inscrite au tableau de l'Ordre des {societe_cible.profession_reglementee_pluriel} du {societe_spfpl.departement_inscription_ordre}.
Au capital de {societe_spfpl.capital_social}
Immatriculee au RCS de {societe_spfpl.ville_rcs} sous le numero {societe_spfpl.numero_rcs}
Siege social : {societe_spfpl.siege.adresse_affichee}
Representee aux presentes par {societe_spfpl.representant.civilite_affichage} {societe_spfpl.representant.prenom} {societe_spfpl.representant.nom} en sa qualite de {societe_spfpl.representant.fonction} et ayant tout pouvoir a l'effet des presentes.

Ci-apres denommee "LE CESSIONNAIRE",
```

Point de blocage :
- la source utilise a cet endroit les variables du cedant pour representer la cessionnaire, puis des variables dediees en signature. Le futur contexte doit confirmer le role a utiliser.

### 5.4 Expose de la societe cible

Squelette variable :

```text
Ont procede de la maniere suivante a la cession des actions de la Societe {societe_cible.denomination}.

La Societe {societe_cible.denomination} est une {societe_cible.forme_sociale_complete}, au capital social de {societe_cible.capital_social} divise en {societe_cible.nb_actions_total} actions d'{societe_cible.valeur_nominale_action_lettres} de valeur nominale, entierement liberees dont le siege est situe au {societe_cible.siege.adresse_affichee}.

La Societe {societe_cible.denomination} est immatriculee au Registre du Commerce et des Societes de {societe_cible.ville_rcs} sous le numero {societe_cible.numero_rcs} et inscrite au tableau de l'Ordre Departemental des {societe_cible.profession_reglementee_pluriel} du {societe_cible.departement_inscription_ordre}.

Son objet social est l'exercice de la profession de {societe_cible.profession_reglementee}.
```

Regle de fidelite :
- le capital est exprime en actions ;
- le placeholder source nomme `[valeur_nominale_part_lettres]` doit etre mappe vers une valeur nominale d'action.

### 5.5 Dirigeants et repartition du capital

La source contient :
- une phrase de presentation des dirigeants ;
- une table `Associes / Actions` ;
- une ligne `Total / [nb_actions]`.

Squelette cible :

```text
{societe_cible.presentation_dirigeants}

Le capital social est reparti a ce jour comme suit :

Associes
Actions
{societe_cible.repartition_capital_avant_operation}
Total
{societe_cible.nb_actions_total}
```

Regles :
- `societe_cible.presentation_dirigeants` doit etre produit depuis un role structure ou fourni comme bloc valide ;
- `societe_cible.repartition_capital_avant_operation` doit etre produit depuis `associes_cible[]` ;
- la table source a trois lignes ne doit pas figer le moteur.

### 5.6 Origine de propriete

Squelette source-structure :

```text
Aux termes des statuts le capital social de la SOCIETE est actuellement detenu comme suit :
{associes_cible.origine_propriete_lignes}
{cedant.civilite_affichage} {cedant.prenom} {cedant.nom}, le CEDANT, declare qu'il est proprietaire des actions pour les avoir souscrites lors de la constitution de la SOCIETE.
```

Point de blocage :
- la source ne decrit pas une origine de propriete dynamique pour tous les cas ; si l'origine differe de la souscription a la constitution, un wording valide est necessaire.

### 5.7 Objet du contrat

Bloc central a conserver comme acte d'actions :

```text
OBJET DU CONTRAT : CESSION D'ACTIONS

Par les presentes, le Cedant cede ce jour, sous les garanties ordinaires de fait et de droit en la matiere, ainsi que celles consenties dans les presentes, a l'Acquereur, qui accepte, la pleine propriete de {cession_actions.nb_actions_lettres} ({cession_actions.nb_actions}) actions qu'il detient, (ci-apres, les "Actions Cedees" ou les "Titres Cedes"), ensemble avec tous les droits, titres et interets qui y sont attaches.
```

Regles :
- `Actions Cedees` et `Titres Cedes` doivent rester coherents avec une cession d'actions ;
- ne pas reprendre le vocabulaire `parts sociales` dans ce document.

### 5.8 Nantissement, pacte d'associes et agrement

Le bloc source affirme notamment :
- les actions ne sont pas nanties ni donnees en garantie ;
- la cession au profit d'un tiers necessite l'agrement des associes ;
- les associes se sont reunis le meme jour et ont agree la cession a l'unanimite.

Decision texte V1 :
- bloc juridique a reprendre strictement si le contexte confirme ces faits ;
- bloquer si l'agrement n'est pas confirme ou si le dossier ne contient pas le PV coherent.

### 5.9 Propriete et jouissance

Le bloc source pose :
- propriete et jouissance a compter de ce jour ;
- date qualifiee de `Date de Realisation` ;
- subrogation dans les droits et obligations ;
- repartition prorata temporis des dividendes de l'exercice en cours.

Decision texte V1 :
- reprendre ce bloc tel que source ;
- toute autre date d'effet ou regle de dividendes exige un wording valide.

### 5.10 Prix et modalites de paiement

Squelette variable :

```text
La cession a lieu moyennant le prix global de {cession_actions.prix_total_lettres} ({cession_actions.prix_total}) euros, soit un prix de {cession_actions.prix_unitaire_action} EUR ({cession_actions.prix_unitaire_action_lettres}) par Action, a payer par la Societe {societe_spfpl.denomination}.
```

Le bloc modalites de paiement source indique :
- paiement au moyen d'un credit bancaire ;
- paiement comptant ce jour ;
- paiement par cheque de banque ;
- quittance par le cedant.

Decision texte V1 :
- ne pas rendre ce bloc si ces modalites ne sont pas confirmees ;
- ne pas inventer une variante virement, credit-vendeur ou paiement echelonne.

### 5.11 Declarations des parties

Bloc source a reprendre comme bloc juridique, avec une attention particuliere a la phrase fixe :

```text
Remplir les conditions exigees par la loi pour detenir des actions de SELAS de chirurgien-dentiste ;
```

Decision texte V1 :
- cette phrase limite la source a un cas SELAS chirurgien-dentiste sauf arbitrage ;
- pour toute autre profession ou forme sociale, blocage ou wording valide requis.

### 5.12 Garantie d'actif et de passif

La source contient une GAP complete :
- garantie contre diminution ou insuffisance d'actif, augmentation ou revelation de passif ;
- fait generateur ;
- absence d'exoneration du cedant en cas de connaissance prealable par le cessionnaire ;
- plafond au prix de cession des actions cedees ;
- durees de reclamation en matiere fiscale/sociale et duree de trois ans ;
- assurance contre les risques mentionnes.

Decision texte V1 :
- traiter la GAP comme bloc source non parametre ;
- toute suppression, duree differente, plafond different ou limitation differente doit etre une decision juridique explicite.

### 5.13 Clauses generales

Blocs source a reprendre strictement, sauf arbitrage juridique :
- `UNICITE DU CONTRAT`
- `RENONCIATION`
- `NEGOCIATION ET EXECUTION DU CONTRAT`
- `AUTONOMIE DES STIPULATIONS DE LA CONVENTION`

Point de vigilance :
- le bloc `NEGOCIATION ET EXECUTION DU CONTRAT` contient une formulation source `demande ou part judiciaire`. Aucune correction silencieuse ne doit etre faite dans la future implementation.

### 5.14 Formalites et ordre

Blocs source :
- `SIGNIFICATION DE LA CESSION`
- `DECLARATION POUR L'ENREGISTREMENT`
- `POUVOIRS`
- `COMMUNICATION DU PRESENT CONTRAT AU CONSEIL DE L'ORDRE`
- `FRAIS`
- `AFFIRMATION DE SINCERITE`
- `LOI APPLICABLE - ATTRIBUTION DE JURIDICTION`

Decisions texte V1 :
- conserver le rattachement aux actions cedees ;
- ne pas modifier la reference a l'article 1690 du Code civil sans validation juridique ;
- conserver la phrase de frais source uniquement avec revue humaine, car elle vise `cession d'action` au singulier.

### 5.15 Signature electronique

Bloc source :
- faculte de proceder a la signature electronique ;
- renonciation a l'acte original papier ;
- preuve valable ;
- signature via Yousign.

Variables :
- `signature.mode`
- `signature.service`

Decision texte V1 :
- `signature.mode = electronique` et `signature.service = Yousign` sont les valeurs source ;
- tout autre service ou mode de signature doit etre arbitre.

### 5.16 Signatures

Squelette final :

```text
Fait a {signature.lieu}
Le {signature.date}
En {cession_actions.nombre_exemplaires_lettres} exemplaires originaux,

Dr {cedant.prenom} {cedant.nom}
La societe {societe_spfpl.denomination}
Representee par {societe_spfpl.representant.civilite_courte} {societe_spfpl.representant.prenom} {societe_spfpl.representant.nom}

Cadre reserve a l'administration
```

Point de blocage :
- le titre `Dr` devant le cedant est fixe dans la source. Il doit etre confirme ou derive d'une variable valide avant code.

## 6. Variables texte

### 6.1 Roles principaux

- `cedant.*`
- `societe_spfpl.*`
- `societe_spfpl.representant.*`
- `societe_cible.*`
- `societe_cible.dirigeants[]`
- `associes_cible[]`
- `cession_actions.*`
- `signature.*`

### 6.2 Variables composees a produire ou fournir

- `societe_cible.presentation_dirigeants`
- `societe_cible.repartition_capital_avant_operation`
- `associes_cible.origine_propriete_lignes`
- `cession_actions.nombre_exemplaires_lettres`

Decision V1 :
- les variables composees doivent etre produites depuis donnees structurees, ou fournies comme blocs valides ;
- si elles sont fournies comme blocs libres, ce choix doit etre documente avant code.

## 7. Overlays textuels

### 7.1 Overlay actions

Le document a un vocabulaire central d'actions :
- `Cession d'actions`
- `cession des actions`
- `actions`
- `Actions Cedees`
- `Titres Cedes`
- `par Action`

Blocage :
- si le rendu cible est une cession de parts, ce document ne doit pas etre utilise.

### 7.2 Overlay SELAS chirurgien-dentiste

La source contient une phrase fixe sur les actions de SELAS de chirurgien-dentiste.

Blocage :
- si la societe cible n'est pas une SELAS de chirurgien-dentiste et qu'aucun wording valide n'est fourni.

### 7.3 Overlay paiement

La source fixe une modalite de paiement bancaire avec cheque de banque.

Blocage :
- si `cession_actions.modalites_paiement` differe de cette modalite et qu'aucun texte valide n'existe.

### 7.4 Overlay GAP

La source integre une GAP detaillee.

Blocage :
- si la GAP est absente ou differente sans arbitrage juridique.

### 7.5 Overlay genre

La source est masculine pour le cedant.

Blocage :
- si `cedant.genre != masculin` et qu'aucune variante validee n'est disponible.

### 7.6 Overlay signature

La source impose une signature electronique via Yousign.

Blocage :
- si le dossier prevoit un autre mode de signature sans texte valide.

## 8. Elements manuels

Elements a traiter manuellement ou a valider avant code :

- revue humaine du DOCX converti ;
- verification de l'agrement unanime des associes ;
- coherence avec le PV d'agrement du meme dossier ;
- verification de la repartition du capital et de l'origine de propriete ;
- confirmation de la modalite de paiement ;
- validation de la GAP ;
- validation de la phrase `SELAS de chirurgien-dentiste` ;
- confirmation du role de representant cessionnaire ;
- confirmation du titre `Dr` en signature ;
- decision sur le `Cadre reserve a l'administration`.

## 9. Regles de blocage avant generation

Un futur generateur doit bloquer si :

- le dossier ne vise pas une cession SPFPL d'actions ;
- le document demande est l'acte de cession de parts ;
- un placeholder source resterait dans le rendu ;
- une variable composee de capital ou d'origine de propriete ne peut pas etre construite ;
- la forme sociale ou la profession ne correspond pas au wording source ;
- le representant cessionnaire n'est pas determine ;
- l'agrement des associes n'est pas confirme ;
- la modalite de paiement n'est pas celle de la source ;
- la GAP n'est pas applicable telle quelle ;
- le genre du cedant exige des accords non sources ;
- le service de signature n'est pas Yousign sans arbitrage.

## 10. Criteres texte avant implementation

Avant tout code, verifier que le ticket de code :

- cible explicitement `SPFPL-ACTE-CESSION-ACTIONS` ;
- confirme les points ouverts ou les transforme en blocages explicites ;
- prevoit une generation from-scratch, sans utiliser le DOCX source comme template d'execution ;
- teste le titre `Cession d'actions` ;
- teste le bloc `OBJET DU CONTRAT : CESSION D'ACTIONS` ;
- teste l'absence de `Cession de parts` et de `parts sociales` dans les zones de titres cedes ;
- teste l'absence de placeholders `[` et `]` ;
- teste la coherence des actions et du prix lorsque les formats numeriques le permettent ;
- preserve le wording juridique source sans correction silencieuse.

## 11. Points ouverts

1. **Validation source** : le DOCX provient d'une conversion d'ancien `.doc`; revue humaine conseillee avant code.
2. **Perimetre SELAS chirurgien-dentiste** : confirmer si la V1 est limitee a ce cas.
3. **Representant cessionnaire** : confirmer cedant ou role distinct.
4. **Genre du cedant** : aucune variante feminine sourcee.
5. **Paiement** : confirmer credit bancaire, comptant, cheque de banque.
6. **GAP** : confirmer que la GAP source est toujours attendue.
7. **Agrement** : confirmer la dependance avec le PV d'agrement et l'unanimite.
8. **Capital dynamique** : confirmer le rendu des actionnaires lorsque la structure differe des trois lignes source.
9. **Signature** : confirmer `Dr` et Yousign.
10. **Cadre administration** : confirmer conservation, suppression ou traitement manuel.

## 12. Statut de la spec texte

`SPEC-ACTE-ACTIONS-001` stabilise la structure texte V1 de l'acte de cession d'actions SPFPL, sans code Python.

La prochaine etape recommandee est une revue metier des points ouverts avant tout ticket de code.
