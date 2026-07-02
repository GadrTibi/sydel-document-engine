from __future__ import annotations

import re
from pathlib import Path

from docx import Document

from sydel_doc_engine.domain.models import DocumentGenerationContext, SpfplPerson
from sydel_doc_engine.generators.lot_05.scm_cession_common import mentions_conjoint
from sydel_doc_engine.generators.lot_05.spfpl_common import (
    company_siege_display,
    elision_de,
    required_cedant,
    required_cession_parts,
    required_int,
    required_societe_cible,
    required_societe_spfpl,
    required_text,
    validate_cession_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    add_hyphen_list_item,
    add_paragraph,
    new_document,
)

OUTPUT_FILENAME = "acte_cession_parts_spfpl.docx"
_SOURCE_NAME = "Acte_cession_SPFPL_tiers_part_modele.docx"

# SP1/SP3/SP4 (Albane 2026-06-25) : ce generateur etait FROM-SCRATCH (texte code en
# dur, non accentue, ~15 sections, paraphrases vs le modele Albane qui en compte ~30 :
# GAP, RENONCIATION, SIGNIFICATION, AFFIRMATION DE SINCERITE...). « Tout revoir » = le
# rebatir en TOKEN-REPLACEMENT : on CHARGE le modele source (texte legal complet, accents
# et formulations d'Albane preserves par construction) et on remplace les placeholders.
# SP2 : le modele utilise [civilite_cedant] (M./Mme) en civilite et « Dr » abrege en
# repartition — JAMAIS « Le Docteur » en civilite ; la fidelite restaure donc la civilite
# civile demandee. Meme infra que les statuts civils (_source_path + remplacement).

# Lignes de repartition du capital : le modele porte 3 lignes figees
# (« - Dr [prenom] [nom] detenant [parts_personne_N] parts »). On les remplace par la
# repartition DYNAMIQUE (une ligne par associe reel via capital_before_lines).
_REPARTITION_MARKER = "[parts_personne_"


def _is_repartition_row(text: str, block_open: bool) -> bool:
    """Une ligne de repartition du capital : porte le placeholder fige
    « [parts_personne_N] », ou (bloc deja ouvert) une ligne « - … detenant … »
    residuelle des personnes 2/3 du modele a 3 lignes figees."""
    if _REPARTITION_MARKER in text:
        return True
    return block_open and bool(re.match(r"^\s*-\s", text)) and "detenant" in text.lower()


def _source_path() -> Path:
    path = Path("project/source_documents/lot_05") / _SOURCE_NAME
    if not path.exists():
        raise ValueError(f"modele source introuvable pour {OUTPUT_FILENAME}: {path}")
    return path


def _date_fr(value: object) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value or "")


def _person_address(person: SpfplPerson, field_name: str) -> str:
    if person.adresse_personnelle_affichee:
        return person.adresse_personnelle_affichee.strip()
    struct = person.adresse_personnelle
    if struct is not None and struct.adresse_affichee:
        return struct.adresse_affichee.strip()
    return required_text(
        person.adresse_personnelle_affichee,
        f"{field_name}.adresse_personnelle_affichee",
    )


def _repartition_lines(ctx: DocumentGenerationContext) -> list[str]:
    """Repartition du capital, FIDELE au modele : « Dr <prenom> <nom> detenant N part(s) »
    (abrege « Dr », accents preserves), une ligne par associe reel."""
    associes = ctx.associes_cible or []
    if not associes:
        raise ValueError(f"associes_cible est obligatoire pour {OUTPUT_FILENAME}.")
    lines: list[str] = []
    for index, associe in enumerate(associes):
        field = f"associes_cible[{index}]"
        nb_parts = required_int(associe.nb_parts_avant, f"{field}.nb_parts_avant")
        label = "part" if nb_parts == 1 else "parts"
        if associe.type == "personne_morale":
            who = required_text(associe.denomination, f"{field}.denomination")
        else:
            prenom = required_text(associe.prenom, f"{field}.prenom")
            nom = required_text(associe.nom, f"{field}.nom")
            who = f"Dr {prenom} {nom}"
        lines.append(f"{who} détenant {nb_parts} {label}")
    return lines


class ActeCessionPartsSpfplGenerator:
    """Generateur token-replacement de l'acte de cession de parts SPFPL (fidele au
    modele source Albane, cf. SP1-SP4 2026-06-25)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_cession_context(ctx)
        cedant = required_cedant(ctx)
        cession_parts = required_cession_parts(ctx)
        societe_spfpl = required_societe_spfpl(ctx)
        societe_cible = required_societe_cible(ctx)
        representant = societe_spfpl.representant
        if representant is None:
            raise ValueError("societe_spfpl.representant est obligatoire.")

        replacements = self._build_replacements(
            ctx, cedant, cession_parts, societe_spfpl, societe_cible, representant
        )
        repartition = _repartition_lines(ctx)

        source = Document(str(_source_path()))
        docx = new_document()
        repartition_block_open = False
        for paragraph in source.paragraphs:
            text = paragraph.text
            if _is_repartition_row(text, repartition_block_open):
                # Premiere ligne d'un bloc de repartition -> emettre la liste dynamique ;
                # lignes suivantes du meme bloc fige (personne_2/3) -> absorbees.
                if not repartition_block_open:
                    for line in repartition:
                        add_hyphen_list_item(docx, line)
                repartition_block_open = True
                continue
            repartition_block_open = False
            rendered = _replace(text, replacements).strip()
            if not rendered:
                continue
            add_paragraph(docx, rendered)

        # SP3 (Akainu M1/M2) : PAS de bloc signature ajoute — le modele source porte DEJA sa
        # ligne de signature (« Dr <cedant> / La société <cessionnaire> / Représentée par … »),
        # rendue fidelement (accentuee) par le token-replacement ci-dessus. Un bloc ajoute la
        # dupliquait ET perdait les accents (« La societe »/« Representee »).
        self._assert_no_residual(docx)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        docx.save(output_path)
        return output_path

    def _build_replacements(
        self, ctx, cedant, cession_parts, societe_spfpl, societe_cible, representant
    ) -> dict[str, str]:
        cible_total = required_int(societe_cible.nb_parts_total, "societe_cible.nb_parts_total")
        cible_capital = required_text(societe_cible.capital_social, "societe_cible.capital_social")
        ordre = cedant.ordre
        conjoint = cedant.conjoint
        # R0702-02 / Akainu M1 (2026-07-02) : le menu matrimonial complet ouvre le cas NON-MARIE.
        # Le modele porte « [situation_maritale_cedant] avec [conjoint...] » (« avec » LITTERAL) ->
        # un non-marie faisait fuiter « célibataire avec (À COMPLÉTER : …) » (conjoint fantome +
        # placeholder shippe). On branche la ligne comme l'acte d'ACTIONS (garde PARTAGE
        # mentions_conjoint, R22-02) : marie -> ligne complete BYTE-IDENTIQUE ; sinon -> statut seul.
        # La cle COMBINEE (plus longue) est traitee AVANT les tokens simples par `_replace`, donc
        # elle consomme tout le fragment « [situation_maritale_cedant] avec [conjoint...] » de P36.
        cedant_maritale = required_text(cedant.situation_maritale, "cedant.situation_maritale")
        if mentions_conjoint(cedant.situation_maritale):
            conjoint_civilite = required_text(
                conjoint.civilite_affichage if conjoint else None,
                "cedant.conjoint.civilite_affichage",
            )
            conjoint_prenom = required_text(
                conjoint.prenom if conjoint else None, "cedant.conjoint.prenom"
            )
            conjoint_nom = required_text(conjoint.nom if conjoint else None, "cedant.conjoint.nom")
            ligne_maritale_cedant = (
                f"{cedant_maritale} avec {conjoint_civilite} {conjoint_prenom} {conjoint_nom}"
            )
        else:
            conjoint_civilite = conjoint_prenom = conjoint_nom = ""
            ligne_maritale_cedant = cedant_maritale
        repl = {
            # Cle COMBINEE (fragment matrimonial complet) : branche marie/non-marie, byte-identique
            # au modele pour un marie. Placee avant les tokens simples (longest-first dans _replace).
            "[situation_maritale_cedant] avec [civilite_conjoint_cedant] "
            "[prenom_conjoint_cedant] [nom_conjoint_cedant]": ligne_maritale_cedant,
            # Cedant (personne physique)
            "[civilite_cedant]": required_text(
                cedant.civilite_affichage, "cedant.civilite_affichage"
            ),
            "[prenom_cedant]": required_text(cedant.prenom, "cedant.prenom"),
            "[nom_cedant]": required_text(cedant.nom, "cedant.nom"),
            "[profession_cedant]": required_text(cedant.profession, "cedant.profession"),
            "[date_naissance_cedant]": _date_fr(cedant.date_naissance),
            "[ville_naissance_cedant]": required_text(
                cedant.ville_naissance, "cedant.ville_naissance"
            ),
            "[departement_naissance_cedant]": required_text(
                cedant.departement_naissance, "cedant.departement_naissance"
            ),
            "[nationalite_cedant]": required_text(cedant.nationalite, "cedant.nationalite"),
            "[adresse_cedant]": _person_address(cedant, "cedant"),
            # Fallback (P36 est deja consomme par la cle combinee ci-dessus ; ces tokens simples
            # ne restent que pour robustesse s'ils apparaissaient ailleurs). Valeurs conjoint = ""
            # pour un non-marie (jamais de « (À COMPLÉTER) » ni de conjoint fantome).
            "[situation_maritale_cedant]": cedant_maritale,
            "[numero_rpps_cedant]": required_text(
                ordre.numero_rpps if ordre else None, "cedant.ordre.numero_rpps"
            ),
            "[ordre_departemental_cedant]": required_text(
                ordre.departement if ordre else None, "cedant.ordre.departement"
            ),
            "[profession_reglementee]": required_text(
                cedant.profession_reglementee, "cedant.profession_reglementee"
            ),
            "[profession_reglementee_pluriel]": required_text(
                cedant.profession_reglementee_pluriel, "cedant.profession_reglementee_pluriel"
            ),
            "[civilite_conjoint_cedant]": conjoint_civilite,
            "[prenom_conjoint_cedant]": conjoint_prenom,
            "[nom_conjoint_cedant]": conjoint_nom,
            # Societe cedee (cible)
            "[denomination_societe_cedee]": required_text(
                societe_cible.denomination, "societe_cible.denomination"
            ),
            "[forme_sociale_complete]": required_text(
                societe_cible.forme_sociale_complete, "societe_cible.forme_sociale_complete"
            ),
            "[capital_social_societe_cedee]": cible_capital,
            "[nb_parts_total_societe_cedee]": str(cible_total),
            "[ville_rcs_societe_cedee]": required_text(
                societe_cible.ville_rcs, "societe_cible.ville_rcs"
            ),
            "[numero_rcs_societe_cedee]": required_text(
                societe_cible.numero_rcs, "societe_cible.numero_rcs"
            ),
            "[adresse_siege]": company_siege_display(societe_cible, "societe_cible"),
            "[departement_inscription_societe]": required_text(
                ordre.departement if ordre else None, "cedant.ordre.departement"
            ),
            # SP3 (Akainu M3) : champ CTX « cent euros » + elision corrigee. Le modele colle
            # « d’[valeur…] » : « cent euros » commence par une consonne -> « DE cent euros »
            # (pas « d’cent euros »). La cle combinee (plus longue) est traitee en premier.
            "d’[valeur_nominale_part_lettres]": elision_de(
                required_text(
                    societe_cible.valeur_nominale_part_lettres,
                    "societe_cible.valeur_nominale_part_lettres",
                )
            ),
            "[valeur_nominale_part_lettres]": required_text(
                societe_cible.valeur_nominale_part_lettres,
                "societe_cible.valeur_nominale_part_lettres",
            ),
            # Societe cessionnaire (SPFPL acquereur)
            "[denomination_societe_cessionnaire]": required_text(
                societe_spfpl.denomination, "societe_spfpl.denomination"
            ),
            "[forme_sociale_acquereur]": required_text(
                societe_spfpl.forme_sociale, "societe_spfpl.forme_sociale"
            ),
            "[capital_social_cessionnaire]": required_text(
                societe_spfpl.capital_social, "societe_spfpl.capital_social"
            ),
            "[ville_rcs_cessionnaire]": required_text(
                societe_spfpl.ville_rcs, "societe_spfpl.ville_rcs"
            ),
            "[numero_rcs_acquereur]": required_text(
                societe_spfpl.numero_rcs, "societe_spfpl.numero_rcs"
            ),
            "[adresse_siege_cessionnaire]": company_siege_display(societe_spfpl, "societe_spfpl"),
            "[civilite_acquereur_representant]": required_text(
                representant.civilite_affichage, "representant.civilite_affichage"
            ),
            "[civilite_representant_cessionnaire_courte]": required_text(
                representant.civilite_courte, "representant.civilite_courte"
            ),
            "[prenom_representant_cessionnaire]": required_text(
                representant.prenom, "representant.prenom"
            ),
            "[nom_representant_cessionnaire]": required_text(representant.nom, "representant.nom"),
            "[fonction_acquereur_representant]": required_text(
                representant.fonction, "representant.fonction"
            ),
            # Cession
            "[nb_parts_cedees]": str(
                required_int(cession_parts.nb_parts, "cession_parts.nb_parts")
            ),
            "[nb_parts_cedees_lettres]": required_text(
                cession_parts.nb_parts_lettres, "cession_parts.nb_parts_lettres"
            ),
            "[prix_unitaire_part]": required_text(
                cession_parts.prix_unitaire, "cession_parts.prix_unitaire"
            ),
            "[prix_unitaire_part_lettres]": required_text(
                cession_parts.prix_unitaire_lettres, "cession_parts.prix_unitaire_lettres"
            ),
            "[prix_cession]": required_text(cession_parts.prix_total, "cession_parts.prix_total"),
            "[prix_cession_lettres]": required_text(
                cession_parts.prix_total_lettres, "cession_parts.prix_total_lettres"
            ),
            # Signature
            "[lieu_signature]": required_text(ctx.signature.lieu, "signature.lieu"),
            "[date_signature]": _date_fr(ctx.signature.date),
            "[nombre_exemplaires_lettres]": required_text(
                cession_parts.nombre_exemplaires_lettres
                or (ctx.document.nombre_exemplaires_lettres if ctx.document else None),
                "cession_parts.nombre_exemplaires_lettres",
            ),
        }
        return repl

    @staticmethod
    def _assert_no_residual(docx) -> None:
        full = "\n".join(p.text for p in docx.paragraphs)
        if "[" in full or "]" in full:
            residual = re.findall(r"\[[^\]]+\]", full)
            raise ValueError(f"placeholder source residuel dans {OUTPUT_FILENAME}: {residual}")


def _replace(text: str, replacements: dict[str, str]) -> str:
    out = text
    # Tokens les plus LONGS d'abord : une cle combinee « d’[valeur…] » (gestion de l'elision)
    # doit etre traitee AVANT le token simple « [valeur…] » qu'elle contient.
    for token in sorted(replacements, key=len, reverse=True):
        if token in out:
            out = out.replace(token, replacements[token])
    return out

