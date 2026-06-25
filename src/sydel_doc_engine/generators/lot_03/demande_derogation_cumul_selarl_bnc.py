from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import Company, DocumentGenerationContext, Person
from sydel_doc_engine.generators.lot_03.derogations_common import (
    CUMUL_SEL_BNC,
    MANUAL_BLANK,
    format_display_date,
    require_company,
    require_company_inscription,
    require_derogation_context,
    require_person_contact,
    require_structure,
    required_text,
)
from sydel_doc_engine.rendering.docx_builder import (
    DEROGATION_CUMUL_STYLE_PROFILE,
    add_checkbox_line,
    add_form_section_heading,
    add_italic_instruction,
    add_notice_box,
    add_paragraph,
    new_document,
)

OUTPUT_FILENAME = "demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx"


class DemandeDerogationCumulSelarlBncGenerator:
    """Generateur partiel de la demande de cumul SELARL / BNC."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        require_structure(ctx, selarl_only=True)
        require_derogation_context(ctx, CUMUL_SEL_BNC)
        company = require_company(ctx)

        docx = new_document(style_profile=DEROGATION_CUMUL_STYLE_PROFILE)
        _add_header(docx)
        _add_principle_notice(docx)
        _add_declarant(docx, ctx.personne_signataire, company)
        _add_company(docx, company)
        _add_lieux_exercice(docx, company)
        _add_motifs(docx)
        _add_certification(docx, ctx)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        docx.save(output_path)
        return output_path


def _add_header(docx) -> None:
    add_paragraph(
        docx,
        "Demande de cumul d'exercices en société d'exercice libéral (SEL)",
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
    )
    add_paragraph(docx, "et à titre individuel", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    add_paragraph(
        docx,
        "(Articles R.4113-3 et R.4127-85 du Code de la santé publique)",
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
    )


def _add_declarant(docx, signataire: Person, company: Company) -> None:
    contact = require_person_contact(signataire)
    numero_ordre = required_text(
        signataire.numero_inscription_ordre,
        "personne_signataire.numero_inscription_ordre",
    )
    qualification = required_text(
        signataire.qualification_principale,
        "personne_signataire.qualification_principale",
    )
    add_form_section_heading(docx, "Identification du déclarant")
    add_paragraph(docx, "Demande formulée par le Docteur :")
    add_paragraph(docx, f"Nom : {required_text(signataire.nom, 'personne_signataire.nom')}")
    add_paragraph(
        docx,
        f"Prénom : {required_text(signataire.prenom, 'personne_signataire.prenom')}",
    )
    inscription = require_company_inscription(company)
    add_paragraph(
        docx,
        (
            "Inscrit au Tableau du Conseil départemental de : "
            f"{required_text(inscription.ville, 'societe.inscription_ordre.ville')}"
        ),
    )
    add_paragraph(docx, f"Sous le numéro : {numero_ordre}")
    add_paragraph(docx, f"Qualification principale : {qualification}")
    add_paragraph(
        docx,
        (
            "Autres disciplines exercées (Compétences, DESC du groupe 1, VAE ordinale, "
            f"Capacités, Orientations) : {MANUAL_BLANK}"
        ),
    )
    siege = company.siege
    add_paragraph(docx, f"Adresse de correspondance : {_siege_address(company)}")
    add_paragraph(
        docx,
        f"Code postal : {required_text(siege.cp if siege else None, 'societe.siege.cp')}",
    )
    add_paragraph(
        docx,
        f"Commune : {required_text(siege.ville if siege else None, 'societe.siege.ville')}",
    )
    add_paragraph(docx, "Coordonnées :")
    add_paragraph(
        docx,
        (
            "N° de téléphone : "
            f"{required_text(contact.telephone, 'personne_signataire.contact.telephone')} ; "
            "|__|__|__|__|__|__|__|__|__|__|"
        ),
    )
    add_paragraph(
        docx,
        (
            "Adresse électronique : "
            f"{required_text(contact.email, 'personne_signataire.contact.email')}"
        ),
    )


def _add_company(docx, company: Company) -> None:
    inscription = require_company_inscription(company)
    add_form_section_heading(docx, "Identification de la société (SEL)")
    add_paragraph(
        docx,
        f"Dénomination sociale : {required_text(company.denomination, 'societe.denomination')}",
    )
    add_paragraph(
        docx,
        (
            "Inscrite au Tableau du Conseil départemental de : "
            f"{required_text(inscription.ville, 'societe.inscription_ordre.ville')}"
        ),
    )
    add_paragraph(
        docx,
        (
            "Sous le numéro : "
            f"{required_text(inscription.numero, 'societe.inscription_ordre.numero')}"
        ),
    )
    add_paragraph(docx, f"Adresse du siège social : {_siege_address(company)}")


def _add_lieux_exercice(docx, company: Company) -> None:
    add_form_section_heading(docx, "Lieux d'exercices")
    add_paragraph(docx, "Concernant votre exercice à titre individuel :")
    add_paragraph(docx, "Type d'activité :         Salariée        □ Libérale")
    add_paragraph(docx, f"Adresse : {MANUAL_BLANK}")
    add_paragraph(
        docx,
        f"Temps hebdomadaire consacré (nombre de demi-journées) : {MANUAL_BLANK}",
    )
    add_paragraph(docx, "Concernant votre exercice en SEL :")
    add_paragraph(
        docx,
        (
            "Adresse de la résidence professionnelle de votre SEL (activité principale) : "
            f"{_siege_address(company)}"
        ),
    )
    add_paragraph(
        docx,
        f"Temps hebdomadaire consacré (nombre de demi-journées) : {MANUAL_BLANK}",
    )
    add_paragraph(docx, "Autre(s) site(s) d'exercice déjà déclaré(s) (activité(s) secondaire(s)) :")
    add_checkbox_line(docx, "Aucun")
    add_checkbox_line(docx, f"Oui - nombre de sites : {MANUAL_BLANK}")
    add_paragraph(docx, "1er site distinct :")
    add_paragraph(docx, f"Adresse du site : {MANUAL_BLANK}")
    add_paragraph(
        docx,
        f"Temps hebdomadaire consacré (nombre de demi-journées) : {MANUAL_BLANK}",
    )
    add_paragraph(
        docx,
        (
            "Autres sites distincts (indiquer l'adresse et le temps hebdomadaire "
            f"consacré) : {MANUAL_BLANK}"
        ),
    )
    add_paragraph(docx, "Continuité des soins sur l'ensemble de vos lieux d'exercices :")
    add_paragraph(docx, f"À l'adresse de votre activité à titre individuel : {MANUAL_BLANK}")
    add_paragraph(
        docx,
        (
            "À l'adresse de la résidence professionnelle de votre SEL "
            f"(activité principale) : {MANUAL_BLANK}"
        ),
    )
    add_paragraph(
        docx,
        f"À l'adresse du 1er site distinct de votre SEL (activité secondaire) : {MANUAL_BLANK}",
    )
    add_paragraph(
        docx,
        f"À l'adresse des autres sites de votre SEL (activité(s) secondaire(s)) : {MANUAL_BLANK}",
    )


def _add_motifs(docx) -> None:
    add_form_section_heading(
        docx,
        "Critère(s) sur le(s)quel(s) est fondée la demande de cumul",
    )
    add_italic_instruction(docx, "Toute case cochée doit être accompagnée d'une explication :")
    add_checkbox_line(
        docx,
        (
            "L'exercice dans votre SEL est lié à des techniques médicales nécessitant "
            "un regroupement ou un travail en équipe (motif non applicable dans le cadre "
            "d'une SEL unipersonnelle, si vous êtes le seul associé)"
        ),
    )
    add_checkbox_line(
        docx,
        (
            "L'exercice dans votre SEL est lié à l'acquisition d'équipements ou de "
            "matériels lourds soumis à autorisation"
        ),
    )
    add_checkbox_line(
        docx,
        (
            "L'exercice dans votre SEL nécessite l'acquisition d'équipements ou de "
            "matériels qui justifient des utilisations multiples"
        ),
    )


def _add_certification(docx, ctx: DocumentGenerationContext) -> None:
    prenom = required_text(ctx.personne_signataire.prenom, "personne_signataire.prenom")
    nom = required_text(ctx.personne_signataire.nom, "personne_signataire.nom")
    add_paragraph(docx, f"Je soussigné(e) Dr {prenom} {nom} certifie :", space_before_pt=10)
    add_paragraph(
        docx,
        (
            "L'exactitude de l'ensemble des informations fournies ou jointes au présent "
            "formulaire et que toute modification de mes conditions d'exercice sera "
            "communiquée au conseil départemental de ma résidence professionnelle,"
        ),
    )
    add_italic_instruction(
        docx,
        (
            "(Le Conseil départemental vous informe que toute déclaration volontairement "
            "inexacte ou incomplète faite au Conseil de l'Ordre par un médecin peut "
            "donner lieu à des poursuites disciplinaires, conformément à l'article "
            "R. 4127-110 du Code de la santé publique)"
        ),
    )
    add_paragraph(
        docx,
        (
            "Que l'ouverture du site n'est pas contraire aux dispositions législatives "
            "et réglementaires."
        ),
    )
    add_paragraph(docx, f"Fait le {format_display_date(ctx.signature.date, 'signature.date')}")
    add_paragraph(docx, f"à {required_text(ctx.signature.lieu, 'signature.lieu')}")
    add_paragraph(docx, "Signature :")
    add_notice_box(
        docx,
        [
            "PIÈCES À JOINDRE AU PRÉSENT FORMULAIRE DE DÉCLARATION",
            "Projet d'acte constitutif ou justificatif utile selon la demande.",
        ],
        style_profile=DEROGATION_CUMUL_STYLE_PROFILE,
    )


def _add_principle_notice(docx) -> None:
    add_notice_box(
        docx,
        [
            (
                "En principe, lorsqu'un médecin décide d'exercer en SEL, il ne peut "
                "cumuler cette activité avec un exercice à titre individuel."
            ),
            (
                "Cependant, une dérogation peut être demandée dans les cas prévus par "
                "les textes applicables."
            ),
        ],
        style_profile=DEROGATION_CUMUL_STYLE_PROFILE,
    )


def _siege_address(company: Company) -> str:
    siege = company.siege
    return required_text(
        siege.adresse_affichee if siege else None,
        "societe.siege.adresse_affichee",
    )
