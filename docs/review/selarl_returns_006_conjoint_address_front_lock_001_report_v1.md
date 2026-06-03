# Rapport SELARL - verrou front adresse conjoint

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001`

## Declencheur

Gad a confirme, apres retour associe, que le front pouvait encore afficher ou
porter une adresse conjoint dans le parcours `Documents regime de la communaute`.
Le retour humain 006 disait pourtant :

- l'adresse du conjoint est identique a celle de l'associe ;
- supprimer la variable `adresse du conjoint` de l'interface ;
- associer naturellement l'adresse du conjoint a l'adresse personnelle.

## Auto-critique

Le traitement precedent etait trop local.

Ce qui avait ete corrige :

- le rendu `DOC-006` utilisait l'adresse personnelle de l'associe/signataire ;
- le champ visible simple n'etait plus demande dans une partie du front ;
- des tests prouvaient que le generateur ignorait une ancienne adresse conjoint.

Ce qui manquait :

- verifier toutes les branches front, pas seulement le rendu document ;
- supprimer les anciennes cles `conjoint_adresse_*` du clean front ;
- retirer le champ technique `conjoint_adresse` de l'ancien formulaire simple ;
- retirer `adresse_conjoint` des exigences `DOC-006` dans le schema SELARL ;
- ajouter des tests qui prouvent l'absence du champ dans les parcours UI
  regime communautaire.

## Corrections appliquees

### Clean front `front_app`

- suppression des cles de prefill `selarl_conjoint_adresse_*` ;
- suppression des champs `conjoint_adresse_*` du modele `SelarlSliceInput` ;
- suppression des retours `conjoint_adresse_*` dans `_render_conjoint` ;
- discard explicite des anciennes cles `conjoint_adresse_*` dans
  `build_clean_data_entry` pour neutraliser tout etat Streamlit ancien.

### Front historique / assistant metier

- suppression du champ `conjoint_adresse` de `FrontDossierSimpleEntry` ;
- suppression de la lecture `front_entry_conjoint_adresse` dans le session state ;
- suppression de `adresse_conjoint` des variables requises `DOC-006` ;
- tests ajoutés sur l'assistant metier : `Identite du conjoint` reste visible,
  mais aucune combinaison label/cle `adresse + conjoint` ne doit apparaitre.

### Docs actives corrigees

- `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md` ;
- `docs/project/SELARL_PROCESS_SPEC_V1.md` ;
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`.

La formulation active est maintenant : adresse conjoint derivee depuis l'adresse
personnelle de l'associe/signataire, jamais demandee comme champ front separe.

## Verifications

Recherches code :

- plus de champ applicatif `selarl_conjoint_adresse` ;
- plus de lecture `front_entry_conjoint_adresse` ;
- plus de variable requise `adresse_conjoint` ;
- seules occurrences restantes dans `src/` et `tests/` : discard legacy et
  assertions negatives.

Tests cibles anti-regression :

```text
pytest tests/unit/test_clean_front_app.py::test_clean_front_selarl_regime_does_not_require_conjoint_address tests/unit/test_clean_front_app.py::test_clean_front_selarl_regime_ui_never_exposes_conjoint_address_fields tests/unit/test_business_wizard.py::test_business_prefill_complex_selarl_scenarios_show_expected_blocks tests/unit/test_selarl_form_schema.py::test_doc_006_is_generable_without_source_reserve tests/unit/test_selarl_form_schema.py::test_regime_conjoint_schema_does_not_expose_conjoint_address_variable tests/unit/test_front_generation_actions.py::test_front_generation_regime_communautaire_adds_doc_005_and_doc_006 -q
```

Resultat : `6 passed`.

Ruff cible :

```text
ruff check src/sydel_doc_engine/front_app/data_entry.py src/sydel_doc_engine/front_app/shell.py src/sydel_doc_engine/front_app/selarl_slice.py src/sydel_doc_engine/app/front_dossier_entry.py src/sydel_doc_engine/app/streamlit_app.py src/sydel_doc_engine/app/selarl_form_schema.py tests/unit/test_clean_front_app.py tests/unit/test_business_wizard.py tests/unit/test_front_generation_actions.py tests/unit/test_selarl_form_schema.py
```

Resultat : `All checks passed!`

## Limite de validation large

Le paquet large cible a execute `107 passed`, puis `7 errors` liees aux acces
Windows aux dossiers temporaires de pytest / tempfile. Les erreurs observees
sont des `PermissionError` sur `AppData\Local\Temp`, `C:\tmp` ou les dossiers
temporaires de workspace, pas des echecs d'assertion metier.

Les smokes DOCX utilisant `tmp_path` restent donc a relancer dans un
environnement temporaire Windows propre avant de presenter cette correction
comme pack final pousse.

## Verdict

`DONE` cote correction front/adresse conjoint.

Le retour associe est fonde : la correction precedente n'avait pas verrouille
toutes les branches front. Le front et le schema actif sont maintenant alignes
sur la regle : aucune saisie adresse conjoint, derivee depuis l'adresse
personnelle.
