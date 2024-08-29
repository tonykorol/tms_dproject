from fastapi import FastAPI
from app.auth.handlers import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")
