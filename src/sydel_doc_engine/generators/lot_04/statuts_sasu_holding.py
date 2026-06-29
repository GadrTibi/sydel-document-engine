from __future__ import annotations

from datetime import date
from pathlib import Path

from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Person,
    StatutsSasuHoldingContext,
)
from sydel_doc_engine.rendering.docx_template_fill import fill_docx_template
from sydel_doc_engine.utils.months import FRENCH_MONTHS

DOCUMENT_CODE = "CODE-STATUTS-SASU-HOLDING-001"
OUTPUT_FILENAME = "statuts_sasu_holding.docx"
EXPECTED_STRUCTURE = "SASU_HOLDING"

# Modele source tokenise (modele officiel Albane 2026-06-29, SASU Holding generaliste).
# Resolu independamment du cwd : parents[4] = racine du repo.
_SOURCE_MODEL = (
    Path(__file__).resolve().parents[4]
    / "project"
    / "source_documents"
    / "lot_04"
    / "statuts SASU Holding.docx"
)


class StatutsSasuHoldingGenerator:
    """Generateur des statuts SASU Holding (SAS unipersonnelle, holding patrimoniale).

    Token-replacement pur sur le modele officiel Albane (l'acte est unipersonnel : un seul
    associe = le president, aucun bloc repetitif). Le genre de l'associe unique accorde les
    tournures figees du modele (« Le soussigne »/« La soussignee », « il/elle a decide »,
    « ne/nee le »).
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        if ctx.structure != EXPECTED_STRUCTURE:
            raise ValueError(
                f"dossier.structure doit etre {EXPECTED_STRUCTURE} pour {DOCUMENT_CODE}."
            )
        statuts = _required(ctx.statuts_sasu_holding, "statuts_sasu_holding")
        societe = _required(ctx.societe, "societe")
        associe = _required(ctx.personne_signataire, "personne_signataire")
        _required(ctx.exercice_social, "exercice_social")
        siege = _required(societe.siege, "societe.siege")
        adresse_perso = _required(associe.adresse_perso, "personne_signataire.adresse_perso")

        replacements = _build_replacements(statuts, societe, associe, ctx, siege, adresse_perso)
        gender_pairs = [(associe.genre, _SOUSSIGNE_PAIRS)]

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        return fill_docx_template(
            _SOURCE_MODEL, replacements, output_path, gender_pairs=gender_pairs
        )


# Accords de genre de l'associe unique (modele fige au masculin). Pour une associee unique
# personne physique feminin -> accorder les tournures de comparution.
_SOUSSIGNE_PAIRS: list[tuple[str, str]] = [
    ("Le soussigné", "La soussignée"),
    ("qu’il a décidé", "qu’elle a décidé"),
    ("né le", "née le"),
    ("l’associé unique pourra", "l’associée unique pourra"),
]


def _build_replacements(
    statuts: StatutsSasuHoldingContext,
    societe: Company,
    associe: Person,
    ctx: DocumentGenerationContext,
    siege: Address,
    adresse_perso: Address,
) -> dict[str, str]:
    capital = _required_text(statuts.capital_social or societe.capital, "statuts.capital_social")
    return {
        "[denomination_societe]": _required_text(societe.denomination, "societe.denomination"),
        "[forme_sociale]": _required_text(statuts.forme_sociale, "statuts.forme_sociale"),
        "[capital_social]": capital,
        "[capital_lettres]": _required_text(
            statuts.capital_social_lettres, "statuts.capital_social_lettres"
        ),
        "[num_voie_siege]": _text(siege.num_voie),
        "[voie_siege]": _required_text(siege.voie, "societe.siege.voie"),
        "[ville_siege]": _required_text(siege.ville, "societe.siege.ville"),
        "[cp_siege]": _required_text(siege.cp, "societe.siege.cp"),
        "[civilite]": _required_text(associe.civilite, "personne_signataire.civilite"),
        "[prenom]": _required_text(associe.prenom, "personne_signataire.prenom"),
        "[nom]": _required_text(associe.nom, "personne_signataire.nom"),
        "[date_naissance]": _french_date(associe.date_naissance, "date_naissance"),
        "[ville_naissance]": _required_text(
            associe.ville_naissance, "personne_signataire.ville_naissance"
        ),
        "[nationalite]": _required_text(associe.nationalite, "personne_signataire.nationalite"),
        "[num_voie_perso]": _text(adresse_perso.num_voie),
        "[voie_perso]": _required_text(adresse_perso.voie, "adresse_perso.voie"),
        "[cp_perso]": _required_text(adresse_perso.cp, "adresse_perso.cp"),
        "[ville_perso]": _required_text(adresse_perso.ville, "adresse_perso.ville"),
        "[nb_actions]": str(_required_int(statuts.nb_actions, "statuts.nb_actions")),
        "[nom_banque]": _required_text(statuts.nom_banque, "statuts.nom_banque"),
        "[debut_exercice]": _required_text(
            _required(ctx.exercice_social, "exercice_social").debut, "exercice_social.debut"
        ),
        "[fin_exercice]": _required_text(ctx.exercice_social.fin, "exercice_social.fin"),
        "[date_cloture_exercice_1]": _required_text(
            ctx.exercice_social.date_cloture_premier_exercice,
            "exercice_social.date_cloture_premier_exercice",
        ),
        "[lieu_signature]": _required_text(ctx.signature.lieu, "signature.lieu"),
        "[date_signature]": _french_date(ctx.signature.date, "signature.date"),
        "[qualite_associe]": _required_text(statuts.qualite_associe, "statuts.qualite_associe"),
        "[fonction_dirigeant]": _required_text(
            statuts.fonction_dirigeant, "statuts.fonction_dirigeant"
        ),
    }


def _french_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return f"{value.day} {FRENCH_MONTHS[value.month]} {value.year}"
    return _required_text(value, field_name)


def _required(value, field_name: str):
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return str(value).strip()


def _required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _text(value: str | None) -> str:
    return str(value).strip() if value is not None else ""


__all__ = ["StatutsSasuHoldingGenerator", "DOCUMENT_CODE", "EXPECTED_STRUCTURE"]
