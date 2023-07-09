import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


def get_time() -> datetime.datetime:
    return datetime.datetime.now()


class Project(Base):
    project_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=False, nullable=False)
    color_icon = Column(String, index=False, nullable=False)
    is_favorite = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    owner = relationship("User", back_populates="projects")


class User(Base):
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tasks = relationship("Task", back_populates="owner")
    projects = relationship("Project", back_populates="owner")
    sections = relationship("Section", back_populates="owner")


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_title = Column(String, index=True, nullable=False)
    task_description = Column(String, index=True)
    task_priority = Column(Integer, index=True)
    create_at = Column(Date, default=get_time)
    comment_count = Column(Integer, default=0)
    url = Column(String, index=True)
    finished_at = Column(Date, default=get_time)
    is_completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    project_id = Column(Integer, ForeignKey("project.project_id"))
    section_id = Column(Integer, ForeignKey("section.section_id"))
    owner = relationship("User", back_populates="tasks")


class Section(Base):
    section_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.project_id"))
    order = Column(Integer)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.user_id"))
    owner = relationship("User", back_populates="sections")
