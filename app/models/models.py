import datetime

from db.database import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


def get_time() -> datetime.datetime:
    return datetime.datetime.now()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_title = Column(String, index=True, nullable=False)
    task_description = Column(String, index=True)
    task_piority = Column(Integer, index=True)
    create_at = Column(Date, default=get_time)
    finished_at = Column(Date, default=get_time)
    is_completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="tasks")
