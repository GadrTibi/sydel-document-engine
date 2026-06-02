from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from unicodedata import normalize as unicode_normalize

from sydel_doc_engine.domain.models import Associe, DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    DOCUMENT_CODE,
    OVERLAY_SELAS_MEDECIN,
    STRUCTURE_SELAS,
    add_conjoint_replacements,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    capital_titles_total,
    common_replacements,
    render_statuts_sel_docx,
    required_associe_unique,
    required_company,
    required_text,
    validate_sel_context,
    validate_selas_second_lieu,
)
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_templates import (
    STATUTS_SELAS_MEDECIN_BLOCKS,
)

OUTPUT_FILENAME = "statuts_selas_medecin.docx"

_TRUE_VALUES = {"1", "true", "yes", "oui", "on"}
_PRESIDENT_FUNCTIONS = {"president", "presidente"}
_COMPLEX_CASE_FLAGS = {
    "selas_directeur_general_nomme": "Directeur General nomme",
    "directeur_general_nomme": "Directeur General nomme",
    "selas_actions_preference": "actions de preference",
    "actions_preference": "actions de preference",
    "selas_categories_actions": "categories d'actions",
    "categories_actions": "categories d'actions",
    "selas_demembrement_actions": "demembrement d'actions",
    "demembrement_actions": "demembrement d'actions",
    "selas_personne_morale_actionnaire": "personne morale actionnaire",
    "actionnaire_personne_morale": "personne morale actionnaire",
    "selas_micro_holding": "micro-holding actionnaire",
    "micro_holding": "micro-holding actionnaire",
    "selas_droits_vote_derogatoires": "droits de vote derogatoires",
    "droits_vote_derogatoires": "droits de vote derogatoires",
    "selas_droits_financiers_derogatoires": "droits financiers derogatoires",
    "droits_financiers_derogatoires": "droits financiers derogatoires",
}
_PROPORTIONAL_PERCENTAGE_FIELDS = {
    "selas_pourcentage_droits_vote": "droits de vote",
    "pourcentage_droits_vote": "droits de vote",
    "selas_pourcentage_droits_financiers": "droits financiers",
    "pourcentage_droits_financiers": "droits financiers",
}


class StatutsSelasMedecinGenerator:
    """Generateur from-scratch des statuts SELAS medecin V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_sel_context(
            ctx,
            expected_structure=STRUCTURE_SELAS,
            expected_overlay=OVERLAY_SELAS_MEDECIN,
        )
        associate = required_associe_unique(ctx)
        second_lieu_enabled = validate_selas_second_lieu(ctx)
        _validate_doc018_v1_scope(ctx, associate)
        replacements = common_replacements(ctx, title_type="actions")
        add_conjoint_replacements(replacements, associate)
        add_ordre_replacements(replacements, associate)
        add_depot_replacements(replacements, ctx, require_address=True)
        add_exercice_replacements(
            replacements,
            ctx,
            require_debut_fin=True,
            require_lieu=True,
        )
        company = required_company(ctx)
        replacements.update(
            {
                "[forme_sociale]": required_text(
                    company.forme_sociale or company.forme_sociale_affichage,
                    "societe.forme_sociale",
                ),
                "[forme_sociale_abregee]": required_text(
                    company.forme_sociale_abregee,
                    "societe.forme_sociale_abregee",
                ),
                "[duree_societe]": required_text(company.duree, "societe.duree"),
                "[nb_actions_lettres]": required_text(
                    ctx.capital.nombre_titres_total_lettres,
                    "capital.nombre_titres_total_lettres",
                ),
                "[valeur_nominale_action_lettres]": required_text(
                    ctx.capital.valeur_nominale_titre_lettres,
                    "capital.valeur_nominale_titre_lettres",
                ),
                "[titre_professionnel]": required_text(
                    associate.titre_professionnel or associate.civilite_affichage,
                    "associes[0].titre_professionnel",
                ),
                "[qualification_principale]": required_text(
                    associate.qualification_principale,
                    "associes[0].qualification_principale",
                ),
                "[qualite_associe]": required_text(
                    associate.qualite,
                    "associes[0].qualite",
                ),
                "[fonction_dirigeant]": required_text(
                    ctx.dirigeant_nomine.fonction_affichage,
                    "dirigeant_nomine.fonction_affichage",
                ),
                "[duree_mandat_dirigeant]": required_text(
                    ctx.dirigeant_nomine.duree_mandat,
                    "dirigeant_nomine.duree_mandat",
                ),
                "[prestataire_signature_electronique]": required_text(
                    ctx.signature.prestataire_signature_electronique,
                    "signature.prestataire_signature_electronique",
                ),
            }
        )
        if second_lieu_enabled and ctx.exercice_social is not None:
            second_lieu = ctx.exercice_social.lieux[1]
            replacements.update(
                {
                    "[nom_lieu_exercice_2]": required_text(
                        second_lieu.nom,
                        "exercice_social.lieux[1].nom",
                    ),
                    "[adresse_lieu_exercice_2]": required_text(
                        second_lieu.adresse_affichee,
                        "exercice_social.lieux[1].adresse_affichee",
                    ),
                }
            )

        return render_statuts_sel_docx(
            STATUTS_SELAS_MEDECIN_BLOCKS,
            replacements,
            output_dir / OUTPUT_FILENAME,
            associate=associate,
            render_selas_second_lieu=second_lieu_enabled,
        )


def _validate_doc018_v1_scope(
    ctx: DocumentGenerationContext,
    associate: Associe,
) -> None:
    if ctx.dirigeant_nomine is None:
        raise ValueError(f"dirigeant_nomine est obligatoire pour {DOCUMENT_CODE}.")
    if ctx.capital is None:
        raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
    for flag, label in _COMPLEX_CASE_FLAGS.items():
        if _metadata_enabled(ctx, flag):
            raise ValueError(f"{label} est hors V1 pour DOC-018.")

    function = _normalize(ctx.dirigeant_nomine.fonction_affichage)
    if "directeur general" in function:
        raise ValueError("Directeur General nomme est hors V1 pour DOC-018.")
    if function not in _PRESIDENT_FUNCTIONS:
        raise ValueError(
            "dirigeant_nomine.fonction_affichage doit etre President pour DOC-018."
        )

    title_type = required_text(ctx.capital.type_titre, "capital.type_titre").lower()
    if title_type != "actions":
        raise ValueError("capital.type_titre doit etre actions pour DOC-018.")

    total_titles = capital_titles_total(ctx)
    if total_titles <= 0:
        raise ValueError("capital.nombre_titres_total doit etre positif pour DOC-018.")
    nominal_value = _decimal_amount(
        ctx.capital.valeur_nominale_titre or ctx.capital.valeur_nominale_part,
        "capital.valeur_nominale_titre",
    )
    if nominal_value <= 0:
        raise ValueError(
            "capital.valeur_nominale_titre doit etre positif pour DOC-018."
        )
    capital_amount = _decimal_amount(ctx.capital.montant, "capital.montant")
    if capital_amount <= 0:
        raise ValueError("capital.montant doit etre positif pour DOC-018.")
    if nominal_value * Decimal(total_titles) != capital_amount:
        raise ValueError(
            "capital.nombre_titres_total * capital.valeur_nominale_titre "
            "doit correspondre a capital.montant pour DOC-018."
        )
    associate_apport = _decimal_amount(
        associate.apport_numeraire,
        "associes[0].apport_numeraire",
    )
    if associate_apport != capital_amount:
        raise ValueError(
            "associes[0].apport_numeraire doit correspondre a capital.montant "
            "pour DOC-018."
        )

    _validate_proportional_rights(ctx)
    _validate_action_numbering(ctx, total_titles)


def _metadata_enabled(ctx: DocumentGenerationContext, key: str) -> bool:
    return (ctx.metadata.get(key) or "").strip().lower() in _TRUE_VALUES


def _validate_proportional_rights(ctx: DocumentGenerationContext) -> None:
    for field, label in _PROPORTIONAL_PERCENTAGE_FIELDS.items():
        value = ctx.metadata.get(field)
        if value is None or not value.strip():
            continue
        if _decimal_amount(value, field) != Decimal("100"):
            raise ValueError(f"{label} non proportionnels hors V1 pour DOC-018.")


def _validate_action_numbering(
    ctx: DocumentGenerationContext,
    total_titles: int,
) -> None:
    expected = _normalize_numbering(f"1 a {total_titles}")
    for field in ("capital.actions.numerotation", "selas_actions_numerotation"):
        value = ctx.metadata.get(field)
        if value is None or not value.strip():
            continue
        if _normalize_numbering(value) != expected:
            raise ValueError(
                "capital.actions.numerotation doit rester simple "
                f"(1 a {total_titles}) pour DOC-018."
            )


def _decimal_amount(value: str | None, field_name: str) -> Decimal:
    raw = required_text(value, field_name)
    compact = raw.replace("\u00a0", " ").replace(" ", "")
    compact = compact.replace("euros", "").replace("euro", "")
    compact = re.sub(r"[^0-9,.-]", "", compact)
    if "," in compact and "." in compact:
        compact = compact.replace(".", "").replace(",", ".")
    else:
        compact = compact.replace(",", ".")
    try:
        return Decimal(compact)
    except InvalidOperation as exc:
        raise ValueError(
            f"{field_name} doit etre un montant numerique pour DOC-018."
        ) from exc


def _normalize(value: str | None) -> str:
    if value is None:
        return ""
    ascii_value = (
        unicode_normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    return re.sub(r"\s+", " ", ascii_value.strip().lower())


def _normalize_numbering(value: str) -> str:
    normalized = _normalize(value)
    normalized = normalized.replace("n°", "").replace("no", "")
    normalized = re.sub(r"actions?", "", normalized)
    normalized = re.sub(r"[^0-9a-z]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized
