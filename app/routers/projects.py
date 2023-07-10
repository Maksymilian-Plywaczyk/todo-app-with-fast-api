from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.projects import create_project, get_project_by_id
from app.crud.users import get_user_by_id
from app.dependencies import get_current_user, get_db
from app.routers.utils.tags import Tags
from app.schemas.project import Project, ProjectCreate
from app.schemas.users import User

router = APIRouter(tags=[Tags.projects])


@router.get(
    "/project/{project_id}", summary="Get project by id", status_code=status.HTTP_200_OK
)
def get_project(project_id: int, db: Session = Depends(get_db)) -> Project:
    current_project = get_project_by_id(db=db, project_id=project_id)
    if current_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return current_project


@router.post(
    "/create_project", summary="Create new project", status_code=status.HTTP_201_CREATED
)
def create_new_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logged_user_id = current_user.user_id
    if get_user_by_id(db=db, user_id=logged_user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot create new project for non existing user",
        )
    new_project = create_project(db=db, new_project=project, user_id=logged_user_id)
    return new_project
