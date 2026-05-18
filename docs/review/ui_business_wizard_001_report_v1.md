# Rapport UI-BUSINESS-WIZARD-001

Date : 2026-05-18

Workspace : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`

## Objet

Creation d'une premiere interface Streamlit metier, sobre et dossier-centree,
en conservant l'ancienne interface YAML/JSON comme mode technique / diagnostic.

## Fichiers modifies

- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/ui_runtime.py`
- `tests/unit/test_business_wizard.py`
- `docs/review/ui_business_wizard_001_report_v1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`

## Parcours UI cree

Mode principal : `Assistant metier`.

Parcours affiche :

1. Type de dossier metier.
2. Informations du dossier par sections : societe, associes / personnes
   physiques, dirigeant / pharmacien, domiciliation, capital / parts, dates,
   options documentaires.
3. Documents generables avec code, nom, statut et champs manquants.
4. Validation avec nombre de documents generables, documents bloques, champs
   manquants et incoherences.
5. Generation via boutons separes : DOCX, ZIP, PDF.
6. Telechargements DOCX, ZIP et PDF si disponibles.

Mode conserve : `Technique / diagnostic`.

Le mode technique garde le chargement YAML/JSON, la selection orchestrateur, la
generation dossier DOCX/PDF optionnel/ZIP et les telechargements existants.

## Documents supportes en V1

Le perimetre metier generable de cette V1 est volontairement limite au scenario
SCI simple recette par `REVIEW-FINAL-001` :

- `DOC-001` : Declaration sur l'honneur de non-condamnation.
- `DOC-002` : Autorisation de domiciliation.
- `DOC-003` : Procuration.
- `DOC-004` : PV nomination gerant.

Les autres structures connues du moteur sont affichees comme structures de
diagnostic V1. Le formulaire ne promet pas leur generation complete.

## Limites connues

- Le formulaire metier complet est limite a `SCI` pour ce ticket.
- Les structures `SELARL`, `SELAS`, `SPFPL cession`, `SPFPL apport`, `SCS`,
  `SCI IRIS`, `SCM` et `SAS` restent visibles mais non generables par le mode
  assistant V1.
- Les documents hors `DOC-001` a `DOC-004` sont marques indisponibles dans le
  mode assistant metier V1.
- Aucune clause ni formulation juridique n'a ete modifiee.
- La selection documentaire reste calculee par l'orchestrateur lorsque le
  contexte metier est construit.
- Le mode technique reste necessaire pour les contextes YAML/JSON complets
  hors assistant V1.

## Etat PDF

- Le backend PDF existant n'a pas ete modifie.
- L'UI detecte la disponibilite PDF via le backend existant.
- Le bouton PDF du mode assistant est desactive si aucun backend local fiable
  n'est detecte.
- En cas d'erreur PDF pendant la conversion, l'UI affiche un message et laisse
  les DOCX et le ZIP fonctionner.

## Tests lances

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Resultat : OK.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\unit\test_business_wizard.py tests\unit\test_ui_runtime.py tests\unit\test_orchestrator_service.py tests\unit\test_docx_builder.py tests\unit\test_zip_bundle.py
```

Resultat : 37 passed.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Resultat : 196 passed.

## Prochaine etape recommandee

Effectuer une recette manuelle du mode assistant Streamlit sur le scenario SCI
simple, puis lancer `CLOSE-PROJECT-V1-001` si la recette produit bien les DOCX,
le ZIP avec manifest et les telechargements attendus.
