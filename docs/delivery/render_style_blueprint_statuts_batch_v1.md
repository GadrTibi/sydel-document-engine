# DAAT x SYDEL - Blueprint de style statuts batch V1
## Ticket STYLE-ANALYSE-STATUTS-BATCH-001

## 1. Objet

Produire un blueprint de rendu pour les statuts generes from-scratch, sans chercher une copie Word parfaite au millimetre.

Le but est d'ameliorer la fidelite structurelle des statuts sur les axes suivants :

- titres et hierarchie ;
- gras, souligne, italique ;
- centrages ;
- signatures ;
- retraits et respiration ;
- tableaux et blocs structurants.

Ce document ne modifie aucun wording juridique. Il documente des ecarts visuels et structurels pour preparer des tickets de correction de rendu.

## 2. References lues

Memoire projet et cadrage :

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
- `docs/delivery/render_style_blueprint_batch_v1.md`

Specs et arbitrages statuts :

- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`

## 3. Sources et rendus compares

Sources Word Lot 04 :

- `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx`
- `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx`
- `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx`
- `project/source_documents/lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- `project/source_documents/lot_04/Modele statuts SELARL medecins.docx`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
- `project/source_documents/lot_04/Statuts_SCS_modele.docx`
- `project/source_documents/lot_04/Modele statuts SCI.docx`
- `project/source_documents/lot_04/Modele statuts SCI IRIS.docx`

Note : certains noms de fichiers source sont normalises sans accents pour la lisibilite. Les fichiers physiques conservent leurs noms exacts sur disque.

DOCX generes compares :

- `artifacts/lot_04_statuts_sas_smoke_test/statuts_sas_spfpl_medecins.docx`
- `artifacts/lot_04_statuts_spfpl_smoke_test/statuts_spfpl_cession.docx`
- `artifacts/lot_04_statuts_spfpl_smoke_test/statuts_spfpl_apport.docx`
- `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selarl_chirurgien_dentiste.docx`
- `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selarl_medecin.docx`
- `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selas_medecin.docx`
- `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_scs.docx`
- `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_sci.docx`
- `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_sci_iris.docx`

Note d'execution : les artefacts `statuts_civils_core` ont ete lus dans la worktree locale qui les contenait deja. Ils ne sont pas versionnes, conformement au fonctionnement habituel de `artifacts/`.

## 4. Methode

Analyse structurelle en lecture seule des DOCX avec extraction des elements suivants :

- marges de section ;
- paragraphes non vides ;
- alignements explicites ;
- styles de paragraphe ;
- runs en gras, italique et souligne ;
- listes Word via `numPr` ;
- tirets visibles ;
- retraits et retraits suspendus ;
- tables, bordures et contenus de cellules ;
- blocs de signature et d'annexe.

Cette analyse ne vaut pas validation juridique. Les ecarts de contenu ou de mention identifies au passage doivent rester des points de revue juridique separes, sans correction implicite dans un ticket de style.

## 5. Constat transversal

Les statuts generes conservent globalement l'ordre des paragraphes et la majorite des contenus structurants, mais la couche de rendu actuelle aplatit fortement la mise en page Word source.

Ecarts recurrents :

- les titres d'articles perdent presque toujours le souligne source ;
- les styles Word sources `Heading`, `Body Text`, `List Paragraph` et variantes sont remplaces par `Normal` ;
- les listes Word numerotees ou a retrait suspendu deviennent des paragraphes simples ou des tirets visibles ;
- les retraits fins, retraits suspendus et marges propres a certaines familles sont perdus ;
- les tableaux structurants des sources sont rarement reproduits ;
- les signatures perdent souvent le centrage, l'italique des mentions et les grilles a deux colonnes ;
- les annexes sont conservees textuellement mais moins lisibles visuellement ;
- la generation applique souvent le profil standard 2,5 cm partout, meme lorsque la source a une densite differente.

Lecture cible :

- ne pas revenir a un moteur template ;
- conserver la generation from-scratch ;
- ajouter des blocs de rendu statuts explicites et reutilisables ;
- activer les variantes de rendu par sous-famille, pas par deduction automatique du texte.

## 6. Ecarts par sous-famille

### 6.1 Statuts SAS

Source :

- marges standard 2,5 cm ;
- page de garde centree ;
- `STATUTS` centre et en gras ;
- articles en gras et soulignes ;
- paragraphes juridiques majoritairement justifies ;
- quelques listes Word avec retrait suspendu ;
- signature finale avec nom centre ;
- mention d'acceptation en italique ;
- annexe centree en gras.

Genere :

- marges conformes au standard 2,5 cm ;
- nombre de paragraphes proche de la source ;
- page de garde partiellement conservee ;
- articles en gras mais sans souligne ;
- listes Word source remplacees par paragraphes ou tirets visibles ;
- plusieurs alignements source `justify` deviennent des paragraphes sans alignement explicite ;
- signature finale rendue en flux gauche, sans italique sur la mention ;
- annexe encore centree et en gras.

Priorite SAS :

- restaurer le style `article_heading` avec gras + souligne ;
- restaurer les listes a retrait suspendu ;
- restaurer le bloc signature president avec nom centre et mention italique ;
- ne pas modifier les formulations heterogenes deja documentees dans la spec SAS.

### 6.2 Statuts SPFPL cession / apport

Source :

- marges tres atypiques par rapport au profil global : haut environ 2,82 cm, bas parfois 0 cm, marges laterales plus etroites ;
- page de garde centree ;
- titres d'articles en gras, parfois avec alignement gauche et retrait ;
- nombreux paragraphes justifies avec retraits source ;
- listes Word et retraits suspendus ;
- six tableaux 1 colonne bordes servant de grands intertitres :
  - `DECISIONS DES ACTIONNAIRES`
  - `RESULTATS SOCIAUX`
  - `TRANSFORMATION DE LA SOCIETE`
  - `DISSOLUTION - LIQUIDATION`
  - `CONTESTATIONS`
  - `CONSTITUTION DE LA SOCIETE`
- signature finale centree ;
- mention d'acceptation en italique ;
- annexe centree en gras.

Genere :

- profil global 2,5 cm applique ;
- grands intertitres rendus en paragraphes centres gras, sans tableau borde ;
- articles en gras mais sans restitution des retraits source ;
- listes Word non conservees comme listes Word ;
- signature et mention d'acceptation rendues en paragraphes justifies, sans italique ;
- annexe conservee et encore lisible.

Ecarts specifiques :

- l'apport et la cession ont le meme besoin de blocs structurants, mais pas necessairement les memes marges ;
- les grands intertitres bordes sont le marqueur visuel le plus fort perdu par le rendu actuel ;
- les signatures SPFPL doivent retrouver une variante `president_acceptance_signature`.

Priorite SPFPL :

- restaurer les tableaux d'intertitres bordes avant les ajustements fins de marge ;
- restaurer signature centree + mention italique ;
- ajouter un profil de marge `statuts_spfpl_source_like` seulement si la revue humaine confirme que la densite source est prioritaire.

### 6.3 Statuts SEL d'exercice

Sources :

- page de garde centree ;
- titre `STATUTS` en table dans les trois variantes, avec bordure visible pour SELARL dentiste et SELAS, et table sans bordure visible pour SELARL medecin ;
- nombreux articles en gras + soulignes ;
- SELARL dentiste : style source moins justifie, beaucoup de paragraphes en flux normal ;
- SELARL medecin et SELAS medecin : paragraphes majoritairement justifies ;
- listes Word presentes selon les variantes ;
- mentions finales souvent centrees et en italique ;
- annexe centree en gras ou structuree selon source.

Generes :

- les tables de titre disparaissent ;
- seuls quelques paragraphes de page de garde restent centres ;
- les articles sont rendus en gras mais perdent le souligne ;
- tous les styles sont aplatis en `Normal` ;
- les listes Word sont transformees en paragraphes simples ;
- les signatures sont rendues sans bloc dedie fort ;
- l'italique des mentions finales est souvent perdu.

Ecarts specifiques :

- SELARL dentiste perd fortement son caractere source, car la source n'est pas aussi uniformement justifiee que le rendu genere ;
- SELARL medecin et SELAS restent plus proches dans le flux de corps, mais perdent le soulignement des articles ;
- les mentions de signature doivent etre relues comme point juridique separe si leur texte differe de la source ; le ticket style ne doit pas corriger ce wording.

Priorite SEL :

- creer un bloc `statuts_title_box` avec variantes `bordered` et `unbordered`;
- restaurer `article_heading` gras + souligne ;
- restaurer les mentions finales centrees et italiques ;
- conserver une politique d'alignement par overlay au lieu de justifier toute la famille uniformement.

### 6.4 Statuts civils core : SCS, SCI, SCI IRIS

Sources SCS :

- page de garde centree ;
- titre `STATUTS` en table bordee ;
- titres `TITRE` et articles en gras ;
- listes Word avec retraits suspendus ;
- signature finale en table 2 colonnes, avec mention `Lu et approuve` en italique ;
- annexe centree en gras.

Genere SCS :

- table de titre supprimee ;
- `TITRE` rendu centre et gras, ce qui reste lisible ;
- articles en gras mais sans conservation des retraits source ;
- listes Word aplaties ;
- signature empilee en paragraphes, sans table 2 colonnes ni italique ;
- annexe en flux justifie plutot que centre.

Sources SCI / SCI IRIS :

- marges proches mais non identiques au profil global : haut environ 2,79 cm, bas environ 1,91 cm, gauche environ 2,36 cm, droite environ 2,19 cm ;
- page de garde centree ;
- articles en style `Heading 1`, soulignes, avec retraits ;
- nombreux paragraphes avec retraits ou retraits suspendus ;
- listes Word structurees ;
- signatures avec lignes de noms soulignees / en gras selon source ;
- annexe centree ;
- SCI IRIS contient un tableau 4 lignes x 2 colonnes pour les groupes de parts et quotes-parts de resultat exceptionnel.

Generes SCI / SCI IRIS :

- profil standard 2,5 cm partout ;
- page de garde moins centree ;
- articles en gras mais sans souligne ni retrait ;
- listes Word remplacees par paragraphes simples ;
- signatures simplifiees en noms centres ;
- annexe rendue en flux justifie ;
- SCI IRIS transforme le tableau de quotes-parts en lignes simples.

Priorite civils core :

- restaurer le style `civil_article_heading` avec souligne et indentation minimale ;
- restaurer la table de signature SCS ;
- restaurer le tableau SCI IRIS des groupes de parts ;
- ajouter un bloc `civil_signature_lines` qui conserve les noms centres mais peut appliquer gras / souligne selon source ;
- ajuster les marges SCI seulement apres revue humaine de pagination.

## 7. Patterns communs a formaliser

### 7.1 Page de garde statuts

Pattern :

- denomination ;
- forme sociale ;
- capital ;
- siege ;
- titre `STATUTS`.

Besoin :

- lignes centrees compactes ;
- titre final en table bordee, table non bordee ou paragraphe centre selon sous-famille ;
- espacement vertical controle avant la comparution.

### 7.2 Titre `STATUTS` en table

Variantes observees :

- table bordee simple : SELARL dentiste, SELAS, SCS ;
- table sans bordure visible : SELARL medecin ;
- pas de table : SAS ;
- grands intertitres bordes : SPFPL.

Besoin :

- helper distinct de `add_framed_title`, car les statuts ne veulent pas toujours un cartouche Lot 1 ;
- largeur, bordure, graisse et espacement configurables.

### 7.3 Titre d'article

Pattern majoritaire :

- libelle article en gras ;
- souligne frequent dans SAS, SEL, SCI et SCI IRIS ;
- alignement source parfois justifie, gauche ou sans alignement explicite ;
- espace avant notable.

Besoin :

- `add_statuts_article_heading(text, underline=True, alignment=None, indent_profile=None)` ;
- ne pas transformer automatiquement la casse ni la ponctuation.

### 7.4 Titre de partie / grand intertitre

Pattern :

- `TITRE I`, `TITRE II`, etc. dans les statuts civils ;
- grands intertitres bordes dans SPFPL.

Besoin :

- variante paragraphe centre gras ;
- variante table 1 colonne bordee ;
- espacement avant/apres distinct des articles.

### 7.5 Paragraphe juridique avec retraits

Pattern :

- sources longues avec retraits gauches, retraits premiere ligne ou retraits suspendus ;
- rendu genere tres plat avec `space_after` uniforme.

Besoin :

- profils de paragraphes par famille : `statuts_body`, `statuts_body_indented`, `statuts_body_hanging`;
- ne pas forcer la justification lorsque la source d'un overlay est en flux normal.

### 7.6 Liste statuts

Pattern :

- listes Word `numPr` dans SAS, SPFPL, SELAS, SCS, SCI et SCI IRIS ;
- certaines listes visibles en tirets simples.

Besoin :

- helper de liste a retrait suspendu stable ;
- option `marker="- "` pour conserver les tirets visibles source ;
- option future pour utiliser de vraies listes Word si le rendu cible le demande.

### 7.7 Signature statuts

Variantes observees :

- nom centre simple ;
- mention manuscrite en italique ;
- table 2 colonnes pour plusieurs signataires SCS ;
- noms centres soulignes / gras dans SCI et SCI IRIS ;
- bloc president avec mention d'acceptation.

Besoin :

- `add_statuts_signature_block`;
- variantes `single_centered`, `multi_centered_lines`, `two_column_grid`, `president_acceptance`;
- support de mention italique ;
- support de gras / souligne par ligne ;
- aucune invention de mention manuscrite.

### 7.8 Annexe statuts

Pattern :

- `ANNEXE` ou `ANNEXE 1` centre en gras ;
- titre d'annexe centre en gras ;
- liste d'actes ou engagements ;
- parfois paragraphes simples, parfois tirets.

Besoin :

- bloc `add_statuts_annex_heading`;
- bloc `add_statuts_annex_items`;
- alignement par sous-famille.

### 7.9 Tableau structurant

Tables source importantes :

- titre `STATUTS` ;
- grands intertitres SPFPL ;
- signatures SCS ;
- tableau SCI IRIS des groupes de parts et quote-parts.

Besoin :

- helper table 1 colonne bordee ;
- helper table signature 2 colonnes ;
- helper table simple avec en-tete pour donnees structurees ;
- controle des bordures sans dependre du style Word par defaut.

## 8. Blocs de rendu recommandes

Blocs existants a conserver ou etendre :

- `add_paragraph`
- `add_centered_block`
- `add_hyphen_list_item`
- `add_framed_title`
- `add_signature_lines`

Blocs nouveaux ou variantes a ajouter :

- `add_statuts_cover_block(lines, title_mode)`
- `add_statuts_title_box(text, bordered=True)`
- `add_statuts_article_heading(text, underline=True, space_before_pt=10)`
- `add_statuts_part_heading(text, mode="paragraph" | "boxed")`
- `add_statuts_body_paragraph(text, alignment, indent_profile)`
- `add_statuts_hanging_list_item(text, marker=None)`
- `add_statuts_signature_block(signers, variant, mention_lines=None)`
- `add_statuts_signature_grid(signers, columns=2, mention=None)`
- `add_statuts_annex_heading(title, subtitle=None)`
- `add_statuts_annex_items(items, marker="-")`
- `add_statuts_matrix_table(headers, rows, bordered=True)`
- `SydelDocxStyleProfile` variantes `statuts_standard`, `statuts_spfpl_compact`, `statuts_civil_compact`.

Option technique transversale :

- permettre des runs multiples dans un meme paragraphe pour preserver les portions en gras, italique ou souligne sans decouper artificiellement le texte.

## 9. Priorites de correction

### Priorite 1 - Restaurer la hierarchie des titres

Documents concernes :

- tous les statuts du batch.

Corrections :

- articles en gras + souligne lorsque la source l'impose ;
- `TITRE` civils en bloc distinct ;
- grands intertitres SPFPL en table bordee ;
- titre `STATUTS` selon la variante source.

### Priorite 2 - Restaurer les signatures

Documents concernes :

- SAS ;
- SPFPL cession / apport ;
- SEL d'exercice ;
- SCS ;
- SCI / SCI IRIS.

Corrections :

- centrage des noms ;
- italique des mentions ;
- grille 2 colonnes SCS ;
- gras / souligne des noms lorsque source ;
- bloc president avec mention d'acceptation.

### Priorite 3 - Restaurer les listes et retraits

Documents concernes :

- SAS ;
- SPFPL ;
- SELAS ;
- SCS ;
- SCI ;
- SCI IRIS.

Corrections :

- listes a retrait suspendu ;
- retraits de paragraphes juridiques ;
- eviter l'aplatissement systematique en paragraphes sans indentation.

### Priorite 4 - Restaurer les tableaux structurants

Documents concernes :

- SPFPL cession / apport ;
- SCS ;
- SCI IRIS ;
- SEL d'exercice selon le titre.

Corrections :

- tables 1 colonne bordees pour intertitres ;
- table de signature SCS ;
- table SCI IRIS des groupes de parts ;
- tables de titre `STATUTS`.

### Priorite 5 - Ajuster marges et respiration

Documents concernes :

- surtout SPFPL et statuts civils.

Corrections :

- ne pas appliquer aveuglement 2,5 cm partout ;
- creer des profils de famille ;
- valider humainement la densite avant de chercher a rapprocher les marges source, notamment quand la source a des marges atypiques.

## 10. Points de vigilance

- Toute correction de wording observee pendant la revue style doit etre traitee dans un ticket juridique ou texte separe.
- Les tables source ne doivent pas pousser a revenir a un template DOCX ; elles doivent etre reconstruites from-scratch.
- Les differences de marges peuvent etre des artefacts de source ; elles doivent etre corrigees seulement si elles ameliorent la lisibilite ou la pagination.
- Les signatures sont sensibles : le rendu peut etre ameliore, mais les mentions manuscrites exactes doivent venir des specs et arbitrages.
- Les blocs SEL, SPFPL, SAS et civils ne doivent pas etre fusionnes par similarite visuelle.

## 11. Synthese operationnelle

Le batch statuts confirme que le moteur from-scratch produit des DOCX propres et ordonnes, mais avec un rendu encore trop plat pour des statuts longs.

La prochaine correction de style devrait se concentrer sur des helpers statuts transverses, dans cet ordre :

1. titres et intertitres ;
2. signatures ;
3. listes et retraits ;
4. tableaux structurants ;
5. profils de marges.

Cette approche permet d'ameliorer fortement la fidelite structurelle sans modifier le wording juridique et sans abandonner la generation from-scratch.
