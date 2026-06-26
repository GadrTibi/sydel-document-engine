from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

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
# « ... a completer » SANS surlignage (R22b-01) quand la saisie ne fournit pas la valeur.
DESTINATAIRE_FIXED_LINE = "Service départemental de l'enregistrement de"
# Espace blanc au-dessus du bloc destinataire pour le faire tomber dans la
# fenetre d'enveloppe (haut). Calibre sur le top margin du modele client (~3 cm).
ENVELOPE_WINDOW_SPACER_PT = 28
# Albane 2026-06-26 §C1 : les 5 premieres lignes (en-tete destinataire) demarrent « vers le
# cm 12 de la regle » -> retrait gauche de 12 cm (texte aligne a gauche mais decale a droite).
ENTETE_LEFT_INDENT_CM = 12.0
# §C3 : espace avant le bloc lieu/date + objet pour les faire commencer plus bas.
OBJET_SPACER_PT = 24

# Montant FIXE des droits d'enregistrement (§8.3), texte noir standard (R22b-01 :
# plus de rouge). PAS une variable.
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
        # Albane 2026-06-26 §C1 : les 5 premieres lignes (en-tete destinataire) sont alignees a
        # GAUCHE mais demarrent vers le cm 12 de la regle -> retrait gauche de 12 cm.
        add_spacer(document, space_after_pt=ENVELOPE_WINDOW_SPACER_PT)
        fixed_para = add_paragraph(
            document, DESTINATAIRE_FIXED_LINE, alignment=WD_ALIGN_PARAGRAPH.LEFT
        )
        fixed_para.paragraph_format.left_indent = Cm(ENTETE_LEFT_INDENT_CM)
        for value, placeholder in (
            (enregistrement.service, "Nom du service"),
            (enregistrement.centre_finances_publiques, "Centre des finances publiques"),
            (enregistrement.adresse_service, "Adresse"),
            (enregistrement.cp_ville_service, "Code postal et ville"),
        ):
            _add_fillable_destinataire_line(
                document, value, placeholder, left_indent_cm=ENTETE_LEFT_INDENT_CM
            )

        # §C3 — espace avant l'objet / le corps pour les faire commencer plus bas.
        add_spacer(document, space_after_pt=OBJET_SPACER_PT)
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
            space_before_pt=OBJET_SPACER_PT,
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


def _add_fillable_destinataire_line(
    document, value, placeholder: str, *, left_indent_cm: float = 0.0
) -> None:
    """Ligne du bloc destinataire : saisie reelle si fournie, sinon champ a completer.

    Quand la valeur n'est pas saisie (cas SELARL), on rend un libelle de champ
    « [Nom du service] a completer » SANS surlignage (R22b-01), sans token moteur ni
    placeholder source « [ ] » (qui ferait planter save_clean_document).

    Albane 2026-06-26 §C1 : `left_indent_cm` decale la ligne vers le cm 12 de la regle
    (en-tete destinataire aligne a gauche mais demarrant a droite).
    """
    text = value.strip() if isinstance(value, str) else (value or None)
    if text:
        paragraph = add_paragraph(document, str(text), alignment=WD_ALIGN_PARAGRAPH.LEFT)
        paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
        return
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
    # R22b-01 (Rafael 2026-06-22) : aucun surlignage/couleur sur le texte.
    paragraph.add_run(f"{placeholder} à compléter")


def _add_corps_exemplaires(document, exemplaires: str, denomination: str) -> None:
    # Albane 2026-06-26 §C2 : eviter le doublon « SCM SCM CABINET CENTRAL » (la forme « SCM »
    # est deja portee par la denomination). On ecrit « de la Société {denomination} ».
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.add_run(
        "Je vous prie de bien vouloir trouver sous ce pli "
        f"{exemplaires} exemplaires de l'acte de cession de parts de la Société "
    )
    paragraph.add_run(denomination)
    paragraph.add_run(" pour les enregistrer.")


def _add_corps_droits(document) -> None:
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.add_run("Vous trouverez également un chèque de ")
    # R22b-01 : montant des droits sans couleur rouge (texte noir standard).
    paragraph.add_run(f"{MONTANT_DROITS_FIXE} ")
    paragraph.add_run("euros correspondants aux droits d'enregistrements.")
