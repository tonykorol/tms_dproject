from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.schemas import UserCreationSchema, UserSchema
from app.auth.services.users import create_user
from database.database import get_session

router = APIRouter(prefix="/auth", tags=["User authentication/registration"])

@router.post("/users", response_model=UserSchema)
def register_user(
        user: UserCreationSchema, session: Session = Depends(get_session)
):
    """Регистрация нового пользователя"""
    try:
        return create_user(user, session)
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=422, detail="User already exists")
