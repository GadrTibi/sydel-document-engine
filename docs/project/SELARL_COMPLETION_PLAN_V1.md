# Plan de complétion SELARL — V1 (autonomie + reprise)

Date : 2026-06-03 · Branche de travail : `review/selarl` (clone). **PUSH sur `review/selarl`
uniquement, JAMAIS `main`, JAMAIS de déploiement, JAMAIS de wording légal inventé.**

## Comment reprendre (après reset / nouvelle session)
1. Ouvrir le clone `C:\Users\Gad\Desktop\Sydel\sydel-document-engine-claude`, branche `review/selarl`.
2. Lire ce plan + le **JOURNAL D'AVANCEMENT** (bas du doc).
3. Continuer au **prochain bloc non terminé**. Tests : `python -m pytest -q -p no:cacheprovider --basetemp="C:/Users/Gad/pt_run"`.
4. Vérif pack : `python scripts/generate_pack.py --all`.

## Objectif
Passer la SELARL de ~75% à **~90% (la part codeable)**. Les **10% restants = bloqués Albane**
(statuts multi-associés complets — référence légale ligne-par-ligne requise) : **specs seulement,
pas de code**.

## État de départ (fait + validé en attente)
SELARL SIMPLE (médecin/dentiste + régime communautaire) = codée, packs OK, sur `review/selarl`,
en attente de validation Albane. Outil : `scripts/generate_pack.py` + `scenarios/selarl.py`.

## Rails (garde-fous autonomes)
- Clone only ; push `review/selarl` ; jamais `main` / déploiement / contact externe.
- **Spec de sous-cas AVANT code** (règle du projet : pas de cas complexe sans spec).
- Réutiliser les **générateurs existants** (déjà validés) — ne PAS réécrire de wording.
- **Sérialiser** : les blocs touchent des actifs partagés (`front_app/selarl_slice.py` :
  `SelarlSliceInput`, `build_generation_context`, `selected_selarl_document_codes` ;
  `domain/models.py`). Donc **un bloc à la fois**, tests verts avant le suivant.
- Chaque bloc fini → commit + push `review/selarl` + MAJ journal ci-dessous.

## Blocs CODEABLES (générateur prêt → câbler le front)

### Bloc 1 — Cession de cabinet (médical/dentaire) — DOC-007..012
- Moteur prêt : `generators/lot_03/cession_cabinets_common.py`
  (`generate_cession_cabinet_docx(ctx, out, CessionCabinetVariant(etape, type_cabinet))`),
  + `avenant_contrat_bail.py` (DOC-007) et `appel_fond_sel.py` (DOC-008) via `bail_appel_common.py`.
- Conditions (orchestrateur) : `_cession_cabinet_enabled` (cession.etape ∈ {acte,compromis} ×
  type_cabinet ∈ {medical,dentaire}) ; `_appel_fonds_enabled` (SELARL + dentaire) ;
  `_avenant_bail` (cession).
- À FAIRE : (a) lire le contexte requis (`domain/models.py` : `CessionContext` + champs cédant/
  cessionnaire/cabinet/prix/fonds/bail) ; (b) étendre `SelarlSliceInput` (champs cession) +
  `build_generation_context` (assembler `ctx.cession`, `ctx.dossier_options.cession=True`) +
  `selected_selarl_document_codes` (ajouter DOC-007..012 selon options) ; (c) sous-formulaire front
  dans `front_app/shell.py` ; (d) scénario `selarl_medecin_cession_*` dans `scenarios/selarl.py` ;
  (e) tests + `generate_pack`. Spec détaillée : voir `docs/delivery/lot_03_cession_*`.

### Bloc 2 — Cession SCM — DOC-031..033
- Moteur prêt : `generators/lot_05/scm_cession_common.py`
  (`validate_scm_cession_enabled` : structure {SELARL,SELAS} + `scm_cession.variante_structure`).
- À FAIRE : contexte `ScmCessionContext` (personne_1..4, répartitions avant/après, cédant/
  cessionnaire/crédit-vendeur) → étendre `SelarlSliceInput` + `build_generation_context` +
  codes ; sous-formulaire ; scénario ; tests. Spec : `docs/delivery/lot_05_scm_cession_*`.

### Bloc 3 — Bail / appel de fonds (si pas déjà couvert par Bloc 1) — DOC-007/008
- Moteur prêt : `bail_appel_common.py`. Vérifier que Bloc 1 ne l'a pas déjà couvert ; sinon finir.

## Blocs BLOQUÉS Albane (SPEC SEULEMENT, NE PAS CODER)
- Statuts multi-associés complets `DOC-016`/`DOC-017` (préambule/comparution/signatures pluriels).
- Médecin multi-associés, plusieurs gérants, président de séance externe, associé absent /
  quorum partiel / vote non unanime.
- → Produire : la spec du sous-cas + la **liste de questions précises pour Albane** (référence
  ligne-par-ligne du wording pluriel). Fichier : `docs/delivery/selarl_multi_associes_questions_albane_v1.md`.

## Hors code (manuel) : dérogation SEL BNC sans code, site distinct CD94.

---

## JOURNAL D'AVANCEMENT (mettre à jour à chaque étape)
| Date | Bloc | Étape | Statut | Commit |
|---|---|---|---|---|
| 2026-06-03 | — | Plan créé | ✅ | 7d12e6f |
| 2026-06-03 | Bloc 1 cession cabinet | Spec de sous-cas rédigée (avant code) | ✅ | docs/delivery/selarl_cession_cabinet_subform_spec_v1.md |
| 2026-06-04 | Bloc 1 cession cabinet | Câblage front : `cession_context` sur `SelarlSliceInput` + `build_generation_context` (ctx.cession + `dossier_options.cession`) + `selected_selarl_document_codes` + scénario `selarl_medecin_cession_cabinet_medical` + test positif. **Acte DOC-009 (cession cabinet médical) généré** (pack OK, 306 tests verts) | ✅ | (voir commit) |
| 2026-06-04 | Bloc 1 cession cabinet | Bail médical (DOC-007) câblé : `bail_context` sur `SelarlSliceInput` + `ctx.bail` + builder. Pack médical = 8 DOCX | ✅ | 14d37ff |
| 2026-06-04 | Bloc 1 cession cabinet | **Cession dentaire complète** : acte DOC-011 + bail DOC-007 + **appel de fonds DOC-008** (sélection DOC-008 si dentaire ; règles métier dentaire respectées : pas de crédit-vendeur ni SCM). Scénario `selarl_dentiste_cession_cabinet_dentaire`, pack = 9 DOCX, 307 tests verts | ✅ | (voir commit) |
| 2026-06-04 | Bloc 1 cession cabinet | **RESTE** (non bloquant pour le pack de revue) : sous-formulaire interactif `shell.py` (saisie des ~40 champs cession + bail) ; placeholder `nombre_pages_lettres="vingt"` à remplacer par saisie réelle | ⏳ UI à câbler | — |
| 2026-06-04 | Bloc 2 cession SCM | **Cession de parts SCM complète** : `scm_cession_context` sur `SelarlSliceInput` + `ctx.scm_cession` + `dossier_options.scm_cession` + codes DOC-031/032/033 + scénario `selarl_dentiste_cession_scm` (variante SELARL) + test. Pack = 9 DOCX (PV AGE + courrier SDE + acte parts SCM), 308 tests verts | ✅ | (voir commit) |
| 2026-06-04 | Bloc 3 bail / appel de fonds | **Couvert par Bloc 1** : avenant bail DOC-007 (médical + dentaire) et appel de fonds DOC-008 (dentaire) déjà câblés et générés | ✅ | dc702d2 |
| 2026-06-04 | Bloc 2 cession SCM | **RESTE** (non bloquant pour le pack) : sous-formulaire interactif `shell.py` ; composition dossier (SCM seul vs bundlé avec création) à arbitrer dans l'UI | ⏳ UI à câbler | — |
| 2026-06-04 | Bloqué Albane | Spec + **questions précises** pour les statuts multi-associés complets (comparution/signatures pluriels, co-gérance, quorum/majorité, président externe, associé absent) rédigées | ✅ (spec) | docs/delivery/selarl_multi_associes_questions_albane_v1.md |
| 2026-06-04 | Bloc 1 cession cabinet | **Compromis** ajoutés : `DOC-010` (médical, sans crédit-vendeur ni SCM) + `DOC-012` (dentaire), même moteur, étape compromis. Scénarios + test, 309 verts. **Lot cession complet : DOC-007 → DOC-012.** | ✅ | (voir commit) |
