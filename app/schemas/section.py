from typing import Union

from pydantic import BaseModel, Field


class SectionBase(BaseModel):
    order: int = Field(..., description="Section order")
    name: str = Field(..., description="Section name")


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    order: Union[int, None] = Field(None, description="Section order")
    name: Union[str, None] = Field(None, description="Section name")


class Section(SectionBase):
    section_id: int
    project_id: int
    owner_id: int

    class Config:
        orm_mode = True
