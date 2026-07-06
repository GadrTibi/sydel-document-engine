"""Generateur from-scratch des statuts SELAS UNIPERSONNELLE chirurgien-dentiste (DOC-046).

Retour Rafael #5 : « la SELAS unipersonnelle dentiste = la pluripersonnelle dentiste
mais avec un seul associe ». Clone structurel du generateur SELAS uni medecin
(`StatutsSelasMedecinGenerator`) : meme machinerie partagee (associe unique, ordre,
depot, exercice, capital en lettres, clause matrimoniale, signature electronique),
mais avec les BLOCS DENTISTE (`STATUTS_SELAS_DENTISTE_BLOCKS`, wording repris VERBATIM
du modele source dentiste pluri valide, uni-fie) et l'overlay `selas_dentiste`.

Aucune regle metier ni wording juridique inventes : le texte des statuts vient du
modele `Statuts_SELAS_dentiste_pluri_modele.docx` ; le generateur n'emet que des
substitutions de tokens deja portees par la couche partagee SEL d'exercice.
"""

from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    DOCUMENT_CODE,
    OVERLAY_SELAS_DENTISTE,
    STRUCTURE_SELAS,
    add_conjoint_replacements,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    render_statuts_sel_docx,
    required_associe_unique,
    required_text,
    validate_sel_context,
)
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_templates import (
    STATUTS_SELAS_DENTISTE_BLOCKS,
)
from sydel_doc_engine.utils.grammar import montant_lettres_avec_unite

OUTPUT_FILENAME = "statuts_selas_dentiste.docx"


class StatutsSelasDentisteGenerator:
    """Generateur from-scratch des statuts SELAS unipersonnelle chirurgien-dentiste V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_sel_context(
            ctx,
            expected_structure=STRUCTURE_SELAS,
            expected_overlay=OVERLAY_SELAS_DENTISTE,
        )
        associate = required_associe_unique(ctx)
        # Le modele dentiste vit avec un titre encadre genere par le renderer partage ;
        # les blocs dentiste ne portent pas de second lieu d'exercice (un seul lieu, comme
        # le modele source dentiste pluri) -> pas de gestion de second lieu ici.
        replacements = common_replacements(ctx, title_type="actions")
        add_conjoint_replacements(replacements, associate)
        add_ordre_replacements(replacements, associate)
        add_depot_replacements(replacements, ctx, require_address=True)
        add_exercice_replacements(
            replacements,
            ctx,
            require_debut_fin=True,
            require_lieu=True,
        )
        if ctx.capital is None:
            raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
        # Tokens specifiques aux blocs dentiste non couverts par common_replacements :
        # le nombre d'actions et la valeur nominale EN LETTRES (article 6), le titre
        # professionnel de l'apporteur (« Le Docteur … »), et le prestataire de
        # signature electronique (article 32).
        replacements.update(
            {
                "[nb_actions_lettres]": required_text(
                    ctx.capital.nombre_titres_total_lettres,
                    "capital.nombre_titres_total_lettres",
                ),
                # 7.5 (Albane 2026-07-06) : token unique lettres+unite (anti double-euro / espace).
                # ENTIER -> « un euro » (byte-identique) ; DECIMAL -> « un centime d’euro ».
                "[valeur_nominale_action_avec_unite]": montant_lettres_avec_unite(
                    required_text(
                        ctx.capital.valeur_nominale_titre_lettres,
                        "capital.valeur_nominale_titre_lettres",
                    ),
                    ctx.capital.valeur_nominale_titre,
                ),
                "[titre_professionnel]": required_text(
                    associate.titre_professionnel or associate.civilite_affichage,
                    "associes[0].titre_professionnel",
                ),
                "[prestataire_signature_electronique]": required_text(
                    ctx.signature.prestataire_signature_electronique,
                    "signature.prestataire_signature_electronique",
                ),
            }
        )

        return render_statuts_sel_docx(
            STATUTS_SELAS_DENTISTE_BLOCKS,
            replacements,
            output_dir / OUTPUT_FILENAME,
            associate=associate,
            # Retours Albane « mise en forme » : mise en forme SELAS (adresse du
            # siege en gras, sous-articles soulignes) et saut de page avant
            # l'ANNEXE (2.10). Le modele dentiste n'a pas de designation President
            # nominative (art. 19 generique) -> 2.7 sans effet ici (attendu).
            selas_formatting=True,
            annex_page_break=True,
        )
