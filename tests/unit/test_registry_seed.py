from __future__ import annotations

from sydel_doc_engine.registry.catalog import build_seed_catalog


def test_seed_catalog_contains_forty_three_documents() -> None:
    catalog = build_seed_catalog()
    assert len(catalog) == 43


def test_seed_catalog_contains_lot_one_to_lot_five_entries() -> None:
    catalog = build_seed_catalog()
    assert {document.lot for document in catalog} == {1, 2, 3, 4, 5}


def test_seed_catalog_pv_nomination_gerant_scope_excludes_sas() -> None:
    catalog = build_seed_catalog()

    pv_document = next(document for document in catalog if document.doc_id == "DOC-004")

    assert set(pv_document.structures) == {
        "SELARL",
        "SELAS",
        "SPFPL cession",
        "SPFPL apport",
        "SCS",
        "SCI",
        "SCM",
    }
    assert "SAS" not in pv_document.structures


def test_seed_catalog_regime_communautaire_scope_is_limited_to_batch_structures() -> None:
    catalog = build_seed_catalog()

    rc_documents = [document for document in catalog if document.doc_id in {"DOC-005", "DOC-006"}]

    assert len(rc_documents) == 2
    for document in rc_documents:
        assert set(document.structures) == {
            "SELARL",
            "SELAS",
            "SPFPL cession",
            "SPFPL apport",
        }
        assert document.general_condition == "dossier.options.regime_communautaire == true"


def test_seed_catalog_bail_appel_fonds_scope_is_limited_to_cession_structures() -> None:
    catalog = build_seed_catalog()

    avenant = next(document for document in catalog if document.doc_id == "DOC-007")
    appel = next(document for document in catalog if document.doc_id == "DOC-008")

    assert set(avenant.structures) == {"SELARL", "SELAS"}
    assert set(appel.structures) == {"SELARL"}
    assert avenant.general_condition == "dossier.options.cession == true"
    assert appel.general_condition == "dossier.options.cession == true"


def test_seed_catalog_cession_cabinets_scope_is_limited_to_sel_structures() -> None:
    catalog = build_seed_catalog()

    cession_documents = [
        document
        for document in catalog
        if document.doc_id in {"DOC-009", "DOC-010", "DOC-011", "DOC-012"}
    ]

    assert len(cession_documents) == 4
    for document in cession_documents:
        assert set(document.structures) == {"SELARL", "SELAS"}
        assert document.general_condition == "dossier.options.cession == true"


def test_seed_catalog_derogations_core_scope_is_explicitly_incomplete() -> None:
    catalog = build_seed_catalog()

    multi_sites = next(document for document in catalog if document.doc_id == "DOC-013")
    cumul_bnc = next(document for document in catalog if document.doc_id == "DOC-014")

    assert set(multi_sites.structures) == {"SELARL", "SELAS"}
    assert set(cumul_bnc.structures) == {"SELARL"}
    assert multi_sites.general_condition == "dossier.options.derogation == true"
    assert cumul_bnc.general_condition == "dossier.options.derogation == true"
    assert any(
        "formulaire_a_completer" in condition
        for condition in multi_sites.specific_conditions
    )
    assert any("formulaire_a_completer" in condition for condition in cumul_bnc.specific_conditions)


def test_seed_catalog_statuts_sas_scope_is_limited_to_sas_spfpl_medecins() -> None:
    catalog = build_seed_catalog()

    statuts = next(document for document in catalog if document.doc_id == "DOC-015")

    assert set(statuts.structures) == {"SAS"}
    assert statuts.general_condition == "dossier.structure == SAS"
    assert "statuts_sas.type == spfpl_medecins" in statuts.specific_conditions
    assert "statuts_sas.profession == medecin" in statuts.specific_conditions


def test_seed_catalog_statuts_sel_scope_is_split_by_overlay() -> None:
    catalog = build_seed_catalog()

    dentiste = next(document for document in catalog if document.doc_id == "DOC-016")
    medecin = next(document for document in catalog if document.doc_id == "DOC-017")
    selas = next(document for document in catalog if document.doc_id == "DOC-018")

    assert set(dentiste.structures) == {"SELARL"}
    assert set(medecin.structures) == {"SELARL"}
    assert set(selas.structures) == {"SELAS"}
    assert "statuts_sel.overlay == selarl_dentiste" in dentiste.specific_conditions
    assert "statuts_sel.overlay == selarl_medecin" in medecin.specific_conditions
    assert "statuts_sel.overlay == selas_medecin" in selas.specific_conditions


def test_seed_catalog_statuts_civils_core_scope_is_limited_to_civil_structures() -> None:
    catalog = build_seed_catalog()

    scs = next(document for document in catalog if document.doc_id == "DOC-019")
    sci = next(document for document in catalog if document.doc_id == "DOC-020")
    sci_iris = next(document for document in catalog if document.doc_id == "DOC-021")
    scm = next(document for document in catalog if document.doc_id == "DOC-025")

    assert set(scs.structures) == {"SCS"}
    assert set(sci.structures) == {"SCI"}
    assert set(sci_iris.structures) == {"SCI IRIS"}
    assert set(scm.structures) == {"SCM"}
    assert "statuts_civils.type == scs" in scs.specific_conditions
    assert "statuts_civils.type == sci" in sci.specific_conditions
    assert "statuts_civils.type == sci_iris" in sci_iris.specific_conditions
    assert "statuts_civils.type == scm" in scm.specific_conditions


def test_seed_catalog_option_is_scope_is_limited_to_sci_structures() -> None:
    catalog = build_seed_catalog()

    option_is = next(document for document in catalog if document.doc_id == "DOC-022")

    assert set(option_is.structures) == {"SCI", "SCI IRIS"}
    assert option_is.general_condition == "dossier.options.option_is == true"
    assert option_is.source_path == "project/source_documents/lot_05/lettre option IS.docx"


def test_seed_catalog_sas_satellites_scope_is_limited_to_sas() -> None:
    catalog = build_seed_catalog()

    pv = next(document for document in catalog if document.doc_id == "DOC-023")
    attestation = next(document for document in catalog if document.doc_id == "DOC-024")

    assert set(pv.structures) == {"SAS"}
    assert set(attestation.structures) == {"SAS"}
    assert "remuneration_president.type == absence_remuneration" in pv.specific_conditions
    assert "un seul souscripteur" in attestation.specific_conditions


def test_seed_catalog_reconciled_order_and_spfpl_generators_are_exposed() -> None:
    catalog = build_seed_catalog()
    documents = {document.doc_id: document for document in catalog}

    assert set(documents["DOC-034"].structures) == {
        "SELARL",
        "SELAS",
        "SPFPL cession",
        "SPFPL apport",
        "SCM",
    }
    assert set(documents["DOC-035"].structures) == {"SPFPL cession"}
    assert set(documents["DOC-036"].structures) == {"SPFPL apport"}
    assert set(documents["DOC-037"].structures) == {"SPFPL cession", "SPFPL apport"}
    assert set(documents["DOC-038"].structures) == {"SPFPL cession"}
    assert set(documents["DOC-039"].structures) == {"SPFPL cession"}
    assert set(documents["DOC-040"].structures) == {"SPFPL cession"}
    assert set(documents["DOC-041"].structures) == {"SPFPL apport"}
    assert set(documents["DOC-042"].structures) == {"SPFPL apport"}
    assert set(documents["DOC-043"].structures) == {"SPFPL apport"}


def test_seed_catalog_scm_satellites_scope_is_limited_to_scm_docx_batch() -> None:
    catalog = build_seed_catalog()

    scm_documents = [
        document
        for document in catalog
        if document.doc_id in {"DOC-026", "DOC-027", "DOC-028", "DOC-030"}
    ]

    assert len(scm_documents) == 4
    for document in scm_documents:
        assert set(document.structures) == {"SCM"}
        assert document.general_condition == (
            "dossier.structure == SCM et dossier.options.scm_satellites == true"
        )
        assert document.source_path.endswith(".docx")

    liste_depenses = next(document for document in scm_documents if document.doc_id == "DOC-030")
    assert any(
        "liste_depenses_communes" in condition
        for condition in liste_depenses.specific_conditions
    )


def test_seed_catalog_acte_cession_actions_scope_is_limited_to_spfpl_cession() -> None:
    catalog = build_seed_catalog()

    acte = next(document for document in catalog if document.doc_id == "DOC-029")

    assert set(acte.structures) == {"SPFPL cession"}
    assert "operation_spfpl.nature_titres == actions" in acte.specific_conditions
    assert acte.source_path == (
        "project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx"
    )


def test_seed_catalog_scm_cession_scope_is_limited_to_sel_structures() -> None:
    catalog = build_seed_catalog()

    scm_cession_documents = [
        document
        for document in catalog
        if document.doc_id in {"DOC-031", "DOC-032", "DOC-033"}
    ]

    assert len(scm_cession_documents) == 3
    for document in scm_cession_documents:
        assert set(document.structures) == {"SELARL", "SELAS"}
        assert "dossier.options.scm_cession == true" in document.general_condition
        assert document.specification_path == (
            "docs/delivery/lot_05_scm_cession_block_resolution_v1.md"
        )
