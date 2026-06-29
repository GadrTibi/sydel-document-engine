"""Generateur DOC-050 — Liste des souscripteurs SASU Holding (modele Albane 2026-06-29).

Satellite GENERALISTE de la SASU Holding (SAS unipersonnelle, holding patrimoniale), DISTINCT
de l'attestation capital / liste des souscripteurs SAS SPFPL medecins (DOC-024, verrouille SPFPL
medecins, apports en NATURE de parts, profession=medecin). Le modele Albane SASU Holding est
beaucoup plus simple : un « Etat des souscriptions » avec un tableau (souscripteur unique = le
president) et une ligne TOTAL, sans apport en nature, sans profession, sans SPFPL.

Self-contained : lit l'identite de l'associe unique depuis `ctx.personne_signataire`, la societe
(denomination, capital, nb_actions) depuis `ctx.societe` / `ctx.statuts_sasu_holding`, la
signature depuis `ctx.signature`. Genre libre (holding generaliste).

Fidelite : rendu byte-fidele au modele officiel Albane
`docs/review/albane_sas_2026-06-29/Liste_des_souscripteurs.docx`.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext, Person
from sydel_doc_engine.rendering.docx_builder import (
    add_bordered_data_table,
    add_paragraph,
    new_document,
)

DOCUMENT_CODE = "DOC-050"
OUTPUT_FILENAME = "liste_souscripteurs_sasu_holding.docx"
# Forme courte verbatim du modele Albane (« Etat des souscriptions / De la SAS <denom> »).
FORME_COURTE = "SAS"
# Apostrophe typographique (U+2019) : en-tete « Nombre d'actions souscrites » du modele Albane
# (byte-fidelite — le modele emploie la courbe, pas la droite).
_APOS = chr(0x2019)


class ListeSouscripteursSasuHoldingGenerator:
    """Generateur from-scratch de la liste des souscripteurs SASU Holding (generaliste)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        data = _ResolvedListeSasuHolding.from_context(ctx)
        document = new_document()

        add_paragraph(document, "Etat des souscriptions ")
        add_paragraph(document, f"De la {FORME_COURTE} {data.denomination}")
        add_bordered_data_table(
            document,
            [
                "Noms, prénoms et adresse des souscripteurs",
                f"Nombre d{_APOS}actions souscrites",
                "Montant des souscriptions",
            ],
            [
                [data.souscripteur_nom, f"{data.nb_actions_dot} ", f"{data.montant} "],
                ["TOTAL", f"{data.nb_actions_dot} actions", f"{data.montant} euros"],
            ],
        )
        add_paragraph(document, f"Fait à {data.lieu_signature}")
        add_paragraph(document, f"Le {data.date_signature}")
        add_paragraph(document, f" {data.signature_nom}")

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


class _ResolvedListeSasuHolding:
    def __init__(
        self,
        *,
        denomination: str,
        souscripteur_nom: str,
        nb_actions_dot: str,
        montant: str,
        lieu_signature: str,
        date_signature: str,
        signature_nom: str,
    ) -> None:
        self.denomination = denomination
        self.souscripteur_nom = souscripteur_nom
        self.nb_actions_dot = nb_actions_dot
        self.montant = montant
        self.lieu_signature = lieu_signature
        self.date_signature = date_signature
        self.signature_nom = signature_nom

    @classmethod
    def from_context(cls, ctx: DocumentGenerationContext) -> _ResolvedListeSasuHolding:
        if ctx.structure != "SASU_HOLDING":
            raise ValueError(f"dossier.structure doit etre SASU_HOLDING pour {DOCUMENT_CODE}.")
        person = _required_person(ctx)
        statuts = ctx.statuts_sasu_holding
        if statuts is None:
            raise ValueError(f"statuts_sasu_holding est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.societe is None:
            raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")

        nb_actions = statuts.nb_actions
        if nb_actions is None or nb_actions < 1:
            raise ValueError(
                f"statuts_sasu_holding.nb_actions doit etre superieur a zero pour {DOCUMENT_CODE}."
            )
        civilite = _required_text(person.civilite, "personne_signataire.civilite")
        prenom = _required_text(person.prenom, "personne_signataire.prenom")
        nom = _required_text(person.nom, "personne_signataire.nom")

        return cls(
            denomination=_required_text(ctx.societe.denomination, "societe.denomination"),
            souscripteur_nom=f"{civilite} {prenom} {nom}",
            nb_actions_dot=_fmt_dot_thousands(nb_actions),
            montant=_required_text(ctx.societe.capital_social, "societe.capital_social"),
            lieu_signature=_required_text(ctx.signature.lieu, "signature.lieu"),
            date_signature=_display_date(ctx.signature.date, "signature.date"),
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


def _fmt_dot_thousands(value: int) -> str:
    """Format milliers a POINT (« 10000 » -> « 10.000 »), verbatim modele Albane."""
    return f"{value:,}".replace(",", ".")


def _display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return _required_text(value, field_name)
