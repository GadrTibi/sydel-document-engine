from __future__ import annotations

from pydantic import BaseModel, Field

from sydel_doc_engine.domain.enums import DocumentCategory, WorkflowStatus


class DocumentDefinition(BaseModel):
    doc_id: str
    canonical_name: str
    generator_name: str
    lot: int
    category: DocumentCategory
    structures: list[str]
    general_condition: str
    specific_conditions: list[str] = Field(default_factory=list)
    dynamic_associates: bool = False
    grammar_variants: bool = False
    out_of_scope_initial: bool = False
    workflow_status: WorkflowStatus
    source_path: str | None = None
    specification_path: str | None = None
    notes: str | None = None
