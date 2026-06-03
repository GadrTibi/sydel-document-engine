from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    ApportTitres,
    Associe,
    CapitalContext,
    CapitalSouscripteur,
    CapitalSouscription,
    Company,
    DecisionContext,
    DirigeantNomine,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    ExerciceSocial,
    Mandataire,
    OperationSpfpl,
    OrdreAddress,
    OrdreProfessionnel,
    Person,
    RemunerationPresident,
    ReunionContext,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplPerson,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsCapitalDepot,
    StatutsCivilsContext,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
    StatutsPresident,
    StatutsSas,
)
from sydel_doc_engine.orchestrator.service import (
    DocumentOrchestrator,
    MissingDocumentGeneratorError,
    build_generator_registry,
)
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _context(structure: str = "SELARL") -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            titre_affichage="Dr",
            prenom="Jean",
            nom="Durand",
            adresse_personnelle_affichee="12 rue des Lilas\n75008 Paris",
            adresse_perso=Address(
                num_voie="12",
                voie="rue des Lilas",
                cp="75008",
                ville="Paris",
            ),
            date_naissance=date(1990, 2, 3),
            ville_naissance="Paris",
            nationalite="francaise",
            nom_pere="Pierre Durand",
            nom_mere="Anne Martin",
            fonction_dirigeant="President",
        ),
        societe=Company(
            forme_sociale="SELARL",
            forme_sociale_affichage="SELARL",
            forme_sociale_libelle_long="société d'exercice libéral à responsabilité limitée",
            denomination="DURAND CONSEIL",
            capital="1 000",
            capital_social="1 000",
            capital_variable=True,
            siege=Address(
                num_voie="80",
                voie="avenue Marceau",
                cp="75008",
                ville="Paris",
            ),
            ville_rcs="Paris",
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee="15 rue du Libre, Lyon 69002",
        ),
        ordre=OrdreProfessionnel(
            conseil_departemental_libelle="Conseil departemental de l'Ordre",
            destinataire_appel="Monsieur le President",
            profession_signataire_affichee="chirurgien-dentiste",
            profession_ligne_destinataire="chirurgiens-dentistes",
            profession_reglementee_pluriel="chirurgiens-dentistes",
            adresse=OrdreAddress(
                ligne_1="6 rue du Conseil",
                cp="75001",
                ville="Paris",
            ),
        ),
        mandataire=Mandataire(
            civilite_affichage="Madame",
            prenom="Sophie",
            nom="Martin",
            fonction="juriste",
            cabinet="DAAT",
        ),
        decision=DecisionContext(date="13 mai 2026"),
        reunion=ReunionContext(date_lettres="treize mai deux mille vingt-six", heure="10 heures"),
        capital=CapitalContext(
            nb_parts_total=100,
            valeur_nominale_part="1",
        ),
        associes=[
            Associe(
                genre=Gender.MASCULIN,
                civilite_affichage="Monsieur",
                prenom="Jean",
                nom="Durand",
                nb_parts=100,
            )
        ],
        dirigeant_nomine=DirigeantNomine(
            genre=Gender.MASCULIN,
            civilite_affichage="Monsieur",
            prenom="Jean",
            nom="Durand",
            date_naissance=date(1990, 2, 3),
            ville_naissance="Paris",
            departement_naissance="Paris",
            nationalite="francaise",
            adresse_personnelle=Address(
                num_voie="12",
                voie="rue des Lilas",
                cp="75008",
                ville="Paris",
            ),
            fonction_affichage="gérant",
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 12),
            nombre_exemplaires="3",
        ),
    )


def _sas_satellites_context() -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SAS",
        dossier_options=DossierOptions(associe_unique=True, apport=True),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        statuts_sas=StatutsSas(type="spfpl_medecins", profession="medecin"),
        societe_spfpl=SocieteSpfpl(
            denomination="SPFPL DURAND",
            forme_sociale="Société par actions simplifiée",
            capital_social="60 000",
            nb_actions_total=600,
            valeur_nominale_action="100",
            profession="Médecins",
            ville_rcs="Paris",
            siege=Address(adresse_affichee="10 rue de la Paix, 75002 Paris"),
        ),
        actionnaire_unique=SpfplPerson(
            civilite_affichage="Docteur",
            prenom="Jean",
            nom="Durand",
            genre=Gender.MASCULIN,
            profession="médecin",
            qualite_associe="actionnaire unique",
            adresse_personnelle=Address(
                num_voie="5",
                voie="rue Royale",
                cp="75008",
                ville="Paris",
            ),
            adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ),
        president=StatutsPresident(
            ref_associe_index=0,
            civilite_affichage="Docteur",
            prenom="Jean",
            nom="Durand",
            fonction="Président",
        ),
        exercice_social=ExerciceSocial(date_cloture_premier_exercice="31 décembre 2026"),
        remuneration_president=RemunerationPresident(
            type="absence_remuneration",
            date_fin_non_remuneree="31 décembre 2026",
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=600,
            valeur_nominale_action="100",
            apports_nature_montant="50 000",
            apports_numeraire_montant="10 000",
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage="Docteur",
                    prenom="Jean",
                    nom="Durand",
                    profession="médecin",
                    adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
                    nb_actions=600,
                )
            ],
        ),
        apport_titres=ApportTitres(nb_parts=50),
        societe_cible=SocieteCible(
            denomination="SELARL CABINET DURAND",
            forme_sociale="SELARL",
            siege=Address(adresse_affichee="12 avenue des Ternes, 75017 Paris"),
            ville_rcs="Paris",
            numero_rcs="900 000 001",
        ),
    )


def _scm_context() -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SCM",
        dossier_options=DossierOptions(),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        societe=Company(
            denomination="SCM CABINET DURAND MARTIN",
            denomination_courte="CABINET DURAND MARTIN",
            forme_sociale="Societe civile de moyens",
            siege=Address(
                num_voie="10",
                voie="rue de la Paix",
                cp="75002",
                ville="Paris",
            ),
        ),
        statuts_civils=StatutsCivilsContext(
            type="scm",
            forme_sociale="Societe civile de moyens",
            capital_social="1200",
            capital_social_lettres="mille deux cents euros",
            nb_parts_total=120,
            valeur_nominale_part="10 euros",
            capital_depot=StatutsCivilsCapitalDepot(
                banque_nom="BANQUE EXEMPLE",
                banque_adresse="1 rue Banque, 75009 Paris",
            ),
            associes=[
                StatutsCivilsAssocie(
                    type_personne="personne_morale",
                    denomination="SELARL DURAND",
                    forme_juridique="SELARL",
                    profession="chirurgien-dentiste",
                    capital_social="1 000 euros",
                    siege=Address(adresse_affichee="5 rue Royale, 75008 Paris"),
                    numero_rcs="900 000 001",
                    ville_rcs="Paris",
                    representant=StatutsCivilsRepresentant(
                        civilite_affichage="Monsieur",
                        prenom="Jean",
                        nom="Durand",
                        fonction="gerant",
                    ),
                    apport=StatutsCivilsApport(
                        montant="700",
                        montant_lettres="sept cents euros",
                    ),
                    parts=StatutsCivilsParts(nb=70),
                ),
                StatutsCivilsAssocie(
                    type_personne="personne_physique",
                    genre=Gender.FEMININ,
                    civilite_affichage="Madame",
                    prenom="Alice",
                    prenoms="Alice",
                    nom="Martin",
                    profession="chirurgien-dentiste",
                    date_naissance="2 fevrier 1982",
                    ville_naissance="Lyon",
                    nationalite="francaise",
                    situation_maritale="celibataire",
                    adresse_personnelle_affichee="2 rue Exemple, 69000 Lyon",
                    apport=StatutsCivilsApport(
                        montant="500",
                        montant_lettres="cinq cents euros",
                    ),
                    parts=StatutsCivilsParts(nb=50),
                ),
            ],
        ),
    )


def _spfpl_cession_selection_context(*, associe_unique: bool = True) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SPFPL cession",
        dossier_options=DossierOptions(cession=True, associe_unique=associe_unique),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        operation_spfpl=OperationSpfpl(type="cession"),
    )


def _spfpl_apport_selection_context() -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SPFPL apport",
        dossier_options=DossierOptions(apport=True),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        operation_spfpl=OperationSpfpl(type="apport"),
        capital_souscription=CapitalSouscription(
            souscripteurs=[CapitalSouscripteur(prenom="Jean", nom="Durand")]
        ),
    )


def test_select_documents_for_selarl_includes_pv_nomination_gerant() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SELARL")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-005",
        "DOC-006",
        "DOC-007",
        "DOC-008",
        "DOC-009",
        "DOC-010",
        "DOC-011",
        "DOC-012",
        "DOC-013",
        "DOC-014",
        "DOC-016",
        "DOC-017",
        "DOC-031",
        "DOC-032",
        "DOC-033",
    ]


def test_catalog_and_generator_registry_have_same_doc_ids() -> None:
    catalog_ids = {document.doc_id for document in build_seed_catalog()}
    registry_ids = set(build_generator_registry())

    assert catalog_ids == registry_ids


def test_select_documents_for_sci_includes_pv_nomination_gerant() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SCI")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-020",
        "DOC-022",
    ]


def test_select_documents_for_sas_excludes_pv_nomination_gerant() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SAS")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-015",
        "DOC-023",
        "DOC-024",
    ]


def test_select_documents_for_sas_context_includes_satellites_when_enabled() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(_sas_satellites_context())

    assert "DOC-023" in [document.doc_id for document in selected]
    assert "DOC-024" in [document.doc_id for document in selected]


def test_select_documents_for_sas_context_excludes_satellites_by_default() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(_context("SAS"))

    assert "DOC-023" not in [document.doc_id for document in selected]
    assert "DOC-024" not in [document.doc_id for document in selected]


def test_select_documents_for_spfpl_cession_context_includes_reconciled_generators() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected_ids = [
        document.doc_id
        for document in orchestrator.select_documents_for_context(
            _spfpl_cession_selection_context()
        )
    ]

    assert "DOC-034" in selected_ids
    assert "DOC-035" in selected_ids
    assert "DOC-037" in selected_ids
    assert "DOC-038" in selected_ids
    assert "DOC-039" not in selected_ids
    assert "DOC-040" in selected_ids


def test_select_documents_for_spfpl_apport_context_includes_reconciled_generators() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected_ids = [
        document.doc_id
        for document in orchestrator.select_documents_for_context(_spfpl_apport_selection_context())
    ]

    assert "DOC-034" in selected_ids
    assert "DOC-036" in selected_ids
    assert "DOC-037" in selected_ids
    assert "DOC-041" in selected_ids
    assert "DOC-042" in selected_ids
    assert "DOC-043" in selected_ids


def test_select_documents_for_sci_iris_includes_dedicated_statuts() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SCI IRIS")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-021",
        "DOC-022",
    ]


def test_select_documents_for_scm_includes_dedicated_statuts() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents("SCM")

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-025",
        "DOC-026",
        "DOC-027",
        "DOC-028",
        "DOC-030",
    ]


def test_select_documents_for_scm_context_includes_statuts_scm_when_enabled() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(_scm_context())

    assert "DOC-025" in [document.doc_id for document in selected]


def test_select_documents_for_sci_context_includes_option_is_only_when_enabled() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    ctx = _context("SCI")

    selected_without_option = orchestrator.select_documents_for_context(ctx)
    assert "DOC-022" not in [document.doc_id for document in selected_without_option]

    ctx.dossier_options = DossierOptions(option_is=True)
    selected_with_option = orchestrator.select_documents_for_context(ctx)

    assert "DOC-022" in [document.doc_id for document in selected_with_option]


def test_generate_documents_creates_docx_for_selected_documents(tmp_path: Path) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    output_paths = orchestrator.generate_documents(_context(), tmp_path)

    assert len(output_paths) == 5
    assert all(path.suffix == ".docx" for path in output_paths)
    assert all(path.is_file() for path in output_paths)
    assert tmp_path / "pv_nomination_gerant.docx" in output_paths
    assert tmp_path / "demande_inscription_ordre.docx" in output_paths
    assert tmp_path / "lettre_renonciation_associe.docx" not in output_paths
    assert tmp_path / "lettre_avertissement_conjoint.docx" not in output_paths


def test_generate_documents_outputs_follow_catalog_order(tmp_path: Path) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    output_paths = orchestrator.generate_documents(_context(), tmp_path)

    assert [path.name for path in output_paths] == [
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
        "demande_inscription_ordre.docx",
    ]


def test_generate_documents_raises_clear_error_when_generator_is_missing(
    tmp_path: Path,
) -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog(), generators={})

    with pytest.raises(MissingDocumentGeneratorError, match="DOC-001"):
        orchestrator.generate_documents(_context(), tmp_path)
