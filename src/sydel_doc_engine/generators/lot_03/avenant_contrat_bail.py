from __future__ import annotations

from datetime import datetime
from pathlib import Path

from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from sydel_doc_engine.domain.models import (
    BailContext,
    BailParty,
    Company,
    DocumentGenerationContext,
)
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.generators.lot_03.bail_appel_common import (
    DOCUMENT_CODE,
    format_display_date,
    required_text,
    validate_avenant_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    BAIL_COMPACT_STYLE_PROFILE,
    add_article_heading,
    add_framed_title,
    add_paragraph,
    add_party_marker,
    add_signature_table,
    add_spacer,
    keep_signature_block_together,
    new_document,
)
from sydel_doc_engine.utils.grammar import accord_terme_genre
from sydel_doc_engine.utils.months import FRENCH_MONTHS

OUTPUT_FILENAME = "avenant_contrat_bail.docx"


class AvenantContratBailGenerator:
    """Generateur from-scratch de l'avenant au contrat de bail."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_avenant_context(ctx)
        bail = _required_bail(ctx.bail)
        company = _required_company(ctx.societe)
        bailleur = _required_party(bail.bailleur, "bail.bailleur")
        locataire = _required_party(bail.locataire, "bail.locataire")

        if not bail.societe_en_cours_immatriculation:
            raise ValueError(
                "bail.societe_en_cours_immatriculation doit etre confirme pour "
                f"{DOCUMENT_CODE}."
            )
        if not bail.bailleur_accepte_changement_locataire:
            raise ValueError(
                "bail.bailleur_accepte_changement_locataire doit etre confirme pour "
                f"{DOCUMENT_CODE}."
            )

        docx = new_document(style_profile=BAIL_COMPACT_STYLE_PROFILE)
        # Retour Albane 2026-06-17 (ticket lot 2, §10.1) : la date de l'encadre doit
        # etre celle du bail d'origine (meme variable que l'article 1), pas la date
        # de signature de l'avenant. Tolere le vide comme l'article 1 (date d'origine
        # facultative) : pas de date fabriquee, pas de « du » orphelin.
        date_bail_origine = _display_date_or_empty(bail.date_signature_origine)
        titre_avenant = (
            f"Avenant n°1 au bail du {date_bail_origine}"
            if date_bail_origine
            else "Avenant n°1 au bail"
        )
        add_framed_title(
            docx,
            [titre_avenant],
            style_profile=BAIL_COMPACT_STYLE_PROFILE,
        )
        _add_parties(docx, bailleur, locataire)
        # AV4 (Albane 2026-06-26) : « ajouter un espace entre chaque article » ->
        # un espace dedie entre l'article 1, 2 et 3.
        _add_article_1(docx, bail, locataire, company)
        add_spacer(docx, space_after_pt=BAIL_COMPACT_STYLE_PROFILE.standard_space_after_pt)
        _add_article_2(docx, locataire)
        add_spacer(docx, space_after_pt=BAIL_COMPACT_STYLE_PROFILE.standard_space_after_pt)
        _add_article_3(docx)
        # AV5 (Albane 2026-06-26) : « on peut retirer "en quatre exemplaires" » ->
        # plus de mention du nombre d'exemplaires dans l'avenant.
        add_paragraph(
            docx,
            (
                f"Fait à {required_text(ctx.signature.lieu, 'signature.lieu')}, le "
                f"{format_display_date(ctx.signature.date, 'signature.date')}"
            ),
        )
        signature_table = _add_signature_table(docx)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        # KAN-36 : « Fait à … » + cases de signature (table) sur une seule page (helper table :
        # keepNext sur l'intro + cantSplit sur les cases).
        keep_signature_block_together(docx, signature_table)
        docx.save(output_path)
        return output_path


def _required_bail(bail: BailContext | None) -> BailContext:
    if bail is None:
        raise ValueError(f"bail est obligatoire pour {DOCUMENT_CODE}.")
    return bail


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def _required_party(party: BailParty | None, field_name: str) -> BailParty:
    # Retours client 2026-06-11 (ticket 3.1) : l'identite du LOCATAIRE est
    # toujours derivee de l'associe unique (nom requis) ; les champs du BAILLEUR
    # non renseignes sont omis de la ligne de partie au lieu de bloquer.
    if party is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if field_name == "bail.locataire":
        required_text(party.nom, f"{field_name}.nom")
    return party


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _coerce_date(value):
    """Rafael 2026-07-09 : les champs date de l'avenant arrivent parfois en CHAINE ISO
    (« 1975-03-10 ») -> l'ancien fallback `str(value)` sortait l'ISO brut au lieu du format
    francais du reste du moteur. On parse ISO (YYYY-MM-DD) et JJ/MM/AAAA en objet date."""
    if value is None:
        return None
    if hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day"):
        return value
    raw = str(value).strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def _display_date_or_empty(value) -> str:
    parsed = _coerce_date(value)
    if parsed is not None:
        return parsed.strftime("%d/%m/%Y")
    return "" if value is None else str(value).strip()


def _display_birthdate(value) -> str:
    # AV2 (Albane 2026-06-26) : « que le chiffre ne soit pas 1 janvier mais 01 janvier »
    # -> date de naissance en « JJ mois AAAA » avec jour sur 2 chiffres et mois accentue
    # en toutes lettres (meme presentation que cession_cabinets_common §A26-33/A26-69).
    # Rafael 2026-07-09 : parse une chaine ISO/numerique avant formatage (plus de « 1975-03-10 »).
    parsed = _coerce_date(value)
    if parsed is not None:
        return f"{parsed.day:02d} {FRENCH_MONTHS[parsed.month]} {parsed.year}"
    return "" if value is None else str(value).strip()


def _locataire_nom_avec_titre(locataire: BailParty, article: str = "") -> str:
    # R3 « supprimer PARTOUT » (Rafael 2026-07-09) : « le Docteur … » n'existe plus. La civilite
    # d'un locataire personne physique est CIVILE (Monsieur/Madame accorde au genre) et ne prend
    # JAMAIS d'article (« Monsieur X », pas « le Monsieur X »). On resout donc le titre par
    # `civilite_civile` (le titre court « Docteur »/« Dr » -> Monsieur/Madame ; une civilite deja
    # civile est renvoyee inchangee) et on IGNORE le parametre `article` — SUPERSEDE AV3 (l'article
    # « le/Le » ne se posait que devant un titre professionnel, qui n'apparait plus).
    titre_source = _clean(locataire.civilite_courte) or _clean(locataire.civilite_affichage)
    titre = civilite_civile(titre_source, locataire.genre) if titre_source else ""
    parts = [titre, _clean(locataire.prenom), _clean(locataire.nom)]
    return " ".join(part for part in parts if part)


def _party_other_segments(party: BailParty) -> list[str]:
    # Segments d'identite HORS nom : composes uniquement a partir des informations
    # saisies : aucun « ne le , a » incomplet quand un element du bailleur manque.
    segments: list[str] = []
    if _clean(party.profession):
        segments.append(_clean(party.profession))
    naissance = _display_birthdate(party.date_naissance)
    # M1 (Akainu SELARL ronde 4, 2026-07-12) : « né le / né à » s'accorde au genre de la partie
    # (locataire OU bailleur) -> « née » pour une femme (parite avec les actes de cession). No-op
    # au masculin. Theme transversal ACCORD EN GENRE, propage a l'avenant (regle 68 « partout »).
    ne = accord_terme_genre("né", party.genre)
    if naissance:
        ville = _clean(party.ville_naissance)
        segments.append(f"{ne} le {naissance}" + (f", à {ville}" if ville else ""))
    elif _clean(party.ville_naissance):
        segments.append(f"{ne} à {_clean(party.ville_naissance)}")
    if _clean(party.nationalite):
        segments.append(f"de nationalité {_clean(party.nationalite)}")
    if _clean(party.adresse_affichee):
        segments.append(f"demeurant au {_clean(party.adresse_affichee)}")
    return segments


def _party_full_runs(party: BailParty, field_name: str) -> list[tuple[str, bool]]:
    # AV1 (Albane 2026-06-26) : « l'identite du Locataire devrait etre en non gras
    # (sauf son nom), peut-etre pareil pour le bailleur » -> seul le NOM (prenom + nom)
    # reste en gras ; la civilite et tout le reste de l'identite passent en non gras.
    # Applique au LOCATAIRE comme au BAILLEUR.
    # R3 « supprimer PARTOUT » (Rafael 2026-07-09) : la civilite de tete d'identite est CIVILE
    # (« Docteur X » -> « Monsieur/Madame X », accorde au genre), jamais un titre professionnel.
    civilite_source = _clean(party.civilite_affichage)
    civilite = civilite_civile(civilite_source, party.genre) if civilite_source else ""
    nom_complet = " ".join(
        part for part in (_clean(party.prenom), _clean(party.nom)) if part
    )
    rest = _party_other_segments(party)

    runs: list[tuple[str, bool]] = []
    has_head = bool(civilite or nom_complet)
    if civilite:
        runs.append((f"{civilite} " if nom_complet else civilite, False))
    if nom_complet:
        runs.append((nom_complet, True))  # NOM en gras
    # Le reste de l'identite (non gras) ; virgule de separation seulement si une tete existe.
    if rest:
        joined = ", ".join(rest)
        prefix = ", " if has_head else ""
        runs.append((f"{prefix}{joined},", False))
    elif has_head:
        runs.append((",", False))
    return runs


def _add_article_1(
    docx,
    bail: BailContext,
    locataire: BailParty,
    company: Company,
) -> None:
    _add_article_title(docx, "ARTICLE 1 : changement de locataire")
    date_origine = _display_date_or_empty(bail.date_signature_origine)
    date_segment = f" en date du {date_origine}" if date_origine else ""
    profession = _clean(locataire.profession)
    profession_segment = f", ({profession})" if profession else ""
    # AV3 (Albane 2026-06-26) : « devant Docteur, mettre "le docteur" » -> article
    # « le » devant l'identite du locataire a l'article 1 (milieu de phrase -> minuscule).
    add_paragraph(
        docx,
        (
            f"Le bail signé{date_segment}, "
            f"a pour locataire {_locataire_nom_avec_titre(locataire, article='le')}"
            f"{profession_segment}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    siege = company.siege
    adresse_siege = required_text(
        siege.adresse_affichee if siege else None,
        "societe.siege.adresse_affichee",
    )
    add_paragraph(
        docx,
        (
            "Le présent avenant donne bail à la société "
            f"{required_text(company.denomination, 'societe.denomination')} en cours "
            # Retour Albane 2026-06-17 (ticket lot 2, §10.3) : « de » manquant apres RCS.
            "d’immatriculation au RCS de "
            f"{required_text(company.ville_rcs, 'societe.rcs_ville')}, domiciliée au "
            f"{adresse_siege}."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_article_2(docx, locataire: BailParty) -> None:
    _add_article_title(docx, "ARTICLE 2 : Responsabilité pour une société en cours de formation")
    # M1 (Akainu 2026-06-26) : meme regle d'article que l'art1 — « Le Docteur … » devant un
    # titre professionnel, « Monsieur … » (sans article) sinon. required_text garde la garde
    # sur le nom obligatoire.
    required_text(locataire.nom, "bail.locataire.nom")
    domicile = _clean(locataire.adresse_affichee)
    # M1 (Akainu ronde 4) : « domicilié » accorde au genre du locataire (« domiciliée »).
    domicilie = accord_terme_genre("domicilié", locataire.genre)
    domicile_segment = f", {domicilie} {domicile}" if domicile else ""
    add_paragraph(
        docx,
        (
            f"{_locataire_nom_avec_titre(locataire, article='Le')}"
            f"{domicile_segment}, "
            "engage sa responsabilité pour tous les actes passés au nom de la société jusqu’à "
            "l’immatriculation au RCS."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )
    # AV3 (Albane 2026-06-26) : « pareil a l'art 2 sur la seconde phrase » -> article
    # « Le » devant l'identite (debut de phrase -> majuscule), comme la 1re phrase.
    locataire_label = _locataire_nom_avec_titre(locataire, article="Le")
    add_paragraph(
        docx,
        (
            f"{locataire_label} s’engage à fournir au Bailleur un "
            "extrait KBIS une fois que les démarches seront finies."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_article_3(docx) -> None:
    _add_article_title(docx, "ARTICLE 3 : Clauses du bail")
    add_paragraph(
        docx,
        "Le présent avenant ne modifie pas les clauses du bail en cours.",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )


def _add_party_line(docx, party: BailParty, field_name: str) -> None:
    # AV1 : paragraphe d'identite en runs multiples (nom gras, reste non gras).
    # On reproduit les reglages de style d'add_paragraph (space_before/after du
    # profil compact, JUSTIFY) sans modifier docx_builder.
    paragraph = docx.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(
        BAIL_COMPACT_STYLE_PROFILE.standard_space_after_pt
    )
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for text, bold in _party_full_runs(party, field_name):
        run = paragraph.add_run(text)
        run.bold = bold


def _add_parties(docx, bailleur: BailParty, locataire: BailParty) -> None:
    add_paragraph(docx, "Entre les soussign\u00e9s :", style_profile=BAIL_COMPACT_STYLE_PROFILE)
    _add_party_line(docx, bailleur, "bail.bailleur")
    # M1 (Akainu ronde 4) : le participe "designe" accorde au genre de la partie
    # ("designee" pour une femme). Le LABEL "le Bailleur"/"le Locataire" reste (juridique, [n4]).
    designe_bailleur = accord_terme_genre("d\u00e9sign\u00e9", bailleur.genre)
    designe_locataire = accord_terme_genre("d\u00e9sign\u00e9", locataire.genre)
    add_party_marker(
        docx,
        f"Ci-apr\u00e8s {designe_bailleur} \u00ab le Bailleur \u00bb",
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    add_paragraph(docx, "ET :", bold=True, style_profile=BAIL_COMPACT_STYLE_PROFILE)
    _add_party_line(docx, locataire, "bail.locataire")
    add_party_marker(
        docx,
        f"Ci-apr\u00e8s {designe_locataire} \u00ab le Locataire \u00bb",
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    add_paragraph(
        docx,
        "Les parties conviennent de ce qui suit :",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )


def _add_article_title(docx, title: str) -> None:
    add_article_heading(docx, title, style_profile=BAIL_COMPACT_STYLE_PROFILE)


def _add_signature_table(docx):
    table = add_signature_table(
        docx,
        [
            ["Le Bailleur", "L\u2019ancien locataire", "Le nouveau locataire"],
        ],
        style_profile=BAIL_COMPACT_STYLE_PROFILE,
    )
    # Mise en forme (Albane 2026-06-17, \u00a710.4) : agrandir les cases de
    # signature (compatible signature electronique YouSign) en imposant une
    # hauteur minimale de ligne. ADDITIF : on garde le tableau borde, on ne
    # retire aucune bordure.
    for row in table.rows:
        row.height = Cm(2.6)
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    return table
