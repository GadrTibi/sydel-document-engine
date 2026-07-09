from __future__ import annotations

from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

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
    Emprunt,
    Person,
    ReunionContext,
    ReunionPresident,
    Signature,
    SpfplPerson,
)
from sydel_doc_engine.generators.lot_02.pv_nomination_gerant import (
    _PV_COMPACT_SPACE_AFTER_PT,
    VOTE_FORMULA,
    PvNominationGerantGenerator,
)


def _associes(count: int = 2) -> list[Associe]:
    if count == 1:
        # Associe unique : identite complete (le PV « decisions de l'associe unique »
        # decrit l'associe — retour Albane 2026-06-10).
        return [
            Associe(
                genre=Gender.FEMININ,
                civilite_affichage="Madame",
                prenom="Alice",
                nom="Durand",
                nb_parts=1,
                profession="médecin",
                date_naissance=date(1986, 7, 9),
                ville_naissance="Lyon",
                departement_naissance="Rhône",
                nationalite="française",
                adresse_personnelle=Address(
                    num_voie="3",
                    voie="rue des Lilas",
                    cp="69003",
                    ville="Lyon",
                ),
            )
        ]
    return [
        Associe(
            genre=Gender.FEMININ,
            civilite_affichage="Madame",
            prenom="Alice",
            nom="Durand",
            nb_parts=60,
        ),
        Associe(
            genre=Gender.MASCULIN,
            civilite_affichage="Monsieur",
            prenom="Bruno",
            nom="Martin",
            nb_parts=40,
        ),
    ]


def _context(
    *,
    associes: list[Associe] | None = None,
    emprunt_actif: bool = False,
    valeur_nominale_part: str = "1",
) -> DocumentGenerationContext:
    associes = associes or _associes()
    return DocumentGenerationContext(
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Signataire",
        ),
        societe=Company(
            forme_sociale_affichage="Société civile immobilière",
            forme_sociale_libelle_long="société civile immobilière",
            denomination="SCI TEST",
            capital_social="1 000",
            capital_variable=True,
            siege=Address(
                num_voie="10",
                voie="rue du Siège",
                cp="75001",
                ville="Paris",
            ),
            ville_rcs="Paris",
        ),
        decision=DecisionContext(date="13 mai 2026"),
        reunion=ReunionContext(
            date_lettres="treize mai deux mille vingt-six",
            president=ReunionPresident(
                civilite_president_seance="Madame",
                prenom_president_seance="Alice",
                nom_personne_seance="Durand",
            ),
        ),
        capital=CapitalContext(
            nb_parts_total=sum(associe.nb_parts for associe in associes),
            valeur_nominale_part=valeur_nominale_part,
        ),
        associes=associes,
        dirigeant_nomine=DirigeantNomine(
            genre=Gender.FEMININ,
            civilite_affichage="Madame",
            prenom="Claire",
            nom="Bernard",
            date_naissance=date(1985, 4, 3),
            ville_naissance="Lyon",
            departement_naissance="Rhône",
            nationalite="française",
            adresse_personnelle=Address(
                num_voie="22",
                voie="avenue des Fleurs",
                cp="69002",
                ville="Lyon",
            ),
            fonction_affichage="gérant",
        ),
        emprunt=Emprunt(
            actif=emprunt_actif,
            montant_max="250 000" if emprunt_actif else None,
        ),
        bien_immobilier=(
            BienImmobilier(
                adresse=Address(
                    num_voie="5",
                    voie="rue du Bien",
                    cp="33000",
                    ville="Bordeaux",
                )
            )
            if emprunt_actif
            else None
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 13),
            nombre_exemplaires="3",
        ),
    )


def _generate(tmp_path: Path, ctx: DocumentGenerationContext | None = None) -> Path:
    return PvNominationGerantGenerator().generate(ctx or _context(), tmp_path)


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs)
    return "\n".join(text for text in texts if text)


def _paragraphs(path: Path) -> list[str]:
    return [paragraph.text for paragraph in Document(path).paragraphs if paragraph.text]


def _find_paragraph(document: Document, text: str):
    return next(paragraph for paragraph in document.paragraphs if paragraph.text == text)


def test_pv_nomination_gerant_creates_docx(tmp_path: Path) -> None:
    output_path = _generate(tmp_path)

    assert output_path == tmp_path / "pv_nomination_gerant.docx"
    assert output_path.is_file()


def test_pv_nomination_gerant_selarl_header_uses_written_form_and_simple_capital(
    tmp_path: Path,
) -> None:
    ctx = _context(associes=_associes(1))
    ctx.societe.forme_sociale = "SELARL"
    ctx.societe.forme_sociale_affichage = "SELARL"
    ctx.societe.forme_sociale_complete = "société d’exercice libéral à responsabilité limitée"
    ctx.societe.forme_sociale_abregee = "SELARL"
    ctx.societe.denomination = "SELARL MARTIN"
    ctx.societe.capital_social = "5 000"
    ctx.associes[0].profession_reglementee = "médecin"

    text = _docx_text(_generate(tmp_path, ctx))
    paragraphs = _paragraphs(_generate(tmp_path / "second", ctx))

    assert "SELARL MARTIN" in paragraphs
    assert "Société d’exercice libéral à responsabilité limitée de médecin" in paragraphs
    assert "Au capital de 5 000 euros" in paragraphs
    assert "SELARL à capital variable" not in text
    assert "Au capital minimum et effectif" not in text


def test_pv_nomination_gerant_repeats_two_associes(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path))
    paragraphs = _paragraphs(_generate(tmp_path / "second"))

    assert "Les associés de la Société civile immobilière SCI TEST" in text
    # Rafael 2026-07-09 : le capital de la 1re phrase porte « euros » (accorde) comme
    # l'en-tete, plus jamais « au capital de <montant> » nu (montant_avec_euros).
    assert "au capital de 1 000 euros, composé de" in text
    assert "au capital de 1 000, composé de" not in text
    assert "composé de 100 parts de 1 euro chacune, se sont réunis au siège social." in text
    # Pluriel « euros » des que la valeur nominale est >= 2 (bug remonte Rafael 2026-06-08 :
    # « 10 euro » sans s). Singulier conserve a 1 euro (cf. assertion ci-dessus).
    plural_text = _docx_text(_generate(tmp_path / "valeur10", _context(valeur_nominale_part="10")))
    assert "composé de 100 parts de 10 euros chacune" in plural_text
    assert "10 euro chacune" not in plural_text
    assert "Sont présents ou représentés :" in text
    assert "Madame Alice Durand, détenant 60 parts," in text
    assert "Monsieur Bruno Martin, détenant 40 parts," in text
    assert "- Madame Alice Durand, détenant 60 parts," in paragraphs
    assert "- Monsieur Bruno Martin, détenant 40 parts," in paragraphs
    assert (
        "Les associés présents ou représentés disposent ensemble de la totalité des parts "
        "sociales. Cet ensemble est habilité à prendre des décisions."
    ) in text
    assert "Madame Alice Durand préside la séance." in text
    assert "Le président rappelle l’ordre du jour :" in text
    # PV4 (Albane 2026-06-26) : ordre du jour en tirets « - » (plus de « · »).
    assert "- Nomination du gérant" in paragraphs
    assert "- Pouvoirs" in paragraphs
    assert "· Nomination du gérant" not in text
    assert "· Pouvoirs" not in text
    assert "RCS de Paris" not in text
    assert "En cours d’immatriculation" in text
    assert "EXTRAORDINAIRE" not in text
    assert "extraordinaire" not in text
    assert "10 heures" not in text
    assert "De tout ce qui a été décidé" not in text
    assert "L’ordre du jour étant épuisé" not in text
    assert "Alice Durand" in paragraphs
    assert "Bruno Martin" in paragraphs


def test_pv_nomination_gerant_one_associe_is_associe_unique_pv(
    tmp_path: Path,
) -> None:
    # Retour Albane 2026-06-10 : avec UN SEUL associe, le PV est un PV des
    # DECISIONS DE L'ASSOCIE UNIQUE (juridiquement, une societe a un seul
    # associe ne tient pas d'assemblee generale). Structure simplifiee + ordre
    # du jour en tirets.
    ctx = _context(associes=_associes(1))
    text = _docx_text(_generate(tmp_path, ctx))
    paragraphs = _paragraphs(_generate(tmp_path / "second", ctx))

    # Titre + structure associe unique (pas d'assemblee generale, pas de bloc presents).
    assert "DE L’ASSOCIE UNIQUE" in text
    assert "ASSEMBLEE GENERALE" not in text
    assert "Sont présents ou représentés" not in text
    assert "se sont réunis au siège social" not in text
    # Identite de l'associe unique.
    assert "- Madame Alice Durand" in paragraphs
    assert "Née le 09/07/1986 à Lyon" in text
    # Rafael/Albane 2026-07-09 : « Demeurant [adresse] » -> « Demeurant au [adresse] ».
    assert "Demeurant au 3 rue des Lilas, 69003 Lyon" in text
    assert (
        "Associée unique, propriétaire de toutes les parts de la société SCI TEST "
        "en cours de formation."
    ) in text
    assert "À l’issue de la signature des statuts, a pris les décisions suivantes :" in text
    # Ordre du jour en tirets.
    assert "- Nomination du gérant" in paragraphs
    assert "- Pouvoir" in paragraphs
    # Decisions de l'associe unique (femme -> gerante).
    assert (
        "L’associée unique décide de désigner en qualité de gérante Madame Alice Durand, "
        "médecin de profession, née le 09/07/1986 à Lyon, de nationalité française, "
        "demeurant au 3 rue des Lilas, 69003 Lyon associée unique de la Société."
    ) in text
    assert "Sa rémunération sera fixée ultérieurement." in text
    assert (
        "au greffe du Tribunal de Commerce de la Société de Paris."
    ) in text
    assert "Cette résolution est adoptée à l’unanimité" not in text
    assert "Bon pour acceptation des fonctions de gérante" in text


def test_pv_nomination_gerant_without_emprunt_omits_borrowing_decision(
    tmp_path: Path,
) -> None:
    text = _docx_text(_generate(tmp_path, _context(emprunt_actif=False)))

    assert "Autorisation de  contracter un emprunt" not in text
    assert "contracter un emprunt d’un montant maximum" not in text
    assert "DEUXIEME DECISION" in text
    assert "TROISIEME DECISION" not in text


def test_pv_nomination_gerant_with_emprunt_writes_borrowing_decision(
    tmp_path: Path,
) -> None:
    output = _generate(tmp_path, _context(emprunt_actif=True))
    text = _docx_text(output)
    paragraphs = _paragraphs(output)

    # PV4 (Albane 2026-06-26) : item d'ordre du jour en tiret « - ».
    assert (
        "- Autorisation de contracter un emprunt pour l’achat d’un bien immobilier sis "
        "5 rue du Bien, 33000 Bordeaux"
    ) in paragraphs
    assert (
        "L’assemblée générale décide de contracter un emprunt d’un montant "
        "maximum de 250 000 euros pour l’acquisition d’un bien immobilier sis "
        "5 rue du Bien, 33000 Bordeaux."
    ) in text
    assert "TROISIEME DECISION" in text


def test_pv_nomination_gerant_uses_plural_agenda_for_plural_function(
    tmp_path: Path,
) -> None:
    ctx = _context()
    ctx.dirigeant_nomine.fonction_affichage = "gérants"

    paragraphs = _paragraphs(_generate(tmp_path, ctx))

    # PV4 (Albane 2026-06-26) : tiret « - » devant l'item d'ordre du jour.
    assert "- Nomination des premiers gérants" in paragraphs


def test_pv_nomination_gerant_uses_distinct_dirigeant_nomine(
    tmp_path: Path,
) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "Madame Claire Bernard, née le 03/04/1985 à Lyon (Rhône)" in text
    assert "demeurant au 22 avenue des Fleurs, 69002 Lyon." in text
    assert "Madame Alice Durand, née le" not in text
    assert "Monsieur Bruno Martin, né le" not in text


def test_pv_nomination_gerant_uses_feminine_birth_variant(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "née le 03/04/1985" in text
    assert "né le 03/04/1985" not in text


def test_pv_nomination_gerant_restores_essential_docx_structure(tmp_path: Path) -> None:
    document = Document(_generate(tmp_path, _context(emprunt_actif=True)))

    company_name = _find_paragraph(document, "SCI TEST")
    assert company_name.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert company_name.runs[0].bold is True

    title_paragraph = document.tables[0].cell(0, 0).paragraphs[0]
    assert title_paragraph.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert title_paragraph.text == (
        "PROCES-VERBAL DES DECISIONS\n"
        " DE L’ASSEMBLEE GENERALE\n"
        " DU 13 mai 2026"
    )
    assert all(run.bold for run in title_paragraph.runs if run.text.strip())

    first_decision = _find_paragraph(document, "PREMIERE DECISION")
    assert first_decision.runs[0].bold is True
    assert first_decision.runs[0].underline is True
    assert first_decision.paragraph_format.space_before is not None

    vote_formula = _find_paragraph(document, VOTE_FORMULA)
    assert vote_formula.runs[0].italic is True

    decision_item = _find_paragraph(document, "- Nomination du gérant")
    assert decision_item.text == "- Nomination du gérant"

    signature_name = _find_paragraph(document, "Alice Durand")
    assert signature_name.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert signature_name.runs[0].bold is True

    acceptance = _find_paragraph(
        document,
        (
            "Faire précéder la signature de la mention "
            "« Bon pour acceptation des fonctions de gérant »"
        ),
    )
    assert acceptance.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert acceptance.runs[0].italic is True


# ---------------------------------------------------------------------------
# Extension SELAS : nomination de PLUSIEURS dirigeants (President + Directeur
# General), d'apres le modele PV nominations dirigeants (Albane 2026-06-17).
# Vocabulaire « actions », une decision par dirigeant, bloc signatures 2 colonnes.
# ---------------------------------------------------------------------------


def _selas_dirigeants() -> list[DirigeantNomine]:
    president = DirigeantNomine(
        genre=Gender.MASCULIN,
        civilite_affichage="Monsieur",
        prenom="Alain",
        nom="FEDOROWSKY",
        date_naissance=date(1980, 2, 20),
        ville_naissance="RENNES",
        departement_naissance="35",
        nationalite="française",
        adresse_personnelle=Address(
            num_voie="31B",
            voie="Boulevard de Sévigné",
            cp="35700",
            ville="RENNES",
        ),
        fonction_affichage="Président",
    )
    directeur_general = DirigeantNomine(
        genre=Gender.MASCULIN,
        civilite_affichage="Monsieur",
        prenom="Jean-Pierre",
        nom="HUBERMAN",
        date_naissance=date(1975, 6, 5),
        ville_naissance="PARIS",
        departement_naissance="75",
        nationalite="française",
        adresse_personnelle=Address(
            num_voie="2",
            voie="rue de la Paix",
            cp="75002",
            ville="PARIS",
        ),
        fonction_affichage="Directeur Général",
    )
    return [president, directeur_general]


def _selas_associes() -> list[Associe]:
    return [
        Associe(
            genre=Gender.MASCULIN,
            civilite_affichage="Monsieur",
            prenom="Alain",
            nom="FEDOROWSKY",
            nb_parts=60,
        ),
        Associe(
            genre=Gender.MASCULIN,
            civilite_affichage="Monsieur",
            prenom="Jean-Pierre",
            nom="HUBERMAN",
            nb_parts=40,
        ),
    ]


def _selas_context(
    *, dirigeants: list[DirigeantNomine] | None = None
) -> DocumentGenerationContext:
    associes = _selas_associes()
    ctx = DocumentGenerationContext(
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Alain",
            nom="FEDOROWSKY",
        ),
        societe=Company(
            forme_sociale="SELAS",
            forme_sociale_affichage="SELAS",
            forme_sociale_abregee="SELAS",
            forme_sociale_complete="société d’exercice libéral par actions simplifiée",
            denomination="SELAS DENTAIRE",
            capital_social="1 000",
            capital_variable=True,
            siege=Address(num_voie="31B", voie="Boulevard de Sévigné", cp="35700", ville="RENNES"),
            ville_rcs="Rennes",
        ),
        decision=DecisionContext(date="15 juin 2026"),
        reunion=ReunionContext(
            date_lettres="quinze juin deux mille vingt-six",
            president=ReunionPresident(
                civilite_president_seance="Monsieur",
                prenom_president_seance="Alain",
                nom_personne_seance="FEDOROWSKY",
            ),
        ),
        capital=CapitalContext(
            nb_parts_total=100,
            valeur_nominale_part="10",
            type_titre="actions",
        ),
        associes=associes,
        dirigeant_nomine=DirigeantNomine(
            genre=Gender.MASCULIN,
            civilite_affichage="Monsieur",
            prenom="Alain",
            nom="FEDOROWSKY",
            date_naissance=date(1980, 2, 20),
            ville_naissance="RENNES",
            departement_naissance="35",
            nationalite="française",
            adresse_personnelle=Address(
                num_voie="31B", voie="Boulevard de Sévigné", cp="35700", ville="RENNES"
            ),
            fonction_affichage="président",
        ),
        signature=Signature(lieu="Rennes", date=date(2026, 6, 15), nombre_exemplaires="quatre"),
    )
    if dirigeants is not None:
        ctx.dirigeants_nomines = dirigeants
    return ctx


def test_pv_nomination_selas_rend_identite_phrase_complete(tmp_path: Path) -> None:
    # A26-PV5 (Akainu M2) : quand un dirigeant porte une `identite_phrase` (SELAS), le PV la rend
    # VERBATIM (profession reglementee + situation maritale du modele Albane) + le wording du
    # modele « pour une durée indéterminée : ». Couvre le chemin de rendu identite_phrase
    # (pv_nomination_gerant.py:660-662) + la bascule use_model_wording (L629) — non exerces sinon.
    phrase = (
        "Monsieur Jean-Guillaume FUCHS, chirurgien-dentiste, de nationalité française, "
        "né le 20 février 1994 à RENNES (35), marié sous le régime de la séparation des biens "
        # Rafael/Albane 2026-07-09 : « demeurant [adresse] » -> « demeurant au [adresse] ».
        "avec société d’acquêts, avec Madame Eva ROUAULT, demeurant au 31B Boulevard de Sévigné, "
        "35700 RENNES"
    )
    dirigeant = DirigeantNomine(
        genre=Gender.MASCULIN, civilite_affichage="Monsieur", prenom="Jean-Guillaume", nom="FUCHS",
        date_naissance=date(1994, 2, 20), ville_naissance="RENNES", departement_naissance="35",
        nationalite="française",
        adresse_personnelle=Address(
            num_voie="31B", voie="Boulevard de Sévigné", cp="35700", ville="RENNES"
        ),
        fonction_affichage="Président", identite_phrase=phrase,
    )
    text = _docx_text(_generate(tmp_path, _selas_context(dirigeants=[dirigeant])))
    assert phrase in text  # rendu verbatim de la phrase du modele
    assert "chirurgien-dentiste" in text  # profession reglementee presente
    assert "Docteur" not in text  # jamais le titre (Akainu B1)
    assert "pour une durée indéterminée :" in text  # wording modele (use_model_wording)


def test_pv_nomination_selas_actions_vocabulary(tmp_path: Path) -> None:
    # Vocabulaire « actions » (SELAS) au lieu de « parts » : intro + bloc associes.
    ctx = _selas_context(dirigeants=_selas_dirigeants())
    text = _docx_text(_generate(tmp_path, ctx))

    # Rafael 2026-07-09 : le capital porte « euros » (accorde) sur le chemin actions aussi.
    assert "au capital de 1 000 euros, composé de 100 actions" in text
    assert "composé de 100 actions, se sont réunis au siège de la Société." in text
    assert "Monsieur Alain FEDOROWSKY, détenant 60 actions," in text
    assert "Monsieur Jean-Pierre HUBERMAN, détenant 40 actions," in text
    assert (
        "Les associés présents ou représentés disposent ensemble la totalité des actions "
        "formant le capital de la société. L’assemblée est habilitée à prendre les "
        "décisions extraordinaires."
    ) in text
    # Pas de vocabulaire « parts » sur le chemin actions.
    assert "détenant 60 parts" not in text
    assert "totalité des parts sociales" not in text


def test_pv_nomination_selas_president_then_directeur_general(tmp_path: Path) -> None:
    # PREMIERE DECISION = President, DEUXIEME DECISION = Directeur General,
    # TROISIEME DECISION = Pouvoirs (modele PV nominations dirigeants).
    ctx = _selas_context(dirigeants=_selas_dirigeants())
    text = _docx_text(_generate(tmp_path, ctx))
    paragraphs = _paragraphs(_generate(tmp_path / "second", ctx))

    # Ordre du jour : une ligne par dirigeant + pouvoirs, en tirets (PV4).
    assert "- Nomination du Président" in paragraphs
    assert "- Nomination du Directeur Général" in paragraphs
    assert "- Pouvoirs" in paragraphs
    assert "· Nomination du Président" not in text

    # PREMIERE DECISION = President.
    assert "PREMIERE DECISION" in text
    assert (
        "L’assemblée générale décide de désigner en qualité de Président, "
        "pour une durée indéterminée :"
    ) in text
    assert (
        "Monsieur Alain FEDOROWSKY, né le 20/02/1980 à RENNES (35), "
        "de nationalité française, demeurant au 31B Boulevard de Sévigné, 35700 RENNES."
    ) in text

    # DEUXIEME DECISION = Directeur General.
    assert "DEUXIEME DECISION" in text
    assert (
        "L’assemblée générale décide de désigner en qualité de Directeur Général, "
        "pour une durée indéterminée :"
    ) in text
    assert (
        "Monsieur Jean-Pierre HUBERMAN, né le 05/06/1975 à PARIS (75), "
        "de nationalité française, demeurant au 2 rue de la Paix, 75002 PARIS."
    ) in text

    # TROISIEME DECISION = Pouvoirs (sans emprunt).
    assert "TROISIEME DECISION" in text
    assert "QUATRIEME DECISION" not in text

    # Deux votes a l'unanimite (un par nomination) + un pour les pouvoirs.
    assert paragraphs.count(VOTE_FORMULA) == 3


def test_pv_nomination_selas_multi_signature_block_two_functions(tmp_path: Path) -> None:
    # Bloc signatures 2 colonnes : nom + « Bon pour acceptation des fonctions de
    # Président » / « ... Directeur Général » (mention verbatim du modele).
    output = _generate(tmp_path, _selas_context(dirigeants=_selas_dirigeants()))
    text = _docx_text(output)

    assert "Bon pour acceptation des fonctions de Président" in text
    assert "Bon pour acceptation des fonctions de Directeur Général" in text
    # Les deux noms sont sur la meme ligne (2 colonnes).
    assert "Alain FEDOROWSKY" in text and "Jean-Pierre HUBERMAN" in text
    # Pas de mention « gérant » sur ce chemin SELAS.
    assert "fonctions de gérant" not in text

    # PV7 (Albane 2026-06-26) : les mentions ne doivent plus decaler les noms.
    # Le bloc est desormais un TABLEAU (cases), chaque colonne portant SON nom
    # ET SA mention -> nom et mention de la meme colonne sont dans la meme cellule,
    # plus aucune jointure par tabulations.
    document = Document(output)
    signature_table = document.tables[-1]
    assert len(signature_table.columns) == 2
    cell_texts = [
        "\n".join(p.text for p in signature_table.cell(0, col).paragraphs)
        for col in range(2)
    ]
    assert "Alain FEDOROWSKY" in cell_texts[0]
    assert "fonctions de Président" in cell_texts[0]
    assert "Jean-Pierre HUBERMAN" in cell_texts[1]
    assert "fonctions de Directeur Général" in cell_texts[1]
    # Plus de separateur tabulation (ancienne mise en page qui decalait).
    assert "\t" not in text


def test_pv_nomination_selas_single_president_keeps_mono_structure(tmp_path: Path) -> None:
    # Un SEUL dirigeant (President) -> pas de comma model wording, pas de DEUXIEME
    # decision de nomination ; mode mono preserve (signature par associes).
    only_president = _selas_dirigeants()[:1]
    ctx = _selas_context(dirigeants=only_president)
    output = _generate(tmp_path, ctx)
    text = _docx_text(output)
    paragraphs = _paragraphs(output)

    assert "- Nomination du Président" in paragraphs
    assert "Nomination du Directeur Général" not in text
    assert "PREMIERE DECISION" in text
    # Sans emprunt ni DG : pouvoirs = DEUXIEME DECISION (mono).
    assert "DEUXIEME DECISION" in text
    assert "TROISIEME DECISION" not in text
    # Mono : pas de virgule modele dans l'intro de la decision.
    assert (
        "L’assemblée générale décide de désigner en qualité de Président pour une "
        "durée indéterminée :"
    ) in text


# ---------------------------------------------------------------------------
# Retours Albane 2026-06-26 (PV nomination dirigeant) — assertions adversariales.
# Verbatim = spec : intitule « dirigeant » et non « gerant » (SELAS), entete
# profession (jamais « Docteur »), ordre du jour en tirets, suppression de la
# mention « X exemplaires », signatures en cases (pas de decalage).
# ---------------------------------------------------------------------------


def test_pv_nomination_selas_intitule_dirigeant_jamais_gerant(tmp_path: Path) -> None:
    # PV1 : « ce ne sont justement pas des gerants » -> aucun « gerant »/« gerante »
    # dans le PV SELAS (l'intitule parle de Président / Directeur Général).
    text = _docx_text(_generate(tmp_path, _selas_context(dirigeants=_selas_dirigeants())))

    assert "gérant" not in text.lower()
    assert "Nomination du Président" in text
    assert "Nomination du Directeur Général" in text


def test_pv_nomination_selas_entete_profession_pas_docteur(tmp_path: Path) -> None:
    # PV2 : l'entete affiche la PROFESSION (« chirurgien-dentiste »), jamais le
    # titre « Docteur » — meme si le front n'a fourni que « Docteur ».
    ctx = _selas_context(dirigeants=_selas_dirigeants())
    for associe in ctx.associes:
        associe.profession_reglementee = "chirurgien-dentiste"
    paragraphs = _paragraphs(_generate(tmp_path, ctx))

    assert (
        "Société d’exercice libéral par actions simplifiée de chirurgien-dentiste"
        in paragraphs
    )
    assert not any("de Docteur" in p for p in paragraphs)


def test_pv_nomination_header_excludes_docteur_title_fallback(tmp_path: Path) -> None:
    # PV2 (garde-fou) : si la seule donnee est « Docteur » (titre), l'entete ne
    # doit PAS afficher « de Docteur » — le titre est ecarte comme profession.
    ctx = _selas_context(dirigeants=_selas_dirigeants())
    for associe in ctx.associes:
        associe.profession_reglementee = None
        associe.qualification_principale = None
        associe.profession = "Docteur"
    text = _docx_text(_generate(tmp_path, ctx))

    assert "de Docteur" not in text


def test_pv_nomination_selas_ordre_du_jour_tirets(tmp_path: Path) -> None:
    # PV4 : points de l'ordre du jour prefixes d'un tiret « - » (plus de « · »).
    paragraphs = _paragraphs(_generate(tmp_path, _selas_context(dirigeants=_selas_dirigeants())))

    assert "- Nomination du Président" in paragraphs
    assert "- Nomination du Directeur Général" in paragraphs
    assert "- Pouvoirs" in paragraphs
    assert not any(p.startswith("·") for p in paragraphs)


def test_pv_nomination_supprime_mention_exemplaires(tmp_path: Path) -> None:
    # PV6 : « en quatre exemplaires » apres la ville est supprime (SELAS + SELARL).
    selas_text = _docx_text(_generate(tmp_path, _selas_context(dirigeants=_selas_dirigeants())))
    assert "Fait à Rennes" in selas_text
    assert "exemplaires" not in selas_text
    assert "quatre exemplaires" not in selas_text

    selarl_text = _docx_text(_generate(tmp_path / "selarl", _context(associes=_associes(1))))
    assert "Fait à Paris" in selarl_text
    assert "exemplaires" not in selarl_text


def test_pv_nomination_selarl_garde_intitule_gerant(tmp_path: Path) -> None:
    # Non-regression PV1 : la SELARL nomme un GERANT -> « gérant »/« gérante »
    # reste correct (l'intitule « dirigeant » de PV1 ne s'impose qu'au SELAS).
    text = _docx_text(_generate(tmp_path, _context(associes=_associes(1))))

    assert "Nomination du gérant" in text
    assert "Bon pour acceptation des fonctions de gérante" in text


def _find_para(document: Document, needle: str):
    return next(p for p in document.paragraphs if needle in p.text)


def test_pv_associe_unique_designation_client_en_interligne_simple(
    tmp_path: Path,
) -> None:
    # Retour Albane « mise en forme » 1.4 (M3) : la DESIGNATION DU CLIENT (nom, naissance,
    # adresse, nationalite) de l'associe unique sort en interligne SIMPLE (1.0), pas en
    # interligne par defaut. Branche ASSOCIE UNIQUE.
    document = Document(_generate(tmp_path, _context(associes=_associes(1))))
    for needle in (
        "Madame Alice Durand",
        "Née le 09/07/1986",
        "Demeurant au 3 rue des Lilas",
        "De nationalité française",
    ):
        assert _find_para(document, needle).paragraph_format.line_spacing == 1.0


def test_pv_ag_multi_enumeration_associes_en_interligne_simple(tmp_path: Path) -> None:
    # Retour Albane 1.4 (M3) : la designation des clients (enumeration des associes
    # presents/representes) de l'AG multi sort en interligne SIMPLE (1.0). Branche MULTI.
    document = Document(_generate(tmp_path, _context(associes=_associes(2))))
    for needle in (
        "Madame Alice Durand, détenant 60",
        "Monsieur Bruno Martin, détenant 40",
    ):
        assert _find_para(document, needle).paragraph_format.line_spacing == 1.0


# ---------------------------------------------------------------------------
# Micro holding (retours Albane 2026-07-09) : societe civile a capital variable.
# C1 (« Société civile » fige), C2 (capital variable), C3 (date encadre
# « JJ MOIS AAAA » majuscule), C4 (chaque associe signe sous son nom + espace).
# Scope MICRO_HOLDING : les autres types restent inchanges (cf. tests SCI/SELARL/SELAS).
# ---------------------------------------------------------------------------


def _micro_context(*, associes: list[Associe] | None = None) -> DocumentGenerationContext:
    ctx = _context(associes=associes)
    ctx.structure = "MICRO_HOLDING"
    ctx.societe.denomination = "MA MICRO HOLDING"
    ctx.societe.forme_sociale = "société civile"
    # Avant C1, la cle interne de structure fuyait en en-tete / 1re phrase.
    ctx.societe.forme_sociale_affichage = "MICRO_HOLDING"
    ctx.societe.forme_sociale_libelle_long = None
    ctx.societe.forme_sociale_complete = None
    ctx.societe.capital = "1020"
    ctx.societe.capital_social = "1020"
    # C3 : la date de decision arrive en « JJ/MM/AAAA » dans le flux reel.
    ctx.decision = DecisionContext(date="13/05/2026")
    return ctx


def test_pv_micro_holding_c1_forme_societe_civile(tmp_path: Path) -> None:
    # C1 : « Société civile » (texte fige) en en-tete ET dans la 1re phrase ; jamais
    # la cle interne « MICRO_HOLDING ».
    paragraphs = _paragraphs(_generate(tmp_path, _micro_context()))
    assert "Société civile" in paragraphs
    assert "MICRO_HOLDING" not in "\n".join(paragraphs)
    intro = next(p for p in paragraphs if p.startswith("Les associés de la"))
    assert intro.startswith("Les associés de la Société civile MA MICRO HOLDING,")


def test_pv_micro_holding_c2_capital_variable(tmp_path: Path) -> None:
    # C2 : mention capital variable (meme wording que la domiciliation micro) ;
    # plus jamais « Au capital de <montant> euros ».
    text = _docx_text(_generate(tmp_path, _micro_context()))
    assert (
        "À capital variable au capital minimum de 1 020 € et au capital effectif de 1 020 €"
    ) in text
    assert "Au capital de 1 020 euros" not in text


def test_pv_micro_holding_c3_date_encadre_majuscule(tmp_path: Path) -> None:
    # C3 : date de l'encadre au format « JJ MOIS AAAA » (mois MAJUSCULE accentue).
    document = Document(_generate(tmp_path, _micro_context()))
    framed = "\n".join(
        cell.text for table in document.tables for row in table.rows for cell in row.cells
    )
    assert "DU 13 MAI 2026" in framed
    assert "13/05/2026" not in framed


def test_pv_micro_holding_c4_signature_par_associe_avec_espace(tmp_path: Path) -> None:
    # C4 : chaque associe signe SOUS SON NOM ; une zone de signature (paragraphe vide)
    # suit chaque nom (au lieu des noms empiles sans espace).
    document = Document(_generate(tmp_path, _micro_context()))
    paras = list(document.paragraphs)
    idx_alice = next(i for i, p in enumerate(paras) if p.text == "Alice Durand")
    idx_bruno = next(i for i, p in enumerate(paras) if p.text == "Bruno Martin")
    assert paras[idx_alice + 1].text.strip() == ""  # zone de signature sous Alice
    assert idx_bruno > idx_alice + 1  # Bruno vient apres la zone d'Alice
    assert paras[idx_bruno + 1].text.strip() == ""  # zone de signature sous Bruno


def test_pv_non_micro_capital_line_unchanged(tmp_path: Path) -> None:
    # Non-regression : sans structure micro, la ligne de capital reste « Au capital
    # de <montant> euros » et aucune mention capital-variable n'apparait.
    text = _docx_text(_generate(tmp_path))
    assert "Au capital de 1 000 euros" in text
    assert "À capital variable au capital minimum" not in text


# ---------------------------------------------------------------------------
# Retours Rafael 2026-07-09 (soir) — PV nomination (P1/P2).
# P1 : espacement COMPACT sur la designation du client + les decisions.
# P2 : en-tete SPFPLAS = forme legale complete (profession reglementee au pluriel).
# ---------------------------------------------------------------------------


def _spfplas_context() -> DocumentGenerationContext:
    """Contexte d'un PV nomination d'une SPFPL par actions simplifiee (SPFPLAS),
    calque sur le flux reel (spfpl_slice) : forme abregee « SPFPL », libelle front
    « société de participations financières de professions libérales », cedant
    portant `profession_reglementee_pluriel`, titres = actions."""
    ctx = _context(associes=_associes(1))
    ctx.societe.forme_sociale = "SPFPL"
    ctx.societe.forme_sociale_affichage = "SPFPL"
    ctx.societe.forme_sociale_abregee = "SPFPL"
    ctx.societe.forme_sociale_complete = (
        "société de participations financières de professions libérales"
    )
    ctx.societe.forme_sociale_libelle_long = (
        "Société de participations financières de professions libérales"
    )
    ctx.societe.denomination = "SPFPL DURAND"
    ctx.capital.type_titre = "actions"
    ctx.dirigeant_nomine.fonction_affichage = "président"
    ctx.cedant = SpfplPerson(
        civilite_affichage="Monsieur",
        prenom="Alice",
        nom="Durand",
        genre=Gender.FEMININ,
        profession_reglementee_pluriel="chirurgiens-dentistes",
    )
    return ctx


def test_pv_nomination_spfplas_header_forme_legale_complete(tmp_path: Path) -> None:
    # P2 : l'en-tete SPFPLAS rend la forme LEGALE COMPLETE (bonne casse, profession
    # reglementee AU PLURIEL titre-casee, forme « par actions simplifiée »), au lieu du
    # libelle « société de participations financières de professions libérales » du front.
    ctx = _spfplas_context()
    paragraphs = _paragraphs(_generate(tmp_path, ctx))
    text = _docx_text(_generate(tmp_path / "second", ctx))

    assert (
        "Société de Participations Financières de Profession Libérale de "
        "Chirurgiens-Dentistes par actions simplifiée"
    ) in paragraphs
    assert "société de participations financières de professions libérales" not in text
    assert "professions libérales" not in text  # jamais le pluriel « professions »


def test_pv_nomination_spfplas_header_uses_associe_plural_fallback(tmp_path: Path) -> None:
    # P2 (repli) : sans cedant/apporteur, la profession plurielle est prise sur l'associe
    # s'il la porte (`profession_reglementee_pluriel`).
    ctx = _spfplas_context()
    ctx.cedant = None
    ctx.associes[0].profession_reglementee_pluriel = "chirurgiens-dentistes"
    paragraphs = _paragraphs(_generate(tmp_path, ctx))
    assert (
        "Société de Participations Financières de Profession Libérale de "
        "Chirurgiens-Dentistes par actions simplifiée"
    ) in paragraphs


def test_pv_nomination_spfplas_header_without_plural_falls_back(tmp_path: Path) -> None:
    # P2 (garde-fou) : sans profession plurielle connue, on ne DEVINE rien -> repli sur le
    # libelle existant (pas de format SPFPLAS incomplet, pas de crash).
    ctx = _spfplas_context()
    ctx.cedant = None
    ctx.associes[0].profession_reglementee_pluriel = None
    text = _docx_text(_generate(tmp_path, ctx))
    # Repli = le libelle existant (forme_sociale_complete du front, non modifie).
    assert "société de participations financières de professions libérales" in text
    assert "Profession Libérale de" not in text  # pas de format SPFPLAS incomplet


def test_pv_associe_unique_designation_client_compact_spacing(tmp_path: Path) -> None:
    # P1 : la designation du client (nom / naissance / adresse / nationalite / qualite) sort
    # en espacement COMPACT (plus d'« espace parasite » de 10 pt entre chaque ligne).
    document = Document(_generate(tmp_path, _context(associes=_associes(1))))
    for needle in (
        "Madame Alice Durand",
        "Née le 09/07/1986",
        "Demeurant au 3 rue des Lilas",
        "De nationalité française",
        "Associée unique, propriétaire",
    ):
        assert (
            _find_para(document, needle).paragraph_format.space_after.pt
            == _PV_COMPACT_SPACE_AFTER_PT
        )


def test_pv_associe_unique_decisions_compact_but_keep_inter_decision_space(
    tmp_path: Path,
) -> None:
    # P1 : le corps des decisions est resserre (espacement COMPACT) MAIS l'aeration ENTRE
    # decisions reste (space_before du titre de decision = 10 pt).
    document = Document(_generate(tmp_path, _context(associes=_associes(1))))
    body = _find_para(document, "L’associée unique décide de désigner")
    assert body.paragraph_format.space_after.pt == _PV_COMPACT_SPACE_AFTER_PT
    # Ordre du jour (enonciations des decisions) compact aussi.
    assert (
        _find_paragraph(document, "- Nomination du gérant").paragraph_format.space_after.pt
        == _PV_COMPACT_SPACE_AFTER_PT
    )
    # Aeration entre decisions preservee.
    assert _find_paragraph(document, "DEUXIEME DECISION").paragraph_format.space_before.pt == 10.0


def test_pv_ag_multi_designation_and_decisions_compact_spacing(tmp_path: Path) -> None:
    # P1 : idem sur la branche AG multi — enumeration des associes (designation client) +
    # corps des decisions en espacement COMPACT, aeration inter-decisions preservee.
    document = Document(_generate(tmp_path, _context(associes=_associes(2))))
    for needle in (
        "Madame Alice Durand, détenant 60",
        "Monsieur Bruno Martin, détenant 40",
    ):
        assert (
            _find_para(document, needle).paragraph_format.space_after.pt
            == _PV_COMPACT_SPACE_AFTER_PT
        )
    body = _find_para(document, "Madame Claire Bernard, née le")
    assert body.paragraph_format.space_after.pt == _PV_COMPACT_SPACE_AFTER_PT
    vote = _find_paragraph(document, VOTE_FORMULA)
    assert vote.paragraph_format.space_after.pt == _PV_COMPACT_SPACE_AFTER_PT
    assert _find_paragraph(document, "PREMIERE DECISION").paragraph_format.space_before.pt == 10.0
