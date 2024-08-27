from datetime import datetime, UTC
from typing import List

from sqlalchemy import Text, String, Integer, ARRAY, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))
    url: Mapped[str] = mapped_column(String(15))
    publications: Mapped[List["Publication"]] = relationship(back_populates="site")


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(Integer)
    publication_date: Mapped[datetime]
    link: Mapped[str] = mapped_column(String(75), unique=True)
    images: Mapped[list[str]] = mapped_column(ARRAY(String))
    description: Mapped[str] = mapped_column(Text)
    engine_type: Mapped[str] = mapped_column(String(50))
    engine_hp: Mapped[str] = mapped_column(String(10))
    engine_volume: Mapped[str] = mapped_column(String(10), nullable=True)
    transmission_type: Mapped[str] = mapped_column(String(10))
    car_drive: Mapped[str] = mapped_column(String(20))
    mileage: Mapped[str] = mapped_column(String(10))
    car_year: Mapped[int] = mapped_column(Integer)


    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    site: Mapped["Site"] = relationship(back_populates="publications")

    prices: Mapped[List["PublicationPrice"]] = relationship(back_populates="publication")

    car_model_id: Mapped[int] = mapped_column(ForeignKey("car_models.id"))
    car_model: Mapped[List["CarModel"]] = relationship(back_populates="publications")


class PublicationPrice(Base):
    __tablename__ = "publication_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(Integer)
    price_date: Mapped[datetime]

    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"))
    publication: Mapped["Publication"] = relationship(back_populates="prices")


class CarModel(Base):
    __tablename__ = "car_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(20))
    model: Mapped[str] = mapped_column(String(20))
    generation: Mapped[str] = mapped_column(String(25))

    publications: Mapped[List["Publication"]] = relationship(back_populates="car_model")

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="model")


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    added_time: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    car_model_id: Mapped[int] = mapped_column(ForeignKey("car_models.id"))
    model: Mapped["CarModel"] = relationship(back_populates="favorites")

    users: Mapped[list["User"]] = relationship(secondary="users_favorites", back_populates="favorites")


class UsersFavorites(Base):
    __tablename__ = "users_favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"), primary_key=True)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))\

    users: Mapped[List["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[List["Role"]] = relationship(back_populates="users")

    favorites: Mapped[list["Favorite"]] = relationship(secondary="users_favorites", back_populates="users")
