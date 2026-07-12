from __future__ import annotations

import re
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


@pytest.mark.parametrize(
    ("generator", "etape", "type_cabinet"),
    [
        (ActeCessionCabinetMedicalGenerator(), "acte", "medical"),
        (ActeCessionCabinetDentaireGenerator(), "acte", "dentaire"),
        (CompromisCessionCabinetMedicalGenerator(), "compromis", "medical"),
        (CompromisCessionCabinetDentaireGenerator(), "compromis", "dentaire"),
    ],
)
def test_r9_clause_ordre_porte_departement_du_vendeur(
    generator, etape: str, type_cabinet: str, tmp_path: Path
) -> None:
    # R9 (Albane 2026-07-07) : la clause « communiqué au Conseil départemental de l’Ordre »
    # nomme le departement de l'Ordre du VENDEUR en NOM avec la preposition correcte
    # (« de Paris » sur la fixture ; numero « 77 » -> « de Seine-et-Marne »). Le segment
    # existe dans les 4 modeles (actes ET compromis) -> propagation a toutes les variantes.
    ctx = _context(etape=etape, type_cabinet=type_cabinet)
    text = _docx_text(generator.generate(ctx, tmp_path))
    assert "communiqué au Conseil départemental de l’Ordre de Paris en vue" in text
    assert "de l’Ordre en vue" not in text  # plus jamais la clause nue sans departement

    ctx2 = _context(etape=etape, type_cabinet=type_cabinet)
    ctx2.cession.vendeur.ordre_departemental = "77"
    text2 = _docx_text(generator.generate(ctx2, tmp_path / "dep77"))
    assert "communiqué au Conseil départemental de l’Ordre de Seine-et-Marne en vue" in text2


def test_o24_14_compromis_genere_meme_si_cession_etape_acte(tmp_path: Path) -> None:
    # O24-14 (onglet 24) : en SELAS l'acte ET le compromis sont produits ENSEMBLE, donc le
    # compromis est généré alors que cession.etape est forcée à 'acte'. Avant le fix,
    # _validate_selection levait « cession.etape doit etre compromis pour compromis_... ».
    # Le document est piloté par le VARIANT (variant.etape), pas par cession.etape.
    # re-Akainu 2026-06-23 (MINEUR O24-14) : on prouve le « À LA FOIS » du verbatim — acte ET
    # compromis générés depuis le MÊME contexte (cession.etape='acte'), chacun avec son contenu
    # propre (le compromis porte le financement : montant du prêt) et sans token résiduel.
    ctx = _context(etape="acte", type_cabinet="dentaire")
    acte_path = ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path)
    compromis_path = CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)
    assert acte_path == tmp_path / "acte_cession_cabinet_dentaire.docx"
    assert compromis_path == tmp_path / "compromis_cession_cabinet_dentaire.docx"
    assert acte_path.exists() and compromis_path.exists()
    compromis_text = _docx_text(compromis_path)
    assert "240 000" in compromis_text  # montant du prêt (CessionPret), propre au financement
    _assert_no_residual_tokens(compromis_text)


def test_o24_14_compromis_tolere_salaries_partages_avec_acte(tmp_path: Path) -> None:
    # re-Akainu tour 2 (MAJEUR O24-14) : en SELAS, l'acte ET le compromis partagent UN SEUL
    # contexte. Si l'acte dentaire porte des salariés repris (clause propre à l'acte), le
    # compromis recoit le même contexte → il doit les IGNORER, pas lever. Avant le fix,
    # _validate_salaries crashait le compromis → tout le bundle « acte + compromis » échouait.
    ctx = _context(
        etape="acte",
        type_cabinet="dentaire",
        salaries=[
            CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit"),
            CessionSalarie(civilite_affichage="Monsieur", prenom="Noe", nom="Robert"),
        ],
    )
    # l'acte rend la clause salariés ; le compromis ne doit PAS lever malgré les salariés.
    acte_path = ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path)
    compromis_path = CompromisCessionCabinetDentaireGenerator().generate(ctx, tmp_path)
    assert acte_path.exists() and compromis_path.exists()
    acte_text = _docx_text(acte_path)
    assert "Petit" in acte_text and "Robert" in acte_text  # clause salariés sur l'acte
    _assert_no_residual_tokens(_docx_text(compromis_path))


def test_o24_11_acte_retranscrit_regime_et_conjoint_du_vendeur(tmp_path: Path) -> None:
    # re-Akainu tour 2 (MINEUR O24-11) : preuve END-TO-END (DOCX) que le verbatim « toutes les
    # informations du vendeur retranscrites » est honoré dans l'acte — régime matrimonial ET
    # conjoint présents, sans artefact « Marie(e) » du libellé brut ni token résiduel. (Le
    # branchement SELAS context-building — valeur collapsée pour l'affichage, libellé brut pour
    # le régime — est verrouillé par le test unitaire de dissociation situation/régime.)
    ctx = _context()  # vendeur marié (communauté réduite), conjoint Madame Claire Durand
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))
    assert "Claire Durand" in text  # conjoint du vendeur retranscrit dans l'acte
    assert "communaute reduite aux acquets" in text  # régime matrimonial retranscrit (fixture)
    # pas d'artefact du LIBELLE BRUT du menu situation (« Marie(e) sous le regime ... » doublé) :
    assert "Marié(e)" not in text
    assert text.count("sous le régime") <= 1  # régime jamais doublé (« ... régime ... régime ... »)
    _assert_no_residual_tokens(text)


def test_acte_medical_blocks_without_medical_bail_validation(tmp_path: Path) -> None:
    ctx = _context(
        validations=CessionValidations(
            mentions_bail_medical_validees=False,
            ligne_contrats_travail_medical_supprimee=True,
        ),
    )

    with pytest.raises(ValueError, match="mentions_bail_medical_validees"):
        ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path)


def test_compromis_tolere_credit_vendeur_du_contexte_partage(tmp_path: Path) -> None:
    # re-Akainu tour 5 (BLOQUANT O24-14) : en SELAS, l'acte ET le compromis sont generes
    # ENSEMBLE depuis UN SEUL contexte. Un credit-vendeur actif (clause PROPRE a l'acte medical)
    # ne doit PAS faire lever le COMPROMIS qui partage ce contexte -> il l'IGNORE (sa garde ne
    # s'applique qu'au variant acte medical qui rend reellement la clause). Avant le fix, le
    # compromis levait et cassait tout le bundle. (Ancien test qui asserait la levee = retire :
    # il codait une regle contraire au verbatim « acte ET compromis ensemble ».)
    ctx = _context(etape="acte", credit_vendeur=True)  # contexte d'acte porteur, partage
    compromis = CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path)
    assert compromis.exists()
    _assert_no_residual_tokens(_docx_text(compromis))


def test_o24_14_bundle_medical_acte_et_compromis_avec_credit_vendeur_et_scm(
    tmp_path: Path,
) -> None:
    # O24-14 (re-Akainu T5, MAJEUR — preuve de BUNDLE manquante) : en SELAS l'ACTE (DOC-009)
    # ET le COMPROMIS (DOC-010) du cabinet MEDICAL sont generes ENSEMBLE depuis UN SEUL contexte.
    # Ce contexte porte des champs PROPRES a l'acte medical — credit-vendeur ET clause SCM, tous
    # deux ACTIFS ici — que le compromis ne rend pas. Le bundle ne doit PAS lever : le compromis
    # IGNORE ces champs (garde restreinte au variant acte medical, _validate_financement). Avant
    # le fix (commit 01eaa27), le compromis levait sur credit_vendeur/scm -> tout le bundle
    # crashait. On genere les DEUX depuis le MEME contexte, dans le meme tmp_path.
    ctx = _context(etape="acte", type_cabinet="medical", credit_vendeur=True)
    # Sanity : le contexte porte bien les deux clauses propres a l'acte, actives.
    assert ctx.cession.financement.credit_vendeur.actif is True
    assert ctx.cession.scm.actif is True

    acte_path = ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path)
    compromis_path = CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path)

    assert acte_path == tmp_path / "acte_cession_cabinet_medical.docx"
    assert compromis_path == tmp_path / "compromis_cession_cabinet_medical.docx"
    assert acte_path.exists() and compromis_path.exists()

    acte_text = _docx_text(acte_path)
    compromis_text = _docx_text(compromis_path)
    # L'ACTE rend bien les clauses propres (SCM : nb de parts ; credit-vendeur : duree en annees).
    assert "10" in acte_text  # nb_parts_scm_a_ceder rendu dans l'acte
    assert "trois" in acte_text.casefold()  # duree credit-vendeur (« trois » ans)
    # Aucun token residuel sur AUCUN des deux documents du bundle.
    _assert_no_residual_tokens(acte_text)
    _assert_no_residual_tokens(compromis_text)


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
        # Sujet = vendeur, pas l'acquereur (Alice Moreau). Rafael 2026-07-09 « supprimer
        # partout » : civilite CIVILE (« Monsieur Jean Durand »), plus « Docteur ».
        assert "Monsieur Jean Durand est propriétaire des éléments constitutifs du cabinet" in text
        assert "Docteur" not in text
        # A26-33 (Albane 2026-06-26) : jour sur 2 chiffres (« 01 janvier », pas « 1 janvier »).
        assert "pour l’avoir régulièrement créé le 01 janvier 2020." in text
        assert "Alice Moreau est propriétaire" not in text
        _assert_no_residual_tokens(text)


def test_origine_propriete_purchased_describes_vendeur(tmp_path: Path) -> None:
    # FIX 1 : variante « achete » -> origine via achat anterieur du vendeur.
    ctx = _context(credit_vendeur=True)
    ctx.cession.cabinet.origine_propriete_mode = "achete"
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    # Rafael 2026-07-09 « supprimer partout » : civilite CIVILE, plus « Docteur ».
    assert "Monsieur Jean Durand est propriétaire des éléments constitutifs du cabinet" in text
    assert "pour les avoir régulièrement acquis auprès de Monsieur Paul Bernard" in text
    assert "Docteur" not in text
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
    # Verbatim Albane (IMG_7837) : 1 salarie -> « LE CONTRAT » (singulier) + profession
    # rendue par « , <profession> » (PAS « en qualite de » : « sans aucun mot de plus »).
    ctx = _context(
        type_cabinet="dentaire",
        salaries=[
            CessionSalarie(
                civilite_affichage="Madame", prenom="Lea", nom="Petit", poste="assistante dentaire"
            )
        ],
    )

    text = _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))

    assert "De reprendre le contrat de travail de Madame Lea Petit, assistante dentaire." in text
    assert "en qualité de" not in text
    assert "les contrats de travail" not in text  # singulier pour 1 salarie
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

    assert "Madame Lea Petit ; Monsieur Noe Robert et de Madame Ines Faure" in text
    _assert_no_residual_tokens(text)


def test_acte_dentaire_salary_requires_complete_identity(tmp_path: Path) -> None:
    # Garde-fou : un salarie liste doit avoir civilite/prenom/nom (identite complete).
    ctx = _context(
        type_cabinet="dentaire",
        salaries=[CessionSalarie(civilite_affichage="Madame", prenom="Lea")],
    )

    with pytest.raises(ValueError, match="salaries"):
        ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path)


# ---------------------------------------------------------------------------
# R5-contrats (verbatim Albane IMG_7837, 2026-06-29) : clause de reprise des contrats
# de travail rendue EN PLACE a sa position du modele = POINT 3, APRES « De payer tous
# frais... », sur l'acte MEDICAL ET DENTAIRE. Accord singulier/pluriel sur « contrat »,
# profession « , <profession> » (sans « en qualite de »), conditionnelle au nb de salaries.
# ---------------------------------------------------------------------------

_R5_GENERATORS = {
    "medical": ActeCessionCabinetMedicalGenerator,
    "dentaire": ActeCessionCabinetDentaireGenerator,
}


def _r5_paragraphs(type_cabinet: str, salaries, tmp_path: Path) -> list[str]:
    ctx = _context(type_cabinet=type_cabinet, salaries=salaries)
    out = _R5_GENERATORS[type_cabinet]().generate(ctx, tmp_path)
    document = Document(out)
    return [p.text for p in document.paragraphs]


def _index_of(paras: list[str], needle: str) -> int | None:
    return next((i for i, t in enumerate(paras) if needle in t), None)


@pytest.mark.parametrize("type_cabinet", ["medical", "dentaire"])
def test_r5_clause_after_payer_frais_two_salaries(type_cabinet: str, tmp_path: Path) -> None:
    # Verbatim Albane : 2 salaries -> « les contrats » (pluriel), joints par « et de »,
    # clause au POINT 3 = APRES « De payer tous frais » (et avant la section suivante).
    paras = _r5_paragraphs(type_cabinet, _DENT_SALARIES, tmp_path)
    idx_payer = _index_of(paras, "De payer tous frais")
    idx_clause = _index_of(paras, "De reprendre les contrats de travail")
    assert idx_payer is not None
    assert idx_clause is not None
    # Point 3 : juste APRES « De payer tous frais » (a un blanc pres du modele).
    assert idx_payer < idx_clause <= idx_payer + 2
    assert (
        paras[idx_clause]
        == "De reprendre les contrats de travail de Madame Lea Petit et de Monsieur Noe Robert."
    )


@pytest.mark.parametrize("type_cabinet", ["medical", "dentaire"])
def test_r5_clause_absent_when_zero_salaries(type_cabinet: str, tmp_path: Path) -> None:
    # 0 salarie repris -> clause ABSENTE (ni a l'ancien emplacement, ni au nouveau),
    # aucun token residuel, aucune phrase incomplete heritee du modele.
    paras = _r5_paragraphs(type_cabinet, [], tmp_path)
    full = "\n".join(p for p in paras if p)
    assert "De reprendre les contrats de travail" not in full
    assert "[clause_reprise_salaries]" not in full
    assert "[" not in full and "]" not in full


@pytest.mark.parametrize("type_cabinet", ["medical", "dentaire"])
def test_r5_clause_single_salary(type_cabinet: str, tmp_path: Path) -> None:
    # Verbatim Albane : 1 salarie -> « LE CONTRAT » (singulier), sans « et de », point 3.
    salaries = [CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit")]
    paras = _r5_paragraphs(type_cabinet, salaries, tmp_path)
    idx_payer = _index_of(paras, "De payer tous frais")
    idx_clause = _index_of(paras, "De reprendre le contrat de travail")
    assert idx_payer is not None and idx_clause is not None
    assert idx_payer < idx_clause <= idx_payer + 2
    assert paras[idx_clause] == "De reprendre le contrat de travail de Madame Lea Petit."
    assert " et de " not in paras[idx_clause]
    assert "les contrats de travail" not in "\n".join(paras)  # singulier pour 1 salarie


@pytest.mark.parametrize("type_cabinet", ["medical", "dentaire"])
def test_r5_clause_three_salaries_joined(type_cabinet: str, tmp_path: Path) -> None:
    # N salaries -> tous listes, separes par « , » et le dernier par « et de ».
    salaries = [
        CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit"),
        CessionSalarie(civilite_affichage="Monsieur", prenom="Noe", nom="Robert"),
        CessionSalarie(civilite_affichage="Madame", prenom="Ines", nom="Faure"),
    ]
    paras = _r5_paragraphs(type_cabinet, salaries, tmp_path)
    idx_clause = _index_of(paras, "De reprendre les contrats de travail")
    # Separateur « ; » entre salaries (Akainu m1) : non ambigu vis-a-vis de la virgule interne.
    assert paras[idx_clause] == (
        "De reprendre les contrats de travail de Madame Lea Petit ; "
        "Monsieur Noe Robert et de Madame Ines Faure."
    )


@pytest.mark.parametrize("type_cabinet", ["medical", "dentaire"])
def test_r5_clause_three_salaries_with_profession_unambiguous(
    type_cabinet: str, tmp_path: Path
) -> None:
    # Akainu m1/n1 (2026-06-29) : le CAS NOMINAL du verbatim = salarie « <identite>, <profession> ».
    # A N>=3 avec profession, le separateur entre salaries doit rester non ambigu (« ; »), sinon la
    # virgule de profession et la virgule de separation se confondent. Format multi-salaries =
    # INTERIM a confirmer Albane (QUESTIONS_RAFAEL R5).
    salaries = [
        CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit", poste="juriste"),
        CessionSalarie(
            civilite_affichage="Monsieur", prenom="Noe", nom="Robert", poste="assistant dentaire"
        ),
        CessionSalarie(
            civilite_affichage="Madame", prenom="Ines", nom="Faure", poste="secretaire"
        ),
    ]
    paras = _r5_paragraphs(type_cabinet, salaries, tmp_path)
    idx_clause = _index_of(paras, "De reprendre les contrats de travail")
    assert paras[idx_clause] == (
        "De reprendre les contrats de travail de Madame Lea Petit, juriste ; "
        "Monsieur Noe Robert, assistant dentaire et de Madame Ines Faure, secretaire."
    )
    # Aucune virgule de separation inter-salaries (seules les virgules nom/profession subsistent).
    assert "en qualité de" not in paras[idx_clause]


@pytest.mark.parametrize("type_cabinet", ["medical", "dentaire"])
def test_r5_clause_not_duplicated(type_cabinet: str, tmp_path: Path) -> None:
    # Clause rendue EN PLACE (token/ligne statique du modele) -> elle n'apparait QU'UNE
    # fois, aucun doublon.
    paras = _r5_paragraphs(type_cabinet, _DENT_SALARIES, tmp_path)
    occurrences = [i for i, t in enumerate(paras) if "De reprendre les contrats de travail" in t]
    assert len(occurrences) == 1


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


def test_acte_medical_selarl_acquereur_keeps_selarl_au_capital(tmp_path: Path) -> None:
    # Verrou SYMETRIQUE de la correction d18c0fd (override segment « SELARL au capital de »
    # -> « [forme_sociale_acquereur] au capital de »). La face SELAS (ABSENCE de « SELARL au
    # capital de ») est testee dans test_multi_type_front.py:2493 ; ici on verrouille la face
    # SELARL : pour un acquereur SELARL (cf. _context, forme_sociale="SELARL") le token doit se
    # remplir « SELARL » -> la ligne de forme ressort « SELARL au capital de » (byte-identique au
    # modele source d'origine = claim « gold intact » de d18c0fd). Sans ce test, l'override
    # pourrait casser le rendu SELARL sans qu'aucun test ne le signale.
    text = _docx_text(
        ActeCessionCabinetMedicalGenerator().generate(
            _context(credit_vendeur=True),
            tmp_path,
        )
    )

    assert "SELARL au capital de" in text, (
        "acquereur SELARL : la ligne de forme doit ressortir « SELARL au capital de » "
        "(fidelite gold, symetrique du test d'absence SELAS)"
    )
    _assert_no_residual_tokens(text)


def test_compromis_titre_inscription_reflete_forme_acquereur(tmp_path: Path) -> None:
    # O24-fidelite-SELARL #2 (Albane/Rafael 2026-07-01, « comme les modeles ») : le titre de
    # clause « Inscription de la SELARL au Tableau » des 2 compromis (medical + dentaire) doit
    # refleter la VRAIE forme de l'acquereur (token [forme_sociale_acquereur], comme ses modeles
    # « transforme »). Acquereur SELARL -> « SELARL » (byte-identique au gold). Acquereur SELAS
    # -> « SELAS » (plus de « SELARL » parasite). Teste les 2 faces sur les 2 compromis.
    for generator, cabinet in (
        (CompromisCessionCabinetMedicalGenerator(), "medical"),
        (CompromisCessionCabinetDentaireGenerator(), "dentaire"),
    ):
        # Face SELARL (defaut) : titre byte-identique au modele source.
        ctx_selarl = _context(etape="compromis", type_cabinet=cabinet)
        text_selarl = _docx_text(generator.generate(ctx_selarl, tmp_path / f"{cabinet}-selarl"))
        assert "Inscription de la SELARL au Tableau" in text_selarl, (
            f"compromis {cabinet} acquereur SELARL : titre « Inscription de la SELARL au "
            "Tableau » attendu (fidelite gold)"
        )

        # Face SELAS : le titre suit la forme reelle de l'acquereur.
        ctx_selas = _context(etape="compromis", type_cabinet=cabinet)
        ctx_selas.cession.acquereur.forme_sociale = "SELAS"
        text_selas = _docx_text(generator.generate(ctx_selas, tmp_path / f"{cabinet}-selas"))
        assert "Inscription de la SELAS au Tableau" in text_selas, (
            f"compromis {cabinet} acquereur SELAS : titre « Inscription de la SELAS au "
            "Tableau » attendu (forme dynamique)"
        )
        assert "Inscription de la SELARL au Tableau" not in text_selas, (
            f"compromis {cabinet} acquereur SELAS : plus de « SELARL » parasite dans le titre"
        )


def test_orchestrator_selects_both_cession_cabinet_documents_for_sel() -> None:
    # MD1 (Albane 2026-07-10) : une cession SEL (SELARL, ici) produit l'ACTE ET le COMPROMIS
    # ENSEMBLE pour le type de cabinet (l'etape n'est plus filtrante, comme la SELAS). Seuls
    # les documents de l'AUTRE type de cabinet restent exclus.
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected_ids = {
        document.doc_id
        for document in orchestrator.select_documents_for_context(
            _context(etape="compromis", type_cabinet="dentaire"),
        )
    }

    # Dentaire : acte (DOC-011) ET compromis (DOC-012) produits ensemble.
    assert "DOC-011" in selected_ids
    assert "DOC-012" in selected_ids
    # Type medical exclu (mauvais type de cabinet).
    assert "DOC-009" not in selected_ids
    assert "DOC-010" not in selected_ids


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


def test_vendeur_pacse_affiche_partenaire(tmp_path: Path) -> None:
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : un vendeur PACSE affiche son PARTENAIRE
    # (« pacsé avec Madame Claire Durand. »), SANS « sous le régime de … » (pas de sous-regime).
    ctx = _context()
    vendeur = ctx.cession.vendeur.model_copy(
        update={"situation_maritale": "pacsé", "regime_matrimonial": None}
    )
    ctx = _with_cession_updates(ctx, vendeur=vendeur)
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))
    assert "pacsé avec Madame Claire Durand." in text
    assert "pacsé sous le régime" not in text
    _assert_no_residual_tokens(text)


def test_vendeur_pacse_sans_partenaire_no_mention(tmp_path: Path) -> None:
    # « Pas de mention sans nom » (Albane 6.3) : un vendeur pacse SANS partenaire -> « pacsé. » nu.
    ctx = _context()
    vendeur = ctx.cession.vendeur.model_copy(
        update={"situation_maritale": "pacsé", "regime_matrimonial": None, "conjoint": None}
    )
    ctx = _with_cession_updates(ctx, vendeur=vendeur)
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))
    assert "pacsé." in text
    assert "pacsé avec" not in text
    assert "Claire Durand" not in text
    assert "COMPLÉTER" not in text
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
    # Gauche = le cedant (vendeur). Rafael 2026-07-09 « supprimer partout » : civilite CIVILE
    # (« Monsieur Jean Durand »), plus « Docteur »/« Dr ».
    assert left.strip() == "Monsieur Jean Durand"
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
def test_compromis_pages_count_is_seven_not_twenty(
    generator,
    type_cabinet: str,
    tmp_path: Path,
) -> None:
    # CE4 (Albane 2026-06-26) : le compromis fige « sept pages » (defaut demande,
    # l'auto-comptage reel etant impossible sans moteur de pagination) et non plus
    # « huit » (retour 9.9 supersede) ni le placeholder « vingt » du front.
    ctx = _context(etape="compromis", type_cabinet=type_cabinet)
    text = _docx_text(generator.generate(ctx, tmp_path))

    assert "Sur sept pages." in text
    assert "Sur huit pages." not in text
    assert "vingt pages" not in text


def test_acte_pages_count_unchanged(tmp_path: Path) -> None:
    # 9.9 hors perimetre : l'acte conserve la valeur du contexte (non mappee).
    ctx = _context(credit_vendeur=True)
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Sur vingt pages." in text


# ---------------------------------------------------------------------------
# Retours Albane 2026-06-26 — LOT « Compromis + Acte de cession » (CE1..CE8)
# ---------------------------------------------------------------------------


def _bold_run_texts(path: Path) -> list[str]:
    document = Document(path)
    texts: list[str] = []

    def _scan(paragraphs) -> None:
        for paragraph in paragraphs:
            for run in paragraph.runs:
                if run.bold and run.text.strip():
                    texts.append(run.text)

    _scan(document.paragraphs)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                _scan(cell.paragraphs)
    return texts


def _identity_paragraph(path: Path) -> tuple[str, list[tuple[str, bool]]]:
    """1er paragraphe d'identite vendeur (« <civ> <prenom> <nom>, ... né... »)."""
    document = Document(path)
    for paragraph in document.paragraphs:
        t = paragraph.text
        # Rafael 2026-07-09 « supprimer partout » : la tete d'identite est civile (« Monsieur »).
        if t.startswith("Monsieur Jean Durand") and ("né" in t or "née" in t):
            runs = [(r.text, bool(r.bold)) for r in paragraph.runs if r.text.strip()]
            return t, runs
    raise AssertionError("paragraphe d'identite vendeur introuvable")


@pytest.mark.parametrize(
    ("generator", "etape", "type_cabinet"),
    [
        # CE1 (nom SEUL en gras) reste vrai sur le COMPROMIS (hors perimetre AC1 2026-07-10).
        # Sur l'ACTE, CE1 est SUPERSEDE par AC1 (designation ENTIERE en gras) —
        # cf. test_ac1_acte_cedant_designation_fully_bold ci-dessous.
        (CompromisCessionCabinetMedicalGenerator(), "compromis", "medical"),
        (CompromisCessionCabinetDentaireGenerator(), "compromis", "dentaire"),
    ],
)
def test_ce1_only_vendeur_name_is_bold(generator, etape, type_cabinet, tmp_path: Path) -> None:
    # CE1 : dans l'identite du vendeur, SEUL le nom (« Durand ») est en gras ;
    # la civilite/prenom (« Monsieur » [R3, ex-« Docteur »], « Jean ») ne le sont PAS.
    salaries = (
        [CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit")]
        if (etape == "acte" and type_cabinet == "dentaire")
        else None
    )
    ctx = _context(etape=etape, type_cabinet=type_cabinet, salaries=salaries)
    out = generator.generate(ctx, tmp_path)

    _, runs = _identity_paragraph(out)
    # Le nom « Durand » est porte par un run gras.
    assert any(is_bold and "Durand" in text for text, is_bold in runs), runs
    # Aucune civilite/prenom en gras dans la zone d'identite (civilite = « Monsieur » depuis
    # R3 « supprimer partout », 2026-07-09 ; « Docteur » ne doit plus apparaitre du tout).
    for text, is_bold in runs:
        if is_bold:
            assert "Monsieur" not in text, f"civilite ne doit pas etre en gras : {text!r}"
            assert "Docteur" not in text, f"« Docteur » eradique : {text!r}"
            assert "Jean" not in text, f"prenom ne doit pas etre en gras : {text!r}"


@pytest.mark.parametrize(
    ("generator", "type_cabinet"),
    [
        (ActeCessionCabinetMedicalGenerator(), "medical"),
        (ActeCessionCabinetDentaireGenerator(), "dentaire"),
    ],
)
def test_ac1_acte_cedant_designation_fully_bold(generator, type_cabinet, tmp_path: Path) -> None:
    # AC1 (Albane 2026-07-10) : sur l'ACTE, la tete de la designation du cedant
    # (« Monsieur Jean Durand ») passe ENTIEREMENT en gras — civilite + prenom + nom — et le
    # RESTE de la ligne (profession, naissance...) reste en maigre. SUPERSEDE CE1 (nom seul) sur
    # l'acte, meme patron que l'acte de cession de parts SPFPL (A2). Le compromis garde CE1.
    salaries = (
        [CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit")]
        if type_cabinet == "dentaire"
        else None
    )
    ctx = _context(etape="acte", type_cabinet=type_cabinet, salaries=salaries)
    text, runs = _identity_paragraph(generator.generate(ctx, tmp_path))

    bold = [t for t, is_bold in runs if is_bold]
    maigre = [t for t, is_bold in runs if not is_bold]
    # Les runs gras couvrent EXACTEMENT « Monsieur Jean Durand » (civilite + prenom + nom).
    assert "".join(bold) == "Monsieur Jean Durand", runs
    # Le reste de la ligne est en maigre (commence par la virgule, porte la profession/naissance).
    assert maigre and maigre[0].startswith(","), runs
    assert "né" in "".join(maigre), runs
    # « Docteur » eradique (R3) et jamais en gras.
    assert "Docteur" not in text


@pytest.mark.parametrize(
    ("generator", "etape", "type_cabinet"),
    [
        (ActeCessionCabinetMedicalGenerator(), "acte", "medical"),
        (CompromisCessionCabinetMedicalGenerator(), "compromis", "medical"),
        # CE2 etendu aux DEUX variants DENTAIRES (Akainu, M3 — siloing regle 68 Q4) :
        # le fix CE2 (plage de dates + « € » apres resultat) doit valoir sur le dentaire
        # exactement comme sur le medical, et les 3 resultats doivent etre DISTINCTS
        # (B2 : le compromis dentaire dupliquait [resultat_1] sur la ligne 2 -> 80 000).
        (ActeCessionCabinetDentaireGenerator(), "acte", "dentaire"),
        (CompromisCessionCabinetDentaireGenerator(), "compromis", "dentaire"),
    ],
)
def test_ce2_exercices_date_range_and_euro_on_resultat(
    generator, etape, type_cabinet, tmp_path: Path
) -> None:
    # CE2 : les exercices saisis en annee seule sont rendus en PLAGE de dates,
    # et le sigle « € » suit les montants de RESULTAT. Verifie sur les 4 variants
    # (medical ET dentaire, acte ET compromis) — le dentaire ne doit pas etre silote.
    salaries = (
        [CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit")]
        if (etape == "acte" and type_cabinet == "dentaire")
        else None
    )
    ctx = _context(etape=etape, type_cabinet=type_cabinet, salaries=salaries)
    text = _docx_text(generator.generate(ctx, tmp_path))

    # Plages de dates : une SEULE par ligne d'exercice (plus de texte fige parasite
    # « Du 01/01/2023 ... du 01/0 » colle devant le token sur l'acte dentaire).
    assert "Du 01/01/2023 au 31/12/2023" in text
    assert "Du 01/01/2024 au 31/12/2024" in text
    assert "Du 01/01/2025 au 31/12/2025" in text
    assert text.count("Du 01/01/2023 au 31/12/2023") == 1
    assert text.count("Du 01/01/2024 au 31/12/2024") == 1
    assert text.count("Du 01/01/2025 au 31/12/2025") == 1
    # Resultats avec euro, et les 3 valeurs DISTINCTES (anti-duplication B2).
    assert "80 000 €" in text
    assert "85 000 €" in text
    assert "90 000 €" in text
    _assert_no_residual_tokens(text)


@pytest.mark.parametrize(
    ("generator", "type_cabinet"),
    [
        (CompromisCessionCabinetMedicalGenerator(), "medical"),
        (CompromisCessionCabinetDentaireGenerator(), "dentaire"),
    ],
)
def test_ce3_promesse_prefixes_le_docteur(generator, type_cabinet, tmp_path: Path) -> None:
    # Rafael 2026-07-09 « supprimer partout » : « le Docteur … » de la section III (promesse)
    # est SUPERSEDE (CE3) -> le cedant y est nomme par sa civilite CIVILE (« Monsieur … »),
    # sans article. « Docteur »/« Dr » ne doit plus apparaitre du tout dans le compromis.
    ctx = _context(etape="compromis", type_cabinet=type_cabinet)
    text = _docx_text(generator.generate(ctx, tmp_path))

    assert "Par les présentes, Monsieur Jean Durand" in text
    assert "s’oblige envers Monsieur Jean Durand" in text
    # Plus aucune trace « Docteur » ni article parasite « le Monsieur ».
    assert "Docteur" not in text
    assert "le Monsieur Jean" not in text


def test_ce3_non_docteur_civilite_untouched(tmp_path: Path) -> None:
    # CE3 borne : si la civilite n'est PAS « Docteur » (ex. « Madame »), on ne
    # prefixe pas « le » (verbatim « lorsqu'il y a docteur »).
    ctx = _context(etape="compromis")
    vendeur = ctx.cession.vendeur.model_copy(update={"civilite_affichage": "Madame"})
    ctx = _with_cession_updates(ctx, vendeur=vendeur)
    text = _docx_text(CompromisCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Par les présentes, Madame Jean Durand" in text
    assert "le Madame" not in text


@pytest.mark.parametrize(
    ("generator", "type_cabinet"),
    [
        (CompromisCessionCabinetMedicalGenerator(), "medical"),
        (CompromisCessionCabinetDentaireGenerator(), "dentaire"),
    ],
)
def test_ce4_compromis_default_seven_pages(generator, type_cabinet, tmp_path: Path) -> None:
    # CE4 : le compromis affiche « sept pages » par defaut (et non « huit »).
    ctx = _context(etape="compromis", type_cabinet=type_cabinet)
    text = _docx_text(generator.generate(ctx, tmp_path))

    assert "Sur sept pages." in text
    assert "huit pages" not in text


def test_ce5_credit_vendeur_active_removes_redaction_note(tmp_path: Path) -> None:
    # CE5 : credit-vendeur actif -> la mention de redaction « Ajouter en cas de CV : »
    # est retiree, la clause credit-vendeur restant presente.
    ctx = _context(credit_vendeur=True)
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "Ajouter en cas de CV" not in text
    assert "crédit-vendeur à hauteur de 60 000" in text
    _assert_no_residual_tokens(text)


def test_r5_contrats_medical_clause_no_longer_highlighted(tmp_path: Path) -> None:
    # R5-contrats (Rafael 2026-06-29) SUPERSEDE CE6 : le passage « contrats de
    # travail » de l'acte medical n'est plus une zone surlignee a completer a la
    # main, mais une clause GENEREE (cf. tests R5 ci-dessous). Avec des salaries
    # repris, la clause est presente mais AUCUN run ne doit rester surligne (champ
    # rempli, pas zone a completer).
    ctx = _context(type_cabinet="medical", salaries=_DENT_SALARIES)
    out = ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path)

    highlighted = _docx_highlighted_run_texts(out)
    assert not any("contrats de travail" in t for t in highlighted)


def test_ce7_no_extra_blank_after_affirmation_sincerite(tmp_path: Path) -> None:
    # CE7 : un seul paragraphe vide entre l'affirmation de sincerite et la section
    # suivante (plus d'espaces surnumeraires).
    ctx = _context(credit_vendeur=True)
    out = ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path)

    paras = _docx_paragraph_texts(out)
    prefix = "Les parties affirment sous les peines"
    anchor = next(i for i, t in enumerate(paras) if t.strip().startswith(prefix))
    empties = 0
    j = anchor + 1
    while j < len(paras) and not paras[j].strip():
        empties += 1
        j += 1
    assert empties == 1, f"attendu 1 paragraphe vide, trouve {empties}"


def test_ce8_point8_scm_clause_when_scm_active(tmp_path: Path) -> None:
    # CE8 : avec une SCM, le point 8 porte la clause « De céder l'intégralité des
    # parts qu'il détient de la SCM <denomination> » et le « De maintenir le cabinet
    # médical dans son état actuel... » est RETIRE.
    ctx = _context(credit_vendeur=True)
    ctx = _with_cession_updates(
        ctx, scm=CessionScm(actif=True, nb_parts_a_ceder="10", denomination="CMS DU PARC")
    )
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "De céder l’intégralité des parts qu’il détient de la SCM CMS DU PARC" in text
    assert "De maintenir le cabinet médical dans son état actuel" not in text
    # Ancien wording (nombre de parts) disparu.
    assert "parts sociales lui appartenant au sein de la Société civile de Moyens" not in text
    _assert_no_residual_tokens(text)


def test_ce8_without_scm_keeps_maintenir_and_drops_scm_clause(tmp_path: Path) -> None:
    # CE8 borne : sans SCM, la clause SCM (point 8) est supprimee et le « De
    # maintenir le cabinet médical... » (point 9) reste.
    ctx = _context(credit_vendeur=True)
    ctx = _with_cession_updates(ctx, scm=CessionScm(actif=False, nb_parts_a_ceder=None))
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "détient de la SCM" not in text
    assert "De maintenir le cabinet médical dans son état actuel" in text
    _assert_no_residual_tokens(text)


def test_ce8_scm_denomination_empty_renders_blank_zone(tmp_path: Path) -> None:
    # CE8 : SCM active sans denomination -> zone vide a completer a la main, jamais
    # bloquant ni token residuel.
    ctx = _context(credit_vendeur=True)
    ctx = _with_cession_updates(
        ctx, scm=CessionScm(actif=True, nb_parts_a_ceder="10", denomination=None)
    )
    text = _docx_text(ActeCessionCabinetMedicalGenerator().generate(ctx, tmp_path))

    assert "De céder l’intégralité des parts qu’il détient de la SCM" in text
    _assert_no_residual_tokens(text)


# ---------------------------------------------------------------------------
# Retours Albane 2026-07-10 — ACTE CESSION CABINET (dentaire) : AC1..AC5
# ---------------------------------------------------------------------------

_AC_DENT_SALARIES = [CessionSalarie(civilite_affichage="Madame", prenom="Lea", nom="Petit")]


def _ac_dentaire_acte_text(tmp_path: Path, **cabinet_updates) -> str:
    ctx = _context(type_cabinet="dentaire", salaries=_AC_DENT_SALARIES)
    for key, value in cabinet_updates.items():
        setattr(ctx.cession.cabinet, key, value)
    return _docx_text(ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path))


def test_ac2_acte_dentaire_origine_cree(tmp_path: Path) -> None:
    # AC2 (verbatim O1) : cabinet CREE (origine_propriete_mode="cree") -> clause
    # « ... est propriétaire des éléments constitutifs du cabinet pour les avoir régulièrement
    # créés le <date>. » (a la place de la clause « acquis » figee du modele dentaire).
    text = _ac_dentaire_acte_text(tmp_path, origine_propriete_mode="cree")
    assert (
        "Monsieur Jean Durand est propriétaire des éléments constitutifs du cabinet "
        "pour les avoir régulièrement créés le 01 janvier 2020." in text
    )
    assert "acquis auprès de" not in text  # la clause « acquis » a bien ete remplacee
    _assert_no_residual_tokens(text)


def test_ac2_acte_dentaire_origine_acquis_default(tmp_path: Path) -> None:
    # AC2 : mode absent (defaut) -> clause « acquis » du modele CONSERVEE (byte-fidele au gold).
    text = _ac_dentaire_acte_text(tmp_path)  # origine_propriete_mode = None
    assert (
        "Monsieur Jean Durand est propriétaire des éléments constitutifs du cabinet "
        "pour les avoir régulièrement acquis auprès de Monsieur Paul Bernard, "
        "le 01 janvier 2020 au prix de 120 000 euros." in text
    )
    assert "créés le" not in text
    _assert_no_residual_tokens(text)


def test_ac2_acte_dentaire_origine_achete_explicit_keeps_model(tmp_path: Path) -> None:
    # AC2 : mode "achete" explicite -> meme clause « acquis » du modele (aucune bascule « cree »).
    text = _ac_dentaire_acte_text(tmp_path, origine_propriete_mode="achete")
    assert "pour les avoir régulièrement acquis auprès de Monsieur Paul Bernard" in text
    assert "créés le" not in text
    _assert_no_residual_tokens(text)


def test_ac3_acte_dentaire_no_residual_word_revision(tmp_path: Path) -> None:
    # AC3 : le modele dentaire acte porte une revision Word residuelle (« Sur le droit
    # ~~d'exercer dans les lieux~~ au bail », controle de contenu Google « goog_rdk »). Le
    # document genere ne doit porter AUCUNE marque de revision, et le titre doit lire le texte
    # ACCEPTE « Sur le droit au bail » (coherent avec le corps « Le droit au bail des locaux… »).
    ctx = _context(type_cabinet="dentaire", salaries=_AC_DENT_SALARIES)
    out = ActeCessionCabinetDentaireGenerator().generate(ctx, tmp_path)

    doc_xml = _docx_document_xml(out)
    # w:ins / w:del ELEMENTS (le motif exclut <w:insideH>/<w:delText> par le caractere suivant).
    assert not re.search(r"<w:ins[ />]", doc_xml)
    assert not re.search(r"<w:del[ />]", doc_xml)
    assert "w:delText" not in doc_xml
    assert "w:rPrChange" not in doc_xml
    assert "w:pPrChange" not in doc_xml
    assert "goog_rdk" not in doc_xml  # controles de contenu de revision aplatis
    assert "<w:sdt>" not in doc_xml and "<w:sdt " not in doc_xml

    text = _docx_text(out)
    assert "Sur le droit au bail" in text  # revision acceptee (texte deja visible), sans marque
    _assert_no_residual_tokens(text)


def test_ac4_acte_dentaire_transfert_date_left_blank(tmp_path: Path) -> None:
    # AC4 : la DATE DU TRANSFERT DE PROPRIETE (page 6) etait fausse -> laissee VIERGE (aucune
    # variable). La phrase de transfert subsiste, mais « à la date du » n'est plus suivi d'une date.
    text = _ac_dentaire_acte_text(tmp_path)
    assert "le transfert de propriété auront lieu" in text  # la clause de transfert existe
    assert "à la date du ." in text  # zone vide a completer a la main (pas de date injectee)
    # La date de debut de bail (01 janvier 2021) n'est jamais rendue comme date de transfert.
    m = re.search(r"à la date du ([^.\n]*)\.", text)
    assert m is not None and m.group(1).strip() == "", m
    _assert_no_residual_tokens(text)


def test_ac5_acte_dentaire_pages_count_is_seven(tmp_path: Path) -> None:
    # AC5 : l'acte dentaire indiquait « vingt » pages (constante du front) alors qu'il en fait
    # SEPT -> « Sur sept pages. ».
    text = _ac_dentaire_acte_text(tmp_path)
    assert "Sur sept pages." in text
    assert "vingt pages" not in text
