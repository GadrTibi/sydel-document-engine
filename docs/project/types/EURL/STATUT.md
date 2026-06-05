# EURL — Statut de fondation

_Daté du 2026-06-05. Tâche de fondation read-only ; aucun code écrit ; aucun git._

## Verdict en une ligne

**Fondation EURL NON démarrable** : ni modèles tokenisés, ni carte officielle cas→documents.
Le travail utile immédiat est de **faire fournir les deux** (cf. `NOTEBOOKLM_PROMPTS.md`).

## 1. Ce que Codex a déjà fait pour EURL dans `src/` — RE-VÉRIFIÉ, zéro confiance

Vérification directe du code (pas d'auto-rapport) :

| Vérification | Résultat |
|---|---|
| `CaseType` enum (`domain/case_catalog.py`) contient EURL ? | **NON** — uniquement SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI, SCM, SAS. |
| Modèle / générateur / fixture / slice UI EURL dans `src/` ? | **NON** — `find src -iname *eurl*` → 0 résultat. |
| Référence EURL dans `src/` ou `project/` ? | **1 seule**, et c'est une mention de passage dans un fichier **SELARL** (`project/source_truth/notebooklm_selarl_10_prompts_v1.md`, qui cite « EURL/SELARL unipersonnelle » en illustration). **Aucun artefact EURL.** |

**Conclusion :** Codex n'a produit **aucun** livrable EURL. Rien à reprendre, rien à corriger. EURL
est un type **vierge**.

## 2. Ce qui manque

| Intrant requis (Phase 1-2 du workflow) | État | Bloquant ? |
|---|---|---|
| **Modèles `.docx` tokenisés EURL** | **0** sur le Drive (scan nom + contenu de 125 docx) | OUI — bloque le moteur. |
| **Canon cas→documents EURL** | **Absent** (le canon V3 est SELARL : SELARL ×23, EURL ×0) | OUI — bloque la cartographie. |
| **Locks de retours humains EURL** | Aucun | OUI pour la gate juridique. |
| **Périmètre EURL confirmé** (Sydel traite-t-elle des EURL ? santé ou commercial ?) | **Inconnu** | OUI — question structurante. |

> Aucun dossier `project/source_documents/eurl/` n'a été créé : il n'y a rien à y placer. Il sera
> créé **uniquement** quand des modèles EURL réels seront fournis.

## 3. Plan de fondation ordonné (à exécuter une fois les cas connus)

Suit `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. La SELARL est l'implémentation de référence
(« Réf. SELARL » ci-dessous).

0. **Débloquer les intrants (PRÉ-REQUIS, ici et maintenant).**
   - Envoyer le **Bloc 1** de `NOTEBOOKLM_PROMPTS.md` (existence EURL + liste des cas + carte
     cas→documents). Puis Bloc 2 (modèles + variables).
   - Si NotebookLM ne suffit pas → **Pack de passation Rafael** (via Gad). **Ne rien inventer.**
   - **Sortie de gate :** carte officielle cas→documents EURL + modèles `.docx` tokenisés reçus.

1. **Phase 1 — Sources.** Ranger les modèles EURL dédupliqués (NFC/NFD, pas de doublon) dans
   `project/source_documents/eurl/` (à créer alors). Charger le canon EURL et les locks humains.
   _Réf. SELARL : `project/source_documents/lot_*`, `project/source_truth/`._

2. **Phase 2 — Cartographie des cas.** Construire la matrice cas→documents EURL (remplacer les
   hypothèses de `CARTOGRAPHIE_TENTATIVE.md` par le canon ratifié). Ajouter `EURL` à `CaseType` et
   les occurrences de documents au `case_catalog`.

3. **Phase 3 — Moteur.** Un générateur par document (`generators/lot_*`), module `eurl_common.py`,
   remplissage `fill_docx_template` + garde anti-token-résiduel ; fixtures `scenarios/eurl.py` ;
   modèles `…Context` dans `domain/models.py` ; codes documents + mapping registre.
   _Réf. SELARL : `generators/lot_01..05/`, `rendering/docx_template_fill.py`, `scenarios/selarl.py`._

4. **Phase 4 — Règles juridiques.** Escalade sources → NotebookLM → Rafael. Pièges : coquilles
   inter-profession, durée société (figée) vs domiciliation (« indéterminée »), origine de propriété,
   salariés 0/1/N. **Spécifique EURL : option fiscale IR/IS, décision de l'associé unique.**

5. **Phase 5 — Transverses.** Genre (paires de chaînes exactes, jamais de regex de terminaison) ;
   **unipersonnel → singulier** par défaut. _Réf. SELARL : `utils/grammar.py`._

6. **Phase 6 — UI Streamlit.** Slice `front_app/eurl_slice.py` + sous-formulaires par cas + bouton
   « Générer des données de test » prérempli depuis les fixtures (1 clic, 0 token résiduel).
   _Réf. SELARL : `front_app/shell.py`, `front_app/selarl_slice.py`._

7. **Phase 7 — Vérification.** `ruff` clean + suite COMPLÈTE verte (`--basetemp` hors repo), 0 token
   résiduel, masculin **et** féminin, tous les cas. Re-vérifier soi-même (pas d'auto-rapport).

8. **Phase 8 — Gate juridique.** Génération **NO-GO** tant que Rafael/Albane n'a pas validé le
   wording. Fondation technique + UI peuvent être GO indépendamment (preview/test).

9. **Phase 9 — Journal & clôture.** Décisions ratifiées avec codes stables `EURL-…` ; reverser les
   leçons dans le workflow. **Merge `eurl/… → main` + déploiement = geste PM.**

## 4. Discipline (rappel)

1 type = 1 branche `eurl/<ticket>` ; vérifier `git branch --show-current` avant tout edit/commit ;
`add` explicite ; ne pas éditer la couche partagée à deux sessions ; merge `main` réservé au PM.
