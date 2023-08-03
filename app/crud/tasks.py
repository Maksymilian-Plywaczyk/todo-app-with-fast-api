from fastapi.encoders import jsonable_encoder
from sqlalchemy import Integer, and_, cast
from sqlalchemy.orm import Session

from app.models.models import Task
from app.schemas.tasks import TaskCreate, TaskUpdate


# get list of tasks for selected user
def get_tasks_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()


# get task by task id
def get_task_by_id(db: Session, task_id: int):
    task = db.query(Task).filter(cast(Task.id, Integer) == task_id).first()
    return task


def get_active_task(db: Session, task_id: int):
    active_task = (
        db.query(Task)
        .filter(and_(Task.id == task_id, Task.is_completed is False))
        .first()
    )
    return active_task


def get_latest_task(db: Session, user_id: int):
    latest_task = (
        db.query(Task)
        .filter(and_(Task.user_id == user_id, Task.is_completed.is_(False)))
        .order_by(Task.id.desc())
        .first()
    )
    return latest_task


# Create new task for selected user
def create_task(
    db: Session, newTask: TaskCreate, user_id: int, project_id, section_id, url: str
):
    database_task = Task(
        **newTask.dict(),
        user_id=user_id,
        project_id=project_id,
        section_id=section_id,
        url=url
    )
    db.add(database_task)
    db.commit()
    db.refresh(database_task)
    return database_task


# Delete specific task for selected user
def delete_task(db: Session, task_id: int):
    deleted_task = db.query(Task).filter(cast(Task.id, Integer) == task_id).first()
    db.delete(deleted_task)
    db.commit()
    db.close()
    return deleted_task


def mark_task_as_completed(db: Session, task: TaskUpdate):
    task.is_completed = True
    db.commit()
    db.refresh(task)
    return True


# Update specific task for selected user
def update_task(db: Session, task_update: TaskUpdate, task_in: TaskUpdate):
    item_in_db = jsonable_encoder(task_in)
    updated_task = task_update.dict(exclude_unset=True)
    for field in item_in_db:
        if field in updated_task:
            setattr(task_in, field, updated_task[field])
    db.add(task_in)
    db.commit()
    db.refresh(task_in)
    return task_in
