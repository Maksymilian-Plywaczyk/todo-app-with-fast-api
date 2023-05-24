from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_hashed_password,
    verify_reset_password_token,
)
from app.crud.users import get_user_by_email, user_authentication, user_is_active
from app.dependencies import get_db
from app.routers.utils.tags import Tags
from app.schemas.msg import Msg
from app.schemas.token import Token

router = APIRouter()


@router.post("/token", response_model=Token, tags=[Tags.login])
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = user_authentication(
        db=db, user_email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=30)
    return {
        "access_token": create_access_token(
            subject=user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/reset-password/", tags=[Tags.reset_password], response_model=Msg)
def reset_user_password(
    token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)
):
    email = verify_reset_password_token(token=token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    user = get_user_by_email(db=db, user_email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif not user_is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active."
        )
    hashed_password = get_hashed_password(plain_password=new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    db.close()
    return {"message": "Password updated successfully"}
