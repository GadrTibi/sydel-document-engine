from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import (
    BailContext,
    BailParty,
    Company,
    DocumentContext,
    DocumentGenerationContext,
)
from sydel_doc_engine.generators.lot_03.bail_appel_common import (
    DOCUMENT_CODE,
    format_display_date,
    required_text,
    validate_avenant_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    BAIL_COMPACT_STYLE_PROFILE,
    add_article_heading,
    add_framed_title,
    add_paragraph,
    add_party_marker,
    add_signature_table,
    new_document,
)

OUTPUT_FILENAME = "avenant_contrat_bail.docx"


class AvenantContratBailGenerator:
    """Generateur from-scratch de l'avenant au contrat de bail."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_avenant_context(ctx)
        bail = _required_bail(ctx.bail)
        company = _required_company(ctx.societe)
        document_context = _required_document_context(ctx.document)
        bailleur = _required_party(bail.bailleur, "bail.bailleur")
        locataire = _required_party(bail.locataire, "bail.locataire")

        if not bail.societe_en_cours_immatriculation:
            raise ValueError(
                "bail.societe_en_cours_immatriculation doit etre confirme pour "
                f"{DOCUMENT_CODE}."
            )
        if not bail.bailleur_accepte_changement_locataire:
            raise ValueError(
                "bail.bailleur_accepte_changement_locataire doit etre confirme pour "
                f"{DOCUMENT_CODE}."
            )

        docx = new_document(style_profile=BAIL_COMPACT_STYLE_PROFILE)
        add_framed_title(
            docx,
            [
                (
                    "Avenant n°1 au bail du "
                    f"{format_display_date(bail.date_avenant, 'bail.date_avenant')}"
                )
            ],
            style_profile=BAIL_COMPACT_STYLE_PROFILE,
        )
        _add_parties(docx, bailleur, locataire)
        _add_article_1(docx, bail, locataire, company)
        _add_article_2(docx, locataire)
        _add_article_3(docx)
        nombre_exemplaires = required_text(
            document_context.nombre_exemplaires_lettres,
            "document.nombre_exemplaires_lettres",
        )
        add_paragraph(
            docx,
            (
                f"Fait à {required_text(ctx.signature.lieu, 'signature.lieu')} en "
                f"{nombre_exemplaires} exemplaires, le "
                f"{format_display_date(ctx.signature.date, 'signature.date')}"
            ),
        )
        _add_signature_table(docx)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        docx.save(output_path)
        return output_path


def _required_bail(bail: BailContext | None) -> BailContext:
    if bail is None:
        raise ValueError(f"bail est obligatoire pour {DOCUMENT_CODE}.")
    return bail


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def _required_document_context(document_context: DocumentContext | None) -> DocumentContext:
    if document_context is None:
        raise ValueError(f"document est obligatoire pour {DOCUMENT_CODE}.")
    return document_context


def _required_party(party: BailParty | None, field_name: str) -> BailParty:
    # Retours client 2026-06-11 (ticket 3.1) : l'identite du LOCATAIRE est
    # toujours derivee de l'associe unique (nom requis) ; les champs du BAILLEUR
    # non renseignes sont omis de la ligne de partie au lieu de bloquer.
    if party is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if field_name == "bail.locataire":
        required_text(party.nom, f"{field_name}.nom")
    return party


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _display_date_or_empty(value) -> str:
    if value is None:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value).strip()


def _party_identity(party: BailParty, field_name: str) -> str:
    parts = [_clean(party.civilite_affichage), _clean(party.prenom), _clean(party.nom)]
    return " ".join(part for part in parts if part)


def _party_full_line(party: BailParty, field_name: str) -> str:
    # Segments composes uniquement a partir des informations saisies : aucun
    # « ne le , a » incomplet quand un element du bailleur manque.
    segments = [_party_identity(party, field_name)]
    if _clean(party.profession):
        segments.append(_clean(party.profession))
    naissance = _display_date_or_empty(party.date_naissance)
    if naissance:
        ville = _clean(party.ville_naissance)
        segments.append(f"né le {naissance}" + (f", à {ville}" if ville else ""))
    elif _clean(party.ville_naissance):
        segments.append(f"né à {_clean(party.ville_naissance)}")
    if _clean(party.nationalite):
        segments.append(f"de nationalité {_clean(party.nationalite)}")
    if _clean(party.adresse_affichee):
        segments.append(f"demeurant {_clean(party.adresse_affichee)}")
    return ", ".join(segment for segment in segments if segment) + ","


def _add_article_1(
    docx,
    bail: BailContext,
    locataire: BailParty,
    company: Company,
) -> None:
    _add_article_title(docx, "ARTICLE 1 : changement de locataire")
    date_origine = _display_date_or_empty(bail.date_signature_origine)
    date_segment = f" en date du {date_origine}" if date_origine else ""
    profession = _clean(locataire.profession)
    profession_segment = f", ({profession})" if profession else ""
    add_paragraph(
        docx,
        (
            f"Le bail signé{date_segment}, "
            f"a pour locataire {_party_identity(locataire, 'bail.locataire')}"
            f"{profession_segment}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    siege = company.siege
    adresse_siege = required_text(
        siege.adresse_affichee if siege else None,
        "societe.siege.adresse_affichee",
    )
    add_paragraph(
        docx,
        (
            "Le présent avenant donne bail à la société "
            f"{required_text(company.denomination, 'societe.denomination')} en cours "
            "d’immatriculation au RCS "
            f"{required_text(company.ville_rcs, 'societe.rcs_ville')}, domiciliée au "
            f"{adresse_siege}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_article_2(docx, locataire: BailParty) -> None:
    _add_article_title(docx, "ARTICLE 2 : Responsabilité pour une société en cours de formation")
    civilite_courte = _clean(locataire.civilite_courte) or _clean(locataire.civilite_affichage)
    domicile = _clean(locataire.adresse_affichee)
    domicile_segment = f", domicilié {domicile}" if domicile else ""
    add_paragraph(
        docx,
        (
            f"Le {civilite_courte} "
            f"{_clean(locataire.prenom)} "
            f"{required_text(locataire.nom, 'bail.locataire.nom')}"
            f"{domicile_segment}, "
            "engage sa responsabilité pour tous les actes passés au nom de la société jusqu’à "
            "l’immatriculation au RCS."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    add_paragraph(
        docx,
        (
            f"{_party_identity(locataire, 'bail.locataire')} s’engage à fournir au Bailleur un "
            "extrait KBIS une fois que les démarches seront finies."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_article_3(docx) -> None:
    _add_article_title(docx, "ARTICLE 3 : Clauses du bail")
    add_paragraph(
        docx,
        "Le présent avenant ne modifie pas les clauses du bail en cours.",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_parties(docx, bailleur: BailParty, locataire: BailParty) -> None:
    add_paragraph(docx, "Entre les soussign\u00e9s :", style_profile=BAIL_COMPACT_STYLE_PROFILE)
    add_paragraph(
        docx,
        _party_full_line(bailleur, "bail.bailleur"),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        bold=True,
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    add_party_marker(
        docx,
        "Ci-apr\u00e8s d\u00e9sign\u00e9 \u00ab le Bailleur \u00bb",
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    add_paragraph(docx, "ET :", bold=True, style_profile=BAIL_COMPACT_STYLE_PROFILE)
    add_paragraph(
        docx,
        _party_full_line(locataire, "bail.locataire"),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        bold=True,
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    add_party_marker(
        docx,
        "Ci-apr\u00e8s d\u00e9sign\u00e9 \u00ab le Locataire \u00bb",
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    add_paragraph(
        docx,
        "Les parties conviennent de ce qui suit :",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )


def _add_article_title(docx, title: str) -> None:
    add_article_heading(docx, title, style_profile=BAIL_COMPACT_STYLE_PROFILE)


def _add_signature_table(docx) -> None:
    add_signature_table(
        docx,
        [
            ["Le Bailleur", "L\u2019ancien locataire", "Le nouveau locataire"],
        ],
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
