"""Slices des statuts civils (SCI, SCI IRIS, SCS, SCM) sur patron SELARL.

Ces quatre types partagent le meme contexte moteur (`StatutsCivilsContext`) et le
meme generateur de famille (statuts_civils). Le slice :
  1. expose une saisie societe + un repeater d'associes generique ;
  2. mappe ces saisies dans un `DocumentGenerationContext` valide ;
  3. appelle le generateur via `generate_docx_files_for_document_codes`.

Patron repris de `selarl_slice` : un contexte de DEFAUT valide (mirroir des
payloads de test/exemple, generation sans token residuel) sur lequel on
superpose les saisies utilisateur. Aucune regle metier nouvelle : on ne fait que
collecter et router vers le moteur existant.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import streamlit as st

from sydel_doc_engine.app.ui_runtime import (
    GeneratedDossier,
    generate_docx_files_for_document_codes,
    generate_zip_file,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Person,
    Signature,
    StatutsCivilsAssocie,
    StatutsCivilsCapitalDepot,
    StatutsCivilsContext,
    StatutsCivilsGroupeParts,
)
from sydel_doc_engine.front_app.associe_repeater import RepeaterConfig, render_associe_repeater
from sydel_doc_engine.front_app.field_derivations import (
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

# Mapping structure -> (type statuts civils, doc_code).
CIVIL_TYPE_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SCI": ("sci", "DOC-020"),
    "SCI IRIS": ("sci_iris", "DOC-021"),
    "SCS": ("scs", "DOC-019"),
    "SCM": ("scm", "DOC-025"),
}


@dataclass(frozen=True)
class CivilSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str


def _signature_date(structure: str) -> date | None:
    key = f"{_prefix(structure)}_signature_date"
    raw = st.session_state.get(key)
    parsed = parse_french_date(raw)
    return parsed


def _prefix(structure: str) -> str:
    return CIVIL_TYPE_BY_STRUCTURE[structure][0]


def render_civil_form(structure: str) -> dict[str, object]:
    """Rend la saisie societe + associes pour un type civil et retourne un payload."""

    statuts_type, _doc = CIVIL_TYPE_BY_STRUCTURE[structure]
    prefix = statuts_type
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe ({structure})**")

    col_a, col_b = st.columns(2)
    denomination = _text(col_a, prefix, "denomination", "Denomination sociale")
    forme_sociale = _text(col_b, prefix, "forme_sociale", "Forme sociale (libelle)")
    col_c, col_d = st.columns(2)
    capital_social = _text(col_c, prefix, "capital_social", "Capital social")
    nb_parts_total = _int(col_d, prefix, "nb_parts_total", "Nombre total de parts")
    col_e, col_f = st.columns(2)
    valeur_nominale = _text(col_e, prefix, "valeur_nominale_part", "Valeur nominale d'une part")
    duree = _text(col_f, prefix, "duree_societe", "Duree (annees)")

    st.markdown("Siege social")
    col_g, col_h, col_i, col_j = st.columns(4)
    siege_num = _text(col_g, prefix, "siege_num", "No")
    siege_voie = _text(col_h, prefix, "siege_voie", "Voie")
    siege_cp = _text(col_i, prefix, "siege_cp", "CP")
    siege_ville = _text(col_j, prefix, "siege_ville", "Ville")
    ville_rcs = _text(st, prefix, "ville_rcs", "RCS (ville)")

    st.markdown("Depot des fonds")
    col_k, col_l = st.columns(2)
    banque_nom = _text(col_k, prefix, "banque_nom", "Banque")
    banque_adresse = _text(col_l, prefix, "banque_adresse", "Adresse banque")
    date_cloture = _text(
        st, prefix, "date_cloture_premier_exercice", "Cloture du premier exercice"
    )

    st.markdown("**Signature**")
    col_m, col_n = st.columns(2)
    signature_lieu = _text(col_m, prefix, "signature_lieu", "Lieu de signature")
    with col_n:
        signature_date = _date_input(prefix, "signature_date", "Date de signature")

    role_options: tuple[str, ...] = ()
    if structure == "SCS":
        role_options = ("commandite", "commanditaire")

    associes = render_associe_repeater(
        RepeaterConfig(
            key_prefix=prefix,
            titre_unite="parts",
            nb_min=1 if structure in {"SCI", "SCM"} else 2,
            nb_max=6,
            nb_defaut=2,
            allow_personne_morale=True,
            role_statutaire_options=role_options,
        )
    )

    return {
        "structure": structure,
        "statuts_type": statuts_type,
        "denomination": denomination,
        "forme_sociale": forme_sociale,
        "capital_social": capital_social,
        "nb_parts_total": nb_parts_total,
        "valeur_nominale_part": valeur_nominale,
        "duree_societe": duree,
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "ville_rcs": ville_rcs,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "date_cloture_premier_exercice": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "associes": associes,
    }


def build_civil_plan(payload: dict[str, object]) -> CivilSlicePlan:
    structure = str(payload["structure"])
    _statuts_type, doc_code = CIVIL_TYPE_BY_STRUCTURE[structure]
    blockers = _validate(payload)
    warnings = (
        f"{structure} : creation, slice sur patron SELARL. Le moteur valide la coherence "
        "des parts / du capital.",
    )
    if blockers:
        return CivilSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=(doc_code,),
            blockers=blockers,
            warnings=warnings,
            target_engine_adapter="front_app.civil_statuts_slice",
        )
    return CivilSlicePlan(
        can_generate=True,
        status="ready",
        reason=f"Pret pour generation {structure} V1.",
        document_codes=(doc_code,),
        blockers=(),
        warnings=warnings,
        target_engine_adapter="front_app.civil_statuts_slice",
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    structure = str(payload["structure"])
    if not str(payload.get("denomination") or "").strip():
        blockers.append("Denomination sociale requise.")
    if not str(payload.get("capital_social") or "").strip():
        blockers.append("Capital social requis.")
    nb_parts_total = int(payload.get("nb_parts_total") or 0)
    if nb_parts_total < 1:
        blockers.append("Nombre total de parts requis et superieur a zero.")
    if not str(payload.get("valeur_nominale_part") or "").strip():
        blockers.append("Valeur nominale d'une part requise.")
    if not str(payload.get("siege_ville") or "").strip():
        blockers.append("Ville du siege requise.")
    if not str(payload.get("ville_rcs") or "").strip():
        blockers.append("Ville RCS requise.")
    if not str(payload.get("banque_nom") or "").strip():
        blockers.append("Banque de depot des fonds requise.")
    if not str(payload.get("date_cloture_premier_exercice") or "").strip():
        blockers.append("Date de cloture du premier exercice requise.")
    if not str(payload.get("signature_lieu") or "").strip():
        blockers.append("Lieu de signature requis.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or not associes:
        blockers.append("Au moins un associe requis.")
    else:
        if structure == "SCI" and any(
            a.type_personne == "personne_morale" for a in associes
        ):
            blockers.append("SCI : personne morale hors perimetre V1 (bloque par le moteur).")
        if structure == "SCI IRIS" and not any(
            a.type_personne == "personne_morale" for a in associes
        ):
            blockers.append("SCI IRIS : au moins une personne morale associee requise.")
        for idx, associe in enumerate(associes, start=1):
            if not _associe_named(associe):
                blockers.append(f"Identite de l'associe {idx} requise.")
            if associe.parts is None or not associe.parts.nb:
                blockers.append(f"Nombre de parts de l'associe {idx} requis.")
            if associe.apport is None or not str(associe.apport.montant or "").strip():
                blockers.append(f"Apport de l'associe {idx} requis.")
            if structure == "SCM" and not str(associe.profession or "").strip():
                blockers.append(f"Profession de l'associe {idx} requise (SCM).")
            if associe.type_personne == "personne_physique":
                for field, name in (
                    ("date_naissance", "date de naissance"),
                    ("ville_naissance", "ville de naissance"),
                    ("departement_naissance", "departement de naissance"),
                    ("nationalite", "nationalite"),
                    ("situation_maritale", "situation matrimoniale"),
                    ("adresse_personnelle_affichee", "adresse"),
                ):
                    if not str(getattr(associe, field) or "").strip():
                        blockers.append(f"Associe {idx} : {name} requise.")
        # Coherence dure exigee par le moteur : somme parts = nb_parts_total,
        # somme apports = capital_social. On la SURFACE en blocage front au lieu
        # de la decouvrir a la generation.
        if nb_parts_total:
            total_parts = sum((a.parts.nb or 0) for a in associes if a.parts)
            if total_parts != nb_parts_total:
                blockers.append(
                    f"Somme des parts ({total_parts}) != total declare ({nb_parts_total})."
                )
        capital = _safe_int(payload.get("capital_social"))
        if capital:
            total_apports = sum(
                _safe_int(a.apport.montant) for a in associes if a.apport
            )
            if total_apports != capital:
                blockers.append(
                    f"Somme des apports ({total_apports}) != capital social ({capital})."
                )
    if structure == "SCS":
        roles = {a.role_statutaire for a in associes if isinstance(associes, list)}
        if "commandite" not in roles or "commanditaire" not in roles:
            blockers.append("SCS : au moins un commandite ET un commanditaire requis.")
    return tuple(dict.fromkeys(blockers))


def _associe_named(associe: StatutsCivilsAssocie) -> bool:
    if associe.type_personne == "personne_morale":
        return bool((associe.denomination or "").strip())
    return bool((associe.prenom or "").strip()) and bool((associe.nom or "").strip())


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    structure = str(payload["structure"])
    statuts_type = str(payload["statuts_type"])
    associes: list[StatutsCivilsAssocie] = list(payload.get("associes") or [])

    siege = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=_siege_display(payload),
    )
    signataire = _first_physique_or_default(associes)
    capital = str(payload.get("capital_social") or "")
    nb_parts = int(payload.get("nb_parts_total") or 0)

    statuts_civils = StatutsCivilsContext(
        type=statuts_type,
        forme_sociale=str(payload.get("forme_sociale") or structure),
        mention_capital_variable="a capital variable",
        capital_social=capital,
        capital_social_lettres=number_words_from_value(capital),
        capital_autorise=str(int(_safe_int(capital) * 10)) if _safe_int(capital) else None,
        capital_autorise_lettres=number_words_from_value(_safe_int(capital) * 10)
        if _safe_int(capital)
        else None,
        capital_maximal=str(int(_safe_int(capital) * 10)) if _safe_int(capital) else None,
        capital_maximal_lettres=number_words_from_value(_safe_int(capital) * 10)
        if _safe_int(capital)
        else None,
        nb_parts_total=nb_parts,
        nb_parts_total_lettres=number_words_from_value(nb_parts),
        valeur_nominale_part=str(payload.get("valeur_nominale_part") or ""),
        valeur_nominale_part_lettres=number_words_from_value(
            payload.get("valeur_nominale_part")
        )
        or str(payload.get("valeur_nominale_part") or ""),
        plage_parts_totale=f"1 a {nb_parts}" if nb_parts else None,
        duree_societe=str(payload.get("duree_societe") or "99"),
        capital_depot=StatutsCivilsCapitalDepot(
            banque_nom=str(payload.get("banque_nom") or ""),
            banque_adresse=str(payload.get("banque_adresse") or ""),
        ),
        associes=associes,
        date_cloture_premier_exercice=str(payload.get("date_cloture_premier_exercice") or ""),
        nombre_exemplaires_lettres="trois",
        denomination_cabinet_mandataire="DAAT",
    )

    if structure == "SCS":
        statuts_civils.total_apports_commandites = _sum_apports(
            associes, role="commandite"
        )
    if structure == "SCI IRIS":
        _apply_iris_result_groups(statuts_civils, associes)

    return DocumentGenerationContext(
        structure=structure,
        personne_signataire=signataire,
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
        ),
        societe=Company(
            denomination=str(payload.get("denomination") or ""),
            denomination_courte=str(payload.get("denomination") or ""),
            forme_sociale=str(payload.get("forme_sociale") or structure),
            siege=siege,
            ville_rcs=str(payload.get("ville_rcs") or ""),
        ),
        statuts_civils=statuts_civils,
        metadata={"front_slice": f"track_b_{statuts_type}_v1"},
    )


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_civil_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(
        ctx,
        output_dir,
        plan.document_codes,
    )
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


# --- helpers internes ---------------------------------------------------------


def _siege_display(payload: dict[str, object]) -> str:
    return (
        f"{payload.get('siege_num', '')} {payload.get('siege_voie', '')}, "
        f"{payload.get('siege_cp', '')} {payload.get('siege_ville', '')}"
    ).strip(" ,")


def _first_physique_or_default(associes: list[StatutsCivilsAssocie]) -> Person:
    for associe in associes:
        if associe.type_personne == "personne_physique" and (associe.nom or "").strip():
            return Person(
                genre=associe.genre or Gender.MASCULIN,
                civilite=associe.civilite_affichage or "Monsieur",
                prenom=associe.prenom or "",
                nom=associe.nom or "",
            )
    # Personne morale uniquement : on derive le signataire de son representant.
    for associe in associes:
        if associe.representant is not None:
            rep = associe.representant
            return Person(
                genre=Gender.MASCULIN,
                civilite=rep.civilite_affichage or "Monsieur",
                prenom=rep.prenom or "",
                nom=rep.nom or "",
            )
    return Person(genre=Gender.MASCULIN, civilite="Monsieur", prenom="", nom="")


def _safe_int(value: object) -> int:
    try:
        cleaned = str(value).replace(" ", "").replace(" ", "").replace(",", ".")
        return int(float(cleaned))
    except (TypeError, ValueError):
        return 0


def _sum_apports(associes: list[StatutsCivilsAssocie], *, role: str) -> str:
    total = 0
    for associe in associes:
        if associe.role_statutaire == role and associe.apport and associe.apport.montant:
            total += _safe_int(associe.apport.montant)
    return str(total) if total else ""


def _apply_iris_result_groups(
    statuts_civils: StatutsCivilsContext,
    associes: list[StatutsCivilsAssocie],
) -> None:
    """SCI IRIS exige des groupes de resultat exceptionnel par plage de parts."""

    total_parts = sum((a.parts.nb or 0) for a in associes if a.parts) or 0
    groupes: list[StatutsCivilsGroupeParts] = []
    if total_parts:
        for associe in associes:
            if associe.parts and associe.parts.nb:
                quote = round(100 * (associe.parts.nb or 0) / total_parts)
                groupes.append(
                    StatutsCivilsGroupeParts(
                        parts_debut=associe.parts.debut,
                        parts_fin=associe.parts.fin,
                        quote_part_resultat_exceptionnel=f"{quote} %",
                    )
                )
    statuts_civils.resultat_groupes_parts = groupes
    statuts_civils.resultat_quote_part_exceptionnel_total = "100 %"


def _text(container, prefix: str, field: str, label: str) -> str:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _int(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date_input(prefix: str, field: str, label: str) -> date | None:
    key = f"{prefix}_{field}"
    current = st.session_state.get(key)
    if isinstance(current, date):
        st.session_state[key] = format_french_date(current)
    elif current is None:
        st.session_state[key] = format_french_date(date.today())
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
