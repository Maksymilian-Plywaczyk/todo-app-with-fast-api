import datetime

from pydantic import BaseModel, Field
from typing import Union
from datetime import date


def get_time() -> datetime.datetime:
    return datetime.datetime.now()


# Shared properties to Task schemas
class BaseTask(BaseModel):
    task_title: str
    description: Union[str, None] = Field(default=None,
                                          description="Task description must be less than 300 characters.",
                                          max_length=300)
    task_piority: Union[int, None] = Field(default=None, ge=0, le=4, description="Task piority choose 1-4")
    create_at: Union[date, None] = Field(default=get_time(), description="Create time for task")
    finished_at: Union[date, None] = None


class TaskUpdate(BaseTask):
    pass

# Properties to receive via API on update
class TaskCreate(BaseTask):
    pass


class Task(BaseTask):
    id: int
    user_id: int

    class Config:
        orm_mode = True
