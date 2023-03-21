from fastapi.encoders import jsonable_encoder
from models.models import Task
from schemas.tasks import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session


# get list of tasks for selected user
def get_tasks_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()


# get task by task id
def get_task_by_id(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    return task


# Create new task for selected user
def create_task(db: Session, newTask: TaskCreate, user_id: int):
    database_task = Task(**newTask.dict(), user_id=user_id)
    db.add(database_task)
    db.commit()
    db.refresh(database_task)
    return database_task


# Delete specific task for selected user
def delete_task(db: Session, task_id: int):
    deleted_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(deleted_task)
    db.commit()
    db.refresh(deleted_task)
    return deleted_task


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
