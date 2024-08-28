from dataclasses import dataclass
from datetime import datetime


@dataclass
class CarModel:
    brand: str
    model: str
    generation: str


@dataclass
class Publication:
    id: int
    publication_date: datetime
    link: str
    images: list[str]
    description: str
    engine_type: str
    engine_hp: str
    engine_volume: str
    transmission_type: str
    car_drive: str
    mileage: str
    car_year: int
    car_body_type: str
    price: int
    car_model: CarModel
    site_name: str
    site_url: str


@dataclass
class PublicationOtherData:
    engine_type: str
    engine_hp: str
    engine_volume: str
    transmission_type: str
    drive: str
    mileage: str
    body_type: str


@dataclass
class PublicationTitleData:
    car_brand: str
    car_model: str
    car_model_generation: str
    car_year: str
