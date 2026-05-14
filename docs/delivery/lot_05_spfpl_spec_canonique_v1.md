# DAAT x SYDEL - SPEC CANONIQUE V1
## Batch SPFPL specifique

## 1. Objet

Formaliser le batch documentaire SPFPL specifique avant tout codage.

Cette spec couvre uniquement les documents SPFPL non deja traites par les lots transverses :
- note d'information ;
- PV d'agrement de cession SPFPL, variante SELARL avec associe unique ;
- PV d'agrement de cession SPFPL, variante SELARL avec plusieurs associes ;
- acte de cession de parts ;
- contrat d'apport SEL vers SPFPL ;
- attestation sur le capital / liste des souscripteurs ;
- acte de designation du commissaire aux apports.

Cette spec ne code rien, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partage.

Document explicitement non specifie :
- acte de cession d'actions, faute de source DOCX confirmee.

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

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Constat de placement :
- `project/source_documents/lot_05/` contient seulement un README ;
- les sources SPFPL analysees viennent donc de `project/source_import/raw_drive_dump/`.

Sources SPFPL lues :
- `project/source_import/raw_drive_dump/Creation SPFPL/NOTE D_INFORMATION.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/Documents de base/Note d_information.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/Documents de base/Copie de Note d_information.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/PV agrement cession/PV SELARL agrement cession SPFPL - SELARL plusieurs associes - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/PV agrement cession/PV SELARL agrement cession SPFPL - SELARL 1 associe.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/Cession/Acte_cession_SPFPL_tiers_part_modele.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/apport doc/Contrat d_apport SEL SPFPL.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/apport doc/Attestation sur le capital - apport - liste des souscripteurs.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/apport doc/attestation nomination commissaire aux apports - transforme.docx`

Variantes ou doublons consultes a titre de controle :
- `project/source_import/raw_drive_dump/Creation SPFPL/Attestation sur le capital - apport - liste des souscripteurs - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession + apport/apport doc/Copie de Contrat d_apport SEL SPFPL - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession + apport/apport doc/Copie de attestation nomination commissaire aux apports - transforme.docx`

Notes de source :
- la source demandee `PV SELARL agrement cession SPFPL - SELARL 1 associe - transforme.docx` n'a pas ete trouvee sous ce nom exact ; le fichier disponible et lu est `PV SELARL agrement cession SPFPL - SELARL 1 associe.docx` ;
- la source de verite mentionne `Attestation nomination comm. aux comptes`, mais le fichier source disponible porte sur un commissaire aux apports ;
- les trois notes d'information lues ont le meme contenu visible ;
- des variantes `- transforme` existent pour certains documents d'apport et parametrent davantage l'evaluateur ou les commissaires, mais elles ne remplacent pas automatiquement les sources nommees ci-dessus.

## 3. Perimetre documentaire V1

La source de verite distingue deux chemins SPFPL :
- `SPFPL cession` ;
- `SPFPL apport`.

Documents hors perimetre de cette spec :
- documents universels deja couverts par le tronc commun ;
- statuts SPFPL ;
- PV nomination gerant ;
- demande d'inscription a l'ordre ;
- batch regime communautaire deja specifie separement ;
- acte de cession d'actions, tant que la source n'est pas confirmee.

Conditions de selection de travail :
- `dossier.structure == SPFPL_CESSION` pour le sous-batch cession ;
- `dossier.structure == SPFPL_APPORT` pour le sous-batch apport ;
- `dossier.options.cession == true` pour les documents de cession ;
- `dossier.options.apport == true` pour les documents d'apport.

Identifiants de travail proposes pour la future implementation, sans attribution catalogue definitive dans cette spec :

| Identifiant de travail | Document canonique | Chemin |
|---|---|---|
| `SPFPL-NOTE-INFORMATION` | Note d'information | cession et apport |
| `SPFPL-PV-AGREMENT-UNIQUE` | PV agrement cession SPFPL - SELARL 1 associe | cession |
| `SPFPL-PV-AGREMENT-PLURIEL` | PV agrement cession SPFPL - SELARL plusieurs associes | cession |
| `SPFPL-ACTE-CESSION-PARTS` | Acte de cession de parts | cession |
| `SPFPL-CONTRAT-APPORT` | Contrat d'apport SEL SPFPL | apport |
| `SPFPL-ATTESTATION-CAPITAL` | Attestation sur le capital / liste des souscripteurs | apport |
| `SPFPL-DESIGNATION-CAA` | Acte de designation d'un commissaire aux apports | apport |

## 4. Cycle documentaire

| Document | Inventorie | Source recue | Analyse | Specifie | Pret a coder |
|---|---:|---:|---:|---:|---:|
| Note d'information | oui | oui | oui | oui | oui, sous reserve du wording cession/apport |
| PV agrement 1 associe | oui | oui, nom exact divergent | oui | oui | non, arbitrage wording requis |
| PV agrement plusieurs associes | oui | oui | oui | oui | non, arbitrage wording requis |
| Acte de cession de parts | oui | oui | oui | oui | oui, sous reserve de la liste dynamique des associes |
| Contrat d'apport | oui | oui | oui | oui | non, arbitrage evaluateur/commissaire requis |
| Attestation capital / liste souscripteurs | oui | oui | oui | oui | non, arbitrage associe unique vs liste dynamique requis |
| Designation commissaire aux apports | oui | oui | oui | oui | non, choix commissaire requis |
| Acte de cession d'actions | oui | non confirme | non | non | non |

## 5. Variables canoniques communes

Les placeholders sources ne doivent pas devenir la verite canonique du moteur. Les nouveaux roles ci-dessous sont des propositions de spec pour le batch SPFPL ; leur integration eventuelle dans le dictionnaire canonique devra faire l'objet d'un ticket dedie si necessaire.

### 5.1 Dossier et operation

- `dossier.structure`
- `dossier.options.cession`
- `dossier.options.apport`
- `dossier.options.associe_unique`
- `operation_spfpl.type` : `cession` ou `apport`

Regles :
- `operation_spfpl.type == cession` pilote les documents de cession ;
- `operation_spfpl.type == apport` pilote les documents d'apport ;
- si le contexte demande simultanement cession et apport, le moteur devra selectionner explicitement les deux sous-batchs ou bloquer selon l'arbitrage du ticket code.

### 5.2 Societe SPFPL en constitution

Role canonique :
- `societe_spfpl`

Variables :
- `societe_spfpl.denomination`
- `societe_spfpl.forme_sociale`
- `societe_spfpl.forme_sociale_abregee`
- `societe_spfpl.capital_social`
- `societe_spfpl.activite`
- `societe_spfpl.ville_rcs`
- `societe_spfpl.siege.adresse_affichee`
- `societe_spfpl.siege.num_voie`
- `societe_spfpl.siege.voie`
- `societe_spfpl.siege.cp`
- `societe_spfpl.siege.ville`
- `societe_spfpl.dirigeant.fonction`

Aliases sources principaux :
- `[denomination_societe]`
- `[denomination_societe_cessionnaire]`
- `[forme_sociale]`
- `[forme_sociale_acquereur]`
- `[capital_social]`
- `[capital_social_cessionnaire]`
- `[adresse_siege]`
- `[adresse_siege_cessionnaire]`
- `[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]`
- `[ville_rcs]`, `[ville_rcs_cessionnaire]`
- `[fonction_dirigeant]`

### 5.3 Personne principale

Deux roles doivent rester distincts :
- `cedant` pour le sous-batch cession ;
- `apporteur` pour le sous-batch apport.

Variables communes :
- `*.civilite_affichage`
- `*.genre`
- `*.prenom`
- `*.nom`
- `*.profession`
- `*.profession_reglementee`
- `*.date_naissance`
- `*.ville_naissance`
- `*.departement_naissance`
- `*.nationalite`
- `*.situation_maritale`
- `*.conjoint.civilite_affichage`
- `*.conjoint.prenom`
- `*.conjoint.nom`
- `*.adresse_personnelle.adresse_affichee`
- `*.adresse_personnelle.num_voie`
- `*.adresse_personnelle.voie`
- `*.adresse_personnelle.cp`
- `*.adresse_personnelle.ville`
- `*.ordre.departemental`
- `*.ordre.numero`
- `*.ordre.numero_rpps`

Aliases sources cession :
- `[civilite_cedant]`, `[prenom_cedant]`, `[nom_cedant]`
- `[profession_cedant]`
- `[date_naissance_cedant]`, `[ville_naissance_cedant]`, `[departement_naissance_cedant]`
- `[nationalite_cedant]`
- `[adresse_cedant]`
- `[situation_maritale_cedant]`
- `[civilite_conjoint_cedant]`, `[prenom_conjoint_cedant]`, `[nom_conjoint_cedant]`
- `[ordre_departemental_cedant]`, `[numero_rpps_cedant]`

Aliases sources apport :
- `[civilite]`, `[prenom]`, `[nom]`
- `[date_naissance]`, `[ville_naissance]`, `[departement_naissance]`
- `[nationalite]`
- `[num_voie_perso]`, `[voie_perso]`, `[cp_perso]`, `[ville_perso]`
- `[situation_maritale]`, `[nom_conjoint]`
- `[ordre_professionnel]`, `[departement_ordre]`, `[numero_ordre]`, `[numero_rpps]`

### 5.4 Societe cible / apportee / cedee

Role canonique :
- `societe_cible`

Ce role represente la SEL / societe professionnelle dont les titres sont cedes ou apportes a la SPFPL.

Variables :
- `societe_cible.denomination`
- `societe_cible.forme_sociale`
- `societe_cible.forme_sociale_complete`
- `societe_cible.profession_reglementee`
- `societe_cible.profession_reglementee_pluriel`
- `societe_cible.capital_social`
- `societe_cible.capital_social_lettres`
- `societe_cible.nb_parts_total`
- `societe_cible.valeur_nominale_part`
- `societe_cible.valeur_nominale_part_lettres`
- `societe_cible.siege.adresse_affichee`
- `societe_cible.ville_rcs`
- `societe_cible.numero_rcs`
- `societe_cible.departement_inscription_ordre`
- `societe_cible.dirigeant.civilite_affichage`
- `societe_cible.dirigeant.prenom`
- `societe_cible.dirigeant.nom`
- `societe_cible.dirigeant.fonction`

Aliases sources :
- `[denomination_societe_cedee]`
- `[denomination_societe_apportee]`
- `[forme_sociale_societe_cedee]`
- `[forme_sociale_societe_apportee]`
- `[forme_sociale_complete]`
- `[capital_social_societe_cedee]`
- `[capital_social_societe_apportee]`
- `[capital_lettres_societe_apportee]`
- `[nb_parts_total_societe_cedee]`
- `[nb_parts_total_societe_apportee]`
- `[valeur_nominale_part]`
- `[valeur_nominale_part_lettres]`
- `[adresse_siege_societe_cedee]`
- `[adresse_siege_societe_apportee]`
- `[ville_rcs_societe_cedee]`
- `[ville_rcs_societe_apportee]`
- `[numero_rcs_societe_cedee]`
- `[numero_rcs_societe_apportee]`

### 5.5 Associes de la societe cible

Role canonique :
- `associes_cible[]`

Variables par associe :
- `type` : `personne_physique` ou `personne_morale`
- `civilite_affichage`
- `prenom`
- `nom`
- `denomination`
- `nb_parts_avant`
- `nb_parts_apres`
- `plage_parts`
- `numero_part_unique`
- `qualite`

Regle canonique :
- les placeholders locaux `personne_2`, `personne_3`, `societe_associe_1` et lignes fixes de repartition ne doivent pas etre codes comme structure definitive ;
- les listes de capital doivent etre generees depuis `associes_cible[]` avec une entree SPFPL ajoutee ou mise a jour apres cession/apport.

Aliases sources observes :
- `[prenom_personne_2]`, `[nom_personne_2]`, `[nb_parts_personne_2]`, `[numero_part_personne_2]`
- `[prenom_personne_3]`, `[nom_personne_3]`, `[parts_personne_3]`
- `[denomination_societe_associe_1]`, `[nb_parts_societe_associe_1]`, `[plage_parts_societe_associe_1]`
- `[nb_parts_apporteur_avant]`, `[nb_parts_apporteur_apres]`, `[numero_part_apporteur_apres]`
- `[parts_personne_1]`, `[parts_personne_2]`, `[parts_personne_3]`

### 5.6 Cession de parts

Role canonique :
- `cession_parts`

Variables :
- `cession_parts.nb_parts`
- `cession_parts.nb_parts_lettres`
- `cession_parts.plage_parts`
- `cession_parts.prix_unitaire`
- `cession_parts.prix_unitaire_lettres`
- `cession_parts.prix_total`
- `cession_parts.prix_total_lettres`
- `cession_parts.date_realisation`
- `cession_parts.nombre_exemplaires_lettres`

Aliases sources :
- `[nb_parts_cedees]`
- `[nb_parts_cedees_lettres]`
- `[plage_parts_cedees]` si source confirmee ulterieurement
- `[prix_unitaire_part]`
- `[prix_unitaire_part_lettres]`
- `[prix_cession]`
- `[prix_cession_lettres]`
- `[nombre_exemplaires_lettres]`

### 5.7 Apport de titres

Role canonique :
- `apport_titres`

Variables :
- `apport_titres.nb_parts`
- `apport_titres.nb_parts_lettres`
- `apport_titres.plage_parts`
- `apport_titres.nature_titres` : `parts sociales` ou `actions`
- `apport_titres.valeur_par_titre`
- `apport_titres.valeur_par_titre_lettres`
- `apport_titres.valeur_globale`
- `apport_titres.valeur_globale_lettres`
- `apport_titres.nb_actions_attribuees`
- `apport_titres.nb_actions_attribuees_lettres`
- `apport_titres.valeur_nominale_action`
- `apport_titres.valeur_nominale_action_lettres`

Aliases sources :
- `[nb_parts_apportees]`
- `[nb_parts_apportees_lettres]`
- `[plage_parts_apportees]`
- `[parts_sociales_ou_actions]`
- `[valeur_apport_par_part]`
- `[valeur_apport_par_part_lettres]`
- `[valeur_apport_global]`
- `[valeur_apport_global_lettres]`
- `[nb_actions]`
- `[nb_actions_lettres]`
- `[valeur_nominale_action_lettres]`

### 5.8 Reunion / PV d'agrement

Role canonique :
- `reunion`

Variables :
- `reunion.date_pv`
- `reunion.annee_pv_lettres`
- `reunion.date_reunion_lettres`
- `reunion.heure_reunion`
- `reunion.president.civilite_affichage`
- `reunion.president.prenom`
- `reunion.president.nom`
- `reunion.president.qualite`

Aliases sources :
- `[date_pv]`
- `[annee_pv_lettres]`
- `[date_reunion_lettres]`
- `[heure_reunion]`
- `[qualite_associe]`

### 5.9 Capital / liste des souscripteurs

Role canonique :
- `capital_souscription`

Variables :
- `capital_souscription.nb_actions_total`
- `capital_souscription.valeur_nominale_action`
- `capital_souscription.apports_nature_montant`
- `capital_souscription.apports_numeraire_montant`
- `capital_souscription.souscripteurs[]`

Variables par souscripteur :
- `civilite_affichage`
- `prenom`
- `nom`
- `profession`
- `adresse_personnelle_affichee`
- `nb_actions`
- `qualite`

Aliases sources :
- `[nb_actions]`
- `[valeur_nominale_part]`
- `[montant_apports_nature]`
- `[montant_apports_numeraire]`
- `[adresse_personnelle]`
- `[profession]`

Decision V1 :
- la source disponible de l'attestation capital / liste des souscripteurs ne couvre explicitement qu'un actionnaire unique ;
- la generation d'une liste dynamique de souscripteurs reste un point ouvert avant code.

### 5.10 Evaluateur et commissaire aux apports

Roles canoniques :
- `evaluateur_apport`
- `commissaire_aux_apports`

Variables evaluateur :
- `evaluateur_apport.denomination`
- `evaluateur_apport.forme_sociale`
- `evaluateur_apport.capital_social`
- `evaluateur_apport.siege.adresse_affichee`
- `evaluateur_apport.ville_rcs`
- `evaluateur_apport.numero_rcs`
- `evaluateur_apport.representant.civilite_affichage`
- `evaluateur_apport.representant.prenom`
- `evaluateur_apport.representant.nom`

Variables commissaire :
- `commissaire_aux_apports.denomination`
- `commissaire_aux_apports.forme_sociale`
- `commissaire_aux_apports.capital_social`
- `commissaire_aux_apports.siege.adresse_affichee`
- `commissaire_aux_apports.ville_rcs`
- `commissaire_aux_apports.numero_rcs`
- `commissaire_aux_apports.representant.civilite_affichage`
- `commissaire_aux_apports.representant.prenom`
- `commissaire_aux_apports.representant.nom`

Decision V1 :
- les sources avec `OU` ne doivent pas etre rendues telles quelles ;
- le futur contexte doit fournir un commissaire selectionne ;
- si aucun commissaire n'est selectionne, la generation doit bloquer.

## 6. Sous-familles documentaires

### 6.1 Note d'information

Role :
- informer sur la constitution de la SPFPL et l'acquisition ou l'apport de titres de la societe cible.

Chemins :
- SPFPL cession ;
- SPFPL apport.

Structure source :
- titre ;
- constitution de la societe ;
- paragraphe de presentation de la SPFPL ;
- presentation de la societe cible ;
- decomposition du capital apres operation ;
- signature du dirigeant.

Blocs conditionnels :
- `operation_spfpl.type == cession` : le wording source `acquerir/de recevoir en apport en nature` doit etre arbitre vers un wording cession, sans conserver la double formule ;
- `operation_spfpl.type == apport` : meme point, vers un wording apport ;
- la decomposition du capital apres operation doit etre construite depuis les parts restantes de l'apporteur / cedant et les parts detenues par la SPFPL.

Point sensible :
- la source contient une double formulation cession/apport ; aucune generation ne doit conserver cette double formulation sans validation.

### 6.2 PV agrement cession - SELARL 1 associe

Role :
- decision de l'associe unique de la societe cible pour agreer la SPFPL comme nouvelle associee et modifier les statuts.

Structure source :
- en-tete societe cible ;
- titre `PROCES-VERBAL DE L'ASSOCIE UNIQUE` ;
- date de decision ;
- identification de l'associe unique ;
- ordre du jour ;
- trois resolutions ;
- signature de l'associe unique.

Blocs conditionnels :
- selection si `dossier.options.associe_unique == true` ;
- article 7 bis a generer depuis la repartition capital apres operation ;
- signatures limitees a l'associe unique dans la source.

Point sensible :
- le fichier disponible n'a pas le suffixe `- transforme` demande ;
- le texte source parle d'`apport` et de `parts apportees`, alors que le referentiel classe le document dans `SPFPL cession` et le nomme `agrement cession`.

### 6.3 PV agrement cession - SELARL plusieurs associes

Role :
- assemblee generale extraordinaire de la societe cible pour agreer la SPFPL comme nouvelle associee et modifier les statuts.

Structure source :
- en-tete societe cible ;
- titre `PROCES-VERBAL DE L'ASSEMBLEE GENERALE EXTRAORDINAIRE` ;
- convocation et reunion ;
- liste des associes presents ou representes ;
- depot des documents ;
- ordre du jour ;
- trois resolutions ;
- signatures de tous les associes.

Blocs conditionnels :
- selection si `dossier.options.associe_unique == false` ;
- liste des presents ou representes depuis `associes_cible[]` ;
- verifications de quorum/totalite : la source indique que les associes presents disposent de la totalite des parts ;
- article 7 bis a generer depuis la repartition capital apres operation ;
- signatures de tous les associes presents ou representes.

Point sensible :
- comme la variante associe unique, la source parle d'`apport` et de `contrat d'apport` dans un dossier nomme `PV agrement cession`.

### 6.4 Acte de cession de parts

Role :
- formaliser la cession de parts de la societe cible par le cedant a la SPFPL cessionnaire.

Structure source :
- titre `Cession de parts` ;
- identification du cedant ;
- identification de la SPFPL cessionnaire ;
- expose relatif a la societe cible ;
- origine de propriete ;
- objet du contrat ;
- nantissement / pacte / agrement ;
- propriete et jouissance ;
- prix et modalites de paiement ;
- declarations des parties ;
- garantie d'actif et de passif ;
- clauses generales ;
- signification de la cession ;
- enregistrement ;
- communication au Conseil de l'Ordre ;
- frais ;
- signature electronique ;
- signatures.

Blocs conditionnels :
- liste de repartition du capital actuel depuis `associes_cible[]` ;
- prix de cession depuis `cession_parts` ;
- conjoint du cedant selon les donnees matrimoniales source ;
- nombre d'exemplaires.

Points sensibles :
- la source est un acte de cession de parts, pas d'actions ;
- une phrase de frais mentionne `cession d'action` dans l'acte de cession de parts source ; ce wording doit etre relu avant toute correction ou automatisation ;
- la repartition du capital source est fixee sur trois personnes et devra etre rendue dynamique avant code.

### 6.5 Contrat d'apport SEL SPFPL

Role :
- formaliser l'apport par l'apporteur a la SPFPL de titres de la societe cible.

Structure source :
- titre `Contrat d'apport` ;
- identification de l'apporteur ;
- identification de la SPFPL beneficiaire ;
- expose ;
- biens apportes ;
- evaluation de l'apport ;
- remuneration de l'apport ;
- option pour le report d'imposition ;
- conditions suspensives ;
- affirmation de sincerite ;
- frais ;
- election de domicile ;
- date d'effet ;
- signature electronique ;
- signatures.

Blocs conditionnels :
- nature des titres : `parts sociales` ou `actions` ;
- nombre et plage des titres apportes ;
- evaluateur de l'apport ;
- commissaire aux apports ;
- conditions suspensives ordre / immatriculation.

Points sensibles :
- la source nommee contient des entites fixes pour l'evaluation et le commissaire ;
- une variante `Copie de Contrat d_apport SEL SPFPL - transforme.docx` parametre l'evaluateur et les commissaires ;
- le futur code doit choisir une seule source canonique ou un mode de parametrage explicite avant implementation.

### 6.6 Attestation sur le capital / liste des souscripteurs

Role :
- attester la repartition du capital de la SPFPL et la souscription des actions, incluant les apports en nature et en numeraire.

Structure source :
- en-tete SPFPL ;
- titre `ATTESTATION` ;
- sous-titre `Liste des souscripteurs` ;
- attestation du president ;
- capital social ;
- nombre d'actions et valeur nominale ;
- repartition ;
- apports en nature ;
- total des apports ;
- apports en numeraire ;
- certification par le president ;
- signature.

Blocs conditionnels :
- liste des souscripteurs depuis `capital_souscription.souscripteurs[]` si plusieurs souscripteurs sont arbitres ;
- bloc apports en nature obligatoire pour le sous-batch apport ;
- apports en numeraire affiches depuis le contexte.

Point sensible :
- la source V1 est redigee pour un actionnaire unique ; le referentiel projet indique que la liste des souscripteurs peut concerner un nombre variable d'associes pour SPFPL / SELAS / SCS.

### 6.7 Designation du commissaire aux apports

Role :
- designer le commissaire aux apports charge d'etablir le rapport sur la valeur de l'apport en nature.

Structure source :
- adresse de la personne principale ;
- titre `Acte de designation d'un commissaire aux apports` ;
- identification du soussigne ;
- rappel de la constitution de la SPFPL ;
- description de l'apport en nature ;
- nomination du commissaire ;
- mission ;
- signature.

Blocs conditionnels :
- selection obligatoire d'un commissaire ;
- suppression du `OU` source dans tout rendu automatise ;
- apport de titres depuis `apport_titres`.

Points sensibles :
- la source principale hard-code deux options de commissaire ;
- la variante `Copie de attestation nomination commissaire aux apports - transforme.docx` parametre ces commissaires ;
- la source est redigee pour un seul futur associe.

## 7. Variantes structurelles

| Famille | Variante | Condition | Source |
|---|---|---|---|
| Note d'information | cession | `operation_spfpl.type == cession` | meme DOCX, wording a arbitrer |
| Note d'information | apport | `operation_spfpl.type == apport` | meme DOCX, wording a arbitrer |
| PV agrement | associe unique | `dossier.options.associe_unique == true` | fichier 1 associe |
| PV agrement | plusieurs associes | `dossier.options.associe_unique == false` | fichier plusieurs associes |
| Acte de cession | parts | cession de parts | DOCX source confirme |
| Acte de cession | actions | cession d'actions | source absente ou ambigue |
| Contrat d'apport | source nommee | apport | DOCX source avec evaluateur/commissaire fixes |
| Contrat d'apport | variante transformee | apport | DOCX de controle avec roles parametrables |
| Attestation capital | actionnaire unique | apport V1 source | source confirmee |
| Attestation capital | liste dynamique | nombre de souscripteurs > 1 | source a arbitrer |
| Commissaire aux apports | commissaire 1 ou 2 | choix explicite | source avec `OU`, a normaliser |

## 8. Regles de blocage avant generation

Un futur generateur SPFPL doit bloquer si :
- `dossier.structure` n'est ni `SPFPL_CESSION` ni `SPFPL_APPORT` ;
- les documents de cession sont demandes sans `dossier.options.cession == true` ;
- les documents d'apport sont demandes sans `dossier.options.apport == true` ;
- une variable obligatoire du role `societe_spfpl`, `cedant`, `apporteur` ou `societe_cible` manque ;
- le document demande contient une double formulation source non arbitree, notamment `acquerir/de recevoir en apport en nature` ;
- le PV agrement doit etre produit alors que le wording `cession` versus `apport` n'est pas arbitre ;
- la repartition de capital avant/apres operation ne peut pas etre calculee ;
- une liste dynamique d'associes ou de souscripteurs est requise sans donnees structurees ;
- un document de commissaire aux apports est demande sans commissaire selectionne ;
- l'acte de cession d'actions est demande sans source confirmee.

## 9. Criteres avant implementation

Un ticket de code SPFPL pourra demarrer seulement si :
- le ou les documents cibles du ticket sont explicitement listes ;
- le choix cession versus apport est arbitre pour la note d'information ;
- le wording des PV `agrement cession` qui mentionnent l'apport est arbitre ;
- l'acte de cession d'actions est exclu du ticket ou sa source est fournie ;
- la regle associe unique / plusieurs associes est fournie dans le contexte ;
- les listes `associes_cible[]` et, si necessaire, `capital_souscription.souscripteurs[]` sont structurees ;
- le choix evaluateur / commissaire aux apports est explicite ;
- aucun DOCX source n'est utilise comme template d'execution ;
- les tests futurs verifient l'absence de placeholders `[` / `]` ;
- aucun wording juridique n'est modifie hors arbitrages documentes.

## 10. Points ouverts

1. **Acte de cession d'actions** : la source de verite le mentionne, mais aucune source DOCX explicitement nommee `acte de cession d'actions` n'a ete retrouvee. Le raw dump contient des fichiers `.doc` de cession SPFPL, dont `Acte_cession_SPFPL_tiers_modele.doc`, mais ils ne confirment pas a eux seuls le document canonique attendu. Ce document doit rester bloque.
2. **PV agrement cession versus apport** : les deux sources `PV SELARL agrement cession SPFPL` utilisent le vocabulaire de l'apport (`contrat d'apport`, `parts apportees`) alors que le referentiel les classe dans `SPFPL cession`. Aucune correction automatique ne doit etre faite sans validation juridique.
3. **Note d'information** : la source contient `acquerir/de recevoir en apport en nature`. Il faut choisir une variante cession, une variante apport, ou valider explicitement la double formule.
4. **Commissaire aux apports** : la source de verite parle de `comm. aux comptes`, mais les sources disponibles concernent un commissaire aux apports. Le libelle canonique retenu dans cette spec est `commissaire aux apports`, sous reserve de validation metier.
5. **Contrat d'apport** : la source nommee contient des informations fixes pour l'evaluateur et le commissaire ; une variante transformee parametre ces roles. Le futur ticket doit choisir la base source.
6. **Liste des souscripteurs** : la source disponible est centree sur un actionnaire unique. La prise en charge de plusieurs souscripteurs reste a arbitrer.
7. **Cession de parts** : le document source contient une mention isolee de `cession d'action` dans le bloc frais ; ce point doit etre relu avant code.

## 11. Statut de la spec canonique

`SPEC-SPFPL-001` est complet cote cadrage canonique pour le batch SPFPL specifique, sans code Python.

Prochaine etape recommandee :
- arbitrer les points ouverts 1 a 4 avant tout ticket de code SPFPL ;
- ouvrir ensuite un ticket de code limite a une sous-famille, en commencant de preference par la note d'information ou par l'acte de cession de parts seulement si les arbitrages requis sont tranches.
