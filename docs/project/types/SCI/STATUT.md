# Statut de fondation — type SCI (V1, 2026-06-05)

> **Nature de ce document :** photographie de l'existant SCI + plan de fondation. **Préparation
> seulement** : aucun code moteur écrit, aucun Git. Tout ce qui suit sur `src/` est à
> **RE-VÉRIFIER soi-même, zéro confiance dans l'auto-rapport** (workflow Phase 7).

---

## 1. Le bloquant n°1 : pas de canon cas → documents pour la SCI

- Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` est **entièrement SELARL**
  (**vérifié : 23 « SELARL », 0 « SCI »**). **Aucune carte officielle « cas SCI → documents ».**
- On dispose des **modèles** (Drive *Création SCI*, 7 `.docx`), mais **pas de l'assemblage par cas**.
- ➡️ Conséquence : on ne peut pas figer le backlog SCI tant que NotebookLM/Rafael n'a pas livré la
  liste des cas + la carte (voir `NOTEBOOKLM_PROMPTS.md`, BLOC A). **Ne rien inventer.**

## 2. Ce que Codex semble avoir déjà fait pour SCI dans `src/` (À RE-VÉRIFIER)

> Constats de lecture statique, datés 2026-06-05. À reprouver par exécution (génération + tests +
> ouverture des DOCX), jamais sur la foi de ce tableau.

| Zone | Fichier | Constat de lecture | Verdict provisoire |
|---|---|---|---|
| Type de cas | `domain/case_catalog.py` (`CaseType.SCI = "SCI"`) | un `CaseType.SCI` existe | présent |
| Documents catalogués | `domain/case_catalog.py` | `statuts_sci` (DOC-020), `statuts_sci_iris` (DOC-021), `lettre_option_is` (DOC-022) déclarés `GENERATABLE` ; les 3 docs « tous les cas » + PV nomination gérant réutilisent DOC-001/002/003/004 | présent mais **non adossé à un canon SCI** |
| Carte cas→docs (code) | `registry/catalog.py` lignes ~693-700 | une **carte SCI codée** : `statuts_sci` (si non IRIS), `statuts_sci_iris` (si IRIS), `lettre_option_is` (si IS), `declaration_non_condamnation`, `procuration`, `autorisation_domiciliation`, `pv_nomination_gerant` | ⚠️ **carte INVENTÉE par Codex sans canon** — à confronter à BLOC A NotebookLM |
| Générateurs statuts | `generators/lot_04/statuts_sci.py`, `statuts_sci_iris.py`, `statuts_civils_common.py` (740 lignes) | ⚠️ **GÉNÉRATION FROM-SCRATCH** : le document est **reconstruit en Python** (`docx_builder.add_paragraph`), **PAS** rempli depuis le modèle tokenisé (`fill_docx_template` **absent**). Docstring : « Generateur from-scratch des statuts SCI civils V1 ». | ⚠️ **DRIFT DE FIDÉLITÉ** vs Principe 1 du workflow (« remplissage de template, jamais de paraphrase ») — le wording vit **dans le code**, non validé humainement |
| Lettre option IS | `generators/lot_05/lettre_option_is.py` | générateur présent (partagé) | à re-vérifier (template-fill ?) |
| Orchestrateur | `orchestrator/service.py` (l.51-52, 145-146, 197-198) | DOC-020→`StatutsSciGenerator`, DOC-021→`StatutsSciIrisGenerator` câblés | présent |
| Modèles sources | `project/source_documents/lot_04/Modèle statuts SCI[ IRIS].docx` | les 2 statuts SCI étaient déjà rangés en lot_04 | présent |
| Prefill UI | `front_data/test_prefill_presets.py` (`SCI_SIMPLE_PROFILE`) | profil « legacy SCI happy path », commentaire « non-regression » | ⚠️ probable **legacy** non aligné sur la recette UI cible |

**Points de vigilance majeurs à reprouver :**
1. **Fidélité statuts** : les statuts SCI sont **construits en code**, pas remplis depuis le `.docx`
   tokenisé → le wording n'est **pas** celui du modèle source validé. À trancher : revenir au
   **template-fill** (Principe 1) ou faire valider le wording from-scratch par Rafael/Albane.
2. **Carte cas→docs codée sans canon** : la sélection de documents SCI dans `registry/catalog.py` est
   une **hypothèse de Codex**, pas un canon. À confirmer/corriger après BLOC A.
3. **0 token résiduel & genre** : non vérifiés ici ; à prouver par génération réelle masculin **et**
   féminin, 0 crochet `[` résiduel.

## 3. Ce qui manque

- **Canon** : la carte officielle *cas SCI → documents* (LE bloquant — BLOC A NotebookLM).
- **Modèles** : aucun manquant pour le cas *création* connu (les 7 du Drive sont copiés dans
  `project/source_documents/sci/`). **Mais** on ignore si d'autres cas SCI (cession de parts…) exigent
  des modèles non fournis → question ouverte (BLOC A/D).
- **Décisions juridiques** : sens de « IRIS », condition de l'option IS, durée société, objet social,
  borne d'associés, apport en nature (BLOCS B/C/E).
- **Couches** : table de genre SCI, règle de pluriel (non validée Albane), recette UI par cas.
- **Journal de décisions SCI** : inexistant (à créer une fois les cas ratifiés : `JOURNAL_DECISIONS_SCI_V1.md`, codes `SCI-…`).

## 4. Plan de fondation ordonné (suivant `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`)

> Statut actuel : **Phase 0-1 partiellement faites** (modèles réunis, canon lu — et **prouvé absent**
> pour SCI). **Phase 2 BLOQUÉE** faute de canon. On ne descend pas en Phase 3+ avant le déblocage.

| # | Phase workflow | Action SCI | Pré-requis / GO |
|---|---|---|---|
| 0 | Phase 0 — Cadrage & branche | Brancher `sci/<ticket>` avant tout code (geste à venir, pas fait ici) | — |
| 1 | Phase 1 — Sources | ✅ 7 modèles copiés `project/source_documents/sci/` + inventaire ; canon SELARL lu, **SCI absent confirmé** | fait (préparation) |
| 2 | **Phase 2 — Cartographie** | **Envoyer BLOC A NotebookLM** → obtenir liste des cas + carte cas→docs officielle ; remplacer `CARTOGRAPHIE_TENTATIVE.md` par la matrice ratifiée | **BLOQUANT — GO NotebookLM/Rafael** |
| 3 | Phase 3 — Moteur | Décider **template-fill vs from-scratch** pour les statuts (corriger le drift §2.1) ; un générateur par doc, sécurité anti-token-résiduel ; scénarios/fixtures par cas ; modèles de données | dépend de Phase 2 |
| 4 | Phase 4 — Règles juridiques | Trancher BLOCS B/C/E (IRIS, option IS, durée, objet, apport nature, anti-coquille SEL) via NotebookLM puis Rafael | dépend de Phase 2 |
| 5 | Phase 5 — Genre/pluriel | Table de genre SCI (paires exactes, par personne) ; pluriel **après** validation Albane | dépend de Phase 4 |
| 6 | Phase 6 — UI Streamlit | Recette par cas (checkbox → sous-formulaire → génération) + bouton « données de test » ; retirer/aligner le `SCI_SIMPLE_PROFILE` legacy | dépend de Phase 3 |
| 7 | Phase 7 — Vérification | ruff clean + suite **complète** verte (chiffres, `--basetemp` hors repo) ; DOCX ouverts, 0 token résiduel, masculin **et** féminin ; revue de fidélité | continu |
| 8 | Phase 8 — Gate juridique | Génération **NO-GO** tant que wording SCI non validé Rafael/Albane ; pack de passation | GO Rafael |
| 9 | Phase 9 — Journal & clôture | Créer `JOURNAL_DECISIONS_SCI_V1.md` (codes `SCI-…`) ; merge `sci/… → main` + déploiement = **geste PM** | GO PM |

## 5. Livrables de cette préparation
- `project/source_documents/sci/` — 7 modèles SCI (dédupliqués, NFC, 0 doublon NFC/NFD).
- `docs/project/types/SCI/INVENTAIRE_MODELES.md` — modèle → variables → nature.
- `docs/project/types/SCI/CARTOGRAPHIE_TENTATIVE.md` — regroupement probable (bandeau « carte officielle manquante »).
- `docs/project/types/SCI/NOTEBOOKLM_PROMPTS.md` — prompts prêts à envoyer (BLOCS A-E).
- `docs/project/types/SCI/STATUT.md` — ce document.
