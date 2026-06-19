---
name: project-selas-parity-context
description: SELAS pluripersonnelle parity port context — RAF-001 to RAF-006, gold-anchored method, implementation entry points
metadata:
  type: project
---

Methode ratifiee gold-anchored parity (docs/review/METHODE_PARITE_GOLD.md). SELARL = gold.

Retours Rafael SELAS pluri 2026-06-19 : RAF-001 (bug RC), RAF-002 (valeur nominale), RAF-003 (logiques SELARL toutes), RAF-004 (placeholders), RAF-005 (dates Aujourd'hui), RAF-006 (cloture +1 an).

**Why:** SELAS multi slice (selas_multi_slice.py) construit en parallele du gold SELARL au lieu d'en deriver -> ecarts UX + bug generation.

**How to apply:** Pour tout nouveau type, partir du gold SELARL (selarl_slice.py + shell.py SELARL section) et lister les differences justifiees avant de construire quoi que ce soit. Helpers partageables vivent dans shell.py (prive, _date_input_with_today) ou common_creation.py (public).

RAF-001 racine : _regime_communautaire() dans selas_multi_slice.py passe signature_date comme date_courrier_avertissement ; si signature_date=None, CODE-RC-001 leve. Fix = date.today() comme fallback (meme comportement que data_entry.py SELARL).

_date_input_with_today est dans shell.py (prive, ligne 1626). A extraire vers common_creation.py ou field_derivations.py pour partage avec selas_multi_slice.py.
