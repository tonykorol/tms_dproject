from datetime import datetime, UTC

from sqlalchemy.orm import Session

from database.database import get_session
from scrappers.data_classes import Publication as PublicationData
from database.models import Publication as PublicationModel, PublicationPrice, Site, CarModel


def save_publications(data: PublicationData):
    with get_session() as session:
        for item in data:
            publication = session.query(PublicationModel).filter_by(publication_id=item.id).first()
            if publication is not None:
                upgrade_pub_data(publication, item, session)
                continue
            site = get_site(item, session)
            car_model = get_car_model(item, session)
            new_publication = add_publication(item, site, car_model, session)
            save_price(new_publication, item, session)
            session.commit()

def get_site(item: PublicationData, session: Session) -> Site:
    site_name = item.site_name
    site = session.query(Site).filter_by(name=site_name).first()
    if not site:
        site = Site(name=site_name, url=item.site_url)
        session.add(site)
    return site

def get_car_model(item: PublicationData, session: Session) -> CarModel:
    car_brand_name = item.car_model.brand
    car_model_name = item.car_model.model
    car_generation_name = item.car_model.generation
    car_model = session.query(CarModel).filter_by(
        brand=car_brand_name,
        model=car_model_name,
        generation=car_generation_name,
    ).first()
    if not car_model:
        car_model = CarModel(
            brand=car_brand_name,
            model=car_model_name,
            generation=car_generation_name,
        )
        session.add(car_model)
    return car_model

def add_publication(item, site, car_model, session: Session) -> PublicationModel:
    publication = PublicationModel(
        publication_id=item.id,
        publication_date=item.publication_date,
        link=item.link,
        images=item.images,
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

def save_price(publication, item, session: Session):
    price = PublicationPrice(
        price=item.price,
        price_date=item.publication_date,
        publication=publication,
    )
    session.add(price)

def upgrade_pub_data(publication: PublicationModel, new_data: PublicationData, session: Session):
    current_price = session.query(PublicationPrice).filter(PublicationPrice.publication_id == publication.id).order_by(PublicationPrice.price_date.desc()).first()
    exist_price = new_data.price
    if current_price.price == exist_price:
        return
    price = PublicationPrice(
        price=new_data.price,
        price_date=datetime.now(UTC),
        publication=publication,
    )
    session.add(price)
