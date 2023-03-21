from typing import Any

from core.security import (
    create_access_token,
    get_hashed_password,
    verify_password,
    verify_reset_password_token,
)
from crud.users import get_user_by_email, user_is_active
from dependencies import get_db
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from routers.utils.tags import Tags
from schemas.msg import Msg
from schemas.token import Token
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/login/",
    summary="Create access token for user",
    response_model=Token,
    tags=[Tags.login],
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = get_user_by_email(db=db, user_email=form_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not verify_password(form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return {"email": create_access_token(user.email), "token_type": "bearer"}


@router.post("/reset-password/", tags=[Tags.reset_password])
def reset_user_password(
    token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)
):
    """
    RESET USER PASSWORD
    """
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
    return {"msg": "Password updated successfully"}
