from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATBASE_URL = os.getenv("SQLALCHEMY_DATBASE_URL")

# argument connect_args is needed only for SQLite databases.
engine = create_engine(url=SQLALCHEMY_DATBASE_URL,
                       connect_args={"check_same_thread": True})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
