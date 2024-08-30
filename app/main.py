from fastapi import FastAPI

from app.auth.auth import auth_backend, fastapi_users
from app.auth.handlers import router as auth_router
from app.auth.schemas import UserReadSchema, UserCreateSchema


app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
