from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from scrappers.data_classes import Publication as PublicationData
from database.models import Publication as PublicationModel, PublicationPrice, Site, CarModel, PublicationImage
from scrappers.notifications.sender import sender
from scrappers.notifications.tg.tg import update_user_tg_ids


async def save_publications(data: PublicationData) -> None:
    """
    Save publications to the database.

    This function updates user Telegram IDs, updates the status of
    existing publications, and saves new publications along with
    their associated data (images, prices, etc.) to the database.

    :param data: PublicationData object containing publication details.
    """
    async with get_async_session() as session:
        await update_user_tg_ids(session)
        await update_publications_status(data, session)
        for item in data:
            publication = await session.execute(
                select(PublicationModel).filter_by(publication_id=item.id)
            )
            publication = publication.unique().scalars().first()
            if publication is not None and not publication.is_active:
                await upgrade_pub_data(publication, item, session)
                continue
            site = await get_site(item, session)
            car_model = await get_car_model(item, session)
            new_publication = await add_publication(item, site, car_model, session)
            await save_images(item, new_publication, session)
            await save_price(new_publication, item, session)
        await session.commit()

async def update_publications_status(current_publications: PublicationData, session: AsyncSession) -> None:
    """
    Update the status of existing publications.

    This function marks publications as inactive if they are not
    present in the current set of publications.

    :param current_publications: CurrentPublicationData object containing active publications.
    :param session: Database session for executing queries.
    """
    existing_publications = await session.execute(select(PublicationModel))
    existing_publications = existing_publications.unique().scalars().all()
    current_ids: set = {pub.id for pub in current_publications}
    for pub in existing_publications:
        if pub.id not in current_ids:
            pub.is_active = False

async def get_site(item: PublicationData, session: AsyncSession) -> Site:
    """
    Retrieve or create a site based on the provided item.

    This function checks if a site with the given name exists in
    the database; if not, it creates a new Site instance.

    :param item: PublicationData object containing site details.
    :param session: Database session for executing queries.
    :return: Site instance.
    """
    site_name = item.site_name
    site = await session.execute(select(Site).filter_by(name=site_name))
    site = site.unique().scalars().first()
    if not site:
        site = Site(name=site_name, url=item.site_url)
        session.add(site)
    return site

async def get_car_model(item: PublicationData, session: AsyncSession) -> CarModel:
    """
    Retrieve or create a car model based on the provided item.

    This function checks if a car model with the specified brand,
    model, and generation exists in the database; if not, it creates
    a new CarModel instance.

    :param item: PublicationData object containing car model details.
    :param session: Database session for executing queries.
    :return: CarModel instance.
    """
    car_brand_name = item.car_model.brand
    car_model_name = item.car_model.model
    car_generation_name = item.car_model.generation
    car_model = await session.execute(select(CarModel).filter_by(
        brand=car_brand_name,
        model=car_model_name,
        generation=car_generation_name,
    ))
    car_model = car_model.unique().scalars().first()
    if not car_model:
        car_model = CarModel(
            brand=car_brand_name,
            model=car_model_name,
            generation=car_generation_name,
        )
        session.add(car_model)
    return car_model

async def add_publication(item: PublicationData, site: Site, car_model: CarModel, session: AsyncSession) -> PublicationModel:
    """
    Add a new publication to the database.
    This function creates a new PublicationModel instance and adds
    it to the database.

    :param item: PublicationData object containing publication details.
    :param site: Site instance associated with the publication.
    :param car_model: CarModel instance associated with the publication.
    :param session: Database session for executing queries.
    :return: The created PublicationModel instance.
    """
    publication = PublicationModel(
        publication_id=item.id,
        publication_date=item.publication_date,
        link=item.link,
        description=item.description,
        engine_type=item.engine_type,
        engine_hp=item.engine_hp,
        engine_volume=item.engine_volume,
        transmission_type=item.transmission_type,
        car_drive=item.car_drive,
        mileage=item.mileage,
        car_year=item.car_year,
        site=site,
        car_model=car_model,
    )
    session.add(publication)
    return publication

async def save_images(item: PublicationData, publication: PublicationModel, session: AsyncSession) -> None:
    """
    Save images associated with a publication.

    This function creates and adds PublicationImage instances for
    each image in the provided item.

    :param item: PublicationData object containing image URLs.
    :param publication: PublicationModel instance to associate images with.
    :param session: Database session for executing queries.
    """
    for img in item.images:
        image = PublicationImage(
            url=img,
            publication=publication
        )
        session.add(image)

async def save_price(publication: PublicationModel, item: PublicationData, session: AsyncSession) -> None:
    """
    Save the price associated with a publication.

    This function creates and adds a PublicationPrice instance
    based on the provided item's price information.

    :param publication: PublicationModel instance to associate price with.
    :param item: PublicationData object containing price details.
    :param session: Database session for executing queries.
    """
    price = PublicationPrice(
        price=item.price,
        price_date=item.publication_date,
        publication=publication,
    )
    session.add(price)

async def upgrade_pub_data(publication: PublicationModel, new_data: PublicationData, session: AsyncSession) -> None:
    """
    Updates the publication data and adds a new price if it has changed.

    :param publication: The publication model to be updated.
    :param new_data: New data for updating the publication, including the price.
    :param session: Asynchronous database session for executing operations.

    :return: None. The function modifies the publication state and adds a new price to the database
             if the price has changed.
    """
    current_price = await session.execute(select(PublicationPrice).filter(PublicationPrice.publication_id == publication.id).order_by(PublicationPrice.price_date.desc()))
    current_price = current_price.unique().scalars().first()
    exist_price = new_data.price
    publication.is_active = True
    session.add(publication)
    if current_price.price == exist_price:
        return
    price = PublicationPrice(
        price=new_data.price,
        price_date=datetime.now(UTC),
        publication=publication,
    )
    session.add(price)
    await sender(publication, price, session)
