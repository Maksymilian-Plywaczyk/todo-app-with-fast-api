from pydantic import BaseModel, EmailStr
from typing import List, Optional


# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str]
    email: EmailStr


# Properites to receive via API on update
class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserInDB):
    id: int
    is_active: bool
    # items: List[Item] = []
    pass
