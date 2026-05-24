# Rapport FRONT-UX-CLEANUP-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket simplifie radicalement la vue principale du nouveau front pour rendre
le test utilisateur reel possible sur le parcours prudent `SELARL creation
simple`.

Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique, fondation `front_data`,
deploiement ou push n'a ete modifie.

## 2. Sources utilisees

- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/front_shell.py`
- `src/sydel_doc_engine/app/front_dossier_editor.py`
- `src/sydel_doc_engine/app/front_dossier_entry.py`
- `src/sydel_doc_engine/app/front_generation_actions.py`
- `docs/review/front_ui_shell_001_report_v1.md`
- `docs/review/front_dossier_editor_001_report_v1.md`
- `docs/review/front_dossier_data_entry_001_report_v1.md`
- `docs/review/front_generation_actions_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`

## 3. Ce qui a ete retire de la vue principale

La vue principale `Nouveau front global` n'affiche plus par defaut :

- le choix interne entre `Accueil / selection`, `Dossier`, `Documents attendus`
  et `Generation` ;
- le tableau complet des etapes du flow ;
- le tableau complet des blocs actifs ;
- le tableau complet des exigences documentaires ;
- le tableau complet des statuts documentaires ;
- le tableau complet du statut de lot ;
- les messages longs d'architecture du shell.

Ces informations restent disponibles pour diagnostic, mais elles ne structurent
plus le parcours de test.

## 4. Ce qui a ete deplace en secondaire

Les details techniques sont regroupes dans des expanders fermes par defaut :

- `Diagnostic dossier` : synthese data-layer, objets `DossierRecord`, roles,
  adresses, flow, blocs, exigences et statuts ;
- `Details generation` : statuts documentaires detailles et garde-fous de
  generation ;
- `Dossier de sortie` : chemin technique des artefacts ;
- `Diagnostic front_data` : navigation cible et apercu documentaire du shell.

Les outils historiques restent dans l'espace separe `Prototype / outils de test`
et ne sont pas melanges avec le parcours principal.

## 5. Ce qui reste dans le parcours principal

Le parcours principal visible suit maintenant une sequence courte :

1. choisir le type de dossier ;
2. saisir les donnees du cas `SELARL creation simple` ;
3. lire un resume minimal des documents prets, bloques et du statut de lot ;
4. lancer la generation DOCX, puis ZIP, et PDF si le backend local est
   disponible ;
5. telecharger les fichiers produits.

Le perimetre fonctionnel conserve reste `DOC-001`, `DOC-002`, `DOC-003` et
`DOC-004`.

## 6. Pourquoi cette simplification aide le test utilisateur

Le test local doit verifier si un utilisateur peut comprendre le parcours sans
connaitre l'architecture interne. Les anciennes tables etaient utiles pour le
rebuild, mais elles mettaient le diagnostic au premier plan.

La nouvelle organisation met l'action produit devant :

- le choix du dossier est visible immediatement ;
- les champs utiles sont le coeur de la page ;
- les statuts sont resumes par quelques metriques ;
- les raisons detaillees restent accessibles sans saturer la page ;
- la generation est visible au meme endroit que la saisie.

## 7. Tests

Tests adaptes :

- `tests/unit/test_front_ui_shell.py`
- `tests/unit/test_front_dossier_editor.py`
- `tests/unit/test_front_dossier_data_entry.py`
- `tests/unit/test_front_generation_actions.py`

Couverture :

- la vue cible n'a plus de navigation interne centrale ;
- les diagnostics sont presents en expanders ;
- les champs de saisie restent accessibles ;
- la generation simple DOCX puis ZIP reste fonctionnelle ;
- la zone prototype reste separee.

Validation cible pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_ui_shell.py tests/unit/test_front_dossier_editor.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_front_generation_actions.py -q`
  : OK, 28 tests passes.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 380 tests passes.

## 8. Limites restantes

- La page reste une Streamlit de transition ; `streamlit_app.py` demeure
  volumineux.
- Les expanders de diagnostic sont encore rendus dans l'arbre Streamlit, meme
  s'ils sont fermes visuellement.
- Le panneau documents operationnel reste a construire si le test local confirme
  la lisibilite du parcours.

## 9. Prochaine etape recommandee

Le prochain jalon devient bien un premier vrai test local du nouveau front sur
`SELARL creation simple`, avec generation `DOC-001` a `DOC-004`, ZIP et PDF si
disponible.
