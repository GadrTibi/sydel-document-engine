# Audit merge/worktrees MERGE-AUDIT-001

Date : 2026-05-18

Workspace audite : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`

## Objet

Verifier qu'aucun travail utile des anciens worktrees ou branches locales/remotes
du projet SYDEL Document Engine n'est reste non repris dans `main`.

Contraintes respectees pendant cet audit :

- aucun code applicatif modifie ;
- aucun merge ;
- aucun cherry-pick ;
- aucune suppression de branche ;
- aucune suppression de dossier ;
- aucune UI relancee ;
- seul ce rapport markdown est ajoute.

## Reserve importante sur l'etat Git

Au tout debut de l'audit, `git status` indiquait :

```text
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

Pendant l'audit, un commit local est apparu sur `main` sans action de
MERGE-AUDIT-001 :

```text
59f40fd docs: add final review execution report
```

Ce commit ajoute/met a jour :

- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`
- `docs/review/review_final_001_execution_report_v1.md`

Etat observe apres apparition de ce commit et avant creation du present rapport :

```text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
nothing to commit, working tree clean
```

Verification finale apres creation du present rapport :

```text
main       = 59f40fd
origin/main = 59f40fd
```

Conclusion de cette reserve : le commit concurrent `59f40fd` est maintenant
present dans la ref locale `origin/main`. Le seul ecart de working tree laisse
par MERGE-AUDIT-001 est le present rapport non suivi.

## Commandes executees

Depuis le dossier canonique :

- `git status`
- `git branch -vv`
- `git remote -v`
- `git log --oneline -10`
- `git worktree list --porcelain`
- `git fetch --all --prune`
- `git branch --merged main`
- `git branch --no-merged main`
- `git log --oneline main..BRANCHE`
- `git diff --name-status main...BRANCHE`
- `git diff --stat main...BRANCHE`
- `git cherry -v main BRANCHE`
- controles `git status --porcelain` dans les worktrees listés
- inspection des dossiers visibles dans `C:\Users\Gad\Desktop\Sydel`

Le rafraichissement des refs a echoue deux fois :

```text
error: cannot open '.git/FETCH_HEAD': Permission denied
```

L'audit repose donc sur les refs locales/remotes deja presentes avant refresh.

Remote observe :

```text
origin https://github.com/GadrTibi/sydel-document-engine.git (fetch)
origin https://github.com/GadrTibi/sydel-document-engine.git (push)
```

## Synthese Git

Derniers commits sur `main` local apres apparition du commit concurrent :

```text
59f40fd docs: add final review execution report
4d7cbce chore: cleanup codex worktrees and clarify ui status v1
caa85f1 feat: sync final ui and closeout foundations v1
d8f3bbf feat: sync ui pdf recipe foundation v1
f2d8937 docs: add final recipe framework v1
5864fe8 feat: add pdf export backend v1
161adba docs: add ui form schema v1
9aee882 docs: add ui document occurrences v1
25ca40f docs: add ui flow v1
c946eee feat: reconcile and close docx engine v1
```

Branches locales topologiquement mergees dans `main` :

- `codex/code-bail-app-001`
- `codex/code-scm-cession-block-001`
- `codex/style-analyse-batch-001`
- `codex/ui-wizard-001`
- `fix/bootstrap-hatch-wheel`
- `main`

Branches locales non mergees topologiquement : nombreuses branches `codex/*`
anciennes. La plupart sont non mergees seulement parce que leur travail a ete
repris par cherry-pick, sync wave ou reimplementation ulterieure.

## Methode d'analyse

Pour chaque branche suspecte, l'audit distingue :

- `main..BRANCHE` : commits topologiquement absents de `main` ;
- `git cherry -v main BRANCHE` : equivalence de patch avec `main` ;
- `main...BRANCHE` : fichiers du travail original depuis le point de fork ;
- etat reel du projet : presence des specs, generateurs, tests, docs de revue
  et rapports de sync dans `main`.

Important : beaucoup de branches anciennes ont un `git diff main BRANCHE`
volumineux parce qu'elles ne contiennent pas les commits plus recents de
`main`. Cela ne signifie pas que `main` a perdu leur travail.

## Branches non mergees sans travail utile oublie

Ces branches sont non mergees topologiquement, mais `git cherry` indique que
leurs commits propres sont deja equivalents a des commits de `main` (`-`), ou
que leur contenu est explicitement repris dans les rapports de synchronisation.

| Branche | Avance/retard vs main | Commits `main..branche` | Fichiers concernes | Diagnostic | Recommandation |
|---|---:|---|---|---|---|
| `codex-spec-cession-bail-001` | +1 / -88 | specs cession/bail | `docs/delivery/lot_03_*` | Specs presentes dans `main`. | Supprimer branche apres backup distant. |
| `codex-spec-derog-001` | +1 / -88 | spec derogations | `docs/delivery/lot_03_derogations_*` | Spec presente dans `main`. | Supprimer branche apres backup distant. |
| `codex/arbitrage-cession-001` | +2 / -77 | arbitrages SPFPL + cession | `docs/delivery/*arbitrages*` | Arbitrages repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/arbitrage-derog-001` | +1 / -77 | arbitrage derogations | `docs/delivery/lot_03_derogations_arbitrages_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/arbitrage-spfpl-001` | +1 / -77 | branche locale mal alignee sur derogations | `docs/delivery/lot_03_derogations_arbitrages_v1.md` | Pas de contenu SPFPL unique local ; remote SPFPL existe et est repris. | Supprimer branche locale. |
| `codex/arbitrage-statuts-civils-001` | +1 / -57 | arbitrage statuts civils | `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/arbitrage-statuts-scm-001` | +1 / -45 | arbitrage statuts SCM | `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/arbitrage-statuts-sel-001` | +2 / -62 | spec + arbitrage SEL | `docs/delivery/lot_04_statuts_sel_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-acte-actions-001` | +1 / -29 | generateur acte actions | `src/generators/lot_05`, tests, contexte | Generateur present dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-cession-cab-001` | +1 / -68 | generateurs cession cabinets | `src/generators/lot_03`, tests, sources | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-derog-core-001` | +2 / -68 | cession + derogations core | `src/generators/lot_03`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-option-is-001` | +1 / -45 | lettre option IS | `src/generators/lot_05`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-sas-satellites-001` | +1 / -39 | satellites SAS | `src/generators/lot_05`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-scm-liste-depenses-001` | +1 / -20 | liste depenses SCM | `src/generators/lot_05`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-spfpl-agr-info-001` | +1 / -71 | agrement/info SPFPL | `src/generators/lot_05`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-spfpl-core-001` | +1 / -65 | coeur SPFPL | `src/generators/lot_05`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-statuts-civils-core-001` | +1 / -48 | statuts civils core | `src/generators/lot_04`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-statuts-sas-001` | +2 / -62 | statuts SAS | `src/generators/lot_04`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-statuts-scm-001` | +1 / -34 | statuts SCM | `src/generators/lot_04`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/code-statuts-sel-001` | +1 / -52 | statuts SEL | `src/generators/lot_04`, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/convert-derog-salariee-001` | +1 / -39 | rapport conversion salariee | `docs/delivery/*derogation_salariee*` | Blocage documente dans `main`. | Supprimer branche apres backup distant. |
| `codex/fix-style-letters-001` | +1 / -49 | style lettres | `rendering/docx_builder.py`, generateurs | Repris et supersede par styles ulterieurs. | Supprimer branche apres backup distant. |
| `codex/fix-style-statuts-batch-001` | +1 / -20 | style statuts | generateurs Lot 04, tests | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/pdf-backend-001` | +1 / -9 | backend PDF | `src/rendering/pdf_export.py`, tests | Present dans `main`; revue finale signale reserve environnementale seulement. | Supprimer branche apres backup distant. |
| `codex/prep-acte-actions-001` | +1 / -45 | audit source acte actions | `docs/delivery/lot_05_acte_cession_actions_audit_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/prep-derog-001` | +1 / -71 | preparation sources derogations | sources Lot 03, docs delivery | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/prep-scm-sat-001` | +1 / -45 | preparation satellites SCM | sources Lot 05, docs delivery | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/prep-statuts-001` | +1 / -68 | preparation statuts | sources Lot 04, docs delivery | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/recipe-frame-001` | +1 / -9 | framework recette finale | `docs/review/final_recipe_framework_v1.md` | Present dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-acte-actions-001` | +2 / -39 | specs acte actions | `docs/delivery/lot_05_acte_cession_actions_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-rc-001` | +1 / -88 | spec regime communautaire | `docs/delivery/lot_02_regime_communautaire_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-sas-satellites-001` | +1 / -45 | specs satellites SAS | `docs/delivery/lot_05_sas_satellites_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-scm-cession-block-001` | +1 / -29 | spec blocage cession SCM | `docs/delivery/lot_05_scm_cession_block_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-scm-satellites-001` | +1 / -39 | specs satellites SCM | `docs/delivery/lot_05_scm_satellites_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-spfpl-001` | +1 / -88 | spec SPFPL | `docs/delivery/lot_05_spfpl_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-statuts-civils-001` | +1 / -62 | specs statuts civils | `docs/delivery/lot_04_statuts_civils_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-statuts-sas-001` | +1 / -62 | specs statuts SAS | `docs/delivery/lot_04_statuts_sas_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-statuts-sel-001` | +1 / -62 | specs statuts SEL | `docs/delivery/lot_04_statuts_sel_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-statuts-spfpl-001` | +1 / -62 | specs statuts SPFPL | `docs/delivery/lot_04_statuts_spfpl_*` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-texte-bail-app-001` | +1 / -82 | spec texte bail/appel | `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-texte-cession-cab-001` | +1 / -82 | spec texte cession | `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-texte-derog-001` | +1 / -82 | spec texte derogations | `docs/delivery/lot_03_derogations_spec_texte_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/spec-texte-spfpl-001` | +1 / -82 | spec texte SPFPL | `docs/delivery/lot_05_spfpl_spec_texte_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/style-analyse-lot03-batch-001` | +1 / -29 | blueprint style Lot 03 | `docs/delivery/render_style_blueprint_lot03_batch_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/style-analyse-statuts-batch-001` | +1 / -29 | blueprint style statuts | `docs/delivery/render_style_blueprint_statuts_batch_v1.md` | Repris dans `main`. | Supprimer branche apres backup distant. |
| `codex/ui-flow-001` | +1 / -9 | spec UI flow | `docs/project/19_UI_FLOW_V1.md` | Present dans `main`. | Supprimer branche apres backup distant. |

## Branches non mergees avec commits `git cherry +`

Ces branches contiennent au moins un commit non equivalent par patch-id. Apres
controle fonctionnel, elles ne revelent pas de travail applicatif utile oublie.

| Branche | Commits `+` principaux | Fichiers concernes | Travail probablement utile ? | Deja repris dans `main` ? | Recommandation |
|---|---|---|---|---|---|
| `codex/arbitrage-scm-cession-resolve-001` | resolution SCM cession | `docs/delivery/lot_05_scm_cession_block_resolution_v1.md` | Oui, mais deja exploite. | Oui, finalisation SCM cession presente et DOC-031 a DOC-033 exposes. | Archiver/supprimer apres backup. |
| `codex/audit-remaining-scope-001` | preparation liste depenses SCM non equivalente | docs audit, sources SCM, satellites SAS | Oui historiquement. | Oui, audit restant et satellites/listes sont presents dans `main`; patch-id diverge apres sync. | Archiver/supprimer apres backup. |
| `codex/close-motor-audit-001` | prep liste depenses + style Lot 03 | audit moteur, style Lot 03 | Oui historiquement. | Oui, audit moteur, style Lot 03 et finalisations sont presents dans `main`. | Archiver/supprimer apres backup. |
| `codex/code-scm-sat-docx-001` | satellites SCM DOCX | generateurs/tests SCM satellites | Oui historiquement. | Oui, satellites SCM et tests sont dans `main`. | Archiver/supprimer apres backup. |
| `codex/code-statuts-spfpl-001` | statuts SPFPL | generateurs/tests Lot 04 SPFPL | Oui historiquement. | Oui, generateurs statuts SPFPL presents dans `main`. | Archiver/supprimer apres backup. |
| `codex/convert-acte-actions-001` | conversion source acte actions | source DOCX + preparation | Oui historiquement. | Oui, source/preparation et generateur acte actions presents dans `main`. | Archiver/supprimer apres backup. |
| `codex/final-motor-audit-002` | audit qualite final | `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md` | Oui historiquement. | Oui, audit final present dans `main`. | Archiver/supprimer apres backup. |
| `codex/fix-style-lot03-batch-001` | style Lot 03 | generateurs Lot 03 + rendu commun | Oui historiquement. | Oui, style Lot 03 repris puis supersede par finalisations. | Archiver/supprimer apres backup. |
| `codex/next-phase-foundation-001` | fondation phase suivante | `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md` | Oui historiquement. | Oui, fondation presente dans `main`. | Archiver/supprimer apres backup. |
| `codex/prep-scm-cession-sources-001` | preparation sources SCM cession | sources/docs Lot 05 | Oui historiquement. | Oui, sources SCM cession et specs/finalisation presentes. | Archiver/supprimer apres backup. |
| `codex/prep-scm-liste-depenses-convert-001` | preparation liste depenses | source liste depenses + preparation | Oui historiquement. | Oui, liste depenses SCM codee et source presente sous nom normalise. | Archiver/supprimer apres backup. |
| `codex/review-batch-lot03-001` | revue Lot 03 + commits precedents | `docs/review/lot_03_batch_review_v1.md` | Oui historiquement. | Oui, revue Lot 03 presente dans `main`. | Archiver/supprimer apres backup. |
| `codex/review-batch-lot04-001` | revue Lot 04 + commits precedents | `docs/review/lot_04_batch_review_v1.md` | Oui historiquement. | Oui, revue Lot 04 presente dans `main`. | Archiver/supprimer apres backup. |
| `codex/review-batch-lot05-001` | revue Lot 05 + commits precedents | `docs/review/lot_05_batch_review_v1.md` | Oui historiquement. | Oui, revue Lot 05 presente dans `main`. | Archiver/supprimer apres backup. |
| `codex/review-final-001` | pack revue finale | `docs/review/final_review_pack_v1.md` | Oui historiquement. | Oui, pack present dans `main`; le rapport d'execution est dans `59f40fd`, aligne sur `origin/main` en fin d'audit. | Archiver/supprimer apres backup. |
| `codex/spec-derog-salariee-manual-001` | strategie salariee manuelle | `docs/delivery/lot_03_derogation_salariee_v1_strategy.md` | Oui historiquement. | Oui, strategie presente dans `main`. | Archiver/supprimer apres backup. |
| `codex/ui-form-schema-001` | schema formulaire UI | `docs/project/21_UI_FORM_SCHEMA_V1.md` | Oui historiquement. | Oui, doc 21 presente dans `main`. | Archiver/supprimer apres backup. |
| `codex/ui-pdf-zip-integration-001` | integration UI/PDF/ZIP | `src/sydel_doc_engine/app`, `docs/review/ui_pdf_zip*`, tests | Oui historiquement. | Oui, UI technique, PDF/ZIP et tests presents dans `main`; branche ancienne ne contient pas le cleanup final. | Archiver/supprimer apres backup. |
| `codex/zip-backend-001` | backend ZIP + commits historiques | `src/rendering/zip_bundle.py`, tests | Oui historiquement. | Oui, backend ZIP present dans `main`. | Archiver/supprimer apres backup. |
| `codex/ui-occurrences-001` | `docs/project/20`, puis commit local `5319c1a` avec `.codex_tmp`, raw dump et sources | `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`, `project/source_import/raw_drive_dump`, `.codex_tmp`, quelques sources | La doc 20 est utile mais deja reprise ; le reste ressemble a import brut/temporaire ou source locale non destinee a etre versionnee. Aucun wizard metier complet. | Oui pour la doc UI ; non volontairement pour raw dump/temp. | Ne pas merger. Archiver avant suppression ; recuperation manuelle seulement si un humain veut sauvegarder `.codex_tmp` ou raw dump versionne. |

## Branches mergees ou identiques

| Branche | Statut | Diagnostic | Recommandation |
|---|---|---|---|
| `codex/code-bail-app-001` | mergee dans `main` | Aucun commit unique. | Supprimable apres backup. |
| `codex/code-scm-cession-block-001` | mergee dans `main` | Aucun commit unique. | Supprimable apres backup. |
| `codex/style-analyse-batch-001` | mergee dans `main` | Aucun commit unique. | Supprimable apres backup. |
| `codex/ui-wizard-001` | pointe sur `4d7cbce`, donc ancien `main` avant `59f40fd` | Ne contient pas de wizard metier ; nom trompeur. | Supprimable apres backup ; ne pas relancer. |
| `fix/bootstrap-hatch-wheel` | mergee dans `main` | Ancien correctif bootstrap. | Supprimable apres backup. |

## Worktrees et dossiers visibles

`git worktree list --porcelain` liste 20 worktrees attaches. Tous les anciens
worktrees attaches controles sont propres (`git status --porcelain` vide).

| Dossier / branche | Statut Git | Commits uniques ? | Fichiers concernés | Travail probablement utile ? | Deja repris dans main ? | Risque si suppression | Recommandation |
|---|---|---|---|---|---|---|---|
| `sydel-document-engine` / `main` | `59f40fd`, aligne avec `origin/main`; present rapport non suivi | Aucun commit unique face a `origin/main`; rapport MERGE-AUDIT non suivi | board, last state, rapport revue finale, present rapport | Oui | Oui pour `59f40fd`; present rapport a commit si conserve | Perdre le present rapport si non committe/sauvegarde | Conserver ; decider si ce rapport doit etre committe. |
| `sydel-document-engine-arbitrage-scm-cession-resolve-001` / `codex/arbitrage-scm-cession-resolve-001` | worktree propre | 1 topologique | resolution SCM cession | Deja exploite | Oui | Faible apres backup | Archiver puis supprimer. |
| `sydel-document-engine-civils-core` / `codex/code-statuts-civils-core-001` | propre | 1 topologique, patch equivalent | statuts civils | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-code-acte-actions-001` / `codex/code-acte-actions-001` | propre | 1 topologique, patch equivalent | acte actions | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-code-scm-liste-depenses-001` / `codex/code-scm-liste-depenses-001` | propre | 1 topologique, patch equivalent | liste depenses SCM | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-code-scm-sat-docx-001` / `codex/code-scm-sat-docx-001` | propre | 2 topologiques dont 1 `cherry +` | satellites SCM | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-code-statuts-scm-001` / `codex/code-statuts-scm-001` | propre | 1 topologique, patch equivalent | statuts SCM | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-convert-derog-salariee-001` / `codex/convert-derog-salariee-001` | propre | 1 topologique, patch equivalent | blocage conversion | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-final-motor-audit-002` / `codex/final-motor-audit-002` | propre | 1 topologique, `cherry +` | audit qualite final | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-fix-style-statuts-batch-001` / `codex/fix-style-statuts-batch-001` | propre | 1 topologique, patch equivalent | style statuts | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-pdf-backend-001` / `codex/pdf-backend-001` | propre | 1 topologique, patch equivalent | backend PDF | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-recipe-frame-001` / `codex/recipe-frame-001` | propre | 1 topologique, patch equivalent | recette finale | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-review-final-001` / `codex/review-final-001` | propre | 1 topologique, `cherry +` | pack revue finale | Deja exploite | Oui, avec complement `59f40fd` maintenant aligne sur `origin/main` | Faible apres backup | Archiver puis supprimer. |
| `sydel-document-engine-spec-scm-cession-block-001` / `codex/spec-scm-cession-block-001` | propre | 1 topologique, patch equivalent | spec blocage SCM | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-spec-scm-satellites-001` / `codex/spec-scm-satellites-001` | propre | 1 topologique, patch equivalent | specs satellites SCM | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-style-analyse-lot03-batch-001` / `codex/style-analyse-lot03-batch-001` | propre | 1 topologique, patch equivalent | blueprint Lot 03 | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-style-statuts` / `codex/style-analyse-statuts-batch-001` | propre | 1 topologique, patch equivalent | blueprint statuts | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-ui-flow-001` / `codex/ui-flow-001` | propre | 1 topologique, patch equivalent | doc UI flow | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-ui-pdf-zip-integration-001` / `codex/ui-pdf-zip-integration-001` | propre | 1 topologique, `cherry +` | UI technique, PDF/ZIP | Deja exploite | Oui | Faible | Archiver puis supprimer. |
| `sydel-document-engine-zip-backend-001` / `codex/zip-backend-001` | propre | 7 topologiques, 4 `cherry +` | ZIP + commits historiques | Deja exploite | Oui | Faible | Archiver puis supprimer. |

Dossiers non worktree observes dans `C:\Users\Gad\Desktop\Sydel` :

| Dossier | Statut | Diagnostic | Recommandation |
|---|---|---|---|
| `_codex_worktrees_archive` | dossier non Git, vide lors du controle | Archive cible mais pas encore peuplee. | Conserver comme cible d'archivage. |
| `_TO_DELETE_sydel-document-engine-sync-main` | dossier non Git, 403 fichiers, pas de `.git` | Copie ancienne sans historique Git ; contient etat avant `REVIEW-FINAL-001` execute. | Archiver/supprimer apres backup, pas a relancer. |
| `.ipynb_checkpoints` | non Git | Hors perimetre moteur. | Supprimable hors Git si confirme inutile. |
| `Notebooks` | non Git | Hors perimetre moteur. | Conserver ou traiter hors audit Git. |

## Remote branches

Les remotes inspectees ont presque toutes une branche locale correspondante.
Points notables :

- `origin/main` pointe sur `59f40fd` dans les refs locales a la verification
  finale.
- `main` local pointe sur `59f40fd` et est aligne avec `origin/main`.
- `origin/codex/ui-occurrences-001` pointe sur `24a881b`, tandis que la branche
  locale `codex/ui-occurrences-001` pointe sur `5319c1a` avec un commit local
  supplementaire contenant notamment `.codex_tmp` et `raw_drive_dump`.
- `origin/codex/close-motor-audit-001` pointe sur `0139202`, alors que la
  branche locale `codex/close-motor-audit-001` pointe sur `bdf6116`.

Ces divergences ne changent pas la conclusion fonctionnelle : le contenu utile
est repris dans `main`. Le commit `59f40fd` n'est plus un ecart local face a la
ref `origin/main` observee en fin d'audit.

## Conclusion

Peut-on considerer `main` comme complet ?

- Oui pour le `main` local actuel `59f40fd`.
- Oui pour la ref locale `origin/main`, qui pointe aussi sur `59f40fd` a la
  verification finale.
- Reserve : `git fetch --all --prune` echoue toujours sur `.git/FETCH_HEAD`, ce
  qui limite la garantie sur un refresh distant effectif pendant cet audit.

Y a-t-il du travail utile oublie dans les anciennes branches/worktrees ?

- Aucun travail applicatif utile oublie n'a ete identifie.
- Aucun wizard metier complet cache n'a ete trouve.
- Les seuls contenus non repris volontairement sont des imports bruts,
  `.codex_tmp`, `.codex/config.toml` ou variantes de sources locales qui ne
  doivent pas etre mergees sans decision explicite.

Branches/dossiers a traiter avant l'UI :

1. Decider si le present rapport `docs/project/merge_audit_001.md` doit etre
   committe.
2. Corriger le blocage local `.git/FETCH_HEAD` pour permettre `git fetch --all --prune`.
3. Archiver les anciens worktrees propres, sans les relancer.
4. Ne pas utiliser `codex/ui-wizard-001` : elle ne contient pas le wizard metier.
5. Ne pas merger `codex/ui-occurrences-001` : la partie utile est deja reprise,
   le reste est brut/temporaire.

Peut-on lancer `UI-BUSINESS-WIZARD-001` sans risque ?

- Oui depuis le dossier canonique local, avec les reserves deja documentees par
  `REVIEW-FINAL-001`.
- Le ticket UI doit partir des specs `docs/project/19_UI_FLOW_V1.md`,
  `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md` et
  `docs/project/21_UI_FORM_SCHEMA_V1.md`, et non d'une ancienne branche.
- Le futur wizard doit continuer a deleguer la selection documentaire a
  l'orchestrateur et ne doit pas presenter la generation comme validation
  juridique.

Prochaine etape recommandee :

1. decider si ce rapport doit etre committe ;
2. reparer le probleme `.git/FETCH_HEAD` ;
3. lancer `UI-BUSINESS-WIZARD-001` depuis le dossier canonique.
