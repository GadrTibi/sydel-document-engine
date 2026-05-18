# Worktree cleanup and UI status V1

Ticket : `WORKTREE-CLEANUP-AND-UI-STATUS-001`

Date : 2026-05-18

## Objet

Ce rapport clarifie l'etat local du projet apres audit des worktrees et de
`main`. Il sert a eviter de relancer une branche intermediaire en pensant tester
l'etat final.

Il ne modifie aucun wording juridique, aucune source documentaire metier et
aucune logique moteur.

## Dossier canonique a garder

Le dossier actif final a utiliser apres cleanup local est :

`C:\Users\Gad\Desktop\Sydel\sydel-document-engine`

Ce dossier doit etre sur `main`, propre, aligne avec `origin/main`, et lance
depuis sa racine.

Commande cible :

```powershell
cd C:\Users\Gad\Desktop\Sydel\sydel-document-engine
.\.venv\Scripts\python.exe -m streamlit run src\sydel_doc_engine\app\streamlit_app.py
```

## Dossiers a archiver localement

Les anciens worktrees `sydel-document-engine-*` du dossier parent
`C:\Users\Gad\Desktop\Sydel\` ne doivent plus servir de reference courante.

Ils sont a archiver sous :

`C:\Users\Gad\Desktop\Sydel\_codex_worktrees_archive`

Liste des dossiers identifies comme obsoletes ou intermediaires :

- `sydel-document-engine` : ancien dossier racine sur `codex/ui-occurrences-001`,
  avec modifications et fichiers non suivis locaux ; il ne doit plus etre utilise
  comme reference.
- `sydel-document-engine-arbitrage-scm-cession-resolve-001`
- `sydel-document-engine-civils-core`
- `sydel-document-engine-close-motor-audit-001`
- `sydel-document-engine-code-acte-actions-001`
- `sydel-document-engine-code-scm-cession-block-001`
- `sydel-document-engine-code-scm-liste-depenses-001`
- `sydel-document-engine-code-scm-sat-docx-001`
- `sydel-document-engine-code-statuts-scm-001`
- `sydel-document-engine-convert-derog-salariee-001`
- `sydel-document-engine-final-motor-audit-002`
- `sydel-document-engine-fix-style-statuts-batch-001`
- `sydel-document-engine-pdf-backend-001`
- `sydel-document-engine-recipe-frame-001`
- `sydel-document-engine-review-final-001`
- `sydel-document-engine-spec-scm-cession-block-001`
- `sydel-document-engine-spec-scm-satellites-001`
- `sydel-document-engine-style-analyse-lot03-batch-001`
- `sydel-document-engine-style-statuts`
- `sydel-document-engine-sync-main`
- `sydel-document-engine-ui-flow-001`
- `sydel-document-engine-ui-pdf-zip-integration-001`
- `sydel-document-engine-zip-backend-001`

Le dossier archive conserve les anciens etats locaux. Aucun worktree archive ne
doit etre relance pour tester le projet.

## Dossiers encore utiles

Aucun worktree intermediaire n'est necessaire pour tester l'application apres
consolidation.

La seule branche qui apportait encore un contenu absent de `main` etait
`codex/review-final-001`, avec :

- `docs/review/final_review_pack_v1.md`

Ce fichier est integre dans `main` par le present ticket.

## Contenu reel de `main`

`main` est la branche de reference. Elle contient :

- les docs de cloture et fondation :
  - `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`
  - `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md`
  - `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md`
- les docs UI :
  - `docs/project/19_UI_FLOW_V1.md`
  - `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`
  - `docs/project/21_UI_FORM_SCHEMA_V1.md`
- les docs de revue :
  - `docs/review/final_recipe_framework_v1.md`
  - `docs/review/ui_pdf_zip_integration_001_smoke.md`
  - `docs/review/final_review_pack_v1.md`
- le backend PDF :
  - `src/sydel_doc_engine/rendering/pdf_export.py`
- le backend ZIP :
  - `src/sydel_doc_engine/rendering/zip_bundle.py`
- l'UI technique actuelle :
  - `src/sydel_doc_engine/app/streamlit_app.py`
  - `src/sydel_doc_engine/app/ui_runtime.py`
- les contextes exemples sous `examples/contexts/`.

Le moteur DOCX expose le registre `DOC-001` a `DOC-043` via le catalogue et
l'orchestrateur.

## Ce que l'UI actuelle sait faire

L'UI Streamlit actuelle est une UI technique de pilotage par contexte.

Elle sait :

- charger un contexte dossier YAML/JSON depuis `examples/contexts/` ;
- charger un contexte YAML/JSON par upload ;
- accepter un contexte colle manuellement dans une zone texte ;
- valider le contexte avec `DocumentGenerationContext` ;
- afficher la selection issue de `select_documents_for_context` ;
- generer les DOCX via `generate_documents` ;
- lancer l'export PDF local si LibreOffice ou Word COM est disponible ;
- creer un ZIP dossier via `rendering/zip_bundle.py` ;
- proposer les telechargements DOCX, PDF produits et ZIP.

## Ce que l'UI actuelle ne fait pas encore

L'UI actuelle n'est pas une UI produit finale.

Elle ne fait pas encore :

- wizard metier multi-etapes ;
- saisie guidee par branche dossier ;
- routage minimal avec socle de branche ;
- cartes personnes ou `associes[]` ;
- blocs conditionnels interactifs ;
- validation progressive champ par champ ;
- resume final riche avant generation ;
- affichage structure des documents manuels ou exclus ;
- experience utilisateur metier finalisee.

Ces elements sont specifies dans `19_UI_FLOW_V1.md`,
`20_UI_DOCUMENT_OCCURRENCES_V1.md` et `21_UI_FORM_SCHEMA_V1.md`, mais ne sont
pas implementes dans l'interface Streamlit actuelle.

## Difference entre UI technique et UI wizard metier

Une UI technique de pilotage charge un contexte canonique deja structure, appelle
le moteur, puis expose les sorties. Elle sert a tester et exploiter le pipeline
deterministe `contexte -> selection -> DOCX -> PDF -> ZIP`.

Une UI wizard metier collecterait elle-meme les donnees dossier via des etapes
ergonomiques : routage, socle de branche, blocs conditionnels, personnes,
controles, resume final et generation. Ce wizard reste un chantier futur.

## Statut retenu

Statut noir sur blanc :

- l'UI actuelle est une **UI technique de pilotage** ;
- l'UI actuelle n'est pas une **UI produit finale** ;
- il ne manque pas une branche cachee contenant le wizard metier complet ;
- le prochain chantier UI produit devra repartir des specs UI deja presentes
  dans `docs/project/19`, `20` et `21`.

## Prochaine etape recommandee

Lancer `REVIEW-FINAL-001` sur le dossier canonique final, puis
`CLOSE-PROJECT-V1-001`.
