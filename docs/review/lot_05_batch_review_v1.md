# Lot 05 - pack de revue humaine batch V1

Ticket : `REVIEW-BATCH-LOT05-001`

## Objet

Preparer une revue humaine des documents Lot 05 deja generes et des sources Lot 05 disponibles.

Ce pack ne valide pas juridiquement les documents. Il sert a guider une relecture visuelle et juridique humaine avant validation metier.

## Sources et sorties relues

Sources relues dans `project/source_documents/lot_05/` :
- `NOTE D'INFORMATION.docx`
- `PV SELARL agrément cession SPFPL - SELARL 1 associé - transforme.docx`
- `PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx`
- `Acte_cession_SPFPL_tiers_part_modele.docx`
- `Contrat d_apport SEL SPFPL.docx`
- `Attestation sur le capital - apport - liste des souscripteurs.docx`
- `attestation nomination commissaire aux apports - transforme.docx`
- `Acte_cession_SPFPL_tiers_modele.docx`
- `Pacte d_associés SCM.docx`
- `Liste dépenses communes SCM.docx`
- `CONTRAT FRAIS COMMUNS.docx`
- `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx`

DOCX generes relus dans `artifacts/` :
- `artifacts/lot_05_spfpl_agrement_info_smoke_test/note_information.docx`
- `artifacts/lot_05_spfpl_agrement_info_smoke_test/pv_agrement_cession_spfpl_associe_unique.docx`
- `artifacts/lot_05_spfpl_agrement_info_smoke_test/pv_agrement_cession_spfpl_plusieurs_associes.docx`
- `artifacts/lot_05_spfpl_core_smoke_test/acte_cession_parts_spfpl.docx`
- `artifacts/lot_05_spfpl_core_smoke_test/contrat_apport_spfpl.docx`
- `artifacts/lot_05_spfpl_core_smoke_test/attestation_capital_liste_souscripteurs.docx`
- `artifacts/lot_05_spfpl_core_smoke_test/attestation_commissaire_apports.docx`
- `artifacts/lot_05_sas_satellites_smoke_test/pv_remuneration_president.docx`
- `artifacts/lot_05_sas_satellites_smoke_test/attestation_capital_liste_souscripteurs_sas.docx`

Constats generaux :
- les DOCX generes relus ne contiennent pas de placeholder source visible de type `[variable]` dans le texte extrait ;
- le rendu des titres de PV SPFPL et SAS doit etre verifie visuellement, car l'extraction texte joint certaines lignes de titre ;
- aucun DOCX genere d'acte de cession d'actions SPFPL n'a ete trouve dans `artifacts/` ;
- aucun DOCX genere de satellites SCM n'a ete trouve dans `artifacts/` localement.

## Sous-famille - note d'information

### Note d'information

Chemin source :
- `project/source_documents/lot_05/NOTE D'INFORMATION.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_agrement_info_smoke_test/note_information.docx`

Points visuels a verifier :
- titre `Note d'informations`, sous-titre `Constitution de la Societe` et denomination clairement separes ;
- lisibilite du paragraphe principal et des listes de repartition du capital ;
- signature finale presente et correctement espacee ;
- absence de residu de placeholder ou de ponctuation issue du modele source.

Points juridiques a verifier :
- wording cession/apport : la sortie relue utilise une variante cession unique, sans double formule source ;
- coherence entre type d'operation, nombre de parts, societe cible et repartition apres operation ;
- denomination, siege, capital, RCS et qualite du signataire ;
- absence de modification non validee du wording source au-dela de l'arbitrage SPFPL V1.

Verdict attendu : OK / corrections.

## Sous-famille - agrement cession SPFPL

### PV agrement cession SPFPL - associe unique

Chemin source :
- `project/source_documents/lot_05/PV SELARL agrément cession SPFPL - SELARL 1 associé - transforme.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_agrement_info_smoke_test/pv_agrement_cession_spfpl_associe_unique.docx`

Points visuels a verifier :
- en-tete societe cible complet et lisible ;
- titre `PROCES-VERBAL DE L'ASSOCIE UNIQUE` separe du bloc date ;
- resolutions clairement separees et numerotees ;
- signature associe unique presente et correctement positionnee.

Points juridiques a verifier :
- le vocabulaire doit etre celui de la cession, conformement a l'arbitrage SPFPL V1 ;
- l'associe unique doit etre la bonne personne et detenir la qualite attendue ;
- l'agrement de la SPFPL et la modification statutaire doivent correspondre a l'operation ;
- l'article de repartition du capital apres operation doit etre coherent avec les parts cedees.

Verdict attendu : OK / corrections.

### PV agrement cession SPFPL - plusieurs associes

Chemin source :
- `project/source_documents/lot_05/PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_agrement_info_smoke_test/pv_agrement_cession_spfpl_plusieurs_associes.docx`

Points visuels a verifier :
- titre AGE lisible, sans collage entre `DE`, `L'ASSEMBLEE` et la date ;
- liste des associes presents ou representes bien structuree ;
- resolutions et pouvoirs separes ;
- signatures de tous les associes attendus presentes.

Points juridiques a verifier :
- coherence de la convocation, de la presence et de la totalite des parts representees ;
- adaptation du wording `apport` vers `cession` conforme a l'arbitrage SPFPL V1 ;
- repartition du capital apres operation conforme aux donnees dossier ;
- pouvoirs et formalites coherents avec une cession de parts a une SPFPL.

Verdict attendu : OK / corrections.

## Sous-famille - SPFPL core

### Acte de cession de parts SPFPL

Chemin source :
- `project/source_documents/lot_05/Acte_cession_SPFPL_tiers_part_modele.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_core_smoke_test/acte_cession_parts_spfpl.docx`

Points visuels a verifier :
- titre `Cession de parts` et blocs `ENTRE` lisibles ;
- structure des clauses conservee : exposes, objet, prix, declarations, formalites, signatures ;
- listes de repartition du capital avant/apres operation clairement lisibles ;
- absence de trous typographiques ou de paragraphes anormalement compactes.

Points juridiques a verifier :
- document bien limite aux parts sociales, sans bascule non justifiee vers les actions ;
- prix unitaire, prix total, nombre et plage de parts cedees coherents ;
- qualite du cedant, du cessionnaire et du representant SPFPL ;
- mention source isolee `cession d'action` dans le bloc frais : verifier si elle a ete conservee, adaptee ou doit etre corrigee avec validation.

Verdict attendu : OK / corrections.

### Contrat d'apport SEL SPFPL

Chemin source :
- `project/source_documents/lot_05/Contrat d_apport SEL SPFPL.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_core_smoke_test/contrat_apport_spfpl.docx`

Points visuels a verifier :
- titre, comparution des parties et expose correctement separes ;
- blocs biens apportes, evaluation, remuneration et conditions suspensives visibles ;
- signatures finales presentes ;
- absence de residus de modele source.

Points juridiques a verifier :
- nature des titres apportes, nombre, plage, valeur par titre et valeur globale ;
- coherence entre apporteur, societe cible et SPFPL beneficiaire ;
- evaluateur et commissaire aux apports fournis par contexte, sans entite hard-codee non validee ;
- conditions suspensives et option fiscale conformes au dossier.

Verdict attendu : OK / corrections.

### Attestation capital / liste des souscripteurs SPFPL

Chemin source :
- `project/source_documents/lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_core_smoke_test/attestation_capital_liste_souscripteurs.docx`

Points visuels a verifier :
- en-tete SPFPL, titre `ATTESTATION` et sous-titre `Liste des souscripteurs` distincts ;
- repartition des actions lisible ;
- blocs apports en nature et apports en numeraire visibles ;
- certification et signature du president presentes.

Points juridiques a verifier :
- V1 limitee a un actionnaire unique : confirmer que le cas relu correspond bien a cette limite ;
- coherence capital social, nombre d'actions, valeur nominale et montants d'apports ;
- coherence avec les statuts SPFPL ou SAS applicables au dossier ;
- absence de generalisation non validee vers plusieurs souscripteurs.

Verdict attendu : OK / corrections.

### Acte de designation du commissaire aux apports

Chemin source :
- `project/source_documents/lot_05/attestation nomination commissaire aux apports - transforme.docx`

Chemin DOCX genere :
- `artifacts/lot_05_spfpl_core_smoke_test/attestation_commissaire_apports.docx`

Points visuels a verifier :
- adresse du soussigne et titre du document correctement separes ;
- presentation de l'apport lisible ;
- presentation du commissaire aux apports non tronquee ;
- signature finale presente.

Points juridiques a verifier :
- un seul commissaire aux apports doit etre retenu en sortie ;
- la source contient un `OU`, mais le DOCX genere relu ne doit pas conserver cette option ;
- commissaire et mission coherents avec l'apport en nature ;
- libelle `commissaire aux apports` confirme, sans confusion avec commissaire aux comptes.

Verdict attendu : OK / corrections.

## Sous-famille - acte de cession d'actions SPFPL

### Acte de cession d'actions

Chemin source :
- `project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx`

Chemin DOCX genere :
- non disponible dans `artifacts/` au moment de cette revue.

Points visuels a verifier :
- a faire lorsque le DOCX genere sera disponible ;
- controler le titre `Cession d'actions`, l'objet du contrat, les clauses actions/titres et les signatures.

Points juridiques a verifier :
- source preparee mais spec dediee encore requise avant implementation ;
- ne pas substituer l'acte de cession de parts a l'acte de cession d'actions ;
- verifier les variables actions : nombre total d'actions, actions cedees, prix et qualite des parties ;
- bloquer toute generation tant que la spec canonique et la spec texte dediees ne sont pas ecrites.

Verdict attendu : corrections.

## Sous-famille - satellites SAS

### PV remuneration president

Chemin source :
- `project/source_import/raw_drive_dump/Creation SAS/PV remuneration president - transforme.docx`
- note : source non presente dans `project/source_documents/lot_05/` d'apres les specs SAS satellites V1.

Chemin DOCX genere :
- `artifacts/lot_05_sas_satellites_smoke_test/pv_remuneration_president.docx`

Points visuels a verifier :
- titre `PROCES-VERBAL DES DECISIONS DE L'ASSOCIE UNIQUE` lisible, sans collage avec la date ;
- en-tete societe complet ;
- decision unique clairement separee ;
- signature finale presente.

Points juridiques a verifier :
- la V1 couvre uniquement une absence de remuneration jusqu'a la cloture du premier exercice ;
- president et actionnaire unique doivent designer la meme personne ;
- cas feminin ou fonction differente : verifier qu'aucune variation non sourcee n'est rendue ;
- coherence avec les statuts SAS sur capital, siege, RCS et exercice social.

Verdict attendu : OK / corrections.

### Attestation capital / liste des souscripteurs SAS

Chemin source :
- `project/source_documents/lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx`

Chemin DOCX genere :
- `artifacts/lot_05_sas_satellites_smoke_test/attestation_capital_liste_souscripteurs_sas.docx`

Points visuels a verifier :
- en-tete SAS, titre et sous-titre bien separes ;
- repartition des actions et apports lisibles ;
- certification finale et signature presentes ;
- absence de confusion visuelle entre attestation SPFPL et satellite SAS.

Points juridiques a verifier :
- attestation traitee comme document unique malgre le double libelle source ;
- V1 limitee a un souscripteur unique ;
- presence d'un apport en nature de parts conforme au dossier ;
- alias source `valeur_nominale_part` : verifier que le rendu parle correctement d'actions sans correction non validee.

Verdict attendu : OK / corrections.

## Sous-famille - satellites SCM

### Pacte d'associes SCM

Chemin source :
- `project/source_documents/lot_05/Pacte d_associés SCM.docx`

Chemin DOCX genere :
- non disponible dans `artifacts/` au moment de cette revue.

Points visuels a verifier :
- a faire lorsque le DOCX genere sera disponible ;
- verifier titres, parties, tableaux ou blocs d'engagements, signatures.

Points juridiques a verifier :
- spec canonique et spec texte SCM satellites requises avant validation d'un rendu ;
- ne pas injecter ce document dans les statuts SCM ;
- verifier les associes, obligations, duree, sorties et clauses sensibles une fois le rendu disponible.

Verdict attendu : corrections.

### Liste depenses communes SCM

Chemin source :
- `project/source_documents/lot_05/Liste dépenses communes SCM.docx`

Chemin DOCX genere :
- non disponible dans `artifacts/` au moment de cette revue.

Points visuels a verifier :
- a faire lorsque le DOCX genere sera disponible ;
- verifier la structure de liste, les intitules de depense et les espaces de completude.

Points juridiques a verifier :
- source legacy convertie : relire toute perte ou deformation apres conversion ;
- clarifier si le document reste formulaire a completer ou document finalise ;
- verifier les categories de depenses communes et la designation de la SCM.

Verdict attendu : corrections.

### Contrat frais communs

Chemin source :
- `project/source_documents/lot_05/CONTRAT FRAIS COMMUNS.docx`

Chemin DOCX genere :
- non disponible dans `artifacts/` au moment de cette revue.

Points visuels a verifier :
- a faire lorsque le DOCX genere sera disponible ;
- verifier titres, parties, clauses de partage des frais et signatures.

Points juridiques a verifier :
- spec SCM satellites requise avant validation ;
- verifier cle de repartition, charges, periode, obligations et articulation avec la SCM ;
- ne pas fusionner avec le pacte ou le reglement interieur.

Verdict attendu : corrections.

### Reglement interieur SCM

Chemin source :
- `project/source_documents/lot_05/REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx`

Chemin DOCX genere :
- non disponible dans `artifacts/` au moment de cette revue.

Points visuels a verifier :
- a faire lorsque le DOCX genere sera disponible ;
- verifier titres, articles, numerotation et signatures.

Points juridiques a verifier :
- source brute portait un prefixe `2024` documente lors de la preparation : confirmer la source canonique ;
- verifier articulation avec statuts SCM, pacte, liste des depenses et contrat frais communs ;
- ne pas reprendre ou modifier des clauses sans spec texte dediee.

Verdict attendu : corrections.

## Synthese des verdicts attendus

| Sous-famille | Documents | Verdict attendu |
|---|---|---|
| Note d'information | Note d'information | OK / corrections |
| Agrement cession SPFPL | PV associe unique, PV plusieurs associes | OK / corrections |
| SPFPL core | Acte parts, contrat apport, attestation capital, commissaire aux apports | OK / corrections |
| Acte cession actions SPFPL | Acte actions | corrections |
| Satellites SAS | PV remuneration president, attestation capital SAS | OK / corrections |
| Satellites SCM | Pacte, liste depenses, contrat frais communs, reglement interieur | corrections |

## Prochaine etape recommandee

Faire relire humainement les DOCX generes disponibles, puis regenerer ou specifier les documents sans sortie disponible avant toute validation metier.
