# TRACK-B-FRONT-ARCHITECTURE-RESET-001 - Rapport court

Date : 2026-05-26

## Contexte prouve

- Dossier de travail : `C:\Users\Gad\Desktop\Sydel\sydel-track-b`.
- Racine Git : `C:/Users/Gad/Desktop/Sydel/sydel-track-b`.
- Branche : `track-b/clean-rebuild`.
- Regle respectee : aucun push, aucun merge, aucun travail hors Track B.

## Runtime Track B

Le runtime local est isole dans `.venv`.

Commande d'installation executee depuis Track B :

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Preuve d'import obtenue :

```text
C:\Users\Gad\Desktop\Sydel\sydel-track-b\src\sydel_doc_engine\__init__.py
```

Commande locale cible pour lancer le nouveau front B :

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\sydel_doc_engine\front_app\app.py
```

Note Windows locale : Python 3.13 cree des dossiers temporaires non reinscriptibles dans ce sandbox quand `ensurepip` utilise `tempfile.mkdtemp(..., mode=0o700)`. Le `.venv` contient un correctif local ignore dans le repo via `sitecustomize.py`; le code projet n'en depend pas.

## Audit court du front actuel

Points d'entree existants :

- `src/sydel_doc_engine/app/streamlit_app.py` : ancien point d'entree Streamlit, encore runnable.
- `src/sydel_doc_engine/app/front_shell.py` : shell cible intermediaire, mais encore attache au legacy par les outils internes.
- `src/sydel_doc_engine/app/front_dossier_entry.py` et `front_generation_actions.py` : adaptateurs utiles, deja plus proches de `front_data`.

Modules legacy encore structurants :

- `business_wizard.py` : assistant metier prototype.
- `single_document_mode.py` : outil Document unitaire.
- `streamlit_app.py` : contient encore le shell historique, les outils internes, le diagnostic technique et beaucoup de widgets.
- `test_prefill_presets.py` : prefills de test, utiles en QA mais pas comme base produit.

Classement architectural :

- shell principal : `streamlit_app.py` ancien, `front_app/app.py` nouveau.
- navigation : ancien checkbox/radio interne ; nouveau flux sans navigation parasite.
- formulaire/saisie : ancien mix de widgets longs ; nouveau `front_app/data_entry.py` minimal et structurel.
- generation : ancien `front_generation_actions.py` branche sur une SELARL deja avancee ; nouveau `front_app/generation.py` garde un slot honnete non generable.
- outils internes/debug/prototypes : conserves dans `app/`, non importes par `front_app/`.

## Nouvelle architecture

Nouveau chemin d'execution cree :

- `src/sydel_doc_engine/front_app/app.py` : entrypoint Streamlit clean.
- `src/sydel_doc_engine/front_app/shell.py` : shell/layout minimal.
- `src/sydel_doc_engine/front_app/routing.py` : orchestration minimale des trois zones.
- `src/sydel_doc_engine/front_app/dossier_selection.py` : selection du type de dossier.
- `src/sydel_doc_engine/front_app/data_entry.py` : zone de saisie structurelle.
- `src/sydel_doc_engine/front_app/generation.py` : zone generation, volontairement non branchee a une vraie SELARL.
- `src/sydel_doc_engine/front_app/legacy_boundary.py` : place explicite du legacy.

Surface exposee par le nouveau point d'entree :

- `Type de dossier`
- `Donnees a saisir`
- `Generation`

Non exposes :

- Assistant metier prototype.
- Document unitaire.
- Technique / diagnostic.
- Debug interne.
- Ecrans historiques.
- Panneaux internes.

## Place du legacy

Reutilise :

- `front_data/` comme fondation metier/data.
- `ui_runtime.py` plus tard comme adaptateur moteur DOCX/PDF/ZIP, pas dans ce ticket.

Ignore par le nouveau chemin :

- `business_wizard.py`
- `single_document_mode.py`
- `streamlit_app.py`
- prefills historiques et panneaux diagnostic

A supprimer plus tard :

- panneaux debug et duplication d'ecrans quand le nouveau front aura une vertical slice equivalente.

## Suite SELARL sans implementation metier

La future vertical slice SELARL pourra se brancher ainsi :

1. activer un type de dossier generable dans `dossier_selection.py` ;
2. etendre `data_entry.py` avec les blocs SELARL valides ;
3. ajouter un adaptateur propre entre l'entree clean et le moteur ;
4. rebrancher DOCX/ZIP/PDF via `ui_runtime.py`.

Ce ticket ne code pas la vraie logique metier SELARL et ne modifie aucun wording juridique.

