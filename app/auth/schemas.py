from pydantic import BaseModel, Field, EmailStr

from database.models import Role


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    email: EmailStr =Field(..., max_length=254)


class UserCreationSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=50)


class RoleSchema(BaseModel):
    name: str


class UserSchema(UserBaseSchema):
    id: int
    role: RoleSchema
    # favorites: List[FavoritesSchema]
