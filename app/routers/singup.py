# TODO make a singup page
from fastapi import FastAPI, status, HTTPException, APIRouter
from app.schemas.user import User, UserCreate

from sqlalchemy.orm import Session
from core.security import get_hashed_password
from crud.user import get_user_by_email, create_new_user
from uuid import uuid4
router = APIRouter()


router.post("/singup/", summary="Create new user", response_model=User)


async def create_user(user: UserCreate, db: Session):
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
