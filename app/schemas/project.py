from typing import List, Union

from pydantic import BaseModel, Field

from app.schemas.section import Section


class ProjectBase(BaseModel):
    name: str = Field(..., description="Project name")
    color_icon: str = Field(..., description="Project color icon")
    is_favorite: bool = Field(default=False, description="Check if project is favorite")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Union[str, None] = Field(None, description="Project name")
    color_icon: Union[str, None] = Field(None, description="Project color icon")
    is_favorite: Union[bool, None] = Field(
        None, description="Check if project is favorite"
    )


class Project(ProjectBase):
    project_id: int
    user_id: int
    sections: List[Section] = Field(default=[], description="User's sections")

    class Config:
        orm_mode = True
