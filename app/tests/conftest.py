import os

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.crud.users import create_new_user
from app.db.database import Base
from app.dependencies import get_db
from app.main import app
from app.schemas.users import UserCreate

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


@pytest.fixture(scope="session")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def override_get_db(db_session):
    yield db_session


@pytest.fixture(scope="session")
def client(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def new_user(db_session):
    create_new_user(
        db=db_session,
        user=UserCreate(
            full_name="Maks Pływaczyk",
            email="plywak12@gmail.com",
            password="haslo123",
            is_active=True,
        ),
    )
