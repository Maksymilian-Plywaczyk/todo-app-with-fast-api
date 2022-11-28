from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    subject: str = None
    exp: int = None
