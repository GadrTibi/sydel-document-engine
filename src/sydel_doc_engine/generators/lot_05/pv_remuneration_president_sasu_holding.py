"""Generateur DOC-049 — PV remuneration president SASU Holding (modele Albane 2026-06-29).

Satellite GENERALISTE de la SASU Holding (SAS unipersonnelle, holding patrimoniale), DISTINCT
du PV remuneration president SPFPL medecins (DOC-023, verrouille SPFPL medecins / masculin /
profession=medecin). Ce generateur est self-contained : il lit l'identite de l'associe unique
(= president) depuis `ctx.personne_signataire`, la societe depuis `ctx.societe`, la cloture du
premier exercice depuis `ctx.exercice_social`, la signature depuis `ctx.signature`. Aucune garde
profession/genre : la holding est generaliste, l'associe(e) unique peut etre un homme ou une femme.

Fidelite : rendu byte-fidele au modele officiel Albane
`docs/review/albane_sas_2026-06-29/PV_remuneration_president.docx` (l'associe unique decide de NE
PAS se remunerer jusqu'a la cloture du 1er exercice + remboursement des frais sur justification).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext, Person
from sydel_doc_engine.rendering.docx_builder import (
    add_framed_title,
    add_paragraph,
    new_document,
)
from sydel_doc_engine.utils.months import FRENCH_MONTHS

DOCUMENT_CODE = "DOC-049"
OUTPUT_FILENAME = "pv_remuneration_president_sasu_holding.docx"


class PvRemunerationPresidentSasuHoldingGenerator:
    """Generateur from-scratch du PV remuneration president SASU Holding (generaliste)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        data = _ResolvedPvSasuHolding.from_context(ctx)
        document = new_document()

        add_framed_title(
            document,
            [
                "PROCES-VERBAL DES DECISIONS",
                "DE L'ASSOCIE UNIQUE",
                f"DU {data.date_signature}",
            ],
        )
        add_paragraph(document, data.associe_nom)
        add_paragraph(document, f"Demeurant {data.adresse_associe}")
        add_paragraph(
            document,
            f"{data.qualite_associe} de la SASU en cours de formation.",
        )
        add_paragraph(document, "a pris la décision suivante : ")
        add_paragraph(document, f"Fixation de la rémunération du {data.fonction_president}")
        add_paragraph(document, "DECISION UNIQUE")
        add_paragraph(
            document,
            f"{data.associe_civilite_nom}, associé unique, décide qu'il ne percevra "
            "aucune rémunération au titre de son mandat de "
            f"{data.fonction_president}, à compter de son immatriculation, et ce, "
            f"jusqu'au {data.date_cloture} inclus, date de la clôture du premier exercice "
            "social.",
        )
        add_paragraph(
            document,
            "Il pourra donc prétendre au remboursement sur justification de ses frais de "
            "représentation et de déplacement.",
        )
        add_paragraph(
            document,
            "De tout ce que dessus, l'associé unique a dressé et signé le présent "
            "procès-verbal.",
        )
        add_paragraph(document, f"Fait à {data.lieu_signature} en trois exemplaires ")
        add_paragraph(document, "________________")
        add_paragraph(document, data.signature_nom)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


class _ResolvedPvSasuHolding:
    def __init__(
        self,
        *,
        date_signature: str,
        associe_nom: str,
        associe_civilite_nom: str,
        adresse_associe: str,
        qualite_associe: str,
        fonction_president: str,
        date_cloture: str,
        lieu_signature: str,
        signature_nom: str,
    ) -> None:
        self.date_signature = date_signature
        self.associe_nom = associe_nom
        self.associe_civilite_nom = associe_civilite_nom
        self.adresse_associe = adresse_associe
        self.qualite_associe = qualite_associe
        self.fonction_president = fonction_president
        self.date_cloture = date_cloture
        self.lieu_signature = lieu_signature
        self.signature_nom = signature_nom

    @classmethod
    def from_context(cls, ctx: DocumentGenerationContext) -> _ResolvedPvSasuHolding:
        if ctx.structure != "SASU_HOLDING":
            raise ValueError(f"dossier.structure doit etre SASU_HOLDING pour {DOCUMENT_CODE}.")
        person = _required_person(ctx)
        statuts = ctx.statuts_sasu_holding
        if statuts is None:
            raise ValueError(f"statuts_sasu_holding est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.exercice_social is None:
            raise ValueError(f"exercice_social est obligatoire pour {DOCUMENT_CODE}.")

        civilite = _required_text(person.civilite, "personne_signataire.civilite")
        prenom = _required_text(person.prenom, "personne_signataire.prenom")
        nom = _required_text(person.nom, "personne_signataire.nom")
        fonction_president = _required_text(
            statuts.fonction_dirigeant,
            "statuts_sasu_holding.fonction_dirigeant",
        )
        qualite_associe = _required_text(
            statuts.qualite_associe,
            "statuts_sasu_holding.qualite_associe",
        )

        return cls(
            date_signature=_long_french_date(ctx.signature.date, "signature.date"),
            associe_nom=f"{civilite} {prenom} {nom}",
            associe_civilite_nom=f"{civilite} {nom}",
            adresse_associe=_required_text(
                person.adresse_personnelle_affichee,
                "personne_signataire.adresse_personnelle_affichee",
            ),
            qualite_associe=qualite_associe,
            fonction_president=fonction_president,
            date_cloture=_required_text(
                ctx.exercice_social.date_cloture_premier_exercice,
                "exercice_social.date_cloture_premier_exercice",
            ),
            lieu_signature=_required_text(ctx.signature.lieu, "signature.lieu"),
            signature_nom=f"{prenom} {nom}",
        )


def _required_person(ctx: DocumentGenerationContext) -> Person:
    if ctx.personne_signataire is None:
        raise ValueError(f"personne_signataire est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.personne_signataire


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def _long_french_date(value: date | str | None, field_name: str) -> str:
    """Date en francais long (« 30 septembre 2020 ») pour le titre du PV (verbatim modele)."""
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return f"{value.day} {FRENCH_MONTHS[value.month]} {value.year}"
    return _required_text(value, field_name)
