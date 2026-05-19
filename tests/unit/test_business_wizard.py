from __future__ import annotations

import unicodedata
from dataclasses import replace
from pathlib import Path
from zipfile import ZipFile

from docx import Document

from sydel_doc_engine.app import business_wizard
from sydel_doc_engine.app.business_wizard import (
    STATUS_CONTEXT_INCOMPLETE,
    STATUS_GENERABLE,
    STATUS_MANUAL_ONLY,
    STATUS_NOT_IMPLEMENTED,
    BusinessWizardInput,
    business_document_table_rows,
    evaluate_business_wizard,
    sample_business_wizard_input,
    selarl_ui_address_labels,
    selarl_ui_block_visibility,
    selarl_ui_condition_specs,
    selarl_ui_document_specs,
    selarl_ui_field,
    selarl_ui_flow_steps,
    selarl_ui_non_automatic_reuse_relations,
    selarl_ui_reuse_projection,
    selarl_ui_reuse_rules,
    selarl_ui_visible_fields_by_step,
    selarl_ui_visible_screen_titles,
)
from sydel_doc_engine.app.ui_runtime import (
    generate_docx_files_for_document_codes,
    generate_zip_file,
)
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def test_business_wizard_uses_case_catalog(monkeypatch) -> None:
    calls: list[object] = []

    def fake_get_expected_documents(case_input: object) -> list[object]:
        calls.append(case_input)
        return []

    monkeypatch.setattr(
        business_wizard,
        "get_expected_documents",
        fake_get_expected_documents,
    )

    evaluate_business_wizard(
        BusinessWizardInput(structure="SCI", sci_iris=False, option_is=False)
    )

    assert calls


def test_business_wizard_builds_minimal_valid_context() -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())

    assert validation.context is not None
    assert validation.can_generate_docx is True
    assert validation.missing_fields == ()
    assert validation.inconsistencies == ()
    assert validation.context.structure == "SCI"
    assert validation.generatable_document_codes == (
        "DOC-001",
        "DOC-003",
        "DOC-002",
        "DOC-004",
    )


def test_business_wizard_validation_detects_missing_fields() -> None:
    data = BusinessWizardInput(structure="SCI")

    validation = evaluate_business_wizard(data)

    assert validation.can_generate_docx is False
    assert "conditions.sci_iris" in validation.missing_fields
    assert "conditions.option_is" in validation.missing_fields
    assert "personne_signataire.civilite" in validation.missing_fields
    assert "societe.denomination" in validation.missing_fields
    assert "signature.date" in validation.missing_fields
    assert any(row.status == "blocked_missing_fields" for row in validation.document_rows)


def test_business_wizard_document_rows_show_expected_documents() -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())

    rows = business_document_table_rows(validation)

    assert [row["code document"] for row in rows] == [
        "DOC-020",
        "DOC-001",
        "DOC-003",
        "DOC-002",
        "DOC-004",
    ]
    assert rows[0]["statut"] == "Contexte incomplet pour génération V2"
    assert {row["statut"] for row in rows[1:]} == {"Générable"}


def test_business_wizard_context_uses_orchestrator_selection() -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())
    assert validation.context is not None
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(validation.context)

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    ]


def test_business_wizard_sci_option_is_displays_doc_022() -> None:
    validation = evaluate_business_wizard(
        replace(sample_business_wizard_input(), option_is=True)
    )

    assert "DOC-022" in _row_codes(validation)
    option_is_row = _row_by_code(validation, "DOC-022")
    assert option_is_row.status == STATUS_CONTEXT_INCOMPLETE


def test_business_wizard_sci_iris_displays_doc_021_and_not_doc_020() -> None:
    validation = evaluate_business_wizard(
        replace(sample_business_wizard_input(), sci_iris=True)
    )

    assert "DOC-021" in _row_codes(validation)
    assert "DOC-020" not in _row_codes(validation)


def test_business_wizard_selarl_regime_communautaire_displays_doc_005_and_doc_006() -> None:
    validation = evaluate_business_wizard(
        _case_data(
            "SELARL",
            profession="medecin",
            site_distinct=False,
            scm_cession=False,
            regime_communautaire=True,
            derogation=False,
            cession=False,
        )
    )

    assert "DOC-005" in _row_codes(validation)
    assert "DOC-006" in _row_codes(validation)


def test_business_wizard_selarl_site_distinct_displays_manual_document() -> None:
    validation = evaluate_business_wizard(
        _case_data(
            "SELARL",
            profession="chirurgien_dentiste",
            site_distinct=True,
            scm_cession=False,
            regime_communautaire=False,
            derogation=False,
            cession=False,
        )
    )

    manual_row = next(row for row in validation.document_rows if row.document_code is None)

    assert manual_row.document_key == "site_distinct_cd94_sel"
    assert manual_row.status == STATUS_MANUAL_ONLY


def test_business_wizard_selas_derogation_displays_not_implemented_document() -> None:
    validation = evaluate_business_wizard(
        _case_data(
            "SELAS",
            profession="medecin",
            scm=False,
            regime_communautaire=False,
            derogation=True,
            cession=False,
        )
    )

    row = next(
        row
        for row in validation.document_rows
        if row.document_key == "derogation_cumul_selarl_salariee"
    )

    assert row.status == STATUS_NOT_IMPLEMENTED


def test_business_wizard_spfpl_cession_displays_agrement_by_associate_count() -> None:
    unique = evaluate_business_wizard(
        _case_data(
            "SPFPL cession",
            regime_communautaire=False,
            associe_unique=True,
            cession_actions=False,
        )
    )
    several = evaluate_business_wizard(
        _case_data(
            "SPFPL cession",
            regime_communautaire=False,
            associe_unique=False,
            cession_actions=False,
        )
    )

    assert "DOC-038" in _row_codes(unique)
    assert "DOC-039" not in _row_codes(unique)
    assert "DOC-039" in _row_codes(several)
    assert "DOC-038" not in _row_codes(several)


def test_business_wizard_manual_and_not_implemented_documents_are_not_sent_to_generation() -> None:
    validation = evaluate_business_wizard(
        _case_data(
            "SELARL",
            profession="medecin",
            site_distinct=True,
            scm_cession=False,
            regime_communautaire=False,
            derogation=True,
            cession=False,
        )
    )

    excluded_statuses = {STATUS_MANUAL_ONLY, STATUS_NOT_IMPLEMENTED}
    excluded_rows = [row for row in validation.document_rows if row.status in excluded_statuses]

    assert excluded_rows
    assert all(
        row.document_code not in validation.generatable_document_codes
        for row in excluded_rows
    )
    assert all(
        _row_by_code(validation, code).status == STATUS_GENERABLE
        for code in validation.generatable_document_codes
    )


def test_streamlit_technical_mode_remains_accessible() -> None:
    app_source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")

    assert "Technique / diagnostic" in app_source
    assert "Assistant metier" in app_source


def test_streamlit_business_mode_exposes_sci_and_selarl() -> None:
    dossier_types = {item.structure for item in business_wizard.business_dossier_types()}

    assert {"SCI", "SELARL"}.issubset(dossier_types)


def test_selarl_ui_conditions_are_available() -> None:
    assert {spec.key for spec in selarl_ui_condition_specs()} == {
        "profession",
        "site_distinct",
        "scm_cession",
        "regime_communautaire",
        "derogation",
        "cession",
        "cabinet_type",
    }


def test_streamlit_selarl_path_uses_business_wording() -> None:
    app_source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")
    banned = "professionnel " + "principal"

    assert "Dirigeant / pharmacien" not in app_source
    assert banned not in app_source.casefold()
    assert "Écran 3 — Fiche Client" not in app_source
    assert "selarl_ui_visible_screen_title(\"fiche_client\")" in app_source
    assert "Praticien" in app_source


def test_selarl_visible_screen_titles_follow_business_order() -> None:
    assert selarl_ui_visible_screen_titles() == (
        "Écran 1 — Qualification",
        "Écran 2 — Fiche Client",
        "Écran 3 — Fiche Société",
        "Écran 4 — Capital & Associés",
        "Écran 5 — Contexte & scénarios métier",
        "Écran 6 — Documents & génération",
    )


def test_streamlit_selarl_path_consumes_schema_and_reuse_projections() -> None:
    app_source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")

    assert "selarl_ui_visible_screen_title(" in app_source
    assert "selarl_ui_visible_fields_by_step(" in app_source
    assert "selarl_ui_reuse_projection(" in app_source
    assert "selarl_ui_reuse_rules()" in app_source
    assert "selarl_ui_document_specs()" in app_source


def test_streamlit_selarl_path_exposes_dossier_unipersonnel() -> None:
    app_source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")

    assert "qualification.dossier_unipersonnel" in app_source
    assert selarl_ui_field("qualification.dossier_unipersonnel").label == (
        "Dossier unipersonnel"
    )
    assert "Le Praticien est l’associé unique, le gérant et le signataire" in app_source
    assert "selarl_dossier_unipersonnel=selarl_dossier_unipersonnel" in app_source


def test_streamlit_selarl_mandataire_is_secondary_and_not_default() -> None:
    app_source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")

    assert "Mandataire (DOC-034 / formalité)" in app_source
    assert "expanded=False" in app_source
    assert "Le mandataire n’est pas assimilé au signataire par défaut." in app_source
    assert 'value=reuse_rules["mandataire_is_signataire"].default_enabled' in app_source


def test_streamlit_selarl_documents_and_generation_share_screen_six() -> None:
    app_source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")

    assert 'selarl_ui_visible_screen_title("documents_generation")' in app_source
    assert "Ecran 7" not in app_source
    assert "Écran 7" not in app_source
    assert "PV d'autorisation d'emprunt" not in app_source
    assert "Emprunt autorise dans le PV nomination gerant (DOC-004)" in app_source


def test_selarl_ui_flow_steps_follow_business_order() -> None:
    labels = [step.label for step in selarl_ui_flow_steps()]

    assert labels == [
        "Qualification",
        "Fiche Client / Praticien",
        "Fiche Société",
        "Capital & Associés",
        "Contexte & scénarios métier",
        "Documents & génération",
    ]
    assert labels.index("Fiche Client / Praticien") < labels.index("Fiche Société")
    assert labels.index("Capital & Associés") < labels.index(
        "Contexte & scénarios métier"
    )
    assert labels[-1] == "Documents & génération"


def test_selarl_ui_visible_fields_by_step_groups_business_blocks() -> None:
    data = _case_data(
        "SELARL",
        profession="medecin",
        site_distinct=False,
        scm_cession=True,
        regime_communautaire=True,
        derogation=False,
        cession=True,
        cabinet_type="medical",
    )

    fields_by_step = selarl_ui_visible_fields_by_step(data)

    assert fields_by_step["fiche_client"][0].key.startswith("professionnel.")
    assert any(field.block_key == "ordre_professionnel" for field in fields_by_step["fiche_client"])
    assert fields_by_step["fiche_societe"][0].key.startswith("societe.")
    assert any(field.block_key == "siege_social" for field in fields_by_step["fiche_societe"])
    assert all(
        field.block_key == "associes" for field in fields_by_step["capital_associes"]
    )
    assert fields_by_step["contexte_scenarios"]
    assert fields_by_step["documents_generation"] == ()


def test_selarl_ui_address_labels_are_qualified() -> None:
    ambiguous_labels = {"adresse", "numero", "voie", "ville", "code postal"}
    labels = selarl_ui_address_labels()

    assert labels
    assert all(label.casefold().strip() not in ambiguous_labels for label in labels)
    assert any("adresse personnelle du praticien" in label.casefold() for label in labels)
    assert any("adresse du siege social" in _plain(label) for label in labels)
    assert any("adresse de la banque" in label.casefold() for label in labels)


def test_selarl_docs_006_013_014_have_required_ui_statuses() -> None:
    validation = evaluate_business_wizard(
        _case_data(
            "SELARL",
            profession="medecin",
            site_distinct=False,
            scm_cession=False,
            regime_communautaire=True,
            derogation=True,
            cession=False,
        )
    )

    assert any("vraie V2" in note for note in _row_by_code(validation, "DOC-006").notes)
    assert _row_by_code(validation, "DOC-013").status == STATUS_MANUAL_ONLY
    assert _row_by_code(validation, "DOC-014").status == STATUS_MANUAL_ONLY
    assert "DOC-013" not in validation.generatable_document_codes
    assert "DOC-014" not in validation.generatable_document_codes


def test_selarl_ui_reuse_rules_cover_main_deduplications() -> None:
    rules_by_key = {rule.key: rule for rule in selarl_ui_reuse_rules()}

    assert {
        "dossier_unipersonnel",
        "signataire_is_associe_1",
        "gerant_is_professional",
        "signataire_is_professional",
        "mandataire_is_signataire",
        "selarl_is_acquirer",
        "selarl_is_scm_transferee",
        "domiciliation_is_registered_office",
    }.issubset(rules_by_key)
    assert all(rule.default_enabled is False for rule in rules_by_key.values())


def test_selarl_dossier_unipersonnel_projection_links_praticien_roles() -> None:
    data = _case_data(
        "SELARL",
        profession="medecin",
        site_distinct=False,
        scm_cession=False,
        regime_communautaire=False,
        derogation=False,
        cession=False,
        selarl_dossier_unipersonnel=True,
    )

    projection = selarl_ui_reuse_projection(data)
    validation = evaluate_business_wizard(data)

    assert projection.active_rule_keys == ("dossier_unipersonnel",)
    assert projection.praticien_is_associe_unique is True
    assert projection.praticien_is_gerant is True
    assert projection.praticien_is_signataire is True
    assert projection.mandataire_is_signataire is False
    assert {
        "associes.associe_unique",
        "dirigeant_nomine",
        "mandataire_signataire.signataire",
    }.issubset(set(projection.locked_targets))
    assert validation.context is not None
    assert validation.context.dossier_options.associe_unique is True


def test_selarl_reuse_projection_inactive_imposes_no_praticien_derivation() -> None:
    projection = selarl_ui_reuse_projection(_case_data("SELARL"))

    assert projection.active_rule_keys == ()
    assert projection.locked_targets == ()
    assert projection.praticien_is_associe_unique is False
    assert projection.praticien_is_gerant is False
    assert projection.praticien_is_signataire is False
    assert projection.mandataire_is_signataire is False


def test_selarl_explicit_reuse_options_remain_available_without_defaults() -> None:
    projection = selarl_ui_reuse_projection(
        _case_data(
            "SELARL",
            selarl_company_is_acquirer=True,
            selarl_company_is_scm_transferee=True,
            selarl_domiciliation_is_registered_office=True,
        )
    )

    assert {
        "selarl_is_acquirer",
        "selarl_is_scm_transferee",
        "domiciliation_is_registered_office",
    }.issubset(set(projection.active_rule_keys))
    assert {
        "cession_cabinet.acquereur",
        "scm.cessionnaire",
        "siege_social.domiciliation",
    }.issubset(set(projection.locked_targets))


def test_selarl_sensitive_relations_are_not_automatic_reuse_rules() -> None:
    relation_keys = {relation.key for relation in selarl_ui_non_automatic_reuse_relations()}
    rule_keys = {rule.key for rule in selarl_ui_reuse_rules()}
    projection = selarl_ui_reuse_projection(_case_data("SELARL"))

    assert {
        "seller_is_current_tenant",
        "registered_office_is_practice_location",
        "registered_office_is_transferred_cabinet",
        "transferred_cabinet_is_practice_location",
        "seller_is_praticien",
        "scm_transferor_is_praticien",
    } == relation_keys
    assert relation_keys.isdisjoint(rule_keys)
    assert set(projection.non_automatic_relation_keys) == relation_keys


def test_selarl_documents_are_unchanged_by_dossier_unipersonnel() -> None:
    base_data = _case_data(
        "SELARL",
        profession="medecin",
        site_distinct=True,
        scm_cession=True,
        regime_communautaire=True,
        derogation=True,
        cession=True,
        cabinet_type="medical",
    )
    unipersonnel_data = replace(base_data, selarl_dossier_unipersonnel=True)

    base_validation = evaluate_business_wizard(base_data)
    unipersonnel_validation = evaluate_business_wizard(unipersonnel_data)

    assert _row_codes(unipersonnel_validation) == _row_codes(base_validation)
    assert "DOC-013" not in unipersonnel_validation.generatable_document_codes
    assert "DOC-014" not in unipersonnel_validation.generatable_document_codes
    assert any(
        "vraie V2" in note for note in _row_by_code(unipersonnel_validation, "DOC-006").notes
    )


def test_selarl_ui_document_specs_stay_aligned_with_catalog_statuses() -> None:
    spec_codes = {document.document_code for document in selarl_ui_document_specs()}
    validation = evaluate_business_wizard(
        _case_data(
            "SELARL",
            profession="medecin",
            site_distinct=True,
            scm_cession=True,
            regime_communautaire=True,
            derogation=True,
            cession=True,
            cabinet_type="medical",
        )
    )
    row_codes = {row.document_code for row in validation.document_rows}

    assert {"DOC-006", "DOC-013", "DOC-014"}.issubset(spec_codes)
    assert {"DOC-006", "DOC-013", "DOC-014"}.issubset(row_codes)


def test_selarl_ui_block_visibility_masks_inactive_specific_blocks() -> None:
    data = _case_data(
        "SELARL",
        profession="medecin",
        site_distinct=False,
        scm_cession=False,
        regime_communautaire=False,
        derogation=False,
        cession=False,
    )

    visibility = selarl_ui_block_visibility(data)

    assert visibility["societe"] is True
    assert visibility["regime_conjoint"] is False
    assert visibility["scm"] is False
    assert visibility["cession_cabinet"] is False
    assert visibility["bail"] is False
    assert visibility["banque_financement"] is False


def test_business_wizard_generates_docx_and_zip_without_residual_placeholders(
    tmp_path: Path,
) -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())
    assert validation.context is not None

    docx_paths = generate_docx_files_for_document_codes(
        validation.context,
        tmp_path,
        validation.generatable_document_codes,
    )
    zip_path = generate_zip_file(tmp_path, docx_paths)

    assert len(docx_paths) == 4
    for docx_path in docx_paths:
        text = _docx_text(docx_path)
        assert "[" not in text
        assert "]" not in text
    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "manifest.json" in names
    assert "declaration_non_condamnation.docx" in names


def _case_data(structure: str, **conditions: object) -> BusinessWizardInput:
    return replace(sample_business_wizard_input(), structure=structure, **conditions)


def _row_codes(validation) -> list[str]:
    return [row.document_code for row in validation.document_rows if row.document_code]


def _row_by_code(validation, code: str):
    return next(row for row in validation.document_rows if row.document_code == code)


def _plain(value: str) -> str:
    return (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .casefold()
    )


def _docx_text(path: Path) -> str:
    document = Document(path)
    paragraph_text = [paragraph.text for paragraph in document.paragraphs]
    table_text = [
        cell.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
    ]
    return "\n".join([*paragraph_text, *table_text])
