from pydantic import BaseModel, Field


class SectionBase(BaseModel):
    order: int = Field(..., description="Section order")
    name: str = Field(..., description="Section name")


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class Section(SectionBase):
    section_id: int
    project_id: int
    owner_id: int
