from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Domiciliation,
    Person,
    Signature,
)
from sydel_doc_engine.orchestrator.service import (
    DocumentOrchestrator,
    MissingDocumentGeneratorError,
)
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _context() -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SELARL",
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
            denomination="DURAND CONSEIL",
            capital="1 000",
            siege=Address(
                num_voie="80",
                voie="avenue Marceau",
                cp="75008",
                ville="Paris",
            ),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee="15 rue du Libre, Lyon 69002",
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 12),
        ),
    )


def test_select_documents_returns_lot_one_universal_documents_for_selarl() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SELARL")

    assert [document.doc_id for document in selected] == ["DOC-001", "DOC-002", "DOC-003"]


def test_generate_documents_creates_three_docx(tmp_path: Path) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    output_paths = orchestrator.generate_documents(_context(), tmp_path)

    assert len(output_paths) == 3
    assert all(path.suffix == ".docx" for path in output_paths)
    assert all(path.is_file() for path in output_paths)


def test_generate_documents_outputs_follow_catalog_order(tmp_path: Path) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    output_paths = orchestrator.generate_documents(_context(), tmp_path)

    assert [path.name for path in output_paths] == [
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
    ]


def test_generate_documents_raises_clear_error_when_generator_is_missing(
    tmp_path: Path,
) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog(), generators={})

    with pytest.raises(MissingDocumentGeneratorError, match="DOC-001"):
        orchestrator.generate_documents(_context(), tmp_path)
