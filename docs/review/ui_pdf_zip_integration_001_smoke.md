# Smoke manuel UI-PDF-ZIP-INTEGRATION-001

Date : 2026-05-17

## Objet

Verifier manuellement que l'UI Streamlit permet :

- de charger un contexte dossier ;
- de previsualiser les documents selectionnes par l'orchestrateur ;
- de generer les DOCX ;
- de lancer la conversion PDF lorsque le backend local est disponible ;
- de telecharger les DOCX et le ZIP dossier.

Ce smoke ne vaut pas validation juridique ni revue visuelle humaine des rendus.

## Pre-requis locaux

- Environnement Python installe avec les dependances du projet.
- Lancement de l'UI :

```powershell
.\.venv\Scripts\python.exe -m streamlit run src/sydel_doc_engine/app/streamlit_app.py
```

- Pour le PDF : LibreOffice disponible dans le PATH, ou chemin configure via
  `SYDEL_LIBREOFFICE_PATH`, ou Microsoft Word COM disponible sous Windows.

Si aucun backend PDF fiable n'est detecte, l'UI doit afficher une limitation
explicite et laisser la generation DOCX/ZIP disponible.

## Scenario nominal

1. Ouvrir l'UI Streamlit.
2. Choisir `lot_02_orchestrator_positive_example.yaml` dans la liste des contextes exemple.
3. Cliquer sur `Charger le contexte exemple`.
4. Verifier que l'UI affiche `Contexte valide`.
5. Verifier que la table de selection contient les documents attendus :
   `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`.
6. Laisser l'option PDF cochee si le backend local est indique disponible.
7. Cliquer sur `Generer le dossier`.
8. Verifier le message de succes avec le nombre de DOCX, le nombre de PDF et le ZIP.
9. Telecharger au moins un DOCX.
10. Telecharger le ZIP dossier.
11. Ouvrir le ZIP localement et verifier qu'il contient les DOCX generes et les PDF
    si la conversion PDF a ete executee.

## Limites attendues

- Les fichiers produits sont sous `artifacts/ui_pdf_zip_integration_001/` et ne
  doivent pas etre versionnes.
- La conversion PDF depend de l'environnement local ; LibreOffice absent ou Word COM
  indisponible doit etre traite comme limitation technique, pas comme erreur juridique.
- Un echec PDF ne doit pas modifier les DOCX generes ; le ZIP contient les fichiers
  effectivement disponibles.
