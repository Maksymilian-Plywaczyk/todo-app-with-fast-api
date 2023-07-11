from datetime import datetime
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.security import ALGORITH, SECRET_KEY
from app.crud.users import get_user_by_email
from app.db.database import SessionLocal
from app.schemas.token import TokenPayload


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="api/v1/token")


def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
):
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
