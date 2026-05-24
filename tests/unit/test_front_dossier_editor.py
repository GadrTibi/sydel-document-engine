from __future__ import annotations

import inspect

from streamlit.testing.v1 import AppTest

import sydel_doc_engine.app.front_dossier_editor as front_dossier_editor
from sydel_doc_engine.app.front_dossier_editor import (
    build_front_dossier_editor_dossier,
    build_front_dossier_editor_view,
    front_dossier_block_rows,
    front_dossier_document_status_rows,
    front_dossier_editor_profile_labels,
    front_dossier_flow_step_rows,
    front_dossier_lot_status_legend_rows,
    front_dossier_lot_status_rows,
    front_dossier_requirement_rows,
    front_dossier_summary_rows,
)
from sydel_doc_engine.app.front_shell import PROTOTYPE_TOOLS_LABEL, TARGET_FRONT_LABEL
from sydel_doc_engine.front_data import DossierRecord, OperationType


def test_front_dossier_editor_builds_minimal_dossier_from_profile() -> None:
    dossier = build_front_dossier_editor_dossier("SELARL creation simple")

    assert isinstance(dossier, DossierRecord)
    assert dossier.structure == "SELARL"
    assert dossier.metadata["front_editor_v1"] is True
    assert set(dossier.document_requirements) == {
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    }
    assert {context.operation_type for context in dossier.operation_contexts.values()} == {
        OperationType.CREATION,
    }
    assert dossier.persons == {}
    assert dossier.companies == {}
    assert dossier.role_assignments == {}
    assert dossier.addresses == {}


def test_front_dossier_editor_exposes_flow_steps_and_active_blocks() -> None:
    view = build_front_dossier_editor_view("SELARL ordre / inscription")
    step_rows = front_dossier_flow_step_rows(view)
    block_rows = front_dossier_block_rows(view)

    assert [row["etape"] for row in step_rows][:3] == [
        "Qualification / type d'operation",
        "Fiche client / personnes",
        "Fiche societe",
    ]
    assert any("Ordre / inscription" == row["etape"] for row in step_rows)
    assert any(row["bloc"] == "Ordre et identifiants ordinaux" for row in block_rows)
    assert any(row["bloc"] == "Mandataire et derogation ordre" for row in block_rows)
    assert all("streamlit" not in row["bloc"].lower() for row in block_rows)


def test_front_dossier_editor_exposes_requirements_statuses_and_lot_statuses() -> None:
    view = build_front_dossier_editor_view("SCM cession de parts")
    summary_rows = front_dossier_summary_rows(view)
    requirement_rows = front_dossier_requirement_rows(view)
    status_rows = front_dossier_document_status_rows(view)
    lot_rows = front_dossier_lot_status_rows(view)
    legend_rows = front_dossier_lot_status_legend_rows()

    assert summary_rows[0]["structure"] == "SCM"
    assert {row["document"] for row in requirement_rows} == {"DOC-033", "DOC-025"}
    assert {row["document"] for row in status_rows} == {"DOC-033", "DOC-025"}
    assert all(row["statut"] == "blocked_missing_data" for row in status_rows)
    assert lot_rows[0]["statut"] == "blocked"
    assert {row["statut"] for row in legend_rows} == {"ready", "partial", "blocked"}


def test_front_dossier_editor_profiles_cover_prudent_first_slice() -> None:
    labels = front_dossier_editor_profile_labels()

    assert labels == (
        "SELARL creation simple",
        "SELARL ordre / inscription",
        "SELARL cession cabinet + bail + financement",
        "SCM cession de parts",
        "SPFPL apport de titres",
    )


def test_front_dossier_editor_has_no_streamlit_dependency() -> None:
    source = inspect.getsource(front_dossier_editor).lower()

    assert "import streamlit" not in source
    assert "session_state" not in source


def test_streamlit_shell_renders_new_dossier_editor() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    assert app.radio[0].value == TARGET_FRONT_LABEL
    app.radio[1].set_value("Dossier")
    app.run(timeout=120)

    assert app.selectbox(key="front_dossier_editor_profile").label == (
        "Type de dossier / structure de base"
    )
    assert any("Editeur dossier" in item.value for item in app.subheader)
    assert any("Documents attendus et statuts" in item.value for item in app.subheader)
    assert any("Placeholder controle" in item.value for item in app.warning)


def test_streamlit_shell_keeps_prototype_zone_secondary() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    app.radio[0].set_value(PROTOTYPE_TOOLS_LABEL)
    app.run(timeout=120)

    assert any(PROTOTYPE_TOOLS_LABEL in item.value for item in app.subheader)
    assert app.radio[1].label == "Outil de test / prototype"
