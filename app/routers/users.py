from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_current_user, get_db
from schemas.users import User, UserCreate
from sqlalchemy.orm import Session
from crud.users import delete_user, get_user_by_email, get_user_list
from typing import List
from schemas.tasks import Task, TaskCreate
from crud.tasks import create_task
from routers.tags import Tags

router = APIRouter()


@router.get("/me", summary="Get details of currently logged in user", response_model=User, tags=[Tags.users])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", summary="Get all users in database", response_model=List[User], tags=[Tags.users])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 0):
    return get_user_list(db=db, skip=skip, limit=limit)


@router.post("/users/{user_id}/task", summary="Create new task for user", response_model=Task, tags=[Tags.tasks])
def create_new_task(user_id: int, new_task: TaskCreate, db: Session = Depends(get_db)):
    task = create_task(db=db, newTask=new_task, user_id=user_id)
    return task


@router.delete("/delete_user", summary="Delete user from database", tags=[Tags.users])
def delete_specific_user(user: UserCreate = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted_user = get_user_by_email(db=db, user_email=user.email)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found user to delete")
    else:
        deleted_user = delete_user(db=db, user_email=user.email)
    return {"User deleted": deleted_user}
