# SCM — Statut & plan de fondation (V1)

> **Posture : ZÉRO CONFIANCE dans l'auto-rapport.** Tout ce qui suit sur l'existant a été **vérifié
> dans le code source** (registre, catalogue de cas, générateurs, scénarios, UI), pas lu dans un
> rapport d'agent. Réf. méthode : `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`.
> **Aucun fichier `src/` n'a été modifié par cette fondation** (tâche sources + docs uniquement).

---

## 1. Ce que Codex a DÉJÀ fait pour SCM dans `src/` (vérifié, à re-tester)

### 1.a — SCM autonome (type d'entreprise « créer une SCM »)
| Élément | Emplacement | État vérifié |
|---|---|---|
| `CaseType.SCM` | `domain/case_catalog.py:16` | Existe. |
| Carte de cas SCM (10 occurrences) | `domain/case_catalog.py:701-713` | Existe, **MAIS extrapolée par Codex — non adossée au canon** (cf. ci-dessous). |
| Générateur statuts | `generators/lot_04/statuts_scm.py` → DOC-025 `generate_statuts_scm` | `general_condition = "dossier.structure == SCM"` ; `workflow_status = TESTE`. |
| Pacte d'associés | `generators/lot_05/pacte_associes_scm.py` → DOC-026 | `dossier.structure == SCM et options.scm_satellites == true` ; `TESTE`. |
| Contrat frais communs | `generators/lot_05/contrat_frais_communs.py` → DOC-027 | idem (satellites) ; `TESTE`. |
| Règlement intérieur | `generators/lot_05/reglement_interieur_scm.py` → DOC-028 | idem (satellites) ; `TESTE`. |
| Liste dépenses communes | `generators/lot_05/liste_depenses_communes_scm.py` → DOC-030 | idem (satellites) ; `TESTE`. |
| Modules communs satellites | `generators/lot_05/scm_satellites_common.py`, `scm_satellites_templates.py` | Existent. |

### 1.b — SCM comme SATELLITE/CESSION d'une SELARL (déjà cartographié au canon)
| Élément | Emplacement | État vérifié |
|---|---|---|
| PV AGE cession parts SCM | `generators/lot_05/pv_age_cession_scm.py` → DOC-031 | `structures = SELARL/SELAS`, `options.scm_cession == true` ; `TESTE`. |
| Courrier SDE cession SCM | `generators/lot_05/courrier_sde_cession_scm.py` → DOC-032 | idem ; `TESTE`. |
| Acte cession parts SCM → SEL | `generators/lot_05/acte_cession_parts_scm.py` → DOC-033 | idem ; `TESTE`. |
| Module commun cession | `generators/lot_05/scm_cession_common.py` | Existe. |
| Fixtures de scénario | `scenarios/selarl.py` (`_scm_cession_selarl`, `scm_cession_fixture`) | **Uniquement la cession SCM côté SELARL.** |
| UI (front) | `front_app/shell.py:394` checkbox « SCM » dans le flux **SELARL** | C'est le **bloc cession SCM dans le dossier SELARL**, pas un type SCM autonome. |

### 1.c — Specs de delivery Codex (contexte, à relire)
`docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`, `lot_05_scm_satellites_*`,
`lot_05_scm_cession_*`, `lot_05_scm_liste_depenses_preparation_v1.md`.

> **Sens de `TESTE` (vérifié `domain/enums.py:18-26`)** : `INVENTORIE → VALIDE → SOURCE_RECUE →
> ANALYSE → SPECIFIE → CODE → TESTE → VALIDE_FINAL`. **`TESTE` ≠ validé juridiquement.** Le wording
> reste **NON validé humainement** tant qu'on n'est pas `VALIDE_FINAL` (gate Rafael/Albane).

---

## 2. Ce qui MANQUE (les vrais trous)

| Trou | Gravité | Détail |
|---|---|---|
| **Carte officielle cas → documents SCM** | **BLOQUANT** | Le canon `Documents_a_generer_par_cas_V3.docx` est 100 % SELARL ; SCM n'y est que « cession de parts vers SELARL ». **Aucune carte « créer une SCM ».** → Bloc 1 NotebookLM/Rafael. |
| **Carte de cas Codex non sourcée** | Élevée | `case_catalog.py:701-713` liste `demande_inscription_ordre` pour la SCM **alors que ce modèle est ABSENT du dossier Drive SCM** → invention probable à challenger. |
| **Liste/optionnalité des cas** | Élevée | Inconnu : quels documents sont systématiques vs optionnels, combien d'associés (modèles = 2, variables Drive → 3). |
| **Type SCM non atteignable en UI** | Moyenne | Aucun dossier « SCM » autonome dans le front ; seul le bloc cession SCM (dans SELARL) est exposé. Phase 6 entièrement à faire pour une SCM autonome. |
| **Scénario/fixture SCM autonome** | Moyenne | `scenarios/` ne contient qu'une fixture de **cession**. Aucune fixture « création SCM » → DOC-025/026/027/028/030 ne sont pas exerçables via un parcours UI SCM. |
| **`.doc` legacy** | Faible | `Liste depenses communes SCM.doc` non tokenisable ; un `.docx` existe côté `lot_05` → arbitrer la référence (Bloc 4.2). |
| **Modèles « communs »** | Faible | `Autorisation domiciliation`, `Declaration non condamnation`, `Procuration` = trames partagées (déjà en `lot_01`/`lot_02`) → réutiliser la couche partagée, ne pas dupliquer. |

---

## 3. PLAN DE FONDATION ordonné (suivant `WORKFLOW_TYPE_ENTREPRISE_V1.md`)

> **Génération NO-GO** tant que les cas ne sont pas confirmés et le wording non validé (gate Phase 8).
> La fondation technique + l'UI peuvent avancer indépendamment **une fois la carte des cas connue**.

**Phase 0 — Cadrage & branche** *(quand le build SCM démarrera)*
- Branche dédiée `scm/<ticket>` ; vérifier `git branch --show-current` avant tout edit. *(Pas de Git
  dans cette tâche de fondation.)*

**Phase 1 — Sources** *(FAIT par cette fondation)*
- [x] 11 modèles copiés (NFC, dédupliqués) dans `project/source_documents/scm/` + `variables_source_scm.csv`.
- [x] Tokens extraits (scan XML) → `INVENTAIRE_MODELES.md`.
- [ ] **Convertir `Liste depenses communes SCM.doc` en `.docx`** (ou retenir la version `lot_05`).

**Phase 2 — Cartographie des cas** *(BLOQUÉ — dépend du Bloc 1 NotebookLM/Rafael)*
- [ ] Obtenir la **carte officielle cas → documents SCM** (Bloc 1 des prompts).
- [ ] Ratifier / corriger la `CARTOGRAPHIE_TENTATIVE.md` ; **réconcilier avec `case_catalog.py:701-713`**
      (supprimer `demande_inscription_ordre` si non confirmé ; ajouter conditions systématique/optionnel ;
      fixer le nombre d'associés).

**Phase 3 — Moteur** *(partiellement amorcé par Codex — à re-vérifier, pas à croire)*
- [ ] Re-tester les générateurs SCM existants (DOC-025/026/027/028/030) en **génération réelle**,
      0 token résiduel, masculin **et** féminin.
- [ ] Compléter les générateurs manquants une fois les cas confirmés ; ranger par lot.
- [ ] Modèles de données `domain/models.py` : un `…Context` SCM **création** (n'existe que pour la cession).

**Phase 4 — Règles juridiques** *(escalade ; cf. `NOTEBOOKLM_PROMPTS.md`)*
- [ ] Trancher durée SCM, domiciliation indéterminée, articulation contrat frais communs / règlement /
      liste, parties au contrat (SEL vs personnes), coquilles inter-profession.

**Phase 5 — Couches transverses**
- [ ] Genre par personne (gérant/associé) ; pluriel (Bloc 3) — **après validation Albane** pour le pluriel.

**Phase 6 — Interface Streamlit** *(à bâtir pour une SCM autonome ; aujourd'hui inexistante)*
- [ ] Sélecteur « dossier SCM » + sous-formulaires par cas + bouton « données de test » bâti sur une
      **fixture scénario SCM** (à créer en Phase 3). Garde-fou : cas coché sans données = bloqué.

**Phase 7 — Vérification** *(jamais l'auto-rapport)*
- [ ] `ruff` clean + **suite complète verte** (`--basetemp` hors repo) ; DOCX ouverts, 0 crochet `[` ;
      création SELARL **intacte** (ne pas régresser la couche partagée).

**Phase 8 — Gate juridique**
- [ ] Génération NO-GO tant que Rafael/Albane n'a pas validé le wording des documents SCM ; produire le
      Pack de passation (points épuisés côté NotebookLM).

**Phase 9 — Journal & clôture**
- [ ] Décisions SCM ratifiées au journal (codes `SCM-…`) ; leçons reversées dans le workflow ; merge
      `main` + déploiement = geste PM.

---

## 4. Décisions techniques prises dans cette fondation (annonce, pas arbitrage)

- **Dossier source** `project/source_documents/scm/` créé (et non un `lot_*`) car la cartographie par
  cas n'est pas encore connue : ranger par lot serait préjuger de l'assemblage. Le rangement par lot se
  fera en Phase 3, une fois les cas confirmés.
- **Noms de fichiers normalisés** (NFC, sans suffixe « - transforme », `SCM` explicite) pour éviter le
  piège doublon NFC/NFD déjà rencontré sur d'autres types.
- **`variables_source_scm.csv`** copié comme **référence** (dictionnaire transverse fourni par le Drive),
  pas comme contrat de variables d'un cas.

## 5. Point de gouvernance (1 ligne)

La SCM est une **feature à bâtir** (type autonome non livré), pas un simple correctif : le code Codex
existant est une **amorce non canon-validée**. Le vrai bloquant est **métier** (carte des cas
manquante) → relayer le **Bloc 1** à NotebookLM/Rafael **avant** tout nouveau code SCM.
