from sqlalchemy.orm import Session
import models.tasks
from schemas.tasks import TaskCreate, Task, TaskUpdate
from fastapi.encoders import jsonable_encoder


# get list of tasks for selected user
def get_tasks_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.tasks.Task).offset(skip).limit(limit).all()


# get task by task id
def get_task_by_id(db: Session, task_id: int):
    task = db.query(models.tasks.Task).filter(models.tasks.Task.id == task_id).first()
    return task


# Create new task for selected user
def create_task(db: Session, newTask: TaskCreate, user_id: int):
    database_task = models.tasks.Task(**newTask.dict(), user_id=user_id)
    db.add(database_task)
    db.commit()
    db.refresh(database_task)
    return database_task


# Delete specific task for selected user
def delete_task(db: Session, task_id: int):
    deleted_task = db.query(models.tasks.Task).filter(models.tasks.Task.id == task_id).first()
    db.delete(deleted_task)
    db.commit()
    db.refresh(deleted_task)
    return deleted_task


# Update specific task for selected user
def update_task(db: Session, task_update: TaskUpdate, task_id: int):
    task_in = db.get(models.tasks.Task, task_id)
    updated_task = task_update.dict(exclude_unset=True)
    for key, value in updated_task.items():
        if key in update_task:
            setattr(task_in, key, value)
    db.add(task_update)
    db.commit()
    db.refresh(task_update)
    return task_in
