# Rapport ASSISTANT-METIER-PREFILL-001

## Objet

Ajouter un mécanisme de préremplissage avec données fictives déterministes dans le mode `Assistant metier`, pour accélérer les tests manuels sans ressaisie complète du dossier.

Le périmètre est strictement limité à l'UI Assistant métier. Aucun générateur DOCX/PDF/ZIP, moteur documentaire, catalogue métier ni wording juridique n'a été modifié.

## Fichiers modifiés

- `src/sydel_doc_engine/app/test_prefill_presets.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_business_wizard.py`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`
- `docs/review/assistant_metier_prefill_001_report_v1.md`

## Scénarios ajoutés

Le module `test_prefill_presets.py` expose quatre presets structurés :

- `SELARL médecin unipersonnelle simple`
- `SELARL chirurgien-dentiste + régime communautaire + site distinct`
- `SELARL médecin + cession cabinet médical + bail + financement`
- `SCI simple`

Les valeurs sont fictives, plausibles, cohérentes entre elles et déterministes. Aucun tirage aléatoire n'est utilisé.

## Logique de préremplissage

Dans `Assistant metier`, l'UI affiche :

- un sélecteur `Scénario de test` ;
- un bouton `Préremplir` ;
- un bouton `Réinitialiser` ;
- une indication visible `Mode test — données fictives préremplies : ...` lorsqu'un preset est chargé.

Le bouton `Préremplir` nettoie d'abord l'état Assistant métier, puis applique le type de dossier et les valeurs du preset sélectionné. Les presets remplissent le dossier complet utile au scénario : qualification, conditions métier, fiche praticien/client, société, siège, domiciliation, capital, associés, dates de décision/réunion/signature et blocs conditionnels du scénario.

Le scénario SELARL simple remplit un dossier unipersonnel prêt pour `DOC-001` à `DOC-004`. Les scénarios complexes activent les conditions nécessaires aux blocs visibles de régime communautaire, site distinct, cession, bail et financement, sans rendre générables les documents explicitement manuels ou non prêts.

## Gestion du session_state

Le préremplissage est isolé sur les clés de l'Assistant métier. Le bouton `Réinitialiser` vide les valeurs du mode Assistant métier et les sorties générées de ce mode, sans affecter les clés du mode `Technique / diagnostic` ni celles du mode `Document unitaire`.

Les champs dérivés désactivés sont synchronisés dans `session_state` :

- `Dossier unipersonnel` propage le praticien vers l'associé unique ;
- le signataire, le gérant et l'associé unique restent cohérents dans le preset SELARL simple ;
- l'option domiciliation = siège force l'adresse de domiciliation affichée à rester identique au siège social ;
- les scénarios SCI conservent le parcours SCI existant.

## Tests lancés

- `.\.venv\Scripts\python.exe -m pytest tests\unit\test_business_wizard.py -q` : OK, 41 tests passés.
- `.\.venv\Scripts\python.exe -m pytest tests\unit\test_single_document_mode.py tests\unit\test_ui_runtime.py -q` : OK, 12 tests passés.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 272 tests passés.

## Couverture ajoutée

Les tests vérifient :

- la présence du sélecteur et des boutons en `Assistant metier` ;
- leur absence en `Technique / diagnostic` ;
- leur absence en `Document unitaire` ;
- le préremplissage du scénario SELARL simple ;
- la propagation du `Dossier unipersonnel` ;
- un `can_generate_docx = True` pour le scénario simple ;
- l'affichage attendu des blocs complexes ;
- le reset propre de l'état Assistant métier ;
- la non-régression du scénario `SCI simple`.

## Prochaine étape recommandée

Faire une revue manuelle Streamlit des quatre scénarios de test, puis poursuivre avec `SELARL-JURIST-REVIEW-001` pour la validation métier/juridique du parcours SELARL.
