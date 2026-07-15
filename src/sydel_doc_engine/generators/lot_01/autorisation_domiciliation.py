# ruff: noqa: E501

from __future__ import annotations

import glob
import re
from datetime import date
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

from sydel_doc_engine.domain.models import Address, Company, DocumentGenerationContext
from sydel_doc_engine.front_app.field_derivations import group_montant
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.rendering.docx_template_fill import fill_docx_template
from sydel_doc_engine.utils.grammar import montant_avec_euros

ROBOTO_FONT = "Roboto"

DOCUMENT_CODE = "DOC-002"
OUTPUT_FILENAME = "autorisation_domiciliation.docx"

# B6 (Albane 2026-07-09) : pour TOUTES les societes CIVILES, la domiciliation dit
# « dans les locaux au <adresse> » (sans « du cabinet »). SEL / SPFPL conservent
# « du cabinet » (OK dans leur modele) ; la SASU Holding a deja son propre wording
# (« dans les locaux situes a … »), traite plus bas.
_CIVIL_STRUCTURES: frozenset[str] = frozenset(
    {"SCI", "SCI IRIS", "SCM", "SCS", "MICRO_HOLDING"}
)

# Dossier des modeles Word tokenises, resolu independamment du cwd.
# parents[4] depuis src/sydel_doc_engine/generators/lot_01/ = racine du repo.
_SOURCE_MODELS_DIR = (
    Path(__file__).resolve().parents[4] / "project" / "source_documents" / "lot_01"
)

# Motif glob robuste aux accents du nom de fichier du modele.
_MODEL_GLOB = "autorisation*domiciliation*.docx"

_ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


class AutorisationDomiciliationGenerator:
    """Générateur cible du DOC-002.

    Rendu fidèle par remplissage du modèle source tokenisé
    (autorisation_domiciliation_transforme.docx) : le texte juridique figé du
    modèle est conservé tel quel (dont « pour une durée indéterminée »), seuls les
    tokens `[variable]` sont remplacés par les valeurs du contexte. Aucune prose
    n'est paraphrasée ni inventée.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        replacements = _build_replacements(ctx)
        model_path = _resolve_model_path()
        output_path = output_dir / OUTPUT_FILENAME
        # Le modele source fige l'ouverture au feminin (« Je soussignée »).
        # On l'accorde au genre du signataire : pour un homme -> « Je soussigné ».
        gender_pairs = [
            (
                ctx.personne_signataire.genre,
                [("Je soussigné", "Je soussignée")],
            )
        ]
        filled = fill_docx_template(
            model_path,
            replacements,
            output_path,
            gender_pairs=gender_pairs,
        )
        # Micro holding (Albane 2026-06-29) : la societe domiciliee est a CAPITAL VARIABLE.
        # Le modele generique fige « au capital de <X> euros » -> on remplace par la mention
        # capital variable du modele Albane « a capital variable au capital minimum de <X> €
        # et au capital effectif de <X> € » (les autres structures ne sont PAS touchees).
        if ctx.structure == "MICRO_HOLDING":
            _apply_micro_holding_capital_variable(filled, _required_text(
                _required_company(ctx.societe).capital, "societe.capital"
            ))
        # SASU Holding (Albane 2026-06-29) : holding patrimoniale, PAS un cabinet -> le wording
        # « dans les locaux du cabinet au … » du tronc commun est inadapte. Le modele Albane SAS
        # ecrit « dans les locaux situes a <adresse>, pour une duree indeterminee » (gate Akainu
        # M1/M2). Remplacement structure-aware (les autres structures ne sont PAS touchees).
        if ctx.structure == "SASU_HOLDING":
            _apply_sasu_holding_locaux(filled)
        # B6 (Albane 2026-07-09) : societes civiles -> « dans les locaux au <adresse> »
        # (retrait de « du cabinet »). Applique apres la mention capital variable du
        # micro (segments distincts du meme paragraphe). SEL/SPFPL non touches.
        if ctx.structure in _CIVIL_STRUCTURES:
            _apply_civil_locaux(filled)
        # Retour Albane 2026-06-10 : police Roboto 10 sur l'autorisation (« le
        # reste c'est top »). Le modele est une lettre courte SANS titre distinct :
        # le « titre en 11 » demande par Albane n'a pas de cible ici (a confirmer
        # avec elle) -> on applique Roboto 10 a tout le corps.
        _apply_roboto_font(filled, body_size_pt=10)
        return filled


def _build_replacements(ctx: DocumentGenerationContext) -> dict[str, str]:
    """Construit le dictionnaire token -> valeur en validant les champs requis.

    La validation métier d'origine (champs obligatoires de DOC-002) est conservée :
    un champ manquant lève ValueError plutôt que d'injecter un trou dans l'acte.
    """
    person = ctx.personne_signataire
    company = _required_company(ctx.societe)

    # R3 (Albane 2026-07-07) : « Docteur » n'est pas une civilité — le token
    # [civilite] du modèle ouvre « Je soussigné(e) __ » : civilité CIVILE
    # (Monsieur/Madame), jamais le titre professionnel posé par le flux.
    civilite = civilite_civile(
        _required_text(person.civilite, "personne_signataire.civilite"),
        person.genre,
    )
    prenom = _required_text(person.prenom, "personne_signataire.prenom")
    nom = _required_text(person.nom, "personne_signataire.nom")
    denomination_societe = _required_text(company.denomination, "societe.denomination")
    capital_social = _required_text(company.capital, "societe.capital")
    siege = _required_siege(company.siege)
    # Numero de voie optionnel (champ fusionne « Numero et voie », retours
    # client 2026-06-11) : un siege sans numero (lieu-dit) reste valide.
    num_voie_siege = (siege.num_voie or "").strip()
    voie_siege = _required_text(siege.voie, "societe.siege.voie")
    cp_siege = _required_text(siege.cp, "societe.siege.cp")
    ville_siege = _required_text(siege.ville, "societe.siege.ville")
    lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")
    date_signature = _french_date(ctx.signature.date)

    return {
        "[civilite]": civilite,
        "[prenom]": prenom,
        "[nom]": nom,
        "[denomination_societe]": denomination_societe,
        # Retour Albane 2026-06-17 (ticket lot 2, §11) : le modele fige
        # « au capital de [capital_social] en cours de formation » sans unite ;
        # on suffixe l'unite ACCORDEE (Rafael 2026-07-09 : « 1 euro » / « 600 euros »,
        # jamais « 1 euros ») via montant_avec_euros (idempotent, R13).
        "[capital_social]": montant_avec_euros(capital_social),
        "[num_voie_siege]": num_voie_siege,
        "[voie_siege]": voie_siege,
        "[cp_siege]": cp_siege,
        "[ville_siege]": ville_siege,
        "[lieu_signature]": lieu_signature,
        "[date_signature]": date_signature,
    }


def _set_run_font(run, *, name: str, size_pt: int) -> None:
    run.font.name = name
    run.font.size = Pt(size_pt)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def _apply_roboto_font(output_path: Path, *, body_size_pt: int) -> None:
    """Force la police Roboto (taille `body_size_pt`) sur tout le document filled.

    Retour Albane 2026-06-10 (autorisation de domiciliation). On regle le style
    Normal ET chaque run (pour ecraser une eventuelle police directe du modele).
    """
    document = Document(str(output_path))
    normal = document.styles["Normal"]
    normal.font.name = ROBOTO_FONT
    normal.font.size = Pt(body_size_pt)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), ROBOTO_FONT)
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            _set_run_font(run, name=ROBOTO_FONT, size_pt=body_size_pt)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        _set_run_font(run, name=ROBOTO_FONT, size_pt=body_size_pt)
    document.save(str(output_path))


def _apply_micro_holding_capital_variable(output_path: Path, capital: str) -> None:
    """Micro holding : remplace « au capital de <X> euros en cours de formation » par la
    mention capital variable du modele Albane (« a capital variable au capital minimum de
    <X> € et au capital effectif de <X> €, en cours de formation »).

    Remplacement au niveau du paragraphe (le segment couvre plusieurs runs apres le
    remplissage des tokens) ; la police est re-appliquee ensuite par _apply_roboto_font.
    NB perimetre (a confirmer Rafael/Albane, cf. QUESTIONS_RAFAEL) : on conserve la
    denomination reelle de la societe (« de la <denomination> ») la ou le modele Albane
    ecrit la forme generique « de la Societe micro holding ».
    """
    # R5 (Rafael 2026-07-09) : capital groupé des 4 chiffres (« 1 020 »), y compris dans
    # la mention capital-variable ; group_montant préserve le format à point Albane
    # (« 1.020 ») et ne touche pas un montant déjà groupé.
    capital_groupe = group_montant(capital)
    old = f"au capital de {montant_avec_euros(capital)} en cours de formation"
    new = (
        f"à capital variable au capital minimum de {capital_groupe} € "
        f"et au capital effectif de {capital_groupe} €, en cours de formation"
    )
    document = Document(str(output_path))
    for paragraph in document.paragraphs:
        if old in paragraph.text:
            new_text = paragraph.text.replace(old, new)
            if paragraph.runs:
                paragraph.runs[0].text = new_text
                for run in paragraph.runs[1:]:
                    run.text = ""
            else:
                paragraph.text = new_text
    document.save(str(output_path))


def _apply_civil_locaux(output_path: Path) -> None:
    """B6 (Albane 2026-07-09) : societes civiles -> retrait de « du cabinet » :
    « dans les locaux du cabinet au <adresse> » -> « dans les locaux au <adresse> ».

    Remplacement au niveau du paragraphe (le segment couvre plusieurs runs apres le
    remplissage des tokens et l'eventuelle mention capital variable) ; la police est
    re-appliquee ensuite par _apply_roboto_font.
    """
    old = "dans les locaux du cabinet au "
    new = "dans les locaux au "
    document = Document(str(output_path))
    for paragraph in document.paragraphs:
        if old in paragraph.text:
            new_text = paragraph.text.replace(old, new)
            if paragraph.runs:
                paragraph.runs[0].text = new_text
                for run in paragraph.runs[1:]:
                    run.text = ""
            else:
                paragraph.text = new_text
    document.save(str(output_path))


def _apply_sasu_holding_locaux(output_path: Path) -> None:
    """SASU Holding : aligne la domiciliation sur le modele Albane SAS (gate Akainu) :
    - « de la <denom> » -> « de la SAS <denom> » (forme abregee, comme la procuration ; le
      modele Albane ecrit « de la SAS … » et le bundle doit etre coherent) ;
    - « dans les locaux du cabinet au <adresse> pour une duree indeterminee » -> « dans les
      locaux situes a <adresse>, pour une duree indeterminee » (une holding n'est pas un
      cabinet ; virgule avant « pour »).

    Remplacement au niveau du paragraphe (segment multi-runs) ; police re-appliquee ensuite.
    """
    document = Document(str(output_path))
    for paragraph in document.paragraphs:
        text = paragraph.text
        if "dans les locaux du cabinet au " not in text:
            continue
        new_text = (
            text.replace(
                "autorise la domiciliation de la ", "autorise la domiciliation de la SAS "
            )
            .replace("dans les locaux du cabinet au ", "dans les locaux situés à ")
            .replace(" pour une durée indéterminée", ", pour une durée indéterminée")
        )
        if paragraph.runs:
            paragraph.runs[0].text = new_text
            for run in paragraph.runs[1:]:
                run.text = ""
        else:
            paragraph.text = new_text
    document.save(str(output_path))


def _resolve_model_path() -> Path:
    matches = glob.glob(str(_SOURCE_MODELS_DIR / _MODEL_GLOB))
    if not matches:
        raise ValueError(
            f"Modèle introuvable pour {DOCUMENT_CODE} "
            f"(motif {_MODEL_GLOB}) dans {_SOURCE_MODELS_DIR}."
        )
    return Path(matches[0])


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def _required_siege(address: Address | None) -> Address:
    if address is None:
        raise ValueError(f"societe.siege est obligatoire pour {DOCUMENT_CODE}.")
    return address


def _required_text(value: str | None, field_name: str) -> str:
    # KAN-2 (Rafael 2026-07-13) : donnée manquante -> marqueur « (À COMPLÉTER : …) » (non bloquant, R10).
    if value is None or not value.strip():
        return f"(À COMPLÉTER : {field_name})"
    return value.strip()


def _french_date(value: date | str | None) -> str:
    """Formate la date de signature en JJ/MM/AAAA (ex. « 12/05/2026 »).

    Convention Albane (propagation, Gad 2026-06-29) : les SATELLITES (domiciliation,
    procuration, liste des souscripteurs) portent la date en JJ/MM/AAAA ; seuls les
    STATUTS sont en toutes lettres. Tous les modeles Albane de domiciliation (SAS +
    micro holding) ecrivent « Le JJ/MM/AAAA ».

    - date -> JJ/MM/AAAA ;
    - str ISO « YYYY-MM-DD » -> parsee puis formatee JJ/MM/AAAA ;
    - autre str -> renvoyee telle quelle.
    """
    # KAN-2 : date non renseignee -> marqueur visible (non bloquant), jamais une date inventee.
    if value is None:
        return "(À COMPLÉTER : signature.date)"
    if isinstance(value, date):
        return f"{value.day:02d}/{value.month:02d}/{value.year}"
    text = value.strip()
    match = _ISO_DATE_RE.match(text)
    if match is not None:
        year, month, day = (int(part) for part in match.groups())
        try:
            parsed = date(year, month, day)
        except ValueError:
            return text
        return f"{parsed.day:02d}/{parsed.month:02d}/{parsed.year}"
    return text
