from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.models import Project as ProjectModel
from app.models.models import User
from app.schemas.project import Project, ProjectCreate, ProjectUpdate


def get_all_project_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProjectModel).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: int):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    return project


def create_project(db: Session, new_project: ProjectCreate, user_id: int):
    database_project = ProjectModel(**new_project.dict(), user_id=user_id)
    db.add(database_project)
    db.commit()
    db.refresh(database_project)
    return database_project


def delete_project(db: Session, project_id: int):
    project_to_delete = get_project_by_id(db=db, project_id=project_id)
    db.delete(project_to_delete)
    db.commit()
    db.refresh(project_to_delete)
    return project_to_delete


def update_existing_project(
    db: Session, project_update: ProjectUpdate, project_in: ProjectUpdate
):
    item_in_db = jsonable_encoder(project_in)
    updated_project = project_update.dict(exclude_unset=True)
    for field in item_in_db:
        if field in updated_project:
            setattr(project_in, field, updated_project[field])
    db.add(project_in)
    db.commit()
    db.refresh(project_in)
    return project_in


def show_collaborators(db: Session, project_id: int):
    collaborators = (
        db.query(User).join(Project).filter(Project.project_id == project_id).all()
    )
    return collaborators
