# DAAT x SYDEL - SPEC CANONIQUE V1
## Lot 04 - Statuts SPFPL

## 1. Objet

Formaliser la spec canonique des statuts SPFPL avant tout codage.

Ticket : `SPEC-STATUTS-SPFPL-001`.

Cette spec couvre uniquement les deux sources statutaires SPFPL placees en Lot 04 :
- statuts SPFPL cession ;
- statuts SPFPL apport.

Cette spec ne code rien, ne modifie aucun wording juridique source, ne modifie aucun fichier Python et ne modifie aucun fichier de pilotage partage.

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
- `docs/delivery/lot_04_statuts_preparation_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources Lot 04 lues :
- `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx`
- `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx`

Constat source de verite :
- le chemin `SPFPL cession` mentionne les statuts `Statuts_SPFPLAS_dentistes_cession.docx` ;
- le chemin `SPFPL apport` mentionne les statuts `Statuts SPFPLAS dentistes - apport.docx` ;
- les deux chemins ont des documents satellites deja traites ou cadres ailleurs : demande d'inscription a l'ordre, regime communautaire, note d'information, PV d'agrement, acte de cession de parts, contrat d'apport, attestation capital et commissaire aux apports.

## 3. Perimetre documentaire V1

Documents canoniques de travail :

| Identifiant de travail | Document canonique | Source | Condition |
|---|---|---|---|
| `STATUTS-SPFPL-CESSION` | Statuts SPFPL cession | `Statuts_SPFPLAS_dentistes_cession.docx` | `dossier.structure == SPFPL_CESSION` |
| `STATUTS-SPFPL-APPORT` | Statuts SPFPL apport | `Statuts SPFPLAS dentistes - apport.docx` | `dossier.structure == SPFPL_APPORT` |

Hors perimetre de cette spec :
- documents universels Lot 1 ;
- PV nomination gerant ;
- demande d'inscription a l'ordre ;
- batch regime communautaire ;
- documents SPFPL specifiques du Lot 05 ;
- statuts SEL, statuts civils, statuts SAS ;
- toute automatisation de documents marques ou traites comme manuels.

Decision V1 :
- conserver deux sorties statutaires distinctes ;
- ne pas fusionner les textes cession et apport tant que la comparaison n'a pas prouve une identite de wording ;
- utiliser un tronc commun structurel, avec des overlays cession/apport explicites.

## 4. Cycle documentaire

| Document | Inventorie | Source recue | Analyse | Specifie | Pret a coder |
|---|---:|---:|---:|---:|---:|
| Statuts SPFPL cession | oui | oui | oui | oui | non, points ouverts a trancher |
| Statuts SPFPL apport | oui | oui | oui | oui | non, points ouverts a trancher |

Les deux documents sont suffisamment inventories et sources pour etre specifies. Ils ne sont pas prets a coder tant que les points ouverts de la section 13 ne sont pas arbitres ou transformes en blocages explicites.

## 5. Structure canonique de famille

La famille `Statuts SPFPL` est structuree en trois couches :

1. Tronc commun SPFPL :
   - forme de statuts d'une SPFPLAS de chirurgiens-dentistes ;
   - objet de prise de participation et gestion de participations dans des SEL ;
   - denomination, siege, duree ;
   - comptes courants ;
   - qualite d'associe ;
   - regime general des actions, cessions, transmission, exclusion ;
   - president, directeurs generaux, commissaires aux comptes ;
   - decisions collectives ;
   - comptes, resultats, transformation, dissolution ;
   - clauses ordinales et contestations ;
   - nomination du president et pouvoirs.

2. Overlay `cession` :
   - constitution par apport en numeraire ;
   - depot bancaire du capital ;
   - capital social exprime via `capital_social`, `capital_lettres`, `nb_actions`, `valeur_nominale_action` ;
   - exercice social entierement parametre ;
   - annexe d'engagements incluant ouverture du compte bancaire, mission SYDEL et acompte d'honoraires.

3. Overlay `apport` :
   - constitution par apport en nature de titres d'une SELARL ;
   - rapport du commissaire aux apports annexe aux statuts ;
   - transfert de propriete des parts au jour de l'immatriculation ;
   - capital social calcule depuis `montant_apports_nature` ;
   - exercice social fixe au 1er janvier / 31 decembre, avec premier exercice parametre par `fin_exercice` ;
   - annexe limitee dans la source a la nomination d'un commissaire aux apports.

## 6. Blocs structurels

### 6.1 En-tete et comparution

Bloc commun fonctionnel :
- denomination de la SPFPL ;
- forme / libelle SPFPL ;
- capital ;
- siege social ;
- titre `STATUTS` ;
- identification du soussigne, futur associe et president.

Variantes :
- la source cession affiche `Societe de Participations Financieres de Profession Liberale de Chirurgiens-Dentistes par actions simplifiee` et `Au capital de [capital_social]` ;
- la source apport affiche `Societe par actions simplifieesau capital de [capital_social] euros` puis `Societe de Participations Financieres de Profession Liberale de dentistes` ;
- la source cession utilise `[prenoms]` dans certains blocs, tandis que la source apport utilise `[prenom]`.

### 6.2 Articles fixes ou quasi fixes

Les articles suivants forment le tronc commun structurel, sous reserve de conserver les micro-variantes propres a chaque source :
- Article 2 - Objet ;
- Article 3 - Denomination ;
- Article 4 - Siege social ;
- Article 5 - Duree ;
- Article 7 - Comptes courants ;
- Article 9 - Qualite d'associe ;
- Articles 10 a 18 - capital, actions, cession, transmission, exclusion ;
- Articles 19 a 22 - president, directeurs generaux, commissaires, conventions ;
- Articles 23 a 26 - decisions collectives et information des associes ;
- Articles 28 a 36 - comptes, resultats, transformation, dissolution, contestations ;
- Articles 37 a 40 - declaration ordinale, nomination du president, actes de formation, publicite.

Regle V1 :
- un futur generateur ne doit pas harmoniser automatiquement ces micro-variantes ;
- tout article marque commun doit reprendre le wording de la source selectionnee, sauf arbitrage juridique explicite.

### 6.3 Articles overlays

Articles a traiter comme overlays forts :
- Article 1 - Forme : wording fixe `SAS` dans la source cession, wording parametre `[forme_sociale]` et bases legales detaillees dans la source apport ;
- Article 6 - Apports : numeraire pour cession, nature pour apport ;
- Article 8 - Capital social : source cession basee sur `capital_social` / `capital_lettres`, source apport basee sur `montant_apports_nature` ;
- Article 27 - Exercice social : dates parametrees dans cession, exercice fixe dans apport ;
- Article 40 / signature / Annexe 1 : date de signature absente en placeholder dans cession, presente dans apport ; annexes differentes.

## 7. Blocs associes dynamiques

Les deux sources SPFPL Lot 04 sont centrees sur un associe unique.

La source de verite projet rappelle toutefois que les statuts peuvent concerner 1 a 6 associes, notamment pour les statuts, avec un seul associe frequent mais non exclusif.

Decision V1 :
- ne pas coder la famille SPFPL comme strictement mono-associe sans arbitrage ;
- modeliser l'actionnariat avec `associes[]` ou `capital_souscription.souscripteurs[]` selon la decision du ticket de code ;
- en V1 de spec, le seul rendu directement source est `associes[0]` / souscripteur unique ;
- si plusieurs associes sont demandes, le futur generateur doit bloquer tant que les formes de comparution, repartition capital, signatures et annexes multi-associes ne sont pas validees.

Blocs dynamiques a prevoir :
- comparution du ou des soussignes ;
- repartition du capital ;
- attribution des actions ;
- nomination du president ;
- signatures ;
- eventuelle liste des engagements repris.

## 8. Variables canoniques

Les placeholders source ne deviennent pas la verite canonique du moteur. Les roles ci-dessous s'appuient sur le dictionnaire existant et sur les roles SPFPL deja poses dans les specs Lot 05.

### 8.1 Dossier et selection

- `dossier.structure`
- `operation_spfpl.type` : `cession` ou `apport`

Regles :
- `SPFPL_CESSION` selectionne `STATUTS-SPFPL-CESSION` ;
- `SPFPL_APPORT` selectionne `STATUTS-SPFPL-APPORT` ;
- aucune sortie ne doit rendre simultanement les overlays cession et apport.

### 8.2 Societe SPFPL

- `societe_spfpl.denomination`
- `societe_spfpl.forme_sociale`
- `societe_spfpl.forme_sociale_abregee`
- `societe_spfpl.libelle_forme_long`
- `societe_spfpl.profession`
- `societe_spfpl.capital_social`
- `societe_spfpl.capital_social_lettres`
- `societe_spfpl.siege.adresse_affichee`
- `societe_spfpl.siege.num_voie`
- `societe_spfpl.siege.voie`
- `societe_spfpl.siege.cp`
- `societe_spfpl.siege.ville`

Aliases source :
- `[denomination_societe]`
- `[forme_sociale]` dans la source apport uniquement
- `[capital_social]`
- `[capital_lettres]`
- `[adresse_siege]`

### 8.3 Associe fondateur / souscripteur

Role canonique recommande :
- `associes[]` pour la verite actionnariale ;
- `associes[0]` pour la source V1 mono-associe ;
- `dirigeant_nomine` pour le president nomme a l'article 38, avec `dirigeant_nomine.ref_associe_index` lorsque le president est l'associe fondateur.

Variables :
- `associes[].civilite_affichage`
- `associes[].prenom`
- `associes[].prenoms`
- `associes[].nom`
- `associes[].profession`
- `associes[].date_naissance`
- `associes[].ville_naissance`
- `associes[].departement_naissance`
- `associes[].adresse_personnelle_affichee`
- `associes[].situation_maritale`
- `associes[].regime_matrimonial`
- `associes[].nationalite`
- `associes[].conjoint.civilite_affichage`
- `associes[].conjoint.prenom`
- `associes[].conjoint.nom`
- `associes[].nb_actions`

Aliases source :
- `[civilite]`
- `[prenom]`
- `[prenoms]`
- `[nom]`
- `[profession]`
- `[date_naissance]`
- `[ville_naissance]`
- `[departement_naissance]`
- `[adresse_personnelle]`
- `[situation_maritale]`
- `[regime_matrimonial]`
- `[nationalite]`
- `[civilite_conjoint]`
- `[prenom_conjoint]`
- `[nom_conjoint]`
- `[nb_actions]`

### 8.4 Ordre professionnel

- `ordre.profession_reglementee`
- `ordre.profession_reglementee_pluriel`
- `ordre.departemental`
- `ordre.ville`
- `ordre.numero`
- `ordre.numero_rpps`

Aliases source :
- `[profession_reglementee]`
- `[ordre_departemental]`
- `[ville_ordre]`
- `[numero_ordre]`
- `[numero_rpps]`

### 8.5 Capital et apports

Capital :
- `capital_souscription.nb_actions_total`
- `capital_souscription.valeur_nominale_action`
- `capital_souscription.valeur_nominale_action_lettres`
- `capital_souscription.repartition_actions`

Aliases source :
- `[nb_actions]`
- `[valeur_nominale_action]`
- `[valeur_nominale_action_lettres]`
- `[valeur_nominale_part]`
- `[valeur_nominale_part_lettres]`

Overlay cession - apport en numeraire :
- `apport_numeraire.montant`
- `apport_numeraire.montant_lettres`
- `apport_numeraire.banque.nom`
- `apport_numeraire.banque.adresse_affichee`

Aliases source :
- `[montant_apport]`
- `[montant_apport_lettres]`
- `[nom_banque]`
- `[adresse_banque]`

Overlay apport - apport en nature :
- `apport_titres.nb_parts`
- `apport_titres.nb_parts_lettres`
- `apport_titres.plage_parts`
- `apport_titres.valeur_globale`
- `societe_cible.denomination`
- `societe_cible.forme_sociale`
- `societe_cible.siege.adresse_affichee`
- `societe_cible.ville_rcs`
- `societe_cible.numero_rcs`
- `commissaire_aux_apports.rapport_annexe`

Aliases source :
- `[nb_parts_apportees]`
- `[nb_parts_apportees_lettres]`
- `[plage_parts_cedees]` dans la source apport, nom source a confirmer ;
- `[montant_apports_nature]`
- `[denomination_societe_cedee]`
- `[ville_rcs_societe_cedee]`
- `[numero_rcs_societe_cedee]`

### 8.6 Exercice social et signature

- `exercice_social.debut`
- `exercice_social.fin`
- `exercice_social.premier_exercice_fin`
- `signature.lieu`
- `signature.date`

Aliases source :
- `[debut_exercice]` source cession ;
- `[fin_exercice]` source cession et apport ;
- `[date_cloture_exercice_1]` source cession ;
- `[lieu_signature]` ;
- `[date_signature]` source apport uniquement.

Regle :
- la source cession contient `Le` sans placeholder visible pour la date ; un futur generateur ne doit pas ajouter `signature.date` a cet endroit sans validation.

## 9. Elements manuels ou fournis par referentiel

Doivent rester fournis par le contexte dossier, une configuration validee ou une saisie humaine :
- libelle exact de profession et d'ordre ;
- adresse affichee du siege lorsque l'adresse detaillee n'est pas disponible ;
- situation matrimoniale, regime matrimonial et conjoint ;
- numero ordinal et RPPS ;
- banque de depot du capital en cession ;
- commissaire aux apports et rapport annexe en apport ;
- date de cloture du premier exercice ;
- date de signature cession si l'on decide de remplir la ligne `Le` ;
- annexes et engagements repris ;
- toute adaptation multi-associes.

Doivent rester hors automatisation V1 sans arbitrage :
- correction des anomalies de source ;
- transformation d'une source mono-associe en source multi-associes ;
- fusion des deux statuts en un seul document ;
- modification de wording ordinal ou legal.

## 10. Regles de blocage avant generation

Un futur generateur doit bloquer si :
- `dossier.structure` n'est pas `SPFPL_CESSION` ou `SPFPL_APPORT` ;
- les deux overlays cession et apport sont demandes dans le meme document de statuts ;
- une variable obligatoire de la societe SPFPL manque ;
- l'associe fondateur ou le president ne peut pas etre resolu ;
- plusieurs associes sont fournis sans arbitrage multi-associes ;
- `operation_spfpl.type == cession` sans montant d'apport numeraire, capital, banque ou repartition d'actions ;
- `operation_spfpl.type == apport` sans titres apportes, societe cible, valeur d'apport ou commissaire aux apports ;
- le rendu final conserverait un placeholder source `[` ou `]` ;
- le rendu necessiterait de corriger une anomalie source sans validation juridique ;
- la date de signature cession doit etre rendue mais n'est pas arbitree.

## 11. Criteres avant implementation

Un ticket de code pourra demarrer seulement si :
- il cible explicitement `STATUTS-SPFPL-CESSION`, `STATUTS-SPFPL-APPORT` ou les deux ;
- le comportement mono-associe versus multi-associes est tranche ;
- les champs de capital et d'apports sont structures ;
- la source de base de chaque overlay est explicitement confirmee ;
- les anomalies de source a corriger ou a conserver sont listees ;
- aucun DOCX source n'est utilise comme template d'execution ;
- les tests futurs verifient l'absence de placeholders residuels ;
- les tests couvrent au moins un cas cession et un cas apport si les deux overlays sont codes ensemble ;
- aucun wording juridique n'est harmonise entre cession et apport sans validation.

## 12. Points ouverts

1. **Multi-associes** : les sources Lot 04 SPFPL sont mono-associe, alors que la source de verite rappelle que les statuts peuvent couvrir 1 a 6 associes. Le mode multi-associes SPFPL doit etre arbitre avant code.
2. **Role canonique de la personne principale** : confirmer si le futur modele doit utiliser exclusivement `associes[0]` + `dirigeant_nomine`, ou introduire un alias local `fondateur_associe`.
3. **Source cession `[prenoms]` / `[prenom]`** : la source cession melange les deux aliases pour la meme personne. La convergence canonique doit etre tranchee avant code.
4. **Signature cession** : la source cession affiche `Le` sans `[date_signature]`, contrairement a la source apport. Il faut confirmer si la date doit rester manuelle ou etre automatisee.
5. **Article 1** : la source cession fixe la forme en SAS tandis que la source apport parametre `[forme_sociale]` et ajoute des bases legales. Ne pas fusionner sans validation.
6. **Article 23 et decisions collectives** : des differences de wording et de contenu existent entre les sources, notamment une phrase sur la visioconference presente dans apport. Ne pas normaliser sans validation.
7. **Article 27** : cession parametre l'exercice, apport fixe `1er janvier` / `31 decembre`. Ce choix doit rester overlay par source.
8. **Apport `[plage_parts_cedees]`** : la source apport utilise un alias nomme `cedees` pour des parts apportees. Le mapping canonique retient `apport_titres.plage_parts`, mais l'alias source doit etre documente.
9. **Anomalies visibles source apport** : la source contient des libelles ou caracteres suspects, par exemple `c_m`, `1cr`, `l'objet <lesdites`, `le1er janvier` et `le cas echant` degrade. Aucune correction automatique n'est autorisee.
10. **Annexe 1** : les engagements repris different fortement entre cession et apport. Le contenu final des annexes doit etre valide avant automatisation.

## 13. Statut de la spec canonique

`SPEC-STATUTS-SPFPL-001` est complet cote cadrage canonique pour ouvrir la spec texte V1 associee :
- `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`

Le ticket de code ne doit pas demarrer avant validation des points ouverts ou definition de blocages explicites.
