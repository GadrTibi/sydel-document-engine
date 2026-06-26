"""Registre central des types d'entreprise selectionnables au front.

C'est la SOURCE DE VERITE de ce que la deroulante `dossier_selection` propose et
de la facon dont `shell` route la saisie + la generation. Auto-extensible : pour
ajouter un type, on enregistre une `RegisteredType` ici (label, structure, module
de slice) sans toucher au reste du front.

Garde-fou SELARL : l'entree SELARL est conservee a l'identique, en PREMIERE
position, structure `SELARL`, generation activee. Le front SELARL existant
(valide client) continue de passer par son chemin dedie (`selarl_slice`) ; le
registre ne fait que le declarer comme premiere option.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class RegisteredType:
    """Un type d'entreprise expose au front.

    - ``key`` : cle stable (clé de session / routing).
    - ``label`` : libelle affiche dans la deroulante.
    - ``structure`` : structure metier (route le moteur ; SELARL conserve sa
      valeur historique).
    - ``slice_module`` : module ``front_app.<...>_slice`` portant le rendu + la
      generation du type. ``None`` pour SELARL (chemin historique dedie).
    - ``generation_enabled`` : la generation reelle est-elle ouverte ?
    - ``status`` : etiquette d'etat (informative).
    """

    key: str
    label: str
    structure: str
    slice_module: str | None
    generation_enabled: bool
    status: str


# Ordre = ordre d'affichage. SELARL TOUJOURS en premier (defaut historique).
REGISTERED_TYPES: Final[tuple[RegisteredType, ...]] = (
    RegisteredType(
        key="selarl_v1",
        label="SELARL creation V1",
        structure="SELARL",
        slice_module=None,
        generation_enabled=True,
        status="bounded_vertical_slice",
    ),
    RegisteredType(
        key="scm_v1",
        label="SCM creation V1",
        structure="SCM",
        slice_module="sydel_doc_engine.front_app.scm_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    RegisteredType(
        key="sci_v1",
        label="SCI creation V1",
        structure="SCI",
        slice_module="sydel_doc_engine.front_app.sci_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    RegisteredType(
        key="sci_iris_v1",
        label="SCI IRIS creation V1",
        structure="SCI IRIS",
        slice_module="sydel_doc_engine.front_app.sci_iris_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    RegisteredType(
        key="scs_v1",
        label="SCS creation V1",
        structure="SCS",
        slice_module="sydel_doc_engine.front_app.scs_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    # Libelles SPFPL clarifies (audit retours Albane lot 2, §17.4) : la deroulante
    # melait « SAS SPFPL medecins », « SPFPL cession » et « SPFPL apport » sans dire
    # ni la FORME ni la PROFESSION, d'ou une confusion + un faux doublon. Les
    # libelles ci-dessous refletent STRICTEMENT ce que le code produit aujourd'hui
    # (factuel, pas une decision metier) : la SAS = SPFPL medecins (forme SAS,
    # DOC-015) ; cession/apport = corpus dentiste (profession figee
    # « chirurgien-dentiste » dans spfpl_slice). Le routing utilise key/structure,
    # pas le label -> renommage purement cosmetique. La question metier « apport /
    # cession ouverts aux medecins ? » reste hors code (arbitrage Albane), non
    # tranchee ici.
    RegisteredType(
        key="sas_spfpl_medecins_v1",
        label="SPFPL medecins (forme SAS) creation V1",
        structure="SAS",
        slice_module="sydel_doc_engine.front_app.sas_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    RegisteredType(
        key="spfpl_cession_v1",
        label="SPFPL dentistes - cession creation V1",
        structure="SPFPL cession",
        slice_module="sydel_doc_engine.front_app.spfpl_cession_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    RegisteredType(
        key="spfpl_apport_v1",
        label="SPFPL dentistes - apport creation V1",
        structure="SPFPL apport",
        slice_module="sydel_doc_engine.front_app.spfpl_apport_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    # Retours Rafael 2026-06-23 : un SEUL cas SELAS pluripersonnelle (la profession
    # est choisie DANS le cas -> plus de « dentiste » dans le nom). L'ancien
    # « SELAS multi-associes creation V1 » est supprime ; l'ancien « SELAS dentiste
    # pluripersonnelle » est fusionne ici. La cle interne reste `selas_multi_v1`
    # (deja en profession libre, corpus dentiste/medecin pilote par la profession).
    RegisteredType(
        key="selas_multi_v1",
        label="SELAS pluripersonnelle creation V1",
        structure="SELAS",
        slice_module="sydel_doc_engine.front_app.selas_multi_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    # Cas NOMME « SELAS unipersonnelle medecin » : rebranche le generateur DOC-018
    # (statuts SELAS medecin from-scratch) qui existait cote moteur mais restait
    # orphelin (aucun parcours front — audit retours Albane lot 2, §17.1). Slice
    # dedie unipersonnel (1 associe / President), structure de routage distincte de
    # la SELAS multi pour ne pas detourner le chemin DOC-044 (>=2 associes).
    RegisteredType(
        key="selas_uni_medecin_v1",
        label="SELAS unipersonnelle medecin creation V1",
        structure="SELAS uni medecin",
        slice_module="sydel_doc_engine.front_app.selas_uni_medecin_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
    # Cas NOMME « SELAS unipersonnelle dentiste » (retour Rafael #5 : « la SELAS
    # unipers dentiste = la pluripersonnelle dentiste mais avec un seul associe »).
    # Clone structurel du parcours SELAS uni medecin, profession chirurgien-dentiste,
    # statuts DOC-046 (blocs dentiste verbatim du modele pluri uni-fie). Structure de
    # routage dediee, distincte de la SELAS uni medecin et de la SELAS pluri.
    RegisteredType(
        key="selas_uni_dentiste_v1",
        label="SELAS unipersonnelle dentiste creation V1",
        structure="SELAS uni dentiste",
        slice_module="sydel_doc_engine.front_app.selas_uni_dentiste_slice",
        generation_enabled=True,
        status="moteur_teste",
    ),
)


def registered_types() -> tuple[RegisteredType, ...]:
    return REGISTERED_TYPES


def registered_type_by_key(key: str) -> RegisteredType:
    for item in REGISTERED_TYPES:
        if item.key == key:
            return item
    raise KeyError(f"Unknown registered type: {key}")
