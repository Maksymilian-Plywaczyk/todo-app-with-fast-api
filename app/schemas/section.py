from typing import List, Union

from pydantic import BaseModel, Field

from app.schemas.tasks import Task


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
    tasks: List[Task] = Field(default=[], description="User's tasks")

    class Config:
        orm_mode = True
