from datetime import date
from typing import Union

from pydantic import BaseModel, Field, HttpUrl


def get_time() -> date:
    return date.today()


# Shared properties to Task schemas
class BaseTask(BaseModel):
    task_title: str
    task_description: Union[str, None] = Field(
        default=None,
        description="Task description must be less than 300 characters.",
        max_length=300,
    )
    task_priority: Union[int, None] = Field(
        default=None, ge=0, le=4, description="Task priority choose 1-4"
    )
    create_at: Union[date, None] = Field(
        default=get_time(), description="Create time for task"
    )
    is_completed: bool = Field(default=False, description="Check if task is completed")
    url: Union[HttpUrl, None] = Field(description="Url for task")
    comment_count: int = Field(default=0, description="Count of comments")
    finished_at: Union[date, None] = None


class TaskUpdate(BaseTask):
    pass


class TaskCreate(BaseTask):
    pass


class Task(BaseTask):
    id: int
    user_id: int
    project_id: int
    section_id: int

    class Config:
        orm_mode = True
