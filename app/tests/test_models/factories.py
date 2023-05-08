from random import randint

import factory

from app.models.models import Task, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    full_name = 'Test model'
    email = 'test@example.com'
    hashed_password = factory.Faker('password')
    is_active = True
    tasks = []


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    task_title = 'Test task'
    task_description = 'Test task description'
    task_priority = randint(1, 4)
    create_at = factory.Faker('date')
    finished_at = factory.Faker('date')
    is_completed = factory.Faker('boolean')
    user_id = 1

    owner = UserFactory()
