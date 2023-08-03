from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.project import Project


class UserBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    email: EmailStr = Field(..., description="Email must be provided")
    password: str
    is_active: bool = Field(default=True, description="User's status")


class UserInDB(UserBase):
    user_id: int
    hashed_password: str
    projects: List[Project] = Field(default=[], description="User's projects")

    class Config:
        orm_mode = True


class User(UserInDB):
    pass
