from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.publications.schemas import PublicationSchema, PricesSchema
from database.models import Publication, PublicationPrice


async def get_publications(session: AsyncSession) -> list[PublicationSchema]:
    result = await session.execute(select(Publication).filter(Publication.is_active == True))
    publications = result.unique().scalars().all()
    if publications is None:
        raise HTTPException(status_code=404, detail="Publications not found")
    return publications

async def get_one_publication(pub_id: int, session: AsyncSession) -> PublicationSchema:
    publication = await session.execute(select(Publication).filter_by(id=pub_id))
    publication = publication.unique().scalars().first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

async def get_all_prices(pub_id:int, session: AsyncSession) -> list[PricesSchema]:
    result = await session.execute(
        select(Publication).filter(Publication.id == pub_id)
    )
    publication = result.scalars().first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    result = await session.execute(select(PublicationPrice).join(Publication).filter_by(id=pub_id))
    prices = result.unique().scalars().all()
    return prices
