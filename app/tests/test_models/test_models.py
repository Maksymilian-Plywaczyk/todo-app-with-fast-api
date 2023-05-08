from app.tests.test_models.factories import TaskFactory, UserFactory


class TestUserModel:
    def test_user_model(self):
        user = UserFactory()
        assert user.full_name == 'Test model'
        assert user.email == 'test@example.com'
        assert len(user.tasks) == 0


class TestTaskModel:
    def test_task_model(self):
        task = TaskFactory()
        assert task.task_title == 'Test task'
        assert task.task_description == 'Test task description'
        assert task.task_priority != 0
