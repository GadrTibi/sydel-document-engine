import sys, os; sys.path.insert(0, os.path.abspath("src"))

import re
import tempfile
from pathlib import Path
from docx import Document

import _audit_selas_coherence as base
from sydel_doc_engine.front_app import selas_multi_slice as slc


def docx_text(path):
    document = Document(str(path))
    parts = [p.text for p in document.paragraphs if p.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.extend(p.text for p in cell.paragraphs if p.text)
    return "\n".join(parts)


def main():
    out = Path(tempfile.mkdtemp(prefix="selas_x_", dir="."))
    dossier = slc.generate_dossier(base.payload, out)
    texts = {Path(p).name: docx_text(p) for p in dossier.docx_paths}

    # --- Extraction de VALEURS effectivement presentes (pas seulement attendues) ---
    # On cherche TOUTE forme alternative qui contredirait la valeur canonique.
    print("==== MONTANTS (tout nombre >=4 chiffres groupes) PAR DOC ====")
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        montants = re.findall(r"\b\d{1,3}(?:[  ]\d{3})+\b", norm)
        montants = sorted(set(montants))
        print(f"  {name:46} {montants}")

    print("\n==== DENOMINATION : variantes du nom de societe ====")
    canon = base.DENOMINATION
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        has_canon = canon in norm
        # variantes possibles : 'SELAS' suivi de mots majuscules
        variantes = re.findall(r"SELAS[ A-ZÉÈÀ'’-]{4,60}", norm)
        variantes = sorted(set(v.strip() for v in variantes))
        print(f"  {name:46} canon={has_canon} variantes={variantes}")

    print("\n==== VILLE RCS : occurrences 'RCS' + ville ====")
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        rcs = re.findall(r"(?:RCS|Registre du Commerce)[^.\n]{0,80}", norm)
        # ville isolee apres immatricul
        imm = re.findall(r"immatricul[^.\n]{0,80}", norm, re.IGNORECASE)
        print(f"  {name:46} RCS={rcs[:2]} IMM={imm[:1]}")

    print("\n==== PRESIDENT / GERANT : civilite+prenom+nom ====")
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        # cherche Claire / Durand et toute autre paire prenom-nom majuscule
        claire = "Claire" in norm
        durand = base.PRES_NOM in norm
        # autres noms propres associes
        marie = "Marie" in norm
        lefevre = "Lefevre" in norm
        paul = "Paul" in norm
        print(f"  {name:46} Claire={claire} Durand={durand} Marie={marie} Lefevre={lefevre} Paul={paul}")

    print("\n==== SIEGE : adresse affichee ====")
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        tilleuls = "rue des Tilleuls" in norm
        cp33 = "33000" in norm
        # adresse du president (ne doit pas etre confondue avec le siege)
        republique = "Republique" in norm or "République" in norm
        print(f"  {name:46} siege_Tilleuls={tilleuls} cp33000={cp33} pres_Republique={republique}")

    print("\n==== NB ACTIONS / VALEUR NOMINALE ====")
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        a3300 = bool(re.search(r"3[  ]?300", norm))
        # valeur nominale 100
        vn = "100 euros" in norm or "100 €" in norm or "cent euros" in norm
        print(f"  {name:46} actions_3300={a3300} vn100={vn}")

    print("\n==== DATES (signature / cloture) ====")
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        d2026 = "2026" in norm
        d2027 = "2027" in norm
        sept = "septembre" in norm or "15/09/2026" in norm
        dec27 = "31 décembre 2027" in norm or "31/12/2027" in norm
        print(f"  {name:46} 2026={d2026} 2027={d2027} sept2026={sept} cloture31dec27={dec27}")


if __name__ == "__main__":
    main()
