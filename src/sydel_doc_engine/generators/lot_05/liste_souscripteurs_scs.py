from __future__ import annotations

import copy
import re
from pathlib import Path

from docx import Document
from docx.table import _Row

from sydel_doc_engine.domain.models import (
    DocumentGenerationContext,
    StatutsCivilsAssocie,
)
from sydel_doc_engine.utils.grammar import montant_avec_euros

OUTPUT_FILENAME = "liste_souscripteurs_scs.docx"
_SOURCE_NAME = "Liste_souscripteurs_SCS_modele.docx"
DOCUMENT_CODE = "DOC-LSS-SCS"

# SCS5 (Albane 2026-06-25 ; arbitrage Rafael : « adapte les termes a la SCS (parts/president) »).
# La SCS est une societe civile a PARTS sociales -> le modele source (copie SAS parlant
# d'« actions ») est adapte « actions » -> « parts ». Le role certificateur « President » est
# CONSERVE (decision Rafael). Civilite civile M./Mme (SP2). Rebuild fidele = token-replacement
# IN-PLACE du modele source (texte legal + accents preserves), table dynamique (1 ligne/associe).


def _source_path() -> Path:
    path = Path("project/source_documents/scs") / _SOURCE_NAME
    if not path.exists():
        raise ValueError(f"modele source introuvable pour {OUTPUT_FILENAME}: {path}")
    return path


def _adapt_actions_to_parts(text: str) -> str:
    """« actions » -> « parts » (SCS = parts sociales). « President » conserve (Rafael)."""
    out = text
    out = out.replace("souscription d’actions", "souscription de parts")
    out = out.replace("souscription d'actions", "souscription de parts")
    out = out.replace("Nombre d’actions souscrites", "Nombre de parts souscrites")
    out = out.replace("Nombre d'actions souscrites", "Nombre de parts souscrites")
    # SCS5 (Akainu n1) : remplacement ancre sur le MOT (robuste a la ponctuation/debut de
    # ligne), pas sur l'espace de tete.
    out = re.sub(r"\bactions\b", "parts", out)
    return out


def _safe_int(value: object) -> int:
    cleaned = re.sub(r"[^\d]", "", str(value or ""))
    return int(cleaned) if cleaned else 0


def _set_para_text(paragraph, text: str) -> None:
    """Remplace le texte d'un paragraphe en conservant le 1er run (formatage) et en
    vidant les suivants — robuste aux placeholders repartis sur plusieurs runs."""
    if paragraph.runs:
        paragraph.runs[0].text = text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(text)


def _render_text(text: str, replacements: dict[str, str]) -> str:
    out = text
    for token, value in replacements.items():
        if token in out:
            out = out.replace(token, value)
    return _adapt_actions_to_parts(out)


def _apply_to_paragraph(paragraph, replacements: dict[str, str]) -> None:
    original = paragraph.text
    rendered = _render_text(original, replacements)
    if rendered != original:
        _set_para_text(paragraph, rendered)


def _all_associes(ctx: DocumentGenerationContext) -> list[StatutsCivilsAssocie]:
    """TOUS les associes (PP + PM), dans l'ordre du dossier (= ordre des plages de parts)."""
    statuts = ctx.statuts_civils
    return list(statuts.associes) if statuts and statuts.associes else []


def _siege_of_associe(associe: StatutsCivilsAssocie) -> str:
    if associe.adresse_personnelle_affichee:
        return associe.adresse_personnelle_affichee.strip()
    siege = associe.siege
    if siege is not None and siege.adresse_affichee:
        return siege.adresse_affichee.strip()
    return ""


def _associe_nb_parts(associe: StatutsCivilsAssocie) -> int:
    if associe.parts and associe.parts.nb:
        return int(associe.parts.nb)
    return 0


def _associe_montant(associe: StatutsCivilsAssocie) -> str:
    if associe.apport and associe.apport.montant:
        return str(associe.apport.montant)
    return ""


class ListeSouscripteursScsGenerator:
    """Liste des souscripteurs d'une SCS (parts/President, SP2 civilite M./Mme),
    token-replacement IN-PLACE du modele source (SCS5)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        # SCS5 (Akainu M2) : la liste des souscripteurs porte TOUS les associes (personnes
        # physiques ET morales) — sinon un associe PM est omis et le TOTAL ne correspond plus
        # au capital souscrit. Le certificateur (signataire) reste le gerant : 1re personne
        # PHYSIQUE (commandite), pas une PM.
        associes = _all_associes(ctx)
        if not associes:
            raise ValueError(f"associes requis pour {OUTPUT_FILENAME}.")
        physiques = [a for a in associes if a.type_personne == "personne_physique"]
        certificateur = physiques[0] if physiques else associes[0]

        total_parts = sum(_associe_nb_parts(a) for a in associes)
        total_montant = sum(_safe_int(_associe_montant(a)) for a in associes)

        company = ctx.societe
        signature = ctx.signature
        replacements = {
            "[forme_sociale_abregee]": "SCS",
            "[denomination_societe]": _txt(company.denomination if company else None),
            "[forme_sociale]": _txt(company.forme_sociale if company else None),
            "[forme_sociale_complete]": _txt(
                (company.forme_sociale_complete if company else None)
                or (company.forme_sociale if company else None)
            ),
            # Rafael 2026-07-09 (transverse devise) : « au capital de [capital_social] »
            # du modele n'a pas d'unite -> derivee (montant nu -> « 1 000 euros »).
            "[capital_social]": montant_avec_euros(
                _txt(company.capital_social if company else None)
            ),
            "[adresse_siege]": _siege(company),
            "[ville_rcs]": _txt(company.ville_rcs if company else None),
            "[montant_sous]": str(total_montant),
            "[lieu_signature]": _txt(signature.lieu if signature else None),
            "[date_signature]": _date(signature),
            "[prenom]": _txt(certificateur.prenom),
            "[nom]": _txt(certificateur.nom),
        }

        document = Document(str(_source_path()))
        for paragraph in document.paragraphs:
            _apply_to_paragraph(paragraph, replacements)

        self._render_table(document, associes, total_parts, total_montant, replacements)

        self._assert_no_residual(document)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path

    def _render_table(self, document, associes, total_parts, total_montant, replacements) -> None:  # noqa: C901
        if not document.tables:
            return
        table = document.tables[0]
        # Ligne 0 = en-tete (adapter « actions » -> « parts »), ligne 1 = gabarit associe,
        # derniere ligne = TOTAL.
        for cell in table.rows[0].cells:
            for paragraph in cell.paragraphs:
                _apply_to_paragraph(paragraph, {})
        template_row = table.rows[1]
        total_row = table.rows[-1]
        # SCS5 (Akainu M1) : chaque nouvelle ligne est inseree APRES la precedente (chainage
        # sur le dernier `tr` cree), sinon `addnext` sur le gabarit empile en LIFO et inverse
        # l'ordre des souscripteurs des 3 associes. Le 1er reutilise le gabarit.
        created_rows = [template_row]
        last_tr = template_row._tr
        for _ in associes[1:]:
            new_tr = copy.deepcopy(template_row._tr)
            last_tr.addnext(new_tr)
            last_tr = new_tr
            created_rows.append(_Row(new_tr, table))

        for associe, row in zip(associes, created_rows, strict=True):
            if associe.type_personne == "personne_morale":
                nom_ligne = _txt(associe.denomination)
                adresse = _siege_of_associe(associe)
            else:
                civilite = _txt(associe.civilite_affichage) or "Monsieur"
                nom_ligne = " ".join(
                    x for x in (civilite, _txt(associe.prenom), _txt(associe.nom)) if x
                )
                adresse = _txt(associe.adresse_personnelle_affichee)
            per = {
                "[civilite] [prenom] [nom]": nom_ligne,
                "[civilite]": "",
                "[prenom]": nom_ligne,
                "[nom]": "",
                "[adresse_personnelle]": adresse,
                "[nb_actions]": str(_associe_nb_parts(associe)),
                "[montant_sous]": _associe_montant(associe) or "0",
            }
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _apply_to_paragraph(paragraph, per)
        # Ligne TOTAL : total parts + total montant.
        total_repl = {"[nb_actions]": str(total_parts), "[montant_sous]": str(total_montant)}
        for cell in total_row.cells:
            for paragraph in cell.paragraphs:
                _apply_to_paragraph(paragraph, total_repl)

    @staticmethod
    def _assert_no_residual(document) -> None:
        texts = [p.text for p in document.paragraphs]
        texts += [
            cell.text
            for table in document.tables
            for row in table.rows
            for cell in row.cells
        ]
        full = "\n".join(texts)
        if "[" in full or "]" in full:
            residual = re.findall(r"\[[^\]]+\]", full)
            raise ValueError(f"placeholder source residuel dans {OUTPUT_FILENAME}: {residual}")


def _txt(value: object) -> str:
    return str(value or "").strip()


def _siege(company) -> str:
    if company is None or company.siege is None:
        return ""
    siege = company.siege
    if siege.adresse_affichee:
        return siege.adresse_affichee.strip()
    voie = f"{_txt(siege.num_voie)} {_txt(siege.voie)}".strip()
    return f"{voie}, {_txt(siege.cp)} {_txt(siege.ville)}".strip(" ,")


def _date(signature) -> str:
    if signature is None or signature.date is None:
        return ""
    value = signature.date
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value)
