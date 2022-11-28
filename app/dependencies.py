from typing import Generator, Union
from db.database import SessionLocal
from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from core.security import SECRET_KEY, ALGORITH
from jose import jwt
from pydantic import ValidationError
from schemas.user import UserCreate
from schemas.token import TokenPayload
from crud.user import get_user_by_email


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH])
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(db=db, user_email=token_data.subject)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user
