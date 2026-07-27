"""Slice front SPFPL cession (DOC-035) — delegue au socle SPFPL."""

from __future__ import annotations

from sydel_doc_engine.front_app.spfpl_slice import (
    build_generation_context,
    build_spfpl_plan,
    generate_dossier,
    render_spfpl_form,
)

STRUCTURE = "SPFPL cession"

__all__ = [
    "STRUCTURE",
    "build_generation_context",
    "build_spfpl_plan",
    "generate_dossier",
    "render_spfpl_form",
]
