from datetime import datetime

from pydantic import BaseModel


class SiteSchema(BaseModel):
    id: int
    name: str
    url: str


class PricesSchema(BaseModel):
    id: int
    price: int
    price_date: datetime


class AllPricesSchema(BaseModel):
    prices: list[PricesSchema]


class ImagesSchema(BaseModel):
    id: int
    url: str


class CarModelSchema(BaseModel):
    id: int
    brand: str
    model: str
    generation: str


class PublicationSchema(BaseModel):
    id: int
    publication_id: int
    publication_date: datetime
    link: str
    description: str
    engine_type: str
    engine_hp: str
    engine_volume: str
    transmission_type: str
    car_drive: str
    mileage: str
    car_year: int
    is_active: bool
    site: SiteSchema
    prices: list[PricesSchema]
    images: list[ImagesSchema]
    car_model: CarModelSchema


class FavoriteSchema(BaseModel):
    id: int
    added_time: datetime
    publication: PublicationSchema


class AllPublicationsSchema(BaseModel):
    publications: list[PublicationSchema]


class AllFavoritesSchema(BaseModel):
    favorites: list[FavoriteSchema]


class TgTokenResponseSchema(BaseModel):
    token: str
    link: str
    message: str
