from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: EmailStr
    is_active: Optional[None] = None


# Properites to receive via API on update
class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    #items: List[Item] = []

    class Config:
        orm_mode = True
