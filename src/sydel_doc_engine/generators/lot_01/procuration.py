from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext


class ProcurationGenerator:
    """Générateur cible du DOC-003.

    L'implémentation réelle sera branchée après pose des helpers transverses.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        raise NotImplementedError(
            "DOC-003 à implémenter dans un ticket dédié après les helpers communs."
        )
