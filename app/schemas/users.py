from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from schemas.tasks import Task


# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str]
    email: EmailStr


# Properties to receive via API on update
class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserInDB):
    user_id: int
    is_active: bool
    items: List[Task] = Field(default=[], description="User's tasks")
