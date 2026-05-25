# Rapport FRONT-MINIMAL-SURFACE-CLEANUP-001

Date : 2026-05-25

## 1. Objet

Application de la surface utilisateur minimale definie dans
`docs/project/FRONT_MINIMAL_USER_SURFACE_V1.md`, avant push, redeploiement ou
test utilisateur.

Contraintes respectees :

- aucun generateur modifie ;
- aucun moteur DOCX/PDF/ZIP modifie ;
- aucune source de verite modifiee ;
- aucun wording juridique modifie ;
- aucun elargissement du perimetre documentaire.

## 2. Surface visible normale

La vue normale affiche maintenant seulement trois zones principales :

1. `Type de dossier` ;
2. `Donnees a saisir` ;
3. `Generation`.

Inventaire AppTest de la surface normale :

- sous-titres : `Type de dossier`, `Donnees a saisir`, `Generation` ;
- radios : 0 ;
- tables : 0 ;
- expanders : 0 ;
- outil interne visible : aucun ;
- checkboxes visibles : `Dossier unipersonnel`, `Domiciliation = siege social` ;
- boutons de generation visibles avec backend PDF local indisponible :
  `Generer les DOCX`, `Generer le ZIP`.

Les intertitres simples du formulaire (`Personne principale`,
`Societe principale`, `Capital, decision et signature`) restent dans le flux de
saisie, sans sous-onglet ni expander.

## 3. Saisie

La saisie reste limitee au profil pilote `SELARL creation simple`.

Changements visibles :

- suppression des trois expanders ouverts ;
- suppression de la caption technique contenant `ReuseRuleState` ;
- aides de format ajoutees pres des champs d'adresse ;
- placeholders ajoutes sur les dates ISO et adresses libres.

Le nombre de champs n'est pas encore reduit : le ticket coupe les faux niveaux
de navigation et le vocabulaire interne, mais ne modifie pas le modele de saisie
ni le perimetre de donnees requis.

## 4. Generation

La zone `Generation` reste limitee au pilote actuel :

- `DOC-001` ;
- `DOC-002` ;
- `DOC-003` ;
- `DOC-004`.

Les documents reserves ou manuels restent hors generation V1.

Changements visibles :

- le perimetre pilote est indique sobrement dans `Generation` ;
- les blocages data-layer sont affiches en messages courts et actionnables ;
- les blocages runtime de l'adaptateur moteur sont affiches dans la meme zone ;
- le bouton PDF est cache quand le backend PDF local est indisponible ;
- le ZIP reste disponible apres generation DOCX.

Exemple de blocage runtime maintenant visible :

- `signature.date doit etre au format AAAA-MM-JJ.`

## 5. Debug interne

Les outils internes ne sont plus visibles en session utilisateur normale.

Ils restent disponibles uniquement via mode interne cache :

- variable d'environnement `SYDEL_ENABLE_INTERNAL_TOOLS=1` ;
- ou flag de session interne `_sydel_internal_tools_unlocked` utilise par les
  tests AppTest.

Une fois le mode interne active, les outils existants restent disponibles :

- `Assistant metier prototype` ;
- `Document unitaire` ;
- `Technique / diagnostic` ;
- `Debug interne`.

## 6. Tests

Tests cibles executes :

```text
.\.venv\Scripts\python.exe -m pytest tests\unit\test_front_ui_shell.py tests\unit\test_front_dossier_data_entry.py tests\unit\test_front_dossier_editor.py tests\unit\test_front_generation_actions.py tests\unit\test_single_document_mode.py tests\unit\test_business_wizard.py -q
```

Resultat : 79 tests passes.

Validations globales :

```text
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
```

Resultat : ruff OK ; pytest OK, 382 tests passes.

## 7. Prochaine etape recommandee

Lancer un test utilisateur local du pilote `SELARL creation simple` sur la
surface minimale.

Ne pas lancer `FRONT-DOCUMENTS-PANEL-001` avant ce test : un panneau documents
visible risquerait de recharger la surface tout de suite apres la coupe.
