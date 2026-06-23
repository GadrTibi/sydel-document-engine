from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    CessionAccessibiliteCabinetDentaire,
    CessionAcquereur,
    CessionBailProfessionnel,
    CessionCabinet,
    CessionConjoint,
    CessionContext,
    CessionCreditVendeur,
    CessionExercice,
    CessionFinancement,
    CessionPrecedentProprietaire,
    CessionPret,
    CessionPrix,
    CessionRepresentant,
    CessionSalarie,
    CessionScm,
    CessionValidations,
    CessionVendeur,
    DocumentContext,
    DocumentGenerationContext,
    DossierOptions,
    Person,
    Signature,
)
from sydel_doc_engine.generators.lot_03.acte_cession_cabinet_dentaire import (
    ActeCessionCabinetDentaireGenerator,
)
from sydel_doc_engine.generators.lot_03.acte_cession_cabinet_medical import (
    ActeCessionCabinetMedicalGenerator,
)
from sydel_doc_engine.generators.lot_03.compromis_cession_cabinet_dentaire import (
    CompromisCessionCabinetDentaireGenerator,
)
from sydel_doc_engine.generators.lot_03.compromis_cession_cabinet_medical import (
    CompromisCessionCabinetMedicalGenerator,
)
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _context(
    *,
    etape: str = "acte",
    type_cabinet: str = "medical",
    credit_vendeur: bool = False,
    validations: CessionValidations | None = None,
    salaries: list[CessionSalarie] | None = None,
    vendeur_genre: Gender = Gender.MASCULIN,
    representant_genre: Gender = Gender.FEMININ,
) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SELARL",
        dossier_options=DossierOptions(cession=True),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 14)),
        cession=CessionContext(
            type_cabinet=type_cabinet,
            etape=etape,
            vendeur=CessionVendeur(
                civilite_affichage="Docteur",
                genre=vendeur_genre,
                prenom="Jean",
                nom="Durand",
                profession="chirurgien-dentiste" if type_cabinet == "dentaire" else "medecin",
                date_naissance=date(1975, 3, 10),
                ville_naissance="Lyon",
                departement_naissance="69",
                cp_naissance="69002",
                pays_naissance="France",
                nationalite="francaise",
                adresse_affichee="4 rue Victor Hugo, 69002 Lyon",
                adresse_exercice_affichee="10 rue du Cabinet, 75008 Paris",
                numero_siren="123 456 789",
                numero_ordre="ORD-123",
                numero_rpps="10101010101",
                ordre_departemental="Paris",
                situation_maritale="marie",
                regime_matrimonial="communaute reduite aux acquets",
                conjoint=CessionConjoint(
                    civilite_affichage="Madame",
                    prenom="Claire",
                    nom="Durand",
                ),
            ),
            acquereur=CessionAcquereur(
                denomination_societe="SELARL CABINET DURAND",
                forme_sociale="SELARL",
                capital_social="10 000",
                siege=Address(adresse_affichee="20 avenue de Wagram, 75017 Paris"),
                rcs_ville="Paris",
                numero_rcs="999 888 777",
                numero_siret="999 888 777 00012",
                date_immatriculation=date(2026, 1, 15),
                date_inscription_ordre=date(2026, 2, 1),
                representant=CessionRepresentant(
                    civilite_affichage="Docteur",
                    genre=representant_genre,
                    prenom="Alice",
                    nom="Moreau",
                    fonction="gerante",
                ),
            ),
            cabinet=CessionCabinet(
                nature_fonds_liberal="medecin generaliste",
                adresse_affichee="10 rue du Cabinet, 75008 Paris",
                adresse_locaux_affichee="10 rue du Cabinet, 75008 Paris",
                telephone="01 44 00 00 00",
                superficie_local="80 m2",
                date_origine_propriete=date(2020, 1, 1),
                annees_acquisition_patientele="2020",
                prix_origine_propriete="120 000",
                precedent_proprietaire=CessionPrecedentProprietaire(
                    civilite_affichage="Docteur",
                    prenom="Paul",
                    nom="Bernard",
                ),
            ),
            bail_professionnel=CessionBailProfessionnel(
                date_bail=date(2021, 1, 1),
                duree="six annees",
                date_debut=date(2021, 1, 1),
                date_fin=date(2027, 1, 1),
                date_reconduction_1=date(2027, 1, 1),
                date_reconduction_2=date(2033, 1, 1),
                loyer_mensuel="2 000 euros",
                activite_autorisee_affichee="activite medicale et paramedicale",
            ),
            exercices=[
                CessionExercice(periode="2023", chiffre_affaires="210 000", resultat="80 000"),
                CessionExercice(periode="2024", chiffre_affaires="220 000", resultat="85 000"),
                CessionExercice(periode="2025", chiffre_affaires="230 000", resultat="90 000"),
            ],
            prix=CessionPrix(
                total="300 000",
                total_lettres="trois cent mille euros",
                elements_corporels="50 000",
                elements_corporels_lettres="cinquante mille euros",
                elements_incorporels="250 000",
                elements_incorporels_lettres="deux cent cinquante mille euros",
            ),
            financement=CessionFinancement(
                pret=CessionPret(montant="240 000", taux="4 %", duree="sept ans"),
                credit_vendeur=CessionCreditVendeur(
                    actif=credit_vendeur,
                    # Regle NotebookLM : unite du credit-vendeur = ANNEES (« Trois ans »).
                    # Le wording du modele rend « [duree_credit_vendeur] ans ».
                    duree="trois",
                    montant="60 000",
                    taux="3 %",
                    majoration_interet_retard="2 points",
                ),
            ),
            scm=CessionScm(actif=credit_vendeur, nb_parts_a_ceder="10"),
            salaries=salaries or [],
            accessibilite_cabinet_dentaire=CessionAccessibiliteCabinetDentaire(
                information_requise="Information d'accessibilite dentaire fournie par contexte.",
            ),
            date_limite_realisation=date(2026, 9, 30),
            validations=validations
            or CessionValidations(
                mentions_bail_medical_validees=True,
                origine_compromis_medical_validee=True,
                date_realisation_compromis_validee=True,
                ligne_contrats_travail_medical_supprimee=True,
                salaries_dentaire_deux_valides=True,
            ),
        ),
        document=DocumentContext(
            nombre_pages_lettres="vingt",
            nombre_exemplaires_lettres="quatre",
            annexes=["ETAT DES ELEMENTS CORPORELS CEDES", "COPIE 2035 AMORTISSEMENTS"],
        ),
    )


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs)
    return "\n".join(text for text in texts if text)


def _assert_no_residual_tokens(text: str) -> None:
    # Le rendu par remplissage de template ne doit laisser aucun token [xxx] residuel.
    assert "[" not in text
    assert "]" not in text


def _docx_part_names(path: Path) -> set[str]:
    import zipfile

    with zipfile.ZipFile(path) as archive:
        return set(archive.namelist())


def _docx_document_xml(path: Path) -> str:
    import zipfile

    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml").decode("utf-8", "replace")


def _docx_highlighted_run_texts(path: Path) -> list[str]:
    document = Document(path)
    texts: list[str] = []

    def _scan(paragraphs) -> None:
        for paragraph in paragraphs:
            for run in paragraph.runs:
                if run.font.highlight_color is not None:
                    texts.append(run.text)

    _scan(document.paragraphs)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                _scan(cell.paragraphs)
    return texts


def _docx_paragraph_texts(path: Path) -> list[str]:
    document = Document(path)
    return [paragraph.text for paragraph in document.paragraphs]


@pytest.mark.parametrize(
    ("generator", "ctx", "filename", "expected_text"),
    [
        (
            ActeCessionCabinetMedicalGenerator(),
            _context(credit_vendeur=True),
            "acte_cession_cabinet_medical.docx",
            "Ordre des Médecins",
        ),
        (
            CompromisCessionCabinetMedicalGenerator(),
            _context(etape="compromis"),
            "compromis_cession_cabinet_medical.docx",
            "Ordre des Médecins",
        ),
        (
            ActeCessionCabinetDentaireGenerator(),
            _context(
                type_cabinet="dentaire",
                salaries=[
                    CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit"),
                    CessionSalarie(civilite_affichage="Monsieur", prenom="Noe", nom="Robert"),
                ],
            ),
            "acte_cession_cabinet_dentaire.docx",
            "Petit",
        ),
        (
            CompromisCessionCabinetDentaireGenerator(),
            _context(etape="compromis", type_cabinet="dentaire"),
            "compromis_cession_cabinet_dentaire.docx",
            "Entre les soussignés",
        ),
    ],
)
def test_cession_cabinet_generators_render_docx(
    generator,
    ctx: DocumentGenerationContext,
    filename: str,
    expected_text: str,
    tmp_path: Path,
) -> None:
    output_path = generator.generate(ctx, tmp_path)

    assert output_path == tmp_path / filename
    text = _docx_text(output_path)
    # Texte juridique d'origine preserve (rendu fidele par template, non paraphrase).
    assert "Entre les soussignés" in text
    assert expected_text in text
    # Tokens du contexte injectes (vendeur + acquereur).
    assert "SELARL CABINET" in text
    assert "Durand" in text or "Martin" in text
    # Dates rendues en francais long, pas en ISO.
    assert "10 mars 1975" in text or "20 juin 1984" in text
    _assert_no_residual_tokens(text)


def test_o24_14_compromis_genere_meme_si_cession_etape_acte(tmp_path: Path) -> None:
    # O24-14 (onglet 24) : en SELAS l'acte ET le compromis sont produits ENSEMBLE, donc le
    # compromis est généré alors que cession.etape est forcée à 'acte'. Avant le fix,
    # _validate_selection levait « cession.etape doit etre compromis pour compromis_... ».
    # Le document est piloté par le VARIANT (variant.etape), pas par cession.etape.
    ctx = _context(etape="acte", type_cabinet="dentaire")
    output_path = CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)
    assert output_path == tmp_path / "compromis_cession_cabinet_dentaire.docx"
    assert output_path.exists()


def test_acte_medical_blocks_without_medical_bail_validation(tmp_path: Path) -> None:
    ctx = _context(
        validations=CessionValidations(
            mentions_bail_medical_validees=False,
            ligne_contrats_travail_medical_supprimee=True,
        ),
    )

    with pytest.raises(ValueError, match="mentions_bail_medical_validees"):
        ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path)


def test_credit_vendeur_blocks_outside_medical_acte(tmp_path: Path) -> None:
    ctx = _context(etape="compromis", credit_vendeur=True)

    with pytest.raises(ValueError, match="credit_vendeur"):
        CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path)


def test_credit_vendeur_duree_rendered_in_years(tmp_path: Path) -> None:
    # FIX 4 : l'unite de duree du credit-vendeur est l'annee (« ... ans »).
    ctx = _context(credit_vendeur=True)

    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "dans un délai maximum de trois ans" in text
    assert "Au terme du délai de trois ans" in text
    assert "mois" not in text.split("crédit-vendeur à hauteur")[1].split("intérêt annuel")[0]
    _assert_no_residual_tokens(text)


def test_origine_propriete_describes_vendeur_created_by_default(tmp_path: Path) -> None:
    # FIX 1 : l'origine decrit le VENDEUR (cedant) ; defaut « cree ».
    for generator, etape in (
        (ActeCessionCabinetMedicalGenerator(), "acte"),
        (CompromisCessionCabinetMedicalGenerator(), "compromis"),
    ):
        ctx = _context(etape=etape, credit_vendeur=(etape == "acte"))
        text = _docx_text(generator.generate(ctx, tmp_path / etape))
        # Sujet = vendeur (Docteur Jean Durand), pas l'acquereur (Alice Moreau).
        assert "Docteur Jean Durand est propriétaire des éléments constitutifs du cabinet" in text
        assert "pour l’avoir régulièrement créé le 1 janvier 2020." in text
        assert "Alice Moreau est propriétaire" not in text
        _assert_no_residual_tokens(text)


def test_origine_propriete_purchased_describes_vendeur(tmp_path: Path) -> None:
    # FIX 1 : variante « achete » -> origine via achat anterieur du vendeur.
    ctx = _context(credit_vendeur=True)
    ctx.cession.cabinet.origine_propriete_mode = "achete"
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Docteur Jean Durand est propriétaire des éléments constitutifs du cabinet" in text
    assert "pour les avoir régulièrement acquis auprès de Docteur Paul Bernard" in text
    # Wording source « au prix de <prix> euros » : la donnee porte le seul montant.
    assert "au prix de 120 000 euros." in text
    _assert_no_residual_tokens(text)


def test_origine_propriete_complex_case_blocks_without_validation(tmp_path: Path) -> None:
    # GARDE-FOU souplesse : une origine COMPLEXE (mode non standard) bloque tant
    # qu'un texte libre valide a la main n'est pas fourni.
    ctx = _context(credit_vendeur=True)
    ctx.cession.cabinet.origine_propriete_mode = "succession"

    with pytest.raises(ValueError, match="origine_propriete_mode"):
        ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path)


def test_origine_propriete_complex_case_renders_free_text_when_validated(tmp_path: Path) -> None:
    # Cas COMPLEXE valide : texte libre rendu tel quel (relecture humaine).
    ctx = _context(credit_vendeur=True)
    ctx.cession.cabinet.origine_propriete_mode = "succession"
    ctx.cession.cabinet.description_origine_propriete = (
        "Le vendeur a recueilli le cabinet par voie de succession de son père en 2015."
    )
    ctx.cession.validations.origine_propriete_complexe_validee = True

    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "par voie de succession de son père en 2015." in text
    _assert_no_residual_tokens(text)


def test_medical_models_have_no_dentaire_leak(tmp_path: Path) -> None:
    # FIX 2 : aucune mention « dentaire » dans les cessions MEDICALES.
    acte = _docx_text(
        ActeCessionCabinetMedicalGenerator().generate(_context(credit_vendeur=True), tmp_path / "a")
    )
    compromis = _docx_text(
        CompromisCessionCabinetMedicalGenerator().generate(
            _context(etape="compromis"), tmp_path / "c"
        )
    )
    for text in (acte, compromis):
        lowered = text.lower()
        assert "dentaire" not in lowered
        assert "dentiste" not in lowered
        assert "stomatologue" not in lowered
        # Le wording medical propre est conserve.
        assert "cabinet médical" in lowered


def test_acte_dentaire_salaries_zero_removes_clause(tmp_path: Path) -> None:
    # Retours client 2026-06-11 (tickets 2.12 / 3.3) : 0 salarie -> la phrase
    # relative aux salaries est SUPPRIMEE de l'acte (remplace la convention
    # « Néant » anterieure). Aucune erreur, generation non bloquee.
    ctx = _context(type_cabinet="dentaire", salaries=[])

    text = _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "Néant" not in text
    assert "De reprendre les contrats de travail de" not in text
    _assert_no_residual_tokens(text)


def test_acte_dentaire_salaries_one_renders_single(tmp_path: Path) -> None:
    # Regle NotebookLM : 1 salarie -> liste a un element (poste optionnel rendu).
    ctx = _context(
        type_cabinet="dentaire",
        salaries=[
            CessionSalarie(
                civilite_affichage="Madame", prenom="Lea", nom="Petit", poste="assistante dentaire"
            )
        ],
    )

    text = _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "De reprendre les contrats de travail de Madame Lea Petit" in text
    assert "en qualité de assistante dentaire" in text
    assert " et de " not in text.split("contrats de travail de")[1].split(".")[0]
    _assert_no_residual_tokens(text)


def test_acte_dentaire_salaries_three_renders_full_list(tmp_path: Path) -> None:
    # Regle NotebookLM : N salaries -> liste complete (assouplissement 0/1/N).
    ctx = _context(
        type_cabinet="dentaire",
        salaries=[
            CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit"),
            CessionSalarie(civilite_affichage="Monsieur", prenom="Noe", nom="Robert"),
            CessionSalarie(civilite_affichage="Madame", prenom="Ines", nom="Faure"),
        ],
    )

    text = _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "Madame Lea Petit, Monsieur Noe Robert et de Madame Ines Faure" in text
    _assert_no_residual_tokens(text)


def test_acte_dentaire_salary_requires_complete_identity(tmp_path: Path) -> None:
    # Garde-fou : un salarie liste doit avoir civilite/prenom/nom (identite complete).
    ctx = _context(
        type_cabinet="dentaire",
        salaries=[CessionSalarie(civilite_affichage="Madame", prenom="Lea")],
    )

    with pytest.raises(ValueError, match="salaries"):
        ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path)


_DENT_SALARIES = [
    CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit"),
    CessionSalarie(civilite_affichage="Monsieur", prenom="Noe", nom="Robert"),
]


def test_acte_dentaire_vendeur_masculin_agreement(tmp_path: Path) -> None:
    # Modele dentaire fige au FEMININ -> vendeur masculin = retour au masculin.
    ctx = _context(
        type_cabinet="dentaire",
        salaries=_DENT_SALARIES,
        vendeur_genre=Gender.MASCULIN,
    )

    text = _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "chirurgien-dentiste, né le 10 mars 1975" in text
    assert "née le 10 mars 1975" not in text
    assert "Inscrit au tableau du Conseil départemental" in text
    assert "Inscrite au tableau du Conseil départemental" not in text
    # Forme de role invariante conservee.
    assert "le soussigné de première part" in text
    _assert_no_residual_tokens(text)


def test_acte_dentaire_vendeur_feminin_agreement(tmp_path: Path) -> None:
    # Modele dentaire deja feminin -> vendeur feminin = conserve tel quel.
    ctx = _context(
        type_cabinet="dentaire",
        salaries=_DENT_SALARIES,
        vendeur_genre=Gender.FEMININ,
    )

    text = _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "chirurgien-dentiste, née le 10 mars 1975" in text
    assert "Inscrite au tableau du Conseil départemental" in text
    _assert_no_residual_tokens(text)


def test_acte_dentaire_representant_gender_agreement(tmp_path: Path) -> None:
    # « domicilié(e) en cette qualité » est pilote par le genre du representant.
    masc = _docx_text(
        ActeCessionCabinetDentaireGenerator().generate(
            _context(
                type_cabinet="dentaire",
                salaries=_DENT_SALARIES,
                representant_genre=Gender.MASCULIN,
            ),
            tmp_path / "masc",
        )
    )
    fem = _docx_text(
        ActeCessionCabinetDentaireGenerator().generate(
            _context(
                type_cabinet="dentaire",
                salaries=_DENT_SALARIES,
                representant_genre=Gender.FEMININ,
            ),
            tmp_path / "fem",
        )
    )

    assert "domicilié en cette qualité audit siège" in masc
    assert "domiciliée en cette qualité" not in masc
    assert "domiciliée en cette qualité audit siège" in fem
    # « Représentée » accorde la societe (toujours feminin) : jamais touche.
    assert "Représentée par" in masc
    assert "Représentée par" in fem


def test_compromis_medical_vendeur_feminin_agreement(tmp_path: Path) -> None:
    # Modele medical fige au MASCULIN -> vendeur feminin = accord au feminin.
    ctx = _context(
        etape="compromis",
        type_cabinet="medical",
        vendeur_genre=Gender.FEMININ,
    )

    text = _docx_text(CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "medecin, née le 10 mars 1975" in text
    assert "inscrite au tableau du Conseil départemental" in text
    # GARDE-FOU : le « Tableau » de la societe (Ordre) ne doit jamais devenir feminin parasite.
    assert "au Tableau de l’Ordre des Médecins" in text
    _assert_no_residual_tokens(text)


def test_compromis_medical_vendeur_masculin_agreement(tmp_path: Path) -> None:
    ctx = _context(
        etape="compromis",
        type_cabinet="medical",
        vendeur_genre=Gender.MASCULIN,
    )

    text = _docx_text(CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "medecin, né le 10 mars 1975" in text
    assert "née le 10 mars 1975" not in text
    assert "inscrit au tableau du Conseil départemental" in text
    _assert_no_residual_tokens(text)


def test_acte_medical_keeps_inclusive_birth_form(tmp_path: Path) -> None:
    # L'acte medical fige la forme inclusive « né(e) le » : jamais accordee,
    # quel que soit le genre du vendeur (aucune paire ne la matche).
    masc = _docx_text(
        ActeCessionCabinetMedicalGenerator().generate(
            _context(credit_vendeur=True, vendeur_genre=Gender.MASCULIN),
            tmp_path / "masc",
        )
    )
    fem = _docx_text(
        ActeCessionCabinetMedicalGenerator().generate(
            _context(credit_vendeur=True, vendeur_genre=Gender.FEMININ),
            tmp_path / "fem",
        )
    )

    assert "né(e) le 10 mars 1975" in masc
    assert "né(e) le 10 mars 1975" in fem


def test_acte_medical_renders_conjoint_prenom_and_nom(tmp_path: Path) -> None:
    # Retour UAT Rafael (DOC-009) : la clause de situation maritale doit afficher
    # le PRENOM ET le NOM du conjoint (« marié(e) à Prenom Nom, sous le régime... »).
    text = _docx_text(
        ActeCessionCabinetMedicalGenerator().generate(
            _context(credit_vendeur=True),
            tmp_path,
        )
    )

    # Conjoint = Claire Durand, regime = communaute reduite aux acquets (cf. _context).
    assert "marie à Claire Durand, sous le régime de communaute reduite aux acquets" in text
    _assert_no_residual_tokens(text)


def test_orchestrator_selects_only_requested_cession_cabinet_document() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected_ids = {
        document.doc_id
        for document in orchestrator.select_documents_for_context(
            _context(etape="compromis", type_cabinet="dentaire"),
        )
    }

    assert "DOC-012" in selected_ids
    assert "DOC-009" not in selected_ids
    assert "DOC-010" not in selected_ids
    assert "DOC-011" not in selected_ids


# ---------------------------------------------------------------------------
# Retours client 2026-06-11 (ticket SELARL dentiste unipersonnelle + cession)
# ---------------------------------------------------------------------------


def _with_cession_updates(ctx: DocumentGenerationContext, **updates) -> DocumentGenerationContext:
    return ctx.model_copy(update={"cession": ctx.cession.model_copy(update=updates)})


def test_descriptif_local_replaces_fixed_sentence(tmp_path: Path) -> None:
    # Ticket 2.5 : descriptif libre rempli -> insere tel quel a la place de la
    # phrase type « Les locaux sont composés d'une pièce de X mètres carrés... ».
    ctx = _context(credit_vendeur=True)
    bail = ctx.cession.bail_professionnel.model_copy(
        update={"descriptif_local": "Les locaux comprennent deux salles de soins et un accueil."}
    )
    ctx = _with_cession_updates(ctx, bail_professionnel=bail)

    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Les locaux comprennent deux salles de soins et un accueil." in text
    assert "mètres carrés" not in text
    _assert_no_residual_tokens(text)


def test_descriptif_local_empty_removes_sentence(tmp_path: Path) -> None:
    # Ticket 2.5 : descriptif vide (et pas de superficie) -> AUCUNE phrase
    # incomplete, paragraphe supprime, generation non bloquee.
    ctx = _context(credit_vendeur=True)
    bail = ctx.cession.bail_professionnel.model_copy(update={"descriptif_local": ""})
    cabinet = ctx.cession.cabinet.model_copy(update={"superficie_local": None})
    ctx = _with_cession_updates(ctx, bail_professionnel=bail, cabinet=cabinet)

    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Les locaux sont composés" not in text
    assert "mètres carrés" not in text
    _assert_no_residual_tokens(text)


def test_descriptif_local_absent_keeps_superficie_behaviour(tmp_path: Path) -> None:
    # Compatibilite scenarios : superficie renseignee sans descriptif -> la
    # phrase type du modele est conservee avec la superficie injectee.
    ctx = _context(credit_vendeur=True)

    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "80 m2 mètres carrés" in text
    _assert_no_residual_tokens(text)


def test_vendeur_celibataire_has_no_marital_remainder(tmp_path: Path) -> None:
    # Vendeur non marie -> le segment « ... sous le régime de ... avec ... » est
    # entierement remplace par la seule situation (aucune phrase incomplete).
    for generator, kwargs, out in (
        (
            ActeCessionCabinetDentaireGenerator(),
            {"type_cabinet": "dentaire", "salaries": _DENT_SALARIES},
            "dent",
        ),
        (ActeCessionCabinetMedicalGenerator(), {"credit_vendeur": True}, "med"),
        (CompromisCessionCabinetMedicalGenerator(), {"etape": "compromis"}, "comp"),
    ):
        ctx = _context(**kwargs)
        vendeur = ctx.cession.vendeur.model_copy(
            update={
                "situation_maritale": "célibataire",
                "regime_matrimonial": None,
                "conjoint": None,
            }
        )
        ctx = _with_cession_updates(ctx, vendeur=vendeur)

        text = _docx_text(generator.generate(ctx, tmp_path / out))

        assert "célibataire." in text
        assert "sous le régime de  " not in text
        assert "avec  " not in text
        _assert_no_residual_tokens(text)


def test_optional_fields_empty_render_blank_zones(tmp_path: Path) -> None:
    # Tickets 2.6 / 2.8 / 3.1 : CA / resultat / loyer / pret vides -> zones a
    # completer a la main, generation NON bloquee, aucun token residuel.
    ctx = _context(etape="compromis")
    cession = ctx.cession.model_copy(
        update={
            "exercices": [
                CessionExercice(periode="2023", chiffre_affaires="", resultat=""),
                CessionExercice(periode="2024", chiffre_affaires="", resultat=""),
                CessionExercice(periode="2025", chiffre_affaires="", resultat=""),
            ],
            "bail_professionnel": ctx.cession.bail_professionnel.model_copy(
                update={"loyer_mensuel": "", "date_bail": None}
            ),
            "financement": ctx.cession.financement.model_copy(
                update={"pret": CessionPret(montant="", taux="", duree="")}
            ),
            "prix": ctx.cession.prix.model_copy(
                update={
                    "elements_corporels": "",
                    "elements_corporels_lettres": "",
                    "elements_incorporels": "",
                    "elements_incorporels_lettres": "",
                }
            ),
        }
    )
    ctx = ctx.model_copy(update={"cession": cession})

    text = _docx_text(CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    _assert_no_residual_tokens(text)
    # Le prix total (strict necessaire) reste rendu.
    assert "300 000" in text


def test_compromis_title_fixed_and_all_ca_years(tmp_path: Path) -> None:
    # Retours Albane lot 2 §9.6 : le mot « DATE » du titre ne doit plus etre
    # remplace par une date (token [date_origine_propriete] retire du TITRE du
    # modele source, conserve au corps pour l'origine de propriete).
    # §9.4 : les 3 exercices de CA doivent TOUS apparaitre (le modele dupliquait
    # l'annee 1 = 210 000 et omettait l'annee 2 = 220 000).
    ctx = _context(etape="compromis")
    text = _docx_text(CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path))
    assert "DATE PREVUE DE REALISATION" in text
    assert "210 000" in text
    assert "220 000" in text  # annee 2 : etait perdue avant le fix du modele
    assert "230 000" in text
    _assert_no_residual_tokens(text)


def test_acte_medical_scm_clause_removed_when_inactive(tmp_path: Path) -> None:
    # Pas de reprise de parts SCM -> la clause « De céder les ... parts sociales »
    # est supprimee de l'acte medical (paragraphe ancre par token).
    ctx = _context(credit_vendeur=True)
    ctx = _with_cession_updates(ctx, scm=CessionScm(actif=False, nb_parts_a_ceder=None))

    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "parts sociales lui appartenant au sein de la Société civile de Moyens" not in text
    _assert_no_residual_tokens(text)


def test_compromis_dentaire_renders_pret_taux_and_duree(tmp_path: Path) -> None:
    # Retour Rafael 2026-06-11 : le compromis dentaire expose desormais le taux
    # ET la duree du pret (variable absente du modele source d'origine, calquee
    # sur le compromis medical). Rempli -> injecte ; aucun token residuel.
    ctx = _context(etape="compromis", type_cabinet="dentaire")
    ctx = _with_cession_updates(
        ctx,
        financement=ctx.cession.financement.model_copy(
            update={"pret": CessionPret(montant="280 000", taux="4 %", duree="sept ans")}
        ),
    )

    text = _docx_text(CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "au taux maximum de 4 % l’an hors assurance" in text
    assert "amortissable sur une période minimum de sept ans" in text
    _assert_no_residual_tokens(text)


def test_compromis_dentaire_pret_taux_vide_ne_bloque_pas(tmp_path: Path) -> None:
    # Ticket 3.1 : taux / duree du pret vides -> zone a completer a la main,
    # generation NON bloquee, aucun token residuel.
    ctx = _context(etape="compromis", type_cabinet="dentaire")
    ctx = _with_cession_updates(
        ctx,
        financement=ctx.cession.financement.model_copy(
            update={"pret": CessionPret(montant="280 000", taux="", duree="")}
        ),
    )

    text = _docx_text(CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    _assert_no_residual_tokens(text)
    assert "au taux maximum de" in text


# ---------------------------------------------------------------------------
# Retours Albane 2026-06-17b — Compromis de cession (sections 9.x)
# ---------------------------------------------------------------------------


def test_compromis_dentaire_strips_word_comments(tmp_path: Path) -> None:
    # 9.3 : le modele dentaire embarque des commentaires Word (annotations de
    # relecture Albane). Le document genere ne doit en porter AUCUN.
    ctx = _context(etape="compromis", type_cabinet="dentaire")
    out = CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)

    parts = _docx_part_names(out)
    assert not any("comment" in name.lower() for name in parts)

    doc_xml = _docx_document_xml(out)
    assert "commentReference" not in doc_xml
    assert "commentRangeStart" not in doc_xml
    assert "commentRangeEnd" not in doc_xml


def test_compromis_medical_has_no_comments_noop(tmp_path: Path) -> None:
    # 9.3 (garde-fou) : le modele medical ne porte aucun commentaire ; le strip
    # est un no-op et ne casse rien.
    ctx = _context(etape="compromis", type_cabinet="medical")
    out = CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path)

    parts = _docx_part_names(out)
    assert not any("comment" in name.lower() for name in parts)
    _assert_no_residual_tokens(_docx_text(out))


def test_compromis_dentaire_filled_fields_lose_highlight(tmp_path: Path) -> None:
    # 9.1 : un champ rempli par une vraie valeur perd le surlignage jaune du
    # modele. Tous champs renseignes -> AUCUN run surligne ne doit subsister.
    ctx = _context(etape="compromis", type_cabinet="dentaire")
    out = CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)

    highlighted = _docx_highlighted_run_texts(out)
    # Aucun run rempli (texte non vide) ne reste surligne.
    assert [t for t in highlighted if t.strip()] == []


def test_compromis_dentaire_empty_optional_field_keeps_highlight(tmp_path: Path) -> None:
    # 9.1 : une zone laissee VIDE volontairement (option non saisie, ex.
    # telephone) GARDE le surlignage jaune (mention a completer a la main).
    ctx = _context(etape="compromis", type_cabinet="dentaire")
    cabinet = ctx.cession.cabinet.model_copy(update={"telephone": None})
    ctx = _with_cession_updates(ctx, cabinet=cabinet)
    out = CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)

    highlighted = _docx_highlighted_run_texts(out)
    # Le seul run surligne restant est la zone vide a completer (telephone).
    assert [t for t in highlighted if t.strip()] == []
    assert any(t == "" for t in highlighted)


def _representee_line(path: Path) -> str:
    for text in _docx_paragraph_texts(path):
        if "Représentée par" in text:
            return text
    raise AssertionError("paragraphe « Représentée par » introuvable")


@pytest.mark.parametrize(
    ("generator", "type_cabinet"),
    [
        (CompromisCessionCabinetDentaireGenerator(), "dentaire"),
        (CompromisCessionCabinetMedicalGenerator(), "medical"),
    ],
)
def test_compromis_representee_uses_representant_with_civil_title(
    generator,
    type_cabinet: str,
    tmp_path: Path,
) -> None:
    # 9.2 : « Représentée par son <fonction>, ... » doit nommer le REPRESENTANT
    # (Alice Moreau), pas le vendeur (Jean Durand), avec un titre CIVIL (Mme),
    # jamais « Docteur ».
    ctx = _context(
        etape="compromis", type_cabinet=type_cabinet, representant_genre=Gender.FEMININ
    )
    line = _representee_line(generator.generate(ctx, tmp_path))

    assert "Mme Alice Moreau" in line
    assert "Docteur" not in line
    assert "Jean Durand" not in line  # plus le vendeur (bug modele dentaire)
    # L'accord en genre de la societe (« domiciliée ») reste correct.
    assert "domiciliée en cette qualité" in line


def test_compromis_representee_masculin_uses_m_title(tmp_path: Path) -> None:
    # 9.2 : representant masculin -> « M. » (jamais « Docteur »).
    ctx = _context(
        etape="compromis", type_cabinet="dentaire", representant_genre=Gender.MASCULIN
    )
    line = _representee_line(
        CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)
    )

    assert "M. Alice Moreau" in line
    assert "Docteur" not in line
    assert "domicilié en cette qualité" in line


def test_acte_dentaire_representee_unchanged(tmp_path: Path) -> None:
    # 9.2 hors perimetre : l'acte n'est PAS touche par le correctif compromis.
    ctx = _context(type_cabinet="dentaire", salaries=_DENT_SALARIES)
    line = _representee_line(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    # L'acte conserve son comportement d'origine (modele « sa <fonction> »).
    assert "Représentée par sa" in line


def _signature_line(path: Path) -> str:
    for text in _docx_paragraph_texts(path):
        if "\t" in text and ("Durand" in text or "Moreau" in text):
            return text
    raise AssertionError("ligne de signature introuvable")


@pytest.mark.parametrize(
    ("generator", "type_cabinet"),
    [
        (CompromisCessionCabinetDentaireGenerator(), "dentaire"),
        (CompromisCessionCabinetMedicalGenerator(), "medical"),
    ],
)
def test_compromis_signatories_cedant_then_societe(
    generator,
    type_cabinet: str,
    tmp_path: Path,
) -> None:
    # 9.8 : 1er signataire = cedant (vendeur) ; 2e = la SEL acquereur (societe),
    # plus deux fois la meme personne « Dr ».
    ctx = _context(etape="compromis", type_cabinet=type_cabinet)
    line = _signature_line(generator.generate(ctx, tmp_path))

    left, _, right = line.partition("\t")
    right = right.strip()
    # Gauche = le cedant (vendeur).
    assert left.strip() == "Docteur Jean Durand"
    # Droite = la societe acquereur (denomination + representant civil), pas une
    # 2e personne physique « Docteur ».
    assert right.startswith("Pour la SELARL CABINET DURAND")
    assert "Mme Alice Moreau" in right
    # Pas de denomination doublee (« SELARL SELARL »).
    assert "SELARL SELARL" not in right
    # Les deux signataires sont DISTINCTS.
    assert left.strip() != right


@pytest.mark.parametrize(
    ("generator", "type_cabinet"),
    [
        (CompromisCessionCabinetDentaireGenerator(), "dentaire"),
        (CompromisCessionCabinetMedicalGenerator(), "medical"),
    ],
)
def test_compromis_pages_count_is_eight_not_twenty(
    generator,
    type_cabinet: str,
    tmp_path: Path,
) -> None:
    # 9.9 : le compromis fige « huit pages » (longueur reelle ~8) et non plus
    # le placeholder « vingt » herite de la constante front.
    ctx = _context(etape="compromis", type_cabinet=type_cabinet)
    text = _docx_text(generator.generate(ctx, tmp_path))

    assert "Sur huit pages." in text
    assert "vingt pages" not in text


def test_acte_pages_count_unchanged(tmp_path: Path) -> None:
    # 9.9 hors perimetre : l'acte conserve la valeur du contexte (non mappee).
    ctx = _context(credit_vendeur=True)
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Sur vingt pages." in text
