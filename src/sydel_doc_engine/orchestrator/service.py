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
from sydel_doc_engine.generators.lot_02.lettre_avertissement_conjoint import (
    LettreAvertissementConjointGenerator,
)
from sydel_doc_engine.generators.lot_02.lettre_renonciation_associe import (
    LettreRenonciationAssocieGenerator,
)
from sydel_doc_engine.generators.lot_02.pv_nomination_gerant import (
    PvNominationGerantGenerator,
)
from sydel_doc_engine.generators.lot_03.appel_fond_sel import AppelFondSelGenerator
from sydel_doc_engine.generators.lot_03.avenant_contrat_bail import (
    AvenantContratBailGenerator,
)

REGIME_COMMUNAUTAIRE_DOCUMENT_IDS = {"DOC-005", "DOC-006"}
BAIL_AVENANT_DOCUMENT_ID = "DOC-007"
APPEL_FONDS_DOCUMENT_ID = "DOC-008"


class MissingDocumentGeneratorError(RuntimeError):
    pass


def build_lot_01_generator_registry() -> dict[str, DocumentGenerator]:
    return {
        "DOC-001": DeclarationNonCondamnationGenerator(),
        "DOC-002": AutorisationDomiciliationGenerator(),
        "DOC-003": ProcurationGenerator(),
        "DOC-004": PvNominationGerantGenerator(),
        "DOC-005": LettreRenonciationAssocieGenerator(),
        "DOC-006": LettreAvertissementConjointGenerator(),
        "DOC-007": AvenantContratBailGenerator(),
        "DOC-008": AppelFondSelGenerator(),
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

    def select_documents_for_context(
        self,
        ctx: DocumentGenerationContext,
    ) -> list[DocumentDefinition]:
        documents = self.select_documents(ctx.structure)
        return [document for document in documents if _document_enabled_for_context(document, ctx)]

    def generate_documents(self, ctx: DocumentGenerationContext, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths: list[Path] = []
        for document in self.select_documents_for_context(ctx):
            generator = self._generators.get(document.doc_id)
            if generator is None:
                raise MissingDocumentGeneratorError(
                    "Aucun generateur enregistre pour "
                    f"{document.doc_id} ({document.canonical_name})."
                )
            output_paths.append(generator.generate(ctx, output_dir))
        return output_paths


def _document_enabled_for_context(
    document: DocumentDefinition,
    ctx: DocumentGenerationContext,
) -> bool:
    if document.doc_id not in REGIME_COMMUNAUTAIRE_DOCUMENT_IDS:
        if document.doc_id == BAIL_AVENANT_DOCUMENT_ID:
            return _cession_bail_enabled(ctx)
        if document.doc_id == APPEL_FONDS_DOCUMENT_ID:
            return _appel_fonds_enabled(ctx)
        return True
    return bool(ctx.dossier_options and ctx.dossier_options.regime_communautaire)


def _cession_bail_enabled(ctx: DocumentGenerationContext) -> bool:
    return bool(ctx.dossier_options and ctx.dossier_options.cession)


def _appel_fonds_enabled(ctx: DocumentGenerationContext) -> bool:
    if not _cession_bail_enabled(ctx):
        return False
    if ctx.structure != "SELARL":
        return False
    if ctx.cession is None or ctx.cession.type_cabinet is None:
        return False
    return ctx.cession.type_cabinet.strip().lower() == "dentaire"
