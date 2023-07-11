from sqlalchemy.orm import Session

from app.models.models import Project as ProjectModel
from app.models.models import User
from app.schemas.collaborators import Collaborator, CollaboratorProperties
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_all_project_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProjectModel).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: int):
    project = (
        db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()
    )
    return project


def create_project(db: Session, new_project: ProjectCreate, user_id: int):
    database_project = ProjectModel(**new_project.dict(), user_id=user_id)
    db.add(database_project)
    db.commit()
    db.refresh(database_project)
    return database_project


def delete_project(db: Session, project_id: int):
    project_to_delete = (
        db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()
    )
    db.delete(project_to_delete)
    db.commit()
    db.close()
    return project_to_delete


def update_existing_project(
    db: Session, project_update: ProjectUpdate, project_in: ProjectUpdate
):
    updated_project = project_update.dict(exclude_unset=True)
    for key, item in updated_project.items():
        setattr(project_in, key, item)
    db.add(project_in)
    db.commit()
    db.refresh(project_in)
    return project_in


def show_collaborators(db: Session, project_id: int):
    users = (
        db.query(User)
        .join(ProjectModel)
        .filter(ProjectModel.project_id == project_id)
        .all()
    )
    collaborators = []
    for user in users:
        collaborators.append(
            Collaborator(
                collaborator=CollaboratorProperties(
                    id=user.user_id, name=user.full_name, email=user.email
                )
            )
        )
    return collaborators
