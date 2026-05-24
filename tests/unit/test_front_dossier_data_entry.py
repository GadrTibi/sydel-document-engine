from __future__ import annotations

from streamlit.testing.v1 import AppTest

from sydel_doc_engine.app.front_dossier_entry import (
    DOMICILIATION_REUSE_RULE_ID,
    FrontDossierSimpleEntry,
    build_front_dossier_entry_dossier,
    build_front_dossier_entry_view,
    front_dossier_entry_address_rows,
    front_dossier_entry_is_supported,
    front_dossier_entry_object_rows,
    front_dossier_entry_role_rows,
)
from sydel_doc_engine.app.front_shell import PROTOTYPE_TOOLS_LABEL, TARGET_FRONT_LABEL
from sydel_doc_engine.front_data import (
    AddressUsage,
    BusinessRole,
    DocumentLotStatus,
    DocumentStatus,
    ValidationSeverity,
    address_ref,
    role_ref,
    validate_dossier,
)


def test_simple_entry_populates_dossier_records() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_simple_entry())

    assert set(dossier.persons) == {"person-praticien-principal"}
    assert set(dossier.companies) == {"company-societe-principale"}
    assert {address.usage for address in dossier.addresses.values()} == {
        AddressUsage.ADRESSE_PERSONNELLE,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.DOMICILIATION,
    }
    assert "personne.signataire.prenom" in dossier.canonical_values
    assert "societe.societe_principale.denomination" in dossier.canonical_values
    assert "domiciliation.adresse" in dossier.canonical_values


def test_dossier_unipersonnel_creates_explicit_role_assignments() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_simple_entry())

    role_targets = {
        assignment.role: assignment.target_id
        for assignment in dossier.role_assignments.values()
    }
    assert role_targets[BusinessRole.PRATICIEN] == "person-praticien-principal"
    assert role_targets[BusinessRole.ASSOCIE] == "person-praticien-principal"
    assert role_targets[BusinessRole.GERANT] == "person-praticien-principal"
    assert role_targets[BusinessRole.SIGNATAIRE] == "person-praticien-principal"
    assert dossier.has_active_reuse_rule(
        role_ref(BusinessRole.PRATICIEN),
        role_ref(BusinessRole.SIGNATAIRE),
    )


def test_domiciliation_same_as_siege_uses_explicit_reuse_rule() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_simple_entry())

    assert DOMICILIATION_REUSE_RULE_ID in dossier.reuse_rules
    assert dossier.has_active_reuse_rule(
        address_ref(AddressUsage.SIEGE_SOCIAL),
        address_ref(AddressUsage.DOMICILIATION),
    )
    domiciliation = dossier.addresses["address-domiciliation"]
    assert domiciliation.source_address_id == "address-siege-social"
    assert domiciliation.source_rule_id == DOMICILIATION_REUSE_RULE_ID


def test_distinct_domiciliation_does_not_create_reuse_rule() -> None:
    entry = _complete_simple_entry(
        domiciliation_same_as_siege=False,
        domiciliation="44 avenue des Tests, 75009 Paris",
    )
    dossier = build_front_dossier_entry_dossier(entry)

    assert DOMICILIATION_REUSE_RULE_ID not in dossier.reuse_rules
    assert dossier.addresses["address-domiciliation"].display_value == (
        "44 avenue des Tests, 75009 Paris"
    )
    assert not dossier.has_active_reuse_rule(
        address_ref(AddressUsage.SIEGE_SOCIAL),
        address_ref(AddressUsage.DOMICILIATION),
    )


def test_simple_entry_recalculates_document_statuses_for_doc_001_to_doc_004() -> None:
    view = build_front_dossier_entry_view(_complete_simple_entry())

    statuses = {
        document.doc_code: document.status
        for document in view.status_summary.documents
    }
    assert statuses == {
        "DOC-001": DocumentStatus.GENERABLE,
        "DOC-002": DocumentStatus.GENERABLE,
        "DOC-003": DocumentStatus.GENERABLE,
        "DOC-004": DocumentStatus.GENERABLE,
    }
    assert view.status_summary.generable_doc_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    )
    assert view.status_summary.lots[0].status is DocumentLotStatus.READY


def test_incomplete_entry_keeps_statuses_blocked_and_explained() -> None:
    view = build_front_dossier_entry_view(
        FrontDossierSimpleEntry(prenom="Alice", nom="Martin")
    )

    assert set(view.status_summary.blocked_doc_codes) == {
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    }
    doc_002 = next(
        document for document in view.status_summary.documents if document.doc_code == "DOC-002"
    )
    assert BusinessRole.SOCIETE_PRINCIPALE in doc_002.missing_roles
    assert AddressUsage.SIEGE_SOCIAL in doc_002.missing_address_usages


def test_entry_rows_expose_real_data_layer_objects() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_simple_entry())

    object_rows = front_dossier_entry_object_rows(dossier)
    role_rows = front_dossier_entry_role_rows(dossier)
    address_rows = front_dossier_entry_address_rows(dossier)

    assert {"objet": "PersonRecord", "nombre": "1"} in object_rows
    assert any(row["role"] == "signataire" for row in role_rows)
    assert any(row["usage"] == "domiciliation" for row in address_rows)
    assert all(
        issue.severity is not ValidationSeverity.BLOCKING
        for issue in validate_dossier(dossier)
    )


def test_entry_support_stays_limited_to_selarl_creation_simple() -> None:
    assert front_dossier_entry_is_supported("SELARL creation simple") is True
    assert front_dossier_entry_is_supported("SELARL ordre / inscription") is False


def test_streamlit_dossier_area_exposes_real_entry_fields() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    assert app.radio[0].value == TARGET_FRONT_LABEL
    app.radio[1].set_value("Dossier")
    app.run(timeout=120)

    assert app.checkbox(key="front_entry_dossier_unipersonnel").label == (
        "Dossier unipersonnel"
    )
    assert app.text_input(key="front_entry_person_prenom").label == "Prenom"
    assert app.text_input(key="front_entry_company_siege_social").label == "Siege social"
    assert app.checkbox(key="front_entry_domiciliation_same_as_siege").label == (
        "Domiciliation = siege social"
    )
    assert any("DossierRecord alimente" in item.value for item in app.subheader)


def test_streamlit_prototype_zone_remains_secondary() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    app.radio[0].set_value(PROTOTYPE_TOOLS_LABEL)
    app.run(timeout=120)

    assert app.radio[1].label == "Outil de test / prototype"
    assert any(PROTOTYPE_TOOLS_LABEL in item.value for item in app.subheader)


def _complete_simple_entry(**overrides: object) -> FrontDossierSimpleEntry:
    values = {
        "civilite_affichage": "Madame",
        "genre": "feminin",
        "prenom": "Alice",
        "nom": "Martin",
        "date_naissance": "1980-01-01",
        "nationalite": "francaise",
        "nom_pere": "Jean Martin",
        "nom_mere": "Claire Durand",
        "adresse_personnelle": "12 rue Exemple, 75001 Paris",
        "societe_denomination": "SELARL Alice Martin",
        "societe_capital_social": "10 000 euros",
        "siege_social": "12 rue Exemple, 75001 Paris",
        "capital_titres_nombre_total": "100",
        "capital_titres_valeur_nominale": "100 euros",
        "decision_date": "2026-05-24",
        "reunion_date_lettres": "vingt-quatre mai deux mille vingt-six",
        "reunion_heure": "10 heures",
        "signature_lieu": "Paris",
        "signature_date": "2026-05-24",
        "signature_nombre_exemplaires": "3",
    }
    values.update(overrides)
    return FrontDossierSimpleEntry(**values)
