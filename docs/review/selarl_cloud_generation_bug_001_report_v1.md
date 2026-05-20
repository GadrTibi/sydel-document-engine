# Rapport SELARL-CLOUD-GENERATION-BUG-001

## Objet

Diagnostiquer et corriger le blocage de génération observé dans le parcours SELARL visible, malgré le smoke local fonctionnel.

## Bug reproduit

Oui.

Le bug est reproduit avec le parcours Streamlit visible via `streamlit.testing.v1.AppTest` :

1. ouvrir `Assistant metier` sur `SELARL` ;
2. sélectionner une qualification simple médecin ;
3. cocher `Dossier unipersonnel` avant de remplir la Fiche Client ;
4. cocher `L'adresse de domiciliation est le siège social` avant de remplir le siège ;
5. remplir ensuite tous les champs source visibles.

Avant correction :

- `can_generate_docx = false` ;
- le compteur `Documents prets` reste à `0` ;
- le bouton `Generer les DOCX` reste désactivé ;
- `generatable_document_codes` reste vide côté UI ;
- aucun appel runtime DOCX / ZIP n'est atteint.

Le problème ne vient donc pas du moteur DOCX, du ZIP, du PDF ni des générateurs.

## Cause racine

Le smoke réaliste validait `evaluate_business_wizard(...)` et la génération via données construites directement, mais il ne reproduisait pas l'état Streamlit des widgets désactivés.

Dans le parcours visible, les champs dérivés et désactivés de l'associé unique (`Associé 1`) étaient initialisés une première fois à vide lorsque l'utilisateur cochait `Dossier unipersonnel` en qualification, avant d'avoir saisi la Fiche Client.

Ensuite, quand le Praticien était saisi, Streamlit conservait les anciennes valeurs vides dans `st.session_state` pour :

- `selarl_associe_genre_0` ;
- `selarl_associe_civilite_0` ;
- `selarl_associe_prenom_0` ;
- `selarl_associe_nom_0`.

Le même risque existait pour l'adresse de domiciliation dérivée depuis le siège social.

Ces champs vides alimentaient ensuite `evaluate_business_wizard(...)`, ce qui bloquait `DOC-004`, puis la construction du contexte moteur, puis toute génération visible.

## Correction faite

Correction minimale dans `src/sydel_doc_engine/app/streamlit_app.py` :

- synchronisation explicite du `session_state` des widgets dérivés de l'associé 1 avant rendu quand `Dossier unipersonnel` ou la copie du Praticien est active ;
- synchronisation explicite de l'adresse de domiciliation quand `L'adresse de domiciliation est le siège social` est cochée ;
- aucune modification des générateurs ;
- aucune modification du moteur DOCX/PDF/ZIP ;
- aucune généralisation aux autres cas métier.

## Etat Cloud

L'état Git local lu au démarrage était `main...origin/main` avec un non-suivi préexistant `docs/docssource_truth/`.

La vérification distante directe par `git ls-remote origin refs/heads/main` a échoué localement pour cause d'identifiants GitHub indisponibles (`SEC_E_NO_CREDENTIALS`). En revanche, le bug étant reproduit localement dans le parcours visible, la cause racine n'est pas seulement un retard Cloud.

Le commit local demandé a été tenté en fin de ticket mais l'environnement Codex a refusé l'écriture dans `.git`
(`Unable to create .../.git/index.lock: Permission denied` et écriture `.git/objects` refusée). Les changements
restent donc dans le workspace local et devront être commités dès que les permissions Git locales seront rétablies,
avec le message prévu : `fix: restore selarl generation in business wizard`.

Après commit, il faudra pousser manuellement puis laisser Streamlit Cloud redéployer.

## Fichiers modifiés

- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_business_wizard.py`
- `docs/review/selarl_smoke_realistic_001_report_v1.md`
- `docs/review/selarl_cloud_generation_bug_001_report_v1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`

Un ajout local non suivi hors ticket est présent dans le workspace : `src/sydel_doc_engine/app/single_document_mode.py`, `tests/unit/test_single_document_mode.py` et `docs/docssource_truth/`. Ces fichiers ne font pas partie de la correction SELARL.

## Tests lancés

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py -q` : OK, 35 tests passés.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : premier passage KO sur le garde-fou wording existant, car le rapport de smoke SELARL contenait littéralement le terme de transcription banni.
- Correction documentaire du rapport de smoke, sans wording juridique.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 266 tests passés.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.

## Résultat

Le parcours visible SELARL peut maintenant générer `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004` même lorsque l'utilisateur active les réutilisations avant de remplir les champs source.

Le test de non-régression clique réellement sur `Generer les DOCX` et vérifie la production des quatre fichiers attendus.

## Recommandation finale

Rétablir les permissions d'écriture Git locales, créer le commit de correction, le pousser manuellement, puis
redéployer Streamlit Cloud et refaire un test utilisateur SELARL unipersonnel avant la revue juriste.
