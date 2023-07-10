from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.tasks import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks_list,
    mark_task_as_completed,
    update_task,
)
from app.crud.users import get_user_by_id
from app.dependencies import get_current_user, get_db
from app.routers.utils.tags import Tags
from app.schemas.msg import Msg
from app.schemas.tasks import Task, TaskCreate, TaskUpdate
from app.schemas.users import User

router = APIRouter(tags=[Tags.tasks])


# TODO make routers for task


@router.get(
    "/user/{user_id}/tasks/",
    summary="Get all tasks from current user",
    response_model=List[Task],
)
def read_user_tasks(
    user_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return get_tasks_list(db=db, skip=skip, limit=limit)


@router.get("/show_task/", summary="Get task by id", response_model=Task)
def read_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.post("/create_task", summary="Create new task for user", response_model=Msg)
def create_new_task(
    new_task: TaskCreate,
    project_id: int,
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    create_task(
        db=db,
        newTask=new_task,
        user_id=user_id,
        project_id=project_id,
        section_id=section_id,
    )
    return {"message": "Task created successfully"}


@router.delete(
    "/users/{user_id}/tasks/{task_id}",
    response_model=Msg,
    summary="Delete user task by id",
)
def delete_user_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if get_task_by_id(db=db, task_id=task_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    delete_task(db=db, task_id=task_id)
    return {"message": "Task deleted successfully"}


@router.put("/users/{user_id}/tasks/{task_id}", response_model=Msg)
def update_user_task(
    user_id: int,
    task_id: int,
    task_updated: TaskUpdate = Body(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db=db, user_id=user_id)
    task_to_update = get_task_by_id(db, task_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    elif task_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find task with this id",
        )
    try:
        task_in = get_task_by_id(db=db, task_id=task_id)
        update_task(db=db, task_update=task_updated, task_in=task_in)
    except Exception as e:
        raise e
    return {"message": "Task updated successfully"}


@router.put("/closed_task/{task_id}", response_model=Msg)
def close_completed_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    is_completed = mark_task_as_completed(db=db, task=task)
    return {"message": is_completed}
