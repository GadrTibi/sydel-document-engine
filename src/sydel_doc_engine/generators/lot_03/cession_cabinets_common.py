# ruff: noqa: E501

from __future__ import annotations

import glob
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from docx import Document
from docx.oxml.ns import qn

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    CessionAcquereur,
    CessionBailProfessionnel,
    CessionCabinet,
    CessionConjoint,
    CessionContext,
    CessionCreditVendeur,
    CessionExercice,
    CessionFinancement,
    CessionPret,
    CessionPrix,
    CessionRepresentant,
    CessionSalarie,
    CessionValidations,
    CessionVendeur,
    DocumentContext,
    DocumentGenerationContext,
)
from sydel_doc_engine.utils.grammar import apply_gender_pairs

DOCUMENT_CODE = "CODE-CESSION-CAB-001"

ACTE = "acte"
COMPROMIS = "compromis"
MEDICAL = "medical"
DENTAIRE = "dentaire"
SUPPORTED_STRUCTURES = {"SELARL", "SELAS"}
SUPPORTED_ETAPES = {ACTE, COMPROMIS}
SUPPORTED_CABINET_TYPES = {MEDICAL, DENTAIRE}

# Origine de propriete (regle NotebookLM) : la clause decrit le VENDEUR (cedant),
# comment il est devenu proprietaire. Deux variantes standard ; defaut = "cree"
# si le praticien n'a pas achete son cabinet. Tout autre cas = COMPLEXE -> texte
# libre saisi a la main + validation explicite (souplesse / relecture humaine).
ORIGINE_MODE_CREE = "cree"
ORIGINE_MODE_ACHETE = "achete"
SUPPORTED_ORIGINE_MODES = {ORIGINE_MODE_CREE, ORIGINE_MODE_ACHETE}

# Convention systeme : une liste vide (0 element) se rend "Néant", a l'image des
# apports en nature inexistants. Utilisee pour la reprise des salaries (0/1/N).
NEANT = "Néant."

# Nombre de pages (en lettres) du modele, par variante (retours 9.9).
# Le front fournissait une constante unique « vingt » pour TOUS les docs de
# cession, fausse pour le compromis (~8 pages). python-docx n'ayant pas de
# moteur de pagination, on ne peut PAS compter les pages a l'execution : on fige
# donc la longueur connue de chaque modele, source deterministe et fidele. Une
# variante non mappee retombe sur la valeur fournie par le contexte.
_PAGES_LETTRES_BY_VARIANT: dict[tuple[str, str], str] = {
    (COMPROMIS, DENTAIRE): "huit",
    (COMPROMIS, MEDICAL): "huit",
}

# Dossier des modeles Word tokenises, resolu independamment du cwd.
# parents[4] depuis src/sydel_doc_engine/generators/lot_03/ = racine du repo.
_SOURCE_MODELS_DIR = (
    Path(__file__).resolve().parents[4] / "project" / "source_documents" / "lot_03"
)

# Motif glob par variante (etape, type_cabinet) -> motif robuste aux accents/apostrophes.
_MODEL_GLOB_BY_VARIANT: dict[tuple[str, str], str] = {
    (ACTE, MEDICAL): "Acte*cession*m*dical*.docx",
    (ACTE, DENTAIRE): "Acte*cession*dentaire*.docx",
    (COMPROMIS, MEDICAL): "Compromis*cession*m*dical*.docx",
    (COMPROMIS, DENTAIRE): "Compromis*cession*dentaire*.docx",
}

# Mois francais accentues pour un rendu fidele "10 mars 1975".
_MONTHS_FR = (
    "",
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)

_ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_TOKEN_RE = re.compile(r"\[[^\]\[]+\]")


@dataclass(frozen=True)
class CessionCabinetVariant:
    etape: Literal["acte", "compromis"]
    type_cabinet: Literal["medical", "dentaire"]
    output_filename: str


def generate_cession_cabinet_docx(
    ctx: DocumentGenerationContext,
    output_dir: Path,
    variant: CessionCabinetVariant,
) -> Path:
    # Validation metier conservee (regles credit-vendeur / SCM = acte medical uniquement, etc.).
    _validate_context(ctx, variant)
    model_path = _resolve_model_path(variant)
    replacements = _build_cession_replacements(ctx, variant)
    gender_pairs = _build_cession_gender_pairs(ctx)
    output_path = output_dir / variant.output_filename
    return render_cession_from_template(
        model_path,
        replacements,
        output_path,
        gender_pairs=gender_pairs,
        paragraph_overrides=_build_paragraph_overrides(ctx, variant),
        segment_overrides=_build_segment_overrides(ctx),
        line_fixes=_build_line_fixes(ctx, variant),
    )


# Titre civil (M./Mme) derive du genre, pour les emplacements ou un titre
# professionnel « Docteur » n'a pas sa place (retours 9.2 : la societe est
# representee par « M./Mme », jamais « Dr »).
_CIVIL_TITLE_BY_GENDER = {
    Gender.MASCULIN: "M.",
    Gender.FEMININ: "Mme",
}


def _civil_title(genre: Gender | None) -> str | None:
    if genre is None:
        return None
    return _CIVIL_TITLE_BY_GENDER.get(genre)


@dataclass(frozen=True)
class _LineFix:
    """Correctif de PARAGRAPHE ancre, applique APRES le remplissage des tokens.

    `anchor` : sous-chaine litterale identifiant le paragraphe cible.
    `pattern` : regex appliquee au texte du paragraphe (apres tokens + genre).
    `replacement` : remplacement (groupes regex autorises).
    """

    anchor: str
    pattern: re.Pattern[str]
    replacement: str


def _build_line_fixes(
    ctx: DocumentGenerationContext,
    variant: CessionCabinetVariant,
) -> list[_LineFix]:
    """Correctifs post-remplissage des modeles de cession (retours 9.2).

    9.2 — « Représentée par son <fonction>, ... » : le modele COMPROMIS dentaire
    pointe le VENDEUR (mauvaise personne) et le compromis affiche « Docteur ». On
    reecrit l'identite du representant de la societe avec un titre CIVIL (M./Mme).
    Perimetre = compromis (cible du ticket) ; l'acte n'est pas touche.

    (Le bloc signature 9.8 est traite en amont, au niveau des tokens
    [signature_acquereur]/[signature_vendeur] dans _build_cession_replacements.)
    """
    fixes: list[_LineFix] = []
    cession = ctx.cession
    if cession is None or variant.etape != COMPROMIS:
        return fixes

    acquereur = cession.acquereur or CessionAcquereur()
    representant = acquereur.representant or CessionRepresentant()

    # --- 9.2 : identite du representant dans « Représentée par son/sa ... » ---
    civil = _civil_title(representant.genre)
    rep_identity = _person_label(civil, representant.prenom, representant.nom)
    if rep_identity:
        # Reecrit ce qui suit « Représentée par sa/son <fonction>, » jusqu'a la
        # virgule precedant « domicilié(e) en cette qualité ». Insensible a la
        # personne erronee (vendeur) ou au titre (Docteur) du modele source.
        fixes.append(
            _LineFix(
                anchor="Représentée par s",
                pattern=re.compile(r"(Représentée par s(?:on|a) [^,]+, ).+?(, domicilié)"),
                replacement=rf"\g<1>{rep_identity.replace(chr(92), chr(92) * 2)}\g<2>",
            )
        )

    return fixes


def _societe_signature_label(
    acquereur: CessionAcquereur,
    representant: CessionRepresentant,
) -> str | None:
    """Libelle de signature de la SOCIETE acquereur (retours 9.8).

    Forme : « Pour la <forme> <denomination>, <fonction> <M./Mme Prenom Nom> ».
    La societe signe via son representant ; titre CIVIL (M./Mme), pas « Docteur ».
    """
    denomination = (acquereur.denomination_societe or "").strip()
    if not denomination:
        return None
    forme = (acquereur.forme_sociale or "").strip()
    # Eviter « Pour la SELARL SELARL CABINET ... » : la denomination saisie
    # contient souvent deja la forme sociale en prefixe. On ne re-prefixe la
    # forme que si elle n'est pas deja en tete de la denomination.
    if forme and denomination.upper().startswith(forme.upper()):
        entete = f"Pour la {denomination}"
    else:
        entete = f"Pour la {forme} {denomination}" if forme else f"Pour la {denomination}"
    entete = re.sub(r"\s+", " ", entete).strip()

    civil = _civil_title(representant.genre)
    rep_identity = _person_label(civil, representant.prenom, representant.nom)
    fonction = (representant.fonction or "").strip()
    if rep_identity and fonction:
        return f"{entete}, {fonction} {rep_identity}"
    if rep_identity:
        return f"{entete}, {rep_identity}"
    return entete


# Segments matrimoniaux EXACTS des modeles (chaines figees relevees dans
# project/source_documents/lot_03/). Quand le vendeur n'est PAS marie, le
# segment complet « ... sous le regime de ... avec ... » est remplace par la
# seule situation maritale : aucune phrase incomplete (retours client
# 2026-06-11). Vendeur marie -> tokens remplis normalement.
_VENDEUR_MARITAL_SEGMENTS: tuple[str, ...] = (
    (
        "[situation_maritale_vendeur] sous le régime de [regime_matrimonial_vendeur] "
        "avec [civilite_conjoint_vendeur] [prenom_conjoint_vendeur] [nom_conjoint_vendeur]."
    ),
    (
        "[situation_maritale_vendeur] à [prenom_conjoint_vendeur] [nom_conjoint_vendeur], "
        "sous le régime de [regime_matrimonial_vendeur]."
    ),
    (
        "[situation_maritale_vendeur] avec [civilite_conjoint_vendeur] "
        "[prenom_conjoint_vendeur] [nom_conjoint_vendeur], sous le régime de "
        "[regime_matrimonial_vendeur], sans contrat de mariage."
    ),
)


def _build_segment_overrides(ctx: DocumentGenerationContext) -> dict[str, str]:
    cession = ctx.cession
    if cession is None:
        return {}
    vendeur = cession.vendeur or CessionVendeur()
    situation = (vendeur.situation_maritale or "").strip()
    normalized = situation.casefold()
    if not situation or normalized.startswith("mari"):
        return {}
    return {segment: f"{situation}." for segment in _VENDEUR_MARITAL_SEGMENTS}


def _build_paragraph_overrides(
    ctx: DocumentGenerationContext,
    variant: CessionCabinetVariant,
) -> dict[str, str | None]:
    """Surcharges PARAGRAPHE entier, pilotees par token ancre (retours client 2026-06-11).

    token -> texte : le paragraphe contenant le token est remplace par ce texte ;
    token -> None : le paragraphe est supprime (aucune phrase incomplete).
    - « Les locaux sont composes d'une piece de [superficie_local]... » : la phrase
      figee est remplacee par le descriptif libre du local s'il est saisi, sinon
      supprimee (ticket 2.5 : jamais de phrase automatique imposee).
    - [clause_reprise_salaries] (acte dentaire) : 0 salarie -> la phrase relative
      aux salaries est supprimee du document (ticket 2.12/3.3 ; remplace la
      convention « Neant » anterieure).
    """
    overrides: dict[str, str | None] = {}
    cession = ctx.cession
    if cession is None:
        return overrides
    bail = cession.bail_professionnel or CessionBailProfessionnel()
    cabinet = cession.cabinet or CessionCabinet()
    descriptif = (bail.descriptif_local or "").strip()
    superficie = (cabinet.superficie_local or "").strip()
    if descriptif:
        overrides["[superficie_local]"] = descriptif
    elif not superficie:
        # Ni descriptif libre ni superficie : la phrase figee est supprimee.
        # Une superficie renseignee (scenarios existants) conserve la phrase du
        # modele avec le token remplace.
        overrides["[superficie_local]"] = None
    if variant.etape == ACTE and variant.type_cabinet == DENTAIRE and not cession.salaries:
        overrides["[clause_reprise_salaries]"] = None
    if variant.etape == ACTE and variant.type_cabinet == MEDICAL:
        # Pas de reprise de parts SCM -> la clause « De ceder les [...] parts
        # sociales ... SCM » (paragraphe unique, ancre par token) est supprimee.
        if cession.scm is None or not cession.scm.actif:
            overrides["[nb_parts_scm_a_ceder]"] = None
    return overrides


# Paires d'accord en genre des modeles de cession, pilotees par la BONNE personne.
# Chaines EXACTES figees relevees dans project/source_documents/lot_03/ :
#  - Acte dentaire : fige au FEMININ ("née le", "Inscrite au tableau",
#    "domiciliée en cette qualité").
#  - Compromis dentaire / medical : fige au MASCULIN ("né le", "inscrit au tableau",
#    "domicilié en cette qualité").
#  - Acte medical : "né(e) le" inclusif (non touche : aucune paire ne le matche).
# JAMAIS de regex de terminaison : uniquement ces chaines litterales ancrees.
# "désigné" (role/invariant) et "Représentée" (la societe, toujours feminin) ne
# sont PAS dans les paires : on n'y touche pas.
_CESSION_VENDEUR_PAIRS: list[tuple[str, str]] = [
    ("né le ", "née le "),
    ("Inscrit au tableau", "Inscrite au tableau"),
    ("inscrit au tableau", "inscrite au tableau"),
]
_CESSION_REPRESENTANT_PAIRS: list[tuple[str, str]] = [
    ("domicilié en cette qualité", "domiciliée en cette qualité"),
]


def _build_cession_gender_pairs(
    ctx: DocumentGenerationContext,
) -> list[tuple[Gender, list[tuple[str, str]]]]:
    """Construit les couples (genre, paires) d'accord pour la cession.

    Le genre vendeur pilote l'identification (« né le », « inscrit au tableau »).
    Le genre du representant de l'acquereur pilote « domicilié en cette qualite ».
    Un genre absent (None, non capture cote front) -> on n'accorde pas cette
    personne et le modele source reste fige tel quel (pas de devinette).
    """
    pairs: list[tuple[Gender, list[tuple[str, str]]]] = []
    cession = ctx.cession
    if cession is None:
        return pairs
    vendeur = cession.vendeur
    if vendeur is not None and vendeur.genre is not None:
        pairs.append((vendeur.genre, _CESSION_VENDEUR_PAIRS))
    acquereur = cession.acquereur
    representant = acquereur.representant if acquereur is not None else None
    if representant is not None and representant.genre is not None:
        pairs.append((representant.genre, _CESSION_REPRESENTANT_PAIRS))
    return pairs


def render_cession_from_template(
    model_path: Path,
    replacements: dict[str, str],
    output_path: Path,
    *,
    gender_pairs: list[tuple[Gender, list[tuple[str, str]]]] | None = None,
    paragraph_overrides: dict[str, str | None] | None = None,
    segment_overrides: dict[str, str] | None = None,
    line_fixes: list[_LineFix] | None = None,
) -> Path:
    """Charge le modele tokenise et remplace chaque token [xxx] run par run.

    `segment_overrides` (optionnel) : remplacement de SEGMENTS exacts du modele
    (chaines litterales pouvant contenir plusieurs tokens) AVANT le remplacement
    token par token. Le paragraphe touche est reecrit sur son premier run.
    Utilise pour les clauses matrimoniales du vendeur non marie.

    `paragraph_overrides` (optionnel) : surcharges PARAGRAPHE entier appliquees
    AVANT le remplacement des tokens. Pour chaque token ancre present dans un
    paragraphe : valeur texte -> le paragraphe est reecrit avec ce texte (mise en
    forme du premier run conservee) ; valeur None -> le paragraphe est supprime.
    Permet les clauses « tout ou rien » (descriptif libre du local, phrase
    salaries) sans jamais laisser de phrase incomplete.

    `gender_pairs` (optionnel) : liste de couples `(genre, paires)` appliques
    APRES le remplacement des tokens et AVANT la securite anti-token-residuel,
    via `grammar.apply_gender_pairs` (corps des paragraphes + cellules de
    tableaux). Chaque entree accorde des chaines EXACTES figees du modele selon
    le `genre` de la BONNE personne (vendeur, representant...). C'est le
    generateur qui pilote les paires : aucune normalisation magique globale.

    `line_fixes` (optionnel) : correctifs regex de PARAGRAPHE appliques APRES le
    remplissage des tokens ET l'accord en genre (donc sur le texte final). Sert
    aux corrections qui ne peuvent pas etre portees par le modele source (lecture
    seule) — ex. 9.2 : l'identite du representant dans « Représentée par son... ».

    Securite anti-trou : si un token [...] subsiste apres remplacement, leve
    ValueError en listant les tokens residuels (un token oublie = un test rouge).
    """
    document = Document(str(model_path))

    # Retours Albane 9.3 : les modeles source embarquent des commentaires Word
    # (annotations de relecture). Ils sont strippes a la generation pour ne
    # jamais fuir dans le document client. No-op si le modele n'en porte pas.
    _strip_word_comments(document)

    if paragraph_overrides:
        _apply_paragraph_overrides(document, paragraph_overrides)
    if segment_overrides:
        _apply_segment_overrides(document, segment_overrides)

    for paragraph in _iter_all_paragraphs(document):
        for run in paragraph.runs:
            text = run.text
            had_token = "[" in text
            if had_token:
                for token, value in replacements.items():
                    if token in text:
                        text = text.replace(token, value)
                if text != run.text:
                    run.text = text
            # 9.1 : retirer le surlignage du modele d'un run REMPLI, sans jamais
            # toucher une zone encore a completer. Cas, par run :
            #  - run-token rempli par une vraie valeur (plus de token, texte non
            #    vide) -> de-surligne (champ complete) ;
            #  - run-token rendu VIDE (option non saisie) -> GARDE le jaune
            #    (zone a completer a la main, retours 9.1) ;
            #  - run statique surligne du modele (jamais de token : ponctuation,
            #    espace, texte fige) -> de-surligne (ce n'est pas un champ).
            still_has_token = "[" in run.text
            if not still_has_token and (run.text.strip() or not had_token):
                _clear_run_highlight(run)

    if gender_pairs:
        for paragraph in _iter_all_paragraphs(document):
            _apply_gender_pairs_to_paragraph(paragraph, gender_pairs)

    if line_fixes:
        for paragraph in _iter_all_paragraphs(document):
            _apply_line_fixes_to_paragraph(paragraph, line_fixes)

    residual = _collect_residual_tokens(document)
    if residual:
        joined = ", ".join(sorted(residual))
        raise ValueError(
            f"Tokens non remplaces dans {model_path.name} pour {DOCUMENT_CODE} : {joined}."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output_path))
    return output_path


def _iter_all_paragraphs(document):
    yield from document.paragraphs
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from cell.paragraphs


# Parts de commentaires Word a retirer du package une fois les references nettoyees.
_COMMENT_PART_SUFFIXES = (
    "comments.xml",
    "commentsExtended.xml",
    "commentsIds.xml",
    "commentsExtensible.xml",
)
# Elements de commentaire references DANS document.xml (corps + tableaux).
_COMMENT_BODY_TAGS = (
    "w:commentRangeStart",
    "w:commentRangeEnd",
    "w:commentReference",
)


def _clear_run_highlight(run) -> None:
    """Retire le surlignage (w:highlight) d'un run rempli (retours 9.1).

    Supprime l'element w:highlight de rPr s'il existe. No-op si le run n'est pas
    surligne. Manipulation XML directe : python-docx n'expose pas la suppression
    propre du highlight (poser AUTO laisserait un w:highlight w:val=\"none\").
    """
    rpr = run._element.find(qn("w:rPr"))
    if rpr is None:
        return
    for highlight in rpr.findall(qn("w:highlight")):
        rpr.remove(highlight)


def _strip_word_comments(document) -> None:
    """Supprime tout commentaire Word herite du modele source (retours 9.3).

    Deux passes complementaires, sinon le DOCX serait corrompu dans Word :
      1. retirer les elements de reference (commentRangeStart/End +
         le run d'ancrage portant commentReference) du document.xml ;
      2. supprimer les parts word/comments*.xml + leurs relations.
    Entierement no-op si le modele ne porte aucun commentaire.
    """
    body = document.element.body

    # 1) Marqueurs de plage : commentRangeStart / commentRangeEnd.
    for tag in ("w:commentRangeStart", "w:commentRangeEnd"):
        for node in body.findall(".//" + qn(tag)):
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)

    # 1bis) Le run d'ancrage (w:r contenant w:commentReference) est retire en
    # entier : c'est un run technique sans texte visible (rPr + commentReference).
    for ref in body.findall(".//" + qn("w:commentReference")):
        run = ref.getparent()
        if run is None or run.tag != qn("w:r"):
            # Reference hors run attendu : retirer au moins l'element lui-meme.
            if run is not None:
                run.remove(ref)
            continue
        run_parent = run.getparent()
        if run_parent is not None:
            run_parent.remove(run)

    # 2) Relations vers les parts de commentaires. Drop la relation suffit :
    # une part orpheline (plus referencee) n'est pas re-serialisee a la sauvegarde.
    main_part = document.part
    for rel_id, related in list(main_part.related_parts.items()):
        partname = str(getattr(related, "partname", ""))
        if partname.endswith(_COMMENT_PART_SUFFIXES):
            main_part.drop_rel(rel_id)


def _apply_line_fixes_to_paragraph(paragraph, line_fixes: list[_LineFix]) -> None:
    """Applique les correctifs regex de paragraphe (texte final, post-tokens).

    Pour chaque fix dont l'ancre est presente, la regex est appliquee au TEXTE
    FUSIONNE du paragraphe ; si le texte change, il est reecrit sur le premier
    run (mise en forme du premier run conservee, comme les autres surcharges).
    """
    if not paragraph.runs:
        return
    text = paragraph.text
    new_text = text
    for fix in line_fixes:
        if fix.anchor in new_text:
            new_text = fix.pattern.sub(fix.replacement, new_text)
    if new_text != text:
        paragraph.runs[0].text = new_text
        for run in paragraph.runs[1:]:
            run.text = ""


def _apply_segment_overrides(
    document,
    segment_overrides: dict[str, str],
) -> None:
    """Remplace des segments litteraux multi-tokens dans les paragraphes.

    Le texte fusionne du paragraphe est reecrit sur le premier run (meme
    strategie de repli que l'accord en genre quand une forme est eclatee).
    """
    for paragraph in _iter_all_paragraphs(document):
        text = paragraph.text
        if not any(segment in text for segment in segment_overrides):
            continue
        for segment, value in segment_overrides.items():
            text = text.replace(segment, value)
        if paragraph.runs:
            paragraph.runs[0].text = text
            for run in paragraph.runs[1:]:
                run.text = ""
        else:
            paragraph.text = text


def _apply_paragraph_overrides(
    document,
    paragraph_overrides: dict[str, str | None],
) -> None:
    """Reecrit ou supprime les paragraphes contenant un token ancre.

    La suppression retire l'element XML du paragraphe (corps comme cellules) ;
    la reecriture conserve la mise en forme du premier run.
    """
    for paragraph in list(_iter_all_paragraphs(document)):
        text = paragraph.text
        for token, override in paragraph_overrides.items():
            if token not in text:
                continue
            if override is None:
                element = paragraph._element
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
            elif paragraph.runs:
                paragraph.runs[0].text = override
                for run in paragraph.runs[1:]:
                    run.text = ""
            else:
                paragraph.text = override
            break


def _apply_gender_pairs_to_paragraph(
    paragraph,
    gender_pairs: list[tuple[Gender, list[tuple[str, str]]]],
) -> None:
    """Accorde en genre les chaines figees d'un paragraphe (corps + cellules).

    Accord d'abord run par run (preserve la mise en forme). Si une forme a
    accorder est eclatee sur plusieurs runs (le texte attendu du paragraphe n'est
    pas atteint), on reecrit le texte fusionne sur le premier run.
    """
    if not paragraph.runs:
        return

    original_paragraph_text = paragraph.text

    for run in paragraph.runs:
        text = run.text
        for genre, pairs in gender_pairs:
            text = apply_gender_pairs(text, genre, pairs)
        if text != run.text:
            run.text = text

    expected_text = original_paragraph_text
    for genre, pairs in gender_pairs:
        expected_text = apply_gender_pairs(expected_text, genre, pairs)

    if paragraph.text != expected_text:
        runs = paragraph.runs
        runs[0].text = expected_text
        for run in runs[1:]:
            run.text = ""


def _collect_residual_tokens(document) -> set[str]:
    residual: set[str] = set()
    for paragraph in _iter_all_paragraphs(document):
        for match in _TOKEN_RE.findall(paragraph.text):
            residual.add(match)
    return residual


def _resolve_model_path(variant: CessionCabinetVariant) -> Path:
    pattern = _MODEL_GLOB_BY_VARIANT[(variant.etape, variant.type_cabinet)]
    matches = glob.glob(str(_SOURCE_MODELS_DIR / pattern))
    if not matches:
        raise ValueError(
            f"Modele introuvable pour {variant.etape}/{variant.type_cabinet} "
            f"(motif {pattern}) dans {_SOURCE_MODELS_DIR}."
        )
    return Path(matches[0])


# ---------------------------------------------------------------------------
# Construction du dictionnaire token -> valeur
# ---------------------------------------------------------------------------


def _build_cession_replacements(
    ctx: DocumentGenerationContext,
    variant: CessionCabinetVariant,
) -> dict[str, str]:
    cession = ctx.cession
    if cession is None:
        raise ValueError(f"cession est obligatoire pour {DOCUMENT_CODE}.")
    vendeur = cession.vendeur or CessionVendeur()
    conjoint = vendeur.conjoint or CessionConjoint()
    acquereur = cession.acquereur or CessionAcquereur()
    representant = acquereur.representant or CessionRepresentant()
    cabinet = cession.cabinet or CessionCabinet()
    precedent = cabinet.precedent_proprietaire
    bail = cession.bail_professionnel or CessionBailProfessionnel()
    prix = cession.prix or CessionPrix()
    financement = cession.financement or CessionFinancement()
    credit_vendeur = financement.credit_vendeur or CessionCreditVendeur()
    pret = financement.pret or CessionPret()
    document = ctx.document or DocumentContext()
    signature = ctx.signature

    replacements: dict[str, str] = {}

    def put(token: str, value: object | None) -> None:
        # Les valeurs None ne sont PAS injectees -> token preserve -> anti-trou (etape 1.3).
        if value is None:
            return
        replacements[token] = str(value)

    def put_opt(token: str, value: object | None) -> None:
        # Champ FACULTATIF (retours client 2026-06-11) : une valeur absente est
        # rendue comme zone vide a completer a la main, sans bloquer la
        # generation ni laisser de token residuel.
        replacements[token] = "" if value is None else str(value)

    # --- Vendeur ---
    put("[civilite_vendeur]", vendeur.civilite_affichage)
    put("[prenom_vendeur]", vendeur.prenom)
    put("[nom_vendeur]", vendeur.nom)
    put("[profession_vendeur]", vendeur.profession)
    put("[date_naissance_vendeur]", _french_date(vendeur.date_naissance))
    put("[ville_naissance_vendeur]", vendeur.ville_naissance)
    put_opt("[departement_naissance_vendeur]", vendeur.departement_naissance)
    put_opt("[cp_naissance_vendeur]", vendeur.cp_naissance)
    put_opt("[pays_naissance_vendeur]", vendeur.pays_naissance)
    put("[nationalite_vendeur]", vendeur.nationalite)
    put("[adresse_vendeur]", vendeur.adresse_affichee)
    put_opt("[adresse_exercice_vendeur]", vendeur.adresse_exercice_affichee)
    put_opt("[numero_siren_vendeur]", vendeur.numero_siren)
    put_opt("[numero_ordre_vendeur]", vendeur.numero_ordre)
    put_opt("[numero_rpps_vendeur]", vendeur.numero_rpps)
    put_opt("[ordre_departemental_vendeur]", vendeur.ordre_departemental)
    put("[situation_maritale_vendeur]", vendeur.situation_maritale)
    put_opt("[regime_matrimonial_vendeur]", vendeur.regime_matrimonial)
    put_opt("[civilite_conjoint_vendeur]", conjoint.civilite_affichage)
    put_opt("[prenom_conjoint_vendeur]", conjoint.prenom)
    put_opt("[nom_conjoint_vendeur]", conjoint.nom)

    # --- Acquereur ---
    put("[denomination_societe_acquereur]", acquereur.denomination_societe)
    put("[forme_sociale_acquereur]", acquereur.forme_sociale)
    put("[capital_social_acquereur]", acquereur.capital_social)
    put("[adresse_siege_acquereur]", _address_label(acquereur.siege))
    put("[ville_rcs_acquereur]", acquereur.rcs_ville)
    put_opt("[numero_rcs_acquereur]", acquereur.numero_rcs)
    put_opt("[numero_siret_acquereur]", acquereur.numero_siret)
    put_opt("[date_immatriculation_acquereur]", _french_date(acquereur.date_immatriculation))
    put_opt(
        "[date_inscription_ordre_acquereur]",
        _french_date(acquereur.date_inscription_ordre),
    )
    put("[civilite_acquereur_representant]", representant.civilite_affichage)
    put("[prenom_acquereur_representant]", representant.prenom)
    put("[nom_acquereur_representant]", representant.nom)
    put("[fonction_acquereur_representant]", representant.fonction)

    # --- Cabinet ---
    put("[adresse_cabinet]", cabinet.adresse_affichee)
    put_opt("[adresse_locaux]", cabinet.adresse_locaux_affichee or cabinet.adresse_affichee)
    put_opt("[telephone_cabinet]", cabinet.telephone)
    put("[superficie_local]", cabinet.superficie_local)
    put("[nature_fonds_liberal]", cabinet.nature_fonds_liberal)
    put("[description_origine_propriete]", cabinet.description_origine_propriete)
    put_opt("[date_origine_propriete]", _french_date(cabinet.date_origine_propriete))
    put_opt("[annees_acquisition_patientele]", cabinet.annees_acquisition_patientele)
    put_opt("[prix_origine_propriete]", cabinet.prix_origine_propriete)
    if precedent is not None:
        put_opt("[civilite_precedent_proprietaire]", precedent.civilite_affichage)
        put_opt("[prenom_precedent_proprietaire]", precedent.prenom)
        put_opt("[nom_precedent_proprietaire]", precedent.nom)
    # Origine de propriete (modeles MEDICAUX) : phrase decrivant le VENDEUR,
    # variante creee/achetee (defaut "cree"), ou texte libre pour un cas complexe.
    # Donnees incompletes -> zone vide a completer a la main (jamais bloquant).
    put_opt("[origine_propriete_phrase]", _build_origine_propriete_phrase(cession))

    # --- Bail professionnel ---
    put_opt("[date_bail]", _french_date(bail.date_bail))
    put("[duree_bail]", bail.duree)
    put_opt("[date_debut_bail]", _french_date(bail.date_debut))
    put_opt("[date_fin_bail]", _french_date(bail.date_fin))
    put_opt("[date_reconduction_bail_1]", _french_date(bail.date_reconduction_1))
    put_opt("[date_reconduction_bail_2]", _french_date(bail.date_reconduction_2))
    put_opt("[loyer_mensuel]", bail.loyer_mensuel)

    # --- Prix ---
    put("[prix_cession]", prix.total)
    put("[prix_cession_lettres]", prix.total_lettres)
    put_opt("[prix_elements_corporels]", prix.elements_corporels)
    put_opt("[prix_elements_corporels_lettres]", prix.elements_corporels_lettres)
    put_opt("[prix_elements_incorporels]", prix.elements_incorporels)
    put_opt("[prix_elements_incorporels_lettres]", prix.elements_incorporels_lettres)

    # --- Financement : credit-vendeur (acte medical) et pret (compromis) ---
    put("[montant_credit_vendeur]", credit_vendeur.montant)
    put("[duree_credit_vendeur]", credit_vendeur.duree)
    put("[taux_credit_vendeur]", credit_vendeur.taux)
    put("[majoration_interet_retard]", credit_vendeur.majoration_interet_retard)
    put_opt("[montant_pret]", pret.montant)
    put_opt("[taux_pret]", pret.taux)
    put_opt("[duree_pret]", pret.duree)

    # --- SCM (acte medical) ---
    if cession.scm is not None:
        put("[nb_parts_scm_a_ceder]", cession.scm.nb_parts_a_ceder)

    # --- Conditions suspensives (compromis) ---
    put_opt("[date_realisation_limite]", _french_date(cession.date_limite_realisation))

    # --- Salaries (acte dentaire) : reprise 0 / 1 / N (regle NotebookLM) ---
    # 0 salarie -> "Néant" (convention systeme) ; 1..N -> liste nom/prenom/poste.
    put("[clause_reprise_salaries]", _build_clause_reprise_salaries(cession.salaries))
    # [date_entree_jouissance] (dentaire) : source choisie = date de debut du bail
    # professionnel (entree en jouissance des locaux). A confirmer cote metier.
    put("[date_entree_jouissance]", _french_date(bail.date_debut))

    # --- Exercices ---
    for index in (0, 1, 2):
        if index < len(cession.exercices):
            exercice = cession.exercices[index]
            put_opt(f"[exercice_{index + 1}]", exercice.periode)
            put_opt(f"[chiffre_affaires_{index + 1}]", exercice.chiffre_affaires)
            put_opt(f"[resultat_{index + 1}]", exercice.resultat)

    # --- Document / signature ---
    put("[lieu_signature]", signature.lieu)
    put("[date_signature]", _french_date(signature.date))
    put("[nombre_exemplaires_lettres]", document.nombre_exemplaires_lettres)
    put("[nombre_pages_lettres]", _nombre_pages_lettres(variant, document))
    _put_signature_tokens(put, variant, vendeur, acquereur, representant)

    return replacements


def _put_signature_tokens(
    put,
    variant: CessionCabinetVariant,
    vendeur: CessionVendeur,
    acquereur: CessionAcquereur,
    representant: CessionRepresentant,
) -> None:
    """Remplit les deux tokens du bloc signature.

    9.8 (COMPROMIS) : le modele rend « [signature_acquereur] <TAB> [signature_vendeur] »
    avec, des deux cotes, une PERSONNE physique « Docteur » (cedant duplique).
    Correctif : 1er signataire (gauche, [signature_acquereur]) = le CEDANT
    (vendeur) ; 2e signataire (droite, [signature_vendeur]) = la SEL acquereur
    (denomination + representant). Les noms de tokens, herites du modele, sont
    donc volontairement « inverses » par rapport a leur intitule.

    ACTE et autres etapes : comportement d'origine conserve (vendeur a gauche du
    token vendeur, representant a droite du token acquereur) — hors perimetre 9.8.
    """
    vendeur_label = _person_label(vendeur.civilite_affichage, vendeur.prenom, vendeur.nom)
    representant_label = _person_label(
        representant.civilite_affichage, representant.prenom, representant.nom
    )
    if variant.etape == COMPROMIS:
        societe_label = _societe_signature_label(acquereur, representant)
        # Gauche (token acquereur) = cedant ; droite (token vendeur) = societe.
        put("[signature_acquereur]", vendeur_label)
        put("[signature_vendeur]", societe_label or representant_label)
        return
    put("[signature_vendeur]", vendeur_label)
    put("[signature_acquereur]", representant_label)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _french_date(value: date | str | None) -> str | None:
    """Formate une date en francais long (ex. "10 mars 1975").

    - date -> jour mois annee en francais ;
    - str ISO "YYYY-MM-DD" -> parsee puis formatee FR ;
    - autre str -> renvoyee telle quelle ;
    - None -> None (laisse le token en place pour l'anti-trou).
    """
    if value is None:
        return None
    if isinstance(value, date):
        return f"{value.day} {_MONTHS_FR[value.month]} {value.year}"
    text = value.strip()
    match = _ISO_DATE_RE.match(text)
    if match is not None:
        year, month, day = (int(part) for part in match.groups())
        try:
            parsed = date(year, month, day)
        except ValueError:
            return text
        return f"{parsed.day} {_MONTHS_FR[parsed.month]} {parsed.year}"
    return text


def _nombre_pages_lettres(
    variant: CessionCabinetVariant,
    document: DocumentContext,
) -> str | None:
    """Nombre de pages en lettres du document (retours 9.9).

    Priorite a la longueur connue du modele (deterministe, fidele). A defaut de
    mapping, on retombe sur la valeur du contexte (front) pour ne pas regresser
    les variantes non visees par le ticket.
    """
    fixed = _PAGES_LETTRES_BY_VARIANT.get((variant.etape, variant.type_cabinet))
    if fixed is not None:
        return fixed
    return document.nombre_pages_lettres


def _person_label(
    civilite: str | None,
    prenom: str | None,
    nom: str | None,
) -> str | None:
    parts = [part for part in (civilite, prenom, nom) if part]
    if not parts:
        return None
    return " ".join(parts)


def _build_origine_propriete_phrase(cession: CessionContext) -> str | None:
    """Construit la clause d'origine de propriete des modeles MEDICAUX.

    Regle NotebookLM : la clause decrit le VENDEUR (cedant) — comment il est
    devenu proprietaire. Deux variantes standard, defaut "cree" :
      - "cree"   -> "... pour l'avoir regulierement cree le <date>."
      - "achete" -> "... pour l'avoir regulierement acquis aupres de <precedent>,
                     le <date> au prix de <prix> euros."
    Un cas COMPLEXE (mode non standard) est porte par le texte libre
    `cabinet.description_origine_propriete`, sous garde-fou de validation manuelle
    (cf. `_validate_origine_propriete`). On reutilise le wording deja valide des
    modeles dentaires (meme sujet vendeur) : aucune reecriture libre.
    """
    cabinet = cession.cabinet or CessionCabinet()
    vendeur = cession.vendeur or CessionVendeur()

    mode = (cabinet.origine_propriete_mode or ORIGINE_MODE_CREE).strip().lower()
    sujet = _person_label(vendeur.civilite_affichage, vendeur.prenom, vendeur.nom)
    description = (cabinet.description_origine_propriete or "").strip()

    # Cas COMPLEXE / non standard -> texte libre saisi a la main (relecture humaine).
    if mode not in SUPPORTED_ORIGINE_MODES:
        return description or None

    if sujet is None:
        # Identite vendeur incomplete -> on ne devine pas, on laisse le token
        # en place (anti-trou) sauf si un texte libre a ete fourni.
        return description or None

    date_origine = _french_date(cabinet.date_origine_propriete)

    if mode == ORIGINE_MODE_CREE:
        if not date_origine:
            return description or None
        phrase = (
            f"{sujet} est propriétaire des éléments constitutifs du cabinet "
            f"pour l’avoir régulièrement créé le {date_origine}."
        )
    else:  # ORIGINE_MODE_ACHETE
        precedent = cabinet.precedent_proprietaire
        precedent_label = (
            _person_label(precedent.civilite_affichage, precedent.prenom, precedent.nom)
            if precedent is not None
            else None
        )
        prix = (cabinet.prix_origine_propriete or "").strip()
        if not date_origine or not precedent_label or not prix:
            return description or None
        phrase = (
            f"{sujet} est propriétaire des éléments constitutifs du cabinet "
            f"pour les avoir régulièrement acquis auprès de {precedent_label}, "
            f"le {date_origine} au prix de {prix} euros."
        )

    # Complement libre eventuel (precisions metier) appose tel quel.
    if description:
        phrase = f"{phrase} {description}"
    return phrase


def _build_clause_reprise_salaries(salaries: list[CessionSalarie]) -> str:
    """Construit la clause de reprise des contrats de travail (acte dentaire).

    Regle NotebookLM : 0 salarie -> "Néant" (convention systeme) ; 1..N salaries
    -> "De reprendre les contrats de travail de <liste>." ou chaque salarie est
    "Civilite Prenom Nom" (+ ", en qualite de <poste>" si le poste est saisi).
    Reutilise le wording de clause existant du modele ; "Néant" applique la
    convention systeme (aucune clause "néant" dediee dans le modele source).
    """
    if not salaries:
        return NEANT

    labels: list[str] = []
    for index, salarie in enumerate(salaries):
        label = _salarie_label(salarie, index)
        poste = (salarie.poste or "").strip()
        if poste:
            label = f"{label}, en qualité de {poste}"
        labels.append(label)

    if len(labels) == 1:
        liste = labels[0]
    else:
        liste = ", ".join(labels[:-1]) + f" et de {labels[-1]}"
    return f"De reprendre les contrats de travail de {liste}."


def _address_label(address: Address | None) -> str | None:
    if address is None:
        return None
    if address.adresse_affichee:
        return address.adresse_affichee
    parts = [address.num_voie, address.voie, address.cp, address.ville]
    joined = " ".join(part for part in parts if part)
    return joined or None


# ---------------------------------------------------------------------------
# Validation metier (inchangee dans son intention : conserve les regles ratifiees)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _CessionData:
    ctx: DocumentGenerationContext
    cession: CessionContext
    vendeur: CessionVendeur
    acquereur: CessionAcquereur
    representant: CessionRepresentant
    cabinet: CessionCabinet
    bail: CessionBailProfessionnel
    prix: CessionPrix
    exercices: list[CessionExercice]
    financement: CessionFinancement
    document: DocumentContext
    validations: CessionValidations


def _validate_context(
    ctx: DocumentGenerationContext,
    variant: CessionCabinetVariant,
) -> _CessionData:
    if ctx.structure not in SUPPORTED_STRUCTURES:
        supported = ", ".join(sorted(SUPPORTED_STRUCTURES))
        raise ValueError(f"dossier.structure doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None or not ctx.dossier_options.cession:
        raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    cession = _required_cession(ctx)
    _validate_selection(cession, variant)

    vendeur = _required_vendeur(cession.vendeur)
    acquereur = _required_acquereur(cession.acquereur)
    representant = _required_representant(acquereur.representant)
    cabinet = _required_cabinet(cession.cabinet)
    bail = _required_bail(cession.bail_professionnel)
    prix = _required_prix(cession.prix)
    financement = cession.financement or CessionFinancement()
    document = _required_document(ctx.document)
    validations = cession.validations or CessionValidations()

    exercices = _required_exercices(cession.exercices)
    _validate_arbitrage_blocks(cession, variant, validations)
    _validate_financement(cession, variant, financement)
    _validate_salaries(cession, variant, validations)
    _validate_origine_propriete(cession, variant, cabinet, validations)

    return _CessionData(
        ctx=ctx,
        cession=cession,
        vendeur=vendeur,
        acquereur=acquereur,
        representant=representant,
        cabinet=cabinet,
        bail=bail,
        prix=prix,
        exercices=exercices,
        financement=financement,
        document=document,
        validations=validations,
    )


def _validate_selection(cession: CessionContext, variant: CessionCabinetVariant) -> None:
    type_cabinet = _required_text(cession.type_cabinet, "cession.type_cabinet").lower()
    if type_cabinet not in SUPPORTED_CABINET_TYPES:
        supported = ", ".join(sorted(SUPPORTED_CABINET_TYPES))
        raise ValueError(f"cession.type_cabinet doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if type_cabinet != variant.type_cabinet:
        raise ValueError(
            f"cession.type_cabinet doit etre {variant.type_cabinet} pour {variant.output_filename}."
        )

    # cession.etape reste un champ REQUIS et borne a SUPPORTED_ETAPES, MAIS il n'est plus
    # PILOTANT (re-Akainu 2026-06-23, NITPICK O24-14 : couplage vestigial documente). Il sert
    # encore de garde de presence/validite de saisie ; un appelant qui le laisse vide/None
    # leve donc ici via _required_text. C'est volontaire : en SELAS le formulaire force
    # toujours etape='acte', et on prefere une garde de presence explicite a un champ optionnel.
    etape = _required_text(cession.etape, "cession.etape").lower()
    if etape not in SUPPORTED_ETAPES:
        supported = ", ".join(sorted(SUPPORTED_ETAPES))
        raise ValueError(f"cession.etape doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    # O24-14 (onglet 24) : en SELAS, l'acte ET le compromis sont produits ENSEMBLE. Le
    # document genere est determine par le VARIANT (variant.etape pilote modele + contenu),
    # jamais par cession.etape. La SELECTION cote orchestrateur (_cession_cabinet_enabled)
    # a deja choisi les bons documents -> on ne leve plus sur un mismatch
    # cession.etape/variant.etape (sinon le compromis crashe quand cession.etape='acte').


def _validate_arbitrage_blocks(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    validations: CessionValidations,
) -> None:
    if variant.type_cabinet == MEDICAL and not validations.mentions_bail_medical_validees:
        raise ValueError(
            "cession.validations.mentions_bail_medical_validees doit etre vrai pour "
            f"{DOCUMENT_CODE}."
        )
    if (
        variant.etape == COMPROMIS
        and variant.type_cabinet == MEDICAL
        and not validations.origine_compromis_medical_validee
    ):
        raise ValueError(
            "cession.validations.origine_compromis_medical_validee doit etre vrai pour "
            f"{DOCUMENT_CODE}."
        )
    if variant.etape == COMPROMIS and not validations.date_realisation_compromis_validee:
        raise ValueError(
            "cession.validations.date_realisation_compromis_validee doit etre vrai pour "
            f"{DOCUMENT_CODE}."
        )
    if (
        variant.etape == ACTE
        and variant.type_cabinet == MEDICAL
        and not validations.ligne_contrats_travail_medical_supprimee
    ):
        raise ValueError(
            "cession.validations.ligne_contrats_travail_medical_supprimee doit etre vrai "
            f"pour {DOCUMENT_CODE}."
        )


def _validate_financement(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    financement: CessionFinancement,
) -> None:
    credit_vendeur = financement.credit_vendeur
    if credit_vendeur is not None and credit_vendeur.actif:
        if not (variant.etape == ACTE and variant.type_cabinet == MEDICAL):
            raise ValueError(
                "cession.financement.credit_vendeur.actif est autorise uniquement pour "
                f"l'acte medical {DOCUMENT_CODE}."
            )
        _required_text(credit_vendeur.montant, "cession.financement.credit_vendeur.montant")
        _required_text(credit_vendeur.duree, "cession.financement.credit_vendeur.duree")
        _required_text(credit_vendeur.taux, "cession.financement.credit_vendeur.taux")
        _required_text(
            credit_vendeur.majoration_interet_retard,
            "cession.financement.credit_vendeur.majoration_interet_retard",
        )

    if cession.scm is not None and cession.scm.actif:
        if not (variant.etape == ACTE and variant.type_cabinet == MEDICAL):
            raise ValueError("cession.scm.actif est autorise uniquement pour l'acte medical.")
        _required_text(cession.scm.nb_parts_a_ceder, "cession.scm.nb_parts_a_ceder")


def _validate_salaries(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    validations: CessionValidations,
) -> None:
    # Reprise des salaries rendue uniquement par l'acte dentaire (seul modele
    # portant la clause). Regle NotebookLM : 0 -> "Néant" ; 1..N -> liste.
    if variant.etape == ACTE and variant.type_cabinet == DENTAIRE:
        # 0..N accepte. Chaque salarie liste doit avoir une identite complete
        # (civilite/prenom/nom). Le poste reste optionnel.
        for index, salarie in enumerate(cession.salaries):
            _salarie_label(salarie, index)
        return
    if cession.salaries:
        raise ValueError(
            f"cession.salaries est rendu uniquement pour l'acte dentaire {DOCUMENT_CODE}."
        )


def _validate_origine_propriete(
    cession: CessionContext,
    variant: CessionCabinetVariant,
    cabinet: CessionCabinet,
    validations: CessionValidations,
) -> None:
    """Garde-fou origine de propriete pour les modeles MEDICAUX (token construit).

    Souplesse cas COMPLEXE : un mode d'origine non standard (ni "cree" ni
    "achete", ex. succession / apport / demembrement) DOIT etre saisi en texte
    libre (`cabinet.description_origine_propriete`) ET valide a la main
    (`validations.origine_propriete_complexe_validee`). Le moteur n'emet pas une
    origine devinee. Les modeles dentaires gardent leur clause figee (non
    concernes par le token construit).
    """
    if variant.type_cabinet != MEDICAL:
        return

    mode = (cabinet.origine_propriete_mode or ORIGINE_MODE_CREE).strip().lower()
    if mode in SUPPORTED_ORIGINE_MODES:
        return

    # Cas complexe : exiger texte libre + validation manuelle (relecture humaine).
    description = (cabinet.description_origine_propriete or "").strip()
    if not description or not validations.origine_propriete_complexe_validee:
        raise ValueError(
            "cession.cabinet.origine_propriete_mode non standard "
            f"({cabinet.origine_propriete_mode!r}) : fournir "
            "cession.cabinet.description_origine_propriete ET "
            "cession.validations.origine_propriete_complexe_validee=True pour "
            f"{DOCUMENT_CODE}."
        )


def _required_cession(ctx: DocumentGenerationContext) -> CessionContext:
    if ctx.cession is None:
        raise ValueError(f"cession est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.cession


def _required_vendeur(vendeur: CessionVendeur | None) -> CessionVendeur:
    if vendeur is None:
        raise ValueError(f"cession.vendeur est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.vendeur.civilite_affichage", vendeur.civilite_affichage),
        ("cession.vendeur.prenom", vendeur.prenom),
        ("cession.vendeur.nom", vendeur.nom),
        ("cession.vendeur.profession", vendeur.profession),
        ("cession.vendeur.date_naissance", vendeur.date_naissance),
        ("cession.vendeur.ville_naissance", vendeur.ville_naissance),
        ("cession.vendeur.nationalite", vendeur.nationalite),
        ("cession.vendeur.adresse_affichee", vendeur.adresse_affichee),
        ("cession.vendeur.situation_maritale", vendeur.situation_maritale),
    ]:
        _required_value(value, field_name)
    return vendeur


def _required_acquereur(acquereur: CessionAcquereur | None) -> CessionAcquereur:
    if acquereur is None:
        raise ValueError(f"cession.acquereur est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.acquereur.denomination_societe", acquereur.denomination_societe),
        ("cession.acquereur.forme_sociale", acquereur.forme_sociale),
        ("cession.acquereur.capital_social", acquereur.capital_social),
        ("cession.acquereur.rcs_ville", acquereur.rcs_ville),
    ]:
        _required_text(value, field_name)
    _required_text(_address_label(acquereur.siege), "cession.acquereur.siege.adresse_affichee")
    return acquereur


def _required_representant(representant: CessionRepresentant | None) -> CessionRepresentant:
    if representant is None:
        raise ValueError(f"cession.acquereur.representant est obligatoire pour {DOCUMENT_CODE}.")
    for field_name, value in [
        ("cession.acquereur.representant.civilite_affichage", representant.civilite_affichage),
        ("cession.acquereur.representant.prenom", representant.prenom),
        ("cession.acquereur.representant.nom", representant.nom),
        ("cession.acquereur.representant.fonction", representant.fonction),
    ]:
        _required_text(value, field_name)
    return representant


def _required_cabinet(cabinet: CessionCabinet | None) -> CessionCabinet:
    if cabinet is None:
        raise ValueError(f"cession.cabinet est obligatoire pour {DOCUMENT_CODE}.")
    _required_value(cabinet.adresse_affichee, "cession.cabinet.adresse_affichee")
    # Telephone et adresse des locaux : champs FACULTATIFS (retours client
    # 2026-06-11, ticket 3.1) — vides, ils laissent une zone a completer a la
    # main sans bloquer la generation.
    # description_origine_propriete n'est plus un token autonome : la clause
    # d'origine medicale est construite a partir des donnees vendeur (mode
    # cree/achete). Le texte libre n'est exige que pour un cas COMPLEXE
    # (cf. _validate_origine_propriete).
    return cabinet


def _required_bail(bail: CessionBailProfessionnel | None) -> CessionBailProfessionnel:
    if bail is None:
        raise ValueError(f"cession.bail_professionnel est obligatoire pour {DOCUMENT_CODE}.")
    # Retours client 2026-06-11 (ticket 3.1) : seule la duree reste obligatoire
    # (preremplie « six annees »). Dates et activite vides -> zones a completer
    # a la main, jamais bloquantes.
    _required_value(bail.duree, "cession.bail_professionnel.duree")
    return bail


def _required_prix(prix: CessionPrix | None) -> CessionPrix:
    if prix is None:
        raise ValueError(f"cession.prix est obligatoire pour {DOCUMENT_CODE}.")
    # Retours client 2026-06-11 (ticket 3.1) : le prix TOTAL (chiffres + lettres)
    # reste le strict necessaire d'un acte de cession ; la ventilation
    # corporels / incorporels vide laisse une zone a completer a la main.
    for field_name, value in [
        ("cession.prix.total", prix.total),
        ("cession.prix.total_lettres", prix.total_lettres),
    ]:
        _required_text(value, field_name)
    return prix


def _required_document(document: DocumentContext | None) -> DocumentContext:
    if document is None:
        raise ValueError(f"document est obligatoire pour {DOCUMENT_CODE}.")
    _required_text(document.nombre_pages_lettres, "document.nombre_pages_lettres")
    _required_text(document.nombre_exemplaires_lettres, "document.nombre_exemplaires_lettres")
    return document


def _required_exercices(exercices: list[CessionExercice]) -> list[CessionExercice]:
    if len(exercices) != 3:
        raise ValueError("cession.exercices doit contenir exactement trois lignes.")
    # Retours client 2026-06-11 (tickets 2.8 / 3.1) : CA et resultat vides par
    # defaut et jamais bloquants -> zones a completer a la main dans l'acte.
    return exercices


def _salarie_label(salarie: CessionSalarie, index: int) -> str:
    field_name = f"cession.salaries[{index}]"
    return (
        f"{_required_text(salarie.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{_required_text(salarie.prenom, f'{field_name}.prenom')} "
        f"{_required_text(salarie.nom, f'{field_name}.nom')}"
    )


def _required_value(value: date | str | None, field_name: str) -> date | str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()
