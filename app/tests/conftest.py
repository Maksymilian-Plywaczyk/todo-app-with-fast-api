import os

import pytest
from db.database import Base
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from models import users
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.dependencies import get_db
from app.main import app

load_dotenv(find_dotenv())

# TODO Configurate for database tests
SQLALCHEMY_DATABASE_TEST_URL = os.getenv("SQLALCHEMY_DATABASE_TEST_URL")


# create database with new engine


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_TEST_URL, connect_args={"check_same_thread": False}
    )
    if not database_exists:
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def override_get_db(db_engine):
    connection = db_engine.connect()

    transaction = connection.begin()

    db = Session(bind=connection)

    yield db
    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    with TestClient(app) as c:
        yield c
