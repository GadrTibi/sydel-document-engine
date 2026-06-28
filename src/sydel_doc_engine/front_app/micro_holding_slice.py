"""Slice front micro holding (DOC-047) — delegue au socle des statuts civils.

Micro holding = societe civile A CAPITAL VARIABLE (demande Albane 2026-06-26). Le socle
civil partage (`civil_statuts_slice`) porte la saisie societe (1..6 associes), le capital
effectif/minimum saisi, le maximum auto = 10x le minimum, la mention de capital variable, et
le selecteur de variante d'objet social A (generique) / B (holding). Aucune regle metier
propre ici : on ne fait que router vers le socle.
"""

from __future__ import annotations

from sydel_doc_engine.front_app.civil_statuts_slice import (
    build_civil_plan,
    build_generation_context,
    generate_dossier,
    render_civil_form,
)

STRUCTURE = "MICRO_HOLDING"

__all__ = [
    "STRUCTURE",
    "build_civil_plan",
    "build_generation_context",
    "generate_dossier",
    "render_civil_form",
]
