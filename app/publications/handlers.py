from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.handlers import get_current_user
from app.publications.schemas import AllPublicationsSchema, PublicationSchema, AllPricesSchema, FavoriteSchema, \
    AllFavoritesSchema, TgTokenResponseSchema
from app.publications.services.favorites import add_to_fav, delete_favorite, get_favorites
from app.publications.services.publications import get_publications, get_one_publication, get_all_prices
from app.publications.services.tg import get_telegram_bot_token
from database.database import get_async_session
from database.models import User

router = APIRouter(prefix="/adverts", tags=["Adverts"])


@router.get("/", response_model=AllPublicationsSchema)
async def get_all_publications(session: AsyncSession = Depends(get_async_session)):
    """Get All Publications"""
    publications = await get_publications(session)
    return {"publications": publications}

@router.get("/favorites", tags=["Favorites"], response_model=AllFavoritesSchema)
async def get_all_favorites(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Get all Favorites from current User"""
    favorites = await get_favorites(user, session)
    return {"favorites": favorites}

@router.get("/favorites/token", tags=["Favorites"], response_model=TgTokenResponseSchema)
async def get_tg_token(
        user: User = Depends(get_current_user),
):
    """Get telegram connect token"""
    return await get_telegram_bot_token(user)

@router.get("/{pub_id}", response_model=PublicationSchema)
async def get_publication(pub_id: int, session: AsyncSession = Depends(get_async_session)):
    """Get Publications by id"""
    return await get_one_publication(pub_id, session)

@router.get("/{pub_id}/price", response_model=AllPricesSchema)
async def get_publication_prices(pub_id: int, session: AsyncSession = Depends(get_async_session)):
    """Get Publication prices by id"""
    prices = await get_all_prices(pub_id, session)
    return {"prices": prices}

@router.post("/{pub_id}/favorite", tags=["Favorites"], response_model=FavoriteSchema)
async def add_to_favorites(
        pub_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Add Publication to Favorites"""
    return await add_to_fav(pub_id, user, session)

@router.delete("/{pub_id}/favorite", tags=["Favorites"])
async def delete_from_favorites(
        pub_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Delete Publication from Favorites"""
    return await delete_favorite(pub_id, user, session)

