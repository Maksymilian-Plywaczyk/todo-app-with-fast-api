# TODO make a singup page
from fastapi import status, HTTPException, APIRouter, Depends
from schemas.users import User, UserCreate

from sqlalchemy.orm import Session
from crud.users import get_user_by_email, create_new_user
from dependencies import get_db
from routers.tags import Tags
router = APIRouter()


@router.post("/singup/", summary="Create new user", response_model=User,tags=[Tags.register])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    database_user = get_user_by_email(db=db, user_email=user.email)
    if database_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exist"
        )
    else:
        new_user = create_new_user(db=db, user=user)
    return new_user
