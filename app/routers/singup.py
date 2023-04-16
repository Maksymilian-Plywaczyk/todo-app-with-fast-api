from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.users import create_new_user, get_user_by_email
from app.dependencies import get_db
from app.routers.utils.tags import Tags
from app.schemas.users import User, UserCreate

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
