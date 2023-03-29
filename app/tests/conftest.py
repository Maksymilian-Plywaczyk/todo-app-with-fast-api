import os

import pytest
from db.database import Base
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.dependencies import get_db

load_dotenv(find_dotenv())

# TODO Configurate for database tests
SQLALCHEMY_DATABASE_TEST_URL = os.getenv("SQLALCHEMY_DATABASE_TEST_URL")


def create_test_tables(engine):
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_TEST_URL,
        connect_args={"check_same_thread": False},
    )

    create_test_tables(engine)

    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def override_get_db(db_session):
    yield db_session


@pytest.fixture(scope="function")
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
