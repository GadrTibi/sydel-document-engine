from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Associe,
    BienImmobilier,
    CapitalContext,
    Company,
    DirigeantNomine,
    DocumentGenerationContext,
    Emprunt,
    ReunionPresident,
)
from sydel_doc_engine.front_app.field_derivations import group_montant
from sydel_doc_engine.rendering.docx_builder import (
    add_centered_block,
    add_framed_title,
    add_hyphen_list_item,
    add_paragraph,
    add_signature_lines,
    add_signature_table,
    add_spacer,
    new_document,
)
from sydel_doc_engine.utils.grammar import accord_fonction, euro_word, montant_avec_euros
from sydel_doc_engine.utils.months import FRENCH_MONTHS

OUTPUT_FILENAME = "pv_nomination_gerant.docx"
DOCUMENT_CODE = "CODE-PV-001"

# Retours Albane 2026-07-09 (PV micro holding). Ces trois conventions sont
# SCOPEES a la micro holding (societe civile a capital variable) : les autres
# types (SELARL / SELAS / SCI / SCM / SCS...) restent byte-identiques.
#   C1 : entete + 1re phrase affichent « Societe civile » (texte fige) au lieu de
#        la cle interne de structure (« MICRO_HOLDING »).
#   C2 : la mention de capital (entete + 1re phrase) reflete le capital VARIABLE,
#        avec la formulation deja validee sur la domiciliation micro
#        (« a capital variable au capital minimum de X € et au capital effectif
#        de X € »).
#   C3 : la date de l'encadre du PV au format « 09 JUILLET 2026 » (jour 2 chiffres,
#        mois en toutes lettres MAJUSCULES accentuees, annee).
_MICRO_HOLDING_FORME_DISPLAY = "Société civile"
_DDMMYYYY_RE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")


def _is_micro_holding(ctx: DocumentGenerationContext) -> bool:
    return (ctx.structure or "").strip().upper() == "MICRO_HOLDING"


def _capital_variable_line(company: Company, *, capitalize: bool) -> str:
    """C2 : mention capital variable REUTILISEE du modele micro de la domiciliation
    (autorisation_domiciliation `_apply_micro_holding_capital_variable`) :
    « à capital variable au capital minimum de X € et au capital effectif de X € ».

    `capitalize=True` -> « À » en tete de la ligne d'en-tete (le reste du wording est
    strictement identique a la domiciliation, montant groupe par 3 via group_montant).
    """
    cap = group_montant(_capital_social(company))
    prefix = "À" if capitalize else "à"
    return (
        f"{prefix} capital variable au capital minimum de {cap} € "
        f"et au capital effectif de {cap} €"
    )


def _framed_date_display(value: date | str | None, *, is_micro: bool) -> str:
    """Date de l'encadre du PV. Comportement historique (DD/MM/AAAA) pour tous les
    types ; C3 (micro holding) : « JJ MOIS AAAA » (mois MAJUSCULE accentue)."""
    base = _required_display_value(value, "decision.date")
    if not is_micro:
        return base
    match = _DDMMYYYY_RE.match(base.strip())
    if match is None:
        return base  # forme inattendue : ne pas inventer de date
    day, month, year = (int(part) for part in match.groups())
    if not 1 <= month <= 12:
        return base
    return f"{day:02d} {FRENCH_MONTHS[month].upper()} {year}"

# Retour Albane 2026-06-26 (PV3) : « mettre de l'espace entre les paragraphes ».
# Espacement apres paragraphe renforce (10 pt vs 6 pt du profil standard), local
# au PV pour aerer le document sans impacter les autres generateurs.
_PV_PARAGRAPH_SPACE_AFTER_PT = 10

# Mise en forme (Albane, retour « mise en forme » 2026-07) : « interligne 0 » sur
# la designation de la societe (en-tete), la designation du client, et CHAQUE
# decision de l'AG. « interligne 0 » = interligne SIMPLE/compact (pas d'interligne
# multiple), et NON une hauteur de ligne nulle. On applique donc un interligne
# SIMPLE (1.0) explicite sur les paragraphes vises (l'espacement APRES-paragraphe
# et l'espace-avant des titres de decision sont conserves : l'aeration inter-blocs
# demeure, seul l'interligne INTRA-paragraphe passe a simple).
_PV_SINGLE_LINE_SPACING = 1.0

# P1 (Rafael 2026-07-09 soir) : « ne pas mettre d'espaces pour la designation du client
# ni pour les decisions ». Le lot « mise en forme 18 » (1.4) avait pose l'interligne SIMPLE
# mais GARDE l'espacement-apres renforce (10 pt) -> il restait un « espace parasite » entre
# CHAQUE ligne de la designation du client (nom / naissance / adresse / nationalite) et a
# l'interieur des decisions. On resserre ces blocs a l'espacement COMPACT (2 pt, identique a
# l'en-tete societe que le client accepte), qui rend ces lignes contigues comme le modele.
# L'aeration ENTRE decisions est preservee (space_before 10 pt du titre de decision) :
# « espace entre 1re decision et texte suivant » (1.4) conserve.
_PV_COMPACT_SPACE_AFTER_PT = 2

VOTE_FORMULA = "Cette résolution est adoptée à l’unanimité"
POWERS_TEXT = (
    "L’assemblée générale confère tous les pouvoirs au porteur d’un original à l’effet de procéder "
    "aux formalités d’enregistrement au greffe du Tribunal de Commerce de la Société."
)

# Titres ordinaux des decisions (PREMIERE, DEUXIEME, ...). Couvre largement le
# nombre de decisions possible (jusqu'a 3 dirigeants + emprunt + pouvoirs).
_DECISION_ORDINALS = (
    "PREMIERE DECISION",
    "DEUXIEME DECISION",
    "TROISIEME DECISION",
    "QUATRIEME DECISION",
    "CINQUIEME DECISION",
    "SIXIEME DECISION",
)


class PvNominationGerantGenerator:
    """Générateur from-scratch du PV nomination gérant."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        company = _required_company(ctx.societe)
        associes = _required_associes(ctx.associes)
        is_micro = _is_micro_holding(ctx)

        # Retour Albane 2026-06-10 : avec UN SEUL associe, le PV est un PV des
        # DECISIONS DE L'ASSOCIE UNIQUE (pas d'assemblee generale, pas de bloc
        # « associes presents »), structure simplifiee du modele qu'elle a fourni.
        # Les types reellement multi-associes (SCI/SCM/SCS/SELAS...) conservent la
        # structure AG existante.
        if len(associes) == 1:
            document = _build_associe_unique_pv(ctx, company, associes[0], is_micro=is_micro)
        else:
            capital = _required_capital(ctx.capital)
            # Liste des dirigeants nommes : extension ADDITIVE (modele PV
            # nominations dirigeants, SELAS). Si `dirigeants_nomines` est fourni,
            # une decision par dirigeant ; sinon, mode mono historique avec
            # `dirigeant_nomine` (un seul gerant). Comportement mono inchange.
            dirigeants = _resolve_dirigeants(ctx)
            represented_associes = _represented_associes(associes)
            represented_parts = _validated_represented_parts(capital, represented_associes)
            emprunt = ctx.emprunt or Emprunt(actif=False)
            bien_immobilier = _required_bien_immobilier(ctx.bien_immobilier, emprunt)
            titre_word = _titre_word(capital)

            document = new_document()
            _add_company_header(
                document,
                company,
                associes,
                is_micro=is_micro,
                spfpl_profession_pluriel=_spfpl_profession_pluriel(ctx),
            )
            _add_title_and_meeting(document, ctx, is_micro=is_micro)
            _add_introduction(document, company, capital, associes, is_micro=is_micro)
            _add_associes_block(document, represented_associes, represented_parts, titre_word)
            _add_order_of_business(document, ctx, dirigeants, emprunt, bien_immobilier)
            ordinal_index = _add_nomination_decisions(document, dirigeants)
            ordinal_index = _add_borrowing_decision(
                document, emprunt, bien_immobilier, ordinal_index
            )
            _add_powers_decision(document, ordinal_index)
            _add_closing_and_signatures(document, ctx, associes, dirigeants, is_micro=is_micro)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def _required_capital(capital: CapitalContext | None) -> CapitalContext:
    if capital is None:
        raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
    return capital


def _required_dirigeant(dirigeant: DirigeantNomine | None) -> DirigeantNomine:
    if dirigeant is None:
        raise ValueError(f"dirigeant_nomine est obligatoire pour {DOCUMENT_CODE}.")
    return dirigeant


def _resolve_dirigeants(ctx: DocumentGenerationContext) -> list[DirigeantNomine]:
    """Liste des dirigeants nommes pour le PV (mode AG multi-associes).

    Extension ADDITIVE (modele PV nominations dirigeants, SELAS) :
    - `dirigeants_nomines` non vide -> une decision par dirigeant (President,
      Directeur General, eventuel DG delegue), dans l'ordre fourni ;
    - sinon -> mode mono historique : un seul gerant porte par `dirigeant_nomine`.
    """
    if ctx.dirigeants_nomines:
        return list(ctx.dirigeants_nomines)
    return [_required_dirigeant(ctx.dirigeant_nomine)]


def _titre_word(capital: CapitalContext) -> str:
    """Vocabulaire du titre social : « actions » (SELAS) ou « parts » (defaut).

    Determine par `capital.type_titre` (le SELAS multi le positionne a
    « actions »). Defaut « parts » -> comportement historique inchange pour
    SELARL / civils.
    """
    type_titre = (capital.type_titre or "").strip().lower()
    if type_titre.startswith("action"):
        return "action"
    return "part"


def _required_associes(associes: list[Associe]) -> list[Associe]:
    if not associes:
        raise ValueError(f"associes[] doit contenir au moins un associé pour {DOCUMENT_CODE}.")
    return associes


def _represented_associes(associes: list[Associe]) -> list[Associe]:
    represented = [associe for associe in associes if associe.est_present_ou_represente]
    if not represented:
        raise ValueError(
            "associes[] doit contenir au moins un associé présent ou représenté "
            f"pour {DOCUMENT_CODE}."
        )
    return represented


def _required_bien_immobilier(
    bien_immobilier: BienImmobilier | None,
    emprunt: Emprunt,
) -> BienImmobilier | None:
    if not emprunt.actif:
        return None
    if bien_immobilier is None:
        raise ValueError("bien_immobilier est obligatoire si emprunt.actif=true.")
    return bien_immobilier


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def _required_positive_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if value < 1:
        raise ValueError(f"{field_name} doit être supérieur ou égal à 1 pour {DOCUMENT_CODE}.")
    return value


def _required_display_value(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return _required_text(value, field_name)


def _required_address(address: Address | None, field_name: str) -> Address:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    # Numero de voie optionnel (champ fusionne « Numero et voie », retours
    # client 2026-06-11) : une adresse sans numero (lieu-dit) reste valide.
    _required_text(address.voie, f"{field_name}.voie")
    _required_text(address.cp, f"{field_name}.cp")
    _required_text(address.ville, f"{field_name}.ville")
    return address


def _address_inline(address: Address) -> str:
    num_voie = (address.num_voie or "").strip()
    voie = _required_text(address.voie, "adresse.voie")
    cp = _required_text(address.cp, "adresse.cp")
    ville = _required_text(address.ville, "adresse.ville")
    return f"{num_voie} {voie}, {cp} {ville}".strip()


def _address_no_comma(address: Address) -> str:
    num_voie = (address.num_voie or "").strip()
    voie = _required_text(address.voie, "adresse.voie")
    cp = _required_text(address.cp, "adresse.cp")
    ville = _required_text(address.ville, "adresse.ville")
    return f"{num_voie} {voie} {cp} {ville}".strip()


def _validated_represented_parts(
    capital: CapitalContext,
    represented_associes: list[Associe],
) -> int:
    nb_parts_total = _required_positive_int(capital.nb_parts_total, "capital.nb_parts_total")
    represented_parts = sum(associe.nb_parts for associe in represented_associes)
    if (
        capital.nb_parts_representees is not None
        and capital.nb_parts_representees != represented_parts
    ):
        raise ValueError(
            "capital.nb_parts_representees doit correspondre à la somme des parts des associés "
            f"présents ou représentés pour {DOCUMENT_CODE}."
        )
    if represented_parts != nb_parts_total:
        raise ValueError(
            "Les parts présentes ou représentées doivent correspondre à la totalité du capital "
            f"pour {DOCUMENT_CODE}."
        )
    return represented_parts


def _parts_label(nb_parts: int, titre_word: str = "part") -> str:
    return titre_word if nb_parts == 1 else f"{titre_word}s"


def _nomination_agenda_label(fonction_affichage: str) -> str:
    normalized = fonction_affichage.strip().lower()
    if "gérant" in normalized or "gerant" in normalized:
        if normalized.endswith("s"):
            return "Nomination des premiers gérants"
        return "Nomination du gérant"
    if normalized.endswith("s"):
        return f"Nomination des {fonction_affichage}"
    return f"Nomination du {fonction_affichage}"


def _ne_label(genre: Gender) -> str:
    return "née" if genre == Gender.FEMININ else "né"


def _capital_social(company: Company) -> str:
    return _required_text(company.capital_social or company.capital, "societe.capital_social")


def _capital_social_header(company: Company) -> str:
    # Rafael 2026-07-09 : unite ACCORDEE (« 1 euro » / « 600 euros », jamais
    # « 1 euros ») ; montant_avec_euros est idempotent (saisie legacy avec unite
    # -> intacte) et couvre la garde « euro/eur/€ deja present » ci-dessus (R13).
    return montant_avec_euros(_capital_social(company))


def _forme_sociale_affichage(company: Company) -> str:
    return _required_text(
        company.forme_sociale_affichage or company.forme_sociale,
        "societe.forme_sociale_affichage",
    )


def _forme_sociale_header(
    company: Company,
    associes: list[Associe],
    *,
    spfpl_profession_pluriel: str | None = None,
) -> str:
    spfplas = _spfplas_forme_header(company, spfpl_profession_pluriel)
    if spfplas is not None:
        return spfplas
    base = _known_forme_sociale_header(company) or _required_text(
        company.forme_sociale_complete
        or company.forme_sociale_libelle_long
        or company.forme_sociale_affichage
        or company.forme_sociale,
        "societe.forme_sociale_complete",
    )
    profession = _sel_profession_for_header(company, associes)
    if profession and not _normalized_contains_profession(base, profession):
        return f"{base} de {profession}"
    return base


def _spfplas_forme_header(company: Company, profession_pluriel: str | None) -> str | None:
    """P2 (Rafael 2026-07-09) : en-tete d'une SPFPL par actions simplifiee (SPFPLAS).

    Rend la forme LEGALE COMPLETE validee — identique au titre des statuts SPFPL
    (`statuts_spfpl_templates`) et a l'identite de l'acquereur de l'acte de cession
    (`acte_cession_parts_spfpl`) : « Société de Participations Financières de Profession
    Libérale de <Profession-Plurielle> par actions simplifiée ». Corrige le libelle
    « société de participations financières de professions libérales » pose par le front
    (spfpl_slice) : bonne casse, profession reglementee AU PLURIEL, forme « par actions
    simplifiée ». Sans profession plurielle connue -> None (repli sur le libelle existant :
    aucune pluralisation inventee)."""
    acronym = (company.forme_sociale_abregee or company.forme_sociale or "").strip().upper()
    if acronym not in {"SPFPL", "SPFPLAS"}:
        return None
    profession = (profession_pluriel or "").strip()
    if not profession:
        return None
    return (
        "Société de Participations Financières de Profession Libérale de "
        f"{profession.title()} par actions simplifiée"
    )


def _spfpl_profession_pluriel(ctx: DocumentGenerationContext) -> str | None:
    """Profession reglementee AU PLURIEL pour l'en-tete SPFPLAS (P2).

    Source = le contexte du dossier SPFPL : le cedant / l'apporteur portent
    `profession_reglementee_pluriel` (deja validee, utilisee par l'acte de cession
    DOC-040). Repli sur un associe qui la porterait. On n'utilise QUE des valeurs
    PLURIELLES fournies par le contexte — jamais de pluralisation devinee a partir
    du singulier."""
    for source in (ctx.cedant, ctx.apporteur):
        if source is not None:
            value = getattr(source, "profession_reglementee_pluriel", None)
            if value and value.strip():
                return value.strip()
    for associe in ctx.associes or []:
        value = getattr(associe, "profession_reglementee_pluriel", None)
        if value and value.strip():
            return value.strip()
    return None


def _known_forme_sociale_header(company: Company) -> str | None:
    acronym = (company.forme_sociale_abregee or company.forme_sociale or "").strip().upper()
    if acronym == "SELARL":
        return "Société d’exercice libéral à responsabilité limitée"
    if acronym == "SELAS":
        return "Société d’exercice libéral par actions simplifiée"
    return None


def _sel_profession_for_header(company: Company, associes: list[Associe]) -> str | None:
    acronym = (company.forme_sociale_abregee or company.forme_sociale or "").strip().upper()
    if acronym not in {"SELARL", "SELAS"}:
        return None
    for associe in associes:
        # Retour Albane 2026-06-26 (PV2) : l'entete doit afficher la PROFESSION
        # (« médecin » / « chirurgien-dentiste »), jamais le TITRE « Docteur ».
        # On privilegie la profession reglementee/qualification ; « Docteur »
        # (titre derive cote front) est ecarte comme valeur d'entete.
        candidates = (
            associe.profession_reglementee,
            associe.qualification_principale,
            associe.profession,
        )
        for candidate in candidates:
            if candidate and candidate.strip() and not _is_title_only(candidate):
                return candidate.strip()
    return None


def _is_title_only(value: str) -> bool:
    """Vrai si `value` est un TITRE d'adresse (« Docteur ») et non une profession.

    Un titre ne doit jamais alimenter l'entete profession (retour Albane PV2).
    """
    return value.strip().casefold() in {"docteur", "dr", "dr."}


def _normalized_contains_profession(base: str, profession: str) -> bool:
    normalized_base = _normalize_for_prefix(base)
    normalized_profession = _normalize_for_prefix(profession)
    return normalized_base.endswith(f" de {normalized_profession}")


def _capital_variable_mention(company: Company) -> str:
    if company.capital_variable is False:
        raise ValueError(
            "societe.capital_variable=false n'est pas couvert par la spec texte V1 "
            f"pour {DOCUMENT_CODE}."
        )
    return (
        company.capital_variable_mention
        if company.capital_variable_mention is not None
        else " à capital variable"
    )


def _capital_variable_formule_intro(company: Company) -> str:
    if company.capital_variable is False:
        raise ValueError(
            "societe.capital_variable=false n'est pas couvert par la spec texte V1 "
            f"pour {DOCUMENT_CODE}."
        )
    return (
        company.capital_variable_formule_intro
        if company.capital_variable_formule_intro is not None
        else "à capital variable"
    )


def _add_paragraph(
    document,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    space_before: int = 0,
    space_after: int = _PV_PARAGRAPH_SPACE_AFTER_PT,
    single_line_spacing: bool = False,
) -> None:
    paragraph = add_paragraph(
        document,
        text,
        alignment=alignment,
        bold=bold,
        italic=italic,
        underline=underline,
        space_before_pt=space_before,
        space_after_pt=space_after,
    )
    # Mise en forme Albane 2026-07 : interligne SIMPLE (1.0) sur les paragraphes
    # vises (designation societe/client, decisions de l'AG).
    if single_line_spacing:
        paragraph.paragraph_format.line_spacing = _PV_SINGLE_LINE_SPACING


def _add_list_item(
    document,
    text: str,
    *,
    single_line_spacing: bool = False,
    space_after: int = _PV_PARAGRAPH_SPACE_AFTER_PT,
) -> None:
    # Retour Albane 2026-06-26 (PV3) : aerer entre les paragraphes (espace apres
    # chaque item de liste aligne sur l'espacement renforce du PV). P1 (Rafael
    # 2026-07-09) : les items de DESIGNATION du client et d'ENONCIATION des decisions
    # passent en espacement COMPACT (`space_after=_PV_COMPACT_SPACE_AFTER_PT`).
    paragraph = add_hyphen_list_item(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        space_after_pt=space_after,
    )
    # Mise en forme Albane 1.4 : interligne SIMPLE (1.0) sur la designation du
    # client (item nominatif de l'associe unique ET enumeration des associes en
    # AG multi). L'espace APRES-paragraphe (aeration inter-items) est conserve ;
    # seul l'interligne INTRA-paragraphe passe a simple.
    if single_line_spacing:
        paragraph.paragraph_format.line_spacing = _PV_SINGLE_LINE_SPACING


def _add_decision_title(document, title: str) -> None:
    _add_paragraph(
        document,
        title,
        bold=True,
        underline=True,
        space_before=10,
        space_after=2,
    )


def _add_vote_formula(document) -> None:
    # P1 (Rafael 2026-07-09) : la formule de vote cloture une decision -> espacement COMPACT
    # (tight a l'interieur de la decision ; l'aeration entre decisions est portee par le
    # space_before du titre de decision suivant).
    _add_paragraph(document, VOTE_FORMULA, italic=True, space_after=_PV_COMPACT_SPACE_AFTER_PT)


def _add_company_header(
    document,
    company: Company,
    associes: list[Associe],
    *,
    is_micro: bool = False,
    spfpl_profession_pluriel: str | None = None,
) -> None:
    siege = _required_address(company.siege, "societe.siege")
    # C1 : « Société civile » (texte fige) en entete pour la micro holding, au lieu
    #      de la cle interne de structure. C2 : ligne de capital VARIABLE.
    forme_line = (
        _MICRO_HOLDING_FORME_DISPLAY
        if is_micro
        else _forme_sociale_header(
            company, associes, spfpl_profession_pluriel=spfpl_profession_pluriel
        )
    )
    capital_line = (
        _capital_variable_line(company, capitalize=True)
        if is_micro
        else f"Au capital de {_capital_social_header(company)}"
    )
    lines = [
        (_required_text(company.denomination, "societe.denomination"), True, False),
        forme_line,
        capital_line,
        f"Siège social : {_address_no_comma(siege)}",
        "En cours d’immatriculation",
    ]
    header_paragraphs = add_centered_block(document, lines, space_after_pt=2)
    # Mise en forme Albane 2026-07 : interligne SIMPLE sur la designation de la
    # societe (en-tete).
    for paragraph in header_paragraphs:
        paragraph.paragraph_format.line_spacing = _PV_SINGLE_LINE_SPACING


def _add_title_and_meeting(
    document,
    ctx: DocumentGenerationContext,
    *,
    is_micro: bool = False,
) -> None:
    decision = ctx.decision
    reunion = ctx.reunion
    if decision is None:
        raise ValueError(f"decision est obligatoire pour {DOCUMENT_CODE}.")
    if reunion is None:
        raise ValueError(f"reunion est obligatoire pour {DOCUMENT_CODE}.")

    add_spacer(document)
    add_framed_title(
        document,
        [
            "PROCES-VERBAL DES DECISIONS",
            " DE L’ASSEMBLEE GENERALE",
            f" DU {_framed_date_display(decision.date, is_micro=is_micro)}",
        ],
    )
    _add_paragraph(document, f"Le {_required_text(reunion.date_lettres, 'reunion.date_lettres')}")


def _add_president_sentence(document, ctx: DocumentGenerationContext) -> None:
    if ctx.reunion is None or ctx.reunion.president is None:
        return
    president = ctx.reunion.president
    civilite = _president_civilite(president)
    prenom = _president_prenom(president)
    nom = _president_nom(president)
    if civilite is None and prenom is None and nom is None:
        return
    _add_paragraph(
        document,
        (
            f"{_required_text(civilite, 'reunion.president.civilite_president_seance')} "
            f"{_required_text(prenom, 'reunion.president.prenom_president_seance')} "
            f"{_required_text(nom, 'reunion.president.nom_personne_seance')} "
            "préside la séance."
        ),
    )


def _president_civilite(president: ReunionPresident) -> str | None:
    return president.civilite_president_seance or president.civilite_affichage


def _president_prenom(president: ReunionPresident) -> str | None:
    return president.prenom_president_seance or president.prenom


def _president_nom(president: ReunionPresident) -> str | None:
    return president.nom_personne_seance or president.nom


def _add_introduction(
    document,
    company: Company,
    capital: CapitalContext,
    associes: list[Associe],
    *,
    is_micro: bool = False,
) -> None:
    denomination = _required_text(company.denomination, "societe.denomination")
    company_designation = _company_designation_for_intro(
        company, denomination, is_micro=is_micro
    )
    nb_parts_total = _required_positive_int(capital.nb_parts_total, "capital.nb_parts_total")
    titre_word = _titre_word(capital)
    if titre_word == "action":
        # Phrase verbatim du modele PV nominations dirigeants (SELAS) : pas de
        # clause « de {valeur} euro chacune », « au siege de la Societe ».
        # Rafael 2026-07-09 : le capital porte « euros » (accorde) comme l'en-tete —
        # montant_avec_euros (groupe + unite) au lieu de group_montant (montant nu).
        text = (
            f"Les associés de la {company_designation}, au capital de "
            f"{montant_avec_euros(_capital_social(company))}, "
            f"composé de {nb_parts_total} actions, "
            "se sont réunis au siège de la Société."
        )
        _add_paragraph(
            document,
            text,
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            single_line_spacing=True,
        )
        return
    valeur_nominale = _required_text(
        capital.valeur_nominale_part,
        "capital.valeur_nominale_part",
    )
    # C2 : pour la micro holding (capital variable), la 1re phrase reflete le capital
    # variable (meme wording que la domiciliation) ; les autres civils gardent
    # « au capital de <montant> ».
    # Rafael 2026-07-09 : hors micro (capital variable en « € »), le capital de la
    # 1re phrase porte « euros » (accorde), aligne sur l'en-tete (_capital_social_header)
    # au lieu du montant nu group_montant qui laissait « au capital de 1 000 ».
    capital_clause = (
        _capital_variable_line(company, capitalize=False)
        if is_micro
        else f"au capital de {montant_avec_euros(_capital_social(company))}"
    )
    common = (
        f"de la {company_designation}, {capital_clause}, "
        f"composé de {nb_parts_total} parts de {valeur_nominale} "
        f"{euro_word(valeur_nominale)} chacune, "
    )
    text = f"Les associés {common}se sont réunis au siège social."
    _add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        single_line_spacing=True,
    )


def _company_designation_for_intro(
    company: Company,
    denomination: str,
    *,
    is_micro: bool = False,
) -> str:
    # C1 : « Société civile <denomination> » (texte fige) pour la micro holding.
    forme = _MICRO_HOLDING_FORME_DISPLAY if is_micro else _forme_sociale_affichage(company)
    if _denomination_starts_with_form(denomination, company, forme):
        return denomination
    return f"{forme} {denomination}"


def _denomination_starts_with_form(
    denomination: str,
    company: Company,
    forme: str,
) -> bool:
    normalized_denomination = _normalize_for_prefix(denomination)
    candidates = [
        forme,
        company.forme_sociale_abregee,
    ]
    return any(
        normalized_denomination.startswith(_normalize_for_prefix(candidate) + " ")
        or normalized_denomination == _normalize_for_prefix(candidate)
        for candidate in candidates
        if candidate and _normalize_for_prefix(candidate)
    )


def _normalize_for_prefix(value: str) -> str:
    return " ".join(value.casefold().replace("’", "'").split())


def _add_associes_block(
    document,
    associes: list[Associe],
    represented_parts: int,
    titre_word: str = "part",
) -> None:
    _add_paragraph(document, "Sont présents ou représentés :")
    for associe in associes:
        _add_list_item(
            document,
            (
                f"{associe.civilite_affichage} {associe.prenom} {associe.nom}, "
                f"détenant {associe.nb_parts} {_parts_label(associe.nb_parts, titre_word)},"
            ),
            # Mise en forme Albane 1.4 : interligne simple sur la designation des
            # clients (enumeration des associes presents/representes en AG multi).
            # P1 (Rafael 2026-07-09) : espacement COMPACT (pas d'espace parasite entre
            # les associes designes).
            single_line_spacing=True,
            space_after=_PV_COMPACT_SPACE_AFTER_PT,
        )
    if titre_word == "action":
        # Clause verbatim du modele PV nominations dirigeants (SELAS).
        closing = (
            "Les associés présents ou représentés disposent ensemble la totalité des actions "
            "formant le capital de la société. L’assemblée est habilitée à prendre les "
            "décisions extraordinaires."
        )
    else:
        closing = (
            "Les associés présents ou représentés disposent ensemble de la totalité des parts "
            "sociales. Cet ensemble est habilité à prendre des décisions."
        )
    _add_paragraph(document, closing, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)


def _ordinal_title(index: int) -> str:
    if 0 <= index < len(_DECISION_ORDINALS):
        return _DECISION_ORDINALS[index]
    raise ValueError(
        f"Trop de decisions pour {DOCUMENT_CODE} : pas d'ordinal pour l'index {index}."
    )


def _add_order_of_business(
    document,
    ctx: DocumentGenerationContext,
    dirigeants: list[DirigeantNomine],
    emprunt: Emprunt,
    bien_immobilier: BienImmobilier | None,
) -> None:
    _add_president_sentence(document, ctx)
    _add_paragraph(document, "Le président rappelle l’ordre du jour :")
    # Retour Albane 2026-06-26 (PV4) : points de l'ordre du jour prefixes d'un
    # tiret « - » (et non plus du point median « · »), comme la structure
    # associe unique du meme PV (coherence intra-document).
    # P1 (Rafael 2026-07-09) : enonciations des decisions en espacement COMPACT.
    for dirigeant in dirigeants:
        fonction_affichage = _required_text(
            dirigeant.fonction_affichage,
            "dirigeant_nomine.fonction_affichage",
        )
        _add_list_item(
            document,
            _nomination_agenda_label(fonction_affichage),
            space_after=_PV_COMPACT_SPACE_AFTER_PT,
        )
    if emprunt.actif:
        bien_adresse = _address_inline(
            _required_address(
                bien_immobilier.adresse if bien_immobilier else None,
                "bien_immobilier.adresse",
            )
        )
        _add_list_item(
            document,
            (
                "Autorisation de contracter un emprunt pour l’achat d’un bien immobilier sis "
                f"{bien_adresse}"
            ),
            space_after=_PV_COMPACT_SPACE_AFTER_PT,
        )
    _add_list_item(document, "Pouvoirs", space_after=_PV_COMPACT_SPACE_AFTER_PT)


def _add_nomination_decisions(
    document,
    dirigeants: list[DirigeantNomine],
) -> int:
    """Une decision de nomination par dirigeant (PREMIERE, DEUXIEME, ...).

    Retourne l'index ordinal de la PROCHAINE decision (emprunt ou pouvoirs).
    Mono-dirigeant -> une seule decision « PREMIERE DECISION » (inchange).

    Mode modele (modele PV nominations dirigeants, SELAS) : declenche des qu'on
    a PLUSIEURS dirigeants ou qu'une phrase d'identite verbatim est fournie. Il
    applique la virgule du modele (« en qualite de Président, pour une duree
    indeterminee : ») ; le mode mono historique reste sans virgule.
    """
    use_model_wording = len(dirigeants) > 1 or any(d.identite_phrase for d in dirigeants)
    for ordinal_index, dirigeant in enumerate(dirigeants):
        _add_single_nomination_decision(document, dirigeant, ordinal_index, use_model_wording)
    return len(dirigeants)


def _add_single_nomination_decision(
    document,
    dirigeant: DirigeantNomine,
    ordinal_index: int,
    use_model_wording: bool,
) -> None:
    fonction_affichage = _required_text(
        dirigeant.fonction_affichage,
        "dirigeant_nomine.fonction_affichage",
    )
    nationality = _required_text(
        dirigeant.nationalite,
        "dirigeant_nomine.nationalite",
    )
    _add_decision_title(document, _ordinal_title(ordinal_index))
    separator = ", pour" if use_model_wording else " pour"
    # P1 (Rafael 2026-07-09) : le corps de la decision est resserre (espacement COMPACT),
    # l'aeration entre decisions restant portee par le space_before du titre suivant.
    _add_paragraph(
        document,
        (
            "L’assemblée générale décide de désigner en qualité de "
            f"{fonction_affichage}{separator} une durée indéterminée :"
        ),
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    # Phrase d'identite : verbatim du modele si fournie (`identite_phrase`),
    # sinon reconstruite a partir des champs (comportement historique).
    if dirigeant.identite_phrase:
        identite = _required_text(dirigeant.identite_phrase, "dirigeant_nomine.identite_phrase")
        _add_paragraph(
            document,
            identite,
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            bold=True,
            single_line_spacing=True,
            space_after=_PV_COMPACT_SPACE_AFTER_PT,
        )
    else:
        address = _required_address(
            dirigeant.adresse_personnelle,
            "dirigeant_nomine.adresse_personnelle",
        )
        birth_date = _required_display_value(
            dirigeant.date_naissance,
            "dirigeant_nomine.date_naissance",
        )
        birth_city = _required_text(
            dirigeant.ville_naissance,
            "dirigeant_nomine.ville_naissance",
        )
        birth_department = _required_text(
            dirigeant.departement_naissance,
            "dirigeant_nomine.departement_naissance",
        )
        _add_paragraph(
            document,
            (
                f"{dirigeant.civilite_affichage} {dirigeant.prenom} {dirigeant.nom}, "
                f"{_ne_label(dirigeant.genre)} le {birth_date} à {birth_city} "
                f"({birth_department}), de nationalité {nationality}, "
                f"demeurant au {_address_inline(address)}."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            single_line_spacing=True,
            space_after=_PV_COMPACT_SPACE_AFTER_PT,
        )
    _add_vote_formula(document)


def _add_borrowing_decision(
    document,
    emprunt: Emprunt,
    bien_immobilier: BienImmobilier | None,
    ordinal_index: int,
) -> int:
    """Decision d'emprunt (si actif). Retourne l'index ordinal suivant."""
    if not emprunt.actif:
        return ordinal_index
    bien_adresse = _address_inline(
        _required_address(
            bien_immobilier.adresse if bien_immobilier else None,
            "bien_immobilier.adresse",
        )
    )
    montant = _required_text(emprunt.montant_max, "emprunt.montant_max")
    _add_decision_title(document, _ordinal_title(ordinal_index))
    _add_paragraph(
        document,
        (
            "L’assemblée générale décide de contracter un emprunt d’un montant "
            f"maximum de {montant} euros pour l’acquisition d’un bien immobilier sis "
            f"{bien_adresse}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_vote_formula(document)
    return ordinal_index + 1


def _add_powers_decision(document, ordinal_index: int) -> None:
    _add_decision_title(document, _ordinal_title(ordinal_index))
    _add_paragraph(
        document,
        POWERS_TEXT,
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_vote_formula(document)


def _add_closing_and_signatures(
    document,
    ctx: DocumentGenerationContext,
    associes: list[Associe],
    dirigeants: list[DirigeantNomine],
    *,
    is_micro: bool = False,
) -> None:
    lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")
    # Retour Albane 2026-06-26 (PV6) : supprimer la mention « en quatre
    # exemplaires » apres le lieu. Seul « Fait à {lieu} » subsiste.
    _add_paragraph(
        document,
        f"Fait à {lieu_signature}",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    add_spacer(document)
    if len(dirigeants) > 1:
        _add_multi_dirigeant_signatures(document, dirigeants)
        return
    dirigeant = dirigeants[0]
    fonction_affichage = _required_text(
        dirigeant.fonction_affichage,
        "dirigeant_nomine.fonction_affichage",
    )
    if is_micro:
        # C4 (Albane 2026-07-09, presentation cible img_09) : chaque associe signe
        # SOUS SON PROPRE NOM, avec une zone de signature dediee sous chaque nom (au
        # lieu des noms empiles sans espace). La mention « Bon pour acceptation... »
        # est conservee (une fois, comme le modele existant).
        for associe in associes:
            add_signature_lines(
                document,
                [f"{associe.prenom} {associe.nom}"],
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=True,
            )
            _add_signature_space(document)
    else:
        add_signature_lines(
            document,
            [f"{associe.prenom} {associe.nom}" for associe in associes],
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
        )
    _add_paragraph(
        document,
        (
            "Faire précéder la signature de la mention « Bon pour acceptation des fonctions de "
            f"{fonction_affichage} »"
        ),
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        italic=True,
    )


def _add_signature_space(document) -> None:
    """Zone manuscrite de signature (lignes vides) sous un nom d'associe (C4)."""
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run("\n\n")


def _add_multi_dirigeant_signatures(
    document,
    dirigeants: list[DirigeantNomine],
) -> None:
    """Bloc signatures multi-colonnes du modele PV nominations dirigeants.

    Une colonne (case bordee) par dirigeant : le nom du dirigeant puis la
    mention « Bon pour acceptation des fonctions de {fonction} ». Wording
    verbatim du modele.

    Retour Albane 2026-06-26 (PV7) : les mentions « ne s'intercalent pas bien »
    avec le separateur tabulation precedent (les noms se decalaient quand la
    mention d'une colonne etait plus longue). On bascule sur des CASES (tableau
    2 colonnes, meme esprit que les statuts) : chaque case contient le nom + sa
    mention propre, alignes par colonne, plus aucun decalage, zone de signature
    suffisante (hauteur de ligne minimale).
    """
    labels = [
        [
            (
                f"{d.prenom} {d.nom}\n"
                "(Faire précéder de la mention « Bon pour acceptation des fonctions de "
                f"{_required_text(d.fonction_affichage, 'dirigeant_nomine.fonction_affichage')} »)"
            )
            for d in dirigeants
        ]
    ]
    add_signature_table(document, labels, min_row_height_cm=2.5)


# ---------------------------------------------------------------------------
# PV des decisions de l'ASSOCIE UNIQUE (retour Albane 2026-06-10) : structure
# simplifiee pour les societes a un seul associe (SELARL unipersonnelle...).
# « les associes » -> « l'associe », « assemblee generale » -> « associe unique »,
# pas de bloc « associes presents », ordre du jour en tirets.
# ---------------------------------------------------------------------------


def _fonction_accordee(fonction_affichage: str, genre: Gender) -> str:
    # Rafael 2026-07-09 : accord en genre par INTENTION via le helper partage
    # (gerant/president/associe... -> feminin), plus seulement « gerant » en dur.
    base = _required_text(fonction_affichage, "dirigeant_nomine.fonction_affichage")
    return accord_fonction(base, genre)


def _build_associe_unique_pv(
    ctx: DocumentGenerationContext,
    company: Company,
    associe: Associe,
    *,
    is_micro: bool = False,
):
    decision = ctx.decision
    reunion = ctx.reunion
    if decision is None:
        raise ValueError(f"decision est obligatoire pour {DOCUMENT_CODE}.")
    if reunion is None:
        raise ValueError(f"reunion est obligatoire pour {DOCUMENT_CODE}.")
    dirigeant = _required_dirigeant(ctx.dirigeant_nomine)

    # Identite de l'associe unique : on prefere la fiche associe si elle est
    # complete ; sinon on retombe sur le dirigeant nomme — MEME personne dans une
    # societe unipersonnelle (les flux SPFPL / civils portent l'identite sur le
    # dirigeant). La profession reste optionnelle (omise si absente).
    identity = associe if associe.adresse_personnelle is not None else dirigeant
    genre = identity.genre
    associe_word = "Associée" if genre == Gender.FEMININ else "Associé"
    associe_word_low = associe_word.lower()
    fonction = _fonction_accordee(dirigeant.fonction_affichage, genre)

    civilite = _required_text(identity.civilite_affichage, "identite.civilite_affichage")
    prenom = _required_text(identity.prenom, "identite.prenom")
    nom = _required_text(identity.nom, "identite.nom")
    address = _required_address(identity.adresse_personnelle, "identite.adresse_personnelle")
    birth_date = _required_display_value(identity.date_naissance, "identite.date_naissance")
    birth_city = _required_text(identity.ville_naissance, "identite.ville_naissance")
    nationality = _required_text(identity.nationalite, "identite.nationalite")
    profession = (
        associe.profession
        or associe.profession_reglementee
        or associe.qualification_principale
        or ""
    ).strip()
    profession_clause = f"{profession} de profession, " if profession else ""
    denomination = _required_text(company.denomination, "societe.denomination")

    document = new_document()
    _add_company_header(
        document,
        company,
        [associe],
        is_micro=is_micro,
        spfpl_profession_pluriel=_spfpl_profession_pluriel(ctx),
    )
    add_spacer(document)
    # m2 (Akainu ronde 2, 2026-07-12) : le titre encadre du PV s'accorde au genre de l'associe
    # unique (« DE L’ASSOCIÉE UNIQUE » pour une femme), coherent avec le corps (« L'associée
    # unique »). Masculin inchange (« ASSOCIE »).
    associe_unique_titre = "ASSOCIÉE" if genre == Gender.FEMININ else "ASSOCIE"
    add_framed_title(
        document,
        [
            "PROCES-VERBAL DES DECISIONS",
            f" DE L’{associe_unique_titre} UNIQUE",
            f" DU {_framed_date_display(decision.date, is_micro=is_micro)}",
        ],
    )
    _add_paragraph(
        document,
        f"Le {_required_text(reunion.date_lettres, 'reunion.date_lettres')}",
    )

    # Identite de l'associe unique (bloc « soussigne » simplifie).
    # Mise en forme Albane 1.4 : interligne SIMPLE sur la designation du client
    # (nom, naissance, adresse, nationalite). P1 (Rafael 2026-07-09) : espacement
    # COMPACT — la designation du client est un bloc contigu (pas d'espace parasite
    # entre nom / naissance / adresse / nationalite / qualite).
    _add_list_item(
        document,
        f"{civilite} {prenom} {nom}",
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_paragraph(
        document,
        f"{_ne_label(genre).capitalize()} le {birth_date} à {birth_city}",
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_paragraph(
        document,
        f"Demeurant au {_address_inline(address)}",
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_paragraph(
        document,
        f"De nationalité {nationality}",
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_paragraph(
        document,
        (
            f"{associe_word} unique, propriétaire de toutes les "
            # Coherence parts/actions 2026-06-22 : « actions » pour une societe par actions
            # (SELAS/SAS, capital.type_titre='actions'), « parts » par defaut (SELARL/civils).
            f"{_titre_word(ctx.capital) if ctx.capital is not None else 'part'}s de la société "
            f"{denomination} en cours de formation."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_paragraph(
        document,
        "À l’issue de la signature des statuts, a pris les décisions suivantes :",
    )

    # Ordre du jour en TIRETS (retour Albane : lister / ajouter facilement).
    # P1 (Rafael 2026-07-09) : enonciations des decisions en espacement COMPACT.
    _add_list_item(
        document,
        _nomination_agenda_label(dirigeant.fonction_affichage),
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )
    _add_list_item(document, "Pouvoir", space_after=_PV_COMPACT_SPACE_AFTER_PT)

    # PREMIERE DECISION : nomination du gerant (l'associe unique se designe).
    # P1 : corps de decision resserre (l'aeration entre decisions = space_before du titre).
    _add_decision_title(document, "PREMIERE DECISION")
    _add_paragraph(
        document,
        (
            f"L’{associe_word_low} unique décide de désigner en qualité de {fonction} "
            f"{civilite} {prenom} {nom}, "
            f"{profession_clause}{_ne_label(genre)} le {birth_date} à {birth_city}, "
            f"de nationalité {nationality}, demeurant au {_address_inline(address)} "
            f"{associe_word_low} unique de la Société. Sa rémunération sera fixée ultérieurement."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )

    # DEUXIEME DECISION : pouvoir (formalites au greffe de la ville du RCS).
    ville_greffe = _required_text(
        company.ville_rcs or (company.siege.ville if company.siege else None),
        "societe.ville_rcs",
    )
    _add_decision_title(document, "DEUXIEME DECISION")
    _add_paragraph(
        document,
        (
            f"L’{associe_word_low} unique confère tous les pouvoirs au porteur d’un original à "
            "l’effet de procéder aux formalités d’enregistrement au greffe du Tribunal de "
            f"Commerce de la Société de {ville_greffe}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        single_line_spacing=True,
        space_after=_PV_COMPACT_SPACE_AFTER_PT,
    )

    # Cloture + signature de l'associe (« Bon pour acceptation des fonctions de gerant »).
    # Retour Albane 2026-06-26 (PV6) : supprimer « en X exemplaires » apres le lieu.
    lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")
    _add_paragraph(
        document,
        f"Fait à {lieu_signature}",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    add_spacer(document)
    add_signature_lines(
        document,
        [f"{prenom} {nom}"],
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
    )
    _add_paragraph(
        document,
        (
            "Faire précéder la signature de la mention « Bon pour acceptation des fonctions de "
            f"{fonction} »"
        ),
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        italic=True,
    )
    return document
