# ruff: noqa: E501

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import (
    Address,
    CessionAcquereur,
    CessionBailProfessionnel,
    CessionCabinet,
    CessionConjoint,
    CessionContext,
    CessionCreditVendeur,
    CessionExercice,
    CessionFinancement,
    CessionPret,
    CessionPrix,
    CessionRepresentant,
    CessionSalarie,
    CessionValidations,
    CessionVendeur,
    DocumentContext,
    DocumentGenerationContext,
)
from sydel_doc_engine.rendering.docx_builder import (
    add_framed_title,
    add_hyphen_list_item,
    add_paragraph,
    add_signature_lines,
    new_document,
)

DOCUMENT_CODE = "CODE-CESSION-CAB-001"

ACTE = "acte"
COMPROMIS = "compromis"
MEDICAL = "medical"
DENTAIRE = "dentaire"
SUPPORTED_STRUCTURES = {"SELARL", "SELAS"}
SUPPORTED_ETAPES = {ACTE, COMPROMIS}
SUPPORTED_CABINET_TYPES = {MEDICAL, DENTAIRE}


@dataclass(frozen=True)
class CessionCabinetVariant:
    etape: Literal["acte", "compromis"]
    type_cabinet: Literal["medical", "dentaire"]
    output_filename: str


def generate_cession_cabinet_docx(
    ctx: DocumentGenerationContext,
    output_dir: Path,
    variant: CessionCabinetVariant,
) -> Path:
    data = _validate_context(ctx, variant)

    docx = new_document()
    _add_title(docx, variant)
    _add_parties(docx, data)
    _add_objet(docx, data, variant)
    _add_declarations(docx)
    _add_consistance(docx, data, variant)
    _add_origine_propriete(docx, data, variant)
    _add_bail(docx, data, variant)
    _add_exercices(docx, data)
    _add_situation_generale(docx, data, variant)
    _add_prix(docx, data)
    _add_financement(docx, data, variant)
    _add_conditions(docx, data, variant)
    _add_droits_et_formalites(docx, data, variant)
    _add_signature(docx, data, variant)
    _add_annexes(docx, data)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / variant.output_filename
    docx.save(output_path)
    return output_path


@dataclass(frozen=True)
class _CessionData:
    ctx: DocumentGenerationContext
    cession: CessionContext
    vendeur: CessionVendeur
    acquereur: CessionAcquereur
    representant: CessionRepresentant
    cabinet: CessionCabinet
    bail: CessionBailProfessionnel
    prix: CessionPrix
    exercices: list[CessionExercice]
    financement: CessionFinancement
    document: DocumentContext
    validations: CessionValidations


def _validate_context(
    ctx: DocumentGenerationContext,
    variant: CessionCabinetVariant,
) -> _CessionData:
    if ctx.structure not in SUPPORTED_STRUCTURES:
        supported = ", ".join(sorted(SUPPORTED_STRUCTURES))
        raise ValueError(f"dossier.structure doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None or not ctx.dossier_options.cession:
        raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    cession = _required_cession(ctx)
    _validate_selection(cession, variant)

    vendeur = _required_vendeur(cession.vendeur)
    acquereur = _required_acquereur(cession.acquereur)
    representant = _required_representant(acquereur.representant)
    cabinet = _required_cabinet(cession.cabinet)
    bail = _required_bail(cession.bail_professionnel)
    prix = _required_prix(cession.prix)
    financement = cession.financement or CessionFinancement()
    document = _required_document(ctx.document)
    validations = cession.validations or CessionValidations()

    exercices = _required_exercices(cession.exercices)
    _validate_arbitrage_blocks(cession, variant, validations)
    _validate_financement(cession, variant, financement)
    _validate_salaries(cession, variant, validations)

    return _CessionData(
        ctx=ctx,
        cession=cession,
        vendeur=vendeur,
        acquereur=acquereur,
        representant=representant,
        cabinet=cabinet,
        bail=bail,
        prix=prix,
        exercices=exercices,
        financement=financement,
        document=document,
        validations=validations,
    )


def _validate_selection(cession: CessionContext, variant: CessionCabinetVariant) -> None:
    type_cabinet = _required_text(cession.type_cabinet, "cession.type_cabinet").lower()
    if type_cabinet not in SUPPORTED_CABINET_TYPES:
        supported = ", ".join(sorted(SUPPORTED_CABINET_TYPES))
        raise ValueError(f"cession.type_cabinet doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if type_cabinet != variant.type_cabinet:
        raise ValueError(
            f"cession.type_cabinet doit etre {variant.type_cabinet} pour {variant.output_filename}."
        )

    etape = _required_text(cession.etape, "cession.etape").lower()
    if etape not in SUPPORTED_ETAPES:
        supported = ", ".join(sorted(SUPPORTED_ETAPES))
        raise ValueError(f"cession.etape doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if etape != variant.etape:
        raise ValueError(f"cession.etape doit etre {variant.etape} pour {variant.output_filename}.")


def _validate_arbitrage_blocks(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    validations: CessionValidations,
) -> None:
    if variant.type_cabinet == MEDICAL and not validations.mentions_bail_medical_validees:
        raise ValueError(
            "cession.validations.mentions_bail_medical_validees doit etre vrai pour "
            f"{DOCUMENT_CODE}."
        )
    if (
        variant.etape == COMPROMIS
        and variant.type_cabinet == MEDICAL
        and not validations.origine_compromis_medical_validee
    ):
        raise ValueError(
            "cession.validations.origine_compromis_medical_validee doit etre vrai pour "
            f"{DOCUMENT_CODE}."
        )
    if variant.etape == COMPROMIS and not validations.date_realisation_compromis_validee:
        raise ValueError(
            "cession.validations.date_realisation_compromis_validee doit etre vrai pour "
            f"{DOCUMENT_CODE}."
        )
    if (
        variant.etape == ACTE
        and variant.type_cabinet == MEDICAL
        and not validations.ligne_contrats_travail_medical_supprimee
    ):
        raise ValueError(
            "cession.validations.ligne_contrats_travail_medical_supprimee doit etre vrai "
            f"pour {DOCUMENT_CODE}."
        )


def _validate_financement(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    financement: CessionFinancement,
) -> None:
    credit_vendeur = financement.credit_vendeur
    if credit_vendeur is not None and credit_vendeur.actif:
        if not (variant.etape == ACTE and variant.type_cabinet == MEDICAL):
            raise ValueError(
                "cession.financement.credit_vendeur.actif est autorise uniquement pour "
                f"l'acte medical {DOCUMENT_CODE}."
            )
        _required_text(credit_vendeur.montant, "cession.financement.credit_vendeur.montant")
        _required_text(credit_vendeur.duree, "cession.financement.credit_vendeur.duree")
        _required_text(credit_vendeur.taux, "cession.financement.credit_vendeur.taux")
        _required_text(
            credit_vendeur.majoration_interet_retard,
            "cession.financement.credit_vendeur.majoration_interet_retard",
        )

    if cession.scm is not None and cession.scm.actif:
        if not (variant.etape == ACTE and variant.type_cabinet == MEDICAL):
            raise ValueError("cession.scm.actif est autorise uniquement pour l'acte medical.")
        _required_text(cession.scm.nb_parts_a_ceder, "cession.scm.nb_parts_a_ceder")


def _validate_salaries(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    validations: CessionValidations,
) -> None:
    if variant.etape == ACTE and variant.type_cabinet == DENTAIRE:
        if cession.salaries:
            if len(cession.salaries) != 2 or not validations.salaries_dentaire_deux_valides:
                raise ValueError(
                    "cession.salaries doit contenir exactement deux salaries valides pour "
                    f"l'acte dentaire {DOCUMENT_CODE}."
                )
            for index, salarie in enumerate(cession.salaries):
                _salarie_label(salarie, index)
        return
    if cession.salaries:
        raise ValueError(
            f"cession.salaries est rendu uniquement pour l'acte dentaire en V1 {DOCUMENT_CODE}."
        )


def _required_cession(ctx: DocumentGenerationContext) -> CessionContext:
    if ctx.cession is None:
        raise ValueError(f"cession est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.cession


def _required_vendeur(vendeur: CessionVendeur | None) -> CessionVendeur:
    if vendeur is None:
        raise ValueError(f"cession.vendeur est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.vendeur.civilite_affichage", vendeur.civilite_affichage),
        ("cession.vendeur.prenom", vendeur.prenom),
        ("cession.vendeur.nom", vendeur.nom),
        ("cession.vendeur.profession", vendeur.profession),
        ("cession.vendeur.date_naissance", vendeur.date_naissance),
        ("cession.vendeur.ville_naissance", vendeur.ville_naissance),
        ("cession.vendeur.nationalite", vendeur.nationalite),
        ("cession.vendeur.adresse_affichee", vendeur.adresse_affichee),
        ("cession.vendeur.situation_maritale", vendeur.situation_maritale),
    ]:
        _required_value(value, field_name)
    return vendeur


def _required_acquereur(acquereur: CessionAcquereur | None) -> CessionAcquereur:
    if acquereur is None:
        raise ValueError(f"cession.acquereur est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.acquereur.denomination_societe", acquereur.denomination_societe),
        ("cession.acquereur.forme_sociale", acquereur.forme_sociale),
        ("cession.acquereur.capital_social", acquereur.capital_social),
        ("cession.acquereur.rcs_ville", acquereur.rcs_ville),
    ]:
        _required_text(value, field_name)
    _required_text(_address_label(acquereur.siege), "cession.acquereur.siege.adresse_affichee")
    return acquereur


def _required_representant(representant: CessionRepresentant | None) -> CessionRepresentant:
    if representant is None:
        raise ValueError(f"cession.acquereur.representant est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.acquereur.representant.civilite_affichage", representant.civilite_affichage),
        ("cession.acquereur.representant.prenom", representant.prenom),
        ("cession.acquereur.representant.nom", representant.nom),
        ("cession.acquereur.representant.fonction", representant.fonction),
    ]:
        _required_text(value, field_name)
    return representant


def _required_cabinet(cabinet: CessionCabinet | None) -> CessionCabinet:
    if cabinet is None:
        raise ValueError(f"cession.cabinet est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.cabinet.adresse_affichee", cabinet.adresse_affichee),
        ("cession.cabinet.adresse_locaux_affichee", cabinet.adresse_locaux_affichee),
        ("cession.cabinet.telephone", cabinet.telephone),
        ("cession.cabinet.description_origine_propriete", cabinet.description_origine_propriete),
    ]:
        _required_value(value, field_name)
    return cabinet


def _required_bail(bail: CessionBailProfessionnel | None) -> CessionBailProfessionnel:
    if bail is None:
        raise ValueError(f"cession.bail_professionnel est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.bail_professionnel.date_bail", bail.date_bail),
        ("cession.bail_professionnel.duree", bail.duree),
        (
            "cession.bail_professionnel.activite_autorisee_affichee",
            bail.activite_autorisee_affichee,
        ),
    ]:
        _required_value(value, field_name)
    return bail


def _required_prix(prix: CessionPrix | None) -> CessionPrix:
    if prix is None:
        raise ValueError(f"cession.prix est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.prix.total", prix.total),
        ("cession.prix.total_lettres", prix.total_lettres),
        ("cession.prix.elements_corporels", prix.elements_corporels),
        ("cession.prix.elements_corporels_lettres", prix.elements_corporels_lettres),
        ("cession.prix.elements_incorporels", prix.elements_incorporels),
        ("cession.prix.elements_incorporels_lettres", prix.elements_incorporels_lettres),
    ]:
        _required_text(value, field_name)
    return prix


def _required_document(document: DocumentContext | None) -> DocumentContext:
    if document is None:
        raise ValueError(f"document est obligatoire pour {DOCUMENT_CODE}.")
    _required_text(document.nombre_pages_lettres, "document.nombre_pages_lettres")
    _required_text(document.nombre_exemplaires_lettres, "document.nombre_exemplaires_lettres")
    return document


def _required_exercices(exercices: list[CessionExercice]) -> list[CessionExercice]:
    if len(exercices) != 3:
        raise ValueError("cession.exercices doit contenir exactement trois lignes.")
    for index, exercice in enumerate(exercices):
        prefix = f"cession.exercices[{index}]"
        _required_text(exercice.periode, f"{prefix}.periode")
        _required_text(exercice.chiffre_affaires, f"{prefix}.chiffre_affaires")
        _required_text(exercice.resultat, f"{prefix}.resultat")
    return exercices


def _add_title(docx, variant: CessionCabinetVariant) -> None:
    title = "ACTE DE CESSION" if variant.etape == ACTE else "COMPROMIS DE CESSION"
    cabinet = "CABINET MEDICAL" if variant.type_cabinet == MEDICAL else "CABINET DENTAIRE"
    add_framed_title(docx, [title, cabinet])


def _add_parties(docx, data: _CessionData) -> None:
    add_paragraph(docx, "Entre les soussignes :", bold=True)
    add_paragraph(
        docx,
        _vendeur_full_line(data.vendeur),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    add_paragraph(docx, "Ci-apres designe le vendeur ou le soussigne de premiere part")
    add_paragraph(docx, "De premiere part")

    add_paragraph(
        docx,
        _required_text(
            data.acquereur.denomination_societe, "cession.acquereur.denomination_societe"
        ),
    )
    add_paragraph(
        docx,
        (
            f"{_required_text(data.acquereur.forme_sociale, 'cession.acquereur.forme_sociale')} "
            f"au capital de {_required_text(data.acquereur.capital_social, 'cession.acquereur.capital_social')} euros"
        ),
    )
    add_paragraph(docx, f"Ayant son siege au {_address_label(data.acquereur.siege)}")
    rcs_line = (
        f"Immatriculee ou en cours d'immatriculation au RCS de "
        f"{_required_text(data.acquereur.rcs_ville, 'cession.acquereur.rcs_ville')}"
    )
    if data.acquereur.numero_rcs:
        rcs_line += f" sous le numero {data.acquereur.numero_rcs}"
    if data.acquereur.numero_siret:
        rcs_line += f" {data.acquereur.numero_siret}"
    add_paragraph(docx, rcs_line)
    add_paragraph(
        docx,
        (
            "Representee par son "
            f"{_required_text(data.representant.fonction, 'cession.acquereur.representant.fonction')}, "
            f"{_representant_label(data.representant)}, domicilie en cette qualite audit siege."
        ),
    )
    add_paragraph(docx, "Ci-apres designe l'acquereur ou le soussigne de seconde part")
    add_paragraph(docx, "De deuxieme part")
    add_paragraph(docx, "Il a ete declare fait et convenu ce qui suit :")


def _add_objet(docx, data: _CessionData, variant: CessionCabinetVariant) -> None:
    _add_section_title(docx, "OBJET DU CONTRAT")
    if variant.etape == ACTE:
        fonds = (
            "fonds liberal de medecin"
            if variant.type_cabinet == MEDICAL
            else f"fonds liberal de {_required_text(data.vendeur.profession, 'cession.vendeur.profession')}"
        )
        text = (
            "Par les presentes, le vendeur cede et transporte en s'obligeant a toutes les "
            "garanties ordinaires de fait et de droit les plus etendues, au cessionnaire, "
            f"qui accepte, le {fonds} dont il est proprietaire, exploite au "
            f"{_required_text(data.cabinet.adresse_affichee, 'cession.cabinet.adresse_affichee')}."
        )
    else:
        nature = (
            _required_text(
                data.cabinet.nature_fonds_liberal, "cession.cabinet.nature_fonds_liberal"
            )
            if variant.type_cabinet == MEDICAL
            else _required_text(data.vendeur.profession, "cession.vendeur.profession")
        )
        text = (
            "Par les presentes, le promettant promet de vendre, sous les garanties ordinaires "
            "de droit et de faits en pareille matiere, au beneficiaire qui accepte et s'engage "
            f"a acquerir le fonds liberal de {nature} attache aux locaux situes a "
            f"{_required_text(data.cabinet.adresse_locaux_affichee, 'cession.cabinet.adresse_locaux_affichee')}."
        )
    add_paragraph(docx, text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_paragraph(
        docx,
        "La presente convention a pour objet de determiner les conditions de la cession a "
        "l'acquereur du fonds liberal appartenant au vendeur, et de fixer les modalites dans "
        "lesquelles aura lieu le transfert de propriete et de jouissance.",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_declarations(docx) -> None:
    _add_section_title(docx, "DECLARATIONS DES PARTIES")
    for text in [
        "que leur etat civil et leur existence juridique est conforme a celui ou celle indique en tete des presentes,",
        "qu'elles ne sont pas susceptibles d'etre l'objet de poursuites ou de mesures pouvant entrainer la confiscation totale ou partielle de leurs biens,",
        "qu'elles ont la pleine capacite juridique pour s'obliger aux presentes,",
        "qu'aucune restriction legale, judiciaire ou contractuelle ne fait obstacle a la cession.",
    ]:
        add_hyphen_list_item(docx, text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)


def _add_consistance(docx, data: _CessionData, variant: CessionCabinetVariant) -> None:
    _add_section_title(docx, "DECLARATION DU VENDEUR - CONSISTANCE DU FONDS LIBERAL")
    cabinet_label = "cabinet medical" if variant.type_cabinet == MEDICAL else "cabinet dentaire"
    add_paragraph(
        docx,
        (
            f"Le vendeur declare etre proprietaire du {cabinet_label} exploite a "
            f"{_required_text(data.cabinet.adresse_affichee, 'cession.cabinet.adresse_affichee')}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    for text in [
        "la patientele et les fichiers attaches au fonds liberal cede,",
        "les dossiers, archives et informations patients, dans le respect des regles professionnelles applicables,",
        "le droit au bail ou le droit d'exercer dans les lieux selon la source du document,",
        f"la ligne telephonique {_required_text(data.cabinet.telephone, 'cession.cabinet.telephone')},",
        "les instruments, materiel professionnel, meubles et objets mobiliers servant a l'exploitation,",
        "les contrats, marches, traites et conventions passes dans le cadre de l'activite liberale.",
    ]:
        add_hyphen_list_item(docx, text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)


def _add_origine_propriete(
    docx,
    data: _CessionData,
    variant: CessionCabinetVariant,
) -> None:
    _add_section_title(docx, "SUR L'ORIGINE DE PROPRIETE")
    if variant.etape == ACTE and variant.type_cabinet == MEDICAL:
        add_paragraph(
            docx,
            (
                "Le vendeur declare avoir acquis ou cree la patientele en "
                f"{_required_text(data.cabinet.annees_acquisition_patientele, 'cession.cabinet.annees_acquisition_patientele')}. "
                f"{_required_text(data.cabinet.description_origine_propriete, 'cession.cabinet.description_origine_propriete')}"
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
        return
    if variant.etape == ACTE and variant.type_cabinet == DENTAIRE:
        previous = data.cabinet.precedent_proprietaire
        if previous is None:
            raise ValueError(
                "cession.cabinet.precedent_proprietaire est obligatoire pour l'acte dentaire."
            )
        add_paragraph(
            docx,
            (
                "Le vendeur declare avoir acquis le fonds liberal aupres de "
                f"{_person_label(previous.civilite_affichage, previous.prenom, previous.nom, 'cession.cabinet.precedent_proprietaire')} "
                f"le {_display_date(data.cabinet.date_origine_propriete, 'cession.cabinet.date_origine_propriete')}, "
                f"moyennant le prix de {_required_text(data.cabinet.prix_origine_propriete, 'cession.cabinet.prix_origine_propriete')}."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
        return
    add_paragraph(
        docx,
        (
            "L'origine de propriete est rendue selon les informations manuelles validees du "
            f"contexte : {_required_text(data.cabinet.description_origine_propriete, 'cession.cabinet.description_origine_propriete')}"
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_bail(docx, data: _CessionData, variant: CessionCabinetVariant) -> None:
    _add_section_title(docx, "DROIT AU BAIL")
    add_paragraph(
        docx,
        (
            "Le fonds liberal est exploite dans des locaux faisant l'objet d'un bail "
            f"professionnel en date du {_display_date(data.bail.date_bail, 'cession.bail_professionnel.date_bail')}, "
            f"d'une duree de {_required_text(data.bail.duree, 'cession.bail_professionnel.duree')}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    if data.bail.date_debut or data.bail.date_fin:
        add_paragraph(
            docx,
            (
                "La periode du bail est renseignee du "
                f"{_display_date(data.bail.date_debut, 'cession.bail_professionnel.date_debut')} "
                f"au {_display_date(data.bail.date_fin, 'cession.bail_professionnel.date_fin')}."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
    if data.bail.loyer_mensuel:
        add_paragraph(docx, f"Le loyer mensuel est de {data.bail.loyer_mensuel}.")
    add_paragraph(
        docx,
        (
            "L'activite autorisee par le bail est la suivante : "
            f"{_required_text(data.bail.activite_autorisee_affichee, 'cession.bail_professionnel.activite_autorisee_affichee')}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    if variant.type_cabinet == MEDICAL:
        add_paragraph(
            docx,
            "La mention medicale du bail a ete rendue uniquement apres validation explicite du contexte.",
            italic=True,
        )


def _add_exercices(docx, data: _CessionData) -> None:
    _add_section_title(docx, "CHIFFRES D'AFFAIRES ET RESULTATS")
    table = docx.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    headers = ["Exercice", "Chiffre d'affaires", "Resultat"]
    for index, header in enumerate(headers):
        table.rows[0].cells[index].paragraphs[0].add_run(header).bold = True
    for exercice in data.exercices:
        cells = table.add_row().cells
        cells[0].text = _required_text(exercice.periode, "cession.exercices[].periode")
        cells[1].text = _required_text(
            exercice.chiffre_affaires,
            "cession.exercices[].chiffre_affaires",
        )
        cells[2].text = _required_text(exercice.resultat, "cession.exercices[].resultat")


def _add_situation_generale(
    docx,
    data: _CessionData,
    variant: CessionCabinetVariant,
) -> None:
    _add_section_title(docx, "SITUATION GENERALE ET LIBRE DISPOSITION")
    profession = (
        "medecin"
        if variant.type_cabinet == MEDICAL
        else _required_text(
            data.vendeur.profession,
            "cession.vendeur.profession",
        )
    )
    for text in [
        "le vendeur a la libre disposition et la pleine propriete du materiel cede,",
        "aucune saisie, confiscation, location, pret ou reserve de propriete ne greve le fonds liberal,",
        "le materiel est declare en bon fonctionnement,",
        "le cabinet respecte les normes de salubrite, hygiene et securite applicables,",
        "l'acquereur declare ne connaitre aucun obstacle a l'exercice de la profession de "
        + profession
        + ".",
    ]:
        add_hyphen_list_item(docx, text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)


def _add_prix(docx, data: _CessionData) -> None:
    _add_section_title(docx, "PRIX")
    add_paragraph(
        docx,
        (
            "La presente cession est consentie et acceptee moyennant le prix principal de "
            f"{_required_text(data.prix.total_lettres, 'cession.prix.total_lettres')} "
            f"({_required_text(data.prix.total, 'cession.prix.total')} euros)."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    for text in [
        (
            "elements corporels : "
            f"{_required_text(data.prix.elements_corporels_lettres, 'cession.prix.elements_corporels_lettres')} "
            f"({_required_text(data.prix.elements_corporels, 'cession.prix.elements_corporels')} euros)"
        ),
        (
            "elements incorporels : "
            f"{_required_text(data.prix.elements_incorporels_lettres, 'cession.prix.elements_incorporels_lettres')} "
            f"({_required_text(data.prix.elements_incorporels, 'cession.prix.elements_incorporels')} euros)"
        ),
    ]:
        add_hyphen_list_item(docx, text)


def _add_financement(
    docx,
    data: _CessionData,
    variant: CessionCabinetVariant,
) -> None:
    if variant.etape == ACTE:
        _add_section_title(docx, "PAIEMENT DU PRIX")
        if variant.type_cabinet == MEDICAL:
            add_paragraph(docx, "Le prix est paye au moyen d'un pret bancaire.")
            _add_credit_vendeur(docx, data.financement.credit_vendeur)
        else:
            add_paragraph(docx, "Le prix est paye comptant par l'acquereur.")
        return

    _add_section_title(docx, "CONDITIONS SUSPENSIVES")
    pret = _required_pret(data.financement.pret)
    if variant.type_cabinet == MEDICAL:
        add_paragraph(
            docx,
            (
                "La realisation des presentes est soumise a l'obtention d'un pret d'un montant "
                f"de {_required_text(pret.montant, 'cession.financement.pret.montant')}, "
                f"au taux de {_required_text(pret.taux, 'cession.financement.pret.taux')} "
                f"et pour une duree de {_required_text(pret.duree, 'cession.financement.pret.duree')}."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
    else:
        add_paragraph(
            docx,
            (
                "La realisation des presentes est soumise a l'obtention d'un pret d'un montant "
                f"de {_required_text(pret.montant, 'cession.financement.pret.montant')}, "
                "au taux maximum source fixe de 5 %."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
    add_paragraph(
        docx,
        (
            "La cession devra etre regularisee au plus tard le "
            f"{_display_date(data.cession.date_limite_realisation, 'cession.date_limite_realisation')}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_credit_vendeur(docx, credit_vendeur: CessionCreditVendeur | None) -> None:
    if credit_vendeur is None or not credit_vendeur.actif:
        return
    add_paragraph(
        docx,
        (
            "Un credit-vendeur est stipule pour un montant de "
            f"{_required_text(credit_vendeur.montant, 'cession.financement.credit_vendeur.montant')}, "
            f"une duree de {_required_text(credit_vendeur.duree, 'cession.financement.credit_vendeur.duree')}, "
            f"au taux de {_required_text(credit_vendeur.taux, 'cession.financement.credit_vendeur.taux')}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    add_paragraph(
        docx,
        (
            "La majoration d'interet de retard est fixee a "
            f"{_required_text(credit_vendeur.majoration_interet_retard, 'cession.financement.credit_vendeur.majoration_interet_retard')}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_conditions(
    docx,
    data: _CessionData,
    variant: CessionCabinetVariant,
) -> None:
    _add_section_title(docx, "CONDITIONS")
    for text in [
        "le vendeur garantit les enonciations relatives a l'origine de propriete et a la consistance du fonds,",
        "le vendeur remet a l'acquereur les dossiers, fichiers et justificatifs necessaires,",
        "l'acquereur prend le fichier et les dossiers patients dans l'etat ou ils se trouvent,",
        "l'acquereur supporte les frais, droits et honoraires des presentes.",
    ]:
        add_hyphen_list_item(docx, text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if data.cession.scm is not None and data.cession.scm.actif:
        add_hyphen_list_item(
            docx,
            (
                "l'acquereur reprend la clause manuelle de cession de parts SCM pour "
                f"{_required_text(data.cession.scm.nb_parts_a_ceder, 'cession.scm.nb_parts_a_ceder')} parts."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
    if variant.etape == ACTE and variant.type_cabinet == DENTAIRE and data.cession.salaries:
        add_paragraph(docx, "L'acquereur reprend les contrats de travail des salaries suivants :")
        for salarie in data.cession.salaries:
            add_hyphen_list_item(docx, _salarie_label(salarie, 0))
    if variant.type_cabinet == DENTAIRE:
        accessibilite = data.cession.accessibilite_cabinet_dentaire
        if accessibilite and accessibilite.information_requise:
            _add_section_title(docx, "ACCESSIBILITE DES CABINETS DENTAIRES")
            add_paragraph(
                docx,
                accessibilite.information_requise,
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            )


def _add_droits_et_formalites(
    docx,
    data: _CessionData,
    variant: CessionCabinetVariant,
) -> None:
    _add_section_title(docx, "DROITS, FRAIS ET FORMALITES")
    add_paragraph(
        docx, "Les droits d'enregistrement sont acquittes conformement aux textes applicables."
    )
    add_paragraph(
        docx, "Les frais, droits et honoraires des presentes sont a la charge de l'acquereur."
    )
    ordre = (
        "Conseil departemental de l'Ordre des Medecins"
        if variant.type_cabinet == MEDICAL
        else "Conseil departemental de l'Ordre des Chirurgiens-Dentistes"
    )
    add_paragraph(docx, f"Le present contrat sera communique au {ordre}.")
    if variant.etape == ACTE:
        _add_section_title(docx, "TRANSFERT DE PROPRIETE")
        add_paragraph(
            docx,
            "L'acquereur aura la propriete et la jouissance du fonds liberal selon les modalites des presentes.",
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
    if variant.type_cabinet == DENTAIRE:
        _add_section_title(docx, "CONCILIATION ORDINALE")
        add_paragraph(
            docx,
            (
                "Tout differend relatif aux presentes sera prealablement soumis au President "
                "du Conseil departemental competent."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
    _add_section_title(docx, "ELECTION DE DOMICILE - ATTRIBUTION DE JURIDICTION")
    add_paragraph(
        docx,
        "Pour l'execution des presentes, les parties font election de domicile en leur domicile ou siege respectif.",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_signature(
    docx,
    data: _CessionData,
    variant: CessionCabinetVariant,
) -> None:
    add_paragraph(
        docx,
        (
            f"Fait a {_required_text(data.ctx.signature.lieu, 'signature.lieu')}, le "
            f"{_display_date(data.ctx.signature.date, 'signature.date')}, en "
            f"{_required_text(data.document.nombre_exemplaires_lettres, 'document.nombre_exemplaires_lettres')} exemplaires."
        ),
    )
    if variant.type_cabinet == DENTAIRE and variant.etape == ACTE:
        add_paragraph(docx, "Lu et approuve", italic=True)
    add_signature_lines(
        docx,
        [
            f"Le vendeur : {_vendeur_label(data.vendeur)}",
            f"L'acquereur : {_required_text(data.acquereur.denomination_societe, 'cession.acquereur.denomination_societe')}",
        ],
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
    )


def _add_annexes(docx, data: _CessionData) -> None:
    annexes = data.document.annexes or [
        "ETAT DES ELEMENTS CORPORELS CEDES",
        "COPIE 2035 AMORTISSEMENTS",
    ]
    _add_section_title(docx, "ANNEXES")
    for annexe in annexes:
        add_hyphen_list_item(docx, annexe)


def _required_pret(pret: CessionPret | None) -> CessionPret:
    if pret is None:
        raise ValueError(f"cession.financement.pret est obligatoire pour {DOCUMENT_CODE}.")
    _required_text(pret.montant, "cession.financement.pret.montant")
    return pret


def _section_label(title: str) -> str:
    return title


def _add_section_title(docx, title: str) -> None:
    add_paragraph(docx, _section_label(title), bold=True, underline=True, space_before_pt=10)


def _vendeur_full_line(vendeur: CessionVendeur) -> str:
    birth_place = _required_text(vendeur.ville_naissance, "cession.vendeur.ville_naissance")
    if vendeur.departement_naissance:
        birth_place += f" ({vendeur.departement_naissance})"
    elif vendeur.cp_naissance:
        birth_place += f" {vendeur.cp_naissance}"
    elif vendeur.pays_naissance:
        birth_place += f" ({vendeur.pays_naissance})"
    line = (
        f"{_vendeur_label(vendeur)}, "
        f"{_required_text(vendeur.profession, 'cession.vendeur.profession')}, "
        f"ne(e) le {_display_date(vendeur.date_naissance, 'cession.vendeur.date_naissance')} "
        f"a {birth_place}, de nationalite "
        f"{_required_text(vendeur.nationalite, 'cession.vendeur.nationalite')}, demeurant "
        f"{_required_text(vendeur.adresse_affichee, 'cession.vendeur.adresse_affichee')}"
    )
    if vendeur.adresse_exercice_affichee:
        line += f", et exercant au {vendeur.adresse_exercice_affichee}"
    if vendeur.numero_siren:
        line += f", inscrit au repertoire SIREN sous le numero {vendeur.numero_siren}"
    if vendeur.numero_ordre:
        line += (
            f", inscrit au tableau du Conseil departemental sous le numero {vendeur.numero_ordre}"
        )
    if vendeur.numero_rpps:
        line += f", inscrit sous le numero RPPS {vendeur.numero_rpps}"
    line += f", {_required_text(vendeur.situation_maritale, 'cession.vendeur.situation_maritale')}"
    if vendeur.conjoint is not None:
        line += f" avec {_conjoint_label(vendeur.conjoint)}"
    if vendeur.regime_matrimonial:
        line += f", sous le regime de {vendeur.regime_matrimonial}"
    return line + "."


def _vendeur_label(vendeur: CessionVendeur) -> str:
    return _person_label(
        vendeur.civilite_affichage,
        vendeur.prenom,
        vendeur.nom,
        "cession.vendeur",
    )


def _representant_label(representant: CessionRepresentant) -> str:
    return _person_label(
        representant.civilite_affichage,
        representant.prenom,
        representant.nom,
        "cession.acquereur.representant",
    )


def _conjoint_label(conjoint: CessionConjoint) -> str:
    return _person_label(
        conjoint.civilite_affichage,
        conjoint.prenom,
        conjoint.nom,
        "cession.vendeur.conjoint",
    )


def _salarie_label(salarie: CessionSalarie, index: int) -> str:
    field_name = f"cession.salaries[{index}]"
    return _person_label(
        salarie.civilite_affichage,
        salarie.prenom,
        salarie.nom,
        field_name,
    )


def _person_label(
    civilite: str | None,
    prenom: str | None,
    nom: str | None,
    field_name: str,
) -> str:
    return (
        f"{_required_text(civilite, f'{field_name}.civilite_affichage')} "
        f"{_required_text(prenom, f'{field_name}.prenom')} "
        f"{_required_text(nom, f'{field_name}.nom')}"
    )


def _address_label(address: Address | None) -> str | None:
    if address is None:
        return None
    if address.adresse_affichee:
        return address.adresse_affichee
    parts = [address.num_voie, address.voie, address.cp, address.ville]
    return " ".join(part for part in parts if part)


def _display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return _required_text(value, field_name)


def _required_value(value: date | str | None, field_name: str) -> date | str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()
