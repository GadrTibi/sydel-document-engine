from __future__ import annotations

import inspect

import sydel_doc_engine.front_data.dossier_flow as dossier_flow
from sydel_doc_engine.front_data import (
    AddressUsage,
    BusinessRole,
    DossierBlockId,
    DossierRecord,
    DossierStepId,
    FlowStatus,
    active_reuse_rules_for_flow,
    build_dossier_flow,
    build_sentinel_dossier_flow,
    sentinel_requirement,
)


def test_build_dossier_flow_contains_expected_steps() -> None:
    flow = build_sentinel_dossier_flow()

    assert [step.id for step in flow.steps] == [
        DossierStepId.QUALIFICATION,
        DossierStepId.PERSONS,
        DossierStepId.COMPANY,
        DossierStepId.ROLES_PARTIES,
        DossierStepId.ADDRESSES,
        DossierStepId.CAPITAL_TITLES_APPORTS,
        DossierStepId.ORDER,
        DossierStepId.OPERATIONS,
        DossierStepId.DOCUMENTS,
        DossierStepId.GENERATION,
    ]
    assert flow.block(DossierBlockId.DOCUMENT_REQUIREMENTS).active
    assert flow.block(DossierBlockId.GENERATION_READINESS).active


def test_blocks_activate_only_for_relevant_documents() -> None:
    order_flow = build_dossier_flow(document_codes=("DOC-034",))
    cession_flow = build_dossier_flow(document_codes=("DOC-009",))

    assert order_flow.block(DossierBlockId.ORDER_MANDATE).status is FlowStatus.AVAILABLE
    assert order_flow.block(DossierBlockId.CESSION_CABINET).status is FlowStatus.INACTIVE
    assert cession_flow.block(DossierBlockId.CESSION_CABINET).status is FlowStatus.AVAILABLE
    assert cession_flow.block(DossierBlockId.ORDER_MANDATE).status is FlowStatus.INACTIVE


def test_dependencies_between_steps_and_blocks_are_explicit() -> None:
    flow = build_sentinel_dossier_flow()

    assert DossierStepId.QUALIFICATION in flow.step(DossierStepId.PERSONS).dependencies
    assert DossierStepId.DOCUMENTS in flow.step(DossierStepId.GENERATION).dependencies
    assert DossierBlockId.DOCUMENT_REQUIREMENTS in (
        flow.block(DossierBlockId.GENERATION_READINESS).dependencies
    )
    assert DossierBlockId.ROLE_ASSIGNMENTS in flow.block(DossierBlockId.ORDER_MANDATE).dependencies


def test_doc_034_flow_structures_order_mandate_and_document_lot() -> None:
    flow = build_dossier_flow(document_codes=("DOC-034",))

    order_identifiers = flow.block(DossierBlockId.ORDER_IDENTIFIERS)
    order_mandate = flow.block(DossierBlockId.ORDER_MANDATE)

    assert order_identifiers.document_codes == ("DOC-034",)
    assert BusinessRole.ORDRE_PROFESSIONNEL in order_identifiers.required_roles
    assert AddressUsage.ORDRE in order_identifiers.required_address_usages
    assert BusinessRole.MANDATAIRE in order_mandate.required_roles
    assert BusinessRole.SIGNATAIRE in order_mandate.required_roles
    assert set(order_mandate.unresolved_ambiguity_keys) == {
        "mandataire_configurable",
        "derogation_manual_block",
    }
    assert flow.documents_for_block(DossierBlockId.DOCUMENT_REQUIREMENTS) == ("DOC-034",)


def test_doc_017_flow_structures_capital_associes_and_order() -> None:
    flow = build_dossier_flow(document_codes=("DOC-017",))

    assert flow.block(DossierBlockId.CAPITAL_ASSOCIATES).status is FlowStatus.AVAILABLE
    assert flow.block(DossierBlockId.CAPITAL_TITLES).status is FlowStatus.AVAILABLE
    assert flow.block(DossierBlockId.ORDER_IDENTIFIERS).status is FlowStatus.AVAILABLE
    assert "capital.repartition_associes" in (
        flow.block(DossierBlockId.CAPITAL_ASSOCIATES).required_canonical_fields
    )
    assert "capital.titres.nombre_total" in (
        flow.block(DossierBlockId.CAPITAL_TITLES).required_canonical_fields
    )
    assert "seuils_gerance" in flow.block(DossierBlockId.CAPITAL_TITLES).unresolved_ambiguity_keys


def test_doc_009_flow_structures_cession_bail_financing_origin_and_exercises() -> None:
    flow = build_dossier_flow(document_codes=("DOC-009",))

    active_blocks = {block.id for block in flow.active_blocks()}

    assert {
        DossierBlockId.CESSION_CABINET,
        DossierBlockId.CESSION_PRICE,
        DossierBlockId.CESSION_ORIGIN,
        DossierBlockId.CESSION_EXERCISES,
        DossierBlockId.BAIL,
        DossierBlockId.FINANCING,
    }.issubset(active_blocks)
    assert "address:lieu_exercice -> address:cabinet_cede" in (
        flow.block(DossierBlockId.CESSION_CABINET).possible_reuse_rules
    )
    assert "address:lieu_exercice -> address:locaux_loues" in (
        flow.block(DossierBlockId.BAIL).possible_reuse_rules
    )
    assert "origine_propriete_libre" in (
        flow.block(DossierBlockId.CESSION_ORIGIN).unresolved_ambiguity_keys
    )
    assert "exercices_financiers_collection" in (
        flow.block(DossierBlockId.CESSION_EXERCISES).unresolved_ambiguity_keys
    )


def test_doc_041_flow_structures_spfpl_apport_titres_and_control_roles() -> None:
    flow = build_dossier_flow(document_codes=("DOC-041",))

    spfpl = flow.block(DossierBlockId.SPFPL)
    apport_titres = flow.block(DossierBlockId.APPORT_TITRES)

    assert spfpl.status is FlowStatus.AVAILABLE
    assert apport_titres.status is FlowStatus.AVAILABLE
    assert BusinessRole.SPFPL_BENEFICIAIRE in spfpl.required_roles
    assert BusinessRole.SOCIETE_CIBLE in spfpl.required_roles
    assert BusinessRole.COMMISSAIRE_AUX_APPORTS in apport_titres.required_roles
    assert BusinessRole.EVALUATEUR_APPORT in apport_titres.required_roles
    assert "apport_titres.*" in apport_titres.required_canonical_fields
    assert "commissaire_label_confirm" in apport_titres.unresolved_ambiguity_keys


def test_doc_025_flow_structures_scm_associes_bank_and_apports() -> None:
    flow = build_dossier_flow(document_codes=("DOC-025",))

    scm = flow.block(DossierBlockId.SCM)
    scm_associes = flow.block(DossierBlockId.SCM_ASSOCIATES)
    financing = flow.block(DossierBlockId.FINANCING)

    assert scm.status is FlowStatus.AVAILABLE
    assert scm_associes.status is FlowStatus.AVAILABLE
    assert financing.status is FlowStatus.AVAILABLE
    assert BusinessRole.SCM in scm.required_roles
    assert BusinessRole.REPRESENTANT_PERSONNE_MORALE in scm.required_roles
    assert BusinessRole.BANQUE in financing.required_roles
    assert "statuts_civils.associes[]" in scm_associes.required_canonical_fields
    assert "legacy_nb_parts_personne_2" in scm_associes.unresolved_ambiguity_keys


def test_empty_dossier_validation_localizes_missing_doc_034_data() -> None:
    dossier = DossierRecord(id="dossier-doc-034")
    dossier.add_document_requirement(sentinel_requirement("DOC-034"))

    flow = build_dossier_flow(dossier)
    mandate_result = flow.validation_for_block(DossierBlockId.ORDER_MANDATE)

    assert mandate_result.status is FlowStatus.BLOCKED
    assert BusinessRole.MANDATAIRE in mandate_result.missing_roles
    assert BusinessRole.SIGNATAIRE in mandate_result.missing_roles
    assert "personne.mandataire.*" in mandate_result.missing_canonical_fields
    assert "mandataire_configurable" in mandate_result.unresolved_ambiguity_keys


def test_dossier_flow_has_no_streamlit_dependency() -> None:
    source = inspect.getsource(dossier_flow).lower()

    assert "streamlit" not in source


def test_flow_does_not_create_implicit_roles_addresses_or_reuse() -> None:
    dossier = DossierRecord(id="dossier-no-flow-fusion")
    dossier.add_document_requirement(sentinel_requirement("DOC-009"))

    flow = build_dossier_flow(dossier)

    assert dossier.role_assignments == {}
    assert dossier.addresses == {}
    assert dossier.reuse_rules == {}
    assert active_reuse_rules_for_flow(dossier) == ()
    assert flow.block(DossierBlockId.ADDRESS_REUSE).possible_reuse_rules
