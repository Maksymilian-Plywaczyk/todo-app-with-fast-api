from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm import relationship
from db import database


class User(database.Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")
