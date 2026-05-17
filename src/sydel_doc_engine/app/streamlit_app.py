from __future__ import annotations

from pathlib import Path

import streamlit as st

from sydel_doc_engine.app.ui_runtime import (
    GeneratedDossier,
    build_output_dir,
    generate_dossier,
    list_context_examples,
    load_context_payload,
    parse_context_payload,
    selected_document_rows,
)
from sydel_doc_engine.rendering.pdf_export import is_pdf_export_available


@st.cache_data(show_spinner=False)
def _pdf_backend_available() -> bool:
    return is_pdf_export_available()


def _download_file(path: Path, *, label: str, mime: str, key: str) -> None:
    st.download_button(
        label=label,
        data=path.read_bytes(),
        file_name=path.name,
        mime=mime,
        key=key,
    )


def _render_downloads(result: GeneratedDossier) -> None:
    st.subheader("Telechargements")

    st.markdown("DOCX")
    for index, path in enumerate(result.docx_paths):
        _download_file(
            path,
            label=path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"download-docx-{index}-{path.name}",
        )

    if result.pdf_paths:
        st.markdown("PDF")
        for index, path in enumerate(result.pdf_paths):
            _download_file(
                path,
                label=path.name,
                mime="application/pdf",
                key=f"download-pdf-{index}-{path.name}",
            )

    _download_file(
        result.zip_path,
        label="Telecharger le ZIP dossier",
        mime="application/zip",
        key=f"download-zip-{result.zip_path.name}",
    )


st.set_page_config(page_title="SYDEL Document Engine", layout="wide")

st.title("SYDEL Document Engine")
st.caption("Generation dossier DOCX, PDF local optionnel et ZIP.")

if "context_payload" not in st.session_state:
    st.session_state.context_payload = ""
if "context_source_name" not in st.session_state:
    st.session_state.context_source_name = "contexte.yaml"
if "generated_dossier" not in st.session_state:
    st.session_state.generated_dossier = None

st.subheader("Contexte dossier")
examples = list_context_examples()
example_names = [""] + [path.name for path in examples]
selected_example = st.selectbox("Charger un exemple", example_names)
if st.button("Charger le contexte exemple", disabled=not selected_example):
    selected_path = next(path for path in examples if path.name == selected_example)
    st.session_state.context_payload = load_context_payload(selected_path)
    st.session_state.context_source_name = selected_path.name
    st.session_state.generated_dossier = None

uploaded_context = st.file_uploader(
    "Ou charger un contexte YAML/JSON",
    type=["yaml", "yml", "json"],
)
if uploaded_context is not None:
    st.session_state.context_payload = uploaded_context.getvalue().decode("utf-8")
    st.session_state.context_source_name = uploaded_context.name
    st.session_state.generated_dossier = None

payload = st.text_area(
    "Contexte YAML/JSON",
    value=st.session_state.context_payload,
    height=320,
)
if payload != st.session_state.context_payload:
    st.session_state.context_payload = payload
    st.session_state.context_source_name = "contexte_manuel.yaml"
    st.session_state.generated_dossier = None

ctx = None
selected_rows: list[dict[str, str]] = []
if st.session_state.context_payload.strip():
    try:
        ctx = parse_context_payload(st.session_state.context_payload)
        selected_rows = selected_document_rows(ctx)
        st.success("Contexte valide.")
    except ValueError as exc:
        st.error(f"Contexte invalide : {exc}")

if ctx is not None:
    st.subheader("Documents selectionnes")
    if selected_rows:
        st.table(selected_rows)
    else:
        st.warning("Aucun document selectionne par l'orchestrateur pour ce contexte.")

pdf_available = _pdf_backend_available()
st.subheader("Generation")
if pdf_available:
    st.info("Backend PDF local disponible. La conversion depend de LibreOffice ou Word local.")
else:
    st.warning(
        "Backend PDF local indisponible. Installez LibreOffice, configurez "
        "SYDEL_LIBREOFFICE_PATH ou utilisez Microsoft Word COM sous Windows."
    )

generate_pdf = st.checkbox(
    "Generer les PDF si le backend local est disponible",
    value=pdf_available,
    disabled=not pdf_available,
)
output_dir = build_output_dir(st.session_state.context_source_name)
st.text_input("Dossier de sortie", value=str(output_dir), disabled=True)

can_generate = ctx is not None and bool(selected_rows)
if st.button("Generer le dossier", type="primary", disabled=not can_generate):
    assert ctx is not None
    with st.spinner("Generation du dossier en cours..."):
        try:
            result = generate_dossier(ctx, output_dir, generate_pdf=generate_pdf)
            st.session_state.generated_dossier = result
        except Exception as exc:  # noqa: BLE001 - Streamlit must display user-facing failures.
            st.session_state.generated_dossier = None
            st.error(f"Generation bloquee : {exc}")

result = st.session_state.generated_dossier
if isinstance(result, GeneratedDossier):
    st.success(
        f"Dossier genere : {len(result.docx_paths)} DOCX, "
        f"{len(result.pdf_paths)} PDF, 1 ZIP."
    )
    if result.pdf_error:
        st.warning(
            "La generation PDF a echoue ; le ZIP contient les fichiers produits "
            f"disponibles. Detail : {result.pdf_error}"
        )
    _render_downloads(result)

st.caption(
    "La generation technique ne vaut pas validation juridique ni revue visuelle humaine. "
    "Les artefacts sont produits sous artifacts/ et restent hors versionnement."
)
