from __future__ import annotations

from decimal import Decimal, InvalidOperation
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    CapitalSouscripteur,
    CapitalSouscription,
    DocumentGenerationContext,
    SocieteSpfpl,
)
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.rendering.docx_builder import (
    add_company_identity_block,
    add_paragraph,
    new_document,
)
from sydel_doc_engine.utils.grammar import subject_line

OUTPUT_FILENAME = "attestation_capital_souscripteurs_selas.docx"
DOCUMENT_CODE = "CODE-SELAS-ATTESTATION-CAPITAL-001"
SELAS_STRUCTURE = "SELAS"


class AttestationCapitalSouscripteursSelasGenerator:
    """Generateur from-scratch de l'attestation capital / liste des souscripteurs SELAS.

    Variante MULTI-SOUSCRIPTEURS (1..6 associes), apports en NUMERAIRE.

    Le wording est reproduit VERBATIM depuis le modele Albane 2026-06-17
    (MODELE_Attestation_capital_liste_souscripteurs.docx). Chaque souscripteur
    genere une ligne de repartition et une ligne d'apport en numeraire ; le
    montant en numeraire d'un souscripteur est determine par
    nb_actions x valeur_nominale (capital SELAS = numeraire pur).
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        data = _ResolvedAttestationSelas.from_context(ctx)
        document = new_document()

        add_company_identity_block(
            document,
            [
                data.denomination,
                "Société d'exercice libérale par Actions simplifiées de "
                f"{data.profession}",
                f"Au capital de {data.capital_social} euros",
                f"Siège social : {data.adresse_siege}",
                "En cours d'immatriculation",
            ],
        )
        add_paragraph(document, "ATTESTATION", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
        add_paragraph(
            document,
            "Liste des souscripteurs",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
        )
        add_paragraph(
            document,
            f"{data.soussigne} {data.president_civilite_phrase} {data.president_signature}, "
            f"Président de la Société {data.denomination}, atteste que le capital de ladite "
            "société est réparti de la manière suivante :",
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
        add_paragraph(document, f"Capital social : {data.capital_social} € en numéraire")
        add_paragraph(
            document,
            f"Nombre d'actions: {data.nb_actions_total} actions d'un montant de "
            f"{data.valeur_nominale_action} euro chacune",
        )
        add_paragraph(document, "Répartition : ")
        for repartition in data.repartition_lignes:
            add_paragraph(document, repartition)
        add_paragraph(
            document,
            f"Capital social de {data.capital_social} € entièrement libéré et déposé "
            f"dans les livres de la banque {data.banque}",
        )
        for apport in data.apport_lignes:
            add_paragraph(document, apport)
        add_paragraph(
            document,
            "Le présent état qui constate la souscription d'actions de la société "
            f"{data.denomination}, ainsi que le versement de la somme de "
            f"{data.capital_social} euros correspondant à la totalité du nominal "
            "desdites actions, est certifié exact, sincère et véritable par le Président, "
            f"{data.president_identite}",
        )
        add_paragraph(document, f"Fait à {data.ville_siege}")
        add_paragraph(document, f"Le {data.date_signature}")
        add_paragraph(document, data.president_signature)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


class _ResolvedAttestationSelas:
    def __init__(
        self,
        *,
        denomination: str,
        profession: str,
        capital_social: str,
        adresse_siege: str,
        ville_siege: str,
        banque: str,
        nb_actions_total: int,
        valeur_nominale_action: str,
        repartition_lignes: list[str],
        apport_lignes: list[str],
        soussigne: str,
        president_civilite_phrase: str,
        president_identite: str,
        president_signature: str,
        date_signature: str,
    ) -> None:
        self.denomination = denomination
        self.profession = profession
        self.capital_social = capital_social
        self.adresse_siege = adresse_siege
        self.ville_siege = ville_siege
        self.banque = banque
        self.nb_actions_total = nb_actions_total
        self.valeur_nominale_action = valeur_nominale_action
        self.repartition_lignes = repartition_lignes
        self.apport_lignes = apport_lignes
        self.soussigne = soussigne
        self.president_civilite_phrase = president_civilite_phrase
        self.president_identite = president_identite
        self.president_signature = president_signature
        self.date_signature = date_signature

    @classmethod
    def from_context(
        cls,
        ctx: DocumentGenerationContext,
    ) -> _ResolvedAttestationSelas:
        _validate_scope(ctx)
        societe = _required_societe_spfpl(ctx)
        capital = _required_capital_souscription(ctx)
        souscripteurs = _required_souscripteurs(capital.souscripteurs)
        president = capital.president or souscripteurs[0]

        nb_actions_total = _required_int(
            capital.nb_actions_total,
            "capital_souscription.nb_actions_total",
        )
        valeur_nominale_action = _required_text(
            capital.valeur_nominale_action,
            "capital_souscription.valeur_nominale_action",
        )
        valeur_nominale = _euro_amount(
            valeur_nominale_action,
            "capital_souscription.valeur_nominale_action",
        )

        repartition_lignes: list[str] = []
        apport_lignes: list[str] = []
        total_actions = 0
        for index, souscripteur in enumerate(souscripteurs):
            field = f"capital_souscription.souscripteurs[{index}]"
            nb_actions = _required_int(souscripteur.nb_actions, f"{field}.nb_actions")
            total_actions += nb_actions
            # Modele : « au Dr {PRENOM NOM} » et « Le Docteur {PRENOM NOM} » (le titre
            # « Dr / Docteur » porte deja la civilite, comme dans le generateur SAS).
            nom_complet = _souscripteur_signature(souscripteur, field)
            repartition_lignes.append(f"{nb_actions} actions attribuées au Dr {nom_complet},")
            montant_numeraire = _format_amount(valeur_nominale * Decimal(nb_actions))
            apport_lignes.append(
                f"Le Docteur {nom_complet} a fait un apport de {montant_numeraire} "
                "euros en numéraire."
            )

        if total_actions != nb_actions_total:
            raise ValueError(
                "La répartition des souscripteurs doit correspondre à "
                f"capital_souscription.nb_actions_total pour {DOCUMENT_CODE}."
            )

        # R3 (Albane 2026-07-07) : « Docteur » n'est pas une civilité — le slot
        # « par le Président, __ » rend la civilité CIVILE (Monsieur/Madame,
        # accordée au genre du signataire), jamais le titre d'affichage.
        president_civilite = civilite_civile(
            _required_text(
                president.civilite_affichage,
                "capital_souscription.president.civilite_affichage",
            ),
            ctx.personne_signataire.genre,
        )
        president_signature = _souscripteur_signature(
            president,
            "capital_souscription.president",
        )

        return cls(
            denomination=_required_text(societe.denomination, "societe_spfpl.denomination"),
            profession=_required_text(societe.profession, "societe_spfpl.profession"),
            capital_social=_required_text(
                societe.capital_social,
                "societe_spfpl.capital_social",
            ),
            adresse_siege=_company_siege_display(societe, "societe_spfpl"),
            ville_siege=_company_ville(societe, "societe_spfpl"),
            banque=_required_banque(ctx),
            nb_actions_total=nb_actions_total,
            valeur_nominale_action=valeur_nominale_action,
            repartition_lignes=repartition_lignes,
            apport_lignes=apport_lignes,
            soussigne=subject_line(ctx.personne_signataire.genre),
            president_civilite_phrase=_addressing_civilite(ctx.personne_signataire.genre),
            president_identite=f"{president_civilite} {president_signature}",
            president_signature=president_signature,
            date_signature=ctx.signature.date.strftime("%d/%m/%Y"),
        )


def _validate_scope(ctx: DocumentGenerationContext) -> None:
    if ctx.structure != SELAS_STRUCTURE:
        raise ValueError(
            f"dossier.structure doit etre {SELAS_STRUCTURE} pour {DOCUMENT_CODE}."
        )


def _required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    if ctx.societe_spfpl is None:
        raise ValueError(f"societe_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_spfpl


def _required_capital_souscription(
    ctx: DocumentGenerationContext,
) -> CapitalSouscription:
    if ctx.capital_souscription is None:
        raise ValueError(f"capital_souscription est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.capital_souscription


def _required_souscripteurs(
    souscripteurs: list[CapitalSouscripteur],
) -> list[CapitalSouscripteur]:
    if not souscripteurs:
        raise ValueError(
            "capital_souscription.souscripteurs doit contenir au moins un souscripteur "
            f"pour {DOCUMENT_CODE}."
        )
    return souscripteurs


def _required_banque(ctx: DocumentGenerationContext) -> str:
    if ctx.depot_fonds is None or ctx.depot_fonds.banque is None:
        raise ValueError(f"depot_fonds.banque est obligatoire pour {DOCUMENT_CODE}.")
    return _required_text(ctx.depot_fonds.banque.nom, "depot_fonds.banque.nom")


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def _required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _euro_amount(value: str, field_name: str) -> Decimal:
    normalized = (
        value.lower()
        .replace("euros", "")
        .replace("euro", "")
        .replace("€", "")
        .replace(" ", "")
        .replace(" ", "")
        .replace(",", ".")
        .strip()
    )
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(
            f"{field_name} doit etre un montant numerique pour {DOCUMENT_CODE}."
        ) from exc


def _format_amount(amount: Decimal) -> str:
    """Rend un montant euro sans decimale parasite (1000.00 -> 1000, 1.50 -> 1,50)."""
    normalized = amount.normalize()
    if normalized == normalized.to_integral_value():
        return f"{int(normalized)}"
    return format(normalized, "f").replace(".", ",")


def _souscripteur_signature(souscripteur: CapitalSouscripteur, field_name: str) -> str:
    return (
        f"{_required_text(souscripteur.prenom, f'{field_name}.prenom')} "
        f"{_required_text(souscripteur.nom, f'{field_name}.nom')}"
    )


def _addressing_civilite(genre: Gender) -> str:
    """Civilite d'adresse du president dans « Je soussigné ... » (Monsieur/Madame).

    Derivee verbatim du modele (« Je soussigné Monsieur Alain FEDOROWSKY »). Le
    titre d'affichage (« Docteur ») ne porte pas le genre : la forme d'adresse est
    accordee sur le genre du signataire (accord en genre demande par les retours),
    jamais inventee.
    """
    return "Madame" if genre == Gender.FEMININ else "Monsieur"


def _company_siege_display(societe: SocieteSpfpl, field_name: str) -> str:
    if societe.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {DOCUMENT_CODE}.")
    if societe.siege.adresse_affichee:
        return societe.siege.adresse_affichee.strip()
    return (
        f"{_required_text(societe.siege.num_voie, f'{field_name}.siege.num_voie')} "
        f"{_required_text(societe.siege.voie, f'{field_name}.siege.voie')}, "
        f"{_required_text(societe.siege.cp, f'{field_name}.siege.cp')} "
        f"{_required_text(societe.siege.ville, f'{field_name}.siege.ville')}"
    )


def _company_ville(societe: SocieteSpfpl, field_name: str) -> str:
    if societe.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {DOCUMENT_CODE}.")
    return _required_text(societe.siege.ville, f"{field_name}.siege.ville")
