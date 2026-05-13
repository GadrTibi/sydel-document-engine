from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from sydel_doc_engine.domain.document import DocumentDefinition
from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.base import DocumentGenerator
from sydel_doc_engine.generators.lot_01.autorisation_domiciliation import (
    AutorisationDomiciliationGenerator,
)
from sydel_doc_engine.generators.lot_01.declaration_non_condamnation import (
    DeclarationNonCondamnationGenerator,
)
from sydel_doc_engine.generators.lot_01.procuration import ProcurationGenerator
from sydel_doc_engine.generators.lot_02.pv_nomination_gerant import (
    PvNominationGerantGenerator,
)


class MissingDocumentGeneratorError(RuntimeError):
    pass


def build_lot_01_generator_registry() -> dict[str, DocumentGenerator]:
    return {
        "DOC-001": DeclarationNonCondamnationGenerator(),
        "DOC-002": AutorisationDomiciliationGenerator(),
        "DOC-003": ProcurationGenerator(),
        "DOC-004": PvNominationGerantGenerator(),
    }


class DocumentOrchestrator:
    def __init__(
        self,
        catalog: Sequence[DocumentDefinition],
        generators: Mapping[str, DocumentGenerator] | None = None,
    ) -> None:
        self._catalog = list(catalog)
        self._generators = dict(
            build_lot_01_generator_registry() if generators is None else generators
        )

    def select_documents(self, structure: str | None = None) -> list[DocumentDefinition]:
        if structure is None:
            return list(self._catalog)
        return [document for document in self._catalog if structure in document.structures]

    def generate_documents(self, ctx: DocumentGenerationContext, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths: list[Path] = []
        for document in self.select_documents(ctx.structure):
            generator = self._generators.get(document.doc_id)
            if generator is None:
                raise MissingDocumentGeneratorError(
                    "Aucun generateur enregistre pour "
                    f"{document.doc_id} ({document.canonical_name})."
                )
            output_paths.append(generator.generate(ctx, output_dir))
        return output_paths
