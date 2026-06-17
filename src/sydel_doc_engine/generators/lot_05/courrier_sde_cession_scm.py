from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import RGBColor

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    add_body_paragraph,
    format_display_date,
    required_text,
    save_clean_document,
    validate_courrier_sde_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    add_header_logo,
    add_letter_place_date,
    add_paragraph,
    add_spacer,
    add_sydel_letter_footer,
    new_document,
)

OUTPUT_FILENAME = "courrier_sde_cession_scm.docx"

# Ligne FIXE du bloc destinataire (modele client + §8.1). Le reste (nom du
# service, adresse, CP/ville) est a completer manuellement -> rendu en champs
# surlignes jaune quand la saisie ne fournit pas la valeur.
DESTINATAIRE_FIXED_LINE = "Service départemental de l'enregistrement de"
# Espace blanc au-dessus du bloc destinataire pour le faire tomber dans la
# fenetre d'enveloppe (haut). Calibre sur le top margin du modele client (~3 cm).
ENVELOPE_WINDOW_SPACER_PT = 28

# Montant FIXE des droits d'enregistrement (§8.3), rendu en rouge pour
# adaptation manuelle eventuelle. PAS une variable.
MONTANT_DROITS_FIXE = "25"
# Signataire FIXE SYDEL (§8.4a) : PAS le client, PAS une variable libre.
SIGNATAIRE_SDE_FIXE = "Clémence ROUSSEL"


class CourrierSdeCessionScmGenerator:
    """Generateur from-scratch du courrier SDE cession SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        scm_cession = validate_courrier_sde_context(ctx)
        scm_cedee = scm_cession.scm_cedee
        if scm_cedee is None:
            raise ValueError("scm_cession.scm_cedee est obligatoire pour le courrier SDE.")
        denomination = required_text(
            scm_cedee.denomination, "scm_cession.scm_cedee.denomination"
        )
        enregistrement = scm_cession.enregistrement
        if enregistrement is None:
            raise ValueError("scm_cession.enregistrement est obligatoire.")

        document = new_document()
        # Logo SYDEL en header, aligne a GAUCHE (retour UAT Rafael DOC-032).
        add_header_logo(document, alignment=WD_ALIGN_PARAGRAPH.LEFT)

        # §8.1 — Bloc destinataire SDE pour TOUTES structures, descendu dans la
        # fenetre d'enveloppe. 1re ligne FIXE, reste a completer (jaune).
        add_spacer(document, space_after_pt=ENVELOPE_WINDOW_SPACER_PT)
        add_paragraph(document, DESTINATAIRE_FIXED_LINE, alignment=WD_ALIGN_PARAGRAPH.LEFT)
        for value, placeholder in (
            (enregistrement.service, "Nom du service"),
            (enregistrement.centre_finances_publiques, "Centre des finances publiques"),
            (enregistrement.adresse_service, "Adresse"),
            (enregistrement.cp_ville_service, "Code postal et ville"),
        ):
            _add_fillable_destinataire_line(document, value, placeholder)

        add_letter_place_date(
            document,
            f"{ctx.signature.lieu}, le {format_display_date(ctx.signature.date, 'signature.date')}",
        )
        # Objet en gras + souligne (retour UAT Rafael DOC-032).
        add_paragraph(
            document,
            "Objet : Enregistrement actes de cession des parts de la société SCM",
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            bold=True,
            underline=True,
        )
        add_body_paragraph(document, "Madame, Monsieur,")
        # §8.2 — nom de la SCM via variable dans le corps (modele client).
        # Le nom est surligne jaune pour signaler le champ a verifier (modele).
        exemplaires = "4"
        _add_corps_exemplaires(document, exemplaires, denomination)
        # §8.3 — droits d'enregistrement : montant FIXE « 25 » en rouge.
        _add_corps_droits(document)
        add_body_paragraph(
            document,
            (
                "Merci de bien vouloir me retourner les originaux chez Sydel. "
                "A cet effet, vous trouverez une enveloppe de retour timbrée."
            ),
        )
        add_body_paragraph(
            document,
            "Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.",
        )
        # §8.4a — Signataire FIXE SYDEL, aligne a DROITE.
        add_paragraph(
            document,
            SIGNATAIRE_SDE_FIXE,
            alignment=WD_ALIGN_PARAGRAPH.RIGHT,
        )
        # §8.4b — pied de page SYDEL (coordonnees) pour contact par le SDE.
        add_sydel_letter_footer(document)
        return save_clean_document(document, output_dir, OUTPUT_FILENAME)


def _add_fillable_destinataire_line(document, value, placeholder: str) -> None:
    """Ligne du bloc destinataire : saisie reelle si fournie, sinon champ jaune.

    Quand la valeur n'est pas saisie (cas SELARL), on rend un libelle de champ
    surligne jaune (« [Nom du service] ») a completer manuellement, sans token
    moteur ni placeholder source « [ ] » (qui ferait planter save_clean_document).
    """
    text = value.strip() if isinstance(value, str) else (value or None)
    if text:
        add_paragraph(document, str(text), alignment=WD_ALIGN_PARAGRAPH.LEFT)
        return
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = paragraph.add_run(f"{placeholder} à compléter")
    run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def _add_corps_exemplaires(document, exemplaires: str, denomination: str) -> None:
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.add_run(
        "Je vous prie de bien vouloir trouver sous ce pli "
        f"{exemplaires} exemplaires de l'acte de cession de parts de la SCM "
    )
    name_run = paragraph.add_run(denomination)
    name_run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    paragraph.add_run(" pour les enregistrer.")


def _add_corps_droits(document) -> None:
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.add_run("Vous trouverez également un chèque de ")
    montant_run = paragraph.add_run(f"{MONTANT_DROITS_FIXE} ")
    montant_run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    paragraph.add_run("euros correspondants aux droits d'enregistrements.")
