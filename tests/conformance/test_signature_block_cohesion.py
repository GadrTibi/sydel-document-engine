"""M4 (KAN-36) — Garde de conformité : le bloc signature reste solidaire (une seule page).

Génère un échantillon RÉEL de documents SIGNÉS via les slices front réels — MÊMES
payloads que les tests unitaires (aucun payload réinventé) — couvrant :

  * statuts SELAS multi, statuts SCM, statuts SCS, statuts SASU holding ;
  * PV agrément SPFPL plusieurs associés, acte cession parts SPFPL ;
  * acte + compromis cession cabinet, appel de fonds, note d'information ;
  * attestations, autorisation de domiciliation, procurations, DNC, PV.

Pour chaque document qui porte un INDICATEUR de signature (« Fait à » / « Fait a » /
« signé après lecture » / « dressé le présent procès-verbal » / « Bon pour » /
« Lu et approuvé » / une table de signature), la garde vérifie que la protection
KAN-36 est appliquée : au moins un paragraphe `keep_with_next` (helper
``keep_final_signature_block_together``) OU au moins une ligne de table `cantSplit`
(helper ``keep_signature_block_together`` pour les grilles de signature). Un document
signé SANS protection => échec listant le(s) document(s).

Exécutable en CI sans Word ni rendu PDF : on inspecte les propriétés de pagination
directement dans le DOCX (python-docx / OOXML).
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest
from docx import Document

# Indicateurs texte de « document signé » (paragraphes OU cellules de table).
SIGNATURE_MARKERS: tuple[str, ...] = (
    "Fait à",
    "Fait a",
    "signé après lecture",
    "dressé le présent procès-verbal",
    "Bon pour",
    "Lu et approuvé",
)

# Documents SIGNÉS dont le bloc signature est une TABLE de cases NON encore couverte :
# le helper PARAGRAPHE (keep_final_signature_block_together) ne pose rien d'utile
# (« Fait à » est le dernier paragraphe, les signataires sont dans une table), et le
# helper TABLE (keep_signature_block_together) n'est pas encore câblé sur leur table.
# Trous CORRIGÉS le 2026-07-16 (re-Akainu KAN-36) — plus aucune exclusion :
#   - avenant_contrat_bail.py : câblé au helper TABLE keep_signature_block_together (cantSplit) ;
#   - pacte_associes_scm.py + tous les satellites SCM : keep_final_signature_block_together posé
#     dans generate_from_template (scm_satellites_common) ;
#   - lettres/note sans starter (note_information, demande_inscription_ordre, appel_fond_sel) :
#     le fallback « queue de document » du helper les couvre désormais.
KNOWN_SIGNATURE_GAPS: frozenset[str] = frozenset()

# NB — les lettres/note SANS starter (« note_information », « demande_inscription_ordre »,
# « appel_fond_sel ») ne portent AUCUN indicateur de la liste ci-dessus : leur clôture est
# une formule de politesse + nom (pas de « Fait à »). Elles ne sont donc pas détectées
# comme « signées » par cette garde et ne sont pas asserties. Le détecteur du helper
# gagnerait à reconnaître ces clôtures ; en l'état le câblage KAN-36 y est un no-op inoffensif.


def _full_text(path: Path) -> str:
    document = Document(str(path))
    parts = [p.text for p in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.extend(p.text for p in cell.paragraphs)
    return "\n".join(parts)


def _is_signed(path: Path) -> bool:
    return any(marker in _full_text(path) for marker in SIGNATURE_MARKERS)


def _has_kan36_protection(path: Path) -> bool:
    """Protection KAN-36 présente ? keepNext (paragraphe) OU cantSplit (ligne de table)."""
    document = Document(str(path))
    if any(p.paragraph_format.keep_with_next for p in document.paragraphs):
        return True
    for table in document.tables:
        for row in table.rows:
            if row._tr.xpath("./w:trPr/w:cantSplit"):  # noqa: SLF001 - accès OOXML python-docx
                return True
    return False


def _generate_sample(base: Path) -> list[Path]:
    """Bundles RÉELS via les slices front (payloads = ceux des tests unitaires)."""
    import test_multi_type_front as mtf
    import test_sasu_holding_plan as sasu_tests
    from _conformance_corpus import _normalise_civil

    from sydel_doc_engine.front_app import (
        civil_statuts_slice as css,
    )
    from sydel_doc_engine.front_app import (
        sasu_holding_slice,
        selas_multi_slice,
        spfpl_slice,
    )
    from sydel_doc_engine.front_app.selarl_slice import generate_selarl_dossier
    from sydel_doc_engine.scenarios.selarl import build_selarl_scenario

    paths: list[Path] = []

    # SELAS pluripersonnelle physique : statuts SELAS multi + attestation souscripteurs
    # SELAS + PV nomination + procuration + DNC + demande inscription + autorisation.
    paths += selas_multi_slice.generate_dossier(
        mtf._selas_payload_n(
            [mtf._selas_phys("Claire", "Durand", 60), mtf._selas_phys("Paul", "Martin", 40)]
        ),
        base / "selas_multi",
    ).docx_paths

    # SPFPL cession : note d'information + PV agrément plusieurs associés + acte cession
    # parts SPFPL + attestation capital/liste souscripteurs + statuts SPFPL.
    spfpl_payload = mtf._spfpl_payload("SPFPL cession")
    spfpl_payload["nationalite"] = "française"
    spfpl_payload["cession_data"] = {
        **spfpl_payload["cession_data"],
        "cible_forme_complete": "société d'exercice libéral à responsabilité limitée",
    }
    paths += spfpl_slice.generate_dossier(spfpl_payload, base / "spfpl_cession").docx_paths

    # SCM : statuts SCM (bloc signature paragraphe) + autorisation + demande inscription +
    # pacte associés SCM (bloc signature en TABLE — trou connu).
    paths += css.generate_dossier(
        _normalise_civil(
            mtf._civil_base(
                "SCM",
                "scm",
                [
                    mtf._pp("Jean", "Durand", 50, 1, 50, 500),
                    mtf._pp("Alice", "Martin", 50, 51, 100, 500),
                ],
            )
        ),
        base / "scm",
    ).docx_paths

    # SCS : liste des souscripteurs SCS + statuts SCS (bloc signature en grille protégée
    # par cantSplit).
    paths += css.generate_dossier(
        _normalise_civil(
            mtf._civil_base(
                "SCS",
                "scs",
                [
                    mtf._pp("Jean", "Durand", 60, 1, 60, 600, role="commandite"),
                    mtf._pp("Alice", "Martin", 40, 61, 100, 400, role="commanditaire"),
                ],
            )
        ),
        base / "scs",
    ).docx_paths

    # SELARL cession médicale : acte + compromis cession cabinet + appel de fonds +
    # avenant bail (table — trou connu) + demande inscription + statuts SELARL.
    scenario = dataclasses.replace(
        build_selarl_scenario("selarl_medecin_cession_cabinet_medical"),
        siege_voie="avenue de Breteuil",
    )
    if scenario.scm_cession_context is not None:
        scenario.scm_cession_context.cedant.nationalite = "française"
        scenario.scm_cession_context.cedant.situation_maritale = "marié"
    paths += generate_selarl_dossier(scenario, base / "selarl_cession").docx_paths

    # SASU holding : statuts SASU (« Fait à » paragraphe) + liste souscripteurs SASU +
    # PV rémunération président + autorisation + procuration + DNC.
    paths += sasu_holding_slice.generate_dossier(
        sasu_tests._payload(), base / "sasu_holding"
    ).docx_paths

    return paths


@pytest.fixture(scope="module")
def sample_signed_docs(tmp_path_factory: pytest.TempPathFactory) -> list[Path]:
    return _generate_sample(tmp_path_factory.mktemp("kan36_signature_cohesion"))


def test_signed_documents_apply_kan36_protection(sample_signed_docs: list[Path]) -> None:
    """Tout document signé (hors trous connus) porte la protection KAN-36."""
    checked = 0
    unprotected: list[str] = []
    for path in sample_signed_docs:
        if path.name in KNOWN_SIGNATURE_GAPS:
            continue
        if not _is_signed(path):
            continue
        checked += 1
        if not _has_kan36_protection(path):
            unprotected.append(path.name)

    # Garde-fou anti-garde-vide : l'échantillon DOIT exercer un volume réel de docs signés
    # (sinon un changement de génération rendrait la garde silencieusement inopérante).
    assert checked >= 15, (
        f"échantillon de documents signés trop maigre ({checked}) — la garde n'exerce plus rien."
    )
    assert not unprotected, (
        "Documents SIGNÉS sans protection KAN-36 (bloc signature scindable sur deux pages) : "
        + ", ".join(sorted(set(unprotected)))
        + ". Câbler keep_final_signature_block_together (bloc paragraphe) "
        "ou keep_signature_block_together (grille en table)."
    )


def test_pv_agrement_plusieurs_associes_b1_closing_block_kept_together(
    tmp_path: Path,
) -> None:
    """Cas B1 reproduit : PV agrément SPFPL avec 9 associés présents (noms longs).

    De la clôture (« … dressé le présent procès-verbal … signé après lecture … »)
    jusqu'à la fin, TOUS les paragraphes portent keepNext (le tout dernier exclu par
    construction du helper) — le bloc clôture + signataires reste sur une seule page.
    """
    import test_lot_05_spfpl_agrement_info as t

    from sydel_doc_engine.domain.models import AssocieCible
    from sydel_doc_engine.generators.lot_05.pv_agrement_cession_spfpl_plusieurs_associes import (
        PvAgrementCessionSpfplPlusieursAssociesGenerator,
    )

    ctx = t._plural_context()
    ctx.associes_cible = [
        AssocieCible(
            civilite_affichage="Docteur",
            prenom=f"Jean-Baptiste{i}",
            nom=f"de la Rochefoucauld-Montmorency{i}",
            nb_parts_avant=10,
            nb_parts_apres=10,
            plage_parts=f"{i * 10 + 1} a {i * 10 + 10}",
            est_present_ou_represente=True,
        )
        for i in range(9)
    ]

    output = PvAgrementCessionSpfplPlusieursAssociesGenerator().generate(ctx, tmp_path)
    paras = Document(str(output)).paragraphs

    closing = next(
        (
            i
            for i, p in enumerate(paras)
            if "signé après lecture" in p.text or "dressé le présent procès-verbal" in p.text
        ),
        None,
    )
    assert closing is not None, "clôture du PV (signé après lecture) introuvable"

    tail = paras[closing:-1]  # le helper pose keepNext sur [start:-1] (dernier exclu)
    assert tail, "aucun paragraphe entre la clôture et la fin du document"
    not_kept = [
        closing + offset
        for offset, p in enumerate(tail)
        if not p.paragraph_format.keep_with_next
    ]
    assert not not_kept, (
        f"paragraphes {not_kept} (clôture -> signataires) sans keepNext : le bloc signature "
        "du PV à 9 associés est scindable sur deux pages (régression cas B1)."
    )

    # 9 associés présents => au moins 9 paragraphes solidarisés (clôture + lignes de noms).
    kept = sum(1 for p in paras if p.paragraph_format.keep_with_next)
    assert kept >= 9, f"attendu >= 9 paragraphes keepNext (9 associés présents), obtenu {kept}"
