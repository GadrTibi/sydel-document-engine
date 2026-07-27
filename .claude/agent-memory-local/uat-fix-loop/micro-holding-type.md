---
name: micro-holding-type
description: Type micro holding (DOC-047) ajoute au moteur Sydel — societe civile a capital variable, objet A/B
metadata:
  type: project
---

Type **micro holding** ajoute au Sydel Document Engine (demande Albane mail 2026-06-26).

**Fait :** societe civile A CAPITAL VARIABLE. Clone du socle civil SCI ; le SEUL bloc objet
(article 2) est pilote par variante **A (generique civil, extrait modele SCI)** / **B (holding,
extrait modele SASU Holding adapte « civiles et commerciales »->« civiles »)**. Capital : effectif
= minimum saisi, maximum = 10x le minimum (deja calcule par le socle civil `build_generation_context`).

**Why :** Albane tranche A vs B « demain » (apres 2026-06-26) ; les DEUX ont ete construites sur
GO PM de Gad, la mauvaise sera retiree ensuite. Aucun texte juridique invente (verbatim du ticket).

**How to apply :**
- Structure = `MICRO_HOLDING` ; type statuts = `micro_holding` ; doc-id = **DOC-047** ; cle registry
  = `micro_holding_v1`.
- Fichiers neufs : `generators/lot_04/statuts_micro_holding.py` (constantes OBJET_VARIANTE_A/B +
  `objet_social_for_variante`), `front_app/micro_holding_slice.py`, modele
  `project/source_documents/lot_04/Modele statuts micro holding.docx` (token `[objet_social]` a
  l'index 55), test `tests/unit/test_statuts_micro_holding.py`.
- Cablage : `CIVIL_TYPE_BY_STRUCTURE`/forme/bornes dans `civil_statuts_slice.py` ;
  `MICRO_HOLDING_TEMPLATE` + hook `[objet_social]` dans `statuts_civils_common.py` ;
  `ALL_STRUCTURES`/`PV_NOMINATION_GERANT_STRUCTURES`/DOC-047 dans `catalog.py` ; mapping+generateur
  dans `orchestrator/service.py` ; CaseType+occurrences dans `case_catalog.py` ; `type_registry.py`.
- Champ modele : `StatutsCivilsContext.objet_social` (None pour les autres civiles).
- Quand Albane tranche : retirer la variante perdante de `OBJET_VARIANTES` + le selecteur du slice.
- Gate Akainu en attente avant de declarer TRAITE (cf. regle 66).
