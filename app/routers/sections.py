from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.sections import create_section, get_all_user_section, get_single_section
from app.crud.users import get_user_by_id
from app.dependencies import get_current_user, get_db
from app.routers.utils.prefixes import APIPrefixes
from app.routers.utils.tags import Tags
from app.schemas.section import Section, SectionCreate
from app.schemas.users import User

router = APIRouter(prefix=APIPrefixes.sections, tags=[Tags.sections])


@router.get(
    "/get_single_section",
    summary="Get single section",
    response_model=Section,
    status_code=status.HTTP_200_OK,
)
def show_single_section(
    section_id: int = Query(..., gt=0), db: Session = Depends(get_db)
):
    section = get_single_section(db, section_id)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section not found"
        )
    return section


@router.get(
    "/get_all_user_sections",
    summary="Get all user sections",
    response_model=List[Section],
    status_code=status.HTTP_200_OK,
)
def show_all_user_sections(user: User = Depends(get_current_user), db=Depends(get_db)):
    user_id = user.user_id
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot show sections from non existing user",
        )
    sections = get_all_user_section(db, user_id)
    return sections


@router.post(
    "/create_section",
    summary="Create section",
    response_model=Section,
    status_code=status.HTTP_201_CREATED,
)
def create_new_section(
    section: SectionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    project_id: int = Query(..., gt=0),
):
    user_id = user.user_id
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot create section from non existing user",
        )
    new_section = create_section(
        db=db, new_section=section, user_id=user_id, project_id=project_id
    )
    return new_section


# TODO create a new router for update existing section
