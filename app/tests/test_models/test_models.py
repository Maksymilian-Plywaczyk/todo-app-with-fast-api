from app.models.models import Project, Section, Task, User
from app.tests.test_models.factories import (
    ProjectFactory,
    SectionFactory,
    TaskFactory,
    UserFactory,
)


class TestUserModel:
    user = UserFactory.create()

    def test_user_model(self):
        assert self.user.user_id is not None
        assert isinstance(self.user, User)
        assert isinstance(self.user.full_name, str)
        assert isinstance(self.user.email, str)
        assert self.user.email is not None
        assert self.user.is_active is True

    def test_relationship_with_project(self):
        project = TestProjectModel.project
        assert project.user_id == self.user.user_id
        for prj in self.user.projects:
            assert isinstance(prj, Project)


class TestProjectModel:
    project = ProjectFactory()

    def test_project_model(self):
        assert self.project.project_id is not None
        assert self.project.name is not None
        assert self.project.color_icon is not None
        assert self.project.is_favorite is not None
        assert self.project.user_id is not None
        assert isinstance(self.project.owner, User)

    def test_relationship_with_user(self):
        user = TestUserModel.user
        assert self.project.user_id == user.user_id
        assert isinstance(self.project.owner, User)

    def test_relationship_with_section(self):
        section = TestSectionModel.section
        assert self.project.project_id == section.project_id
        assert isinstance(self.project.sections, list)
        for sec in self.project.sections:
            assert isinstance(sec, Section)


class TestSectionModel:
    section = SectionFactory()

    def test_section_model(self):
        assert self.section.section_id is not None
        assert self.section.project_id is not None
        assert self.section.order is not None
        assert self.section.name is not None
        assert self.section.owner_id is not None

    def test_relationship_with_project(self):
        project = TestProjectModel.project
        assert self.section.project_id == project.project_id
        assert isinstance(self.section.project, Project)

    def test_relationship_with_task(self):
        task = TestTaskModel.task
        assert self.section.section_id == task.section_id
        assert isinstance(self.section.tasks, list)
        for tsk in self.section.tasks:
            assert isinstance(tsk, Task)


class TestTaskModel:
    task = TaskFactory()

    def test_task_model(self):
        assert self.task.task_title is not None
        assert self.task.task_description is not None
        assert self.task.task_priority != 0

    def test_relationship_with_section(self):
        section = TestSectionModel.section
        assert self.task.section_id == section.section_id
        assert isinstance(self.task.section, Section)
