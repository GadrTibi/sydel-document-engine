# Rapport SELARL-REUSE-RULES-REALIGN-001

## Objet

Réaligner les règles de réutilisation SELARL sur les arbitrages explicites de l'associé, NotebookLM et la hiérarchie de sources corrigée, sans modifier les générateurs, le moteur DOCX/PDF/ZIP, le catalogue métier ni le rendu juridique.

## Sources lues

- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`
- `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`
- `docs/project/SELARL_REBUILD_BACKLOG_V2.md`
- `docs/review/selarl_wording_realign_001_report_v1.md`
- `docs/review/selarl_flow_realign_001_report_v1.md`
- `src/sydel_doc_engine/app/selarl_form_schema.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `tests/unit/test_selarl_form_schema.py`
- `tests/unit/test_business_wizard.py`

## Règles anciennes

Le schéma exposait des liens utiles mais trop dispersés : signataire / associé 1, gérant / Praticien, signataire / Praticien, mandataire / signataire, SELARL acquéreur, SELARL cessionnaire SCM et domiciliation / siège. Le flow corrigé avait déjà placé ces règles au bon niveau conceptuel, mais il ne distinguait pas encore assez clairement le cas pivot `Dossier unipersonnel` des options de confort.

Le risque principal était de laisser croire que certains liens pouvaient être des défauts métier alors qu'ils ne sont valables que dans certains dossiers.

## Règles nouvelles

La logique est désormais organisée en trois niveaux :

- règle pivot : `Dossier unipersonnel` ;
- options explicites conservées ;
- relations sensibles documentées comme non automatiques.

Aucune règle de réutilisation SELARL n'est activée par défaut. Les projections métier exposent les règles actives, les cibles verrouillées et la liste des relations volontairement non automatiques.

## Règle Dossier unipersonnel

Quand `Dossier unipersonnel` est actif :

- le Praticien alimente l'associé unique ;
- le Praticien alimente le gérant ;
- le Praticien alimente le signataire ;
- les cibles dérivées sont déclarées verrouillables : `associes.associe_unique`, `dirigeant_nomine`, `mandataire_signataire.signataire`.

Quand `Dossier unipersonnel` est inactif :

- aucune dérivation Praticien / associé / gérant / signataire n'est imposée ;
- les options individuelles restent disponibles seulement si elles sont cochées explicitement ;
- le contexte documentaire SELARL reste inchangé.

## Réutilisations conservées

Les réutilisations suivantes restent disponibles avec opt-in clair :

- `La SELARL en création est l'acquéreur` : source `societe`, cible `cession.acquereur`, champs société et siège de l'acquéreur, active seulement si l'option est cochée ;
- `La SELARL en création est la cessionnaire des parts SCM` : source `societe`, cible `scm_cession.cessionnaire`, champs identité et siège du cessionnaire, active seulement si l'option est cochée ;
- `L'adresse de domiciliation est le siège social` : source `domiciliation`, cible `societe.siege`, champs d'adresse du siège, active seulement si l'option est cochée.

Les anciennes options individuelles signataire / associé, gérant / Praticien et signataire / Praticien restent lisibles pour compatibilité, mais elles ne remplacent pas la règle pivot et ne sont pas des défauts.

## Réutilisations retirées comme défauts

`mandataire = signataire` n'est plus un défaut. Le schéma conserve seulement une option `Copier le signataire vers le mandataire` pour `DOC-034`, si une variable ou un document l'exige. Le mandataire sort du cœur UX tant que le besoin documentaire ne justifie pas une saisie prioritaire.

## Réutilisations non automatiques

Les relations suivantes sont documentées comme non automatiques :

- vendeur = locataire actuel ;
- siège social = lieu d'exercice ;
- siège social = cabinet cédé ;
- cabinet cédé = lieu d'exercice ;
- vendeur = Praticien ;
- cédant SCM = Praticien.

Elles peuvent exister dans un dossier réel, mais doivent être confirmées par une option explicite ou une saisie séparée avant tout préremplissage.

## Impacts sur le schéma

`src/sydel_doc_engine/app/selarl_form_schema.py` ajoute :

- le champ `qualification.dossier_unipersonnel` ;
- `default_enabled` et `behavior_if_inactive` sur les règles de réutilisation ;
- la règle `dossier_unipersonnel` ;
- la liste `SELARL_NON_AUTOMATIC_REUSE_RELATIONS` ;
- la fonction `selarl_non_automatic_reuse_relations()`.

La validation du schéma vérifie désormais que `dossier_unipersonnel` existe, qu'aucune règle n'est active par défaut et que les relations non automatiques ne sont pas confondues avec les règles opt-in.

## Impacts sur les projections métier

`src/sydel_doc_engine/app/business_wizard.py` ajoute :

- `selarl_dossier_unipersonnel` dans l'entrée du wizard ;
- `SelarlReuseProjection` ;
- `selarl_ui_reuse_projection(...)` ;
- `selarl_ui_non_automatic_reuse_relations()`.

La projection active `dossier_unipersonnel` uniquement si l'option est cochée. Elle garde les options SELARL acquéreur, SELARL cessionnaire SCM et domiciliation / siège comme opt-in. Les documents attendus SELARL restent inchangés.

## Impacts UI visibles

`streamlit_app.py` n'a pas été modifié dans ce ticket. L'UI visible actuellement committée reste non validée produit et ne doit pas être poussée ou redéployée avant `SELARL-UI-REALIGN-001`.

Le prochain ticket UI devra exposer proprement `Dossier unipersonnel`, les champs dérivés verrouillables et les options explicites sans ajouter de mode Projet, filigrane ou couche produit documentaire lourde.

## Impacts tests

Les tests unitaires vérifient :

- l'existence de `Dossier unipersonnel` ;
- le lien Praticien = associé unique = gérant = signataire quand l'option est active ;
- l'absence de dérivation imposée quand l'option est inactive ;
- l'absence de défaut `mandataire = signataire` ;
- les options explicites SELARL acquéreur, SELARL cessionnaire SCM et domiciliation / siège ;
- l'absence d'automatisme vendeur / locataire, siège / cabinet / lieu d'exercice, vendeur / Praticien et cédant SCM / Praticien ;
- l'absence de régression sur les documents SELARL, `DOC-013` / `DOC-014` hors génération et `DOC-006` avec réserve.

Validations exécutées :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` : OK, 48 tests passés ;
- `.\.venv\Scripts\python.exe -m ruff check .` : OK ;
- `.\.venv\Scripts\python.exe -m pytest` : OK, 252 tests passés.

## Prochaine étape recommandée

Lancer `SELARL-UI-REALIGN-001` pour réaligner le parcours Streamlit visible sur le schéma et les projections maintenant corrigés, sans pousser ni redéployer avant validation.
