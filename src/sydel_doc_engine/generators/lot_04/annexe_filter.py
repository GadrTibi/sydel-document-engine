"""Filtre partagé de l'annexe des statuts — golden bloc (O24-01).

Appelé par TOUTES les boucles de rendu de statuts (statuts_civils_common,
statuts_selas_multi, statuts_scm) pour garantir le même comportement partout.
"""

from __future__ import annotations


def is_creation_fee_annexe_line(text: str) -> bool:
    """O24-01 (onglet 24) : les 2 items « Signature d'une lettre de mission … » et
    « Paiement de l'acompte des honoraires … » du cabinet de création doivent être
    retirés de l'ANNEXE de TOUS les statuts (« tous les statuts de tous les cas »).

    Détecté par STRUCTURE, pas par la chaîne « Sydel » : certains modèles (ex. SCS)
    utilisent un placeholder de cabinet mandataire au lieu de « Sydel ».
    """
    low = (text or "").casefold()
    if "lettre de mission" in low and "cabinet" in low:
        return True
    if "acompte des honoraires" in low:
        return True
    return False
