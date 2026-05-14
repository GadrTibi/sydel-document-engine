# DAAT x SYDEL - SPEC CANONIQUE V1
## Famille `statuts civils` - SPEC-STATUTS-CIVILS-001

## 1. Objet

Formaliser la specification canonique V1 de la famille documentaire `statuts civils`, avant tout codage.

Cette spec couvre quatre sous-familles :
- `SCS` - statuts de societe en commandite simple ;
- `SCI` - statuts de societe civile immobiliere ;
- `SCI IRIS` - variante SCI IRIS ;
- `SCM` - statuts de societe civile de moyens.

Objectif V1 :
- distinguer les documents canoniques ;
- identifier les blocs communs eventuels ;
- identifier les blocs non fusionnables ;
- poser les roles dynamiques d'associes ;
- mapper les variables canoniques ;
- lister les elements manuels et points ouverts.

Aucun code Python n'est modifie par cette spec.

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

Sources DOCX Lot 04 lues :
- `project/source_documents/lot_04/Statuts_SCS_modele.docx`
- `project/source_documents/lot_04/Modele statuts SCI.docx`
- `project/source_documents/lot_04/Modele statuts SCI IRIS.docx`
- `project/source_documents/lot_04/Statuts SCM.docx`

Note : les fichiers physiques `Modele statuts SCI*.docx` portent un nom avec accent decompose sur disque. Les chemins ci-dessus sont normalises pour la lisibilite.

## 3. Perimetre documentaire V1

La source de verite rattache les statuts civils aux branches suivantes :
- `SCS` : statuts SCS ;
- `SCI` : statuts SCI, avec lettre option IS separee si option fiscale applicable ;
- `SCI IRIS` : statuts SCI IRIS, avec lettre option IS separee si option fiscale applicable ;
- `SCM` : statuts SCM, puis documents satellites SCM hors perimetre de cette spec.

Decision V1 :
- conserver quatre documents canoniques distincts ;
- ne pas dedupliquer `SCI` et `SCI IRIS` malgre une structure proche ;
- ne pas rapprocher `SCM` des SCI, car la logique de moyens et de contributions est specifique ;
- ne pas rapprocher `SCS` des SCI/SCM, car les roles commandite/commanditaire sont structurants.

Identifiants de travail :
- `LOT04-STATUTS-SCS`
- `LOT04-STATUTS-SCI`
- `LOT04-STATUTS-SCI-IRIS`
- `LOT04-STATUTS-SCM`

Les identifiants catalogue definitifs devront etre attribues dans un futur ticket de code.

## 4. Documents canoniques

### 4.1 `LOT04-STATUTS-SCS`

Role metier :
- constituer les statuts d'une societe en commandite simple a capital variable ;
- distinguer associes commandites et associes commanditaires ;
- organiser les apports, le capital variable, la gerance et les decisions collectives.

Caracteristiques structurantes :
- capital minimal, effectif et maximal ;
- roles statutaires `commandite` / `commanditaire` non interchangeables ;
- possibilite d'associe personne morale observee dans la repartition du capital ;
- compte bancaire de depot du capital ;
- annexe des engagements anterieurs.

### 4.2 `LOT04-STATUTS-SCI`

Role metier :
- constituer les statuts d'une societe civile immobiliere ;
- organiser les apports, la variabilite du capital, la gerance et les decisions collectives.

Caracteristiques structurantes :
- trois associes physiques observes dans la source ;
- capital variable avec capital minimum et capital autorise ;
- objet immobilier et patrimonial large ;
- option IS non integree au statut source : la source de verite mentionne une lettre separee.

### 4.3 `LOT04-STATUTS-SCI-IRIS`

Role metier :
- constituer la variante SCI IRIS ;
- conserver les clauses propres a la repartition du resultat exceptionnel et a la declaration fiscale.

Caracteristiques structurantes :
- structure tres proche de la SCI ;
- article fiscal dedie ;
- repartition du resultat exceptionnel par groupes de parts ;
- presence d'un associe personne morale ou assimile par `denomination_societe_2` dans la repartition du capital ;
- numerotation de parts plus fine que la SCI simple.

### 4.4 `LOT04-STATUTS-SCM`

Role metier :
- constituer les statuts d'une societe civile de moyens ;
- organiser la mise en commun de moyens, les apports, les charges et la gouvernance entre professionnels.

Caracteristiques structurantes :
- associe personne morale professionnelle ;
- associe personne physique professionnel ;
- objet centre sur les moyens communs, personnel auxiliaire, depenses et redevances ;
- clauses ordinales ou professionnelles sensibles ;
- documents satellites SCM hors perimetre : pacte d'associes, liste de depenses communes, contrat frais communs, reglement interieur.

## 5. Blocs communs eventuels

Ces blocs peuvent etre mutualises techniquement uniquement si le futur code represente explicitement les variantes et conserve le wording source :
- page de garde : denomination, forme, capital, siege ;
- comparution / identification des associes fondateurs ;
- forme juridique ;
- denomination ;
- siege social ;
- duree ;
- apports en numeraire ;
- capital social et repartition des parts ;
- indivisibilite des parts ;
- droits et obligations des associes ;
- gerance ou administration ;
- decisions collectives ;
- exercice social et comptes sociaux ;
- dissolution / liquidation ;
- contestations ;
- pouvoirs et publicite ;
- signature finale ;
- annexe des actes accomplis pour le compte de la societe en formation.

Regle V1 :
- un bloc est "commun" seulement au niveau fonctionnel ;
- le texte exact reste porte par chaque source documentaire ;
- aucune harmonisation de formulation n'est autorisee sans arbitrage.

## 6. Blocs non fusionnables

### SCS

Non fusionnable avec SCI/SCI IRIS/SCM :
- statut commandite / commanditaire ;
- responsabilite des commandites ;
- capital variable avec capital maximal explicite ;
- repartition entre commandites, commanditaires et eventuel associe personne morale ;
- clauses propres aux societes en commandite.

### SCI

Non fusionnable avec SCI IRIS sans arbitrage :
- article 33 simple sur affectation et repartition des benefices ;
- absence d'article fiscal dedie dans la source SCI ;
- repartition du capital plus simple ;
- absence des quotes-parts de resultat exceptionnel par groupes de parts.

### SCI IRIS

Non fusionnable avec SCI :
- article `DECLARATION FISCALE` ;
- repartition du resultat exceptionnel par groupes de parts ;
- variables `parts_debut_*`, `parts_fin_*`, `quote_part_resultat_exceptionnel_*` ;
- mention `SCI IRIS` dans les actes et documents emanant de la societe ;
- associe `denomination_societe_2` dans la repartition du capital.

### SCM

Non fusionnable avec SCI/SCS :
- objet de moyens, non objet immobilier patrimonial ;
- associes professionnels et logique de charges ;
- contribution aux pertes et ressources sociales propres a la SCM ;
- clauses de retrait, cession et communication du contrat propres a la SCM ;
- bloc ordinal / conciliation entre professionnels.

## 7. Associes dynamiques

La source de verite indique que les statuts peuvent contenir de 1 a 6 associes et que la meilleure solution cible est de partir d'un meme modele et d'ajouter autant d'associes que necessaire.

Decision canonique :
- ne pas coder `personne_1`, `personne_2`, `personne_3` comme verite metier ;
- utiliser `associes[]` avec des sous-roles et des donnees de repartition ;
- conserver les placeholders source comme aliases documentaires seulement.

### 7.1 Modele canonique commun `associes[]`

Chaque associe doit pouvoir porter :
- `type_personne` : `personne_physique` ou `personne_morale` ;
- `role_statutaire` : valeur propre au document ;
- `civilite_affichage` ;
- `genre` ;
- `prenom` ;
- `prenoms` ;
- `nom` ;
- `nom_naissance` ;
- `date_naissance` ;
- `ville_naissance` ;
- `departement_naissance` ;
- `nationalite` ;
- `profession` ;
- `situation_maritale` ;
- `adresse_personnelle.affichee` ou adresse detaillee ;
- `denomination` pour les personnes morales ;
- `forme_juridique` pour les personnes morales ;
- `capital_social` pour les personnes morales ;
- `siege.affiche` ou siege detaille pour les personnes morales ;
- `numero_rcs` ;
- `ville_rcs` ;
- `representant.civilite_affichage` ;
- `representant.prenom` ;
- `representant.nom` ;
- `representant.fonction` ;
- `apport.montant` ;
- `apport.montant_lettres` ;
- `parts.nb` ;
- `parts.nb_lettres` ;
- `parts.plage_affichee` ;
- `parts.debut` ;
- `parts.fin` ;
- `parts.qualite_associe` ;
- `parts.quote_part_resultat_exceptionnel` si SCI IRIS.

### 7.2 Roles par sous-famille

SCS :
- `associes_commandites[]` ;
- `associes_commanditaires[]` ;
- `associes_personnes_morales[]` si la repartition du capital le requiert ;
- un meme individu ne doit pas etre suppose automatiquement commandite et commanditaire sans validation dossier.

SCI :
- `associes[]` personnes physiques en V1 source ;
- le nombre source observe est 3, mais le modele cible doit etre repetable.

SCI IRIS :
- `associes[]` personnes physiques ;
- `associes_personnes_morales[]` ou associe nomme par denomination ;
- `groupes_parts[]` pour les quotes-parts de resultat exceptionnel.

SCM :
- `associes_personnes_morales[]` ;
- `associes_personnes_physiques[]` ;
- representant de la personne morale ;
- profession et qualite professionnelle obligatoires lorsque le wording source les affiche.

## 8. Variables canoniques

### 8.1 Societe

- `societe.forme`
- `societe.denomination`
- `societe.denomination_courte`
- `societe.capital_social`
- `societe.capital_social_lettres`
- `societe.capital_variable`
- `societe.mention_capital_variable`
- `societe.capital_minimum`
- `societe.capital_minimum_lettres`
- `societe.capital_autorise`
- `societe.capital_autorise_lettres`
- `societe.capital_maximal`
- `societe.capital_maximal_lettres`
- `societe.nb_parts_total`
- `societe.nb_parts_total_lettres`
- `societe.valeur_nominale_part`
- `societe.valeur_nominale_part_lettres`
- `societe.parts.plage_totale`
- `societe.duree`
- `societe.ville_rcs`

### 8.2 Siege

- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.siege.adresse_affichee`

### 8.3 Banque et depot du capital

- `capital_depot.banque.nom`
- `capital_depot.banque.adresse`
- `capital_depot.compte_ouvert`
- `capital_depot.date_depot` si requis dans une variante future.

### 8.4 Exercice et signature

- `exercice.date_cloture_premier_exercice`
- `signature.lieu`
- `signature.date`
- `signature.nombre_exemplaires`
- `signature.nombre_exemplaires_lettres`

### 8.5 Fiscalite et resultat

- `fiscalite.regime`
- `fiscalite.option_is`
- `resultat.groupes_parts[]`
  - `parts_debut`
  - `parts_fin`
  - `quote_part_resultat_exceptionnel`
- `resultat.quote_part_resultat_exceptionnel_total`

### 8.6 Gerance

- `dirigeants[]`
  - `type_personne`
  - `civilite_affichage`
  - `prenom`
  - `nom`
  - `denomination`
  - `fonction`
  - `ref_associe`

Note V1 :
- les sources statuts civils contiennent surtout des clauses generales de gerance ;
- la nomination effective du gerant est deja portee par le document canonique `PV nomination gerant` hors cette spec.

## 9. Mapping source -> canonique

### 9.1 Aliases communs

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | commun |
| `[denomination_societe_courte]` | `societe.denomination_courte` | SCM |
| `[forme_sociale]` | `societe.forme` | commun |
| `[capital_social]` | `societe.capital_social` | commun |
| `[capital_lettres]` | `societe.capital_social_lettres` | commun |
| `[mention_capital_variable]` | `societe.mention_capital_variable` | SCI / SCI IRIS |
| `[capital_autorise]` | `societe.capital_autorise` | SCI / SCI IRIS |
| `[capital_autorise_lettres]` | `societe.capital_autorise_lettres` | SCI / SCI IRIS |
| `[capital_social_maximal]` | `societe.capital_maximal` | SCS |
| `[capital_social_maximal_lettres]` | `societe.capital_maximal_lettres` | SCS |
| `[nb_parts]`, `[nb_parts_total]` | `societe.nb_parts_total` | selon source |
| `[nb_parts_lettres]`, `[nb_parts_total_lettres]` | `societe.nb_parts_total_lettres` | selon source |
| `[valeur_nominale_part]` | `societe.valeur_nominale_part` | commun |
| `[valeur_nominale_part_lettres]` | `societe.valeur_nominale_part_lettres` | SCS |
| `[num_voie_siege]` | `societe.siege.num_voie` | SCI / SCI IRIS / SCM |
| `[voie_siege]` | `societe.siege.voie` | SCI / SCI IRIS / SCM |
| `[cp_siege]` | `societe.siege.cp` | SCI / SCI IRIS / SCM |
| `[ville_siege]` | `societe.siege.ville` | SCI / SCI IRIS / SCM |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | SCS |
| `[ville_rcs]` | `societe.ville_rcs` | SCS |
| `[nom_banque]` | `capital_depot.banque.nom` | commun |
| `[adresse_banque]` | `capital_depot.banque.adresse` | commun |
| `[date_cloture_exercice_1]` | `exercice.date_cloture_premier_exercice` | commun |
| `[lieu_signature]` | `signature.lieu` | commun |
| `[date_signature]` | `signature.date` | commun |
| `[nombre_exemplaires_lettres]` | `signature.nombre_exemplaires_lettres` | SCS |

### 9.2 Aliases associes personnes physiques

| Pattern source | Variable canonique cible | Note |
|---|---|---|
| `[civilite_personne_N]` | `associes[N].civilite_affichage` | alias local |
| `[prenom_personne_N]` | `associes[N].prenom` | alias local |
| `[prenoms_personne_N]` | `associes[N].prenoms` | alias local |
| `[nom_personne_N]` | `associes[N].nom` | alias local |
| `[nom_naissance_personne_N]` | `associes[N].nom_naissance` | SCS |
| `[date_naissance_personne_N]` | `associes[N].date_naissance` | alias local |
| `[ville_naissance_personne_N]` | `associes[N].ville_naissance` | alias local |
| `[departement_naissance_personne_N]` | `associes[N].departement_naissance` | alias local |
| `[nationalite_personne_N]` | `associes[N].nationalite` | alias local |
| `[profession_personne_N]` | `associes[N].profession` | SCM |
| `[situation_maritale_personne_N]` | `associes[N].situation_maritale` | champ sensible |
| `[adresse_personne_N]`, `[adresse_perso_personne_N]` | `associes[N].adresse_personnelle.affichee` | source affichee |
| `[num_voie_perso_personne_N]` | `associes[N].adresse_personnelle.num_voie` | SCI / SCI IRIS |
| `[voie_perso_personne_N]` | `associes[N].adresse_personnelle.voie` | SCI / SCI IRIS |
| `[cp_perso_personne_N]` | `associes[N].adresse_personnelle.cp` | SCI / SCI IRIS |
| `[ville_perso_personne_N]` | `associes[N].adresse_personnelle.ville` | SCI / SCI IRIS |
| `[apport_personne_N]` | `associes[N].apport.montant` | commun |
| `[apport_lettres_personne_N]` | `associes[N].apport.montant_lettres` | commun |
| `[nb_parts_personne_N]` | `associes[N].parts.nb` | commun |
| `[nb_parts_lettres_personne_N]` | `associes[N].parts.nb_lettres` | commun |
| `[plage_parts_personne_N]` | `associes[N].parts.plage_affichee` | SCS |
| `[parts_debut_personne_N]` | `associes[N].parts.debut` | SCI IRIS |
| `[parts_fin_personne_N]` | `associes[N].parts.fin` | SCI IRIS |
| `[qualite_associe_personne_N]` | `associes[N].parts.qualite_associe` | SCS |

### 9.3 Aliases personnes morales

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe_1]` | `associes_personnes_morales[0].denomination` | SCM |
| `[forme_sociale_societe_1]` | `associes_personnes_morales[0].forme_juridique` | SCM |
| `[profession_societe_1]` | `associes_personnes_morales[0].profession` | SCM |
| `[capital_social_societe_1]` | `associes_personnes_morales[0].capital_social` | SCM |
| `[adresse_siege_societe_1]` | `associes_personnes_morales[0].siege.adresse_affichee` | SCM |
| `[numero_rcs_societe_1]` | `associes_personnes_morales[0].numero_rcs` | SCM |
| `[ville_rcs_societe_1]` | `associes_personnes_morales[0].ville_rcs` | SCM |
| `[civilite_personne_1] [prenom_personne_1] [nom_personne_1]` | `associes_personnes_morales[0].representant.*` | SCM, representant |
| `[fonction_personne_1]` | `associes_personnes_morales[0].representant.fonction` | SCM |
| `[denomination_societe_associe_1]` | `associes_personnes_morales[0].denomination` | SCS |
| `[qualite_associe_societe_1]` | `associes_personnes_morales[0].parts.qualite_associe` | SCS |
| `[parts_societe_associe_1]` | `associes_personnes_morales[0].parts.nb` | SCS |
| `[nb_parts_lettres_societe_associe_1]` | `associes_personnes_morales[0].parts.nb_lettres` | SCS |
| `[plage_parts_societe_associe_1]` | `associes_personnes_morales[0].parts.plage_affichee` | SCS |
| `[denomination_societe_2]` | `associes_personnes_morales[0].denomination` | SCI IRIS |
| `[nb_parts_societe_2]` | `associes_personnes_morales[0].parts.nb` | SCI IRIS |
| `[nb_parts_lettres_societe_2]` | `associes_personnes_morales[0].parts.nb_lettres` | SCI IRIS |
| `[parts_debut_societe_2]` | `associes_personnes_morales[0].parts.debut` | SCI IRIS |
| `[parts_fin_societe_2]` | `associes_personnes_morales[0].parts.fin` | SCI IRIS |

### 9.4 Aliases SCS commandite / commanditaire

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[apport_commanditaire_personne_2]` | `associes_commanditaires[].apport.montant` | SCS |
| `[apport_commanditaire_lettres_personne_2]` | `associes_commanditaires[].apport.montant_lettres` | SCS |
| `[total_apports_commandites]` | `scs.total_apports_commandites` | SCS |

### 9.5 Aliases SCI IRIS resultat

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[parts_debut_groupe_1]` | `resultat.groupes_parts[0].parts_debut` | SCI IRIS |
| `[parts_fin_groupe_1]` | `resultat.groupes_parts[0].parts_fin` | SCI IRIS |
| `[quote_part_resultat_exceptionnel_groupe_1]` | `resultat.groupes_parts[0].quote_part_resultat_exceptionnel` | SCI IRIS |
| `[parts_debut_groupe_2]` | `resultat.groupes_parts[1].parts_debut` | SCI IRIS |
| `[parts_fin_groupe_2]` | `resultat.groupes_parts[1].parts_fin` | SCI IRIS |
| `[quote_part_resultat_exceptionnel_groupe_2]` | `resultat.groupes_parts[1].quote_part_resultat_exceptionnel` | SCI IRIS |
| `[quote_part_resultat_exceptionnel_total]` | `resultat.quote_part_resultat_exceptionnel_total` | SCI IRIS |

## 10. Elements manuels

Elements a ne pas automatiser sans arbitrage ou sans donnees explicites :
- `situation_maritale_personne_N` : champ sensible, a fournir en texte valide ;
- `adresse_personne_N` ou adresse detaillee : aucune reconstruction implicite si la source attend une adresse affichee ;
- `nom_banque` et `adresse_banque` ;
- `date_cloture_exercice_1` ;
- `nombre_exemplaires_lettres` ;
- annexe des actes accomplis pour le compte de la societe en formation si la liste doit varier ;
- choix fiscal IS : la lettre option IS est un document separe, non un bloc a injecter dans les statuts SCI/SCI IRIS ;
- clauses de resultat exceptionnel SCI IRIS ;
- roles commandite / commanditaire SCS ;
- qualite professionnelle et donnees ordinales SCM ;
- repartition fine des parts et plages de numerotation.

## 11. Regles de validation avant futur code

Le futur generateur devra bloquer si :
- aucun document canonique n'est selectionne parmi SCS / SCI / SCI IRIS / SCM ;
- une sous-famille tente d'utiliser le texte d'une autre sous-famille ;
- le total des apports ne correspond pas au capital social ;
- le total des parts ne correspond pas au nombre total de parts ;
- une plage de parts est manquante lorsque la source l'exige ;
- un associe personne morale est present sans representant lorsque la source l'affiche ;
- un role SCS `commandite` ou `commanditaire` est manquant ;
- une repartition SCI IRIS de resultat exceptionnel est incomplete ;
- une valeur manuelle sensible est absente mais requise par le wording source.

## 12. Points ouverts

- Confirmer si les quatre documents doivent devenir quatre generateurs distincts ou un module technique partage avec quatre sorties strictement separees.
- Confirmer la gestion cible de 1 a 6 associes pour les statuts : generation dynamique ou limite V1 par source observee.
- Arbitrer le traitement des associes personnes morales dans SCI IRIS et SCM.
- Arbitrer la ligne source SCM de repartition des parts : la source affiche deux fois `nb_parts_personne_2` et ne contient pas de placeholder distinct clair pour les parts de la personne morale.
- Confirmer si les signatures doivent repeter tous les associes dynamiques ou conserver la forme source observee.
- Confirmer si `SCI IRIS` est une forme/variante de denomination a afficher telle quelle ou une famille metier distincte avec donnees propres.
- Ne pas coder la lettre option IS dans cette famille sans spec separee.
- Ne pas coder les documents satellites SCM sans spec separee.
