from datetime import datetime, UTC
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Text, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))
    url: Mapped[str] = mapped_column(String(15))
    publications: Mapped[List["Publication"]] = relationship(back_populates="site", cascade="all, delete")


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(Integer)
    publication_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    link: Mapped[str] = mapped_column(String(75), unique=True)
    description: Mapped[str] = mapped_column(Text)
    engine_type: Mapped[str] = mapped_column(String(50))
    engine_hp: Mapped[str] = mapped_column(String(10))
    engine_volume: Mapped[str] = mapped_column(String(10), nullable=True)
    transmission_type: Mapped[str] = mapped_column(String(10))
    car_drive: Mapped[str] = mapped_column(String(20))
    mileage: Mapped[str] = mapped_column(String(10))
    car_year: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    site: Mapped["Site"] = relationship(back_populates="publications", lazy="joined")

    prices: Mapped[List["PublicationPrice"]] = relationship(
        back_populates="publication", lazy="joined", cascade="all, delete"
    )
    images: Mapped[List["PublicationImage"]] = relationship(
        back_populates="publication", lazy="joined", cascade="all, delete"
    )

    car_model_id: Mapped[int] = mapped_column(ForeignKey("car_models.id"))
    car_model: Mapped[List["CarModel"]] = relationship(back_populates="publications", lazy="joined")

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="publication", cascade="all, delete")


class PublicationPrice(Base):
    __tablename__ = "publication_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(Integer)
    price_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"))
    publication: Mapped["Publication"] = relationship(back_populates="prices", lazy="joined")


class PublicationImage(Base):
    __tablename__ = "publication_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)

    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"))
    publication: Mapped["Publication"] = relationship(back_populates="images", lazy="joined")


class CarModel(Base):
    __tablename__ = "car_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(20))
    model: Mapped[str] = mapped_column(String(20))
    generation: Mapped[str] = mapped_column(String(40))

    publications: Mapped[List["Publication"]] = relationship(back_populates="car_model", cascade="all, delete")


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    added_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"))
    publication: Mapped["Publication"] = relationship(back_populates="favorites", lazy="joined")

    users: Mapped[list["User"]] = relationship(secondary="users_favorites", back_populates="favorites", lazy="joined")


class UsersFavorites(Base):
    __tablename__ = "users_favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"), primary_key=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
    tg_chat_id: Mapped[int] = mapped_column(Integer, nullable=True)

    favorites: Mapped[list["Favorite"]] = relationship(
        secondary="users_favorites", back_populates="users", lazy="joined", cascade="all, delete"
    )
