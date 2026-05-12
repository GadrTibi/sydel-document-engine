from __future__ import annotations

from enum import StrEnum


class Gender(StrEnum):
    MASCULIN = "masculin"
    FEMININ = "feminin"


class DocumentCategory(StrEnum):
    UNIVERSEL = "universel"
    MUTUALISABLE = "mutualisable"
    VARIANTE = "variante"
    SPECIFIQUE = "specifique"


class WorkflowStatus(StrEnum):
    INVENTORIE = "inventorie"
    VALIDE = "valide"
    SOURCE_RECUE = "source_recue"
    ANALYSE = "analyse"
    SPECIFIE = "specifie"
    CODE = "code"
    TESTE = "teste"
    VALIDE_FINAL = "valide_final"