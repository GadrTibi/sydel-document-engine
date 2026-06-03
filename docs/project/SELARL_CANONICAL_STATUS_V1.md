# SELARL canonical status V1

Ticket source : `SELARL-CANONICAL-STATUS-001`

Derniere mise a jour : 2026-06-02

## Role de ce document

Ce fichier est le point d'entree unique pour savoir ou en est la SELARL.

Il ne remplace pas la source de verite juridique. La source metier reste
`project/source_truth/Documents_a_generer_par_cas.docx` et les specs restent
dans `docs/delivery/`.

Pour l'etat projet, ce fichier prime sur les anciens rapports qui indiquent que
`DOC-006` serait encore en reserve. Cette reserve a ete levee le 2026-06-01.

La fin de sprint operationnelle est detaillee dans :

- `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`

## Decision produit actuelle

Decision : `GO validation finale associe` sur le pack 005 amende le 2026-06-03.

Decision : `NO-GO dev` pour une nouvelle extension SELARL complexe tant que le
prochain sous-cas n'est pas choisi et cadre sous gate produit.

La SELARL actuelle est un candidat technique avance pour les cas simples et le
regime communautaire. Les retours humains 006 sont corriges cote code/test,
integres dans le pack 005 et audites cote Codex. L'audit incident du
2026-06-03 a trouve puis corrige `DOC-002` (`pour une duree indeterminee` ->
`pour 99 ans`). Elle n'est pas declaree juridiquement finale sur ce perimetre
tant que l'associe n'a pas valide le pack 005 amende ou donne des ecarts
residuels corriges/classes.

## Dernier checkpoint

- `SELARL-DOC006-REGIME-FIX-001` : DONE.
- `SELARL-CLOSING-PACK-002` : DONE.
- `SELARL-HUMAN-RETURNS-DEEP-AUDIT-002` : DONE.
- `SELARL-CLOSING-PACK-003` : DONE.
- `SELARL-THREE-SOURCE-AUDIT-004` : DONE.
- `SELARL-CLOSING-PACK-004` : DONE.
- `SELARL-CLOSING-SMOKE-001` : DONE.
- `SELARL-HUMAN-RETURNS-006-TRIAGE-001` : DONE.
- `SELARL-RETURNS-006-STATUTS-001` : DONE.
- `SELARL-RETURNS-006-DNC-001` : DONE.
- `SELARL-RETURNS-006-PV-001` : DONE.
- `SELARL-RETURNS-006-PROCURATION-001` : DONE.
- `SELARL-RETURNS-006-CONJOINT-LETTERS-001` : DONE.
- `SELARL-RETURNS-006-ORDRE-001` : DONE.
- `SELARL-RETURNS-006-FRONT-VARIABLES-001` : DONE.
- `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001` : DONE.
- `SELARL-CLOSING-PACK-005` : DONE.
- `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006` : DONE.
- `SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001` : DONE.
- `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` : DONE.
- Pack actif : `artifacts/selarl_closing_pack_005/`.
- Rapport pack : `docs/review/selarl_closing_pack_005_report_v1.md`.
- Rapport audit trois sources : `docs/review/selarl_three_source_alignment_004_report_v1.md`.
- Rapport audit retours humains : `docs/review/selarl_human_returns_deep_audit_002_report_v1.md`.
- Rapport audit incident retours 006 :
  `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`.
- Rapport source/fidelite : `docs/review/selarl_source_fidelity_audit_001_report_v1.md`.
- Brief final associe : `docs/review/selarl_final_validation_001_brief_v1.md`.
- Retour humain brut 006 : `docs/review/selarl_human_returns_006_raw_v1.md`.
- Triage retour humain 006 : `docs/review/selarl_human_returns_triage_006_report_v1.md`.
- Rapport correction statuts 006 :
  `docs/review/selarl_returns_006_statuts_001_report_v1.md`.
- Rapport correction DNC 006 :
  `docs/review/selarl_returns_006_dnc_001_report_v1.md`.
- Rapport correction PV 006 :
  `docs/review/selarl_returns_006_pv_001_report_v1.md`.
- Rapport correction procuration 006 :
  `docs/review/selarl_returns_006_procuration_001_report_v1.md`.
- Rapport correction lettres regime communautaire 006 :
  `docs/review/selarl_returns_006_conjoint_letters_001_report_v1.md`.
- Rapport correction ordre 006 :
  `docs/review/selarl_returns_006_ordre_001_report_v1.md`.
- Rapport correction variables front 006 :
  `docs/review/selarl_returns_006_front_variables_001_report_v1.md`.
- Rapport correction adresses/signatures 006 :
  `docs/review/selarl_returns_006_address_signature_001_report_v1.md`.
- Rapport audit pack 005 / retours 006 :
  `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`.
- Rapport actif apres incident generalise :
  `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`.

Controles techniques :

- Tests cibles retours humains/documents : dernier controle cible 25 passes
  sur statuts/regime apres corrections pack 005.
- Regression SELARL large : 166 passes.
- Regression SELARL ciblee apres amendement 2026-06-03 : 187 passes.
- Ruff cible tickets 006 finaux : OK.
- `pytest -q` complet : 416 passes.
- Manifest pack 005 : 4 scenarios, 0 echec.

## Synthese executive

Ce qui est vraiment disponible :

- SELARL unipersonnelle medecin : pack DOCX/ZIP genere depuis le clean front.
- SELARL unipersonnelle chirurgien-dentiste : pack DOCX/ZIP genere depuis le
  clean front.
- Regime communautaire : `DOC-005` et `DOC-006` sont generes ensemble quand
  l'option est active.
- Multi-associes : uniquement deux sous-cas limites existent :
  `DOC-004` seul, ou dentiste `DOC-004` + `DOC-016` en PARTIAL.

Ce qui n'est pas encore disponible en production complete :

- statuts multi-associes complets ;
- medecin multi-associes ;
- plusieurs gerants ;
- president de seance externe ;
- cession cabinet medicale ou dentaire dans le front Track B ;
- cession SCM dans le front Track B ;
- derogations et site distinct en generation automatique ;
- validation juridique finale globale.

## Pourcentage courant

| Perimetre | Avancement | Lecture |
| --- | ---: | --- |
| SELARL simple + regime communautaire, technique | 99 % | Pack 005 regenere, adresse conjoint front/schema verrouillee, `DOC-002` corrige en `pour 99 ans`, regression 187 tests OK. |
| SELARL simple + regime communautaire, produit | 96 % | Retours humains 006 traites et incidents recents corriges ; validation finale associe requise avant 100 %. |
| SELARL globale tous cas confondus | 75 % | Le coeur est fort, mais les variantes complexes restent hors cloture. |

## Matrice des documents SELARL

| Code | Document | Etat actuel SELARL | Decision |
| --- | --- | --- | --- |
| `DOC-001` | Declaration de non-condamnation | LOCKED sur corrections humaines | Generable dans les packs simples |
| `DOC-002` | Autorisation de domiciliation | LOCKED sur domiciliation siege/cabinet | Generable dans les packs simples |
| `DOC-003` | Procuration | LOCKED sur suppression parasites, clause finale et retour 006 procuration | Generable dans les packs simples |
| `DOC-004` | PV nomination gerant | LOCKED en unipersonnel et multi-associes simple limite | Generable selon sous-cas couvert |
| `DOC-005` | Renonciation conjoint commun en biens | LOCKED sur corrections humaines | Generable si regime communautaire actif |
| `DOC-006` | Avertissement conjoint | Source DOCX et generateur disponibles | Generable si regime communautaire actif |
| `DOC-007` | Avenant bail | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-008` | Appel de fonds | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-009` | Acte cession cabinet medical | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-010` | Compromis cession cabinet medical | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-011` | Acte cession cabinet dentaire | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-012` | Compromis cession cabinet dentaire | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-013` | Formulaire multi-sites SEL | Moteur existant mais manuel dans le flux SELARL verifie | Hors generation SELARL automatique |
| `DOC-014` | Demande derogation cumul SELARL BNC | Moteur existant mais manuel dans le flux SELARL verifie | Hors generation SELARL automatique |
| `DOC-016` | Statuts SELARL chirurgien-dentiste | LOCKED articles 1 a 34 en unipersonnel ; PARTIAL en dentiste multi simple | Generable selon scope, PARTIAL en multi |
| `DOC-017` | Statuts SELARL medecin | LOCKED source-level en unipersonnel | Generable medecin simple, pas multi |
| `DOC-031` | PV AGE cession parts SCM | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-032` | Courrier SDE cession SCM | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-033` | Acte cession parts SCM vers SELARL | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-034` | Demande inscription a l'ordre | Corrige selon retour 006 : conseil compose depuis profession + departement | Generable, verifie dans pack 005 |
| sans code | Site distinct CD94 | Manuel | Afficher comme manuel |
| sans code | Derogation SEL BNC | Manuel | Afficher comme manuel |

## Scenarios couverts

### SELARL medecin unipersonnelle simple

Documents generes :

- `DOC-001`
- `DOC-002`
- `DOC-003`
- `DOC-004`
- `DOC-034`
- `DOC-017`

Statut : candidat technique avance.

### SELARL chirurgien-dentiste unipersonnelle simple

Documents generes :

- `DOC-001`
- `DOC-002`
- `DOC-003`
- `DOC-004`
- `DOC-034`
- `DOC-016`

Statut : candidat technique avance.

### SELARL medecin avec regime communautaire

Documents generes :

- `DOC-001`
- `DOC-002`
- `DOC-003`
- `DOC-004`
- `DOC-034`
- `DOC-005`
- `DOC-006`
- `DOC-017`

Statut : candidat technique avance.

### SELARL chirurgien-dentiste avec regime communautaire

Documents generes :

- `DOC-001`
- `DOC-002`
- `DOC-003`
- `DOC-004`
- `DOC-034`
- `DOC-005`
- `DOC-006`
- `DOC-016`

Statut : candidat technique avance.

### Multi-associes simple limite

Statut : couvert mais limite.

- `DOC-004` seul est couvert pour le mode multi-associes simple limite.
- `DOC-004` + `DOC-016` dentiste est couvert en PARTIAL pour un sous-cas simple.

## Scenarios non couverts

Ces scenarios ne doivent pas etre codes sans nouveau gate produit et nouvelle
spec de sous-cas :

- medecin multi-associes ;
- statuts multi-associes complets `DOC-016` / `DOC-017` ;
- plusieurs gerants ;
- president de seance externe aux associes ;
- associe absent non represente, quorum partiel, vote non unanime ;
- cession cabinet medicale ou dentaire ;
- bail / appel de fonds lie au parcours SELARL ;
- cession SCM ;
- derogations ;
- site distinct.

## Sources de reprise

A lire pour comprendre la SELARL courante :

1. `docs/project/SELARL_CANONICAL_STATUS_V1.md`
2. `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`
3. `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`
4. `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
5. `docs/project/SELARL_PRODUCTION_FACTORY_V1.md`
6. `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`
7. `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`
8. `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`

Rapports de preuve principaux :

- `docs/review/selarl_source_fidelity_audit_001_report_v1.md`
- `docs/review/selarl_three_source_alignment_004_report_v1.md`
- `docs/review/selarl_closing_pack_005_report_v1.md`
- `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`
- `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`
- `docs/review/selarl_closing_pack_004_report_v1.md`
- `docs/review/selarl_human_returns_deep_audit_002_report_v1.md`
- `docs/review/selarl_closing_pack_003_report_v1.md`
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`
- `docs/review/track_b_selarl_medecin_line_by_line_lock_004_report_v1.md`
- `docs/review/track_b_selarl_medecin_regime_communautaire_005_report_v1.md`
- `docs/review/track_b_selarl_multi_associes_doc004_limited_007_report_v1.md`
- `docs/review/track_b_selarl_dentist_multi_associes_statuts_partial_008_report_v1.md`

## Prochaine action recommandee

Poursuivre `SELARL-FINAL-ASSOCIE-VALIDATION-001` :

- ne plus transmettre le pack 003 ni le pack 004 ;
- transmettre `artifacts/selarl_closing_pack_005/` regenere localement apres
  amendement `DOC-002` ;
- transmettre `docs/review/selarl_final_validation_001_brief_v1.md` ;
- demander uniquement une validation finale ou des ecarts concrets document par
  document.

Apres validation associe ou correction d'ecarts residuels, lancer
`SELARL-CANONICAL-CLOSE-001`.
