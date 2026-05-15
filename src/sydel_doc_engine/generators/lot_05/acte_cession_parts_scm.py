# ruff: noqa: E501
from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    acte_signature_prestataire,
    add_body_paragraph,
    add_heading,
    address_display,
    associe_display,
    cedant_display,
    cessionnaire_forme,
    cessionnaire_representant_fonction,
    conjoint_display,
    format_display_date,
    required_text,
    save_clean_document,
    scm_cedee_address_for_acte,
    scm_cedee_forme,
    validate_acte_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    add_framed_title,
    add_signature_lines,
    new_document,
)

OUTPUT_FILENAME = "acte_cession_parts_scm.docx"


class ActeCessionPartsScmGenerator:
    """Generateur from-scratch de l'acte de cession de parts SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        scm_cession = validate_acte_context(ctx)
        scm_cedee = scm_cession.scm_cedee
        cessionnaire = scm_cession.cessionnaire
        cedant = scm_cession.cedant
        parts_cedees = scm_cession.parts_cedees
        prix = scm_cession.prix
        if (
            scm_cedee is None
            or cessionnaire is None
            or cedant is None
            or parts_cedees is None
            or prix is None
            or cessionnaire.representant is None
        ):
            raise ValueError("scm_cession est incomplet pour l'acte de cession SCM.")

        cedant_name = cedant_display(cedant)
        document = new_document()
        add_framed_title(document, ["CESSION DES PARTS", "DE LA SOCIETE CIVILE DE MOYENS"])

        add_body_paragraph(document, "Entre les soussignés :", bold=True)
        add_body_paragraph(
            document,
            (
                f"{cedant_name}, {required_text(cedant.profession, 'scm_cession.cedant.profession')}, "
                f"né le {format_display_date(cedant.date_naissance, 'scm_cession.cedant.date_naissance')} "
                f"à {required_text(cedant.ville_naissance, 'scm_cession.cedant.ville_naissance')} "
                f"({required_text(cedant.departement_naissance, 'scm_cession.cedant.departement_naissance')}), "
                f"de nationalité {required_text(cedant.nationalite, 'scm_cession.cedant.nationalite')}, "
                f"demeurant {required_text(cedant.adresse_affichee, 'scm_cession.cedant.adresse_affichee')}, "
                f"{required_text(cedant.situation_maritale, 'scm_cession.cedant.situation_maritale')} avec {conjoint_display(cedant)}. "
                f"Inscrit au Tableau de l'ordre départemental des {_profession_ordre(ctx, cedant)} "
                f"du {required_text(cedant.ordre.departemental if cedant.ordre else None, 'scm_cession.cedant.ordre.departemental')} "
                f"sous le numéro {required_text(cedant.ordre.numero if cedant.ordre else None, 'scm_cession.cedant.ordre.numero')} "
                f"et sous le numéro RPPS {required_text(cedant.numero_rpps, 'scm_cession.cedant.numero_rpps')}."
            ),
        )
        add_body_paragraph(document, "Soussigné de première part, ci-après dénommé « LE CÉDANT »,")
        add_body_paragraph(document, "ET :", bold=True)
        add_body_paragraph(document, required_text(cessionnaire.denomination, "scm_cession.cessionnaire.denomination"))
        add_body_paragraph(
            document,
            (
                f"{cessionnaire_forme(ctx, cessionnaire)} au capital de "
                f"{required_text(cessionnaire.capital_social, 'scm_cession.cessionnaire.capital_social')}"
                f"{' €' if ctx.structure == 'SELARL' else ''}"
            ),
        )
        add_body_paragraph(
            document,
            f"Ayant son siège au {address_display(cessionnaire.siege, 'scm_cession.cessionnaire.siege')}",
        )
        add_body_paragraph(
            document,
            f"En cours d'immatriculation au RCS de {required_text(cessionnaire.ville_rcs, 'scm_cession.cessionnaire.ville_rcs')}",
        )
        add_body_paragraph(
            document,
            (
                f"Représentée par son {cessionnaire_representant_fonction(ctx, cessionnaire)}, "
                f"{cedant_name}, domicilié en cette qualité audit siège."
            ),
        )
        add_body_paragraph(document, "Soussignée de seconde part, ci-après dénommé « LE CESSIONNAIRE »,")
        add_body_paragraph(
            document,
            f"Ont procédé de la manière suivante à la cession des parts de la Société {required_text(scm_cedee.denomination, 'scm_cession.scm_cedee.denomination')}.",
        )
        add_body_paragraph(document, "Ci-après dénommé « LA SOCIETE »,")

        add_heading(document, "IL EST PREALABLEMENT EXPOSE CE QUI SUIT :")
        add_body_paragraph(
            document,
            (
                f"Par les présentes, {cedant_name} cède à la "
                f"{required_text(cessionnaire.denomination, 'scm_cession.cessionnaire.denomination')}, "
                f"{parts_cedees.nb} parts de la {required_text(scm_cedee.denomination, 'scm_cession.scm_cedee.denomination')}, telle que définie ci-après."
            ),
        )
        add_body_paragraph(
            document,
            (
                f"La Société {required_text(scm_cedee.denomination, 'scm_cession.scm_cedee.denomination')}, dont les parts cédées sont l'objet de la présente cession, est une "
                f"{scm_cedee_forme(ctx, scm_cedee)}, au capital de "
                f"{required_text(scm_cedee.capital_social, 'scm_cession.scm_cedee.capital_social')}"
                f"{' €' if ctx.structure == 'SELARL' else ''}, divisé en {scm_cedee.nb_parts_total} parts sociales, dont le siège est situé "
                f"{scm_cedee_address_for_acte(ctx, scm_cedee, cessionnaire)}, immatriculée au RCS de "
                f"{required_text(scm_cedee.ville_rcs, 'scm_cession.scm_cedee.ville_rcs')} sous le n° "
                f"{required_text(scm_cedee.numero_rcs, 'scm_cession.scm_cedee.numero_rcs')} et dont les cogérants sont "
                f"{_cogerants_display(scm_cession)}."
            ),
        )
        _add_origin_property(document, scm_cession)
        _add_declarations_and_cession(document, scm_cession, cedant_name)
        _add_price_and_payment(document, ctx, scm_cession, cedant_name)
        _add_source_tail(document, ctx, scm_cession)
        add_body_paragraph(document, f"Fait à {ctx.signature.lieu},")
        add_body_paragraph(
            document,
            f"En {required_text(scm_cession.nombre_exemplaires_lettres, 'scm_cession.nombre_exemplaires_lettres')} exemplaires originaux,",
        )
        add_body_paragraph(document, f"Le {scm_cession.date_acte_affichee or ''}")
        add_signature_lines(
            document,
            [
                f"{cedant_name}",
                f"{required_text(cessionnaire.denomination, 'scm_cession.cessionnaire.denomination')}",
                "Le cédant",
                (
                    "Représentée par "
                    f"{required_text(cessionnaire.representant.civilite_courte, 'scm_cession.cessionnaire.representant.civilite_courte')} "
                    f"{required_text(cessionnaire.representant.prenom, 'scm_cession.cessionnaire.representant.prenom')} "
                    f"{required_text(cessionnaire.representant.nom, 'scm_cession.cessionnaire.representant.nom')}"
                ),
                "Le cessionnaire",
            ],
        )
        return save_clean_document(document, output_dir, OUTPUT_FILENAME)


def _profession_ordre(ctx: DocumentGenerationContext, cedant) -> str:
    if ctx.structure == "SELARL":
        return "chirurgiens-dentistes"
    return required_text(
        cedant.profession_reglementee_pluriel,
        "scm_cession.cedant.profession_reglementee_pluriel",
    )


def _cogerants_display(scm_cession) -> str:
    scm_cedee = scm_cession.scm_cedee
    if scm_cedee and scm_cedee.cogerants:
        return ", ".join(scm_cedee.cogerants)
    associes = scm_cession.associes_avant_cession
    cedant = scm_cession.cedant
    if cedant is None:
        raise ValueError("scm_cession.cedant est obligatoire.")
    return (
        f"{associe_display(associes[0], 'scm_cession.associes_avant_cession[0]')}, "
        f"{cedant_display(cedant)} et "
        f"{associe_display(associes[2], 'scm_cession.associes_avant_cession[2]')}"
    )


def _add_origin_property(document, scm_cession) -> None:
    add_heading(document, "ORIGINE DE PROPRIETE")
    add_body_paragraph(
        document,
        "Aux termes des statuts le capital social de la SOCIETE est actuellement détenu comme suit :",
    )
    for index, associe in enumerate(scm_cession.associes_avant_cession, start=1):
        parts = associe.parts
        if parts is None:
            raise ValueError("scm_cession.associes_avant_cession.parts est obligatoire.")
        add_body_paragraph(
            document,
            f"{index}° {associe_display(associe, f'scm_cession.associes_avant_cession[{index - 1}]')}, représentant {parts.nb} parts sociales",
        )
    add_body_paragraph(
        document,
        f"{cedant_display(scm_cession.cedant)}, le CEDANT, déclare qu'il est propriétaire des parts sociales pour les avoir souscrites à la constitution de la société.",
    )


def _add_declarations_and_cession(document, scm_cession, cedant_name: str) -> None:
    add_heading(document, "CECI EXPOSE, IL EST CONVENU CE QUI SUIT :")
    add_heading(document, "DECLARATIONS")
    for text in [
        "Le CEDANT déclare :",
        "- qu'il dispose de la pleine capacité juridique d'aliéner ;",
        "- qu'il est résident français ;",
        "- que les parts sociales cédées sont libres de tout nantissement et de tout droit quelconque ;",
        "- que les parts sociales cédées sont des biens propres.",
    ]:
        add_body_paragraph(document, text)
    add_heading(document, "CESSION")
    add_body_paragraph(
        document,
        (
            f"Par les présentes, {cedant_name}, soussigné de première part, cède et transporte sous les garanties ordinaires de fait ou de droit à la société "
            f"{required_text(scm_cession.cessionnaire.denomination, 'scm_cession.cessionnaire.denomination')}, soussignée de deuxième part qui accepte la pleine propriété de "
            f"{scm_cession.parts_cedees.nb} parts de la {required_text(scm_cession.scm_cedee.denomination, 'scm_cession.scm_cedee.denomination')}, numérotées de "
            f"{required_text(scm_cession.parts_cedees.plage, 'scm_cession.parts_cedees.plage')} inclus."
        ),
    )
    add_heading(document, "PROPRIÉTÉ - JOUISSANCE")
    for text in [
        "Le cessionnaire sera propriétaire des parts cédées et en aura la jouissance à compter de ce jour.",
        "En conséquence, il aura seul droit à tous les dividendes qui seront mis en distribution sur ces parts après cette date.",
        "Le cessionnaire sera subrogé dans tous les droits et obligations attachés à l'actif cédé.",
    ]:
        add_body_paragraph(document, text)


def _add_price_and_payment(
    document,
    ctx: DocumentGenerationContext,
    scm_cession,
    cedant_name: str,
) -> None:
    prix = scm_cession.prix
    add_heading(document, "PRIX")
    add_body_paragraph(
        document,
        (
            "La présente cession est consentie et acceptée moyennant le prix de "
            f"{required_text(prix.unitaire_lettres, 'scm_cession.prix.unitaire_lettres')} "
            f"({required_text(prix.unitaire, 'scm_cession.prix.unitaire')}) euros par part cédée, soit le prix global de "
            f"{required_text(prix.global_lettres, 'scm_cession.prix.global_lettres')} "
            f"({required_text(prix.global_, 'scm_cession.prix.global')}) euros, payé comptant ce jour à {cedant_name} qui lui reconnaît et lui en donne bonne et valable quittance."
        ),
    )
    add_heading(document, "PAIEMENT DU PRIX")
    add_body_paragraph(document, "Le prix est payé au moyen d'un prêt bancaire, établi par acte séparé, par virement.")
    credit = scm_cession.credit_vendeur
    if credit is not None and credit.actif:
        add_body_paragraph(document, _credit_vendeur_intro(ctx, credit))
        for text in [
            "Le Vendeur dispense l'Acquéreur de consentir une garantie sur le paiement du crédit-vendeur.",
            "Tout défaut de paiement, même partiel, de toute échéance mensuelle emportera l'exigibilité anticipée du solde du crédit-vendeur dû à cette date, en principal et intérêts, si bon semble au Vendeur, sans qu'il soit besoin d'aucune mise en demeure ou autre formalité.",
            _credit_vendeur_retard(ctx, credit),
            "A défaut de paiement par l'acquéreur, le Cédant pourra faire ordonner par la Justice, la cession des parts sociales, objet des présentes pour lui garantir le paiement du prix.",
        ]:
            add_body_paragraph(document, text)


def _credit_vendeur_intro(ctx: DocumentGenerationContext, credit) -> str:
    if ctx.structure == "SELAS":
        return (
            "Et pour partie d'un crédit-vendeur à hauteur de "
            f"{required_text(credit.montant, 'scm_cession.credit_vendeur.montant')} que les parties ont convenues de solder dans un délai maximum de "
            f"{required_text(credit.duree, 'scm_cession.credit_vendeur.duree')} à compter de la signature des présentes. Le montant annuel en principal du crédit-vendeur sera productif d'un intérêt annuel non capitalisé au taux de "
            f"{required_text(credit.taux, 'scm_cession.credit_vendeur.taux')}."
        )
    return (
        "Et pour partie d'un crédit-vendeur à hauteur de "
        f"{required_text(credit.montant, 'scm_cession.credit_vendeur.montant')} euros que les parties ont convenu de solder dans un délai maximum de "
        f"{required_text(credit.duree, 'scm_cession.credit_vendeur.duree')} ans à compter de la signature des présentes. Le montant annuel en principal du crédit-vendeur sera productif d'un intérêt annuel non capitalisé au taux de "
        f"{required_text(credit.taux, 'scm_cession.credit_vendeur.taux')} %."
    )


def _credit_vendeur_retard(ctx: DocumentGenerationContext, credit) -> str:
    if ctx.structure == "SELAS":
        return (
            "Au terme du délai de "
            f"{required_text(credit.duree, 'scm_cession.credit_vendeur.duree')}, les sommes restant dues porteront de plein droit et sans mise en demeure préalable, un intérêt de retard calculé sur la base du Taux d'intérêt légal publié par la Banque de France, majoré de "
            f"{required_text(credit.majoration_interet_retard, 'scm_cession.credit_vendeur.majoration_interet_retard')} à compter de la date d'échéance de ladite fraction et jusqu'à son paiement effectif. Les intérêts seront calculés au jour le jour et tout mois commencé sera dû en entier."
        )
    return (
        "Au terme du délai de "
        f"{required_text(credit.duree, 'scm_cession.credit_vendeur.duree')} ans, les sommes restant dues porteront de plein droit et sans mise en demeure préalable, un intérêt de retard calculé sur la base du Taux d'intérêt légal publié par la Banque de France, majoré de 3 points à compter de la date d'échéance de ladite fraction et jusqu'à son paiement effectif. Les intérêts seront calculés au jour le jour et tout mois commencé sera dû en entier."
    )


def _add_source_tail(document, ctx: DocumentGenerationContext, scm_cession) -> None:
    sections = [
        (
            "DISPENSE DE GARANTIE D'ACTIF ET DE PASSIF",
            [
                "L'Acquéreur reconnaît avoir eu accès à tout renseignement, et renonce expressément et irrévocablement au bénéfice de toute garantie d'actif et de passif sur les parts cédées, ceci étant une condition substantielle à la conclusion des présentes sans laquelle le Vendeur n'aurait pas contracté.",
                "Les Parties déclarent avoir pris tout renseignement quant aux conséquences de la présente dispense de garantie d'actif et de passif et déclarent en faire leur affaire personnelle. En conséquence, les Parties donnent décharge pure et simple, entière et définitive et sans réserve au Rédacteur en ce qui concerne lesdites conséquences.",
                "Les Parties déclarent en outre faire leur affaire personnelle de l'intégralité des déclarations afférentes à la présente cession.",
            ],
        ),
        (
            "DÉCLARATIONS GÉNÉRALES",
            [
                "Les soussignés de première et seconde part déclarent, chacun en ce qui le concerne :",
                "qu'ils ont la pleine capacité civile pour s'obliger dans le cadre des présentes et de leurs suites et, plus spécialement, qu'ils ne font pas présentement l'objet d'une procédure collective dans le cadre de la loi du 13 juillet 1967 ou de celle du 25 janvier 1985, ni ne sont susceptibles de l'être en raison de leurs professions et fonctions, ni ne sont en état de cessation de paiements ou déconfiture ;",
                "et qu'ils sont résidents français au sens de la réglementation des relations financières avec l'étranger.",
                "Le soussigné de première part déclare :",
                "qu'il n'existe de son chef ou de celui des précédents propriétaires des parts cédées, aucune restriction d'ordre légal ou contractuel à la libre disposition de celles-ci, notamment par suite de promesses ou offres consenties à des tiers ou de saisies ;",
                "que les parts cédées sont libres de tout nantissement ou promesse de nantissement ;",
                "que la société dont les parts sont présentement cédées n'est pas en cessation de paiements, ni n'a fait l'objet d'une procédure de règlement amiable des entreprises en difficulté ou de redressement et liquidation judiciaire.",
            ],
        ),
        (
            "DÉCLARATION POUR L'ENREGISTREMENT",
            [
                "Pour la perception des droits d'enregistrement, le cédant atteste que les parts, objet de la présente cession, n'assurent pas la jouissance de droits immobiliers.",
                "Le cessionnaire s'engage à supporter tous les frais et droits d'enregistrement relatifs à la cession.",
            ],
        ),
        (
            "FORMALITÉS ET PUBLICITÉ",
            [
                "La présente cession sera signifiée à la société conformément aux dispositions de l'article 1690 du Code Civil. Toutefois, cette signification pourra être remplacée par le dépôt d'un original du présent acte au siège social contre remise par la gérance d'une attestation de ce dépôt.",
                "La gérance de la société se voit confier tous les pouvoirs en vue de remplir les formalités de publicité.",
            ],
        ),
        (
            "AFFIRMATION DE SINCERITE",
            [
                "Les parties affirment sous les peines édictées par l'article 1837 du Code Général des Impôts que le présent acte exprime l'intégralité du prix convenu.",
            ],
        ),
        (
            "COMMUNICATION DU PRESENT CONTRAT AU CONSEIL DE L'ORDRE",
            [
                "Le présent contrat sera, sans délai, communiqué au Conseil départemental de l'Ordre en vue de ses observations éventuelles.",
            ],
        ),
        (
            "FRAIS",
            [
                "Les frais, droits et honoraires des présentes et ceux qui en seront la conséquence, seront supportés par le cessionnaire, qui s'y oblige.",
            ],
        ),
        (
            "CONVENTION SUR LA PREUVE - SIGNATURE ELECTRONIQUE",
            [
                "Les Parties consentent expressément la faculté de procéder à la signature du présent acte par le système de signature électronique. Les Parties renoncent en conséquence expressément à signer et obtenir un quelconque acte original de ce dernier.",
                "Les Parties reconnaissent que le présent acte, tel que signé par voie électronique, constitue une preuve valable permettant d'apprécier les droits, les obligations et responsabilités des Parties et le consentement de leurs signataires.",
                f"Le présent acte est signé par chacune des Parties dans le cadre du processus de signature électronique via le service {acte_signature_prestataire(ctx, scm_cession)}.",
            ],
        ),
    ]
    for heading, paragraphs in sections:
        add_heading(document, heading)
        for text in paragraphs:
            add_body_paragraph(document, text)
