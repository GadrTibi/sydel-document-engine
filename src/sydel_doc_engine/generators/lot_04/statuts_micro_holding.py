from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_civils_common import (
    MICRO_HOLDING_TEMPLATE,
    generate_statuts_civil_docx,
)

# Micro holding (VRAI modele Albane 2026-06-29) : « societe civile de portefeuille a capital
# variable » (26 articles, modele distinct du SCI). Le modele source tokenise vit dans
# project/source_documents/lot_04/ (« Modele statuts micro holding.docx »). L'objet social
# (art. 2) est VERBATIM dans le modele (plus de variante A/B). Le socle civil partage
# (generate_statuts_civil_docx) porte les slices et les block builders specifiques micro
# holding (comparution / apports art. 6 / capital variable art. 7 / signature).


class StatutsMicroHoldingGenerator:
    """Generateur des statuts micro holding (societe civile de portefeuille a capital variable)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        return generate_statuts_civil_docx(ctx, output_dir, MICRO_HOLDING_TEMPLATE)
