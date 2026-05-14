from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Associe,
    CapitalContext,
    Company,
    DecisionContext,
    DirigeantNomine,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    Person,
    ReunionContext,
    Signature,
)
from sydel_doc_engine.orchestrator.service import (
    DocumentOrchestrator,
    MissingDocumentGeneratorError,
)
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _context(structure: str = "SELARL") -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
            adresse_perso=Address(
                num_voie="12",
                voie="rue des Lilas",
                cp="75008",
                ville="Paris",
            ),
            date_naissance=date(1990, 2, 3),
            nationalite="francaise",
            nom_pere="Pierre Durand",
            nom_mere="Anne Martin",
            fonction_dirigeant="President",
        ),
        societe=Company(
            forme_sociale="SELARL",
            forme_sociale_affichage="SELARL",
            forme_sociale_libelle_long="société d'exercice libéral à responsabilité limitée",
            denomination="DURAND CONSEIL",
            capital="1 000",
            capital_social="1 000",
            capital_variable=True,
            siege=Address(
                num_voie="80",
                voie="avenue Marceau",
                cp="75008",
                ville="Paris",
            ),
            ville_rcs="Paris",
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee="15 rue du Libre, Lyon 69002",
        ),
        decision=DecisionContext(date="13 mai 2026"),
        reunion=ReunionContext(date_lettres="treize mai deux mille vingt-six", heure="10 heures"),
        capital=CapitalContext(
            nb_parts_total=100,
            valeur_nominale_part="1",
        ),
        associes=[
            Associe(
                genre=Gender.MASCULIN,
                civilite_affichage="Monsieur",
                prenom="Jean",
                nom="Durand",
                nb_parts=100,
            )
        ],
        dirigeant_nomine=DirigeantNomine(
            genre=Gender.MASCULIN,
            civilite_affichage="Monsieur",
            prenom="Jean",
            nom="Durand",
            date_naissance=date(1990, 2, 3),
            ville_naissance="Paris",
            departement_naissance="Paris",
            nationalite="francaise",
            adresse_personnelle=Address(
                num_voie="12",
                voie="rue des Lilas",
                cp="75008",
                ville="Paris",
            ),
            fonction_affichage="gérant",
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 12),
            nombre_exemplaires="3",
        ),
    )


def test_select_documents_for_selarl_includes_pv_nomination_gerant() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SELARL")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-005",
        "DOC-006",
        "DOC-007",
        "DOC-008",
        "DOC-009",
        "DOC-010",
        "DOC-011",
        "DOC-012",
        "DOC-013",
        "DOC-014",
    ]


def test_select_documents_for_sci_includes_pv_nomination_gerant() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SCI")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    ]


def test_select_documents_for_sas_excludes_pv_nomination_gerant() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SAS")

    assert [document.doc_id for document in selected] == ["DOC-001", "DOC-002", "DOC-003"]


def test_generate_documents_creates_docx_for_selected_documents(tmp_path: Path) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    output_paths = orchestrator.generate_documents(_context(), tmp_path)

    assert len(output_paths) == 4
    assert all(path.suffix == ".docx" for path in output_paths)
    assert all(path.is_file() for path in output_paths)
    assert tmp_path / "pv_nomination_gerant.docx" in output_paths
    assert tmp_path / "lettre_renonciation_associe.docx" not in output_paths
    assert tmp_path / "lettre_avertissement_conjoint.docx" not in output_paths


def test_generate_documents_outputs_follow_catalog_order(tmp_path: Path) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    output_paths = orchestrator.generate_documents(_context(), tmp_path)

    assert [path.name for path in output_paths] == [
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
    ]


def test_generate_documents_raises_clear_error_when_generator_is_missing(
    tmp_path: Path,
) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog(), generators={})

    with pytest.raises(MissingDocumentGeneratorError, match="DOC-001"):
        orchestrator.generate_documents(_context(), tmp_path)
