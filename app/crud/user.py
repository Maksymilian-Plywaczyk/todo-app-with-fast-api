from sqlalchemy.orm import Session
import models.user
from schemas.user import UserCreate
from core.security import get_hashed_password


def get_user_by_email(db: Session, user_email: str):
    user_by_email = db.query(models.user.User).filter(
        models.user.User.email == user_email).first()
    return user_by_email


def create_new_user(db: Session, user: UserCreate):
    hashed_password = get_hashed_password(plain_password=user.password)
    database_user = models.user.User(
        full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    db.add(database_user)
    db.commit()
    db.refresh(database_user)
    return database_user
