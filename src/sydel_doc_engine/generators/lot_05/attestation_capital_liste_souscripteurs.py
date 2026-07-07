from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import CapitalSouscripteur, DocumentGenerationContext
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.generators.lot_05.spfpl_common import (
    company_siege_display,
    elision_de,
    person_short_identity,
    required_apport_titres,
    required_apporteur,
    required_capital_souscription,
    required_int,
    required_societe_cible,
    required_societe_spfpl,
    required_text,
    validate_apport_context,
)
from sydel_doc_engine.rendering.docx_builder import add_paragraph, add_spacer, new_document

OUTPUT_FILENAME = "attestation_capital_liste_souscripteurs.docx"

# Mise en forme (Albane, retour « mise en forme » 2026-07) : « ajouter des espaces »
# sur l'attestation capital / liste des souscripteurs. Deux aerations demandees :
# (a) espace APRES la phrase d'apport (« ... a fait un apport de ... euros ») et
#     APRES la ligne « Total des apports » ;
# (b) espace entre le TITRE (denomination), la DESIGNATION de la societe (forme /
#     activite / siege) et le CORPS du texte.
# On aere via des paragraphes-espaceurs (add_spacer) entre les GROUPES et via un
# space_after renforce sur les lignes visees, sans toucher au wording.
_ATTESTATION_GROUP_SPACER_PT = 10


class AttestationCapitalListeSouscripteursGenerator:
    """Generateur from-scratch de l'attestation capital SPFPL V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_apport_context(ctx)
        societe_spfpl = required_societe_spfpl(ctx)
        societe_cible = required_societe_cible(ctx)
        apporteur = required_apporteur(ctx)
        apport_titres = required_apport_titres(ctx)
        capital = required_capital_souscription(ctx)
        souscripteur = _unique_souscripteur(capital.souscripteurs)
        president = capital.president or souscripteur
        spfpl_name = required_text(societe_spfpl.denomination, "societe_spfpl.denomination")
        spfpl_capital = required_text(societe_spfpl.capital_social, "societe_spfpl.capital_social")
        souscripteur_prenom = required_text(souscripteur.prenom, _souscripteur_field("prenom"))
        souscripteur_nom = required_text(souscripteur.nom, _souscripteur_field("nom"))
        apport_nature = required_text(
            capital.apports_nature_montant,
            "capital_souscription.apports_nature_montant",
        )
        apports_numeraire = required_text(
            capital.apports_numeraire_montant,
            "capital_souscription.apports_numeraire_montant",
        )

        docx = new_document()
        add_paragraph(
            docx,
            spfpl_name,
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
        )
        add_paragraph(
            docx,
            f"Société par actions simplifiée au capital de {spfpl_capital} euros",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
        )
        add_paragraph(
            docx,
            "Société de Participations Financières de Profession Libérale de "
            f"{required_text(societe_spfpl.profession, 'societe_spfpl.profession')}",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
        )
        add_paragraph(
            docx,
            f"Siège social : {company_siege_display(societe_spfpl, 'societe_spfpl')}",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
        )
        # (b) Aeration entre la DESIGNATION de la societe (denomination / forme /
        # activite / siege) et le titre « ATTESTATION » + le corps.
        add_spacer(docx, space_after_pt=_ATTESTATION_GROUP_SPACER_PT)
        add_paragraph(docx, "ATTESTATION", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
        add_paragraph(
            docx,
            "Liste des souscripteurs",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
        )
        # (b) Aeration entre le bloc TITRE (« ATTESTATION » / « Liste des
        # souscripteurs ») et le CORPS du texte.
        add_spacer(docx, space_after_pt=_ATTESTATION_GROUP_SPACER_PT)
        # R3 (Albane 2026-07-07) : « Docteur » n'est pas une civilité — les slots de
        # civilité (tête de désignation, « par le Président, __ », signature) rendent
        # la civilité CIVILE (Monsieur/Madame, genre du signataire) ; le TITRE
        # « Le Docteur X » de la phrase d'apport reste, lui, légitime (A26-45/49).
        president_identite = _souscripteur_identite(
            president,
            "capital_souscription.president",
            genre=ctx.personne_signataire.genre,
        )
        add_paragraph(
            docx,
            f"{president_identite}, "
            f"demeurant {_adresse(president, 'capital_souscription.president')}, "
            f"atteste que le capital de la société {spfpl_name} "
            "est réparti de la manière suivante :",
        )
        add_paragraph(docx, f"Capital social : {spfpl_capital} euros")
        add_paragraph(
            docx,
            "Nombre d'actions : "
            f"{required_int(capital.nb_actions_total, 'capital_souscription.nb_actions_total')} "
            f"actions d'un montant {elision_de(str(_valeur_nominale_action(capital)))} "
            "euros chacune",
        )
        add_paragraph(
            docx,
            "Répartition : "
            f"{required_int(souscripteur.nb_actions, _souscripteur_field('nb_actions'))} "
            f"actions attribuées au Dr {souscripteur_prenom} {souscripteur_nom}, "
            "actionnaire unique",
        )
        add_paragraph(docx, "Apports en nature :", bold=True)
        add_paragraph(
            docx,
            f"{person_short_identity(apporteur, 'apporteur')} fait apport de "
            f"{required_int(apport_titres.nb_parts, 'apport_titres.nb_parts')} parts de la "
            f"{required_text(societe_cible.forme_sociale, 'societe_cible.forme_sociale')} "
            f"dénommée {required_text(societe_cible.denomination, 'societe_cible.denomination')} "
            f"ayant son siège {company_siege_display(societe_cible, 'societe_cible')}, "
            "immatriculée au RCS de "
            f"{required_text(societe_cible.ville_rcs, 'societe_cible.ville_rcs')} "
            f"sous le numéro {required_text(societe_cible.numero_rcs, 'societe_cible.numero_rcs')} "
            f"pour une valeur de {apport_nature} euros.",
            # (a) Espace APRES la phrase d'apport (« ... fait apport de ... pour une
            # valeur de ... euros. »).
            space_after_pt=_ATTESTATION_GROUP_SPACER_PT,
        )
        add_paragraph(
            docx,
            f"Total des apports en nature {apport_nature} euros",
            # (a) Espace APRES la ligne « Total des apports ».
            space_after_pt=_ATTESTATION_GROUP_SPACER_PT,
        )
        add_paragraph(docx, f"Apports en numéraire : {apports_numeraire}")
        add_paragraph(
            docx,
            "Le "
            f"{_souscripteur_nom(souscripteur)} a fait la totalité des apports en nature.",
        )
        add_paragraph(
            docx,
            f"Le présent état qui constate la souscription d'actions de la société {spfpl_name}, "
            "ainsi que l'apport de la somme de "
            f"{apport_nature} euros correspondant à la totalité du nominal desdites actions, est "
            "certifié exact, sincère et véritable par le Président, "
            f"{president_identite}.",
        )
        add_paragraph(docx, f"Fait à {ctx.signature.lieu}")
        add_paragraph(docx, f"Le {ctx.signature.date.strftime('%d/%m/%Y')}")
        add_paragraph(docx, president_identite)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        docx.save(output_path)
        return output_path


def _unique_souscripteur(souscripteurs: list[CapitalSouscripteur]) -> CapitalSouscripteur:
    if len(souscripteurs) != 1:
        raise ValueError(
            "capital_souscription.souscripteurs doit contenir exactement un "
            "souscripteur pour CODE-SPFPL-CORE-001."
        )
    return souscripteurs[0]


def _souscripteur_identite(
    souscripteur: CapitalSouscripteur,
    field_name: str,
    *,
    genre: Gender | None,
) -> str:
    # R3 (Albane 2026-07-07) : identité de SLOT de civilité — un titre professionnel
    # (« Docteur »/« Dr ») posé en civilite_affichage est substitué par la civilité
    # CIVILE accordée au genre ; une civilité déjà civile passe inchangée.
    civilite = civilite_civile(
        required_text(souscripteur.civilite_affichage, f"{field_name}.civilite_affichage"),
        genre,
    )
    return (
        f"{civilite} "
        f"{required_text(souscripteur.prenom, f'{field_name}.prenom')} "
        f"{required_text(souscripteur.nom, f'{field_name}.nom')} "
        f"{required_text(souscripteur.profession, f'{field_name}.profession')}"
    )


def _souscripteur_nom(souscripteur: CapitalSouscripteur) -> str:
    # Slot TITRE (« Le Docteur X a fait la totalité des apports », convention A26-45/49) :
    # toujours le titre professionnel « Docteur » (les souscripteurs SPFPL sont des
    # praticiens), JAMAIS la civilité civile posée par le front (SP2 : M./Mme) — sinon
    # « Le Monsieur X » (défaut pré-existant, rapport conformité 2026-07-07 l.182).
    return (
        "Docteur "
        f"{required_text(souscripteur.prenom, _souscripteur_field('prenom'))} "
        f"{required_text(souscripteur.nom, _souscripteur_field('nom'))}"
    )


def _adresse(souscripteur: CapitalSouscripteur, field_name: str) -> str:
    return required_text(
        souscripteur.adresse_personnelle_affichee,
        f"{field_name}.adresse_personnelle_affichee",
    )


def _souscripteur_field(field_name: str) -> str:
    return f"capital_souscription.souscripteurs[0].{field_name}"


def _valeur_nominale_action(capital) -> str:
    return required_text(
        capital.valeur_nominale_action,
        "capital_souscription.valeur_nominale_action",
    )
