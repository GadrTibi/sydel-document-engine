from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    ApportTitres,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    DepotFonds,
    DocumentGenerationContext,
    DossierOptions,
    ExerciceSocial,
    OperationSpfpl,
    Person,
    ProfessionalEntity,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplOrdre,
    SpfplPerson,
    SpfplRepresentant,
)
from sydel_doc_engine.generators.lot_04.statuts_spfpl_apport import (
    StatutsSpfplApportGenerator,
)
from sydel_doc_engine.generators.lot_04.statuts_spfpl_cession import (
    StatutsSpfplCessionGenerator,
)


def _base_context(*, operation: str) -> DocumentGenerationContext:
    is_apport = operation == "apport"
    founder = SpfplPerson(
        civilite_affichage="Docteur",
        prenom="Camille",
        prenoms="Camille Andre",
        nom="Martin",
        genre=Gender.MASCULIN,
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgiens-dentistes",
        date_naissance=date(1980, 1, 2),
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        situation_maritale="marie",
        regime_matrimonial="la communaute legale",
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
            ville="Paris",
            numero="12345",
            numero_rpps="10000000001",
        ),
    )
    return DocumentGenerationContext(
        structure="SPFPL apport" if is_apport else "SPFPL cession",
        dossier_options=DossierOptions(
            apport=is_apport,
            cession=not is_apport,
            associe_unique=True,
        ),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 14)),
        operation_spfpl=OperationSpfpl(type=operation),
        societe_spfpl=SocieteSpfpl(
            denomination="SPFPL MARTIN",
            forme_sociale="par actions simplifiee",
            capital_social="60 000",
            capital_social_lettres="soixante mille",
            valeur_nominale_action="100",
            valeur_nominale_action_lettres="cent",
            siege=Address(adresse_affichee="10 rue de la Paix, 75002 Paris"),
        ),
        actionnaire_unique=founder,
        # Rafael 2026-07-09 : contrat commun `Apport.montant_lettres` = lettres NUES
        # (le slice fournit number_words_from_value ; l'unite est composee au rendu).
        apport=Apport(montant="60 000", montant_lettres="soixante mille"),
        depot_fonds=DepotFonds(
            banque=CessionBanque(
                nom="BANQUE EXEMPLE",
                adresse_affichee="1 boulevard Haussmann, 75009 Paris",
            )
        ),
        apport_titres=ApportTitres(
            nb_parts=60,
            nb_parts_lettres="soixante",
            plage_parts="41 a 100",
            valeur_globale="60 000",
            valeur_nominale_action="100",
            valeur_nominale_action_lettres="cent",
        ),
        societe_cible=SocieteCible(
            denomination="SELARL CABINET MARTIN",
            siege=Address(adresse_affichee="12 avenue des Ternes, 75017 Paris"),
            ville_rcs="Paris",
            numero_rcs="900 000 001",
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=600,
            valeur_nominale_action="100",
        ),
        exercice_social=None,
        commissaire_aux_apports=_entity(),
    )


def _entity() -> ProfessionalEntity:
    return ProfessionalEntity(
        denomination="CAA EXPERTISE",
        forme_sociale="SAS",
        capital_social="1 000 euros",
        siege=Address(adresse_affichee="1 rue Scheffer, 75016 Paris"),
        ville_rcs="Paris",
        numero_rcs="948 483 730",
        representant=SpfplRepresentant(
            civilite_affichage="Monsieur",
            prenom="Nabil",
            nom="Saidi",
        ),
    )


def _with_exercice(ctx: DocumentGenerationContext) -> DocumentGenerationContext:
    ctx.exercice_social = ExerciceSocial(
        debut="1er janvier",
        fin="31 decembre",
        date_cloture_premier_exercice="31 decembre 2026",
    )
    return ctx


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs if paragraph.text)
    return "\n".join(texts)


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text


def _para_by_text(document: Document, needle: str):
    return next(p for p in document.paragraphs if needle in p.text)


def _paras_by_prefix(document: Document, prefix: str) -> list:
    return [p for p in document.paragraphs if p.text.strip().startswith(prefix)]


def test_statuts_spfpl_cession_generates_source_overlay_without_signature_date(
    tmp_path: Path,
) -> None:
    output_path = StatutsSpfplCessionGenerator().generate(
        _with_exercice(_base_context(operation="cession")),
        tmp_path,
    )

    text = _docx_text(output_path)
    document = Document(output_path)
    table_text = "\n".join(
        paragraph.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for paragraph in cell.paragraphs
    )
    acceptance = next(
        p for p in document.paragraphs if "Bon pour acceptation des fonctions" in p.text
    )

    # R10 (Rafael 2026-07-07) : le fichier statuts porte la denomination.
    assert output_path.name == "Statuts SPFPL MARTIN.docx"
    assert "Société de Participations Financières de Profession Libérale" in text
    assert "BANQUE EXEMPLE sise 1 boulevard Haussmann, 75009 Paris" in text
    # Rafael 2026-07-09 « supprimer partout » : civilite CIVILE (« Monsieur »), plus « Docteur ».
    assert "Le\nMonsieur Camille Martin" in text
    assert "Docteur" not in text
    assert "Le 14/05/2026" not in text
    assert "Nomination d’un commissaire aux apports" not in text
    # KAN-3 (Albane 2026-07-13) : les bandeaux ENCADRES de groupe de sections sont SUPPRIMES
    # (incoherents — presents des « DECISIONS DES ACTIONNAIRES » mais absents en tete et avant
    # l'art. 19). Seuls subsistent les cadres « STATUTS » (titre) et l'annexe.
    assert "DECISIONS DES ACTIONNAIRES" not in table_text
    assert "ETAT DES ENGAGEMENTS PRIS AVANT" in table_text
    assert any(run.italic for run in acceptance.runs)
    # #1 (onglet 24) : l'ANNEXE 1 ne contient plus la lettre de mission ni l'acompte Sydel
    # (supprimes de tous les statuts ; ne subsistaient que dans le template SPFPL cession).
    assert "lettre de mission" not in text
    assert "acompte des honoraires" not in text
    _assert_clean(text)

    # FORME (FIDELITY_AUDIT_V1, volet 2) : la mise en forme doit coller au modele source DOCX.
    # FIX-F1 / STYLE-1 : bloc de titre centre (denomination en gras via Heading 3 source).
    denomination = document.paragraphs[0]
    # S1 (Rafael 2026-07-09) SUPERSEDE 6.8 (Albane 2026-07-06) : le bloc-titre porte la SEULE
    # denomination (plus « Statuts <Nom> »), SANS espacement entre les lignes de l'en-tete.
    assert denomination.text.strip() == "SPFPL MARTIN"
    assert denomination.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert denomination.runs[0].bold is True
    assert denomination.paragraph_format.space_after == Pt(0)
    for needle in ("Société de Participations", "Au capital de", "Siège social"):
        header_line = _para_by_text(document, needle)
        assert header_line.alignment == WD_ALIGN_PARAGRAPH.CENTER
        assert header_line.paragraph_format.space_after == Pt(0)
    # S2 (Rafael 2026-07-09) : « STATUTS » dans un ENCADRE (table 1x1), plus un top-level
    # paragraphe ; le deroule commence apres un SAUT DE PAGE. Deux sauts au total (apres
    # l'encadre STATUTS + avant l'ANNEXE, S5).
    box_texts = [
        para.text.strip()
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for para in cell.paragraphs
    ]
    assert "STATUTS" in box_texts
    assert "STATUTS" not in [p.text.strip() for p in document.paragraphs]
    assert document.element.body.xml.count('w:type="page"') >= 2
    # FIX-F2 / STYLE-2 : "Le soussigné :" souligne. S3 : pas d'espacement superflu apres.
    soussigne = _para_by_text(document, "Le soussigné")
    assert soussigne.runs[0].underline is True
    assert soussigne.paragraph_format.space_after == Pt(0)
    # S4 (Rafael 2026-07-09) : l'ARTICLE 26 (source « ARTICLE\t26 », tabulation) est en GRAS
    # comme les autres titres d'article (il tombait auparavant en paragraphe de corps).
    article_26 = _para_by_text(document, "CONTROLE DES ASSOCIES")
    assert article_26.text.strip().startswith("ARTICLE")
    assert article_26.runs[0].bold is True
    # S5 (Rafael 2026-07-09) : « Fait a … » a GAUCHE, signature client (nom) + mention a DROITE.
    assert _para_by_text(document, "Fait à").alignment == WD_ALIGN_PARAGRAPH.LEFT
    signataire = next(
        p for p in document.paragraphs if p.text.strip() == "Monsieur Camille Martin"
    )
    assert signataire.alignment == WD_ALIGN_PARAGRAPH.RIGHT
    assert signataire.runs[0].bold is True
    assert acceptance.alignment == WD_ALIGN_PARAGRAPH.RIGHT
    # FIX-F3 / STYLE-3 : la ligne d'identite est en gras (run unique incl. le tiret), JUSTIFY.
    # Retour fonctionnel 7.1 (Albane 2026-07-06) / M2 (Akainu 2026-07-06) : « Utiliser 'Prénom'
    # (pas 'Prénoms complets') DANS LES STATUTS » SANS RESERVE -> le soussigne ET la nomination
    # du President rendent le PRENOM usuel (« Camille »). Plus AUCUN « Camille Andre » (prenoms
    # complets) dans les statuts. Rafael 2026-07-09 « supprimer partout » : les DEUX lignes
    # d'identite (soussigne + President) sont en civilite CIVILE = « - Monsieur Camille Martin ».
    # Match EXACT (les lignes d'apport/repartition commencent aussi par « - Monsieur Camille
    # Martin » depuis R3 -> on ne compte que les lignes d'identite pures).
    assert "Camille Andre" not in text
    identites = [
        p for p in document.paragraphs if p.text.strip() == "- Monsieur Camille Martin"
    ]
    assert len(identites) == 2  # soussigne + nomination President, tous deux en prenom usuel
    for identite in identites:
        assert identite.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
        assert identite.runs[0].bold is True
        # M2 (Akainu doc-entier 2026-07-09) : la name line OUVRE le bloc identite compact (2pt),
        # comme « Le soussigné : » (0) et le PV de nomination (bloc identite a 2pt) — coherence.
        assert identite.paragraph_format.space_after == Pt(2)
    # M2 : les lignes CIVILES du bloc identite (adresse, situation maritale) sont AUSSI compactees
    # a 2pt (elles gardaient 6pt : « S3 a moitie »).
    assert _para_by_text(document, "Demeurant au").paragraph_format.space_after == Pt(2)
    assert (
        _para_by_text(document, "sous le régime de la communauté légale avec Madame")
        .paragraph_format.space_after
        == Pt(2)
    )
    # FIX-F3 / STYLE-4 : lignes de capital / total (Art. 6 & 8) en gras.
    total_apports = _para_by_text(document, "Total des apports")
    assert total_apports.runs[0].bold is True
    # Art. 8 (cession) : "- Monsieur ... actions" → identite en gras, bourrage de points non gras
    # (Rafael 2026-07-09 « supprimer partout » : civilite civile, plus « Le Docteur »).
    repartition = next(
        p
        for p in document.paragraphs
        if p.text.strip().startswith("- Monsieur Camille Martin")
        and p.text.strip().endswith("actions")
    )
    assert repartition.runs[0].bold is True
    assert repartition.runs[-1].bold in (False, None)
    total_actions = _para_by_text(document, "Total des actions composant")
    assert total_actions.runs[0].bold is True


def test_statuts_spfpl_apport_comparution_marie_avec_conjoint_et_pacse(tmp_path: Path) -> None:
    # Rafael 2026-07-09 (supersede le verrou « statut nu » du 2026-07-06) : la comparution
    # des statuts APPORT porte le CONJOINT du marie — « Marié avec Alice Martin » (prenom +
    # nom, sans civilite : meme wording que le contrat d'apport DOC-041), SANS « sous le
    # régime de … » (reserve au modele CESSION, ligne combinee). Le PACSE affiche son
    # partenaire via la clause ratifiee Albane 6.3/7.3 (« Pacsé avec Madame Alice Martin »,
    # civilite incluse). « Pas de mention sans nom » : partenaire pacse absent -> statut nu.
    cases = (
        ("marié", "Marié avec Alice Martin"),
        ("pacsé", "Pacsé avec Madame Alice Martin"),
    )
    for situ, attendu in cases:
        ctx = _with_exercice(_base_context(operation="apport"))
        ctx.actionnaire_unique.situation_maritale = situ
        if situ == "pacsé":
            ctx.actionnaire_unique.regime_matrimonial = None
        document = Document(StatutsSpfplApportGenerator().generate(ctx, tmp_path / situ))
        lignes = [p.text.strip() for p in document.paragraphs if p.text.strip() == attendu]
        # comparution du soussigne + nomination du President (meme token, 2 blocs liste).
        assert lignes, f"ligne « {attendu} » introuvable (apport)"
        # jamais de regime sur le modele apport (marie comme pacse)
        assert not any("sous le régime de" in p.text for p in document.paragraphs)


def test_statuts_spfpl_apport_pacse_sans_partenaire_statut_nu(tmp_path: Path) -> None:
    # « Pas de mention sans nom » (Albane 6.3, conserve par Rafael 2026-07-09) : un pacse
    # SANS partenaire renseigne rend « Pacsé » nu — jamais « avec (À COMPLÉTER) ».
    ctx = _with_exercice(_base_context(operation="apport"))
    ctx.actionnaire_unique.situation_maritale = "pacsé"
    ctx.actionnaire_unique.regime_matrimonial = None
    ctx.actionnaire_unique.conjoint = None
    document = Document(StatutsSpfplApportGenerator().generate(ctx, tmp_path))
    pacse_lines = [
        p.text.strip()
        for p in document.paragraphs
        if p.text.strip().lower().startswith("pacsé")
    ]
    assert pacse_lines, "aucune ligne matrimoniale « pacsé » trouvee (apport)"
    assert all(line == "Pacsé" for line in pacse_lines)
    assert not any("COMPLÉTER" in p.text for p in document.paragraphs)


def test_statuts_spfpl_apport_generates_nature_overlay_and_signature_date(
    tmp_path: Path,
) -> None:
    output_path = StatutsSpfplApportGenerator().generate(
        _with_exercice(_base_context(operation="apport")),
        tmp_path,
    )

    text = _docx_text(output_path)

    # R10 (Rafael 2026-07-07) : le fichier statuts porte la denomination.
    assert output_path.name == "Statuts SPFPL MARTIN.docx"
    assert "Apports en nature" in text
    assert "SELARL CABINET MARTIN" in text
    assert "ayant son siège 12 avenue des Ternes, 75017 Paris" in text
    assert "Le 14/05/2026" in text
    assert "Ouverture d'un compte bancaire auprès de la Banque" not in text
    _assert_clean(text)

    document = Document(output_path)
    # FORME (FIDELITY_AUDIT_V1, volet 2) — meme exigences que la cession, sur le modele apport.
    denomination = document.paragraphs[0]
    # S1 (Rafael 2026-07-09) SUPERSEDE 6.8 : le bloc-titre porte la SEULE denomination
    # (plus « Statuts <Nom> »), sans espacement entre les lignes de l'en-tete.
    assert denomination.text.strip() == "SPFPL MARTIN"
    assert denomination.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert denomination.runs[0].bold is True
    assert denomination.paragraph_format.space_after == Pt(0)
    for needle in ("Société par actions", "Société de Participations", "Siège social"):
        assert _para_by_text(document, needle).alignment == WD_ALIGN_PARAGRAPH.CENTER
    # S2 : « STATUTS » dans un encadre (plus un top-level paragraphe) + saut(s) de page.
    box_texts = [
        para.text.strip()
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for para in cell.paragraphs
    ]
    assert "STATUTS" in box_texts
    assert "STATUTS" not in [p.text.strip() for p in document.paragraphs]
    assert document.element.body.xml.count('w:type="page"') >= 2
    # S3 : « Le soussigné » souligne, sans espacement superflu apres.
    soussigne = _para_by_text(document, "Le soussigné")
    assert soussigne.runs[0].underline is True
    assert soussigne.paragraph_format.space_after == Pt(0)
    # S4 : ARTICLE 26 (source « ARTICLE\t26 ») en gras.
    article_26 = _para_by_text(document, "CONTROLE DES ASSOCIES")
    assert article_26.runs[0].bold is True
    # Rafael 2026-07-09 « supprimer partout » : civilite CIVILE, plus « Docteur ». Match EXACT :
    # la ligne de repartition commence aussi par « - Monsieur Camille Martin » (+ suffixe actions)
    # -> on ne compte que les 2 lignes d'identite pures (soussigne + President).
    identites = [
        p for p in document.paragraphs if p.text.strip() == "- Monsieur Camille Martin"
    ]
    assert len(identites) == 2
    for identite in identites:
        assert identite.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
        assert identite.runs[0].bold is True
    # Art. 8 apport : repartition et total des actions en gras (source idx127/128).
    # Rafael 2026-07-09 « supprimer partout » : « - Le Docteur … » -> « - Monsieur … ».
    assert _para_by_text(document, "- Monsieur Camille Martin").runs[0].bold is True
    assert _para_by_text(document, "Total des actions composant").runs[0].bold is True
    # Art. 6 apport : les totaux d'apports ne sont PAS en gras dans la source (pas d'ajout).
    assert _para_by_text(document, "Total des apports en nature").runs[0].bold in (False, None)
    assert _para_by_text(document, "Total des apports réalisés").runs[0].bold in (False, None)


def test_statuts_spfpl_blocks_multi_associes(tmp_path: Path) -> None:
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.capital_souscription.souscripteurs.append(CapitalSouscripteur(prenom="Camille"))
    ctx.capital_souscription.souscripteurs.append(CapitalSouscripteur(prenom="Louise"))

    with pytest.raises(ValueError, match="multi-associes"):
        StatutsSpfplCessionGenerator().generate(ctx, tmp_path)


# ---------------------------------------------------------------------------
# Verrous de VALEUR (Akainu 2026-07-06, regle 65/68 : accord / conversion / casse).
# ---------------------------------------------------------------------------


def test_statuts_spfpl_art8_euro_agreement_plural(tmp_path: Path) -> None:
    """7.5 (Albane 2026-07-06) — VALEUR : la valeur nominale de l'action porte « euro(s) »
    ACCORDE au montant (100 -> « cent euros (100 €) »). Anti double-euro."""
    ctx = _with_exercice(_base_context(operation="cession"))
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "actions de cent euros (100 €) chacune" in text
    assert "euro euro" not in text
    assert "euros euros" not in text


def test_statuts_spfpl_art8_euro_agreement_singular(tmp_path: Path) -> None:
    """7.5 / accord euro (Akainu 2026-07-06) — VALEUR : une valeur nominale de 1 rend
    « un euro » (SINGULIER), JAMAIS « un euros ». Albane 2026-07-07 (R6) : ELIDE —
    « d'un euro », plus « de un euro »."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.societe_spfpl.valeur_nominale_action = "1"
    ctx.societe_spfpl.valeur_nominale_action_lettres = "un"
    ctx.capital_souscription.valeur_nominale_action = "1"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "actions d’un euro (1 €) chacune" in text
    assert "de un euro" not in text  # R6 : forme non elidee proscrite
    assert "un euros" not in text
    assert "euro euro" not in text


def test_statuts_spfpl_art8_valeur_nominale_centime_decimal(tmp_path: Path) -> None:
    """7.5 (Albane 2026-07-06, verbatim RATIFIE) — VALEUR DECIMALE : une valeur nominale
    de 0,01 rend « un centime d'euro (0,01 €) », PAS la figure nue « 0,01 », et SANS double
    « euro » (« un centime d'euro euro » interdit) ni espace parasite.

    Containment 2026-07-06 : le slot `valeur_nominale_action_lettres` porte desormais la
    FIGURE (« 0,01 », ce que produit `number_words_from_value` sur un decimal). La phrase
    monetaire est CALCULEE DEPUIS LA FIGURE par `montant_lettres_avec_unite` au generateur
    (SEUL point de composition). On simule donc le vrai front : le slot lettres = figure."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.societe_spfpl.valeur_nominale_action = "0,01"
    ctx.societe_spfpl.valeur_nominale_action_lettres = "0,01"  # front containment : figure
    ctx.capital_souscription.valeur_nominale_action = "0,01"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    # Albane 2026-07-07 (R6) : ELIDE — « d'un centime d'euro », plus « de un centime ».
    assert "actions d’un centime d’euro (0,01 €) chacune" in text
    assert "de un centime" not in text  # R6 : forme non elidee proscrite
    assert "d’euro euro" not in text
    assert "d’euro (0,01" in text  # unite deja dans la phrase, pas de « euro » ajoute
    assert "  (" not in text  # pas d'espace double la ou l'euro etait ajoute
    # La FIGURE nue ne doit plus occuper le slot rendu (montant_lettres_avec_unite recompose).
    assert "actions de 0,01 (0,01 €)" not in text


def test_statuts_spfpl_art8_valeur_nominale_cinquante_centimes(tmp_path: Path) -> None:
    """7.5 — VALEUR DECIMALE : 0,50 rend « cinquante centimes d'euro (0,50 €) »
    (PLURIEL « centimes », unite « d'euro » incluse). Slot lettres = figure (containment)."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.societe_spfpl.valeur_nominale_action = "0,50"
    ctx.societe_spfpl.valeur_nominale_action_lettres = "0,5"  # front containment : figure
    ctx.capital_souscription.valeur_nominale_action = "0,50"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "actions de cinquante centimes d’euro (0,50 €) chacune" in text
    assert "d’euro euro" not in text


def test_statuts_spfpl_ordre_departement_name_not_number(tmp_path: Path) -> None:
    """7.4 (Albane 2026-07-06) — VALEUR : l'Ordre s'affiche par le NOM du departement
    (« de Seine-et-Marne »), JAMAIS le NUMERO (« de 77 »)."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.actionnaire_unique.ordre.departement = "77"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "Seine-et-Marne" in text
    assert "de 77" not in text
    assert "des Chirurgiens-Dentistes de 77" not in text


def test_statuts_spfpl_title_reprises_company_name(tmp_path: Path) -> None:
    """S1 (Rafael 2026-07-09) SUPERSEDE 6.8 (Albane 2026-07-06) — le bloc-titre porte la
    SEULE denomination (« SPFPL MARTIN »), le mot « Statuts » est retire (le titre « STATUTS »
    figure dans l'encadre plus bas). Verrou explicite (deja couvert par le test de forme)."""
    ctx = _with_exercice(_base_context(operation="cession"))
    document = Document(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert document.paragraphs[0].text.strip() == "SPFPL MARTIN"


def test_statuts_spfpl_marital_line_capitalized_married(tmp_path: Path) -> None:
    """M1 (Akainu 2026-07-06) — 7.2 : la ligne matrimoniale du soussigne commence par une
    MAJUSCULE (« Marié sous le régime … »), pas en minuscule."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.actionnaire_unique.situation_maritale = "marié"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    # B1 (Akainu doc-entier 2026-07-09) : regime ACCENTUE + preposition unique (plus de
    # « sous le régime de regime de communaute » ni « communaute » non accentue).
    assert "Marié sous le régime de la communauté légale avec Madame Alice Martin" in text
    assert "marié sous le régime" not in text  # jamais en minuscule


def test_statuts_spfpl_marital_line_capitalized_single(tmp_path: Path) -> None:
    """M1 (Akainu 2026-07-06) — 7.2 : un statut NON marie (« célibataire ») sort AUSSI
    capitalise (« Célibataire »), dans la comparution ET dans la nomination du President
    (bare token [situation_maritale], propagation regle 68 Q4). Jamais de minuscule en tete."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.actionnaire_unique.situation_maritale = "célibataire"
    ctx.actionnaire_unique.conjoint = None
    ctx.actionnaire_unique.regime_matrimonial = None
    document = Document(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    marital_lines = [
        p.text.strip() for p in document.paragraphs
        if p.text.strip().lower() == "célibataire"
    ]
    # comparution + nomination President : les DEUX lignes existent et sont capitalisees.
    assert marital_lines, "aucune ligne matrimoniale « célibataire » trouvee"
    assert all(line == "Célibataire" for line in marital_lines)
    assert not any(p.text.strip() == "célibataire" for p in document.paragraphs)


def test_statuts_spfpl_marital_line_pacse_shows_partner(tmp_path: Path) -> None:
    """Albane 6.3/7.3 (RATIFIE 2026-07-06) : un actionnaire PACSE affiche son PARTENAIRE
    (« Pacsé avec Madame Alice Martin »), SANS « sous le régime de … » (le PACS n'a pas de
    sous-regime capture par le menu). Capitalise en tete (7.2)."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.actionnaire_unique.situation_maritale = "pacsé"
    ctx.actionnaire_unique.regime_matrimonial = None
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "Pacsé avec Madame Alice Martin" in text
    assert "pacsé sous le régime" not in text
    assert "sous le régime" not in text


def test_statuts_spfpl_marital_line_pacse_without_partner_no_mention(tmp_path: Path) -> None:
    """« Pas de mention sans nom » (Albane 6.3) : un pacse SANS partenaire rend « Pacsé » nu."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.actionnaire_unique.situation_maritale = "pacsé"
    ctx.actionnaire_unique.regime_matrimonial = None
    ctx.actionnaire_unique.conjoint = None
    document = Document(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    pacse_lines = [
        p.text.strip() for p in document.paragraphs
        if p.text.strip().lower().startswith("pacsé")
    ]
    assert pacse_lines, "aucune ligne matrimoniale « pacsé » trouvee"
    assert all(line == "Pacsé" for line in pacse_lines)
    assert "avec" not in " ".join(pacse_lines)
    assert not any("COMPLÉTER" in p.text for p in document.paragraphs)


def test_statuts_spfpl_marital_line_married_unchanged(tmp_path: Path) -> None:
    """Non-regression : un MARIE conserve sa clause complete « sous le régime de … avec … »."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.actionnaire_unique.situation_maritale = "marié"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "Marié sous le régime de la communauté légale avec Madame Alice Martin" in text


def test_statuts_spfpl_marital_regime_from_raw_derivation_values(tmp_path: Path) -> None:
    """B1 (Akainu doc-entier 2026-07-09) — les valeurs BRUTES posees par
    field_derivations.regime_matrimonial_from_status (le chemin de generation REEL, que la
    fixture « la communaute legale » masquait) rendent la forme ACCENTUEE, avec une SEULE
    preposition « de », jamais « sous le régime de regime de communaute »."""
    cases = {
        "regime de communaute": "la communauté légale",
        "communaute universelle": "la communauté universelle",
        "separation de biens": "la séparation de biens",
        "participation aux acquets": "la participation aux acquêts",
    }
    for raw, expected in cases.items():
        ctx = _with_exercice(_base_context(operation="cession"))
        ctx.actionnaire_unique.situation_maritale = "marié"
        ctx.actionnaire_unique.regime_matrimonial = raw
        text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
        assert f"Marié sous le régime de {expected} avec Madame Alice Martin" in text
        # preposition JAMAIS doublee, regime JAMAIS non accentue.
        assert "régime de regime de" not in text
        assert "de communaute avec" not in text
        assert "separation de biens avec" not in text


def test_statuts_spfpl_president_uses_usual_first_name(tmp_path: Path) -> None:
    """M2 (Akainu 2026-07-06) — 7.1 : la nomination du President utilise le PRENOM USUEL
    (« Camille »), pas les prenoms complets (« Camille Andre ») ; « Prénom DANS LES STATUTS »
    sans reserve. Deux lignes d'identite « - Monsieur Camille Martin » (soussigne + President).
    Rafael 2026-07-09 « supprimer partout » : civilite CIVILE, plus « Docteur »."""
    ctx = _with_exercice(_base_context(operation="cession"))
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "Camille Andre" not in text
    # Match EXACT par ligne : les lignes d'apport/repartition COMMENCENT aussi par « - Monsieur
    # Camille Martin » (R3) mais portent une suite ; on ne compte que les 2 lignes d'identite pures.
    assert [line.strip() for line in text.splitlines()].count("- Monsieur Camille Martin") == 2
    assert "Docteur" not in text


# ---------------------------------------------------------------------------
# Verrous Albane 2026-07-07 (retours statuts SPFPL + rapport conformance R4/R5/R6).
# ---------------------------------------------------------------------------


def _table_texts(document: Document) -> list[str]:
    return [
        "\n".join(
            paragraph.text
            for row in table.rows
            for cell in row.cells
            for paragraph in cell.paragraphs
        )
        for table in document.tables
    ]


def test_statuts_spfpl_art8_capital_lettres_puis_chiffres_groupes(tmp_path: Path) -> None:
    """Fix 1 (Albane 2026-07-07) — art. 8 cession : capital en LETTRES puis (CHIFFRES GROUPES) —
    « soixante mille (60 000) euros », plus « 60000 (soixante mille) ». Le montant brut du front
    (« 60000 ») est groupe au rendu."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.societe_spfpl.capital_social = "60000"  # brut, comme injecte par le front
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "fixé à la somme de soixante mille (60 000) euros" in text
    assert "(soixante mille)" not in text  # ancien ordre chiffres (lettres) proscrit
    assert "60000" not in text  # jamais de montant non groupe


def test_statuts_spfpl_art8_capital_six_euros_verbatim_albane(tmp_path: Path) -> None:
    """Fix 1+2 (Albane 2026-07-07, VERBATIM) : capital 6 € / 600 actions -> « six (6) euros »
    (pas « 6 (six) ») et « d'un centime d'euro (0,01 €) chacune » (R6, pas « de un »)."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.societe_spfpl.capital_social = "6"
    ctx.societe_spfpl.capital_social_lettres = "six"
    ctx.societe_spfpl.valeur_nominale_action = "0,01"
    ctx.societe_spfpl.valeur_nominale_action_lettres = "0,01"  # front containment : figure
    ctx.capital_souscription.valeur_nominale_action = "0,01"
    text = _docx_text(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    assert "fixé à la somme de six (6) euros" in text
    assert "6 (six)" not in text
    assert "actions d’un centime d’euro (0,01 €) chacune" in text
    assert "de un" not in text


def test_statuts_spfpl_apport_art8_capital_lettres_puis_chiffres(tmp_path: Path) -> None:
    """Fix 1 (Albane 2026-07-07, propagation cession->apport) — art. 8 apport : « soixante mille
    (60 000) euros ». Lettres calculees en repli depuis la figure quand le slot front
    (`valeur_globale_lettres`) est absent (cas du builder de test)."""
    ctx = _with_exercice(_base_context(operation="apport"))
    ctx.apport_titres.valeur_globale = "60000"  # brut
    text = _docx_text(StatutsSpfplApportGenerator().generate(ctx, tmp_path))
    assert "fixé à la somme de soixante mille (60 000) euros" in text
    assert "somme de 60000 euros" not in text
    assert "60000" not in text


def test_statuts_spfpl_entete_capital_groupe_avec_euros_cession(tmp_path: Path) -> None:
    """Fix 3 (Albane 2026-07-07) — en-tete cession : « Au capital de 60 000 euros »
    (montant GROUPE + mot « euros »), plus « Au capital de 60000 » nu."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.societe_spfpl.capital_social = "60000"  # brut
    document = Document(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    entete = _para_by_text(document, "Au capital de")
    assert entete.text.strip() == "Au capital de 60 000 euros"


def test_statuts_spfpl_entete_capital_groupe_apport(tmp_path: Path) -> None:
    """Fix 3 (Albane 2026-07-07) — en-tete apport : montant GROUPE (« au capital de
    60 000 euros », le mot « euros » etait deja porte par le template)."""
    ctx = _with_exercice(_base_context(operation="apport"))
    ctx.societe_spfpl.capital_social = "60000"  # brut
    text = _docx_text(StatutsSpfplApportGenerator().generate(ctx, tmp_path))
    assert "au capital de 60 000 euros" in text
    assert "au capital de 60000" not in text


def test_statuts_spfpl_ci_montant_groupe_symbole_euro(tmp_path: Path) -> None:
    """Fix 4 (Albane 2026-07-07) — art. 6 cession : « Ci … 60 000 € » (groupe + symbole €),
    plus « 60000 » nu. Meme token pour la ligne « Total des apports » (propagation)."""
    ctx = _with_exercice(_base_context(operation="cession"))
    ctx.apport.montant = "60000"  # brut
    document = Document(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    ligne_ci = next(p for p in document.paragraphs if p.text.strip().startswith("Ci"))
    assert ligne_ci.text.rstrip().endswith("60 000 €")
    total = _para_by_text(document, "Total des apports")
    assert total.text.rstrip().endswith("60 000 €")


def test_statuts_spfpl_annexe_cadre_unique(tmp_path: Path) -> None:
    """Fix 5 (Albane 2026-07-07) — l'annexe (« ANNEXE 1 » + titre sur 2 lignes) sort dans UN
    SEUL cadre (« cadres multiples inutiles » proscrits), sur les DEUX modeles."""
    for operation, generator in (
        ("cession", StatutsSpfplCessionGenerator()),
        ("apport", StatutsSpfplApportGenerator()),
    ):
        ctx = _with_exercice(_base_context(operation=operation))
        document = Document(generator.generate(ctx, tmp_path / operation))
        annexe_tables = [t for t in _table_texts(document) if "ANNEXE 1" in t]
        assert len(annexe_tables) == 1, f"annexe {operation} : cadre unique attendu"
        # Les 3 lignes du titre d'annexe vivent dans le MEME cadre…
        assert "ETAT DES ENGAGEMENTS PRIS AVANT" in annexe_tables[0]
        assert "LA CONSTITUTION DE LA SOCIETE" in annexe_tables[0]
        # … et dans AUCUN autre cadre (plus de cadres empiles).
        autres = [
            t
            for t in _table_texts(document)
            if "ETAT DES ENGAGEMENTS PRIS AVANT" in t and "ANNEXE 1" not in t
        ]
        assert not autres, f"annexe {operation} : cadres multiples detectes"


def test_statuts_spfpl_bandeaux_groupe_supprimes(tmp_path: Path) -> None:
    """KAN-3 (Albane 2026-07-13) : les bandeaux ENCADRES de groupe de sections
    (« DECISIONS DES ACTIONNAIRES », « RESULTATS SOCIAUX », « TRANSFORMATION DE LA SOCIETE »,
    « DISSOLUTION – LIQUIDATION », « CONTESTATIONS », « CONSTITUTION DE LA SOCIETE ») etaient
    INCOHERENTS (presents pour certains groupes, absents en tete et avant l'art. 19). Albane :
    « on les supprime tous ». -> plus AUCUN de ces bandeaux en cadre ; l'espacement
    inter-articles homogene les remplace. Seuls subsistent le cadre « STATUTS » et l'annexe."""
    ctx = _with_exercice(_base_context(operation="cession"))
    document = Document(StatutsSpfplCessionGenerator().generate(ctx, tmp_path))
    tables = _table_texts(document)
    # (« CONSTITUTION DE LA SOCIETE » est aussi un SOUS-texte de l'annexe « LA CONSTITUTION DE LA
    # SOCIETE » -> on exclut les cadres de l'annexe, qui restent legitimes.)
    hors_annexe = [t for t in tables if "ETAT DES ENGAGEMENTS PRIS AVANT" not in t]
    for titre in (
        "DECISIONS DES ACTIONNAIRES",
        "RESULTATS SOCIAUX",
        "TRANSFORMATION DE LA SOCIETE",
        "CONTESTATIONS",
        "CONSTITUTION DE LA SOCIETE",
    ):
        assert not [t for t in hors_annexe if titre in t], f"bandeau « {titre} » encore encadre"
    # Le cadre « STATUTS » (titre) et le cadre de l'annexe restent presents.
    assert any(t.strip() == "STATUTS" for t in tables)
    assert any("ETAT DES ENGAGEMENTS PRIS AVANT" in t for t in tables)


@pytest.mark.parametrize("operation", ["cession", "apport"])
def test_statuts_spfpl_art10_sans_tiret_et_listes_pucees(
    operation: str, tmp_path: Path
) -> None:
    """KAN-3 (Albane 2026-07-13), gate adversarial (Akainu B1/M1/M2) :
    - art 10 : le 1er alinea (« Le capital social peut etre augmente… », numId
      upperRoman dans le modele, pas une puce) ne doit PAS porter de tiret solo ;
    - les vraies listes du modele sont pucees, y compris le 1er item des decisions
      collectives de l'art. 23 (« Approbation des comptes annuels… », fusion intro+item
      dans le template apport reparee) et l'engagement de l'annexe (cession comme apport)."""
    ctx = _with_exercice(_base_context(operation=operation))
    generator = (
        StatutsSpfplCessionGenerator()
        if operation == "cession"
        else StatutsSpfplApportGenerator()
    )
    paragraphs = Document(generator.generate(ctx, tmp_path)).paragraphs
    textes = [p.text for p in paragraphs]

    idx_art10 = next(i for i, t in enumerate(textes) if t.strip().upper().startswith("ARTICLE 10"))
    premier_alinea = textes[idx_art10 + 1].strip()
    assert premier_alinea.startswith("Le capital social peut être augmenté")
    assert not premier_alinea.startswith("-"), "art 10 : tiret solo interdit (Albane point 1)"

    approbation = next(t for t in textes if "Approbation des comptes annuels" in t)
    assert approbation.strip().startswith("- "), "art 23 : 1er item des decisions doit etre puce"

    engagement = next(
        t
        for t in reversed(textes)
        if t.strip() and "Bon pour acceptation" not in t
    )
    assert engagement.strip().startswith("- "), "annexe : engagement doit etre puce"

    # KAN-3 / gate Akainu M1 (2026-07-16) : les 11 decisions collectives de l'art. 23 doivent etre
    # 11 puces DISTINCTES sur cession ET apport. L'apport fusionnait 11 items en 7 puces (« il
    # manque des puces », point 4 du ticket, corrige sur la cession mais silote sur l'apport).
    # Cette assertion garde la parite mecaniquement (le siloing passait la CI sans elle, nitpick n1).
    idx_dec = next(i for i, t in enumerate(textes) if "décisions suivantes" in t)
    idx_fin = next(i for i, t in enumerate(textes) if "Toutes les autres décisions" in t)
    puces_art23 = [t for t in textes[idx_dec + 1 : idx_fin] if t.strip().startswith("- ")]
    assert len(puces_art23) == 11, f"art 23 : 11 decisions attendues, {len(puces_art23)} trouvees"
    assert puces_art23[-1].strip().endswith("."), "art 23 : derniere decision termine par un point"


def test_statuts_spfpl_apport_simplifiee_accentuee(tmp_path: Path) -> None:
    """Fix 6 / R4 (Albane 2026-07-07) — « simplifiée(s) » ACCENTUE dans les statuts apport
    (« par actions simplifiée régie », « …libérales par actions simplifiées »). L'orthographe
    irreprochable prime sur la typo « simplifiee » du verbatim source/front."""
    ctx = _with_exercice(_base_context(operation="apport"))
    text = _docx_text(StatutsSpfplApportGenerator().generate(ctx, tmp_path))
    assert "par actions simplifiée régie" in text
    assert "par actions simplifiées »" in text
    assert "simplifiee" not in text  # typo non accentuee proscrite (R4)
    assert "simplifiees" not in text
