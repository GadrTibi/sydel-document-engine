from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date
from typing import Final

from pydantic import ValidationError

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Associe,
    BienImmobilier,
    CapitalContext,
    Company,
    DecisionContext,
    DirigeantNomine,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    Emprunt,
    Person,
    ReunionContext,
    Signature,
)
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import ALL_STRUCTURES, build_seed_catalog

BUSINESS_WIZARD_SUPPORTED_DOCUMENT_IDS: Final[tuple[str, ...]] = (
    "DOC-001",
    "DOC-002",
    "DOC-003",
    "DOC-004",
)
BUSINESS_WIZARD_GENERABLE_STRUCTURES: Final[tuple[str, ...]] = ("SCI",)
PV_NOMINATION_STRUCTURES: Final[frozenset[str]] = frozenset(
    {"SELARL", "SELAS", "SPFPL cession", "SPFPL apport", "SCS", "SCI", "SCM"}
)


@dataclass(frozen=True)
class BusinessDossierType:
    structure: str
    label: str
    status: str
    generable_in_v1: bool


@dataclass(frozen=True)
class BusinessAssociateInput:
    genre: str = Gender.MASCULIN.value
    civilite_affichage: str = ""
    prenom: str = ""
    nom: str = ""
    nb_parts: int | None = None
    est_present_ou_represente: bool = True


@dataclass(frozen=True)
class BusinessWizardInput:
    structure: str = "SCI"
    personne_genre: str = Gender.MASCULIN.value
    personne_civilite: str = ""
    personne_prenom: str = ""
    personne_nom: str = ""
    personne_date_naissance: date | str | None = None
    personne_nationalite: str = ""
    personne_nom_pere: str = ""
    personne_nom_mere: str = ""
    personne_fonction_dirigeant: str = ""
    personne_adresse_num_voie: str = ""
    personne_adresse_voie: str = ""
    personne_adresse_cp: str = ""
    personne_adresse_ville: str = ""
    societe_forme_sociale: str = ""
    societe_forme_sociale_affichage: str = ""
    societe_forme_sociale_libelle_long: str = ""
    societe_denomination: str = ""
    societe_capital_social: str = ""
    societe_capital_variable: bool = True
    societe_siege_num_voie: str = ""
    societe_siege_voie: str = ""
    societe_siege_cp: str = ""
    societe_siege_ville: str = ""
    societe_ville_rcs: str = ""
    domiciliation_adresse_affichee: str = ""
    associes: tuple[BusinessAssociateInput, ...] = field(default_factory=tuple)
    dirigeant_genre: str = Gender.MASCULIN.value
    dirigeant_civilite_affichage: str = ""
    dirigeant_prenom: str = ""
    dirigeant_nom: str = ""
    dirigeant_date_naissance: date | str | None = None
    dirigeant_ville_naissance: str = ""
    dirigeant_departement_naissance: str = ""
    dirigeant_nationalite: str = ""
    dirigeant_fonction_affichage: str = "gerant"
    dirigeant_adresse_num_voie: str = ""
    dirigeant_adresse_voie: str = ""
    dirigeant_adresse_cp: str = ""
    dirigeant_adresse_ville: str = ""
    capital_nb_parts_total: int | None = None
    capital_valeur_nominale_part: str = ""
    decision_date: date | str | None = None
    reunion_date_lettres: str = ""
    reunion_heure: str = ""
    signature_lieu: str = ""
    signature_date: date | str | None = None
    signature_nombre_exemplaires: str = ""
    emprunt_actif: bool = False
    emprunt_montant_max: str = ""
    bien_adresse_num_voie: str = ""
    bien_adresse_voie: str = ""
    bien_adresse_cp: str = ""
    bien_adresse_ville: str = ""


@dataclass(frozen=True)
class BusinessDocumentRow:
    doc_id: str
    name: str
    status: str
    missing_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class BusinessWizardValidation:
    context: DocumentGenerationContext | None
    document_rows: tuple[BusinessDocumentRow, ...]
    missing_fields: tuple[str, ...]
    inconsistencies: tuple[str, ...]
    warnings: tuple[str, ...]
    can_generate_docx: bool

    @property
    def generable_count(self) -> int:
        return sum(1 for row in self.document_rows if row.status == "generable")

    @property
    def blocked_count(self) -> int:
        return sum(1 for row in self.document_rows if row.status != "generable")


def business_dossier_types() -> tuple[BusinessDossierType, ...]:
    return tuple(
        BusinessDossierType(
            structure=structure,
            label=_structure_label(structure),
            status=_structure_status(structure),
            generable_in_v1=structure in BUSINESS_WIZARD_GENERABLE_STRUCTURES,
        )
        for structure in ALL_STRUCTURES
    )


def sample_business_wizard_input() -> BusinessWizardInput:
    return BusinessWizardInput(
        structure="SCI",
        personne_genre=Gender.MASCULIN.value,
        personne_civilite="Monsieur",
        personne_prenom="Jean",
        personne_nom="Durand",
        personne_date_naissance=date(1990, 2, 3),
        personne_nationalite="francaise",
        personne_nom_pere="Pierre Durand",
        personne_nom_mere="Anne Martin",
        personne_fonction_dirigeant="Gerant",
        personne_adresse_num_voie="12",
        personne_adresse_voie="rue des Lilas",
        personne_adresse_cp="75008",
        personne_adresse_ville="Paris",
        societe_forme_sociale="SCI",
        societe_forme_sociale_affichage="Societe civile immobiliere",
        societe_forme_sociale_libelle_long="societe civile immobiliere",
        societe_denomination="SCI ORCH POSITIVE",
        societe_capital_social="1 000",
        societe_capital_variable=True,
        societe_siege_num_voie="10",
        societe_siege_voie="rue du Siege",
        societe_siege_cp="75001",
        societe_siege_ville="Paris",
        societe_ville_rcs="Paris",
        domiciliation_adresse_affichee="10 rue du Siege, 75001 Paris",
        associes=(
            BusinessAssociateInput(
                genre=Gender.FEMININ.value,
                civilite_affichage="Madame",
                prenom="Alice",
                nom="Durand",
                nb_parts=60,
            ),
            BusinessAssociateInput(
                genre=Gender.MASCULIN.value,
                civilite_affichage="Monsieur",
                prenom="Bruno",
                nom="Martin",
                nb_parts=40,
            ),
        ),
        dirigeant_genre=Gender.FEMININ.value,
        dirigeant_civilite_affichage="Madame",
        dirigeant_prenom="Claire",
        dirigeant_nom="Bernard",
        dirigeant_date_naissance=date(1985, 4, 3),
        dirigeant_ville_naissance="Lyon",
        dirigeant_departement_naissance="Rhone",
        dirigeant_nationalite="francaise",
        dirigeant_fonction_affichage="gerant",
        dirigeant_adresse_num_voie="22",
        dirigeant_adresse_voie="avenue des Fleurs",
        dirigeant_adresse_cp="69002",
        dirigeant_adresse_ville="Lyon",
        capital_nb_parts_total=100,
        capital_valeur_nominale_part="10",
        decision_date=date(2026, 5, 13),
        reunion_date_lettres="treize mai deux mille vingt-six",
        reunion_heure="10 heures",
        signature_lieu="Paris",
        signature_date=date(2026, 5, 13),
        signature_nombre_exemplaires="3",
    )


def evaluate_business_wizard(data: BusinessWizardInput) -> BusinessWizardValidation:
    missing_by_doc = _missing_fields_by_document(data)
    missing_fields = _unique(
        field_name
        for doc_id in _target_document_ids(data.structure)
        for field_name in missing_by_doc.get(doc_id, ())
    )
    inconsistencies = _validate_inconsistencies(data)
    warnings = _business_warnings(data)
    context = None

    if not missing_fields and not inconsistencies:
        try:
            context = build_business_context(data)
        except (ValueError, ValidationError) as exc:
            inconsistencies = (*inconsistencies, f"contexte moteur invalide: {exc}")

    document_rows = _document_rows(data, missing_by_doc, inconsistencies, context)
    can_generate = (
        context is not None
        and data.structure in BUSINESS_WIZARD_GENERABLE_STRUCTURES
        and all(row.status == "generable" for row in document_rows)
    )
    return BusinessWizardValidation(
        context=context,
        document_rows=document_rows,
        missing_fields=missing_fields,
        inconsistencies=inconsistencies,
        warnings=warnings,
        can_generate_docx=can_generate,
    )


def build_business_context(data: BusinessWizardInput) -> DocumentGenerationContext:
    signature_date = _required_date_value(data.signature_date, "signature.date")
    personne_date_naissance = _required_date_value(
        data.personne_date_naissance,
        "personne_signataire.date_naissance",
    )
    dirigeant_date_naissance = _required_date_value(
        data.dirigeant_date_naissance,
        "dirigeant_nomine.date_naissance",
    )
    associes = tuple(_build_associe(associe) for associe in data.associes)
    represented_parts = sum(
        associe.nb_parts for associe in associes if associe.est_present_ou_represente
    )
    company = Company(
        forme_sociale=_required_text_value(data.societe_forme_sociale, "societe.forme_sociale"),
        forme_sociale_affichage=_required_text_value(
            data.societe_forme_sociale_affichage,
            "societe.forme_sociale_affichage",
        ),
        forme_sociale_libelle_long=_required_text_value(
            data.societe_forme_sociale_libelle_long,
            "societe.forme_sociale_libelle_long",
        ),
        denomination=_required_text_value(data.societe_denomination, "societe.denomination"),
        capital=_required_text_value(data.societe_capital_social, "societe.capital"),
        capital_social=_required_text_value(
            data.societe_capital_social,
            "societe.capital_social",
        ),
        capital_variable=data.societe_capital_variable,
        siege=Address(
            num_voie=_required_text_value(data.societe_siege_num_voie, "societe.siege.num_voie"),
            voie=_required_text_value(data.societe_siege_voie, "societe.siege.voie"),
            cp=_required_text_value(data.societe_siege_cp, "societe.siege.cp"),
            ville=_required_text_value(data.societe_siege_ville, "societe.siege.ville"),
        ),
        ville_rcs=_required_text_value(data.societe_ville_rcs, "societe.ville_rcs"),
    )
    context = DocumentGenerationContext(
        structure=_required_text_value(data.structure, "structure"),
        dossier_options=DossierOptions(),
        personne_signataire=Person(
            genre=_required_gender(data.personne_genre, "personne_signataire.genre"),
            civilite=_required_text_value(data.personne_civilite, "personne_signataire.civilite"),
            prenom=_required_text_value(data.personne_prenom, "personne_signataire.prenom"),
            nom=_required_text_value(data.personne_nom, "personne_signataire.nom"),
            adresse_perso=Address(
                num_voie=_required_text_value(
                    data.personne_adresse_num_voie,
                    "personne_signataire.adresse_perso.num_voie",
                ),
                voie=_required_text_value(
                    data.personne_adresse_voie,
                    "personne_signataire.adresse_perso.voie",
                ),
                cp=_required_text_value(
                    data.personne_adresse_cp,
                    "personne_signataire.adresse_perso.cp",
                ),
                ville=_required_text_value(
                    data.personne_adresse_ville,
                    "personne_signataire.adresse_perso.ville",
                ),
            ),
            date_naissance=personne_date_naissance,
            nationalite=_required_text_value(
                data.personne_nationalite,
                "personne_signataire.nationalite",
            ),
            nom_pere=_required_text_value(data.personne_nom_pere, "personne_signataire.nom_pere"),
            nom_mere=_required_text_value(data.personne_nom_mere, "personne_signataire.nom_mere"),
            fonction_dirigeant=_required_text_value(
                data.personne_fonction_dirigeant,
                "personne_signataire.fonction_dirigeant",
            ),
        ),
        signature=Signature(
            lieu=_required_text_value(data.signature_lieu, "signature.lieu"),
            date=signature_date,
            nombre_exemplaires=_required_text_value(
                data.signature_nombre_exemplaires,
                "signature.nombre_exemplaires",
            ),
        ),
        societe=company,
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=_required_text_value(
                data.domiciliation_adresse_affichee,
                "domiciliation.adresse_domiciliation_affichee",
            )
        ),
        associes=list(associes),
        dirigeant_nomine=DirigeantNomine(
            genre=_required_gender(data.dirigeant_genre, "dirigeant_nomine.genre"),
            civilite_affichage=_required_text_value(
                data.dirigeant_civilite_affichage,
                "dirigeant_nomine.civilite_affichage",
            ),
            prenom=_required_text_value(data.dirigeant_prenom, "dirigeant_nomine.prenom"),
            nom=_required_text_value(data.dirigeant_nom, "dirigeant_nomine.nom"),
            date_naissance=dirigeant_date_naissance,
            ville_naissance=_required_text_value(
                data.dirigeant_ville_naissance,
                "dirigeant_nomine.ville_naissance",
            ),
            departement_naissance=_required_text_value(
                data.dirigeant_departement_naissance,
                "dirigeant_nomine.departement_naissance",
            ),
            nationalite=_required_text_value(
                data.dirigeant_nationalite,
                "dirigeant_nomine.nationalite",
            ),
            adresse_personnelle=Address(
                num_voie=_required_text_value(
                    data.dirigeant_adresse_num_voie,
                    "dirigeant_nomine.adresse_personnelle.num_voie",
                ),
                voie=_required_text_value(
                    data.dirigeant_adresse_voie,
                    "dirigeant_nomine.adresse_personnelle.voie",
                ),
                cp=_required_text_value(
                    data.dirigeant_adresse_cp,
                    "dirigeant_nomine.adresse_personnelle.cp",
                ),
                ville=_required_text_value(
                    data.dirigeant_adresse_ville,
                    "dirigeant_nomine.adresse_personnelle.ville",
                ),
            ),
            fonction_affichage=_required_text_value(
                data.dirigeant_fonction_affichage,
                "dirigeant_nomine.fonction_affichage",
            ),
        ),
        decision=DecisionContext(date=_required_present_value(data.decision_date, "decision.date")),
        reunion=ReunionContext(
            date_lettres=_required_text_value(data.reunion_date_lettres, "reunion.date_lettres"),
            heure=_required_text_value(data.reunion_heure, "reunion.heure"),
        ),
        capital=CapitalContext(
            nb_parts_total=data.capital_nb_parts_total,
            valeur_nominale_part=_required_text_value(
                data.capital_valeur_nominale_part,
                "capital.valeur_nominale_part",
            ),
            nb_parts_representees=represented_parts,
        ),
        emprunt=Emprunt(
            actif=data.emprunt_actif,
            montant_max=_optional_text_value(data.emprunt_montant_max),
        ),
        bien_immobilier=_build_bien_immobilier(data),
    )
    return context


def business_document_table_rows(
    validation: BusinessWizardValidation,
) -> list[dict[str, str]]:
    return [
        {
            "code document": row.doc_id,
            "nom document": row.name,
            "statut": row.status,
            "champs manquants": ", ".join(row.missing_fields) if row.missing_fields else "",
        }
        for row in validation.document_rows
    ]


def _structure_label(structure: str) -> str:
    if structure == "SCI":
        return "SCI - assistant metier V1"
    return f"{structure} - diagnostic V1"


def _structure_status(structure: str) -> str:
    if structure in BUSINESS_WIZARD_GENERABLE_STRUCTURES:
        return "generation DOC-001 a DOC-004 recettable dans ce ticket"
    return "structure connue du moteur, formulaire metier complet hors V1"


def _missing_fields_by_document(data: BusinessWizardInput) -> dict[str, tuple[str, ...]]:
    missing: dict[str, list[str]] = {
        doc_id: [] for doc_id in BUSINESS_WIZARD_SUPPORTED_DOCUMENT_IDS
    }
    _validate_doc_001(data, missing["DOC-001"])
    _validate_doc_002(data, missing["DOC-002"])
    _validate_doc_003(data, missing["DOC-003"])
    if data.structure in PV_NOMINATION_STRUCTURES:
        _validate_doc_004(data, missing["DOC-004"])
    return {doc_id: tuple(fields) for doc_id, fields in missing.items()}


def _validate_doc_001(data: BusinessWizardInput, missing: list[str]) -> None:
    _require_gender(data.personne_genre, "personne_signataire.genre", missing)
    _require_text(data.personne_civilite, "personne_signataire.civilite", missing)
    _require_text(data.personne_prenom, "personne_signataire.prenom", missing)
    _require_text(data.personne_nom, "personne_signataire.nom", missing)
    _require_date(data.personne_date_naissance, "personne_signataire.date_naissance", missing)
    _require_text(data.personne_nationalite, "personne_signataire.nationalite", missing)
    _require_text(data.personne_nom_pere, "personne_signataire.nom_pere", missing)
    _require_text(data.personne_nom_mere, "personne_signataire.nom_mere", missing)
    _require_address(data, "personne", "personne_signataire.adresse_perso", missing)
    _require_text(data.signature_lieu, "signature.lieu", missing)
    _require_date(data.signature_date, "signature.date", missing)


def _validate_doc_002(data: BusinessWizardInput, missing: list[str]) -> None:
    _require_text(data.personne_civilite, "personne_signataire.civilite", missing)
    _require_text(data.personne_prenom, "personne_signataire.prenom", missing)
    _require_text(data.personne_nom, "personne_signataire.nom", missing)
    _require_text(data.societe_denomination, "societe.denomination", missing)
    _require_text(data.societe_capital_social, "societe.capital", missing)
    _require_text(
        data.domiciliation_adresse_affichee,
        "domiciliation.adresse_domiciliation_affichee",
        missing,
    )
    _require_text(data.signature_lieu, "signature.lieu", missing)
    _require_date(data.signature_date, "signature.date", missing)


def _validate_doc_003(data: BusinessWizardInput, missing: list[str]) -> None:
    _require_text(data.personne_civilite, "personne_signataire.civilite", missing)
    _require_text(data.personne_prenom, "personne_signataire.prenom", missing)
    _require_text(data.personne_nom, "personne_signataire.nom", missing)
    _require_text(
        data.personne_fonction_dirigeant,
        "personne_signataire.fonction_dirigeant",
        missing,
    )
    _require_address(data, "personne", "personne_signataire.adresse_perso", missing)
    _require_text(data.societe_forme_sociale, "societe.forme_sociale", missing)
    _require_text(data.societe_denomination, "societe.denomination", missing)
    _require_address(data, "societe", "societe.siege", missing)
    _require_text(data.signature_lieu, "signature.lieu", missing)
    _require_date(data.signature_date, "signature.date", missing)


def _validate_doc_004(data: BusinessWizardInput, missing: list[str]) -> None:
    _require_text(data.societe_denomination, "societe.denomination", missing)
    _require_text(data.societe_forme_sociale_affichage, "societe.forme_sociale_affichage", missing)
    _require_text(
        data.societe_forme_sociale_libelle_long,
        "societe.forme_sociale_libelle_long",
        missing,
    )
    _require_text(data.societe_capital_social, "societe.capital_social", missing)
    _require_address(data, "societe", "societe.siege", missing)
    _require_text(data.societe_ville_rcs, "societe.ville_rcs", missing)
    _require_positive_int(data.capital_nb_parts_total, "capital.nb_parts_total", missing)
    _require_text(data.capital_valeur_nominale_part, "capital.valeur_nominale_part", missing)
    _require_associes(data.associes, missing)
    _require_gender(data.dirigeant_genre, "dirigeant_nomine.genre", missing)
    _require_text(data.dirigeant_civilite_affichage, "dirigeant_nomine.civilite_affichage", missing)
    _require_text(data.dirigeant_prenom, "dirigeant_nomine.prenom", missing)
    _require_text(data.dirigeant_nom, "dirigeant_nomine.nom", missing)
    _require_date(data.dirigeant_date_naissance, "dirigeant_nomine.date_naissance", missing)
    _require_text(data.dirigeant_ville_naissance, "dirigeant_nomine.ville_naissance", missing)
    _require_text(
        data.dirigeant_departement_naissance,
        "dirigeant_nomine.departement_naissance",
        missing,
    )
    _require_text(data.dirigeant_nationalite, "dirigeant_nomine.nationalite", missing)
    _require_address(data, "dirigeant", "dirigeant_nomine.adresse_personnelle", missing)
    _require_text(data.dirigeant_fonction_affichage, "dirigeant_nomine.fonction_affichage", missing)
    _require_present(data.decision_date, "decision.date", missing)
    _require_text(data.reunion_date_lettres, "reunion.date_lettres", missing)
    _require_text(data.reunion_heure, "reunion.heure", missing)
    _require_text(data.signature_lieu, "signature.lieu", missing)
    _require_date(data.signature_date, "signature.date", missing)
    _require_text(data.signature_nombre_exemplaires, "signature.nombre_exemplaires", missing)
    if data.emprunt_actif:
        _require_text(data.emprunt_montant_max, "emprunt.montant_max", missing)
        _require_address(data, "bien", "bien_immobilier.adresse", missing)


def _validate_inconsistencies(data: BusinessWizardInput) -> tuple[str, ...]:
    issues: list[str] = []
    if data.structure not in ALL_STRUCTURES:
        issues.append("structure inconnue du catalogue moteur")
    if data.structure in PV_NOMINATION_STRUCTURES and not data.societe_capital_variable:
        issues.append("societe.capital_variable=false bloque DOC-004 en V1")
    if data.capital_nb_parts_total is not None and data.capital_nb_parts_total > 0:
        represented_parts = sum(
            associe.nb_parts or 0
            for associe in data.associes
            if associe.est_present_ou_represente
        )
        if data.associes and represented_parts != data.capital_nb_parts_total:
            issues.append(
                "la somme des parts des associes presents ou representes doit "
                "correspondre a capital.nb_parts_total"
            )
    return tuple(issues)


def _business_warnings(data: BusinessWizardInput) -> tuple[str, ...]:
    warnings: list[str] = [
        "La generation ne vaut pas validation juridique ni revue visuelle humaine.",
        "Les documents non collectes par le formulaire V1 restent en mode technique.",
    ]
    if data.structure not in BUSINESS_WIZARD_GENERABLE_STRUCTURES:
        warnings.append(
            "Le bouton de generation assistant est limite a la SCI simple pour cette V1."
        )
    return tuple(warnings)


def _document_rows(
    data: BusinessWizardInput,
    missing_by_doc: dict[str, tuple[str, ...]],
    inconsistencies: tuple[str, ...],
    context: DocumentGenerationContext | None,
) -> tuple[BusinessDocumentRow, ...]:
    rows: list[BusinessDocumentRow] = []
    target_ids = (
        _selected_document_ids(context)
        if context is not None
        else _target_document_ids(data.structure)
    )
    names = _catalog_names()
    for doc_id in target_ids:
        if doc_id not in BUSINESS_WIZARD_SUPPORTED_DOCUMENT_IDS:
            rows.append(
                BusinessDocumentRow(
                    doc_id=doc_id,
                    name=names.get(doc_id, doc_id),
                    status="indisponible",
                    missing_fields=("hors perimetre assistant metier V1",),
                )
            )
            continue
        missing_fields = missing_by_doc.get(doc_id, ())
        if missing_fields or inconsistencies:
            rows.append(
                BusinessDocumentRow(
                    doc_id=doc_id,
                    name=names.get(doc_id, doc_id),
                    status="incomplet",
                    missing_fields=(*missing_fields, *inconsistencies),
                )
            )
        else:
            rows.append(
                BusinessDocumentRow(
                    doc_id=doc_id,
                    name=names.get(doc_id, doc_id),
                    status="generable",
                )
            )
    return tuple(rows)


def _target_document_ids(structure: str | None) -> tuple[str, ...]:
    if not structure:
        return ()
    if structure in BUSINESS_WIZARD_GENERABLE_STRUCTURES:
        return BUSINESS_WIZARD_SUPPORTED_DOCUMENT_IDS
    catalog = build_seed_catalog()
    return tuple(document.doc_id for document in catalog if structure in document.structures)


def _selected_document_ids(ctx: DocumentGenerationContext) -> tuple[str, ...]:
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    return tuple(document.doc_id for document in orchestrator.select_documents_for_context(ctx))


def _catalog_names() -> dict[str, str]:
    return {document.doc_id: document.canonical_name for document in build_seed_catalog()}


def _build_associe(data: BusinessAssociateInput) -> Associe:
    return Associe(
        genre=_required_gender(data.genre, "associes[].genre"),
        civilite_affichage=_required_text_value(
            data.civilite_affichage,
            "associes[].civilite_affichage",
        ),
        prenom=_required_text_value(data.prenom, "associes[].prenom"),
        nom=_required_text_value(data.nom, "associes[].nom"),
        nb_parts=_required_positive_int_value(data.nb_parts, "associes[].nb_parts"),
        est_present_ou_represente=data.est_present_ou_represente,
    )


def _build_bien_immobilier(data: BusinessWizardInput) -> BienImmobilier | None:
    if not data.emprunt_actif:
        return None
    return BienImmobilier(
        adresse=Address(
            num_voie=_required_text_value(
                data.bien_adresse_num_voie,
                "bien_immobilier.adresse.num_voie",
            ),
            voie=_required_text_value(data.bien_adresse_voie, "bien_immobilier.adresse.voie"),
            cp=_required_text_value(data.bien_adresse_cp, "bien_immobilier.adresse.cp"),
            ville=_required_text_value(data.bien_adresse_ville, "bien_immobilier.adresse.ville"),
        )
    )


def _require_address(
    data: BusinessWizardInput,
    prefix: str,
    field_prefix: str,
    missing: list[str],
) -> None:
    attribute_prefixes = {
        "personne": "personne_adresse",
        "societe": "societe_siege",
        "dirigeant": "dirigeant_adresse",
        "bien": "bien_adresse",
    }
    attribute_prefix = attribute_prefixes[prefix]
    _require_text(
        getattr(data, f"{attribute_prefix}_num_voie"),
        f"{field_prefix}.num_voie",
        missing,
    )
    _require_text(getattr(data, f"{attribute_prefix}_voie"), f"{field_prefix}.voie", missing)
    _require_text(getattr(data, f"{attribute_prefix}_cp"), f"{field_prefix}.cp", missing)
    _require_text(getattr(data, f"{attribute_prefix}_ville"), f"{field_prefix}.ville", missing)


def _require_associes(associes: tuple[BusinessAssociateInput, ...], missing: list[str]) -> None:
    if not associes:
        missing.append("associes[]")
        return
    for index, associe in enumerate(associes, start=1):
        prefix = f"associes[{index}]"
        _require_gender(associe.genre, f"{prefix}.genre", missing)
        _require_text(associe.civilite_affichage, f"{prefix}.civilite_affichage", missing)
        _require_text(associe.prenom, f"{prefix}.prenom", missing)
        _require_text(associe.nom, f"{prefix}.nom", missing)
        _require_positive_int(associe.nb_parts, f"{prefix}.nb_parts", missing)


def _require_text(value: str | None, field_name: str, missing: list[str]) -> None:
    if _is_blank(value):
        missing.append(field_name)


def _require_present(value: date | str | None, field_name: str, missing: list[str]) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        missing.append(field_name)


def _require_date(value: date | str | None, field_name: str, missing: list[str]) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        missing.append(field_name)
        return
    if isinstance(value, str):
        try:
            date.fromisoformat(value)
        except ValueError:
            missing.append(f"{field_name} (format AAAA-MM-JJ)")


def _require_gender(value: str | None, field_name: str, missing: list[str]) -> None:
    if value not in {Gender.MASCULIN.value, Gender.FEMININ.value}:
        missing.append(field_name)


def _require_positive_int(value: int | None, field_name: str, missing: list[str]) -> None:
    if value is None or value < 1:
        missing.append(field_name)


def _required_text_value(value: str | None, field_name: str) -> str:
    if _is_blank(value):
        raise ValueError(f"{field_name} est obligatoire.")
    assert value is not None
    return value.strip()


def _optional_text_value(value: str | None) -> str | None:
    if _is_blank(value):
        return None
    assert value is not None
    return value.strip()


def _required_present_value(value: date | str | None, field_name: str) -> date | str:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"{field_name} est obligatoire.")
    if isinstance(value, str):
        return value.strip()
    return value.isoformat()


def _required_date_value(value: date | str | None, field_name: str) -> date:
    if isinstance(value, date):
        return value
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} doit etre au format AAAA-MM-JJ.") from exc


def _required_gender(value: str | None, field_name: str) -> Gender:
    try:
        return Gender(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} doit valoir masculin ou feminin.") from exc


def _required_positive_int_value(value: int | None, field_name: str) -> int:
    if value is None or value < 1:
        raise ValueError(f"{field_name} doit etre un entier positif.")
    return value


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def _is_blank(value: str | None) -> bool:
    return value is None or not value.strip()
