import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


def get_time() -> datetime.datetime:
    return datetime.datetime.now()


class User(Base):
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_title = Column(String, index=True, nullable=False)
    task_description = Column(String, index=True)
    task_piority = Column(Integer, index=True)
    create_at = Column(Date, default=get_time)
    finished_at = Column(Date, default=get_time)
    is_completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="tasks")
