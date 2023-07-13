from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.projects import (
    create_project,
    delete_project,
    get_all_project_list,
    get_project_by_id,
    show_collaborators,
    update_existing_project,
)
from app.crud.users import get_user_by_id
from app.dependencies import get_current_user, get_db
from app.routers.utils.prefixes import APIPrefixes
from app.routers.utils.tags import Tags
from app.schemas.collaborators import Collaborator
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.users import User

router = APIRouter(prefix=APIPrefixes.projects, tags=[Tags.projects])


@router.get(
    "/show_project",
    summary="Get project by id",
    status_code=status.HTTP_200_OK,
    response_model=Project,
)
def get_project(id: int = Query(..., gt=0), db: Session = Depends(get_db)) -> Project:
    current_project = get_project_by_id(db=db, project_id=id)
    if current_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return current_project


@router.get(
    "/show_all_projects",
    summary="Show all projects",
    status_code=status.HTTP_200_OK,
    response_model=List[Project],
)
def show_all_projects(
    skip: int, limit: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    user = get_user_by_id(db, user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot show projects from non existing user",
        )
    projects = get_all_project_list(db, skip, limit)
    return projects


@router.get(
    "/get_collaboators",
    summary="Show all collaborators",
    status_code=status.HTTP_200_OK,
    response_model=List[Collaborator],
)
def get_collaborators(
    project_id: int = Query(..., description="Project id", gt=0),
    db: Session = Depends(get_db),
):
    collaborators = show_collaborators(db, project_id)
    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            detail="Cannot show collaborators from non existing project",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if collaborators is None:
        raise HTTPException(
            detail="No collaborators found", status_code=status.HTTP_404_NOT_FOUND
        )
    return collaborators


@router.post(
    "/create_project",
    summary="Create new project",
    status_code=status.HTTP_201_CREATED,
    response_model=Project,
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


@router.put(
    "/update_project",
    summary="Update project",
    status_code=status.HTTP_200_OK,
    response_model=Project,
)
def update_project(
    db: Session = Depends(get_db),
    project_id: int = Query(..., description="ID of project to update", gt=0),
    project_update: ProjectUpdate = Body(..., description="Project data to update"),
):
    project_in = get_project_by_id(db, project_id)
    if project_in is None:
        raise HTTPException(
            detail="Cannot update non existing project",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    updated_project = update_existing_project(db, project_update, project_in)
    return updated_project


@router.delete(
    "/delete_project", summary="Delete project", status_code=status.HTTP_204_NO_CONTENT
)
def delete_project_by_id(
    project_id: int = Query(..., description="ID of project to delete", gt=0),
    db: Session = Depends(get_db),
):
    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            detail="Cannot delete non existing project",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    delete_project(db, project_id)
