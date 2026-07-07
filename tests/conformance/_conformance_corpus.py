"""Corpus de conformité transverse — génération RÉELLE de tous les bundles.

Génère le bundle COMPLET de chaque type d'entreprise via les slices front réels
(``generate_dossier`` des slices), en RÉUTILISANT les payloads des tests front
existants (``test_multi_type_front`` / ``test_clean_front_app`` /
``test_sasu_holding_plan`` / ``test_statuts_micro_holding``) — jamais de payload
réinventé. Le corpus est un dict ``{type_key: {nom_doc: texte}}``.

La suite de conformité (``test_conformite_transverse.py``) applique ensuite les
règles transversales client (R1..R9) à CHAQUE document de CHAQUE type. Un retour
client codifié = une assertion permanente : il ne peut plus revenir silencieusement
sur aucun type.

NB chemins : ce module insère ``src`` et ``tests/unit`` dans ``sys.path`` pour
importer les payloads des tests unitaires par nom de module (même mécanique que la
collecte pytest en mode ``prepend``).
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
for _p in (str(_ROOT / "src"), str(_ROOT / "tests" / "unit")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from docx import Document  # noqa: E402


def docx_text(path: Path) -> str:
    """Texte intégral d'un DOCX : paragraphes + tables + en-têtes + pieds de page."""
    document = Document(path)
    texts = [p.text for p in document.paragraphs if p.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(p.text for p in cell.paragraphs if p.text)
    for section in document.sections:
        texts.extend(p.text for p in section.header.paragraphs if p.text)
        texts.extend(p.text for p in section.footer.paragraphs if p.text)
    return "\n".join(texts)


def _bundle(generated) -> dict[str, str]:
    return {p.name: docx_text(p) for p in generated.docx_paths}


# Ordre stable des types du corpus (sert à la paramétrisation pytest — PAS de
# génération à la collecte : la liste est statique, le corpus est bâti en fixture).
CORPUS_KEYS: tuple[str, ...] = (
    "selarl",
    "selarl_regime",
    "selarl_cession_medical",
    "selarl_cession_dentaire",
    "selarl_cession_scm",
    "selas_multi",
    "selas_multi_phys",
    "selas_uni_medecin",
    "selas_uni_dentiste",
    "spfpl_cession",
    # Variante valeur nominale = 1 € (surface R6 : « actions de un euro »), bundle
    # restreint aux statuts pour ne pas dupliquer les autres cellules du type.
    "spfpl_cession_vn1",
    "spfpl_apport",
    "sas",
    "sasu_holding",
    "sci",
    "sci_iris",
    "scm",
    "scs",
    "micro_holding",
)


def _normalise_civil(payload: dict) -> dict:
    """Aligne le payload civil des tests sur ce que l'UI RÉELLE envoie.

    Les payloads unitaires portent des raccourcis non représentatifs qui parasiteraient
    la conformité (R4) sans révéler de défaut GÉNÉRATEUR :
    - ``forme_sociale`` saisi « societe civile » (non accentué) alors que le formulaire
      la DÉRIVE (§18.1, ``civil_forme_sociale`` → « société civile ») → on retire la clé
      pour exercer la dérivation réelle ;
    - ``nationalite``/``situation_maritale`` des associés : l'UI réelle passe par des
      dérivations accentuées (``render_nationalite_selectbox`` → « française » ;
      ``_situation_display_civil`` → « célibataire ») — jamais la forme nue non accentuée.
    """
    payload.pop("forme_sociale", None)
    for associe in payload["associes"]:
        if associe.type_personne == "personne_physique":
            associe.nationalite = "française"
            associe.situation_maritale = "célibataire"
    return payload


def build_corpus(base_dir: Path) -> dict[str, dict[str, str]]:  # noqa: C901 - assemblage séquentiel de 19 bundles, pas de logique
    """Génère une fois le bundle de chaque type et retourne {type: {doc: texte}}."""
    # Imports différés : payloads des tests front existants (réutilisés tels quels).
    import test_clean_front_app as cfa
    import test_multi_type_front as mtf
    import test_sasu_holding_plan as sasu_tests
    import test_statuts_micro_holding as micro_tests

    from sydel_doc_engine.front_app import (
        civil_statuts_slice as css,
    )
    from sydel_doc_engine.front_app import (
        sas_slice,
        sasu_holding_slice,
        selas_multi_slice,
        spfpl_slice,
    )
    from sydel_doc_engine.front_app import (
        selas_uni_dentiste_slice as sd,
    )
    from sydel_doc_engine.front_app import (
        selas_uni_medecin_slice as sm,
    )
    from sydel_doc_engine.front_app.selarl_slice import (
        PROFESSION_MEDECIN,
        generate_selarl_dossier,
    )
    from sydel_doc_engine.scenarios.selarl import build_selarl_scenario

    corpus: dict[str, dict[str, str]] = {}

    # --- SELARL (chemin historique dédié) --------------------------------------
    # ``siege_voie`` du payload de test vaut « avenue du Siege » (non accentué) : pur
    # artefact d'adresse de test qui parasiterait R4 — on nomme une voie neutre.
    selarl_overrides = {"siege_voie": "avenue de Breteuil"}
    corpus["selarl"] = _bundle(
        generate_selarl_dossier(
            cfa._valid_selarl_input(PROFESSION_MEDECIN, **selarl_overrides),
            base_dir / "selarl",
        )
    )
    # Régime communautaire : ajoute lettre de renonciation + avertissement conjoint.
    corpus["selarl_regime"] = _bundle(
        generate_selarl_dossier(
            cfa._valid_selarl_input(
                PROFESSION_MEDECIN, regime_communautaire=True, **selarl_overrides
            ),
            base_dir / "selarl_regime",
        )
    )
    # Cessions (scénarios figés du moteur) : actes + bail + appel de fonds + docs SCM.
    # Normalisation d'artefacts de fixture (couche SOUS l'UI réelle) :
    # - ``siege_voie`` du scénario vaut « avenue du Siege » (adresse de test non
    #   accentuée) → voie neutre ;
    # - le cédant SCM du scénario porte « francaise » / « marie » nus alors que le
    #   chemin UI réel dérive des libellés accentués (``_scm_cedant_situation_
    #   maritale_display``, O24-11) — le scénario, lui, court-circuite la dérivation.
    def _selarl_scenario_ui(key: str):
        import dataclasses

        data = dataclasses.replace(build_selarl_scenario(key), siege_voie="avenue de Breteuil")
        if data.scm_cession_context is not None:
            data.scm_cession_context.cedant.nationalite = "française"
            data.scm_cession_context.cedant.situation_maritale = "marié"
        return data

    corpus["selarl_cession_medical"] = _bundle(
        generate_selarl_dossier(
            _selarl_scenario_ui("selarl_medecin_cession_cabinet_medical"),
            base_dir / "selarl_cession_medical",
        )
    )
    corpus["selarl_cession_dentaire"] = _bundle(
        generate_selarl_dossier(
            _selarl_scenario_ui("selarl_dentiste_cession_cabinet_dentaire"),
            base_dir / "selarl_cession_dentaire",
        )
    )
    corpus["selarl_cession_scm"] = _bundle(
        generate_selarl_dossier(
            _selarl_scenario_ui("selarl_dentiste_cession_scm"),
            base_dir / "selarl_cession_scm",
        )
    )

    # --- SELAS pluripersonnelle -------------------------------------------------
    # Variante mixte (1 physique + 1 personne morale) : chemin identité morale.
    corpus["selas_multi"] = _bundle(
        selas_multi_slice.generate_dossier(mtf._selas_payload(), base_dir / "selas_multi")
    )
    # Variante entièrement physique : ajoute l'attestation souscripteurs (DOC-045).
    corpus["selas_multi_phys"] = _bundle(
        selas_multi_slice.generate_dossier(
            mtf._selas_payload_n(
                [mtf._selas_phys("Claire", "Durand", 60), mtf._selas_phys("Paul", "Martin", 40)]
            ),
            base_dir / "selas_multi_phys",
        )
    )

    # --- SELAS unipersonnelles (médecin / dentiste) ------------------------------
    corpus["selas_uni_medecin"] = _bundle(
        sm.generate_dossier(mtf._selas_uni_payload(), base_dir / "selas_uni_medecin")
    )
    corpus["selas_uni_dentiste"] = _bundle(
        sd.generate_dossier(mtf._selas_uni_payload(), base_dir / "selas_uni_dentiste")
    )

    # --- SPFPL dentistes (cession + apport) --------------------------------------
    def _spfpl_payload_ui(structure: str) -> dict:
        # L'UI réelle sert la nationalité par déroulant accentué (« française ») et la
        # forme complète de la cible est une saisie dont la forme représentative est
        # accentuée — le payload de test porte des raccourcis non accentués qui
        # parasiteraient R4 sans révéler de défaut générateur.
        payload = mtf._spfpl_payload(structure)
        payload["nationalite"] = "française"
        payload["cession_data"] = {
            **payload["cession_data"],
            "cible_forme_complete": "société d'exercice libéral à responsabilité limitée",
        }
        return payload

    corpus["spfpl_cession"] = _bundle(
        spfpl_slice.generate_dossier(_spfpl_payload_ui("SPFPL cession"), base_dir / "spfpl_cession")
    )
    corpus["spfpl_apport"] = _bundle(
        spfpl_slice.generate_dossier(_spfpl_payload_ui("SPFPL apport"), base_dir / "spfpl_apport")
    )
    # Variante valeur nominale = 1 € : surface du retour élision (« actions de un
    # euro » attendu « d'un euro », R6). Bundle restreint aux STATUTS : les autres
    # documents dupliqueraient les cellules du type spfpl_cession sans rien prouver.
    vn1_payload = _spfpl_payload_ui("SPFPL cession")
    vn1_payload.update(
        {"capital_social": "600", "nb_actions_total": 600, "valeur_nominale_action": "1"}
    )
    corpus["spfpl_cession_vn1"] = {
        name: text
        for name, text in _bundle(
            spfpl_slice.generate_dossier(vn1_payload, base_dir / "spfpl_cession_vn1")
        ).items()
        if name == "statuts_spfpl_cession.docx"
    }

    # --- SAS (SPFPL médecins forme SAS) + SASU holding ---------------------------
    # Même normalisation nationalité (déroulant accentué dans l'UI réelle).
    sas_payload = dict(mtf._sas_payload())
    sas_payload["nationalite"] = "française"
    corpus["sas"] = _bundle(sas_slice.generate_dossier(sas_payload, base_dir / "sas"))
    corpus["sasu_holding"] = _bundle(
        sasu_holding_slice.generate_dossier(sasu_tests._payload(), base_dir / "sasu_holding")
    )

    # --- Types civils (socle partagé) ---------------------------------------------
    sci_payload = mtf._civil_base(
        "SCI",
        "sci",
        [
            mtf._pp("Jean", "Durand", 40, 1, 40, 400),
            mtf._pp("Alice", "Martin", 60, 41, 100, 600),
        ],
    )
    # Option IS activée : la lettre d'option IS (DOC-022) entre dans le bundle scanné.
    sci_payload.update(mtf._OPTION_IS_INPUTS)
    corpus["sci"] = _bundle(css.generate_dossier(_normalise_civil(sci_payload), base_dir / "sci"))

    corpus["sci_iris"] = _bundle(
        css.generate_dossier(
            _normalise_civil(
                mtf._civil_base(
                    "SCI IRIS",
                    "sci_iris",
                    [mtf._pm(40, 1, 40, 400), mtf._pp("Alice", "Martin", 60, 41, 100, 600)],
                )
            ),
            base_dir / "sci_iris",
        )
    )

    # SCM à 2 associés physiques + inter-SEL actif : bundle maximal (statuts + demande
    # ordre + pacte + liste dépenses + contrat frais communs + règlement intérieur).
    scm_payload = mtf._civil_base(
        "SCM",
        "scm",
        [
            mtf._pp("Jean", "Durand", 50, 1, 50, 500),
            mtf._pp("Alice", "Martin", 50, 51, 100, 500),
        ],
    )
    scm_payload.update(mtf._SCM_INTER_SEL_INPUTS)
    corpus["scm"] = _bundle(css.generate_dossier(_normalise_civil(scm_payload), base_dir / "scm"))

    corpus["scs"] = _bundle(
        css.generate_dossier(
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
            base_dir / "scs",
        )
    )

    # Le payload micro holding des tests statuts ne porte pas les saisies du tronc
    # commun (DNC / procuration) : on les complète comme le fait le formulaire réel
    # (mêmes champs que ``_civil_base`` de test_multi_type_front).
    micro_payload = micro_tests._payload()
    micro_payload.update(
        {
            "signataire_nom_pere": "Pierre Durand",
            "signataire_nom_mere": "Anne Durand",
            "signataire_adresse_num": "1",
            "signataire_adresse_voie": "rue Exemple",
            "signataire_adresse_cp": "75000",
            "signataire_adresse_ville": "Paris",
            "signataire_fonction": "gerant",
        }
    )
    corpus["micro_holding"] = _bundle(
        css.generate_dossier(micro_payload, base_dir / "micro_holding")
    )

    missing = set(CORPUS_KEYS) - set(corpus)
    if missing:  # défense : la liste statique et le bâtisseur doivent rester alignés
        raise RuntimeError(f"types du corpus non générés : {sorted(missing)}")
    return corpus
