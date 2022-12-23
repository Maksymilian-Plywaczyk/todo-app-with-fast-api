from fastapi import APIRouter, Depends, HTTPException, status
from schemas.tasks import Task
from typing import List
from routers.tags import Tags
from sqlalchemy.orm import Session
from dependencies import get_db
from crud.users import get_user_by_email
from crud.tasks import get_tasks_list, delete_task, get_task_by_id

router = APIRouter()


# TODO make routers for task

@router.get("/tasks/{user_email}", summary="Get all tasks from current user", response_model=List[Task],
            tags=[Tags.tasks])
def read_user_tasks(user_email: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    user = get_user_by_email(db=db, user_email=user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return get_tasks_list(db=db, skip=skip, limit=limit)


@router.delete("/tasks/{task_id}", response_model=Task, summary="Delete user task by id", tags=[Tags.tasks])
def delete_user_task(task_id: int, db: Session = Depends(get_db)):
    if get_task_by_id(db=db, task_id=task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    deleted_task = delete_task(db=db, task_id=task_id)
    return deleted_task
