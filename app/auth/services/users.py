from sqlalchemy.orm import Session

from app.auth.schemas import UserCreationSchema
from app.auth.services.encrypt import encrypt_password
from database.models import User


def create_user(user: UserCreationSchema, session: Session) -> User:
    user_model = User(**user.model_dump())
    user_model.password = encrypt_password(user_model.password)
    session.add(user_model)
    session.commit()
    session.refresh(user_model)
    return user_model