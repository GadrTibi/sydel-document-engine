# Rapport FRONT-GENERATION-ACTIONS-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket branche les premieres actions de generation depuis le nouveau front
visible, uniquement pour le profil prudent `SELARL creation simple`.

Documents ouverts en V1 :

- `DOC-001` - Declaration sur l'honneur de non-condamnation ;
- `DOC-002` - Autorisation de domiciliation ;
- `DOC-003` - Procuration ;
- `DOC-004` - PV nomination gerant.

Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique, deploiement ou push n'a
ete modifie.

## 2. Sources utilisees

- `docs/review/front_dossier_data_entry_001_report_v1.md`
- `docs/review/front_dossier_editor_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/review/front_unit_document_mode_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`
- `src/sydel_doc_engine/app/front_dossier_entry.py`
- `src/sydel_doc_engine/app/front_dossier_editor.py`
- `src/sydel_doc_engine/app/front_shell.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/front_data/document_status.py`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/app/ui_runtime.py`
- `src/sydel_doc_engine/registry/catalog.py`

ADR applicables : ADR-0001 source de verite documentaire, ADR-0002 moteur par
document canonique et ADR-0005 mode de travail Codex/repo-first.

## 3. Ce qui est generable depuis le nouveau front

La zone `Nouveau front global > Dossier` affiche maintenant une section
`Generation V1` quand le profil `SELARL creation simple` est actif.

La zone `Nouveau front global > Generation` relit aussi la saisie en session,
reconstruit un `DossierRecord` et affiche les memes actions.

Actions disponibles :

- `Generer les DOCX` quand `DOC-001` a `DOC-004` sont tous `generable` ;
- `Generer le ZIP` seulement apres production DOCX ;
- `Generer les PDF` seulement si le backend local PDF est disponible et apres
  production DOCX ;
- telechargement des DOCX, du ZIP et des PDF produits.

## 4. Architecture retenue

Nouveau module :

- `src/sydel_doc_engine/app/front_generation_actions.py`

Le module :

- prend un `DossierRecord` issu de la saisie V1 ;
- recalcule une readiness via `build_document_status_summary(...)` ;
- limite le perimetre a `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004` ;
- refuse tout document qui n'est pas strictement `generable` ;
- construit un `DocumentGenerationContext` minimal pour le moteur ;
- appelle `ui_runtime.generate_docx_files_for_document_codes(...)`,
  `generate_zip_file(...)` et `generate_pdf_files(...)` ;
- ne depend pas de `business_wizard.py`.

Le `streamlit_app.py` reste un adaptateur UI : la logique de readiness,
d'exclusion et de construction du contexte moteur est dans le module dedie.

## 5. Donnees runtime ajoutees

La saisie V1 a ete enrichie minimalement avec les champs requis par le moteur
pour `DOC-004` :

- ville de naissance ;
- departement de naissance ;
- ville RCS.

Les adresses V1 restent saisies comme adresse affichee. L'adaptateur utilise les
composants d'adresse s'ils existent ; sinon il accepte prudemment une forme
simple du type `12 rue Exemple, 75001 Paris`. Si cette forme n'est pas exploitable,
la generation est bloquee avec une raison explicite.

## 6. Garde-fous

- `DOC-006` reste exclu de ce mode V1, meme s'il peut etre techniquement
  `generable_with_reserve`.
- `DOC-013` et `DOC-014` restent exclus et jamais envoyes en generation.
- Les documents manuels, incomplets, reserves ou hors perimetre ne sont pas
  transmis au runtime.
- Aucun document complexe ordre, SCM, SPFPL, cession cabinet, bail ou financement
  n'est ouvert.
- Le ZIP est produit uniquement a partir des fichiers DOCX deja generes.
- Le PDF reste best-effort et conditionne par le backend local.

## 7. Limites restantes

- Le panneau `Documents attendus` cible reste a consolider en composant dedie.
- Les adresses composees devraient devenir une vraie saisie decomposee dans un
  ticket ulterieur, plutot qu'un parsing prudent de texte affiche.
- La generation reste limitee au cas simple ; pas d'overrides avances ni de lots
  complexes.
- Le premier test local utilisateur doit encore valider le parcours complet dans
  Streamlit hors AppTest.

## 8. Tests

Tests ajoutes :

- `tests/unit/test_front_generation_actions.py`

Couverture :

- readiness du profil `SELARL creation simple` ;
- generation reelle DOCX pour `DOC-001` a `DOC-004` ;
- ZIP apres DOCX ;
- blocage d'un dossier incomplet ;
- exclusion de `DOC-006`, `DOC-013` et `DOC-014` ;
- absence de dependance au `business_wizard` dans le module d'action ;
- AppTest du nouveau front avec bouton DOCX puis ZIP.

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_generation_actions.py -q`
  : OK, 6 tests passes.
- Ruff cible sur les fichiers modifies : OK.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 380 tests passes.

## 9. Prochaine etape recommandee

Faire un premier vrai test local du nouveau front :

1. ouvrir `Nouveau front global > Dossier` ;
2. remplir `SELARL creation simple` ;
3. verifier que `DOC-001` a `DOC-004` sont generables ;
4. generer les DOCX ;
5. creer le ZIP ;
6. tester le PDF si le backend local est disponible.

Ensuite lancer `FRONT-DOCUMENTS-PANEL-001` pour consolider le panneau documents
attendus.
