from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    DocumentGenerationContext,
    StatutsCivilsAssocie,
    StatutsSelasMultiContext,
    StatutsSelasMultiPresident,
)
from sydel_doc_engine.generators.lot_04.annexe_filter import is_creation_fee_annexe_line
from sydel_doc_engine.rendering.docx_builder import (
    add_paragraph,
    add_statuts_article_heading,
    add_statuts_body_paragraph,
    add_statuts_hanging_list_item,
    add_statuts_part_heading,
    add_statuts_signature_block,
    add_statuts_title_box,
    new_document,
)
from sydel_doc_engine.utils.grammar import elision_de

DOCUMENT_CODE = "CODE-STATUTS-SELAS-MULTI-001"
STRUCTURE_SELAS = "SELAS"
MAX_ASSOCIES = 6  # retours 2026-06-17 : SELAS multi 2 a 6 associes
MIN_ASSOCIES = 2

# --- Profils par profession reglementee --------------------------------------------------
#
# Le moteur lit un modele DOCX tokenise et reinjecte, selon le nombre reel d'associes, les
# blocs DYNAMIQUES (comparution, apports, repartition du capital, designation du President,
# signatures). En dehors de ces fenetres il rend le paragraphe source tel quel en substituant
# les placeholders societe. La SOURCE, les fenetres d'index et le wording reinjecte different
# selon la profession :
#   - medecin           -> Statuts_SELAS_multi_modele.docx (corpus medecin, 38 articles,
#                          deontologie medicale) ; comportement HISTORIQUE inchange.
#   - chirurgien-dentiste -> Statuts_SELAS_dentiste_pluri_modele.docx (corpus dentiste,
#                          32 articles, R. 4113-1 Code de la sante publique).
# Cf. docs/project/types/SELAS/REYNAUD_TOKENISATION_NOTES.md.

SOURCE_NAME = "Statuts_SELAS_multi_modele.docx"  # retro-compat (medecin) — lu par les tests/audits

# Index de paragraphes (0-based python-docx) des blocs dynamiques — MODELE MEDECIN (inchange).
COMPARUTION_SLICE = (16, 20)
APPORTS_SLICE = (72, 74)
CAPITAL_SLICE = (88, 94)
PRESIDENT_SLICE = (221, 223)
SIGNATURE_SLICE = (510, 511)
# Le modele medecin vit avec un titre encadre "STATUTS" dans une TABLE (non iteree par
# python-docx). On le restaure avant "LES SOUSSIGNEES" (para 14), comme les statuts civils.
STATUTS_TITLE_BOX_BEFORE = 14


@dataclass(frozen=True)
class _SelasProfile:
    """Parametrage par profession : modele source, fenetres d'index des blocs dynamiques,
    titre encadre eventuel, et builders de blocs (reproduisant le wording du modele cible)."""

    source_name: str
    comparution_slice: tuple[int, int]
    apports_slice: tuple[int, int]
    capital_slice: tuple[int, int]
    signature_slice: tuple[int, int]
    add_comparution: Callable[[object, _ResolvedSelasMulti], None]
    add_apports: Callable[[object, _ResolvedSelasMulti], None]
    add_capital: Callable[[object, _ResolvedSelasMulti], None]
    add_signature: Callable[[object, _ResolvedSelasMulti], None]
    # Fenetre de designation nominative du President (modele medecin uniquement) ; None pour
    # le modele dentiste, dont l'article President est entierement generique (jamais nomme).
    president_slice: tuple[int, int] | None = None
    add_president: Callable[[object, _ResolvedSelasMulti], None] | None = None
    # Index avant lequel restaurer le titre encadre "STATUTS" (modele medecin) ; None si le
    # modele ne porte pas de titre encadre dans une table (cas dentiste, 0 table).
    title_box_before: int | None = None
    # Substitutions supplementaires propres au modele : le corpus dentiste porte des VALEURS
    # CONCRETES d'exemple dans son boilerplate (denomination, siege, banque, ligne capital) la
    # ou le corpus medecin porte des placeholders [..]. On remplace ces lignes-exemple par les
    # donnees reelles de la societe. None pour le modele medecin (placeholders deja geres).
    boilerplate_replacements: Callable[[_ResolvedSelasMulti], dict[str, str]] | None = None


def _select_profile(profession_reglementee: str) -> _SelasProfile:
    profession = (profession_reglementee or "").strip().casefold()
    if "dentiste" in profession:
        return _DENTISTE_PROFILE
    return _MEDECIN_PROFILE


class StatutsSelasMultiGenerator:
    """Generateur SELAS multi (statuts de creation) lisant le modele tokenise et reinjectant
    les blocs dynamiques (comparution N, apports N, repartition capital N en actions,
    designation du President, ligne de signature N), 2 a 6 associes dont au moins une
    personne physique exercante et un eventuel associe personne morale. Le modele source et
    les fenetres d'index sont choisis selon la profession reglementee (medecin / dentiste)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:  # noqa: C901
        data = _ResolvedSelasMulti.from_context(ctx)
        profile = data.profile
        source_doc = Document(_source_path(profile.source_name))
        output_doc = new_document()
        output_doc.sections[0].footer.paragraphs[0].text = (
            f"{data.denomination} - Statuts constitutifs"
        )

        replacements = data.common_replacements()
        if profile.boilerplate_replacements is not None:
            replacements = {**replacements, **profile.boilerplate_replacements(data)}
        skip_until = -1
        for index, paragraph in enumerate(source_doc.paragraphs):
            if index < skip_until:
                continue
            if profile.title_box_before is not None and index == profile.title_box_before:
                add_statuts_title_box(output_doc, "STATUTS")
            if index == profile.comparution_slice[0]:
                profile.add_comparution(output_doc, data)
                skip_until = profile.comparution_slice[1]
                continue
            if index == profile.apports_slice[0]:
                profile.add_apports(output_doc, data)
                skip_until = profile.apports_slice[1]
                continue
            if index == profile.capital_slice[0]:
                profile.add_capital(output_doc, data)
                skip_until = profile.capital_slice[1]
                continue
            if (
                profile.president_slice is not None
                and profile.add_president is not None
                and index == profile.president_slice[0]
            ):
                profile.add_president(output_doc, data)
                skip_until = profile.president_slice[1]
                continue
            if index == profile.signature_slice[0]:
                profile.add_signature(output_doc, data)
                skip_until = profile.signature_slice[1]
                continue

            text = paragraph.text.strip()
            if not text:
                continue
            # N6 (Rafael 2026-06-24) : les puces a tiret du modele (style « Tirets », numId=7 :
            # art.1, 14, 16, 21...) portent le tiret dans le NUMBERING Word, pas dans .text -> il
            # etait perdu. On re-prefixe « - » pour que le renderer les rende en hanging list item
            # (add_statuts_hanging_list_item). Systemique : toute puce a ce style.
            if _is_tiret_list_paragraph(paragraph) and not text.startswith("-"):
                text = f"- {text}"
            rendered = _replace_placeholders(text, replacements)
            if is_creation_fee_annexe_line(rendered):  # O24-01 : annexe sans frais cabinet création
                continue
            # N6 (Rafael 2026-06-24) : l'annexe demarre sur une NOUVELLE PAGE (parite gold SELARL,
            # cf. annex_page_break du renderer partage). Le modele source porte le titre « ANNEXE ».
            if rendered.strip().upper() == "ANNEXE":
                output_doc.add_page_break()
            _add_rendered_paragraph(output_doc, rendered)

        full_text = "\n".join(paragraph.text for paragraph in output_doc.paragraphs)
        if "[" in full_text or "]" in full_text:
            raise ValueError(f"placeholder source residuel dans le rendu {DOCUMENT_CODE}.")

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "statuts_selas_multi.docx"
        output_doc.save(output_path)
        return output_path


class _ResolvedSelasMulti:
    def __init__(
        self,
        *,
        selas: StatutsSelasMultiContext,
        profile: _SelasProfile,
        denomination: str,
        adresse_siege: str,
        signature_lieu: str,
        signature_date: str,
        associes: list[StatutsCivilsAssocie],
        president: StatutsCivilsAssocie,
    ) -> None:
        self.selas = selas
        self.profile = profile
        self.denomination = denomination
        self.adresse_siege = adresse_siege
        self.signature_lieu = signature_lieu
        self.signature_date = signature_date
        self.associes = associes
        self.president = president

    @classmethod
    def from_context(cls, ctx: DocumentGenerationContext) -> _ResolvedSelasMulti:
        if ctx.structure != STRUCTURE_SELAS:
            raise ValueError(f"dossier.structure doit etre {STRUCTURE_SELAS} pour {DOCUMENT_CODE}.")
        if ctx.statuts_selas_multi is None:
            raise ValueError(f"statuts_selas_multi est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.societe is None or ctx.societe.siege is None:
            raise ValueError(f"societe.siege est obligatoire pour {DOCUMENT_CODE}.")
        selas = ctx.statuts_selas_multi
        profile = _select_profile(
            _required_text(
                selas.profession_reglementee,
                "statuts_selas_multi.profession_reglementee",
            )
        )
        associes = list(selas.associes)
        _validate_associes(associes, selas)
        president = _resolve_president(associes, selas.president)
        return cls(
            selas=selas,
            profile=profile,
            denomination=_required_text(ctx.societe.denomination, "societe.denomination"),
            adresse_siege=_address_display(ctx.societe.siege, "societe.siege"),
            signature_lieu=_required_text(ctx.signature.lieu, "signature.lieu"),
            signature_date=_format_display_date(ctx.signature.date, "signature.date"),
            associes=associes,
            president=president,
        )

    def common_replacements(self) -> dict[str, str]:
        selas = self.selas
        return {
            "[denomination_societe]": self.denomination,
            "[profession_reglementee]": _required_text(
                selas.profession_reglementee,
                "statuts_selas_multi.profession_reglementee",
            ),
            "[profession_reglementee_pluriel]": _required_text(
                selas.profession_reglementee_pluriel,
                "statuts_selas_multi.profession_reglementee_pluriel",
            ),
            "[capital_social]": _required_text(
                selas.capital_social,
                "statuts_selas_multi.capital_social",
            ),
            "[capital_lettres]": _required_text(
                selas.capital_social_lettres,
                "statuts_selas_multi.capital_social_lettres",
            ),
            "[nb_actions]": str(
                _required_int(selas.nb_actions_total, "statuts_selas_multi.nb_actions_total")
            ),
            "[nb_actions_lettres]": _required_text(
                selas.nb_actions_total_lettres,
                "statuts_selas_multi.nb_actions_total_lettres",
            ),
            "[valeur_nominale_action]": _required_text(
                selas.valeur_nominale_action,
                "statuts_selas_multi.valeur_nominale_action",
            ),
            # Akainu B1 (regle 68) : le modele art.8 colle « d’[valeur…] » -> elision via le
            # helper partage. Cle combinee traitee en premier (replace_placeholders trie desc).
            "d’[valeur_nominale_action_lettres]": elision_de(
                _required_text(
                    selas.valeur_nominale_action_lettres,
                    "statuts_selas_multi.valeur_nominale_action_lettres",
                )
            ),
            "[valeur_nominale_action_lettres]": _required_text(
                selas.valeur_nominale_action_lettres,
                "statuts_selas_multi.valeur_nominale_action_lettres",
            ),
            "[adresse_siege]": self.adresse_siege,
            "[adresse_lieu_exercice]": _required_text(
                selas.adresse_lieu_exercice,
                "statuts_selas_multi.adresse_lieu_exercice",
            ),
            "[nom_banque]": _required_text(
                selas.banque_nom,
                "statuts_selas_multi.banque_nom",
            ),
            "[adresse_banque]": _required_text(
                selas.banque_adresse,
                "statuts_selas_multi.banque_adresse",
            ),
            "[date_cloture_premier_exercice]": _required_text(
                selas.date_cloture_premier_exercice,
                "statuts_selas_multi.date_cloture_premier_exercice",
            ),
            "[lieu_signature]": self.signature_lieu,
            "[date_signature]": self.signature_date,
        }


# --- Blocs dynamiques MEDECIN (wording reproduit A L'IDENTIQUE du modele medecin) -----------


def _add_comparution_block(document, data: _ResolvedSelasMulti) -> None:
    profession_pluriel = _required_text(
        data.selas.profession_reglementee_pluriel,
        "statuts_selas_multi.profession_reglementee_pluriel",
    )
    for associe in data.associes:
        if _is_morale(associe):
            _add_morale_comparution(document, associe)
        else:
            _add_physical_comparution(document, associe, profession_pluriel)


def _associe_est_feminin(associe: StatutsCivilsAssocie) -> bool:
    """Genre de l'associe pour l'accord des comparutions (retour Albane / audit
    2026-06-17 : « née » et « Inscrite » etaient figes au feminin -> un associe
    masculin sortait « née … Inscrite »). On prend `associe.genre` ; a defaut on
    derive de la civilite affichee (« Monsieur » -> masculin)."""
    if associe.genre is not None:
        return associe.genre == Gender.FEMININ
    civilite = (associe.civilite_affichage or "").strip().casefold().replace(".", "")
    return civilite in {"madame", "mme", "mademoiselle", "mlle"}


def _add_physical_comparution(
    document,
    associe: StatutsCivilsAssocie,
    profession_pluriel: str,
) -> None:
    feminin = _associe_est_feminin(associe)
    ne = "née" if feminin else "né"
    inscrit = "Inscrite" if feminin else "Inscrit"
    # Source para 16 : "[civilite] [prenoms] [nom], [profession] [qualif], ne(e) le [date] a
    # [ville] ([dep]), de nationalite [nat], demeurant [adresse], [situation]."
    add_paragraph(
        document,
        f"{_person_label(associe)}, "
        f"{_required_text(associe.profession, 'associes[].profession')} "
        f"{_required_text(associe.qualification_principale, 'associes[].qualification_principale')}"
        ", "
        f"{ne} le {_format_display_date(associe.date_naissance, 'associes[].date_naissance')} "
        f"à {_required_text(associe.ville_naissance, 'associes[].ville_naissance')} "
        f"({_required_text(associe.departement_naissance, 'associes[].departement_naissance')}), "
        f"de nationalité {_required_text(associe.nationalite, 'associes[].nationalite')}, "
        f"demeurant {_person_address(associe)}, "
        f"{_required_text(associe.situation_maritale, 'associes[].situation_maritale')}.",
    )
    # Source para 17 : "Inscrit(e) au tableau du conseil de l'ordre des [profession_pluriel] du
    # [ordre_dep] sous le numero departemental [numero_ordre], et sous le numero RPPS [rpps]."
    add_paragraph(
        document,
        f"{inscrit} au tableau du conseil de l’ordre des "
        f"{profession_pluriel} "
        f"du {_required_text(associe.ordre_departemental, 'associes[].ordre_departemental')} "
        "sous le numéro départemental "
        f"{_required_text(associe.numero_ordre, 'associes[].numero_ordre')}, "
        "et sous le numéro RPPS "
        f"{_required_text(associe.numero_rpps, 'associes[].numero_rpps')}.",
    )


def _add_morale_comparution(document, associe: StatutsCivilsAssocie) -> None:
    # Source para 19 : "La [denomination], [forme_sociale], au capital de [capital] euros dont le
    # siege social est situe au [adresse], immatriculee au RCS de [ville_rcs] sous le numero
    # [numero_rcs], representee par son representant legal, [civilite] [prenoms] [nom]."
    representant = associe.representant
    if representant is None:
        raise ValueError(
            f"associes[].representant est obligatoire pour une personne morale {DOCUMENT_CODE}."
        )
    rep_civilite = _required_text(
        representant.civilite_affichage, "associes[].representant.civilite_affichage"
    )
    add_paragraph(
        document,
        f"La {_required_text(associe.denomination, 'associes[].denomination')}, "
        f"{_required_text(associe.forme_juridique, 'associes[].forme_juridique')}, "
        "au capital de "
        f"{_required_text(associe.capital_social, 'associes[].capital_social')} euros "
        f"dont le siège social est situé au {_address_display(associe.siege, 'associes[].siege')}, "
        f"immatriculée au RCS de {_required_text(associe.ville_rcs, 'associes[].ville_rcs')} "
        f"sous le numéro {_required_text(associe.numero_rcs, 'associes[].numero_rcs')}, "
        "représentée par son représentant légal, "
        f"{rep_civilite} "
        f"{_required_text(representant.prenom, 'associes[].representant.prenom')} "
        f"{_required_text(representant.nom, 'associes[].representant.nom')}.",
    )


def _add_apports_block(document, data: _ResolvedSelasMulti) -> None:
    for associe in data.associes:
        apport = associe.apport
        if apport is None:
            raise ValueError(f"associes[].apport est obligatoire pour {DOCUMENT_CODE}.")
        montant = _required_text(apport.montant, "associes[].apport.montant")
        montant_lettres = _required_text(
            apport.montant_lettres, "associes[].apport.montant_lettres"
        )
        if _is_morale(associe):
            # Source para 73 : "La [denomination], apporte a la societe la somme de [lettres]
            # ([montant]) euros." (point final present pour la personne morale).
            add_paragraph(
                document,
                f"La {_required_text(associe.denomination, 'associes[].denomination')}, "
                f"apporte à la société la somme de {montant_lettres} ({montant}) euros.",
            )
        else:
            # Source para 72 : "[civilite] [prenoms] [nom], apporte a la societe la somme de
            # [lettres] ([montant]) euros" (pas de point final pour la personne physique).
            add_paragraph(
                document,
                f"{_person_label(associe)}, apporte à la société la somme de "
                f"{montant_lettres} ({montant}) euros",
            )


def _add_capital_block(document, data: _ResolvedSelasMulti) -> None:
    for associe in data.associes:
        nb_actions = _required_int(associe.nb_actions, "associes[].nb_actions")
        nb_actions_lettres = _required_text(
            associe.nb_actions_lettres, "associes[].nb_actions_lettres"
        )
        qualite = _required_text(associe.qualite_capital, "associes[].qualite_capital")
        if _is_morale(associe):
            # Source para 92 : "La [denomination], [qualite], detient [lettres] actions\t\t".
            add_paragraph(
                document,
                f"La {_required_text(associe.denomination, 'associes[].denomination')}, "
                f"{qualite}, détient {nb_actions_lettres} actions\t\t",
            )
        else:
            # Source para 88 : "[civilite] [prenoms] [nom], [qualite], detient [lettres] actions ".
            add_paragraph(
                document,
                f"{_person_label(associe)}, {qualite}, détient {nb_actions_lettres} actions ",
            )
        # Source paras 89 / 93 : "Ci\t\t\t\t\t\t\t\t\t\t[nb] actions" (dix tabulations).
        add_paragraph(document, f"Ci\t\t\t\t\t\t\t\t\t\t{nb_actions} actions")


def _add_president_block(document, data: _ResolvedSelasMulti) -> None:
    president = data.president
    # Source para 221 : "[civilite] [prenoms] [nom]" puis para 222 : "Demeurant [adresse].".
    add_paragraph(document, _person_label(president))
    add_paragraph(document, f"Demeurant {_person_address(president)}.")


def _add_signature_line(document, data: _ResolvedSelasMulti) -> None:
    # Source para 510 : "[prenoms_personne_1] [nom_personne_1]\t\t\t\t\t\t[denomination_associe_1]".
    # Generalise N : on aligne les etiquettes courtes des signataires separees par six
    # tabulations, dans l'ordre des associes (physique = prenoms + nom ; morale = denomination).
    labels = [_signature_short_label(a) for a in data.associes if a.est_signataire]
    add_statuts_signature_block(document, ["\t\t\t\t\t\t".join(labels)])


# --- Blocs dynamiques DENTISTE (wording reproduit A L'IDENTIQUE du modele dentiste) ---------
#
# Le modele dentiste (Statuts_SELAS_dentiste_pluri_modele.docx, 549 paras, 0 table) porte des
# valeurs concretes d'exemple dupliquees une fois par associe ("gabarit a repeter"). On les
# reinjecte par fenetre d'index, avec le wording propre au corpus dentiste :
#   - comparution : Article 0 (15-23), une SEULE ligne combinee par associe ;
#   - apports     : Article 6 (71-78), "- Le Docteur X, apporte [LETTRES] euros" + "Ci ... euros",
#                   puis trait "___________", puis "Total des apports ... [total] euros" ;
#   - capital     : Article 6 (83-89), "- [civilite] X, [LETTRES] actions" + "Ci ... actions",
#                   puis ligne tabulee vide, puis "Total des actions composant le capital ...".
#   - signature   : "Fait a [lieu]" + "Le [date]" + ligne de noms tabulee.
# Pas de bloc de designation NOMINATIVE du President : l'article President (Art. 19) est
# entierement generique dans le corpus dentiste (le president n'y est jamais nomme).


def _add_comparution_block_dentiste(document, data: _ResolvedSelasMulti) -> None:
    profession = _required_text(
        data.selas.profession_reglementee,
        "statuts_selas_multi.profession_reglementee",
    )
    profession_pluriel = _required_text(
        data.selas.profession_reglementee_pluriel,
        "statuts_selas_multi.profession_reglementee_pluriel",
    )
    for associe in data.associes:
        if _is_morale(associe):
            _add_morale_comparution(document, associe)
        else:
            _add_physical_comparution_dentiste(document, associe, profession, profession_pluriel)


def _add_physical_comparution_dentiste(
    document,
    associe: StatutsCivilsAssocie,
    profession: str,
    profession_pluriel: str,
) -> None:
    # Source para 17 (UNE seule ligne combinee, corpus dentiste) :
    # "[civilite] [prenoms] [nom], [profession], de nationalite [nat], ne(e) le [date] a
    #  [ville] ([dep]), [situation], demeurant [adresse], inscrit(e) au tableau de l'Ordre des
    #  [profession_pluriel] de [ordre_dep] sous le numero national [numero_ordre] et sous le
    #  numero RPPS [rpps]."
    # Differences wording vs medecin : "inscrit au tableau DE L'ORDRE DES [pluriel]" (et non
    # "du conseil de l'ordre"), "numero NATIONAL" (et non "departemental").
    feminin = _associe_est_feminin(associe)
    ne = "née" if feminin else "né"
    inscrit = "inscrite" if feminin else "inscrit"
    add_paragraph(
        document,
        f"{_person_label(associe)}, "
        f"{profession}, "
        f"de nationalité {_required_text(associe.nationalite, 'associes[].nationalite')}, "
        f"{ne} le {_format_display_date(associe.date_naissance, 'associes[].date_naissance')} "
        f"à {_required_text(associe.ville_naissance, 'associes[].ville_naissance')} "
        f"({_required_text(associe.departement_naissance, 'associes[].departement_naissance')}), "
        f"{_required_text(associe.situation_maritale, 'associes[].situation_maritale')}, "
        f"demeurant {_person_address(associe)}, "
        f"{inscrit} au tableau de l’Ordre des {profession_pluriel} "
        f"de {_required_text(associe.ordre_departemental, 'associes[].ordre_departemental')} "
        "sous le numéro national "
        f"{_required_text(associe.numero_ordre, 'associes[].numero_ordre')} "
        f"et sous le numéro RPPS {_required_text(associe.numero_rpps, 'associes[].numero_rpps')}.",
    )


def _add_apports_block_dentiste(document, data: _ResolvedSelasMulti) -> None:
    capital_social = _required_text(
        data.selas.capital_social, "statuts_selas_multi.capital_social"
    )
    for associe in data.associes:
        apport = associe.apport
        if apport is None:
            raise ValueError(f"associes[].apport est obligatoire pour {DOCUMENT_CODE}.")
        montant = _required_text(apport.montant, "associes[].apport.montant")
        montant_lettres = _required_text(
            apport.montant_lettres, "associes[].apport.montant_lettres"
        )
        if _is_morale(associe):
            # Variante personne morale : "- La [denomination], apporte [LETTRES] euros".
            add_paragraph(
                document,
                f"- La {_required_text(associe.denomination, 'associes[].denomination')}, "
                f"apporte {montant_lettres} euros ",
            )
        else:
            # Source para 71 : "- Le Docteur [prenoms] [nom], apporte [LETTRES] euros ".
            add_paragraph(
                document,
                f"- {_apporteur_label_dentiste(associe)}, apporte {montant_lettres} euros ",
            )
        # Source para 72 : "Ci\t...\t[montant] euros" (onze tabulations).
        add_paragraph(document, f"Ci\t\t\t\t\t\t\t\t\t\t\t{montant} euros")
    # Source para 76 : trait separateur "\t...\t___________" (onze tabulations).
    add_paragraph(document, "\t\t\t\t\t\t\t\t\t\t\t___________")
    add_paragraph(document, "")
    # Source para 78 : "Total des apports\t...\t[total] euros" (neuf tabulations).
    add_paragraph(document, f"Total des apports\t\t\t\t\t\t\t\t\t{capital_social} euros")


def _add_capital_block_dentiste(document, data: _ResolvedSelasMulti) -> None:
    nb_actions_total = _required_int(
        data.selas.nb_actions_total, "statuts_selas_multi.nb_actions_total"
    )
    for associe in data.associes:
        nb_actions = _required_int(associe.nb_actions, "associes[].nb_actions")
        nb_actions_lettres = _required_text(
            associe.nb_actions_lettres, "associes[].nb_actions_lettres"
        )
        if _is_morale(associe):
            # Variante personne morale : "- La [denomination], [LETTRES] actions".
            add_paragraph(
                document,
                f"- La {_required_text(associe.denomination, 'associes[].denomination')}, "
                f"{nb_actions_lettres} actions ",
            )
        else:
            # Source para 83 : "- [civilite] [prenoms] [nom], [LETTRES] actions ".
            add_paragraph(document, f"- {_person_label(associe)}, {nb_actions_lettres} actions ")
        # Source para 84 : "Ci\t...\t[nb] actions" (onze tabulations).
        add_paragraph(document, f"Ci\t\t\t\t\t\t\t\t\t\t\t{nb_actions} actions")
    # Source para 88 : ligne de tabulations seule (onze tabulations).
    add_paragraph(document, "\t\t\t\t\t\t\t\t\t\t\t")
    # Source para 89 : "Total des actions composant le capital social\xa0: \t...\t[total] actions".
    add_paragraph(
        document,
        f"Total des actions composant le capital social\xa0: \t\t\t\t\t{nb_actions_total} actions",
    )


def _add_signature_line_dentiste(document, data: _ResolvedSelasMulti) -> None:
    # Source paras 507-512 : "Fait a [lieu]" / "Le [date]" / (espace) / ligne de noms tabulee.
    add_paragraph(document, f"Fait à {data.signature_lieu}")
    add_paragraph(document, f"Le {data.signature_date}")
    add_paragraph(document, "")
    add_paragraph(document, "\t\t")
    labels = [_signature_short_label(a) for a in data.associes if a.est_signataire]
    add_statuts_signature_block(document, ["\t\t\t\t".join(labels)])


def _dentiste_boilerplate_replacements(data: _ResolvedSelasMulti) -> dict[str, str]:
    """Le corpus dentiste porte des valeurs CONCRETES d'exemple dans son boilerplate (la ou le
    corpus medecin porte des placeholders). On mappe chaque ligne-exemple EXACTE du modele vers
    sa version remplie avec les donnees reelles de la societe. Strings prouvees par extraction
    (paras 39 / 55 / 79 / 81 du modele dentiste)."""
    selas = data.selas
    capital_social = _required_text(selas.capital_social, "statuts_selas_multi.capital_social")
    capital_lettres = _required_text(
        selas.capital_social_lettres, "statuts_selas_multi.capital_social_lettres"
    )
    nb_actions = str(
        _required_int(selas.nb_actions_total, "statuts_selas_multi.nb_actions_total")
    )
    valeur_nominale = _required_text(
        selas.valeur_nominale_action, "statuts_selas_multi.valeur_nominale_action"
    )
    valeur_nominale_lettres = _required_text(
        selas.valeur_nominale_action_lettres,
        "statuts_selas_multi.valeur_nominale_action_lettres",
    )
    banque_nom = _required_text(selas.banque_nom, "statuts_selas_multi.banque_nom")
    banque_adresse = _required_text(selas.banque_adresse, "statuts_selas_multi.banque_adresse")
    return {
        # Para 39 : denomination.
        "La société est dénommée « Cabinet Dentaire Fuchs & Associés »,": (
            f"La société est dénommée « {data.denomination} »,"
        ),
        # Para 55 : siege social.
        "Le siège de la société est fixé au 9 rue du Général Chassereau, "
        "35470 BAIN DE BRETAGNE.": (
            f"Le siège de la société est fixé au {data.adresse_siege}."
        ),
        # Para 79 : depot des fonds (banque).
        "Cette somme a été déposée au crédit du compte ouvert dans les livres de la "
        "Banque BPGO, 8 place du parlement de Bretagne, 35000 Rennes.": (
            "Cette somme a été déposée au crédit du compte ouvert dans les livres de la "
            f"Banque {banque_nom}, {banque_adresse}."
        ),
        # Para 81 : ligne capital social (figure + lettres, nb actions, valeur nominale).
        # NB : la boucle applique les replacements sur paragraph.text.STRIP() ; l'espace final
        # apres "\xa0:" du modele disparait -> la cle doit finir par "suit\xa0:" (sans espace).
        "Le capital social est fixé à la somme de 1.020 € (MILLE VINGT) euros divisé en "
        "102.000 actions de 0,01 € (UN CENTIME D’EURO) chacune, entièrement libéré et "
        "attribué comme suit\xa0:": (
            f"Le capital social est fixé à la somme de {capital_social} € ({capital_lettres}) "
            f"euros divisé en {nb_actions} actions de {valeur_nominale} € "
            f"({valeur_nominale_lettres}) chacune, entièrement libéré et attribué comme "
            "suit\xa0:"
        ),
    }


def _apporteur_label_dentiste(associe: StatutsCivilsAssocie) -> str:
    # Corpus dentiste : l'apporteur personne physique est designe "Le Docteur [prenoms] [nom]".
    prenoms = associe.prenoms or associe.prenom
    return (
        f"Le Docteur {_required_text(prenoms, 'associes[].prenoms')} "
        f"{_required_text(associe.nom, 'associes[].nom')}"
    )


_MEDECIN_PROFILE = _SelasProfile(
    source_name=SOURCE_NAME,
    comparution_slice=COMPARUTION_SLICE,
    apports_slice=APPORTS_SLICE,
    capital_slice=CAPITAL_SLICE,
    president_slice=PRESIDENT_SLICE,
    signature_slice=SIGNATURE_SLICE,
    add_comparution=_add_comparution_block,
    add_apports=_add_apports_block,
    add_capital=_add_capital_block,
    add_president=_add_president_block,
    add_signature=_add_signature_line,
    title_box_before=STATUTS_TITLE_BOX_BEFORE,
)

# Fenetres d'index DENTISTE — prouvees par extraction du modele
# Statuts_SELAS_dentiste_pluri_modele.docx (549 paras) :
#   comparution : paras 17 + 20 (gabarit duplique 2 associes) -> fenetre (17, 21)
#   apports     : paras 71-78 (apports + Ci + trait + total) -> fenetre (71, 79)
#   capital     : paras 83-89 (repartition + Ci + ligne tab + total) -> fenetre (83, 90)
#   signature   : paras 507-512 ("Fait a" + date + ligne noms) -> fenetre (507, 513)
# Pas de president_slice ni de title_box (0 table dans le modele dentiste).
_DENTISTE_PROFILE = _SelasProfile(
    source_name="Statuts_SELAS_dentiste_pluri_modele.docx",
    comparution_slice=(17, 21),
    apports_slice=(71, 79),
    capital_slice=(83, 90),
    president_slice=None,
    signature_slice=(507, 513),
    add_comparution=_add_comparution_block_dentiste,
    add_apports=_add_apports_block_dentiste,
    add_capital=_add_capital_block_dentiste,
    add_president=None,
    add_signature=_add_signature_line_dentiste,
    # N6 (Rafael 2026-06-24) : en-tete « STATUTS » manquant sur le dentiste pluri (parite medecin).
    # Le modele dentiste n'a pas de titre encadre en table -> on le restaure avant « Les
    # soussignes, » (index 15), comme le medecin l'insere avant son « LES SOUSSIGNEES » (index 14).
    title_box_before=15,
    boilerplate_replacements=_dentiste_boilerplate_replacements,
)


# --- Resolution / validation ---


def _validate_associes(
    associes: list[StatutsCivilsAssocie],
    selas: StatutsSelasMultiContext,
) -> None:
    if len(associes) < MIN_ASSOCIES:
        raise ValueError(
            f"la SELAS multi requiert au moins {MIN_ASSOCIES} associes pour {DOCUMENT_CODE}."
        )
    if len(associes) > MAX_ASSOCIES:
        raise ValueError(
            f"la SELAS multi est limitee a {MAX_ASSOCIES} associes pour {DOCUMENT_CODE}."
        )
    physiques = [a for a in associes if not _is_morale(a)]
    if not physiques:
        raise ValueError(
            "au moins un associe personne physique exercant est obligatoire "
            f"pour {DOCUMENT_CODE}."
        )
    total_actions = sum(_required_int(a.nb_actions, "associes[].nb_actions") for a in associes)
    expected_actions = _required_int(selas.nb_actions_total, "statuts_selas_multi.nb_actions_total")
    if total_actions != expected_actions:
        raise ValueError(
            "la somme des actions des associes doit correspondre a "
            f"statuts_selas_multi.nb_actions_total pour {DOCUMENT_CODE}."
        )


def _resolve_president(
    associes: list[StatutsCivilsAssocie],
    president: StatutsSelasMultiPresident | None,
) -> StatutsCivilsAssocie:
    physiques = [a for a in associes if not _is_morale(a)]
    if president is None:
        return physiques[0]
    if president.ref_associe_index is not None:
        if not 0 <= president.ref_associe_index < len(associes):
            raise ValueError(
                "statuts_selas_multi.president.ref_associe_index hors bornes "
                f"pour {DOCUMENT_CODE}."
            )
        candidate = associes[president.ref_associe_index]
        if _is_morale(candidate):
            raise ValueError(
                "le President SELAS doit etre une personne physique exercante "
                f"pour {DOCUMENT_CODE}."
            )
        return candidate
    if president.nom:
        for associe in physiques:
            associe_prenoms = associe.prenoms or associe.prenom
            if associe.nom == president.nom and (
                president.prenoms is None or associe_prenoms == president.prenoms
            ):
                return associe
        raise ValueError(
            "statuts_selas_multi.president ne correspond a aucun associe physique "
            f"pour {DOCUMENT_CODE}."
        )
    return physiques[0]


# --- Helpers ---


def _source_path(source_name: str) -> Path:
    path = Path("project/source_documents/lot_04") / source_name
    if not path.exists():
        raise ValueError(f"source DOCX introuvable pour {DOCUMENT_CODE}: {path}")
    return path


def _add_rendered_paragraph(document, text: str) -> None:
    if text == "STATUTS":
        add_statuts_title_box(document, text)
    elif text.startswith("TITRE "):
        add_statuts_part_heading(document, text)
    elif text.startswith("ARTICLE ") or text.startswith("Article "):
        add_statuts_article_heading(document, text, left_indent_cm=0.25)
    elif text.startswith("- "):
        add_statuts_hanging_list_item(document, text[2:])
    elif text.startswith("-\t"):
        add_statuts_hanging_list_item(document, text[2:])
    else:
        add_statuts_body_paragraph(document, text)


def _is_tiret_list_paragraph(paragraph: object) -> bool:
    """Vrai si le paragraphe SOURCE est une puce a tiret (style « Tirets (-) document »).

    N6 (Rafael 2026-06-24) : le tiret de ces listes est porte par le numbering Word (numId=7),
    pas par .text ; on le detecte par le nom de style pour re-prefixer « - » et le rendre en
    hanging list item. Couvre toutes les listes a tirets (art.1, 14, 16, 21...), pas que l'art.1."""
    style = getattr(paragraph, "style", None)
    if style is None:
        return False
    name = getattr(style, "name", None) or ""
    return "tiret" in name.lower()


def _replace_placeholders(text: str, replacements: dict[str, str]) -> str:
    rendered = text
    # Tokens les plus LONGS d'abord : la cle combinee « d’[valeur…] » (elision art.8, Akainu B1)
    # doit etre traitee AVANT le token nu « [valeur…] » qu'elle contient.
    for placeholder in sorted(replacements, key=len, reverse=True):
        rendered = rendered.replace(placeholder, replacements[placeholder])
    return rendered


def _person_label(associe: StatutsCivilsAssocie) -> str:
    prenoms = associe.prenoms or associe.prenom
    return (
        f"{_required_text(associe.civilite_affichage, 'associes[].civilite_affichage')} "
        f"{_required_text(prenoms, 'associes[].prenoms')} "
        f"{_required_text(associe.nom, 'associes[].nom')}"
    )


def _signature_short_label(associe: StatutsCivilsAssocie) -> str:
    if _is_morale(associe):
        return _required_text(associe.denomination, "associes[].denomination")
    prenoms = associe.prenoms or associe.prenom
    return (
        f"{_required_text(prenoms, 'associes[].prenoms')} "
        f"{_required_text(associe.nom, 'associes[].nom')}"
    )


def _person_address(associe: StatutsCivilsAssocie) -> str:
    if associe.adresse_personnelle_affichee:
        return associe.adresse_personnelle_affichee.strip()
    return _address_display(associe.adresse_personnelle, "associes[].adresse_personnelle")


def _is_morale(associe: StatutsCivilsAssocie) -> bool:
    return associe.type_personne == "personne_morale"


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return str(value).strip()


def _required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return _required_text(value, field_name)


def _address_display(address: Address | None, field_name: str) -> str:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{_required_text(address.num_voie, f'{field_name}.num_voie')} "
        f"{_required_text(address.voie, f'{field_name}.voie')} - "
        f"{_required_text(address.cp, f'{field_name}.cp')} "
        f"{_required_text(address.ville, f'{field_name}.ville')}"
    )
