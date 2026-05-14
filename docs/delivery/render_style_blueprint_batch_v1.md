# DAAT x SYDEL - Blueprint de style batch V1
## Ticket STYLE-ANALYSE-BATCH-001

## 1. Objet

Produire un blueprint de style exploitable pour la génération DOCX from-scratch, sans viser une copie Word parfaite au millimètre.

Le but est de formaliser les éléments de structure visuelle importants observés sur un batch de sources et de DOCX générés :

- alignements gauche / droite / centre ;
- gras, souligné, italique ;
- listes avec tirets ou retraits structurants ;
- titres et intertitres ;
- espacements, retraits et profils de marges ;
- blocs de signature et mentions manuscrites.

Ce document ne modifie aucun wording juridique. Il formalise uniquement des écarts et recommandations de rendu.

## 2. Références lues

Mémoire projet et cadrage :

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0004-from-scratch-docx-generation.md`
- `docs/adr/0005-codex-working-mode.md`
- `docs/delivery/render_style_system_v1.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`

Sources DOCX analysées :

- `project/source_documents/lot_01/declaration_non_condamnation_transforme.docx`
- `project/source_documents/lot_01/autorisation_domiciliation_transforme.docx`
- `project/source_documents/lot_01/procuration_transforme.docx`
- `project/source_documents/lot_02/PV nomination gérant - transforme.docx`
- `project/source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx`
- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_documents/lot_02/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`

DOCX générés comparés :

- `artifacts/render_style_001_lot_01_smoke_test/declaration_non_condamnation.docx`
- `artifacts/render_style_001_lot_01_smoke_test/autorisation_domiciliation.docx`
- `artifacts/render_style_001_lot_01_smoke_test/procuration.docx`
- `artifacts/fix_pv_render_001_smoke_test_2/pv_nomination_gerant.docx`
- `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`
- `artifacts/lot_02_regime_communautaire_smoke_test/lettre_renonciation_associe.docx`
- `artifacts/lot_02_regime_communautaire_smoke_test/lettre_avertissement_conjoint.docx`

Note : des artefacts historiques ou orchestrateur existent aussi dans `artifacts/`. La comparaison détaillée retient les rendus les plus récents ou les plus représentatifs de l'état courant de la couche de rendu.

## 3. Méthode

Analyse structurelle en lecture seule des DOCX avec extraction des éléments suivants :

- marges de section ;
- paragraphes non vides ;
- alignements explicites ;
- styles de paragraphe ;
- runs en gras, italique et souligné ;
- listes Word via `numPr` ;
- tirets visibles ;
- retraits et retraits suspendus ;
- tables, bordures et premiers contenus de cellule.

Cette analyse est volontairement orientée rendu. Elle ne valide ni le wording juridique, ni le contenu métier.

## 4. Écarts par document

### DOC-001 - Déclaration de non-condamnation

Source :

- marges homogènes à 2,5 cm ;
- titre encadré en table, avec deux lignes centrées et en gras ;
- bloc identité en lignes courtes ;
- paragraphe de déclaration justifié et en gras ;
- bloc `Rappel` en italique, avec le libellé `Rappel` souligné ;
- signature positionnée à droite dans la source sans table de signature distincte.

Généré :

- marges conformes au profil global 2,5 cm ;
- titre encadré présent ;
- déclaration justifiée et en gras conservée ;
- rappel légal en italique et `Rappel` souligné conservés ;
- signature rendue dans un bloc encadré commun à droite.

Écarts visibles :

- le titre généré est porté par un seul paragraphe de cellule avec saut de ligne, alors que la source expose deux paragraphes de titre distincts ;
- le bloc signature généré est encadré, ce qui standardise la signature mais diffère de la source transformée ;
- le bloc de signature généré contient lieu/date dans la cellule, mais pas le nom du signataire lorsque l'image de signature est absente.

Lecture blueprint :

- DOC-001 est globalement proche de la cible style ;
- conserver le cartouche encadré, le paragraphe justifié gras et le rappel légal ;
- clarifier si la signature encadrée est un choix projet systématique pour Lot 1 ou une surcharge par document.

### DOC-002 - Autorisation de domiciliation

Source :

- marges homogènes à 2,5 cm ;
- titre encadré centré en gras ;
- paragraphe unique justifié ;
- lieu, date et signataire positionnés visuellement vers la droite par retraits, sans table de signature encadrée.

Généré :

- titre encadré conservé ;
- paragraphe unique justifié conservé ;
- signature rendue dans un bloc encadré à droite.

Écarts visibles :

- la source utilise un positionnement droit par retraits, tandis que le généré utilise un bloc encadré ;
- le nom du signataire est intégré au bloc encadré ;
- le passage à une signature encadrée est cohérent avec le render style system V1, mais doit rester une décision explicite.

Lecture blueprint :

- le rendu généré est acceptable pour une approche standardisée ;
- le besoin à formaliser est moins une correction DOC-002 qu'une règle d'activation des signatures encadrées.

### DOC-003 - Procuration

Source :

- titre encadré centré en gras ;
- premier paragraphe légèrement indenté ;
- paragraphes de mandat justifiés ;
- bloc mandataire centré ;
- `SYDEL` en gras ;
- adresse, RCS et téléphone du mandataire en italique ;
- date en italique côté gauche ;
- nom du signataire décalé à droite par retrait.

Généré :

- titre encadré conservé ;
- bloc mandataire centré conservé ;
- `SYDEL` en gras et lignes mandataire en italique conservés ;
- paragraphes de mandat justifiés conservés ;
- signature rendue dans un bloc encadré à droite.

Écarts visibles :

- le premier paragraphe généré n'a plus le léger retrait source ;
- la date et le nom de signature ne reprennent plus la logique source italique gauche / nom à droite, car ils passent dans un bloc signature encadré ;
- l'introduction générée n'est pas explicitement justifiée, contrairement à plusieurs paragraphes source.

Lecture blueprint :

- le bloc mandataire est un bon candidat de standardisation déjà assez bien rendu ;
- ajouter une règle `intro_justified_or_indented` si la revue humaine demande de préserver le retrait source ;
- clarifier la règle de signature encadrée pour les procurations.

### PV nomination gérant

Source :

- marges plus compactes que le profil global, environ 2,25 cm en haut et 1,35 cm en bas ;
- en-tête société centré, première ligne en gras ;
- titre principal dans une table sans bordure visible, centré et en gras ;
- listes Word avec retraits suspendus pour associés et ordre du jour ;
- titres de décisions en gras et soulignés ;
- formules de vote en italique ;
- nombreuses lignes justifiées ;
- signatures finales en table 2 colonnes, centrées et en gras ;
- mention d'acceptation centrée en italique.

Généré :

- marges globales 2,5 cm ;
- en-tête société centré conservé ;
- titre principal rendu en cartouche encadré ;
- listes rendues avec tiret visible et retrait suspendu ;
- titres de décisions gras + soulignés conservés ;
- formules de vote en italique conservées ;
- signatures rendues comme lignes centrées verticales, sans table en colonnes ;
- mention d'acceptation centrée en italique conservée.

Écarts visibles :

- le titre généré est encadré alors que la source PV utilise une table sans bordure visible ;
- les listes source sont des listes Word structurées, le généré utilise des tirets visibles ;
- les signatures source sont en grille 2 colonnes, le généré empile les noms ;
- les marges générées sont moins compactes que la source, ce qui peut impacter la pagination.

Lecture blueprint :

- les décisions, votes et listes ont déjà un bon niveau de restauration structurelle ;
- créer ou décider un bloc de titre PV distinct du cartouche Lot 1 si l'encadré est jugé trop fort ;
- ajouter un bloc `signature_grid` pour les PV multi-associés ;
- prévoir un profil de marges compact pour PV si la densité visuelle devient prioritaire.

### Demande d'inscription à l'ordre

Source :

- expéditeur en haut à gauche ;
- destinataire Conseil de l'Ordre décalé fortement vers la droite par retraits ;
- lieu/date alignés à droite ;
- objet en gras et souligné ;
- corps principal justifié ;
- signature finale alignée à droite.

Généré :

- expéditeur et destinataire rendus en flux gauche ;
- lieu/date rendu en flux gauche ;
- objet rendu en texte standard, sans gras ni souligné ;
- corps principal justifié ;
- signature finale rendue en flux gauche.

Écarts visibles :

- perte nette des alignements droite et retraits structurants ;
- perte du gras/souligné de l'objet ;
- signature finale non alignée à droite ;
- adresse ordinale éclatée en lignes utiles mais sans positionnement visuel destinataire.

Lecture blueprint :

- document prioritaire pour restaurer les blocs `recipient_right_indent`, `letter_place_date_right`, `subject_heading` et `signature_right`;
- les paragraphes de corps justifiés sont globalement bien traités.

### Régime communautaire - Lettre de renonciation

Source :

- marges latérales plus larges que le profil global, environ 3,17 cm ;
- lieu et date alignés à droite ;
- objet en gras et souligné ;
- corps en paragraphes simples ;
- ligne `En ... exemplaires` alignée à gauche ;
- signature conjoint alignée à droite.

Généré :

- marges globales 2,5 cm ;
- lieu/date en flux gauche ;
- objet en texte standard, sans gras ni souligné ;
- paragraphes principaux justifiés ;
- ligne `En ... exemplaires` en flux gauche ;
- signature conjoint en flux gauche.

Écarts visibles :

- perte des alignements droite pour lieu/date et signature ;
- perte du gras/souligné de l'objet ;
- changement de profil de marges ;
- justification des paragraphes longs, acceptable si assumée par le profil commun, mais différente de la source.

Lecture blueprint :

- restaurer les blocs de lettre courte avant toute revue humaine fine ;
- prévoir un profil de lettre à marges latérales élargies si la densité source doit être préservée.

### Régime communautaire - Lettre d'avertissement au conjoint

Source :

- marges latérales environ 3,17 cm ;
- bloc société expéditrice centré, première ligne en gras ;
- bloc conjoint destinataire et date alignés à droite ;
- objet en gras, souligné, aligné à gauche ;
- reprise des caractéristiques société centrée, première ligne en gras ;
- ligne d'apport en liste à tiret ;
- bloc apporteur en italique ;
- instruction de mention manuscrite en italique.

Généré :

- marges globales 2,5 cm ;
- bloc société expéditrice rendu en flux gauche ;
- destinataire/date rendus en flux gauche ;
- objet sans gras ni souligné ;
- reprise société rendue en flux gauche ;
- liste à tiret conservée avec retrait suspendu ;
- bloc apporteur non italique ;
- instruction manuscrite non italique.

Écarts visibles :

- perte importante des centrages structurants ;
- perte des alignements droite du destinataire et de la date ;
- perte du gras/souligné de l'objet ;
- perte de l'italique sur le bloc apporteur et l'instruction manuscrite ;
- seule la liste à tiret est bien structurée dans le généré.

Lecture blueprint :

- c'est le document du batch avec le plus fort écart visuel ;
- prioriser la restauration des blocs `centered_company_block`, `recipient_right_block`, `subject_heading`, `italic_instruction` et `hyphen_list_item`.

## 5. Patterns communs à formaliser

### 5.1 Cartouche de titre encadré

Déjà utile pour DOC-001, DOC-002 et DOC-003.

Règles proposées :

- table 1 colonne avec bordure noire ;
- contenu centré et en gras ;
- lignes de titre traitées comme lignes sémantiques distinctes ;
- espacement contrôlé après le cartouche ;
- activation document par document, car le PV source semble plutôt utiliser un titre centré sans bordure visible.

### 5.2 Titre centré sans bordure

Nécessaire pour les PV ou documents qui n'attendent pas un cartouche.

Règles proposées :

- une ou plusieurs lignes centrées ;
- gras configurable ;
- espace avant/après compact ;
- pas de bordure ;
- compatible avec sous-titre ou date de décision.

### 5.3 Objet de lettre

Récurrent dans Demande d'inscription à l'ordre et batch régime communautaire.

Règles proposées :

- paragraphe aligné à gauche ;
- gras et souligné par défaut ;
- espacement avant/après dédié ;
- aucune transformation du texte.

### 5.4 Bloc expéditeur gauche

Nécessaire pour Demande d'inscription à l'ordre et certaines lettres.

Règles proposées :

- lignes en flux gauche ;
- espacement compact entre lignes ;
- possibilité de rendre une adresse sur plusieurs lignes ;
- pas de gras automatique sauf première ligne explicitement demandée.

### 5.5 Bloc destinataire à droite ou indenté

Nécessaire pour Demande d'inscription à l'ordre et lettre d'avertissement.

Règles proposées :

- support de lignes alignées à droite ;
- support de lignes décalées par retrait gauche important lorsque la source n'utilise pas un alignement droite strict ;
- espacement compact ;
- option de bloc adresse multi-lignes.

### 5.6 Lieu/date à droite

Nécessaire pour Demande d'inscription à l'ordre et renonciation.

Règles proposées :

- paragraphe aligné à droite ;
- format texte fourni par le générateur ;
- pas de formatage métier dans le helper ;
- option de double espace source si le document le demande explicitement.

### 5.7 Bloc société centré

Nécessaire pour PV et lettre d'avertissement.

Règles proposées :

- lignes centrées compactes ;
- première ligne en gras optionnel ;
- variantes sans gras pour lignes de forme sociale, capital et adresse ;
- bloc réutilisable pour en-tête principal et rappel des caractéristiques société.

### 5.8 Paragraphes juridiques justifiés

Utile et déjà largement présent.

Règles proposées :

- alignement justifié pour paragraphes longs ;
- espacement après standard ;
- ne pas justifier mécaniquement les lignes courtes de signature, date, objet ou adresse.

### 5.9 Liste à tiret avec retrait suspendu

Nécessaire pour PV et lettre d'avertissement.

Règles proposées :

- tiret visible `- ` ;
- retrait gauche et retrait suspendu contrôlés ;
- alignement justifié optionnel pour les items longs ;
- pas de conversion automatique de toutes les listes Word sources : le générateur choisit le bloc.

### 5.10 Intertitre de décision

Nécessaire pour PV.

Règles proposées :

- paragraphe en gras + souligné ;
- espace avant contrôlé ;
- pas de numérotation Word automatique ;
- texte déjà fourni par le générateur.

### 5.11 Formule de vote italique

Nécessaire pour PV.

Règles proposées :

- paragraphe italique ;
- espacement compact ou standard selon densité ;
- pas de variation de wording.

### 5.12 Signature simple à droite

Nécessaire pour lettres.

Règles proposées :

- nom/signature finale aligné à droite ;
- possibilité de conserver un bloc lieu/date séparé ;
- sans cadre par défaut.

### 5.13 Signature encadrée

Déjà disponible dans la couche commune, utile pour les signatures Lot 1 si validé.

Règles proposées :

- activation explicite par document ;
- hauteur minimale suffisante si aucune image de signature n'est fournie ;
- lignes internes alignées à gauche ;
- position du bloc configurable : droite, gauche, centré ou pleine largeur.

### 5.14 Grille de signatures

Nécessaire pour PV multi-associés.

Règles proposées :

- table sans bordure visible ;
- 2 colonnes par défaut si plusieurs signataires ;
- noms centrés et en gras ;
- ligne de mention manuscrite centrée en italique sous la grille ;
- option de repli en une colonne pour un seul signataire.

### 5.15 Instruction manuscrite en italique

Nécessaire pour PV et lettre d'avertissement.

Règles proposées :

- paragraphe italique ;
- alignement configurable : centré pour PV, gauche pour lettre d'avertissement ;
- texte fourni par le générateur ou la spec ;
- aucune invention de mention manuscrite.

### 5.16 Profils de marges par famille

Le profil global 2,5 cm fonctionne pour Lot 1 et Demande d'inscription à l'ordre, mais pas pour tous les documents observés.

Profils à envisager :

- `standard_a4` : 2,5 cm partout ;
- `letter_wide_margins` : environ 3,17 cm gauche/droite pour les lettres régime communautaire ;
- `pv_compact` : top environ 2,25 cm, bottom environ 1,35 cm, si la densité du PV source doit être mieux respectée.

## 6. Blocs de rendu recommandés

Blocs déjà présents à consolider :

- `add_framed_title`
- `add_centered_block`
- `add_paragraph`
- `add_hyphen_list_item`
- `add_signature_block`
- `add_framed_signature_block`
- `add_signature_lines`
- `add_legal_reminder`

Blocs ou options à ajouter en priorité :

- `add_subject_heading(text)` : objet gras + souligné ;
- `add_right_aligned_lines(lines)` : dates, signatures finales et destinataires simples ;
- `add_right_indented_block(lines, left_indent_cm)` : destinataire type Conseil de l'Ordre ;
- `add_letter_place_date(text, alignment=right)` ;
- `add_company_identity_block(lines, first_line_bold=True, alignment=center)` ;
- `add_decision_heading(text)` : gras + souligné + espacement avant ;
- `add_italic_instruction(text, alignment)` ;
- `add_signature_grid(names, columns=2, bordered=False)` ;
- `SydelDocxStyleProfile` avec surcharges de marges par famille documentaire ;
- option `alignment`, `bold`, `italic`, `underline` systématique sur les helpers de blocs, pas seulement sur les paragraphes unitaires.

## 7. Priorités de correction

### Priorité 1 - Restaurer les lettres qui ont perdu leur structure gauche/droite

Documents concernés :

- Demande d'inscription à l'ordre ;
- Lettre de renonciation ;
- Lettre d'avertissement.

Corrections :

- lieu/date à droite ;
- signature finale à droite ;
- destinataire à droite ou indenté ;
- objet gras + souligné.

### Priorité 2 - Restaurer les centrages et italiques du batch régime communautaire

Documents concernés :

- surtout Lettre d'avertissement.

Corrections :

- bloc société centré en haut ;
- rappel des caractéristiques société centré ;
- destinataire/date à droite ;
- bloc apporteur en italique si la source l'exige ;
- instruction manuscrite en italique.

### Priorité 3 - Stabiliser la politique de signatures

Documents concernés :

- DOC-001 ;
- DOC-002 ;
- DOC-003 ;
- PV nomination gérant ;
- lettres régime communautaire.

Décisions attendues :

- quels documents utilisent une signature encadrée ;
- quels documents restent en signature simple à droite ;
- comment rendre les signatures multiples du PV : grille sans bordure ou liste centrée ;
- hauteur minimale et contenu des cadres lorsque l'image de signature est absente.

### Priorité 4 - Stabiliser les titres PV vs cartouches Lot 1

Documents concernés :

- PV nomination gérant ;
- DOC-001 à DOC-003.

Corrections :

- conserver le cartouche encadré pour Lot 1 ;
- décider si le PV doit rester en titre centré sans bordure ou garder le cartouche encadré issu de la correction récente ;
- séparer les lignes de titre comme unités sémantiques, même si le rendu visuel reste proche.

### Priorité 5 - Ajuster les profils de marges et espacements

Documents concernés :

- PV nomination gérant ;
- batch régime communautaire.

Corrections :

- ajouter des profils de marge par famille ;
- éviter que le profil global 2,5 cm n'aplatisse les lettres à marges larges ;
- contrôler l'espacement avant/après des objets, signatures et blocs centrés.

## 8. Synthèse opérationnelle

Le batch confirme que la couche commune existe déjà, mais qu'elle reste trop centrée sur les besoins Lot 1 et PV. Les documents de type lettre font apparaître un besoin prioritaire de blocs sémantiques de mise en page :

- bloc objet ;
- bloc destinataire à droite ou indenté ;
- bloc lieu/date à droite ;
- bloc société centré ;
- signature simple à droite ;
- instruction manuscrite italique.

Le prochain ticket de rendu devrait donc éviter de retoucher les textes et se concentrer sur ces blocs transverses, puis migrer en priorité :

1. `Demande d'inscription à l'ordre` ;
2. `Lettre d'avertissement au conjoint` ;
3. `Lettre de renonciation` ;
4. signatures PV ;
5. politique de signatures encadrées Lot 1.
