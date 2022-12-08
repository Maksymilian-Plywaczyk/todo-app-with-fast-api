from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_current_user, get_db
from schemas.users import User, UserCreate
from sqlalchemy.orm import Session
from crud.users import delete_user, get_user_by_email
router = APIRouter()


@router.get("/me", summary="Get details of currently logged in user", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/delete_user", summary="Delete user from database")
def delete_specific_user(user: UserCreate = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted_user = get_user_by_email(db=db, user_email=user.email)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found user to delete")
    else:
        deleted_user = delete_user(db=db, user_email=user.email)
    return {"User deleted": deleted_user}
