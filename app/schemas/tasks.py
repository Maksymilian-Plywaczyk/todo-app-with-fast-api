from pydantic import BaseModel
from typing import Union
from datetime import date


# Shared properties to Task schemas
class BaseTask(BaseModel):
    task_title: str
    description: Union[str, None] = None
    task_piority: Union[int, None] = None
    create_at: Union[date, None] = None
    finished_at: Union[date, None] = None

# Properties to receive via API on update
class TaskCreate(BaseTask):
    pass


class Task(BaseTask):
    id: int
    user_id: int

    class Config:
        orm_mode = True
