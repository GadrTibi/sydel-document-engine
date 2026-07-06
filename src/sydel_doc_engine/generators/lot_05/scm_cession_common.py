# ruff: noqa: E501
from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import (
    Address,
    DocumentGenerationContext,
    ScmCessionAssocie,
    ScmCessionCedant,
    ScmCessionContext,
    ScmCessionCreditVendeur,
    ScmCessionEnregistrement,
    ScmCessionPrix,
    ScmCessionSignataire,
    ScmCessionSociete,
)
from sydel_doc_engine.rendering.docx_builder import add_paragraph

DOCUMENT_CODE = "FINAL-SCM-CESSION-WAVE-001"
SUPPORTED_STRUCTURES = {"SELARL": "selarl", "SELAS": "selas"}


def validate_scm_cession_enabled(ctx: DocumentGenerationContext) -> ScmCessionContext:
    if ctx.structure not in SUPPORTED_STRUCTURES:
        raise ValueError(f"dossier.structure doit etre SELARL ou SELAS pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None or not ctx.dossier_options.scm_cession:
        raise ValueError(f"dossier.options.scm_cession doit etre vrai pour {DOCUMENT_CODE}.")
    if ctx.scm_cession is None:
        raise ValueError(f"scm_cession est obligatoire pour {DOCUMENT_CODE}.")
    expected = SUPPORTED_STRUCTURES[ctx.structure]
    if ctx.scm_cession.variante_structure is not None:
        actual = ctx.scm_cession.variante_structure.strip().lower()
        if actual != expected:
            raise ValueError(
                "scm_cession.variante_structure doit correspondre a dossier.structure "
                f"pour {DOCUMENT_CODE}."
            )
    return ctx.scm_cession


def validate_pv_context(ctx: DocumentGenerationContext) -> ScmCessionContext:
    scm_cession = validate_scm_cession_enabled(ctx)
    scm_cedee = required_scm_cedee(scm_cession)
    required_cessionnaire(scm_cession)
    required_agrement(scm_cession, ctx.structure)
    required_associes(
        scm_cession.associes_presents,
        "scm_cession.associes_presents",
        expected_count=None,
        expected_total=scm_cedee.nb_parts_total,
        require_plage=False,
    )
    required_associes(
        scm_cession.associes_apres_cession,
        "scm_cession.associes_apres_cession",
        expected_count=None,
        expected_total=scm_cedee.nb_parts_total,
        require_plage=True,
    )
    if not scm_cession.signataires_pv:
        raise ValueError(f"scm_cession.signataires_pv est obligatoire pour {DOCUMENT_CODE}.")
    return scm_cession


def validate_courrier_sde_context(ctx: DocumentGenerationContext) -> ScmCessionContext:
    scm_cession = validate_scm_cession_enabled(ctx)
    # §8.2 — le nom de la SCM est desormais imprime dans le corps : on l'exige.
    scm_cedee = required_scm_cedee(scm_cession)
    required_text(scm_cedee.denomination, "scm_cession.scm_cedee.denomination")
    # enregistrement reste un porteur de contexte, mais le bloc destinataire est
    # rendu en champs « a completer » (§8.1) : ses sous-champs ne sont plus
    # obligatoires. Le montant des droits est FIXE « 25 » (§8.3) et le signataire
    # est FIXE « Clémence ROUSSEL » (§8.4a) : ni l'un ni l'autre n'est plus exige.
    required_enregistrement(scm_cession)
    required_text(ctx.signature.lieu, "signature.lieu")
    format_display_date(ctx.signature.date, "signature.date")
    return scm_cession


def validate_acte_context(ctx: DocumentGenerationContext) -> ScmCessionContext:
    scm_cession = validate_scm_cession_enabled(ctx)
    scm_cedee = required_scm_cedee(scm_cession)
    cessionnaire = required_cessionnaire(scm_cession)
    cedant = required_cedant(scm_cession)
    required_associes(
        scm_cession.associes_avant_cession,
        "scm_cession.associes_avant_cession",
        expected_count=None,
        expected_total=scm_cedee.nb_parts_total,
        require_plage=False,
    )
    required_parts_cedees(scm_cession)
    required_prix(scm_cession)
    validate_credit_vendeur(scm_cession.credit_vendeur, ctx.structure)
    required_text(scm_cession.nombre_exemplaires_lettres, "scm_cession.nombre_exemplaires_lettres")
    required_text(ctx.signature.lieu, "signature.lieu")
    if ctx.structure == "SELAS":
        required_text(
            cedant.profession_reglementee_pluriel,
            "scm_cession.cedant.profession_reglementee_pluriel",
        )
        required_text(
            scm_cedee.forme_juridique,
            "scm_cession.scm_cedee.forme_juridique",
        )
        required_text(
            cessionnaire.forme_juridique,
            "scm_cession.cessionnaire.forme_juridique",
        )
        required_text(
            cessionnaire.representant.fonction if cessionnaire.representant else None,
            "scm_cession.cessionnaire.representant.fonction",
        )
        required_text(
            scm_cession.prestataire_signature_electronique
            or ctx.signature.prestataire_signature_electronique,
            "scm_cession.prestataire_signature_electronique",
        )
    if not scm_cession.representant_cessionnaire_confirme:
        raise ValueError(
            "scm_cession.representant_cessionnaire_confirme doit etre vrai "
            f"pour {DOCUMENT_CODE}."
        )
    _validate_representant_matches_cedant(cedant, cessionnaire)
    return scm_cession


def _is_capital_divisible(capital: object, nb_parts: object) -> bool:
    """True si le capital est divisible EXACTEMENT par le nombre de parts.

    Plancher universel O24-05 (re-Akainu tour 3, MAJEUR) : la valeur nominale de la SCM
    cedee est auto-calculee (capital / nb parts) ; un capital non divisible produirait une
    valeur fractionnaire a precision infinie imprimee telle quelle dans le DOCX. On reprend
    la logique de front_app.is_capital_divisible SANS dependance front (layering : un
    generateur n'importe pas l'UI). Donnees incompletes/non numeriques -> True (la garde de
    PRESENCE requise s'en charge ailleurs ; on ne double-signale pas)."""

    def _dec(value: object) -> Decimal | None:
        if value is None:
            return None
        cleaned = str(value).replace(" ", " ").replace(" ", "").replace(",", ".")
        cleaned = re.sub(r"[^0-9.-]", "", cleaned)
        if not cleaned:
            return None
        try:
            return Decimal(cleaned)
        except InvalidOperation:
            return None

    cap = _dec(capital)
    parts = _dec(nb_parts)
    if cap is None or parts is None or parts == 0:
        return True
    quotient = cap / parts
    return quotient == quotient.to_integral_value()


def required_scm_cedee(scm_cession: ScmCessionContext) -> ScmCessionSociete:
    if scm_cession.scm_cedee is None:
        raise ValueError(f"scm_cession.scm_cedee est obligatoire pour {DOCUMENT_CODE}.")
    societe = scm_cession.scm_cedee
    required_text(societe.denomination, "scm_cession.scm_cedee.denomination")
    required_text(societe.capital_social, "scm_cession.scm_cedee.capital_social")
    address_display(societe.siege, "scm_cession.scm_cedee.siege")
    required_text(societe.ville_rcs, "scm_cession.scm_cedee.ville_rcs")
    required_text(societe.numero_rcs, "scm_cession.scm_cedee.numero_rcs")
    required_int(societe.nb_parts_total, "scm_cession.scm_cedee.nb_parts_total")
    required_text(
        societe.valeur_nominale_part,
        "scm_cession.scm_cedee.valeur_nominale_part",
    )
    # N1 (Rafael/Vincent 2026-06-24) : garde de divisibilite RETIREE — la valeur nominale PEUT
    # etre decimale (regle ratifiee, valable partout dans le generateur). L'arrondi au centime
    # (calculate_nominal_value) evite la decimale infinie ; plus aucun blocage ici.
    required_text(societe.plage_parts_total, "scm_cession.scm_cedee.plage_parts_total")
    return societe


def required_cessionnaire(scm_cession: ScmCessionContext) -> ScmCessionSociete:
    if scm_cession.cessionnaire is None:
        raise ValueError(f"scm_cession.cessionnaire est obligatoire pour {DOCUMENT_CODE}.")
    societe = scm_cession.cessionnaire
    required_text(societe.denomination, "scm_cession.cessionnaire.denomination")
    required_text(societe.capital_social, "scm_cession.cessionnaire.capital_social")
    address_display(societe.siege, "scm_cession.cessionnaire.siege")
    required_text(societe.ville_rcs, "scm_cession.cessionnaire.ville_rcs")
    if societe.representant is None:
        raise ValueError(
            f"scm_cession.cessionnaire.representant est obligatoire pour {DOCUMENT_CODE}."
        )
    required_text(
        societe.representant.civilite_affichage,
        "scm_cession.cessionnaire.representant.civilite_affichage",
    )
    required_text(
        societe.representant.civilite_courte,
        "scm_cession.cessionnaire.representant.civilite_courte",
    )
    required_text(societe.representant.prenom, "scm_cession.cessionnaire.representant.prenom")
    required_text(societe.representant.nom, "scm_cession.cessionnaire.representant.nom")
    return societe


def required_cedant(scm_cession: ScmCessionContext) -> ScmCessionCedant:
    if scm_cession.cedant is None:
        raise ValueError(f"scm_cession.cedant est obligatoire pour {DOCUMENT_CODE}.")
    cedant = scm_cession.cedant
    for field_name, value in {
        "civilite_affichage": cedant.civilite_affichage,
        "prenom": cedant.prenom,
        "nom": cedant.nom,
        "profession": cedant.profession,
        "ville_naissance": cedant.ville_naissance,
        "departement_naissance": cedant.departement_naissance,
        "nationalite": cedant.nationalite,
        "adresse_affichee": cedant.adresse_affichee,
        "situation_maritale": cedant.situation_maritale,
        "numero_rpps": cedant.numero_rpps,
    }.items():
        required_text(value, f"scm_cession.cedant.{field_name}")
    format_display_date(cedant.date_naissance, "scm_cession.cedant.date_naissance")
    if cedant.ordre is None:
        raise ValueError(f"scm_cession.cedant.ordre est obligatoire pour {DOCUMENT_CODE}.")
    required_text(cedant.ordre.departemental, "scm_cession.cedant.ordre.departemental")
    required_text(cedant.ordre.numero, "scm_cession.cedant.ordre.numero")
    if cedant.conjoint is None:
        raise ValueError(f"scm_cession.cedant.conjoint est obligatoire pour {DOCUMENT_CODE}.")
    required_text(
        cedant.conjoint.civilite_affichage,
        "scm_cession.cedant.conjoint.civilite_affichage",
    )
    required_text(cedant.conjoint.prenom, "scm_cession.cedant.conjoint.prenom")
    required_text(cedant.conjoint.nom, "scm_cession.cedant.conjoint.nom")
    return cedant


def required_agrement(
    scm_cession: ScmCessionContext,
    structure: str | None,
):
    if scm_cession.agrement is None:
        raise ValueError(f"scm_cession.agrement est obligatoire pour {DOCUMENT_CODE}.")
    agrement = scm_cession.agrement
    format_display_date(agrement.date_pv, "scm_cession.agrement.date_pv")
    required_text(agrement.date_pv_lettres, "scm_cession.agrement.date_pv_lettres")
    if structure == "SELAS":
        required_text(agrement.delai_mois, "scm_cession.agrement.delai_mois")
        required_text(agrement.date_limite, "scm_cession.agrement.date_limite")
    return agrement


def required_parts_cedees(scm_cession: ScmCessionContext):
    if scm_cession.parts_cedees is None:
        raise ValueError(f"scm_cession.parts_cedees est obligatoire pour {DOCUMENT_CODE}.")
    required_int(scm_cession.parts_cedees.nb, "scm_cession.parts_cedees.nb")
    required_text(scm_cession.parts_cedees.plage, "scm_cession.parts_cedees.plage")
    return scm_cession.parts_cedees


def required_prix(scm_cession: ScmCessionContext) -> ScmCessionPrix:
    if scm_cession.prix is None:
        raise ValueError(f"scm_cession.prix est obligatoire pour {DOCUMENT_CODE}.")
    prix = scm_cession.prix
    required_text(prix.unitaire, "scm_cession.prix.unitaire")
    required_text(prix.unitaire_lettres, "scm_cession.prix.unitaire_lettres")
    required_text(prix.global_, "scm_cession.prix.global")
    required_text(prix.global_lettres, "scm_cession.prix.global_lettres")
    return prix


def required_enregistrement(scm_cession: ScmCessionContext) -> ScmCessionEnregistrement:
    if scm_cession.enregistrement is None:
        raise ValueError(f"scm_cession.enregistrement est obligatoire pour {DOCUMENT_CODE}.")
    return scm_cession.enregistrement


def required_signataire_sde(scm_cession: ScmCessionContext) -> ScmCessionSignataire:
    if scm_cession.signataire_sde is None:
        raise ValueError(f"scm_cession.signataire_sde est obligatoire pour {DOCUMENT_CODE}.")
    return scm_cession.signataire_sde


def required_associes(
    associes: list[ScmCessionAssocie],
    field_name: str,
    *,
    expected_count: int | None,
    expected_total: int | None,
    require_plage: bool,
) -> list[ScmCessionAssocie]:
    # §4.1 : le nombre d'associes n'est plus fige (3 presents / 4 apres-cession).
    # `expected_count=None` accepte un roster de taille N coherente (au moins 1) ;
    # la coherence reelle est portee par `expected_total` (somme des parts ==
    # nb_parts_total de la SCM) et par la derivation deterministe de l'apres-cession.
    if not associes:
        raise ValueError(
            f"{field_name} doit contenir au moins un associe pour {DOCUMENT_CODE}."
        )
    if expected_count is not None and len(associes) != expected_count:
        raise ValueError(
            f"{field_name} doit contenir exactement {expected_count} associes "
            f"pour {DOCUMENT_CODE}."
        )
    total = 0
    for index, associe in enumerate(associes):
        prefix = f"{field_name}[{index}]"
        associe_display(associe, prefix)
        if associe.parts is None:
            raise ValueError(f"{prefix}.parts est obligatoire pour {DOCUMENT_CODE}.")
        total += required_int(associe.parts.nb, f"{prefix}.parts.nb")
        if require_plage:
            required_text(associe.parts.plage, f"{prefix}.parts.plage")
    if expected_total is not None and total != expected_total:
        raise ValueError(f"{field_name} doit totaliser scm_cedee.nb_parts_total.")
    return associes


def validate_credit_vendeur(
    credit_vendeur: ScmCessionCreditVendeur | None,
    structure: str | None,
) -> None:
    if credit_vendeur is None or not credit_vendeur.actif:
        return
    required_text(credit_vendeur.montant, "scm_cession.credit_vendeur.montant")
    required_text(credit_vendeur.duree, "scm_cession.credit_vendeur.duree")
    required_text(credit_vendeur.taux, "scm_cession.credit_vendeur.taux")
    if structure == "SELAS":
        required_text(
            credit_vendeur.majoration_interet_retard,
            "scm_cession.credit_vendeur.majoration_interet_retard",
        )


def associe_display(associe: ScmCessionAssocie, field_name: str) -> str:
    if associe.type_personne == "personne_morale":
        return required_text(associe.denomination, f"{field_name}.denomination")
    return (
        f"{required_text(associe.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{required_text(associe.nom, f'{field_name}.nom')}"
    )


def associe_signature(associe: ScmCessionAssocie, field_name: str) -> str:
    if associe.type_personne == "personne_morale":
        return required_text(associe.denomination, f"{field_name}.denomination")
    return (
        f"{required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{required_text(associe.nom, f'{field_name}.nom')}"
    )


def person_signature(civilite: str | None, prenom: str | None, nom: str | None, prefix: str) -> str:
    return (
        f"{required_text(civilite, f'{prefix}.civilite')} "
        f"{required_text(prenom, f'{prefix}.prenom')} "
        f"{required_text(nom, f'{prefix}.nom')}"
    )


def address_display(address: Address | None, field_name: str) -> str:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{required_text(address.num_voie, f'{field_name}.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.voie')}, "
        f"{required_text(address.cp, f'{field_name}.cp')} "
        f"{required_text(address.ville, f'{field_name}.ville')}"
    )


def format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    text = required_text(value, field_name)
    # Albane 2026-06-26 §S9 : une date saisie en TEXTE numerique « 1/1/1980 » ressortait avec
    # le jour/mois sur 1 chiffre (« 1 »). On zero-pad le jour ET le mois a 2 chiffres pour un
    # libelle JJ/MM/AAAA. Les libelles en lettres (« 1er janvier 1980 ») ne matchent pas et
    # restent INCHANGES (echo fidele du modele).
    match = re.fullmatch(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*", text)
    if match is not None:
        jour, mois, annee = match.groups()
        return f"{int(jour):02d}/{int(mois):02d}/{annee}"
    return text


def required_text(value: str | None, field_name: str) -> str:
    # R10 (Rafael 2026-06-24) : donnee manquante -> marqueur « (A COMPLETER : data) » sans crochets
    # (compatible garde-fou anti-placeholder) au lieu de lever.
    if value is None or not str(value).strip():
        return f"(À COMPLÉTER : {field_name})"
    return str(value).strip()


def required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return int(value)


def cessionnaire_forme(ctx: DocumentGenerationContext, cessionnaire: ScmCessionSociete) -> str:
    if ctx.structure == "SELARL":
        return "SELARL"
    return required_text(cessionnaire.forme_juridique, "scm_cession.cessionnaire.forme_juridique")


def cessionnaire_representant_fonction(
    ctx: DocumentGenerationContext,
    cessionnaire: ScmCessionSociete,
) -> str:
    if ctx.structure == "SELARL":
        return "gérant"
    return required_text(
        cessionnaire.representant.fonction if cessionnaire.representant else None,
        "scm_cession.cessionnaire.representant.fonction",
    )


def acte_signature_prestataire(ctx: DocumentGenerationContext, scm_cession: ScmCessionContext) -> str:
    if ctx.structure == "SELARL":
        return "Yousign"
    return required_text(
        scm_cession.prestataire_signature_electronique
        or ctx.signature.prestataire_signature_electronique,
        "scm_cession.prestataire_signature_electronique",
    )


def scm_cedee_forme(ctx: DocumentGenerationContext, scm_cedee: ScmCessionSociete) -> str:
    if ctx.structure == "SELARL":
        return "Société Civile de Moyens"
    return required_text(scm_cedee.forme_juridique, "scm_cession.scm_cedee.forme_juridique")


def scm_cedee_address_for_acte(
    ctx: DocumentGenerationContext,
    scm_cedee: ScmCessionSociete,
    cessionnaire: ScmCessionSociete,
) -> str:
    if ctx.structure == "SELARL":
        return address_display(cessionnaire.siege, "scm_cession.cessionnaire.siege")
    return address_display(scm_cedee.siege, "scm_cession.scm_cedee.siege")


def cedant_display(cedant: ScmCessionCedant) -> str:
    # Albane 2026-06-26 §S8 : la civilite du cedant (soussigne 1) doit commencer par une
    # MAJUSCULE (« Monsieur », pas « monsieur »). On ne capitalise que l'initiale (jamais
    # « MONSIEUR ».casefold() -> « Monsieur ») : une civilite deja correcte est inchangee.
    civilite = required_text(
        cedant.civilite_affichage, "scm_cession.cedant.civilite_affichage"
    )
    civilite = civilite[:1].upper() + civilite[1:]
    return (
        f"{civilite} "
        f"{required_text(cedant.prenom, 'scm_cession.cedant.prenom')} "
        f"{required_text(cedant.nom, 'scm_cession.cedant.nom')}"
    )


def _normalize_situation(situation_maritale: str | None) -> str:
    """Normalise un libelle de situation maritale (NFKD, sans accent, minuscule, trim).

    Robuste au format d'entree : accentue+accorde (« Pacsé »/« pacsée ») OU brut
    (« pacse »/« pacsee »), avec ou sans majuscule. Les generateurs recoivent selon le
    type l'un ou l'autre (situation_display cote slices vs valeur brute) — cette
    normalisation unique garantit un test identique partout."""
    if not situation_maritale:
        return ""
    nfkd = unicodedata.normalize("NFKD", situation_maritale)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).strip().lower()


def mentions_conjoint(situation_maritale: str | None) -> bool:
    """Le conjoint n'est mentionne QUE pour une personne mariee.

    R22-02 (Rafael 2026-06-22) : ne pas afficher de conjoint fantome quand le client
    n'est pas marie (« divorce avec Madame X » alors qu'aucune epouse n'existe). On
    s'aligne sur la garde du gold (statuts SEL) : conjoint affiche seulement si « marie(e) ».
    Helper PARTAGE par les actes de cession (SCM + SPFPL) pour que la regle soit unique.
    """
    norm = _normalize_situation(situation_maritale)
    return norm in {"marie", "mariee"} or norm.startswith(("marie ", "mariee "))


def mentions_partenaire_pacse(situation_maritale: str | None) -> bool:
    """Le partenaire n'est mentionne QUE pour une personne PACSEE.

    Albane 6.3/7.3 (RATIFIE 2026-07-06) : « Nom du conjoint/partenaire (marie OU pacse) :
    ajouter champs nom + prenom ; repris dans les docs ». Symetrique de `mentions_conjoint`
    (marie) : garde PARTAGEE unique pour le cas pacse, afin que la regle soit codifiee a un
    seul endroit. NB : le PACS a bien un regime patrimonial (separation des patrimoines par
    defaut / indivision) MAIS le menu « Pacsé(e) » ne capture pas de sous-regime -> la clause
    de comparution d'un pacse = « pacse(e) avec {partenaire} », PAS « sous le regime de … ».
    """
    norm = _normalize_situation(situation_maritale)
    return norm in {"pacse", "pacsee"} or norm.startswith(("pacse ", "pacsee "))


def mentions_conjoint_ou_partenaire(situation_maritale: str | None) -> bool:
    """True si la comparution doit afficher le conjoint (marie) OU le partenaire (pacse)."""
    return mentions_conjoint(situation_maritale) or mentions_partenaire_pacse(
        situation_maritale
    )


def partenaire_pacse_clause(
    conjoint: Any | None,
    *,
    prefix: str = " avec ",
) -> str:
    """Fragment « avec {Civilite Prenom Nom} » du partenaire pacse, ou "" si non renseigne.

    Albane 6.3 (RATIFIE) : « pas de mention PACS/mariage sans nom ». Contrairement au marie
    (dont le conjoint est requis par le front), le partenaire pacse est OPTIONNEL (« si
    renseigne »). On n'affiche donc « avec … » QUE si un nom OU un prenom existe ; sinon on
    renvoie "" (le pacse reste « pacse(e) » nu, jamais « avec (À COMPLÉTER) »). Le fragment
    inclut la civilite si presente, comme les autres comparutions (« Madame Prenom Nom »)."""
    if conjoint is None:
        return ""
    prenom = (getattr(conjoint, "prenom", None) or "").strip()
    nom = (getattr(conjoint, "nom", None) or "").strip()
    if not prenom and not nom:
        return ""
    civilite = (getattr(conjoint, "civilite_affichage", None) or "").strip()
    parts = [p for p in (civilite, prenom, nom) if p]
    return f"{prefix}{' '.join(parts)}"


def conjoint_display(cedant: ScmCessionCedant) -> str:
    if cedant.conjoint is None:
        raise ValueError(f"scm_cession.cedant.conjoint est obligatoire pour {DOCUMENT_CODE}.")
    return (
        f"{required_text(cedant.conjoint.civilite_affichage, 'scm_cession.cedant.conjoint.civilite_affichage')} "
        f"{required_text(cedant.conjoint.prenom, 'scm_cession.cedant.conjoint.prenom')} "
        f"{required_text(cedant.conjoint.nom, 'scm_cession.cedant.conjoint.nom')}"
    )


def add_body_paragraph(
    document: Any,
    text: str,
    *,
    bold: bool = False,
    italic: bool = False,
    space_after_pt: int | None = None,
) -> None:
    # italic optionnel (defaut False) : preserve le comportement des appelants
    # existants. Le PV SCM (DOC-031) l'active pour la mention d'adoption des
    # resolutions « Cette resolution est adoptee a l'unanimite » (§4.2).
    # space_after_pt optionnel (defaut None -> standard_space_after_pt, rendu inchange
    # pour tous les appelants existants). Albane 2026-06-26 §P2 : le PV SCM le surcharge
    # pour aerer entre paragraphes (« mettre de l'espace entre les paragraphes »). N'affecte
    # que les appelants qui le passent explicitement.
    add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        bold=bold,
        italic=italic,
        space_after_pt=space_after_pt,
    )


def add_heading(
    document: Any,
    text: str,
    *,
    space_before_pt: int = 0,
    space_after_pt: int | None = None,
) -> None:
    # space_before_pt optionnel (defaut 0) : preserve le comportement actuel
    # pour les appelants existants (PV, courrier). L'acte de cession SCM
    # l'utilise pour aerer avant chaque grande section (mise en forme §13.1).
    # space_after_pt optionnel (defaut None -> standard_space_after_pt, rendu
    # inchange pour PV/courrier). Albane 2026-06-26 §S10 : l'acte le surcharge
    # pour aerer APRES chaque titre de section.
    add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
        space_before_pt=space_before_pt,
        space_after_pt=space_after_pt,
    )


def save_clean_document(document: Any, output_dir: Path, output_filename: str) -> Path:
    full_text = "\n".join(
        [paragraph.text for paragraph in document.paragraphs]
        + [
            cell.text
            for table in document.tables
            for row in table.rows
            for cell in row.cells
        ]
    )
    if "[" in full_text or "]" in full_text:
        raise ValueError(f"placeholder source residuel dans le rendu {DOCUMENT_CODE}.")
    if "Ajouter en cas de CV" in full_text:
        raise ValueError(f"instruction credit-vendeur residuelle dans le rendu {DOCUMENT_CODE}.")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename
    document.save(output_path)
    return output_path


def _validate_representant_matches_cedant(
    cedant: ScmCessionCedant,
    cessionnaire: ScmCessionSociete,
) -> None:
    representant = cessionnaire.representant
    if representant is None:
        raise ValueError(
            f"scm_cession.cessionnaire.representant est obligatoire pour {DOCUMENT_CODE}."
        )
    if (
        required_text(representant.prenom, "scm_cession.cessionnaire.representant.prenom")
        != required_text(cedant.prenom, "scm_cession.cedant.prenom")
        or required_text(representant.nom, "scm_cession.cessionnaire.representant.nom")
        != required_text(cedant.nom, "scm_cession.cedant.nom")
    ):
        raise ValueError(
            "le representant de la SEL cessionnaire doit correspondre au cedant "
            f"pour le wording source V1 {DOCUMENT_CODE}."
        )
