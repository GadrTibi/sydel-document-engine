# Backlog migration from-scratch → token-replacement

**Décision PM (Gad, 2026-06-29)** : migrer UNIQUEMENT `statuts_sas` (le seul vrai gain) ;
**tenir tout le reste** (dette tracée ci-dessous). Ne PAS migrer à l'aveugle.

## Constat d'architecture (assessment 2026-06-29, 5 agents read-only)

La prémisse initiale (« le from-scratch est une copie fragile, le modèle est la vérité ») est
**INVERSÉE pour la plupart des documents** :

> **Ce sont les GÉNÉRATEURS (le code) qui portent la vérité validée d'Albane** (retours des
> 10/17/26 juin) ; **les MODÈLES `.docx` tokenisés sont PÉRIMÉS** (état d'avant ces retours).
> Migrer naïvement = **régression** (on perd les édits validés).

Trois familles d'architecture coexistent — seule la famille C est à migrer :

| Famille | Mécanisme | Statut |
|---|---|---|
| A. Déjà token-replacement sur DOCX (`Document(model)` + `_build_*_replacements`) | actes/compromis cession cabinet, autorisation_domiciliation | **FAIT** |
| B. Déjà block-template (tuples `*_BLOCKS` + garde anti-`[ ]`) | statuts lot_04, satellites SCM | **FAIT/convergé** |
| C. From-scratch programmatique (prose codée en dur) | le backlog ci-dessous | **À migrer** |

## FAIT cette session

- **`statuts_sas` (DOC-015)** — VRAI from-scratch (~1100 lignes de prose en dur) → token-replacement
  sur `STATUTS_SAS_SPFPL_medecins_modele.docx` (modèle À JOUR, 30 tokens). 625 lignes supprimées,
  validation métier conservée, 218/220 paragraphes texte-identiques, 7 tests verts sans modification,
  normalisation byte-neutre (NBSP/tabs/trailing), 2 défauts d'authoring du modèle corrigés
  (ligne 93 collage nom/montant ; ARTICLE 23 = seul article non souligné).

  **Gate Akainu (verdict)** : prose juridique **byte-identique** (33263=33263 chars, char-level
  identique), zéro token résiduel, zéro NBSP/TAB, bloc capital correct, gardes métier identiques,
  suite 796 verte. **Décision de gouvernance (Gad-flag)** : sur 3 intitulés (« Le soussigné : »,
  l'entrée du soussigné, la dénomination art.3), le migré **gagne l'emphase gras/souligné du
  modèle d'Albane** que l'ancien from-scratch avait perdue → **plus fidèle au document source**,
  prose inchangée. ARTICLE 23 (défaut modèle) corrigé. Nitpicks acceptés/tracés : titre d'annexe
  en 2 paragraphes (vs 1 avec saut de ligne) ; footer écrit aussi sur `even_page_footer` (rendu
  équivalent). Aucun BLOQUANT.

## TENU (dette — NE PAS migrer sans GO PM + sans gérer le risque de régression)

Critère de risque dominant : **modèle périmé** (régression si migration naïve) et/ou **logique
dynamique** que le token-replacement ne peut pas exprimer (overlays, conditionnels, repeaters,
tableaux dynamiques, accord de genre, surlignage).

### HYBRIDE (8) — token + couche post-fill/blocs, effort moyen
- `lot_01/declaration_non_condamnation` — modèle STALE (pré-Albane) à re-tokeniser (département, ordre adresse, aérations, genre)
- `lot_01/procuration` — conditionnel structure (SASU omet une phrase + modèle SAS), titre encadré, genre
- `lot_02/lettre_avertissement_conjoint` — header profession calculé + prénom + exemplaires (4 vs 3) + genre
- `lot_03/appel_fond_sel` — conditionnel cabinet, signataire=mandataire, montant centré ; re-sync modèle requis
- `lot_05/note_information` — blocs conditionnels apport/cession + repeater multi-associés
- `lot_05/attestation_commissaire_apports` — bloc « OU » entre 2 cabinets en dur à remplacer par token
- `lot_05/pv_remuneration_president` — modèle ne porte pas le bloc identité société (add_company_identity_block)
- `lot_05/courrier_sde_cession_scm` — la valeur ajoutée est du LAYOUT (logo, footer, objet) absent du modèle

### COMPLEXE (9) — logique lourde irréductible, risque HAUT
- `lot_02/demande_inscription_ordre` — 3 overlays structure (SELARL_SELAS/SPFPL/SCM), 1 modèle par overlay
- `lot_02/pv_nomination_gerant` — 2 docs distincts (associé unique vs AG multi), N décisions, table signatures
- `lot_03/avenant_contrat_bail` — run-level bold-split, conditionnel « le Docteur » vs « Monsieur », table 3 col.
- `lot_05/acte_cession_parts_spfpl` — exposé dynamique, sections DROP vs spec (arbitrage Albane)
- `lot_05/acte_cession_parts_scm` — credit-vendeur conditionnel, wording SELARL/SELAS, bloc multi-associés
- `lot_05/pv_age_cession_scm` — modèle PÉRIMÉ (V1/gold), féminisation dynamique, surlignage jaune, repeaters
- `lot_05/pv_agrement_cession_spfpl_associe_unique` + `_plusieurs_associes` — gabarit figé N associés vs repeater
- `lot_05/attestation_capital_souscripteurs_selas` — **BLOQUÉ** : modèle multi-souscripteurs INTROUVABLE

### BLOQUÉ MÉTIER (sous-ensemble) — NO-GO tant qu'Albane n'a pas tranché
Ne pas tokeniser un modèle dont le wording est en litige spec≠modèle (on figerait un défaut) :
- `contrat_apport_spfpl` (5 sections absentes : voulues ?), attestations (€ vs euros, élision),
  apport vs cession, erreur de siège SELARL, Dr vs Docteur, dérogations (encart/pièces curés ?).
- → message Albane groupé requis AVANT d'engager ces items (jamais inventer le wording).

## Filet de sécurité (protocole DUR à toute future migration)
1. Capturer le golden AVANT (texte + formatage) au HEAD courant.
2. Migrer (fill + post-fill minimal).
3. Comparer texte des paragraphes non-vides → différences toutes expliquées (sinon STOP).
4. Les tests existants doivent rester verts SANS modification (= contrat validé préservé).
5. Gate Akainu (génération réelle) avant TRAITÉ.

Référence d'implémentation : `src/sydel_doc_engine/generators/lot_04/statuts_sas.py` (migré 2026-06-29).
