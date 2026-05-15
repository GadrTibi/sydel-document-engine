# DAAT x SYDEL - SPEC CANONIQUE V1
## Acte de cession d'actions SPFPL

Ticket : `SPEC-ACTE-ACTIONS-001`

## 1. Objet

Formaliser le positionnement canonique de l'acte de cession d'actions SPFPL a partir de la source DOCX exploitable :

- `project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx`

Cette spec ne code rien, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partage.

Elle complete les specs SPFPL existantes, qui maintenaient jusqu'ici l'acte de cession d'actions hors automatisation faute de source DOCX confirmee.

## 2. Sources lues

Memoire projet et workflow :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`

Specs SPFPL et audit :
- `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Source documentaire analysee :
- `project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx`

Hash SHA-256 du DOCX analyse :

```text
E615D60C11C67180233FC8B810A29C73755B1EC74B147E5548D4574DD03FDF8D
```

## 3. Nature exacte du document

Le document correspond bien a un acte de cession d'actions.

Indices source concordants :
- titre visible : `Cession d'actions` ;
- phrase d'introduction : `cession des actions de la Societe` ;
- expose : capital social divise en `[nb_actions] actions` ;
- bloc operation : `OBJET DU CONTRAT : CESSION D'ACTIONS` ;
- objet cede : `[nb_actions_cedees] actions` ;
- qualifications internes : `Actions Cedees` et `Titres Cedes` ;
- clauses de prix, propriete, jouissance, garantie et enregistrement toutes rattachees aux actions cedees.

Position canonique retenue :

| Champ | Valeur V1 |
|---|---|
| Identifiant de travail | `SPFPL-ACTE-CESSION-ACTIONS` |
| Document canonique | Acte de cession d'actions SPFPL a un tiers |
| Lot | Lot 05 |
| Chemin metier | `SPFPL_CESSION` |
| Operation | cession de titres sous forme d'actions |
| Source | DOCX converti et place dans `project/source_documents/lot_05/` |
| Relation avec l'acte de parts | document canonique distinct, pas un overlay de `SPFPL-ACTE-CESSION-PARTS` |

Le document ne doit pas etre confondu avec :
- `Acte_cession_SPFPL_tiers_part_modele.docx`, qui est l'acte de cession de parts ;
- les actes de cession de cabinets du Lot 03 ;
- les PV d'agrement SPFPL ;
- les statuts SPFPL.

## 4. Cycle documentaire

| Etape | Statut V1 | Commentaire |
|---|---:|---|
| Inventorie | oui | La source de verite mentionne `Acte de cession d'actions` dans le bloc `SPFPL cession`. |
| Valide | oui, cote perimetre | Le ticket demande explicitement cette spec apres preparation du DOCX. |
| Source recue | oui | DOCX place dans `project/source_documents/lot_05/`. |
| Analyse | oui | Source extraite : 115 paragraphes non vides et placeholders identifies. |
| Specifie | oui, par cette spec et la spec texte associee | Pas de code dans ce ticket. |
| Code | non | Futur ticket separe uniquement apres arbitrage des points ouverts. |
| Teste | non | Aucun generateur n'existe pour ce document. |
| Valide | non | Revue humaine juridique et visuelle requise avant automatisation. |

## 5. Conditions de selection V1

Le futur generateur ne doit etre selectionne que si toutes les conditions generales sont remplies :

- `dossier.structure == SPFPL_CESSION` ;
- `dossier.options.cession == true` ;
- `operation_spfpl.type == cession` ;
- `operation_spfpl.nature_titres == actions` ;
- la societe cible est une societe dont les titres cedes sont des actions ;
- la source d'actions est explicitement demandee, et non l'acte de cession de parts.

Blocage obligatoire :
- si `operation_spfpl.nature_titres == parts`, utiliser ou cibler l'acte de cession de parts, pas ce document ;
- si la nature des titres n'est pas fournie, bloquer ;
- si la societe cible n'est pas une societe par actions ou si l'overlay correspondant n'est pas valide, bloquer.

## 6. Variables canoniques

Les placeholders source ne deviennent pas automatiquement les noms canoniques. Les roles ci-dessous reprennent les conventions deja posees dans la spec SPFPL V1 en ajoutant le role specifique `cession_actions`.

### 6.1 Dossier et operation

- `dossier.structure`
- `dossier.options.cession`
- `operation_spfpl.type`
- `operation_spfpl.nature_titres`
- `operation_spfpl.document_demande`

Valeurs attendues :
- `dossier.structure = SPFPL_CESSION`
- `operation_spfpl.type = cession`
- `operation_spfpl.nature_titres = actions`
- `operation_spfpl.document_demande = acte_cession_actions`

### 6.2 Cedant

Role canonique :
- `cedant`

Variables :
- `cedant.civilite_affichage`
- `cedant.civilite_courte`
- `cedant.genre`
- `cedant.prenom`
- `cedant.nom`
- `cedant.profession`
- `cedant.profession_reglementee`
- `cedant.profession_reglementee_pluriel`
- `cedant.date_naissance`
- `cedant.ville_naissance`
- `cedant.departement_naissance`
- `cedant.nationalite`
- `cedant.adresse_personnelle.adresse_affichee`
- `cedant.situation_maritale`
- `cedant.regime_matrimonial`
- `cedant.conjoint.civilite_affichage`
- `cedant.conjoint.prenom`
- `cedant.conjoint.nom`
- `cedant.ordre.departemental`
- `cedant.ordre.numero_rpps`

Aliases sources principaux :
- `[civilite_cedant]`
- `[prenom_cedant]`
- `[nom_cedant]`
- `[profession_cedant]`
- `[date_naissance_cedant]`
- `[ville_naissance_cedant]`
- `[departement_naissance_cedant]`
- `[nationalite_cedant]`
- `[adresse_cedant]`
- `[situation_maritale_cedant]`
- `[regime_matrimonial]`
- `[civilite_conjoint_cedant]`
- `[prenom_conjoint_cedant]`
- `[nom_conjoint_cedant]`
- `[ordre_departemental_cedant]`
- `[numero_rpps_cedant]`

Point sensible :
- la source contient des formulations masculines fixes (`ne`, `inscrit`, `qu'il est proprietaire`). La variante feminine n'est pas sourcee dans ce document.

### 6.3 Societe SPFPL cessionnaire

Role canonique :
- `societe_spfpl`

Variables :
- `societe_spfpl.denomination`
- `societe_spfpl.forme_sociale`
- `societe_spfpl.forme_sociale_abregee`
- `societe_spfpl.capital_social`
- `societe_spfpl.ville_rcs`
- `societe_spfpl.numero_rcs`
- `societe_spfpl.siege.adresse_affichee`
- `societe_spfpl.departement_inscription_ordre`
- `societe_spfpl.representant.civilite_affichage`
- `societe_spfpl.representant.civilite_courte`
- `societe_spfpl.representant.prenom`
- `societe_spfpl.representant.nom`
- `societe_spfpl.representant.fonction`

Aliases sources principaux :
- `[denomination_societe_cessionnaire]`
- `[forme_sociale_acquereur]`
- `[capital_social_cessionnaire]`
- `[ville_rcs_cessionnaire]`
- `[numero_rcs_acquereur]`
- `[adresse_siege_cessionnaire]`
- `[departement_inscription_societe]`
- `[fonction_acquereur_representant]`
- `[civilite_representant_cessionnaire_courte]`
- `[prenom_representant_cessionnaire]`
- `[nom_representant_cessionnaire]`

Point sensible :
- la comparution cessionnaire source represente la SPFPL par les variables du cedant, tandis que la signature utilise des variables dediees au representant cessionnaire. Le futur modele doit trancher si le representant cessionnaire est toujours le cedant ou s'il s'agit d'un role distinct.

### 6.4 Societe cible dont les actions sont cedees

Role canonique :
- `societe_cible`

Variables :
- `societe_cible.denomination`
- `societe_cible.forme_sociale`
- `societe_cible.forme_sociale_complete`
- `societe_cible.profession_reglementee`
- `societe_cible.profession_reglementee_pluriel`
- `societe_cible.capital_social`
- `societe_cible.nb_actions_total`
- `societe_cible.valeur_nominale_action`
- `societe_cible.valeur_nominale_action_lettres`
- `societe_cible.siege.adresse_affichee`
- `societe_cible.ville_rcs`
- `societe_cible.numero_rcs`
- `societe_cible.departement_inscription_ordre`
- `societe_cible.repartition_capital_avant_operation`

Aliases sources principaux :
- `[denomination_societe_cedee]`
- `[forme_sociale_complete]`
- `[capital_social_societe_cedee]`
- `[nb_actions]`
- `[valeur_nominale_part_lettres]`
- `[adresse_siege]`
- `[ville_rcs_societe_cedee]`
- `[numero_rcs_societe_cedee]`
- `[departement_inscription_societe]`
- `[profession_reglementee]`
- `[profession_reglementee_pluriel]`

Point sensible :
- le placeholder source `[valeur_nominale_part_lettres]` est nomme comme une part, mais le texte source parle d'actions. Le nom canonique doit etre `valeur_nominale_action_lettres`.

### 6.5 Dirigeants de la societe cible

Role canonique :
- `societe_cible.dirigeants[]`

Variables par dirigeant :
- `civilite_affichage`
- `prenom`
- `nom`
- `fonction`
- `ordre_affichage`

Aliases sources observes :
- `[fonction_dirigeant]`
- `[fonction_dirigeant_pluriel]`
- `[civilite_personne_1]`
- `[prenom_president_societe_cedee]`
- `[nom_president_societe_cedee]`
- `[civilite_personne_2]`
- `[prenom_directeur_general_1]`
- `[nom_directeur_general_1]`
- `[civilite_cedant]`
- `[prenom_cedant]`
- `[nom_cedant]`

Point sensible :
- la source fixe un president et deux dirigeants supplementaires. Toute liste dynamique doit etre arbitree avant code.

### 6.6 Associes / actionnaires de la societe cible

Role canonique :
- `associes_cible[]`

Variables par entree :
- `type` : `personne_physique` ou `personne_morale`
- `civilite_affichage`
- `prenom`
- `nom`
- `denomination`
- `nb_actions_avant`
- `nb_actions_avant_lettres`
- `nb_actions_apres`
- `qualite`
- `est_cedant`
- `ordre_affichage`

Aliases sources observes :
- `[denomination_societe_associe_1]`
- `[actions_societe_associe_1]`
- `[civilite_associe_societe_cedee_1]`
- `[prenom_associe_societe_cedee_1]`
- `[nom_associe_societe_cedee_1]`
- `[actions_associe_societe_cedee_1]`
- `[civilite_associe_societe_cedee_2]`
- `[prenom_associe_societe_cedee_2]`
- `[nom_associe_societe_cedee_2]`
- `[actions_associe_societe_cedee_2]`
- `[nb_actions_lettres_personne_1]`
- `[nb_actions_personne_1]`
- `[nb_actions_lettres_personne_2]`
- `[nb_actions_personne_2]`

Regles :
- la table de repartition doit etre generee depuis `associes_cible[]` ;
- la somme des actions affichees doit etre egale a `societe_cible.nb_actions_total` ;
- le cedant doit detenir au moins `cession_actions.nb_actions` avant cession ;
- les donnees fixes a trois lignes de la source ne doivent pas devenir une structure moteur rigide.

### 6.7 Operation de cession d'actions

Role canonique :
- `cession_actions`

Variables :
- `cession_actions.nb_actions`
- `cession_actions.nb_actions_lettres`
- `cession_actions.prix_total`
- `cession_actions.prix_total_lettres`
- `cession_actions.prix_unitaire_action`
- `cession_actions.prix_unitaire_action_lettres`
- `cession_actions.date_realisation`
- `cession_actions.modalites_paiement`
- `cession_actions.nombre_exemplaires_lettres`

Aliases sources :
- `[nb_actions_cedees]`
- `[nb_actions_cedees_lettres]`
- `[prix_cession]`
- `[prix_cession_lettres]`
- `[prix_unitaire_part]`
- `[prix_unitaire_part_lettres]`
- `[nombre_exemplaires_lettres]`

Points sensibles :
- les placeholders `[prix_unitaire_part]` et `[prix_unitaire_part_lettres]` doivent etre mappes vers des variables canoniques d'action ;
- la source fixe le paiement par credit bancaire, comptant, par cheque de banque ;
- toute autre modalite de paiement requiert un overlay texte valide ou un blocage.

### 6.8 Signature

Role canonique :
- `signature`

Variables :
- `signature.lieu`
- `signature.date`
- `signature.mode`
- `signature.service`

Aliases sources :
- `[lieu_signature]`
- `[date_signature]`

Valeurs source :
- `signature.mode = electronique`
- `signature.service = Yousign`

## 7. Overlays eventuels

### 7.1 Overlay forme sociale / profession

La source contient une formulation fixe :

```text
Remplir les conditions exigees par la loi pour detenir des actions de SELAS de chirurgien-dentiste ;
```

Decision V1 :
- ne pas generaliser automatiquement a d'autres formes ou professions ;
- si la societe cible n'est pas une SELAS de chirurgien-dentiste, le futur generateur doit bloquer ou disposer d'un wording valide.

### 7.2 Overlay capital et actionnaires

La source est structuree autour d'une repartition fixe avec :
- une societe associee ;
- deux personnes physiques ;
- le cedant comme detenteur des actions cedees dans l'origine de propriete.

Decision V1 :
- utiliser `associes_cible[]` pour la table de capital ;
- bloquer si la repartition ne permet pas de verifier le total et la detention du cedant ;
- ne pas inventer une repartition apres cession dans cette spec.

### 7.3 Overlay representant cessionnaire

La source melange variables du cedant et variables du representant cessionnaire.

Decision V1 :
- creer le role `societe_spfpl.representant` ;
- bloquer si le contexte ne confirme pas si ce role est le cedant ou une personne distincte.

### 7.4 Overlay paiement

La source prevoit un paiement :
- par credit bancaire ;
- comptant ;
- par cheque de banque ;
- avec quittance.

Decision V1 :
- conserver cette modalite uniquement si le contexte la confirme ;
- sinon, blocage avant code ou wording valide separe.

### 7.5 Overlay garantie d'actif et de passif

La source contient une GAP complete avec plafond au prix de cession et durees fixes.

Decision V1 :
- traiter la GAP comme bloc juridique source a reprendre strictement ;
- toute absence de GAP, limitation differente ou adaptation doit etre une decision juridique explicite.

### 7.6 Overlay genre du cedant

La source contient plusieurs accords masculins non variables.

Decision V1 :
- ne pas generer automatiquement une variante feminine ;
- bloquer si le cedant n'est pas compatible avec le wording source et qu'aucun wording valide n'est fourni.

## 8. Elements manuels

Les elements suivants restent manuels ou soumis a validation avant automatisation :

- validation juridique de la source convertie depuis l'ancien `.doc` ;
- confirmation que le representant cessionnaire est bien le cedant ou fourniture d'un role distinct ;
- confirmation de l'agrement des associes mentionne dans la clause `NANTISSEMENT- PACTE D'ASSOCIES - AGREMENT` ;
- verification de coherence avec le PV d'agrement produit dans le meme dossier ;
- verification de la modalite de paiement bancaire et du cheque de banque ;
- validation de la GAP et de ses durees ;
- validation de la phrase fixe sur les actions de SELAS de chirurgien-dentiste ;
- revue humaine du bloc de signification / depot au siege social ;
- revue humaine de la communication au Conseil de l'Ordre ;
- conservation ou traitement du `Cadre reserve a l'administration`.

## 9. Regles de blocage avant generation

Un futur generateur doit bloquer si :

- le document n'est pas demande dans un dossier `SPFPL_CESSION` ;
- `operation_spfpl.nature_titres` n'est pas `actions` ;
- une variable obligatoire des roles `cedant`, `societe_spfpl`, `societe_cible`, `associes_cible[]`, `cession_actions` ou `signature` manque ;
- la somme des actions de `associes_cible[]` ne correspond pas a `societe_cible.nb_actions_total` ;
- le cedant ne detient pas les actions qu'il cede ;
- le prix total ne peut pas etre rapproche du prix unitaire et du nombre d'actions ;
- la societe cible n'est pas compatible avec le wording source `SELAS de chirurgien-dentiste` ;
- le representant cessionnaire n'est pas determine ;
- la modalite de paiement differe de la source sans wording valide ;
- le genre du cedant impose des accords non sources ;
- le rendu final conserverait un placeholder source `[` ou `]` ;
- le rendu final basculerait vers `parts` ou `parts sociales` pour les titres cedes.

## 10. Criteres avant implementation

Un futur ticket de code pourra demarrer seulement si :

- la spec texte associee existe ;
- le ticket cible uniquement l'acte de cession d'actions SPFPL ou un batch explicitement limite ;
- les points ouverts de forme sociale / profession, representant cessionnaire, genre et paiement sont tranches ou transformes en blocages explicites ;
- aucun DOCX source n'est utilise comme template d'execution ;
- les tests futurs verifient l'absence de placeholders residuels ;
- les tests futurs verifient que le document rendu est bien un acte d'actions et non de parts ;
- les tests futurs couvrent au minimum la coherence `nb_actions * prix_unitaire = prix_total` si les formats numeriques fournis le permettent ;
- aucune correction juridique silencieuse n'est introduite.

## 11. Points ouverts

1. **Source convertie** : le DOCX est exploitable, mais il provient d'un ancien `.doc`. Une validation humaine du rendu source reste requise avant code.
2. **Forme sociale / profession** : la source contient `actions de SELAS de chirurgien-dentiste`. Confirmer si la V1 doit etre limitee a ce cas ou si un wording parametre est fourni.
3. **Representant cessionnaire** : confirmer si le representant de la SPFPL cessionnaire est toujours le cedant ou un role distinct.
4. **Genre du cedant** : la source est au masculin. Aucune variante feminine n'est sourcee.
5. **Paiement** : confirmer si le paiement par credit bancaire, comptant et cheque de banque est toujours applicable.
6. **GAP** : confirmer que la garantie d'actif et de passif source est toujours attendue dans cette famille.
7. **Agrement** : confirmer la dependance avec le PV d'agrement et la preuve que les associes ont agree la cession a l'unanimite.
8. **Capital dynamique** : confirmer le format exact attendu pour la table de repartition lorsque le nombre d'actionnaires differe de la source.

## 12. Statut de la spec canonique

`SPEC-ACTE-ACTIONS-001` etablit que le document est un acte de cession d'actions SPFPL distinct de l'acte de cession de parts.

La prochaine etape recommandee est une revue metier des points ouverts avant tout ticket de code.
