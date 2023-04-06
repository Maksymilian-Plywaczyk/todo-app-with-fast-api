from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.tasks import create_task
from app.crud.users import delete_user, get_user_by_id, get_user_list
from app.dependencies import get_current_user, get_db
from app.routers.utils.tags import Tags
from app.schemas.msg import Msg
from app.schemas.tasks import TaskCreate
from app.schemas.users import User

router = APIRouter()


@router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=User,
    tags=[Tags.users],
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/users",
    summary="Get all users in database",
    response_model=List[User],
    tags=[Tags.users],
)
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 0):
    return get_user_list(db=db, skip=skip, limit=limit)


@router.post(
    "/users/{user_id}/task",
    summary="Create new task for user",
    response_model=Msg,
    tags=[Tags.tasks],
)
def create_new_task(user_id: int, new_task: TaskCreate, db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    create_task(db=db, newTask=new_task, user_id=user_id)
    return {"message": "Task created successfully"}


@router.delete(
    "/delete_user/{user_id}",
    summary="Delete user from database",
    tags=[Tags.users],
    response_model=Msg,
)
def delete_specific_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = get_user_by_id(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found user to delete"
        )
    delete_user(db=db, user_id=deleted_user.user_id)
    return {"message": "User deleted successfully"}
