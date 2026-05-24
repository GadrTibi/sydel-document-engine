from __future__ import annotations

from dataclasses import dataclass

from sydel_doc_engine.front_data.models import (
    AddressUsage,
    BusinessRole,
    CanonicalFieldDefinition,
    CanonicalFieldValue,
    CanonicalRelationType,
    DocumentRequirementRecord,
    FieldFormKind,
    FrontObjectType,
    OperationType,
)

SENTINEL_SOURCE_CSV = "docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv"


@dataclass(frozen=True)
class LegacyAliasMapping:
    alias_path: str
    canonical_path: str
    relation_type: CanonicalRelationType
    form_kind: FieldFormKind
    notes: str = ""


def _field(
    field_path: str,
    front_object: FrontObjectType,
    *,
    relation_type: CanonicalRelationType = CanonicalRelationType.SAME_FIELD,
    role: BusinessRole | None = None,
    address_usage: AddressUsage | None = None,
    operation_type: OperationType | None = None,
    form_kind: FieldFormKind = FieldFormKind.BUSINESS,
    notes: str = "",
) -> CanonicalFieldDefinition:
    return CanonicalFieldDefinition(
        field_path=field_path,
        front_object=front_object,
        relation_type=relation_type,
        role=role,
        address_usage=address_usage,
        operation_type=operation_type,
        form_kind=form_kind,
        notes=notes,
    )


CANONICAL_FIELD_DEFINITIONS: dict[str, CanonicalFieldDefinition] = {
    "personne.{role}.*": _field(
        "personne.{role}.*",
        FrontObjectType.PERSON,
        notes="Generic role placeholder resolved by RoleAssignment; no default role.",
    ),
    "personne.{role}.civilite_affichage": _field(
        "personne.{role}.civilite_affichage",
        FrontObjectType.PERSON,
    ),
    "personne.{role}.prenom": _field("personne.{role}.prenom", FrontObjectType.PERSON),
    "personne.{role}.nom": _field("personne.{role}.nom", FrontObjectType.PERSON),
    "personne.{role}.profession": _field(
        "personne.{role}.profession",
        FrontObjectType.PERSON,
    ),
    "personne.{role}.adresse_personnelle": _field(
        "personne.{role}.adresse_personnelle",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
    ),
    "personne.{role}.adresse_personnelle.adresse_affichee": _field(
        "personne.{role}.adresse_personnelle.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
        form_kind=FieldFormKind.DISPLAY,
    ),
    "personne.{role}.adresse_personnelle.num_voie": _field(
        "personne.{role}.adresse_personnelle.num_voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
    ),
    "personne.{role}.adresse_personnelle.voie": _field(
        "personne.{role}.adresse_personnelle.voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
    ),
    "personne.{role}.adresse_personnelle.cp": _field(
        "personne.{role}.adresse_personnelle.cp",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
    ),
    "personne.{role}.adresse_personnelle.ville": _field(
        "personne.{role}.adresse_personnelle.ville",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
    ),
    "personne.{role}.adresse_personnelle.pays": _field(
        "personne.{role}.adresse_personnelle.pays",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ADRESSE_PERSONNELLE,
    ),
    "personne.praticien.adresse_domicile": _field(
        "personne.praticien.adresse_domicile",
        FrontObjectType.ADDRESS,
        role=BusinessRole.PRATICIEN,
        address_usage=AddressUsage.DOMICILE_PRATICIEN,
        notes="Domicile pivot du praticien, distinct du siege et du cabinet.",
    ),
    "personne.{role}.numero_ordre": _field(
        "personne.{role}.numero_ordre",
        FrontObjectType.PERSON,
    ),
    "personne.{role}.numero_rpps": _field(
        "personne.{role}.numero_rpps",
        FrontObjectType.PERSON,
    ),
    "personne.mandataire.*": _field(
        "personne.mandataire.*",
        FrontObjectType.PERSON,
        role=BusinessRole.MANDATAIRE,
    ),
    "societe.{role}.*": _field(
        "societe.{role}.*",
        FrontObjectType.COMPANY,
        notes="Generic company role placeholder; never defaults to societe_principale.",
    ),
    "societe.{role}.denomination": _field(
        "societe.{role}.denomination",
        FrontObjectType.COMPANY,
    ),
    "societe.{role}.capital_social": _field(
        "societe.{role}.capital_social",
        FrontObjectType.COMPANY,
    ),
    "societe.{role}.siege.adresse": _field(
        "societe.{role}.siege.adresse",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.SIEGE_SOCIAL,
    ),
    "societe.{role}.siege.adresse_affichee": _field(
        "societe.{role}.siege.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        address_usage=AddressUsage.SIEGE_SOCIAL,
        form_kind=FieldFormKind.DISPLAY,
    ),
    "societe.{role}.siege.num_voie": _field(
        "societe.{role}.siege.num_voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.SIEGE_SOCIAL,
    ),
    "societe.{role}.siege.voie": _field(
        "societe.{role}.siege.voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.SIEGE_SOCIAL,
    ),
    "societe.{role}.siege.cp": _field(
        "societe.{role}.siege.cp",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.SIEGE_SOCIAL,
    ),
    "societe.{role}.siege.ville": _field(
        "societe.{role}.siege.ville",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.SIEGE_SOCIAL,
    ),
    "societe.{role}.siege.pays": _field(
        "societe.{role}.siege.pays",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.SIEGE_SOCIAL,
    ),
    "forme_sociale": _field("forme_sociale", FrontObjectType.COMPANY),
    "capital_social": _field("capital_social", FrontObjectType.COMPANY),
    "domiciliation.adresse": _field(
        "domiciliation.adresse",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        address_usage=AddressUsage.DOMICILIATION,
        notes="Can reuse siege_social only through an explicit ReuseRuleState.",
    ),
    "domiciliation.adresse_affichee": _field(
        "domiciliation.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        address_usage=AddressUsage.DOMICILIATION,
        form_kind=FieldFormKind.DISPLAY,
        notes="Displayed form derived from the registered-office address or overridden.",
    ),
    "domiciliation.adresse.num_voie": _field(
        "domiciliation.adresse.num_voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.DOMICILIATION,
    ),
    "domiciliation.adresse.voie": _field(
        "domiciliation.adresse.voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.DOMICILIATION,
    ),
    "domiciliation.adresse.cp": _field(
        "domiciliation.adresse.cp",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.DOMICILIATION,
    ),
    "domiciliation.adresse.ville": _field(
        "domiciliation.adresse.ville",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.DOMICILIATION,
    ),
    "domiciliation.adresse.pays": _field(
        "domiciliation.adresse.pays",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.DOMICILIATION,
    ),
    "exercice.lieu_principal.adresse": _field(
        "exercice.lieu_principal.adresse",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.LIEU_EXERCICE,
    ),
    "exercice.lieu_principal.adresse_affichee": _field(
        "exercice.lieu_principal.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        address_usage=AddressUsage.LIEU_EXERCICE,
        form_kind=FieldFormKind.DISPLAY,
    ),
    "exercice.lieu_principal.num_voie": _field(
        "exercice.lieu_principal.num_voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.LIEU_EXERCICE,
    ),
    "exercice.lieu_principal.voie": _field(
        "exercice.lieu_principal.voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.LIEU_EXERCICE,
    ),
    "exercice.lieu_principal.cp": _field(
        "exercice.lieu_principal.cp",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.LIEU_EXERCICE,
    ),
    "exercice.lieu_principal.ville": _field(
        "exercice.lieu_principal.ville",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.LIEU_EXERCICE,
    ),
    "exercice.lieu_principal.pays": _field(
        "exercice.lieu_principal.pays",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.LIEU_EXERCICE,
    ),
    "signature.*": _field("signature.*", FrontObjectType.DOSSIER),
    "signature.lieu": _field("signature.lieu", FrontObjectType.DOSSIER),
    "signature.date": _field("signature.date", FrontObjectType.DOSSIER),
    "ordre.professionnel": _field(
        "ordre.professionnel",
        FrontObjectType.COMPANY,
        role=BusinessRole.ORDRE_PROFESSIONNEL,
        operation_type=OperationType.ORDRE,
    ),
    "ordre.adresse": _field(
        "ordre.adresse",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
    ),
    "ordre.adresse_affichee": _field(
        "ordre.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
        form_kind=FieldFormKind.DISPLAY,
    ),
    "ordre.adresse.num_voie": _field(
        "ordre.adresse.num_voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
    ),
    "ordre.adresse.voie": _field(
        "ordre.adresse.voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
    ),
    "ordre.adresse.cp": _field(
        "ordre.adresse.cp",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
    ),
    "ordre.adresse.ville": _field(
        "ordre.adresse.ville",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
    ),
    "ordre.adresse.pays": _field(
        "ordre.adresse.pays",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.ORDRE,
        operation_type=OperationType.ORDRE,
    ),
    "dossier.options.derogation": _field(
        "dossier.options.derogation",
        FrontObjectType.DOSSIER,
        operation_type=OperationType.DEROGATION,
    ),
    "capital.titres.*": _field(
        "capital.titres.*",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CREATION,
    ),
    "capital.titres.nombre_total": _field(
        "capital.titres.nombre_total",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CREATION,
    ),
    "capital.titres.valeur_nominale": _field(
        "capital.titres.valeur_nominale",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CREATION,
    ),
    "capital.repartition_associes": _field(
        "capital.repartition_associes",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CREATION,
    ),
    "apport.numeraire.montant": _field(
        "apport.numeraire.montant",
        FrontObjectType.OPERATION,
        operation_type=OperationType.APPORT,
    ),
    "apport.nature.montant": _field(
        "apport.nature.montant",
        FrontObjectType.OPERATION,
        operation_type=OperationType.APPORT,
    ),
    "banque.{role}": _field(
        "banque.{role}",
        FrontObjectType.COMPANY,
        role=BusinessRole.BANQUE,
    ),
    "banque.{role}.adresse": _field(
        "banque.{role}.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.BANQUE,
        address_usage=AddressUsage.BANQUE,
    ),
    "banque.{role}.adresse_affichee": _field(
        "banque.{role}.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        role=BusinessRole.BANQUE,
        address_usage=AddressUsage.BANQUE,
        form_kind=FieldFormKind.DISPLAY,
    ),
    "cession.parts.nombre": _field(
        "cession.parts.nombre",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "cession.parts.plage": _field(
        "cession.parts.plage",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "cession.prix.*": _field(
        "cession.prix.*",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "cession.prix.total": _field(
        "cession.prix.total",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "cession.prix.unitaire": _field(
        "cession.prix.unitaire",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "cession.cabinet.adresse": _field(
        "cession.cabinet.adresse",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        address_usage=AddressUsage.CABINET_CEDE,
        operation_type=OperationType.CESSION,
    ),
    "cession.cabinet.adresse_affichee": _field(
        "cession.cabinet.adresse_affichee",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        address_usage=AddressUsage.CABINET_CEDE,
        operation_type=OperationType.CESSION,
        form_kind=FieldFormKind.DISPLAY,
    ),
    "cession.cabinet.num_voie": _field(
        "cession.cabinet.num_voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.CABINET_CEDE,
        operation_type=OperationType.CESSION,
    ),
    "cession.cabinet.voie": _field(
        "cession.cabinet.voie",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.CABINET_CEDE,
        operation_type=OperationType.CESSION,
    ),
    "cession.cabinet.cp": _field(
        "cession.cabinet.cp",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.CABINET_CEDE,
        operation_type=OperationType.CESSION,
    ),
    "cession.cabinet.ville": _field(
        "cession.cabinet.ville",
        FrontObjectType.ADDRESS,
        address_usage=AddressUsage.CABINET_CEDE,
        operation_type=OperationType.CESSION,
    ),
    "cession.cabinet.prix_composantes": _field(
        "cession.cabinet.prix_composantes",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "cession.vendeur.*": _field(
        "cession.vendeur.*",
        FrontObjectType.ROLE_ASSIGNMENT,
        role=BusinessRole.VENDEUR,
        operation_type=OperationType.CESSION,
    ),
    "cession.acquereur.*": _field(
        "cession.acquereur.*",
        FrontObjectType.ROLE_ASSIGNMENT,
        role=BusinessRole.ACQUEREUR,
        operation_type=OperationType.CESSION,
    ),
    "cession.financement.*": _field(
        "cession.financement.*",
        FrontObjectType.OPERATION,
        operation_type=OperationType.FINANCEMENT,
    ),
    "cession.exercices[]": _field(
        "cession.exercices[]",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION,
    ),
    "bail.parties": _field(
        "bail.parties",
        FrontObjectType.OPERATION,
        operation_type=OperationType.BAIL,
    ),
    "bail.bailleur.adresse": _field(
        "bail.bailleur.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.BAILLEUR,
        address_usage=AddressUsage.BAILLEUR,
        operation_type=OperationType.BAIL,
    ),
    "bail.locataire.adresse": _field(
        "bail.locataire.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.LOCATAIRE,
        address_usage=AddressUsage.LOCATAIRE,
        operation_type=OperationType.BAIL,
    ),
    "bail.locaux.adresse": _field(
        "bail.locaux.adresse",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        address_usage=AddressUsage.LOCAUX_LOUES,
        operation_type=OperationType.BAIL,
    ),
    "bail.dates": _field(
        "bail.dates",
        FrontObjectType.OPERATION,
        operation_type=OperationType.BAIL,
    ),
    "spfpl.operation.type": _field(
        "spfpl.operation.type",
        FrontObjectType.OPERATION,
        operation_type=OperationType.APPORT,
    ),
    "apport_titres.*": _field(
        "apport_titres.*",
        FrontObjectType.OPERATION,
        operation_type=OperationType.APPORT,
    ),
    "commissaire_aux_apports.{champ}": _field(
        "commissaire_aux_apports.{champ}",
        FrontObjectType.ROLE_ASSIGNMENT,
        role=BusinessRole.COMMISSAIRE_AUX_APPORTS,
    ),
    "societe_spfpl.*": _field(
        "societe_spfpl.*",
        FrontObjectType.COMPANY,
        role=BusinessRole.SPFPL_BENEFICIAIRE,
    ),
    "societe_spfpl.siege.adresse": _field(
        "societe_spfpl.siege.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.SPFPL_BENEFICIAIRE,
        address_usage=AddressUsage.SPFPL,
    ),
    "societe_cible.*": _field(
        "societe_cible.*",
        FrontObjectType.COMPANY,
        role=BusinessRole.SOCIETE_CIBLE,
    ),
    "societe_cible.siege.adresse": _field(
        "societe_cible.siege.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.SOCIETE_CIBLE,
        address_usage=AddressUsage.SOCIETE_CIBLE,
    ),
    "scm.adresse": _field(
        "scm.adresse",
        FrontObjectType.ADDRESS,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        role=BusinessRole.SCM,
        address_usage=AddressUsage.SCM,
        notes="Regle standard : reutilisation du lieu d'exercice seulement via trace.",
    ),
    "scm.siege.adresse": _field(
        "scm.siege.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.SCM,
        address_usage=AddressUsage.SCM,
    ),
    "scm_cession.scm_cedee.*": _field(
        "scm_cession.scm_cedee.*",
        FrontObjectType.COMPANY,
        role=BusinessRole.SCM_CEDEE,
        operation_type=OperationType.CESSION_PARTS_SCM,
    ),
    "scm_cession.scm_cedee.siege.adresse": _field(
        "scm_cession.scm_cedee.siege.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.SCM_CEDEE,
        address_usage=AddressUsage.SCM_CEDEE,
        operation_type=OperationType.CESSION_PARTS_SCM,
    ),
    "scm_cession.cessionnaire.siege.adresse": _field(
        "scm_cession.cessionnaire.siege.adresse",
        FrontObjectType.ADDRESS,
        role=BusinessRole.CESSIONNAIRE,
        address_usage=AddressUsage.CESSIONNAIRE_SCM,
        operation_type=OperationType.CESSION_PARTS_SCM,
        notes="Distinct de la SCM cedee par defaut, meme si les libelles sont proches.",
    ),
    "scm_cession.cedant.*": _field(
        "scm_cession.cedant.*",
        FrontObjectType.ROLE_ASSIGNMENT,
        role=BusinessRole.CEDANT,
        operation_type=OperationType.CESSION_PARTS_SCM,
    ),
    "scm_cession.{champ}": _field(
        "scm_cession.{champ}",
        FrontObjectType.OPERATION,
        operation_type=OperationType.CESSION_PARTS_SCM,
    ),
    "statuts_civils.associes[]": _field(
        "statuts_civils.associes[]",
        FrontObjectType.ROLE_ASSIGNMENT,
        role=BusinessRole.ASSOCIE,
    ),
}


LEGACY_ALIAS_MAPPINGS: dict[str, LegacyAliasMapping] = {
    "domiciliation.adresse_domiciliation_affichee": LegacyAliasMapping(
        alias_path="domiciliation.adresse_domiciliation_affichee",
        canonical_path="domiciliation.adresse",
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        form_kind=FieldFormKind.DOCUMENTARY_ALIAS,
        notes="Legacy document display form for DOC-002, not a competing business field.",
    ),
    "personne_2.nb_parts": LegacyAliasMapping(
        alias_path="personne_2.nb_parts",
        canonical_path="statuts_civils.associes[]",
        relation_type=CanonicalRelationType.SAME_DATA_DIFFERENT_SHAPE,
        form_kind=FieldFormKind.DOCUMENTARY_ALIAS,
        notes="Legacy SCM/statuts line shape; associate rows remain canonical.",
    ),
}


SENTINEL_DOCUMENT_REQUIREMENTS: dict[str, DocumentRequirementRecord] = {
    "DOC-002": DocumentRequirementRecord(
        doc_code="DOC-002",
        doc_label="Autorisation de domiciliation",
        required_roles=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.PRATICIEN,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_address_usages=(AddressUsage.DOMICILIATION, AddressUsage.SIEGE_SOCIAL),
        required_entities=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.PRATICIEN,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_canonical_fields=(
            "personne.{role}.civilite_affichage",
            "personne.{role}.prenom",
            "personne.{role}.nom",
            "societe.{role}.denomination",
            "societe.{role}.capital_social",
            "societe.{role}.siege.adresse",
            "domiciliation.adresse",
            "signature.lieu",
            "signature.date",
        ),
        target_screen_blocks=(
            "fiche_client",
            "fiche_societe",
            "adresses",
            "documents_attendus",
            "generation",
        ),
        possible_reuse_rules=("address:siege_social -> address:domiciliation",),
        unresolved_ambiguity_keys=("legacy_domiciliation_display_alias",),
        verdict="VERT",
        action_needed=(
            "Mapper le champ legacy vers une forme affichee/override documentaire."
        ),
    ),
    "DOC-034": DocumentRequirementRecord(
        doc_code="DOC-034",
        doc_label="Demande d'inscription a l'ordre",
        required_roles=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.SOCIETE_PRINCIPALE,
            BusinessRole.MANDATAIRE,
            BusinessRole.ORDRE_PROFESSIONNEL,
        ),
        required_address_usages=(AddressUsage.ADRESSE_PERSONNELLE, AddressUsage.ORDRE),
        required_entities=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.SOCIETE_PRINCIPALE,
            BusinessRole.MANDATAIRE,
            BusinessRole.ORDRE_PROFESSIONNEL,
        ),
        required_canonical_fields=(
            "personne.{role}.prenom",
            "personne.{role}.nom",
            "personne.{role}.profession",
            "personne.{role}.adresse_personnelle",
            "societe.{role}.denomination",
            "ordre.professionnel",
            "ordre.adresse",
            "personne.mandataire.*",
            "signature.lieu",
            "signature.date",
            "dossier.options.derogation",
        ),
        target_screen_blocks=(
            "fiche_client",
            "fiche_societe",
            "ordre_identifiants",
            "documents_attendus",
            "generation",
        ),
        unresolved_ambiguity_keys=(
            "ordre_model_per_inscrit",
            "mandataire_configurable",
            "derogation_manual_block",
        ),
        verdict="ORANGE",
        action_needed="Roles signataire/mandataire/ordre explicites, sans valeur magique.",
    ),
    "DOC-017": DocumentRequirementRecord(
        doc_code="DOC-017",
        doc_label="Statuts SELARL medecin",
        required_roles=(
            BusinessRole.ASSOCIE,
            BusinessRole.PRATICIEN,
            BusinessRole.GERANT,
            BusinessRole.SIGNATAIRE,
            BusinessRole.BANQUE,
            BusinessRole.ORDRE_PROFESSIONNEL,
        ),
        required_address_usages=(
            AddressUsage.SIEGE_SOCIAL,
            AddressUsage.ADRESSE_PERSONNELLE,
            AddressUsage.BANQUE,
        ),
        required_entities=(
            BusinessRole.SOCIETE_PRINCIPALE,
            BusinessRole.ASSOCIE,
            BusinessRole.GERANT,
            BusinessRole.BANQUE,
            BusinessRole.ORDRE_PROFESSIONNEL,
        ),
        required_canonical_fields=(
            "societe.{role}.denomination",
            "forme_sociale",
            "capital_social",
            "capital.titres.nombre_total",
            "capital.titres.valeur_nominale",
            "capital.repartition_associes",
            "personne.{role}.*",
            "personne.{role}.numero_ordre",
            "personne.{role}.numero_rpps",
            "banque.{role}",
            "signature.*",
        ),
        target_screen_blocks=(
            "fiche_client",
            "fiche_societe",
            "capital_associes",
            "ordre_identifiants",
            "generation",
        ),
        unresolved_ambiguity_keys=(
            "pluralite_associes_statuts_selarl",
            "seuils_gerance",
            "banque_depot_parametrage",
        ),
        verdict="ORANGE",
        action_needed="Structurer capital, repartition, banque et seuils sans deduction.",
    ),
    "DOC-033": DocumentRequirementRecord(
        doc_code="DOC-033",
        doc_label="Acte de cession des parts de la SCM vers SEL",
        required_roles=(
            BusinessRole.CEDANT,
            BusinessRole.CONJOINT,
            BusinessRole.CESSIONNAIRE,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
            BusinessRole.SCM_CEDEE,
            BusinessRole.SIGNATAIRE,
        ),
        required_address_usages=(
            AddressUsage.DOMICILE_CEDANT,
            AddressUsage.CESSIONNAIRE_SCM,
            AddressUsage.SCM_CEDEE,
        ),
        required_entities=(
            BusinessRole.CEDANT,
            BusinessRole.CESSIONNAIRE,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
            BusinessRole.SCM_CEDEE,
        ),
        required_canonical_fields=(
            "personne.{role}.*",
            "societe.cessionnaire.*",
            "scm_cession.scm_cedee.*",
            "scm_cession.cedant.*",
            "cession.parts.nombre",
            "cession.parts.plage",
            "cession.prix.total",
            "cession.prix.unitaire",
            "signature.*",
        ),
        target_screen_blocks=(
            "scm",
            "cession",
            "parties",
            "adresses",
            "generation",
        ),
        unresolved_ambiguity_keys=(
            "representant_cessionnaire_explicit",
            "credit_vendeur_conditionnel",
        ),
        verdict="VERT",
        action_needed="Encoder roles et adresses SCM comme distincts par defaut.",
    ),
    "DOC-009": DocumentRequirementRecord(
        doc_code="DOC-009",
        doc_label="Acte de cession d'un cabinet medical",
        required_roles=(
            BusinessRole.VENDEUR,
            BusinessRole.CONJOINT,
            BusinessRole.ACQUEREUR,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
            BusinessRole.BAILLEUR,
            BusinessRole.LOCATAIRE,
            BusinessRole.SIGNATAIRE,
        ),
        required_address_usages=(
            AddressUsage.DOMICILE_CEDANT,
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.CABINET_CEDE,
            AddressUsage.LOCAUX_LOUES,
            AddressUsage.SIEGE_SOCIAL,
            AddressUsage.BAILLEUR,
            AddressUsage.LOCATAIRE,
            AddressUsage.BANQUE,
        ),
        required_entities=(
            BusinessRole.VENDEUR,
            BusinessRole.ACQUEREUR,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
            BusinessRole.BAILLEUR,
            BusinessRole.LOCATAIRE,
        ),
        required_canonical_fields=(
            "cession.cabinet.adresse",
            "cession.cabinet.prix_composantes",
            "cession.vendeur.*",
            "cession.acquereur.*",
            "cession.financement.*",
            "cession.prix.*",
            "cession.exercices[]",
            "bail.parties",
            "bail.dates",
            "signature.*",
        ),
        target_screen_blocks=(
            "cession",
            "bail",
            "financement",
            "parties",
            "adresses",
            "documents_attendus",
            "generation",
        ),
        possible_reuse_rules=(
            "address:lieu_exercice -> address:cabinet_cede",
            "address:lieu_exercice -> address:locaux_loues",
        ),
        unresolved_ambiguity_keys=(
            "origine_propriete_libre",
            "exercices_financiers_collection",
            "bailleur_locataire_no_deduction",
        ),
        verdict="ORANGE",
        action_needed="Ajouter sous-blocs cession, bail, origine, prix, financement.",
    ),
    "DOC-041": DocumentRequirementRecord(
        doc_code="DOC-041",
        doc_label="Contrat d'apport SEL vers SPFPL",
        required_roles=(
            BusinessRole.APPORTEUR,
            BusinessRole.SPFPL_BENEFICIAIRE,
            BusinessRole.SOCIETE_CIBLE,
            BusinessRole.DIRIGEANT,
            BusinessRole.EVALUATEUR_APPORT,
            BusinessRole.COMMISSAIRE_AUX_APPORTS,
            BusinessRole.CONJOINT,
            BusinessRole.SIGNATAIRE,
        ),
        required_address_usages=(
            AddressUsage.DOMICILE_PRATICIEN,
            AddressUsage.SPFPL,
            AddressUsage.SOCIETE_CIBLE,
        ),
        required_entities=(
            BusinessRole.APPORTEUR,
            BusinessRole.SPFPL_BENEFICIAIRE,
            BusinessRole.SOCIETE_CIBLE,
            BusinessRole.EVALUATEUR_APPORT,
            BusinessRole.COMMISSAIRE_AUX_APPORTS,
        ),
        required_canonical_fields=(
            "spfpl.operation.type",
            "apport_titres.*",
            "commissaire_aux_apports.{champ}",
            "societe_spfpl.*",
            "societe_cible.*",
            "personne.{role}.*",
            "capital.titres.*",
            "signature.*",
        ),
        target_screen_blocks=(
            "spfpl",
            "capital_titres_apports",
            "fiche_societe",
            "fiche_client",
            "generation",
        ),
        unresolved_ambiguity_keys=(
            "evaluateur_commissaire_fixed_source",
            "commissaire_label_confirm",
            "spfpl_uncertain_fields",
        ),
        verdict="ORANGE",
        action_needed="Modeliser apport_titres, societe_cible, evaluateur et commissaire.",
    ),
    "DOC-025": DocumentRequirementRecord(
        doc_code="DOC-025",
        doc_label="Statuts SCM",
        required_roles=(
            BusinessRole.SCM,
            BusinessRole.ASSOCIE,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
            BusinessRole.SIGNATAIRE,
            BusinessRole.BANQUE,
        ),
        required_address_usages=(
            AddressUsage.SCM,
            AddressUsage.ADRESSE_PERSONNELLE,
            AddressUsage.SIEGE_SOCIAL,
            AddressUsage.BANQUE,
        ),
        required_entities=(
            BusinessRole.SCM,
            BusinessRole.ASSOCIE,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
            BusinessRole.BANQUE,
        ),
        required_canonical_fields=(
            "statuts_civils.associes[]",
            "societe.{role}.*",
            "capital.titres.nombre_total",
            "capital.titres.valeur_nominale",
            "capital.repartition_associes",
            "apport.numeraire.montant",
            "banque.{role}",
            "signature.*",
        ),
        target_screen_blocks=(
            "scm",
            "fiche_societe",
            "capital_associes",
            "adresses",
            "generation",
        ),
        unresolved_ambiguity_keys=(
            "legacy_nb_parts_personne_2",
            "associes_scm_one_to_six",
            "apports_parts_per_associe",
        ),
        verdict="ORANGE",
        action_needed="Definir associes[] SCM avec parts et apports par ligne.",
    ),
}


def canonical_definition(field_path: str) -> CanonicalFieldDefinition | None:
    exact = CANONICAL_FIELD_DEFINITIONS.get(field_path)
    if exact:
        return exact

    for registered_path, definition in CANONICAL_FIELD_DEFINITIONS.items():
        if registered_path.endswith(".*") and field_path.startswith(registered_path[:-1]):
            return definition
        if registered_path.endswith("[]") and field_path.startswith(registered_path):
            return definition
        if "{role}" in registered_path:
            prefix, _, suffix = registered_path.partition("{role}")
            if field_path.startswith(prefix) and field_path.endswith(suffix):
                return definition

    return None


def canonicalize_legacy_alias(alias_path: str, value: object) -> CanonicalFieldValue:
    mapping = LEGACY_ALIAS_MAPPINGS[alias_path]
    return CanonicalFieldValue(
        field_path=mapping.canonical_path,
        value=value,
        relation_type=mapping.relation_type,
        form_kind=mapping.form_kind,
        source_field_path=mapping.alias_path,
        source_aliases=(mapping.alias_path,),
    )


def sentinel_requirement(doc_code: str) -> DocumentRequirementRecord:
    return SENTINEL_DOCUMENT_REQUIREMENTS[doc_code]


def all_sentinel_requirements() -> tuple[DocumentRequirementRecord, ...]:
    return tuple(SENTINEL_DOCUMENT_REQUIREMENTS.values())
