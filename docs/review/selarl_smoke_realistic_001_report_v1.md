# Rapport SELARL-SMOKE-REALISTIC-001

## Objet

Exécuter un smoke test réaliste du pilote SELARL après réalignement wording, flow, règles de réutilisation et UI, sans push ni redéploiement.

Le smoke vérifie que le parcours SELARL réel :

- affiche l'ordre métier cible : Qualification, Fiche Client, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération ;
- garde `Dossier unipersonnel` comme règle pivot ;
- affiche les documents attendus mais ne génère que les documents prêts ;
- exclut les documents manuels de la génération ;
- ne réintroduit pas `professionnel principal` ni le terme de transcription erroné
  issu de NotebookLM dans les sorties contrôlées.

## Sources lues

- `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`
- `docs/project/SELARL_REBUILD_BACKLOG_V2.md`
- `docs/review/selarl_wording_realign_001_report_v1.md`
- `docs/review/selarl_flow_realign_001_report_v1.md`
- `docs/review/selarl_reuse_rules_realign_001_report_v1.md`
- `docs/review/selarl_ui_realign_001_report_v1.md`
- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- `src/sydel_doc_engine/app/selarl_form_schema.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/streamlit_app.py`

## État Git initial

- Branche : `main`.
- État : `main...origin/main [ahead 7]`.
- Non suivi avant ticket : `docs/docssource_truth/`.
- Dernier commit avant smoke : `8da6ad8 fix: realign selarl ui to business flow`.

Le dossier `artifacts/` est ignoré par Git ; les sorties de smoke y restent hors versionnement.

## Harnais de smoke

Le smoke a été lancé via le modèle actuel du business wizard :

- construction de `BusinessWizardInput` réalistes ;
- évaluation par `evaluate_business_wizard(...)` ;
- lecture des projections `selarl_ui_reuse_projection(...)` ;
- génération via `generate_docx_files_for_document_codes(...)` avec les seuls `validation.generatable_document_codes` ;
- ZIP via `generate_zip_file(...)` ;
- PDF tenté seulement si `is_pdf_export_available()` le permet.

Résultat environnement PDF :

```text
pdf_available: False
```

Le PDF local est donc indisponible sur ce poste pour ce ticket. Le smoke DOCX/ZIP reste valide.

Artefacts générés :

```text
C:\Users\Gad\Desktop\Sydel\sydel-document-engine\artifacts\selarl_smoke_realistic_001\20260519_185045\
```

Résumé brut :

```text
C:\Users\Gad\Desktop\Sydel\sydel-document-engine\artifacts\selarl_smoke_realistic_001\20260519_185045\smoke_summary.json
```

Écrans visibles confirmés par projection :

1. Écran 1 — Qualification
2. Écran 2 — Fiche Client
3. Écran 3 — Fiche Société
4. Écran 4 — Capital & Associés
5. Écran 5 — Contexte & scénarios métier
6. Écran 6 — Documents & génération

## Scénario A — SELARL médecin unipersonnelle simple

Description : médecin créant une SELARL simple, sans site distinct, sans SCM, sans régime communautaire, sans dérogation et sans cession.

Paramètres :

- `profession = medecin`
- `dossier_unipersonnel = oui`
- `site_distinct = non`
- `scm_cession = non`
- `regime_communautaire = non`
- `derogation = non`
- `cession = non`

Règles de réutilisation activées :

- active : `dossier_unipersonnel`
- effet confirmé : Praticien = associé unique = gérant = signataire
- cibles verrouillables : `associes.associe_unique`, `dirigeant_nomine`, `mandataire_signataire.signataire`
- `mandataire_is_signataire = false`

Documents attendus :

| Code | Document | Statut smoke |
|---|---|---|
| `DOC-001` | Déclaration sur l'honneur de non-condamnation | Généré |
| `DOC-002` | Autorisation de domiciliation | Généré |
| `DOC-003` | Procuration | Généré |
| `DOC-004` | PV nomination gérant | Généré |
| `DOC-034` | Demande d'inscription à l'ordre | Contexte incomplet V2 |
| `DOC-017` | Statuts SELARL médecin | Contexte incomplet V2 |

Documents générés :

```text
...\scenario_a_medecin_unipersonnelle_simple\declaration_non_condamnation.docx
...\scenario_a_medecin_unipersonnelle_simple\autorisation_domiciliation.docx
...\scenario_a_medecin_unipersonnelle_simple\procuration.docx
...\scenario_a_medecin_unipersonnelle_simple\pv_nomination_gerant.docx
...\scenario_a_medecin_unipersonnelle_simple\dossier_generation.zip
```

ZIP :

```text
autorisation_domiciliation.docx
declaration_non_condamnation.docx
manifest.json
procuration.docx
pv_nomination_gerant.docx
```

Champs manquants / documents bloqués :

- `DOC-034` : attendu, mais contexte incomplet pour génération dans cette V2.
- `DOC-017` : attendu, mais contexte incomplet pour génération dans cette V2 ; note catalogue sur le libellé source médecin/dentiste conservée.

Bugs trouvés : aucun.

## Scénario B — SELARL chirurgien-dentiste avec régime communautaire et site distinct

Description : chirurgien-dentiste avec régime communautaire, site distinct et dérogation. Le scénario est volontairement non unipersonnel pour vérifier que le système n'impose pas Praticien = associé unique quand l'option n'est pas active.

Paramètres :

- `profession = chirurgien_dentiste`
- `dossier_unipersonnel = non`
- `site_distinct = oui`
- `scm_cession = non`
- `regime_communautaire = oui`
- `derogation = oui`
- `cession = non`

Justification métier :

- Le site distinct rend la dérogation cohérente dans le parcours.
- Le dossier non unipersonnel couvre le cas où le Praticien reste associé 1, gérant et signataire par options explicites, sans être associé unique.

Règles de réutilisation activées :

- active : `signataire_is_associe_1`
- active : `gerant_is_professional`
- active : `signataire_is_professional`
- non active : `dossier_unipersonnel`
- effet confirmé : `praticien_is_associe_unique = false`
- `mandataire_is_signataire = false`

Documents attendus :

| Code | Document | Statut smoke |
|---|---|---|
| `DOC-001` | Déclaration sur l'honneur de non-condamnation | Généré |
| `DOC-002` | Autorisation de domiciliation | Généré |
| `DOC-003` | Procuration | Généré |
| `DOC-004` | PV nomination gérant | Généré |
| `DOC-034` | Demande d'inscription à l'ordre | Contexte incomplet V2 |
| `DOC-016` | Statuts SELARL chirurgien-dentiste | Contexte incomplet V2 |
| sans code | Formulaire site distinct CD94 avec la SEL | Manuel, exclu |
| `DOC-005` | Lettre de renonciation à revendiquer la qualité d'associé | Contexte incomplet V2 |
| `DOC-006` | Lettre d'avertissement au conjoint | Contexte incomplet V2 avec réserve |
| `DOC-013` | Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL | Manuel, exclu |
| sans code | Dérogation SEL BNC | Manuel, exclu |
| `DOC-014` | Demande de dérogation cumul SELARL BNC | Manuel, exclu |

Réserves :

- `DOC-006` affiche la réserve attendue : la vraie V2 indique que ce document ne figure pas parmi les sources fournies ; génération moteur existante à afficher avec réserve dans le pilote SELARL.
- `DOC-013` et `DOC-014` sont visibles mais `À remplir manuellement`.

Documents générés :

```text
...\scenario_b_dentiste_communaute_site_distinct\declaration_non_condamnation.docx
...\scenario_b_dentiste_communaute_site_distinct\autorisation_domiciliation.docx
...\scenario_b_dentiste_communaute_site_distinct\procuration.docx
...\scenario_b_dentiste_communaute_site_distinct\pv_nomination_gerant.docx
...\scenario_b_dentiste_communaute_site_distinct\dossier_generation.zip
```

ZIP :

```text
autorisation_domiciliation.docx
declaration_non_condamnation.docx
manifest.json
procuration.docx
pv_nomination_gerant.docx
```

Contrôles obligatoires :

- aucun document manuel n'est présent dans le ZIP ;
- `DOC-013` n'est pas généré ;
- `DOC-014` n'est pas généré ;
- le mandataire n'est pas assimilé au signataire.

Bugs trouvés : aucun.

## Scénario C — SELARL médecin avec cession cabinet médical, bail et financement

Description : médecin en BNC transférant son cabinet médical vers une SELARL unipersonnelle ; cession, bail et financement actifs.

Paramètres :

- `profession = medecin`
- `dossier_unipersonnel = oui`
- `site_distinct = non`
- `scm_cession = non`
- `regime_communautaire = non`
- `derogation = non`
- `cession = oui`
- `cabinet_type = medical`
- `emprunt_actif = oui`

Règles de réutilisation activées :

- active : `dossier_unipersonnel`
- active : `selarl_is_acquirer`
- effet confirmé : Praticien = associé unique = gérant = signataire
- effet confirmé : SELARL en création = acquéreur explicite
- `mandataire_is_signataire = false`

Documents attendus :

| Code | Document | Statut smoke |
|---|---|---|
| `DOC-001` | Déclaration sur l'honneur de non-condamnation | Généré |
| `DOC-002` | Autorisation de domiciliation | Généré |
| `DOC-003` | Procuration | Généré |
| `DOC-004` | PV nomination gérant | Généré |
| `DOC-034` | Demande d'inscription à l'ordre | Contexte incomplet V2 |
| `DOC-017` | Statuts SELARL médecin | Contexte incomplet V2 |
| `DOC-007` | Avenant contrat de bail | Contexte incomplet V2 |
| `DOC-008` | Appel de fonds SEL | Contexte incomplet V2 |
| `DOC-009` | Acte de cession d'un cabinet médical | Contexte incomplet V2 |
| `DOC-010` | Compromis de cession d'un cabinet médical | Contexte incomplet V2 |

Documents générés :

```text
...\scenario_c_medecin_cession_bail_financement\declaration_non_condamnation.docx
...\scenario_c_medecin_cession_bail_financement\autorisation_domiciliation.docx
...\scenario_c_medecin_cession_bail_financement\procuration.docx
...\scenario_c_medecin_cession_bail_financement\pv_nomination_gerant.docx
...\scenario_c_medecin_cession_bail_financement\dossier_generation.zip
```

ZIP :

```text
autorisation_domiciliation.docx
declaration_non_condamnation.docx
manifest.json
procuration.docx
pv_nomination_gerant.docx
```

Contrôle financement :

- le financement est porté dans `DOC-004` ;
- le PV d'autorisation d'emprunt n'apparaît pas comme document autonome ;
- extrait contrôlé : le `PV nomination gérant` contient le marqueur `150 000`.

Champs manquants / documents bloqués :

- `DOC-007`, `DOC-008`, `DOC-009` et `DOC-010` sont attendus par le catalogue, mais correctement marqués contexte incomplet V2 au lieu d'être présentés comme réussis.

Bugs trouvés : aucun.

## Contrôles transverses

| Contrôle | Résultat |
|---|---|
| `Fiche Client` apparaît comme étape visible | OK |
| `Écran 2 — Fiche Client` avant `Écran 3 — Fiche Société` | OK |
| `professionnel principal` absent des DOCX générés | OK |
| Terme de transcription erroné issu de NotebookLM absent des DOCX générés | OK |
| Aucun placeholder `[` / `]` dans les DOCX générés | OK |
| `Dossier unipersonnel` verrouille associé unique / gérant / signataire si actif | OK |
| Si `Dossier unipersonnel` inactif, pas de dérivation associé unique imposée | OK |
| Mandataire non assimilé au signataire par défaut | OK |
| `DOC-006` visible avec réserve | OK, scénario B |
| `DOC-013` / `DOC-014` visibles si dérogation active | OK, scénario B |
| `DOC-013` / `DOC-014` exclus de génération | OK |
| Aucun document manuel dans les ZIP | OK |
| PV d'autorisation d'emprunt non autonome | OK |
| SCI et mode Technique / diagnostic | Non modifiés dans ce ticket |

## Corrections faites

Aucune correction applicative n'a été faite.

Aucun fichier Python, générateur, moteur DOCX/PDF/ZIP, catalogue ou UI n'a été modifié.

## Validations finales

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 257 tests passés.

## Limites et risques

- Le pilote est prêt à tester le parcours et la sélection documentaire, mais pas à promettre une génération complète de tous les documents SELARL.
- Les statuts SELARL, la demande d'inscription à l'ordre, le régime communautaire, le bail, l'appel de fonds et les actes de cession restent visibles comme attendus mais marqués `Contexte incomplet pour génération V2`.
- Le backend PDF local est indisponible pendant ce smoke ; les sorties validées sont DOCX et ZIP.
- Le verdict ne remplace pas une revue juridique/visuelle des documents générés.

## Verdict global

Verdict : prêt pour revue associé / juriste du pilote Streamlit SELARL, avec réserves explicites.

Le pilote SELARL est prêt pour un test associé sur Streamlit Cloud uniquement après décision de push/redéploiement : le smoke local confirme que le parcours réaligné ne génère que les documents prêts, exclut les documents manuels, affiche les réserves et ne présente pas les documents incomplets comme réussis.

Prochaine étape recommandée : `SELARL-JURIST-REVIEW-001`.
