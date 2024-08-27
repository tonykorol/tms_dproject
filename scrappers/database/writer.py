from datetime import datetime, UTC

from sqlalchemy.orm import Session

from database.database import get_session
from database.models import Publication, Site, CarModel, PublicationPrice
from scrappers.awb_by.awb_scrapper import AbwParser


def write_to_database(data):
    session_generator = get_session()
    session = next(session_generator)
    try:
        for item in data:
            publication = session.query(Publication).filter_by(publication_id=item.get("id")).first()
            if publication is not None:
                upgrade_pub_data(publication, item, session)
                continue

            site_name = item.get("site_name")
            site = session.query(Site).filter_by(name=site_name).first()

            if not site:
                site = Site(name=site_name, url=item.get("site_url"))
                session.add(site)

            car_brand_name = item.get("car_model").get("brand")
            car_model_name = item.get("car_model").get("model")
            car_generation_name = item.get("car_model").get("generation")
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

            publication = Publication(
                publication_id=item.get("id"),
                publication_date=item.get("publication_date"),
                link=item.get("link"),
                images=item.get("images"),
                description=item.get("description"),
                engine_type=item.get("engine_type"),
                engine_hp=item.get("engine_hp"),
                engine_volume=item.get("engine_volume"),
                transmission_type=item.get("transmission_type"),
                car_drive=item.get("car_drive"),
                mileage=item.get("mileage"),
                car_year=item.get("car_year"),
                site=site,
                car_model=car_model,
            )
            session.add(publication)

            price = PublicationPrice(
                price=item.get("price"),
                price_date=item.get("publication_date"),
                publication=publication,
            )
            session.add(price)
            session.commit()
    finally:
        session_generator.close()


def upgrade_pub_data(publication: Publication, new_data: dict, session: Session):
    current_price = session.query(PublicationPrice).filter(PublicationPrice.publication_id == publication.id).order_by(PublicationPrice.price_date.desc()).first()
    exist_price = new_data.get("price")
    if current_price.price == exist_price:
        return
    price = PublicationPrice(
        price=new_data.get("price"),
        price_date=datetime.now(UTC),
        publication=publication,
    )
    session.add(price)
    session.commit()


if __name__ == "__main__":
    abw = AbwParser()
    abw_data = abw.get_data()
    write_to_database(abw_data)
