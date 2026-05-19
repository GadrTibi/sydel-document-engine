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
    BusinessWizardValidation,
    business_document_table_rows,
    business_dossier_types,
    evaluate_business_wizard,
    selarl_ui_block_visibility,
    selarl_ui_condition_specs,
    selarl_ui_document_specs,
    selarl_ui_field,
    selarl_ui_reuse_rules,
    selarl_ui_visible_fields_by_block,
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

    if data.structure == "SELARL":
        st.subheader("Ecran 6 - Documents attendus")
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

    st.subheader("Etape 5 - Generation" if data.structure != "SELARL" else "Ecran 7 - Generation")
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
    }
    with st.expander("Conditions metier de selection documentaire", expanded=True):
        if case_type == "SCI":
            variant = st.selectbox(
                "SCI simple ou SCI IRIS",
                ("", "SCI simple", "SCI IRIS"),
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
    st.subheader("Etape 1 - Type de dossier")
    dossier_types = business_dossier_types()
    selected_type = st.selectbox(
        "Type de dossier metier",
        dossier_types,
        format_func=lambda item: item.label,
    )
    st.caption(selected_type.status)
    conditions = _collect_case_conditions(selected_type.structure)

    if selected_type.structure == "SELARL":
        return _collect_selarl_business_input(conditions)

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

    with st.expander("Representant legal", expanded=True):
        dirigeant_genre = st.selectbox("Genre du representant legal", GENDER_OPTIONS)
        dirigeant_civilite_affichage = st.selectbox(
            "Civilite du representant legal",
            ("", "Monsieur", "Madame"),
        )
        dirigeant_cols = st.columns(2)
        dirigeant_prenom = dirigeant_cols[0].text_input("Prenom du representant legal")
        dirigeant_nom = dirigeant_cols[1].text_input("Nom du representant legal")
        dirigeant_date_naissance = st.text_input(
            "Date de naissance du representant legal (AAAA-MM-JJ)"
        )
        dirigeant_ville_naissance = st.text_input("Ville de naissance du representant legal")
        dirigeant_departement_naissance = st.text_input(
            "Departement de naissance du representant legal"
        )
        dirigeant_nationalite = st.text_input("Nationalite du representant legal")
        dirigeant_fonction_affichage = st.text_input("Fonction nommee", value="gerant")
        st.markdown("Adresse personnelle du representant legal")
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


def _collect_selarl_business_input(conditions: dict[str, object | None]) -> BusinessWizardInput:
    st.subheader("Ecran 2 - Societe")
    reuse_rules = {rule.key: rule for rule in selarl_ui_reuse_rules()}
    with st.expander("Societe", expanded=True):
        societe_denomination = st.text_input(
            selarl_ui_field("societe.denomination").label,
            help=selarl_ui_field("societe.denomination").help_text,
        )
        societe_forme_sociale = st.text_input(
            selarl_ui_field("societe.forme_sociale").label,
            value="SELARL",
            help=selarl_ui_field("societe.forme_sociale").help_text,
        )
        societe_forme_sociale_affichage = st.text_input(
            "Forme sociale affichee de la SELARL",
            value="Societe d'exercice liberal a responsabilite limitee",
        )
        societe_forme_sociale_libelle_long = st.text_input(
            "Libelle long de forme sociale de la SELARL",
            value="societe d'exercice liberal a responsabilite limitee",
        )
        societe_capital_social = st.text_input(
            selarl_ui_field("societe.capital_social").label,
            help=selarl_ui_field("societe.capital_social").help_text,
        )
        parts_cols = st.columns(2)
        capital_nb_parts_total_input = parts_cols[0].number_input(
            "Nombre total de parts de la SELARL",
            min_value=0,
            value=0,
        )
        capital_valeur_nominale_part = parts_cols[1].text_input(
            "Valeur nominale d'une part de la SELARL"
        )
        societe_ville_rcs = st.text_input(
            "Ville du RCS de la SELARL",
            help=selarl_ui_field("societe.rcs").help_text,
        )
        st.markdown("Adresse du siege social")
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
            value=True,
            help=reuse_rules["domiciliation_is_registered_office"].effect,
        )
        derived_domiciliation = _format_address(
            societe_siege_num_voie,
            societe_siege_voie,
            societe_siege_cp,
            societe_siege_ville,
        )
        domiciliation_adresse_affichee = st.text_input(
            selarl_ui_field("siege_social.domiciliation").label,
            value=derived_domiciliation if selarl_domiciliation_is_registered_office else "",
            disabled=selarl_domiciliation_is_registered_office,
            help=selarl_ui_field("siege_social.domiciliation").help_text,
        )
        if selarl_domiciliation_is_registered_office:
            st.caption("Donnee derivee depuis l'adresse du siege social.")

    st.subheader("Ecran 3 - Fiche Client")
    with st.expander("Fiche Client - Praticien et gerant", expanded=True):
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
        personne_prenom = person_cols[0].text_input("Prenom du Praticien")
        personne_nom = person_cols[1].text_input("Nom du Praticien")
        personne_date_naissance = st.text_input(
            "Date de naissance du Praticien (AAAA-MM-JJ)"
        )
        naissance_cols = st.columns(2)
        dirigeant_ville_naissance = naissance_cols[0].text_input(
            "Ville de naissance du Praticien"
        )
        dirigeant_departement_naissance = naissance_cols[1].text_input(
            "Departement de naissance du Praticien"
        )
        personne_nationalite = st.text_input("Nationalite du Praticien")
        personne_nom_pere = st.text_input("Nom du pere du Praticien")
        personne_nom_mere = st.text_input("Nom de la mere du Praticien")
        personne_fonction_dirigeant = st.text_input(
            "Fonction du Praticien",
            value="Gerant",
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
        selarl_gerant_is_professional = st.checkbox(
            reuse_rules["gerant_is_professional"].label,
            value=True,
            help=reuse_rules["gerant_is_professional"].effect,
        )
        selarl_signataire_is_professional = st.checkbox(
            reuse_rules["signataire_is_professional"].label,
            value=True,
            help=reuse_rules["signataire_is_professional"].effect,
        )
        selarl_mandataire_is_signataire = st.checkbox(
            reuse_rules["mandataire_is_signataire"].label,
            value=True,
            help=reuse_rules["mandataire_is_signataire"].effect,
        )
        if selarl_gerant_is_professional:
            st.caption("Gerant derive depuis le Praticien.")
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
            st.markdown("Gerant distinct du Praticien")
            dirigeant_genre = st.selectbox(
                "Genre grammatical du gerant distinct",
                GENDER_OPTIONS,
                key="selarl_dirigeant_genre",
            )
            dirigeant_civilite_affichage = st.selectbox(
                "Civilite du gerant distinct",
                ("", "Monsieur", "Madame", "Docteur"),
                key="selarl_dirigeant_civilite",
            )
            dirigeant_cols = st.columns(2)
            dirigeant_prenom = dirigeant_cols[0].text_input("Prenom du gerant distinct")
            dirigeant_nom = dirigeant_cols[1].text_input("Nom du gerant distinct")
            dirigeant_date_naissance = st.text_input(
                "Date de naissance du gerant distinct (AAAA-MM-JJ)"
            )
            dirigeant_nationalite = st.text_input("Nationalite du gerant distinct")
            dirigeant_fonction_affichage = st.text_input(
                "Fonction du gerant distinct",
                value="gerant",
            )
            dirigeant_adresse_num_voie = st.text_input(
                "Adresse personnelle du gerant distinct - numero"
            )
            dirigeant_adresse_voie = st.text_input(
                "Adresse personnelle du gerant distinct - voie"
            )
            dirigeant_adresse_cp = st.text_input(
                "Adresse personnelle du gerant distinct - code postal"
            )
            dirigeant_adresse_ville = st.text_input(
                "Adresse personnelle du gerant distinct - ville"
            )

    st.subheader("Ecran 4 - Associes")
    with st.expander("Associes", expanded=True):
        associe_count = st.number_input(
            "Nombre d'associes de la SELARL",
            min_value=1,
            max_value=2,
            value=1,
        )
        selarl_signataire_is_associe_1 = st.checkbox(
            reuse_rules["signataire_is_associe_1"].label,
            value=True,
            help=reuse_rules["signataire_is_associe_1"].effect,
        )
        copy_associe_1_from_professional = st.checkbox(
            "Copier depuis le Praticien",
            value=True,
        )
        associes = _collect_selarl_associes(
            int(associe_count),
            copy_associe_1=selarl_signataire_is_associe_1
            or copy_associe_1_from_professional,
            personne_genre=personne_genre,
            personne_civilite=personne_civilite,
            personne_prenom=personne_prenom,
            personne_nom=personne_nom,
        )
        gerant_choice = st.selectbox(
            "Choix du gerant parmi les associes",
            tuple(f"Associe {index + 1}" for index in range(int(associe_count))),
        )
        st.caption(f"Selection actuelle : {gerant_choice}.")

    st.subheader("Ecran 5 - Conditions specifiques")
    selarl_company_is_acquirer = False
    selarl_company_is_scm_transferee = False
    with st.expander("Blocs conditionnels SELARL", expanded=True):
        visibility_probe = BusinessWizardInput(
            structure="SELARL",
            profession=conditions["profession"],
            site_distinct=conditions["site_distinct"],
            scm_cession=conditions["scm_cession"],
            regime_communautaire=conditions["regime_communautaire"],
            derogation=conditions["derogation"],
            cession=conditions["cession"],
            cabinet_type=conditions["cabinet_type"],
        )
        visible_blocks = selarl_ui_block_visibility(visibility_probe)
        active_any = False
        if visible_blocks["regime_conjoint"]:
            active_any = True
            _render_selarl_schema_block("regime_conjoint", visibility_probe, "regime")
        if visible_blocks["scm"]:
            active_any = True
            selarl_company_is_scm_transferee = st.checkbox(
                reuse_rules["selarl_is_scm_transferee"].label,
                value=True,
                help=reuse_rules["selarl_is_scm_transferee"].effect,
            )
            if selarl_company_is_scm_transferee:
                st.caption("Cessionnaire SCM derive depuis la SELARL en creation.")
            _render_selarl_schema_block("scm", visibility_probe, "scm")
        if visible_blocks["cession_cabinet"]:
            active_any = True
            selarl_company_is_acquirer = st.checkbox(
                reuse_rules["selarl_is_acquirer"].label,
                value=True,
                help=reuse_rules["selarl_is_acquirer"].effect,
            )
            if selarl_company_is_acquirer:
                st.caption("Acquereur derive depuis la SELARL en creation.")
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
        if not active_any:
            st.caption("Aucun bloc conditionnel actif pour cette qualification.")

    with st.expander("Signature et option DOC-004", expanded=True):
        decision_date = st.text_input("Date de decision du PV nomination gerant")
        reunion_date_lettres = st.text_input("Date de reunion en lettres")
        reunion_heure = st.text_input("Heure de reunion")
        signature_lieu = st.text_input("Lieu de signature")
        signature_date = st.text_input("Date de signature (AAAA-MM-JJ)")
        signature_nombre_exemplaires = st.text_input("Nombre d'exemplaires")
        emprunt_actif = st.checkbox(
            "Emprunt autorise dans le PV nomination gerant (DOC-004)",
            value=False,
            help=selarl_ui_field("banque.emprunt_pv").help_text,
        )
        emprunt_montant_max = ""
        bien_adresse_num_voie = ""
        bien_adresse_voie = ""
        bien_adresse_cp = ""
        bien_adresse_ville = ""
        if emprunt_actif:
            emprunt_montant_max = st.text_input("Montant maximum de l'emprunt DOC-004")
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
        selarl_gerant_is_professional=selarl_gerant_is_professional,
        selarl_signataire_is_professional=selarl_signataire_is_professional,
        selarl_mandataire_is_signataire=selarl_mandataire_is_signataire,
        selarl_company_is_acquirer=selarl_company_is_acquirer,
        selarl_company_is_scm_transferee=selarl_company_is_scm_transferee,
        selarl_domiciliation_is_registered_office=(
            selarl_domiciliation_is_registered_office
        ),
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
        st.markdown(f"Associe {index + 1}")
        derived = index == 0 and copy_associe_1
        cols = st.columns(5)
        genre = cols[0].selectbox(
            f"Associe {index + 1} - genre grammatical",
            GENDER_OPTIONS,
            index=GENDER_OPTIONS.index(personne_genre) if derived else 0,
            key=f"selarl_associe_genre_{index}",
            disabled=derived,
        )
        civilite = cols[1].selectbox(
            f"Associe {index + 1} - civilite",
            ("", "Monsieur", "Madame", "Docteur"),
            index=_selectbox_index(("", "Monsieur", "Madame", "Docteur"), personne_civilite)
            if derived
            else 0,
            key=f"selarl_associe_civilite_{index}",
            disabled=derived,
        )
        prenom = cols[2].text_input(
            f"Associe {index + 1} - prenom",
            value=personne_prenom if derived else "",
            key=f"selarl_associe_prenom_{index}",
            disabled=derived,
        )
        nom = cols[3].text_input(
            f"Associe {index + 1} - nom",
            value=personne_nom if derived else "",
            key=f"selarl_associe_nom_{index}",
            disabled=derived,
        )
        nb_parts_input = cols[4].number_input(
            f"Associe {index + 1} - nombre de parts",
            min_value=0,
            value=0,
            key=f"selarl_associe_parts_{index}",
        )
        present = st.checkbox(
            f"Associe {index + 1} present ou represente",
            value=True,
            key=f"selarl_associe_present_{index}",
        )
        if derived:
            st.caption(f"Associe {index + 1} derive depuis le Praticien.")
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


def _selectbox_index(options: tuple[str, ...], value: str) -> int:
    return options.index(value) if value in options else 0


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
