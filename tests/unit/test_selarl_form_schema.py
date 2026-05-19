from __future__ import annotations

import subprocess
from pathlib import Path

from sydel_doc_engine.app.selarl_form_schema import (
    FieldRequirement,
    VariableCoverageStatus,
    all_selarl_v2_variables,
    selarl_blocks,
    selarl_document_specs,
    selarl_expected_documents,
    selarl_fields,
    selarl_generable_document_codes,
    selarl_required_conditions,
    selarl_reuse_rules,
    selarl_variable_coverage,
    validate_selarl_schema,
)
from sydel_doc_engine.domain.case_catalog import DocumentAvailability


def test_selarl_schema_validation_has_no_internal_issue() -> None:
    assert validate_selarl_schema() == ()


def test_required_business_blocks_exist() -> None:
    block_keys = {field.block_key for field in selarl_fields()}

    assert {
        "qualification",
        "societe",
        "siege_social",
        "professionnel_gerant",
        "ordre_professionnel",
        "associes",
        "mandataire_signataire",
        "regime_conjoint",
        "cession_cabinet",
        "bail",
        "scm",
        "banque_financement",
        "signature",
    }.issubset(block_keys)


def test_no_field_has_exact_adresse_label_or_ambiguous_address_label() -> None:
    ambiguous_labels = {"adresse", "numero", "numéro", "voie", "ville", "code postal"}

    for field in selarl_fields():
        assert field.label.casefold().strip() not in ambiguous_labels


def test_address_fields_have_qualified_labels() -> None:
    address_labels = [
        field.label.casefold() for field in selarl_fields() if "adresse" in field.label.casefold()
    ]

    assert address_labels
    expected_qualified_fragments = {
        "adresse personnelle du praticien",
        "adresse du siège social",
        "adresse de domiciliation",
        "adresse du conseil de l'ordre",
        "adresse du lieu d'exercice",
        "adresse du cabinet cédé",
        "adresse du vendeur",
        "adresse d'exercice du vendeur",
        "adresse du bailleur",
        "adresse du locataire",
        "adresse des locaux loués",
        "adresse de la banque",
        "adresse du bien financé",
        "adresse du cédant scm",
        "adresse du cessionnaire scm",
        "adresse de la scm cédée",
        "adresse du service d'enregistrement",
    }

    for fragment in expected_qualified_fragments:
        assert any(fragment in label for label in address_labels), fragment


def test_selarl_visible_wording_uses_business_terms() -> None:
    visible_text = "\n".join(_visible_selarl_schema_texts())
    visible_text_folded = visible_text.casefold()
    banned = "professionnel " + "principal"

    assert banned not in visible_text_folded
    assert "Fiche Client" in visible_text
    assert "Praticien" in visible_text
    assert "gérant" in visible_text_folded
    assert "associé" in visible_text_folded
    assert "signataire" in visible_text_folded
    assert "mandataire" in visible_text_folded


def test_transcription_error_term_is_absent_outside_notebooklm_source() -> None:
    banned = b"CE" + b"LAR"
    allowed_path = Path("project/source_truth/notebooklm_selarl_10_prompts_v1.md")
    tracked_files = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")

    violations = [
        str(path)
        for raw_path in tracked_files
        if raw_path
        for path in [Path(raw_path.decode("utf-8", errors="surrogateescape"))]
        if path != allowed_path and banned in path.read_bytes()
    ]

    assert violations == []


def test_reuse_rules_cover_required_selarl_deduplications() -> None:
    rule_keys = {rule.key for rule in selarl_reuse_rules()}

    assert {
        "signataire_is_associe_1",
        "gerant_is_professional",
        "signataire_is_professional",
        "mandataire_is_signataire",
        "selarl_is_acquirer",
        "selarl_is_scm_transferee",
        "domiciliation_is_registered_office",
    }.issubset(rule_keys)


def test_doc_013_and_doc_014_are_visible_manual_and_not_generable() -> None:
    documents = selarl_expected_documents({"derogation": True})
    docs_by_code = {
        document.document_code: document for document in documents if document.document_code
    }
    generable_codes = set(selarl_generable_document_codes({"derogation": True}))

    assert docs_by_code["DOC-013"].availability == DocumentAvailability.MANUAL_ONLY
    assert docs_by_code["DOC-014"].availability == DocumentAvailability.MANUAL_ONLY
    assert "DOC-013" not in generable_codes
    assert "DOC-014" not in generable_codes


def test_doc_006_carries_source_v2_reserve_in_schema_and_catalog_projection() -> None:
    specs_by_code = {
        document.document_code: document
        for document in selarl_document_specs()
        if document.document_code
    }
    expected_by_code = {
        document.document_code: document
        for document in selarl_expected_documents({"regime_communautaire": True})
        if document.document_code
    }

    assert specs_by_code["DOC-006"].expected_availability == DocumentAvailability.GENERATABLE
    assert specs_by_code["DOC-006"].reserve_note is not None
    assert "vraie V2" in specs_by_code["DOC-006"].reserve_note
    assert any("vraie V2" in note for note in expected_by_code["DOC-006"].notes)


def test_doc_005_and_conditional_selarl_documents_remain_generable() -> None:
    assert "DOC-005" in selarl_generable_document_codes({"regime_communautaire": True})
    assert {"DOC-031", "DOC-032", "DOC-033"}.issubset(
        selarl_generable_document_codes({"scm_cession": True})
    )
    assert {"DOC-007", "DOC-008"}.issubset(
        selarl_generable_document_codes({"cession": True})
    )
    assert {"DOC-009", "DOC-010"}.issubset(
        selarl_generable_document_codes({"cession": True, "cabinet_type": "medical"})
    )
    assert {"DOC-011", "DOC-012"}.issubset(
        selarl_generable_document_codes({"cession": True, "cabinet_type": "dentaire"})
    )


def test_manual_documents_remain_visible() -> None:
    documents = selarl_expected_documents({"site_distinct": True, "derogation": True})
    manual_keys = {
        document.document_key
        for document in documents
        if document.availability == DocumentAvailability.MANUAL_ONLY
    }

    assert {
        "site_distinct_cd94_sel",
        "formulaire_derogation_sites_sel",
        "derogation_sel_bnc",
        "derogation_cumul_selarl_bnc",
    }.issubset(manual_keys)


def test_required_selarl_conditions_exist() -> None:
    assert set(selarl_required_conditions()) == {
        "profession",
        "site_distinct",
        "scm_cession",
        "regime_communautaire",
        "derogation",
        "cession",
        "cabinet_type",
    }


def test_form_schema_is_grouped_by_business_blocks() -> None:
    fields_by_block = {}
    for field in selarl_fields():
        fields_by_block.setdefault(field.block_key, []).append(field)

    assert len(fields_by_block) >= 13
    assert all(fields for fields in fields_by_block.values())
    assert any(field.requirement == FieldRequirement.CONDITIONAL for field in selarl_fields())


def test_variable_v2_coverage_is_not_empty_and_has_no_silent_gap() -> None:
    coverage = selarl_variable_coverage()

    assert all_selarl_v2_variables()
    assert coverage
    assert {entry.variable for entry in coverage} == set(all_selarl_v2_variables())


def test_critical_v2_variables_are_mapped_or_derived() -> None:
    coverage_by_variable = {entry.variable: entry for entry in selarl_variable_coverage()}
    critical_variables = {
        "civilite",
        "prenom",
        "nom",
        "date_naissance",
        "num_voie_perso",
        "voie_perso",
        "cp_perso",
        "ville_perso",
        "denomination_societe",
        "capital_social",
        "num_voie_siege",
        "voie_siege",
        "cp_siege",
        "ville_siege",
        "adresse_conseil_ordre",
        "cp_ordre",
        "ville_ordre",
        "adresse_banque",
        "adresse_bailleur",
        "adresse_locataire",
        "adresse_vendeur",
        "adresse_cabinet",
        "adresse_locaux",
        "adresse_cedant",
        "adresse_siege_cessionnaire",
    }

    assert critical_variables.issubset(coverage_by_variable)
    assert all(
        coverage_by_variable[variable].status
        in {VariableCoverageStatus.UI_FIELD, VariableCoverageStatus.REUSE_RULE}
        for variable in critical_variables
    )


def _visible_selarl_schema_texts() -> tuple[str, ...]:
    texts: list[str] = []
    for block in selarl_blocks():
        texts.extend((block.label, block.description))
    for field in selarl_fields():
        texts.append(field.label)
        texts.append(field.help_text)
        if field.display_condition:
            texts.append(field.display_condition)
        if field.example:
            texts.append(field.example)
    for rule in selarl_reuse_rules():
        texts.extend((rule.label, rule.effect, rule.activation_condition))
    return tuple(texts)
