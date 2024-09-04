from fastapi import FastAPI

from app.publications.handlers import router as adverts_router
from app.auth.auth import auth_backend, fastapi_users
from app.auth.handlers import router as auth_router
from app.auth.schemas import UserReadSchema, UserCreateSchema


app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/v1/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
    prefix="/api/v1/auth",
    tags=["auth"],
)


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(adverts_router, prefix="/api/v1")
