from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    email: str
    token_type: str


class TokenPayload(BaseModel):
    email: str = None
    exp: int = None
