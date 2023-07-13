from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.users import delete_user, get_user_by_id, get_user_list
from app.dependencies import get_current_user, get_db
from app.routers.utils.prefixes import APIPrefixes
from app.routers.utils.tags import Tags
from app.schemas.users import User

router = APIRouter(prefix=APIPrefixes.users, tags=[Tags.users])


@router.get("/me", summary="Get details of currently user", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", summary="Get all users in database", response_model=List[User])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 0):
    return get_user_list(db=db, skip=skip, limit=limit)


@router.delete(
    "/delete_user/{user_id}", summary="Delete user from database", tags=[Tags.users]
)
def delete_specific_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = get_user_by_id(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found user to delete"
        )
    delete_user(db=db, user_id=deleted_user.user_id)
    return {"message": "User deleted successfully"}
