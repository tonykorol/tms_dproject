import requests

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import TG_BOT_TOKEN
from database.models import PublicationPrice, User, Favorite
from database.models import Publication

async def sender(publication: Publication, price: PublicationPrice, session: AsyncSession):
    users = await get_users(publication, session)
    chat_ids = await get_chat_ids(users, session)
    message = await create_message(publication, price)
    for chat_id in chat_ids:
        await send_notification(chat_id, message)

async def get_users(publication: Publication, session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).join(Favorite.users).filter(Favorite.publication_id == publication.id))
    users = result.unique().scalars().all() # []
    return users


async def get_chat_ids(users: list[User], session: AsyncSession) -> list:
    chat_ids: list = []
    for user in users:
        chat_id = user.tg_chat_id
        if chat_id is not None:
            chat_ids.append(chat_id)
    return chat_ids


async def create_message(publication: Publication, price: PublicationPrice) -> str:
    message = f"""
    В объявлении изменилась цена!
На сайте {publication.site.name}
{publication.car_model.model} {publication.car_model.brand} {publication.car_model.generation} {publication.car_year}
Новая цена: {price.price} $USD
{publication.link}
"""
    return message


async def send_notification(chat_id: int, message: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
