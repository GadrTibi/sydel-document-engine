from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import (
    Company,
    DerogationContext,
    DerogationRole,
    DocumentGenerationContext,
)
from sydel_doc_engine.generators.lot_03.derogations_common import (
    MANUAL_BLANK,
    MULTI_SITES_SEL,
    optional_display_date,
    require_company,
    require_company_inscription,
    require_derogation_context,
    require_role,
    require_structure,
    required_text,
)
from sydel_doc_engine.rendering.docx_builder import (
    DEROGATION_FORM_STYLE_PROFILE,
    add_checkbox_line,
    add_form_section_heading,
    add_italic_instruction,
    add_paragraph,
    new_document,
)

OUTPUT_FILENAME = "formulaire_derogation_sites_sel_formulaire_a_completer.docx"


class FormulaireDerogationSitesSelGenerator:
    """Generateur partiel du formulaire multi-sites SEL pre-rempli."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        require_structure(ctx)
        derogation = require_derogation_context(ctx, MULTI_SITES_SEL)
        company = require_company(ctx)
        representant = require_role(
            derogation.representant_legal,
            "derogation.representant_legal",
        )
        associe = require_role(derogation.associe_exercant, "derogation.associe_exercant")

        docx = new_document(style_profile=DEROGATION_FORM_STYLE_PROFILE)
        _add_header(docx)
        _add_identification(docx, company, representant, associe)
        _add_site_declare(docx, ctx)
        _add_activity_sections(docx)
        _add_sites_existants(docx, ctx, derogation)
        _add_conditions(docx)
        _add_certification(docx, representant)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        docx.save(output_path)
        return output_path


def _add_header(docx) -> None:
    add_paragraph(
        docx,
        (
            "Déclaration préalable d'ouverture d'un site distinct de la résidence "
            "professionnelle d'une SEL"
        ),
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
    )
    add_italic_instruction(
        docx,
        (
            "À adresser au conseil départemental du lieu où se situe le site au plus tard "
            "deux mois avant le début d'activité"
        ),
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
    )
    add_paragraph(
        docx,
        "Article R4113- 23 du code de la santé publique",
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
    )


def _add_identification(
    docx,
    company: Company,
    representant: DerogationRole,
    associe: DerogationRole,
) -> None:
    inscription = require_company_inscription(company)
    add_form_section_heading(docx, "I - Identification du déclarant")
    add_paragraph(docx, "Société", bold=True)
    add_paragraph(
        docx,
        f"Dénomination de la SEL : {required_text(company.denomination, 'societe.denomination')}",
    )
    add_paragraph(
        docx,
        (
            "Département d'inscription de la SEL : "
            f"{required_text(inscription.departement, 'societe.inscription_ordre.departement')}"
        ),
    )
    add_paragraph(
        docx,
        (
            "N° départemental d'inscription de la SEL : "
            f"{required_text(inscription.numero, 'societe.inscription_ordre.numero')}"
        ),
    )
    add_paragraph(docx, f"Adresse du siège social : {_siege_address(company)}")
    add_paragraph(
        docx,
        (
            "SEL mono disciplinaire de (préciser la qualification principale exercée et/ou "
            f"les autres disciplines exercées) : {MANUAL_BLANK}"
        ),
    )
    add_paragraph(
        docx,
        (
            "SEL pluri disciplinaire de (préciser les qualifications principales exercées "
            f"et/ou les autres disciplines exercées) : {MANUAL_BLANK}"
        ),
    )
    add_paragraph(docx, "Représentant légal de la société", bold=True)
    add_paragraph(
        docx,
        (
            f"Nom : {required_text(representant.nom, 'derogation.representant_legal.nom')}      "
            f"Prénom : {required_text(representant.prenom, 'derogation.representant_legal.prenom')}"
        ),
    )
    add_paragraph(
        docx,
        (
            "Mandat (gérant/président/...) : "
            f"{required_text(representant.fonction, 'derogation.representant_legal.fonction')}"
        ),
    )
    add_paragraph(docx, "N° départemental d'inscription au Tableau de l'Ordre :")
    add_paragraph(docx, "N° de téléphone")
    add_paragraph(docx, "Fixe                                 Mobile")
    email = representant.contact.email if representant.contact else None
    add_paragraph(
        docx,
        (
            "Adresse électronique : "
            f"{required_text(email, 'derogation.representant_legal.contact.email')}"
        ),
    )
    add_paragraph(
        docx,
        "Identification de l'associé/des associés qui exercera/ont sur le nouveau site",
        bold=True,
    )
    add_paragraph(docx, f"Nom : {required_text(associe.nom, 'derogation.associe_exercant.nom')}")
    add_paragraph(
        docx,
        f"Prénom : {required_text(associe.prenom, 'derogation.associe_exercant.prenom')}",
    )
    add_paragraph(docx, "N° départemental d'inscription au Tableau de l'Ordre :")
    add_paragraph(docx, "Conseil départemental d'inscription :")
    qualification = required_text(
        associe.qualification_principale,
        "derogation.associe_exercant.qualification_principale",
    )
    add_paragraph(docx, f"Qualification : {qualification}")


def _add_site_declare(docx, ctx: DocumentGenerationContext) -> None:
    add_form_section_heading(
        docx,
        "II - Adresse complète du site pour lequel la déclaration est faite :",
    )
    if ctx.site_declare and ctx.site_declare.adresse_affichee:
        add_paragraph(docx, ctx.site_declare.adresse_affichee)
    else:
        add_paragraph(docx, MANUAL_BLANK)
    add_paragraph(docx, f"Date prévisionnelle de début d'activité : {_site_declare_date(ctx)}")
    add_italic_instruction(
        docx,
        (
            "(Attention dans le choix de la date, car le Conseil départemental dispose "
            "d'un délai deux mois à compter de la réception de la déclaration pour vous "
            "faire connaître une éventuelle opposition par une décision motivée)."
        ),
    )


def _site_declare_date(ctx: DocumentGenerationContext) -> str:
    if ctx.site_declare is None:
        return MANUAL_BLANK
    return optional_display_date(ctx.site_declare.date_debut_activite)


def _add_activity_sections(docx) -> None:
    add_form_section_heading(
        docx,
        "III- Nature de l'activité envisagée sur le nouveau site :",
    )
    add_paragraph(docx, f"- consultations (décrire): {MANUAL_BLANK}")
    add_paragraph(docx, f"- actes médico techniques (décrire) : {MANUAL_BLANK}")
    add_paragraph(docx, f"- actes chirurgicaux (décrire) : {MANUAL_BLANK}")
    add_paragraph(docx, f"autres : {MANUAL_BLANK}")
    add_paragraph(
        docx,
        f"Temps hebdomadaire consacré (nombre de jours/demi-journées) : {MANUAL_BLANK}",
    )


def _add_sites_existants(
    docx,
    ctx: DocumentGenerationContext,
    derogation: DerogationContext,
) -> None:
    add_form_section_heading(
        docx,
        (
            "IV - Renseignements sur l'activité au lieu de la résidence professionnelle "
            "et le cas échéant, sur les autres sites déjà autorisés"
        ),
    )
    add_paragraph(docx, "Adresse de la résidence professionnelle :")
    add_paragraph(docx, "Autres sites d'exercice :")
    present = _sites_existants_present(derogation)
    add_checkbox_line(docx, "NON", checked=not present)
    add_checkbox_line(docx, "OUI", checked=present)
    nombre_sites = str(len(ctx.sites_existants)) if present else MANUAL_BLANK
    add_paragraph(docx, f"Nombre de sites : {nombre_sites}")
    _add_first_site(docx, ctx, present)
    for index in range(2, 5):
        add_paragraph(docx, f"{index}e site")
        add_paragraph(docx, "Date du début d'activité : ___|___|/|___|___|/|___|___|___|___|")
        add_paragraph(docx, f"Adresse du site : {MANUAL_BLANK}")
        add_paragraph(
            docx,
            f"Temps hebdomadaire consacré (nombre de jours/demi-journées) : {MANUAL_BLANK}",
        )


def _sites_existants_present(derogation: DerogationContext) -> bool:
    if derogation.sites_existants_present is None:
        raise ValueError(
            "derogation.sites_existants_present est obligatoire pour CODE-DEROG-CORE-001."
        )
    return derogation.sites_existants_present


def _add_first_site(docx, ctx: DocumentGenerationContext, present: bool) -> None:
    first_site = ctx.sites_existants[0] if present and ctx.sites_existants else None
    if present and first_site is None:
        raise ValueError(
            "sites_existants[0] est obligatoire lorsque "
            "derogation.sites_existants_present est vrai."
        )
    add_paragraph(docx, "1er site")
    add_paragraph(
        docx,
        (
            "Date du début d'activité : "
            f"{optional_display_date(first_site.date_debut_activite if first_site else None)}"
        ),
    )
    add_paragraph(docx, f"Adresse du site : {_site_address(first_site)}")
    add_paragraph(
        docx,
        "Temps hebdomadaire consacré (nombre de jours/demi-journées) : "
        f"{_site_temps(first_site)}",
    )


def _add_conditions(docx) -> None:
    add_form_section_heading(docx, "V- Conditions de l'exercice")
    add_paragraph(docx, "Qualité et sécurité des soins")
    add_paragraph(docx, "Pour les consultations :")
    add_paragraph(docx, f"- moyens en personnel : {MANUAL_BLANK}")
    add_paragraph(
        docx,
        f"- matériels (décrire le type de matériel existant et/ou prévu) : {MANUAL_BLANK}",
    )
    add_paragraph(docx, "Pour les autres actes :")
    add_paragraph(docx, f"- moyens en personnel : {MANUAL_BLANK}")
    add_paragraph(
        docx,
        f"- matériels (décrire le type de matériel existant et/ou prévu) : {MANUAL_BLANK}",
    )
    add_paragraph(docx, "Continuité des soins")
    add_italic_instruction(
        docx,
        (
            "- dispositions prises pour assurer la continuité des soins sur les différents "
            f"sites : {MANUAL_BLANK}"
        ),
    )
    add_paragraph(docx, "Respect des dispositions du code de déontologie médicale :")
    add_paragraph(docx, f"- informations sur l'environnement de travail : {MANUAL_BLANK}")


def _add_certification(docx, representant: DerogationRole) -> None:
    prenom = required_text(representant.prenom, "derogation.representant_legal.prenom")
    nom = required_text(representant.nom, "derogation.representant_legal.nom")
    add_paragraph(docx, f"Je soussigné Monsieur {prenom} {nom} certifie :", space_before_pt=10)
    add_paragraph(
        docx,
        (
            "l'exactitude de l'ensemble des informations fournies ou jointes au présent "
            "formulaire et que toute modification de mes conditions d'exercice sera "
            "communiquée au conseil départemental de la résidence professionnelle de la SEL,"
        ),
    )
    add_paragraph(
        docx,
        (
            "que l'ouverture du site n'est pas contraire aux dispositions législatives "
            "et réglementaires."
        ),
    )
    add_paragraph(docx, "Fait le ___|___|/|___|___|/|___|___|___|___| à")
    add_paragraph(docx, "Pièces à joindre :")
    add_paragraph(docx, "- toute pièce utile à l'examen de la déclaration")
    add_paragraph(docx, "- le(s) projet(s) de contrat(s) relatifs aux locaux ou aux matériels")


def _siege_address(company: Company) -> str:
    siege = company.siege
    return required_text(
        siege.adresse_affichee if siege else None,
        "societe.siege.adresse_affichee",
    )


def _site_address(first_site) -> str:
    if first_site is None or not first_site.adresse_affichee:
        return MANUAL_BLANK
    return first_site.adresse_affichee


def _site_temps(first_site) -> str:
    if first_site is None or not first_site.temps_hebdomadaire:
        return MANUAL_BLANK
    return first_site.temps_hebdomadaire
