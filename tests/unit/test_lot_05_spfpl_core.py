from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest
from _accents import assert_no_unaccented_french
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    ApportTitres,
    AssocieCible,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionParts,
    DocumentContext,
    DocumentGenerationContext,
    DossierOptions,
    OperationSpfpl,
    Person,
    ProfessionalEntity,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplDirigeant,
    SpfplOrdre,
    SpfplPerson,
    SpfplRepresentant,
)
from sydel_doc_engine.generators.lot_05.acte_cession_parts_spfpl import (
    ActeCessionPartsSpfplGenerator,
)
from sydel_doc_engine.generators.lot_05.attestation_capital_liste_souscripteurs import (
    AttestationCapitalListeSouscripteursGenerator,
)
from sydel_doc_engine.generators.lot_05.attestation_capital_liste_souscripteurs_cession import (
    AttestationCapitalListeSouscripteursCessionGenerator,
)
from sydel_doc_engine.generators.lot_05.attestation_commissaire_apports import (
    AttestationCommissaireApportsGenerator,
)
from sydel_doc_engine.generators.lot_05.contrat_apport_spfpl import (
    ContratApportSpfplGenerator,
)
from sydel_doc_engine.generators.lot_05.spfpl_common import elision_de


def _base_context(*, operation: str = "cession") -> DocumentGenerationContext:
    is_apport = operation == "apport"
    return DocumentGenerationContext(
        structure="SPFPL apport" if is_apport else "SPFPL cession",
        dossier_options=DossierOptions(apport=is_apport, cession=not is_apport),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 14), nombre_exemplaires="trois"),
        operation_spfpl=OperationSpfpl(type=operation),
        societe_spfpl=SocieteSpfpl(
            denomination="SPFPL MARTIN",
            forme_sociale="SPFPLAS",
            capital_social="60 000",
            # Albane 2026-07-07 : le capital du bloc acquereur se rend « lettres (chiffres)
            # euros » -> le front pose les lettres nues (number_words_from_value).
            capital_social_lettres="soixante mille",
            activite="participations financières de profession libérale",
            profession="chirurgien-dentiste",
            ville_rcs="Paris",
            numero_rcs="en cours",
            siege=Address(adresse_affichee="10 rue de la Paix, 75002 Paris"),
            dirigeant=SpfplDirigeant(fonction="Président"),
            representant=SpfplRepresentant(
                civilite_affichage="Monsieur",
                civilite_courte="M.",
                prenom="Camille",
                nom="Martin",
                fonction="Président",
            ),
        ),
        cedant=_spfpl_person(),
        apporteur=_spfpl_person(),
        societe_cible=SocieteCible(
            denomination="SELARL CABINET MARTIN",
            forme_sociale="SELARL",
            forme_sociale_complete=(
                "société d'exercice libéral à responsabilité limitée"
            ),
            profession_reglementee="chirurgien-dentiste",
            profession_reglementee_pluriel="chirurgiens-dentistes",
            capital_social="10 000",
            capital_social_lettres="dix mille euros",
            nb_parts_total=100,
            valeur_nominale_part="100",
            valeur_nominale_part_lettres="cent euros",
            siege=Address(adresse_affichee="12 avenue des Ternes, 75017 Paris"),
            ville_rcs="Paris",
            numero_rcs="900 000 001",
        ),
        associes_cible=[
            AssocieCible(
                civilite_affichage="Docteur",
                prenom="Camille",
                nom="Martin",
                nb_parts_avant=70,
                nb_parts_apres=10,
                plage_parts="1 a 10",
            ),
            AssocieCible(
                civilite_affichage="Docteur",
                prenom="Louise",
                nom="Bernard",
                nb_parts_avant=30,
                nb_parts_apres=30,
                plage_parts="11 a 40",
            ),
        ],
        cession_parts=CessionParts(
            nb_parts=60,
            nb_parts_lettres="soixante",
            plage_parts="41 a 100",
            prix_unitaire="1 000",
            prix_unitaire_lettres="mille euros",
            prix_total="60 000",
            prix_total_lettres="soixante mille euros",
            nombre_exemplaires_lettres="trois",
        ),
        apport_titres=ApportTitres(
            nb_parts=60,
            nb_parts_lettres="soixante",
            nature_titres="parts sociales",
            plage_parts="41 a 100",
            valeur_par_titre="1 000",
            valeur_par_titre_lettres="mille",
            valeur_globale="60 000",
            valeur_globale_lettres="soixante mille",
            nb_actions_attribuees=600,
            nb_actions_attribuees_lettres="six cents",
            valeur_nominale_action="100",
            valeur_nominale_action_lettres="cent",
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=600,
            valeur_nominale_action="100",
            apports_nature_montant="60 000",
            apports_numeraire_montant="0 euro",
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage="Docteur",
                    prenom="Camille",
                    nom="Martin",
                    profession="chirurgien-dentiste",
                    adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
                    nb_actions=600,
                    qualite="actionnaire unique",
                )
            ],
        ),
        evaluateur_apport=_entity("EVAL CONSEIL", "Madame", "Eva", "Lemoine"),
        commissaire_aux_apports=_entity("CAA EXPERTISE", "Monsieur", "Nabil", "Saidi"),
        document=DocumentContext(nombre_exemplaires_lettres="trois"),
    )


def _spfpl_person() -> SpfplPerson:
    return SpfplPerson(
        # SP2 (Rafael 2026-06-25) : civilite civile M./Mme (reflete le slice : selectbox
        # « Monsieur/Madame »), « Docteur » reste le TITRE (« Dr » abrege en repartition).
        civilite_affichage="Monsieur",
        prenom="Camille",
        nom="Martin",
        genre=Gender.MASCULIN,
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgien-dentiste",
        profession_reglementee_pluriel="chirurgiens-dentistes",
        date_naissance=date(1980, 1, 2),
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        situation_maritale="marie",
        conjoint=SpfplConjoint(
            civilite_affichage="Madame",
            prenom="Alice",
            nom="Martin",
        ),
        adresse_personnelle=Address(adresse_affichee="5 rue Royale, 75008 Paris"),
        adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ordre=SpfplOrdre(
            professionnel="Ordre des chirurgiens-dentistes",
            departement="Paris",
            numero="12345",
            numero_rpps="10000000001",
        ),
    )


def _entity(
    denomination: str,
    civilite: str,
    prenom: str,
    nom: str,
) -> ProfessionalEntity:
    return ProfessionalEntity(
        denomination=denomination,
        forme_sociale="SAS",
        capital_social="1 000 euros",
        siege=Address(adresse_affichee="1 rue Scheffer, 75016 Paris"),
        ville_rcs="Paris",
        numero_rcs="948 483 730",
        representant=SpfplRepresentant(
            civilite_affichage=civilite,
            prenom=prenom,
            nom=nom,
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


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text
    assert "\nOU\n" not in text
    assert "d'acquerir/de recevoir" not in text


# Akainu Bilan de Santé 2026-06-26 (cause racine M4) : la garde anti-accents n'existait que
# sur les PV agrément → 3 générateurs juridiques sortaient du texte NON accentué sans qu'aucun
# test n'échoue. Le garde-fou mot-à-mot est désormais CENTRALISÉ (Akainu B1/M1, 2026-06-26)
# dans ``_accents.assert_no_unaccented_french`` (liste noire unique et exhaustive). On y ajoute
# ici deux contrôles de PHRASE propres à ces attestations (« présent état », « déclarent ») que le
# check mot-à-mot ne couvre pas (homographes verbaux exclus de la liste centrale).
def _assert_no_unaccented_french(text: str) -> None:
    assert_no_unaccented_french(text)
    assert "present etat" not in text, "« présent état » non accentué dans la sortie générée."
    assert "souscripteurs declarent" not in text, "« déclarent » non accentué dans la sortie."


def test_acte_cession_parts_generates_dynamic_capital_and_preserves_source_frais(
    tmp_path: Path,
) -> None:
    output_path = ActeCessionPartsSpfplGenerator().generate(_base_context(), tmp_path)

    text = _docx_text(output_path)

    # SP1/SP3/SP4 (Albane 2026-06-25) : acte rebati en TOKEN-REPLACEMENT fidele au modele
    # source -> texte legal COMPLET (clauses GAP / SIGNIFICATION / AFFIRMATION DE SINCERITE,
    # absentes de l'ancien from-scratch), accents preserves. Fidelite de STRUCTURE (aucun .docx
    # gold de sortie n'existe pour cet acte).
    # Rafael 2026-07-09 « supprimer partout » : « Docteur »/« Dr » n'est jamais une civilite -> la
    # phrase d'identite ET la repartition rendent la civilite CIVILE (« Monsieur »). SUPERSEDE
    # l'ancien « Dr <nom> détenant … » abrege du modele. `AssocieCible` sans genre -> masculin par
    # defaut (limite documentee : accord feminin non capturable ici).
    assert output_path.name == "acte_cession_parts_spfpl.docx"
    assert "Monsieur Camille Martin" in text
    assert "Docteur" not in text
    assert "Dr " not in text
    # Repartition dynamique : civilite civile + « détenant » accentue.
    assert "Monsieur Camille Martin détenant 70 parts" in text
    assert "Monsieur Louise Bernard détenant 30 parts" in text
    # Clauses du modele source qui MANQUAIENT dans l'ancien from-scratch (SP1 « tout revoir »).
    assert "GARANTIE D’ACTIF ET DE PASSIF" in text
    assert "AFFIRMATION DE SINCERITE" in text
    assert "SIGNIFICATION DE LA CESSION" in text
    assert "moyennant le prix de" in text
    assert "FRAIS" in text  # clause frais presente (l'ancien from-scratch la paraphrasait)
    # Akainu M1 : signature UNIQUE (le modele porte deja sa ligne ; pas de bloc ajoute en double).
    assert text.count("Représentée par M. Camille Martin") == 1
    # Akainu M2 : accents preserves dans la signature (pas de « La societe »/« Representee » nus).
    assert "La societe" not in text
    assert "Representee" not in text
    assert "La société SPFPL MARTIN" in text
    # Akainu M3 : valeur nominale = champ ctx « cent euros » AVEC elision correcte « de cent euros »
    # (le modele colle « d’ » au placeholder ; consonne -> « de »). NB apostrophe COURBE (’, U+2019)
    # comme dans le rendu reel — l'apostrophe droite (') passait faussement vert.
    assert "de cent euros de valeur nominale" in text
    assert "d’cent" not in text
    assert "d'cent" not in text
    # R2 (Albane 2026-07-07) : SPFPL acquereuse non immatriculee -> identite « en cours de
    # constitution » + « En cours d’immatriculation au RCS de <ville> » ; plus jamais
    # « Immatriculée … sous le numéro en cours ».
    assert "par actions simplifiée en cours de constitution" in text
    assert "En cours d’immatriculation au RCS de Paris" in text
    assert "sous le numéro en cours" not in text
    # R8 (Albane 2026-07-07) : UNE SEULE repartition du capital (recital de l'EXPOSE
    # PREALABLE conserve, liste + intro du bloc ORIGINE DE PROPRIETE retirees, phrase
    # « déclare qu'il est propriétaire » conservee). Supersede les « 2 recitals fideles ».
    assert "Le capital social est réparti à ce jour comme suit" in text
    assert "actuellement détenu comme suit" not in text
    # Rafael 2026-07-09 « supprimer partout » : civilite civile en repartition, plus « Dr ».
    assert text.count("Monsieur Camille Martin détenant 70 parts") == 1
    assert text.count("Monsieur Louise Bernard détenant 30 parts") == 1
    assert "déclare qu’il est propriétaire des parts" in text
    # R9 (Albane 2026-07-07) : clause de communication au Conseil de l'Ordre AVEC le
    # departement de l'Ordre du cedant en nom (fixture : « Paris »).
    assert "communiqué au Conseil départemental de l’Ordre de Paris en vue" in text
    assert "de l’Ordre en vue" not in text
    # Albane 2026-07-07 : capitaux en « lettres (chiffres groupes) euros ».
    assert "Au capital de soixante mille (60 000) euros" in text
    assert "Au capital de 60" not in text  # plus de figure nue dans le bloc acquereur
    assert "au capital social de dix mille (10 000) euros divisé" in text
    _assert_clean(text)


def test_contrat_apport_uses_context_evaluateur_and_commissaire(tmp_path: Path) -> None:
    output_path = ContratApportSpfplGenerator().generate(
        _base_context(operation="apport"),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "contrat_apport_spfpl.docx"
    # SP1/SP3 (Albane 2026-06-25) : rebuild HYBRIDE token-replacement -> societes template du
    # modele (SYDEL evaluateur, TS EXPERTISE commissaire) DYNAMISEES depuis le ctx, texte legal
    # ACCENTUE (le from-scratch etait entierement non accentue).
    assert "EVAL CONSEIL" in text
    assert "CAA EXPERTISE" in text
    assert "SYDEL" not in text  # societe template du modele dynamisee
    assert "TS EXPERTISE" not in text
    # Accents preserves (le from-scratch shippait « Societe »/« Representee »/« beneficiaire » nus).
    assert "Société" in text
    assert "bénéficiaire" in text
    assert not re.search(r"\bSociete\b", text)
    assert "Representee" not in text
    # SP2 : civilite civile M./Mme, jamais « Docteur ».
    assert "Monsieur" in text
    assert "Docteur" not in text
    # Akainu M1/M2 : adresses NON vides (le ctx fournit l'adresse via adresse_affichee ; lire
    # seulement num/voie/cp/ville sortait « Demeurant  , » / « Siège social :  ,  »).
    assert "5 rue Royale, 75008 Paris" in text  # adresse perso de l'apporteur
    assert "10 rue de la Paix, 75002 Paris" in text  # siege de la SPFPL
    assert "Demeurant  ," not in text
    _assert_clean(text)


def test_contrat_apport_blocks_missing_commissaire(tmp_path: Path) -> None:
    ctx = _base_context(operation="apport")
    ctx.commissaire_aux_apports = None

    with pytest.raises(ValueError, match="commissaire_aux_apports"):
        ContratApportSpfplGenerator().generate(ctx, tmp_path)


def test_contrat_apport_empty_address_renders_marker_not_blank(tmp_path: Path) -> None:
    """Akainu M1 round 2 : le front construit toujours `Address(adresse_affichee=str(...) or "")`.
    Une adresse vide (adresse_affichee="" + sous-champs vides) NE DOIT PAS rendre un blanc
    silencieux (« Siège social :  » / « Demeurant  , ») mais le marqueur « (À COMPLÉTER : …) »
    (R10), cohérent avec les jumeaux company_siege_display / person_address_display."""
    ctx = _base_context(operation="apport")
    ctx.apporteur.adresse_personnelle = Address(adresse_affichee="")
    ctx.societe_spfpl.siege = Address(adresse_affichee="")

    output_path = ContratApportSpfplGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    # Aucun blanc silencieux : pas de « Demeurant  , » ni de siège vide.
    assert "Demeurant  ," not in text
    assert "Demeurant ," not in text
    # Le marqueur visible apparait a la place (jamais une adresse fantome).
    assert "(À COMPLÉTER : apporteur.adresse_personnelle" in text
    assert "(À COMPLÉTER : societe_spfpl.siege" in text


def test_acte_cession_ordre_departement_numero_rendered_as_name(tmp_path: Path) -> None:
    # Convention Albane 7.4/9.2 propagee a l'acte : le departement de l'Ordre en NUMERO
    # (« 77 ») doit se rendre en NOM (« Seine-et-Marne »), jamais « de 77 ». Sans
    # `departement_nom` cable, ce test echouerait (garde d'integration, Akainu DEPT m2).
    ctx = _base_context()
    ctx.cedant.ordre.departement = "77"
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(ctx, tmp_path))
    assert "Seine-et-Marne" in text
    assert "de 77" not in text
    # R9 (Albane 2026-07-07, verbatim) : la clause Ordre porte aussi le departement en nom
    # (« au Conseil départemental de l’Ordre de Seine-et-Marne »).
    assert "communiqué au Conseil départemental de l’Ordre de Seine-et-Marne en vue" in text


def test_acte_cession_parts_pacse_reprises_partner(tmp_path: Path) -> None:
    # Albane 6.3/7.3 : un cedant PACSE avec partenaire renseigne -> partenaire repris
    # (« avec Madame Alice Martin »), SANS « sous le régime de … » (un PACS n'a pas de regime).
    ctx = _base_context(operation="cession")
    ctx.cedant.situation_maritale = "pacse"
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(ctx, tmp_path))
    assert "avec Madame Alice Martin" in text
    assert "sous le régime de" not in text


def test_acte_cession_parts_pacse_sans_partenaire_no_mention(tmp_path: Path) -> None:
    # « Pas de mention sans nom » (Albane 6.3) : pacse SANS partenaire -> pas de reprise.
    ctx = _base_context(operation="cession")
    ctx.cedant.situation_maritale = "pacse"
    ctx.cedant.conjoint = None
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(ctx, tmp_path))
    assert "Alice Martin" not in text
    assert "(À COMPLÉTER" not in text


def test_contrat_apport_pacse_reprises_partner(tmp_path: Path) -> None:
    # Le modele contrat d'apport reprend le partenaire en prenom+nom (sans civilite, miroir marie).
    ctx = _base_context(operation="apport")
    ctx.apporteur.situation_maritale = "pacse"
    text = _docx_text(ContratApportSpfplGenerator().generate(ctx, tmp_path))
    assert "avec Alice Martin" in text
    assert "sous le régime de" not in text


def test_attestation_commissaire_pacse_reprises_partner_nom(tmp_path: Path) -> None:
    # Le modele attestation ne porte que le NOM du conjoint/partenaire (fidelite, miroir marie).
    ctx = _base_context(operation="apport")
    ctx.apporteur.situation_maritale = "pacse"
    text = _docx_text(AttestationCommissaireApportsGenerator().generate(ctx, tmp_path))
    assert "avec Martin" in text


def test_acte_cession_vrai_numero_rcs_garde_ligne_immatriculee(tmp_path: Path) -> None:
    # R2 (Albane 2026-07-07) — garde-fou inverse : une SPFPL acquereuse DEJA immatriculee
    # (vrai numero RCS) conserve la ligne du modele « Immatriculée au RCS de <ville> sous le
    # numéro <numero> », sans « en cours de constitution » parasite.
    ctx = _base_context()
    ctx.societe_spfpl.numero_rcs = "912 345 678"
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(ctx, tmp_path))
    assert "Immatriculée au RCS de Paris sous le numéro 912 345 678" in text
    assert "en cours de constitution" not in text
    assert "En cours d’immatriculation" not in text


def test_contrat_apport_forme_simplifiee_accentuee(tmp_path: Path) -> None:
    # R4 (Albane 2026-07-07) : le front pose la forme abregee NON accentuee
    # (« par actions simplifiee ») -> la sortie doit rendre « par actions simplifiée ».
    ctx = _base_context(operation="apport")
    ctx.societe_spfpl.forme_sociale = "par actions simplifiee"  # valeur reelle du front
    text = _docx_text(ContratApportSpfplGenerator().generate(ctx, tmp_path))
    assert "par actions simplifiée" in text
    assert "simplifiee" not in text


def test_attestation_commissaire_forme_simplifiee_accentuee(tmp_path: Path) -> None:
    # R4 (Albane 2026-07-07) : idem attestation du commissaire aux apports (« … par actions
    # simplifiee de chirurgien-dentiste en cours de formation » etait non accentue).
    ctx = _base_context(operation="apport")
    ctx.societe_spfpl.forme_sociale = "par actions simplifiee"  # valeur reelle du front
    text = _docx_text(AttestationCommissaireApportsGenerator().generate(ctx, tmp_path))
    assert "par actions simplifiée de chirurgien-dentiste en cours de formation" in text
    assert "simplifiee" not in text


def test_attestation_capital_is_limited_to_unique_souscripteur(tmp_path: Path) -> None:
    ctx = _base_context(operation="apport")
    ctx.capital_souscription.souscripteurs.append(
        CapitalSouscripteur(
            civilite_affichage="Docteur",
            prenom="Louise",
            nom="Bernard",
            profession="chirurgien-dentiste",
            adresse_personnelle_affichee="9 rue Bleue, 75009 Paris",
            nb_actions=1,
        )
    )

    with pytest.raises(ValueError, match="exactement un souscripteur"):
        AttestationCapitalListeSouscripteursGenerator().generate(ctx, tmp_path)


def test_attestation_capital_generates_unique_shareholder_wording(tmp_path: Path) -> None:
    output_path = AttestationCapitalListeSouscripteursGenerator().generate(
        _base_context(operation="apport"),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "attestation_capital_liste_souscripteurs.docx"
    assert "actionnaire unique" in text
    assert "Apports en numéraire : 0 euro" in text
    # Akainu Bilan de Santé (fidélité) : B1 doublon « Le Docteur Docteur » corrigé +
    # M1 texte juridique ACCENTUÉ (le from-scratch sortait tout non accentué).
    assert "Docteur Docteur" not in text
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49) — la phrase
    # d'apport rend la civilité CIVILE, plus de titre « Le Docteur X a fait ».
    assert "Monsieur Camille Martin a fait la totalité des apports en nature." in text
    # R3 (Albane 2026-07-07) : la fixture pose civilite_affichage="Docteur" -> les
    # slots de civilité (tête de désignation, « par le Président, __ », signature)
    # rendent la civilité CIVILE ; durci Rafael 2026-07-07 : plus AUCUN « Docteur »
    # en sortie, titre du corps compris.
    assert "Monsieur Camille Martin chirurgien-dentiste, demeurant" in text
    assert "par le Président, Monsieur Camille Martin chirurgien-dentiste." in text
    assert "Docteur Camille Martin chirurgien-dentiste" not in text
    assert "Président, Docteur" not in text
    assert "Docteur" not in text
    _assert_no_unaccented_french(text)
    _assert_clean(text)


def test_attestation_capital_cession_wording_and_genre(tmp_path: Path) -> None:
    gen = AttestationCapitalListeSouscripteursCessionGenerator()

    # Civilite PROD-REALISTE « Monsieur » (le slice pose la civilite civile, jamais
    # « Docteur » — Akainu M2 : la fixture « Docteur » derivait masculin par accident
    # et ne couvrait pas le feminin). Cas MASCULIN.
    ctx_m = _base_context(operation="cession")
    ctx_m.capital_souscription.souscripteurs[0].civilite_affichage = "Monsieur"
    output_path = gen.generate(ctx_m, tmp_path)
    text_m = _docx_text(output_path)

    assert output_path.name == "attestation_capital_liste_souscripteurs_cession.docx"
    # Variante CESSION (retour Albane 11) vs apport DOC-042 : capital deja libere/depose.
    assert "en numéraire" in text_m
    assert "entièrement libéré et déposé dans les livres de la banque" in text_m
    assert "euros en numéraire" in text_m
    assert "actionnaire unique" in text_m
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49) — la
    # répartition rend « à [civilité civile] [prenom] [nom] », plus l'abrégé
    # « au Dr [prenom] [nom] » (ni le doublon « Dr Docteur »).
    assert "Dr Docteur" not in text_m
    assert "à Monsieur Camille Martin" in text_m
    assert "au Dr " not in text_m
    assert "Docteur" not in text_m
    # Accord MASCULIN.
    assert "Je soussigné " in text_m
    assert "soussignée" not in text_m
    _assert_no_unaccented_french(text_m)
    _assert_clean(text_m)

    # Cas FEMININ « Madame » -> « Je soussignée » (couverture absente avant Akainu M2).
    ctx_f = _base_context(operation="cession")
    ctx_f.capital_souscription.souscripteurs[0].civilite_affichage = "Madame"
    text_f = _docx_text(gen.generate(ctx_f, tmp_path))
    assert "Je soussignée" in text_f
    assert "Dr Docteur" not in text_f
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49).
    assert "Docteur" not in text_f
    _assert_no_unaccented_french(text_f)
    _assert_clean(text_f)

    # R3 (Albane 2026-07-07) : civilite « Docteur » (titre) -> slot « Je soussigné __ »
    # rendu en civilité CIVILE, accordée au genre du SIGNATAIRE (le titre ne porte
    # pas le genre) ; fixture de base = « Docteur » + signataire masculin.
    ctx_d = _base_context(operation="cession")  # souscripteur « Docteur » (fixture)
    text_d = _docx_text(gen.generate(ctx_d, tmp_path))
    assert "Je soussigné Monsieur Camille Martin chirurgien-dentiste" in text_d
    assert "soussigné Docteur" not in text_d
    assert "Président, Docteur" not in text_d
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49) — même avec la
    # fixture-titre « Docteur », AUCUN « Docteur » ne sort.
    assert "Docteur" not in text_d
    # R4 (Albane 2026-07-07, explicite) : « d'un montant de 100 d'euro chacune » ->
    # « de 100 euros chacune » (accord euro_word, aligné variante SAS).
    assert "actions d’un montant de 100 euros chacune" in text_d
    assert "d’euro chacune" not in text_d
    _assert_no_unaccented_french(text_d)
    _assert_clean(text_d)


def test_attestation_commissaire_apports_renders_single_selected_commissaire(
    tmp_path: Path,
) -> None:
    output_path = AttestationCommissaireApportsGenerator().generate(
        _base_context(operation="apport"),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "attestation_commissaire_apports.docx"
    assert "Aux fins de réalisation de cet apport en nature" in text
    assert "CAA EXPERTISE" in text
    assert "ADVENSO" not in text
    assert "TS EXPERTISE" not in text
    # Akainu Bilan de Santé (fidélité M4) : ce from-scratch sortait tout non accentué.
    _assert_no_unaccented_french(text)
    _assert_clean(text)

def test_elision_de_couvre_voyelle_consonne_h_aspire_onze() -> None:
    # Akainu m1 (regle 68) : test direct du helper d'elision partage. « de » devant
    # consonne, « d’ » (courbe) devant voyelle, « de » pour h aspire (« huit ») et
    # l'exception « onze ». Couvre la branche voyelle (non exercee par les actes).
    assert elision_de("cent euros") == "de cent euros"
    assert elision_de("100") == "de 100"
    assert elision_de("un euro") == "d’un euro"
    assert elision_de("onze euros") == "de onze euros"
    assert elision_de("huit euros") == "de huit euros"
    assert elision_de("") == "de "


# ---------------------------------------------------------------------------
# Verrous de VALEUR (Akainu 2026-07-06, regle 65/68 : assertions d'accord / ordre /
# omission, pas de simple presence). Le front pose les lettres SANS unite figee ; l'acte
# accorde « euro(s) » au MONTANT. On regenere l'acte avec des prix distincts.
# ---------------------------------------------------------------------------


def _acte_price_line(text: str) -> str:
    # n3 (Albane 2026-07-06) : l'ancre exclut le « de » car l'ELISION le transforme en « d’ »
    # pour un montant a initiale vocalique (« le prix d’un euro ») -> ancrer sur « moyennant le
    # prix » (invariant a l'elision), pas « moyennant le prix de ».
    for line in text.split("\n"):
        if "moyennant le prix" in line:
            return line
    raise AssertionError("ligne de prix (« moyennant le prix … ») absente de l'acte.")


def _render_acte_with_price(
    tmp_path: Path,
    *,
    prix_unitaire: str,
    prix_unitaire_lettres: str,
    prix_total: str,
    prix_total_lettres: str,
) -> str:
    ctx = _base_context(operation="cession")
    cp = ctx.cession_parts
    assert cp is not None
    cp.prix_unitaire = prix_unitaire
    cp.prix_unitaire_lettres = prix_unitaire_lettres
    cp.prix_total = prix_total
    cp.prix_total_lettres = prix_total_lettres
    return _docx_text(ActeCessionPartsSpfplGenerator().generate(ctx, tmp_path))


def test_acte_price_singular_euro_for_one(tmp_path: Path) -> None:
    """12.6 / B1 (Akainu 2026-07-06) — VALEUR : un prix de 1 € rend « un euro » (SINGULIER),
    JAMAIS « un euros ». Le front pose les lettres sans unite (« un ») ; l'acte accorde via
    `euro_word`. Anti double-euro (« euro euro ») verifie aussi.

    n3 (Albane 2026-07-06) — ELISION euphonique : « de un euro » -> « d’un euro » (apostrophe
    courbe U+2019) sur le prix UNITAIRE et le prix TOTAL. On verrouille la forme elidee ET
    l'absence de la forme non elidee « de un euro »."""
    line = _acte_price_line(
        _render_acte_with_price(
            tmp_path,
            prix_unitaire="1",
            prix_unitaire_lettres="un",
            prix_total="1",
            prix_total_lettres="un",
        )
    )
    # n3 : elision « d’un euro » (unitaire + total), plus de « de un euro ».
    assert "le prix d’un euro (1 €) part cédée" in line  # unitaire : elide + singulier + € lisible
    assert "soit un prix d’un euro (1 €)" in line  # total : elide + singulier
    assert "de un euro" not in line  # forme non elidee proscrite (n3)
    assert "un euros" not in line  # accord incorrect proscrit
    assert "euro euro" not in line  # anti double-unite
    assert "(1) part" not in line  # plus de chiffre nu sans unite avant « part »


def test_acte_price_plural_euros_above_one(tmp_path: Path) -> None:
    """12.6 / 12.3 (Akainu 2026-07-06) — VALEUR : un prix > 1 rend « euros » (PLURIEL) et
    l'ordre LETTRES puis CHIFFRES. Robustesse : des lettres deja suffixees « euros »
    (fixture) ne doublent pas l'unite."""
    line = _acte_price_line(
        _render_acte_with_price(
            tmp_path,
            prix_unitaire="1 000",
            prix_unitaire_lettres="mille euros",  # fixture avec unite -> ne doit pas doubler
            prix_total="60 000",
            prix_total_lettres="soixante mille euros",
        )
    )
    assert "mille euros (1 000 €) part cédée" in line
    assert "soit un prix de soixante mille euros (60 000 €)" in line
    assert "euros euros" not in line


def test_acte_price_decimal_keeps_figure_no_double_euro(tmp_path: Path) -> None:
    """Akainu M1 2026-07-06 — un prix DECIMAL garde la FIGURE en lettres (« 0,01 »), le
    wording monetaire (« un centime d'euro ») n'est PAS ratifie pour le PRIX (seulement pour
    la valeur nominale, 7.5). Le front pose desormais `prix_lettres_from_value` (figure sur
    decimal) -> l'acte accorde « euro » sur la figure et ne DOUBLE PLUS l'unite (regression
    « d'un centime d'euro euro » proscrite)."""
    line = _acte_price_line(
        _render_acte_with_price(
            tmp_path,
            prix_unitaire="0,01",
            prix_unitaire_lettres="0,01",  # figure = ce que produit prix_lettres_from_value
            prix_total="0,05",
            prix_total_lettres="0,05",
        )
    )
    assert "0,01 euro (0,01 €) part cédée" in line  # figure + « euro » accorde une seule fois
    assert "centime d’euro" not in line  # phrase monetaire proscrite pour le prix
    assert "euro euro" not in line  # anti double-unite (regression M1)
    assert "euro euro" not in line


def test_acte_acquereur_full_legal_form(tmp_path: Path) -> None:
    """12.2 (Albane 2026-07-06) — VALEUR : l'acquereur (SPFPL) porte sa forme LEGALE COMPLETE
    (« Société de Participations Financières … par actions simplifiée »), JAMAIS l'abrege
    « par actions simplifiee » (non accentue) injecte par le front."""
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(_base_context(), tmp_path))
    assert (
        "Société de Participations Financières de Profession Libérale de "
        "Chirurgiens-Dentistes par actions simplifiée" in text
    )
    assert "par action simplifié" not in text  # ni singulier ni non-accentue
    assert "par actions simplifiee" not in text  # abrege front non accentue proscrit


def test_acte_payment_wording_au_moyen(tmp_path: Path) -> None:
    """12.7 (Albane 2026-07-06) — VALEUR : la phrase de paiement est « au moyen d’un chèque ou
    virement », plus « par le moyen d’un chèque ou d’un virement »."""
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(_base_context(), tmp_path))
    assert "Le prix est payé au moyen d’un chèque ou virement." in text
    assert "par le moyen" not in text


def test_acte_repartition_omits_zero_part_line(tmp_path: Path) -> None:
    """12.5(a) (Albane 2026-07-06) — OMISSION : un associe / une SPFPL detenant 0 part ne
    figure PAS dans la repartition du capital (« détenant 0 part » n'a pas de sens)."""
    ctx = _base_context(operation="cession")
    ctx.associes_cible.append(
        AssocieCible(
            type="personne_morale",
            denomination="SPFPL ACQUEREUR",
            nb_parts_avant=0,  # pre-liste avant cession -> ligne omise
            nb_parts_apres=60,
        )
    )
    text = _docx_text(ActeCessionPartsSpfplGenerator().generate(ctx, tmp_path))
    assert "SPFPL ACQUEREUR" not in text  # la ligne 0 part est omise
    assert "détenant 0 part" not in text
    assert "detenant 0 part" not in text
    # les associes a parts > 0 restent presents (civilite civile, R3 2026-07-09).
    assert "Monsieur Camille Martin détenant 70 parts" in text

