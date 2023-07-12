from sqlalchemy.orm import Session

from app.models.models import Section as SectionModel
from app.schemas.section import SectionCreate, SectionUpdate


def get_single_section(db: Session, section_id: int):
    section = (
        db.query(SectionModel).filter(SectionModel.section_id == section_id).first()
    )
    return section


def get_all_user_section(db: Session, user_id: int):
    user_sections = (
        db.query(SectionModel).filter(SectionModel.owner_id == user_id).all()
    )
    return user_sections


def create_section(
    db: Session, new_section: SectionCreate, user_id: int, project_id: int
):
    database_section = SectionModel(
        **new_section.dict(), owner_id=user_id, project_id=project_id
    )
    db.add(database_section)
    db.commit()
    db.refresh(database_section)
    return database_section


def delete_section(db: Session, section_id: int):
    deleted_section = (
        db.query(SectionModel).filter(SectionModel.section_id == section_id).first()
    )
    db.delete(deleted_section)
    db.commit()
    db.close()
    return deleted_section


def update_section(db: Session, update_section: SectionUpdate, in_section_id: int):
    in_section = get_single_section(db, in_section_id)
    updated_section = update_section.dict(exclude_unset=True)
    for key, item in updated_section.items():
        setattr(in_section, key, item)
    db.add(in_section)
    db.commit()
    db.refresh(in_section)
    return in_section
