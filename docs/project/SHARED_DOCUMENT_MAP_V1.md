# Carte des documents partagés V1 — boussole de parallélisation

Date : 2026-06-03 · Établie par audit multi-agents (lecture seule) + vérification adverse.
But : (1) prouver la propreté de la réutilisation (1 document = 1 fonction, variantes par paramètre) ;
(2) servir de **boussole anti-collision** pour paralléliser plusieurs chantiers (Gad / Naomi /
plusieurs Claude Code) sans casse Git.

## 1. Constat global (vérifié)

- **43 documents `DOC-001..DOC-043` = 43 générateurs réels, tous câblés** par `doc_id` dans
  `orchestrator/service.py:build_generator_registry()`. **Aucun stub, aucun `NotImplementedError`,
  aucun DOC orphelin, aucun générateur non mappé.** Le moteur est réel et complet.
- **Réutilisation = bien architecturée** : un helper `_common.py` porte la logique de rendu, des
  générateurs minces (~30 l.) délèguent, la variante est choisie par un **champ du contexte**
  (`structure`, `overlay`/profession, `etape`, `type_cabinet`, `operation_spfpl.type`, options
  booléennes). **Variantes par paramètre, pas par fonction dupliquée** — pattern dominant et propre.

## 2. Clusters de mutualisation (helper partagé → documents)

| Helper `_common` / `_templates` | Documents | Déclencheur de variante |
|---|---|---|
| `lot_02/regime_communautaire_common` | DOC-005, DOC-006 | `structure` + option `regime_communautaire` |
| `lot_03/bail_appel_common` | DOC-007, DOC-008 | `structure` + `cession.type_cabinet` |
| `lot_03/cession_cabinets_common` | DOC-009, DOC-010, DOC-011, DOC-012 | dataclass `CessionCabinetVariant(etape × type_cabinet)` |
| `lot_03/derogations_common` | DOC-013, DOC-014 | `derogation.type` + `mode_rendu` |
| `lot_04/statuts_sel_exercice_common` (+templates) | DOC-016, DOC-017, DOC-018 | `structure` + `statuts_sel.overlay` (dérivé profession) |
| `lot_04/statuts_spfpl_common` (+templates) | DOC-035, DOC-036 | `structure` + `operation_spfpl.type` |
| `lot_04/statuts_civils_common` | DOC-019, DOC-020, DOC-021 | dataclass `StatutsCivilTemplate` (slices) |
| `lot_05/spfpl_common` | DOC-037, DOC-040, DOC-041, DOC-042, DOC-043, DOC-029 | `structure` + opération |
| `lot_05/pv_agrement_common` | DOC-038, DOC-039 | `associe_unique` |
| `lot_05/sas_satellites_common` | DOC-023, DOC-024 | base SAS + champ satellite |
| `lot_05/scm_satellites_common` (+templates) | DOC-026, DOC-027, DOC-028, DOC-030 | jeu de blocs + `scm_satellites.<field>` |
| `lot_05/scm_cession_common` | DOC-031, DOC-032, DOC-033 | `structure` ↔ `scm_cession.variante_structure` |
| _autonomes (pas de `_common`)_ | DOC-001, DOC-002, DOC-003, DOC-004, DOC-034, DOC-015, DOC-022, DOC-025 | — |

## 3. Matrice document ↔ type d'entreprise (classification)

- **UNIVERSEL** (≈tous les types) : `DOC-001`, `DOC-002`, `DOC-003` (8/8) ; `DOC-004` (7/8, sauf SAS).
- **PARTAGÉ** (plusieurs types) : `DOC-034` (5 : SELARL/SELAS/SPFPL-c/SPFPL-a/SCM) ; `DOC-005`,
  `DOC-006` (4, cond. régime communautaire) ; `DOC-007`, `DOC-009..012`, `DOC-013`, `DOC-031..033`
  (2 : SELARL/SELAS).
- **SPÉCIFIQUE** (un type) : `DOC-008`,`DOC-014`,`DOC-016`,`DOC-017` (SELARL) ; `DOC-018` (SELAS) ;
  `DOC-015`,`DOC-023`,`DOC-024` (SAS) ; `DOC-035`,`DOC-037`,`DOC-038`,`DOC-039`,`DOC-040`,`DOC-029`
  (SPFPL-c) ; `DOC-036`,`DOC-041`,`DOC-042`,`DOC-043` (SPFPL-a) ; `DOC-019`(SCS) ; `DOC-020`,`DOC-021`,
  `DOC-022`(SCI) ; `DOC-025`,`DOC-026`,`DOC-027`,`DOC-028`,`DOC-030`(SCM).

## 4. Liste des ACTIFS PARTAGÉS — règle de sérialisation (la boussole)

**Deux chantiers qui touchent le MÊME fichier ci-dessous doivent SÉRIALISER** (un seul à la fois).
Deux chantiers sur des **clusters disjoints** peuvent rester parallèles **tant qu'ils ne remontent pas
dans les rangs 1–5**.

**Cœur transverse (impact = tous/plusieurs documents → sérialisation quasi systématique) :**
1. `domain/models.py` — `DocumentGenerationContext` + ~110 modèles ; importé par **les 43 générateurs**.
2. `rendering/docx_builder.py` — importé par **~34 fichiers** ; style/signature → tous les DOCX.
3. `registry/catalog.py` — les 43 `DocumentDefinition` + listes de structures.
4. `orchestrator/service.py` — registre + toute la sélection (`_*_enabled`).
5. `domain/enums.py` — `Gender`, etc. (~15 fichiers).

**Helpers `_common`/`_templates` (impact = leur cluster)** : voir §2. Le plus partagé = `spfpl_common`
(10+ documents), puis `cession_cabinets_common` et `scm_satellites_common` (4 chacun).

**Front partagé** : `front_data/models`, `front_data/canonical_mapping`, `domain/case_catalog`,
`front_data/{document_status,dossier_flow,validation,address_model,role_model}`, `utils/addresses`,
`front_app/field_derivations`.

## 5. Dettes trouvées (à traiter pour un projet « méga-propre »)

**Réutilisation — « zéro duplication » est partiellement faux : 3 forks confirmés (dette de divergence,
pas de bug de routage). Critique pour un produit juridique : une correction de wording doit être faite
2 fois → risque de divergence légale.**
1. **Acte cession SPFPL parts (`DOC-040`) vs actions (`DOC-029`)** — même acte de base, corps réécrit
   inline dans chaque fichier, pas de rendeur partagé. **Fossile de copier-coller prouvé** :
   `lot_05/acte_cession_parts_spfpl.py:167` contient « cession **d'action** » dans le document *parts*.
2. **Squelette « acte de cession » fait 3×** (`DOC-040`, `DOC-029`, `DOC-033`) — boilerplate (Ordre,
   frais, signature électronique) répété ; factorisation par cluster mais pas par famille d'acte.
3. **Attestation capital `DOC-024` (SAS) vs `DOC-042` (SPFPL)** — corps paragraphe-pour-paragraphe
   identique, 2 générateurs, déjà en divergence (accents, « € » vs « euros »).
   → Reco (à arbitrer PM) : extraire un helper commun paramétré (comme `cession_cabinets_common`),
   en gardant 2 `doc_id`.

**Cohérence / traçabilité :**
4. **Drift catalogue ↔ exécution** : `case_catalog.py` déclare « toujours » beaucoup de docs, mais
   `service.py` ajoute les vraies conditions → le catalogue **surestime** ce qui sera généré. Drifts de
   nommage : `scm_cession` vs `scm` (SELAS), `cession_actions` (booléen) vs `nature_titres`.
5. **`generator_name` du catalogue = libellé mort** (ne correspond à aucune fonction ; câblage réel par
   `doc_id`) — trompeur, à aligner/documenter.
6. **`DOC-023` `source_path` cassé** — pointe `project/source_import/raw_drive_dump/...` **absent du
   repo**. Sans impact runtime (la source n'est pas ouverte), mais référence pendante côté audit.
7. **`DOC-001/002/003` statut `SPECIFIE`** au catalogue alors qu'ils sont **implémentés et câblés**
   (GENERATABLE) — écart statut déclaré vs réalité, à clarifier produit.

## 6. Règle d'usage (parallélisation)

Avant de lancer 2+ chantiers : consulter cette carte. Chantiers sur **clusters/documents disjoints**
(ex. statuts civils vs cession SCM) = parallèle OK. Dès qu'un chantier doit modifier un **actif des
rangs 1–5** ou un **`_common` partagé** que l'autre utilise → **sérialiser** : isoler le changement
partagé dans un ticket dédié traité **en premier**, puis diffuser (`pull --ff-only`). C'est
`git-branch-steward` qui applique cette règle et arbitre les collisions avec le PM.
