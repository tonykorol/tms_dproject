from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.publications.schemas import PublicationSchema, PricesSchema
from database.models import Publication, PublicationPrice


async def get_publications(session: AsyncSession) -> list[PublicationSchema]:
    """
    Retrieves a list of active publications.

    :param session: The asynchronous database session.

    :return: A list of PublicationSchema objects representing active publications.

    :raises HTTPException: If no active publications are found (404).
    """
    result = await session.execute(select(Publication).filter(Publication.is_active == True))
    publications = result.unique().scalars().all()
    if publications is None:
        raise HTTPException(status_code=404, detail="Publications not found")
    return publications

async def get_one_publication(pub_id: int, session: AsyncSession) -> PublicationSchema:
    """
    Retrieves a single publication by its ID.

    :param pub_id: The ID of the publication to retrieve.
    :param session: The asynchronous database session.

    :return: A PublicationSchema object representing the requested publication.

    :raises HTTPException: If the publication is not found (404).
    """
    publication = await session.execute(select(Publication).filter_by(id=pub_id))
    publication = publication.unique().scalars().first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

async def get_all_prices(pub_id:int, session: AsyncSession) -> list[PricesSchema]:
    """
    Retrieves all prices associated with a specific publication.

    :param pub_id: The ID of the publication for which to retrieve prices.
    :param session: The asynchronous database session.

    :return: A list of PricesSchema objects representing the prices for the specified publication.

    :raises HTTPException: If the publication is not found (404).
    """
    result = await session.execute(
        select(Publication).filter(Publication.id == pub_id)
    )
    publication = result.scalars().first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    result = await session.execute(select(PublicationPrice).join(Publication).filter_by(id=pub_id))
    prices = result.unique().scalars().all()
    return prices
