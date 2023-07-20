from app.models.models import User
from app.tests.test_models.factories import TaskFactory, UserFactory


class TestUserModel:
    user = UserFactory.create()

    def test_user_model(self):
        assert self.user.user_id is not None
        assert isinstance(self.user, User)
        assert isinstance(self.user.full_name, str)
        assert isinstance(self.user.email, str)
        assert self.user.email is not None
        assert self.user.is_active is True

    def test_relationship_with_task(self):
        task = TaskFactory.create()
        assert task.user_id == self.user.user_id
        assert isinstance(task.owner, User)


class TestTaskModel:
    def test_task_model(self):
        task = TaskFactory()
        assert task.task_title is not None
        assert task.task_description is not None
        assert task.task_priority != 0
