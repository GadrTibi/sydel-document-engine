# DAAT x SYDEL - SPEC TEXTE V1
## Famille `derogations`

## 1. Objet

Stabiliser les textes, blocs et zones variables de la famille documentaire
`derogations`, sans coder.

Cette spec texte complete :
- `docs/delivery/lot_03_derogations_spec_canonique_v1.md`

Elle vise a preparer d'eventuels generateurs deterministes partiels, tout en
conservant hors automatisation initiale les formulaires ou zones marquees
manuelles.

Regles appliquees :
- aucun wording juridique n'est corrige ou enrichi ;
- aucun contenu narratif sensible n'est invente ;
- aucun document marque `A REMPLIR A LA MAIN` n'est transforme en document
  automatisable ;
- les zones libres restent manuelles ou bloquantes si un futur rendu ne doit pas
  contenir de blanc.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_03_derogations_spec_canonique_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Constat de placement :
- `project/source_documents/lot_03/` ne contient que `README.md` ;
- les sources demandees ont donc ete lues dans
  `project/source_import/raw_drive_dump/`, conformement au fallback du ticket.

Sources Lot 03 lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Derogation/Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Derogation/Demande de derogation cumul SELARL - BNC.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`

Note de chemin :
- les chemins ci-dessus sont normalises sans accents dans cette spec ;
- les fichiers reels conservent leurs accents et variantes Unicode dans le depot.

Note technique sur le `.doc` legacy :
- le fichier `Demande_derogation_cumul_SELARL_salariee.doc` est un ancien
  format Word binaire ;
- il a ete lu en extraction texte read-only depuis les chaines Unicode du
  document ;
- une conversion en DOCX propre reste obligatoire avant tout codage.

## 3. Rattachements source de verite

### 3.1 SELARL

La source de verite rattache a la famille SELARL :
- `Si site distinct` :
  - `Formulaire derogation procuration` ;
  - statut explicite `A REMPLIR A LA MAIN` ;
  - source nommee : `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx`.
- `Si derogation` :
  - `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL` ;
  - `Derogation SEL BNC` marquee `A REMPLIR A LA MAIN` ;
  - `Derogation cumul SELARL BNC` avec source
    `Demande de derogation cumul SELARL - BNC.docx`.

### 3.2 SELAS

La source de verite rattache a la famille SELAS :
- `Si derogation` :
  - `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL` ;
  - `Demande de derog. cumul SELARL salarie` avec source
    `Demande_derogation_cumul_SELARL_salariee.doc`.

Decision texte V1 :
- SELARL et SELAS restent deux structures eligibles ;
- `site distinct`, `multi_sites_sel`, `cumul_sel_bnc` et `cumul_salariee`
  restent des sous-familles distinctes ;
- aucune fusion entre site distinct CD94, formulaire multi-sites SEL et cumul
  d'exercices n'est faite dans cette spec.

## 4. Documents et statuts texte V1

| Sous-famille | Source | Statut texte V1 | Automatisation V1 |
|---|---|---|---|
| `site_distinct_manual` | `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx` | formulaire ordinal manuel | hors automatisation initiale |
| `multi_sites_sel` | `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx` | formulaire pre-remplissable partiellement | candidat generateur partiel apres arbitrage |
| `sel_bnc_manual` | `Derogation SEL BNC` / formulaire complet | piece manuelle | hors automatisation initiale |
| `cumul_sel_bnc` | `Demande de derogation cumul SELARL - BNC.docx` | demande pre-remplissable partiellement | candidat generateur partiel apres arbitrage |
| `cumul_salariee` | `Demande_derogation_cumul_SELARL_salariee.doc` | demande pre-remplissable partiellement, source legacy | bloquee avant conversion DOCX |

## 5. Texte source - formulaire multi-sites SEL

Source :
- `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx`

Titre source :

```text
Declaration prealable d'ouverture d'un site distinct de la residence professionnelle d'une SEL
A adresser au conseil departemental du lieu ou se situe le site au plus tard deux mois avant le debut d'activite
Article R4113- 23 du code de la sante publique
```

### 5.1 Blocs automatisables

Les blocs suivants contiennent des placeholders ou zones structurees
pre-remplissables.

#### Identification de la societe

```text
Societe
Denomination de la SEL : [denomination_societe]
Departement d'inscription de la SEL : [departement_inscription_societe]
N° departemental d'inscription de la SEL : [numero_inscription_societe]
Adresse du siege social : [adresse_siege]
```

Automatisable si les variables de societe et d'inscription ordinale SEL sont
fournies.

#### Representant legal

```text
Representant legal de la societe
Nom : [nom_personne_1]      Prenom : [prenom_personne_1]
Mandat (gerant/president/...) : [fonction_dirigeant]
Adresse electronique : [email_personne_1]
```

Automatisable en mappant `personne_1` vers le role canonique valide pour le
document.

Point de vigilance :
- la source ne prouve pas que le representant legal et l'associe exercant sont
  toujours la meme personne ;
- la spec canonique propose de distinguer `signataire`, `representant_legal` et
  `associe_exercant` si le futur code en a besoin.

#### Associe exercant sur le nouveau site

```text
Identification de l'associe/des associes qui exercera/ont sur le nouveau site
Nom : [nom_personne_1]
Prenom : [prenom_personne_1]
Qualification : [qualification_principale]
```

Automatisable pour un premier associe si le contexte des roles est arbitre.

#### Sites deja autorises

```text
Autres sites d'exercice :
NON
[choix_oui]OUI
Nombre de sites :
1er site
Date du debut d'activite : [date_debut_activite_site_1]
Adresse du site : [adresse_siege]
```

Automatisable uniquement si :
- le choix oui/non est fourni explicitement ;
- les sites existants sont fournis sous forme structuree ;
- la source `[adresse_siege]` utilisee dans `Adresse du site` est confirmee
  comme voulue, et non comme placeholder de repli.

#### Certification finale

```text
Je soussigne Monsieur [prenom_personne_1] [nom_personne_1] certifie :
l'exactitude de l'ensemble des informations fournies ou jointes au present formulaire et que toute modification de mes conditions d'exercice sera communiquee au conseil departemental de la residence professionnelle de la SEL,
que l'ouverture du site n'est pas contraire aux dispositions legislatives et reglementaires.
Fait le ___|___|/|___|___|/|___|___|___|___| a
```

Automatisable partiellement :
- prenom et nom du signataire ;
- eventuellement date et lieu de signature si le formulaire est transforme en
  document pre-rempli.

Non automatise en V1 sans validation :
- `Monsieur` reste fixe dans la source lue ;
- aucune feminisation ou variation `Monsieur/Madame` ne doit etre ajoutee sans
  arbitrage.

### 5.2 Blocs manuels

Restent manuels, meme dans un futur generateur partiel :
- qualification mono-disciplinaire ou pluri-disciplinaire detaillee ;
- adresse complete du nouveau site si elle n'est pas fournie comme variable
  structuree ;
- nature de l'activite envisagee :
  - consultations ;
  - actes medico-techniques ;
  - actes chirurgicaux ;
  - autres ;
- temps hebdomadaire consacre ;
- autres sites d'exercice au-dela du premier si aucune liste structuree n'est
  fournie ;
- moyens en personnel ;
- materiels ;
- dispositions de continuite des soins ;
- informations sur l'environnement de travail ;
- pieces a joindre.

Regle :
- ces champs sont des contenus narratifs ou operationnels sensibles ;
- le moteur ne doit pas les inventer ;
- un futur rendu devra soit les recevoir explicitement, soit laisser le
  formulaire clairement a completer, soit bloquer.

### 5.3 Variables du formulaire multi-sites SEL

| Placeholder source | Variable canonique texte V1 | Statut |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | automatisable |
| `[departement_inscription_societe]` | `societe.inscription_ordre.departement` | automatisable |
| `[numero_inscription_societe]` | `societe.inscription_ordre.numero` | automatisable |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | automatisable, a verifier selon emplacement |
| `[nom_personne_1]` | `representant_legal.nom` ou `associe_exercant.nom` | arbitrage role requis |
| `[prenom_personne_1]` | `representant_legal.prenom` ou `associe_exercant.prenom` | arbitrage role requis |
| `[fonction_dirigeant]` | `representant_legal.fonction` | automatisable |
| `[email_personne_1]` | `representant_legal.contact.email` | automatisable |
| `[qualification_principale]` | `associe_exercant.qualification_principale` | automatisable |
| `[choix_oui]` | `sites_existants.present` | automatisable si explicite |
| `[date_debut_activite_site_1]` | `sites_existants[0].date_debut_activite` | automatisable si liste fournie |

## 6. Texte source - cumul SELARL / BNC

Source :
- `Demande de derogation cumul SELARL - BNC.docx`

Titre source :

```text
Demande de cumul d'exercices en societe d'exercice liberal (SEL)
et a titre individuel
(Articles R.4113-3 et R.4127-85 du Code de la sante publique)
```

### 6.1 Blocs automatisables

#### Identification du declarant

```text
Demande formulee par le Docteur :
Nom : [nom]
Prenom : [prenom]
Inscrit au Tableau du Conseil departemental de: [ville_ordre]
Sous le numero : [numero_inscription_ordre]
Qualification principale : [qualification_principale]
Adresse de correspondance : [adresse_siege]
Code postal :  [cp_siege]
Commune : [ville_siege]
N° de telephone : [telephone]
Adresse electronique : [email]
```

Automatisable si le declarant et son contact ordinal sont fournis.

#### Identification de la SEL

```text
Identification de la societe (SEL)
Denomination sociale : [denomination_societe]
Inscrite au Tableau du Conseil departemental de: [ville_ordre_sel]
Sous le numero : [numero_inscription_societe]
Adresse du siege social : [adresse_siege]
```

Automatisable si les variables de societe et d'inscription ordinale SEL sont
fournies.

#### Lieux d'exercice - valeurs structurees

```text
Concernant votre exercice en SEL :
Adresse de la residence professionnelle de votre SEL(activite principale) : [adresse_siege]
Temps hebdomadaire consacre(nombre de demi-journees) :
```

Automatisable pour l'adresse du siege ; manuel pour le temps hebdomadaire si
absent du contexte.

#### Certification et signature

```text
Je soussigne(e) Dr [prenom] [nom]certifie :
L'exactitude de l'ensemble des informations fournies ou jointes au present formulaire et que toute modification de mes conditions d'exercice sera communiquee au conseil departemental de ma residence professionnelle,
(Le Conseil departemental vous informe que toute declaration volontairement inexacte ou incomplete faite au Conseil de l'Ordre par un medecin peut donner lieu a des poursuites disciplinaires, conformement a l'article R. 4127-110 du Code de la sante publique)
Que l'ouverture du site n'est pas contraire aux dispositions legislatives et reglementaires.
Fait le [date_signature]
a [lieu_signature]
Signature :
```

Automatisable :
- prenom, nom ;
- date et lieu de signature.

Regle de fidelite :
- conserver `soussigne(e)` tel que source ;
- ne pas corriger l'absence d'espace dans `[nom]certifie` sans ticket explicite
  de correction ou validation humaine.

### 6.2 Blocs manuels

Restent manuels :
- autres disciplines exercees ;
- type d'activite individuelle `Salariee` / `Liberale` ;
- adresse de l'activite individuelle ;
- temps hebdomadaire de l'activite individuelle ;
- temps hebdomadaire en SEL ;
- autres sites d'exercice deja declares ;
- continuite des soins sur chaque lieu ;
- choix des criteres fondant la demande de cumul ;
- explication obligatoire de chaque case cochee ;
- pieces jointes.

Extrait source sensible :

```text
Toute case cochee doit etre accompagnee d'une explication :
□ - L'exercice dans votre SEL est lie a des techniques medicales necessitant un regroupement ou un travail en equipe
□ - L'exercice dans votre SEL est lie a l'acquisition d'equipements ou de materiels lourds soumis a autorisation
□ - L'exercice dans votre SEL necessite l'acquisition d'equipements ou de materiels qui justifient des utilisations multiples
```

Regle :
- aucune case ne doit etre cochee automatiquement ;
- aucune explication ne doit etre generee par defaut ;
- si un futur document final exige ces rubriques, leur absence doit bloquer la
  generation.

### 6.3 Variables de cumul SELARL / BNC

| Placeholder source | Variable canonique texte V1 | Statut |
|---|---|---|
| `[nom]` | `signataire.nom` | automatisable |
| `[prenom]` | `signataire.prenom` | automatisable |
| `[ville_ordre]` | `ordre.ville` | automatisable |
| `[numero_inscription_ordre]` | `signataire.numero_inscription_ordre` | automatisable |
| `[qualification_principale]` | `signataire.qualification_principale` | automatisable |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | automatisable |
| `[cp_siege]` | `societe.siege.cp` | automatisable |
| `[ville_siege]` | `societe.siege.ville` | automatisable |
| `[telephone]` | `signataire.contact.telephone` | automatisable |
| `[email]` | `signataire.contact.email` | automatisable |
| `[denomination_societe]` | `societe.denomination` | automatisable |
| `[ville_ordre_sel]` | `societe.inscription_ordre.ville` | automatisable |
| `[numero_inscription_societe]` | `societe.inscription_ordre.numero` | automatisable |
| `[date_signature]` | `signature.date` | automatisable |
| `[lieu_signature]` | `signature.lieu` | automatisable |

## 7. Texte source - cumul salariee / activite externe

Source :
- `Demande_derogation_cumul_SELARL_salariee.doc`

Statut source :
- ancien format Word `.doc` ;
- rattache dans le raw dump SELAS ;
- nomme `SELARL_salariee` ;
- texte source mentionnant plus largement une `activite externe`.

Titre source extrait :

```text
Renseignements en vue d'une demande
de cumul d'exercice
(article R.4113-3 du code de la sante publique)
```

### 7.1 Blocs automatisables

#### Rappel legal fixe

```text
Pour rappel, l'article R.4113-3 du Code de la Sante Publique exige que le medecin exerce uniquement son activite dans la SEL (Societe d'Exercice Liberal) et ne peut donc cumuler cette activite avec un exercice a titre individuel ou en SCP.
Cependant, le meme article prevoit une derogation dans le cas ou l'exercice en SEL par le medecin concerne :
- est lie a des techniques medicales necessitant un regroupement ou un travail en equipe ;
- necessite l'acquisition d'equipements ou de materiels soumis a une autorisation ;
- necessite l'acquisition d'equipements ou de materiels qui justifient des utilisations multiples.
Si l'une des conditions est remplie, le Conseil departemental de [ville_ordre] peut autoriser le medecin a cumuler son activite en SEL avec une activite externe.
```

Automatisable seulement pour `[ville_ordre]`.

Regle :
- le rappel legal peut etre rendu fixe apres conversion DOCX propre ;
- ne pas corriger ni reformuler le texte source sans validation.

#### Demande formulee par

```text
DEMANDE FORMULEE PAR :
Le Docteur [prenom] [nom]
Inscrit au tableau du Conseil departemental sous le n° [numero_inscription_ordre]
Qualification : [qualification_principale]
Adresse du siege social de votre SEL
[adresse_siege]
Adresse du site pour lequel l'autorisation est sollicitee
[adresse_lieu_exercice]
```

Automatisable pour les donnees d'identification, de siege et de site si elles
sont fournies.

#### Date et signature

```text
Date :
[date_signature]
Signature :
```

Automatisable uniquement pour la date ; la signature manuscrite reste manuelle.

### 7.2 Blocs manuels

Restent manuels :
- case(s) cochee(s) sur les criteres de demande ;
- explication associee a chaque case cochee ;
- renseignements sur l'activite a la residence professionnelle habituelle ;
- dispositions de continuite des soins ;
- reponse aux urgences ;
- organisation pratique pour les patients pris en charge dans le cadre de la
  SEL ;
- signature manuscrite.

Extrait source sensible :

```text
A : Critere(s) sur le(s)quel(s) est fondee la demande :
(Cochez la ou les cases concernees. Toute case cochee doit etre accompagne d'une explication)
B : Renseignements sur l'activite a la residence professionnelle habituelle
Dispositions prises pour assurer la continuite des soins et reponse aux urgences (secretariat, portable, collaborateur disponible, etc.) pour les patients prises en charge dans le cadre de la SEL
N. B. : Le Conseil departemental de [ville_ordre] se positionnera uniquement si les points A et B sont remplis consciencieusement par le medecin.
```

Regle :
- le futur moteur ne doit pas produire une demande finalisee si les points A et B
  obligatoires sont absents ;
- a defaut, le rendu doit etre explicitement classe comme formulaire a completer.

### 7.3 Variables de cumul salariee / activite externe

| Placeholder source | Variable canonique texte V1 | Statut |
|---|---|---|
| `[ville_ordre]` | `ordre.ville` | automatisable |
| `[prenom]` | `signataire.prenom` | automatisable |
| `[nom]` | `signataire.nom` | automatisable |
| `[numero_inscription_ordre]` | `signataire.numero_inscription_ordre` | automatisable |
| `[qualification_principale]` | `signataire.qualification_principale` | automatisable |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | automatisable |
| `[adresse_lieu_exercice]` | `site_declare.adresse_affichee` | automatisable |
| `[date_signature]` | `signature.date` | automatisable |

## 8. Formulaires a remplir a la main

### 8.1 Site distinct CD94

Statut :
- source de verite : `A REMPLIR A LA MAIN` ;
- aucun generateur V1 ;
- piece eventuellement listable dans un futur ZIP dossier.

Regle :
- ne pas automatiser tant qu'un arbitrage explicite ne retire pas le statut
  manuel ;
- ne pas assimiler ce formulaire au formulaire multi-sites SEL, meme si les
  objets metier sont proches.

### 8.2 Derogation SEL BNC manuelle / formulaire complet

Statut :
- source de verite : `Derogation SEL BNC` marquee `A REMPLIR A LA MAIN` ;
- spec canonique : `Derogation SEL BNC complet.docx` classe comme formulaire ou
  aide complete manuelle ;
- aucun generateur V1.

Regle :
- ne pas fusionner cette piece avec `Demande de derogation cumul SELARL - BNC.docx`
  sans arbitrage texte ;
- elle peut servir de reference de revue, pas de source executable.

### 8.3 Zones narratives des documents pre-remplissables

Meme lorsqu'un document est candidat a un generateur partiel, les zones suivantes
restent manuelles :
- activite envisagee ;
- temps hebdomadaires ;
- autres sites ;
- materiels et moyens ;
- continuite des soins ;
- environnement professionnel ;
- criteres de derogation ;
- explications associees aux cases cochees ;
- pieces jointes ;
- signatures manuscrites.

## 9. Variables canoniques consolidees

### 9.1 Selection dossier

- `dossier.structure`
- `dossier.options.site_distinct`
- `dossier.options.derogation`
- `derogation.type`

Valeurs `derogation.type` retenues pour cette famille :
- `site_distinct_manual`
- `multi_sites_sel`
- `cumul_sel_bnc`
- `cumul_salariee`
- `sel_bnc_manual`

### 9.2 Societe / SEL

- `societe.denomination`
- `societe.siege.adresse_affichee`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.inscription_ordre.departement`
- `societe.inscription_ordre.ville`
- `societe.inscription_ordre.numero`

### 9.3 Signataire / declarant

- `signataire.prenom`
- `signataire.nom`
- `signataire.numero_inscription_ordre`
- `signataire.qualification_principale`
- `signataire.contact.telephone`
- `signataire.contact.telephone_mobile`
- `signataire.contact.email`

### 9.4 Roles a arbitrer

- `representant_legal.prenom`
- `representant_legal.nom`
- `representant_legal.fonction`
- `representant_legal.contact.email`
- `associe_exercant.prenom`
- `associe_exercant.nom`
- `associe_exercant.qualification_principale`

Regle :
- ces roles peuvent pointer vers `signataire` ou `associes[]`, mais ce mapping
  doit etre arbitre avant code.

### 9.5 Ordre professionnel

- `ordre.ville`
- `ordre.departement`

### 9.6 Site declare et sites existants

- `site_declare.adresse_affichee`
- `site_declare.date_debut_activite`
- `site_declare.activite.description_consultations`
- `site_declare.activite.description_actes_medico_techniques`
- `site_declare.activite.description_actes_chirurgicaux`
- `site_declare.activite.description_autres`
- `site_declare.temps_hebdomadaire`
- `sites_existants.present`
- `sites_existants[]`
  - `adresse_affichee`
  - `date_debut_activite`
  - `temps_hebdomadaire`
  - `nature_activite`

### 9.7 Cumul et conditions

- `derogation.cumul.activite_individuelle.type`
- `derogation.cumul.activite_individuelle.adresse_affichee`
- `derogation.cumul.activite_individuelle.temps_hebdomadaire`
- `derogation.cumul.activite_sel.temps_hebdomadaire`
- `derogation.cumul.activite_externe.libelle`
- `derogation.cumul.motifs.regroupement_equipe`
- `derogation.cumul.motifs.equipement_soumis_autorisation`
- `derogation.cumul.motifs.equipement_usages_multiples`
- `derogation.cumul.motifs.explication`
- `derogation.conditions.continuite_soins`
- `derogation.conditions.environnement_travail`
- `derogation.conditions.reponse_urgences`

### 9.8 Signature

- `signature.date`
- `signature.lieu`

## 10. Regles de blocage avant futur code

Un futur generateur doit bloquer si :
- `derogation.type` est absent ou non reconnu ;
- le document cible est classe manuel ;
- la source propre n'est pas disponible dans `project/source_documents/lot_03/`
  ou explicitement arbitree depuis le raw dump ;
- le document source est encore en `.doc` legacy ;
- un role source `personne_1` doit etre rendu sans arbitrage
  `signataire` / `representant_legal` / `associe_exercant` ;
- une zone narrative obligatoire est absente alors que le rendu attendu est un
  document finalise ;
- une case a cocher devrait etre cochee sans donnee explicite ;
- une explication juridique devrait etre generee sans texte fourni ;
- une feminisation ou correction de wording source serait necessaire sans
  validation.

Un futur generateur partiel peut seulement produire un formulaire a completer si :
- ce statut est explicite dans le nom du document produit ou dans son registre ;
- les zones laissees vides restent visibles ;
- la piece n'est pas presentee comme document juridiquement finalise.

## 11. Criteres avant implementation

Aucun code ne doit demarrer avant :
- placement ou arbitrage explicite des sources Lot 03 ;
- conversion du `.doc` legacy en DOCX propre pour `cumul_salariee` ;
- decision sur `formulaire pre-rempli avec blancs visibles` vs `blocage si
  champs narratifs absents` ;
- arbitrage des roles `signataire`, `representant_legal` et `associe_exercant` ;
- decision sur la gestion des cases a cocher ;
- decision sur la feminisation eventuelle de `Monsieur` dans le formulaire
  multi-sites ;
- tests prevus par sous-famille, avec verification d'absence de placeholders
  residuels pour tout document finalise.

## 12. Points ouverts

1. Les sources Lot 03 ne sont pas encore placees dans
   `project/source_documents/lot_03/`.
2. Faut-il autoriser des formulaires pre-remplis avec zones vierges visibles, ou
   bloquer tant que toutes les zones narratives obligatoires ne sont pas saisies ?
3. Le role `[nom_personne_1]` / `[prenom_personne_1]` du formulaire multi-sites
   represente-t-il toujours le signataire, le representant legal et l'associe
   exercant ?
4. Le placeholder `[adresse_siege]` utilise comme `Adresse du site` dans le
   premier site existant est-il intentionnel ?
5. Le `.doc` `Demande_derogation_cumul_SELARL_salariee.doc` doit etre converti
   en DOCX propre avant tout codage.
6. La sous-famille `cumul_salariee` doit-elle etre renommee
   `cumul_activite_externe`, puisque le texte source parle d'activite externe ?
7. Le formulaire multi-sites conserve `Monsieur [prenom_personne_1]
   [nom_personne_1]` ; aucune feminisation n'est arbitree.
8. Les cases cochees et leurs explications doivent rester des donnees explicites,
   jamais deduites automatiquement.
9. Les pieces jointes obligatoires sont listees par les sources, mais leur
   production automatique reste hors perimetre de cette spec.

## 13. Statut de la spec texte

`SPEC-TEXTE-DEROG-001` est complete cote spec texte V1, sans code Python et sans
modification des fichiers de pilotage partages.

Prochaine etape recommandee :
- arbitrer le statut de rendu des formulaires pre-remplis pour `multi_sites_sel`
  et `cumul_sel_bnc`, puis convertir ou remplacer la source `.doc` legacy avant
  toute implementation de `cumul_salariee`.
