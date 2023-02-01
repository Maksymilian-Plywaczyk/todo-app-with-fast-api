import datetime

from db import database
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


def get_time() -> datetime.datetime:
    return datetime.datetime.now()


class Task(database.Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_title = Column(String, index=True, nullable=False)
    task_description = Column(String, index=True)
    task_piority = Column(Integer, index=True)
    create_at = Column(Date, default=get_time)
    finished_at = Column(Date, default=get_time)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="tasks")
