from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any
from unicodedata import combining, normalize


class CaseType(StrEnum):
    SELARL = "SELARL"
    SELAS = "SELAS"
    SPFPL_CESSION = "SPFPL cession"
    SPFPL_APPORT = "SPFPL apport"
    SCS = "SCS"
    SCI = "SCI"
    SCM = "SCM"
    SAS = "SAS"


class DocumentAvailability(StrEnum):
    GENERATABLE = "GENERATABLE"
    MANUAL_ONLY = "MANUAL_ONLY"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NEEDS_MAPPING = "NEEDS_MAPPING"


@dataclass(frozen=True)
class CaseCondition:
    key: str
    value: Any
    default: Any = False
    label: str | None = None


@dataclass(frozen=True)
class CaseInput:
    case_type: CaseType
    conditions: dict[str, Any]


@dataclass(frozen=True)
class CatalogDocument:
    document_key: str
    document_label: str
    source_template_filename: str | None
    document_code: str | None
    availability: DocumentAvailability
    notes: str | None = None


@dataclass(frozen=True)
class DocumentOccurrence:
    case_type: CaseType
    document_key: str
    reason: str
    conditions: tuple[CaseCondition, ...] = ()
    source_section: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class ExpectedDocument:
    case_type: CaseType
    document_key: str
    document_label: str
    source_template_filename: str | None
    document_code: str | None
    availability: DocumentAvailability
    reasons: tuple[str, ...]
    conditions: tuple[CaseCondition, ...]
    occurrence_count: int
    notes: tuple[str, ...]


SOURCE_TRUTH_PATH = "project/source_truth/Documents_a_generer_par_cas.docx"


def condition(key: str, value: Any = True, *, default: Any = False) -> CaseCondition:
    return CaseCondition(key=key, value=value, default=default)


CATALOG_DOCUMENTS: tuple[CatalogDocument, ...] = (
    CatalogDocument(
        "declaration_non_condamnation",
        "Declaration sur l'honneur de non-condamnation",
        "Declaration sur l'honneur de non condamnation.docx",
        "DOC-001",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "autorisation_domiciliation",
        "Autorisation de domiciliation",
        "Autorisation de domiciliation.docx",
        "DOC-002",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "procuration",
        "Procuration",
        "Procuration.docx",
        "DOC-003",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "pv_nomination_gerant",
        "PV nomination gerant",
        "PV nomination gerant.docx",
        "DOC-004",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "demande_inscription_ordre",
        "Demande d'inscription a l'ordre",
        "Demande d'inscription a l'ordre.docx",
        "DOC-034",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_selarl_chirurgien_dentiste",
        "Statuts SELARL chirurgien-dentiste",
        "Modele statuts SELARL chirurgien dentiste sans communaute.docx",
        "DOC-016",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_selarl_medecin",
        "Statuts SELARL medecin",
        "Modele statuts SELARL medecins.docx",
        "DOC-017",
        DocumentAvailability.GENERATABLE,
        "La source libelle la ligne 'Statuts dentiste' sous la condition medecin.",
    ),
    CatalogDocument(
        "site_distinct_cd94_sel",
        "Formulaire de declaration prealable de site distinct CD94 avec la SEL",
        "Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx",
        None,
        DocumentAvailability.MANUAL_ONLY,
        "La source indique explicitement 'A REMPLIR A LA MAIN'.",
    ),
    CatalogDocument(
        "pv_age_cession_parts_scm",
        "PV AGE cession part SCM",
        "PV AGE cession part SCM.docx",
        "DOC-031",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "courrier_sde_cession_scm",
        "Courrier SDE cession SCM",
        "Courrier SDE.docx",
        "DOC-032",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "acte_cession_parts_scm_sel",
        "Acte de cession des parts de la SCM vers SEL",
        "Acte de cession des parts de la SCM a la SELARL.docx",
        "DOC-033",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "lettre_renonciation_associe",
        "Lettre de renonciation a revendiquer la qualite d'associe",
        "Lettre de renonciation a revendiquer la qualite d'associe.docx",
        "DOC-005",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "lettre_avertissement_conjoint",
        "Lettre d'avertissement au conjoint en cas d'apport d'un bien commun",
        "Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.docx",
        "DOC-006",
        DocumentAvailability.GENERATABLE,
        (
            "Source DOCX Lot 2 disponible ; document a generer avec DOC-005 quand "
            "le regime communautaire est actif."
        ),
    ),
    CatalogDocument(
        "formulaire_derogation_sites_sel",
        "Formulaire de derogation pour exercer sur plusieurs sites avec la SEL",
        "Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx",
        "DOC-013",
        DocumentAvailability.MANUAL_ONLY,
        (
            "Source V2 SELARL: le document est mentionne, mais indique comme "
            "non fourni dans les sources de variables; hors generation pilote."
        ),
    ),
    CatalogDocument(
        "derogation_sel_bnc",
        "Derogation SEL BNC",
        None,
        None,
        DocumentAvailability.MANUAL_ONLY,
        "La source indique explicitement 'A REMPLIR A LA MAIN'.",
    ),
    CatalogDocument(
        "derogation_cumul_selarl_bnc",
        "Demande de derogation cumul SELARL BNC",
        "Demande de derogation cumul SELARL - BNC.docx",
        "DOC-014",
        DocumentAvailability.MANUAL_ONLY,
        "Source V2 SELARL: document indique comme a remplir a la main.",
    ),
    CatalogDocument(
        "avenant_contrat_bail",
        "Avenant contrat de bail",
        "Avenant Contrat de bail.docx",
        "DOC-007",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "appel_fonds_sel",
        "Appel de fonds SEL",
        "appel de fond sel.docx",
        "DOC-008",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "acte_cession_cabinet_medical",
        "Acte de cession d'un cabinet medical",
        "Acte de cession d_un cabinet medical.docx",
        "DOC-009",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "compromis_cession_cabinet_medical",
        "Compromis de cession d'un cabinet medical",
        "Compromis de cession d_un cabinet medical.docx",
        "DOC-010",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "acte_cession_cabinet_dentaire",
        "Acte de cession d'un cabinet dentaire",
        "Acte de cession d'un cabinet dentaire.docx",
        "DOC-011",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "compromis_cession_cabinet_dentaire",
        "Compromis de cession d'un cabinet dentaire",
        "Compromis de cession d_un cabinet dentaire.docx",
        "DOC-012",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_selas_medecin",
        "Statuts SELAS medecin",
        "Statuts_SELAS_medecin.docx",
        "DOC-018",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "derogation_cumul_selarl_salariee",
        "Demande de derogation cumul SELARL salariee",
        "Demande_derogation_cumul_SELARL_salariee.doc",
        None,
        DocumentAvailability.NOT_IMPLEMENTED,
        "Source legacy .doc non convertie en DOCX propre dans le moteur V1.",
    ),
    CatalogDocument(
        "statuts_spfpl_cession",
        "Statuts SPFPL dentiste cession",
        "Statuts_SPFPLAS_dentistes_cession.docx",
        "DOC-035",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "note_information_spfpl",
        "Note d'information SPFPL",
        "NOTE D'INFORMATION.docx",
        "DOC-037",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "pv_agrement_spfpl_plusieurs_associes",
        "PV SELARL agrement cession SPFPL - plusieurs associes",
        "PV SELARL agrement cession SPFPL - SELARL plusieurs associes - transforme.docx",
        "DOC-039",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "pv_agrement_spfpl_associe_unique",
        "PV SELARL agrement cession SPFPL - associe unique",
        "PV SELARL agrement cession SPFPL - SELARL 1 associe - transforme.docx",
        "DOC-038",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "acte_cession_parts_spfpl",
        "Acte de cession de parts SPFPL",
        "Acte_cession_SPFPL_tiers_part_modele.docx",
        "DOC-040",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "acte_cession_actions_spfpl",
        "Acte de cession d'actions SPFPL",
        "Acte_cession_SPFPL_tiers_modele.docx",
        "DOC-029",
        DocumentAvailability.GENERATABLE,
        "La ligne source ne donne pas le nom de fichier complet, le registre le precise.",
    ),
    CatalogDocument(
        "statuts_spfpl_apport",
        "Statuts SPFPL dentistes apport",
        "Statuts SPFPLAS dentistes - apport.docx",
        "DOC-036",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "contrat_apport_spfpl",
        "Contrat d'apport SEL vers SPFPL",
        "Contrat d_apport SEL SPFPL.docx",
        "DOC-041",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "attestation_capital_spfpl",
        "Attestation sur le capital / liste des souscripteurs SPFPL",
        "Attestation sur le capital - apport - liste des souscripteurs.docx",
        "DOC-042",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "attestation_commissaire_apports",
        "Attestation nomination commissaire aux apports",
        "attestation nomination commissaire aux apports - transforme.docx",
        "DOC-043",
        DocumentAvailability.GENERATABLE,
        "Le libelle source parle de comm. aux comptes mais le fichier vise les apports.",
    ),
    CatalogDocument(
        "statuts_scs",
        "Statuts SCS",
        "Statuts_SCS_modele.docx",
        "DOC-019",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_sci",
        "Statuts SCI",
        "Modele statuts SCI.docx",
        "DOC-020",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_sci_iris",
        "Statuts SCI IRIS",
        "Modele statuts SCI IRIS.docx",
        "DOC-021",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "lettre_option_is",
        "Lettre option IS",
        "lettre option IS.docx",
        "DOC-022",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_scm",
        "Statuts SCM",
        "Statuts SCM.docx",
        "DOC-025",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "pacte_associes_scm",
        "Pacte d'associes SCM",
        "Pacte d_associes SCM.docx",
        "DOC-026",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "liste_depenses_communes_scm",
        "Liste depenses communes SCM",
        "Liste depenses communes SCM.doc",
        "DOC-030",
        DocumentAvailability.GENERATABLE,
        "La source verite liste un .doc ; le registre moteur utilise la conversion DOCX.",
    ),
    CatalogDocument(
        "contrat_frais_communs_scm",
        "Contrat d'exercice professionnel a frais communs",
        "CONTRAT FRAIS COMMUNS.docx",
        "DOC-027",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "reglement_interieur_scm",
        "Reglement interieur de la SCM",
        "REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx",
        "DOC-028",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "statuts_sas",
        "Statuts SAS / SPFPL medecins",
        "STATUTS_SAS_SPFPL_medecins_modele.docx",
        "DOC-015",
        DocumentAvailability.GENERATABLE,
    ),
    CatalogDocument(
        "attestation_capital_sas",
        "Attestation sur le capital / liste des souscripteurs SAS",
        "Attestation sur le capital - apport - liste des souscripteurs.docx",
        "DOC-024",
        DocumentAvailability.GENERATABLE,
        "Meme source nominale que SPFPL apport, mais DOC canonique distinct.",
    ),
    CatalogDocument(
        "pv_remuneration_president",
        "PV remuneration president",
        "PV remuneration president - transforme.docx",
        "DOC-023",
        DocumentAvailability.GENERATABLE,
    ),
)

DOCUMENTS_BY_KEY = {document.document_key: document for document in CATALOG_DOCUMENTS}


CATALOG_OCCURRENCES: tuple[DocumentOccurrence, ...] = (
    # SELARL
    DocumentOccurrence(
        CaseType.SELARL, "declaration_non_condamnation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(
        CaseType.SELARL, "autorisation_domiciliation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(CaseType.SELARL, "procuration", "Docs a generer dans tous les cas"),
    DocumentOccurrence(CaseType.SELARL, "pv_nomination_gerant", "SELARL"),
    DocumentOccurrence(CaseType.SELARL, "demande_inscription_ordre", "SELARL"),
    DocumentOccurrence(CaseType.SELARL, "declaration_non_condamnation", "Rappel source SELARL"),
    DocumentOccurrence(CaseType.SELARL, "autorisation_domiciliation", "Rappel source SELARL"),
    DocumentOccurrence(
        CaseType.SELARL,
        "statuts_selarl_chirurgien_dentiste",
        "Si chirurgien-dentiste",
        (condition("profession", "chirurgien_dentiste"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "statuts_selarl_medecin",
        "Si medecin",
        (condition("profession", "medecin"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "site_distinct_cd94_sel",
        "Si site distinct",
        (condition("site_distinct"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "pv_age_cession_parts_scm",
        "Si SCM cession",
        (condition("scm_cession"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "courrier_sde_cession_scm",
        "Si SCM cession",
        (condition("scm_cession"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "acte_cession_parts_scm_sel",
        "Si SCM cession",
        (condition("scm_cession"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "lettre_renonciation_associe",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "lettre_avertissement_conjoint",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "formulaire_derogation_sites_sel",
        "Si derogation",
        (condition("derogation"),),
    ),
    DocumentOccurrence(
        CaseType.SELARL, "derogation_sel_bnc", "Si derogation", (condition("derogation"),)
    ),
    DocumentOccurrence(
        CaseType.SELARL, "derogation_cumul_selarl_bnc", "Si derogation", (condition("derogation"),)
    ),
    DocumentOccurrence(
        CaseType.SELARL, "avenant_contrat_bail", "Si cession", (condition("cession"),)
    ),
    DocumentOccurrence(CaseType.SELARL, "appel_fonds_sel", "Si cession", (condition("cession"),)),
    DocumentOccurrence(
        CaseType.SELARL,
        "acte_cession_cabinet_medical",
        "Si cession de cabinet medical",
        (condition("cession"), condition("cabinet_type", "medical")),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "compromis_cession_cabinet_medical",
        "Si cession de cabinet medical",
        (condition("cession"), condition("cabinet_type", "medical")),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "acte_cession_cabinet_dentaire",
        "Si cession de cabinet dentaire",
        (condition("cession"), condition("cabinet_type", "dentaire")),
    ),
    DocumentOccurrence(
        CaseType.SELARL,
        "compromis_cession_cabinet_dentaire",
        "Si cession de cabinet dentaire",
        (condition("cession"), condition("cabinet_type", "dentaire")),
    ),
    # SELAS
    DocumentOccurrence(
        CaseType.SELAS, "declaration_non_condamnation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(
        CaseType.SELAS, "autorisation_domiciliation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(CaseType.SELAS, "procuration", "Docs a generer dans tous les cas"),
    DocumentOccurrence(CaseType.SELAS, "pv_nomination_gerant", "SELAS"),
    DocumentOccurrence(CaseType.SELAS, "demande_inscription_ordre", "SELAS"),
    DocumentOccurrence(CaseType.SELAS, "declaration_non_condamnation", "Rappel source SELAS"),
    DocumentOccurrence(CaseType.SELAS, "autorisation_domiciliation", "Rappel source SELAS"),
    DocumentOccurrence(
        CaseType.SELAS,
        "statuts_selas_medecin",
        "Statuts medecin",
        (condition("profession", "medecin"),),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "lettre_renonciation_associe",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "lettre_avertissement_conjoint",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(CaseType.SELAS, "pv_age_cession_parts_scm", "Si SCM", (condition("scm"),)),
    DocumentOccurrence(CaseType.SELAS, "courrier_sde_cession_scm", "Si SCM", (condition("scm"),)),
    DocumentOccurrence(CaseType.SELAS, "acte_cession_parts_scm_sel", "Si SCM", (condition("scm"),)),
    DocumentOccurrence(
        CaseType.SELAS, "avenant_contrat_bail", "Si cession", (condition("cession"),)
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "acte_cession_cabinet_medical",
        "Si cession de cabinet medical",
        (condition("cession"), condition("cabinet_type", "medical")),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "compromis_cession_cabinet_medical",
        "Si cession de cabinet medical",
        (condition("cession"), condition("cabinet_type", "medical")),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "acte_cession_cabinet_dentaire",
        "Si cession de cabinet dentaire",
        (condition("cession"), condition("cabinet_type", "dentaire")),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "compromis_cession_cabinet_dentaire",
        "Si cession de cabinet dentaire",
        (condition("cession"), condition("cabinet_type", "dentaire")),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "formulaire_derogation_sites_sel",
        "Si derogation",
        (condition("derogation"),),
    ),
    DocumentOccurrence(
        CaseType.SELAS,
        "derogation_cumul_selarl_salariee",
        "Si derogation",
        (condition("derogation"),),
    ),
    # SPFPL cession
    DocumentOccurrence(
        CaseType.SPFPL_CESSION, "declaration_non_condamnation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION, "autorisation_domiciliation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(CaseType.SPFPL_CESSION, "procuration", "Docs a generer dans tous les cas"),
    DocumentOccurrence(CaseType.SPFPL_CESSION, "statuts_spfpl_cession", "Statuts"),
    DocumentOccurrence(CaseType.SPFPL_CESSION, "pv_nomination_gerant", "SPFPL cession"),
    DocumentOccurrence(CaseType.SPFPL_CESSION, "demande_inscription_ordre", "SPFPL cession"),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION, "declaration_non_condamnation", "Rappel source SPFPL cession"
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION, "autorisation_domiciliation", "Rappel source SPFPL cession"
    ),
    DocumentOccurrence(CaseType.SPFPL_CESSION, "note_information_spfpl", "SPFPL cession"),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION,
        "lettre_renonciation_associe",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION,
        "lettre_avertissement_conjoint",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION,
        "pv_agrement_spfpl_plusieurs_associes",
        "Si plusieurs associes",
        (condition("associe_unique", False),),
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION,
        "pv_agrement_spfpl_associe_unique",
        "Si associe unique",
        (condition("associe_unique"),),
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION,
        "acte_cession_parts_spfpl",
        "Acte de cession de parts",
        (condition("cession_actions", False),),
    ),
    DocumentOccurrence(
        CaseType.SPFPL_CESSION,
        "acte_cession_actions_spfpl",
        "Acte de cession d'actions",
        (condition("cession_actions"),),
    ),
    # SPFPL apport
    DocumentOccurrence(
        CaseType.SPFPL_APPORT, "declaration_non_condamnation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(
        CaseType.SPFPL_APPORT, "autorisation_domiciliation", "Docs a generer dans tous les cas"
    ),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "procuration", "Docs a generer dans tous les cas"),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "statuts_spfpl_apport", "Statuts"),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "pv_nomination_gerant", "SPFPL apport"),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "demande_inscription_ordre", "SPFPL apport"),
    DocumentOccurrence(
        CaseType.SPFPL_APPORT, "declaration_non_condamnation", "Rappel source SPFPL apport"
    ),
    DocumentOccurrence(
        CaseType.SPFPL_APPORT, "autorisation_domiciliation", "Rappel source SPFPL apport"
    ),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "note_information_spfpl", "SPFPL apport"),
    DocumentOccurrence(
        CaseType.SPFPL_APPORT,
        "lettre_renonciation_associe",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(
        CaseType.SPFPL_APPORT,
        "lettre_avertissement_conjoint",
        "Si regime communautaire",
        (condition("regime_communautaire"),),
    ),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "contrat_apport_spfpl", "Apport doc"),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "attestation_capital_spfpl", "Apport doc"),
    DocumentOccurrence(CaseType.SPFPL_APPORT, "attestation_commissaire_apports", "Apport doc"),
    # SCS
    DocumentOccurrence(CaseType.SCS, "statuts_scs", "SCS"),
    DocumentOccurrence(CaseType.SCS, "declaration_non_condamnation", "SCS"),
    DocumentOccurrence(CaseType.SCS, "autorisation_domiciliation", "SCS"),
    DocumentOccurrence(CaseType.SCS, "procuration", "SCS"),
    DocumentOccurrence(CaseType.SCS, "pv_nomination_gerant", "SCS"),
    # SCI
    DocumentOccurrence(CaseType.SCI, "statuts_sci", "Si SCI", (condition("sci_iris", False),)),
    DocumentOccurrence(CaseType.SCI, "statuts_sci_iris", "Si SCI IRIS", (condition("sci_iris"),)),
    DocumentOccurrence(CaseType.SCI, "lettre_option_is", "Si IS", (condition("option_is"),)),
    DocumentOccurrence(CaseType.SCI, "declaration_non_condamnation", "SCI"),
    DocumentOccurrence(CaseType.SCI, "procuration", "SCI"),
    DocumentOccurrence(CaseType.SCI, "autorisation_domiciliation", "SCI"),
    DocumentOccurrence(CaseType.SCI, "pv_nomination_gerant", "SCI"),
    # SCM
    DocumentOccurrence(CaseType.SCM, "statuts_scm", "SCM"),
    DocumentOccurrence(CaseType.SCM, "declaration_non_condamnation", "SCM"),
    DocumentOccurrence(CaseType.SCM, "autorisation_domiciliation", "SCM"),
    DocumentOccurrence(CaseType.SCM, "procuration", "SCM"),
    DocumentOccurrence(CaseType.SCM, "pv_nomination_gerant", "SCM"),
    DocumentOccurrence(CaseType.SCM, "demande_inscription_ordre", "SCM"),
    DocumentOccurrence(CaseType.SCM, "declaration_non_condamnation", "Rappel source SCM"),
    DocumentOccurrence(CaseType.SCM, "autorisation_domiciliation", "Rappel source SCM"),
    DocumentOccurrence(CaseType.SCM, "pacte_associes_scm", "SCM"),
    DocumentOccurrence(CaseType.SCM, "liste_depenses_communes_scm", "SCM"),
    DocumentOccurrence(CaseType.SCM, "contrat_frais_communs_scm", "SCM"),
    DocumentOccurrence(CaseType.SCM, "reglement_interieur_scm", "SCM"),
    # SAS
    DocumentOccurrence(CaseType.SAS, "statuts_sas", "SAS"),
    DocumentOccurrence(CaseType.SAS, "declaration_non_condamnation", "SAS"),
    DocumentOccurrence(CaseType.SAS, "autorisation_domiciliation", "SAS"),
    DocumentOccurrence(CaseType.SAS, "procuration", "SAS"),
    DocumentOccurrence(CaseType.SAS, "attestation_capital_sas", "SAS"),
    DocumentOccurrence(CaseType.SAS, "pv_remuneration_president", "SAS"),
    DocumentOccurrence(CaseType.SAS, "attestation_capital_sas", "Liste des souscripteurs"),
)


def get_expected_documents(case_input: CaseInput | dict[str, Any]) -> list[ExpectedDocument]:
    normalized_input = _normalize_case_input(case_input)
    selected_occurrences = [
        occurrence
        for occurrence in CATALOG_OCCURRENCES
        if occurrence.case_type == normalized_input.case_type
        and _occurrence_matches(occurrence, normalized_input.conditions)
    ]

    grouped: dict[str, list[DocumentOccurrence]] = {}
    for occurrence in selected_occurrences:
        grouped.setdefault(occurrence.document_key, []).append(occurrence)

    expected_documents: list[ExpectedDocument] = []
    for document_key, occurrences in grouped.items():
        document = DOCUMENTS_BY_KEY[document_key]
        notes = tuple(
            note
            for note in [document.notes, *(occurrence.notes for occurrence in occurrences)]
            if note
        )
        expected_documents.append(
            ExpectedDocument(
                case_type=normalized_input.case_type,
                document_key=document.document_key,
                document_label=document.document_label,
                source_template_filename=document.source_template_filename,
                document_code=document.document_code,
                availability=document.availability,
                reasons=tuple(occurrence.reason for occurrence in occurrences),
                conditions=_dedupe_conditions(occurrences),
                occurrence_count=len(occurrences),
                notes=notes,
            )
        )
    return expected_documents


def catalog_documents_by_availability(
    availability: DocumentAvailability,
) -> tuple[CatalogDocument, ...]:
    return tuple(
        document for document in CATALOG_DOCUMENTS if document.availability == availability
    )


def mapped_document_codes() -> tuple[str, ...]:
    return tuple(
        sorted(
            document.document_code
            for document in CATALOG_DOCUMENTS
            if document.document_code is not None
        )
    )


def _normalize_case_input(case_input: CaseInput | dict[str, Any]) -> CaseInput:
    if isinstance(case_input, CaseInput):
        return _normalize_case_input_dict(
            {"case_type": case_input.case_type, "conditions": case_input.conditions}
        )
    return _normalize_case_input_dict(case_input)


def _normalize_case_input_dict(case_input: dict[str, Any]) -> CaseInput:
    raw_case_type = (
        case_input.get("case_type") or case_input.get("type_dossier") or case_input.get("structure")
    )
    if raw_case_type is None:
        raise ValueError("case_type is required")

    conditions = dict(case_input.get("conditions") or {})
    for key, value in case_input.items():
        if key not in {"case_type", "type_dossier", "structure", "conditions"}:
            conditions[key] = value

    case_type_label = str(raw_case_type).strip()
    if _normalize_text(case_type_label) == "sci_iris":
        conditions["sci_iris"] = True
        case_type_label = CaseType.SCI.value

    try:
        case_type = CaseType(case_type_label)
    except ValueError as exc:
        raise ValueError(f"unknown case_type: {raw_case_type}") from exc

    return CaseInput(case_type=case_type, conditions=conditions)


def _occurrence_matches(
    occurrence: DocumentOccurrence,
    conditions: dict[str, Any],
) -> bool:
    return all(_condition_matches(condition, conditions) for condition in occurrence.conditions)


def _condition_matches(condition_: CaseCondition, conditions: dict[str, Any]) -> bool:
    actual = conditions.get(condition_.key, condition_.default)
    return _normalize_condition_value(actual) == _normalize_condition_value(condition_.value)


def _dedupe_conditions(occurrences: list[DocumentOccurrence]) -> tuple[CaseCondition, ...]:
    deduped: dict[tuple[str, str], CaseCondition] = {}
    for occurrence in occurrences:
        for condition_ in occurrence.conditions:
            key = (condition_.key, repr(_normalize_condition_value(condition_.value)))
            deduped.setdefault(key, condition_)
    return tuple(deduped.values())


def _normalize_condition_value(value: Any) -> Any:
    if isinstance(value, str):
        return _normalize_text(value)
    return value


def _normalize_text(value: str) -> str:
    without_accents = "".join(
        character for character in normalize("NFKD", value) if not combining(character)
    )
    normalized = without_accents.strip().lower()
    for character in ("-", " ", "'", "’", "/"):
        normalized = normalized.replace(character, "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized.strip("_")
