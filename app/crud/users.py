from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import (
    get_hashed_password,
    oauth2_scheme,
    verify_password,
    verify_reset_password_token,
)
from app.models.models import User
from app.schemas.users import UserCreate


def get_user_by_email(db: Session, user_email: str):
    user_by_email = db.query(User).filter(User.email == user_email).first()
    return user_by_email


def get_user_by_id(db: Session, user_id: int):
    user_by_id = db.query(User).filter(User.user_id == user_id).first()

    return user_by_id


def get_user_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_new_user(db: Session, user: UserCreate):
    hashed_password = get_hashed_password(plain_password=user.password)
    database_user = User(
        full_name=user.full_name, email=user.email, hashed_password=hashed_password
    )
    db.add(database_user)
    db.commit()
    db.refresh(database_user)
    return database_user


def delete_user(db: Session, user_id: int):
    deleted_user = db.query(User).filter(User.user_id == user_id).first()
    db.delete(deleted_user)
    db.commit()
    db.close()
    return deleted_user


def user_is_active(user: User):
    return user.is_active


def user_authentication(db: Session, user_email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db=db, user_email=user_email)
    if not user:
        return None
    if not verify_password(password, hashed_password=user.hashed_password):
        return None
    return user
