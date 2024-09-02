from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.publications.schemas import FavoriteSchema
from database.models import User, Publication, Favorite


async def add_to_fav(pub_id: int, user: User, session: AsyncSession) -> Favorite:
    result = await session.execute(
        select(Publication).filter(Publication.id == pub_id)
    )
    publication = result.scalars().first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    existing_favorite = await session.execute(
        select(Favorite).join(Favorite.users)
        .filter(Favorite.publication_id == pub_id, User.id == user.id)
    )
    if existing_favorite.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Publication already in favorites")
    result = await session.execute(
        select(Publication).filter(Publication.id == pub_id)
    )
    publication = result.scalars().first()
    favorite = Favorite(
        publication_id=publication.id,
    )
    favorite.users.append(user)
    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)
    return favorite

async def delete_favorite(pub_id: int, user: User, session: AsyncSession) -> dict:
    result = await session.execute(
        select(Favorite).join(Favorite.users).filter(Favorite.publication_id == pub_id, User.id == user.id)
    )
    favorite = result.scalars().first()
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    await session.delete(favorite)
    await session.commit()
    return {"status": True}

async def get_favorites(user: User, session: AsyncSession) -> list[FavoriteSchema]:
    result = await session.execute(
        select(Favorite).join(Favorite.users).filter(User.id == user.id)
    )
    favorites = result.unique().scalars().all()
    return favorites
