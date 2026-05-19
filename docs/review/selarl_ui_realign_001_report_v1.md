# Rapport SELARL-UI-REALIGN-001

## Objet

Réaligner le parcours UI Streamlit visible du pilote SELARL sur le wording, le flow et les règles de réutilisation corrigés, sans modifier les générateurs, le moteur DOCX/PDF/ZIP, `case_catalog.py`, le parcours SCI ou le mode `Technique / diagnostic`.

## Fichiers modifiés

- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_business_wizard.py`
- `docs/project/SELARL_UI_WIZARD_SPEC_V1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`
- `docs/review/selarl_ui_realign_001_report_v1.md`

## Ancien rendu visible

Le parcours Streamlit SELARL committé techniquement affichait encore :

1. Qualification ;
2. Société ;
3. Fiche Client ;
4. Associés ;
5. Conditions spécifiques ;
6. Documents attendus ;
7. Génération.

Il exposait aussi plusieurs réutilisations cochées par défaut, dont le mandataire copié depuis le signataire, et la génération apparaissait comme un écran séparé.

## Nouveau rendu visible

Le parcours visible consomme désormais les titres dérivés du flow SELARL :

1. Écran 1 — Qualification ;
2. Écran 2 — Fiche Client ;
3. Écran 3 — Fiche Société ;
4. Écran 4 — Capital & Associés ;
5. Écran 5 — Contexte & scénarios métier ;
6. Écran 6 — Documents & génération.

La Fiche Client précède la Fiche Société. Les documents attendus, réserves, champs manquants et actions de génération sont regroupés dans l'écran 6. Aucun écran 7 n'est conservé.

## Consommation du schéma et des projections

`streamlit_app.py` consomme :

- `selarl_ui_visible_screen_title(...)`, qui dérive les titres depuis `selarl_ui_flow_steps()` ;
- `selarl_ui_visible_fields_by_step(...)` pour le contexte visible ;
- `selarl_ui_reuse_projection(...)` pour l'effet des réutilisations ;
- `selarl_ui_reuse_rules()` pour les libellés, effets, défauts et comportements inactifs ;
- `selarl_ui_document_specs()` pour la synthèse documentaire SELARL.

Aucune logique métier documentaire parallèle n'a été ajoutée dans Streamlit.

## Dossier unipersonnel

`Dossier unipersonnel` est affiché dans la qualification via le champ du schéma `qualification.dossier_unipersonnel`.

Quand l'option est active, l'UI affiche : `Le Praticien est l’associé unique, le gérant et le signataire`. Les champs dérivés associés et gérant sont préremplis ou verrouillés depuis la Fiche Client / Praticien, avec indication de provenance.

Quand l'option est inactive, les liens Praticien / associé / gérant / signataire ne sont pas imposés.

## Bloc mandataire

Le mandataire n'est plus présenté comme sujet central. Il est déplacé dans un expander secondaire replié : `Mandataire (DOC-034 / formalité)`.

Le texte visible indique que le mandataire n'est pas assimilé au signataire par défaut. La case `Copier le signataire vers le mandataire` utilise `default_enabled=False` depuis le schéma.

## DOC-006 / DOC-013 / DOC-014

- `DOC-006` reste visible avec sa réserve source V2.
- `DOC-013` et `DOC-014` restent visibles quand la dérogation est active, mais restent `MANUAL_ONLY` et exclus de la génération.
- Le PV d'autorisation d'emprunt n'est pas affiché comme document autonome ; l'emprunt reste une option du `DOC-004`.

## Limites restantes avant smoke

- Le rendu Streamlit est réaligné conceptuellement, mais pas encore validé sur dossier réaliste complet.
- Le prochain ticket doit vérifier un scénario SELARL unipersonnel, un scénario chirurgien-dentiste avec régime communautaire et un scénario avec cession.
- Aucun push ou redéploiement ne doit être fait avant ce smoke réaliste.

## Tests lancés

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py` : OK, 34 tests passés.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 257 tests passés.

## Prochaine étape recommandée

Lancer `SELARL-SMOKE-REALISTIC-001`.
