# TODO make a singup page
from crud.users import create_new_user, get_user_by_email
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from routers.utils.tags import Tags
from schemas.users import User, UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/signup/", summary="Create new user", response_model=User, tags=[Tags.register]
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    database_user = get_user_by_email(db=db, user_email=user.email)
    if database_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exist",
        )
    new_user = create_new_user(db=db, user=user)
    return new_user
