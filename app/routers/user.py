from fastapi import APIRouter, Depends
from dependencies import get_current_user
from schemas.user import User

router = APIRouter()


@router.get("/me", summary="Get details of currently logged in user", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
