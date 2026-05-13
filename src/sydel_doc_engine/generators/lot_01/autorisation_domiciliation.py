from __future__ import annotations

from datetime import date
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import Company, DocumentGenerationContext, Domiciliation
from sydel_doc_engine.rendering.docx_builder import (
    add_framed_title,
    add_paragraph,
    add_signature_block,
    new_document,
)
from sydel_doc_engine.utils.grammar import subject_line

OUTPUT_FILENAME = "autorisation_domiciliation.docx"


class AutorisationDomiciliationGenerator:
    """Générateur cible du DOC-002."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        person = ctx.personne_signataire
        company = _required_company(ctx.societe)
        domiciliation = _required_domiciliation(ctx.domiciliation)

        civilite = _required_text(person.civilite, "personne_signataire.civilite")
        prenom = _required_text(person.prenom, "personne_signataire.prenom")
        nom = _required_text(person.nom, "personne_signataire.nom")
        denomination_societe = _required_text(company.denomination, "societe.denomination")
        capital_social = _required_text(company.capital, "societe.capital")
        adresse_domiciliation = _required_text(
            domiciliation.adresse_domiciliation_affichee,
            "domiciliation.adresse_domiciliation_affichee",
        )
        lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")

        document = new_document()
        _add_title(document)
        _add_paragraph(
            document,
            (
                f"{subject_line(person.genre)} {civilite} {prenom} {nom} autorise la "
                f"domiciliation de la Société {denomination_societe} au capital de "
                f"{capital_social} € en cours de formation, dans les locaux situés au "
                f"{adresse_domiciliation}, pour une durée indéterminée."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
        _add_final_block(
            document,
            lieu_signature=lieu_signature,
            date_signature=_format_date(ctx.signature.date),
            signatory_name=f"{civilite} {prenom} {nom}",
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError("societe est obligatoire pour DOC-002.")
    return company


def _required_domiciliation(domiciliation: Domiciliation | None) -> Domiciliation:
    if domiciliation is None:
        raise ValueError("domiciliation est obligatoire pour DOC-002.")
    return domiciliation


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour DOC-002.")
    return value.strip()


def _format_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def _add_title(document) -> None:
    add_framed_title(document, ["AUTORISATION DE DOMICILIATION"])


def _add_paragraph(
    document,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
) -> None:
    add_paragraph(document, text, alignment=alignment)


def _add_final_block(
    document,
    *,
    lieu_signature: str,
    date_signature: str,
    signatory_name: str,
) -> None:
    add_signature_block(
        document,
        [f"Fait à {lieu_signature}", f"Le {date_signature}", signatory_name],
        framed=True,
    )
