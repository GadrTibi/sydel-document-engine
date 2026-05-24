from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date
from typing import Final

from sydel_doc_engine.domain.case_catalog import (
    CaseInput,
    CaseType,
    DocumentAvailability,
    ExpectedDocument,
    get_expected_documents,
)
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
from sydel_doc_engine.front_data.models import (
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CanonicalFieldValue,
    CanonicalRelationType,
    CompanyRecord,
    DossierRecord,
    FrontObjectType,
    PersonRecord,
    ReuseRuleKind,
    ReuseRuleState,
    ReuseRuleStatus,
    RoleScope,
    RoleTargetType,
    address_ref,
)
from sydel_doc_engine.front_data.unit_document_mode import (
    UNIT_DOCUMENT_V1_SUPPORTED_CODES,
    UnitDocumentPlan,
    UnitDocumentScopeStatus,
    build_unit_document_plan,
    prepare_unit_document_generation,
    unit_document_requirement,
    unit_document_requirement_rows,
)

SUPPORTED_SINGLE_DOCUMENT_CODES: Final[tuple[str, ...]] = UNIT_DOCUMENT_V1_SUPPORTED_CODES

UNIT_STATUS_SUPPORTED: Final = "supported"
UNIT_STATUS_MANUAL_ONLY: Final = "manual_only"
UNIT_STATUS_NOT_IMPLEMENTED: Final = "not_implemented"
UNIT_STATUS_NEEDS_MAPPING: Final = "needs_mapping"
UNIT_STATUS_NOT_SUPPORTED: Final = "not_supported"
UNIT_STATUS_GENERABLE_WITH_RESERVE: Final = "generable_with_reserve"

UNIT_STATUS_LABELS: Final[dict[str, str]] = {
    UNIT_STATUS_SUPPORTED: "Supporte dans ce mode",
    UNIT_STATUS_MANUAL_ONLY: "A remplir manuellement",
    UNIT_STATUS_NOT_IMPLEMENTED: "Non implemente",
    UNIT_STATUS_NEEDS_MAPPING: "Mapping DOC-XXX a confirmer",
    UNIT_STATUS_NOT_SUPPORTED: "Pas encore supporte dans ce mode",
    UNIT_STATUS_GENERABLE_WITH_RESERVE: "Visible avec reserve",
}


@dataclass(frozen=True)
class SingleDocumentChoice:
    document_key: str
    document_label: str
    document_code: str | None
    availability: DocumentAvailability
    status: str
    reasons: tuple[str, ...]
    notes: tuple[str, ...]

    @property
    def identifier(self) -> str:
        return self.document_code or self.document_key

    @property
    def display_label(self) -> str:
        prefix = self.document_code or "sans DOC-XXX"
        return f"{prefix} - {self.document_label}"


@dataclass(frozen=True)
class SingleDocumentFieldSpec:
    key: str
    label: str
    group: str
    kind: str = "text"
    example: str | int | bool | None = ""
    choices: tuple[str, ...] = ()
    required: bool = True
    help_text: str = ""


@dataclass(frozen=True)
class SingleDocumentAssociateInput:
    genre: str = Gender.MASCULIN.value
    civilite_affichage: str = ""
    prenom: str = ""
    nom: str = ""
    nb_parts: int | None = None
    est_present_ou_represente: bool = True


@dataclass(frozen=True)
class SingleDocumentInput:
    structure: str = CaseType.SELARL.value
    document_code: str = "DOC-001"
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
    societe_siege_num_voie: str = ""
    societe_siege_voie: str = ""
    societe_siege_cp: str = ""
    societe_siege_ville: str = ""
    societe_ville_rcs: str = ""
    domiciliation_adresse_affichee: str = ""
    associes: tuple[SingleDocumentAssociateInput, ...] = field(default_factory=tuple)
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


FIELD_SPECS_BY_DOCUMENT: Final[dict[str, tuple[SingleDocumentFieldSpec, ...]]] = {
    "DOC-001": (
        SingleDocumentFieldSpec(
            "personne_genre",
            "Genre grammatical du signataire",
            "Signataire",
            "choice",
            Gender.MASCULIN.value,
            (Gender.MASCULIN.value, Gender.FEMININ.value),
        ),
        SingleDocumentFieldSpec(
            "personne_civilite",
            "Civilite du signataire",
            "Signataire",
            "choice",
            "Monsieur",
            ("Monsieur", "Madame"),
        ),
        SingleDocumentFieldSpec(
            "personne_prenom", "Prenom du signataire", "Signataire", example="Jean"
        ),
        SingleDocumentFieldSpec(
            "personne_nom", "Nom du signataire", "Signataire", example="Durand"
        ),
        SingleDocumentFieldSpec(
            "personne_date_naissance",
            "Date de naissance du signataire",
            "Signataire",
            "date",
            "1990-02-03",
            help_text="Format AAAA-MM-JJ.",
        ),
        SingleDocumentFieldSpec(
            "personne_nationalite",
            "Nationalite du signataire",
            "Signataire",
            example="francaise",
        ),
        SingleDocumentFieldSpec(
            "personne_nom_pere", "Nom du pere", "Signataire", example="Pierre Durand"
        ),
        SingleDocumentFieldSpec(
            "personne_nom_mere", "Nom de la mere", "Signataire", example="Anne Martin"
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_num_voie",
            "Adresse personnelle du signataire - numero",
            "Adresse personnelle",
            example="12",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_voie",
            "Adresse personnelle du signataire - voie",
            "Adresse personnelle",
            example="rue des Lilas",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_cp",
            "Adresse personnelle du signataire - code postal",
            "Adresse personnelle",
            example="75008",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_ville",
            "Adresse personnelle du signataire - ville",
            "Adresse personnelle",
            example="Paris",
        ),
        SingleDocumentFieldSpec(
            "signature_lieu", "Lieu de signature", "Signature", example="Paris"
        ),
        SingleDocumentFieldSpec(
            "signature_date",
            "Date de signature",
            "Signature",
            "date",
            "2026-05-20",
            help_text="Format AAAA-MM-JJ.",
        ),
    ),
    "DOC-002": (
        SingleDocumentFieldSpec(
            "personne_civilite",
            "Civilite du signataire",
            "Signataire",
            "choice",
            "Monsieur",
            ("Monsieur", "Madame"),
        ),
        SingleDocumentFieldSpec(
            "personne_prenom", "Prenom du signataire", "Signataire", example="Jean"
        ),
        SingleDocumentFieldSpec(
            "personne_nom", "Nom du signataire", "Signataire", example="Durand"
        ),
        SingleDocumentFieldSpec(
            "societe_denomination",
            "Denomination de la societe",
            "Societe",
            example="SELARL DU CENTRE",
        ),
        SingleDocumentFieldSpec(
            "societe_capital_social", "Capital social", "Societe", example="5 000"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_num_voie", "Adresse du siege - numero", "Siege", example="12"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_voie", "Adresse du siege - voie", "Siege", example="rue de la Paix"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_cp", "Adresse du siege - code postal", "Siege", example="75002"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_ville", "Adresse du siege - ville", "Siege", example="Paris"
        ),
        SingleDocumentFieldSpec(
            "domiciliation_adresse_affichee",
            "Adresse de domiciliation affichee",
            "Domiciliation",
            example="12 rue de la Paix, 75002 Paris",
        ),
        SingleDocumentFieldSpec(
            "signature_lieu", "Lieu de signature", "Signature", example="Paris"
        ),
        SingleDocumentFieldSpec(
            "signature_date",
            "Date de signature",
            "Signature",
            "date",
            "2026-05-20",
            help_text="Format AAAA-MM-JJ.",
        ),
    ),
    "DOC-003": (
        SingleDocumentFieldSpec(
            "personne_civilite",
            "Civilite du signataire",
            "Signataire",
            "choice",
            "Monsieur",
            ("Monsieur", "Madame"),
        ),
        SingleDocumentFieldSpec(
            "personne_prenom", "Prenom du signataire", "Signataire", example="Jean"
        ),
        SingleDocumentFieldSpec(
            "personne_nom", "Nom du signataire", "Signataire", example="Durand"
        ),
        SingleDocumentFieldSpec(
            "personne_fonction_dirigeant",
            "Fonction du signataire",
            "Signataire",
            example="Gerant",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_num_voie",
            "Adresse personnelle du signataire - numero",
            "Adresse personnelle",
            example="12",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_voie",
            "Adresse personnelle du signataire - voie",
            "Adresse personnelle",
            example="rue des Lilas",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_cp",
            "Adresse personnelle du signataire - code postal",
            "Adresse personnelle",
            example="75008",
        ),
        SingleDocumentFieldSpec(
            "personne_adresse_ville",
            "Adresse personnelle du signataire - ville",
            "Adresse personnelle",
            example="Paris",
        ),
        SingleDocumentFieldSpec(
            "societe_forme_sociale", "Forme sociale", "Societe", example="SELARL"
        ),
        SingleDocumentFieldSpec(
            "societe_denomination",
            "Denomination de la societe",
            "Societe",
            example="SELARL DU CENTRE",
        ),
        SingleDocumentFieldSpec(
            "societe_siege_num_voie", "Adresse du siege - numero", "Siege", example="12"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_voie", "Adresse du siege - voie", "Siege", example="rue de la Paix"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_cp", "Adresse du siege - code postal", "Siege", example="75002"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_ville", "Adresse du siege - ville", "Siege", example="Paris"
        ),
        SingleDocumentFieldSpec(
            "signature_lieu", "Lieu de signature", "Signature", example="Paris"
        ),
        SingleDocumentFieldSpec(
            "signature_date",
            "Date de signature",
            "Signature",
            "date",
            "2026-05-20",
            help_text="Format AAAA-MM-JJ.",
        ),
    ),
    "DOC-004": (
        SingleDocumentFieldSpec(
            "societe_denomination",
            "Denomination de la societe",
            "Societe",
            example="SELARL DU CENTRE",
        ),
        SingleDocumentFieldSpec(
            "societe_forme_sociale", "Forme sociale", "Societe", example="SELARL"
        ),
        SingleDocumentFieldSpec(
            "societe_forme_sociale_affichage",
            "Forme sociale affichee",
            "Societe",
            example="Societe d'exercice liberal a responsabilite limitee",
        ),
        SingleDocumentFieldSpec(
            "societe_forme_sociale_libelle_long",
            "Libelle long de forme sociale",
            "Societe",
            example="societe d'exercice liberal a responsabilite limitee",
        ),
        SingleDocumentFieldSpec(
            "societe_capital_social", "Capital social", "Societe", example="5 000"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_num_voie", "Adresse du siege - numero", "Siege", example="12"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_voie", "Adresse du siege - voie", "Siege", example="rue de la Paix"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_cp", "Adresse du siege - code postal", "Siege", example="75002"
        ),
        SingleDocumentFieldSpec(
            "societe_siege_ville", "Adresse du siege - ville", "Siege", example="Paris"
        ),
        SingleDocumentFieldSpec("societe_ville_rcs", "Ville RCS", "Societe", example="Paris"),
        SingleDocumentFieldSpec(
            "capital_nb_parts_total",
            "Nombre total de parts",
            "Capital",
            "int",
            500,
        ),
        SingleDocumentFieldSpec(
            "capital_valeur_nominale_part",
            "Valeur nominale d'une part",
            "Capital",
            example="10",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_genre",
            "Genre grammatical du gerant",
            "Gerant nomme",
            "choice",
            Gender.MASCULIN.value,
            (Gender.MASCULIN.value, Gender.FEMININ.value),
        ),
        SingleDocumentFieldSpec(
            "dirigeant_civilite_affichage",
            "Civilite du gerant",
            "Gerant nomme",
            "choice",
            "Monsieur",
            ("Monsieur", "Madame"),
        ),
        SingleDocumentFieldSpec(
            "dirigeant_prenom", "Prenom du gerant", "Gerant nomme", example="Jean"
        ),
        SingleDocumentFieldSpec("dirigeant_nom", "Nom du gerant", "Gerant nomme", example="Durand"),
        SingleDocumentFieldSpec(
            "dirigeant_date_naissance",
            "Date de naissance du gerant",
            "Gerant nomme",
            "date",
            "1990-02-03",
            help_text="Format AAAA-MM-JJ.",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_ville_naissance",
            "Ville de naissance du gerant",
            "Gerant nomme",
            example="Lyon",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_departement_naissance",
            "Departement de naissance du gerant",
            "Gerant nomme",
            example="Rhone",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_nationalite", "Nationalite du gerant", "Gerant nomme", example="francaise"
        ),
        SingleDocumentFieldSpec(
            "dirigeant_fonction_affichage",
            "Fonction affichee du gerant",
            "Gerant nomme",
            example="gerant",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_adresse_num_voie",
            "Adresse personnelle du gerant - numero",
            "Adresse du gerant",
            example="12",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_adresse_voie",
            "Adresse personnelle du gerant - voie",
            "Adresse du gerant",
            example="rue des Lilas",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_adresse_cp",
            "Adresse personnelle du gerant - code postal",
            "Adresse du gerant",
            example="75008",
        ),
        SingleDocumentFieldSpec(
            "dirigeant_adresse_ville",
            "Adresse personnelle du gerant - ville",
            "Adresse du gerant",
            example="Paris",
        ),
        SingleDocumentFieldSpec(
            "decision_date",
            "Date de decision",
            "Decision et reunion",
            "date",
            "2026-05-20",
            help_text="Format AAAA-MM-JJ.",
        ),
        SingleDocumentFieldSpec(
            "reunion_date_lettres",
            "Date de reunion en lettres",
            "Decision et reunion",
            example="vingt mai deux mille vingt-six",
        ),
        SingleDocumentFieldSpec(
            "reunion_heure", "Heure de reunion", "Decision et reunion", example="10 heures"
        ),
        SingleDocumentFieldSpec(
            "signature_lieu", "Lieu de signature", "Signature", example="Paris"
        ),
        SingleDocumentFieldSpec(
            "signature_date",
            "Date de signature",
            "Signature",
            "date",
            "2026-05-20",
            help_text="Format AAAA-MM-JJ.",
        ),
        SingleDocumentFieldSpec(
            "signature_nombre_exemplaires",
            "Nombre d'exemplaires",
            "Signature",
            example="3",
        ),
        SingleDocumentFieldSpec(
            "emprunt_actif",
            "Emprunt autorise dans le PV",
            "Emprunt optionnel",
            "bool",
            False,
            required=False,
        ),
    ),
}

DOC_004_EMPRUNT_FIELD_SPECS: Final[tuple[SingleDocumentFieldSpec, ...]] = (
    SingleDocumentFieldSpec(
        "emprunt_montant_max",
        "Montant maximum de l'emprunt",
        "Emprunt optionnel",
        example="150 000",
    ),
    SingleDocumentFieldSpec(
        "bien_adresse_num_voie", "Adresse du bien finance - numero", "Bien finance", example="4"
    ),
    SingleDocumentFieldSpec(
        "bien_adresse_voie",
        "Adresse du bien finance - voie",
        "Bien finance",
        example="rue du Cabinet",
    ),
    SingleDocumentFieldSpec(
        "bien_adresse_cp", "Adresse du bien finance - code postal", "Bien finance", example="75015"
    ),
    SingleDocumentFieldSpec(
        "bien_adresse_ville", "Adresse du bien finance - ville", "Bien finance", example="Paris"
    ),
)


def single_document_choices(
    structure: str,
    conditions: Mapping[str, object | None] | None = None,
) -> tuple[SingleDocumentChoice, ...]:
    case_input = CaseInput(
        case_type=_normalize_case_type(structure),
        conditions=_clean_conditions(conditions or {}),
    )
    return tuple(_choice_from_expected(document) for document in get_expected_documents(case_input))


def single_document_table_rows(
    choices: tuple[SingleDocumentChoice, ...],
) -> list[dict[str, str]]:
    return [
        {
            "code document": choice.document_code or "",
            "libelle document": choice.document_label,
            "statut": UNIT_STATUS_LABELS[choice.status],
            "raison de presence": " ; ".join(choice.reasons),
            "notes": " ; ".join(choice.notes),
        }
        for choice in choices
    ]


def single_document_requirement_rows(document_code: str) -> tuple[dict[str, str], ...]:
    return unit_document_requirement_rows(document_code)


def field_specs_for_document(document_code: str) -> tuple[SingleDocumentFieldSpec, ...]:
    return FIELD_SPECS_BY_DOCUMENT.get(document_code, ())


def emprunt_field_specs_for_doc_004() -> tuple[SingleDocumentFieldSpec, ...]:
    return DOC_004_EMPRUNT_FIELD_SPECS


def sample_single_document_input(
    document_code: str,
    *,
    structure: str = CaseType.SELARL.value,
) -> SingleDocumentInput:
    associes = (
        SingleDocumentAssociateInput(
            genre=Gender.MASCULIN.value,
            civilite_affichage="Monsieur",
            prenom="Jean",
            nom="Durand",
            nb_parts=500,
        ),
    )
    return SingleDocumentInput(
        structure=structure,
        document_code=document_code,
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
        societe_forme_sociale="SELARL" if structure == CaseType.SELARL.value else structure,
        societe_forme_sociale_affichage=(
            "Societe d'exercice liberal a responsabilite limitee"
            if structure == CaseType.SELARL.value
            else structure
        ),
        societe_forme_sociale_libelle_long=(
            "societe d'exercice liberal a responsabilite limitee"
            if structure == CaseType.SELARL.value
            else structure.lower()
        ),
        societe_denomination="SELARL DU CENTRE",
        societe_capital_social="5 000",
        societe_siege_num_voie="12",
        societe_siege_voie="rue de la Paix",
        societe_siege_cp="75002",
        societe_siege_ville="Paris",
        societe_ville_rcs="Paris",
        domiciliation_adresse_affichee="12 rue de la Paix, 75002 Paris",
        associes=associes,
        dirigeant_genre=Gender.MASCULIN.value,
        dirigeant_civilite_affichage="Monsieur",
        dirigeant_prenom="Jean",
        dirigeant_nom="Durand",
        dirigeant_date_naissance=date(1990, 2, 3),
        dirigeant_ville_naissance="Lyon",
        dirigeant_departement_naissance="Rhone",
        dirigeant_nationalite="francaise",
        dirigeant_fonction_affichage="gerant",
        dirigeant_adresse_num_voie="12",
        dirigeant_adresse_voie="rue des Lilas",
        dirigeant_adresse_cp="75008",
        dirigeant_adresse_ville="Paris",
        capital_nb_parts_total=500,
        capital_valeur_nominale_part="10",
        decision_date=date(2026, 5, 20),
        reunion_date_lettres="vingt mai deux mille vingt-six",
        reunion_heure="10 heures",
        signature_lieu="Paris",
        signature_date=date(2026, 5, 20),
        signature_nombre_exemplaires="3",
        emprunt_actif=False,
        emprunt_montant_max="150 000",
        bien_adresse_num_voie="4",
        bien_adresse_voie="rue du Cabinet",
        bien_adresse_cp="75015",
        bien_adresse_ville="Paris",
    )


def validate_single_document_input(data: SingleDocumentInput) -> tuple[str, ...]:
    missing: list[str] = []
    for spec in field_specs_for_document(data.document_code):
        if spec.key == "emprunt_actif":
            continue
        _require_field(data, spec, missing)
    if data.document_code == "DOC-004":
        _validate_doc_004_associes(data, missing)
        if data.emprunt_actif:
            for spec in DOC_004_EMPRUNT_FIELD_SPECS:
                _require_field(data, spec, missing)
    return tuple(dict.fromkeys(missing))


def build_single_document_front_dossier(data: SingleDocumentInput) -> DossierRecord:
    dossier = DossierRecord(
        id=f"unit-{data.document_code}",
        label=f"Document unitaire {data.document_code}",
        structure=data.structure,
    )
    dossier.add_document_requirement(unit_document_requirement(data.document_code))

    if data.document_code == "DOC-004":
        _populate_doc_004_front_dossier(dossier, data)
    else:
        _populate_common_signataire(dossier, data)
        if data.document_code in {"DOC-002", "DOC-003"}:
            _populate_common_company(dossier, data)
        if data.document_code == "DOC-002":
            _populate_doc_002_front_data(dossier, data)
        if data.document_code == "DOC-003":
            _populate_doc_003_front_data(dossier, data)
        if data.document_code == "DOC-001":
            _populate_doc_001_front_data(dossier, data)

    _add_canonical_value(dossier, "signature.lieu", data.signature_lieu)
    _add_canonical_value(dossier, "signature.date", data.signature_date)
    return dossier


def build_single_document_unit_plan(data: SingleDocumentInput) -> UnitDocumentPlan:
    dossier = build_single_document_front_dossier(data)
    return prepare_unit_document_generation(data.document_code, dossier).plan


def build_single_document_context(data: SingleDocumentInput) -> DocumentGenerationContext:
    missing = validate_single_document_input(data)
    if missing:
        raise ValueError("Champs manquants: " + ", ".join(missing))

    if data.document_code == "DOC-001":
        return _build_doc_001_context(data)
    if data.document_code == "DOC-002":
        return _build_doc_002_context(data)
    if data.document_code == "DOC-003":
        return _build_doc_003_context(data)
    if data.document_code == "DOC-004":
        return _build_doc_004_context(data)
    raise ValueError(f"Document non supporte dans ce mode: {data.document_code}")


def _populate_common_signataire(
    dossier: DossierRecord,
    data: SingleDocumentInput,
) -> None:
    person = PersonRecord(
        id="person-signataire",
        civilite_affichage=data.personne_civilite or None,
        genre=data.personne_genre or None,
        prenom=data.personne_prenom or None,
        nom=data.personne_nom or None,
        fonction=data.personne_fonction_dirigeant or None,
    )
    dossier.add_person(person)
    dossier.assign_role(
        BusinessRole.SIGNATAIRE,
        RoleTargetType.PERSON,
        person.id,
        scope=RoleScope.DOCUMENT,
        document_code=data.document_code,
    )
    if data.document_code == "DOC-002":
        dossier.assign_role(
            BusinessRole.PRATICIEN,
            RoleTargetType.PERSON,
            person.id,
            scope=RoleScope.DOSSIER,
        )

    address = _front_address_from_parts(
        "address-signataire",
        AddressUsage.ADRESSE_PERSONNELLE,
        data.personne_adresse_num_voie,
        data.personne_adresse_voie,
        data.personne_adresse_cp,
        data.personne_adresse_ville,
    )
    if address.has_value():
        dossier.add_address(address)
        person.add_address(address.id)


def _populate_common_company(
    dossier: DossierRecord,
    data: SingleDocumentInput,
) -> None:
    company = CompanyRecord(
        id="company-principale",
        denomination=data.societe_denomination or "__societe_a_completer__",
        forme_sociale=data.societe_forme_sociale or None,
        capital_social=data.societe_capital_social or None,
    )
    dossier.add_company(company)
    dossier.assign_role(
        BusinessRole.SOCIETE_PRINCIPALE,
        RoleTargetType.COMPANY,
        company.id,
        scope=RoleScope.DOSSIER,
    )
    address = _front_address_from_parts(
        "address-siege",
        AddressUsage.SIEGE_SOCIAL,
        data.societe_siege_num_voie,
        data.societe_siege_voie,
        data.societe_siege_cp,
        data.societe_siege_ville,
    )
    if address.has_value():
        dossier.add_address(address)
        company.add_address(address.id)


def _populate_doc_001_front_data(
    dossier: DossierRecord,
    data: SingleDocumentInput,
) -> None:
    _add_canonical_value(dossier, "personne.signataire.genre", data.personne_genre)
    _add_canonical_value(
        dossier,
        "personne.signataire.civilite_affichage",
        data.personne_civilite,
    )
    _add_canonical_value(dossier, "personne.signataire.prenom", data.personne_prenom)
    _add_canonical_value(dossier, "personne.signataire.nom", data.personne_nom)
    _add_canonical_value(
        dossier,
        "personne.signataire.date_naissance",
        data.personne_date_naissance,
    )
    _add_canonical_value(
        dossier,
        "personne.signataire.nationalite",
        data.personne_nationalite,
    )
    _add_canonical_value(dossier, "personne.signataire.nom_pere", data.personne_nom_pere)
    _add_canonical_value(dossier, "personne.signataire.nom_mere", data.personne_nom_mere)
    _add_canonical_value(
        dossier,
        "personne.signataire.adresse_personnelle",
        _display_address(
            data.personne_adresse_num_voie,
            data.personne_adresse_voie,
            data.personne_adresse_cp,
            data.personne_adresse_ville,
        ),
    )


def _populate_doc_002_front_data(
    dossier: DossierRecord,
    data: SingleDocumentInput,
) -> None:
    _add_canonical_value(
        dossier,
        "personne.signataire.civilite_affichage",
        data.personne_civilite,
    )
    _add_canonical_value(dossier, "personne.signataire.prenom", data.personne_prenom)
    _add_canonical_value(dossier, "personne.signataire.nom", data.personne_nom)
    _add_canonical_value(
        dossier,
        "societe.societe_principale.denomination",
        data.societe_denomination,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.capital_social",
        data.societe_capital_social,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.siege.adresse",
        _display_address(
            data.societe_siege_num_voie,
            data.societe_siege_voie,
            data.societe_siege_cp,
            data.societe_siege_ville,
        ),
    )
    domiciliation = AddressRecord(
        id="address-domiciliation",
        usage=AddressUsage.DOMICILIATION,
        display_value=data.domiciliation_adresse_affichee or None,
    )
    if domiciliation.has_value():
        dossier.add_address(domiciliation)
    dossier.add_reuse_rule(
        ReuseRuleState(
            id="unit-doc-002-siege-domiciliation",
            source_ref=address_ref(AddressUsage.SIEGE_SOCIAL),
            target_ref=address_ref(AddressUsage.DOMICILIATION),
            relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
            label="Document unitaire : domiciliation depuis le siege",
            kind=ReuseRuleKind.REFERENCE,
            status=ReuseRuleStatus.ACTIVE,
            explicit=True,
        )
    )
    _add_canonical_value(
        dossier,
        "domiciliation.adresse",
        data.domiciliation_adresse_affichee,
    )
    dossier.resolve_ambiguity("legacy_domiciliation_display_alias")


def _populate_doc_003_front_data(
    dossier: DossierRecord,
    data: SingleDocumentInput,
) -> None:
    _add_canonical_value(
        dossier,
        "personne.signataire.civilite_affichage",
        data.personne_civilite,
    )
    _add_canonical_value(dossier, "personne.signataire.prenom", data.personne_prenom)
    _add_canonical_value(dossier, "personne.signataire.nom", data.personne_nom)
    _add_canonical_value(
        dossier,
        "personne.signataire.fonction",
        data.personne_fonction_dirigeant,
    )
    _add_canonical_value(
        dossier,
        "personne.signataire.adresse_personnelle",
        _display_address(
            data.personne_adresse_num_voie,
            data.personne_adresse_voie,
            data.personne_adresse_cp,
            data.personne_adresse_ville,
        ),
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.forme_sociale",
        data.societe_forme_sociale,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.denomination",
        data.societe_denomination,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.siege.adresse",
        _display_address(
            data.societe_siege_num_voie,
            data.societe_siege_voie,
            data.societe_siege_cp,
            data.societe_siege_ville,
        ),
    )


def _populate_doc_004_front_dossier(
    dossier: DossierRecord,
    data: SingleDocumentInput,
) -> None:
    person = PersonRecord(
        id="person-gerant",
        civilite_affichage=data.dirigeant_civilite_affichage or None,
        genre=data.dirigeant_genre or None,
        prenom=data.dirigeant_prenom or None,
        nom=data.dirigeant_nom or None,
        fonction=data.dirigeant_fonction_affichage or None,
    )
    dossier.add_person(person)
    for role in (BusinessRole.GERANT, BusinessRole.ASSOCIE):
        dossier.assign_role(
            role,
            RoleTargetType.PERSON,
            person.id,
            scope=RoleScope.DOSSIER,
        )
    dossier.assign_role(
        BusinessRole.SIGNATAIRE,
        RoleTargetType.PERSON,
        person.id,
        scope=RoleScope.DOCUMENT,
        document_code=data.document_code,
    )

    company = CompanyRecord(
        id="company-principale",
        denomination=data.societe_denomination or "__societe_a_completer__",
        forme_sociale=data.societe_forme_sociale or None,
        capital_social=data.societe_capital_social or None,
    )
    dossier.add_company(company)
    dossier.assign_role(
        BusinessRole.SOCIETE_PRINCIPALE,
        RoleTargetType.COMPANY,
        company.id,
        scope=RoleScope.DOSSIER,
    )

    gerant_address = _front_address_from_parts(
        "address-gerant",
        AddressUsage.ADRESSE_PERSONNELLE,
        data.dirigeant_adresse_num_voie,
        data.dirigeant_adresse_voie,
        data.dirigeant_adresse_cp,
        data.dirigeant_adresse_ville,
    )
    if gerant_address.has_value():
        dossier.add_address(gerant_address)
        person.add_address(gerant_address.id)

    siege = _front_address_from_parts(
        "address-siege",
        AddressUsage.SIEGE_SOCIAL,
        data.societe_siege_num_voie,
        data.societe_siege_voie,
        data.societe_siege_cp,
        data.societe_siege_ville,
    )
    if siege.has_value():
        dossier.add_address(siege)
        company.add_address(siege.id)

    _add_canonical_value(
        dossier,
        "societe.societe_principale.denomination",
        data.societe_denomination,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.forme_sociale",
        data.societe_forme_sociale,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.capital_social",
        data.societe_capital_social,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.siege.adresse",
        _display_address(
            data.societe_siege_num_voie,
            data.societe_siege_voie,
            data.societe_siege_cp,
            data.societe_siege_ville,
        ),
    )
    _add_canonical_value(
        dossier,
        "capital.titres.nombre_total",
        data.capital_nb_parts_total,
    )
    _add_canonical_value(
        dossier,
        "capital.titres.valeur_nominale",
        data.capital_valeur_nominale_part,
    )
    _add_canonical_value(dossier, "capital.repartition_associes", data.associes)
    _add_canonical_value(
        dossier,
        "personne.gerant.civilite_affichage",
        data.dirigeant_civilite_affichage,
    )
    _add_canonical_value(dossier, "personne.gerant.prenom", data.dirigeant_prenom)
    _add_canonical_value(dossier, "personne.gerant.nom", data.dirigeant_nom)
    _add_canonical_value(
        dossier,
        "personne.gerant.date_naissance",
        data.dirigeant_date_naissance,
    )
    _add_canonical_value(
        dossier,
        "personne.gerant.nationalite",
        data.dirigeant_nationalite,
    )
    _add_canonical_value(
        dossier,
        "personne.gerant.adresse_personnelle",
        _display_address(
            data.dirigeant_adresse_num_voie,
            data.dirigeant_adresse_voie,
            data.dirigeant_adresse_cp,
            data.dirigeant_adresse_ville,
        ),
    )
    _add_canonical_value(dossier, "decision.date", data.decision_date)
    _add_canonical_value(dossier, "reunion.date_lettres", data.reunion_date_lettres)
    _add_canonical_value(dossier, "reunion.heure", data.reunion_heure)
    _add_canonical_value(
        dossier,
        "signature.nombre_exemplaires",
        data.signature_nombre_exemplaires,
    )


def _front_address_from_parts(
    address_id: str,
    usage: AddressUsage,
    street_number: str,
    street_name: str,
    postal_code: str,
    city: str,
) -> AddressRecord:
    return AddressRecord(
        id=address_id,
        usage=usage,
        display_value=_display_address(street_number, street_name, postal_code, city),
        street_number=street_number or None,
        street_name=street_name or None,
        postal_code=postal_code or None,
        city=city or None,
        owner_object_type=(
            FrontObjectType.COMPANY
            if usage is AddressUsage.SIEGE_SOCIAL
            else FrontObjectType.PERSON
        ),
    )


def _display_address(
    street_number: str,
    street_name: str,
    postal_code: str,
    city: str,
) -> str:
    return " ".join(
        part.strip()
        for part in (street_number, street_name, postal_code, city)
        if part and part.strip()
    )


def _add_canonical_value(
    dossier: DossierRecord,
    field_path: str,
    value: object,
) -> None:
    if _is_blank(value):
        return
    dossier.add_canonical_value(
        CanonicalFieldValue(
            field_path=field_path,
            value=value,
        )
    )


def _choice_from_expected(document: ExpectedDocument) -> SingleDocumentChoice:
    return SingleDocumentChoice(
        document_key=document.document_key,
        document_label=document.document_label,
        document_code=document.document_code,
        availability=document.availability,
        status=_choice_status(document),
        reasons=document.reasons,
        notes=document.notes,
    )


def _choice_status(document: ExpectedDocument) -> str:
    if document.document_code is not None:
        return _app_status_from_unit_scope(
            build_unit_document_plan(document.document_code).scope_status
        )
    if document.availability == DocumentAvailability.MANUAL_ONLY:
        return UNIT_STATUS_MANUAL_ONLY
    if document.availability == DocumentAvailability.NOT_IMPLEMENTED:
        return UNIT_STATUS_NOT_IMPLEMENTED
    if (
        document.availability == DocumentAvailability.NEEDS_MAPPING
        or document.document_code is None
    ):
        return UNIT_STATUS_NEEDS_MAPPING
    return UNIT_STATUS_NOT_SUPPORTED


def _app_status_from_unit_scope(scope_status: UnitDocumentScopeStatus) -> str:
    if scope_status is UnitDocumentScopeStatus.SUPPORTED:
        return UNIT_STATUS_SUPPORTED
    if scope_status is UnitDocumentScopeStatus.MANUAL_ONLY:
        return UNIT_STATUS_MANUAL_ONLY
    if scope_status is UnitDocumentScopeStatus.NOT_IMPLEMENTED:
        return UNIT_STATUS_NOT_IMPLEMENTED
    if scope_status is UnitDocumentScopeStatus.CONTEXT_INCOMPLETE:
        return UNIT_STATUS_NEEDS_MAPPING
    if scope_status is UnitDocumentScopeStatus.GENERABLE_WITH_RESERVE:
        return UNIT_STATUS_GENERABLE_WITH_RESERVE
    return UNIT_STATUS_NOT_SUPPORTED


def _clean_conditions(conditions: Mapping[str, object | None]) -> dict[str, object]:
    return {key: value for key, value in conditions.items() if value is not None}


def _normalize_case_type(structure: str) -> CaseType:
    if structure == "SCI IRIS":
        return CaseType.SCI
    return CaseType(structure)


def _require_field(
    data: SingleDocumentInput,
    spec: SingleDocumentFieldSpec,
    missing: list[str],
) -> None:
    value = getattr(data, spec.key)
    if spec.kind == "int":
        if not isinstance(value, int) or value < 1:
            missing.append(spec.key)
        return
    if spec.kind == "date":
        _require_date(value, spec.key, missing)
        return
    if spec.kind == "choice":
        if value not in spec.choices:
            missing.append(spec.key)
        return
    if spec.kind == "bool":
        return
    if _is_blank(value):
        missing.append(spec.key)


def _validate_doc_004_associes(data: SingleDocumentInput, missing: list[str]) -> None:
    if not data.associes:
        missing.append("associes[]")
        return
    represented_parts = 0
    for index, associe in enumerate(data.associes, start=1):
        prefix = f"associes[{index}]"
        if associe.genre not in {Gender.MASCULIN.value, Gender.FEMININ.value}:
            missing.append(f"{prefix}.genre")
        _require_text(associe.civilite_affichage, f"{prefix}.civilite_affichage", missing)
        _require_text(associe.prenom, f"{prefix}.prenom", missing)
        _require_text(associe.nom, f"{prefix}.nom", missing)
        if associe.nb_parts is None or associe.nb_parts < 1:
            missing.append(f"{prefix}.nb_parts")
        elif associe.est_present_ou_represente:
            represented_parts += associe.nb_parts
    if (
        data.capital_nb_parts_total is not None
        and data.capital_nb_parts_total > 0
        and represented_parts != data.capital_nb_parts_total
    ):
        missing.append("capital.nb_parts_total doit correspondre aux parts representees")


def _build_doc_001_context(data: SingleDocumentInput) -> DocumentGenerationContext:
    return _base_context(
        data,
        person=Person(
            genre=Gender(data.personne_genre),
            civilite=_required_text_value(data.personne_civilite, "personne_civilite"),
            prenom=_required_text_value(data.personne_prenom, "personne_prenom"),
            nom=_required_text_value(data.personne_nom, "personne_nom"),
            adresse_perso=_address_from_parts(
                data.personne_adresse_num_voie,
                data.personne_adresse_voie,
                data.personne_adresse_cp,
                data.personne_adresse_ville,
            ),
            date_naissance=_required_date_value(
                data.personne_date_naissance, "personne_date_naissance"
            ),
            nationalite=_required_text_value(data.personne_nationalite, "personne_nationalite"),
            nom_pere=_required_text_value(data.personne_nom_pere, "personne_nom_pere"),
            nom_mere=_required_text_value(data.personne_nom_mere, "personne_nom_mere"),
        ),
    )


def _build_doc_002_context(data: SingleDocumentInput) -> DocumentGenerationContext:
    return _base_context(
        data,
        person=_basic_person(data),
        societe=Company(
            denomination=_required_text_value(data.societe_denomination, "societe_denomination"),
            capital=_required_text_value(data.societe_capital_social, "societe_capital_social"),
            capital_social=_required_text_value(
                data.societe_capital_social,
                "societe_capital_social",
            ),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=_required_text_value(
                data.domiciliation_adresse_affichee,
                "domiciliation_adresse_affichee",
            )
        ),
    )


def _build_doc_003_context(data: SingleDocumentInput) -> DocumentGenerationContext:
    return _base_context(
        data,
        person=Person(
            genre=Gender(data.personne_genre),
            civilite=_required_text_value(data.personne_civilite, "personne_civilite"),
            prenom=_required_text_value(data.personne_prenom, "personne_prenom"),
            nom=_required_text_value(data.personne_nom, "personne_nom"),
            adresse_perso=_address_from_parts(
                data.personne_adresse_num_voie,
                data.personne_adresse_voie,
                data.personne_adresse_cp,
                data.personne_adresse_ville,
            ),
            fonction_dirigeant=_required_text_value(
                data.personne_fonction_dirigeant,
                "personne_fonction_dirigeant",
            ),
        ),
        societe=Company(
            forme_sociale=_required_text_value(data.societe_forme_sociale, "societe_forme_sociale"),
            denomination=_required_text_value(data.societe_denomination, "societe_denomination"),
            siege=_address_from_parts(
                data.societe_siege_num_voie,
                data.societe_siege_voie,
                data.societe_siege_cp,
                data.societe_siege_ville,
            ),
        ),
    )


def _build_doc_004_context(data: SingleDocumentInput) -> DocumentGenerationContext:
    dirigeant_address = _address_from_parts(
        data.dirigeant_adresse_num_voie,
        data.dirigeant_adresse_voie,
        data.dirigeant_adresse_cp,
        data.dirigeant_adresse_ville,
    )
    dirigeant_birth_date = _required_date_value(
        data.dirigeant_date_naissance,
        "dirigeant_date_naissance",
    )
    return _base_context(
        data,
        person=Person(
            genre=Gender(data.dirigeant_genre),
            civilite=_required_text_value(
                data.dirigeant_civilite_affichage,
                "dirigeant_civilite_affichage",
            ),
            prenom=_required_text_value(data.dirigeant_prenom, "dirigeant_prenom"),
            nom=_required_text_value(data.dirigeant_nom, "dirigeant_nom"),
            adresse_perso=dirigeant_address,
            date_naissance=dirigeant_birth_date,
            nationalite=_required_text_value(data.dirigeant_nationalite, "dirigeant_nationalite"),
            fonction_dirigeant=_required_text_value(
                data.dirigeant_fonction_affichage,
                "dirigeant_fonction_affichage",
            ),
        ),
        societe=Company(
            forme_sociale=_required_text_value(data.societe_forme_sociale, "societe_forme_sociale"),
            forme_sociale_affichage=_required_text_value(
                data.societe_forme_sociale_affichage,
                "societe_forme_sociale_affichage",
            ),
            forme_sociale_libelle_long=_required_text_value(
                data.societe_forme_sociale_libelle_long,
                "societe_forme_sociale_libelle_long",
            ),
            denomination=_required_text_value(data.societe_denomination, "societe_denomination"),
            capital=_required_text_value(data.societe_capital_social, "societe_capital_social"),
            capital_social=_required_text_value(
                data.societe_capital_social,
                "societe_capital_social",
            ),
            capital_variable=True,
            siege=_address_from_parts(
                data.societe_siege_num_voie,
                data.societe_siege_voie,
                data.societe_siege_cp,
                data.societe_siege_ville,
            ),
            ville_rcs=_required_text_value(data.societe_ville_rcs, "societe_ville_rcs"),
        ),
        associes=[_build_associe(associe) for associe in data.associes],
        dirigeant_nomine=DirigeantNomine(
            genre=Gender(data.dirigeant_genre),
            civilite_affichage=_required_text_value(
                data.dirigeant_civilite_affichage,
                "dirigeant_civilite_affichage",
            ),
            prenom=_required_text_value(data.dirigeant_prenom, "dirigeant_prenom"),
            nom=_required_text_value(data.dirigeant_nom, "dirigeant_nom"),
            date_naissance=dirigeant_birth_date,
            ville_naissance=_required_text_value(
                data.dirigeant_ville_naissance,
                "dirigeant_ville_naissance",
            ),
            departement_naissance=_required_text_value(
                data.dirigeant_departement_naissance,
                "dirigeant_departement_naissance",
            ),
            nationalite=_required_text_value(data.dirigeant_nationalite, "dirigeant_nationalite"),
            adresse_personnelle=dirigeant_address,
            fonction_affichage=_required_text_value(
                data.dirigeant_fonction_affichage,
                "dirigeant_fonction_affichage",
            ),
        ),
        decision=DecisionContext(date=_required_present_value(data.decision_date, "decision_date")),
        reunion=ReunionContext(
            date_lettres=_required_text_value(data.reunion_date_lettres, "reunion_date_lettres"),
            heure=_required_text_value(data.reunion_heure, "reunion_heure"),
        ),
        capital=CapitalContext(
            nb_parts_total=_required_positive_int_value(
                data.capital_nb_parts_total,
                "capital_nb_parts_total",
            ),
            valeur_nominale_part=_required_text_value(
                data.capital_valeur_nominale_part,
                "capital_valeur_nominale_part",
            ),
            nb_parts_representees=sum(
                associe.nb_parts or 0
                for associe in data.associes
                if associe.est_present_ou_represente
            ),
        ),
        emprunt=Emprunt(
            actif=data.emprunt_actif,
            montant_max=(
                _required_text_value(data.emprunt_montant_max, "emprunt_montant_max")
                if data.emprunt_actif
                else None
            ),
        ),
        bien_immobilier=(
            BienImmobilier(
                adresse=_address_from_parts(
                    data.bien_adresse_num_voie,
                    data.bien_adresse_voie,
                    data.bien_adresse_cp,
                    data.bien_adresse_ville,
                )
            )
            if data.emprunt_actif
            else None
        ),
    )


def _base_context(
    data: SingleDocumentInput,
    *,
    person: Person,
    societe: Company | None = None,
    domiciliation: Domiciliation | None = None,
    associes: list[Associe] | None = None,
    dirigeant_nomine: DirigeantNomine | None = None,
    decision: DecisionContext | None = None,
    reunion: ReunionContext | None = None,
    capital: CapitalContext | None = None,
    emprunt: Emprunt | None = None,
    bien_immobilier: BienImmobilier | None = None,
) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure=data.structure,
        dossier_options=DossierOptions(
            associe_unique=len(associes or []) == 1,
            scm_cession=False,
            regime_communautaire=False,
            cession=False,
            apport=False,
        ),
        personne_signataire=person,
        signature=Signature(
            lieu=_required_text_value(data.signature_lieu, "signature_lieu"),
            date=_required_date_value(data.signature_date, "signature_date"),
            nombre_exemplaires=(
                _required_text_value(
                    data.signature_nombre_exemplaires,
                    "signature_nombre_exemplaires",
                )
                if data.document_code == "DOC-004"
                else None
            ),
        ),
        societe=societe,
        domiciliation=domiciliation,
        associes=associes or [],
        dirigeant_nomine=dirigeant_nomine,
        decision=decision,
        reunion=reunion,
        capital=capital,
        emprunt=emprunt,
        bien_immobilier=bien_immobilier,
    )


def _basic_person(data: SingleDocumentInput) -> Person:
    return Person(
        genre=Gender(data.personne_genre),
        civilite=_required_text_value(data.personne_civilite, "personne_civilite"),
        prenom=_required_text_value(data.personne_prenom, "personne_prenom"),
        nom=_required_text_value(data.personne_nom, "personne_nom"),
    )


def _build_associe(data: SingleDocumentAssociateInput) -> Associe:
    return Associe(
        genre=Gender(data.genre),
        civilite_affichage=_required_text_value(data.civilite_affichage, "associes[].civilite"),
        prenom=_required_text_value(data.prenom, "associes[].prenom"),
        nom=_required_text_value(data.nom, "associes[].nom"),
        nb_parts=_required_positive_int_value(data.nb_parts, "associes[].nb_parts"),
        est_present_ou_represente=data.est_present_ou_represente,
    )


def _address_from_parts(num_voie: str, voie: str, cp: str, ville: str) -> Address:
    return Address(
        num_voie=_required_text_value(num_voie, "adresse.num_voie"),
        voie=_required_text_value(voie, "adresse.voie"),
        cp=_required_text_value(cp, "adresse.cp"),
        ville=_required_text_value(ville, "adresse.ville"),
    )


def _require_text(value: str | None, field_name: str, missing: list[str]) -> None:
    if _is_blank(value):
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


def _required_text_value(value: str | None, field_name: str) -> str:
    if _is_blank(value):
        raise ValueError(f"{field_name} est obligatoire.")
    assert value is not None
    return value.strip()


def _required_date_value(value: date | str | None, field_name: str) -> date:
    if isinstance(value, date):
        return value
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} doit etre au format AAAA-MM-JJ.") from exc


def _required_present_value(value: date | str | None, field_name: str) -> date | str:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"{field_name} est obligatoire.")
    if isinstance(value, str):
        return value.strip()
    return value.isoformat()


def _required_positive_int_value(value: int | None, field_name: str) -> int:
    if value is None or value < 1:
        raise ValueError(f"{field_name} doit etre un entier positif.")
    return value


def _is_blank(value: object) -> bool:
    return (
        value is None
        or (isinstance(value, str) and not value.strip())
        or (isinstance(value, (tuple, list)) and not value)
    )
