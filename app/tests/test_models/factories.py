from random import randint

import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models.models import Base, Task, User

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.metadata.create_all(bind=engine)


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = SessionLocal

    user_id = factory.Sequence(lambda n: n)
    full_name = factory.Faker('name')
    email = factory.Faker('email')
    hashed_password = factory.Faker('password')
    is_active = True


class TaskFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Task
        sqlalchemy_session = SessionLocal

    id = factory.Sequence(lambda n: n)
    task_title = factory.Faker('sentence')
    task_description = factory.Faker('text')
    task_priority = randint(1, 4)
    create_at = factory.Faker('date')
    finished_at = factory.Faker('date')
    is_completed = factory.Faker('boolean')

    user_id = UserFactory.user_id
    owner = factory.SubFactory(UserFactory)
