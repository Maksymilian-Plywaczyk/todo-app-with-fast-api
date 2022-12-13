from sqlalchemy.orm import Session
import models.tasks
from schemas.tasks import TaskCreate, Task, TaskUpdate
from fastapi.encoders import jsonable_encoder


# get list of tasks for selected user
def get_tasks_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.tasks.Task).offset(skip).limit(limit).all()


# Create new task for selected user
def create_task(db: Session, newTask: TaskCreate, user_id: int):
    database_task = models.tasks.Task(**newTask.dict(), owner=user_id)
    db.add(database_task)
    db.commit()
    db.refresh(database_task)


# Delete specific task for selected user
def delete_task(db: Session, task_id: int):
    deleted_task = db.query(models.tasks.Task).filter(models.tasks.Task.id == task_id).first()
    db.delete(deleted_task)
    db.commit()
    db.refresh(deleted_task)


# Update specific task for selected user
def update_task(db: Session, task_update: TaskUpdate, task_in: Task, task_id: int):
    updated_task = jsonable_encoder(task_update)
    if isinstance(task_in, dict):
        update_task = task_in
    else:
        update_task = task_in.dict(exclude_unset=True)
    for field in updated_task:
        if field in update_task:
            setattr(task_update, field, update_task[field])
    db.add(task_update)
    db.commit()
    db.refresh(task_update)
