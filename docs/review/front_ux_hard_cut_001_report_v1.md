# Rapport FRONT-UX-HARD-CUT-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket retire de la surface utilisateur normale tout ce qui n'est pas
strictement utile au test local du nouveau front.

Aucun generateur, moteur DOCX/PDF/ZIP, fondation `front_data`, wording
juridique, deploiement ou push n'a ete modifie.

## 2. Ce qui a ete retire de la vue principale

La vue principale ne contient plus :

- la navigation `Accueil / selection`, `Dossier`, `Documents attendus`,
  `Generation` ;
- la navigation `Prototype / outils de test` ;
- les tableaux de flow ;
- les tableaux de blocs actifs ;
- les tableaux d'exigences ;
- les tableaux de statuts documentaires ;
- les tableaux de statut de lot ;
- les messages d'architecture ou placeholders du shell ;
- les expanders `Diagnostic dossier`, `Details generation`,
  `Diagnostic front_data` et `Dossier de sortie`.

Le rendu AppTest par defaut confirme : aucun radio, aucun tableau et uniquement
trois sous-zones visibles.

## 3. Ce qui reste visible

La surface utilisateur normale affiche seulement :

1. `Type de dossier`
   - selecteur de profil, limite au profil testable `SELARL creation simple`.
2. `Donnees a saisir`
   - champs reels regroupes par personne, societe, capital/decision/signature.
3. `Generation`
   - compteur des documents prets ;
   - compteur des documents bloques ;
   - boutons `Generer les DOCX`, `Generer le ZIP` et `Generer les PDF` si le
     backend local le permet ;
   - telechargements uniquement apres production d'artefacts.

## 4. Outils internes

Les outils historiques ne sont pas supprimes. Ils sont deplaces derriere la
checkbox de sidebar `Outils internes`.

Quand cette checkbox est activee, un selecteur `Outil interne` donne acces a :

- `Assistant metier prototype` ;
- `Document unitaire` ;
- `Technique / diagnostic` ;
- `Debug interne`.

Ils ne sont donc plus presents dans le parcours utilisateur normal.

## 5. Debug minimal

Le debug minimal prend la forme de l'outil interne `Debug interne`.

Il expose les tables utiles a l'equipe projet :

- synthese `DossierRecord` ;
- objets data ;
- roles ;
- adresses ;
- statuts de generation ;
- garde-fous de generation.

Ce debug n'est pas rendu par defaut et n'apparait qu'apres activation volontaire
de `Outils internes`.

## 6. Pourquoi cette version est testable cote user

Le testeur n'a plus a comprendre les fondations internes, les sentinelles, les
statuts de lot ou les zones du shell. Le parcours visible correspond a l'action
attendue :

- choisir un dossier ;
- renseigner les donnees ;
- generer.

Les diagnostics restent disponibles pour l'equipe, sans melanger le produit et
les outils de rebuild.

## 7. Tests

Tests adaptes :

- `tests/unit/test_front_ui_shell.py`
- `tests/unit/test_front_dossier_editor.py`
- `tests/unit/test_front_dossier_data_entry.py`
- `tests/unit/test_front_generation_actions.py`
- `tests/unit/test_business_wizard.py`
- `tests/unit/test_single_document_mode.py`

Validation cible :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_ui_shell.py tests/unit/test_front_dossier_editor.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_front_generation_actions.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py -q`
  : OK, 77 tests passes.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 380 tests passes.

## 8. Prochaine etape recommandee

Le prochain jalon devient bien un vrai test local utilisateur sur `SELARL
creation simple`, avec generation de `DOC-001` a `DOC-004`, ZIP et PDF si le
backend local est disponible.
