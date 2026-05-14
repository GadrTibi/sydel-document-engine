# DAAT x SYDEL - ARBITRAGES V1
## Famille `statuts civils` - ARBITRAGE-STATUTS-CIVILS-001

## 1. Objet

Fermer les points ouverts prioritaires avant tout codage des statuts civils.

Cette note complete :
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.

Elle ne code aucun generateur et ne modifie aucun wording juridique source.

## 2. Sources relues

Memoire projet :
- `AGENTS.md` ;
- `docs/project/00_MASTER_PLAN.md` ;
- `docs/project/01_EXECUTION_BOARD.md` ;
- `docs/project/02_CODEX_WORKFLOW.md` ;
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` ;
- `docs/project/04_LAST_STATE.md`.

Specs et preparation :
- `docs/delivery/lot_04_statuts_preparation_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.

ADR reperes :
- `docs/adr/0001-source-of-truth.md` ;
- `docs/adr/0002-engine-per-document.md` ;
- `docs/adr/0003-lot-based-delivery.md` ;
- `docs/adr/0005-codex-working-mode.md`.

Source de verite metier relue :
- `project/source_truth/Documents_a_generer_par_cas.docx`.

Sources DOCX civiles relues en lecture seule :
- `project/source_documents/lot_04/Statuts_SCS_modele.docx` ;
- `project/source_documents/lot_04/Modele statuts SCI.docx` ;
- `project/source_documents/lot_04/Modele statuts SCI IRIS.docx` ;
- `project/source_documents/lot_04/Statuts SCM.docx`.

Note : les noms physiques des fichiers SCI contiennent un accent decompose sur disque. Les chemins ci-dessus sont normalises pour la lisibilite.

La source de verite confirme notamment :
- les statuts SCS, SCI, SCI IRIS et SCM comme branches civiles distinctes ;
- la lettre option IS comme document separe des statuts SCI / SCI IRIS ;
- les documents satellites SCM comme documents distincts des statuts SCM ;
- la variabilite possible de 1 a 6 associes dans les statuts.

## 3. Synthese des arbitrages

| Point | Classement V1 | Decision |
|---|---|---|
| Associes dynamiques 1 a 6 | tranche | V1 retient une liste canonique `associes[]`, bornee de 1 a 6, avec rendu repetable par document. |
| Associes personnes morales | tranche | Les personnes morales sont des associes canoniques de type `personne_morale`, pas des champs libres ni des `personne_N` physiques. |
| Donnees sensibles des associes | manuel V1 | Les situations matrimoniales, adresses affichees, professions, qualites, RCS, representants et fonctions sont fournies explicitement. |
| Anomalie de repartition des parts SCM | tranche | L'anomalie source est traitee comme anomalie d'alias : le futur code doit utiliser des parts explicites par associe et verifier le total. |
| Anomalie de repartition des parts SCM en donnees legacy | bloquant | Un contexte qui ne fournit que `nb_parts_personne_2` pour les deux lignes SCM est insuffisant et doit bloquer. |
| Signatures dynamiques | tranche | Les signatures sont rendues depuis une liste de signataires, par defaut les associes du document, dans l'ordre source ou l'ordre fourni. |
| Frontieres exactes du perimetre V1 | tranche | La V1 couvre uniquement les quatre statuts civils SCS, SCI, SCI IRIS et SCM comme documents distincts. |
| Option IS SCI / SCI IRIS | manuel V1 | La lettre d'option IS reste hors generateur de statuts civils et doit faire l'objet d'une spec separee si elle est automatisee. |
| Documents satellites SCM | manuel V1 | Pacte d'associes, liste de depenses communes, contrat frais communs et reglement interieur restent hors automatisation V1. |

## 4. Associes dynamiques 1 a 6

### Classement

Tranche.

### Decision

La V1 des statuts civils supporte de 1 a 6 associes via `associes[]`.

Les placeholders sources `personne_1`, `personne_2`, `personne_3`, `societe_1`, `societe_2` restent des aliases documentaires observes. Ils ne deviennent pas la verite metier du moteur.

Le futur code devra rendre dynamiquement, selon le document :
- la comparution des associes ;
- les apports ;
- la repartition du capital ;
- les plages ou numeros de parts lorsque la source les exige ;
- les signatures.

### Regles par sous-famille

SCS :
- les roles `commandite` et `commanditaire` sont obligatoires ;
- un associe peut porter des lignes d'apport distinctes uniquement si le dossier le fournit explicitement ;
- le role ne doit jamais etre deduit du rang dans `associes[]`.

SCI :
- les associes physiques observes dans la source deviennent une repetition de `associes[]` ;
- la V1 peut accepter 1 a 6 associes si les apports, parts et signatures sont coherents.

SCI IRIS :
- les associes et les groupes de parts sont repetables ;
- la repartition du resultat exceptionnel reste pilotee par `resultat.groupes_parts[]`.

SCM :
- les associes personnes morales et personnes physiques sont repetables ;
- la qualite professionnelle et les donnees de representation sont obligatoires quand elles sont affichees par la source.

### Blocages associes

Le generateur devra bloquer si :
- aucun associe n'est fourni ;
- plus de 6 associes sont fournis ;
- un role obligatoire est absent pour SCS ;
- un associe requis par une ligne d'apport, de parts ou de signature n'a pas les donnees necessaires ;
- les totaux d'apports ou de parts ne correspondent pas au capital et au nombre total de parts.

## 5. Associes personnes morales

### Classement

Tranche, avec donnees d'identification en manuel V1.

### Decision

Les associes personnes morales sont admis dans le modele canonique V1.

Ils doivent etre representes comme des objets `associes[]` avec :
- `type_personne = personne_morale` ;
- `denomination` ;
- `forme_juridique` si la source l'affiche ;
- `capital_social` si la source l'affiche ;
- `siege.affiche` ou siege detaille ;
- `numero_rcs` et `ville_rcs` si la source les affiche ;
- `profession` ou qualite professionnelle pour SCM si la source l'affiche ;
- `representant.*` lorsque le texte fait intervenir un representant ;
- apports et parts propres.

### Application par document

SCS :
- la ligne `[denomination_societe_associe_1]` de repartition du capital est une personne morale associee si le dossier la fournit ;
- sa qualite d'associe et ses parts doivent etre explicites.

SCI :
- la source observee ne contient pas de personne morale en comparution ni en repartition ;
- une personne morale SCI reste hors source observee V1 et ne doit pas etre inventee sans spec complementaire.

SCI IRIS :
- `[denomination_societe_2]` est traite comme associe personne morale dans la repartition du capital ;
- faute de comparution complete dans la source, les donnees d'identification et de representation doivent etre explicites si un futur rendu les affiche.

SCM :
- `[denomination_societe_1]` est une personne morale professionnelle associee ;
- son representant, sa fonction, sa profession, son capital, son siege et son RCS sont des donnees obligatoires des que le document est finalise.

### Donnees manuelles V1

Restent fournis par le contexte dossier ou par un referentiel valide :
- denomination ;
- forme juridique ;
- profession ou qualite professionnelle ;
- capital social ;
- siege ;
- RCS ;
- representant ;
- fonction du representant ;
- qualite d'associe ;
- apports et parts.

Le moteur ne doit pas completer ces donnees par inference.

## 6. Anomalie de repartition des parts SCM

### Classement

Tranche pour la strategie de modele.

Bloquant pour tout contexte legacy ambigu.

### Constat source

Dans `Statuts SCM.docx`, la repartition du capital contient deux lignes distinctes :
- personne morale : `[denomination_societe_1][nb_parts_personne_2] parts` ;
- personne physique : `[civilite_personne_2] [prenom_personne_2] [nom_personne_2][nb_parts_personne_2] parts`.

Le meme placeholder `[nb_parts_personne_2]` est donc utilise pour deux associes differents.

La source contient aussi une ligne d'apport personne physique avec une valeur fixe `510 euros` alors que la ligne precedente porte `[apport_lettres_personne_2]`.

### Decision

Le futur code ne doit pas conserver `nb_parts_personne_2` comme source unique de verite pour SCM.

La V1 doit utiliser une repartition explicite par associe :
- `associes_personnes_morales[0].parts.nb` ou `associes[].parts.nb` pour la personne morale ;
- `associes_personnes_physiques[0].parts.nb` ou `associes[].parts.nb` pour la personne physique ;
- `societe.nb_parts_total` pour le total.

La generation SCM est autorisable seulement si les parts de chaque associe sont fournies separement et si leur somme correspond au total.

### Blocages SCM

Le generateur SCM devra bloquer si :
- le contexte ne fournit qu'une seule valeur heritee `nb_parts_personne_2` pour les deux lignes ;
- les apports distincts personne morale / personne physique ne sont pas fournis ;
- la ligne fixe `510 euros` n'est pas remplacee par une valeur explicitement validee dans le modele de donnees ou documentee comme wording source a conserver ;
- la somme des parts par associe ne correspond pas a `[nb_parts]`.

## 7. Signatures dynamiques

### Classement

Tranche.

### Decision

Les signatures des statuts civils sont dynamiques en V1.

Par defaut, la liste des signataires est derivee des associes du document, dans l'ordre de comparution ou dans l'ordre fourni par `signataires[]` si le contexte le precise.

Le rendu doit rester propre a chaque source :
- SCS : une ligne par signataire avec la mention source a faire preceder de `Lu et approuve` ;
- SCI : une ligne par associe signataire, sans mention `Lu et approuve` observee dans la source ;
- SCI IRIS : une ligne par associe signataire, sans mention `Lu et approuve` observee dans la source ;
- SCM : une signature pour la personne morale representee et une signature pour la personne physique, avec la mention source `Lu et approuve` separee proprement par signataire.

### Personnes morales signataires

Quand un associe personne morale signe, le rendu doit afficher :
- la denomination de la personne morale ;
- le representant si la source ou le contexte l'exige ;
- la fonction du representant si la source l'affiche.

Le moteur ne doit pas remplacer une signature de personne morale par la seule personne physique representante sans trace de la personne morale.

### Blocages signatures

Le generateur devra bloquer si :
- un associe requis comme signataire n'a pas de libelle de signature calculable ;
- une personne morale signataire n'a pas de representant alors que le document l'affiche ;
- le nombre de signatures attendues ne correspond pas aux associes ou signataires fournis ;
- un contexte demande une signature d'un tiers non associe sans spec complementaire.

## 8. Frontieres exactes du perimetre V1

### Classement

Tranche.

### Inclus V1

La V1 des statuts civils couvre uniquement les documents canoniques suivants :
- `LOT04-STATUTS-SCS` ;
- `LOT04-STATUTS-SCI` ;
- `LOT04-STATUTS-SCI-IRIS` ;
- `LOT04-STATUTS-SCM`.

Ces quatre documents restent des sorties distinctes.

### Exclu V1

Sont hors perimetre de ce ticket et du futur code statuts civils V1 :
- statuts SEL ;
- statuts SPFPL ;
- statuts SAS ;
- option IS sous forme de lettre separee ;
- pacte d'associes SCM ;
- liste de depenses communes SCM ;
- contrat de frais communs SCM ;
- reglement interieur SCM ;
- tout formulaire ou annexe non sourcee dans les quatre DOCX civils ;
- PDF, ZIP et UI.

### Regles de non-fusion

Le futur code ne doit pas :
- fusionner SCI et SCI IRIS ;
- rapprocher SCM de SCI ou SCS ;
- deduire les roles SCS depuis la position d'un associe ;
- injecter un bloc fiscal IS dans les statuts SCI ou SCI IRIS ;
- automatiser un document satellite SCM depuis les statuts.

## 9. Option IS et documents satellites SCM

### Classement

Manuel V1.

### Option IS

La lettre d'option IS mentionnee par la source de verite est un document separe.

Elle ne doit pas etre codee dans la famille `statuts civils` et ne doit pas etre injectee comme bloc dans les statuts SCI ou SCI IRIS.

Si `fiscalite.option_is = true` dans un contexte dossier :
- les statuts restent produits selon leur source propre ;
- la lettre option IS reste a produire manuellement ou via un futur ticket dedie ;
- une demande de generation automatique de la lettre IS doit bloquer tant qu'aucune spec separee n'existe.

### Documents satellites SCM

Les documents satellites SCM restent hors automatisation V1 :
- pacte d'associes ;
- liste de depenses communes ;
- contrat de frais communs ;
- reglement interieur.

Ils doivent etre traites manuellement ou par futurs tickets separes avec sources, specs et arbitrages dedies.

## 10. Points bloquants restants avant code

Les arbitrages ci-dessus ferment les choix de modele principaux.

Restent bloquants pour le futur code si non fournis par la spec de code ou le contexte :
- texte source long a reprendre sans derive, article par article ou via reconstruction documentee ;
- donnees sensibles manuelles : situations matrimoniales, banques, adresses, RCS, professions, fonctions, qualites, dates ;
- coherence numerique apports / capital / parts / plages ;
- donnees de resultat exceptionnel SCI IRIS ;
- donnees de personnes morales et representants ;
- decision explicite sur le traitement de la ligne SCM fixe `510 euros` ;
- validation humaine juridique et visuelle du premier rendu DOCX.

## 11. Prochaine etape recommandee

Ouvrir un ticket de code limite a un seul document civil, de preference `LOT04-STATUTS-SCI`, apres redaction d'une spec de code detaillee de reprise du texte et des validations d'entree.
