---
name: sasu-holding-type
description: SASU Holding (SAS unipersonnelle holding generaliste) cable en DOC-048 ; les satellites SAS DOC-023/DOC-024 sont verrouilles SPFPL medecins et NON reutilisables tels quels
metadata:
  type: project
---

Type **SASU Holding** = SAS unipersonnelle, holding patrimoniale GENERALISTE (modele officiel
Albane 2026-06-29), DISTINCT de la « SAS / SPFPL medecins » (DOC-015, conservee). Cable Phase 1
(commit `bff8913`, branche `sprint/engine-completion`).

**Why:** decision PM ratifiee ; patron = enregistrement micro holding.

**How to apply / faits durables :**
- Statuts = **DOC-048**, generator `StatutsSasuHoldingGenerator` (token-replacement pur,
  contexte dedie `statuts_sasu_holding`, accord de genre associe(e) unique). Gating
  orchestrateur = `_statuts_sasu_holding_enabled` (structure `SASU_HOLDING` + contexte present,
  PAS de condition profession). Slice = `front_app/sasu_holding_slice.py`, route dans
  `shell._render_typed_dossier` (branche `structure == "SASU_HOLDING"`).
- **PIEGE satellites** : le bundle Albane = 6 pieces (statuts + DNC + domiciliation + procuration
  + PV remuneration president + liste souscripteurs). Les 2 derniers ont leurs PROPRES modeles
  generalistes (locks `docs/review/albane_sas_2026-06-29/`) MAIS les generateurs existants
  **DOC-023 (PvRemunerationPresident) / DOC-024 (AttestationCapitalListeSouscripteursSas)** sont
  **verrouilles SPFPL medecins** par `sas_satellites_common.validate_sas_satellite_scope`
  (raise si structure != SAS, type != spfpl_medecins, profession hors {medecin}, genre !=
  masculin) et emettent du wording « SPFPL de Profession Liberale de medecins ». **Non
  reutilisables** pour une holding generaliste -> a BATIR (generateurs generalistes neufs,
  phase fidelite). Bundle generable a ce stade = **4 pieces** (statuts + tronc commun
  DOC-001/002/003, universels via `ALL_STRUCTURES`).
- `Person.date_naissance` est typee `date` STRICTE (pydantic) : ne JAMAIS y mettre une chaine
  verbatim (« 1er janvier 1990 ») -> ValidationError. Pour SASU Holding le statuts derive le
  rendu francais de la date ISO (`_french_date` accepte `date|str`), donc une seule source ISO
  suffit (pas le double champ verbatim/ISO du slice SAS). Lie a [[trap-date-fields-verbatim-not-calendar]].
- Tests : `tests/unit/test_statuts_sasu_holding.py` (generateur) + `tests/unit/test_sasu_holding_plan.py`
  (wiring/bundle/routing). Assertions de count a maj quand on ajoute un type : `CATALOG_DOCUMENTS`
  (53), dropdown `test_multi_type_front`, set des structures.
