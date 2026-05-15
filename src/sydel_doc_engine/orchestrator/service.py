from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from sydel_doc_engine.domain.document import DocumentDefinition
from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.base import DocumentGenerator
from sydel_doc_engine.generators.lot_01.autorisation_domiciliation import (
    AutorisationDomiciliationGenerator,
)
from sydel_doc_engine.generators.lot_01.declaration_non_condamnation import (
    DeclarationNonCondamnationGenerator,
)
from sydel_doc_engine.generators.lot_01.procuration import ProcurationGenerator
from sydel_doc_engine.generators.lot_02.lettre_avertissement_conjoint import (
    LettreAvertissementConjointGenerator,
)
from sydel_doc_engine.generators.lot_02.lettre_renonciation_associe import (
    LettreRenonciationAssocieGenerator,
)
from sydel_doc_engine.generators.lot_02.pv_nomination_gerant import (
    PvNominationGerantGenerator,
)
from sydel_doc_engine.generators.lot_03.acte_cession_cabinet_dentaire import (
    ActeCessionCabinetDentaireGenerator,
)
from sydel_doc_engine.generators.lot_03.acte_cession_cabinet_medical import (
    ActeCessionCabinetMedicalGenerator,
)
from sydel_doc_engine.generators.lot_03.appel_fond_sel import AppelFondSelGenerator
from sydel_doc_engine.generators.lot_03.avenant_contrat_bail import (
    AvenantContratBailGenerator,
)
from sydel_doc_engine.generators.lot_03.compromis_cession_cabinet_dentaire import (
    CompromisCessionCabinetDentaireGenerator,
)
from sydel_doc_engine.generators.lot_03.compromis_cession_cabinet_medical import (
    CompromisCessionCabinetMedicalGenerator,
)
from sydel_doc_engine.generators.lot_03.demande_derogation_cumul_selarl_bnc import (
    DemandeDerogationCumulSelarlBncGenerator,
)
from sydel_doc_engine.generators.lot_03.formulaire_derogation_sites_sel import (
    FormulaireDerogationSitesSelGenerator,
)
from sydel_doc_engine.generators.lot_04.statuts_sas import StatutsSasGenerator
from sydel_doc_engine.generators.lot_04.statuts_sci import StatutsSciGenerator
from sydel_doc_engine.generators.lot_04.statuts_sci_iris import StatutsSciIrisGenerator
from sydel_doc_engine.generators.lot_04.statuts_scm import StatutsScmGenerator
from sydel_doc_engine.generators.lot_04.statuts_scs import StatutsScsGenerator
from sydel_doc_engine.generators.lot_04.statuts_selarl_dentiste import (
    StatutsSelarlDentisteGenerator,
)
from sydel_doc_engine.generators.lot_04.statuts_selarl_medecin import (
    StatutsSelarlMedecinGenerator,
)
from sydel_doc_engine.generators.lot_04.statuts_selas_medecin import (
    StatutsSelasMedecinGenerator,
)
from sydel_doc_engine.generators.lot_05.acte_cession_actions_spfpl import (
    ActeCessionActionsSpfplGenerator,
)
from sydel_doc_engine.generators.lot_05.acte_cession_parts_scm import (
    ActeCessionPartsScmGenerator,
)
from sydel_doc_engine.generators.lot_05.attestation_capital_liste_souscripteurs_sas import (
    AttestationCapitalListeSouscripteursSasGenerator,
)
from sydel_doc_engine.generators.lot_05.contrat_frais_communs import (
    ContratFraisCommunsGenerator,
)
from sydel_doc_engine.generators.lot_05.courrier_sde_cession_scm import (
    CourrierSdeCessionScmGenerator,
)
from sydel_doc_engine.generators.lot_05.lettre_option_is import LettreOptionIsGenerator
from sydel_doc_engine.generators.lot_05.liste_depenses_communes_scm import (
    ListeDepensesCommunesScmGenerator,
)
from sydel_doc_engine.generators.lot_05.pacte_associes_scm import PacteAssociesScmGenerator
from sydel_doc_engine.generators.lot_05.pv_age_cession_scm import (
    PvAgeCessionScmGenerator,
)
from sydel_doc_engine.generators.lot_05.pv_remuneration_president import (
    PvRemunerationPresidentGenerator,
)
from sydel_doc_engine.generators.lot_05.reglement_interieur_scm import (
    ReglementInterieurScmGenerator,
)

REGIME_COMMUNAUTAIRE_DOCUMENT_IDS = {"DOC-005", "DOC-006"}
BAIL_AVENANT_DOCUMENT_ID = "DOC-007"
APPEL_FONDS_DOCUMENT_ID = "DOC-008"
CESSION_CABINET_DOCUMENT_IDS = {
    "DOC-009": ("acte", "medical"),
    "DOC-010": ("compromis", "medical"),
    "DOC-011": ("acte", "dentaire"),
    "DOC-012": ("compromis", "dentaire"),
}
DEROGATION_DOCUMENT_TYPES = {
    "DOC-013": "multi_sites_sel",
    "DOC-014": "cumul_sel_bnc",
}
STATUTS_SAS_DOCUMENT_ID = "DOC-015"
STATUTS_SEL_DOCUMENTS = {
    "DOC-016": ("SELARL", "selarl_dentiste"),
    "DOC-017": ("SELARL", "selarl_medecin"),
    "DOC-018": ("SELAS", "selas_medecin"),
}
STATUTS_CIVILS_DOCUMENT_TYPES = {
    "DOC-019": "scs",
    "DOC-020": "sci",
    "DOC-021": "sci_iris",
    "DOC-025": "scm",
}
OPTION_IS_DOCUMENT_ID = "DOC-022"
SAS_PV_REMUNERATION_PRESIDENT_DOCUMENT_ID = "DOC-023"
SAS_ATTESTATION_CAPITAL_DOCUMENT_ID = "DOC-024"
SCM_SATELLITES_DOCUMENT_IDS = {
    "DOC-026": "pacte_associes",
    "DOC-027": "contrat_frais_communs",
    "DOC-028": "reglement_interieur",
    "DOC-030": "liste_depenses_communes",
}
ACTE_CESSION_ACTIONS_DOCUMENT_ID = "DOC-029"
SCM_CESSION_DOCUMENT_IDS = {"DOC-031", "DOC-032", "DOC-033"}


class MissingDocumentGeneratorError(RuntimeError):
    pass


def build_lot_01_generator_registry() -> dict[str, DocumentGenerator]:
    return {
        "DOC-001": DeclarationNonCondamnationGenerator(),
        "DOC-002": AutorisationDomiciliationGenerator(),
        "DOC-003": ProcurationGenerator(),
        "DOC-004": PvNominationGerantGenerator(),
        "DOC-005": LettreRenonciationAssocieGenerator(),
        "DOC-006": LettreAvertissementConjointGenerator(),
        "DOC-007": AvenantContratBailGenerator(),
        "DOC-008": AppelFondSelGenerator(),
        "DOC-009": ActeCessionCabinetMedicalGenerator(),
        "DOC-010": CompromisCessionCabinetMedicalGenerator(),
        "DOC-011": ActeCessionCabinetDentaireGenerator(),
        "DOC-012": CompromisCessionCabinetDentaireGenerator(),
        "DOC-013": FormulaireDerogationSitesSelGenerator(),
        "DOC-014": DemandeDerogationCumulSelarlBncGenerator(),
        "DOC-015": StatutsSasGenerator(),
        "DOC-016": StatutsSelarlDentisteGenerator(),
        "DOC-017": StatutsSelarlMedecinGenerator(),
        "DOC-018": StatutsSelasMedecinGenerator(),
        "DOC-019": StatutsScsGenerator(),
        "DOC-020": StatutsSciGenerator(),
        "DOC-021": StatutsSciIrisGenerator(),
        "DOC-022": LettreOptionIsGenerator(),
        "DOC-023": PvRemunerationPresidentGenerator(),
        "DOC-024": AttestationCapitalListeSouscripteursSasGenerator(),
        "DOC-025": StatutsScmGenerator(),
        "DOC-026": PacteAssociesScmGenerator(),
        "DOC-027": ContratFraisCommunsGenerator(),
        "DOC-028": ReglementInterieurScmGenerator(),
        "DOC-029": ActeCessionActionsSpfplGenerator(),
        "DOC-030": ListeDepensesCommunesScmGenerator(),
        "DOC-031": PvAgeCessionScmGenerator(),
        "DOC-032": CourrierSdeCessionScmGenerator(),
        "DOC-033": ActeCessionPartsScmGenerator(),
    }


def _statuts_sel_enabled(
    ctx: DocumentGenerationContext,
    expected: tuple[str, str],
) -> bool:
    expected_structure, expected_overlay = expected
    if ctx.structure != expected_structure or ctx.statuts_sel is None:
        return False
    return (ctx.statuts_sel.overlay or "").lower() == expected_overlay


class DocumentOrchestrator:
    def __init__(
        self,
        catalog: Sequence[DocumentDefinition],
        generators: Mapping[str, DocumentGenerator] | None = None,
    ) -> None:
        self._catalog = list(catalog)
        self._generators = dict(
            build_lot_01_generator_registry() if generators is None else generators
        )

    def select_documents(self, structure: str | None = None) -> list[DocumentDefinition]:
        if structure is None:
            return list(self._catalog)
        return [document for document in self._catalog if structure in document.structures]

    def select_documents_for_context(
        self,
        ctx: DocumentGenerationContext,
    ) -> list[DocumentDefinition]:
        documents = self.select_documents(ctx.structure)
        return [document for document in documents if _document_enabled_for_context(document, ctx)]

    def generate_documents(self, ctx: DocumentGenerationContext, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths: list[Path] = []
        for document in self.select_documents_for_context(ctx):
            generator = self._generators.get(document.doc_id)
            if generator is None:
                raise MissingDocumentGeneratorError(
                    "Aucun generateur enregistre pour "
                    f"{document.doc_id} ({document.canonical_name})."
                )
            output_paths.append(generator.generate(ctx, output_dir))
        return output_paths


def _document_enabled_for_context(
    document: DocumentDefinition,
    ctx: DocumentGenerationContext,
) -> bool:
    if document.doc_id not in REGIME_COMMUNAUTAIRE_DOCUMENT_IDS:
        if document.doc_id == BAIL_AVENANT_DOCUMENT_ID:
            return _cession_bail_enabled(ctx)
        if document.doc_id == APPEL_FONDS_DOCUMENT_ID:
            return _appel_fonds_enabled(ctx)
        if document.doc_id in CESSION_CABINET_DOCUMENT_IDS:
            return _cession_cabinet_enabled(document.doc_id, ctx)
        if document.doc_id in DEROGATION_DOCUMENT_TYPES:
            return _derogation_enabled(ctx, DEROGATION_DOCUMENT_TYPES[document.doc_id])
        if document.doc_id == STATUTS_SAS_DOCUMENT_ID:
            return _statuts_sas_enabled(ctx)
        if document.doc_id in STATUTS_SEL_DOCUMENTS:
            return _statuts_sel_enabled(ctx, STATUTS_SEL_DOCUMENTS[document.doc_id])
        if document.doc_id in STATUTS_CIVILS_DOCUMENT_TYPES:
            return _statuts_civils_enabled(ctx, STATUTS_CIVILS_DOCUMENT_TYPES[document.doc_id])
        if document.doc_id == OPTION_IS_DOCUMENT_ID:
            return _option_is_enabled(ctx)
        if document.doc_id == SAS_PV_REMUNERATION_PRESIDENT_DOCUMENT_ID:
            return _sas_pv_remuneration_president_enabled(ctx)
        if document.doc_id == SAS_ATTESTATION_CAPITAL_DOCUMENT_ID:
            return _sas_attestation_capital_enabled(ctx)
        if document.doc_id in SCM_SATELLITES_DOCUMENT_IDS:
            return _scm_satellite_enabled(ctx, SCM_SATELLITES_DOCUMENT_IDS[document.doc_id])
        if document.doc_id == ACTE_CESSION_ACTIONS_DOCUMENT_ID:
            return _acte_cession_actions_enabled(ctx)
        if document.doc_id in SCM_CESSION_DOCUMENT_IDS:
            return _scm_cession_enabled(ctx)
        return True
    return bool(ctx.dossier_options and ctx.dossier_options.regime_communautaire)


def _cession_bail_enabled(ctx: DocumentGenerationContext) -> bool:
    return bool(ctx.dossier_options and ctx.dossier_options.cession)


def _appel_fonds_enabled(ctx: DocumentGenerationContext) -> bool:
    if not _cession_bail_enabled(ctx):
        return False
    if ctx.structure != "SELARL":
        return False
    if ctx.cession is None or ctx.cession.type_cabinet is None:
        return False
    return ctx.cession.type_cabinet.strip().lower() == "dentaire"


def _cession_cabinet_enabled(doc_id: str, ctx: DocumentGenerationContext) -> bool:
    if not _cession_bail_enabled(ctx):
        return False
    if ctx.cession is None or ctx.cession.etape is None or ctx.cession.type_cabinet is None:
        return False
    expected_etape, expected_type = CESSION_CABINET_DOCUMENT_IDS[doc_id]
    return (
        ctx.cession.etape.strip().lower() == expected_etape
        and ctx.cession.type_cabinet.strip().lower() == expected_type
    )


def _derogation_enabled(ctx: DocumentGenerationContext, derogation_type: str) -> bool:
    if ctx.dossier_options is None or not ctx.dossier_options.derogation:
        return False
    if ctx.derogation is None or ctx.derogation.type != derogation_type:
        return False
    return ctx.derogation.mode_rendu == "formulaire_a_completer"


def _statuts_sas_enabled(ctx: DocumentGenerationContext) -> bool:
    if ctx.structure != "SAS" or ctx.statuts_sas is None:
        return False
    statuts_type = ctx.statuts_sas.type or ""
    profession = ctx.statuts_sas.profession or ""
    return statuts_type.lower() == "spfpl_medecins" and profession.lower() in {
        "medecin",
        "médecin",
    }


def _statuts_civils_enabled(ctx: DocumentGenerationContext, statuts_type: str) -> bool:
    if ctx.statuts_civils is None or ctx.statuts_civils.type is None:
        return False
    return ctx.statuts_civils.type.strip().lower() == statuts_type


def _option_is_enabled(ctx: DocumentGenerationContext) -> bool:
    return bool(ctx.dossier_options and ctx.dossier_options.option_is)


def _sas_base_satellite_enabled(ctx: DocumentGenerationContext) -> bool:
    if ctx.structure != "SAS":
        return False
    if ctx.dossier_options is None or not ctx.dossier_options.associe_unique:
        return False
    if not _statuts_sas_enabled(ctx):
        return False
    if ctx.actionnaire_unique is None or ctx.president is None:
        return False
    return ctx.president.ref_associe_index == 0


def _sas_pv_remuneration_president_enabled(ctx: DocumentGenerationContext) -> bool:
    if not _sas_base_satellite_enabled(ctx):
        return False
    if ctx.remuneration_president is None:
        return False
    return ctx.remuneration_president.type == "absence_remuneration"


def _sas_attestation_capital_enabled(ctx: DocumentGenerationContext) -> bool:
    if not _sas_base_satellite_enabled(ctx):
        return False
    if ctx.dossier_options is None or not ctx.dossier_options.apport:
        return False
    if ctx.capital_souscription is None:
        return False
    if len(ctx.capital_souscription.souscripteurs) != 1:
        return False
    return bool(ctx.capital_souscription.apports_nature_montant)


def _scm_satellite_enabled(ctx: DocumentGenerationContext, satellite_field: str) -> bool:
    if ctx.structure != "SCM":
        return False
    if ctx.dossier_options is None or not ctx.dossier_options.scm_satellites:
        return False
    if ctx.scm_satellites is None:
        return False
    return bool(getattr(ctx.scm_satellites, satellite_field))


def _acte_cession_actions_enabled(ctx: DocumentGenerationContext) -> bool:
    if ctx.structure != "SPFPL cession":
        return False
    if ctx.dossier_options is None or not ctx.dossier_options.cession:
        return False
    if ctx.operation_spfpl is None:
        return False
    return (
        (ctx.operation_spfpl.type or "").strip().lower() == "cession"
        and (ctx.operation_spfpl.nature_titres or "").strip().lower() == "actions"
        and (ctx.operation_spfpl.document_demande or "").strip().lower()
        == "acte_cession_actions"
    )


def _scm_cession_enabled(ctx: DocumentGenerationContext) -> bool:
    if ctx.structure not in {"SELARL", "SELAS"}:
        return False
    if ctx.dossier_options is None or not ctx.dossier_options.scm_cession:
        return False
    if ctx.scm_cession is None:
        return False
    if ctx.scm_cession.variante_structure is None:
        return True
    return ctx.scm_cession.variante_structure.strip().lower() == ctx.structure.lower()
