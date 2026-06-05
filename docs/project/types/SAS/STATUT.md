# SAS — Statut de fondation & plan (V1)

> **Date :** 2026-06-05 · **Auteur :** session fondation SAS (lecture seule sur Drive/repo ; écriture
> limitée à `project/source_documents/sas/` et `docs/project/types/SAS/`).
> **Posture : ZÉRO CONFIANCE dans l'auto-rapport.** Tout ce qui suit sur le code Codex est constaté par
> lecture des fichiers, **pas** par exécution. Les statuts d'avancement déclarés par Codex
> (`workflow_status=TESTE`) sont à **re-vérifier soi-même** (suite complète + ouverture DOCX) avant d'y croire.

---

## 1. Ce que Codex a DÉJÀ fait pour SAS dans `src/` (constaté, à RE-VÉRIFIER)

| Élément | Emplacement | Constat | À re-vérifier |
|---|---|---|---|
| Type de cas `SAS` | `domain/case_catalog.py` (`CaseType.SAS`) | Déclaré. Documents listés : statuts_sas, declaration_non_condamnation, autorisation_domiciliation, procuration, attestation_capital_sas, pv_remuneration_president, + entrée « Liste des souscripteurs ». | Cet assemblage est **inventé par Codex** (pas de canon SAS) → non ratifié. |
| Registre documents | `registry/catalog.py` | DOC-015 (statuts SAS/SPFPL médecins), DOC-023 (PV rémunération président SAS), DOC-024 (attestation capital / liste souscripteurs). `workflow_status=TESTE`. Périmètre verrouillé **SPFPL médecins / actionnaire unique**. | Statut « TESTE » non prouvé ici ; périmètre profession non confirmé. |
| Générateur statuts | `generators/lot_04/statuts_sas.py` (`StatutsSasGenerator`) | **FROM-SCRATCH** : construit le document en code (`new_document()`, `add_statuts_article_heading`…), **ne remplit PAS le modèle .docx source**. | ⚠️ **Viole le principe de fidélité** (Phase 1/3 : remplissage de template). Le wording vit dans le code, pas dans le `.docx`. |
| Générateurs satellites | `generators/lot_05/` : `sas_satellites_common.py`, `pv_remuneration_president.py`, `attestation_capital_liste_souscripteurs_sas.py` | Également **from-scratch** (`new_document()`). | Même réserve de fidélité. |
| Câblage moteur | `orchestrator/service.py` | DOC-015/023/024 mappés aux générateurs ; activation gardée par `ctx.structure == "SAS"` + `statuts_sas.type == "spfpl_medecins"` + actionnaire unique. | OK structurellement, mais dépend du périmètre non confirmé. |
| Specs de travail | `docs/delivery/lot_04_statuts_sas_*`, `docs/delivery/lot_05_sas_satellites_*` | Specs canonique + texte écrites par Codex. | Ce sont des specs **dérivées**, pas du canon validé Rafael. |
| Tests | `tests/unit/test_lot_05_sas_satellites.py` (+ refs SAS dans `test_case_catalog.py`, `test_orchestrator_service.py`) | Présents. | **NON exécutés dans cette session** (tâche fondation, lecture seule). À lancer suite COMPLÈTE (`--basetemp` hors repo) avant toute confiance. |

### Anomalies relevées (à traiter)
- **Référence source morte :** DOC-023/DOC-024 pointent `project/source_import/raw_drive_dump/Creation SAS/…`
  → **ce dossier n'existe pas** dans ce repo. Les modèles réels viennent désormais de
  `project/source_documents/sas/` (copiés cette session).
- **`attestation_capital_sas` sans modèle source :** aucun `.docx` « Attestation sur le capital - apport -
  liste des souscripteurs » dans `Création SAS`. Soit modèle manquant, soit confusion avec la « Liste des
  souscripteurs » → **question NotebookLM B4**.
- **Pas de `scenarios/sas.py`** (seul `scenarios/selarl.py` existe) et **aucune slice UI SAS**
  (`front_app/` n'a que `selarl_slice.py`) → la SAS **n'est pas branchée à l'interface**, pas de bouton
  « données de test » SAS.
- **From-scratch vs template-fill :** les générateurs SAS reconstruisent le texte en Python. À décider :
  refondre en remplissage du `.docx` source (fidélité), ou assumer le from-scratch (risque de dérive du
  wording, non validé Rafael).

---

## 2. Ce qui MANQUE (bloquants de fondation)

1. **LE CANON SAS (bloquant n°1).** Aucune carte officielle « cas → documents » pour la SAS : le canon
   `Documents_a_generer_par_cas_V3.docx` est **100 % SELARL** (vérifié sur le contenu). → résoudre via
   `NOTEBOOKLM_PROMPTS.md` bloc A, puis Rafael. Sans ça, **le backlog SAS n'est pas ratifiable**.
2. **Périmètre du type SAS non confirmé** : médecin seulement ? SASU/holding inclus ? cession d'actions ?
   régime communautaire ? (blocs A4/A5, D2).
3. **Modèle « attestation capital » introuvable** (B4) et **deux variantes « liste des souscripteurs »**
   non arbitrées (B3).
4. **Wording non validé** : génération SAS **NO-GO** tant que Rafael/Albane n'a pas validé (Phase 8).
5. **Couche UI absente** : pas de slice ni de scénarios SAS (Phase 6 non entamée).
6. **Fidélité non garantie** : générateurs from-scratch ≠ remplissage du modèle source.

### Modèles : présents (pas un manque)
Les 7 modèles `.docx` du dossier `Création SAS` sont **copiés** dans `project/source_documents/sas/`
(cf. `INVENTAIRE_MODELES.md`). Le seul statuts est **SAS/SPFPL médecins**. Candidat hors corpus non
copié : `statuts SASU Holding` (à arbitrer).

---

## 3. PLAN DE FONDATION ordonné (selon `WORKFLOW_TYPE_ENTREPRISE_V1.md`)

> Ordre strict : on ne code pas un backlog non ratifié. La **fondation technique + UI** peut avancer en
> parallèle sur branche dédiée, mais la **génération reste NO-GO** jusqu'au gate juridique.

- **Étape 0 — Cadrage & branche (Phase 0).** Branche `sas/<ticket>` dédiée (via `git-branch-steward`).
  Périmètre confirmé. *(Git = hors scope de cette session.)*
- **Étape 1 — Sources (Phase 1). [PARTIELLEMENT FAIT]** Modèles copiés et inventoriés. **Reste** :
  trancher SASU Holding + variantes liste souscripteurs ; localiser/écarter « attestation capital ».
- **Étape 2 — Cartographie des cas (Phase 2). [BLOQUÉ canon]** Envoyer `NOTEBOOKLM_PROMPTS.md` bloc A →
  obtenir la liste des cas + carte cas → documents → ratifier la matrice (remplace `CARTOGRAPHIE_TENTATIVE.md`).
  **Gate :** rien en aval n'est figé tant que cette matrice n'est pas validée.
- **Étape 3 — Moteur fidèle (Phase 3).** Une fois les cas connus : pour chaque document, **remplissage du
  modèle source** (`rendering/docx_template_fill.py`) avec sécurité anti-token-résiduel ; ranger par lot ;
  déclarer les codes `DOC-0xx` + mapping registre ; **réconcilier** avec les générateurs Codex existants
  (refondre les from-scratch en template-fill, ou justifier). Corriger les `source_path` morts.
- **Étape 4 — Règles juridiques (Phase 4).** Vérifier durée société SAS, mentions profession (anti-coquille
  médecin/dentiste/pharmacien), absence/rémunération président, origine du capital. Blocs B + D.
- **Étape 5 — Genre / pluriel (Phase 5).** Paires de chaînes exactes (président/présidente, actionnaire
  unique/associée…) via `utils/grammar.apply_gender_pairs`. Pluriel **après validation Albane**. Bloc C.
- **Étape 6 — UI Streamlit (Phase 6).** Créer `scenarios/sas.py` (fixtures complètes) puis `front_app/sas_slice.py`
  + câblage shell : qualification SAS → sous-formulaires par cas → génération ; bouton « données de test »
  préremplit tout (1 clic). Réf. SELARL.
- **Étape 7 — Vérification (Phase 7).** `ruff` clean + **suite COMPLÈTE verte** (`--basetemp` hors repo) ;
  génération via le chemin UI sans token résiduel ; masculin **et** féminin ; ouvrir les DOCX (preuve) ;
  revue de fidélité vs modèle source. **Ne jamais croire l'auto-rapport.**
- **Étape 8 — Gate juridique (Phase 8).** Génération **NO-GO** tant que wording non validé Rafael/Albane.
  Pack de passation = questions épuisées côté NotebookLM, formulées pour Rafael.
- **Étape 9 — Journal & clôture (Phase 9).** Décisions ratifiées au journal (`SAS-…`), état courant à jour,
  leçons reversées dans le workflow. **Merge `sas/… → main` + déploiement = geste PM.**

---

## 4. Pack de passation (à finaliser après NotebookLM, message Rafael — pas au PM)

Questions à épuiser d'abord côté NotebookLM (cf. `NOTEBOOKLM_PROMPTS.md`), puis, pour les restantes,
message Rafael (jamais une question métier au PM) :
- Liste des cas SAS + carte cas → documents (A1-A3) — **bloquant**.
- Périmètre profession/forme : médecin only ? SASU/holding ? (A4-A5).
- Modèle « attestation capital » : existe-t-il, distinct de la liste des souscripteurs ? (B4).
- Variante de référence « liste des souscripteurs » (B3).
- Cas cession d'actions / régime communautaire en SAS (D2).
- Durée de la société SAS (figée ou variable) (B1).

> Tant que ces points ne sont pas tranchés, la SAS reste en **fondation** : on peut bâtir la mécanique
> et l'UI sur branche, mais **la génération de documents SAS est NO-GO**.
