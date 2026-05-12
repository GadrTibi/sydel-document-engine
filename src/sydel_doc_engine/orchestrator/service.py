from __future__ import annotations

from collections.abc import Sequence

from sydel_doc_engine.domain.document import DocumentDefinition


class DocumentOrchestrator:
    def __init__(self, catalog: Sequence[DocumentDefinition]) -> None:
        self._catalog = list(catalog)

    def select_documents(self, structure: str | None = None) -> list[DocumentDefinition]:
        if structure is None:
            return list(self._catalog)
        return [document for document in self._catalog if structure in document.structures]
