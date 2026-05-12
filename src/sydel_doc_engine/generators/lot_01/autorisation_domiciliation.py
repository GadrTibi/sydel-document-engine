from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext


class AutorisationDomiciliationGenerator:
    """Générateur cible du DOC-002.

    L'implémentation est bloquée par l'arbitrage métier sur l'adresse de domiciliation.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        raise NotImplementedError(
            "DOC-002 à implémenter après arbitrage explicite de la règle d'adresse."
        )
