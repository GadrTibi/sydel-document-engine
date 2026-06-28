# ruff: noqa: E501
from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_civils_common import (
    MICRO_HOLDING_TEMPLATE,
    generate_statuts_civil_docx,
)

# Micro holding (demande Albane 2026-06-26) : societe civile A CAPITAL VARIABLE. Deux variantes
# d'objet social, composees A PARTIR de nos modeles sources (provenance tracee, rien d'invente) :
#   - VARIANTE A : objet du modele SCI, article 2 — VERBATIM mot-a-mot (apostrophes typographiques
#     U+2019 preservees, conformite gold-fidelity au modele source).
#   - VARIANTE B (objet holding) : COMPOSITE (PAS un verbatim SASU integral, A FAIRE VALIDER PAR
#     ALBANE) = chapeau « caractere strictement civil » (AJOUTE pour l'adaptation civile, absent du
#     SASU) + SEUL le para « participation… » est VERBATIM SASU mot-a-mot + para « portefeuille de
#     valeurs mobilieres » IMPORTE du modele SCI (absent du SASU) + clause finale = VERBATIM SASU
#     avec la seule adaptation « civiles et commerciales » -> « civiles ». La composition de B
#     (chapeau ajoute + para portefeuille importe + retrait « et commerciales ») reste A VALIDER par
#     Albane. Albane tranchera A vs B ; on construit les deux, la mauvaise sera retiree.

OBJET_VARIANTE_A = "La Société a pour objet, dans la limite des opérations à caractère strictement civil, à l'exclusion de toute opération commerciale :\nL'acquisition, l’administration, l’exploitation et la gestion, la location, la disposition de tous biens et droits immobiliers.\nExceptionnellement, l’aliénation de ces mêmes biens, notamment au moyen de vente, échange ou apport en société.\nLa propriété, l'administration et l'exploitation par bail, location ou autre de tous immeubles, bâtis ou non bâtis, dont la Société pourrait devenir propriétaire ultérieurement, par voie d'acquisition, échange, apport ou autrement.\nLa mise en copropriété de tous immeubles, appartements, locaux séparés et droits ou jouissance exclusive et particulière portant sur des lots à fractions de lots, soit achevés, soit à terme ou en l'état futur d'achèvement.\nL'organisation du patrimoine social en vue d'en faciliter la gestion et la transmission afin d'éviter qu'il ne soit livré aux aléas de l'indivision du patrimoine familial des associés,\nLa propriété et la gestion d'un portefeuille de valeurs mobilières, droits sociaux ou tous autres titres, détenus en pleine propriété, nue-propriété ou usufruit, par voie d'achat, d'échange, d'apport, de souscriptions de parts, d'actions, obligations et de tous titres ou droits sociaux en général.\nTous emprunts avec ou sans garantie hypothécaire ayant pour but de permettre la réalisation de l'objet social.\nEt généralement, toutes opérations quelconques pouvant se rattacher directement ou indirectement à l'objet ci-dessus défini ou en faciliter la réalisation pourvu que ces opérations ne modifient en rien le caractère civil de la Société."

OBJET_VARIANTE_B = "La Société a pour objet, dans la limite des opérations à caractère strictement civil :\nLa participation de la société, par tous moyens, à toutes entreprises ou sociétés créées ou à créer, pouvant se rattacher à l’objet social, notamment par voie de création de sociétés nouvelles, d’apport, de commandite, souscription ou rachat de titres ou droits sociaux, fusion, alliance ou association en participation ou groupement d’intérêt économique ou de location-gérance.\nLa propriété et la gestion d'un portefeuille de valeurs mobilières, droits sociaux ou tous autres titres, détenus en pleine propriété, nue-propriété ou usufruit, par voie d'achat, d'échange, d'apport, de souscriptions de parts, d'actions, obligations et de tous titres ou droits sociaux en général.\nEt, plus généralement, toutes opérations, de quelque nature qu'elles soient, juridiques, économiques et financières, civiles, se rattachant à l'objet sus-indiqué ou à tous autres objets similaires ou connexes, de nature à favoriser, directement ou indirectement, le but poursuivi par la société, son extension ou son développement."

OBJET_VARIANTES: dict[str, str] = {
    "A": OBJET_VARIANTE_A,
    "B": OBJET_VARIANTE_B,
}


def objet_social_for_variante(variante: str | None) -> str:
    """Texte de l'objet social pour la variante choisie (defaut « A »).

    Aucune valeur inventee : map fermee sur les deux variantes composees des modeles sources.
    """
    key = (str(variante or "A").strip().upper()) or "A"
    return OBJET_VARIANTES.get(key, OBJET_VARIANTE_A)


class StatutsMicroHoldingGenerator:
    """Generateur des statuts micro holding (societe civile a capital variable).

    Reutilise integralement le socle civil (generate_statuts_civil_docx) avec le modele
    clone du SCI dont le seul bloc objet est le token [objet_social]. L'objet (variante A
    ou B) est resolu en amont (slice) et porte par ctx.statuts_civils.objet_social.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        return generate_statuts_civil_docx(ctx, output_dir, MICRO_HOLDING_TEMPLATE)
