# DAAT x SYDEL - Blueprint de style Lot 03 batch V1
## Ticket STYLE-ANALYSE-LOT03-BATCH-001

## 1. Objet

Documenter les ecarts de structure visuelle restants entre les sources Word Lot 03 et les DOCX generes dans `artifacts/`.

Le moteur reste en generation DOCX from-scratch. Ce blueprint ne demande donc pas une copie Word au millimetre, mais identifie les blocs de rendu qui doivent mieux restituer la structure visible des sources.

Ce document ne modifie aucun wording juridique. Il ne valide ni le fond juridique, ni les arbitrages metier deja ouverts dans les specs Lot 03.

## 2. References lues

Memoire projet et cadrage :

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/adr/0004-from-scratch-docx-generation.md`
- `docs/adr/0005-codex-working-mode.md`
- `docs/delivery/render_style_system_v1.md`
- `docs/delivery/render_style_blueprint_batch_v1.md`

Specs Lot 03 :

- `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`
- `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`
- `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`
- `docs/delivery/lot_03_derogations_spec_canonique_v1.md`
- `docs/delivery/lot_03_derogations_spec_texte_v1.md`

## 3. Documents compares

### 3.1 Sources Word

- `project/source_documents/lot_03/Avenant Contrat de bail.docx`
- `project/source_documents/lot_03/appel de fond sel.docx`
- `project/source_documents/lot_03/Acte de cession d_un cabinet medical.docx`
- `project/source_documents/lot_03/Compromis de cession d_un cabinet medical.docx`
- `project/source_documents/lot_03/Acte de cession d'un cabinet dentaire.docx`
- `project/source_documents/lot_03/Compromis de cession d_un cabinet dentaire.docx`
- `project/source_documents/lot_03/Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx`
- `project/source_documents/lot_03/Demande de derogation cumul SELARL - BNC.docx`

### 3.2 DOCX generes

- `artifacts/lot_03_bail_appel_fonds_smoke_test/avenant_contrat_bail.docx`
- `artifacts/lot_03_bail_appel_fonds_smoke_test/appel_fond_sel.docx`
- `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_medical.docx`
- `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_medical.docx`
- `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_dentaire.docx`
- `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_dentaire.docx`
- `artifacts/lot_03_derogations_core_smoke_test/formulaire_derogation_sites_sel_formulaire_a_completer.docx`
- `artifacts/lot_03_derogations_core_smoke_test/demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx`

## 4. Methode

Analyse structurelle en lecture seule des DOCX :

- marges de section ;
- paragraphes non vides ;
- alignements explicites ;
- gras, italique et soulignement ;
- listes Word via `numPr` ou tirets visibles ;
- retraits et retraits suspendus ;
- tables, bordures et premiers contenus de cellules.

Cette analyse est limitee au rendu visuel. Elle ne signale pas les ecarts de texte juridique sauf lorsqu'une structure de rendu porte visiblement le texte, par exemple un titre, un objet ou une table de signature.

## 5. Ecarts par document

### 5.1 Avenant bail

Source :

- marges haut/bas compactes : environ `1,75 cm` en haut et `0,5 cm` en bas ;
- titre encadre en table 1 colonne ;
- paragraphes de corps majoritairement justifies ;
- libelles `Ci-apres designe ...` alignes a droite, en gras et soulignes ;
- titres d'articles en gras et soulignes ;
- table de signatures 2 x 2 avec bordures explicites.

Genere :

- profil standard `2,5 cm` sur toutes les marges ;
- titre encadre conserve ;
- corps partiellement justifie ;
- libelles `Ci-apres designe ...` rendus en flux standard, sans alignement droite, gras ni soulignement ;
- titres d'articles en gras mais sans soulignement ;
- table de signatures conservee en 2 x 2, mais les bordures directes OpenXML ne sont pas posees comme dans la source.

Ecarts visibles :

- perte des marqueurs visuels droite + gras + soulignement sur les qualifications des parties ;
- perte du soulignement sur les titres d'articles ;
- densite verticale differente a cause des marges standard ;
- rendu de la signature proche en structure, mais a stabiliser via un bloc de table signature avec bordures directes.

Lecture blueprint :

- document plutot proche de la structure source ;
- correction prioritaire limitee : style des libelles de parties, style des articles, bordures directes de la table de signatures et profil de marges compact optionnel.

### 5.2 Appel de fonds SEL

Source :

- marges standard `2,5 cm` ;
- banque positionnee par retrait / retrait suspendu ;
- lieu et date sur une ligne dediee ;
- destinataire en italique ;
- objet en gras et souligne ;
- montant centre ;
- corps principal justifie ;
- signataire final en bas, avec alignement source non strictement reproduit par le flux standard.

Genere :

- marges standard conservees ;
- toutes les lignes de tete sont en flux gauche standard ;
- destinataire sans italique ;
- objet sans gras ni soulignement ;
- montant et symbole euro rendus sur deux lignes en flux gauche ;
- corps principal justifie ;
- signature finale en flux gauche.

Ecarts visibles :

- perte nette du style de lettre : objet, destinataire, montant et signature ;
- disparition du montant centre ;
- absence d'italique pour le destinataire ;
- absence de blocs dedies `letter_header`, `subject_heading`, `amount_centered` et `signature_right`.

Lecture blueprint :

- document prioritaire du mini-batch bail/appel ;
- le wording est stable, mais le rendu doit restaurer les codes visuels minimaux d'une lettre bancaire.

### 5.3 Cession cabinets

Sources medicales et dentaires :

- marges standard `2,5 cm` ;
- titres principaux en tables encadrees ;
- plusieurs titres de grandes sections en tables 1 colonne encadrees ;
- tableaux de chiffres d'affaires avec bordures explicites ;
- nombreux paragraphes justifies ;
- listes Word structurees avec retraits suspendus ;
- marqueurs `De premiere part` / `De deuxieme part` alignes a droite ;
- signatures finales variables selon document : placeholders image, mentions manuscrites, `Lu et approuve`, clauses de signature electronique, annexes.

Generes :

- marges standard conservees ;
- titre principal encadre conserve ;
- grands titres rendus en paragraphes gras + soulignes, sans table encadree ;
- tableaux de chiffres d'affaires presents, mais bordures directes non posees comme dans les sources ;
- listes rendues en tirets visibles avec retrait suspendu, pas en listes Word source ;
- alignements droite des marqueurs de parties absents ;
- signatures reduites a deux lignes centrees `Le vendeur` / `L'acquereur` ;
- annexes rendues en tirets visibles.

Ecarts visibles communs :

- perte des encadres de section qui structurent fortement les actes et compromis sources ;
- table de chiffres d'affaires moins proche visuellement des sources ;
- listes lisibles mais non equivalentes aux listes Word source ;
- perte des alignements droite sur les marqueurs de parties ;
- signatures beaucoup plus simples que les sources, avec disparition des emplacements image / mentions de signature selon variantes.

Lecture blueprint :

- la structure logique est lisible, mais le rendu reste plus "memoire de spec" que "acte source" ;
- l'amelioration doit porter d'abord sur les blocs transverses : titre de section encadre, table de donnees bordee, liste juridique structuree, marqueur de partie a droite, grille de signatures.

### 5.4 Derogations coeur - formulaire multi-sites SEL

Source :

- marge haute plus compacte, environ `2,0 cm` ;
- titre en trois lignes centrees ;
- sections en gras et souligne ;
- nombreux retraits et listes Word ;
- plusieurs lignes en italique, notamment l'instruction d'envoi, des champs de temps hebdomadaire et une instruction de continuite des soins ;
- zones de formulaire avec blancs, cases et lignes a completer ;
- alternance de sections centrees, lignes en flux gauche et paragraphes justifies.

Genere :

- profil standard `2,5 cm` ;
- titre en trois lignes centrees conserve ;
- sections en gras, mais sans soulignement ;
- pas d'italique ;
- lignes de formulaire rendues en paragraphes simples ;
- tirets visibles conserves pour certaines zones, sans retraits Word ;
- blancs manuels visibles conserves.

Ecarts visibles :

- perte du soulignement des sections ;
- perte des italiques de consigne ;
- aplatissement des zones de formulaire en lignes simples ;
- perte des retraits et de la structure de liste source ;
- aspect "formulaire a completer" encore fonctionnel, mais peu proche de la source ordinale.

Lecture blueprint :

- l'objectif ne doit pas etre de finaliser juridiquement les zones manuelles ;
- il faut toutefois un rendu de formulaire plus structure : champs, retraits, cases et instructions.

### 5.5 Derogations coeur - cumul SELARL / BNC

Source :

- marge haute importante, environ `3,25 cm`, bas `2,0 cm` ;
- titre centre ;
- sections largement en gras + souligne ;
- nombreux retraits et listes Word ;
- plusieurs passages en italique ;
- deux tables 1 colonne encadrees : rappel de principe et pieces a joindre ;
- lignes de champs de formulaire structurees par retraits.

Genere :

- profil standard `2,5 cm` ;
- titre en trois lignes centrees ;
- quelques sections en gras, sans soulignement ;
- aucune table encadree ;
- aucune italique ;
- listes/cases rendues en texte courant ;
- champs manuels conserves sous forme de blancs visibles.

Ecarts visibles :

- perte des deux encadres structurants ;
- perte des soulignements et italiques ;
- perte des retraits de formulaire ;
- rendu plus lineaire, moins separable en rubriques ordinales ;
- pieces a joindre non mises en encadre source.

Lecture blueprint :

- correction prioritaire pour les formulaires : encadres, titres de rubriques, champs alignes et consignes en italique ;
- tant que les zones narratives restent manuelles, le rendu doit assumer le statut `formulaire_a_completer`.

## 6. Patterns communs

### 6.1 Encadres de titre et de section

Le Lot 03 utilise des tables encadrees pour autre chose que le titre principal :

- avenant bail : titre principal ;
- cession cabinets : titre principal et titres de grandes sections ;
- cumul SELARL / BNC : encadres de rappel et pieces a joindre.

Le rendu actuel sait produire un titre encadre principal, mais les encadres secondaires sont souvent remplaces par de simples paragraphes gras/soulignes.

### 6.2 Objets et en-tetes de lettres

L'appel de fonds montre le besoin de blocs de lettre :

- destinataire ou attention en italique ;
- objet en gras + souligne ;
- montant centre ;
- signature finale positionnee.

Ces besoins recoupent le blueprint batch V1 deja etabli pour les lettres.

### 6.3 Formulaires a completer

Les derogations ne sont pas de simples lettres. Elles ont besoin de blocs de formulaire :

- ligne libelle / valeur ;
- paires de champs sur une meme ligne ;
- cases a cocher ;
- blancs visibles ;
- retraits de zones de reponse ;
- consignes en italique ;
- encadres de rappel ou de pieces jointes.

### 6.4 Listes juridiques

Les sources cession et derogations utilisent des listes Word structurees. Le rendu from-scratch emploie souvent des tirets visibles.

Le tiret visible est acceptable pour une premiere restauration, mais il ne couvre pas tous les cas :

- listes juridiques de declarations ;
- listes de pieces ;
- listes de criteres avec cases ;
- annexes.

### 6.5 Signatures

Les signatures Lot 03 ont plusieurs formes :

- table 2 x 2 pour l'avenant bail ;
- signature simple de lettre pour appel de fonds ;
- lignes ou placeholders vendeur/acquereur dans les actes/compromis ;
- mentions manuscrites selon variante ;
- signature manuscrite attendue dans les formulaires.

Le rendu actuel est trop uniforme. Il faut choisir explicitement le bloc de signature par document.

### 6.6 Profils de marges

Le profil global `2,5 cm` est correct pour une partie du Lot 03, mais pas pour tout :

- avenant bail source : haut/bas plus compacts ;
- formulaire multi-sites : haut autour de `2,0 cm` ;
- cumul SELARL / BNC : haut autour de `3,25 cm` ;
- cession cabinets et appel de fonds : profil standard acceptable.

## 7. Blocs de rendu a ameliorer

Blocs existants a reutiliser ou consolider :

- `add_framed_title`
- `add_subject_heading`
- `add_letter_place_date`
- `add_right_aligned_lines`
- `add_right_indented_block`
- `add_company_identity_block`
- `add_italic_instruction`
- `add_hyphen_list_item`
- `add_signature_lines`
- `SydelDocxStyleProfile`

Blocs ou options a ajouter / specialiser :

- `add_framed_section_title(text)` : table 1 colonne encadree pour grandes sections cession ;
- `add_notice_box(lines)` : encadre de rappel ou pieces a joindre pour derogations ;
- `add_bordered_data_table(headers, rows)` : tableau de chiffres d'affaires avec bordures directes explicites ;
- `add_party_marker(text)` : libelle de partie aligne a droite, gras + souligne selon source ;
- `add_article_heading(text)` : article en gras + souligne, avec espacement controle ;
- `add_form_section_heading(text)` : rubrique de formulaire en gras + souligne ;
- `add_form_field(label, value_or_blank)` : ligne de formulaire libelle / valeur ;
- `add_form_field_pair(left_label, left_value, right_label, right_value)` : deux champs sur une ligne ;
- `add_checkbox_line(label, checked=False, indent=None)` : case et texte de formulaire ;
- `add_centered_amount(lines)` : montant et devise centre pour l'appel de fonds ;
- `add_signature_table(labels, rows, cols, bordered=True)` : table de signatures avenant / actes ;
- `add_signature_placeholder_lines(...)` : emplacements de signature sans les transformer en signature image ;
- profils de marges par famille : `standard_a4`, `bail_compact`, `derogation_form`, `derogation_cumul_top_heavy`.

## 8. Priorites de correction

### Priorite 1 - Restaurer les blocs de lettre de l'appel de fonds

Document concerne :

- `appel_fond_sel.docx`

Corrections :

- objet en gras + souligne ;
- attention/destinataire en italique si la source le demande ;
- montant centre ;
- signature finale positionnee ;
- eventuel retrait de banque si la revue humaine le juge utile.

Raison :

- correction limitee, faible risque metier, fort gain visuel.

### Priorite 2 - Restaurer les formulaires derogations

Documents concernes :

- `formulaire_derogation_sites_sel_formulaire_a_completer.docx`
- `demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx`

Corrections :

- rubriques gras + souligne ;
- consignes en italique ;
- champs de formulaire alignes ;
- cases a cocher ;
- encadres de rappel et pieces a joindre ;
- profils de marges dedies.

Raison :

- ces documents sont explicitement des formulaires a completer ; la structure visuelle porte le statut incomplet et evite de les faire lire comme lettres finalisees.

### Priorite 3 - Stabiliser l'avenant bail

Document concerne :

- `avenant_contrat_bail.docx`

Corrections :

- restaurer les libelles de parties a droite, gras + souligne ;
- restaurer le soulignement des articles ;
- poser des bordures directes sur la table de signatures ;
- envisager le profil de marges compact source.

Raison :

- le document est deja proche, mais les quelques marqueurs perdus sont tres visibles.

### Priorite 4 - Rehausser les actes et compromis de cession

Documents concernes :

- `acte_cession_cabinet_medical.docx`
- `compromis_cession_cabinet_medical.docx`
- `acte_cession_cabinet_dentaire.docx`
- `compromis_cession_cabinet_dentaire.docx`

Corrections :

- titres de section encadres pour les grandes sections ;
- table de chiffres d'affaires avec bordures directes ;
- marqueurs de parties a droite ;
- listes juridiques mieux structurees ;
- bloc signature par variante.

Raison :

- impact visuel important, mais surface documentaire plus large et risque de toucher beaucoup de blocs.

### Priorite 5 - Formaliser une politique de signatures Lot 03

Documents concernes :

- avenant bail ;
- appel de fonds ;
- cession cabinets ;
- derogations coeur.

Decision attendue :

- choisir document par document entre signature simple, table de signatures, grille, placeholders image et mention manuscrite ;
- ne pas activer une signature encadree ou image sans choix explicite de la spec ou de l'arbitrage.

## 9. Synthese operationnelle

Le Lot 03 confirme que la couche de rendu commune couvre deja les besoins de base : document propre, marges standard, titre encadre principal, paragraphes justifies, tirets visibles et signatures simples.

Les ecarts restants ne relevent pas d'une reecriture juridique. Ils relevent de blocs visuels transverses encore manquants ou insuffisamment utilises :

- encadres secondaires ;
- objets de lettre ;
- champs de formulaire ;
- cases a cocher ;
- tables bordees ;
- signatures par variante ;
- profils de marges par famille.

La prochaine correction de style devrait rester strictement documentaire et commencer par l'appel de fonds puis les formulaires derogations, avant de toucher aux actes/compromis de cession plus volumineux.
