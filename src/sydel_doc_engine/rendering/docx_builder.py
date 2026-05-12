from __future__ import annotations

from docx import Document


def new_document() -> Document:
    """Crée un document DOCX vide.

    Ce helper servira de point d'entrée commun lorsque les générateurs réels seront branchés.
    """
    return Document()
