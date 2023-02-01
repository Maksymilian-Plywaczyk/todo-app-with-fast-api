from core.security import create_access_token, verify_password
from crud.users import get_user_by_email
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from routers.tags import Tags
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
    return {"access_token": create_access_token(user.email), "token_type": "bearer"}
