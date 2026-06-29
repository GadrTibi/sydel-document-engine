"""Tests PLAN / wiring SASU Holding (nouveau type, modele officiel Albane 2026-06-29).

Verifie le cablage end-to-end du type SASU_HOLDING (SAS unipersonnelle, holding patrimoniale
generaliste, DISTINCTE de la « SAS / SPFPL medecins ») :
- le type est enregistre au front (type_registry) ;
- le bundle de creation liste les doc_ids attendus (statuts DOC-048 + tronc commun) ;
- le contexte construit route bien le statuts DOC-048 (et PAS le DOC-015 SAS medecins) ;
- la generation reelle produit les pieces du bundle sans token residuel ;
- la SAS / SPFPL medecins existante (DOC-015) n'est PAS impactee.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from sydel_doc_engine.front_app import sasu_holding_slice
from sydel_doc_engine.front_app.type_registry import registered_types
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _payload() -> dict[str, object]:
    return {
        "denomination": "MLG",
        "forme_sociale": "Société par actions simplifiée unipersonnelle",
        "siege": "5 Allée de la Clarté, 56700 KERVIGNAC",
        "siege_num": "5",
        "siege_voie": "Allée de la Clarté",
        "siege_cp": "56700",
        "siege_ville": "KERVIGNAC",
        "capital_social": "1000",
        "nb_actions": 10000,
        "civilite": "Monsieur",
        "prenom": "Malo",
        "nom": "LE GUEN",
        "genre": None,  # derive par le slice
        "date_naissance": "1 janvier 1990",
        "date_naissance_iso": date(1990, 1, 1),
        "ville_naissance": "Lorient",
        "nationalite": "française",
        "adresse": "5 Allée de la Clarté, 56700 KERVIGNAC",
        "adresse_num": "5",
        "adresse_voie": "Allée de la Clarté",
        "adresse_cp": "56700",
        "adresse_ville": "KERVIGNAC",
        "nom_pere": "LE GUEN",
        "nom_mere": "MARTIN",
        "mandataire_prenom": "",
        "mandataire_nom": "",
        "banque_nom": "HSBC",
        "signature_lieu": "KERVIGNAC",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 décembre",
        "date_cloture": "le 31 décembre 2026",
        "signature_date": date(2025, 11, 13),
    }


def test_sasu_holding_registered_type() -> None:
    by_key = {item.key: item for item in registered_types()}
    assert "sasu_holding_v1" in by_key
    rt = by_key["sasu_holding_v1"]
    assert rt.structure == "SASU_HOLDING"
    assert rt.slice_module == "sydel_doc_engine.front_app.sasu_holding_slice"
    assert rt.generation_enabled is True
    # La SAS / SPFPL medecins existante reste presente et intacte.
    assert "sas_spfpl_medecins_v1" in by_key
    assert by_key["sas_spfpl_medecins_v1"].structure == "SAS"


def test_sasu_holding_bundle_codes() -> None:
    # Bundle complet (6 pieces) = statuts (DOC-048) + tronc commun (DNC/domic/procuration)
    # + PV remuneration president (DOC-049) + liste des souscripteurs (DOC-050).
    assert sasu_holding_slice.SASU_HOLDING_BUNDLE_CODES == (
        "DOC-048",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-049",
        "DOC-050",
    )
    plan = sasu_holding_slice.build_sasu_holding_plan(_payload())
    assert plan.can_generate, plan.blockers
    assert plan.document_codes == (
        "DOC-048",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-049",
        "DOC-050",
    )


def test_sasu_holding_context_routes_doc_048_not_sas_medecins() -> None:
    ctx = sasu_holding_slice.build_generation_context(_payload())
    assert ctx.structure == "SASU_HOLDING"
    assert ctx.statuts_sasu_holding is not None
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    selected = {doc.doc_id for doc in orchestrator.select_documents_for_context(ctx)}
    # Le statuts SASU Holding est selectionne ; le statuts SAS / SPFPL medecins NON.
    assert "DOC-048" in selected
    assert "DOC-015" not in selected
    # Tronc commun + 2 satellites generalistes presents.
    assert {"DOC-001", "DOC-002", "DOC-003", "DOC-049", "DOC-050"} <= selected
    # Les satellites SPFPL medecins (DOC-023 / DOC-024) NE sont PAS selectionnes.
    assert "DOC-023" not in selected
    assert "DOC-024" not in selected


def test_sasu_holding_generates_bundle(tmp_path: Path) -> None:
    result = sasu_holding_slice.generate_dossier(_payload(), tmp_path)
    names = {p.name for p in result.docx_paths}
    assert "statuts_sasu_holding.docx" in names
    assert "pv_remuneration_president_sasu_holding.docx" in names
    assert "liste_souscripteurs_sasu_holding.docx" in names
    # 6 pieces du bundle (statuts + tronc commun + 2 satellites generalistes) generees.
    assert len(result.docx_paths) == 6
    assert result.zip_path is not None and result.zip_path.exists()
