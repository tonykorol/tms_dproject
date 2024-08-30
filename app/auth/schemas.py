from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, Field, EmailStr


class UserReadSchema(schemas.BaseUser[int], BaseModel):
    id: int
    username: str = Field(..., min_length=2, max_length=150)
    email: EmailStr = Field(..., max_length=320)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    # favorites: List[FavoritesSchema]


class UserCreateSchema(schemas.BaseUserCreate, BaseModel):
    username: str = Field(..., min_length=2, max_length=150)
    email: EmailStr = Field(..., max_length=320)
    password: str = Field(..., min_length=8, max_length=50)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdateSchema(schemas.BaseUserUpdate, BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
