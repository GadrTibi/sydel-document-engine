# Rapport FRONT-REALITY-CHECK-001

Date : 2026-05-25

## 1. Objet

Audit de realite du nouveau front global apres les debriefs recents. Le but est
de verifier ce qui est vraiment visible, ce qui est vraiment branche cote
generation, et ce qui doit etre coupe avant tout push, redeploiement ou test
utilisateur.

Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a
ete modifie.

## 2. Etat Git observe

Commandes demandees :

- `git status --short --branch` : `## main...origin/main` avec
  `?? docs/docssource_truth/` au demarrage du ticket.
- `git branch -vv` : branche courante `main` sur `4744904 [origin/main]
  fix: hard-cut front ui to user essentials`. Le depot conserve de nombreuses
  branches locales `codex/*`, dont plusieurs liees a d'anciens worktrees.
- `git log --oneline -15` :
  - `4744904 fix: hard-cut front ui to user essentials`
  - `42e2e93 fix: simplify front ui for real user testing`
  - `aa9e5ee feat: add front generation actions foundation`
  - `24aa90c feat: add front dossier data entry foundation`
  - `9ed9f93 feat: add front dossier editor foundation`
  - `1879363 feat: add front ui shell foundation`
  - `a335252 docs: review prototype front against new foundations`
  - `79e96b2 feat: realign front test prefill on data layer`
  - `643eaf9 feat: add front unit document mode foundation`
  - `bbd5bec feat: add front document status layer foundation`
  - `f8b10a4 feat: add front dossier flow foundation`
  - `9d8dee7 feat: refine front address model foundation`
  - `2411ef6 feat: refine front role model foundation`
  - `37de45a feat: add front data layer foundation`
  - `c745dfa docs: add global front architecture QA checks`

Pendant l'audit, des changements de pilotage non committes lies a
`FRONT-STATE-AUDIT-001` etaient deja presents dans le worktree. Ils sont
conserves et completes, sans rollback.

## 3. Etat reel visible du nouveau front

Le chemin "Nouveau front global > Dossier" est maintenant un chemin de code, pas
une navigation visible. La page normale appelle directement
`_render_target_front_shell()`, puis `_render_target_front_dossier()`.

Inventaire AppTest de la vue normale :

- sous-titres visibles : `Type de dossier`, `Donnees a saisir`, `Generation` ;
- sidebar visible : checkbox `Outils internes` ;
- selectbox visible : `Type de dossier / structure de base` ;
- selectbox disponibles dans les champs : `Civilite`, `Genre grammatical`,
  `Forme sociale` ;
- checkbox visibles : `Dossier unipersonnel`, `Domiciliation = siege social`,
  plus `Outils internes` en sidebar ;
- sous-zones de saisie visibles : expanders ouverts `Personne principale`,
  `Societe principale`, `Capital, decision et signature` ;
- champs texte visibles : 22 ;
- boutons visibles : `Generer les DOCX`, `Generer le ZIP`, `Generer les PDF` ;
- metriques visibles : `Prets a generer`, `Bloques` ;
- tableaux visibles par defaut : 0 ;
- radios visibles par defaut : 0.

Le selecteur de type de dossier n'expose en pratique qu'un profil :

- `SELARL creation simple`.

Les autres profils existent dans `front_dossier_editor.py`, mais ils ne sont pas
affiches dans la surface normale parce que `front_dossier_entry_is_supported(...)`
filtre la liste aux profils saisissables.

## 4. Sous-zones et pollution encore visibles

La promesse "trois zones" est vraie techniquement, mais la zone de saisie reste
chargee :

- trois expanders ouverts par defaut fonctionnent comme des sous-zones ;
- 22 champs texte sont visibles pour un seul profil pilote ;
- le libelle technique `Domiciliation = siege social` reste acceptable, mais la
  caption expose encore `ReuseRuleState`, qui est du vocabulaire interne ;
- le bouton `Generer les PDF` reste visible meme quand le backend PDF local est
  indisponible ;
- les metriques `Prets a generer` / `Bloques` sont visibles, mais les raisons de
  blocage ne le sont pas dans la surface normale ;
- la sidebar affiche `Outils internes`, ce qui rappelle encore le chantier de
  rebuild dans une session utilisateur normale ;
- une caption finale indique que les artefacts vont dans `artifacts/`, ce qui est
  utile a l'equipe mais pas necessaire pour un testeur produit.

Quand `Outils internes` est active, les outils suivants reapparaissent :

- `Assistant metier prototype` ;
- `Document unitaire` ;
- `Technique / diagnostic` ;
- `Debug interne`.

`Debug interne` affiche des tables de diagnostic : `DossierRecord`, objets data,
roles, adresses, statuts de generation et garde-fous. Elles ne polluent pas la
vue normale, mais l'entree vers ces outils reste visible en sidebar.

## 5. Etat reel des actions de generation

La generation du nouveau front est branchee, mais uniquement sur un perimetre
pilote tres restreint.

Documents effectivement cibles :

- `DOC-001` ;
- `DOC-002` ;
- `DOC-003` ;
- `DOC-004`.

Documents explicitement exclus par l'action V1 :

- `DOC-006` ;
- `DOC-013` ;
- `DOC-014`.

DOCX :

- reellement branche ;
- `generate_front_docx(...)` construit un `DocumentGenerationContext`, puis
  appelle `generate_docx_files_for_document_codes(...)` avec un catalogue filtre
  aux quatre documents cibles ;
- les tests existants prouvent une generation reelle des quatre fichiers DOCX :
  `declaration_non_condamnation.docx`, `autorisation_domiciliation.docx`,
  `procuration.docx`, `pv_nomination_gerant.docx`.

ZIP :

- reellement branche apres production DOCX ;
- `generate_front_zip(...)` refuse un ZIP sans DOCX, puis appelle le backend ZIP
  existant avec manifeste.

PDF :

- branche en code, mais conditionnel ;
- le bouton est desactive tant que le backend local PDF est indisponible ou tant
  qu'aucun DOCX n'a ete produit ;
- controle local pendant ce ticket : `is_pdf_export_available()` retourne
  `False` dans cet environnement. Donc le PDF n'est pas generable ici, meme si
  le chemin de code existe.

## 6. Vrais garde-fous

Les garde-fous reels sont dans `front_generation_actions.py` :

- profil obligatoire : `SELARL creation simple` ;
- `DossierRecord` obligatoire issu de la saisie V1 (`front_data_entry_v1`) ;
- les quatre documents cibles doivent tous etre `generable` cote
  `document_status` ;
- les documents reserves, manuels ou hors perimetre ne sont pas envoyes au
  runtime ;
- l'adaptateur moteur impose des champs et formats plus stricts que la simple
  readiness data-layer ;
- les dates moteur doivent etre au format ISO `AAAA-MM-JJ` ;
- les adresses libres doivent etre parsees sous une forme stricte du type
  `12 rue Exemple, 75001 Paris` ;
- `societe.societe_principale.rcs.ville`, ville/departement de naissance et
  autres champs runtime doivent etre presents ;
- ZIP et PDF exigent des DOCX deja produits.

Point trompeur majeur : si `document_status` juge les quatre documents
generables mais que l'adaptateur moteur trouve un format invalide, la vue normale
montre seulement un compteur `Bloques` et un message generique. Le detail du
blocage est cache dans `Debug interne`.

## 7. Comparaison avec les debriefs recents

| Debrief | Realite actuelle | Verdict |
|---|---|---|
| `FRONT-UI-SHELL-001` | Le shell et ses zones existent encore dans `front_shell.py`, mais la navigation visible `Nouveau front global` / `Prototype` et les zones `Accueil / Dossier / Documents attendus / Generation` ne sont plus rendues par defaut. | Vrai historiquement, partiellement faux comme description actuelle. |
| `FRONT-DOSSIER-EDITOR-001` | Les profils et lignes flow/blocs/exigences/statuts existent, mais ne sont plus visibles dans la surface normale. Seul `SELARL creation simple` est exposable via la saisie. | Vrai en couche interne, trompeur si lu comme UI actuelle. |
| `FRONT-DOSSIER-DATA-ENTRY-001` | La saisie reelle existe pour `SELARL creation simple` et alimente un vrai `DossierRecord`. Les autres profils restent non saisissables. | Vrai, avec perimetre tres limite. |
| `FRONT-GENERATION-ACTIONS-001` | DOCX et ZIP sont vraiment branches pour `DOC-001` a `DOC-004`; PDF est conditionnel au backend local, indisponible ici. Les blocages runtime restent peu visibles. | Majoritairement vrai, partiellement trompeur cote PDF et UX de blocage. |
| `FRONT-UX-HARD-CUT-001` | Aucun radio, aucun tableau par defaut, trois sous-titres principaux. Mais la vue contient encore 3 expanders ouverts, 22 champs, le bouton PDF desactive, `Outils internes` en sidebar et une caption technique. | Vrai techniquement, insuffisant pour le ressenti utilisateur. |

## 8. Elements encore prototype ou placeholder

- Les profils `SELARL ordre / inscription`, `SELARL cession cabinet + bail +
  financement`, `SCM cession de parts` et `SPFPL apport de titres` existent
  comme profils prudents, mais ne sont pas saisissables dans la surface normale.
- Le panneau `Documents attendus` n'existe pas comme surface utilisateur minimale
  actuelle ; il reste une cible/backlog et des helpers internes.
- Les outils `Assistant metier prototype`, `Document unitaire` et
  `Technique / diagnostic` restent des outils internes.
- Le debug est utile mais ne doit pas rester accessible comme signal visible
  pendant un test utilisateur.
- Le parsing d'adresse libre est un compromis technique, pas une vraie UX de
  saisie structuree.

## 9. Coupe franche UX proposee

Objectif : conserver strictement trois surfaces et rien d'autre :

1. type de dossier ;
2. saisie ;
3. generation.

Coupe immediate :

- masquer `Outils internes` dans la session utilisateur normale ; le debug doit
  etre active par configuration interne, pas par une checkbox visible ;
- supprimer les expanders ouverts de la surface principale ou les remplacer par
  un formulaire unique compact ;
- retirer toute mention `ReuseRuleState`, `front_data`, artefacts, chemins et
  vocabulaire de chantier ;
- cacher le bouton PDF si le backend est indisponible au lieu de montrer une
  action desactivee ;
- afficher les blocages exacts uniquement dans la zone `Generation`, en texte
  court et actionnable ;
- ne pas ajouter un panneau `Documents attendus` visible avant le test minimal ;
- garder les details documents, statuts de lot et tables uniquement dans un debug
  interne cache.

## 10. Prochain ticket unique recommande

`FRONT-MINIMAL-SURFACE-CLEANUP-001`

Objectif : transformer la surface actuelle en un formulaire produit minimal,
sans ajouter de nouveau panneau et sans etendre le perimetre documentaire.

Sorties attendues :

- page normale sans sidebar visible de debug ;
- seulement `Type de dossier`, `Donnees a saisir`, `Generation` ;
- saisie compacte sans tables, radios, sous-onglets ni expanders de diagnostic ;
- aides de format visibles seulement au niveau du champ concerne ;
- generation DOCX + ZIP claire pour `DOC-001` a `DOC-004` ;
- PDF cache si backend local indisponible ;
- blocages runtime affiches dans la zone `Generation` ;
- outils internes accessibles seulement via mode cache equipe.

`FRONT-GENERATION-READINESS-UX-001` et `FRONT-DOCUMENTS-PANEL-001` ne doivent pas
etre lances comme tickets separes avant cette coupe : ils risquent de rajouter de
la surface au lieu de simplifier. Leur contenu utile doit etre absorbe dans le
cleanup minimal.

## 11. Validations

- Relecture code des chemins `streamlit_app.py`, `front_dossier_entry.py`,
  `front_dossier_editor.py`, `front_generation_actions.py`, `front_shell.py` et
  `ui_runtime.py`.
- Inventaire AppTest de la vue normale : confirme 3 sous-titres, 0 table, 0 radio,
  3 expanders, 22 champs texte et 3 boutons de generation.
- Controle PDF local : `is_pdf_export_available()` retourne `False`.
- Aucun fichier Python modifie ; pas de `ruff` ni `pytest` requis.
