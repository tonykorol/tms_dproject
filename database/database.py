from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    """
    Asynchronously provides an SQLAlchemy session.

    This function is used as a context manager to ensure that the
    session is properly closed after use.

    :return: An asynchronous SQLAlchemy session.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def get_async_api_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronously provides an SQLAlchemy session for API use.

    This function yields an SQLAlchemy session that can be used in
    API routes, ensuring proper session management.

    :yield: An asynchronous SQLAlchemy session.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_api_session)):
    """
    Provides an instance of SQLAlchemyUserDatabase for user management.

    This function uses dependency injection to provide a user database
    instance, which can be used for user-related operations.

    :param session: An asynchronous SQLAlchemy session (default is provided by get_async_api_session).

    :yield: An instance of SQLAlchemyUserDatabase configured with the provided session and User model.
    """
    from database.models import User
    yield SQLAlchemyUserDatabase(session, User)
