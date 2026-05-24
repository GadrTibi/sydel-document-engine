from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Final

from sydel_doc_engine.app.front_dossier_entry import (
    COMPANY_MAIN_ID,
    DOMICILIATION_ADDRESS_ID,
    PERSONAL_ADDRESS_ID,
    REGISTERED_OFFICE_ADDRESS_ID,
    SELARL_CREATION_SIMPLE_PROFILE_KEY,
)
from sydel_doc_engine.app.ui_runtime import (
    GeneratedPdfBatch,
    build_output_dir,
    generate_docx_files_for_document_codes,
    generate_pdf_files,
    generate_zip_file,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Associe,
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
from sydel_doc_engine.front_data.document_status import (
    DocumentStatus,
    DocumentStatusRecord,
    DocumentStatusSummary,
    build_document_status_summary,
)
from sydel_doc_engine.front_data.models import (
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CompanyRecord,
    DossierRecord,
    PersonRecord,
    RoleTargetType,
)

FRONT_GENERATION_PROFILE_KEY: Final = SELARL_CREATION_SIMPLE_PROFILE_KEY
FRONT_GENERATION_PROFILE_LABEL: Final = "SELARL creation simple"
FRONT_GENERATION_SUPPORTED_DOC_CODES: Final[tuple[str, ...]] = (
    "DOC-001",
    "DOC-002",
    "DOC-003",
    "DOC-004",
)
FRONT_GENERATION_EXCLUDED_DOC_CODES: Final[tuple[str, ...]] = (
    "DOC-006",
    "DOC-013",
    "DOC-014",
)
FRONT_GENERATION_ARTIFACTS_DIR: Final = Path("artifacts") / "front_generation_actions_001"

_ADDRESS_PATTERN = re.compile(
    r"^\s*(?P<number>\d+[A-Za-z]?(?:\s*(?:bis|ter|quater))?)\s+"
    r"(?P<street>.+?)[,\s]+(?P<postal_code>\d{5})\s+(?P<city>.+?)\s*$",
    re.IGNORECASE,
)

_FORME_LABELS: Final[dict[str, tuple[str, str]]] = {
    "SELARL": (
        "Societe d'exercice liberal a responsabilite limitee",
        "societe d'exercice liberal a responsabilite limitee",
    ),
    "SELAS": (
        "Societe d'exercice liberal par actions simplifiee",
        "societe d'exercice liberal par actions simplifiee",
    ),
    "SCM": ("Societe civile de moyens", "societe civile de moyens"),
    "SCI": ("Societe civile immobiliere", "societe civile immobiliere"),
}


class FrontGenerationBlockedError(RuntimeError):
    pass


@dataclass(frozen=True)
class FrontGenerationReadiness:
    summary: DocumentStatusSummary
    target_doc_codes: tuple[str, ...]
    generable_doc_codes: tuple[str, ...]
    blocked_doc_codes: tuple[str, ...]
    excluded_doc_codes: tuple[str, ...]
    runtime_blockers: tuple[str, ...] = ()

    @property
    def can_generate_docx(self) -> bool:
        return (
            self.generable_doc_codes == self.target_doc_codes
            and not self.runtime_blockers
        )

    @property
    def blocked_or_excluded_doc_codes(self) -> tuple[str, ...]:
        return (*self.blocked_doc_codes, *self.excluded_doc_codes)


@dataclass(frozen=True)
class FrontGenerationDocxResult:
    readiness: FrontGenerationReadiness
    context: DocumentGenerationContext
    output_dir: Path
    docx_paths: tuple[Path, ...]


def front_generation_supported_doc_codes() -> tuple[str, ...]:
    return FRONT_GENERATION_SUPPORTED_DOC_CODES


def front_generation_readiness(dossier: DossierRecord) -> FrontGenerationReadiness:
    summary = build_document_status_summary(
        dossier,
        document_codes=FRONT_GENERATION_SUPPORTED_DOC_CODES,
        lot_id=f"front-generation-{FRONT_GENERATION_PROFILE_KEY}",
        lot_label=FRONT_GENERATION_PROFILE_LABEL,
    )
    generable_doc_codes = tuple(
        status.doc_code
        for status in summary.documents
        if status.status is DocumentStatus.GENERABLE
    )
    blocked_doc_codes = tuple(
        status.doc_code
        for status in summary.documents
        if status.status is not DocumentStatus.GENERABLE
    )
    runtime_blockers: tuple[str, ...] = ()
    if generable_doc_codes == FRONT_GENERATION_SUPPORTED_DOC_CODES:
        try:
            build_front_generation_context(dossier)
        except FrontGenerationBlockedError as exc:
            runtime_blockers = (str(exc),)

    return FrontGenerationReadiness(
        summary=summary,
        target_doc_codes=FRONT_GENERATION_SUPPORTED_DOC_CODES,
        generable_doc_codes=generable_doc_codes,
        blocked_doc_codes=blocked_doc_codes,
        excluded_doc_codes=FRONT_GENERATION_EXCLUDED_DOC_CODES,
        runtime_blockers=runtime_blockers,
    )


def front_generation_document_rows(
    readiness: FrontGenerationReadiness,
) -> tuple[dict[str, str], ...]:
    return tuple(_status_row(status) for status in readiness.summary.documents)


def front_generation_runtime_rows(
    readiness: FrontGenerationReadiness,
) -> tuple[dict[str, str], ...]:
    rows = [
        {
            "controle": "profil",
            "statut": "pret" if not readiness.runtime_blockers else "bloque",
            "detail": "SELARL creation simple",
        },
        {
            "controle": "documents cibles",
            "statut": "pret" if readiness.can_generate_docx else "bloque",
            "detail": ", ".join(readiness.target_doc_codes),
        },
        {
            "controle": "documents exclus",
            "statut": "exclus",
            "detail": ", ".join(readiness.excluded_doc_codes),
        },
    ]
    rows.extend(
        {
            "controle": "contexte moteur",
            "statut": "bloque",
            "detail": blocker,
        }
        for blocker in readiness.runtime_blockers
    )
    return tuple(rows)


def build_front_generation_context(dossier: DossierRecord) -> DocumentGenerationContext:
    _require_generation_profile(dossier)
    person = _main_person(dossier)
    company = _main_company(dossier)
    person_address = _engine_address(
        _required_address_record(dossier, AddressUsage.ADRESSE_PERSONNELLE, PERSONAL_ADDRESS_ID),
        "personne_signataire.adresse_perso",
    )
    company_address = _engine_address(
        _required_address_record(dossier, AddressUsage.SIEGE_SOCIAL, REGISTERED_OFFICE_ADDRESS_ID),
        "societe.siege",
    )
    domiciliation_address = _required_address_record(
        dossier,
        AddressUsage.DOMICILIATION,
        DOMICILIATION_ADDRESS_ID,
    )

    signature_date = _required_date(_field(dossier, "signature.date"), "signature.date")
    birth_date = _required_date(
        _role_field(dossier, BusinessRole.PRATICIEN, "date_naissance"),
        "personne.praticien.date_naissance",
    )
    total_parts = _required_positive_int(
        _field(dossier, "capital.titres.nombre_total"),
        "capital.titres.nombre_total",
    )
    forme_sociale = _required_text(
        company.forme_sociale or _field(dossier, "societe.societe_principale.forme_sociale"),
        "societe.societe_principale.forme_sociale",
    )
    forme_affichage, forme_longue = _forme_labels(forme_sociale)

    return DocumentGenerationContext(
        structure="SELARL",
        dossier_options=DossierOptions(
            associe_unique=True,
            regime_communautaire=False,
            cession=False,
            apport=False,
            scm_cession=False,
        ),
        personne_signataire=Person(
            genre=_required_gender(
                _role_field(dossier, BusinessRole.SIGNATAIRE, "genre", BusinessRole.PRATICIEN),
                "personne.signataire.genre",
            ),
            civilite=_required_text(
                _role_field(
                    dossier,
                    BusinessRole.SIGNATAIRE,
                    "civilite_affichage",
                    BusinessRole.PRATICIEN,
                )
                or person.civilite_affichage,
                "personne.signataire.civilite_affichage",
            ),
            prenom=_required_text(
                _role_field(dossier, BusinessRole.SIGNATAIRE, "prenom", BusinessRole.PRATICIEN)
                or person.prenom,
                "personne.signataire.prenom",
            ),
            nom=_required_text(
                _role_field(dossier, BusinessRole.SIGNATAIRE, "nom", BusinessRole.PRATICIEN)
                or person.nom,
                "personne.signataire.nom",
            ),
            adresse_perso=person_address,
            date_naissance=birth_date,
            nationalite=_required_text(
                _role_field(dossier, BusinessRole.PRATICIEN, "nationalite"),
                "personne.praticien.nationalite",
            ),
            nom_pere=_required_text(
                _role_field(dossier, BusinessRole.PRATICIEN, "nom_pere"),
                "personne.praticien.nom_pere",
            ),
            nom_mere=_required_text(
                _role_field(dossier, BusinessRole.PRATICIEN, "nom_mere"),
                "personne.praticien.nom_mere",
            ),
            fonction_dirigeant=_required_text(
                _role_field(dossier, BusinessRole.SIGNATAIRE, "fonction", BusinessRole.GERANT),
                "personne.signataire.fonction",
            ),
        ),
        signature=Signature(
            lieu=_required_text(_field(dossier, "signature.lieu"), "signature.lieu"),
            date=signature_date,
            nombre_exemplaires=_required_text(
                _field(dossier, "signature.nombre_exemplaires"),
                "signature.nombre_exemplaires",
            ),
        ),
        societe=Company(
            forme_sociale=forme_sociale,
            forme_sociale_affichage=forme_affichage,
            forme_sociale_libelle_long=forme_longue,
            denomination=_required_text(
                company.denomination
                or _field(dossier, "societe.societe_principale.denomination"),
                "societe.societe_principale.denomination",
            ),
            capital=_money_text(
                _required_text(
                    company.capital_social
                    or _field(dossier, "societe.societe_principale.capital_social"),
                    "societe.societe_principale.capital_social",
                )
            ),
            capital_social=_money_text(
                _required_text(
                    company.capital_social
                    or _field(dossier, "societe.societe_principale.capital_social"),
                    "societe.societe_principale.capital_social",
                )
            ),
            capital_variable=True,
            siege=company_address,
            ville_rcs=_required_text(
                company.rcs_ville or _field(dossier, "societe.societe_principale.rcs.ville"),
                "societe.societe_principale.rcs.ville",
            ),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=_required_text(
                _address_display(domiciliation_address),
                "domiciliation.adresse",
            )
        ),
        associes=[
            Associe(
                genre=_required_gender(
                    _role_field(dossier, BusinessRole.ASSOCIE, "genre", BusinessRole.PRATICIEN),
                    "personne.associe.genre",
                ),
                civilite_affichage=_required_text(
                    _role_field(
                        dossier,
                        BusinessRole.ASSOCIE,
                        "civilite_affichage",
                        BusinessRole.PRATICIEN,
                    ),
                    "personne.associe.civilite_affichage",
                ),
                prenom=_required_text(
                    _role_field(dossier, BusinessRole.ASSOCIE, "prenom", BusinessRole.PRATICIEN),
                    "personne.associe.prenom",
                ),
                nom=_required_text(
                    _role_field(dossier, BusinessRole.ASSOCIE, "nom", BusinessRole.PRATICIEN),
                    "personne.associe.nom",
                ),
                nb_parts=total_parts,
                est_present_ou_represente=True,
            )
        ],
        dirigeant_nomine=DirigeantNomine(
            genre=_required_gender(
                _role_field(dossier, BusinessRole.GERANT, "genre", BusinessRole.PRATICIEN),
                "personne.gerant.genre",
            ),
            civilite_affichage=_required_text(
                _role_field(
                    dossier,
                    BusinessRole.GERANT,
                    "civilite_affichage",
                    BusinessRole.PRATICIEN,
                ),
                "personne.gerant.civilite_affichage",
            ),
            prenom=_required_text(
                _role_field(dossier, BusinessRole.GERANT, "prenom", BusinessRole.PRATICIEN),
                "personne.gerant.prenom",
            ),
            nom=_required_text(
                _role_field(dossier, BusinessRole.GERANT, "nom", BusinessRole.PRATICIEN),
                "personne.gerant.nom",
            ),
            date_naissance=birth_date,
            ville_naissance=_required_text(
                _role_field(
                    dossier,
                    BusinessRole.GERANT,
                    "ville_naissance",
                    BusinessRole.PRATICIEN,
                ),
                "personne.gerant.ville_naissance",
            ),
            departement_naissance=_required_text(
                _role_field(
                    dossier,
                    BusinessRole.GERANT,
                    "departement_naissance",
                    BusinessRole.PRATICIEN,
                ),
                "personne.gerant.departement_naissance",
            ),
            nationalite=_required_text(
                _role_field(dossier, BusinessRole.GERANT, "nationalite", BusinessRole.PRATICIEN),
                "personne.gerant.nationalite",
            ),
            adresse_personnelle=person_address,
            fonction_affichage=_required_text(
                _role_field(dossier, BusinessRole.GERANT, "fonction", BusinessRole.PRATICIEN),
                "personne.gerant.fonction",
            ),
        ),
        decision=DecisionContext(
            date=_required_text(_field(dossier, "decision.date"), "decision.date")
        ),
        reunion=ReunionContext(
            date_lettres=_required_text(
                _field(dossier, "reunion.date_lettres"),
                "reunion.date_lettres",
            ),
            heure=_required_text(_field(dossier, "reunion.heure"), "reunion.heure"),
        ),
        capital=CapitalContext(
            nb_parts_total=total_parts,
            valeur_nominale_part=_money_text(
                _required_text(
                    _field(dossier, "capital.titres.valeur_nominale"),
                    "capital.titres.valeur_nominale",
                )
            ),
            nb_parts_representees=total_parts,
        ),
        emprunt=Emprunt(actif=False),
        metadata={
            "front_generation_v1": "true",
            "front_generation_profile": FRONT_GENERATION_PROFILE_KEY,
        },
    )


def generate_front_docx(
    dossier: DossierRecord,
    output_dir: Path | None = None,
) -> FrontGenerationDocxResult:
    readiness = front_generation_readiness(dossier)
    if not readiness.can_generate_docx:
        raise FrontGenerationBlockedError(_generation_block_message(readiness))
    context = build_front_generation_context(dossier)
    active_output_dir = output_dir or build_output_dir(
        "nouveau_front_selarl_creation_simple.yaml",
        FRONT_GENERATION_ARTIFACTS_DIR,
    )
    docx_paths = generate_docx_files_for_document_codes(
        context,
        active_output_dir,
        readiness.generable_doc_codes,
    )
    return FrontGenerationDocxResult(
        readiness=readiness,
        context=context,
        output_dir=active_output_dir,
        docx_paths=tuple(docx_paths),
    )


def generate_front_zip(
    output_dir: Path,
    docx_paths: Iterable[Path],
    pdf_paths: Iterable[Path] = (),
) -> Path:
    paths = list(docx_paths)
    if not paths:
        raise FrontGenerationBlockedError("Aucun DOCX disponible pour creer le ZIP.")
    return generate_zip_file(output_dir, paths, list(pdf_paths))


def generate_front_pdf(output_dir: Path, docx_paths: Iterable[Path]) -> GeneratedPdfBatch:
    paths = list(docx_paths)
    if not paths:
        raise FrontGenerationBlockedError("Aucun DOCX disponible pour convertir en PDF.")
    return generate_pdf_files(paths, output_dir)


def _status_row(status: DocumentStatusRecord) -> dict[str, str]:
    return {
        "document": status.doc_code,
        "libelle": status.doc_label,
        "statut": status.status.value,
        "generation V1": (
            "oui"
            if status.status is DocumentStatus.GENERABLE
            and status.doc_code in FRONT_GENERATION_SUPPORTED_DOC_CODES
            else "non"
        ),
        "raisons": _labels(reason.message for reason in status.reasons),
    }


def _require_generation_profile(dossier: DossierRecord) -> None:
    profile = dossier.metadata.get("front_editor_profile")
    if profile != FRONT_GENERATION_PROFILE_KEY:
        raise FrontGenerationBlockedError(
            "Generation V1 limitee au profil SELARL creation simple."
        )
    if not dossier.metadata.get("front_data_entry_v1"):
        raise FrontGenerationBlockedError(
            "Generation V1 attend un DossierRecord alimente par la saisie V1."
        )


def _main_person(dossier: DossierRecord) -> PersonRecord:
    person = dossier.persons.get("person-praticien-principal")
    if person is not None:
        return person
    assignment = next(
        (
            role
            for role in dossier.roles_for(BusinessRole.SIGNATAIRE)
            if role.target_type is RoleTargetType.PERSON
        ),
        None,
    )
    if assignment and assignment.target_id in dossier.persons:
        return dossier.persons[assignment.target_id]
    raise FrontGenerationBlockedError("PersonRecord principal/signataire manquant.")


def _main_company(dossier: DossierRecord) -> CompanyRecord:
    company = dossier.companies.get(COMPANY_MAIN_ID)
    if company is not None:
        return company
    assignment = next(
        (
            role
            for role in dossier.roles_for(BusinessRole.SOCIETE_PRINCIPALE)
            if role.target_type is RoleTargetType.COMPANY
        ),
        None,
    )
    if assignment and assignment.target_id in dossier.companies:
        return dossier.companies[assignment.target_id]
    raise FrontGenerationBlockedError("CompanyRecord societe_principale manquant.")


def _required_address_record(
    dossier: DossierRecord,
    usage: AddressUsage,
    preferred_id: str,
) -> AddressRecord:
    address = dossier.addresses.get(preferred_id)
    if address is not None and address.has_value():
        return address
    address = next(
        (candidate for candidate in dossier.addresses_for_usage(usage) if candidate.has_value()),
        None,
    )
    if address is None:
        raise FrontGenerationBlockedError(f"Adresse typee manquante: {usage.value}.")
    return address


def _engine_address(address: AddressRecord, field_name: str) -> Address:
    if address.street_number and address.street_name and address.postal_code and address.city:
        return Address(
            num_voie=address.street_number.strip(),
            voie=address.street_name.strip(),
            cp=address.postal_code.strip(),
            ville=address.city.strip(),
        )
    display_value = _address_display(address)
    match = _ADDRESS_PATTERN.match(display_value)
    if match is None:
        raise FrontGenerationBlockedError(
            f"{field_name} doit etre structuree sous la forme '12 rue Exemple, 75001 Paris'."
        )
    return Address(
        num_voie=match.group("number").strip(),
        voie=match.group("street").strip().rstrip(","),
        cp=match.group("postal_code").strip(),
        ville=match.group("city").strip(),
    )


def _address_display(address: AddressRecord) -> str:
    if address.display_value and address.display_value.strip():
        return address.display_value.strip()
    parts = (
        address.street_number,
        address.street_name,
        address.postal_code,
        address.city,
    )
    return " ".join(part.strip() for part in parts if part and part.strip())


def _role_field(
    dossier: DossierRecord,
    role: BusinessRole,
    suffix: str,
    *fallback_roles: BusinessRole,
) -> str:
    for candidate in (role, *fallback_roles):
        value = _field(dossier, f"personne.{candidate.value}.{suffix}")
        if value:
            return value
    return ""


def _field(dossier: DossierRecord, field_path: str) -> str:
    value = dossier.canonical_values.get(field_path)
    if value is None or value.value in (None, ""):
        return ""
    return str(value.value).strip()


def _required_text(value: object, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise FrontGenerationBlockedError(f"Champ moteur manquant: {field_name}.")
    return str(value).strip()


def _required_gender(value: object, field_name: str) -> Gender:
    text = _required_text(value, field_name)
    try:
        return Gender(text)
    except ValueError as exc:
        raise FrontGenerationBlockedError(
            f"{field_name} doit valoir 'masculin' ou 'feminin'."
        ) from exc


def _required_date(value: object, field_name: str) -> date:
    text = _required_text(value, field_name)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise FrontGenerationBlockedError(
            f"{field_name} doit etre au format AAAA-MM-JJ."
        ) from exc


def _required_positive_int(value: object, field_name: str) -> int:
    text = _required_text(value, field_name)
    match = re.search(r"\d+", text.replace(" ", ""))
    if match is None:
        raise FrontGenerationBlockedError(f"{field_name} doit contenir un entier positif.")
    parsed = int(match.group(0))
    if parsed < 1:
        raise FrontGenerationBlockedError(f"{field_name} doit etre superieur a 0.")
    return parsed


def _money_text(value: str) -> str:
    return re.sub(r"\s*(?:euros?|eur)\s*$", "", value.strip(), flags=re.IGNORECASE)


def _forme_labels(forme_sociale: str) -> tuple[str, str]:
    return _FORME_LABELS.get(
        forme_sociale.upper(),
        (forme_sociale, forme_sociale.lower()),
    )


def _generation_block_message(readiness: FrontGenerationReadiness) -> str:
    blockers = [
        *(
            f"documents non generables: {', '.join(readiness.blocked_doc_codes)}"
            for _ in (0,)
            if readiness.blocked_doc_codes
        ),
        *readiness.runtime_blockers,
    ]
    return "; ".join(blockers) if blockers else "Generation V1 bloquee."


def _labels(values: Iterable[object]) -> str:
    labels = tuple(str(value) for value in values if value)
    return ", ".join(labels) if labels else "-"
