from __future__ import annotations

from dataclasses import dataclass

from sydel_doc_engine.front_data.dossier_flow import DossierFlow, build_dossier_flow
from sydel_doc_engine.front_data.models import (
    AddressUsage,
    BusinessRole,
    DocumentRequirementRecord,
    DocumentRequirementStatus,
    DossierRecord,
)

SELAS_FRONT_SCHEMA_TICKET = "SELAS-FRONT-SCHEMA-001"
SELAS_STRUCTURE = "SELAS"
SELAS_FRONT_SCHEMA_SCOPE = "SELAS medecin, actionnaire unique, president unique"
SELAS_FRONT_SCHEMA_GENERATION_ENABLED = False
SELAS_ACTIVE_PROFESSIONS = ("medecin",)

SELAS_DECISION_PRESIDENT_CODE = "SELAS-DECISION-PRESIDENT"
SELAS_STATUTS_DENTISTE_CODE = "SELAS-STATUTS-DENTISTE"
SELAS_ATTESTATION_CAPITAL_CODE = "SELAS-ATTESTATION-CAPITAL"

SELAS_READY_DOCUMENT_CODES = ("DOC-001", "DOC-002", "DOC-003", "DOC-034", "DOC-018")
SELAS_CONDITIONAL_DOCUMENT_CODES = ("DOC-005", "DOC-006")
SELAS_RESERVED_DOCUMENT_CODES = (
    SELAS_DECISION_PRESIDENT_CODE,
    SELAS_STATUTS_DENTISTE_CODE,
    SELAS_ATTESTATION_CAPITAL_CODE,
)


@dataclass(frozen=True)
class SelasBlockedCase:
    key: str
    label: str
    reason: str


@dataclass(frozen=True)
class SelasPackReadiness:
    generation_enabled: bool
    ready_document_codes: tuple[str, ...]
    conditional_document_codes: tuple[str, ...]
    active_conditional_document_codes: tuple[str, ...]
    reserved_document_codes: tuple[str, ...]
    blocked_case_keys: tuple[str, ...]
    next_ticket: str

    @property
    def active_pack_document_codes(self) -> tuple[str, ...]:
        return (*self.ready_document_codes, *self.active_conditional_document_codes)


@dataclass(frozen=True)
class SelasFrontSchema:
    structure: str
    label: str
    active_professions: tuple[str, ...]
    generation_enabled: bool
    candidate_document_requirements: tuple[DocumentRequirementRecord, ...]
    reserved_document_requirements: tuple[DocumentRequirementRecord, ...]
    blocked_cases: tuple[SelasBlockedCase, ...]
    pack_readiness: SelasPackReadiness
    flow: DossierFlow

    @property
    def candidate_document_codes(self) -> tuple[str, ...]:
        return tuple(
            requirement.doc_code
            for requirement in self.candidate_document_requirements
        )

    @property
    def reserved_document_codes(self) -> tuple[str, ...]:
        return tuple(
            requirement.doc_code
            for requirement in self.reserved_document_requirements
        )


def build_selas_front_schema(
    *,
    regime_communautaire: bool = False,
) -> SelasFrontSchema:
    dossier = build_selas_schema_dossier(
        regime_communautaire=regime_communautaire,
    )
    candidate_requirements = selas_candidate_document_requirements(
        regime_communautaire=regime_communautaire,
    )
    reserved_requirements = selas_reserved_document_requirements()
    blocked_cases = selas_blocked_cases()

    return SelasFrontSchema(
        structure=SELAS_STRUCTURE,
        label=SELAS_FRONT_SCHEMA_SCOPE,
        active_professions=SELAS_ACTIVE_PROFESSIONS,
        generation_enabled=SELAS_FRONT_SCHEMA_GENERATION_ENABLED,
        candidate_document_requirements=candidate_requirements,
        reserved_document_requirements=reserved_requirements,
        blocked_cases=blocked_cases,
        pack_readiness=selas_pack_readiness(
            regime_communautaire=regime_communautaire,
            blocked_cases=blocked_cases,
        ),
        flow=build_dossier_flow(dossier),
    )


def selas_pack_readiness(
    *,
    regime_communautaire: bool = False,
    blocked_cases: tuple[SelasBlockedCase, ...] | None = None,
) -> SelasPackReadiness:
    blocked = selas_blocked_cases() if blocked_cases is None else blocked_cases
    return SelasPackReadiness(
        generation_enabled=SELAS_FRONT_SCHEMA_GENERATION_ENABLED,
        ready_document_codes=SELAS_READY_DOCUMENT_CODES,
        conditional_document_codes=SELAS_CONDITIONAL_DOCUMENT_CODES,
        active_conditional_document_codes=(
            SELAS_CONDITIONAL_DOCUMENT_CODES if regime_communautaire else ()
        ),
        reserved_document_codes=SELAS_RESERVED_DOCUMENT_CODES,
        blocked_case_keys=tuple(case.key for case in blocked),
        next_ticket="SELAS-ORCHESTRATOR-PACK-001",
    )


def build_selas_schema_dossier(
    *,
    regime_communautaire: bool = False,
) -> DossierRecord:
    dossier = DossierRecord(
        id="selas-front-schema",
        label=SELAS_FRONT_SCHEMA_SCOPE,
        structure=SELAS_STRUCTURE,
        metadata={
            "generation_enabled": SELAS_FRONT_SCHEMA_GENERATION_ENABLED,
            "ticket": SELAS_FRONT_SCHEMA_TICKET,
            "scope": SELAS_FRONT_SCHEMA_SCOPE,
        },
    )

    for requirement in (
        *selas_candidate_document_requirements(
            regime_communautaire=regime_communautaire,
        ),
        *selas_reserved_document_requirements(),
    ):
        dossier.add_document_requirement(requirement)

    return dossier


def selas_candidate_document_requirements(
    *,
    regime_communautaire: bool = False,
) -> tuple[DocumentRequirementRecord, ...]:
    requirements = [
        _requirement(
            "DOC-001",
            "DNC president SELAS",
            roles=(BusinessRole.PRESIDENT, BusinessRole.SIGNATAIRE),
            addresses=(AddressUsage.ADRESSE_PERSONNELLE,),
            fields=(
                "personne.president.genre",
                "personne.president.civilite_affichage",
                "personne.president.prenom",
                "personne.president.nom",
                "personne.president.date_naissance",
                "personne.president.nationalite",
                "personne.president.nom_pere",
                "personne.president.nom_mere",
                "personne.president.adresse_personnelle",
                "signature.lieu",
                "signature.date",
            ),
            action_needed=(
                "Renseigner le president signataire, son adresse personnelle "
                "et sa filiation complete avant generation."
            ),
        ),
        _requirement(
            "DOC-002",
            "Attestation de domiciliation SELAS",
            roles=(
                BusinessRole.PRESIDENT,
                BusinessRole.SIGNATAIRE,
                BusinessRole.SOCIETE_PRINCIPALE,
            ),
            addresses=(AddressUsage.SIEGE_SOCIAL, AddressUsage.DOMICILIATION),
            fields=(
                "personne.president.genre",
                "personne.president.civilite_affichage",
                "personne.president.prenom",
                "personne.president.nom",
                "societe.societe_principale.denomination",
                "societe.societe_principale.capital_social",
                "societe.societe_principale.siege.adresse.num_voie",
                "societe.societe_principale.siege.adresse.voie",
                "societe.societe_principale.siege.adresse.cp",
                "societe.societe_principale.siege.adresse.ville",
                "signature.lieu",
                "signature.date",
            ),
            required_reuse_rules=("address:siege_social -> address:domiciliation",),
            reuse_rules=("address:siege_social -> address:domiciliation",),
            action_needed=(
                "Generer uniquement si le president signataire est renseigne "
                "et si la domiciliation reutilise explicitement le siege/cabinet."
            ),
        ),
        _requirement(
            "DOC-003",
            "Procuration president SELAS",
            roles=(
                BusinessRole.PRESIDENT,
                BusinessRole.SIGNATAIRE,
                BusinessRole.MANDATAIRE,
                BusinessRole.SOCIETE_PRINCIPALE,
            ),
            fields=(
                "personne.president.*",
                "personne.mandataire.*",
                "societe.societe_principale.denomination",
                "signature.*",
            ),
            action_needed=(
                "Document SELAS-safe pour President unique ; completer "
                "president, mandataire, societe et signature avant generation."
            ),
        ),
        _requirement(
            "DOC-034",
            "Demande d'inscription a l'ordre SELAS",
            roles=(
                BusinessRole.SIGNATAIRE,
                BusinessRole.MANDATAIRE,
                BusinessRole.SOCIETE_PRINCIPALE,
                BusinessRole.ORDRE_PROFESSIONNEL,
            ),
            addresses=(AddressUsage.ORDRE, AddressUsage.ADRESSE_PERSONNELLE),
            fields=(
                "personne.signataire.titre_affichage",
                "personne.signataire.prenom",
                "personne.signataire.nom",
                "personne.signataire.adresse_personnelle",
                "societe.societe_principale.denomination",
                "ordre.conseil_departemental_libelle",
                "ordre.destinataire_appel",
                "ordre.profession_signataire_affichee",
                "ordre.profession_ligne_destinataire",
                "ordre.profession_reglementee_pluriel",
                "ordre.adresse.ligne_1",
                "ordre.adresse.cp",
                "ordre.adresse.ville",
                "mandataire.civilite_affichage",
                "mandataire.prenom",
                "mandataire.nom",
                "mandataire.fonction",
                "mandataire.cabinet",
                "signature.lieu",
                "signature.date",
                "dossier.options.derogation",
            ),
            ambiguities=("selas_ordre_pieces_plans_devis",),
            action_needed=(
                "Renseigner signataire, societe, ordre, mandataire et signature ; "
                "les plans/devis restent des pieces attendues hors generation DOCX."
            ),
        ),
        _requirement(
            "DOC-018",
            "Statuts SELAS medecin",
            roles=(
                BusinessRole.PRATICIEN,
                BusinessRole.ACTIONNAIRE,
                BusinessRole.PRESIDENT,
                BusinessRole.SIGNATAIRE,
                BusinessRole.SOCIETE_PRINCIPALE,
                BusinessRole.BANQUE,
                BusinessRole.ORDRE_PROFESSIONNEL,
            ),
            addresses=(
                AddressUsage.ADRESSE_PERSONNELLE,
                AddressUsage.SIEGE_SOCIAL,
                AddressUsage.LIEU_EXERCICE,
                AddressUsage.BANQUE,
            ),
            fields=(
                "societe.societe_principale.denomination",
                "societe.societe_principale.forme_sociale",
                "societe.societe_principale.forme_sociale_complete",
                "societe.societe_principale.forme_sociale_abregee",
                "societe.societe_principale.capital_social",
                "societe.societe_principale.capital_social_lettres",
                "societe.societe_principale.duree",
                "societe.societe_principale.siege.adresse.num_voie",
                "societe.societe_principale.siege.adresse.voie",
                "societe.societe_principale.siege.adresse.cp",
                "societe.societe_principale.siege.adresse.ville",
                "personne.actionnaire.genre",
                "personne.actionnaire.civilite_affichage",
                "personne.actionnaire.prenom",
                "personne.actionnaire.nom",
                "personne.actionnaire.date_naissance",
                "personne.actionnaire.ville_naissance",
                "personne.actionnaire.departement_naissance",
                "personne.actionnaire.nationalite",
                "personne.actionnaire.adresse_personnelle",
                "personne.actionnaire.titre_professionnel",
                "personne.actionnaire.qualification_principale",
                "personne.actionnaire.qualite",
                "personne.president.genre",
                "personne.president.civilite_affichage",
                "personne.president.prenom",
                "personne.president.nom",
                "personne.president.fonction_affichage",
                "personne.president.duree_mandat",
                "capital.type_titre",
                "capital.actions.nombre_total",
                "capital.actions.nombre_total_lettres",
                "capital.actions.valeur_nominale",
                "capital.actions.valeur_nominale_lettres",
                "capital.actions.repartition_actionnaires",
                "apport.montant",
                "apport.montant_lettres",
                "banque_depot.nom",
                "banque_depot.adresse",
                "ordre.numero_rpps",
                "ordre.numero",
                "ordre.ville",
                "ordre.professionnel",
                "exercice.lieu_principal.adresse",
                "exercice.date_debut",
                "exercice.date_fin",
                "exercice.date_cloture_premier_exercice",
                "signature.lieu",
                "signature.date",
                "signature.prestataire_signature_electronique",
            ),
            action_needed=(
                "Document SELAS-safe pour le cas medecin actionnaire unique ; "
                "bloquer DG, multi-actionnaires, droits derogatoires et actions complexes."
            ),
        ),
    ]

    if regime_communautaire:
        requirements.extend(
            (
                _requirement(
                    "DOC-005",
                    "Renonciation conjoint - regime communautaire SELAS",
                    roles=(
                        BusinessRole.PRATICIEN,
                        BusinessRole.CONJOINT,
                        BusinessRole.SIGNATAIRE,
                        BusinessRole.SOCIETE_PRINCIPALE,
                    ),
                    addresses=(
                        AddressUsage.ADRESSE_PERSONNELLE,
                        AddressUsage.SIEGE_SOCIAL,
                    ),
                    fields=_regime_communautaire_fields(),
                    ambiguities=("selas_regime_communautaire_effect",),
                    status=DocumentRequirementStatus.CONTEXT_INCOMPLETE,
                    action_needed=(
                        "Generer uniquement si le praticien est marie sous "
                        "regime communautaire et si conjoint/apport/societe "
                        "sont complets."
                    ),
                ),
                _requirement(
                    "DOC-006",
                    "Avertissement conjoint - regime communautaire SELAS",
                    roles=(
                        BusinessRole.PRATICIEN,
                        BusinessRole.CONJOINT,
                        BusinessRole.SIGNATAIRE,
                        BusinessRole.SOCIETE_PRINCIPALE,
                    ),
                    addresses=(
                        AddressUsage.ADRESSE_PERSONNELLE,
                        AddressUsage.SIEGE_SOCIAL,
                    ),
                    fields=_regime_communautaire_fields(),
                    ambiguities=("selas_regime_communautaire_effect",),
                    status=DocumentRequirementStatus.CONTEXT_INCOMPLETE,
                    action_needed=(
                        "Generer avec DOC-005 dans le batch regime communautaire ; "
                        "ne pas afficher en parcours simple."
                    ),
                ),
            )
        )

    return tuple(requirements)


def selas_reserved_document_requirements() -> tuple[DocumentRequirementRecord, ...]:
    return (
        _requirement(
            SELAS_DECISION_PRESIDENT_CODE,
            "Decision de nomination du president SELAS",
            roles=(
                BusinessRole.ACTIONNAIRE,
                BusinessRole.PRESIDENT,
                BusinessRole.SIGNATAIRE,
                BusinessRole.SOCIETE_PRINCIPALE,
            ),
            fields=(
                "personne.actionnaire.*",
                "personne.president.*",
                "societe.societe_principale.denomination",
                "signature.date",
                "signature.lieu",
            ),
            status=DocumentRequirementStatus.NOT_IMPLEMENTED,
            action_needed=(
                "Reserve : la nomination du President est absorbee par les statuts V1."
            ),
        ),
        _requirement(
            SELAS_STATUTS_DENTISTE_CODE,
            "Statuts SELAS dentiste",
            roles=(BusinessRole.ACTIONNAIRE, BusinessRole.PRESIDENT),
            status=DocumentRequirementStatus.NOT_IMPLEMENTED,
            action_needed="Reserve tant que la source statuts dentiste SELAS n'est pas analysee.",
        ),
        _requirement(
            SELAS_ATTESTATION_CAPITAL_CODE,
            "Attestation sur le capital SELAS",
            roles=(BusinessRole.BANQUE, BusinessRole.SOCIETE_PRINCIPALE),
            addresses=(AddressUsage.BANQUE,),
            fields=("capital.actions.nombre_total", "capital_social"),
            status=DocumentRequirementStatus.NOT_IMPLEMENTED,
            action_needed="A specifier avant automatisation de l'attestation capital.",
        ),
    )


def _regime_communautaire_fields() -> tuple[str, ...]:
    return (
        "dossier.options.regime_communautaire",
        "personne.apporteur.civilite_affichage",
        "personne.apporteur.prenom",
        "personne.apporteur.nom",
        "personne.apporteur.fonction_dirigeant",
        "personne.conjoint.civilite_affichage",
        "personne.conjoint.prenom",
        "personne.conjoint.nom",
        "personne.conjoint.adresse.num_voie",
        "personne.conjoint.adresse.voie",
        "personne.conjoint.adresse.cp",
        "personne.conjoint.adresse.ville",
        "societe.societe_principale.denomination",
        "societe.societe_principale.forme_sociale",
        "societe.societe_principale.forme_sociale_complete",
        "societe.societe_principale.forme_sociale_abregee",
        "societe.societe_principale.capital_social",
        "societe.societe_principale.siege.adresse.num_voie",
        "societe.societe_principale.siege.adresse.voie",
        "societe.societe_principale.siege.adresse.cp",
        "societe.societe_principale.siege.adresse.ville",
        "apport.montant",
        "apport.montant_lettres",
        "regime_communautaire.avertissement.date_signature",
        "regime_communautaire.renonciation.lieu_signature",
        "regime_communautaire.renonciation.date_signature",
        "regime_communautaire.date_courrier_avertissement",
        "regime_communautaire.regime_matrimonial",
        "regime_communautaire.qualite_renoncee",
        "regime_communautaire.renonciation.nombre_exemplaires_lettres",
    )


def selas_blocked_cases() -> tuple[SelasBlockedCase, ...]:
    return (
        SelasBlockedCase(
            key="chirurgien_dentiste",
            label="SELAS dentiste",
            reason="Source statuts dentiste SELAS non analysee dans ce ticket.",
        ),
        SelasBlockedCase(
            key="multi_actionnaires",
            label="Plusieurs actionnaires",
            reason="Pluriel, PV d'assemblee et droits de vote hors V1 schema.",
        ),
        SelasBlockedCase(
            key="directeur_general",
            label="Directeur general",
            reason="Non trouve dans les sources NotebookLM du sprint.",
        ),
        SelasBlockedCase(
            key="personne_morale_ou_micro_holding",
            label="Personne morale / micro-holding",
            reason="Reserve jusqu'a specification des roles representes.",
        ),
        SelasBlockedCase(
            key="actions_preference",
            label="Actions de preference",
            reason="Droits financiers/vote derogatoires hors V1.",
        ),
        SelasBlockedCase(
            key="cession_fonds",
            label="Cession de fonds liberal",
            reason="Brouillon Word humain requis ; redaction ultra personnalisee.",
        ),
        SelasBlockedCase(
            key="scm",
            label="SCM",
            reason="Automatisation API potentielle, mais hors premier ticket dev.",
        ),
        SelasBlockedCase(
            key="site_distinct_derogation",
            label="Site distinct / derogation",
            reason="Bloc conditionnel a garder visible mais non automatise ici.",
        ),
        SelasBlockedCase(
            key="numerotation_actions_complexe",
            label="Numerotation complexe des actions",
            reason="Demenbrement et droits derogatoires non specifiques en V1.",
        ),
    )


def _requirement(
    doc_code: str,
    doc_label: str,
    *,
    roles: tuple[BusinessRole, ...] = (),
    addresses: tuple[AddressUsage, ...] = (),
    fields: tuple[str, ...] = (),
    required_reuse_rules: tuple[str, ...] = (),
    reuse_rules: tuple[str, ...] = (),
    ambiguities: tuple[str, ...] = (),
    status: DocumentRequirementStatus = DocumentRequirementStatus.EXPECTED,
    action_needed: str = "",
) -> DocumentRequirementRecord:
    return DocumentRequirementRecord(
        doc_code=doc_code,
        doc_label=doc_label,
        required_roles=roles,
        required_address_usages=addresses,
        required_canonical_fields=fields,
        required_reuse_rules=required_reuse_rules,
        possible_reuse_rules=reuse_rules,
        unresolved_ambiguity_keys=ambiguities,
        verdict="ORANGE",
        action_needed=action_needed,
        status=status,
    )
