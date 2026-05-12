from __future__ import annotations

from enum import Enum


class Gender(str, Enum):
    MASCULIN = "masculin"
    FEMININ = "feminin"


class DocumentCategory(str, Enum):
    UNIVERSEL = "universel"
    MUTUALISABLE = "mutualisable"
    VARIANTE = "variante"
    SPECIFIQUE = "specifique"


class WorkflowStatus(str, Enum):
    INVENTORIE = "inventorie"
    VALIDE = "valide"
    SOURCE_RECUE = "source_recue"
    ANALYSE = "analyse"
    SPECIFIE = "specifie"
    CODE = "code"
    TESTE = "teste"
    VALIDE_FINAL = "valide_final"
