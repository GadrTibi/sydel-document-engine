"""Slice front SCS (DOC-019) — delegue au socle des statuts civils."""

from __future__ import annotations

from sydel_doc_engine.front_app.civil_statuts_slice import (
    build_civil_plan,
    build_generation_context,
    generate_dossier,
    render_civil_form,
)

STRUCTURE = "SCS"

__all__ = [
    "STRUCTURE",
    "build_civil_plan",
    "build_generation_context",
    "generate_dossier",
    "render_civil_form",
]
