# DAAT x SYDEL - ARBITRAGES V1
## Statuts SCM - ARBITRAGE-STATUTS-SCM-001

## 1. Objet

Fermer les arbitrages specifiques aux statuts SCM avant tout code SCM.

Cette note complete :
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.

Elle ne code aucun generateur, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partage.

## 2. Sources relues

Memoire projet :
- `AGENTS.md` ;
- `docs/project/00_MASTER_PLAN.md` ;
- `docs/project/01_EXECUTION_BOARD.md` ;
- `docs/project/02_CODEX_WORKFLOW.md` ;
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` ;
- `docs/project/04_LAST_STATE.md`.

Specs et arbitrages :
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.

ADR reperes :
- `docs/adr/0001-source-of-truth.md` ;
- `docs/adr/0002-engine-per-document.md` ;
- `docs/adr/0003-lot-based-delivery.md` ;
- `docs/adr/0005-codex-working-mode.md`.

Source de verite metier relue :
- `project/source_truth/Documents_a_generer_par_cas.docx`.

Source statuts SCM relue :
- `project/source_documents/lot_04/Statuts SCM.docx`.

Documents SCM satellites presents et lus en lecture seule :
- `project/source_import/raw_drive_dump/creation scm/Pacte d_associes SCM.docx` ;
- `project/source_import/raw_drive_dump/creation scm/Liste depenses communes SCM.doc` ;
- `project/source_import/raw_drive_dump/creation scm/CONTRAT FRAIS COMMUNS.docx` ;
- `project/source_import/raw_drive_dump/creation scm/2024 REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx` ;
- copies presentes hors commit dans `project/source_documents/lot_05/` lorsque disponibles.

Note : les chemins ci-dessus sont normalises sans accents pour la lisibilite. Les noms physiques peuvent contenir des accents decomposes sur disque.

## 3. Synthese des arbitrages SCM

| Point | Classement V1 | Decision |
|---|---|---|
| Associes dynamiques | tranche | Les statuts SCM utilisent `associes[]` comme verite metier, avec 1 a 6 associes, personnes physiques ou morales. |
| Donnees sensibles des associes SCM | manuel V1 | Profession, qualite, situation matrimoniale, RCS, representant et fonction sont fournis explicitement par le dossier ou un referentiel valide. |
| Anomalie de repartition des parts | tranche | Le placeholder source duplique ne doit pas etre conserve comme source de verite ; les parts sont explicites par associe. |
| Contexte legacy de parts SCM ambigu | bloquant | Une seule valeur heritee `nb_parts_personne_2` pour deux lignes de repartition est insuffisante et doit bloquer. |
| Ligne fixe `510 euros` / `510 EUR` | tranche | La valeur fixe est une anomalie source ; le montant de l'apport personne physique doit venir d'une donnee explicite. |
| Apport personne physique absent ou incoherent | bloquant | La generation bloque si le montant explicite ou sa coherence avec les apports/capital n'est pas fourni. |
| Signatures dynamiques | tranche | Les signatures sont rendues depuis les associes ou une liste `signataires[]`, avec une mention par signataire. |
| Frontiere statuts SCM / satellites SCM | tranche | `Statuts SCM.docx` est le seul document statutaire SCM du Lot 04 ; les satellites SCM sont des documents distincts hors code statuts SCM. |
| Documents satellites SCM | manuel V1 | Pacte, liste de depenses, contrat frais communs et reglement interieur restent hors automatisation du generateur statuts SCM. |

## 4. Associes dynamiques SCM

### Classement

Tranche.

Les donnees d'identification sensibles sont en manuel V1.

### Decision

Les statuts SCM ne doivent pas etre codes avec les roles fixes `societe_1` et `personne_2` comme verite metier.

La V1 retient une liste canonique `associes[]`, bornee de 1 a 6 associes, pouvant contenir :
- des associes personnes morales professionnelles ;
- des associes personnes physiques professionnelles.

Les placeholders source observes restent des aliases documentaires :
- `[denomination_societe_1]` ;
- `[forme_sociale_societe_1]` ;
- `[profession_societe_1]` ;
- `[civilite_personne_2]` ;
- `[prenom_personne_2]` ;
- `[nom_personne_2]`.

Le futur code SCM devra rendre dynamiquement :
- la comparution ;
- les apports ;
- la repartition du capital ;
- les signatures.

### Donnees manuelles V1

Les champs suivants ne sont pas deduits par le moteur :
- profession ou qualite professionnelle ;
- situation matrimoniale ;
- adresse affichee ;
- RCS et ville RCS ;
- representant de personne morale ;
- fonction du representant ;
- apport ;
- nombre de parts.

## 5. Anomalie de repartition des parts

### Classement

Tranche pour la strategie de modele.

Bloquant pour tout contexte legacy ambigu.

### Constat source

Dans `Statuts SCM.docx`, la repartition du capital contient deux lignes distinctes :
- personne morale : `[denomination_societe_1][nb_parts_personne_2] parts` ;
- personne physique : `[civilite_personne_2] [prenom_personne_2] [nom_personne_2][nb_parts_personne_2] parts`.

Le meme placeholder `[nb_parts_personne_2]` est donc utilise pour deux associes differents.

### Decision

Le futur code SCM ne doit jamais utiliser `nb_parts_personne_2` comme valeur unique pour les deux associes.

La V1 exige une repartition explicite par associe :
- `associes[].parts.nb` pour chaque associe ;
- `societe.nb_parts_total` pour le total ;
- controle de somme entre les parts par associe et le total.

### Blocage attendu

La generation SCM doit bloquer si :
- le contexte ne fournit qu'une seule valeur heritee `nb_parts_personne_2` ;
- une ligne de repartition n'a pas de nombre de parts propre ;
- la somme des parts par associe ne correspond pas a `societe.nb_parts_total`.

## 6. Ligne fixe `510 euros`

### Classement

Tranche pour le traitement documentaire.

Bloquant si la donnee explicite est absente.

### Constat source

Dans `Statuts SCM.docx`, l'article 6 contient :
- une ligne d'apport personne morale avec placeholders ;
- une ligne d'apport personne physique dont le montant en lettres est variable ;
- une ligne de montant chiffre fixe `510 EUR` dans la source extraite.

Cette valeur fixe ne peut pas etre consideree comme une regle metier generale.

### Decision

Le futur code SCM ne doit pas coder `510 EUR` en dur.

Le montant chiffre de l'apport de la personne physique doit provenir d'une donnee explicite :
- `associes[].apport.montant` ;
- avec, si la source le rend, `associes[].apport.montant_lettres`.

Si le dossier confirme que l'apport est effectivement de 510 euros, le rendu peut afficher cette valeur parce qu'elle vient du contexte, pas parce qu'elle est fixe dans le modele source.

### Blocage attendu

La generation SCM doit bloquer si :
- l'apport chiffre de la personne physique est absent ;
- l'apport en lettres et l'apport chiffre sont incoherents ;
- le total des apports ne correspond pas au capital social ;
- le contexte tente de reutiliser la valeur fixe source sans decision dossier explicite.

## 7. Signatures dynamiques

### Classement

Tranche.

### Decision

Les signatures SCM sont dynamiques.

Par defaut, les signataires sont derives des associes du document. Le contexte peut fournir `signataires[]` uniquement pour imposer un ordre ou un libelle de signature, sans ajouter de tiers non prevu par la spec.

Le rendu doit produire une signature par signataire :
- associe personne morale : denomination de la personne morale et, lorsque requis, representant et fonction ;
- associe personne physique : civilite, prenom et nom ;
- mention source `Lu et approuve` separee par signataire.

### Blocage attendu

La generation SCM doit bloquer si :
- un associe signataire n'a pas de libelle de signature calculable ;
- une personne morale signataire n'a pas de representant alors que le texte l'affiche ;
- `signataires[]` contient un tiers non associe sans spec complementaire ;
- le nombre de signatures ne correspond pas aux associes ou signataires fournis.

## 8. Frontiere exacte statuts SCM / satellites SCM

### Classement

Tranche pour la frontiere.

Manuel V1 pour les satellites.

### Inclus dans les statuts SCM Lot 04

Le generateur `LOT04-STATUTS-SCM` couvre uniquement le document :
- `project/source_documents/lot_04/Statuts SCM.docx`.

Le perimetre de ce document comprend :
- page de garde ;
- comparution ;
- forme ;
- denomination ;
- siege ;
- objet social ;
- duree ;
- apports ;
- capital social ;
- droits et obligations attaches aux parts ;
- cessions, retrait et deces ;
- gerance ;
- decisions collectives ;
- comptes sociaux ;
- prorogation, transformation, dissolution et liquidation ;
- litiges, contre-lettre, election de domicile et communication du contrat ;
- signatures.

### Hors generateur statuts SCM

Les documents suivants sont des sorties distinctes et ne doivent pas etre injectes dans les statuts SCM :
- `Pacte d_associes SCM.docx` ;
- `Liste depenses communes SCM.doc` ;
- `CONTRAT FRAIS COMMUNS.docx` ;
- `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx`.

Sont egalement hors generateur statuts SCM :
- `Fiche de creation de SCM - transforme.docx`, traitee comme support de collecte d'informations et non comme statut ;
- documents de cession de parts SCM vers SELARL ou SELAS ;
- PV AGE de cession de parts SCM ;
- courrier SDE ;
- PV nomination gerant, demande d'inscription a l'ordre, declaration de non-condamnation, autorisation de domiciliation et procuration, qui relevent deja d'autres documents canoniques.

### Consequence

Le futur code des statuts SCM ne doit pas :
- ajouter un pacte d'associes en annexe ;
- ajouter la liste de depenses communes ;
- ajouter le contrat de frais communs ;
- ajouter le reglement interieur ;
- reprendre des clauses satellites pour completer les statuts.

Chaque satellite SCM devra faire l'objet d'une spec separee avant automatisation.

## 9. Points manuels V1

Restent manuels ou fournis explicitement par contexte/referentiel valide :
- donnees professionnelles des associes ;
- donnees RCS et representants des personnes morales ;
- situations matrimoniales ;
- banque et adresse de banque ;
- apports chiffres et en lettres ;
- parts par associe ;
- signatures et ordre de signature si l'ordre source ne suffit pas ;
- production des satellites SCM.

## 10. Points bloquants restants

Aucun arbitrage SCM liste par ce ticket ne reste ouvert.

En revanche, le futur generateur SCM devra bloquer a l'execution si :
- les donnees explicites d'apports ou de parts sont absentes ;
- les totaux apports / capital / parts sont incoherents ;
- une personne morale affichee n'a pas de representant requis ;
- une signature attendue n'est pas calculable ;
- un satellite SCM est demande via le generateur statuts SCM.

Avant tout code satellite SCM, une spec separee reste obligatoire.

## 11. Prochaine etape recommandee

Ouvrir un ticket de code limite au seul generateur `LOT04-STATUTS-SCM`, avec reprise stricte du texte source `Statuts SCM.docx`, validations d'entree explicites et tests ciblant les blocages ci-dessus.
