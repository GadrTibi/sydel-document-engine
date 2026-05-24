from __future__ import annotations

from streamlit.testing.v1 import AppTest

from sydel_doc_engine.app.front_shell import (
    PROTOTYPE_TOOLS_LABEL,
    TARGET_FRONT_LABEL,
    front_shell_navigation_rows,
    shell_document_status_rows,
    shell_flow_step_rows,
    shell_lot_status_rows,
)


def test_front_shell_navigation_separates_target_and_prototype_tools() -> None:
    rows = front_shell_navigation_rows()

    assert {row["espace"] for row in rows} == {
        TARGET_FRONT_LABEL,
        PROTOTYPE_TOOLS_LABEL,
    }
    assert {"Accueil / selection", "Dossier", "Documents attendus", "Generation"}.issubset(
        {row["zone"] for row in rows}
    )
    assert {"Document unitaire", "Technique / diagnostic"}.issubset(
        {row["zone"] for row in rows if row["espace"] == PROTOTYPE_TOOLS_LABEL}
    )


def test_front_shell_exposes_dossier_flow_steps_from_front_data() -> None:
    rows = shell_flow_step_rows()
    labels = [row["zone"] for row in rows]

    assert labels[:3] == [
        "Qualification / type d'operation",
        "Fiche client / personnes",
        "Fiche societe",
    ]
    assert "Documents attendus" in labels
    assert "Generation" in labels
    assert any("Assignments de roles" in row["blocs actifs"] for row in rows)


def test_front_shell_exposes_document_status_preview() -> None:
    rows = {row["document"]: row for row in shell_document_status_rows()}
    lot_rows = shell_lot_status_rows()

    assert rows["DOC-002"]["statut"] == "expected"
    assert rows["DOC-006"]["statut"] == "generable_with_reserve"
    assert rows["DOC-013"]["statut"] == "manual_only"
    assert rows["DOC-014"]["generation"] == "non"
    assert lot_rows[0]["statut"] == "partial"


def test_streamlit_shell_renders_target_front_by_default() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    assert app.radio[0].label == "Espace de travail"
    assert app.radio[0].value == TARGET_FRONT_LABEL
    assert any(TARGET_FRONT_LABEL in item.value for item in app.subheader)
    assert any("nouvelle entree produit" in item.value for item in app.info)


def test_streamlit_shell_keeps_prototype_tools_secondary() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    app.radio[0].set_value(PROTOTYPE_TOOLS_LABEL)
    app.run(timeout=120)

    assert any(PROTOTYPE_TOOLS_LABEL in item.value for item in app.subheader)
    assert any("front cible" in item.value for item in app.caption)

    app.radio[1].set_value("Document unitaire")
    app.run(timeout=120)
    assert app.selectbox(key="single_document_choice").label == "Document a tester"

    app.radio[1].set_value("Technique / diagnostic")
    app.run(timeout=120)
    assert any("Mode technique / diagnostic" in item.value for item in app.subheader)
