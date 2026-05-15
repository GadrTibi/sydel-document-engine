# DAAT x SYDEL - SPEC CANONIQUE V1
## Bloc cession de parts SCM vers SEL

## 1. Objet

Ticket : `SPEC-SCM-CESSION-BLOCK-001`.

Cette spec formalise le bloc documentaire de cession de parts de SCM vers une SEL d'exercice, pour les chemins :
- SELARL ;
- SELAS.

Elle couvre uniquement les six sources demandees :
- `PV AGE cession part SCM.docx` ;
- `Courrier SDE.docx` ;
- `Acte de cession des parts de la SCM a la SELARL - transforme.docx` ;
- `PV AGE cession part SCM - SELAS.docx` ;
- `Courrier SDE - SELAS.docx` ;
- `Acte_cession_parts_SCM_SEL_modele.docx`.

Elle ne code rien, ne deplace aucune source, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partage.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md` ;
- `docs/project/00_MASTER_PLAN.md` ;
- `docs/project/01_EXECUTION_BOARD.md` en lecture seule ;
- `docs/project/02_CODEX_WORKFLOW.md` ;
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` ;
- `docs/project/04_LAST_STATE.md` en lecture seule ;
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md` ;
- `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md` ;
- `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md` ;
- `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md` ;
- `docs/delivery/lot_05_scm_satellites_preparation_v1.md` ;
- `docs/delivery/lot_05_scm_satellites_spec_canonique_v1.md` ;
- `docs/delivery/lot_05_scm_satellites_spec_texte_v1.md`.

ADR reperes :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`.

Sources documentaires lues depuis le raw dump local, car elles ne sont pas placees dans `project/source_documents/lot_05/` sur la branche de travail :
- `project/source_import/raw_drive_dump/Creation SELARL/scm cession/PV AGE cession part SCM.docx` ;
- `project/source_import/raw_drive_dump/Creation SELARL/scm cession/Courrier SDE.docx` ;
- `project/source_import/raw_drive_dump/Creation SELARL/scm cession/Acte de cession des parts de la SCM a la SELARL - transforme.docx` ;
- `project/source_import/raw_drive_dump/Creation SELAS/SCM/PV AGE cession part SCM - SELAS.docx` ;
- `project/source_import/raw_drive_dump/Creation SELAS/SCM/Courrier SDE - SELAS.docx` ;
- `project/source_import/raw_drive_dump/Creation SELAS/SCM/Acte_cession_parts_SCM_SEL_modele.docx`.

Note : les chemins ci-dessus sont normalises sans accents pour la lisibilite. Les fichiers physiques peuvent contenir des accents decomposes.

## 3. Inventaire source de verite

Dans `Documents_a_generer_par_cas.docx`, le chemin SELARL prevoit, si cession SCM :
- PV cession de parts a la SCM -> `PV AGE cession part SCM.docx` ;
- courrier SDE -> `Courrier SDE.docx` ;
- acte de cession SCM vers SELARL -> `Acte de cession des parts de la SCM a la SELARL - transforme.docx`.

Le meme bloc source mentionne aussi `Acte de cession des parts de la SCM a la SELARL.docx`. Cette source non transformee n'est pas incluse dans le ticket et reste hors comparaison V1.

Dans le chemin SELAS, la source de verite prevoit, si SCM :
- PV AGE cession part SCM SELAS -> `PV AGE cession part SCM - SELAS.docx` ;
- courrier SDE SELAS -> `Courrier SDE - SELAS.docx` ;
- acte de cession des parts de la SCM vers SEL -> `Acte_cession_parts_SCM_SEL_modele.docx`.

## 4. Perimetre canonique du bloc

Le bloc canonique `SCM-CESSION-BLOCK` est un mini-batch de trois documents, selectionnable pour une structure cible SELARL ou SELAS lorsque le dossier contient une cession de parts de SCM vers la SEL.

Documents canoniques de travail :

| Identifiant de travail | Role | Sources SELARL | Sources SELAS |
|---|---|---|---|
| `SCM-CESSION-PV-AGE` | Decision collective SCM agreant le nouvel associe et modifiant la repartition statutaire | `PV AGE cession part SCM.docx` | `PV AGE cession part SCM - SELAS.docx` |
| `SCM-CESSION-COURRIER-SDE` | Courrier d'enregistrement fiscal des actes de cession | `Courrier SDE.docx` | `Courrier SDE - SELAS.docx` |
| `SCM-CESSION-ACTE-PARTS` | Acte contractuel de cession des parts de SCM au profit de la SEL | `Acte de cession des parts de la SCM a la SELARL - transforme.docx` | `Acte_cession_parts_SCM_SEL_modele.docx` |

Hors perimetre :
- statuts SCM ;
- satellites SCM de creation : pacte, liste de depenses, contrat frais communs, reglement interieur ;
- cession de cabinet medical ou dentaire ;
- acte de cession de parts SPFPL ;
- acte de cession d'actions SPFPL ;
- source SELARL non transformee mentionnee par la source de verite ;
- tout document marque a remplir a la main.

## 5. Comparaison canonique des six sources

### 5.1 Bloc commun SELARL / SELAS

Les trois paires de documents partagent la meme fonction metier :
- faire approuver l'entree de la SEL comme nouvel associe de la SCM ;
- modifier la repartition des parts de la SCM ;
- formaliser l'acte de cession des parts ;
- transmettre les actes au service d'enregistrement avec le montant des droits.

Le texte source montre un tronc commun fort :
- PV AGE : 58 lignes extraites pour SELARL et SELAS, structure identique hors deux differences textuelles ;
- courrier SDE : objet et corps de lettre communs ;
- acte : 79 lignes extraites pour chaque variante, plan identique et clauses principales communes.

### 5.2 Overlays SELARL

PV AGE SELARL :
- date de titre sous placeholder local `[date_du_jour]` ;
- premiere resolution avec agrement immediat "a compter de ce jour" ;
- aucun delai d'agrement ni date limite dans la source.

Courrier SDE SELARL :
- pas de bloc destinataire en tete ;
- nombre d'exemplaires fixe dans la source a `4 exemplaires` ;
- placeholders limites a lieu/date, montant des droits et signataire.

Acte SELARL :
- cessionnaire affichee comme `SELARL` fixe ;
- representant indique comme `gerant` fixe ;
- ordre professionnel du cedant fixe sur les chirurgiens-dentistes ;
- signature electronique fixe sur `Yousign` ;
- retard credit-vendeur fixe sur une majoration de `3 points` ;
- siege de la societe cedee source affiche avec `[adresse_siege_cessionnaire]`, anomalie probable a ne pas corriger sans validation.

### 5.3 Overlays SELAS

PV AGE SELAS :
- date de titre sous placeholder local `[date_pv]` ;
- premiere resolution ajoute `[delai_agrement]` et `[date_limite_agrement]`.

Courrier SDE SELAS :
- bloc destinataire en tete : service, centre des finances publiques, adresse, CP/ville ;
- nombre d'exemplaires variable via `[nombre_exemplaires]`.

Acte SELAS :
- profession ordinale du cedant variable via `[profession_reglementee_pluriel]` ;
- forme sociale du cessionnaire variable via `[forme_sociale_cessionnaire]` ;
- fonction du representant cessionnaire variable via `[fonction_representant_cessionnaire]` ;
- societe cedee variable via `[forme_sociale_societe_cedee]` et `[adresse_siege_societe_cedee]` ;
- majoration de retard variable via `[majoration_interet_retard]` ;
- prestataire de signature electronique variable via `[prestataire_signature_electronique]`.

Le texte SELAS contient aussi des formulations differentes ou degradations source, notamment `pleine-propriete [nb_parts_cedees] parts`, `convenues`, `reconnait`, et plusieurs unites non affichees autour du credit-vendeur. Ces ecarts sont des constats de source et ne doivent pas etre corriges automatiquement.

## 6. Roles metier des documents

### 6.1 `SCM-CESSION-PV-AGE`

Role :
- constater une assemblee generale extraordinaire de la SCM ;
- agreer la SEL comme nouvel associe ;
- modifier l'article 7 des statuts SCM pour la nouvelle repartition du capital ;
- donner pouvoirs pour les formalites.

Dependances metier :
- la SCM cedee existe ou est identifiee ;
- les associes presents ou representes sont connus ;
- le president de seance est connu ;
- la societe nouvel associe est identifiee ;
- la repartition avant/apres cession est fournie.

### 6.2 `SCM-CESSION-COURRIER-SDE`

Role :
- transmettre les exemplaires de l'acte de cession au service d'enregistrement ;
- annoncer le cheque correspondant aux droits d'enregistrement ;
- demander le retour des originaux chez Sydel.

Dependances metier :
- service d'enregistrement si la variante SELAS est retenue ou si le bloc destinataire est active ;
- nombre d'exemplaires si la variante SELAS est retenue ;
- montant des droits d'enregistrement ;
- signataire Sydel.

### 6.3 `SCM-CESSION-ACTE-PARTS`

Role :
- formaliser la cession des parts de la SCM entre le cedant et la SEL cessionnaire ;
- identifier la SCM cedee, les parts cedees, le prix et le paiement ;
- porter les declarations, formalites et signatures.

Dependances metier :
- cedant personne physique et conjoint le cas echeant ;
- SEL cessionnaire et representant ;
- SCM cedee ;
- associes de la SCM et repartition du capital ;
- parts cedees et prix ;
- paiement, credit-vendeur eventuel, signature electronique.

## 7. Variables canoniques

Les placeholders source restent des aliases documentaires. La verite cible est organisee par roles.

### 7.1 Dossier et selection

- `dossier.structure` : `SELARL` ou `SELAS`.
- `dossier.options.scm_cession`.
- `scm_cession.documents.pv_age`.
- `scm_cession.documents.courrier_sde`.
- `scm_cession.documents.acte_cession_parts`.
- `scm_cession.variante_structure` : `selarl` ou `selas`.

### 7.2 Societe cedee : SCM

Role canonique local : `scm_cedee`.

- `scm_cedee.denomination`
- `scm_cedee.forme_juridique`
- `scm_cedee.capital_social`
- `scm_cedee.siege.adresse_affichee`
- `scm_cedee.ville_rcs`
- `scm_cedee.numero_rcs`
- `scm_cedee.nb_parts_total`
- `scm_cedee.valeur_nominale_part`
- `scm_cedee.plage_parts_total`
- `scm_cedee.cogerants[]`

### 7.3 Societe nouvel associe / cessionnaire

Role canonique local : `cessionnaire`.

- `cessionnaire.denomination`
- `cessionnaire.forme_juridique`
- `cessionnaire.capital_social`
- `cessionnaire.siege.adresse_affichee`
- `cessionnaire.ville_rcs`
- `cessionnaire.representant.civilite_affichage`
- `cessionnaire.representant.civilite_courte`
- `cessionnaire.representant.prenom`
- `cessionnaire.representant.nom`
- `cessionnaire.representant.fonction`

Decision V1 :
- si le cedant est aussi representant de la SEL cessionnaire, ce lien doit etre explicite dans le contexte ;
- le moteur ne doit pas copier silencieusement les champs `cedant` vers `cessionnaire.representant`.

### 7.4 Cedant et conjoint

Role canonique local : `cedant`.

- `cedant.civilite_affichage`
- `cedant.prenom`
- `cedant.nom`
- `cedant.profession`
- `cedant.date_naissance`
- `cedant.ville_naissance`
- `cedant.departement_naissance`
- `cedant.nationalite`
- `cedant.adresse_affichee`
- `cedant.situation_maritale`
- `cedant.ordre.departemental`
- `cedant.ordre.numero`
- `cedant.numero_rpps`

Role canonique local : `cedant.conjoint`.

- `cedant.conjoint.civilite_affichage`
- `cedant.conjoint.prenom`
- `cedant.conjoint.nom`

### 7.5 Associes SCM avant/apres cession

Roles canoniques locaux :
- `scm_cession.associes_presents[]` pour les associes participant au PV ;
- `scm_cession.associes_avant_cession[]` pour l'origine de propriete dans l'acte ;
- `scm_cession.associes_apres_cession[]` pour la nouvelle repartition de l'article 7.

Variables par associe personne physique :
- `civilite_affichage`
- `prenom`
- `nom`
- `parts.nb`
- `parts.plage`
- `role_pv` : par exemple president de seance, associe present, gerant associe.

Variables par associe personne morale :
- `denomination`
- `forme_juridique`
- `parts.nb`
- `parts.plage`

Decision V1 :
- les aliases `personne_1`, `personne_2`, `personne_3`, `personne_4` ne sont pas des roles canoniques ;
- la source PV melange associes presents, president de seance et repartition apres cession ; un contexte futur doit mapper explicitement les roles ;
- toute repartition de parts doit etre fournie par associe et controlee contre `scm_cedee.nb_parts_total`.

### 7.6 Agrement, cession et prix

Role canonique local : `scm_cession.agrement`.

- `scm_cession.agrement.date_pv`
- `scm_cession.agrement.date_pv_lettres`
- `scm_cession.agrement.delai_mois`
- `scm_cession.agrement.date_limite`

Role canonique local : `scm_cession.parts_cedees`.

- `scm_cession.parts_cedees.nb`
- `scm_cession.parts_cedees.plage`
- `scm_cession.prix.unitaire_lettres`
- `scm_cession.prix.unitaire`
- `scm_cession.prix.global_lettres`
- `scm_cession.prix.global`
- `scm_cession.paiement.mode`
- `scm_cession.credit_vendeur.actif`
- `scm_cession.credit_vendeur.montant`
- `scm_cession.credit_vendeur.duree`
- `scm_cession.credit_vendeur.taux`
- `scm_cession.credit_vendeur.majoration_interet_retard`

Decision V1 :
- la ligne source `Ajouter en cas de CV` est une instruction documentaire, pas un texte fixe a rendre sans condition ;
- le credit-vendeur doit etre soit explicitement active avec donnees completes, soit exclu du rendu avec validation texte.

### 7.7 Enregistrement et signature

Role canonique local : `enregistrement`.

- `enregistrement.service`
- `enregistrement.centre_finances_publiques`
- `enregistrement.adresse_service`
- `enregistrement.cp_ville_service`
- `enregistrement.nombre_exemplaires`
- `enregistrement.montant_droits`

Role canonique : `signature`.

- `signature.lieu`
- `signature.date`
- `signature.nombre_exemplaires_lettres`
- `signature.prestataire_electronique`
- `signature.signataire_sde.prenom`
- `signature.signataire_sde.nom`

## 8. Mapping placeholders source

### 8.1 PV AGE cession SCM

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `scm_cedee.denomination` | SCM |
| `[capital_social]` | `scm_cedee.capital_social` | SCM |
| `[adresse_siege]` | `scm_cedee.siege.adresse_affichee` | SCM |
| `[ville_rcs]` | `scm_cedee.ville_rcs` | SCM |
| `[numero_rcs]` | `scm_cedee.numero_rcs` | SCM |
| `[date_du_jour]` | `scm_cession.agrement.date_pv` | alias SELARL |
| `[date_pv]` | `scm_cession.agrement.date_pv` | alias SELAS |
| `[date_pv_lettres]` | `scm_cession.agrement.date_pv_lettres` | commun |
| `[nb_parts_total]` | `scm_cedee.nb_parts_total` | controle somme |
| `[valeur_nominale_part]` | `scm_cedee.valeur_nominale_part` | commun |
| `[plage_parts_total]` | `scm_cedee.plage_parts_total` | commun |
| `[civilite_personne_1]`, `[prenom_personne_1]`, `[nom_personne_1]` | `scm_cession.associes_presents[0]` et/ou `scm_cession.associes_apres_cession[]` | role a mapper |
| `[civilite_personne_2]`, `[prenom_personne_2]`, `[nom_personne_2]` | `scm_cession.associes_presents[1]` et/ou `scm_cession.associes_apres_cession[]` | role a mapper |
| `[civilite_personne_3]`, `[prenom_personne_3]`, `[nom_personne_3]` | `scm_cession.president_seance` ou `scm_cession.associes_presents[2]` | source preside la seance |
| `[civilite_personne_4]`, `[prenom_personne_4]`, `[nom_personne_4]` | `scm_cession.associes_apres_cession[]` | role absent des presents |
| `[parts_personne_1]` a `[parts_personne_4]` | `scm_cession.associes_apres_cession[].parts.nb` | par associe |
| `[plage_parts_personne_1]`, `[plage_parts_personne_2]`, `[plage_parts_personne_4]` | `scm_cession.associes_apres_cession[].parts.plage` | par associe |
| `[denomination_societe_nouvel_associe]` | `cessionnaire.denomination` | nouvel associe personne morale |
| `[plage_parts_societe_nouvel_associe]` | `cessionnaire.parts.plage` | parts nouvel associe |
| `[delai_agrement]` | `scm_cession.agrement.delai_mois` | SELAS uniquement |
| `[date_limite_agrement]` | `scm_cession.agrement.date_limite` | SELAS uniquement |

### 8.2 Courrier SDE

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[service_enregistrement]` | `enregistrement.service` | SELAS uniquement |
| `[centre_finances_publiques]` | `enregistrement.centre_finances_publiques` | SELAS uniquement |
| `[adresse_service_enregistrement]` | `enregistrement.adresse_service` | SELAS uniquement |
| `[cp_ville_service_enregistrement]` | `enregistrement.cp_ville_service` | SELAS uniquement |
| `[lieu_signature]` | `signature.lieu` | commun |
| `[date_signature]` | `signature.date` | commun |
| `[nombre_exemplaires]` | `enregistrement.nombre_exemplaires` | SELAS ; SELARL source fixe 4 |
| `[montant_droits_enregistrement]` | `enregistrement.montant_droits` | commun |
| `[prenom_signataire]` | `signature.signataire_sde.prenom` | commun |
| `[nom_signataire]` | `signature.signataire_sde.nom` | commun |

### 8.3 Acte de cession des parts SCM

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[civilite_cedant]`, `[prenom_cedant]`, `[nom_cedant]` | `cedant.civilite_affichage`, `cedant.prenom`, `cedant.nom` | cedant personne physique |
| `[profession_cedant]` | `cedant.profession` | commun |
| `[profession_reglementee_pluriel]` | `cedant.profession_reglementee_pluriel` | SELAS ; SELARL fixe chirurgiens-dentistes |
| `[date_naissance_cedant]`, `[ville_naissance_cedant]`, `[departement_naissance_cedant]` | `cedant.date_naissance`, `cedant.ville_naissance`, `cedant.departement_naissance` | commun |
| `[nationalite_cedant]` | `cedant.nationalite` | commun |
| `[adresse_cedant]` | `cedant.adresse_affichee` | commun |
| `[situation_maritale_cedant]` | `cedant.situation_maritale` | commun |
| `[civilite_conjoint_cedant]`, `[prenom_conjoint_cedant]`, `[nom_conjoint_cedant]` | `cedant.conjoint.*` | commun |
| `[ordre_departemental_cedant]`, `[numero_ordre_cedant]`, `[numero_rpps_cedant]` | `cedant.ordre.*`, `cedant.numero_rpps` | commun |
| `[denomination_societe_cessionnaire]` | `cessionnaire.denomination` | SEL cessionnaire |
| `[forme_sociale_cessionnaire]` | `cessionnaire.forme_juridique` | SELAS ; SELARL fixe `SELARL` |
| `[capital_social_cessionnaire]` | `cessionnaire.capital_social` | commun |
| `[adresse_siege_cessionnaire]` | `cessionnaire.siege.adresse_affichee` | commun |
| `[ville_rcs_cessionnaire]` | `cessionnaire.ville_rcs` | commun |
| `[fonction_representant_cessionnaire]` | `cessionnaire.representant.fonction` | SELAS ; SELARL fixe `gerant` |
| `[civilite_representant_cessionnaire_courte]`, `[prenom_representant_cessionnaire]`, `[nom_representant_cessionnaire]` | `cessionnaire.representant.*` | signature acte |
| `[denomination_societe_cedee]` | `scm_cedee.denomination` | SCM cedee |
| `[forme_sociale_societe_cedee]` | `scm_cedee.forme_juridique` | SELAS ; SELARL fixe Societe Civile de Moyens |
| `[capital_social_societe_cedee]` | `scm_cedee.capital_social` | commun |
| `[adresse_siege_societe_cedee]` | `scm_cedee.siege.adresse_affichee` | SELAS |
| `[ville_rcs_societe_cedee]`, `[numero_rcs_societe_cedee]` | `scm_cedee.ville_rcs`, `scm_cedee.numero_rcs` | commun |
| `[nb_parts_total_societe_cedee]` | `scm_cedee.nb_parts_total` | commun |
| `[civilite_associe_societe_cedee_1]`, `[prenom_associe_societe_cedee_1]`, `[nom_associe_societe_cedee_1]` | `scm_cession.associes_avant_cession[0]` | role a mapper |
| `[civilite_associe_societe_cedee_3]`, `[prenom_associe_societe_cedee_3]`, `[nom_associe_societe_cedee_3]` | `scm_cession.associes_avant_cession[2]` | role a mapper |
| `[parts_associe_societe_cedee_1]` | `scm_cession.associes_avant_cession[].parts.nb` | SELAS source repete l'alias, blocage si non detaille |
| `[nb_parts_cedees]` | `scm_cession.parts_cedees.nb` | commun |
| `[plage_parts_cedees]` | `scm_cession.parts_cedees.plage` | commun |
| `[prix_unitaire_part_lettres]`, `[prix_unitaire_part]` | `scm_cession.prix.unitaire_lettres`, `scm_cession.prix.unitaire` | commun |
| `[prix_global_parts_lettres]`, `[prix_global_parts]` | `scm_cession.prix.global_lettres`, `scm_cession.prix.global` | commun |
| `[montant_credit_vendeur]`, `[duree_credit_vendeur]`, `[taux_credit_vendeur]` | `scm_cession.credit_vendeur.*` | conditionnel |
| `[majoration_interet_retard]` | `scm_cession.credit_vendeur.majoration_interet_retard` | SELAS ; SELARL fixe 3 points |
| `[prestataire_signature_electronique]` | `signature.prestataire_electronique` | SELAS ; SELARL fixe Yousign |
| `[lieu_signature]` | `signature.lieu` | commun |
| `[nombre_exemplaires_lettres]` | `signature.nombre_exemplaires_lettres` | commun |

## 9. Conditions de selection futures

Condition commune minimale :
- `dossier.options.scm_cession == true` ;
- `dossier.structure in {"SELARL", "SELAS"}`.

Selection recommandee :
- produire les trois documents ensemble, sauf decision metier explicite ;
- utiliser l'overlay SELARL pour `dossier.structure == SELARL` ;
- utiliser l'overlay SELAS pour `dossier.structure == SELAS`.

Blocages de selection :
- bloquer si les sources de travail ne sont pas placees ou referencees de maniere stable avant code ;
- bloquer si la cession SCM est confondue avec une cession de cabinet ou une cession SPFPL ;
- bloquer si le dossier necessite une autre forme de cessionnaire ;
- bloquer si les roles `personne_1` a `personne_4` ne sont pas mappes explicitement ;
- bloquer si la repartition des parts avant/apres cession n'est pas coherent avec le total de parts.

## 10. Elements manuels

Elements a fournir par contexte dossier, saisie controlee ou arbitrage :
- activation du bloc cession SCM ;
- choix SELARL / SELAS ;
- confirmation de la source acte SELARL transformee ou non transformee ;
- date du PV et date en lettres ;
- delai et date limite d'agrement si l'overlay SELAS est retenu ;
- identite et role des associes SCM avant/apres cession ;
- president de seance ;
- cogestion de la SCM cedee ;
- representant de la SEL cessionnaire ;
- conjoint du cedant et situation maritale ;
- donnees ordinales et RPPS du cedant ;
- nombre, plage et prix des parts cedees ;
- paiement par pret bancaire et credit-vendeur eventuel ;
- montant des droits d'enregistrement ;
- service d'enregistrement et nombre d'exemplaires si applicable ;
- lieu/date de signature et prestataire de signature electronique ;
- nombre d'exemplaires originaux en lettres.

Le moteur ne doit pas inventer ces valeurs.

## 11. Points ouverts et blocages avant code

1. **Placement des sources** : les six sources ont ete lues dans le raw dump local, mais ne sont pas placees dans `project/source_documents/lot_05/` sur la branche de travail.
2. **Source SELARL non transformee** : la source de verite mentionne aussi `Acte de cession des parts de la SCM a la SELARL.docx`; confirmer si elle doit etre ignoree, comparee ou remplacer la source transformee.
3. **Roles PV `personne_1` a `personne_4`** : la source PV distingue mal associes presents, president de seance, cedant sortant et repartition apres cession.
4. **Repartition des parts dans l'acte** : les deux actes repetent un placeholder de parts sur plusieurs lignes d'associes ; un futur code doit exiger une valeur par associe.
5. **Siege de la SCM cedee en SELARL** : l'acte SELARL utilise `[adresse_siege_cessionnaire]` dans la description de la SCM cedee ; correction interdite sans validation.
6. **Representant cessionnaire** : l'acte SELARL utilise les donnees du cedant dans la phrase de representation ; confirmer si le cedant est aussi representant de la SEL.
7. **Credit-vendeur** : la ligne source `Ajouter en cas de CV` doit devenir un bloc conditionnel ou rester manuel ; ne pas la rendre brute sans arbitrage.
8. **Overlay d'agrement SELAS** : confirmer si le delai/date limite doit aussi exister pour SELARL ou rester specifique SELAS.
9. **Courrier SDE** : confirmer si le bloc destinataire et le nombre d'exemplaires variable SELAS doivent etre generalises a SELARL.
10. **Ecarts de wording SELAS** : plusieurs formulations SELAS paraissent anormales ; aucune correction ne doit etre appliquee sans note de validation.
11. **Date de l'acte** : l'acte contient `Le` sans placeholder de date ; confirmer si la date reste manuelle ou doit devenir `signature.date`.

## 12. Statut

`SPEC-SCM-CESSION-BLOCK-001` stabilise la spec canonique V1 du bloc cession SCM, sans code Python et sans modification des fichiers de pilotage.

La prochaine etape recommandee est un arbitrage metier cible sur les points ouverts 1 a 11 avant tout ticket de code.
