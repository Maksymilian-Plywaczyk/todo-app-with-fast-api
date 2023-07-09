from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.project import Project
from app.schemas.section import Section
from app.schemas.tasks import Task


# Shared properties
class UserBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# Properties to receive via API on update
class UserCreate(UserBase):
    email: EmailStr = Field(..., description="Email must be provided")
    password: str


class UserInDB(UserBase):
    user_id: int
    hashed_password: str
    projects: List[Project] = Field(default=[], description="User's projects")
    tasks: List[Task] = Field(default=[], description="User's tasks")
    sections: List[Section] = Field(default=[], description="User's sections")

    class Config:
        orm_mode = True


class User(UserInDB):
    pass
