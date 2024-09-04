from fastapi import APIRouter, Depends

from app.auth.auth import current_user
from app.auth.schemas import UserReadSchema
from database.models import User

router = APIRouter(prefix="/me")


@router.get("/", response_model=UserReadSchema)
def get_current_user(user: User = Depends(current_user)):
    """Get current user"""
    return user
