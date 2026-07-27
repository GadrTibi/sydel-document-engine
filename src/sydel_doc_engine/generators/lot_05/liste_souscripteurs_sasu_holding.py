"""Generateur DOC-050 — Liste des souscripteurs SASU Holding (modele Albane 2026-06-29).

Satellite GENERALISTE de la SASU Holding (SAS unipersonnelle, holding patrimoniale), DISTINCT
de l'attestation capital / liste des souscripteurs SAS SPFPL medecins (DOC-024, verrouille SPFPL
medecins, apports en NATURE de parts, profession=medecin). Le modele Albane SASU Holding est
beaucoup plus simple : un « Etat des souscriptions » avec un tableau (souscripteur unique = le
president) et une ligne TOTAL, sans apport en nature, sans profession, sans SPFPL.

Self-contained : lit l'identite de l'associe unique depuis `ctx.personne_signataire`, la societe
(denomination, capital, nb_actions) depuis `ctx.societe` / `ctx.statuts_sasu_holding`, la
signature depuis `ctx.signature`. Genre libre (holding generaliste).

Fidelite : rendu byte-fidele au modele officiel Albane
`docs/review/albane_sas_2026-06-29/Liste_des_souscripteurs.docx`.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Company,
    DocumentGenerationContext,
    Person,
    StatutsSasuHoldingContext,
)
from sydel_doc_engine.front_app.field_derivations import group_montant
from sydel_doc_engine.generators.lot_05.spfpl_libelles import libelle_metier
from sydel_doc_engine.rendering.docx_builder import (
    add_bordered_data_table,
    add_paragraph,
    keep_final_signature_block_together,
    new_document,
)
from sydel_doc_engine.utils.grammar import montant_avec_euros

DOCUMENT_CODE = "DOC-050"
OUTPUT_FILENAME = "liste_souscripteurs_sasu_holding.docx"
# Forme courte verbatim du modele Albane (« Etat des souscriptions / De la SAS <denom> »).
FORME_COURTE = "SAS"
# Apostrophe typographique (U+2019) : en-tete « Nombre d'actions souscrites » du modele Albane
# (byte-fidelite — le modele emploie la courbe, pas la droite).
_APOS = chr(0x2019)


class ListeSouscripteursSasuHoldingGenerator:
    """Generateur from-scratch de la liste des souscripteurs SASU Holding (generaliste)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        data = _ResolvedListeSasuHolding.from_context(ctx)
        document = new_document()

        add_paragraph(document, "Etat des souscriptions ")
        add_paragraph(document, f"De la {FORME_COURTE} {data.denomination}")
        add_bordered_data_table(
            document,
            [
                "Noms, prénoms et adresse des souscripteurs",
                f"Nombre d{_APOS}actions souscrites",
                "Montant des souscriptions",
            ],
            [
                [
                    data.souscripteur_nom,
                    f"{data.nb_actions_dot} ",
                    # R5 (Rafael 2026-07-09) : montant groupe des 4 chiffres (« 1 000 »).
                    f"{group_montant(data.montant)} ",
                ],
                # TOTAL : montant groupe + unite « euros » derivee/accordee (« 1 000 euros »).
                ["TOTAL", f"{data.nb_actions_dot} actions", f"{montant_avec_euros(data.montant)}"],
            ],
        )
        add_paragraph(document, f"Fait à {data.lieu_signature}")
        add_paragraph(document, f"Le {data.date_signature}")
        add_paragraph(document, f" {data.signature_nom}")

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        # KAN-36 : bloc signature final solidaire (une seule page).
        keep_final_signature_block_together(document)
        document.save(output_path)
        return output_path


class _ResolvedListeSasuHolding:
    def __init__(
        self,
        *,
        denomination: str,
        souscripteur_nom: str,
        nb_actions_dot: str,
        montant: str,
        lieu_signature: str,
        date_signature: str,
        signature_nom: str,
    ) -> None:
        self.denomination = denomination
        self.souscripteur_nom = souscripteur_nom
        self.nb_actions_dot = nb_actions_dot
        self.montant = montant
        self.lieu_signature = lieu_signature
        self.date_signature = date_signature
        self.signature_nom = signature_nom

    @classmethod
    def from_context(cls, ctx: DocumentGenerationContext) -> _ResolvedListeSasuHolding:
        if ctx.structure != "SASU_HOLDING":
            raise ValueError(f"dossier.structure doit etre SASU_HOLDING pour {DOCUMENT_CODE}.")
        # KAN-2 (Rafael 2026-07-14) : « tous les documents doivent pouvoir être générés, MÊME SI
        # aucun champ n'est rempli. » -> aucun `raise` sur donnée manquante : un objet absent tombe
        # sur une instance VIDE dont chaque champ ressort en « (À COMPLÉTER : … ) »
        # (`_required_text`), jamais un crash. La sortie NOMINALE reste byte-identique.
        person = _required_person(ctx)
        statuts = ctx.statuts_sasu_holding or StatutsSasuHoldingContext()
        societe = ctx.societe or Company()

        # AFFICHAGE d'une quantité : non renseignée (None) OU nulle -> marqueur, JAMAIS un « 0 »
        # affirmé (un état des souscriptions qui annonce « 0 action » est faux). Renseignée ->
        # format à point du modèle Albane (« 10.000 »), byte-identique au gold.
        nb_actions = statuts.nb_actions
        nb_actions_dot = (
            _fmt_dot_thousands(nb_actions)
            if nb_actions is not None and nb_actions >= 1
            else _marqueur("nombre d'actions souscrites")
        )
        civilite = _required_text(person.civilite, "civilité de l'associé")
        prenom = _required_text(person.prenom, "prénom de l'associé")
        nom = _required_text(person.nom, "nom de l'associé")

        return cls(
            denomination=_required_text(societe.denomination, "dénomination de la société"),
            souscripteur_nom=f"{civilite} {prenom} {nom}",
            nb_actions_dot=nb_actions_dot,
            montant=_required_text(societe.capital_social, "capital social"),
            lieu_signature=_required_text(ctx.signature.lieu, "lieu de signature"),
            date_signature=_display_date(ctx.signature.date, "date de signature"),
            signature_nom=f"{prenom} {nom}",
        )


# KAN-2 (Rafael 2026-07-14) — champ absent -> marqueur métier visible « (À COMPLÉTER : <libellé> ) »
# (via `libelle_metier`, aligné sur le pattern SPFPL / `statuts_sel_exercice_common.required_text`).
# Le libellé passé est déjà métier -> `libelle_metier` le laisse traverser et garantit qu'il reste
# SANS point / underscore / crochet / chiffre.
def _marqueur(field_name: str) -> str:
    return f"(À COMPLÉTER : {libelle_metier(field_name)})"


def _required_person(ctx: DocumentGenerationContext) -> Person:
    # KAN-2 : associé absent -> instance vide (genre masculin neutre, identité vide) dont chaque
    # champ ressort en marqueur ; `Person` exige genre/civilite/prenom/nom, on les fournit vides.
    if ctx.personne_signataire is None:
        return Person(genre=Gender.MASCULIN, civilite="", prenom="", nom="")
    return ctx.personne_signataire


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        return _marqueur(field_name)
    return value.strip()


def _fmt_dot_thousands(value: int) -> str:
    """Format milliers a POINT (« 10000 » -> « 10.000 »), verbatim modele Albane."""
    return f"{value:,}".replace(",", ".")


def _display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        return _marqueur(field_name)
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return _required_text(value, field_name)
