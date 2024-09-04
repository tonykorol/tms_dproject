import requests

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import TG_BOT_TOKEN
from database.models import PublicationPrice, User, Favorite
from database.models import Publication

async def sender(publication: Publication, price: PublicationPrice, session: AsyncSession):
    """
    Sends a notification about a price change in a publication to users who have favorited it.

    :param publication: The publication object containing details about the listing.
    :param price: The publication price object with the new price information.
    :param session: Asynchronous database session for executing operations.

    :return: None. The function sends notifications to users.
    """
    users = await get_users(publication, session)
    chat_ids = await get_chat_ids(users)
    message = await create_message(publication, price)
    for chat_id in chat_ids:
        await send_notification(chat_id, message)

async def get_users(publication: Publication, session: AsyncSession) -> list[User]:
    """
    Retrieves users who have favorited a specific publication.

    :param publication: The publication object to fetch users for.
    :param session: Asynchronous database session for executing operations.

    :return: A list of User objects who have favorited the publication.
    """
    result = await session.execute(select(User).join(Favorite.users).filter(Favorite.publication_id == publication.id))
    users = result.unique().scalars().all() # []
    return users


async def get_chat_ids(users: list[User]) -> list:
    """
    Extracts Telegram chat IDs from a list of users.

    :param users: A list of User objects to extract chat IDs from.

    :return: A list of Telegram chat IDs associated with the users.
    """
    chat_ids: list = []
    for user in users:
        chat_id = user.tg_chat_id
        if chat_id is not None:
            chat_ids.append(chat_id)
    return chat_ids


async def create_message(publication: Publication, price: PublicationPrice) -> str:
    """
    Creates a notification message about a price change for a publication.

    :param publication: The publication object containing details about the listing.
    :param price: The publication price object with the new price information.

    :return: A formatted string message indicating the price change.
    """
    message = f"""
    В объявлении изменилась цена!
На сайте {publication.site.name}
{publication.car_model.model} {publication.car_model.brand} {publication.car_model.generation} {publication.car_year}
Новая цена: {price.price} $USD
{publication.link}
"""
    return message


async def send_notification(chat_id: int, message: str):
    """
    Sends a notification message to a specific Telegram chat.

    :param chat_id: The Telegram chat ID to send the message to.
    :param message: The message content to be sent.

    :return: None. The function performs a network request to send the message.
    """
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
