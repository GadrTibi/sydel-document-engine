from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext


class DeclarationNonCondamnationGenerator:
    """Générateur cible du DOC-001.

    L'implémentation réelle est volontairement différée.
    Le document est spécifié, mais le dépôt V1 reste un bootstrap GitHub + Codex.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        raise NotImplementedError(
            "DOC-001 à implémenter dans un ticket dédié après validation de la stratégie de rendu."
        )
