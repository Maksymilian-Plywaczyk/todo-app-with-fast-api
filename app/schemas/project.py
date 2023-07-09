from pydantic import BaseModel, Field

from app.schemas.colors import ColorBase


class ProjectBase(BaseModel):
    name: str = Field(..., description="Project name")
    color_icon: ColorBase = Field(..., description="Project color icon")
    is_favorite: bool = Field(default=False, description="Check if project is favorite")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    project_id: int
    user_id: int

    class Config:
        orm_mode = True
