import os

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from models import users
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.dependencies import get_db
from app.main import app

load_dotenv(find_dotenv())

# TODO Configurate for database tests

engine = create_engine(
    os.getenv("SQLALCHEMY_DATABASE_TEST_URL"), connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
users.database.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    connection = engine.connect()
    #   transaction = connection.begin()

    # bind an individual Session to the connection
    db = TestingSessionLocal(bind=connection)
    # db = Session(db_engine)

    yield db

    db.rollback()
    connection.close()


#
@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
