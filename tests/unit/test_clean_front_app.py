from __future__ import annotations

from datetime import date
from pathlib import Path

from streamlit.testing.v1 import AppTest

from sydel_doc_engine.front_app.data_entry import build_clean_data_entry
from sydel_doc_engine.front_app.dossier_selection import dossier_type_by_label
from sydel_doc_engine.front_app.generation import build_clean_generation_plan
from sydel_doc_engine.front_app.legacy_boundary import legacy_boundary_items
from sydel_doc_engine.front_app.routing import clean_front_routes
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    PROFESSION_MEDECIN,
    build_generation_context,
    generate_selarl_dossier,
)
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def test_clean_front_routes_are_minimal() -> None:
    assert [route.label for route in clean_front_routes()] == [
        "Type de dossier",
        "Donnees a saisir",
        "Generation",
    ]


def test_clean_front_selarl_slice_is_generable_for_medecin() -> None:
    dossier_type = dossier_type_by_label("SELARL creation V1")
    data_entry = _valid_selarl_input(PROFESSION_MEDECIN)

    plan = build_clean_generation_plan(dossier_type, data_entry)

    assert plan.can_generate is True
    assert plan.status == "ready"
    assert plan.target_engine_adapter == "front_app.selarl_slice"
    assert plan.document_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-017",
    )
    assert "DOC-006" not in plan.document_codes


def test_clean_front_selarl_slice_switches_statuts_for_dentiste() -> None:
    dossier_type = dossier_type_by_label("SELARL creation V1")
    data_entry = _valid_selarl_input(PROFESSION_DENTISTE)

    plan = build_clean_generation_plan(dossier_type, data_entry)

    assert plan.can_generate is True
    assert "DOC-016" in plan.document_codes
    assert "DOC-017" not in plan.document_codes


def test_clean_front_selarl_slice_adds_doc_005_only_for_regime() -> None:
    dossier_type = dossier_type_by_label("SELARL creation V1")
    data_entry = _valid_selarl_input(PROFESSION_MEDECIN, regime_communautaire=True)

    plan = build_clean_generation_plan(dossier_type, data_entry)

    assert plan.can_generate is True
    assert "DOC-005" in plan.document_codes
    assert "DOC-006" not in plan.document_codes
    assert any(row.doc_code == "DOC-006" and row.status == "reserve" for row in plan.document_rows)


def test_clean_front_selarl_slice_blocks_out_of_scope_cases() -> None:
    dossier_type = dossier_type_by_label("SELARL creation V1")
    data_entry = build_clean_data_entry(
        dossier_type,
        **{
            **_valid_selarl_kwargs(PROFESSION_MEDECIN),
            "cession": True,
        },
    )

    plan = build_clean_generation_plan(dossier_type, data_entry)

    assert plan.can_generate is False
    assert "Cession hors perimetre V1." in plan.blockers


def test_clean_front_selarl_context_selects_only_expected_engine_docs() -> None:
    ctx = build_generation_context(_valid_selarl_input(PROFESSION_DENTISTE))
    selected = DocumentOrchestrator(build_seed_catalog()).select_documents_for_context(ctx)
    selected_codes = {document.doc_id for document in selected}

    assert {"DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-034", "DOC-016"}.issubset(
        selected_codes
    )
    assert "DOC-017" not in selected_codes
    assert "DOC-005" not in selected_codes
    assert "DOC-006" not in selected_codes


def test_clean_front_selarl_generation_smoke(tmp_path: Path) -> None:
    generated = generate_selarl_dossier(
        _valid_selarl_input(PROFESSION_MEDECIN),
        tmp_path / "selarl-medecin",
    )

    assert len(generated.docx_paths) == 6
    assert generated.zip_path.exists()
    assert {path.name for path in generated.docx_paths} >= {
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
        "demande_inscription_ordre.docx",
        "statuts_selarl_medecin.docx",
    }


def test_clean_front_legacy_boundary_is_explicit() -> None:
    items = legacy_boundary_items()
    decisions = {item.decision for item in items}
    components = {item.component for item in items}

    assert {"reused", "legacy_reference", "ignored_by_clean_front", "remove_later"}.issubset(
        decisions
    )
    assert "src/sydel_doc_engine/front_data/" in components
    assert "src/sydel_doc_engine/app/streamlit_app.py" in components


def test_clean_front_entrypoint_does_not_import_legacy_screens() -> None:
    source = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in (
            "src/sydel_doc_engine/front_app/app.py",
            "src/sydel_doc_engine/front_app/shell.py",
            "src/sydel_doc_engine/front_app/selarl_slice.py",
        )
    )

    assert "business_wizard" not in source
    assert "single_document_mode" not in source
    assert "streamlit_app" not in source
    assert "front_internal_tool" not in source
    assert "Technique / diagnostic" not in source
    assert "Document unitaire" not in source
    assert "Debug interne" not in source


def test_clean_front_streamlit_surface_is_not_legacy() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)

    assert [item.value for item in app.subheader] == [
        "Type de dossier",
        "Donnees a saisir",
        "Generation",
    ]
    assert app.selectbox(key="clean_dossier_type").label == "Type de dossier"
    assert app.selectbox(key="clean_dossier_type").value == "SELARL creation V1"
    assert app.button(key="clean_generate_dossier").disabled is True
    assert len(app.radio) == 0
    assert len(app.table) == 0
    assert len(app.expander) == 0
    assert not any(item.label == "Outils internes" for item in app.checkbox)


def _valid_selarl_input(
    profession: str,
    *,
    regime_communautaire: bool = False,
):
    dossier_type = dossier_type_by_label("SELARL creation V1")
    return build_clean_data_entry(
        dossier_type,
        **_valid_selarl_kwargs(
            profession,
            regime_communautaire=regime_communautaire,
        ),
    )


def _valid_selarl_kwargs(
    profession: str,
    *,
    regime_communautaire: bool = False,
) -> dict[str, object]:
    return {
        "dossier_reference": "B-SELARL-001",
        "profession": profession,
        "dossier_unipersonnel": True,
        "regime_communautaire": regime_communautaire,
        "civilite": "Monsieur",
        "prenom": "Jean",
        "nom": "Martin",
        "titre_affichage": "Docteur",
        "date_naissance": date(1984, 4, 12),
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "francaise",
        "nom_pere": "Pierre Martin",
        "nom_mere": "Anne Martin",
        "adresse_num_voie": "10",
        "adresse_voie": "rue Test",
        "adresse_cp": "75001",
        "adresse_ville": "Paris",
        "situation_maritale": "marie",
        "regime_matrimonial": "regime de communaute",
        "numero_ordre": "ORD-123",
        "numero_rpps": "10000000001",
        "departement_ordre": "75",
        "denomination": "SELARL MARTIN",
        "capital_social": "1000",
        "capital_social_lettres": "mille",
        "nb_parts_total": 100,
        "nb_parts_total_lettres": "cent",
        "valeur_nominale_part": "10",
        "valeur_nominale_part_lettres": "dix",
        "siege_num_voie": "20",
        "siege_voie": "avenue du Siege",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "ville_rcs": "Paris",
        "ordre_conseil": "Conseil departemental de l'Ordre de Paris",
        "ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "ordre_cp": "75008",
        "ordre_ville": "Paris",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 26),
        "signature_nombre_exemplaires": "deux",
        "decision_date": date(2026, 5, 26),
        "reunion_date_lettres": "vingt-six mai deux mille vingt-six",
        "reunion_heure": "10 heures",
        "depot_banque_nom": "Banque Test",
        "depot_banque_adresse": "30 boulevard Banque, 75009 Paris",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 decembre",
        "exercice_cloture_premier": "31 decembre 2026",
        "lieu_exercice_adresse": "20 avenue du Siege, 75002 Paris",
        "seuil_achat_materiel": "5000",
        "seuil_emprunt": "10000",
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Claire",
        "conjoint_nom": "Martin",
        "qualite_renoncee": "associe",
        "date_courrier_avertissement": date(2026, 5, 20)
        if regime_communautaire
        else None,
    }
