from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date
from typing import Final

from pydantic import ValidationError

from sydel_doc_engine.app.selarl_form_schema import (
    FormField,
    FormStep,
    NonAutomaticReuseRelation,
    ReuseRule,
    SelarlDocumentSpec,
    selarl_blocks,
    selarl_document_specs,
    selarl_fields,
    selarl_fields_by_block,
    selarl_flow_steps,
    selarl_non_automatic_reuse_relations,
    selarl_reuse_rules,
)
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
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import ALL_STRUCTURES, build_seed_catalog

BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS: Final[tuple[str, ...]] = (
    "DOC-001",
    "DOC-002",
    "DOC-003",
    "DOC-004",
)
PV_NOMINATION_STRUCTURES: Final[frozenset[str]] = frozenset(
    {"SELARL", "SELAS", "SPFPL cession", "SPFPL apport", "SCS", "SCI", "SCM"}
)

STATUS_GENERABLE: Final = "generable"
STATUS_BLOCKED_MISSING: Final = "blocked_missing_fields"
STATUS_CONTEXT_INCOMPLETE: Final = "context_incomplete_v2"
STATUS_MANUAL_ONLY: Final = "manual_only"
STATUS_NOT_IMPLEMENTED: Final = "not_implemented"
STATUS_NEEDS_MAPPING: Final = "needs_mapping"

STATUS_LABELS: Final[dict[str, str]] = {
    STATUS_GENERABLE: "Générable",
    STATUS_BLOCKED_MISSING: "Bloqué par champs manquants",
    STATUS_CONTEXT_INCOMPLETE: "Contexte incomplet pour génération V2",
    STATUS_MANUAL_ONLY: "À remplir manuellement",
    STATUS_NOT_IMPLEMENTED: "Non implémenté",
    STATUS_NEEDS_MAPPING: "Mapping à confirmer",
}

SELARL_ALWAYS_VISIBLE_BLOCK_KEYS: Final[tuple[str, ...]] = (
    "qualification",
    "professionnel_gerant",
    "ordre_professionnel",
    "societe",
    "siege_social",
    "associes",
    "mandataire_signataire",
    "signature",
)

PRODUCT_TREATED_CASE_TYPES: Final[frozenset[CaseType]] = frozenset(
    {CaseType.SELARL, CaseType.SELAS}
)
PRODUCT_GENERABLE_CASE_TYPES: Final[frozenset[CaseType]] = frozenset({CaseType.SELARL})


@dataclass(frozen=True)
class BusinessDossierType:
    structure: str
    label: str
    status: str
    generable_in_v1: bool


@dataclass(frozen=True)
class BusinessConditionSpec:
    key: str
    label: str
    kind: str
    required: bool = True
    choices: tuple[tuple[str, str], ...] = ()
    note: str | None = None


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
    structure: str = CaseType.SCI.value
    profession: str | None = None
    sci_iris: bool | None = None
    option_is: bool | None = None
    site_distinct: bool | None = None
    scm: bool | None = None
    scm_cession: bool | None = None
    regime_communautaire: bool | None = None
    derogation: bool | None = None
    cession: bool | None = None
    cabinet_type: str | None = None
    associe_unique: bool | None = None
    cession_actions: bool | None = None
    nombre_associes: int | None = None
    personne_genre: str = Gender.MASCULIN.value
    personne_civilite: str = ""
    personne_prenom: str = ""
    personne_nom: str = ""
    personne_date_naissance: date | str | None = None
    personne_ville_naissance: str = ""
    personne_ville_naissance_article_au: bool = False
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
    selarl_signataire_is_associe_1: bool = False
    selarl_dossier_unipersonnel: bool = False
    selarl_gerant_is_professional: bool = False
    selarl_signataire_is_professional: bool = False
    selarl_mandataire_is_signataire: bool = False
    selarl_company_is_acquirer: bool = False
    selarl_company_is_scm_transferee: bool = False
    selarl_domiciliation_is_registered_office: bool = False


@dataclass(frozen=True)
class BusinessDocumentRow:
    document_key: str
    document_code: str | None
    document_label: str
    status: str
    reasons: tuple[str, ...]
    notes: tuple[str, ...] = ()
    missing_fields: tuple[str, ...] = ()

    @property
    def doc_id(self) -> str:
        return self.document_code or self.document_key


@dataclass(frozen=True)
class BusinessWizardValidation:
    context: DocumentGenerationContext | None
    expected_documents: tuple[ExpectedDocument, ...]
    document_rows: tuple[BusinessDocumentRow, ...]
    missing_fields: tuple[str, ...]
    inconsistencies: tuple[str, ...]
    warnings: tuple[str, ...]
    can_generate_docx: bool

    @property
    def generable_count(self) -> int:
        return sum(1 for row in self.document_rows if row.status == STATUS_GENERABLE)

    @property
    def blocked_count(self) -> int:
        return sum(1 for row in self.document_rows if row.status != STATUS_GENERABLE)

    @property
    def generatable_document_codes(self) -> tuple[str, ...]:
        return tuple(
            row.document_code
            for row in self.document_rows
            if row.status == STATUS_GENERABLE and row.document_code is not None
        )


@dataclass(frozen=True)
class SelarlReuseProjection:
    active_rule_keys: tuple[str, ...]
    locked_targets: tuple[str, ...]
    non_automatic_relation_keys: tuple[str, ...]
    praticien_is_associe_unique: bool = False
    praticien_is_gerant: bool = False
    praticien_is_signataire: bool = False
    mandataire_is_signataire: bool = False


def business_dossier_types() -> tuple[BusinessDossierType, ...]:
    return tuple(
        BusinessDossierType(
            structure=case_type.value,
            label=_structure_label(case_type),
            status=_structure_status(case_type),
            generable_in_v1=case_type in PRODUCT_GENERABLE_CASE_TYPES,
        )
        for case_type in CaseType
    )


def get_ui_conditions_for_case(case_type: CaseType | str) -> tuple[BusinessConditionSpec, ...]:
    normalized_case_type = _normalize_case_type_value(case_type)
    if normalized_case_type == CaseType.SCI:
        return (
            BusinessConditionSpec(
                "sci_iris",
                "SCI simple ou SCI IRIS",
                "choice",
                choices=(("false", "SCI simple"), ("true", "SCI IRIS")),
            ),
            BusinessConditionSpec("option_is", "Option IS", "bool"),
        )
    if normalized_case_type == CaseType.SELARL:
        return selarl_ui_condition_specs()
    if normalized_case_type == CaseType.SELAS:
        return (
            BusinessConditionSpec(
                "profession",
                "Profession",
                "choice",
                choices=(("medecin", "medecin"),),
            ),
            BusinessConditionSpec("scm", "SCM", "bool"),
            BusinessConditionSpec("regime_communautaire", "Regime communautaire", "bool"),
            BusinessConditionSpec("derogation", "Derogation", "bool"),
            BusinessConditionSpec("cession", "Cession", "bool"),
            BusinessConditionSpec(
                "cabinet_type",
                "Type de cabinet si cession",
                "choice",
                required=False,
                choices=(
                    ("aucun", "aucun"),
                    ("medical", "cabinet medical"),
                    ("dentaire", "cabinet dentaire"),
                ),
                note="Reserve: le bloc SCM SELAS pointe vers DOC-031/DOC-032/DOC-033.",
            ),
        )
    if normalized_case_type == CaseType.SPFPL_CESSION:
        return (
            BusinessConditionSpec("regime_communautaire", "Regime communautaire", "bool"),
            BusinessConditionSpec("associe_unique", "Associe unique", "bool"),
            BusinessConditionSpec(
                "cession_actions",
                "Cession de parts ou cession d'actions",
                "choice",
                choices=(("false", "cession de parts"), ("true", "cession d'actions")),
            ),
        )
    if normalized_case_type == CaseType.SPFPL_APPORT:
        return (
            BusinessConditionSpec("regime_communautaire", "Regime communautaire", "bool"),
        )
    if normalized_case_type == CaseType.SAS:
        return (
            BusinessConditionSpec(
                "associe_unique",
                "Associe unique ou plusieurs associes",
                "bool",
                note=(
                    "Champ de vigilance UI V2 ; le catalogue CASE-CATALOG-001 "
                    "ne filtre pas SAS dessus."
                ),
            ),
        )
    return ()


def selarl_ui_condition_specs() -> tuple[BusinessConditionSpec, ...]:
    fields = _selarl_field_index()
    return (
        BusinessConditionSpec(
            "profession",
            fields["qualification.profession"].label,
            "choice",
            choices=(
                ("medecin", "medecin"),
                ("chirurgien_dentiste", "chirurgien-dentiste"),
            ),
            note=fields["qualification.profession"].help_text,
        ),
        BusinessConditionSpec(
            "site_distinct",
            fields["qualification.site_distinct"].label,
            "bool",
            note=fields["qualification.site_distinct"].help_text,
        ),
        BusinessConditionSpec(
            "scm_cession",
            fields["qualification.scm_cession"].label,
            "bool",
            note=fields["qualification.scm_cession"].help_text,
        ),
        BusinessConditionSpec(
            "regime_communautaire",
            fields["qualification.regime_communautaire"].label,
            "bool",
            note=fields["qualification.regime_communautaire"].help_text,
        ),
        BusinessConditionSpec(
            "derogation",
            fields["qualification.derogation"].label,
            "bool",
            note=fields["qualification.derogation"].help_text,
        ),
        BusinessConditionSpec(
            "cession",
            fields["qualification.cession"].label,
            "bool",
            note=fields["qualification.cession"].help_text,
        ),
        BusinessConditionSpec(
            "cabinet_type",
            fields["qualification.cabinet_type"].label,
            "choice",
            required=False,
            choices=(
                ("aucun", "aucun"),
                ("medical", "cabinet medical"),
                ("dentaire", "cabinet dentaire"),
            ),
            note=fields["qualification.cabinet_type"].help_text,
        ),
    )


def selarl_ui_block_visibility(data: BusinessWizardInput) -> dict[str, bool]:
    visibility = {
        block.key: block.key in SELARL_ALWAYS_VISIBLE_BLOCK_KEYS
        for block in selarl_blocks()
    }
    visibility["regime_conjoint"] = data.regime_communautaire is True
    visibility["scm"] = data.scm_cession is True
    visibility["cession_cabinet"] = data.cession is True
    visibility["bail"] = data.cession is True
    visibility["banque_financement"] = data.cession is True or data.emprunt_actif
    return visibility


def selarl_ui_visible_fields_by_block(
    data: BusinessWizardInput,
) -> dict[str, tuple[FormField, ...]]:
    visibility = selarl_ui_block_visibility(data)
    fields_by_block = selarl_fields_by_block()
    return {
        block_key: fields
        for block_key, fields in fields_by_block.items()
        if visibility.get(block_key, False)
    }


def selarl_ui_flow_steps() -> tuple[FormStep, ...]:
    return selarl_flow_steps()


def selarl_ui_visible_screen_title(step_key: str) -> str:
    for index, step in enumerate(selarl_ui_flow_steps(), start=1):
        if step.key == step_key:
            visible_label = "Fiche Client" if step.key == "fiche_client" else step.label
            return f"Écran {index} — {visible_label}"
    raise KeyError(f"Étape SELARL inconnue: {step_key}")


def selarl_ui_visible_screen_titles() -> tuple[str, ...]:
    return tuple(
        selarl_ui_visible_screen_title(step.key) for step in selarl_ui_flow_steps()
    )


def selarl_ui_visible_fields_by_step(
    data: BusinessWizardInput,
) -> dict[str, tuple[FormField, ...]]:
    fields_by_block = selarl_ui_visible_fields_by_block(data)
    return {
        step.key: tuple(
            field
            for block_key in step.block_keys
            for field in fields_by_block.get(block_key, ())
        )
        for step in selarl_flow_steps()
    }


def selarl_ui_reuse_projection(data: BusinessWizardInput) -> SelarlReuseProjection:
    active_rule_keys: list[str] = []
    locked_targets: list[str] = []

    if data.selarl_dossier_unipersonnel:
        active_rule_keys.append("dossier_unipersonnel")
        locked_targets.extend(
            (
                "associes.associe_unique",
                "dirigeant_nomine",
                "mandataire_signataire.signataire",
            )
        )
    else:
        if data.selarl_signataire_is_associe_1:
            active_rule_keys.append("signataire_is_associe_1")
            locked_targets.append("associes.associe_1")
        if data.selarl_gerant_is_professional:
            active_rule_keys.append("gerant_is_professional")
            locked_targets.append("dirigeant_nomine")
        if data.selarl_signataire_is_professional:
            active_rule_keys.append("signataire_is_professional")
            locked_targets.append("mandataire_signataire.signataire")

    if data.selarl_mandataire_is_signataire:
        active_rule_keys.append("mandataire_is_signataire")
        locked_targets.append("mandataire_signataire.mandataire")
    if data.selarl_company_is_acquirer:
        active_rule_keys.append("selarl_is_acquirer")
        locked_targets.append("cession_cabinet.acquereur")
    if data.selarl_company_is_scm_transferee:
        active_rule_keys.append("selarl_is_scm_transferee")
        locked_targets.append("scm.cessionnaire")
    if data.selarl_domiciliation_is_registered_office:
        active_rule_keys.append("domiciliation_is_registered_office")
        locked_targets.append("siege_social.domiciliation")

    return SelarlReuseProjection(
        active_rule_keys=tuple(dict.fromkeys(active_rule_keys)),
        locked_targets=tuple(dict.fromkeys(locked_targets)),
        non_automatic_relation_keys=tuple(
            relation.key for relation in selarl_non_automatic_reuse_relations()
        ),
        praticien_is_associe_unique=data.selarl_dossier_unipersonnel,
        praticien_is_gerant=(
            data.selarl_dossier_unipersonnel or data.selarl_gerant_is_professional
        ),
        praticien_is_signataire=(
            data.selarl_dossier_unipersonnel or data.selarl_signataire_is_professional
        ),
        mandataire_is_signataire=data.selarl_mandataire_is_signataire,
    )


def selarl_ui_field(key: str) -> FormField:
    return _selarl_field_index()[key]


def selarl_ui_reuse_rules() -> tuple[ReuseRule, ...]:
    return selarl_reuse_rules()


def selarl_ui_non_automatic_reuse_relations() -> tuple[NonAutomaticReuseRelation, ...]:
    return selarl_non_automatic_reuse_relations()


def selarl_ui_document_specs() -> tuple[SelarlDocumentSpec, ...]:
    return selarl_document_specs()


def selarl_ui_field_labels() -> tuple[str, ...]:
    return tuple(field.label for field in selarl_fields())


def selarl_ui_address_labels() -> tuple[str, ...]:
    return tuple(
        field.label for field in selarl_fields() if "adresse" in field.label.casefold()
    )


def _selarl_field_index() -> dict[str, FormField]:
    return {field.key: field for field in selarl_fields()}


def sample_business_wizard_input() -> BusinessWizardInput:
    return BusinessWizardInput(
        structure=CaseType.SCI.value,
        sci_iris=False,
        option_is=False,
        nombre_associes=2,
        personne_genre=Gender.MASCULIN.value,
        personne_civilite="Monsieur",
        personne_prenom="Jean",
        personne_nom="Durand",
        personne_date_naissance=date(1990, 2, 3),
        personne_ville_naissance="Paris",
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
    expected_documents = tuple(get_expected_documents(_case_input(data)))
    condition_missing_fields = _condition_missing_fields(data)
    missing_by_doc = _missing_fields_by_document(data, expected_documents)
    missing_fields = _unique(
        [
            *condition_missing_fields,
            *(
                field_name
                for fields in missing_by_doc.values()
                for field_name in fields
            ),
        ]
    )
    inconsistencies = _validate_inconsistencies(data, expected_documents)
    context = None

    if not missing_fields and not inconsistencies:
        try:
            context = build_business_context(data)
        except (ValueError, ValidationError) as exc:
            inconsistencies = (*inconsistencies, f"contexte moteur invalide: {exc}")

    document_rows = _document_rows(
        data,
        expected_documents,
        missing_by_doc,
        inconsistencies,
        context,
    )
    can_generate = context is not None and any(
        row.status == STATUS_GENERABLE for row in document_rows
    )
    return BusinessWizardValidation(
        context=context,
        expected_documents=expected_documents,
        document_rows=document_rows,
        missing_fields=missing_fields,
        inconsistencies=inconsistencies,
        warnings=_business_warnings(data, document_rows),
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
        structure=_runtime_structure(data),
        dossier_options=_build_dossier_options(data),
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
            ville_naissance=_required_text_value(
                data.personne_ville_naissance,
                "personne_signataire.ville_naissance",
            ),
            ville_naissance_article_au=data.personne_ville_naissance_article_au,
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
            "code document": row.document_code or "",
            "libelle document": row.document_label,
            "statut": STATUS_LABELS[row.status],
            "raison de presence": " ; ".join(row.reasons),
            "notes": " ; ".join([*row.notes, *row.missing_fields]),
        }
        for row in validation.document_rows
    ]


def _structure_label(case_type: CaseType) -> str:
    if case_type == CaseType.SELARL:
        return "SELARL - sprint produit actif"
    if case_type == CaseType.SELAS:
        return "SELAS - sprint produit actif (NO-GO dev)"
    return f"{case_type.value} - inventaire technique seulement"


def _structure_status(case_type: CaseType) -> str:
    if case_type == CaseType.SELARL:
        return (
            "SPRINT_ACTIF/PARTIAL : type en traitement avance ; generation produit "
            "bornee aux sous-cas SELARL valides."
        )
    if case_type == CaseType.SELAS:
        return (
            "SPRINT_ACTIF/BLOCKED sync/NO-GO dev : type en traitement Naomie ; "
            "aucune generation produit avant synchronisation et gates NotebookLM."
        )
    condition_count = len(get_ui_conditions_for_case(case_type))
    if condition_count:
        return (
            "INVENTAIRE_TECHNIQUE : present dans le catalogue/code, mais non traite "
            "comme sprint produit ; usage diagnostic seulement avec conditions catalogue."
        )
    return (
        "INVENTAIRE_TECHNIQUE : present dans le catalogue/code, mais non traite "
        "comme sprint produit ; usage diagnostic seulement avec selection catalogue directe."
    )


def _missing_fields_by_document(
    data: BusinessWizardInput,
    expected_documents: tuple[ExpectedDocument, ...],
) -> dict[str, tuple[str, ...]]:
    expected_codes = {
        document.document_code
        for document in expected_documents
        if document.document_code is not None
    }
    missing: dict[str, list[str]] = {
        doc_id: []
        for doc_id in BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS
        if doc_id in expected_codes
    }
    if "DOC-001" in missing:
        _validate_doc_001(data, missing["DOC-001"])
    if "DOC-002" in missing:
        _validate_doc_002(data, missing["DOC-002"])
    if "DOC-003" in missing:
        _validate_doc_003(data, missing["DOC-003"])
    if "DOC-004" in missing:
        _validate_doc_004(data, missing["DOC-004"])
    return {doc_id: tuple(fields) for doc_id, fields in missing.items()}


def _validate_doc_001(data: BusinessWizardInput, missing: list[str]) -> None:
    _require_gender(data.personne_genre, "personne_signataire.genre", missing)
    _require_text(data.personne_civilite, "personne_signataire.civilite", missing)
    _require_text(data.personne_prenom, "personne_signataire.prenom", missing)
    _require_text(data.personne_nom, "personne_signataire.nom", missing)
    _require_date(data.personne_date_naissance, "personne_signataire.date_naissance", missing)
    _require_text(data.personne_ville_naissance, "personne_signataire.ville_naissance", missing)
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


def _validate_inconsistencies(
    data: BusinessWizardInput,
    expected_documents: tuple[ExpectedDocument, ...],
) -> tuple[str, ...]:
    issues: list[str] = []
    if _runtime_structure(data) not in ALL_STRUCTURES:
        issues.append("structure inconnue du catalogue moteur")
    expected_codes = {
        document.document_code
        for document in expected_documents
        if document.document_code is not None
    }
    if "DOC-004" in expected_codes and not data.societe_capital_variable:
        issues.append("societe.capital_variable=false bloque DOC-004 en V1")
    if data.nombre_associes is not None and data.associes:
        if data.nombre_associes != len(data.associes):
            issues.append("nombre_associes doit correspondre aux cartes associes saisies")
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


def _business_warnings(
    data: BusinessWizardInput,
    document_rows: tuple[BusinessDocumentRow, ...],
) -> tuple[str, ...]:
    case_type = _normalize_case_type(data)
    warnings: list[str] = [
        "La generation ne vaut pas validation juridique ni revue visuelle humaine.",
        "La generation Assistant se limite aux documents attendus, generables, "
        "codes en DOC-XXX et prets avec le contexte formulaire V2.",
    ]
    if case_type not in PRODUCT_TREATED_CASE_TYPES:
        warnings.append(
            "Statut produit du type : INVENTAIRE_TECHNIQUE. Le type existe dans "
            "le catalogue/code, mais n'a pas ete traite comme sprint produit."
        )
    elif case_type not in PRODUCT_GENERABLE_CASE_TYPES:
        warnings.append(
            "Statut produit du type : SPRINT_ACTIF/NO-GO dev. Le type est en "
            "traitement, mais pas encore generable comme produit V1."
        )
    if any(row.status == STATUS_CONTEXT_INCOMPLETE for row in document_rows):
        warnings.append(
            "Certains documents sont attendus par le catalogue, mais le contexte "
            "formulaire est incomplet pour generation dans cette V2."
        )
    if any(row.status == STATUS_MANUAL_ONLY for row in document_rows):
        warnings.append("Les documents manuels restent visibles et exclus de la generation.")
    if any(row.status == STATUS_NOT_IMPLEMENTED for row in document_rows):
        warnings.append(
            "Les documents non implementes restent visibles et exclus de la generation."
        )
    if case_type == CaseType.SELAS and data.scm is True:
        warnings.append(
            "Reserve SELAS + SCM : la source contient des fichiers specifiques SELAS, "
            "mais le catalogue mappe le bloc SCM vers DOC-031/DOC-032/DOC-033."
        )
    if data.nombre_associes is not None:
        warnings.append(
            "Le nombre d'associes est collecte pour signaler les limites V2 ; "
            "il ne resout pas encore toutes les generations variables."
        )
    return tuple(warnings)


def _document_rows(
    data: BusinessWizardInput,
    expected_documents: tuple[ExpectedDocument, ...],
    missing_by_doc: dict[str, tuple[str, ...]],
    inconsistencies: tuple[str, ...],
    context: DocumentGenerationContext | None,
) -> tuple[BusinessDocumentRow, ...]:
    selected_ids = _selected_document_ids(context) if context is not None else ()
    rows: list[BusinessDocumentRow] = []
    for document in expected_documents:
        status = _row_status(document, missing_by_doc, inconsistencies, context, selected_ids)
        missing_fields = _row_missing_fields(document, status, missing_by_doc, inconsistencies)
        notes = _row_notes(data, document)
        rows.append(
            BusinessDocumentRow(
                document_key=document.document_key,
                document_code=document.document_code,
                document_label=document.document_label,
                status=status,
                reasons=document.reasons,
                notes=notes,
                missing_fields=missing_fields,
            )
        )
    return tuple(rows)


def _row_status(
    document: ExpectedDocument,
    missing_by_doc: dict[str, tuple[str, ...]],
    inconsistencies: tuple[str, ...],
    context: DocumentGenerationContext | None,
    selected_ids: tuple[str, ...],
) -> str:
    if document.availability == DocumentAvailability.MANUAL_ONLY:
        return STATUS_MANUAL_ONLY
    if document.availability == DocumentAvailability.NOT_IMPLEMENTED:
        return STATUS_NOT_IMPLEMENTED
    if (
        document.availability == DocumentAvailability.NEEDS_MAPPING
        or document.document_code is None
    ):
        return STATUS_NEEDS_MAPPING
    if document.document_code not in BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS:
        return STATUS_CONTEXT_INCOMPLETE
    if missing_by_doc.get(document.document_code) or inconsistencies:
        return STATUS_BLOCKED_MISSING
    if context is None:
        return STATUS_BLOCKED_MISSING
    if document.document_code not in selected_ids:
        return STATUS_CONTEXT_INCOMPLETE
    return STATUS_GENERABLE


def _row_missing_fields(
    document: ExpectedDocument,
    status: str,
    missing_by_doc: dict[str, tuple[str, ...]],
    inconsistencies: tuple[str, ...],
) -> tuple[str, ...]:
    if status == STATUS_MANUAL_ONLY:
        return ("exclu de la generation automatique: document a remplir a la main",)
    if status == STATUS_NOT_IMPLEMENTED:
        return ("exclu de la generation automatique: document non implemente",)
    if status == STATUS_NEEDS_MAPPING:
        return ("exclu de la generation automatique: mapping DOC-XXX a confirmer",)
    if status == STATUS_CONTEXT_INCOMPLETE:
        return ("document attendu, mais contexte incomplet pour generation dans cette V2",)
    if status == STATUS_BLOCKED_MISSING and document.document_code is not None:
        return (*missing_by_doc.get(document.document_code, ()), *inconsistencies)
    return ()


def _row_notes(data: BusinessWizardInput, document: ExpectedDocument) -> tuple[str, ...]:
    notes = list(document.notes)
    if (
        _normalize_case_type(data) == CaseType.SELAS
        and data.scm is True
        and document.document_code in {"DOC-031", "DOC-032", "DOC-033"}
    ):
        notes.append(
            "Reserve SELAS + SCM: variante SELAS a confirmer cote moteur avant generation."
        )
    return tuple(notes)


def _case_input(data: BusinessWizardInput) -> CaseInput:
    return CaseInput(case_type=_normalize_case_type(data), conditions=_case_conditions(data))


def _case_conditions(data: BusinessWizardInput) -> dict[str, object]:
    case_type = _normalize_case_type(data)
    conditions: dict[str, object] = {}
    if case_type == CaseType.SCI:
        _set_condition(conditions, "sci_iris", data.sci_iris)
        _set_condition(conditions, "option_is", data.option_is)
    elif case_type == CaseType.SELARL:
        _set_condition(conditions, "profession", data.profession)
        _set_condition(conditions, "site_distinct", data.site_distinct)
        _set_condition(conditions, "scm_cession", data.scm_cession)
        _set_condition(conditions, "regime_communautaire", data.regime_communautaire)
        _set_condition(conditions, "derogation", data.derogation)
        _set_condition(conditions, "cession", data.cession)
        _set_condition(
            conditions,
            "dossier_unipersonnel",
            data.selarl_dossier_unipersonnel,
        )
        if data.cession is True and data.cabinet_type not in {None, "aucun"}:
            _set_condition(conditions, "cabinet_type", data.cabinet_type)
    elif case_type == CaseType.SELAS:
        _set_condition(conditions, "profession", data.profession)
        _set_condition(conditions, "scm", data.scm)
        _set_condition(conditions, "regime_communautaire", data.regime_communautaire)
        _set_condition(conditions, "derogation", data.derogation)
        _set_condition(conditions, "cession", data.cession)
        if data.cession is True and data.cabinet_type not in {None, "aucun"}:
            _set_condition(conditions, "cabinet_type", data.cabinet_type)
    elif case_type == CaseType.SPFPL_CESSION:
        _set_condition(conditions, "regime_communautaire", data.regime_communautaire)
        _set_condition(conditions, "associe_unique", data.associe_unique)
        _set_condition(conditions, "cession_actions", data.cession_actions)
    elif case_type == CaseType.SPFPL_APPORT:
        _set_condition(conditions, "regime_communautaire", data.regime_communautaire)
    elif case_type == CaseType.SAS:
        _set_condition(conditions, "associe_unique", data.associe_unique)
    return conditions


def _condition_missing_fields(data: BusinessWizardInput) -> tuple[str, ...]:
    case_type = _normalize_case_type(data)
    missing: list[str] = []
    for spec in get_ui_conditions_for_case(case_type):
        if not spec.required or spec.key == "cabinet_type":
            continue
        if _condition_value(data, spec.key) is None:
            missing.append(f"conditions.{spec.key}")
    if case_type in {CaseType.SELARL, CaseType.SELAS} and data.cession is True:
        if data.cabinet_type is None:
            missing.append("conditions.cabinet_type")
    return tuple(missing)


def _condition_value(data: BusinessWizardInput, key: str) -> object | None:
    return getattr(data, key)


def _set_condition(conditions: dict[str, object], key: str, value: object | None) -> None:
    if value is not None:
        conditions[key] = value


def _normalize_case_type(data: BusinessWizardInput) -> CaseType:
    return _normalize_case_type_value(data.structure)


def _normalize_case_type_value(case_type: CaseType | str) -> CaseType:
    if isinstance(case_type, CaseType):
        return case_type
    if case_type == "SCI IRIS":
        return CaseType.SCI
    return CaseType(str(case_type))


def _runtime_structure(data: BusinessWizardInput) -> str:
    case_type = _normalize_case_type(data)
    if case_type == CaseType.SCI and data.sci_iris is True:
        return "SCI IRIS"
    return case_type.value


def _build_dossier_options(data: BusinessWizardInput) -> DossierOptions:
    case_type = _normalize_case_type(data)
    return DossierOptions(
        derogation=_bool_value(data.derogation),
        site_distinct=_bool_value(data.site_distinct),
        regime_communautaire=_bool_value(data.regime_communautaire),
        cession=_bool_value(data.cession) or case_type == CaseType.SPFPL_CESSION,
        apport=case_type == CaseType.SPFPL_APPORT,
        associe_unique=_bool_value(data.associe_unique)
        or (case_type == CaseType.SELARL and data.selarl_dossier_unipersonnel),
        option_is=_bool_value(data.option_is),
        scm_cession=_bool_value(data.scm_cession) or _bool_value(data.scm),
    )


def _bool_value(value: bool | None) -> bool:
    return bool(value)


def _selected_document_ids(ctx: DocumentGenerationContext | None) -> tuple[str, ...]:
    if ctx is None:
        return ()
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    return tuple(document.doc_id for document in orchestrator.select_documents_for_context(ctx))


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
