# ruff: noqa: E402

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import streamlit as st

from sydel_doc_engine.app.business_wizard import (
    BusinessAssociateInput,
    BusinessWizardInput,
    BusinessWizardValidation,
    business_document_table_rows,
    business_dossier_types,
    evaluate_business_wizard,
    selarl_ui_block_visibility,
    selarl_ui_condition_specs,
    selarl_ui_document_specs,
    selarl_ui_field,
    selarl_ui_reuse_projection,
    selarl_ui_reuse_rules,
    selarl_ui_visible_fields_by_block,
    selarl_ui_visible_fields_by_step,
    selarl_ui_visible_screen_title,
)
from sydel_doc_engine.app.front_dossier_editor import (
    front_dossier_editor_profile_labels,
    front_dossier_summary_rows,
)
from sydel_doc_engine.app.front_dossier_entry import (
    FrontDossierSimpleEntry,
    build_front_dossier_entry_view,
    front_dossier_entry_address_rows,
    front_dossier_entry_is_supported,
    front_dossier_entry_object_rows,
    front_dossier_entry_role_rows,
)
from sydel_doc_engine.app.front_generation_actions import (
    FRONT_GENERATION_ARTIFACTS_DIR,
    front_generation_document_rows,
    front_generation_readiness,
    front_generation_runtime_rows,
    generate_front_docx,
    generate_front_pdf,
    generate_front_zip,
)
from sydel_doc_engine.app.front_shell import (
    PROTOTYPE_TOOL_LABELS,
)
from sydel_doc_engine.app.single_document_mode import (
    UNIT_STATUS_GENERABLE_WITH_RESERVE,
    UNIT_STATUS_MANUAL_ONLY,
    UNIT_STATUS_NEEDS_MAPPING,
    UNIT_STATUS_NOT_IMPLEMENTED,
    UNIT_STATUS_NOT_SUPPORTED,
    UNIT_STATUS_SUPPORTED,
    SingleDocumentAssociateInput,
    SingleDocumentChoice,
    SingleDocumentFieldSpec,
    SingleDocumentInput,
    build_single_document_context,
    build_single_document_unit_plan,
    emprunt_field_specs_for_doc_004,
    field_specs_for_document,
    sample_single_document_input,
    single_document_choices,
    single_document_requirement_rows,
    single_document_table_rows,
    validate_single_document_input,
)
from sydel_doc_engine.app.test_prefill_presets import (
    business_test_prefill_by_label,
    business_test_prefill_labels,
    business_test_prefill_widget_keys,
)
from sydel_doc_engine.app.ui_runtime import (
    DEFAULT_ARTIFACTS_DIR,
    GeneratedDossier,
    build_output_dir,
    generate_docx_files_for_document_codes,
    generate_dossier,
    generate_pdf_files,
    generate_zip_file,
    list_context_examples,
    load_context_payload,
    parse_context_payload,
    selected_document_rows,
)
from sydel_doc_engine.rendering.pdf_export import is_pdf_export_available

BUSINESS_ARTIFACTS_DIR = Path("artifacts") / "ui_case_wizard_002"
SINGLE_DOCUMENT_ARTIFACTS_DIR = Path("artifacts") / "document_unitaire_001"
GENDER_OPTIONS = ("masculin", "feminin")
BUSINESS_STRUCTURE_OVERRIDE_KEY = "business_structure_override"
BUSINESS_STRUCTURE_WIDGET_KEY = "business_structure_type"
INTERNAL_DEBUG_LABEL = "Debug interne"
INTERNAL_TOOL_LABELS = (*PROTOTYPE_TOOL_LABELS, INTERNAL_DEBUG_LABEL)
INTERNAL_TOOLS_ENV_VAR = "SYDEL_ENABLE_INTERNAL_TOOLS"
INTERNAL_TOOLS_SESSION_FLAG = "_sydel_internal_tools_unlocked"


@st.cache_data(show_spinner=False)
def _pdf_backend_available() -> bool:
    return is_pdf_export_available()


def _internal_tools_available() -> bool:
    env_value = os.environ.get(INTERNAL_TOOLS_ENV_VAR, "")
    return env_value.strip().lower() in {"1", "true", "yes", "on"} or bool(
        st.session_state.get(INTERNAL_TOOLS_SESSION_FLAG)
    )


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


def _render_business_prefill_controls() -> None:
    labels = business_test_prefill_labels()
    selected_label = st.selectbox(
        "Scénario de test",
        labels,
        key="business_prefill_scenario",
        help="Charge uniquement des données fictives déterministes pour tester l'Assistant métier.",
    )
    preset = business_test_prefill_by_label(selected_label)
    st.caption(preset.description)
    col_prefill, col_reset = st.columns(2)
    with col_prefill:
        if st.button("Préremplir", key="business_prefill_apply"):
            _clear_business_assistant_state()
            st.session_state[BUSINESS_STRUCTURE_OVERRIDE_KEY] = preset.case_type
            for key, value in preset.widget_values.items():
                st.session_state[key] = value
            st.session_state.business_prefill_loaded = True
            st.session_state.business_prefill_label = preset.label
    with col_reset:
        if st.button("Réinitialiser", key="business_prefill_reset"):
            _clear_business_assistant_state()
            st.session_state.business_prefill_loaded = False
            st.session_state.business_prefill_label = ""

    if st.session_state.get("business_prefill_loaded"):
        label = st.session_state.get("business_prefill_label", selected_label)
        st.info(f"Mode test — données fictives préremplies : {label}")


def _clear_business_assistant_state() -> None:
    for key in (
        BUSINESS_STRUCTURE_WIDGET_KEY,
        BUSINESS_STRUCTURE_OVERRIDE_KEY,
        *business_test_prefill_widget_keys(),
    ):
        st.session_state.pop(key, None)
    _clear_business_generated_outputs()


def _clear_business_generated_outputs() -> None:
    for key in (
        "business_docx_paths",
        "business_pdf_results",
        "business_pdf_error",
        "business_zip_path",
        "business_output_dir",
    ):
        st.session_state.pop(key, None)


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


def _render_target_front_shell() -> None:
    _render_target_front_dossier()


def _render_target_front_dossier() -> None:
    st.subheader("Type de dossier")
    profile_options = tuple(
        label
        for label in front_dossier_editor_profile_labels()
        if front_dossier_entry_is_supported(label)
    )
    profile_label = st.selectbox(
        "Type de dossier / structure de base",
        profile_options,
        key="front_dossier_editor_profile",
    )

    st.subheader("Donnees a saisir")
    entry = _render_front_dossier_simple_entry(profile_label)
    view = build_front_dossier_entry_view(entry)
    _render_front_generation_actions(view.dossier)


def _render_front_dossier_simple_entry(profile_label: str) -> FrontDossierSimpleEntry:
    dossier_unipersonnel = st.checkbox(
        "Dossier unipersonnel",
        value=True,
        key="front_entry_dossier_unipersonnel",
    )

    st.markdown("Personne principale")
    col_identity_left, col_identity_right = st.columns(2)
    civilite_affichage = col_identity_left.selectbox(
        "Civilite",
        ("", "Madame", "Monsieur"),
        key="front_entry_person_civilite",
    )
    genre = col_identity_right.selectbox(
        "Genre grammatical",
        ("", "feminin", "masculin"),
        key="front_entry_person_genre",
    )
    prenom = col_identity_left.text_input(
        "Prenom",
        key="front_entry_person_prenom",
    )
    nom = col_identity_right.text_input("Nom", key="front_entry_person_nom")
    date_naissance = col_identity_left.text_input(
        "Date de naissance (AAAA-MM-JJ)",
        key="front_entry_person_date_naissance",
        placeholder="1980-01-01",
    )
    ville_naissance = col_identity_right.text_input(
        "Ville de naissance",
        key="front_entry_person_ville_naissance",
    )
    departement_naissance = col_identity_left.text_input(
        "Departement de naissance",
        key="front_entry_person_departement_naissance",
    )
    nationalite = col_identity_right.text_input(
        "Nationalite",
        key="front_entry_person_nationalite",
    )
    nom_pere = col_identity_left.text_input(
        "Nom du pere",
        key="front_entry_person_nom_pere",
    )
    nom_mere = col_identity_right.text_input(
        "Nom de la mere",
        key="front_entry_person_nom_mere",
    )
    adresse_personnelle = st.text_input(
        "Adresse personnelle",
        key="front_entry_person_adresse_personnelle",
        help="Format attendu : 12 rue Exemple, 75001 Paris.",
        placeholder="12 rue Exemple, 75001 Paris",
    )

    st.markdown("Societe principale")
    col_company_left, col_company_right = st.columns(2)
    societe_denomination = col_company_left.text_input(
        "Denomination",
        key="front_entry_company_denomination",
    )
    societe_forme_sociale = col_company_right.selectbox(
        "Forme sociale",
        ("SELARL", "SELAS", "SCM", "SCI"),
        key="front_entry_company_forme_sociale",
    )
    societe_capital_social = col_company_left.text_input(
        "Capital social",
        key="front_entry_company_capital_social",
    )
    societe_ville_rcs = col_company_right.text_input(
        "Ville RCS",
        key="front_entry_company_ville_rcs",
    )
    siege_social = col_company_right.text_input(
        "Siege social",
        key="front_entry_company_siege_social",
        help="Format attendu : 12 rue Exemple, 75001 Paris.",
        placeholder="12 rue Exemple, 75001 Paris",
    )
    domiciliation_same_as_siege = st.checkbox(
        "Domiciliation = siege social",
        value=True,
        key="front_entry_domiciliation_same_as_siege",
    )
    domiciliation = ""
    if not domiciliation_same_as_siege:
        domiciliation = st.text_input(
            "Adresse de domiciliation",
            key="front_entry_company_domiciliation",
            help="Format attendu : 12 rue Exemple, 75001 Paris.",
            placeholder="12 rue Exemple, 75001 Paris",
        )

    st.markdown("Capital, decision et signature")
    col_capital_left, col_capital_right = st.columns(2)
    capital_titres_nombre_total = col_capital_left.text_input(
        "Nombre total de titres",
        key="front_entry_capital_titres_nombre_total",
    )
    capital_titres_valeur_nominale = col_capital_right.text_input(
        "Valeur nominale",
        key="front_entry_capital_titres_valeur_nominale",
    )
    capital_repartition_associes = st.text_input(
        "Repartition des associes",
        key="front_entry_capital_repartition_associes",
        help=(
            "Optionnel en dossier unipersonnel : une repartition simple peut "
            "etre deduite depuis la personne et le nombre de titres."
        ),
    )
    decision_date = col_capital_left.text_input(
        "Date de decision (AAAA-MM-JJ)",
        key="front_entry_decision_date",
        placeholder="2026-05-24",
    )
    reunion_date_lettres = col_capital_right.text_input(
        "Date de reunion en lettres",
        key="front_entry_reunion_date_lettres",
    )
    reunion_heure = col_capital_left.text_input(
        "Heure de reunion",
        key="front_entry_reunion_heure",
    )
    signature_lieu = col_capital_right.text_input(
        "Lieu de signature",
        key="front_entry_signature_lieu",
    )
    signature_date = col_capital_left.text_input(
        "Date de signature (AAAA-MM-JJ)",
        key="front_entry_signature_date",
        placeholder="2026-05-24",
    )
    signature_nombre_exemplaires = col_capital_right.text_input(
        "Nombre d'exemplaires",
        key="front_entry_signature_nombre_exemplaires",
    )

    return FrontDossierSimpleEntry(
        profile_key=profile_label,
        dossier_unipersonnel=dossier_unipersonnel,
        domiciliation_same_as_siege=domiciliation_same_as_siege,
        civilite_affichage=civilite_affichage,
        genre=genre,
        prenom=prenom,
        nom=nom,
        date_naissance=date_naissance,
        ville_naissance=ville_naissance,
        departement_naissance=departement_naissance,
        nationalite=nationalite,
        nom_pere=nom_pere,
        nom_mere=nom_mere,
        adresse_personnelle=adresse_personnelle,
        societe_denomination=societe_denomination,
        societe_forme_sociale=societe_forme_sociale,
        societe_capital_social=societe_capital_social,
        societe_ville_rcs=societe_ville_rcs,
        siege_social=siege_social,
        domiciliation=domiciliation,
        capital_titres_nombre_total=capital_titres_nombre_total,
        capital_titres_valeur_nominale=capital_titres_valeur_nominale,
        capital_repartition_associes=capital_repartition_associes,
        decision_date=decision_date,
        reunion_date_lettres=reunion_date_lettres,
        reunion_heure=reunion_heure,
        signature_lieu=signature_lieu,
        signature_date=signature_date,
        signature_nombre_exemplaires=signature_nombre_exemplaires,
    )


def _front_dossier_entry_from_session_state(profile_label: str) -> FrontDossierSimpleEntry:
    return FrontDossierSimpleEntry(
        profile_key=profile_label,
        dossier_unipersonnel=bool(
            st.session_state.get("front_entry_dossier_unipersonnel", True)
        ),
        domiciliation_same_as_siege=bool(
            st.session_state.get("front_entry_domiciliation_same_as_siege", True)
        ),
        civilite_affichage=str(st.session_state.get("front_entry_person_civilite", "") or ""),
        genre=str(st.session_state.get("front_entry_person_genre", "") or ""),
        prenom=str(st.session_state.get("front_entry_person_prenom", "") or ""),
        nom=str(st.session_state.get("front_entry_person_nom", "") or ""),
        date_naissance=str(
            st.session_state.get("front_entry_person_date_naissance", "") or ""
        ),
        ville_naissance=str(
            st.session_state.get("front_entry_person_ville_naissance", "") or ""
        ),
        departement_naissance=str(
            st.session_state.get("front_entry_person_departement_naissance", "") or ""
        ),
        nationalite=str(st.session_state.get("front_entry_person_nationalite", "") or ""),
        nom_pere=str(st.session_state.get("front_entry_person_nom_pere", "") or ""),
        nom_mere=str(st.session_state.get("front_entry_person_nom_mere", "") or ""),
        adresse_personnelle=str(
            st.session_state.get("front_entry_person_adresse_personnelle", "") or ""
        ),
        societe_denomination=str(
            st.session_state.get("front_entry_company_denomination", "") or ""
        ),
        societe_forme_sociale=str(
            st.session_state.get("front_entry_company_forme_sociale", "SELARL")
            or "SELARL"
        ),
        societe_capital_social=str(
            st.session_state.get("front_entry_company_capital_social", "") or ""
        ),
        societe_ville_rcs=str(
            st.session_state.get("front_entry_company_ville_rcs", "") or ""
        ),
        siege_social=str(st.session_state.get("front_entry_company_siege_social", "") or ""),
        domiciliation=str(
            st.session_state.get("front_entry_company_domiciliation", "") or ""
        ),
        capital_titres_nombre_total=str(
            st.session_state.get("front_entry_capital_titres_nombre_total", "") or ""
        ),
        capital_titres_valeur_nominale=str(
            st.session_state.get("front_entry_capital_titres_valeur_nominale", "") or ""
        ),
        capital_repartition_associes=str(
            st.session_state.get("front_entry_capital_repartition_associes", "") or ""
        ),
        decision_date=str(st.session_state.get("front_entry_decision_date", "") or ""),
        reunion_date_lettres=str(
            st.session_state.get("front_entry_reunion_date_lettres", "") or ""
        ),
        reunion_heure=str(st.session_state.get("front_entry_reunion_heure", "") or ""),
        signature_lieu=str(st.session_state.get("front_entry_signature_lieu", "") or ""),
        signature_date=str(st.session_state.get("front_entry_signature_date", "") or ""),
        signature_nombre_exemplaires=str(
            st.session_state.get("front_entry_signature_nombre_exemplaires", "") or ""
        ),
    )


def _front_generation_blocker_messages(readiness) -> tuple[str, ...]:
    messages = list(readiness.runtime_blockers)
    if not messages:
        for document in readiness.summary.documents:
            if document.is_generable:
                continue
            messages.extend(
                _front_generation_reason_message(reason)
                for reason in document.why_not_generable()
            )

    unique_messages: list[str] = []
    for message in messages:
        normalized = message.strip()
        if normalized and normalized not in unique_messages:
            unique_messages.append(normalized)
    return tuple(unique_messages)


def _front_generation_reason_message(reason) -> str:
    reason_type = getattr(reason.reason_type, "value", str(reason.reason_type))
    if reason_type == "missing_role" and reason.role is not None:
        role_label = getattr(reason.role, "value", str(reason.role))
        return f"Role manquant : {role_label}."
    if reason_type == "missing_typed_address" and reason.address_usage is not None:
        address_label = getattr(reason.address_usage, "value", str(reason.address_usage))
        return f"Adresse manquante : {address_label}."
    if reason_type == "missing_canonical_value" and reason.field_path is not None:
        return f"Champ manquant : {reason.field_path}."
    if reason_type == "unresolved_ambiguity" and reason.ambiguity_key is not None:
        return f"Ambiguite a lever : {reason.ambiguity_key}."
    return reason.message


def _render_front_generation_actions(dossier) -> None:
    st.subheader("Generation")
    readiness = front_generation_readiness(dossier)
    st.caption(
        "Pilote actuel : DOC-001 a DOC-004 en DOCX puis ZIP. "
        "Les documents reserves ou manuels restent hors generation V1."
    )
    ready_col, blocked_col = st.columns(2)
    ready_col.metric("Prets a generer", len(readiness.generable_doc_codes))
    blocked_col.metric(
        "Bloques",
        len(readiness.blocked_doc_codes) + len(readiness.runtime_blockers),
    )

    if readiness.can_generate_docx:
        st.success("Les quatre documents V1 sont prets pour generation DOCX.")
    else:
        st.warning(
            "Generation bloquee tant que tous les documents V1 ne sont pas "
            "generables et que le contexte moteur minimal n'est pas complet."
        )
        blocker_messages = _front_generation_blocker_messages(readiness)
        if blocker_messages:
            displayed_messages = blocker_messages[:5]
            st.markdown(
                "Blocages a corriger :\n"
                + "\n".join(f"- {message}" for message in displayed_messages)
            )
            remaining_count = len(blocker_messages) - len(displayed_messages)
            if remaining_count > 0:
                st.caption(
                    f"{remaining_count} autre(s) blocage(s) seront verifies apres saisie."
                )

    output_dir = build_output_dir(
        "nouveau_front_selarl_creation_simple.yaml",
        FRONT_GENERATION_ARTIFACTS_DIR,
    )

    _ensure_front_generation_session_defaults()
    docx_paths = _front_generation_docx_paths()
    pdf_paths = _front_generation_pdf_paths()
    zip_path = _front_generation_zip_path()
    pdf_available = _pdf_backend_available()

    generation_columns = st.columns(3 if pdf_available else 2)
    docx_col, zip_col = generation_columns[:2]
    with docx_col:
        if st.button(
            "Generer les DOCX",
            type="primary",
            key="front_generation_generate_docx",
            disabled=not readiness.can_generate_docx,
        ):
            with st.spinner("Generation DOCX depuis le nouveau front..."):
                try:
                    result = generate_front_docx(dossier, output_dir)
                    docx_paths = list(result.docx_paths)
                    st.session_state.front_generation_docx_paths = docx_paths
                    st.session_state.front_generation_pdf_results = []
                    st.session_state.front_generation_pdf_error = None
                    st.session_state.front_generation_zip_path = None
                    st.session_state.front_generation_output_dir = result.output_dir
                    st.success(f"{len(docx_paths)} DOCX generes depuis le nouveau front.")
                except Exception as exc:  # noqa: BLE001 - Streamlit displays the failure.
                    st.error(f"Generation DOCX bloquee : {exc}")
    with zip_col:
        if st.button(
            "Generer le ZIP",
            key="front_generation_generate_zip",
            disabled=not docx_paths,
        ):
            with st.spinner("Creation du ZIP depuis le nouveau front..."):
                try:
                    active_output_dir = _front_generation_output_dir(output_dir)
                    zip_path = generate_front_zip(active_output_dir, docx_paths, pdf_paths)
                    st.session_state.front_generation_zip_path = zip_path
                    st.success("ZIP nouveau front genere avec manifest.")
                except Exception as exc:  # noqa: BLE001 - Streamlit displays the failure.
                    st.error(f"Generation ZIP bloquee : {exc}")
    if pdf_available:
        pdf_col = generation_columns[2]
        with pdf_col:
            if st.button(
                "Generer les PDF",
                key="front_generation_generate_pdf",
                disabled=not docx_paths,
            ):
                with st.spinner("Conversion PDF depuis le nouveau front..."):
                    active_output_dir = _front_generation_output_dir(output_dir)
                    pdf_batch = generate_front_pdf(active_output_dir, docx_paths)
                    st.session_state.front_generation_pdf_results = pdf_batch.pdf_results
                    st.session_state.front_generation_pdf_error = pdf_batch.pdf_error
                    if pdf_batch.pdf_error:
                        st.warning(f"PDF non produits : {pdf_batch.pdf_error}")
                    else:
                        st.success(f"{len(pdf_batch.pdf_paths)} PDF generes.")

    docx_paths = _front_generation_docx_paths()
    pdf_paths = _front_generation_pdf_paths()
    zip_path = _front_generation_zip_path()
    if docx_paths or pdf_paths or zip_path is not None:
        st.subheader("Telechargements")
    if docx_paths:
        _render_docx_downloads(docx_paths, key_prefix="front-generation")
    if pdf_paths:
        _render_pdf_downloads(pdf_paths, key_prefix="front-generation")
    if zip_path is not None:
        _download_file(
            zip_path,
            label="Telecharger le ZIP nouveau front",
            mime="application/zip",
            key=f"download-front-generation-zip-{zip_path.name}",
        )


def _ensure_front_generation_session_defaults() -> None:
    st.session_state.setdefault("front_generation_docx_paths", [])
    st.session_state.setdefault("front_generation_pdf_results", [])
    st.session_state.setdefault("front_generation_pdf_error", None)
    st.session_state.setdefault("front_generation_zip_path", None)
    st.session_state.setdefault("front_generation_output_dir", None)


def _front_generation_docx_paths() -> list[Path]:
    return list(st.session_state.get("front_generation_docx_paths") or [])


def _front_generation_pdf_paths() -> list[Path]:
    return [
        result.pdf_path
        for result in st.session_state.get("front_generation_pdf_results") or []
    ]


def _front_generation_zip_path() -> Path | None:
    return st.session_state.get("front_generation_zip_path")


def _front_generation_output_dir(default: Path) -> Path:
    return st.session_state.get("front_generation_output_dir") or default


def _render_internal_tools_shell(tool: str) -> None:
    st.subheader("Outils internes")
    if tool == "Assistant metier prototype":
        st.warning(
            "Assistant metier conserve comme bac a sable historique. "
            "Le futur editeur dossier sera reconstruit depuis front_data."
        )
        _render_business_mode()
    elif tool == "Document unitaire":
        st.warning(
            "Mode de test separe du parcours dossier complet. Il reste utile "
            "pour verifier un document isole."
        )
        _render_single_document_mode()
    elif tool == "Technique / diagnostic":
        st.warning(
            "Diagnostic technique reserve aux contextes YAML/JSON et aux "
            "verifications moteur."
        )
        _render_technical_mode()
    else:
        _render_internal_debug()


def _render_internal_debug() -> None:
    st.warning("Debug interne reserve a l'equipe projet.")
    profile_label = str(
        st.session_state.get(
            "front_dossier_editor_profile",
            front_dossier_editor_profile_labels()[0],
        )
    )
    entry = _front_dossier_entry_from_session_state(profile_label)
    view = build_front_dossier_entry_view(entry)
    readiness = front_generation_readiness(view.dossier)
    st.caption("DossierRecord")
    st.table(front_dossier_summary_rows(view))
    st.caption("Objets data")
    st.table(front_dossier_entry_object_rows(view.dossier))
    st.caption("Roles")
    st.table(front_dossier_entry_role_rows(view.dossier))
    st.caption("Adresses")
    st.table(front_dossier_entry_address_rows(view.dossier))
    st.caption("Statuts generation")
    st.table(front_generation_document_rows(readiness))
    st.caption("Garde-fous")
    st.table(front_generation_runtime_rows(readiness))


def _render_business_mode() -> None:
    st.subheader("Mode Assistant metier")
    _render_business_prefill_controls()
    data = _collect_business_input()
    validation = evaluate_business_wizard(data)

    if data.structure == "SELARL":
        st.subheader(selarl_ui_visible_screen_title("documents_generation"))
    else:
        st.subheader("Etape 3 - Documents attendus")
    document_rows = business_document_table_rows(validation)
    if document_rows:
        st.table(document_rows)
    else:
        st.warning("Aucun document cible pour ce type de dossier.")
    if data.structure == "SELARL":
        _render_selarl_document_summary(validation)

    st.subheader("Etape 4 - Validation" if data.structure != "SELARL" else "Validation")
    col_generable, col_blocked = st.columns(2)
    col_generable.metric("Documents prets", validation.generable_count)
    col_blocked.metric("Documents non prets ou exclus", validation.blocked_count)
    if validation.missing_fields:
        st.warning("Champs manquants : " + ", ".join(validation.missing_fields))
    if validation.inconsistencies:
        st.error("Incoherences : " + " ; ".join(validation.inconsistencies))
    for warning in validation.warnings:
        st.info(warning)

    st.subheader("Etape 5 - Generation" if data.structure != "SELARL" else "Génération")
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
                    docx_paths = generate_docx_files_for_document_codes(
                        validation.context,
                        output_dir,
                        validation.generatable_document_codes,
                    )
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

    st.subheader("Etape 6 - Telechargement" if data.structure != "SELARL" else "Telechargement")
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


def _render_single_document_mode() -> None:
    st.subheader("Mode Document unitaire")
    st.caption(
        "Mode de test limite : il selectionne un document attendu par le catalogue "
        "et ne genere que les documents explicitement couverts par le formulaire V1."
    )

    dossier_types = business_dossier_types()
    selected_type = st.selectbox(
        "Structure / cas de test",
        dossier_types,
        format_func=lambda item: item.label,
        key="single_document_structure",
    )
    st.caption(
        "La structure sert a lister les documents attendus et a appliquer les "
        "conditions de selection documentaire."
    )
    conditions = _collect_case_conditions(selected_type.structure)
    choices = single_document_choices(selected_type.structure, conditions)

    if choices:
        st.subheader("Documents disponibles pour ce cas")
        st.table(single_document_table_rows(choices))
    else:
        st.warning("Aucun document cible pour ce cas.")
        return

    selected_choice = st.selectbox(
        "Document a tester",
        choices,
        format_func=lambda choice: choice.display_label,
        key="single_document_choice",
    )
    _render_single_document_choice_status(selected_choice)
    if selected_choice.document_code is not None:
        st.subheader("Exigences data-layer")
        st.table(single_document_requirement_rows(selected_choice.document_code))
    if selected_choice.status != UNIT_STATUS_SUPPORTED or selected_choice.document_code is None:
        return

    selection_key = (selected_type.structure, selected_choice.identifier)
    _ensure_single_document_session_defaults(selection_key)

    use_examples = st.checkbox(
        "Pre-remplir avec des donnees d'exemple",
        value=False,
        key=f"single_document_examples_{selected_choice.identifier}",
    )
    data = _collect_single_document_input(
        selected_choice.document_code,
        selected_type.structure,
        use_examples,
    )
    missing_fields = validate_single_document_input(data)
    unit_plan = build_single_document_unit_plan(data)
    if missing_fields:
        st.warning("Champs manquants : " + ", ".join(missing_fields))
    elif not unit_plan.is_generation_allowed:
        st.warning(
            "Generation bloquee par la couche data : "
            + " ; ".join(unit_plan.explain_blockers())
        )
    else:
        st.success("Champs requis du document completés.")

    output_dir = build_output_dir(
        f"document_unitaire_{selected_choice.document_code}.yaml",
        SINGLE_DOCUMENT_ARTIFACTS_DIR,
    )
    st.text_input("Dossier de sortie", value=str(output_dir), disabled=True)

    pdf_available = _pdf_backend_available()
    if pdf_available:
        st.info("Backend PDF local disponible. La conversion reste dependante du poste.")
    else:
        st.warning("PDF local indisponible : DOCX et ZIP restent disponibles.")

    docx_paths = _single_document_docx_paths()
    pdf_paths = _single_document_pdf_paths()
    zip_path = _single_document_zip_path()

    docx_col, zip_col, pdf_col = st.columns(3)
    with docx_col:
        if st.button(
            "Generer le DOCX",
            type="primary",
            disabled=bool(missing_fields) or not unit_plan.is_generation_allowed,
        ):
            with st.spinner("Generation DOCX en cours..."):
                try:
                    ctx = build_single_document_context(data)
                    docx_paths = generate_docx_files_for_document_codes(
                        ctx,
                        output_dir,
                        (selected_choice.document_code,),
                    )
                    st.session_state.single_document_docx_paths = docx_paths
                    st.session_state.single_document_pdf_results = []
                    st.session_state.single_document_pdf_error = None
                    st.session_state.single_document_zip_path = None
                    st.session_state.single_document_output_dir = output_dir
                    st.success(f"{len(docx_paths)} DOCX genere.")
                except Exception as exc:  # noqa: BLE001 - Streamlit displays the failure.
                    st.error(f"Generation DOCX bloquee : {exc}")
    with zip_col:
        if st.button("Generer le ZIP", disabled=not docx_paths):
            with st.spinner("Creation du ZIP en cours..."):
                try:
                    active_output_dir = _single_document_output_dir(output_dir)
                    zip_path = generate_zip_file(active_output_dir, docx_paths, pdf_paths)
                    st.session_state.single_document_zip_path = zip_path
                    st.success("ZIP document genere avec manifest.")
                except Exception as exc:  # noqa: BLE001 - Streamlit displays the failure.
                    st.error(f"Generation ZIP bloquee : {exc}")
    with pdf_col:
        if st.button(
            "Generer le PDF",
            disabled=not (pdf_available and docx_paths),
        ):
            with st.spinner("Conversion PDF en cours..."):
                active_output_dir = _single_document_output_dir(output_dir)
                pdf_batch = generate_pdf_files(docx_paths, active_output_dir)
                st.session_state.single_document_pdf_results = pdf_batch.pdf_results
                st.session_state.single_document_pdf_error = pdf_batch.pdf_error
                if pdf_batch.pdf_error:
                    st.warning(f"PDF non produit : {pdf_batch.pdf_error}")
                else:
                    st.success(f"{len(pdf_batch.pdf_paths)} PDF genere.")

    st.subheader("Telechargement")
    docx_paths = _single_document_docx_paths()
    pdf_paths = _single_document_pdf_paths()
    zip_path = _single_document_zip_path()
    if docx_paths:
        _render_docx_downloads(docx_paths, key_prefix="single-document")
    if pdf_paths:
        _render_pdf_downloads(pdf_paths, key_prefix="single-document")
    if zip_path is not None:
        _download_file(
            zip_path,
            label="Telecharger le ZIP document",
            mime="application/zip",
            key=f"download-single-document-zip-{zip_path.name}",
        )
    if not docx_paths and zip_path is None:
        st.caption("Aucune sortie generee pour le moment.")


def _render_single_document_choice_status(choice: SingleDocumentChoice) -> None:
    if choice.status == UNIT_STATUS_SUPPORTED:
        st.success("Document supporte dans ce mode : seuls ses champs requis sont affiches.")
        return
    if choice.status == UNIT_STATUS_MANUAL_ONLY:
        st.warning(
            "Document affiche par le catalogue, mais a remplir manuellement : "
            "aucune generation automatique dans ce mode."
        )
        return
    if choice.status == UNIT_STATUS_NOT_IMPLEMENTED:
        st.warning("Document non implemente dans le moteur : generation impossible.")
        return
    if choice.status == UNIT_STATUS_NEEDS_MAPPING:
        st.warning("Document sans mapping DOC-XXX confirme : generation impossible.")
        return
    if choice.status == UNIT_STATUS_GENERABLE_WITH_RESERVE:
        st.warning(
            "Document visible avec reserve documentaire : non ouvert a la generation "
            "dans le perimetre unitaire V1."
        )
        return
    if choice.status == UNIT_STATUS_NOT_SUPPORTED:
        st.info("Document pas encore supporte dans ce mode unitaire.")


def _collect_single_document_input(
    document_code: str,
    structure: str,
    use_examples: bool,
) -> SingleDocumentInput:
    sample = sample_single_document_input(document_code, structure=structure)
    values: dict[str, object] = {
        "structure": structure,
        "document_code": document_code,
    }
    for group, specs in _single_document_field_groups(
        field_specs_for_document(document_code)
    ).items():
        with st.expander(group, expanded=True):
            for spec in specs:
                values[spec.key] = _render_single_document_field(
                    spec,
                    sample,
                    document_code,
                    use_examples,
                )

    associes: tuple[SingleDocumentAssociateInput, ...] = ()
    if document_code == "DOC-004":
        with st.expander("Associes", expanded=True):
            associe_count = st.number_input(
                "Nombre d'associes",
                min_value=1,
                max_value=4,
                value=len(sample.associes) if use_examples else 1,
                key="single_document_doc_004_associe_count",
            )
            associes = _collect_single_document_associes(
                int(associe_count),
                sample,
                use_examples,
            )
        if bool(values.get("emprunt_actif")):
            with st.expander("Bien finance", expanded=True):
                for spec in emprunt_field_specs_for_doc_004():
                    values[spec.key] = _render_single_document_field(
                        spec,
                        sample,
                        document_code,
                        use_examples,
                    )

    return SingleDocumentInput(**values, associes=associes)


def _single_document_field_groups(
    fields: tuple[SingleDocumentFieldSpec, ...],
) -> dict[str, tuple[SingleDocumentFieldSpec, ...]]:
    grouped: dict[str, list[SingleDocumentFieldSpec]] = {}
    for field in fields:
        grouped.setdefault(field.group, []).append(field)
    return {group: tuple(items) for group, items in grouped.items()}


def _render_single_document_field(
    spec: SingleDocumentFieldSpec,
    sample: SingleDocumentInput,
    document_code: str,
    use_examples: bool,
) -> object:
    key = f"single_document_{document_code}_{spec.key}"
    initial = getattr(sample, spec.key) if use_examples else _empty_unit_value(spec)
    if spec.kind == "choice":
        options = ("", *spec.choices)
        initial_value = str(initial) if initial else ""
        return st.selectbox(
            spec.label,
            options,
            index=_selectbox_index(options, initial_value),
            format_func=lambda value: value or "Choisir",
            key=key,
            help=spec.help_text or None,
        )
    if spec.kind == "bool":
        return st.checkbox(
            spec.label,
            value=bool(initial),
            key=key,
            help=spec.help_text or None,
        )
    if spec.kind == "int":
        int_value = int(initial) if isinstance(initial, int) and initial > 0 else 0
        value = st.number_input(
            spec.label,
            min_value=0,
            value=int_value,
            key=key,
            help=spec.help_text or None,
        )
        return int(value) if value > 0 else None
    return st.text_input(
        spec.label,
        value=_display_unit_value(initial),
        key=key,
        help=spec.help_text or None,
    )


def _collect_single_document_associes(
    count: int,
    sample: SingleDocumentInput,
    use_examples: bool,
) -> tuple[SingleDocumentAssociateInput, ...]:
    associes: list[SingleDocumentAssociateInput] = []
    for index in range(count):
        example = sample.associes[index] if use_examples and index < len(sample.associes) else None
        st.markdown(f"Associe {index + 1}")
        cols = st.columns(5)
        genre = cols[0].selectbox(
            f"Associe {index + 1} - genre grammatical",
            GENDER_OPTIONS,
            index=_selectbox_index(GENDER_OPTIONS, example.genre if example else GENDER_OPTIONS[0]),
            key=f"single_document_associe_genre_{index}",
        )
        civilite = cols[1].selectbox(
            f"Associe {index + 1} - civilite",
            ("", "Monsieur", "Madame"),
            index=_selectbox_index(
                ("", "Monsieur", "Madame"),
                example.civilite_affichage if example else "",
            ),
            key=f"single_document_associe_civilite_{index}",
            format_func=lambda value: value or "Choisir",
        )
        prenom = cols[2].text_input(
            f"Associe {index + 1} - prenom",
            value=example.prenom if example else "",
            key=f"single_document_associe_prenom_{index}",
        )
        nom = cols[3].text_input(
            f"Associe {index + 1} - nom",
            value=example.nom if example else "",
            key=f"single_document_associe_nom_{index}",
        )
        nb_parts_input = cols[4].number_input(
            f"Associe {index + 1} - parts",
            min_value=0,
            value=example.nb_parts if example and example.nb_parts else 0,
            key=f"single_document_associe_parts_{index}",
        )
        present = st.checkbox(
            f"Associe {index + 1} present ou represente",
            value=example.est_present_ou_represente if example else True,
            key=f"single_document_associe_present_{index}",
        )
        associes.append(
            SingleDocumentAssociateInput(
                genre=genre,
                civilite_affichage=civilite,
                prenom=prenom,
                nom=nom,
                nb_parts=int(nb_parts_input) if nb_parts_input > 0 else None,
                est_present_ou_represente=present,
            )
        )
    return tuple(associes)


def _empty_unit_value(spec: SingleDocumentFieldSpec) -> object:
    if spec.kind == "bool":
        return False
    if spec.kind == "int":
        return 0
    if spec.kind == "choice":
        return ""
    return ""


def _display_unit_value(value: object) -> str:
    if isinstance(value, date):
        return value.isoformat()
    return "" if value is None else str(value)


def _selectbox_index(options: tuple[str, ...], value: str) -> int:
    return options.index(value) if value in options else 0


def _render_selarl_document_summary(validation: BusinessWizardValidation) -> None:
    generable = [row.doc_id for row in validation.document_rows if row.status == "generable"]
    manual = [row.doc_id for row in validation.document_rows if row.status == "manual_only"]
    reserved = [
        row.doc_id
        for row in validation.document_rows
        if any("reserve" in note.casefold() or "vraie v2" in note.casefold() for note in row.notes)
    ]
    excluded = [row.doc_id for row in validation.document_rows if row.status != "generable"]
    with st.expander("Synthese SELARL des statuts documentaires", expanded=True):
        st.caption(
            "Liste calculee depuis le catalogue et les specs SELARL "
            f"({len(selarl_ui_document_specs())} documents pilotes)."
        )
        st.markdown("Documents generables prets : " + (", ".join(generable) or "aucun"))
        st.markdown("Documents manuels visibles : " + (", ".join(manual) or "aucun"))
        st.markdown("Documents avec reserve source : " + (", ".join(reserved) or "aucun"))
        st.markdown(
            "Documents exclus ou incomplets pour la generation pilote : "
            + (", ".join(excluded) or "aucun")
        )
        st.caption(
            "DOC-013 et DOC-014 restent visibles si la derogation est active, "
            "mais ne sont jamais envoyes a la generation automatique SELARL."
        )


def _collect_case_conditions(case_type: str) -> dict[str, object | None]:
    conditions: dict[str, object | None] = {
        "profession": None,
        "sci_iris": None,
        "option_is": None,
        "site_distinct": None,
        "scm": None,
        "scm_cession": None,
        "regime_communautaire": None,
        "derogation": None,
        "cession": None,
        "cabinet_type": None,
        "associe_unique": None,
        "cession_actions": None,
        "dossier_unipersonnel": None,
    }
    with st.expander("Conditions metier de selection documentaire", expanded=True):
        if case_type == "SCI":
            variant = st.selectbox(
                "SCI simple ou SCI IRIS",
                ("", "SCI simple", "SCI IRIS"),
                key="condition_sci_variant",
                format_func=lambda value: value or "Choisir",
            )
            conditions["sci_iris"] = None if not variant else variant == "SCI IRIS"
            conditions["option_is"] = _select_bool("Option IS", key="condition_option_is")
        elif case_type == "SELARL":
            condition_specs = {spec.key: spec for spec in selarl_ui_condition_specs()}
            conditions["profession"] = _select_choice(
                condition_specs["profession"].label,
                dict(condition_specs["profession"].choices),
                key="condition_selarl_profession",
            )
            conditions["site_distinct"] = _select_bool(
                condition_specs["site_distinct"].label,
                key="condition_selarl_site_distinct",
            )
            conditions["scm_cession"] = _select_bool(
                condition_specs["scm_cession"].label,
                key="condition_selarl_scm_cession",
            )
            conditions["regime_communautaire"] = _select_bool(
                condition_specs["regime_communautaire"].label,
                key="condition_selarl_regime_communautaire",
            )
            conditions["derogation"] = _select_bool(
                condition_specs["derogation"].label,
                key="condition_selarl_derogation",
            )
            conditions["cession"] = _select_bool(
                condition_specs["cession"].label,
                key="condition_selarl_cession",
            )
            if conditions["cession"] is True:
                conditions["cabinet_type"] = _select_choice(
                    condition_specs["cabinet_type"].label,
                    dict(condition_specs["cabinet_type"].choices),
                    key="condition_selarl_cabinet_type",
                )
            dossier_field = selarl_ui_field("qualification.dossier_unipersonnel")
            conditions["dossier_unipersonnel"] = st.checkbox(
                dossier_field.label,
                value=False,
                key="condition_selarl_dossier_unipersonnel",
                help=dossier_field.help_text,
            )
            if conditions["dossier_unipersonnel"] is True:
                st.info("Le Praticien est l’associé unique, le gérant et le signataire")
            for spec in condition_specs.values():
                if spec.note:
                    st.caption(f"{spec.label} : {spec.note}")
        elif case_type == "SELAS":
            conditions["profession"] = _select_choice(
                "Profession",
                {"medecin": "medecin"},
                key="condition_selas_profession",
            )
            conditions["scm"] = _select_bool("SCM", key="condition_selas_scm")
            conditions["regime_communautaire"] = _select_bool(
                "Regime communautaire",
                key="condition_selas_regime_communautaire",
            )
            conditions["derogation"] = _select_bool(
                "Derogation",
                key="condition_selas_derogation",
            )
            conditions["cession"] = _select_bool("Cession", key="condition_selas_cession")
            if conditions["cession"] is True:
                conditions["cabinet_type"] = _select_choice(
                    "Si cession : type de cabinet",
                    {
                        "aucun": "aucun",
                        "medical": "cabinet medical",
                        "dentaire": "cabinet dentaire",
                    },
                    key="condition_selas_cabinet_type",
                )
            if conditions["scm"] is True:
                st.info(
                    "Reserve SELAS + SCM : le catalogue expose DOC-031/DOC-032/DOC-033, "
                    "mais la variante SELAS reste a confirmer avant generation."
                )
        elif case_type == "SPFPL cession":
            conditions["regime_communautaire"] = _select_bool(
                "Regime communautaire",
                key="condition_spfpl_cession_regime_communautaire",
            )
            conditions["associe_unique"] = _select_bool(
                "Associe unique",
                key="condition_spfpl_cession_associe_unique",
            )
            cession_kind = st.selectbox(
                "Cession de parts ou cession d'actions",
                ("", "cession de parts", "cession d'actions"),
                format_func=lambda value: value or "Choisir",
            )
            if cession_kind:
                conditions["cession_actions"] = cession_kind == "cession d'actions"
        elif case_type == "SPFPL apport":
            conditions["regime_communautaire"] = _select_bool(
                "Regime communautaire",
                key="condition_spfpl_apport_regime_communautaire",
            )
        elif case_type == "SAS":
            conditions["associe_unique"] = _select_bool(
                "Associe unique",
                key="condition_sas_associe_unique",
            )
            st.caption(
                "Ce choix est collecte pour eviter une hypothese silencieuse ; "
                "le catalogue V1 ne filtre pas encore SAS dessus."
            )
        else:
            st.caption("Pas de condition metier specifique dans cette V1.")
    return conditions


def _select_bool(label: str, *, key: str) -> bool | None:
    selected = st.selectbox(
        label,
        ("", "Oui", "Non"),
        key=key,
        format_func=lambda value: value or "Choisir",
    )
    if not selected:
        return None
    return selected == "Oui"


def _select_choice(label: str, choices: dict[str, str], *, key: str) -> str | None:
    selected = st.selectbox(
        label,
        ("", *choices.keys()),
        key=key,
        format_func=lambda value: choices.get(value, "Choisir"),
    )
    return selected or None


def _collect_business_input() -> BusinessWizardInput:
    st.subheader("Type de dossier")
    dossier_types = business_dossier_types()
    _apply_business_structure_override(dossier_types)
    selected_type = st.selectbox(
        "Type de dossier metier",
        dossier_types,
        format_func=lambda item: item.label,
        key=BUSINESS_STRUCTURE_WIDGET_KEY,
    )
    st.caption(selected_type.status)
    if selected_type.structure == "SELARL":
        st.subheader(selarl_ui_visible_screen_title("qualification"))
    else:
        st.subheader("Etape 1 - Conditions")
    conditions = _collect_case_conditions(selected_type.structure)

    if selected_type.structure == "SELARL":
        return _collect_selarl_business_input(conditions)

    st.subheader("Etape 2 - Informations du dossier")
    with st.expander("Societe", expanded=True):
        societe_forme_sociale = st.text_input(
            "Forme sociale",
            value=selected_type.structure,
            key="business_societe_forme_sociale",
        )
        societe_forme_sociale_affichage = st.text_input(
            "Forme sociale affichee",
            value=_default_forme_affichage(selected_type.structure),
            key="business_societe_forme_sociale_affichage",
        )
        societe_forme_sociale_libelle_long = st.text_input(
            "Libelle long de forme sociale",
            value=_default_forme_longue(selected_type.structure),
            key="business_societe_forme_sociale_libelle_long",
        )
        societe_denomination = st.text_input(
            "Denomination",
            key="business_societe_denomination",
        )
        societe_capital_social = st.text_input(
            "Capital social",
            key="business_societe_capital_social",
        )
        societe_capital_variable = st.checkbox(
            "Capital variable",
            value=True,
            key="business_societe_capital_variable",
        )
        societe_ville_rcs = st.text_input("Ville RCS", key="business_societe_ville_rcs")
        st.markdown("Adresse du siege")
        siege_cols = st.columns(4)
        societe_siege_num_voie = siege_cols[0].text_input(
            "Numero",
            key="business_societe_num",
        )
        societe_siege_voie = siege_cols[1].text_input(
            "Voie",
            key="business_societe_voie",
        )
        societe_siege_cp = siege_cols[2].text_input(
            "Code postal",
            key="business_societe_cp",
        )
        societe_siege_ville = siege_cols[3].text_input(
            "Ville",
            key="business_societe_ville",
        )

    with st.expander("Associes / personnes physiques", expanded=True):
        personne_genre = st.selectbox(
            "Genre du signataire",
            GENDER_OPTIONS,
            key="business_personne_genre",
        )
        personne_civilite = st.selectbox(
            "Civilite du signataire",
            ("", "Monsieur", "Madame"),
            key="business_personne_civilite",
        )
        person_cols = st.columns(2)
        personne_prenom = person_cols[0].text_input(
            "Prenom du signataire",
            key="business_personne_prenom",
        )
        personne_nom = person_cols[1].text_input(
            "Nom du signataire",
            key="business_personne_nom",
        )
        personne_date_naissance = st.text_input(
            "Date de naissance signataire (AAAA-MM-JJ)",
            key="business_personne_date_naissance",
        )
        personne_nationalite = st.text_input(
            "Nationalite du signataire",
            key="business_personne_nationalite",
        )
        personne_nom_pere = st.text_input("Nom du pere", key="business_personne_nom_pere")
        personne_nom_mere = st.text_input("Nom de la mere", key="business_personne_nom_mere")
        personne_fonction_dirigeant = st.text_input(
            "Fonction du signataire",
            key="business_personne_fonction",
        )
        st.markdown("Adresse personnelle du signataire")
        personne_addr_cols = st.columns(4)
        personne_adresse_num_voie = personne_addr_cols[0].text_input(
            "Numero",
            key="business_personne_num",
        )
        personne_adresse_voie = personne_addr_cols[1].text_input(
            "Voie",
            key="business_personne_voie",
        )
        personne_adresse_cp = personne_addr_cols[2].text_input(
            "Code postal",
            key="business_personne_cp",
        )
        personne_adresse_ville = personne_addr_cols[3].text_input(
            "Ville",
            key="business_personne_ville",
        )

        associe_count = st.number_input(
            "Nombre d'associes",
            min_value=1,
            max_value=4,
            value=2,
            key="business_associe_count",
        )
        associes = _collect_associes(int(associe_count))

    with st.expander("Representant legal", expanded=True):
        dirigeant_genre = st.selectbox(
            "Genre du representant legal",
            GENDER_OPTIONS,
            key="business_dirigeant_genre",
        )
        dirigeant_civilite_affichage = st.selectbox(
            "Civilite du representant legal",
            ("", "Monsieur", "Madame"),
            key="business_dirigeant_civilite",
        )
        dirigeant_cols = st.columns(2)
        dirigeant_prenom = dirigeant_cols[0].text_input(
            "Prenom du representant legal",
            key="business_dirigeant_prenom",
        )
        dirigeant_nom = dirigeant_cols[1].text_input(
            "Nom du representant legal",
            key="business_dirigeant_nom",
        )
        dirigeant_date_naissance = st.text_input(
            "Date de naissance du representant legal (AAAA-MM-JJ)",
            key="business_dirigeant_date_naissance",
        )
        dirigeant_ville_naissance = st.text_input(
            "Ville de naissance du representant legal",
            key="business_dirigeant_ville_naissance",
        )
        dirigeant_departement_naissance = st.text_input(
            "Departement de naissance du representant legal",
            key="business_dirigeant_departement_naissance",
        )
        dirigeant_nationalite = st.text_input(
            "Nationalite du representant legal",
            key="business_dirigeant_nationalite",
        )
        dirigeant_fonction_affichage = st.text_input(
            "Fonction nommee",
            value="gerant",
            key="business_dirigeant_fonction",
        )
        st.markdown("Adresse personnelle du representant legal")
        dirigeant_addr_cols = st.columns(4)
        dirigeant_adresse_num_voie = dirigeant_addr_cols[0].text_input(
            "Numero",
            key="business_dirigeant_num",
        )
        dirigeant_adresse_voie = dirigeant_addr_cols[1].text_input(
            "Voie",
            key="business_dirigeant_voie",
        )
        dirigeant_adresse_cp = dirigeant_addr_cols[2].text_input(
            "Code postal",
            key="business_dirigeant_cp",
        )
        dirigeant_adresse_ville = dirigeant_addr_cols[3].text_input(
            "Ville",
            key="business_dirigeant_ville",
        )

    with st.expander("Adresse de domiciliation", expanded=True):
        domiciliation_adresse_affichee = st.text_input(
            "Adresse de domiciliation affichee",
            key="business_domiciliation_adresse_affichee",
        )

    with st.expander("Capital / parts", expanded=True):
        capital_cols = st.columns(2)
        capital_nb_parts_total_input = capital_cols[0].number_input(
            "Nombre total de parts",
            min_value=0,
            value=0,
            key="business_capital_nb_parts_total",
        )
        capital_valeur_nominale_part = capital_cols[1].text_input(
            "Valeur nominale par part",
            key="business_capital_valeur_nominale_part",
        )

    with st.expander("Dates", expanded=True):
        decision_date = st.text_input(
            "Date de decision (AAAA-MM-JJ ou libelle)",
            key="business_decision_date",
        )
        reunion_date_lettres = st.text_input(
            "Date de reunion en lettres",
            key="business_reunion_date_lettres",
        )
        reunion_heure = st.text_input("Heure de reunion", key="business_reunion_heure")
        signature_lieu = st.text_input("Lieu de signature", key="business_signature_lieu")
        signature_date = st.text_input(
            "Date de signature (AAAA-MM-JJ)",
            key="business_signature_date",
        )
        signature_nombre_exemplaires = st.text_input(
            "Nombre d'exemplaires",
            key="business_signature_nombre_exemplaires",
        )

    with st.expander("Options documentaires", expanded=False):
        emprunt_actif = st.checkbox(
            "PV avec autorisation d'emprunt",
            value=False,
            key="business_emprunt_actif",
        )
        emprunt_montant_max = ""
        bien_adresse_num_voie = ""
        bien_adresse_voie = ""
        bien_adresse_cp = ""
        bien_adresse_ville = ""
        if emprunt_actif:
            emprunt_montant_max = st.text_input(
                "Montant maximum de l'emprunt",
                key="business_emprunt_montant_max",
            )
            bien_cols = st.columns(4)
            bien_adresse_num_voie = bien_cols[0].text_input(
                "Numero",
                key="business_bien_num",
            )
            bien_adresse_voie = bien_cols[1].text_input("Voie", key="business_bien_voie")
            bien_adresse_cp = bien_cols[2].text_input(
                "Code postal",
                key="business_bien_cp",
            )
            bien_adresse_ville = bien_cols[3].text_input(
                "Ville",
                key="business_bien_ville",
            )

    return BusinessWizardInput(
        structure=selected_type.structure,
        profession=conditions["profession"],
        sci_iris=conditions["sci_iris"],
        option_is=conditions["option_is"],
        site_distinct=conditions["site_distinct"],
        scm=conditions["scm"],
        scm_cession=conditions["scm_cession"],
        regime_communautaire=conditions["regime_communautaire"],
        derogation=conditions["derogation"],
        cession=conditions["cession"],
        cabinet_type=conditions["cabinet_type"],
        associe_unique=conditions["associe_unique"],
        cession_actions=conditions["cession_actions"],
        nombre_associes=int(associe_count),
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


def _apply_business_structure_override(dossier_types: tuple[object, ...]) -> None:
    requested_structure = st.session_state.pop(BUSINESS_STRUCTURE_OVERRIDE_KEY, None)
    if requested_structure is None:
        return
    for dossier_type in dossier_types:
        if getattr(dossier_type, "structure", None) == requested_structure:
            st.session_state[BUSINESS_STRUCTURE_WIDGET_KEY] = dossier_type
            return


def _collect_selarl_business_input(conditions: dict[str, object | None]) -> BusinessWizardInput:
    reuse_rules = {rule.key: rule for rule in selarl_ui_reuse_rules()}
    selarl_dossier_unipersonnel = conditions["dossier_unipersonnel"] is True

    st.subheader(selarl_ui_visible_screen_title("fiche_client"))
    with st.expander("Fiche Client - Praticien", expanded=True):
        if selarl_dossier_unipersonnel:
            st.info("Le Praticien est l’associé unique, le gérant et le signataire")
        personne_genre = st.selectbox(
            "Genre grammatical du Praticien",
            GENDER_OPTIONS,
            key="selarl_personne_genre",
        )
        personne_civilite = st.selectbox(
            "Civilite du Praticien",
            ("", "Monsieur", "Madame", "Docteur"),
            key="selarl_personne_civilite",
        )
        person_cols = st.columns(2)
        personne_prenom = person_cols[0].text_input(
            "Prenom du Praticien",
            key="selarl_personne_prenom",
        )
        personne_nom = person_cols[1].text_input(
            "Nom du Praticien",
            key="selarl_personne_nom",
        )
        personne_date_naissance = st.text_input(
            "Date de naissance du Praticien (AAAA-MM-JJ)",
            key="selarl_personne_date_naissance",
        )
        naissance_cols = st.columns(2)
        dirigeant_ville_naissance = naissance_cols[0].text_input(
            "Ville de naissance du Praticien",
            key="selarl_personne_ville_naissance",
        )
        dirigeant_departement_naissance = naissance_cols[1].text_input(
            "Departement de naissance du Praticien",
            key="selarl_personne_departement_naissance",
        )
        personne_nationalite = st.text_input(
            "Nationalite du Praticien",
            key="selarl_personne_nationalite",
        )
        personne_nom_pere = st.text_input(
            "Nom du pere du Praticien",
            key="selarl_personne_nom_pere",
        )
        personne_nom_mere = st.text_input(
            "Nom de la mere du Praticien",
            key="selarl_personne_nom_mere",
        )
        personne_fonction_dirigeant = st.text_input(
            "Fonction du Praticien",
            value="Gerant",
            key="selarl_personne_fonction",
            help=selarl_ui_field("professionnel.fonction").help_text,
        )
        st.markdown("Adresse personnelle du Praticien")
        personne_addr_cols = st.columns(4)
        personne_adresse_num_voie = personne_addr_cols[0].text_input(
            "Adresse personnelle du Praticien - numero",
            key="selarl_personne_num",
        )
        personne_adresse_voie = personne_addr_cols[1].text_input(
            "Adresse personnelle du Praticien - voie",
            key="selarl_personne_voie",
        )
        personne_adresse_cp = personne_addr_cols[2].text_input(
            "Adresse personnelle du Praticien - code postal",
            key="selarl_personne_cp",
        )
        personne_adresse_ville = personne_addr_cols[3].text_input(
            "Adresse personnelle du Praticien - ville",
            key="selarl_personne_ville",
        )
        st.markdown("Ordre professionnel")
        ordre_cols = st.columns(2)
        ordre_cols[0].text_input(
            "Numero RPPS du Praticien",
            key="selarl_numero_rpps",
            help=selarl_ui_field("ordre.numeros").help_text,
        )
        ordre_cols[1].text_input(
            "Numero ordinal du Praticien",
            key="selarl_numero_ordre",
            help=selarl_ui_field("ordre.numeros").help_text,
        )
        st.text_input(
            selarl_ui_field("ordre.adresse_conseil").label,
            key="selarl_adresse_conseil_ordre",
            help=selarl_ui_field("ordre.adresse_conseil").help_text,
        )
        st.text_input(
            selarl_ui_field("ordre.adresse_lieu_exercice").label,
            key="selarl_adresse_lieu_exercice",
            help=selarl_ui_field("ordre.adresse_lieu_exercice").help_text,
        )
        if selarl_dossier_unipersonnel:
            selarl_gerant_is_professional = False
            selarl_signataire_is_professional = False
            st.caption("Gérant et signataire alimentés depuis la Fiche Client.")
        else:
            selarl_gerant_is_professional = st.checkbox(
                reuse_rules["gerant_is_professional"].label,
                value=reuse_rules["gerant_is_professional"].default_enabled,
                key="selarl_gerant_is_professional",
                help=reuse_rules["gerant_is_professional"].effect,
            )
            selarl_signataire_is_professional = st.checkbox(
                reuse_rules["signataire_is_professional"].label,
                value=reuse_rules["signataire_is_professional"].default_enabled,
                key="selarl_signataire_is_professional",
                help=reuse_rules["signataire_is_professional"].effect,
            )

        reuse_projection = selarl_ui_reuse_projection(
            BusinessWizardInput(
                structure="SELARL",
                selarl_dossier_unipersonnel=selarl_dossier_unipersonnel,
                selarl_gerant_is_professional=selarl_gerant_is_professional,
                selarl_signataire_is_professional=selarl_signataire_is_professional,
            )
        )
        if reuse_projection.praticien_is_gerant:
            st.caption("Gérant dérivé depuis le Praticien.")
            dirigeant_genre = personne_genre
            dirigeant_civilite_affichage = personne_civilite
            dirigeant_prenom = personne_prenom
            dirigeant_nom = personne_nom
            dirigeant_date_naissance = personne_date_naissance
            dirigeant_nationalite = personne_nationalite
            dirigeant_fonction_affichage = "gerant"
            dirigeant_adresse_num_voie = personne_adresse_num_voie
            dirigeant_adresse_voie = personne_adresse_voie
            dirigeant_adresse_cp = personne_adresse_cp
            dirigeant_adresse_ville = personne_adresse_ville
        else:
            st.markdown("Gérant distinct du Praticien")
            dirigeant_genre = st.selectbox(
                "Genre grammatical du gérant distinct",
                GENDER_OPTIONS,
                key="selarl_dirigeant_genre",
            )
            dirigeant_civilite_affichage = st.selectbox(
                "Civilité du gérant distinct",
                ("", "Monsieur", "Madame", "Docteur"),
                key="selarl_dirigeant_civilite",
            )
            dirigeant_cols = st.columns(2)
            dirigeant_prenom = dirigeant_cols[0].text_input(
                "Prénom du gérant distinct",
                key="selarl_dirigeant_prenom",
            )
            dirigeant_nom = dirigeant_cols[1].text_input(
                "Nom du gérant distinct",
                key="selarl_dirigeant_nom",
            )
            dirigeant_date_naissance = st.text_input(
                "Date de naissance du gérant distinct (AAAA-MM-JJ)",
                key="selarl_dirigeant_date_naissance",
            )
            dirigeant_nationalite = st.text_input(
                "Nationalité du gérant distinct",
                key="selarl_dirigeant_nationalite",
            )
            dirigeant_fonction_affichage = st.text_input(
                "Fonction du gérant distinct",
                value="gerant",
                key="selarl_dirigeant_fonction",
            )
            dirigeant_adresse_num_voie = st.text_input(
                "Adresse personnelle du gérant distinct - numéro",
                key="selarl_dirigeant_num",
            )
            dirigeant_adresse_voie = st.text_input(
                "Adresse personnelle du gérant distinct - voie",
                key="selarl_dirigeant_voie",
            )
            dirigeant_adresse_cp = st.text_input(
                "Adresse personnelle du gérant distinct - code postal",
                key="selarl_dirigeant_cp",
            )
            dirigeant_adresse_ville = st.text_input(
                "Adresse personnelle du gérant distinct - ville",
                key="selarl_dirigeant_ville",
            )

    st.subheader(selarl_ui_visible_screen_title("fiche_societe"))
    with st.expander("Fiche Société - SELARL, siège et domiciliation", expanded=True):
        societe_denomination = st.text_input(
            selarl_ui_field("societe.denomination").label,
            key="selarl_societe_denomination",
            help=selarl_ui_field("societe.denomination").help_text,
        )
        societe_forme_sociale = st.text_input(
            selarl_ui_field("societe.forme_sociale").label,
            value="SELARL",
            key="selarl_societe_forme_sociale",
            help=selarl_ui_field("societe.forme_sociale").help_text,
        )
        societe_forme_sociale_affichage = st.text_input(
            "Forme sociale affichée de la SELARL",
            value="Société d'exercice libéral à responsabilité limitée",
            key="selarl_societe_forme_sociale_affichage",
        )
        societe_forme_sociale_libelle_long = st.text_input(
            "Libellé long de forme sociale de la SELARL",
            value="société d'exercice libéral à responsabilité limitée",
            key="selarl_societe_forme_sociale_libelle_long",
        )
        societe_capital_social = st.text_input(
            selarl_ui_field("societe.capital_social").label,
            key="selarl_societe_capital_social",
            help=selarl_ui_field("societe.capital_social").help_text,
        )
        societe_ville_rcs = st.text_input(
            "Ville du RCS de la SELARL",
            key="selarl_societe_ville_rcs",
            help=selarl_ui_field("societe.rcs").help_text,
        )
        st.markdown("Adresse du siège social")
        siege_cols = st.columns(4)
        societe_siege_num_voie = siege_cols[0].text_input(
            selarl_ui_field("siege_social.numero").label,
            key="selarl_societe_num",
        )
        societe_siege_voie = siege_cols[1].text_input(
            selarl_ui_field("siege_social.voie").label,
            key="selarl_societe_voie",
        )
        societe_siege_cp = siege_cols[2].text_input(
            selarl_ui_field("siege_social.cp").label,
            key="selarl_societe_cp",
        )
        societe_siege_ville = siege_cols[3].text_input(
            selarl_ui_field("siege_social.ville").label,
            key="selarl_societe_ville",
        )
        selarl_domiciliation_is_registered_office = st.checkbox(
            reuse_rules["domiciliation_is_registered_office"].label,
            value=reuse_rules["domiciliation_is_registered_office"].default_enabled,
            key="selarl_domiciliation_is_registered_office",
            help=reuse_rules["domiciliation_is_registered_office"].effect,
        )
        derived_domiciliation = _format_address(
            societe_siege_num_voie,
            societe_siege_voie,
            societe_siege_cp,
            societe_siege_ville,
        )
        domiciliation_key = "selarl_domiciliation_adresse_affichee"
        if selarl_domiciliation_is_registered_office:
            st.session_state[domiciliation_key] = derived_domiciliation
        domiciliation_adresse_affichee = st.text_input(
            selarl_ui_field("siege_social.domiciliation").label,
            key=domiciliation_key,
            disabled=selarl_domiciliation_is_registered_office,
            help=selarl_ui_field("siege_social.domiciliation").help_text,
        )
        if selarl_domiciliation_is_registered_office:
            domiciliation_adresse_affichee = derived_domiciliation
        if selarl_domiciliation_is_registered_office:
            st.caption("Donnée dérivée depuis l'adresse du siège social.")

    st.subheader(selarl_ui_visible_screen_title("capital_associes"))
    with st.expander("Capital & Associés", expanded=True):
        parts_cols = st.columns(2)
        capital_nb_parts_total_input = parts_cols[0].number_input(
            "Nombre total de parts de la SELARL",
            min_value=0,
            value=0,
            key="selarl_capital_nb_parts_total",
        )
        capital_valeur_nominale_part = parts_cols[1].text_input(
            "Valeur nominale d'une part de la SELARL",
            key="selarl_capital_valeur_nominale_part",
        )
        associe_count_input = st.number_input(
            "Nombre d'associés de la SELARL",
            min_value=1,
            max_value=2,
            value=1,
            key="selarl_associe_count",
            disabled=selarl_dossier_unipersonnel,
        )
        associe_count = 1 if selarl_dossier_unipersonnel else int(associe_count_input)
        if selarl_dossier_unipersonnel:
            selarl_signataire_is_associe_1 = False
            copy_associe_1_from_professional = True
            st.caption("Associé unique alimenté depuis la Fiche Client / Praticien.")
        else:
            selarl_signataire_is_associe_1 = st.checkbox(
                reuse_rules["signataire_is_associe_1"].label,
                value=reuse_rules["signataire_is_associe_1"].default_enabled,
                key="selarl_signataire_is_associe_1",
                help=reuse_rules["signataire_is_associe_1"].effect,
            )
            copy_associe_1_from_professional = st.checkbox(
                "Copier l'associé 1 depuis le Praticien",
                value=False,
                key="selarl_copy_associe_1_from_professional",
            )
        associes = _collect_selarl_associes(
            associe_count,
            copy_associe_1=selarl_signataire_is_associe_1 or copy_associe_1_from_professional,
            personne_genre=personne_genre,
            personne_civilite=personne_civilite,
            personne_prenom=personne_prenom,
            personne_nom=personne_nom,
        )
        gerant_choice = st.selectbox(
            "Choix du gérant parmi les associés",
            tuple(f"Associé {index + 1}" for index in range(associe_count)),
            key="selarl_gerant_choice",
            disabled=selarl_dossier_unipersonnel,
        )
        if selarl_dossier_unipersonnel:
            st.caption("Gérant alimenté depuis la Fiche Client / Praticien.")
        else:
            st.caption(f"Sélection actuelle : {gerant_choice}.")

    st.subheader(selarl_ui_visible_screen_title("contexte_scenarios"))
    selarl_company_is_acquirer = False
    selarl_company_is_scm_transferee = False
    selarl_mandataire_is_signataire = False
    visibility_probe = BusinessWizardInput(
        structure="SELARL",
        profession=conditions["profession"],
        site_distinct=conditions["site_distinct"],
        scm_cession=conditions["scm_cession"],
        regime_communautaire=conditions["regime_communautaire"],
        derogation=conditions["derogation"],
        cession=conditions["cession"],
        cabinet_type=conditions["cabinet_type"],
        selarl_dossier_unipersonnel=selarl_dossier_unipersonnel,
    )
    visible_fields_by_step = selarl_ui_visible_fields_by_step(visibility_probe)
    contexte_fields = visible_fields_by_step["contexte_scenarios"]
    with st.expander("Régime, SCM, cession, bail et financement", expanded=True):
        visible_blocks = selarl_ui_block_visibility(visibility_probe)
        active_any = False
        if visible_blocks["regime_conjoint"]:
            active_any = True
            _render_selarl_schema_block("regime_conjoint", visibility_probe, "regime")
        if visible_blocks["scm"]:
            active_any = True
            selarl_company_is_scm_transferee = st.checkbox(
                reuse_rules["selarl_is_scm_transferee"].label,
                value=reuse_rules["selarl_is_scm_transferee"].default_enabled,
                key="selarl_company_is_scm_transferee",
                help=reuse_rules["selarl_is_scm_transferee"].effect,
            )
            if selarl_company_is_scm_transferee:
                st.caption("Cessionnaire SCM dérivé depuis la SELARL en création.")
            _render_selarl_schema_block("scm", visibility_probe, "scm")
        if visible_blocks["cession_cabinet"]:
            active_any = True
            selarl_company_is_acquirer = st.checkbox(
                reuse_rules["selarl_is_acquirer"].label,
                value=reuse_rules["selarl_is_acquirer"].default_enabled,
                key="selarl_company_is_acquirer",
                help=reuse_rules["selarl_is_acquirer"].effect,
            )
            if selarl_company_is_acquirer:
                st.caption("Acquéreur dérivé depuis la SELARL en création.")
            _render_selarl_schema_block("cession_cabinet", visibility_probe, "cession")
            _render_selarl_schema_block("bail", visibility_probe, "bail")
            _render_selarl_schema_block(
                "banque_financement",
                visibility_probe,
                "banque",
                skip_keys={"banque.emprunt_pv", "banque.adresse_bien_finance"},
            )
        if conditions["derogation"] is True:
            active_any = True
            st.info(
                "Derogation SELARL : DOC-013 et DOC-014 restent visibles comme "
                "pieces manuelles / hors generation pilote."
            )
        if not active_any and contexte_fields:
            st.caption("Aucun bloc conditionnel actif pour cette qualification.")

    reuse_projection = selarl_ui_reuse_projection(
        BusinessWizardInput(
            structure="SELARL",
            selarl_dossier_unipersonnel=selarl_dossier_unipersonnel,
            selarl_gerant_is_professional=selarl_gerant_is_professional,
            selarl_signataire_is_professional=selarl_signataire_is_professional,
            selarl_signataire_is_associe_1=selarl_signataire_is_associe_1,
            selarl_company_is_acquirer=selarl_company_is_acquirer,
            selarl_company_is_scm_transferee=selarl_company_is_scm_transferee,
            selarl_domiciliation_is_registered_office=(selarl_domiciliation_is_registered_office),
        )
    )
    with st.expander("Signataire, signature et option DOC-004", expanded=True):
        if reuse_projection.praticien_is_signataire:
            st.caption("Signataire alimenté depuis le Praticien.")
        else:
            st.caption("Le signataire reste distinct sauf option explicite.")
        decision_date = st.text_input(
            "Date de décision du PV nomination gérant",
            key="selarl_decision_date",
        )
        reunion_date_lettres = st.text_input(
            "Date de réunion en lettres",
            key="selarl_reunion_date_lettres",
        )
        reunion_heure = st.text_input("Heure de réunion", key="selarl_reunion_heure")
        signature_lieu = st.text_input("Lieu de signature", key="selarl_signature_lieu")
        signature_date = st.text_input(
            "Date de signature (AAAA-MM-JJ)",
            key="selarl_signature_date",
        )
        signature_nombre_exemplaires = st.text_input(
            "Nombre d'exemplaires",
            key="selarl_signature_nombre_exemplaires",
        )
        emprunt_actif = st.checkbox(
            "Emprunt autorise dans le PV nomination gerant (DOC-004)",
            value=False,
            key="selarl_emprunt_actif",
            help=selarl_ui_field("banque.emprunt_pv").help_text,
        )
        emprunt_montant_max = ""
        bien_adresse_num_voie = ""
        bien_adresse_voie = ""
        bien_adresse_cp = ""
        bien_adresse_ville = ""
        if emprunt_actif:
            emprunt_montant_max = st.text_input(
                "Montant maximum de l'emprunt DOC-004",
                key="selarl_emprunt_montant_max",
            )
            bien_cols = st.columns(4)
            bien_adresse_num_voie = bien_cols[0].text_input(
                "Adresse du bien finance - numero",
                key="selarl_bien_num",
            )
            bien_adresse_voie = bien_cols[1].text_input(
                "Adresse du bien finance - voie",
                key="selarl_bien_voie",
            )
            bien_adresse_cp = bien_cols[2].text_input(
                "Adresse du bien finance - code postal",
                key="selarl_bien_cp",
            )
            bien_adresse_ville = bien_cols[3].text_input(
                "Adresse du bien finance - ville",
                key="selarl_bien_ville",
            )

    with st.expander("Mandataire (DOC-034 / formalité)", expanded=False):
        st.caption("Le mandataire n’est pas assimilé au signataire par défaut.")
        selarl_mandataire_is_signataire = st.checkbox(
            reuse_rules["mandataire_is_signataire"].label,
            value=reuse_rules["mandataire_is_signataire"].default_enabled,
            key="selarl_mandataire_is_signataire",
            help=(
                reuse_rules["mandataire_is_signataire"].effect
                + " "
                + reuse_rules["mandataire_is_signataire"].behavior_if_inactive
            ),
        )

    return BusinessWizardInput(
        structure="SELARL",
        profession=conditions["profession"],
        site_distinct=conditions["site_distinct"],
        scm_cession=conditions["scm_cession"],
        regime_communautaire=conditions["regime_communautaire"],
        derogation=conditions["derogation"],
        cession=conditions["cession"],
        cabinet_type=conditions["cabinet_type"],
        nombre_associes=int(associe_count),
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
        societe_capital_variable=True,
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
        selarl_signataire_is_associe_1=selarl_signataire_is_associe_1,
        selarl_dossier_unipersonnel=selarl_dossier_unipersonnel,
        selarl_gerant_is_professional=selarl_gerant_is_professional,
        selarl_signataire_is_professional=selarl_signataire_is_professional,
        selarl_mandataire_is_signataire=selarl_mandataire_is_signataire,
        selarl_company_is_acquirer=selarl_company_is_acquirer,
        selarl_company_is_scm_transferee=selarl_company_is_scm_transferee,
        selarl_domiciliation_is_registered_office=(selarl_domiciliation_is_registered_office),
    )


def _render_selarl_schema_block(
    block_key: str,
    data: BusinessWizardInput,
    key_prefix: str,
    *,
    skip_keys: set[str] | None = None,
) -> None:
    skip_keys = skip_keys or set()
    fields = selarl_ui_visible_fields_by_block(data).get(block_key, ())
    if not fields:
        return
    st.markdown(next(field.block_key for field in fields).replace("_", " ").title())
    for field in fields:
        if field.key in skip_keys:
            continue
        st.text_input(
            field.label,
            key=f"selarl_{key_prefix}_{field.key.replace('.', '_')}",
            help=field.help_text,
            placeholder=field.example or "",
        )


def _collect_selarl_associes(
    count: int,
    *,
    copy_associe_1: bool,
    personne_genre: str,
    personne_civilite: str,
    personne_prenom: str,
    personne_nom: str,
) -> tuple[BusinessAssociateInput, ...]:
    associes: list[BusinessAssociateInput] = []
    for index in range(count):
        st.markdown(f"Associé {index + 1}")
        derived = index == 0 and copy_associe_1
        genre_key = f"selarl_associe_genre_{index}"
        civilite_key = f"selarl_associe_civilite_{index}"
        prenom_key = f"selarl_associe_prenom_{index}"
        nom_key = f"selarl_associe_nom_{index}"
        if derived:
            st.session_state[genre_key] = personne_genre
            st.session_state[civilite_key] = personne_civilite
            st.session_state[prenom_key] = personne_prenom
            st.session_state[nom_key] = personne_nom
        cols = st.columns(5)
        genre = cols[0].selectbox(
            f"Associé {index + 1} - genre grammatical",
            GENDER_OPTIONS,
            key=genre_key,
            disabled=derived,
        )
        civilite = cols[1].selectbox(
            f"Associé {index + 1} - civilité",
            ("", "Monsieur", "Madame", "Docteur"),
            key=civilite_key,
            disabled=derived,
        )
        prenom = cols[2].text_input(
            f"Associé {index + 1} - prénom",
            key=prenom_key,
            disabled=derived,
        )
        nom = cols[3].text_input(
            f"Associé {index + 1} - nom",
            key=nom_key,
            disabled=derived,
        )
        nb_parts_input = cols[4].number_input(
            f"Associé {index + 1} - nombre de parts",
            min_value=0,
            value=0,
            key=f"selarl_associe_parts_{index}",
        )
        present = st.checkbox(
            f"Associé {index + 1} présent ou représenté",
            value=True,
            key=f"selarl_associe_present_{index}",
        )
        if derived:
            st.caption(f"Associé {index + 1} dérivé depuis le Praticien.")
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


def _format_address(num_voie: str, voie: str, cp: str, ville: str) -> str:
    street = " ".join(part for part in (num_voie, voie) if part.strip())
    locality = " ".join(part for part in (cp, ville) if part.strip())
    return ", ".join(part for part in (street, locality) if part)


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
            f"Dossier genere : {len(result.docx_paths)} DOCX, {len(result.pdf_paths)} PDF, 1 ZIP."
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


def _ensure_single_document_session_defaults(selection_key: tuple[str, str]) -> None:
    if st.session_state.get("single_document_selection_key") == selection_key:
        return
    st.session_state.single_document_selection_key = selection_key
    st.session_state.single_document_docx_paths = []
    st.session_state.single_document_pdf_results = []
    st.session_state.single_document_pdf_error = None
    st.session_state.single_document_zip_path = None
    st.session_state.single_document_output_dir = None


def _single_document_docx_paths() -> list[Path]:
    return list(st.session_state.get("single_document_docx_paths", []))


def _single_document_pdf_paths() -> list[Path]:
    return [result.pdf_path for result in st.session_state.get("single_document_pdf_results", [])]


def _single_document_zip_path() -> Path | None:
    return st.session_state.get("single_document_zip_path")


def _single_document_output_dir(default: Path) -> Path:
    output_dir = st.session_state.get("single_document_output_dir")
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
st.caption("Creation de dossier et generation des documents prets.")

internal_tools_available = _internal_tools_available()
internal_tools_enabled = False
internal_tool = None
if internal_tools_available:
    with st.sidebar:
        internal_tools_enabled = st.checkbox(
            "Outils internes",
            value=False,
            key="front_internal_tools_enabled",
        )
        if internal_tools_enabled:
            internal_tool = st.radio(
                "Outil interne",
                INTERNAL_TOOL_LABELS,
                key="front_internal_tool",
            )

if internal_tools_enabled and internal_tool is not None:
    _render_internal_tools_shell(internal_tool)
else:
    _render_target_front_shell()

if internal_tools_available:
    st.caption(
        "La generation technique ne vaut pas validation juridique ni revue visuelle humaine. "
        "Les artefacts sont produits sous artifacts/ et restent hors versionnement."
    )
