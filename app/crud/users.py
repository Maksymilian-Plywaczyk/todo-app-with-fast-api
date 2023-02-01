import models.users
from core.security import get_hashed_password
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def get_user_by_email(db: Session, user_email: str):
    user_by_email = (
        db.query(models.users.User)
        .filter(models.users.User.email == user_email)
        .first()
    )
    return user_by_email


def get_user_by_id(db: Session, user_id: int):
    user_by_id = (
        db.query(models.users.User).filter(models.users.User.user_id == user_id).first()
    )

    return user_by_id


def get_user_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users.User).offset(skip).limit(limit).all()


def create_new_user(db: Session, user: UserCreate):
    hashed_password = get_hashed_password(plain_password=user.password)
    database_user = models.users.User(
        full_name=user.full_name, email=user.email, hashed_password=hashed_password
    )
    db.add(database_user)
    db.commit()
    db.refresh(database_user)
    return database_user


def delete_user(db: Session, user_email: str):
    deleted_user = (
        db.query(models.users.User)
        .filter(models.users.User.email == user_email)
        .first()
    )
    db.delete(deleted_user)
    db.commit()
    db.close()
    return deleted_user
