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

INTERNAL_TOOLS_SESSION_FLAG = "_sydel_internal_tools_unlocked"


def test_simple_entry_populates_dossier_records() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_simple_entry())

    assert {"person-praticien-principal", "person-mandataire-ordre"}.issubset(
        dossier.persons
    )
    assert {
        "company-societe-principale",
        "company-ordre-professionnel",
        "company-banque-depot",
    }.issubset(dossier.companies)
    assert {address.usage for address in dossier.addresses.values()} == {
        AddressUsage.ADRESSE_PERSONNELLE,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.DOMICILIATION,
        AddressUsage.ORDRE,
        AddressUsage.BANQUE,
    }
    assert "personne.signataire.prenom" in dossier.canonical_values
    assert "societe.societe_principale.denomination" in dossier.canonical_values
    assert "domiciliation.adresse" in dossier.canonical_values
    assert "ordre.professionnel" in dossier.canonical_values
    assert "banque.depot.nom" in dossier.canonical_values


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


def test_simple_entry_recalculates_document_statuses_for_simple_selarl_pack() -> None:
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
        "DOC-017": DocumentStatus.GENERABLE,
        "DOC-034": DocumentStatus.GENERABLE,
    }
    assert view.status_summary.generable_doc_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-017",
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
        "DOC-017",
        "DOC-034",
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

    assert {"objet": "PersonRecord", "nombre": "2"} in object_rows
    assert any(row["role"] == "signataire" for row in role_rows)
    assert any(row["usage"] == "domiciliation" for row in address_rows)
    assert all(
        issue.severity is not ValidationSeverity.BLOCKING
        for issue in validate_dossier(dossier)
    )


def test_entry_support_keeps_single_visible_selarl_surface() -> None:
    assert front_dossier_entry_is_supported("SELARL creation simple") is True
    assert front_dossier_entry_is_supported("SELARL ordre / inscription") is False


def test_streamlit_dossier_area_exposes_real_entry_fields() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    assert app.checkbox(key="front_entry_dossier_unipersonnel").label == (
        "Dossier unipersonnel"
    )
    assert app.text_input(key="front_entry_person_prenom").label == "Prenom"
    assert app.text_input(key="front_entry_company_siege_social").label == "Siege social"
    assert app.checkbox(key="front_entry_domiciliation_same_as_siege").label == (
        "Domiciliation = siege social"
    )
    assert len(app.expander) == 0
    assert not any(item.label == "Diagnostic dossier" for item in app.expander)
    assert any(metric.label == "Prets a generer" for metric in app.metric)
    assert len(app.table) == 0


def test_streamlit_prototype_zone_remains_secondary() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    assert len(app.radio) == 0
    assert not any(item.label == "Outils internes" for item in app.checkbox)
    app.session_state[INTERNAL_TOOLS_SESSION_FLAG] = True
    app.run(timeout=120)
    app.checkbox(key="front_internal_tools_enabled").set_value(True)
    app.run(timeout=120)

    assert app.radio(key="front_internal_tool").label == "Outil interne"
    assert any("Outils internes" in item.value for item in app.subheader)


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
        "signature_prestataire": "Yousign",
        "titre_affichage": "Dr",
        "ordre_conseil_departemental_libelle": "Conseil departemental de l'Ordre",
        "ordre_destinataire_appel": "Madame la Presidente",
        "ordre_profession_signataire_affichee": "medecin",
        "ordre_profession_ligne_destinataire": "medecins",
        "ordre_profession_reglementee_pluriel": "medecins",
        "ordre_adresse_ligne_1": "6 rue du Conseil",
        "ordre_adresse_cp": "75001",
        "ordre_adresse_ville": "Paris",
        "ordre_numero": "12345",
        "ordre_numero_rpps": "10000000001",
        "mandataire_civilite_affichage": "Madame",
        "mandataire_prenom": "Sophie",
        "mandataire_nom": "Durand",
        "mandataire_fonction": "juriste",
        "mandataire_cabinet": "DAAT",
        "statuts_capital_social_lettres": "dix mille",
        "statuts_apport_montant": "10 000",
        "statuts_apport_montant_lettres": "dix mille",
        "statuts_nombre_titres_total_lettres": "cent",
        "statuts_valeur_nominale_titre_lettres": "cent euros",
        "statuts_associe_qualification_principale": "cardiologue",
        "statuts_associe_situation_maritale": "celibataire",
        "statuts_associe_regime_matrimonial": "neant",
        "depot_banque_nom": "BANQUE EXEMPLE",
        "depot_banque_adresse": "1 boulevard Haussmann, 75009 Paris",
        "exercice_social_debut": "1er janvier",
        "exercice_social_fin": "31 decembre",
        "exercice_social_date_cloture_premier_exercice": "31 decembre 2026",
        "exercice_lieu_principal_adresse": "12 avenue de la Republique, 75011 Paris",
        "gerance_seuil_achat_materiel": "10 000 euros",
        "gerance_seuil_emprunt": "50 000 euros",
        "document_nombre_exemplaires_lettres": "trois",
    }
    values.update(overrides)
    return FrontDossierSimpleEntry(**values)
