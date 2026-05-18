# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import streamlit as st

from sydel_doc_engine.app.business_wizard import (
    BusinessAssociateInput,
    BusinessWizardInput,
    business_document_table_rows,
    business_dossier_types,
    evaluate_business_wizard,
)
from sydel_doc_engine.app.ui_runtime import (
    DEFAULT_ARTIFACTS_DIR,
    GeneratedDossier,
    build_output_dir,
    generate_docx_files,
    generate_dossier,
    generate_pdf_files,
    generate_zip_file,
    list_context_examples,
    load_context_payload,
    parse_context_payload,
    selected_document_rows,
)
from sydel_doc_engine.rendering.pdf_export import is_pdf_export_available

BUSINESS_ARTIFACTS_DIR = Path("artifacts") / "ui_business_wizard_001"
GENDER_OPTIONS = ("masculin", "feminin")


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
    _render_docx_downloads(result.docx_paths, key_prefix="technical")
    if result.pdf_paths:
        _render_pdf_downloads(result.pdf_paths, key_prefix="technical")
    _download_file(
        result.zip_path,
        label="Telecharger le ZIP dossier",
        mime="application/zip",
        key=f"download-technical-zip-{result.zip_path.name}",
    )


def _render_docx_downloads(docx_paths: list[Path], *, key_prefix: str) -> None:
    if not docx_paths:
        return
    st.markdown("DOCX")
    for index, path in enumerate(docx_paths):
        _download_file(
            path,
            label=path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"download-{key_prefix}-docx-{index}-{path.name}",
        )


def _render_pdf_downloads(pdf_paths: list[Path], *, key_prefix: str) -> None:
    if not pdf_paths:
        return
    st.markdown("PDF")
    for index, path in enumerate(pdf_paths):
        _download_file(
            path,
            label=path.name,
            mime="application/pdf",
            key=f"download-{key_prefix}-pdf-{index}-{path.name}",
        )


def _render_business_mode() -> None:
    st.subheader("Mode Assistant metier")
    data = _collect_business_input()
    validation = evaluate_business_wizard(data)

    st.subheader("Etape 3 - Documents generables")
    document_rows = business_document_table_rows(validation)
    if document_rows:
        st.table(document_rows)
    else:
        st.warning("Aucun document cible pour ce type de dossier.")

    st.subheader("Etape 4 - Validation")
    col_generable, col_blocked = st.columns(2)
    col_generable.metric("Documents generables", validation.generable_count)
    col_blocked.metric("Documents bloques", validation.blocked_count)
    if validation.missing_fields:
        st.warning("Champs manquants : " + ", ".join(validation.missing_fields))
    if validation.inconsistencies:
        st.error("Incoherences : " + " ; ".join(validation.inconsistencies))
    for warning in validation.warnings:
        st.info(warning)

    st.subheader("Etape 5 - Generation")
    output_dir = build_output_dir(
        f"assistant_{data.structure}.yaml",
        BUSINESS_ARTIFACTS_DIR,
    )
    st.text_input("Dossier de sortie", value=str(output_dir), disabled=True)

    _ensure_business_session_defaults()
    pdf_available = _pdf_backend_available()
    if pdf_available:
        st.info("Backend PDF local disponible. La conversion reste dependante du poste.")
    else:
        st.warning(
            "PDF local indisponible : DOCX et ZIP restent disponibles. "
            "Installez LibreOffice ou utilisez Word COM si le poste le permet."
        )

    docx_paths = _business_docx_paths()
    pdf_paths = _business_pdf_paths()
    zip_path = _business_zip_path()

    docx_col, zip_col, pdf_col = st.columns(3)
    with docx_col:
        if st.button(
            "Generer les DOCX",
            type="primary",
            disabled=not validation.can_generate_docx,
        ):
            assert validation.context is not None
            with st.spinner("Generation DOCX en cours..."):
                try:
                    docx_paths = generate_docx_files(validation.context, output_dir)
                    st.session_state.business_docx_paths = docx_paths
                    st.session_state.business_pdf_results = []
                    st.session_state.business_pdf_error = None
                    st.session_state.business_zip_path = None
                    st.session_state.business_output_dir = output_dir
                    st.success(f"{len(docx_paths)} DOCX generes.")
                except Exception as exc:  # noqa: BLE001 - Streamlit displays the failure.
                    st.error(f"Generation DOCX bloquee : {exc}")
    with zip_col:
        if st.button("Generer le ZIP", disabled=not docx_paths):
            with st.spinner("Creation du ZIP en cours..."):
                try:
                    active_output_dir = _business_output_dir(output_dir)
                    zip_path = generate_zip_file(active_output_dir, docx_paths, pdf_paths)
                    st.session_state.business_zip_path = zip_path
                    st.success("ZIP dossier genere avec manifest.")
                except Exception as exc:  # noqa: BLE001 - Streamlit displays the failure.
                    st.error(f"Generation ZIP bloquee : {exc}")
    with pdf_col:
        if st.button(
            "Generer les PDF",
            disabled=not (pdf_available and docx_paths),
        ):
            with st.spinner("Conversion PDF en cours..."):
                active_output_dir = _business_output_dir(output_dir)
                pdf_batch = generate_pdf_files(docx_paths, active_output_dir)
                st.session_state.business_pdf_results = pdf_batch.pdf_results
                st.session_state.business_pdf_error = pdf_batch.pdf_error
                if pdf_batch.pdf_error:
                    st.warning(f"PDF non produits : {pdf_batch.pdf_error}")
                else:
                    st.success(f"{len(pdf_batch.pdf_paths)} PDF generes.")

    st.subheader("Etape 6 - Telechargement")
    docx_paths = _business_docx_paths()
    pdf_paths = _business_pdf_paths()
    zip_path = _business_zip_path()
    if docx_paths:
        _render_docx_downloads(docx_paths, key_prefix="business")
    if pdf_paths:
        _render_pdf_downloads(pdf_paths, key_prefix="business")
    if zip_path is not None:
        _download_file(
            zip_path,
            label="Telecharger le ZIP dossier",
            mime="application/zip",
            key=f"download-business-zip-{zip_path.name}",
        )
    if not docx_paths and zip_path is None:
        st.caption("Aucune sortie generee pour le moment.")


def _collect_business_input() -> BusinessWizardInput:
    st.subheader("Etape 1 - Type de dossier")
    dossier_types = business_dossier_types()
    selected_type = st.selectbox(
        "Type de dossier metier",
        dossier_types,
        format_func=lambda item: item.label,
    )
    st.caption(selected_type.status)

    st.subheader("Etape 2 - Informations du dossier")
    with st.expander("Societe", expanded=True):
        societe_forme_sociale = st.text_input("Forme sociale", value=selected_type.structure)
        societe_forme_sociale_affichage = st.text_input(
            "Forme sociale affichee",
            value=_default_forme_affichage(selected_type.structure),
        )
        societe_forme_sociale_libelle_long = st.text_input(
            "Libelle long de forme sociale",
            value=_default_forme_longue(selected_type.structure),
        )
        societe_denomination = st.text_input("Denomination")
        societe_capital_social = st.text_input("Capital social")
        societe_capital_variable = st.checkbox("Capital variable", value=True)
        societe_ville_rcs = st.text_input("Ville RCS")
        st.markdown("Adresse du siege")
        siege_cols = st.columns(4)
        societe_siege_num_voie = siege_cols[0].text_input("Numero", key="societe_num")
        societe_siege_voie = siege_cols[1].text_input("Voie", key="societe_voie")
        societe_siege_cp = siege_cols[2].text_input("Code postal", key="societe_cp")
        societe_siege_ville = siege_cols[3].text_input("Ville", key="societe_ville")

    with st.expander("Associes / personnes physiques", expanded=True):
        personne_genre = st.selectbox("Genre du signataire", GENDER_OPTIONS)
        personne_civilite = st.selectbox("Civilite du signataire", ("", "Monsieur", "Madame"))
        person_cols = st.columns(2)
        personne_prenom = person_cols[0].text_input("Prenom du signataire")
        personne_nom = person_cols[1].text_input("Nom du signataire")
        personne_date_naissance = st.text_input("Date de naissance signataire (AAAA-MM-JJ)")
        personne_nationalite = st.text_input("Nationalite du signataire")
        personne_nom_pere = st.text_input("Nom du pere")
        personne_nom_mere = st.text_input("Nom de la mere")
        personne_fonction_dirigeant = st.text_input("Fonction du signataire")
        st.markdown("Adresse personnelle du signataire")
        personne_addr_cols = st.columns(4)
        personne_adresse_num_voie = personne_addr_cols[0].text_input(
            "Numero",
            key="personne_num",
        )
        personne_adresse_voie = personne_addr_cols[1].text_input(
            "Voie",
            key="personne_voie",
        )
        personne_adresse_cp = personne_addr_cols[2].text_input(
            "Code postal",
            key="personne_cp",
        )
        personne_adresse_ville = personne_addr_cols[3].text_input(
            "Ville",
            key="personne_ville",
        )

        associe_count = st.number_input("Nombre d'associes", min_value=1, max_value=4, value=2)
        associes = _collect_associes(int(associe_count))

    with st.expander("Dirigeant / pharmacien", expanded=True):
        dirigeant_genre = st.selectbox("Genre du dirigeant", GENDER_OPTIONS)
        dirigeant_civilite_affichage = st.selectbox(
            "Civilite du dirigeant",
            ("", "Monsieur", "Madame"),
        )
        dirigeant_cols = st.columns(2)
        dirigeant_prenom = dirigeant_cols[0].text_input("Prenom du dirigeant")
        dirigeant_nom = dirigeant_cols[1].text_input("Nom du dirigeant")
        dirigeant_date_naissance = st.text_input("Date de naissance dirigeant (AAAA-MM-JJ)")
        dirigeant_ville_naissance = st.text_input("Ville de naissance du dirigeant")
        dirigeant_departement_naissance = st.text_input("Departement de naissance du dirigeant")
        dirigeant_nationalite = st.text_input("Nationalite du dirigeant")
        dirigeant_fonction_affichage = st.text_input("Fonction nommee", value="gerant")
        st.markdown("Adresse personnelle du dirigeant")
        dirigeant_addr_cols = st.columns(4)
        dirigeant_adresse_num_voie = dirigeant_addr_cols[0].text_input(
            "Numero",
            key="dirigeant_num",
        )
        dirigeant_adresse_voie = dirigeant_addr_cols[1].text_input(
            "Voie",
            key="dirigeant_voie",
        )
        dirigeant_adresse_cp = dirigeant_addr_cols[2].text_input(
            "Code postal",
            key="dirigeant_cp",
        )
        dirigeant_adresse_ville = dirigeant_addr_cols[3].text_input(
            "Ville",
            key="dirigeant_ville",
        )

    with st.expander("Adresse de domiciliation", expanded=True):
        domiciliation_adresse_affichee = st.text_input("Adresse de domiciliation affichee")

    with st.expander("Capital / parts", expanded=True):
        capital_cols = st.columns(2)
        capital_nb_parts_total_input = capital_cols[0].number_input(
            "Nombre total de parts",
            min_value=0,
            value=0,
        )
        capital_valeur_nominale_part = capital_cols[1].text_input("Valeur nominale par part")

    with st.expander("Dates", expanded=True):
        decision_date = st.text_input("Date de decision (AAAA-MM-JJ ou libelle)")
        reunion_date_lettres = st.text_input("Date de reunion en lettres")
        reunion_heure = st.text_input("Heure de reunion")
        signature_lieu = st.text_input("Lieu de signature")
        signature_date = st.text_input("Date de signature (AAAA-MM-JJ)")
        signature_nombre_exemplaires = st.text_input("Nombre d'exemplaires")

    with st.expander("Options documentaires", expanded=False):
        emprunt_actif = st.checkbox("PV avec autorisation d'emprunt", value=False)
        emprunt_montant_max = ""
        bien_adresse_num_voie = ""
        bien_adresse_voie = ""
        bien_adresse_cp = ""
        bien_adresse_ville = ""
        if emprunt_actif:
            emprunt_montant_max = st.text_input("Montant maximum de l'emprunt")
            bien_cols = st.columns(4)
            bien_adresse_num_voie = bien_cols[0].text_input("Numero", key="bien_num")
            bien_adresse_voie = bien_cols[1].text_input("Voie", key="bien_voie")
            bien_adresse_cp = bien_cols[2].text_input("Code postal", key="bien_cp")
            bien_adresse_ville = bien_cols[3].text_input("Ville", key="bien_ville")

    return BusinessWizardInput(
        structure=selected_type.structure,
        personne_genre=personne_genre,
        personne_civilite=personne_civilite,
        personne_prenom=personne_prenom,
        personne_nom=personne_nom,
        personne_date_naissance=personne_date_naissance,
        personne_nationalite=personne_nationalite,
        personne_nom_pere=personne_nom_pere,
        personne_nom_mere=personne_nom_mere,
        personne_fonction_dirigeant=personne_fonction_dirigeant,
        personne_adresse_num_voie=personne_adresse_num_voie,
        personne_adresse_voie=personne_adresse_voie,
        personne_adresse_cp=personne_adresse_cp,
        personne_adresse_ville=personne_adresse_ville,
        societe_forme_sociale=societe_forme_sociale,
        societe_forme_sociale_affichage=societe_forme_sociale_affichage,
        societe_forme_sociale_libelle_long=societe_forme_sociale_libelle_long,
        societe_denomination=societe_denomination,
        societe_capital_social=societe_capital_social,
        societe_capital_variable=societe_capital_variable,
        societe_siege_num_voie=societe_siege_num_voie,
        societe_siege_voie=societe_siege_voie,
        societe_siege_cp=societe_siege_cp,
        societe_siege_ville=societe_siege_ville,
        societe_ville_rcs=societe_ville_rcs,
        domiciliation_adresse_affichee=domiciliation_adresse_affichee,
        associes=associes,
        dirigeant_genre=dirigeant_genre,
        dirigeant_civilite_affichage=dirigeant_civilite_affichage,
        dirigeant_prenom=dirigeant_prenom,
        dirigeant_nom=dirigeant_nom,
        dirigeant_date_naissance=dirigeant_date_naissance,
        dirigeant_ville_naissance=dirigeant_ville_naissance,
        dirigeant_departement_naissance=dirigeant_departement_naissance,
        dirigeant_nationalite=dirigeant_nationalite,
        dirigeant_fonction_affichage=dirigeant_fonction_affichage,
        dirigeant_adresse_num_voie=dirigeant_adresse_num_voie,
        dirigeant_adresse_voie=dirigeant_adresse_voie,
        dirigeant_adresse_cp=dirigeant_adresse_cp,
        dirigeant_adresse_ville=dirigeant_adresse_ville,
        capital_nb_parts_total=(
            int(capital_nb_parts_total_input) if capital_nb_parts_total_input > 0 else None
        ),
        capital_valeur_nominale_part=capital_valeur_nominale_part,
        decision_date=decision_date,
        reunion_date_lettres=reunion_date_lettres,
        reunion_heure=reunion_heure,
        signature_lieu=signature_lieu,
        signature_date=signature_date,
        signature_nombre_exemplaires=signature_nombre_exemplaires,
        emprunt_actif=emprunt_actif,
        emprunt_montant_max=emprunt_montant_max,
        bien_adresse_num_voie=bien_adresse_num_voie,
        bien_adresse_voie=bien_adresse_voie,
        bien_adresse_cp=bien_adresse_cp,
        bien_adresse_ville=bien_adresse_ville,
    )


def _collect_associes(count: int) -> tuple[BusinessAssociateInput, ...]:
    associes: list[BusinessAssociateInput] = []
    for index in range(count):
        st.markdown(f"Associe {index + 1}")
        cols = st.columns(5)
        genre = cols[0].selectbox(
            "Genre",
            GENDER_OPTIONS,
            key=f"associe_genre_{index}",
        )
        civilite = cols[1].selectbox(
            "Civilite",
            ("", "Monsieur", "Madame"),
            key=f"associe_civilite_{index}",
        )
        prenom = cols[2].text_input("Prenom", key=f"associe_prenom_{index}")
        nom = cols[3].text_input("Nom", key=f"associe_nom_{index}")
        nb_parts_input = cols[4].number_input(
            "Parts",
            min_value=0,
            value=0,
            key=f"associe_parts_{index}",
        )
        present = st.checkbox(
            "Present ou represente",
            value=True,
            key=f"associe_present_{index}",
        )
        associes.append(
            BusinessAssociateInput(
                genre=genre,
                civilite_affichage=civilite,
                prenom=prenom,
                nom=nom,
                nb_parts=int(nb_parts_input) if nb_parts_input > 0 else None,
                est_present_ou_represente=present,
            )
        )
    return tuple(associes)


def _render_technical_mode() -> None:
    st.subheader("Mode technique / diagnostic")
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
    output_dir = build_output_dir(st.session_state.context_source_name, DEFAULT_ARTIFACTS_DIR)
    st.text_input("Dossier de sortie", value=str(output_dir), disabled=True)

    can_generate = ctx is not None and bool(selected_rows)
    if st.button("Generer le dossier", type="primary", disabled=not can_generate):
        assert ctx is not None
        with st.spinner("Generation du dossier en cours..."):
            try:
                result = generate_dossier(ctx, output_dir, generate_pdf=generate_pdf)
                st.session_state.generated_dossier = result
            except Exception as exc:  # noqa: BLE001 - Streamlit must display failures.
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


def _ensure_business_session_defaults() -> None:
    if "business_docx_paths" not in st.session_state:
        st.session_state.business_docx_paths = []
    if "business_pdf_results" not in st.session_state:
        st.session_state.business_pdf_results = []
    if "business_pdf_error" not in st.session_state:
        st.session_state.business_pdf_error = None
    if "business_zip_path" not in st.session_state:
        st.session_state.business_zip_path = None
    if "business_output_dir" not in st.session_state:
        st.session_state.business_output_dir = None


def _business_docx_paths() -> list[Path]:
    return list(st.session_state.get("business_docx_paths", []))


def _business_pdf_paths() -> list[Path]:
    return [result.pdf_path for result in st.session_state.get("business_pdf_results", [])]


def _business_zip_path() -> Path | None:
    return st.session_state.get("business_zip_path")


def _business_output_dir(default: Path) -> Path:
    output_dir = st.session_state.get("business_output_dir")
    return output_dir if isinstance(output_dir, Path) else default


def _default_forme_affichage(structure: str) -> str:
    defaults = {
        "SCI": "Societe civile immobiliere",
        "SCS": "Societe civile de soins",
        "SCM": "Societe civile de moyens",
    }
    return defaults.get(structure, structure)


def _default_forme_longue(structure: str) -> str:
    defaults = {
        "SCI": "societe civile immobiliere",
        "SCS": "societe civile de soins",
        "SCM": "societe civile de moyens",
    }
    return defaults.get(structure, structure)


st.set_page_config(page_title="SYDEL Document Engine", layout="wide")

st.title("SYDEL Document Engine")
st.caption("Generation dossier DOCX, PDF local optionnel et ZIP.")

mode = st.radio(
    "Mode d'utilisation",
    ("Assistant metier", "Technique / diagnostic"),
    horizontal=True,
)

if mode == "Assistant metier":
    _render_business_mode()
else:
    _render_technical_mode()

st.caption(
    "La generation technique ne vaut pas validation juridique ni revue visuelle humaine. "
    "Les artefacts sont produits sous artifacts/ et restent hors versionnement."
)
