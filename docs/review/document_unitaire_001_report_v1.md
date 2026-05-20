# DOCUMENT-UNITAIRE-001 - Rapport V1

## Objectif
Ajouter un mode Streamlit `Document unitaire` pour tester un document isolé sans remplir tout un dossier métier complet.

## Périmètre implémenté
- Nouveau choix de mode Streamlit : `Assistant metier`, `Document unitaire`, `Technique / diagnostic`.
- Sélection du cas métier et des conditions applicables via le catalogue existant, puis choix d'un document par code et libellé.
- Affichage limité aux champs nécessaires au document sélectionné.
- Préremplissage optionnel par données d'exemple.
- Validation des champs manquants avant génération.
- Génération d'un DOCX unique, téléchargement DOCX, ZIP optionnel et PDF optionnel si le backend local est disponible.

## Documents supportés V1
- `DOC-001` - Déclaration de non-condamnation.
- `DOC-002` - Autorisation de domiciliation.
- `DOC-003` - Procuration.
- `DOC-004` - PV de nomination du gérant.

Ces documents sont couverts car ils disposent déjà de générateurs et de champs stables dans le parcours UI existant.

## Limites explicites
- Les documents manuels restent affichés comme non générables dans ce mode.
- Les documents non implémentés, sans mapping ou hors périmètre V1 affichent un message clair de non-support.
- Le mode ne généralise pas automatiquement aux 43 documents du moteur.
- Aucun générateur DOCX/PDF/ZIP, moteur documentaire, registre de génération ou wording juridique n'a été modifié.

## Fichiers principaux
- `src/sydel_doc_engine/app/single_document_mode.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_single_document_mode.py`

## Validations
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 266 tests passés.
- Tests ciblés du mode unitaire : visibilité du mode Streamlit, sélection documentaire, statuts supporté/non supporté/manuel, champs limités, génération DOCX et ZIP sur cas simples.

## Risques et suites
- Le backend PDF reste dépendant de LibreOffice ou Word COM local, comme dans le reste de l'application.
- L'extension à d'autres documents doit rester incrémentale, document par document, après vérification des champs réellement nécessaires.
- Prochaine étape recommandée : revue utilisateur du mode `Document unitaire` sur `DOC-001` à `DOC-004`, puis ajout contrôlé d'un lot suivant si le schéma couvre les cas.
