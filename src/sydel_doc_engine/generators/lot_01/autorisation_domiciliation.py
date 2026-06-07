# ruff: noqa: E501

from __future__ import annotations

import glob
import re
from datetime import date
from pathlib import Path

from sydel_doc_engine.domain.models import Address, Company, DocumentGenerationContext
from sydel_doc_engine.rendering.docx_template_fill import fill_docx_template

DOCUMENT_CODE = "DOC-002"
OUTPUT_FILENAME = "autorisation_domiciliation.docx"

# Dossier des modeles Word tokenises, resolu independamment du cwd.
# parents[4] depuis src/sydel_doc_engine/generators/lot_01/ = racine du repo.
_SOURCE_MODELS_DIR = (
    Path(__file__).resolve().parents[4] / "project" / "source_documents" / "lot_01"
)

# Motif glob robuste aux accents du nom de fichier du modele.
_MODEL_GLOB = "autorisation*domiciliation*.docx"

# Mois francais accentues pour un rendu fidele "12 mai 2026".
_MONTHS_FR = (
    "",
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)

_ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


class AutorisationDomiciliationGenerator:
    """Générateur cible du DOC-002.

    Rendu fidèle par remplissage du modèle source tokenisé
    (autorisation_domiciliation_transforme.docx) : le texte juridique figé du
    modèle est conservé tel quel (dont « pour une durée indéterminée »), seuls les
    tokens `[variable]` sont remplacés par les valeurs du contexte. Aucune prose
    n'est paraphrasée ni inventée.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        replacements = _build_replacements(ctx)
        model_path = _resolve_model_path()
        output_path = output_dir / OUTPUT_FILENAME
        # Le modele source fige l'ouverture au feminin (« Je soussignée »).
        # On l'accorde au genre du signataire : pour un homme -> « Je soussigné ».
        gender_pairs = [
            (
                ctx.personne_signataire.genre,
                [("Je soussigné", "Je soussignée")],
            )
        ]
        return fill_docx_template(
            model_path,
            replacements,
            output_path,
            gender_pairs=gender_pairs,
        )


def _build_replacements(ctx: DocumentGenerationContext) -> dict[str, str]:
    """Construit le dictionnaire token -> valeur en validant les champs requis.

    La validation métier d'origine (champs obligatoires de DOC-002) est conservée :
    un champ manquant lève ValueError plutôt que d'injecter un trou dans l'acte.
    """
    person = ctx.personne_signataire
    company = _required_company(ctx.societe)

    civilite = _required_text(person.civilite, "personne_signataire.civilite")
    prenom = _required_text(person.prenom, "personne_signataire.prenom")
    nom = _required_text(person.nom, "personne_signataire.nom")
    denomination_societe = _required_text(company.denomination, "societe.denomination")
    capital_social = _required_text(company.capital, "societe.capital")
    siege = _required_siege(company.siege)
    num_voie_siege = _required_text(siege.num_voie, "societe.siege.num_voie")
    voie_siege = _required_text(siege.voie, "societe.siege.voie")
    cp_siege = _required_text(siege.cp, "societe.siege.cp")
    ville_siege = _required_text(siege.ville, "societe.siege.ville")
    lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")
    date_signature = _french_date(ctx.signature.date)

    return {
        "[civilite]": civilite,
        "[prenom]": prenom,
        "[nom]": nom,
        "[denomination_societe]": denomination_societe,
        "[capital_social]": capital_social,
        "[num_voie_siege]": num_voie_siege,
        "[voie_siege]": voie_siege,
        "[cp_siege]": cp_siege,
        "[ville_siege]": ville_siege,
        "[lieu_signature]": lieu_signature,
        "[date_signature]": date_signature,
    }


def _resolve_model_path() -> Path:
    matches = glob.glob(str(_SOURCE_MODELS_DIR / _MODEL_GLOB))
    if not matches:
        raise ValueError(
            f"Modèle introuvable pour {DOCUMENT_CODE} "
            f"(motif {_MODEL_GLOB}) dans {_SOURCE_MODELS_DIR}."
        )
    return Path(matches[0])


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def _required_siege(address: Address | None) -> Address:
    if address is None:
        raise ValueError(f"societe.siege est obligatoire pour {DOCUMENT_CODE}.")
    return address


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def _french_date(value: date | str | None) -> str:
    """Formate une date en français long (ex. « 12 mai 2026 »).

    - date -> jour mois année en français ;
    - str ISO « YYYY-MM-DD » -> parsée puis formatée FR ;
    - autre str -> renvoyée telle quelle.
    """
    if value is None:
        raise ValueError(f"signature.date est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return f"{value.day} {_MONTHS_FR[value.month]} {value.year}"
    text = value.strip()
    match = _ISO_DATE_RE.match(text)
    if match is not None:
        year, month, day = (int(part) for part in match.groups())
        try:
            parsed = date(year, month, day)
        except ValueError:
            return text
        return f"{parsed.day} {_MONTHS_FR[parsed.month]} {parsed.year}"
    return text
